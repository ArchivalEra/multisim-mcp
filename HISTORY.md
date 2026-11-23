# HISTORY.md

> Append-only provenance narrative (kept off every scan surface by `check_history.py`).

## 2026-11-23 · Upgrade Einfacht to Trust v2 (`ArchivalEra/Einfacht@492ff79`)

Following the sibling `ArchivalEra/S26-1_202609` migration pattern:

- Replaced `zreflect/` and `ruff.toml` with the sealed Einfacht Trust v2 suite (`zreflect/SEAL.json`, `trust.py`, `trust_core.py`, `check_explain.py`, `check_history.py`, `check_secrets.py`, `examples.py`, `impact.py`).
- Retired `reflect-hooks/` (`Einfacht.env`, `einfacht-env.sh`, `gate.py`, `install.py`, `pre-commit`, `pre-push`) in favor of `knobs.json` + `reflect-local/hook.py --chain`.
- Moved repo-local extensions out of sealed `zreflect/` into `reflect-local/`: `reflect-local/goal_multisim_criteria.py`, `reflect-local/figure_live_criteria.py`, `reflect-local/mail-read.py`, and declarative local principles in `reflect-local/principles.json` (retiring the custom `zreflect/goals.py` patch).
- Initialized `ANCHORS.json` (schema 2) via `python3 zreflect/trust.py --init`, re-measured `FACTS.json`, rendered `STATE.md` and `PRINCIPLES.md`, and updated `.github/workflows/ci.yml` shellcheck targets.
