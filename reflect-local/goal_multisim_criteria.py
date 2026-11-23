#!/usr/bin/env python3
"""Judging commands for this repo's Multisim goal-scope principles.

Kept as a file, not `python3 -c` strings: the ledger executes each cmd
verbatim at every commit, and a quoting trap inside a one-liner is a
permanently-red row waiting to happen. Three subcommands, each rc=0 pass /
rc=1 fail, each printing a stance line (never silent, never OFF-laundered).
"""
from __future__ import annotations

import os
import subprocess
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "zreflect"),
)
from gate import module_meta  # noqa: E402

MODULE = module_meta(
    "goal-multisim-criteria",
    "judging commands for the multisim-mcp local principles",
    selftest=False,
)

PREFIX = os.path.expanduser("~/.multisim143")
LAUNCHER = os.path.expanduser(
    "~/.local/share/applications/wine/Programs/NI Multisim 14.3.desktop",
)
LNK = os.path.join(
    PREFIX,
    "drive_c/users/archivalera/AppData/Roaming/Microsoft/Windows/"
    "Start Menu/Programs/NI Multisim 14.3.lnk",
)
COM_REL = (
    "C:\\\\Program Files (x86)\\\\National Instruments\\\\"
    "Circuit Design Suite 14.3\\\\MSInterface.dll"
)


def _resolve_lnk_exe():
    if not os.path.isfile(LNK):
        return None
    raw = open(LNK, "rb").read().decode("latin-1", errors="replace")
    tokens = [
        t for t in raw.replace("\x00", "\n").split("\n")
        if t.lower().endswith("multisim.exe")
    ]
    if not tokens:
        return None
    target = tokens[-1].strip("\\")
    if ":" in target:
        target = target.split(":", 1)[1].lstrip("\\")
    return os.path.join(PREFIX, "drive_c", target.replace("\\", "/"))


def production_path() -> int:
    """Launcher .lnk -> multisim.exe -> same prefix's COM InprocServer32."""
    exe = _resolve_lnk_exe()
    exe_ok = exe is not None and os.path.isfile(exe)
    com_ok = False
    reg = os.path.join(PREFIX, "system.reg")
    if os.path.isfile(reg):
        for line in open(reg, encoding="utf-8", errors="replace"):
            if "MSInterface.dll" in line and line.strip().startswith("@="):
                com_ok = COM_REL in line
                break
    print(
        "production_path exe=%s exe_exists=%s com_dll_in_prefix=%s"
        % (exe or "(unresolved)", exe_ok, com_ok),
    )
    return 0 if (exe_ok and com_ok) else 1


def no_orthogonal() -> int:
    """Verify repo-local hook wiring (reflect-local/hook.py --chain) and zreflect/next.py."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hook = os.path.join(root, ".git", "hooks", "pre-commit")
    hook_entry = os.path.join(root, "reflect-local", "hook.py")
    hook_ok = False
    if os.path.isfile(hook) and os.path.isfile(hook_entry):
        text = open(hook, encoding="utf-8", errors="replace").read()
        hook_ok = hook_entry in text and "hook.py --chain" in text
    nxt = os.path.join(root, "zreflect", "next.py")
    next_ok = os.path.isfile(nxt)
    if next_ok:
        env = {**os.environ, "REFLECT_LANG": ""}
        proc = subprocess.run(
            [sys.executable, nxt, root],
            capture_output=True,
            text=True,
            env=env,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        next_ok = proc.returncode == 0 and "tree_state" in proc.stdout
    print("no_orthogonal local_hook=%s vendor_next=%s" % (hook_ok, next_ok))
    return 0 if (hook_ok and next_ok) else 1


def no_requirements_in_git() -> int:
    """Requirements/RFP/brief documents belong in questions/ or outside git, never as tracked docs."""
    cjk = "".join(chr(c) for c in (0x9700, 0x6C42))
    markers = ("rfp", "research-brief", cjk)
    allow = (
        "mcp_server/requirements.txt",
        "docs/requirement_engineering.md",
        ("mcp_server/multisim_mcp/harness_skills/"
         "multisim-verify-requirements/skill.md"),
    )
    bad = []
    proc = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for path in proc.stdout.splitlines():
        low = path.lower()
        if low.replace("\\", "/") in allow or low.startswith("questions/"):
            continue
        if low.endswith((".md", ".txt")) and any(m in low for m in markers):
            bad.append(path)
    print("tracked_requirements=%d" % len(bad))
    for path in bad:
        print("note | tracked requirement file: " + path)
    return 1 if bad else 0


def main(argv=None):
    """Dispatch `production-path`, `no-orthogonal`, or `no-requirements-in-git`."""
    args = list(sys.argv[1:] if argv is None else argv)
    dispatch = {
        "no-requirements-in-git": no_requirements_in_git,
        "production-path": production_path,
        "no-orthogonal": no_orthogonal,
    }
    if not args:
        print("usage: goal_multisim_criteria.py production-path|no-orthogonal|no-requirements-in-git")
        return 2
    fn = dispatch.get(args[0])
    if fn is None:
        print("unknown subcommand: %s" % args[0])
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
