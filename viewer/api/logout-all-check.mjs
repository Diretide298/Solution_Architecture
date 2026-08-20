// Signing out everywhere, from both ends.
//
// The claim under test is a counting one — *that* account's sessions, all of
// them, and nobody else's — and the only way a client can count sessions is to
// hold several at once and see which of them still answer afterwards. So this
// keeps five cookie jars open at a time and asks each of them who it is.
//
// Point the service at a scratch store before running it, the way the other
// harnesses want:
//
//   TICVAI_DB=/tmp/scratch.db python -m uvicorn api.main:app --port 8787
//   node api/logout-all-check.mjs
const API = 'http://localhost:8787';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const jar = new Map();
async function call(method, path, body, { jarName = 'admin' } = {}) {
  const cookie = jar.get(jarName);
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      'content-type': 'application/json',
      ...(cookie ? { cookie } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) {
    const pair = set.split(';')[0].trim();
    // Starlette clears a cookie by sending it back as `ticvai_session=""` — an
    // empty *quoted* value, not an empty one. api-check.mjs looks only for the
    // unquoted form, so its jar quietly keeps a dead cookie after a logout;
    // that check passes anyway because the session row is gone server-side, but
    // this one is asking about the cookie itself and has to read it properly.
    if (/^ticvai_session=(""|)$/.test(pair)) jar.delete(jarName);
    else jar.set(jarName, pair);
  }
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data, raw: set };
}

const signedIn = async (jarName) =>
  (await call('GET', '/api/auth/me', undefined, { jarName })).data?.signedIn === true;

const health = await call('GET', '/api/health');
check('the service is up', health.status === 200, `${health.data?.accounts} accounts`);

// ── two people, several devices each ─────────────────────────────────
const ADMIN = { email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' };

// An empty store gets its admin here rather than by hand. Without this the run
// signs in against an account nobody made, every later step 401s, and it reports
// 5/24 — which reads as the feature being broken rather than the harness being
// half set up. `/api/auth/bootstrap` only answers while there are no accounts,
// so this is a no-op on a store that already has one.
if (health.data?.accounts === 0) {
  await call('POST', '/api/auth/bootstrap', { ...ADMIN, name: 'Harness admin' });
}

const login = await call('POST', '/api/auth/login', ADMIN);
check('the admin signs in', login.status === 200, `${login.status}`);

// Fresh addresses each run: accounts are permanent by design, so a fixed one
// makes the second run fail on the first run's success.
const stamp = process.env.RUN_STAMP ?? Math.floor(process.hrtime()[1] / 1000);
const ALPHA = `harness.alpha${stamp}@softlabsgroup.com`;
const BETA = `harness.beta${stamp}@softlabsgroup.com`;
const PASSWORD = 'another-long-passphrase';

async function enrol(email, firstJar) {
  const invite = await call('POST', '/api/invites', { email, role: 'reviewer' });
  const redeem = await call('POST', '/api/auth/redeem',
    { token: invite.data?.token, name: email.split('@')[0], password: PASSWORD },
    { jarName: firstJar });
  return redeem.status === 200;
}

check('a reviewer is enrolled and signed in on their first device',
  await enrol(ALPHA, 'a1'), ALPHA);
check('and a second reviewer, who is the control',
  await enrol(BETA, 'b1'), BETA);

// Signing in again does not replace a session, it adds one — which is what
// makes "everywhere" a real question rather than a synonym for "here".
for (const jarName of ['a2', 'a3']) {
  await call('POST', '/api/auth/login', { email: ALPHA, password: PASSWORD }, { jarName });
}
await call('POST', '/api/auth/login', { email: BETA, password: PASSWORD }, { jarName: 'b2' });
check('the first reviewer now holds three sessions',
  (await signedIn('a1')) && (await signedIn('a2')) && (await signedIn('a3')));
check('and the second holds two', (await signedIn('b1')) && (await signedIn('b2')));

// ── a verdict, which must survive all of this ────────────────────────
const TARGET = { target_kind: 'operation', target_id: `harness-logout-all-${stamp}` };
const recorded = await call('POST', '/api/validation',
  { ...TARGET, verdict: 'approved', note: 'recorded before every session was ended' },
  { jarName: 'a1' });
check('the reviewer records a verdict', recorded.status === 200, `${recorded.status}`);

const roster = async () => (await call('GET', '/api/accounts')).data?.accounts ?? [];
const find = (people, email) => people.find((p) => p.email === email);
const before = await roster();
const alphaId = find(before, ALPHA)?.id;
const betaId = find(before, BETA)?.id;
check('the admin can see both of them', Boolean(alphaId && betaId), `${alphaId} / ${betaId}`);

// ── the reviewer ends their own, from one of the three ───────────────
const mine = await call('POST', '/api/auth/logout-all', undefined, { jarName: 'a2' });
check('signing out everywhere is allowed to anybody signed in, not only an admin',
  mine.status === 200, `${mine.status} ${JSON.stringify(mine.data)}`);
check('and it answers with how many it dropped', mine.data?.dropped === 3,
  `dropped ${mine.data?.dropped}, expected 3`);
check('the caller’s own cookie is cleared, so this device is signed out too',
  !jar.has('a2'), mine.raw ?? 'no set-cookie');

check('every one of that account’s sessions is gone, the two it was not called from included',
  !(await signedIn('a1')) && !(await signedIn('a2')) && !(await signedIn('a3')));
check('and nobody else’s were touched',
  (await signedIn('b1')) && (await signedIn('b2')) && (await signedIn('admin')));

const emptied = await call('POST', '/api/auth/login', { email: ALPHA, password: PASSWORD },
  { jarName: 'a4' });
check('the account still works — ending sessions is not disabling', emptied.status === 200);
const again = await call('POST', '/api/auth/logout-all', undefined, { jarName: 'a4' });
check('a second call drops the one session that is left and says so',
  again.data?.dropped === 1, `dropped ${again.data?.dropped}`);

// ── the verdict is still there, and still theirs ─────────────────────
const history = await call('GET',
  `/api/validation/${TARGET.target_kind}/${TARGET.target_id}`);
check('the verdict survives, with its author',
  history.data?.current?.verdict === 'approved'
  && history.data?.current?.by_email === ALPHA,
  `${history.data?.current?.verdict} by ${history.data?.current?.by_email}`);

// ── the admin doing it to somebody else ──────────────────────────────
const ghost = await call('POST', '/api/accounts/999999/logout-all');
check('an unknown account is a 404, not a silent nothing', ghost.status === 404,
  `${ghost.status} ${ghost.data?.detail ?? ''}`);

const notAdmin = await call('POST', `/api/accounts/${alphaId}/logout-all`, undefined,
  { jarName: 'b1' });
check('a reviewer cannot end somebody else’s sessions', notAdmin.status === 403,
  `${notAdmin.status} ${notAdmin.data?.detail ?? ''}`);
check('and the refusal really was a refusal', await signedIn('b1'));

const theirs = await call('POST', `/api/accounts/${betaId}/logout-all`);
check('an admin can end somebody else’s', theirs.status === 200 && theirs.data?.dropped === 2,
  `${theirs.status}, dropped ${theirs.data?.dropped}`);
check('both of their devices are signed out',
  !(await signedIn('b1')) && !(await signedIn('b2')));
check('the admin’s own session is untouched by doing it to somebody else',
  await signedIn('admin'));

const after = await roster();
const betaAfter = find(after, BETA);
check('the account is still enabled, so they can come back',
  betaAfter?.active === 1 || betaAfter?.active === true, `active: ${betaAfter?.active}`);
check('and every verdict count is exactly what it was',
  after.every((p) => find(before, p.email)?.verdicts === p.verdicts),
  after.map((p) => `${p.email.split('@')[0]}:${p.verdicts}`).join(' '));

console.log(`\nRESULT: ${pass}/${pass + fail} passed — ${fail ? 'FAIL' : 'PASS'}`);
process.exitCode = fail ? 1 : 0;
