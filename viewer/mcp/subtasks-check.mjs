#!/usr/bin/env node
// The pull's "Sub-tasks" and "Part of", and the board's sub-task count and startHere, as the connector writes them
// (CHG-ADM-006). No services: a stand-in client answers the accounts-service routes the tools ask, so the wording
// is held exactly. viewer/api/subtasks-check.mjs runs the same tools against the real service.
//
//   node viewer/mcp/subtasks-check.mjs

import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { BY_NAME } from './tools.mjs';

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` — ${detail}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};

/** A client whose accounts service answers from `routes`: [RegExp on "METHOD /path?query", data]. Anything else is
 *  a 404, which is how an ADAM without the pin or changes routes answers, and the pull goes on without them. */
function stub(routes) {
  return {
    projectId: async () => 'ticvai',
    packageJson: async () => ({ ok: false, status: 404, data: null }),
    async service(route, { method = 'GET' } = {}) {
      const hit = routes.find(([re]) => re.test(`${method} ${route}`));
      return hit ? { ok: true, status: 200, data: hit[1] } : { ok: false, status: 404, data: { detail: 'not in the stub' } };
    },
  };
}

const ticket = (key, subject) => ({
  key, subject, type: 'Task', status: 'New', assignee: 'Sub Tasker', project: 'TICVAI (harness)',
  url: `http://op.test/work_packages/${key}`, description: 'The work.', comments: [],
});
const sub = (key, subject, status, assignee, depth, parent) => ({
  key, subject, status, assignee, depth, parent, percentDone: 0, dueDate: null, url: `http://op.test/work_packages/${key}`,
});
const SUBS = [
  sub('7401', 'claimCart', 'Closed', 'Sub Tasker', 1, '7400'),
  sub('7402', 'createCart', 'New', 'Hrushikant Patkar', 1, '7400'),
  sub('7403', 'extendCart', 'New', 'Sub Tasker', 1, '7400'),
  sub('7404', 'getCart', 'New', 'Sub Tasker', 1, '7400'),
  sub('7405', 'getCart: expiry rule', 'New', '', 2, '7404'),
];
const START = { key: '7403', subject: 'extendCart', status: 'New', partOf: '7400', partOfSubject: 'OrderService' };

async function pull(answer, key) {
  const dir = await mkdtemp(path.join(tmpdir(), 'adam-subtasks-pure-'));
  try {
    const result = await BY_NAME.get('adam_pull').run(
      stub([[new RegExp(`^GET /api/work-packages/${key}\\?`), answer]]), { key, dir });
    const folder = path.join(dir, '.adam', 'work', key);
    const readme = await readFile(path.join(folder, 'README.md'), 'utf8').catch(() => '');
    const saved = JSON.parse(await readFile(path.join(folder, 'ticket.json'), 'utf8').catch(() => '{}'));
    return { result, readme, saved };
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

// ── a ticket with sub-tasks ─────────────────────────────────────────
const parent = await pull({ workPackage: ticket('7400', 'OrderService: claimCart, createCart, extendCart, getCart'),
  touches: [], blockedBy: [], subtasks: SUBS, partOf: null }, '7400');
const at = parent.readme.indexOf('## Sub-tasks (5)');
check('**a pull lists the sub-tasks, above the description**',
  at > 0 && at < parent.readme.indexOf('## Description'), parent.readme.slice(0, 900));
check('each with its status and who holds it, somebody else\'s included',
  parent.readme.includes('- #7402 createCart - New, Hrushikant Patkar\n'), parent.readme.slice(at, at + 600));
check('a closed one is listed as closed', parent.readme.includes('- #7401 claimCart - Closed, Sub Tasker\n'));
check('one two levels down names the sub-task it hangs under, and an unassigned one says so',
  parent.readme.includes('- #7405 getCart: expiry rule - New, unassigned (under #7404)\n'), parent.readme.slice(at, at + 600));
const order = parent.readme.split('\n').filter((l) => /^- #74\d\d /.test(l)).map((l) => l.slice(3, 7)).join(' ');
check('in the order ADAM gave, never re-sorted', order === '7401 7402 7403 7404 7405', order);
check('the section says to pull one before working on it',
  parent.readme.includes('The work under this ticket, in the order it is done. Pull one (adam_pull with its number) before you work on it.'));
check('ticket.json keeps them', (parent.saved.subtasks ?? []).length === 5, JSON.stringify(parent.saved.subtasks ?? null).slice(0, 200));
check('the answer counts them and says where they are',
  parent.result.subtasks === 5 && /"Sub-tasks"/.test(parent.result.next ?? ''),
  JSON.stringify({ subtasks: parent.result.subtasks, next: parent.result.next }));
check('a ticket under nothing has no Part of line', !parent.readme.includes('**Part of:**'));

// ── a sub-task ──────────────────────────────────────────────────────
const leaf = await pull({ workPackage: ticket('7405', 'getCart: expiry rule'), touches: [], blockedBy: [], subtasks: [],
  partOf: { key: '7404', subject: 'getCart', status: 'New', assignee: 'Sub Tasker', url: 'http://op.test/work_packages/7404', read: true } }, '7405');
check('**a sub-task names its parent, with its status and who holds it**',
  leaf.readme.includes('- **Part of:** #7404 getCart (New, Sub Tasker)\n'), leaf.readme.slice(0, 700));
check('its answer says so', leaf.result.partOf === '7404' && /"Part of"/.test(leaf.result.next ?? ''),
  JSON.stringify({ partOf: leaf.result.partOf, next: leaf.result.next }));
check('nothing under it, no Sub-tasks section', !leaf.readme.includes('## Sub-tasks'));
const unreadParent = await pull({ workPackage: ticket('7405', 'getCart: expiry rule'), touches: [], blockedBy: [], subtasks: [],
  partOf: { key: '7404', subject: 'getCart', status: '', assignee: '', url: '', read: false } }, '7405');
check('a parent that could not be read is still named, and says so',
  unreadParent.readme.includes('- **Part of:** #7404 getCart (could not be read)\n'), unreadParent.readme.slice(0, 700));

// ── sub-tasks that could not be read, and an older ADAM ─────────────
const failed = await pull({ workPackage: ticket('7400', 'OrderService'), touches: [], blockedBy: [], subtasks: null, partOf: null }, '7400');
check('**sub-tasks that could not be read are said, not shown as none**',
  failed.readme.includes('## Sub-tasks\n\n_Could not be read from OpenProject. Open the ticket\'s link above to see them, and pull again later._\n')
    && failed.result.subtasks === 'could not be read',
  failed.readme.slice(0, 900));
const old = await pull({ workPackage: ticket('7400', 'OrderService'), touches: [], blockedBy: [] }, '7400');
check('an ADAM from before sub-tasks gets no section and no error', old.result.found === true && !old.readme.includes('## Sub-tasks'),
  JSON.stringify(old.result).slice(0, 300));

// ── the board ───────────────────────────────────────────────────────
const row = (key, subject, subtasks) => ({ key, subject, status: 'New', buildOrder: null, module: null, subtasks, blockedBy: [] });
const board = (extra) => BY_NAME.get('adam_board').run(stub([[/^GET \/api\/board\/mine\?/, {
  total: 2, workable: 2, blocked: 0, startHere: START,
  items: [row('7400', 'OrderService', []), row('7403', 'extendCart', [])], ...extra,
}]]), { only: 'workable' });
const unknown = await board({ subtasksKnown: false, modulesKnown: false });
check('**the board shows ? for sub-tasks it could not read, not 0**',
  (unknown.rows ?? []).length === 2 && unknown.rows.every((r) => r.subtasks === '?'), JSON.stringify(unknown.rows));
check('and says so in a note', /could not be read/.test(unknown.subtaskNote ?? ''), String(unknown.subtaskNote));
check('the subtasks column is shown', (unknown.columns ?? []).includes('subtasks'), JSON.stringify(unknown.columns));
const known = await board({ subtasksKnown: true, items: [row('7400', 'OrderService', SUBS)] });
check('a board that read them counts them, with no note', known.rows?.[0]?.subtasks === 5 && !('subtaskNote' in known),
  JSON.stringify({ rows: known.rows, note: known.subtaskNote }));
check('**the board hands on startHere: the ticket /ticket with no number starts**',
  known.startHere?.key === '7403' && known.startHere?.partOf === '7400', JSON.stringify(known.startHere));

// ── an older /ticket that calls adam_pull with no key ───────────────
const dir = await mkdtemp(path.join(tmpdir(), 'adam-subtasks-board-'));
try {
  const whole = await BY_NAME.get('adam_pull').run(stub([[/^GET \/api\/board\/mine\?/, { total: 0, items: [], startHere: START }]]), { dir });
  check('a whole-board pull hands on startHere too', whole.startHere?.key === '7403', JSON.stringify(whole).slice(0, 300));
} finally {
  await rm(dir, { recursive: true, force: true });
}

// ── what an agent reads about it ────────────────────────────────────
const said = (name) => BY_NAME.get(name).description;
check('adam_board says what startHere is, and never to ask for a number',
  /startHere/.test(said('adam_board')) && /never ask for a number/i.test(said('adam_board')), said('adam_board'));
check('adam_pull says README.md has "Sub-tasks" and "Part of"',
  /"Sub-tasks"/.test(said('adam_pull')) && /"Part of"/.test(said('adam_pull')), said('adam_pull'));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
