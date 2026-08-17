// The rules that matter here are the ones about who gets in, so this spends
// most of its time trying to get in the ways that should not work.
const API = 'http://localhost:8787';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

// a cookie jar, because sessions are the thing under test
const jar = new Map();
async function call(method, path, body, { jarName = 'a' } = {}) {
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
    const pair = set.split(';')[0];
    if (/ticvai_session=;?$/.test(pair) || pair.endsWith('=')) jar.delete(jarName);
    else jar.set(jarName, pair);
  }
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data, raw: set };
}

const health = await call('GET', '/api/health');
check('the service is up', health.status === 200,
  `${health.data?.accounts} accounts, domain ${health.data?.domain}`);

// ── signed out, everything that writes must refuse ───────────────────
const anon = await call('GET', '/api/auth/me');
check('it answers "not signed in" rather than erroring', anon.status === 200 && anon.data.signedIn === false);

const noAuthVerdict = await call('POST', '/api/validation',
  { target_kind: 'table', target_id: 'orders.sales_order', verdict: 'approved' });
check('a stranger cannot record a verdict', noAuthVerdict.status === 401, `${noAuthVerdict.status}`);

const noAuthInvite = await call('POST', '/api/invites', { email: 'x@softlabsgroup.com' });
check('a stranger cannot mint an invite', noAuthInvite.status === 401, `${noAuthInvite.status}`);

const forged = await fetch(`${API}/api/auth/me`, { headers: { cookie: 'ticvai_session=not-a-real-token' } });
check('a forged cookie is simply nobody', (await forged.json()).signedIn === false);

// ── the admin signs in ───────────────────────────────────────────────
const ADMIN = { email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' };
const badPass = await call('POST', '/api/auth/login', { email: ADMIN.email, password: 'wrong-but-long-enough' });
check('a wrong password is refused', badPass.status === 401);

const noSuch = await call('POST', '/api/auth/login', { email: 'ghost@softlabsgroup.com', password: 'wrong-but-long-enough' });
check('an unknown account gives the same answer as a wrong password',
  noSuch.status === badPass.status && noSuch.data?.detail === badPass.data?.detail,
  JSON.stringify(noSuch.data?.detail));

const login = await call('POST', '/api/auth/login', ADMIN);
check('the admin signs in', login.status === 200, `${login.status}`);
check('the session cookie is httponly and lax', /httponly/i.test(login.raw ?? '') && /lax/i.test(login.raw ?? ''),
  (login.raw ?? '').replace(/ticvai_session=[^;]+/, 'ticvai_session=…'));

const who = await call('GET', '/api/auth/me');
check('and is recognised as an admin', who.data?.account?.role === 'admin', who.data?.account?.email);

// ── the domain rule ──────────────────────────────────────────────────
const outside = await call('POST', '/api/invites', { email: 'ceo@gmail.com' });
check('an invite outside the domain is refused', outside.status === 400, outside.data?.detail);

const malformed = await call('POST', '/api/invites', { email: 'not-an-email' });
check('a malformed address is refused', malformed.status === 400);

// ── an invite, and what it can and cannot do ─────────────────────────
// A fresh address each run. Accounts are permanent by design, so a fixed one
// makes the second run fail on the first run's success.
const INVITED = `harness.reviewer${process.env.RUN_STAMP ?? Math.floor(process.hrtime()[1] / 1000)}@softlabsgroup.com`;
const invite = await call('POST', '/api/invites', { email: INVITED, role: 'reviewer' });
check('an admin can invite someone in the domain', invite.status === 200, invite.data?.link);
const token = invite.data?.token;

const peek = await fetch(`${API}/api/invites/check/${token}`).then((r) => r.json());
check('the link says who it is for, before any password is chosen', peek.email === INVITED, peek.email);

const badToken = await fetch(`${API}/api/invites/check/definitely-not-a-token`);
check('an invented link is refused', badToken.status === 404);

// the address comes from the invite, not the form — so there is nothing to claim
const claim = await call('POST', '/api/auth/redeem',
  { token, name: 'Impostor', password: 'another-long-passphrase', email: 'ceo@softlabsgroup.com' },
  { jarName: 'b' });
check('redeeming makes the account the invite named, not one the caller asks for',
  claim.status === 200 && claim.data?.email === INVITED, claim.data?.email);

const shortPw = await call('POST', '/api/auth/redeem', { token: 'x', password: 'short' }, { jarName: 'c' });
check('a short password is refused', shortPw.status === 400 || shortPw.status === 404);

const reuse = await call('POST', '/api/auth/redeem',
  { token, name: 'Second', password: 'yet-another-passphrase' }, { jarName: 'd' });
check('an invite works exactly once', reuse.status === 409, reuse.data?.detail);

// the redeemed account is signed in, and is NOT an admin
const reviewerWho = await call('GET', '/api/auth/me', undefined, { jarName: 'b' });
check('the invited person is signed in as themselves',
  reviewerWho.data?.account?.email === INVITED && reviewerWho.data?.account?.role === 'reviewer',
  `${reviewerWho.data?.account?.email} / ${reviewerWho.data?.account?.role}`);

const escalate = await call('POST', '/api/invites', { email: 'someone@softlabsgroup.com' }, { jarName: 'b' });
check('a reviewer cannot mint invites', escalate.status === 403, `${escalate.status}`);

// ── verdicts ─────────────────────────────────────────────────────────
const target = { target_kind: 'operation', target_id: 'listProducts' };
const v1 = await call('POST', '/api/validation',
  { ...target, verdict: 'needs-work', note: 'routing says replica, workbook says write' },
  { jarName: 'b' });
check('a signed-in reviewer can record a verdict', v1.status === 200);

const badVerdict = await call('POST', '/api/validation', { ...target, verdict: 'lgtm' }, { jarName: 'b' });
check('an invented verdict is refused', badVerdict.status === 400, badVerdict.data?.detail);

const badKind = await call('POST', '/api/validation',
  { target_kind: 'sandwich', target_id: 'x', verdict: 'approved' }, { jarName: 'b' });
check('an invented target kind is refused', badKind.status === 400);

const v2 = await call('POST', '/api/validation',
  { ...target, verdict: 'approved', note: 'vendor confirmed the workbook is right' },
  { jarName: 'b' });
check('a second verdict is recorded, not an overwrite', v2.status === 200 && v2.data.id !== v1.data.id);

const hist = await fetch(`${API}/api/validation/operation/listProducts`).then((r) => r.json());
check('the newest verdict is the current one',
  hist.current?.verdict === 'approved', hist.current?.verdict);
check('and the earlier one is kept', hist.history.length >= 2,
  `${hist.history.length} in history: ${hist.history.map((h) => h.verdict).join(' <- ')}`);
check('each says who and when', Boolean(hist.current?.by_email && hist.current?.at),
  `${hist.current?.by_email} at ${hist.current?.at}`);

const sum = await fetch(`${API}/api/validation`).then((r) => r.json());
check('the summary holds one row per artefact',
  sum.items.filter((i) => i.target_id === 'listProducts').length === 1,
  JSON.stringify(sum.counts));

// ── signing out ──────────────────────────────────────────────────────
await call('POST', '/api/auth/logout', undefined, { jarName: 'b' });
const after = await call('GET', '/api/auth/me', undefined, { jarName: 'b' });
check('signing out ends the session', after.data?.signedIn === false);

console.log(`\nRESULT: ${pass}/${pass + fail} passed — ${fail ? 'FAIL' : 'PASS'}`);
process.exitCode = fail ? 1 : 0;
