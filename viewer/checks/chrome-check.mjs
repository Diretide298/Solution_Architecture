/**
 * The standalone pages' top bar names the same layers the viewer does.
 *
 * `public/page-chrome.js` carries its own list of layer keys and labels rather
 * than importing `LAYERS` from `core.js`, because core.js drags the tooltip
 * engine, the glossary and the layer vocabulary in behind it and a settings
 * page has no use for any of them. **A copy is only acceptable when something
 * checks it**, so this is that something.
 *
 * It catches the two ways the copy can rot, and one of them had already
 * happened while the chrome was being written: the Architecture layer's key is
 * `services`, not `architecture` — the layer was renamed and the key stayed,
 * because the key is in deep links, API paths and every mode id under it.
 * Guessing the key from the label gives a tab that lands on the default layer
 * and reads as a dead button.
 *
 *     node checks/chrome-check.mjs
 *
 * Static — no browser, no session, no running server.
 */
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PUBLIC = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'public');

/** `key: 'frontend', … label: 'Frontend'` out of core.js, in file order. */
async function layersFromCore() {
  const source = await readFile(path.join(PUBLIC, 'core.js'), 'utf8');
  const body = source.slice(source.indexOf('export const LAYERS = ['));
  const out = [];
  // Each layer object opens with its key and carries exactly one label. Read
  // pairwise rather than by parsing: the file is a module with imports, so it
  // cannot be required, and the shape here is regular enough to trust.
  const re = /^\s{4}key: '([^']+)',[\s\S]*?^\s{4}label: '([^']+)',/gm;
  let m;
  while ((m = re.exec(body))) out.push([m[1], m[2]]);
  return out;
}

/** The `LAYER_LINKS` table out of page-chrome.js. */
async function layersFromChrome() {
  const source = await readFile(path.join(PUBLIC, 'page-chrome.js'), 'utf8');
  const body = source.slice(source.indexOf('const LAYER_LINKS = ['));
  const out = [];
  const re = /^\s*\['([^']+)', '([^']+)',/gm;
  let m;
  while ((m = re.exec(body))) out.push([m[1], m[2]]);
  return out;
}

const core = await layersFromCore();
const chrome = await layersFromChrome();
const problems = [];

if (!core.length) problems.push('read no layers out of core.js — has LAYERS moved?');
if (!chrome.length) problems.push('read no layers out of page-chrome.js');

const coreKeys = core.map(([k]) => k);
const chromeKeys = chrome.map(([k]) => k);

for (const [key, label] of core) {
  const found = chrome.find(([k]) => k === key);
  if (!found) problems.push(`core.js has layer '${key}' (${label}) and the chrome does not`);
  else if (found[1] !== label) {
    problems.push(`layer '${key}' is "${label}" in core.js and "${found[1]}" in the chrome`);
  }
}
for (const [key, label] of chrome) {
  if (!coreKeys.includes(key)) {
    problems.push(`the chrome links to layer '${key}' (${label}) and core.js has no such key`);
  }
}
// Order is not correctness, but it is the thing a reader notices: the tabs are
// the same nine in both bars and they should read left to right the same way.
if (!problems.length && coreKeys.join() !== chromeKeys.join()) {
  problems.push(`same nine layers, different order:\n    core.js      ${coreKeys.join(' · ')}`
    + `\n    page-chrome  ${chromeKeys.join(' · ')}`);
}

if (problems.length) {
  console.error(`FAIL — ${problems.length} problem(s)`);
  for (const p of problems) console.error(`  ${p}`);
  process.exit(1);
}
console.log(`PASS — ${core.length} layers, same keys, labels and order in both bars`);
console.log(`  ${coreKeys.join(' · ')}`);
