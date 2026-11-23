#!/usr/bin/env python3
"""文字压文字检查：机检判据。

取图中每个 Text 的窗口包围盒，两两求交，交集面积超过较小框的 8% 即报重叠。
轴名与刻度不参与（它们按设计贴轴）。

用法：/tmp/figvenv/bin/python overlaptext.py --all
      /tmp/figvenv/bin/python overlaptext.py ge08.py
退出码：0 无重叠；1 有重叠。
"""
from __future__ import annotations
import runpy, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text

AREA_RATIO = 0.08


def grab(path: Path):
    figs = []
    orig = matplotlib.figure.Figure.savefig
    def savefig(self, *a, **k):
        if self not in figs:
            figs.append(self)
        return orig(self, *a, **k)
    matplotlib.figure.Figure.savefig = savefig
    old = plt.close
    plt.close = lambda *a, **k: None
    try:
        runpy.run_path(str(path), run_name="__main__")
        if not figs:
            for n in plt.get_fignums():
                figs.append(plt.figure(n))
    finally:
        matplotlib.figure.Figure.savefig = orig
        plt.close = old
    return figs


def boxes(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    out = []
    for ax in fig.axes:
        for t in ax.texts:
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


def overlap(a, b):
    x0 = max(a.x0, b.x0); x1 = min(a.x1, b.x1)
    y0 = max(a.y0, b.y0); y1 = min(a.y1, b.y1)
    if x1 <= x0 or y1 <= y0:
        return 0.0
    inter = (x1 - x0) * (y1 - y0)
    small = min(a.width * a.height, b.width * b.height)
    return inter / small if small > 0 else 0.0


def check(path: Path):
    probs = []
    for fig in grab(path):
        bs = boxes(fig)
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                s1, b1 = bs[i]; s2, b2 = bs[j]
                r = overlap(b1, b2)
                if r >= AREA_RATIO:
                    probs.append((s1, s2, r))
    return probs


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
        print(f"{p.name}: {len(probs)} text-text overlap(s)")
        for a, b, r in probs:
            print(f"    {r*100:.0f}%  '{a[:28]}' <> '{b[:28]}'")
        total += len(probs)
    print(f"overlap_summary scripts={len(scripts)} overlaps={total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
