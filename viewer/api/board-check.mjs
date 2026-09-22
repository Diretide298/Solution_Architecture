// A developer's own board, and the fact that it is only ever their own.
//
// Two properties:
//
//   **`assignee = me` means the caller.** Every PMS call is made with the
//   caller's own OpenProject token, so the board cannot be asked for somebody
//   else's — there is no id in the request to change. The stand-in answers
//   differently per token precisely so this can be asserted rather than assumed
//   from the absence of a parameter.
//
//   **The gate is on the board.** The testing rule shipped with the Claude
//   connector as its only interface, which meant somebody not using Claude Code
//   could be refused a close by a rule they had no way to satisfy. What the
//   board says about it has to match what the service will do.
//
//   node api/fake-openproject.mjs                           # port 8798
//   TICVAI_DB=/tmp/board.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/board.db API=http://localhost:8799 PMS=http://127.0.0.1:8798 \
//     node api/board-check.mjs

const API = process.env.API ?? 'http://localhost:8787';
const PMS = process.env.PMS ?? 'http://127.0.0.1:8798';
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

const connect = (who, token) =>
  as(who, 'PUT', '/api/settings/openproject', { token, endpoint: PMS });

const keys = (board) => (board.data?.items ?? []).map((t) => t.key).sort();

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
// Two people with two OpenProject accounts, which is the arrangement the whole
// "your own token, never a shared one" rule exists for.
check('the admin connects as one OpenProject user',
  (await connect('boss', 'other-key')).status === 200);
check('the project is pointed at OpenProject',
  (await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);

check('a developer is invited', (await recruit('harness.dev', 'dev')).ok);
check('and connects as a different one',
  (await connect('harness.dev', 'harness-key')).status === 200);
check('and a second developer, to do the checking', (await recruit('harness.dev2', 'dev')).ok);
check('who connects too', (await connect('harness.dev2', 'harness-key')).status === 200);

// ── a board is only ever your own ────────────────────────────────────

const mine = await as('harness.dev', 'GET', '/api/board/mine');
check('a developer has a board', mine.status === 200,
  `${mine.status} ${JSON.stringify(mine.data?.detail ?? '')}`);
check('with the tickets assigned to them', keys(mine).join(' ') === '7001 7002 7003 7004',
  keys(mine).join(' '));
check('and not the one assigned to somebody else',
  !keys(mine).includes('7100'), keys(mine).join(' '));
check('the closed one is not on the open list', !keys(mine).includes('7005'),
  keys(mine).join(' '));

const theirs = await as('boss', 'GET', '/api/board/mine');
check('somebody else asking the same route gets their own instead',
  keys(theirs).join(' ') === '7100', keys(theirs).join(' '));

// ── and it says what was finished ────────────────────────────────────

const done = (mine.data?.finished ?? []).map((t) => t.key);
check('what they closed recently comes back too', done.includes('7005'), done.join(' ') || 'none');
check('and is kept apart from what is open',
  !keys(mine).includes('7005'), 'open list is open only');

// ── what the board needs to draw itself ──────────────────────────────
//
// The grouping is overdue / this week / started / backlog, and it is built
// from two fields rather than from status names, because a status name is a
// thing a team renames on a Tuesday.

const byKey = Object.fromEntries((mine.data?.items ?? []).map((t) => [t.key, t]));
check('every ticket carries the dates the grouping needs',
  byKey['7001']?.dueDate && byKey['7002']?.dueDate,
  `${byKey['7001']?.dueDate} ${byKey['7002']?.dueDate}`);
check('and the percentage that says work has started',
  byKey['7003']?.percentDone === 40, String(byKey['7003']?.percentDone));
check('and the backlog one has neither', !byKey['7004']?.dueDate && !byKey['7004']?.percentDone,
  `${byKey['7004']?.dueDate} ${byKey['7004']?.percentDone}`);
check('one is genuinely overdue, so the first section is not vacuous',
  new Date(byKey['7001'].dueDate) < new Date(), byKey['7001'].dueDate);

// The timeline needs these two, and they are the reason it can be drawn at all
// without ADAM storing a schedule of its own.
const overview = await as('boss', 'GET', '/api/board/overview');
check('the overview carries milestones for the timeline to group by',
  (overview.data?.items ?? []).some((t) => t.version === 'M1 Checkout'),
  [...new Set((overview.data?.items ?? []).map((t) => t.version).filter(Boolean))].join(' '));
check('and epics for it to draw a bar per',
  (overview.data?.items ?? []).some((t) => t.parent),
  [...new Set((overview.data?.items ?? []).map((t) => t.parent).filter(Boolean))].join(' '));

// ── the gate, on the board ───────────────────────────────────────────

check('a board with nothing closed says nothing about testing',
  mine.data?.testing === null, JSON.stringify(mine.data?.testing));

// Close ten, which is what it takes.
for (let n = 0; n < 10; n += 1) {
  const key = 8000 + n;
  const made = await as('harness.dev', 'POST', `/api/work-packages/${key}/proposals`,
    { status: 'Closed', comment: 'Done.' });
  if (made.status !== 200) { check(`close ${n} proposes`, false, `${made.status}`); break; }
  const sent = await as('harness.dev', 'POST',
    `/api/work-packages/${key}/proposals/${made.data.proposal}/apply`, {});
  if (sent.status !== 200) { check(`close ${n} applies`, false, `${sent.status}`); break; }
}
const blocked = await as('harness.dev', 'GET', '/api/board/mine');
check('once the batch is full the board says so before anything is refused',
  blocked.data?.testing?.full === true, JSON.stringify(blocked.data?.testing));
check('and names the number, so it matches the refusal that is coming',
  blocked.data?.testing?.closed === 10, String(blocked.data?.testing?.closed));

// What the board offers has to be what the service will accept.
const batches = await as('harness.dev', 'GET', '/api/test-batches');
check('the batch is readable from the page as well as the connector',
  batches.data?.mine?.id === blocked.data?.testing?.id,
  `${batches.data?.mine?.id} vs ${blocked.data?.testing?.id}`);
check('and nobody else is offered it to check while it is unsubmitted',
  !(await as('harness.dev2', 'GET', '/api/test-batches')).data?.waiting?.length,
  'nothing waiting yet');

const submitted = await as('harness.dev', 'POST',
  `/api/test-batches/${batches.data.mine.id}/submit`,
  { notes: 'Ran the POS pack against staging: 96 passed, nothing failed.' });
check('submitting from the page works', submitted.status === 200, `${submitted.status}`);

const waiting = await as('harness.dev2', 'GET', '/api/test-batches');
check('and it appears for a teammate to check',
  (waiting.data?.waiting ?? []).length === 1,
  String((waiting.data?.waiting ?? []).length));
check('carrying what they said they ran, which is the thing being checked',
  /96 passed/.test(waiting.data.waiting[0].notes ?? ''), waiting.data.waiting[0].notes ?? '');
check('the maker is not offered their own',
  !((await as('harness.dev', 'GET', '/api/test-batches')).data?.waiting ?? []).length,
  'not offered');

const passed = await as('harness.dev2', 'POST',
  `/api/test-batches/${batches.data.mine.id}/check`, { verdict: 'passed', note: 'Fine.' });
check('a teammate passes it', passed.status === 200, `${passed.status}`);

const freed = await as('harness.dev', 'GET', '/api/board/mine');
check('and the board stops warning', freed.data?.testing === null,
  JSON.stringify(freed.data?.testing));

// ── not connected is a setup step, not a failure ─────────────────────

const stranger = await recruit('harness.new', 'dev');
check('somebody new is invited', stranger.ok, stranger.why ?? '');
const noToken = await as('harness.new', 'GET', '/api/board/mine');
check('a board without an OpenProject token answers 428, not 500',
  noToken.status === 428, `${noToken.status}`);
check('and says which half is missing',
  /token|OpenProject/i.test(String(noToken.data?.detail)), String(noToken.data?.detail));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
