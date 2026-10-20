#!/usr/bin/env node
// A pull shows the task text of the release ADAM serves, for every ticket, and says in one line when the
// OpenProject ticket still has an older text (r8 re-walk, `started-ticket-text-fix-not-delivered`: four started
// tickets read "Written at release r6" after the plan rewrote them). The package route (lib/ticket-text.mjs) runs
// against the TICVAI package beside the viewer; the pull runs with a stand-in client. No services, no network.
//
//   node viewer/mcp/ticket-text-check.mjs            the checks
//   node viewer/mcp/ticket-text-check.mjs --show     and the README a pull of ARCH-TESTS (#27688) writes

import { mkdtemp, readFile, rm, stat } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { BY_NAME, sameText, textNotice } from './tools.mjs';
import { ticketText } from '../lib/ticket-text.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TICVAI = path.resolve(HERE, '..', '..', 'ticvai');
const DEMO = path.resolve(HERE, '..', '..', 'demo', 'package');

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` — ${detail}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};

// ARCH-TESTS as OpenProject holds it: the r6 pointer, left alone because the ticket is started (Ready for QA).
const R6 = '**Architecture tests for 17 modules: no module references another, and no module\'s SQL names another\'s schema**\n\n'
  + '- Key: `ARCH-TESTS`\n- Builds: `adr ADR-0055`, `adr ADR-0028`\n- Pull via ADAM: `/ticket 27688`\n- Written at release `r6`\n\n'
  + '**What:** Architecture tests for 17 modules: no module references another, and no module\'s SQL names another\'s '
  + 'schema. Builds: `adr ADR-0055`, `adr ADR-0028`. Extend tests/Ticvai.ArchitectureTests/ModuleBoundaryTests.cs from '
  + 'six modules to 17 (ADR-0055), and add a test that fails when a module\'s SQL names another module\'s schema other '
  + 'than through a published read view.\n\n'
  + '**Done when:** a deliberate cross-module reference and a raw cross-schema query each fail the build in CI.\n\n'
  + 'The rest of the spec (contract, tables, screens) lives in ADAM at the release tag. OpenProject holds who, when, state and order.';

const bundle = JSON.parse(await readFile(path.join(TICVAI, 'handoff', 'service-docs', 'op-release.json'), 'utf8')
  .catch(() => 'null'));
if (!bundle) {
  console.log('SKIP  no ticvai/handoff/service-docs/op-release.json beside the viewer');
  process.exit(0);
}
const SERVED = bundle.release;

// ── the package route ───────────────────────────────────────────────
const arch = await ticketText(TICVAI, { id: '27688', served: SERVED });
check('**#27688 is found by its OpenProject number, as ARCH-TESTS, with the bundle\'s text**',
  arch.found && arch.key === 'ARCH-TESTS' && arch.source === 'bundle' && arch.release === SERVED, JSON.stringify(arch).slice(0, 300));
check('the text is the release\'s pointer with the number filled in',
  arch.text?.includes('- Pull via ADAM: `/ticket 27688`') && arch.text.includes(`- Written at release \`${SERVED}\``)
  && !arch.text.includes('%ID%'), arch.text?.slice(0, 400));
check('and it is the corrected text (CHG-R8WFC-008), not r6\'s',
  arch.text?.includes('`TICVAI.Application/Features/<Module>/`') && !arch.text.includes('ModuleBoundaryTests.cs'));

// Every ticket of the bundle answers the same way: a rule, not a list of four.
let wrong = [];
let asked = 0;
for (const t of bundle.tickets) {
  const id = bundle.ids[t.key];
  if (!id) continue;
  asked += 1;
  const got = await ticketText(TICVAI, { id: String(id), served: SERVED });
  if (!got.found || got.key !== t.key || got.text !== t.pointer.replace(/%ID%/g, String(id))) wrong.push(t.key);
}
check(`every pushed ticket of the bundle (${asked}) answers with its own pointer`, asked > 1000 && !wrong.length,
  wrong.slice(0, 5).join(', '));
const fresh = bundle.tickets.find((t) => !bundle.ids[t.key]);
if (fresh) {
  const got = await ticketText(TICVAI, { id: '999999991', key: fresh.key, served: SERVED });
  check('a ticket made at this release (no number in the bundle yet) is found by the key its pointer names',
    got.found && got.key === fresh.key && got.text.includes('/ticket 999999991'), JSON.stringify(got).slice(0, 200));
}

const extras = JSON.parse(await readFile(path.join(TICVAI, 'docs', 'active', 'block-a-extra-tasks.json'), 'utf8')
  .catch(() => 'null'));
// Those in this release's plan: the file also holds tasks of later blocks, which are no ticket yet.
const planned = new Set(bundle.tickets.map((t) => t.key));
const extraKeys = (Array.isArray(extras) ? extras : extras?.tasks ?? []).map((e) => e?.key).filter((k) => planned.has(k));
const extraMiss = [];
for (const k of extraKeys) {
  const id = bundle.ids[k];
  const got = await ticketText(TICVAI, { id: id ? String(id) : '', key: k, served: SERVED });
  if (!got.found) extraMiss.push(k);
}
check(`every hand-written task in the plan (block-a-extra-tasks.json, ${extraKeys.length}) has the release's text`,
  extraKeys.length > 0 && !extraMiss.length, extraMiss.slice(0, 5).join(', '));

const later = await ticketText(TICVAI, { id: '27688', served: 'r99' });
check('a bundle from another release than the one served is not used: the plan\'s text is, at the served release',
  later.found && later.source === 'plan' && later.release === 'r99'
  && later.text.includes('- Written at release `r99`') && later.text.includes('**Done when:** a deliberate cross-module reference')
  && later.text.includes('Features/<Module>'), later.text?.slice(0, 500));
const nobody = await ticketText(TICVAI, { id: '1', served: SERVED });
check('a number that is no ticket of the plan is not found', nobody.found === false && /not a ticket/.test(nobody.why));
const demoRoot = (await stat(DEMO).catch(() => null)) ? DEMO : tmpdir();
const demo = await ticketText(demoRoot, { id: '27688', key: 'ARCH-TESTS', served: 'r1' });
check('a package with neither file answers not found, and the pull keeps OpenProject\'s text', demo.found === false);

// ── the pull ────────────────────────────────────────────────────────
function stub(description, textAnswer) {
  const wp = { key: '27688', subject: '[BE] Architecture tests for 17 modules: no module references another, and no module\'s SQL names another\'s schema',
    type: 'Task', status: 'Ready for QA', assignee: 'Pranay Shinde', project: 'TICVAI',
    url: 'http://op.test/work_packages/27688', description, comments: [] };
  return {
    projectId: async () => 'ticvai',
    packageJson: async (route, params) => {
      if (route !== 'ticket-text') return { ok: false, status: 404, data: null };
      const answer = await textAnswer(params);
      return answer ? { ok: true, status: 200, data: answer } : { ok: false, status: 404, data: null };
    },
    async service(route, { method = 'GET' } = {}) {
      if (method === 'GET' && /^\/api\/work-packages\/27688\?/.test(route)) {
        return { ok: true, status: 200, data: { workPackage: wp, touches: [], blockedBy: [], subtasks: [], partOf: null } };
      }
      return { ok: false, status: 404, data: { detail: 'not in the stub' } };
    },
  };
}
const fromPackage = async (params) => ({ project: 'ticvai', served: SERVED,
  ...(await ticketText(TICVAI, { id: params.id, key: params.key, served: SERVED })) });

async function pull(client) {
  const dir = await mkdtemp(path.join(tmpdir(), 'adam-ticket-text-'));
  try {
    const result = await BY_NAME.get('adam_pull').run(client, { key: '27688', dir });
    const folder = path.join(dir, '.adam', 'work', '27688');
    const readme = await readFile(path.join(folder, 'README.md'), 'utf8').catch(() => '');
    const saved = JSON.parse(await readFile(path.join(folder, 'ticket.json'), 'utf8').catch(() => '{}'));
    return { result, readme, saved };
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

const stale = await pull(stub(R6, fromPackage));
const desc = stale.readme.slice(stale.readme.indexOf('## Description'));
const LINE = `The text below is ${SERVED}'s; your OpenProject ticket still has the text from r6`;
check('**a started ticket with an older text: the README shows the release\'s text and says so in one line**',
  desc.startsWith(`## Description\n\n${LINE}`) && desc.includes('Features/<Module>'), desc.slice(0, 600));
check('the old text is not in the README', !stale.readme.includes('ModuleBoundaryTests.cs'));
check('ticket.json keeps both: OpenProject\'s description and the release\'s text, marked as different',
  stale.saved.workPackage?.description === R6 && stale.saved.releaseText?.release === SERVED
  && stale.saved.releaseText?.matchesOpenProject === false && stale.saved.releaseText?.openProjectRelease === 'r6',
  JSON.stringify(stale.saved.releaseText ?? null).slice(0, 300));

const current = await pull(stub(arch.text.replace(`\`${SERVED}\``, '`r7`'), fromPackage));
check('the same text written at another release: no line (only the release line differs)',
  !current.readme.includes('The text below is') && current.readme.includes('Features/<Module>'));
check('sameText ignores the release line and CRLF', sameText(arch.text.replace(/\n/g, '\r\n'), arch.text)
  && !sameText(R6, arch.text));

const plain = await pull(stub('Hand-written in OpenProject, before pointers.', fromPackage));
check('a ticket whose OpenProject text is no pointer: the release\'s text, and "an older text"',
  plain.readme.includes(`The text below is ${SERVED}'s; your OpenProject ticket still has an older text`)
  && plain.readme.includes('Features/<Module>'));
check('textNotice is empty when the texts agree', textNotice({ same: true, release: 'r8' }) === '');
check('a description the accounts service cut at its limit is the same text when the release\'s starts with it',
  sameText(arch.text.slice(0, 600), arch.text, true) && !sameText(R6.slice(0, 500), arch.text, true));

const older = await pull(stub(R6, async () => null));
check('an ADAM without the route (or a package without the files): OpenProject\'s description, as before',
  older.readme.includes('ModuleBoundaryTests.cs') && !older.readme.includes('The text below is')
  && older.saved.releaseText === undefined);

if (process.argv.includes('--show')) {
  console.log('\n----- README.md a pull of #27688 writes (stand-in OpenProject: the r6 description) -----\n');
  console.log(stale.readme);
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
