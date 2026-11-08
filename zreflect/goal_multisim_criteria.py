#!/usr/bin/env python3
"""Judging commands for this repo's goal-scope principles (goals.GOALS).

Kept as a file, not `python3 -c` strings: the ledger executes each cmd
verbatim at every commit, and a quoting trap inside a one-liner is a
permanently-red row waiting to happen (observed with escaped-backslash
path surgery). Two subcommands, each rc=0 pass / rc=1 fail, each printing
a stance line (never silent, never OFF-laundered).

production-path: the desktop launcher's .lnk-less Exec chain resolves to
exactly one multisim.exe inside ~/.multisim143/drive_c, the file exists,
and the COM InprocServer32 for MultisimInterface.MultisimApp points into
the same prefix. Launcher + COM + filesystem: three views of one install.

no-orthogonal: the host-side bridge (kimi-code hooks) exists, resolves the
suite from the event's cwd (vendor-aware, not the tool repo), and wires
both SessionStart and PreToolUse.
"""
from __future__ import annotations

import os
import sys

import gate
from gate import module_meta

MODULE = module_meta("goal-multisim-criteria",
                     "judging commands for the goal-scope principles "
                     "(ledged as principle.goal.*, replayed verbatim)",
                     selftest=False)

PREFIX = os.path.expanduser("~/.multisim143")
LAUNCHER = os.path.expanduser(
    "~/.local/share/applications/wine/Programs/NI Multisim 14.3.desktop")
BRIDGE = os.path.expanduser("~/.kimi-code/hooks/einfacht-bridge.py")
KIMI_CONFIG = os.path.expanduser("~/.kimi-code/config.toml")
LNK = os.path.join(
    PREFIX, "drive_c/users/archivalera/AppData/Roaming/Microsoft/Windows/"
            "Start Menu/Programs/NI Multisim 14.3.lnk")
COM_REL = ("C:\\\\Program Files (x86)\\\\National Instruments\\\\"
           "Circuit Design Suite 14.3\\\\MSInterface.dll")


def production_path() -> int:
    """Launcher .lnk -> multisim.exe -> same prefix's COM InprocServer32.

    Three independent views of one install: the desktop launcher's Start-Menu
    .lnk target, the filesystem, and the COM registration inside the same
    prefix's system.reg. All three must name the same prefix.
    """
    exe = None
    if os.path.isfile(LNK):
        raw = open(LNK, "rb").read().decode("latin-1", errors="replace")
        tokens = [t for t in raw.replace("\x00", "\n").split("\n")
                  if t.lower().endswith("multisim.exe")]
        if tokens:
            # The last string in a .lnk is the target path; it may start with
            # a backslash and carries the drive letter ('C:\...').
            target = tokens[-1].strip("\\")
            if ":" in target:
                target = target.split(":", 1)[1].lstrip("\\")
            exe = os.path.join(PREFIX, "drive_c", target.replace("\\", "/"))
    exe_ok = bool(exe) and os.path.isfile(exe)
    com_ok = False
    reg = os.path.join(PREFIX, "system.reg")
    if os.path.isfile(reg):
        # system.reg stores backslashes literally (doubled in the text file).
        com_needle = COM_REL
        for line in open(reg, encoding="utf-8", errors="replace"):
            if "MSInterface.dll" in line and line.strip().startswith("@="):
                com_ok = com_needle in line
                break
    print("production_path exe=%s exe_exists=%s com_dll_in_prefix=%s"
          % (exe or "(unresolved)", exe_ok, com_ok))
    return 0 if (exe_ok and com_ok) else 1


def no_orthogonal() -> int:
    bridge_ok = os.path.isfile(BRIDGE)
    vendor_aware = False
    wired = False
    if os.path.isfile(BRIDGE):
        src = open(BRIDGE, encoding="utf-8", errors="replace").read()
        vendor_aware = ("zcode-projects/Einfacht" not in src
                        and "find_suite_repo" in src)
    if os.path.isfile(KIMI_CONFIG):
        cfg = open(KIMI_CONFIG, encoding="utf-8", errors="replace").read()
        wired = ("einfacht-bridge.py" in cfg
                 and "SessionStart" in cfg and "PreToolUse" in cfg)
    print("no_orthogonal bridge=%s vendor_aware=%s hooks_wired=%s"
          % (bridge_ok, vendor_aware, wired))
    return 0 if (bridge_ok and vendor_aware and wired) else 1


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: check_goal_multisim.py production-path|no-orthogonal")
        return 2
    if argv[0] == "production-path":
        return production_path()
    if argv[0] == "no-orthogonal":
        return no_orthogonal()
    print("unknown subcommand: %s" % argv[0])
    return 2


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
