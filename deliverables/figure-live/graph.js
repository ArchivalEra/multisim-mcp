// Shared graph builder: the page and the geometry settler both call this.
// One origin for node sizes, partitions, ports and layout options — changing
// a layout parameter here changes both the drawing and its judge.
//
// Browser: loaded as a classic script, exposes window.FigureGraph.
// Node:    module.exports = { buildGraph, GATE_W, GATE_H, TERM_W, TERM_H }.

(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.FigureGraph = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const GATE_W = 92, GATE_H = 56;
  const TERM_W = 22, TERM_H = 22;

  function buildGraph(data) {
    const mkGate = (g) => ({
      id: g.id, width: GATE_W, height: GATE_H,
      layoutOptions: {'elk.portConstraints': 'FIXED_ORDER'},
      ports: [
        ...g.in.map((n, i) => ({id: `${g.id}.i${i}`, layoutOptions: {'elk.port.side': 'WEST'}})),
        {id: `${g.id}.o`, layoutOptions: {'elk.port.side': 'EAST'}},
      ],
    });
    const inputNames = Object.keys(data.inputs);
    // Topological depth: primary inputs are partition 0, each gate sits one
    // layer after its deepest input. ELK owns every coordinate, including the
    // primary-input fan-out; no hand-computed channel constants remain.
    const depth = {};
    for (const n of inputNames) depth[n] = 0;
    const depthOf = (id) => {
      if (depth[id] !== undefined) return depth[id];
      const g = data.gates.find((x) => x.id === id);
      depth[id] = 1 + Math.max(...g.in.map(depthOf));
      return depth[id];
    };
    for (const g of data.gates) depthOf(g.id);
    const terminals = inputNames.map((n) => ({
      id: `in:${n}`, width: TERM_W, height: TERM_H,
      layoutOptions: {'elk.portConstraints': 'FIXED_SIDE',
                      'elk.partitioning.partition': 0},
      ports: [{id: `in:${n}.o`, layoutOptions: {'elk.port.side': 'EAST'}}],
    }));
    const gates = data.gates.map((g) => {
      const node = mkGate(g);
      node.layoutOptions['elk.partitioning.partition'] = depth[g.id];
      return node;
    });
    const children = [...terminals, ...gates];
    const edges = [];
    for (const g of data.gates)
      for (let i = 0; i < g.in.length; i++) {
        const src = g.in[i];
        const source = Object.prototype.hasOwnProperty.call(data.inputs, src)
          ? `in:${src}.o` : `${src}.o`;
        edges.push({id: `e-${src}-${g.id}-${i}`,
                    sources: [source], targets: [`${g.id}.i${i}`]});
      }
    return {
      id: 'root',
      layoutOptions: {
        'elk.algorithm': 'layered', 'elk.direction': 'RIGHT',
        'elk.edgeRouting': 'ORTHOGONAL',
        'elk.layered.spacing.nodeNodeBetweenLayers': '90',
        'elk.spacing.nodeNode': '34',
        'elk.layered.cycleBreaking.strategy': 'GREEDY',
        'elk.partitioning.activate': true,
      },
      children, edges,
    };
  }

  return {buildGraph, GATE_W, GATE_H, TERM_W, TERM_H};
}));
