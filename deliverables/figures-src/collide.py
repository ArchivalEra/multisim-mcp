#!/usr/bin/env python3
"""文字-线条碰撞检查：机器判据，替代肉眼看图。

原理：运行 geNN.py 拿到 matplotlib Figure，取出所有 Text 的渲染包围盒，
再取出所有线条（Line2D、箭头、patches path）在显示坐标下的线段，
逐段判断是否穿过文字包围盒内部（先内缩几像素，避免边界相接误报）。

用法：
    /tmp/figvenv/bin/python collide.py ge01.py ge02.py ...
    /tmp/figvenv/bin/python collide.py --all        # 检查目录下所有 ge*.py

退出码：0 无碰撞；1 有碰撞。
"""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PathCollection  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Patch  # noqa: E402
from matplotlib.text import Text  # noqa: E402

SHRINK = 3.0  # 包围盒内缩像素，避免文字边缘与线相接误报


def text_boxes(fig):
    """所有可读文字 → (文字内容, 显示坐标 bbox)。"""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    out = []
    for ax in fig.axes:
        for art in list(ax.texts) + [ax.title, ax.xaxis.label, ax.yaxis.label]:
            if not isinstance(art, Text):
                continue
            s = (art.get_text() or "").strip()
            if not s:
                continue
            try:
                bb = art.get_window_extent(renderer)
            except Exception:
                continue
            if bb.width <= 1 or bb.height <= 1:
                continue
            out.append((s, bb))
    return out


def display_segments(fig):
    """所有线条 → 显示坐标线段列表 [(x0,y0,x1,y1)]。"""
    segs = []
    for ax in fig.axes:
        # 数据线（跳过作为 grid 的线与不可见线）
        for ln in ax.lines:
            if not ln.get_visible():
                continue
            if ln.get_linestyle() in ("None", "none", "", None):
                continue
            if not isinstance(ln, Line2D):
                continue
            try:
                xy = ln.get_transform().transform(np.column_stack(ln.get_data()))
            except Exception:
                continue
            if xy is None or len(xy) < 2:
                continue
            for i in range(len(xy) - 1):
                segs.append((xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1]))
        # patch（箭头、矩形、三角形等）
        for p in ax.patches:
            if not p.get_visible():
                continue
            if isinstance(p, FancyArrowPatch):
                try:
                    verts = p.get_path().vertices
                    xy = p.get_transform().transform(verts)
                    for i in range(len(xy) - 1):
                        if not np.all(np.isfinite(xy[i])):
                            continue
                        segs.append((xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1]))
                except Exception:
                    pass
            elif isinstance(p, Patch):
                try:
                    xy = p.get_transform().transform(p.get_path().vertices)
                    for i in range(len(xy) - 1):
                        if not np.all(np.isfinite(xy[i])):
                            continue
                        segs.append((xy[i][0], xy[i][1], xy[i + 1][0], xy[i + 1][1]))
                except Exception:
                    pass
        # 散点等 collection 略过（不会压字）
    return segs


def seg_hits_box(seg, bb):
    """线段是否穿过内缩后的文字包围盒。"""
    x0, y0, x1, y1 = seg
    xmin, xmax = bb.x0 + SHRINK, bb.x1 - SHRINK
    ymin, ymax = bb.y0 + SHRINK, bb.y1 - SHRINK
    if xmax <= xmin or ymax <= ymin:
        return False
    # 线段与轴对齐矩形求交
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return False
                if r > t0:
                    t0 = r
            else:
                if r < t0:
                    return False
                if r < t1:
                    t1 = r
    return t0 <= t1


def check_script(path: Path) -> list[str]:
    """运行脚本，返回碰撞描述列表。"""
    figs = []
    orig_savefig = matplotlib.figure.Figure.savefig
    orig_close = plt.close

    def savefig(self, *a, **k):
        if self not in figs:
            figs.append(self)
        return orig_savefig(self, *a, **k)

    matplotlib.figure.Figure.savefig = savefig
    plt.close = lambda *a, **k: None
    try:
        runpy.run_path(str(path), run_name="__main__")
        if not figs:
            for num in plt.get_fignums():
                figs.append(plt.figure(num))
    finally:
        matplotlib.figure.Figure.savefig = orig_savefig
        plt.close = orig_close

    problems = []
    for fig in figs:
        boxes = text_boxes(fig)
        segs = display_segments(fig)
        hits = {}
        for s, bb in boxes:
            for seg in segs:
                if seg_hits_box(seg, bb):
                    hits.setdefault(s, 0)
                    hits[s] += 1
        for s, n in hits.items():
            problems.append(f"text '{s}' crossed by {n} line segment(s)")
    return problems


def main(argv: list[str]) -> int:
    args = argv[1:]
    here = Path(__file__).resolve().parent
    if "--all" in args:
        scripts = sorted(here.glob("ge*.py"))
    else:
        scripts = [Path(a) if Path(a).is_absolute() else here / a for a in args]
    scripts = [p for p in scripts if p.is_file()]
    if not scripts:
        print(__doc__.strip())
        return 2
    total = 0
    for p in scripts:
        try:
            probs = check_script(p)
        except Exception as e:
            print(f"collide {p.name}: ERROR {type(e).__name__}: {e}")
            total += 1
            continue
        print(f"collide {p.name}: {len(probs)} collision(s)")
        for x in probs:
            print("   ", x)
        total += len(probs)
    print(f"collide_summary scripts={len(scripts)} collisions={total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))