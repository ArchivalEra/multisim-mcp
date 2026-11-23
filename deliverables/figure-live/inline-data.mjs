#!/usr/bin/env node
// Inline data/*.json into index.html so the page works over file:// without
// fetch. The JSON files are the single source of truth; this script is the
// only writer of the inline copies. Run after editing data/.
//
//   node inline-data.mjs          -> rewrite the two inline blocks
//   node inline-data.mjs --check  -> rc=0 if inline copies match the files
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(HERE, 'index.html');
const pairs = [
  ['data-logic', 'data/logic-7gate.json'],
  ['data-wave', 'data/wave-multirow.json'],
];

function inline(html, id, json) {
  const open = `<script type="application/json" id="${id}">`;
  const i = html.indexOf(open);
  if (i < 0) throw new Error(`missing inline block ${id}`);
  const j = html.indexOf('</script>', i);
  return html.slice(0, i + open.length) + '\n' + json.trimEnd() + '\n' + html.slice(j);
}

let html = fs.readFileSync(htmlPath, 'utf8');
const check = process.argv.includes('--check');
let bad = 0;
for (const [id, file] of pairs) {
  const json = fs.readFileSync(path.join(HERE, file), 'utf8');
  const next = inline(html, id, json);
  if (check) {
    if (next !== html) { console.log(`STALE | ${id} != ${file}`); bad++; }
  } else {
    html = next;
  }
}
if (check) {
  console.log(`inline_data_check stale=${bad}`);
  process.exit(bad ? 1 : 0);
}
fs.writeFileSync(htmlPath, html);
console.log('inline_data_written blocks=2');
