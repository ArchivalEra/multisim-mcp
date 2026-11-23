#!/usr/bin/env python3
"""白底转换器：把任意 PNG 统一成不透明白底 RGB。

为什么需要：透明底的 PNG 在图里中文会显示成马赛克，读图时会被误判成字体缺失。
凡是交给课程站或交给读图子代理的 PNG，都必须先过这一步。

用法：
    python whiten.py <png> [<png> ...]        # 原地转换，覆盖原文件
    python whiten.py --check <png> [...]      # 只检查，不写（有 alpha 或非 RGB 即 rc=1）
    python whiten.py --out DIR <png> ...      # 输出到 DIR，不改原文件

退出码：0 全部已是白底 RGB；1 有文件需要转换（--check）或转换失败。
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


def whiten(path: Path, out_dir: Path | None = None) -> bool:
    """把 path 转成不透明白底 RGB。返回是否发生了实际改动。"""
    im = Image.open(path)
    changed = im.mode != "RGB"
    if im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
        changed = True
    elif im.mode != "RGB":
        im = im.convert("RGB")
        changed = True
    target = (out_dir / path.name) if out_dir else path
    im.save(target)
    return changed


def needs_work(path: Path) -> bool:
    im = Image.open(path)
    if im.mode != "RGB":
        return True
    return "transparency" in im.info


def main(argv: list[str]) -> int:
    args = argv[1:]
    check = "--check" in args
    args = [a for a in args if a != "--check"]
    out_dir = None
    if "--out" in args:
        i = args.index("--out")
        out_dir = Path(args[i + 1]).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        args = args[:i] + args[i + 2:]
    files = [Path(a) for a in args]
    if not files:
        print(__doc__.strip())
        return 2
    if check:
        bad = [p for p in files if needs_work(p)]
        print(f"whiten_check total={len(files)} needs_work={len(bad)}")
        for p in bad:
            print("  needs whitening:", p)
        return 1 if bad else 0
    changed = sum(1 for p in files if whiten(p, out_dir))
    print(f"whiten_done files={len(files)} changed={changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))