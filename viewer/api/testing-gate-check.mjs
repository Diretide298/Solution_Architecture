// Ten tickets, then stop and test — and a teammate says you did.
//
// Two properties, and the first is the reason any of this is worth building:
//
//   **The gate is a rule, not a reminder.** It is on the route that closes a
//   ticket, so there is no connector flag, no agent instruction and no second
//   path that reaches around it. Most of this file is the refusal happening in
//   places somebody would try.
//
//   **The maker cannot be the checker.** A single "I tested it" button is a box
//   that gets ticked on the way past. The refusal of your own batch has no
//   override — not for an admin, not for the owner — and that is asserted here
//   rather than assumed from the absence of a route.
//
// Run against a stand-in OpenProject, for the same reason cr-ticket-check does:
// closing tickets is a write, and the live instance holds the real plan.
//
//   node api/fake-openproject.mjs                           # port 8798
//   TICVAI_DB=/tmp/gate.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/gate.db API=http://localhost:8799 PMS=http://127.0.0.1:8798 \
//     node api/testing-gate-check.mjs

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

const connect = (who) =>
  as(who, 'PUT', '/api/settings/openproject', { token: 'harness-key', endpoint: PMS });

/** Close one ticket: propose a closing status, then apply. `head` is what the
 *  connector would have read off git; a browser sends none. */
async function close(who, key, head) {
  const made = await as(who, 'POST', `/api/work-packages/${key}/proposals`,
    { status: 'Closed', comment: `Built and closed #${key}.` });
  if (made.status !== 200) return { stage: 'propose', ...made };
  const done = await as(who, 'POST',
    `/api/work-packages/${key}/proposals/${made.data.proposal}/apply`,
    { ...(head ? { head, dirty: false } : {}) });
  return { stage: 'apply', proposed: made.data, ...done };
}

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
await connect('boss');
const mapped = await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 });
check('the project is pointed at OpenProject', mapped.status === 200, `${mapped.status}`);

check('a developer is invited', (await recruit('harness.dev', 'dev')).ok);
await connect('harness.dev');
check('and a second one, to do the checking', (await recruit('harness.dev2', 'dev')).ok);
await connect('harness.dev2');

// ── closing, and being counted ───────────────────────────────────────

const EVERY = (await as('harness.dev', 'GET', '/api/test-batches')).data?.every;
check('the service says how often testing is due', EVERY === 10, String(EVERY));

const first = await close('harness.dev', 3000);
check('the first close goes through', first.status === 200,
  `${first.stage} ${first.status} ${JSON.stringify(first.data?.detail ?? '')}`);
check('and is counted against a batch that opened itself',
  first.data?.testing?.closed === 1 && first.data?.testing?.full === false,
  JSON.stringify(first.data?.testing ?? null));
check('which says how many are left rather than only how many there are',
  /9 more/.test(first.data?.testing?.say ?? ''), first.data?.testing?.say);

// A change that does not close is not a closure. Counting it would mean a
// developer who moves nine tickets to In progress is one move from a gate.
const moved = await as('harness.dev', 'POST', '/api/work-packages/3001/proposals',
  { status: 'In progress', comment: 'Started.' });
const movedDone = await as('harness.dev', 'POST',
  `/api/work-packages/3001/proposals/${moved.data.proposal}/apply`, {});
check('a change that does not close the ticket is not counted',
  movedDone.status === 200 && movedDone.data?.testing === undefined,
  JSON.stringify(movedDone.data?.testing ?? 'not counted'));

for (let n = 2; n <= 10; n += 1) {
  const done = await close('harness.dev', 3000 + n);
  if (done.status !== 200) { check(`close ${n} goes through`, false, `${done.stage} ${done.status}`); break; }
}
const full = await as('harness.dev', 'GET', '/api/test-batches');
check('ten closes fill the batch', full.data?.mine?.closed === 10, String(full.data?.mine?.closed));
check('and it knows it is full', full.data?.mine?.full === true);

// ── and then the gate ────────────────────────────────────────────────

const eleventh = await close('harness.dev', 3020);
check('the eleventh close is refused', eleventh.status === 409,
  `${eleventh.stage} ${eleventh.status}`);
check('and says what to do, not just no',
  /[Tt]est them.*submit/s.test(String(eleventh.data?.detail)), String(eleventh.data?.detail));

// The refusal has to come before anything is sent, or a "refused" close would
// still have closed the ticket in OpenProject.
const stillOpen = await as('harness.dev', 'GET', '/api/work-packages/3020');
check('and nothing was sent — the ticket is untouched',
  stillOpen.data?.workPackage?.status !== 'Closed',
  stillOpen.data?.workPackage?.status ?? '?');

// The proposal is unspent too, so nothing has to be redone once the gate opens.
const reused = await as('harness.dev', 'POST',
  `/api/work-packages/3020/proposals/${eleventh.proposed.proposal}/apply`, {});
check('the proposal was not spent by the refusal', reused.status === 409,
  `${reused.status}`);

// The obvious way round: a different ticket. Also the obvious way an agent
// would try to be helpful.
const another = await close('harness.dev', 3021);
check('another ticket does not get round it', another.status === 409, `${another.status}`);

// Somebody else is not held up by this person's batch. The gate is personal.
const other = await close('harness.dev2', 3030);
check('a teammate is not blocked by somebody else\'s batch', other.status === 200,
  `${other.stage} ${other.status}`);

// The warning arrives at the proposal too, so nobody says yes to something
// that is about to be refused.
const warned = await as('harness.dev', 'POST', '/api/work-packages/3022/proposals',
  { status: 'Closed', comment: 'Another one.' });
check('a closing proposal warns before the person agrees to it',
  warned.data?.testing?.full === true && warned.data?.closes === true,
  JSON.stringify(warned.data?.testing ?? null));

// ── submitting is not passing ────────────────────────────────────────

const batchId = full.data.mine.id;
const thin = await as('harness.dev', 'POST', `/api/test-batches/${batchId}/submit`,
  { notes: 'tested' });
check('"tested" is refused, because a checker cannot check it',
  thin.status === 400 && /not something anybody can check/.test(String(thin.data?.detail)),
  String(thin.data?.detail));

const submitted = await as('harness.dev', 'POST', `/api/test-batches/${batchId}/submit`, {
  notes: 'Ran the contract suite and the POS smoke pack against staging: 412 passed, '
    + '2 failed on the receipt total, both traced to CR-001 and left failing on purpose.',
  evidence: 'pytest -q tests/contracts: 412 passed, 2 failed in 96s',
});
check('a real account of what was run is accepted', submitted.status === 200,
  `${submitted.status} ${JSON.stringify(submitted.data?.detail ?? '')}`);

const stillShut = await close('harness.dev', 3023);
check('but submitting does not open the gate — that is the point',
  stillShut.status === 409, `${stillShut.status}`);
check('and it says it is now somebody else\'s move',
  /teammate has to look/.test(String(stillShut.data?.detail)), String(stillShut.data?.detail));

// ── the maker cannot be the checker ──────────────────────────────────

const self = await as('harness.dev', 'POST', `/api/test-batches/${batchId}/check`,
  { verdict: 'passed' });
check('you cannot check your own testing', self.status === 403, `${self.status}`);
check('and the refusal says why rather than just no',
  /whole of what this is for/.test(String(self.data?.detail)), String(self.data?.detail));

// No override. This is the assertion that says the rule has no back door —
// an admin waving it through for themselves would be the same hole renamed.
const bossOwn = await close('boss', 3040);
check('an admin closes normally', bossOwn.status === 200, `${bossOwn.status}`);
const bossBatch = (await as('boss', 'GET', '/api/test-batches')).data?.mine?.id;
await as('boss', 'POST', `/api/test-batches/${bossBatch}/submit`,
  { notes: 'Ran everything there is to run, twice, and read the output.' });
const bossSelf = await as('boss', 'POST', `/api/test-batches/${bossBatch}/check`,
  { verdict: 'passed' });
check('and an admin cannot check their own either — there is no override',
  bossSelf.status === 403, `${bossSelf.status}`);

const noReason = await as('harness.dev2', 'POST', `/api/test-batches/${batchId}/check`,
  { verdict: 'failed' });
check('failing without a reason is refused', noReason.status === 400,
  String(noReason.data?.detail));

const sentBack = await as('harness.dev2', 'POST', `/api/test-batches/${batchId}/check`,
  { verdict: 'failed', note: 'The two failures are not explained. Say which tickets they are about.' });
check('a teammate can send it back', sentBack.status === 200, `${sentBack.status}`);

const afterFail = await close('harness.dev', 3024);
check('being sent back does not open the gate', afterFail.status === 409, `${afterFail.status}`);
check('and the refusal carries the reason it was sent back',
  /not explained/.test(String(afterFail.data?.detail)), String(afterFail.data?.detail));

// ── and passing lets them go on ──────────────────────────────────────

await as('harness.dev', 'POST', `/api/test-batches/${batchId}/submit`, {
  notes: 'Both failures are #3002 and #3005, both waiting on CR-001. Everything else green.',
});
const passed = await as('harness.dev2', 'POST', `/api/test-batches/${batchId}/check`,
  { verdict: 'passed', note: 'Clear now.' });
check('and pass it once it says enough', passed.status === 200, `${passed.status}`);
check('the batch records who checked it, which is the audit trail',
  passed.data?.batch?.checkedBy === 'harness.dev2', passed.data?.batch?.checkedBy);

const freed = await close('harness.dev', 3025);
check('closing works again', freed.status === 200, `${freed.stage} ${freed.status}`);
check('and a fresh batch has opened with one in it',
  freed.data?.testing?.closed === 1, JSON.stringify(freed.data?.testing ?? null));

const history = await as('harness.dev', 'GET', '/api/test-batches');
check('the passed batch is kept as history rather than deleted',
  (history.data?.past ?? []).some((b) => b.id === batchId),
  (history.data?.past ?? []).map((b) => b.id).join(' '));
check('and the batch waiting on nobody is not offered to its own author',
  !(history.data?.waiting ?? []).some((b) => b.who.name === 'harness.dev'),
  (history.data?.waiting ?? []).map((b) => b.who.name).join(' ') || 'none');

// ── the commit nudge, which is a sentence and never a refusal ────────
//
// Item 13. ADAM cannot see anybody's repository, so this is evidence and a
// prompt; the assertions are about it being *said*, and about it never being
// the reason a close fails.

let nudged = null;
for (let n = 0; n < 5; n += 1) {
  const done = await close('harness.dev2', 3100 + n, 'abc1234def5678abc1234def5678abc1234def56');
  if (done.status !== 200) { check('the nudge run closes cleanly', false, `${done.status}`); break; }
  nudged = done.data?.commit ?? nudged;
}
check('five closes at one commit are noticed', Boolean(nudged), String(nudged));
check('and named by the sha rather than vaguely',
  /abc1234d/.test(String(nudged)), String(nudged));

const moved2 = await close('harness.dev2', 3110, 'fedcba9876543210fedcba9876543210fedcba98');
check('a close at a new commit is not nudged', moved2.status === 200 && !moved2.data?.commit,
  String(moved2.data?.commit ?? 'no nudge'));

const noGit = await close('harness.dev2', 3111);
check('and somebody sending no commit at all is never nudged, only counted',
  noGit.status === 200 && !noGit.data?.commit && noGit.data?.testing?.closed > 0,
  JSON.stringify(noGit.data?.testing ?? null));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
