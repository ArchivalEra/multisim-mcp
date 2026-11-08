# PRINCIPLES

> design rules that do not change. Each one is a **runnable
> command**, replayed by `check_facts_replay` on every commit.

<!-- AUTO:RULES -->
> This block is rendered by `zreflect/facts.py --render-doc` from the `RULES` table in `zreflect/doc.py`; **do not hand-edit**.
> Every row's judging command is in `FACTS.json` and is executed verbatim at every commit (`check_facts_replay`).

| id | principle | judging command |
|---|---|---|
| `assertion_lifecycle` | a retracted claim must not quietly return as current state | `python3 zreflect/check_retractions.py` |
| `declared_not_globbed` | predicates are declarations, not filenames: the execution surface reads registry --run <phase> | `python3 zreflect/registry.py --gates` |
| `falsifiable` | claims must be falsifiable: always-true shortcuts are swept by AST and any hit fails | `python3 zreflect/registry.py --selftest` |
| `host_agnostic` | the suite's source recognizes no host's directory names / config formats (host wiring belongs to the consumer) | `python3 -c "import os,sys;w=['.'+chr(122)+chr(99)+chr(111)+chr(100)+chr(101)+'/','ZCODE_'+'PROJECT_DIR','hook'+'SpecificOutput'];bad=[(d,f) for d in ('zreflect','reflect-hooks') for r,_,fs in os.walk(d) for f in fs if f.endswith(('.py','.sh')) and any(k in open(os.path.join(r,f),encoding='utf-8',errors='replace').read() for k in w)];print('host_coupled=%d' % len(bad));sys.exit(1 if bad else 0)"` |
| `machine_rows` | machine rows are defined in one place, machine.ROWS; the shell side has a behavior reconciler | `python3 zreflect/machine.py --selftest` |
| `no_retired_names` | retired names must not appear as current state; sha provenance and age are checkable | `python3 zreflect/check_stale.py` |
| `number_once` | each number is produced once: documents reference it as [[key]], never hand-copied (enforced both ways) | `python3 zreflect/check_facts.py` |
| `off_is_visible` | off must be distinguishable from "ran and passed"; a gate that can go off must declare why | `python3 -c "import sys;sys.path.insert(0,'zreflect');import registry, criteria;gs=registry.gates()[0];p=criteria.off_reason_problems(gs);print('off_reason_ok gates=%d problems=%d' % (len(gs), len(p)));sys.exit(0 if gs and not p else 1)"` |
| `only_measured` | numbers/behavior trust measurement only; every fact must carry a re-run command | `python3 -c "import json,sys;d=json.load(open('FACTS.json', encoding='utf-8'))['facts'];bad=[k for k,v in d.items() if not (isinstance(v,dict) and str(v.get('cmd','')).strip())];print('facts_without_cmd=%d' % len(bad));sys.exit(1 if bad else 0)"` |
| `open_questions_settle` | every unresolved open question must carry a runnable settler | `python3 zreflect/check_questions.py` |
| `selfcert_harness` | every gate must have a --selftest entry (written but never run = decoration) | `python3 -c "import sys;sys.path.insert(0,'zreflect');import registry;u=registry.modules()[1];print('undeclared_modules=%d' % len(u));sys.exit(1 if u else 0)"` |
| `snapshot_hygiene` | a mutable global imported across modules is a value copy (stale snapshot): read via the module attribute instead | `python3 zreflect/check_snapshots.py` |
| `three_readmes` | the three-language READMEs are three copies of one assertion: change one, change all three in the same batch | `python3 zreflect/check_readme_sync.py` |
| `zero_language` | zero language in the core: user-visible messages go through M(code); machine contracts are untranslatable by construction | `python3 zreflect/check_i18n.py` |

14 principles — each with a judging command that **really runs**.
<!-- /AUTO:RULES -->
