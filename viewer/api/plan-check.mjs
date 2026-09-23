// Modules on a chart, dragged, and shipped only when somebody says so.
//
// Four things are worth proving here, and only one of them is the arithmetic:
//
//   **The page is one person's.** Not "hidden from the menu for everybody
//   else" — refused at the door. An admin is the interesting case, because an
//   admin can do nearly everything else in this service.
//
//   **A drag sends nothing.** The whole design rests on the draft being
//   private and unsent; if dragging a bar quietly reached OpenProject, the
//   confirm step would be theatre. So the ticket is re-read after a drag and
//   has to be untouched.
//
//   **The confirm ships what was confirmed.** A bar dragged between the
//   preview and the apply must not go — otherwise "are you sure" is being
//   asked about one thing and answered about another.
//
//   **A parent is refused unless it is taken off automatic scheduling.** That
//   is OpenProject's rule, the stand-in enforces it, and `update()` sending
//   `scheduleManually` is the only reason it works.
//
//   node api/fake-openproject.mjs                           # port 8798
//   TICVAI_DB=/tmp/plan.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/plan.db API=http://localhost:8799 PMS=http://127.0.0.1:8798 \
//     node api/plan-check.mjs

import { execFileSync } from 'node:child_process';

const API = process.env.API ?? 'http://localhost:8787';
const PMS = process.env.PMS ?? 'http://127.0.0.1:8798';
const STORE = process.env.TICVAI_DB ?? '';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const jars = new Map();
async function as(who, method, path, body) {
  const cookie = jars.get(who);
  const res = await fetch(`${API}${path}`, {
    method,
    headers: { 'content-type': 'application/json', ...(cookie ? { cookie } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) jars.set(who, set.split(';')[0]);
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data };
}

function cli(...args) {
  return execFileSync('python', ['-m', 'api.cli', ...args], {
    cwd: new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'),
    env: { ...process.env, TICVAI_DB: STORE },
    encoding: 'utf8',
  });
}

const PASSWORD = 'a-long-enough-passphrase';

async function recruit(handle, role) {
  const email = `${handle}@softlabsgroup.com`;
  const made = await as('boss', 'POST', '/api/invites', { email, role });
  if (made.status !== 200) return { ok: false, why: `invite: ${made.status}` };
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  const took = await as(handle, 'POST', '/api/auth/redeem',
    { token, password: PASSWORD, name: handle });
  return took.status === 200 ? { ok: true } : { ok: false, why: `redeem: ${took.status}` };
}

const connect = (who) =>
  as(who, 'PUT', '/api/settings/openproject', { token: 'harness-key', endpoint: PMS });

/** A work package straight from the stand-in, going nowhere near ADAM. The
 *  only way to prove ADAM did not write is to ask the other system. */
async function atSource(key) {
  const res = await fetch(`${PMS}/api/v3/work_packages/${key}`, {
    headers: { authorization: `Basic ${Buffer.from('apikey:harness-key').toString('base64')}` },
  });
  return res.json();
}

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an account exists', boot.status === 200, `${boot.status}`);
check('and is made the System Architect, because the plan is theirs',
  /is now System Architect/.test(STORE ? cli('owner', 'harness.boss@softlabsgroup.com') : ''),
  STORE ? '' : 'no TICVAI_DB given');
check('connected to the stand-in OpenProject', (await connect('boss')).status === 200);
check('the ADAM project is pointed at an OpenProject project',
  (await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);

check('an admin is invited', (await recruit('harness.admin2', 'admin')).ok);
await connect('harness.admin2');
check('and a project manager', (await recruit('harness.pm', 'pm')).ok);
await connect('harness.pm');

// ── the door ─────────────────────────────────────────────────────────

const byAdmin = await as('harness.admin2', 'GET', '/api/plan');
check('an admin cannot read the plan', byAdmin.status === 403, `${byAdmin.status}`);
const byPm = await as('harness.pm', 'GET', '/api/plan');
check('nor can a project manager', byPm.status === 403, `${byPm.status}`);
// The write half separately: a page that hides a button is not a rule, and a
// 403 on the read says nothing about the PUT.
const draftByAdmin = await as('harness.admin2', 'PUT', '/api/plan/draft',
  { project_id: 'ticvai', bars: [{ key: '900', start: '2026-01-01', due: '2026-01-10' }] });
check('and an admin cannot move a bar either', draftByAdmin.status === 403, `${draftByAdmin.status}`);
const shipByAdmin = await as('harness.admin2', 'POST', '/api/plan/preview', { project_id: 'ticvai' });
check('nor preview a shipment', shipByAdmin.status === 403, `${shipByAdmin.status}`);

// ── the modules ──────────────────────────────────────────────────────

const plan = await as('boss', 'GET', '/api/plan?project_id=ticvai');
check('the System Architect reads the plan', plan.status === 200, `${plan.status}`);
const modules = plan.data?.modules ?? [];
const keys = modules.map((m) => m.key);
check('and gets the top-level tickets as modules',
  ['900', '901', '902'].every((k) => keys.includes(k)), keys.join(' '));
// The point of "top-level": a child must not appear as a module of its own, or
// the chart double-counts the same work at two levels.
check('but not the tickets hanging underneath them',
  !keys.includes('7001') && !keys.includes('7003'), keys.join(' '));
// 7100 belongs to somebody else and has no parent, so it IS top-level — the
// plan is the project's, not one person's board, and leaving it out would hide
// work from the one screen whose job is to show all of it.
check('and does include a parentless ticket that is somebody else\'s',
  keys.includes('7100'), keys.join(' '));

const m1 = modules.find((m) => m.key === '900');
check('a module counts what hangs under it', m1?.children === 3, `${m1?.children} children`);
check('and says how many of those are still open', m1?.openChildren === 2, `${m1?.openChildren} open`);
check('and reports whether OpenProject schedules it for itself',
  m1?.scheduleManually === false && modules.find((m) => m.key === '902')?.scheduleManually === true,
  `900:${m1?.scheduleManually} 902:${modules.find((m) => m.key === '902')?.scheduleManually}`);
check('nothing has been dragged yet', plan.data?.draftCount === 0, `${plan.data?.draftCount}`);

// ── a drag sends nothing ─────────────────────────────────────────────

const before = await atSource('900');
const moved = await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai',
  bars: [{ key: '900', start: '2026-11-03', due: '2026-12-12' }],
});
check('a bar can be moved', moved.status === 200, `${moved.status} ${JSON.stringify(moved.data?.detail ?? '')}`);
check('and the move is held as a draft', moved.data?.draftCount === 1, `${moved.data?.draftCount}`);

const after = await atSource('900');
check('**and OpenProject has not been touched**',
  after.startDate === before.startDate && after.dueDate === before.dueDate
    && after.lockVersion === before.lockVersion,
  `${before.startDate}->${after.startDate}, lock ${before.lockVersion}->${after.lockVersion}`);

const reread = await as('boss', 'GET', '/api/plan?project_id=ticvai');
const drafted = (reread.data?.modules ?? []).find((m) => m.key === '900');
check('the draft comes back on the next read',
  drafted?.draft?.start === '2026-11-03' && drafted?.draft?.due === '2026-12-12',
  JSON.stringify(drafted?.draft ?? null));
check('while the module still reports where OpenProject has it',
  drafted?.barStart === before.startDate, `${drafted?.barStart} vs ${before.startDate}`);

// A bar dragged back to where it started is not a change, and storing it would
// make "is there anything to ship" answer yes forever.
const back = await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai',
  bars: [{ key: '900', start: before.startDate, due: before.dueDate }],
});
check('dragging a bar back to where it was clears the draft',
  back.data?.draftCount === 0 && back.data?.returned === 1,
  `count ${back.data?.draftCount} returned ${back.data?.returned}`);

// ── what will not be accepted ────────────────────────────────────────

const backwards = await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai', bars: [{ key: '900', start: '2026-12-01', due: '2026-11-01' }],
});
check('a bar cannot finish before it starts', backwards.status === 400, `${backwards.status}`);
const nonsense = await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai', bars: [{ key: '900', start: 'next tuesday', due: '2026-11-01' }],
});
check('and a date has to be a date', nonsense.status === 400,
  `${nonsense.status} ${JSON.stringify(nonsense.data?.detail ?? '')}`);
// The same mistake one character shorter. Both are "that is not a date" and
// both have to answer the same way, or the length of the typo decides whether
// the person gets a sentence or a schema error.
const impossible = await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai', bars: [{ key: '900', start: '2026-13-45', due: '2026-11-01' }],
});
check('and an impossible one is refused the same way', impossible.status === 400,
  `${impossible.status}`);
check('saying which end of which bar, in words',
  /#900/.test(String(impossible.data?.detail ?? '')), String(impossible.data?.detail ?? ''));
const notModule = await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai', bars: [{ key: '7001', start: '2026-11-01', due: '2026-11-20' }],
});
check('a ticket that is not a module cannot be dragged', notModule.status === 404, `${notModule.status}`);

const nothing = await as('boss', 'POST', '/api/plan/preview', { project_id: 'ticvai' });
check('with nothing moved there is nothing to ship', nothing.status === 409, `${nothing.status}`);

// ── shipping ─────────────────────────────────────────────────────────

await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai',
  bars: [
    { key: '900', start: '2026-11-03', due: '2026-12-12' },
    { key: '902', start: '2026-10-05', due: '2026-10-30' },
  ],
});
const preview = await as('boss', 'POST', '/api/plan/preview', { project_id: 'ticvai' });
check('the preview lists what would change', preview.status === 200
  && preview.data?.changes?.length === 2, `${preview.status} ${preview.data?.changes?.length}`);
check('and says so in the words of the thing being done',
  /starts .* -> 2026-11-03/.test(preview.data?.changes?.find((c) => c.key === '900')?.said ?? ''),
  preview.data?.changes?.find((c) => c.key === '900')?.said);
// 900 is on automatic scheduling and 902 is not, so exactly one of the two is
// about to change how OpenProject treats it — and the person is told before
// they agree, not after.
check('and warns which modules will switch to manual scheduling',
  preview.data?.becomingManual === 1, `${preview.data?.becomingManual}`);
check('still without touching OpenProject',
  (await atSource('900')).lockVersion === before.lockVersion,
  `lock ${(await atSource('900')).lockVersion}`);

// Dragged again, after the preview. This must not travel: the summary the
// person read did not mention it.
await as('boss', 'PUT', '/api/plan/draft', {
  project_id: 'ticvai', bars: [{ key: '901', start: '2027-01-04', due: '2027-02-02' }],
});

const shipped = await as('boss', 'POST',
  `/api/plan/${preview.data.proposal}/apply`, { project_id: 'ticvai' });
check('confirming sends them', shipped.status === 200 && shipped.data?.ok === true,
  `${shipped.status} ${JSON.stringify(shipped.data?.failed ?? [])}`);
check('and two modules land', shipped.data?.sent?.length === 2, `${shipped.data?.sent?.length}`);

const landed = await atSource('900');
check('**OpenProject now has the dragged dates**',
  landed.startDate === '2026-11-03' && landed.dueDate === '2026-12-12',
  `${landed.startDate} -> ${landed.dueDate}`);
check('and the automatically scheduled parent was switched to manual, or it would have refused',
  landed.scheduleManually === true, `${landed.scheduleManually}`);

const untouched = await atSource('901');
check('**the bar dragged after the preview did not travel**',
  untouched.startDate !== '2027-01-04',
  `${untouched.startDate}`);
check('and is still sitting in the draft, waiting to be confirmed',
  shipped.data?.remaining === 1, `${shipped.data?.remaining}`);

// ── the token is worth one use ───────────────────────────────────────

const again = await as('boss', 'POST', `/api/plan/${preview.data.proposal}/apply`,
  { project_id: 'ticvai' });
check('the same confirmation cannot be sent twice', again.status === 409, `${again.status}`);

const forged = await as('boss', 'POST', '/api/plan/not-a-real-token/apply', { project_id: 'ticvai' });
check('and a made-up one is refused', forged.status === 404, `${forged.status}`);

// ── throwing the sketch away ─────────────────────────────────────────

const cleared = await as('boss', 'DELETE', '/api/plan/draft?project_id=ticvai');
check('the sketch can be discarded', cleared.status === 200 && cleared.data?.cleared === 1,
  `${cleared.status} cleared ${cleared.data?.cleared}`);
const empty = await as('boss', 'GET', '/api/plan?project_id=ticvai');
check('and then there is nothing left to ship', empty.data?.draftCount === 0,
  `${empty.data?.draftCount}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
