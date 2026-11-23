#!/usr/bin/env python3
"""Settler for questions/02-figure-live-renderer.md.

Judges the shipped validation artifact, not a promise in prose:

  rc=0  every structural contract holds
  rc=1  at least one contract is broken (each failure printed with a tag)

Checks are deliberately mechanical: no browser, no rendering, no "looks fine".
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "zreflect"),
)
from gate import module_meta  # noqa: E402

MODULE = module_meta(
    "figure-live-criteria",
    "structural settler for the live-figure validation "
    "artifact (text nodes, dual projection, offline vendor)",
    selftest=True,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO = os.path.join(ROOT, "deliverables", "figure-live")


def read(name):
    """Read a UTF-8 file relative to `DEMO`."""
    with open(os.path.join(DEMO, name), encoding="utf-8") as f:
        return f.read()


def _check_logic_graph(html, graph):
    checks = (
        ("'elk.partitioning.partition': 0" not in graph, "inputs_not_in_partition_zero"),
        ("? `in:${src}.o`" not in graph, "input_edges_not_wired_to_elk"),
        ('src="graph.js"' not in html, "page_not_using_shared_graph"),
        ("for (const e of out.edges || [])" not in html, "wires_not_from_elk_sections"),
        ("el('text'" not in html or "<use" in html, "logic_text_not_text_nodes"),
        ("elk.partitioning.partition" not in graph, "inputs_not_elk_nodes"),
    )
    return [tag for cond, tag in checks if cond]


def _check_logic_and_projection(html, logic, graph):
    bad = _check_logic_graph(html, graph)
    if "#projection" not in html or "project(logic, values)" not in html:
        bad.append("missing_text_projection")
    inputs = set(logic["inputs"])
    gate_ids = {q["id"] for q in logic["gates"]}
    for g in logic["gates"]:
        if not set(g["in"]).issubset(inputs | gate_ids):
            bad.append(f"unresolved_net:{g['id']}")
    if "in=${g.in.join(',')} out=${g.id} value=${values[g.id]}" not in html:
        bad.append("missing_netlist_template")
    if len(logic["gates"]) != 7:
        bad.append(f"gate_count={len(logic['gates'])}, expected 7")
    return bad


def _check_ui_and_vendor(html):
    checks = (
        ("addEventListener('click', show)" not in html, "missing_click_inspect"),
        ("addEventListener('change', redraw)" not in html, "missing_state_redraw"),
        ("root.dataset.theme" not in html or "var(--fg)" not in html, "missing_theme_variables"),
        ("vendor/elk.bundled.js" not in html or "vendor/wavedrom.unpkg.min.js" not in html, "missing_vendor_scripts"),
        (bool(re.search(r"https?://(?!www\.w3\.org)", html)), "external_url_in_html"),
        ("const mid = x0 + 18" in html or "terminals[n] = " in html, "hand_computed_fanout_present"),
        ("fetch('data/" in html, "local_fetch_breaks_file_protocol"),
        ("svg { max-width: 100%" in html, "zoom_clamped_by_max_width"),
    )
    bad = [tag for cond, tag in checks if cond]
    for f in (
        "vendor/elk.bundled.js",
        "vendor/wavedrom.unpkg.min.js",
        "vendor/ELK-LICENSE",
        "vendor/WAVEDROM-LICENSE",
    ):
        if not os.path.isfile(os.path.join(DEMO, f)):
            bad.append(f"missing_vendor_file:{f}")
    return bad


def _check_waveform(html, wave, wave_raw):
    bad = []
    if "rail-hi" not in html or "rail-lo" not in html:
        bad.append("missing_wave_reference_rails")
    levels = {s["name"]: s["wave"] for s in wave["signals"]}
    if not any("1" in v and "0" in v for v in levels.values()):
        bad.append("wave_has_no_transition")
    if not any(set(v.replace(".", "")) == {"1"} for v in levels.values()):
        bad.append("wave_missing_constant_high")
    if not any(set(v.replace(".", "")) == {"0"} for v in levels.values()):
        bad.append("wave_missing_constant_low")
    ticks = {len(s["wave"]) for s in wave["signals"]}
    if len(ticks) != 1:
        bad.append("wave_rows_unequal_length:%s" % sorted(ticks))
    if "wave.levels" in html or '"levels"' in wave_raw:
        bad.append("levels_duplicated_in_data")
    if "Object.fromEntries(wave.signals.map" not in html:
        bad.append("levels_not_derived")
    return bad


def _check_wire_styles(html, logic):
    bad = []
    styles = logic.get("wireStyles", {})
    nets = set(logic["inputs"]) | {g["id"] for g in logic["gates"]}
    for net, st in styles.items():
        if net not in nets:
            bad.append(f"wirestyle_unknown_net:{net}")
        if not isinstance(st, dict) or set(st) - {"color", "dash"}:
            bad.append(f"wirestyle_extra_knobs:{net}")
        if "color" in st and not re.fullmatch(r"#[0-9a-fA-F]{6}", str(st["color"])):
            bad.append(f"wirestyle_bad_color:{net}")
        if "dash" in st and st["dash"] not in ("solid", "dashed"):
            bad.append(f"wirestyle_bad_dash:{net}")
    if styles and "data.wireStyles" not in html:
        bad.append("wirestyles_not_rendered")
    if styles and "# wire styles" not in html:
        bad.append("wirestyles_not_projected")
    return bad


def _check_geometry_and_inline():
    bad = []
    geo = os.path.join(DEMO, "geometry.mjs")
    if not os.path.isfile(geo):
        bad.append("missing_geometry_settler")
    else:
        r = subprocess.run(
            ["node", geo], capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if r.returncode != 0:
            bad.append("geometry_gate_failed:" + r.stdout.strip().replace("\n", ";"))
        r2 = subprocess.run(
            ["node", geo, "--selftest"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if r2.returncode != 0 or "hand_fanout_caught=true" not in r2.stdout:
            bad.append("geometry_selftest_failed:" + r2.stdout.strip().replace("\n", ";"))
    r3 = subprocess.run(
        ["node", os.path.join(DEMO, "inline-data.mjs"), "--check"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r3.returncode != 0:
        bad.append("inline_data_stale:" + r3.stdout.strip())
    return bad


def check():
    """Run all structural and geometry checks on the live-figure demo."""
    html = read("index.html")
    graph = read("graph.js")
    logic = json.loads(read("data/logic-7gate.json"))
    wave_raw = read("data/wave-multirow.json")
    wave = json.loads(wave_raw)
    bad = _check_logic_and_projection(html, logic, graph)
    bad += _check_ui_and_vendor(html)
    bad += _check_waveform(html, wave, wave_raw)
    bad += _check_wire_styles(html, logic)
    bad += _check_geometry_and_inline()
    return bad


def selftest():
    """Two distinguishable outcomes: intact fixture -> 0; mutated copy -> 1."""
    import tempfile  # noqa: PLC0415
    global DEMO
    original = DEMO
    ok = check()
    with tempfile.TemporaryDirectory() as t:
        fixtures = {
            n: read(n)
            for n in (
                "index.html",
                "geometry.mjs",
                "graph.js",
                "inline-data.mjs",
                "data/logic-7gate.json",
                "data/wave-multirow.json",
            )
        }
        DEMO = t
        os.makedirs(os.path.join(t, "data"))
        os.makedirs(os.path.join(t, "vendor"))
        for n, body in fixtures.items():
            with open(os.path.join(t, n), "w", encoding="utf-8") as f:
                f.write(body)
        for v in ("elk.bundled.js", "wavedrom.unpkg.min.js", "ELK-LICENSE", "WAVEDROM-LICENSE"):
            with open(os.path.join(t, "vendor", v), "w", encoding="utf-8") as f:
                f.write(read("vendor/" + v))
        p = os.path.join(t, "index.html")
        with open(p, encoding="utf-8") as f:
            s = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(s.replace("addEventListener('change', redraw)", "").replace("rail-hi", ""))
        broken = check()
    DEMO = original
    intact = not ok
    mutated = bool(broken)
    passed = (1 if intact else 0) + (1 if mutated else 0)
    failed = 2 - passed
    print(
        "selftest intact_passes=%s mutant_detected=%s mutant_tags=%d"
        % (intact, mutated, len(broken)),
    )
    print("=== %d PASS / %d FAIL ===" % (passed, failed))
    return 0 if failed == 0 else 1


def main(argv=None):
    """CLI entry: `--selftest` or structural check against `deliverables/figure-live`."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--selftest":
        return selftest()
    bad = check()
    print(
        "figure_live_contract text_nodes=dual_projection=interaction=offline "
        "checked problems=%d" % len(bad),
    )
    for b in bad:
        print("FAIL | " + b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
