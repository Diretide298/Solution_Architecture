// Release tags, ticket pins, the diff since a pin, and change request intake
// (plan item 1D: council C2, C9 and C8).
//
//   node api/release-check.mjs
//
// **Self-contained.** The thing under test is the viewer deciding which state of
// a package to serve and the accounts service recording what a pull saw, so the
// check builds its own package — a throwaway git repository with two release
// tags, r1 and r2, and an uncommitted edit on top — and starts its own stand-in
// OpenProject, accounts service and viewer against it, on ports of their own.
// It restarts the viewer three times, the way a deploy does: serving the working
// tree, then r1, then r2. Nothing outside the temporary folder is touched.
//
// What it holds:
//   - the viewer serves the newest tag, not the working tree, from an export
//     (and the second export links the files the first already holds);
//   - a pull records the tag in force as the ticket's pin, and only the first;
//   - once the served tag moves on, a pull keeps the pinned files, writes the
//     diff, and a breaking change in docs/active/breaking-changes.yaml makes the
//     re-pin required for the producer and the consumer — and nobody else;
//   - adam_repin moves the pin and pulls again;
//   - change request intake: the rules, the defaults, the release it was raised
//     at, the intake route, the ticket text, and the release notes between tags.
//
// Needs python with the service's requirements, git and node 22 — the same
// things the other checks need.

import { spawn, spawnSync, execFileSync } from 'node:child_process';
import { mkdtemp, mkdir, readFile, readdir, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ViewerClient } from '../mcp/client.mjs';
import { BY_NAME } from '../mcp/tools.mjs';

const VIEWER_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORTS = { pms: 8871, api: 8872, viewer: 8873 };
const PMS = `http://127.0.0.1:${PORTS.pms}`;
const API = `http://127.0.0.1:${PORTS.api}`;
const VIEWER = `http://127.0.0.1:${PORTS.viewer}`;
const EMAIL = 'harness.release@softlabsgroup.com';
const PASSWORD = 'a-long-enough-passphrase';

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` — ${detail}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};

const T = await mkdtemp(path.join(tmpdir(), 'adam-release-'));
const REPO = path.join(T, 'repo');
const PKG = path.join(REPO, 'pkg');
const RELEASES = path.join(T, '.releases', 'ticvai');
const STORE = path.join(T, 'store.db');
const WORK = path.join(T, 'work');
const children = [];

function git(...args) {
  return execFileSync('git', ['-c', 'user.name=Harness', '-c', 'user.email=harness@example.com', ...args],
    { cwd: REPO, encoding: 'utf8', env: { ...process.env, ...gitDate } });
}
let gitDate = {};

// ── the package, at two releases ──────────────────────────────────────

const screens = (purpose) => `platform:
  code: P01
  name: Greenleaf Web
screens:
  - id: WEB-001
    name: Borrow a book
    purpose: ${purpose}
    apis:
      - operationId: getBook
      - operationId: borrowBook
    states: { loading: spinner, empty: none, error: message }
  - id: WEB-002
    name: Member profile
    purpose: A member sees their own details.
    apis:
      - operationId: getMember
    states: { loading: spinner, empty: none, error: message }
`;

const contract = await readFile(path.join(VIEWER_DIR, '..', 'demo', 'package', 'contracts', 'lending.yaml'), 'utf8');
await mkdir(path.join(PKG, 'contracts'), { recursive: true });
await mkdir(path.join(PKG, 'screens'), { recursive: true });
await mkdir(path.join(PKG, 'repos', 'ticvai-docs', 'project-bible'), { recursive: true });
await mkdir(path.join(PKG, 'repos', 'ticvai-docs', '.github', 'workflows'), { recursive: true });
await writeFile(path.join(PKG, 'contracts', 'lending.yaml'), contract);
await writeFile(path.join(PKG, 'screens', 'P01-web.yaml'), screens('A member borrows a book from the shelf.'));
// A mirror, the way repos/ holds them: its copy of the package is left out of
// an export and its workflow is kept.
await writeFile(path.join(PKG, 'repos', 'ticvai-docs', 'project-bible', 'copy.md'), '# a mirrored copy\n');
await writeFile(path.join(PKG, 'repos', 'ticvai-docs', '.github', 'workflows', 'ci.yml'), 'name: ci\non: [push]\njobs: {}\n');
await writeFile(path.join(PKG, 'repos', 'ticvai-docs', 'package.json'), '{ "name": "mirror" }\n');

git('init', '-q');
git('add', '-A');
gitDate = { GIT_COMMITTER_DATE: '2026-01-05T10:00:00Z', GIT_AUTHOR_DATE: '2026-01-05T10:00:00Z' };
git('commit', '-q', '-m', 'first release');
git('tag', '-a', 'r1', '-m', 'r1');

// r2: borrowBook's loan is 21 days now, the borrow screen says so, and the
// change is declared breaking.
await writeFile(path.join(PKG, 'contracts', 'lending.yaml'), contract
  .replace(/summary: Borrow a book(\r?\n)/, 'summary: Borrow a book for 21 days$1')
  .replace('due **14 days** after', 'due **21 days** after'));
await writeFile(path.join(PKG, 'screens', 'P01-web.yaml'), screens('A member borrows a book; the loan is for 21 days.'));
await mkdir(path.join(PKG, 'docs', 'active'), { recursive: true });
await writeFile(path.join(PKG, 'docs', 'active', 'breaking-changes.yaml'), `- id: BC-001
  contract: lending
  operation: borrowBook
  reason: The loan period moves from 14 to 21 days, and dueAt with it.
  approved-by: Harness Architect
`);
git('add', '-A');
gitDate = { GIT_COMMITTER_DATE: '2099-01-05T10:00:00Z', GIT_AUTHOR_DATE: '2099-01-05T10:00:00Z' };
git('commit', '-q', '-m', 'second release');
git('tag', '-a', 'r2', '-m', 'r2');
// And an edit nobody has released, which must never be served while a tag is.
await writeFile(path.join(PKG, 'contracts', 'lending.yaml'), contract
  .replace('summary: List books with how many copies are on the shelf', 'summary: UNRELEASED EDIT'));

await writeFile(path.join(T, 'projects.json'), JSON.stringify({
  default: 'ticvai',
  projects: [{ id: 'ticvai', name: 'TICVAI', root: './repo/pkg', contracts: 'contracts', active: true }],
}, null, 2));

// ── the services ──────────────────────────────────────────────────────

const key = spawnSync('python', ['-c', 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'],
  { encoding: 'utf8' }).stdout.trim();
const env = {
  ...process.env,
  TICVAI_DB: STORE,
  TICVAI_SECRET_KEY: key,
  TICVAI_PROJECTS: path.join(T, 'projects.json'),
  TICVAI_AUTH: API,
};
delete env.ADAM_PACKAGE_REF;

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

function start(cmd, args, extra, log) {
  const child = spawn(cmd, args, { cwd: VIEWER_DIR, env: { ...env, ...extra }, windowsHide: true });
  let out = '';
  child.stdout.on('data', (c) => { out += c; });
  child.stderr.on('data', (c) => { out += c; });
  child.log = () => out;
  children.push(child);
  return child;
}

async function stop(child) {
  // A child killed by a signal has a signalCode and no exitCode, and its exit
  // has already been announced: waiting for it again waits for ever.
  if (!child || child.exitCode !== null || child.signalCode !== null) return;
  const gone = new Promise((resolve) => child.once('exit', resolve));
  // The whole tree on Windows: `python` can be a launcher with the interpreter
  // under it, and killing the launcher leaves the port held.
  if (process.platform === 'win32') spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], { windowsHide: true });
  else child.kill();
  await Promise.race([gone, new Promise((resolve) => setTimeout(resolve, 5000))]);
}

let viewer = null;
async function startViewer(ref) {
  await stop(viewer);
  viewer = start(process.execPath, ['server.mjs', '--port', String(PORTS.viewer), '--host', '127.0.0.1'],
    ref ? { ADAM_PACKAGE_REF: ref } : {});
  await waitFor(`${VIEWER}/login.html`, 'the viewer');
}

let client = null;
const tool = (name, args) => BY_NAME.get(name).run(client, args);

try {
  start('node', ['api/fake-openproject.mjs'], { PORT: String(PORTS.pms) });
  start('python', ['-m', 'uvicorn', 'api.main:app', '--port', String(PORTS.api)], {});
  await waitFor(`${PMS}/_created`, 'the stand-in OpenProject');
  await waitFor(`${API}/api/health`, 'the accounts service');

  const jar = { cookie: '' };
  const call = async (method, route, body) => {
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
  };

  const boot = await call('POST', '/api/auth/bootstrap', { email: EMAIL, name: 'Harness Release', password: PASSWORD });
  check('an admin exists', boot.status === 200, `${boot.status} ${JSON.stringify(boot.data)}`);
  check('and connects to the stand-in OpenProject',
    (await call('PUT', '/api/settings/openproject', { token: 'harness-key', endpoint: PMS })).status === 200);
  check('the ADAM project reads the harness OpenProject project',
    (await call('PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);

  // 7001 is the consumer (its screen calls borrowBook), 7002 the producer (linked
  // to the operation), 7003 is linked to a screen nothing changed in.
  for (const [kind, id, k] of [
    ['screen', 'WEB-001', '7001'], ['operation', 'lending#borrowBook', '7002'], ['screen', 'WEB-002', '7003'],
  ]) {
    const made = await call('POST', '/api/links', { target_kind: kind, target_id: id, external_key: k, project_id: 'ticvai' });
    check(`#${k} is linked to ${kind} ${id}`, made.status === 200, `${made.status} ${JSON.stringify(made.data)}`);
  }

  // ── the working tree, while there is no tag in force ──────────────
  await startViewer('working');
  client = new ViewerClient({ base: VIEWER, project: 'ticvai', email: EMAIL, password: PASSWORD });
  const workingRelease = await client.packageJson('release');
  check('packageRef working serves the working tree, and says so',
    workingRelease.data?.mode === 'working' && workingRelease.data?.tag === null,
    JSON.stringify(workingRelease.data));
  check('and lists both tags it could serve',
    String(workingRelease.data?.releases?.map((r) => r.tag)) === 'r1,r2', JSON.stringify(workingRelease.data?.releases));
  const noPin = await call('POST', '/api/work-packages/7001/pin', { project_id: 'ticvai', reason: 'pull' });
  check('a pull while the working tree is served records no pin, and says why',
    noPin.status === 200 && noPin.data?.recorded === false && /working tree/.test(noPin.data?.note ?? ''),
    JSON.stringify(noPin.data));
  const unreleased = await tool('adam_contract', { name: 'lending' });
  check('the working tree is what was served: the unreleased edit shows',
    unreleased.contract?.operations?.some((o) => o.summary === 'UNRELEASED EDIT'), JSON.stringify(unreleased).slice(0, 200));

  // ── r1 ───────────────────────────────────────────────────────────
  await startViewer('r1');
  client = new ViewerClient({ base: VIEWER, project: 'ticvai', email: EMAIL, password: PASSWORD });
  const r1 = await client.packageJson('release');
  check('packageRef r1 serves r1', r1.data?.mode === 'tag' && r1.data?.tag === 'r1', JSON.stringify(r1.data));
  const served1 = JSON.parse(await readFile(path.join(RELEASES, 'served.json'), 'utf8'));
  check('and writes served.json, which is how the accounts service knows', served1.tag === 'r1' && served1.mode === 'tag');
  const atR1 = await tool('adam_contract', { name: 'lending', operation: 'borrowBook' });
  check('the operation served is r1\'s', atR1.operation?.title === 'Borrow a book', atR1.operation?.title);
  const r1Tree = path.join(RELEASES, 'r1');
  check('r1 is an export of the tag, not the working tree',
    !(await readFile(path.join(r1Tree, 'contracts', 'lending.yaml'), 'utf8')).includes('UNRELEASED EDIT'));
  check('an export keeps a mirror\'s workflow',
    Boolean(await stat(path.join(r1Tree, 'repos', 'ticvai-docs', '.github', 'workflows', 'ci.yml')).catch(() => null)));
  check('and leaves its copy of the package out, keeping the folder',
    (await readdir(path.join(r1Tree, 'repos', 'ticvai-docs', 'project-bible')).catch(() => null))?.length === 0);

  await mkdir(WORK, { recursive: true });
  const first = await tool('adam_pull', { key: '7001', dir: WORK });
  check('the first pull pins the ticket at r1',
    first.found && first.release?.current === 'r1' && first.release?.pinned === 'r1' && !first.release?.stale,
    JSON.stringify(first.release ?? first));
  const readme1 = await readFile(path.join(WORK, '.adam', 'work', '7001', 'README.md'), 'utf8');
  check('and README.md names the release', /\*\*Release:\*\* r1 \(pinned by this pull\)/.test(readme1), readme1.slice(0, 400));
  const file1 = JSON.parse(await readFile(path.join(WORK, '.adam', 'work', '7001', 'screen-WEB-001.json'), 'utf8'));
  check('and each linked file says which release it is', file1.release === 'r1', JSON.stringify(file1).slice(0, 200));
  const again = await call('POST', '/api/work-packages/7001/pin', { project_id: 'ticvai', reason: 'pull' });
  check('a second pull at the same release records nothing new', again.data?.recorded === false && again.data?.pin?.tag === 'r1');
  for (const k of ['7002', '7003']) await tool('adam_pull', { key: k, dir: WORK });

  // A request raised from a ticket while it is pinned at r1 records r1.
  const gap = await tool('adam_draft_change', {
    kind: 'operation', target: 'lending#borrowBook', title: 'dueAt is not in the response',
    problem: 'The loan says it is due in 14 days but the response carries no dueAt field to show.',
    ticket: '7002',
  });
  check('a developer drafts a gap from /ticket; source defaults to developer and the ref to the ticket',
    gap.ok && gap.preview?.source === 'developer' && gap.preview?.source_ref === '#7002', JSON.stringify(gap).slice(0, 300));
  check('and the draft records the release the ticket is pinned at', gap.preview?.raised_tag === 'r1', gap.preview?.raised_tag);
  const filed = await tool('adam_raise_change', { draft: gap.draft });
  check('filed, it carries its intake',
    filed.filed && filed.change?.source === 'developer' && filed.change?.raisedTag === 'r1', JSON.stringify(filed.change ?? filed).slice(0, 300));

  // ── r2, the way a deploy moves it on ─────────────────────────────
  await startViewer(null);
  client = new ViewerClient({ base: VIEWER, project: 'ticvai', email: EMAIL, password: PASSWORD });
  const r2 = await client.packageJson('release');
  check('with no packageRef the newest tag, r2, is served', r2.data?.mode === 'tag' && r2.data?.tag === 'r2', JSON.stringify(r2.data));
  const listed = await tool('adam_contract', { name: 'lending' });
  check('and not the working tree', !listed.contract?.operations?.some((o) => o.summary === 'UNRELEASED EDIT'));
  const manifest = JSON.parse(await readFile(path.join(RELEASES, 'r2.json'), 'utf8'));
  check('r2\'s export links the files r1 already holds instead of copying them',
    manifest.counts?.linked > 0 && manifest.counts?.written > 0, JSON.stringify(manifest.counts));

  const badTag = await client.packageJson('release-diff', { from: 'banana', to: 'r2' });
  check('a diff between things that are not tags is a 400', badTag.status === 400);
  const noTag = await client.packageJson('release-diff', { from: 'r9', to: 'r2' });
  check('and one with a tag that does not exist is a 409 that says so', noTag.status === 409 && /r9/.test(noTag.data?.error ?? ''));

  const consumer = await tool('adam_pull', { key: '7001', dir: WORK });
  check('a pull after the release moved on says the spec changed',
    consumer.release?.stale === true && consumer.release?.pinned === 'r1' && consumer.release?.current === 'r2',
    JSON.stringify(consumer.release));
  check('and the breaking change makes the re-pin required for the consumer',
    consumer.release?.repinRequired === true && consumer.release?.breaking?.[0] === 'BC-001 (consumer)',
    JSON.stringify(consumer.release));
  check('and the next step says so, as required', /requires this ticket to move off r1/.test(consumer.next ?? ''), consumer.next);
  const dir1 = path.join(WORK, '.adam', 'work', '7001');
  const readme2 = await readFile(path.join(dir1, 'README.md'), 'utf8');
  check('README.md has the section, with r1 and r2 in its title',
    readme2.includes('## Spec changed since you pulled at r1 (now r2)'), readme2.slice(0, 600));
  check('and marks the re-pin required, naming the change and the role',
    /Re-pin required/.test(readme2) && /BC-001/.test(readme2) && /\*\*consumer\*\*, via screen WEB-001/.test(readme2));
  const pinnedScreen = JSON.parse(await readFile(path.join(dir1, 'screen-WEB-001.json'), 'utf8'));
  check('the linked file stays at the pinned release until the change is taken',
    pinnedScreen.release === 'r1' && pinnedScreen.screen?.purpose === 'A member borrows a book from the shelf.',
    JSON.stringify(pinnedScreen).slice(0, 300));
  const specDiff = await readFile(path.join(dir1, 'spec-diff.md'), 'utf8').catch(() => '');
  check('spec-diff.md holds the diff of what the developer was handed',
    /-\s+"purpose": "A member borrows a book from the shelf\."/.test(specDiff)
      && /\+\s+"purpose": "A member borrows a book; the loan is for 21 days\."/.test(specDiff), specDiff.slice(0, 800));

  const producer = await tool('adam_pull', { key: '7002', dir: WORK });
  check('the producer of the operation must re-pin too',
    producer.release?.repinRequired === true && producer.release?.breaking?.[0] === 'BC-001 (producer)',
    JSON.stringify(producer.release));
  const opDiff = await readFile(path.join(WORK, '.adam', 'work', '7002', 'spec-diff.md'), 'utf8');
  check('and its diff shows the operation\'s summary moving',
    /-\s+"title": "Borrow a book",/.test(opDiff) && /\+\s+"title": "Borrow a book for 21 days",/.test(opDiff), opDiff.slice(0, 800));

  const bystander = await tool('adam_pull', { key: '7003', dir: WORK });
  check('a ticket whose artefacts did not change is told the release moved, with nothing changed',
    bystander.release?.stale === true && bystander.release?.changed === 0 && bystander.release?.repinRequired === false,
    JSON.stringify(bystander.release));
  const readme3 = await readFile(path.join(WORK, '.adam', 'work', '7003', 'README.md'), 'utf8');
  check('and not told to re-pin', !/Re-pin required/.test(readme3) && /None of the artefacts/.test(readme3));

  const board = await tool('adam_board', {});
  const row = (k) => board.rows?.find((r) => String(r.ticket) === k);
  check('the board has a release column once a release is served', board.columns?.includes('release'), JSON.stringify(board.columns));
  check('and shows a pin behind the served release as r1 -> r2', row('7001')?.release === 'r1 -> r2', JSON.stringify(row('7001')));
  check('and a ticket never pulled as blank', row('7004')?.release === '', JSON.stringify(row('7004')));

  const moved = await tool('adam_repin', { key: '7001', dir: WORK, breaking: true, note: 'BC-001' });
  check('adam_repin moves the pin to r2', moved.ok && moved.moved && moved.pinned === 'r2' && moved.from === 'r1', JSON.stringify(moved));
  check('and pulls again, so the files are r2', moved.pulled?.release?.stale === false, JSON.stringify(moved.pulled));
  const nowScreen = JSON.parse(await readFile(path.join(dir1, 'screen-WEB-001.json'), 'utf8'));
  check('the linked file is the new release now',
    nowScreen.release === 'r2' && /21 days/.test(nowScreen.screen?.purpose ?? ''), JSON.stringify(nowScreen).slice(0, 200));
  const history = await call('GET', '/api/work-packages/7001/pin?project_id=ticvai');
  check('the pin history keeps the pull and the forced move',
    history.data?.log?.[0]?.reason === 'breaking' && history.data?.log?.[0]?.from === 'r1'
      && history.data?.log?.[1]?.reason === 'pull', JSON.stringify(history.data?.log));
  const twice = await tool('adam_repin', { key: '7001' });
  check('re-pinning at the served release changes nothing and says so', twice.ok && !twice.moved && /Already pinned/.test(twice.note ?? ''));
  const nonsense = await call('POST', '/api/work-packages/7001/pin', { project_id: 'ticvai', reason: 'because' });
  check('a pin reason outside pull, accept and breaking is refused', nonsense.status === 400);

  // ── change request intake ────────────────────────────────────────
  const raise = (fields) => call('POST', '/api/changes', {
    project_id: 'ticvai', target_kind: 'operation', target_id: 'lending#borrowBook',
    title: 'Loan period', problem: 'The loan period changed and the notices still say 14 days.', ...fields,
  });
  let r = await raise({ source: 'minutes', source_ref: 'MoM 30 Sep, item 4' });
  check('a change from minutes without the client\'s sign-off is refused',
    r.status === 400 && /sign-off/.test(r.data?.detail ?? ''), JSON.stringify(r.data));
  r = await raise({ source: 'minutes' });
  check('any source needs the line that finds it again', r.status === 400 && /source_ref/.test(r.data?.detail ?? ''));
  r = await raise({ source: 'developer' });
  check('except a developer\'s, raised outside a ticket: the row already says who and when',
    r.status === 200 && r.data?.change?.source === 'developer' && r.data?.change?.sourceRef === '', JSON.stringify(r.data));
  await call('POST', `/api/changes/${r.data?.change?.id}/resolve`, { project_id: 'ticvai', status: 'rejected', resolution: 'Harness.' });
  r = await raise({ source: 'answer', source_ref: 'Q-12', contract_impact: 'breaking' });
  check('a breaking contract change needs an approver', r.status === 400 && /approver/.test(r.data?.detail ?? ''));
  r = await raise({ source: 'design', source_ref: 'board 3', triage: 'urgent' });
  check('a triage class outside the three is refused', r.status === 400);
  r = await raise({});
  check('a request with no intake still files, as before 1 October', r.status === 200 && r.data?.change?.source === '');
  const legacy = r.data.change.id;
  r = await raise({
    source: 'Minutes', source_ref: 'MoM 30 Sep, item 4', client_signoff: 'Allam, email 30 Sep',
    approver: 'Harness Architect', triage: 'scope', when: 'now', contract_impact: 'breaking',
    effort_points: 3.5, artefacts: ['screen:WEB-001', 'screen:WEB-001', 'table:lending.loan'], ticket: '7001',
  });
  const full = r.data?.change ?? {};
  check('a full intake is recorded', r.status === 200 && full.source === 'minutes' && full.clientSignoff === 'Allam, email 30 Sep'
    && full.triage === 'scope' && full.when === 'now' && full.contractImpact === 'breaking' && full.effortPoints === 3.5
    && full.approver === 'Harness Architect', JSON.stringify(full));
  check('with its artefacts listed once each', String(full.artefacts) === 'screen:WEB-001,table:lending.loan', JSON.stringify(full.artefacts));
  check('and the release it was raised at: the ticket\'s pin', full.raisedTag === 'r2', full.raisedTag);

  const later = await call('POST', `/api/changes/${legacy}/intake`, { project_id: 'ticvai', triage: 'clarification', when: 'later' });
  check('the intake can be completed after filing', later.status === 200 && later.data?.change?.triage === 'clarification'
    && later.data?.change?.when === 'later', JSON.stringify(later.data));
  const badLater = await call('POST', `/api/changes/${legacy}/intake`, { project_id: 'ticvai', source: 'minutes', source_ref: 'MoM 1 Oct' });
  check('and the same rules hold when it is', badLater.status === 400 && /sign-off/.test(badLater.data?.detail ?? ''));

  const ticket = await call('POST', `/api/changes/${full.id}/ticket/preview`, { project_id: 'ticvai' });
  const text = ticket.data?.willCreate?.description ?? '';
  check('the ticket filed from a request carries its intake',
    ticket.status === 200 && /\*\*Intake\*\*/.test(text) && /Client sign-off: Allam/.test(text) && /Effort change: \+3\.5 points/.test(text),
    `${ticket.status} ${text.slice(-400)}`);

  // ── release notes ────────────────────────────────────────────────
  const settle = (id, status, resolution = '') => call('POST', `/api/changes/${id}/resolve`, { project_id: 'ticvai', status, resolution });
  check('a request is accepted', (await settle(full.id, 'accepted')).status === 200);
  check('another is done', (await settle(filed.change.id, 'done')).status === 200);
  check('one is rejected, which is not in any release', (await settle(legacy, 'rejected', 'Not a change.')).status === 200);
  const early = await raise({ source: 'audit', source_ref: 'R016' });
  await settle(early.data.change.id, 'accepted');
  // Settled before r1 was tagged: the store is the only way to make it older.
  execFileSync('python', ['-c', `import sqlite3; c = sqlite3.connect(r"${STORE}"); `
    + `c.execute("UPDATE change_request SET resolved_at = '2025-12-01T00:00:00+00:00' WHERE number = ${early.data.change.number}"); c.commit()`]);

  const notes = await call('GET', '/api/changes/release-notes?project_id=ticvai&from=r1&to=r2');
  const ids = (notes.data?.items ?? []).map((c) => c.id).sort();
  check('the release note from r1 to r2 is what was settled in between',
    String(ids) === String([full.id, filed.change.id].sort()), JSON.stringify(ids));
  check('with a markdown note naming them',
    notes.data?.markdown?.startsWith('# Release r2 (since r1)') && notes.data.markdown.includes(full.id), notes.data?.markdown);
  const upToR1 = await call('GET', '/api/changes/release-notes?project_id=ticvai&to=r1');
  check('and up to r1, only what was settled before it', upToR1.data?.items?.length === 1
    && upToR1.data.items[0].id === early.data.change.id, JSON.stringify(upToR1.data?.items?.map((c) => c.id)));
  const served = await call('GET', '/api/changes/release-notes?project_id=ticvai');
  check('with no tags given, everything up to the release served', served.data?.to?.tag === 'r2' && served.data?.total === 3);
  check('an earlier `to` than `from` is refused',
    (await call('GET', '/api/changes/release-notes?project_id=ticvai&from=r2&to=r1')).status === 400);
  check('and a tag ADAM has not seen is a 404',
    (await call('GET', '/api/changes/release-notes?project_id=ticvai&from=r7')).status === 404);
  const viaTool = await tool('adam_changes', { from: 'r1', to: 'r2' });
  check('adam_changes with from and to answers the same release note', viaTool.total === 2 && /# Release r2/.test(viaTool.markdown ?? ''));
} catch (error) {
  check('the harness ran to the end', false, error.stack ?? error.message);
  for (const child of children) {
    const log = child.log?.() ?? '';
    if (log.trim()) console.log(`--- ${child.spawnargs.slice(0, 3).join(' ')}\n${log.slice(-3000)}`);
  }
} finally {
  for (const child of children) await stop(child);
  await rm(T, { recursive: true, force: true }).catch(() => {});
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
