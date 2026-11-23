#!/usr/bin/env python3
"""像素级文字-线条碰撞检查。

做法：运行脚本得到 Figure，把 figure 分两次渲染：
  A. 完整图
  B. 只渲染文字（其它 artist 全隐藏）
在 B 里测到每块文字的连通域包围盒，回 A 里看该包围盒内部是否出现
"明显不是字形"的深色像素（即被线条穿过）。纯像素判据，不依赖 transform。

用法：
    /tmp/figvenv/bin/python collide2.py ge01.py ...
    /tmp/figvenv/bin/python collide2.py --all
退出码：0 无碰撞；1 有碰撞。
"""
from __future__ import annotations
import runpy, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def render(fig, text_only: bool) -> np.ndarray:
    """渲染成灰度数组。text_only=True 时只保留文字。"""
    saved = []
    if text_only:
        for ax in fig.axes:
            for attr in ("lines", "patches", "collections", "images"):
                lst = getattr(ax, attr, None)
                if lst is None:
                    continue
                for a in list(lst):
                    saved.append((a, a.get_visible()))
                    a.set_visible(False)
            for attr in ("spines",):
                for k, sp in getattr(ax, attr).items():
                    saved.append((sp, sp.get_visible()))
                    sp.set_visible(False)
            saved.append((ax.xaxis, ax.xaxis.get_visible()))
            ax.xaxis.set_visible(False)
            saved.append((ax.yaxis, ax.yaxis.get_visible()))
            ax.yaxis.set_visible(False)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    for a, v in saved:
        try:
            a.set_visible(v)
        except Exception:
            pass
    return buf.mean(axis=2)

def label_boxes_from_text_only(gray: np.ndarray):
    """只含文字的图里，按连通域求每块文字的包围盒。"""
    mask = gray < 200
    H, W = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    boxes = []
    from collections import deque
    for y in range(0, H):
        row = np.where(mask[y] & ~seen[y])[0]
        for x in row:
            if seen[y, x]:
                continue
            q = deque([(y, x)])
            seen[y, x] = True
            y0 = y1 = y; x0 = x1 = x
            n = 0
            while q:
                cy, cx = q.popleft(); n += 1
                if cy < y0: y0 = cy
                if cy > y1: y1 = cy
                if cx < x0: x0 = cx
                if cx > x1: x1 = cx
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            q.append((ny, nx))
            w, h = x1 - x0, y1 - y0
            if n >= 25 and w <= 420 and h <= 110:  # 过滤噪点与多块粘连
                boxes.append((x0, y0, x1, y1, n))
    return boxes

def check(path: Path):
    figs = []
    orig = matplotlib.figure.Figure.savefig
    def savefig(self, *a, **k):
        if self not in figs: figs.append(self)
        return orig(self, *a, **k)
    matplotlib.figure.Figure.savefig = savefig
    plt.close = lambda *a, **k: None
    try:
        runpy.run_path(str(path), run_name="__main__")
        if not figs:
            for n in plt.get_fignums(): figs.append(plt.figure(n))
    finally:
        matplotlib.figure.Figure.savefig = orig; plt.close = orig and plt.close
    probs = []
    for fig in figs:
        full = render(fig, text_only=False)
        txt  = render(fig, text_only=True)
        boxes = label_boxes_from_text_only(txt)
        # 文字块内：把"完整图的像素"与"只有文字的像素"逐像素比。
        # 文字轮廓位置两者相同；线条穿过来会在文字块内多出非字形像素，
        # 且该像素在 text-only 图里不是字形（灰色为 255）。
        # 判据与颜色无关：只看该点是否有墨。
        for (x0, y0, x1, y1, n) in boxes:
            y0i, y1i, x0i, x1i = y0 + 2, y1 - 2, x0 + 2, x1 - 2
            if y1i <= y0i or x1i <= x0i:
                continue
            wt = txt[y0i:y1i + 1, x0i:x1i + 1]
            wf = full[y0i:y1i + 1, x0i:x1i + 1]
            ink_t = wt < 200
            ink_f = wf < 200
            # 文字块内，完整图有墨但文字图无墨的位置 = 线条穿过（含同色覆盖的情况：
            # 同色覆盖会改变灰度值，用差值阈值判定）
            extra_ink = ink_f & ~ink_t
            # 同色覆盖：文字图里该位置原本是白（255），完整图里变深了
            became_dark = (wt > 240) & (wf < 220)
            hit = int(extra_ink.sum() + became_dark.sum())
            if hit >= 15:
                probs.append(f"label bbox ({x0},{y0})-({x1},{y1}) line_pixels={hit}")
    return probs

def main(argv):
    args = argv[1:]
    here = Path(__file__).resolve().parent
    scripts = sorted(here.glob("ge*.py")) if "--all" in args else [Path(a) if Path(a).is_absolute() else here/a for a in args]
    scripts = [p for p in scripts if p.is_file()]
    if not scripts:
        print(__doc__.strip()); return 2
    total = 0
    for p in scripts:
        try:
            probs = check(p)
        except Exception as e:
            print(f"collide2 {p.name}: ERROR {type(e).__name__}: {e}"); total += 1; continue
        print(f"collide2 {p.name}: {len(probs)} suspect(s)")
        for x in probs[:8]: print("   ", x)
        total += len(probs)
    print(f"collide2_summary scripts={len(scripts)} suspects={total}")
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
