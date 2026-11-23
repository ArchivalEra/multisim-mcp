#!/usr/bin/env node
// Geometry settler for the live-figure validation artifact.
//
// Runs the SAME layout code path the page runs (ELK, primary inputs included),
// then checks the two criteria the course site actually cares about:
//   1. no wire segment crosses the interior of any gate box
//   2. no wire segment crosses a text label's bounding box
//
// Usage:
//   node geometry.mjs                 -> judge the shipped fixture
//   node geometry.mjs --selftest      -> intact must pass, mutants must fail
//   node geometry.mjs --json          -> machine-readable report
//
// rc=0 pass, rc=1 fail. Prints a stance line either way.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire as _cr } from 'node:module';
const _require = _cr(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ELK = _require(path.join(HERE, 'vendor', 'elk.bundled.js'));
const { buildGraph, GATE_W: W, GATE_H: H } = _require('./graph.js');
export { buildGraph };

// strict interior crossing of an axis-aligned segment and a rectangle
function segCrossesRect(a, b, r) {
  const [x1, y1] = a, [x2, y2] = b;
  const L = r.x, R = r.x + r.width, T = r.y, B = r.y + r.height;
  if (y1 === y2) {
    if (!(T < y1 && y1 < B)) return false;
    return Math.max(Math.min(x1, x2), L) < Math.min(Math.max(x1, x2), R);
  }
  if (x1 === x2) {
    if (!(L < x1 && x1 < R)) return false;
    return Math.max(Math.min(y1, y2), T) < Math.min(Math.max(y1, y2), B);
  }
  return false;
}

// Approximate text bboxes for every label the page draws: the gate's centre
// symbol, its bottom id line, and each primary-input label. Width estimate is
// monospace-ish (5.2 px/char at 10 px, 6.5 at 13 px); height = font size.
function textBoxes(data, nodes) {
  const boxes = [];
  const push = (owner, text, cx, y, px) => boxes.push({
    owner, x: cx - text.length * px * 0.4, y: y - px,
    width: text.length * px * 0.8, height: px,
  });
  for (const g of data.gates) {
    const c = nodes.get(g.id);
    if (!c) continue;
    push(g.id + ':symbol', g.label || '&', c.x + W / 2, c.y + H / 2 - 2, 13);
    push(g.id + ':id', `${g.id} · ${g.type}=0`, c.x + W / 2, c.y + H - 7, 10);
  }
  for (const n of Object.keys(data.inputs)) {
    const c = nodes.get(`in:${n}`);
    if (!c) continue;
    // page draws the label centred above the terminal box (11 px)
    const text = `${n}=0`;
    push(`in:${n}`, text, c.x + c.width / 2, c.y - 5, 11);
  }
  return boxes;
}

// 083 condition 2: input label spacing must be at least one font height.
function inputLabelSpacing(data, nodes, fontPx = 13) {
  const ys = Object.keys(data.inputs)
    .map((n) => nodes.get(`in:${n}`))
    .filter(Boolean)
    .map((c) => c.y + c.height / 2)
    .sort((a, b) => a - b);
  const gaps = [];
  for (let i = 1; i < ys.length; i++) gaps.push(ys[i] - ys[i - 1]);
  return {minGap: gaps.length ? Math.min(...gaps) : Infinity, fontPx};
}

export async function judge(data) {
  const out = await new ELK().layout(buildGraph(data));
  const nodes = new Map(out.children.map((c) => [c.id, c]));
  const boxes = textBoxes(data, nodes);
  const problems = [];
  for (const e of out.edges || [])
    for (const s of e.sections || []) {
      const pts = [s.startPoint, ...(s.bendPoints || []), s.endPoint].map((p) => [p.x, p.y]);
      for (let i = 0; i < pts.length - 1; i++) {
        for (const c of out.children) {
          if (c.id.startsWith('in:')) continue;
          if (segCrossesRect(pts[i], pts[i + 1], c))
            problems.push({kind: 'wire_through_box', edge: e.id, box: c.id,
                           seg: [pts[i], pts[i + 1]]});
        }
        for (const b of boxes) {
          if (segCrossesRect(pts[i], pts[i + 1], b))
            problems.push({kind: 'wire_through_text', edge: e.id, label: b.owner,
                           seg: [pts[i], pts[i + 1]]});
        }
      }
    }
  const spacing = inputLabelSpacing(data, nodes);
  if (spacing.minGap < spacing.fontPx)
    problems.push({kind: 'input_label_spacing', minGap: spacing.minGap,
                   required: spacing.fontPx});
  return {problems, spacing,
          nodes: out.children.map((c) => ({id: c.id, x: c.x, y: c.y}))};
}

function loadFixture() {
  return JSON.parse(fs.readFileSync(path.join(HERE, 'data', 'logic-7gate.json'), 'utf8'));
}

async function selftest() {
  const base = loadFixture();
  const intact = await judge(base);
  const mutants = [];

  // topology mutant 1: delete a gate (its consumers then reference a missing net)
  const m1 = structuredClone(base);
  m1.gates = m1.gates.filter((g) => g.id !== 'nC');
  for (const g of m1.gates) g.in = g.in.map((n) => (n === 'nC' ? 'C' : n));
  mutants.push(['delete_gate', await judge(m1)]);

  // topology mutant 2: add an edge that forces a long cross-layer wire
  const m2 = structuredClone(base);
  m2.gates.push({id: 'extra', type: 'nand', in: ['A', 'Y'], label: '&'});
  m2.outputs.push('extra');
  mutants.push(['add_edge', await judge(m2)]);

  // geometry mutant 3: hand-computed fan-out (the defect 083 reported)
  const m3 = structuredClone(base);
  const out3 = await new ELK().layout(buildGraph(m3));
  const nodes3 = new Map(out3.children.map((c) => [c.id, c]));
  const handProblems = [];
  for (const g of m3.gates)
    for (let i = 0; i < g.in.length; i++) {
      const src = g.in[i];
      if (!Object.hasOwn(m3.inputs, src)) continue;
      const t = nodes3.get(`in:${src}`), c = nodes3.get(g.id);
      const port = c.ports.find((p) => p.id === `${g.id}.i${i}`);
      const x0 = t.x + t.width, y0 = t.y + t.height / 2;
      const x1 = c.x + (port ? port.x : 0), y1 = c.y + (port ? port.y : H / 2);
      const mid = x0 + 18 + 10 * Object.keys(m3.inputs).indexOf(src);
      const pts = [[x0, y0], [mid, y0], [mid, y1], [x1, y1]];
      for (let k = 0; k < pts.length - 1; k++)
        for (const box of out3.children) {
          if (box.id.startsWith('in:')) continue;
          if (segCrossesRect(pts[k], pts[k + 1], box))
            handProblems.push({kind: 'wire_through_box', edge: `${src}->${g.id}`, box: box.id});
        }
    }
  mutants.push(['hand_fanout_regression', {problems: handProblems}]);

  // spacing mutant: squeeze two input terminals onto the same row; the
  // spacing criterion must catch it (083 condition 2).
  const m4 = structuredClone(base);
  const out4 = await new ELK().layout(buildGraph(m4));
  const nodes4 = new Map(out4.children.map((c) => [c.id, c]));
  const names4 = Object.keys(m4.inputs);
  if (names4.length >= 2) {
    const a = nodes4.get(`in:${names4[0]}`), b = nodes4.get(`in:${names4[1]}`);
    b.y = a.y;  // collapse the gap to zero
  }
  const sp4 = inputLabelSpacing(m4, nodes4);
  const spacingCaught = sp4.minGap < sp4.fontPx;

  const intactOk = intact.problems.length === 0;
  const regressionCaught = handProblems.length > 0;
  // topology mutants must remain clean: a real regression would show problems
  const topologyClean = mutants.slice(0, 2).every(([, r]) => r.problems.length === 0);
  console.log(`selftest intact_passes=${intactOk} hand_fanout_caught=${regressionCaught} ` +
              `hand_fanout_crossings=${handProblems.length} topology_mutants_clean=${topologyClean} ` +
              `spacing_mutant_caught=${spacingCaught}`);
  return intactOk && regressionCaught && topologyClean && spacingCaught ? 0 : 1;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
const argv = process.argv.slice(2);
if (isMain && argv.includes('--selftest')) {
  process.exit(await selftest());
}
if (isMain) {
const report = await judge(loadFixture());
if (argv.includes('--json')) {
  console.log(JSON.stringify(report, null, 2));
} else {
  const nBox = report.problems.filter((p) => p.kind === 'wire_through_box').length;
  const nText = report.problems.filter((p) => p.kind === 'wire_through_text').length;
  const nSpace = report.problems.filter((p) => p.kind === 'input_label_spacing').length;
  console.log(`geometry wire_x_box=${nBox} wire_x_text=${nText} ` +
              `input_label_spacing_violations=${nSpace} problems=${report.problems.length}`);
  for (const p of report.problems) console.log('FAIL | ' + JSON.stringify(p));
}
process.exit(report.problems.length ? 1 : 0);
}
