#!/usr/bin/env python3
"""Goal-scope principles: promises made **for the duration of one goal**.

## Why this module exists (first consumer: this repo's Multisim goal)

`doc.RULES` holds **permanent** principles. A goal ("drive Multisim through
the MCP bridge") accumulates promises that bind only *while that goal runs* —
"never touch a second Wine prefix", "every circuit goes through the same
multisim.exe the desktop launcher starts". Two diseases are possible:

1. Written into prose (chat, handoff): no judging command, no re-runner —
   the exact "fact that rots" this suite exists to kill.
2. Written into `doc.RULES`: permanent scope for a temporary promise — after
   the goal ends the row is dead weight the ledger keeps paying for.

Same shape as a principle (id + sentence + judging command; rc=0 passes,
stdout must take a stance), but a **separate, explicitly scoped registry**.

## Activation is a knob, not "GOALS is non-empty"

Same reasoning as `doc.accepts_principles()`: "rows exist" and "this repo
commits to obeying them now" are different claims. `REFLECT_GOAL` names the
live goal(s) (ids or `all`); unsetting it is the explicit "goal over" — the
next `facts.py --accept-principles` drops the rows (drops must be explicitly
accepted, which is exactly the discipline a goal's end deserves).
"""
from __future__ import annotations

import gate as _gate_mod  # noqa: PLC0415  (vendor layout: same dir)
from typing import NamedTuple


class GoalRule(NamedTuple):
    """Same shape as doc.Rule — one re-runner, zero new shapes.

    `scope` = the repo the promise binds (absolute path). Empty = binds
    wherever the suite is vendored.
    """
    id: str
    text: str
    cmd: str
    scope: str = ""


# ── Active goal registry (single place of origin, same discipline as RULES) ──
#
# ⚠️ Every cmd must take a stance. Judging commands live here, not in shell
# one-liners with quoting traps: each is a tiny `python3 -c` whose logic is a
# **file check + stance line**, kept readable on purpose (they run verbatim
# in the ledger at every commit).
GOALS = (
    GoalRule(
        "goal.multisim.production_path_only",
        "every Multisim binary this goal touches is the one production binary "
        "the desktop launcher starts (same Wine prefix ~/.multisim143, same "
        "multisim.exe); any second prefix or parallel install is a violation",
        "python3 zreflect/goal_multisim_criteria.py production-path",
        scope="/mnt/hdd/kimicode-projects/multisim-mcp",
    ),
    GoalRule(
        "goal.multisim.no_orthogonal_tests",
        "every verification goes through multisim-mcp's own COM worker "
        "protocol (the production path the MCP frontend uses); a hand-rolled "
        "parallel COM client that re-verifies what the MCP stack already "
        "exercises is an orthogonal test and forbidden",
        "python3 zreflect/goal_multisim_criteria.py no-orthogonal",
        scope="/mnt/hdd/kimicode-projects/multisim-mcp",
    ),
)

MODULE = _gate_mod.module_meta(
    "Goal-scope principles",
    "promises made for one goal: registered in GOALS, activated by REFLECT_GOAL, "
    "judged via principle.goal.* in the ledger, expired by unsetting the knob",
    selftest=False)


_BY_ID = {g.id: g for g in GOALS}

GOALS_BEGIN = "<!-- AUTO:GOALS -->"
GOALS_END = "<!-- /AUTO:GOALS -->"


def active_goals(repo_root=None):
    """GOALS filtered to the current activation state. **Pure function**.

    Live = `REFLECT_GOAL` names the id (comma list or `all`). Rows with a
    `scope` bind only when the repo under judgment is that repo.
    """
    import os  # noqa: PLC0415

    named = os.environ.get("REFLECT_GOAL", "").strip()
    if not named:
        return []
    wanted = {p.strip().casefold() for p in named.split(",") if p.strip()}
    root = os.path.abspath(repo_root or os.getcwd()).casefold()
    out = []
    for g in GOALS:
        if g.id.casefold() not in wanted and "all" not in wanted:
            continue
        if g.scope and os.path.abspath(g.scope).casefold() != root:
            continue
        out.append(g)
    return out


def render_goals(rows=None):
    """Goals → the `AUTO:GOALS` machine block. **Pure function**.

    Not part of `facts.py --check`'s byte-exact surface: the active set
    changes when a goal starts/ends, and a block that flips mid-goal makes
    --check red for anyone without the same knob. The judged surface is the
    ledger (`principle.goal.*`); this block is a view.
    """
    rows = active_goals() if rows is None else rows
    lines = [GOALS_BEGIN,
             ("> Rendered by `zreflect/goals.py --render` from the `GOALS` table; "
             "**do not hand-edit**. Judged surface = `principle.goal.*` in "
             "FACTS.json (`check_facts_replay`), not this block."),
             "",
             "| id | promise | judging command |",
             "|---|---|---|"]
    for r in rows:
        lines.append("| `%s` | %s | `%s` |" % (r.id, r.text, r.cmd))
    lines += ["", "%d active goal principles." % len(rows), GOALS_END]
    return "\n".join(lines)


def facts_of_goals():
    """Active goals → `{key: ledger.fact(...)}`, same shape as
    doc.facts_of_rules. **Pure function**. Key prefix `principle.goal.`;
    kind="principle" (judged by rc, like every other principle)."""
    import ledger  # noqa: PLC0415
    out = {}
    for g in active_goals():
        out["principle." + g.id] = ledger.fact(
            "ok", g.cmd, "principle", g.text, kind="principle")
    return out


def main(argv=None):
    """`--render` = active view; `--list` = full registry. Views only — the
    ledger write goes through facts.py's existing `--accept-principles`."""
    import sys  # noqa: PLC0415
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--render" in argv:
        print(render_goals())
        return 0
    if "--list" in argv:
        print(render_goals(GOALS))
        return 0
    print("goals.py: use --render (active) or --list (full registry)")
    return 2


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
