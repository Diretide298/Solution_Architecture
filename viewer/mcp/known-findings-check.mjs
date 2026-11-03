#!/usr/bin/env node
// A pull lists the package's known findings on what the ticket links (r14 lane k, CHG-R14PUL-001; the lead, 3 November
// 2026: "a ticket's pull lists the package checks it already fails, so developers stop raising change requests for
// gaps we already know about"). The package route (lib/known-findings.mjs) reads this repository's
// ticvai/handoff/known-findings.json; the pull runs with a stand-in client over real tickets of
// ticvai/handoff/service-docs/adam-links.json. No services, no network.
//
//   node viewer/mcp/known-findings-check.mjs            the checks, and the pull's time with and without the index
//   node viewer/mcp/known-findings-check.mjs --show     and the section a pull of the first ticket writes
//
//   1. the route's answer: every finding of the index, each with its artefacts; a package without the file answers
//      not found;
//   2. a ticket whose links carry known findings: README.md has "Known gaps in the package (already on our list)"
//      with each finding once (its link, check, rule and message) and the line to follow; ticket.json keeps them;
//      the pull's answer counts them and its next step says what to do;
//   3. a ticket whose links carry none, and an ADAM without the route: no section;
//   4. more than KNOWN_SHOWN: the README lists the first ones and names ticket.json for the rest;
//   5. the index is read once per answer: the second pull reuses the map built for the first, and a pull with the
//      index takes no longer than one without, within noise.

import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { BY_NAME, KNOWN_SHOWN, knownFor, knownSection } from './tools.mjs';
import { knownFindings } from '../lib/known-findings.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TICVAI = path.resolve(HERE, '..', '..', 'ticvai');

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` - ${String(detail).slice(0, 600)}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};

// ---- 1. the route ------------------------------------------------------------------------------------------------
const answer = await knownFindings(TICVAI);
if (!answer.found) {
  console.log(`SKIP  ${answer.why}`);
  process.exit(0);
}
const index = JSON.parse(readFileSync(path.join(TICVAI, 'handoff', 'known-findings.json'), 'utf8'));
check('**the route answers every finding of the index, each with its artefacts**',
  answer.findings.length === index.findings.length && answer.findings.length > 0
  && answer.findings.every((f) => f.check && f.message && f.artefacts.length), `${answer.findings.length} of ${index.findings.length}`);
check('read once per file version: a second ask is the same answer', (await knownFindings(TICVAI)) === answer);
const none = await knownFindings(tmpdir());
check('a package without the file answers not found', none.found === false && /has no handoff\/known-findings\.json/.test(none.why));

// ---- real tickets ------------------------------------------------------------------------------------------------
const links = JSON.parse(readFileSync(path.join(TICVAI, 'handoff', 'service-docs', 'adam-links.json'), 'utf8')).links;
const byTicket = new Map();
for (const l of links) {
  if (!byTicket.has(l.key)) byTicket.set(l.key, { subject: l.subject ?? '', type: l.type ?? 'Task', touches: [] });
  const t = byTicket.get(l.key);
  if (!t.touches.some((x) => x.kind === l.kind && x.id === l.id)) t.touches.push({ kind: l.kind, id: l.id });
}
const at = new Map();
for (const f of answer.findings) for (const a of f.artefacts) at.set(a, (at.get(a) ?? 0) + 1);
const count = (t) => new Set(t.touches.flatMap((x) => answer.findings.filter((f) => f.artefacts.includes(`${x.kind}:${x.id}`)))).size;
const tasks = [...byTicket.entries()].filter(([, t]) => t.type === 'Task');
const some = tasks.find(([, t]) => t.touches.length <= 12 && count(t) >= 3 && count(t) <= 8);
const clean = tasks.find(([, t]) => t.touches.length >= 2 && t.touches.every((x) => !at.has(`${x.kind}:${x.id}`)));
const many = tasks.find(([, t]) => count(t) > KNOWN_SHOWN + 5);

/** A stand-in ADAM: the ticket from adam-links, every lookup layer empty, and `known-findings` from the package
 *  route (or `known` given: null for an ADAM without the route). */
function standIn(key, { known = answer } = {}) {
  const t = byTicket.get(key);
  const wp = { key, subject: t.subject, type: t.type, status: 'New', project: 'TICVAI', url: `http://op.test/work_packages/${key}`,
    description: '', comments: [] };
  const asked = [];
  return {
    asked,
    projectId: async () => 'ticvai',
    async layer(route) {
      asked.push(route);
      if (route === 'known-findings') {
        if (known === null) throw new Error('GET known-findings → 404');
        return { project: 'ticvai', served: 'r14', ...known };
      }
      return {};
    },
    async packageJson() { return { ok: false, status: 404, data: null }; },
    async file() { return { ok: false, status: 404, text: '' }; },
    async service(route, { method = 'GET' } = {}) {
      if (method === 'GET' && route.startsWith(`/api/work-packages/${key}?`)) {
        return { ok: true, status: 200, data: { workPackage: wp, touches: t.touches, blockedBy: [], subtasks: [], partOf: null } };
      }
      return { ok: false, status: 404, data: { detail: 'not in the stand-in' } };
    },
  };
}

async function pull(client, key) {
  const dir = await mkdtemp(path.join(tmpdir(), 'adam-known-'));
  try {
    const started = performance.now();
    const result = await BY_NAME.get('adam_pull').run(client, { key, dir });
    const ms = performance.now() - started;
    const folder = path.join(dir, '.adam', 'work', key);
    const readme = await readFile(path.join(folder, 'README.md'), 'utf8').catch(() => '');
    const saved = JSON.parse(await readFile(path.join(folder, 'ticket.json'), 'utf8').catch(() => '{}'));
    return { result, readme, saved, ms };
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

// ---- 2. a ticket with known findings ------------------------------------------------------------------------------
check('a real task with 3 to 8 known findings on 12 links or fewer, and one with none, are in adam-links.json',
  Boolean(some && clean), `${some?.[0]} ${clean?.[0]}`);
const [someKey, someT] = some;
const expected = count(someT);
const withGaps = await pull(standIn(someKey), someKey);
const head = `## Known gaps in the package (already on our list) (${expected})`;
const sectionText = withGaps.readme.slice(withGaps.readme.indexOf(head), withGaps.readme.indexOf('## Before you report a gap'));
check(`**#${someKey}: README.md lists its ${expected} known findings, once each, under the heading**`,
  withGaps.readme.includes(head) && (sectionText.match(/^- /gm) ?? []).length === expected, sectionText.slice(0, 900));
check('with the line to follow: known, being fixed, build around them, a change request only if one blocks',
  sectionText.includes('**They are known and being fixed: build around them as the package says now, and raise a change '
    + 'request only if one blocks you.**'));
const first = answer.findings.find((f) => someT.touches.some((x) => f.artefacts.includes(`${x.kind}:${x.id}`)));
check('each line names the link it came by, the check, the rule and the message',
  sectionText.includes(` - ${first.check} ${first.rule}: ${first.message.replace(/\s+/g, ' ').trim()}`), sectionText.slice(0, 600));
check('before "Before you report a gap", after what the ticket touches',
  withGaps.readme.indexOf(head) > withGaps.readme.indexOf('## What this touches')
  && withGaps.readme.indexOf(head) < withGaps.readme.indexOf('## Before you report a gap'));
check('ticket.json keeps every one, with the link it came by',
  withGaps.saved.knownFindings?.length === expected && withGaps.saved.knownFindings.every((f) => f.via && f.check && f.message));
check('the pull counts them, and its next step says build around them and raise a change request only if one blocks',
  withGaps.result.knownGaps === expected && /known gaps? in the package on what this ticket links/.test(withGaps.result.next)
  && /raise a change request only if one blocks you/.test(withGaps.result.next), withGaps.result.next);

// ---- 3. none, and an older ADAM -----------------------------------------------------------------------------------
const [cleanKey] = clean;
const noGaps = await pull(standIn(cleanKey), cleanKey);
check(`#${cleanKey}, whose ${clean[1].touches.length} links carry no known finding: no section, nothing counted`,
  !noGaps.readme.includes('Known gaps in the package') && noGaps.result.knownGaps === undefined
  && noGaps.saved.knownFindings === undefined, noGaps.readme.slice(0, 300));
const older = await pull(standIn(someKey, { known: null }), someKey);
check('an ADAM without the route: the pull goes on with no section, as before',
  older.result.found && !older.readme.includes('Known gaps in the package') && older.result.knownGaps === undefined);
const noIndex = await pull(standIn(someKey, { known: { found: false, why: 'no file' } }), someKey);
check('a release without the index: no section', !noIndex.readme.includes('Known gaps in the package'));

// ---- 4. more than the README shows ---------------------------------------------------------------------------------
if (many) {
  const got = await knownFor(standIn(many[0]), many[1].touches);
  const text = knownSection(got);
  check(`#${many[0]} (${got.findings.length} known findings): the README lists ${KNOWN_SHOWN} and names ticket.json for the rest`,
    (text.match(/^- /gm) ?? []).length === KNOWN_SHOWN
    && text.includes(`${got.findings.length - KNOWN_SHOWN} more are in ticket.json (\`knownFindings\`).`), text.slice(-300));
} else {
  console.log(`skip  no task with more than ${KNOWN_SHOWN + 5} known findings`);
}
const twoWay = answer.findings.find((x) => x.artefacts.length >= 2);
const bothLinks = twoWay.artefacts.slice(0, 2).map((x) => ({ kind: x.slice(0, x.indexOf(':')), id: x.slice(x.indexOf(':') + 1) }));
check(`a finding reached by two links is listed once (${twoWay.key}: ${twoWay.artefacts.slice(0, 2).join(', ')})`,
  (await knownFor(standIn(someKey), bothLinks)).findings.filter((x) => x.message === twoWay.message).length === 1);
check('no findings, no section', knownSection({ findings: [] }) === '' && knownSection(null) === '');

// ---- 5. one read, and no slower ------------------------------------------------------------------------------------
const shared = standIn(someKey);
const once = await knownFor(shared, someT.touches);
const t0 = performance.now();
const twice = await knownFor(shared, someT.touches);
const reuse = performance.now() - t0;
check('a pull asks the layer once, and the second pull of the same answer reuses its map (under 5 ms)',
  shared.asked.filter((r) => r === 'known-findings').length === 2 && reuse < 5 && twice.findings.length === once.findings.length,
  `${reuse.toFixed(2)} ms`);
// The pull with the index and without it, the slower of the two tickets' sets, five each, alternated.
const runs = { with: [], without: [] };
for (let i = 0; i < 5; i += 1) {
  runs.with.push((await pull(standIn(someKey), someKey)).ms);
  runs.without.push((await pull(standIn(someKey, { known: null }), someKey)).ms);
}
const median = (xs) => [...xs].sort((a, b) => a - b)[Math.floor(xs.length / 2)];
const [mWith, mWithout] = [median(runs.with), median(runs.without)];
console.log(`      pull of #${someKey} (${someT.touches.length} links, stand-in ADAM): ${mWith.toFixed(1)} ms with the index, `
  + `${mWithout.toFixed(1)} ms without (median of 5)`);
check('a pull with the index takes no longer than one without, within noise (median +20 ms at most)',
  mWith <= mWithout + 20, `${mWith.toFixed(1)} vs ${mWithout.toFixed(1)} ms`);

if (process.argv.includes('--show')) {
  console.log(`\n----- the section a pull of #${someKey} writes -----\n${sectionText}`);
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
