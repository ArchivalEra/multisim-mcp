#!/usr/bin/env python3
"""文字压线检查（带文字内容版）。

对每张图跑两次渲染（完整 / 仅文字），用 matplotlib 自己报告的每个 Text
的窗口包围盒去查：该文字框内是否存在"完整图有墨、仅文字图无墨"的像素。
报告里直接给文字内容，便于定位。

用法：/tmp/figvenv/bin/python collide3.py --all
      /tmp/figvenv/bin/python collide3.py ge02.py
退出码：0 无压线；1 有压线。
"""
from __future__ import annotations
import runpy, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import Text

PAD_SHRINK = 2   # 文字框内缩像素


def grab_figures(path: Path):
    figs = []
    orig = matplotlib.figure.Figure.savefig
    def savefig(self, *a, **k):
        if self not in figs:
            figs.append(self)
        return orig(self, *a, **k)
    matplotlib.figure.Figure.savefig = savefig
    old_close = plt.close
    plt.close = lambda *a, **k: None
    try:
        runpy.run_path(str(path), run_name="__main__")
        if not figs:
            for n in plt.get_fignums():
                figs.append(plt.figure(n))
    finally:
        matplotlib.figure.Figure.savefig = orig
        plt.close = old_close
    return figs


def render(fig, text_only: bool) -> np.ndarray:
    saved = []
    if text_only:
        for ax in fig.axes:
            for attr in ("lines", "patches", "collections", "images"):
                for a in list(getattr(ax, attr, []) or []):
                    saved.append((a, a.get_visible()))
                    a.set_visible(False)
            for sp in ax.spines.values():
                saved.append((sp, sp.get_visible()))
                sp.set_visible(False)
            for axis in (ax.xaxis, ax.yaxis):
                saved.append((axis, axis.get_visible()))
                axis.set_visible(False)
    fig.canvas.draw()
    arr = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].mean(axis=2)
    for a, v in saved:
        try:
            a.set_visible(v)
        except Exception:
            pass
    return arr


def text_bboxes(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    out = []
    for ax in fig.axes:
        # 只查图内标注文字；轴名与刻度按设计贴轴，排除
        cands = list(ax.texts)
        for t in cands:
            if not isinstance(t, Text):
                continue
            s = (t.get_text() or "").strip()
            if not s:
                continue
            try:
                bb = t.get_window_extent(r)
            except Exception:
                continue
            if bb.width < 3 or bb.height < 3:
                continue
            out.append((s, bb))
    return out


def check(path: Path):
    problems = []
    for fig in grab_figures(path):
        H = None
        full = render(fig, text_only=False)
        txt = render(fig, text_only=True)
        H, W = full.shape
        for s, bb in text_bboxes(fig):
            # matplotlib 窗口坐标原点在左下，图像数组原点在左上
            x0 = int(max(0, bb.x0 + PAD_SHRINK))
            x1 = int(min(W - 1, bb.x1 - PAD_SHRINK))
            y0 = int(max(0, H - bb.y1 + PAD_SHRINK))
            y1 = int(min(H - 1, H - bb.y0 - PAD_SHRINK))
            if x1 <= x0 or y1 <= y0:
                continue
            wt = txt[y0:y1 + 1, x0:x1 + 1]
            wf = full[y0:y1 + 1, x0:x1 + 1]
            # 只在"文字图里是白、完整图里变深"的位置计数
            became = int(((wt > 235) & (wf < 215)).sum())
            if became >= 12:
                problems.append((s, became))
    return problems


def main(argv):
    args = argv[1:]
    here = Path(__file__).resolve().parent
    scripts = sorted(here.glob("ge[0-9][0-9].py")) if "--all" in args else [
        Path(a) if Path(a).is_absolute() else here / a for a in args]
    scripts = [p for p in scripts if p.is_file()]
    if not scripts:
        print(__doc__.strip()); return 2
    total = 0
    for p in scripts:
        try:
            probs = check(p)
        except Exception as e:
            print(f"{p.name}: ERROR {type(e).__name__}: {e}"); total += 1; continue
        print(f"{p.name}: {len(probs)} text(s) crossed")
        for s, n in probs:
            print(f"    [{n} px] {s[:60]}")
        total += len(probs)
    print(f"summary scripts={len(scripts)} crossed_texts={total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
