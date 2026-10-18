// The work under a ticket and the ticket above it, and where work starts when nobody names a ticket
// (CHG-ADM-006, lane A of the post-r6 plan: items 1 and 17 of the 18 October list).
//
//   node api/subtasks-check.mjs
//
// **Self-contained**, like release-check: its own stand-in OpenProject with the sub-task dataset (FAKE_SUBTASKS=1)
// and accounts service on ports 8891-8892, and a store in a temporary folder. Nothing else is touched.
//
// Found on live ADAM on 18 October: pulling #27735 listed none of its four sub-tasks, pulling #30681 did not name
// #27735, and the board filled sub-tasks from the held project read and showed 0 when that read failed. So the
// pull's sub-tasks are asserted **while the project read is failing**, and through each ticket's own `children`
// links when the instance refuses the parent filter (OpenProject 10 is from 2019).

import { spawn, spawnSync } from 'node:child_process';
import { mkdir, mkdtemp, readFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ViewerClient } from '../mcp/client.mjs';
import { BY_NAME } from '../mcp/tools.mjs';

const VIEWER_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORTS = { pms: 8891, api: 8892 };
const PMS = `http://127.0.0.1:${PORTS.pms}`;
const API = `http://127.0.0.1:${PORTS.api}`;
const EMAIL = 'harness.subtasks@softlabsgroup.com';
const PASSWORD = 'a-long-enough-passphrase';

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` — ${detail}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};

const T = await mkdtemp(path.join(tmpdir(), 'adam-subtasks-'));
const WORK = path.join(T, 'work');
const secret = spawnSync('python', ['-c', 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'],
  { encoding: 'utf8' }).stdout.trim();
const env = { ...process.env, TICVAI_DB: path.join(T, 'store.db'), TICVAI_SECRET_KEY: secret, FAKE_SUBTASKS: '1' };
const children = [];

function start(cmd, args, extra) {
  const child = spawn(cmd, args, { cwd: VIEWER_DIR, env: { ...env, ...extra }, windowsHide: true });
  let out = '';
  child.stdout.on('data', (c) => { out += c; });
  child.stderr.on('data', (c) => { out += c; });
  child.log = () => out;
  children.push(child);
  return child;
}

async function stop(child) {
  if (!child || child.exitCode !== null || child.signalCode !== null) return;
  const gone = new Promise((resolve) => child.once('exit', resolve));
  if (process.platform === 'win32') spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], { windowsHide: true });
  else child.kill();
  await Promise.race([gone, new Promise((resolve) => setTimeout(resolve, 5000))]);
}

async function waitFor(url, what) {
  for (let i = 0; i < 120; i += 1) {
    try {
      const r = await fetch(url);
      if (r.status < 500) return;
    } catch { /* not yet */ }
    await new Promise((resolve) => setTimeout(resolve, 250));
  }
  throw new Error(`${what} never answered at ${url}`);
}

const jar = { cookie: '' };
async function call(method, route, body) {
  const res = await fetch(`${API}${route}`, {
    method,
    headers: { 'content-type': 'application/json', ...(jar.cookie ? { cookie: jar.cookie } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) jar.cookie = set.split(';')[0];
  let data = null;
  try { data = await res.json(); } catch { /* empty */ }
  return { status: res.status, data };
}
const knob = (query) => fetch(`${PMS}/_break?${query}`).then((r) => r.ok, () => false);
const keys = (list) => (list ?? []).map((t) => t.key).join(' ');
const short = (value) => JSON.stringify(value ?? null).slice(0, 400);

try {
  start('node', ['api/fake-openproject.mjs'], { PORT: String(PORTS.pms) });
  start('python', ['-m', 'uvicorn', 'api.main:app', '--port', String(PORTS.api)], {});
  await waitFor(`${PMS}/_created`, 'the stand-in OpenProject');
  await waitFor(`${API}/api/health`, 'the accounts service');

  const boot = await call('POST', '/api/auth/bootstrap', { email: EMAIL, name: 'Harness Subtasks', password: PASSWORD });
  check('an admin exists', boot.status === 200, `${boot.status} ${short(boot.data)}`);
  check('and connects as the OpenProject user who holds the sub-task tickets',
    (await call('PUT', '/api/settings/openproject', { token: 'sub-key', endpoint: PMS })).status === 200);
  check('the ADAM project reads the harness OpenProject project',
    (await call('PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);

  // ── the whole-project read fails ──────────────────────────────────
  check('the stand-in can refuse the whole-project read', await knob('project=503'));
  const broken = await call('GET', '/api/board/mine?project_id=ticvai');
  check('the board still answers while the project read fails', broken.status === 200, `${broken.status} ${short(broken.data)}`);
  check('**and says the sub-tasks could not be read, rather than showing 0**',
    broken.data?.subtasksKnown === false && broken.data?.modulesKnown === false,
    `subtasksKnown=${broken.data?.subtasksKnown} modulesKnown=${broken.data?.modulesKnown}`);
  check('in the board order: the ticket, its open sub-tasks of yours, the next ticket, then one whose parent is not yours',
    keys(broken.data?.items) === '7400 7403 7404 7405 7410 7421', keys(broken.data?.items));
  check('**startHere is the first open sub-task of yours under the first workable ticket, even without the tree**',
    broken.data?.startHere?.key === '7403' && broken.data?.startHere?.partOf === '7400', short(broken.data?.startHere));

  const parent = await call('GET', '/api/work-packages/7400?project_id=ticvai');
  const subs = parent.data?.subtasks ?? [];
  check('**the work package lists every sub-task while the project read is failing**',
    parent.status === 200 && keys(subs) === '7401 7402 7403 7404 7405', `${parent.status} ${keys(subs)}`);
  check('each with its status and who holds it: a closed one and somebody else\'s included',
    subs[0]?.status === 'Closed' && subs[1]?.assignee === 'Hrushikant Patkar' && subs[2]?.assignee === 'Sub Tasker',
    short(subs.slice(0, 3)));
  check('two levels down, with the sub-task it hangs under',
    subs[4]?.depth === 2 && subs[4]?.parent === '7404' && subs[0]?.depth === 1 && subs[0]?.parent === '7400',
    short(subs.map((s) => `${s.key}:${s.depth}:${s.parent}`)));
  check('a ticket that hangs under nothing has partOf null', 'partOf' in (parent.data ?? {}) && parent.data.partOf === null,
    short(parent.data?.partOf));

  const leaf = await call('GET', '/api/work-packages/7405?project_id=ticvai');
  check('**a sub-task names its parent, with the parent\'s status and holder**',
    leaf.data?.partOf?.key === '7404' && leaf.data.partOf.subject === 'getCart' && leaf.data.partOf.status === 'New'
      && leaf.data.partOf.assignee === 'Sub Tasker' && leaf.data.partOf.read === true,
    short(leaf.data?.partOf));
  check('and has an empty list of sub-tasks, not a missing one', Array.isArray(leaf.data?.subtasks) && leaf.data.subtasks.length === 0,
    short(leaf.data?.subtasks));

  const yours = await call('GET', '/api/work-packages/7421?project_id=ticvai');
  check('**a sub-task of yours whose parent is somebody else\'s still names it**',
    yours.data?.partOf?.key === '7420' && yours.data.partOf.assignee === 'Hrushikant Patkar', short(yours.data?.partOf));
  const theirs = await call('GET', '/api/work-packages/7420?project_id=ticvai');
  check('and that parent lists it', keys(theirs.data?.subtasks) === '7421', keys(theirs.data?.subtasks));

  // ── the sub-task read itself fails, or the instance does not know the parent filter ──
  await knob('children=503');
  const unread = await call('GET', '/api/work-packages/7400?project_id=ticvai');
  check('**sub-tasks that could not be read are null, and the ticket still answers**',
    unread.status === 200 && unread.data?.subtasks === null && unread.data?.workPackage?.key === '7400',
    `${unread.status} ${short(unread.data?.subtasks)}`);
  await knob('children=400');
  const walked = await call('GET', '/api/work-packages/7400?project_id=ticvai');
  check('an instance that refuses the parent filter is walked through each ticket\'s children links',
    keys(walked.data?.subtasks) === '7401 7402 7403 7404 7405' && walked.data.subtasks[4]?.depth === 2,
    keys(walked.data?.subtasks));
  await knob('off=1');

  // An instance that accepts the parent filter and ignores it must not turn every ticket into a sub-task (I-1).
  await knob('ignoreparent=1');
  const ignored = await call('GET', '/api/work-packages/7400?project_id=ticvai');
  check('**a parent filter the instance ignores does not make unrelated tickets sub-tasks**',
    keys(ignored.data?.subtasks) === '7401 7402 7403 7404 7405', keys(ignored.data?.subtasks));
  await knob('off=1');

  // ── the project read works again ──────────────────────────────────
  const healed = await call('GET', '/api/board/mine?project_id=ticvai');
  const first = (healed.data?.items ?? []).find((t) => t.key === '7400');
  check('with the tree read, the board says so', healed.data?.subtasksKnown === true, String(healed.data?.subtasksKnown));
  check('and carries the sub-tasks in the same order as the pull', keys(first?.subtasks) === '7401 7402 7403 7404 7405',
    keys(first?.subtasks));
  check('startHere skips the closed sub-task and somebody else\'s, and takes yours',
    healed.data?.startHere?.key === '7403' && healed.data?.startHere?.partOf === '7400', short(healed.data?.startHere));
  const workable = await call('GET', '/api/board/mine?project_id=ticvai&only=workable');
  check('startHere is the same whatever `only` shows', workable.data?.startHere?.key === '7403', short(workable.data?.startHere));

  // Work that is finished is not started again (I-2): Ready for QA stays open in OpenProject.
  const move = (id, status) => fetch(`${PMS}/_status?id=${id}&status=${status}`).then((r) => r.ok);
  await move(7403, 9);
  const qaSub = await call('GET', '/api/board/mine?project_id=ticvai');
  check('**a sub-task waiting for QA is not where work starts: the next open one of yours is**',
    qaSub.data?.startHere?.key === '7404', short(qaSub.data?.startHere));
  await knob('project=503');
  const qaSubNoTree = await call('GET', '/api/board/mine?project_id=ticvai');
  check('and the same without the project tree', qaSubNoTree.data?.startHere?.key === '7404', short(qaSubNoTree.data?.startHere));
  await knob('off=1');
  await move(7400, 4);
  const heldFirst = await call('GET', '/api/board/mine?project_id=ticvai');
  check('**a first ticket that is on hold is not started: the next ticket of yours in board order is**',
    heldFirst.data?.startHere?.key === '7405' && heldFirst.data.startHere.partOf === '7404', short(heldFirst.data?.startHere));
  await move(7400, 9);
  const qaFirst = await call('GET', '/api/board/mine?project_id=ticvai');
  check('and so is one waiting for QA', qaFirst.data?.startHere?.key === '7405', short(qaFirst.data?.startHere));
  await move(7400, 1);
  await move(7403, 1);

  // ── the same through the connector ────────────────────────────────
  // Straight at the accounts service: the pull of a ticket with no links reads nothing from the package, so the
  // viewer is not needed. A ViewerClient signs in at /api/auth/login, which the accounts service answers itself.
  await mkdir(WORK, { recursive: true });
  const client = new ViewerClient({ base: API, project: 'ticvai', email: EMAIL, password: PASSWORD });
  const tool = (name, args) => BY_NAME.get(name).run(client, args);
  const readme = (k) => readFile(path.join(WORK, '.adam', 'work', k, 'README.md'), 'utf8').catch(() => '');

  const pulled = await tool('adam_pull', { key: '7400', dir: WORK });
  const r7400 = await readme('7400');
  check('**adam_pull of a ticket with sub-tasks lists them in README.md, with status and holder**',
    pulled.found && pulled.subtasks === 5 && r7400.includes('## Sub-tasks (5)')
      && r7400.includes('- #7402 createCart - New, Hrushikant Patkar\n')
      && r7400.includes('- #7405 getCart: expiry rule - New, Sub Tasker (under #7404)\n'),
    r7400.slice(0, 1200));
  await tool('adam_pull', { key: '7405', dir: WORK });
  check('**adam_pull of a sub-task names its parent**',
    (await readme('7405')).includes('- **Part of:** #7404 getCart (New, Sub Tasker)\n'), (await readme('7405')).slice(0, 600));
  await tool('adam_pull', { key: '7421', dir: WORK });
  check('and names a parent that is somebody else\'s',
    (await readme('7421')).includes('- **Part of:** #7420 Parent held by someone else (New, Hrushikant Patkar)\n'),
    (await readme('7421')).slice(0, 600));
  await knob('children=503');
  const lost = await tool('adam_pull', { key: '7400', dir: WORK });
  check('a sub-task read that fails is said in README.md',
    lost.subtasks === 'could not be read' && (await readme('7400')).includes('_Could not be read from OpenProject.'),
    JSON.stringify(lost).slice(0, 300));
  await knob('off=1');
  const shown = await tool('adam_board', { only: 'workable' });
  check('**adam_board hands on startHere, and counts the sub-tasks it read**',
    shown.startHere?.key === '7403' && shown.rows?.find((r) => r.ticket === '7400')?.subtasks === 5,
    JSON.stringify({ startHere: shown.startHere, rows: shown.rows }).slice(0, 400));
} catch (error) {
  check('the check ran to the end', false, error.stack ?? String(error));
  for (const child of children) console.log(child.log?.().slice(-2000));
} finally {
  for (const child of children) await stop(child);
  await rm(T, { recursive: true, force: true }).catch(() => {});
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
