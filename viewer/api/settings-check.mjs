#!/usr/bin/env node
/**
 * The settings endpoints, and the promise the settings page makes.
 *
 *   node viewer/api/settings-check.mjs
 *
 * Same shape as the other harnesses here: no framework, one file, non-zero exit
 * on a failure, parameterised on TICVAI_VIEWER so it does not have to run
 * against the instance backed by the real account database.
 *
 * **The check that matters is the negative one.** This stores a credential and
 * then asserts the credential does not come back — not in the settings payload,
 * not anywhere. Everything else here is plumbing; that is the property the
 * whole design exists to hold.
 */

const BASE = (process.env.TICVAI_VIEWER ?? 'http://127.0.0.1:4173').replace(/\/+$/, '');
const EMAIL = process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com';
const PASSWORD = process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase';
// A real one is needed to exercise the validate-before-store path. Without it
// that half is skipped rather than faked: a stub would prove the storage works
// and say nothing about whether the checking does.
const TOKEN = process.env.TICVAI_OP_TOKEN ?? '';

const results = [];
const pass = (what) => { results.push(true); console.log(`  ok    ${what}`); };
const fail = (what, why) => { results.push(false); console.log(`  FAIL  ${what}\n        ${why}`); };
const skip = (what, why) => console.log(`  skip  ${what} — ${why}`);

let cookie = '';

async function call(path, { method = 'GET', body } = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      ...(cookie ? { cookie } : {}),
      ...(body === undefined ? {} : { 'content-type': 'application/json' }),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  let data = null;
  try { data = await res.json(); } catch { /* an empty body is fine */ }
  return { status: res.status, data, res };
}

// ---- sign in ----------------------------------------------------------------

console.log('\nsettings');

const login = await fetch(`${BASE}/api/auth/login`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: EMAIL, password: PASSWORD }),
});
if (!login.ok) {
  console.log(`  cannot sign in as ${EMAIL} (${login.status}).`);
  console.log('  Make the account with: python -m api.cli admin ' + EMAIL);
  process.exit(1);
}
const token = (login.headers.getSetCookie?.() ?? [])
  .map((line) => /ticvai_session=([^;]+)/.exec(line)?.[1]).find(Boolean);
cookie = `ticvai_session=${decodeURIComponent(token)}`;
pass(`signed in as ${EMAIL}`);

// ---- the shape ---------------------------------------------------------------

const me = await call('/api/settings/me');
if (me.status === 200 && me.data?.email) pass('GET /api/settings/me answers');
else fail('GET /api/settings/me answers', JSON.stringify(me));

// Whether a credential can be stored at all is said up front, so the page can
// explain rather than let somebody type a live token into a box that will 503.
if (typeof me.data?.canStoreCredentials === 'boolean') {
  pass(`canStoreCredentials is stated (${me.data.canStoreCredentials})`);
  if (!me.data.canStoreCredentials && me.data.whyNot) pass('and it says why not, naming the variable');
} else fail('canStoreCredentials is stated', JSON.stringify(me.data));

// Signed out, this is nobody's business.
const saved = cookie;
cookie = '';
const anon = await call('/api/settings/me');
if (anon.status === 401) pass('signed out, settings are 401');
else fail('signed out, settings are 401', `got ${anon.status}`);
cookie = saved;

// ---- git identity ------------------------------------------------------------

const good = await call('/api/settings/git-identity', { method: 'PUT', body: { git_email: 'dev@example.com' } });
if (good.status === 200 && good.data.gitEmail === 'dev@example.com') pass('a git identity saves');
else fail('a git identity saves', JSON.stringify(good));

const bad = await call('/api/settings/git-identity', { method: 'PUT', body: { git_email: 'not-an-address' } });
if (bad.status === 400) pass('a malformed git identity is refused');
else fail('a malformed git identity is refused', `got ${bad.status}`);

const cleared = await call('/api/settings/git-identity', { method: 'PUT', body: { git_email: '' } });
if (cleared.status === 200 && cleared.data.gitEmail === '') pass('and it can be cleared');
else fail('and it can be cleared', JSON.stringify(cleared));

// ---- the credential ----------------------------------------------------------

const nonsense = await call('/api/settings/openproject', { method: 'PUT', body: { token: 'not-a-real-token' } });
if (nonsense.status === 400 || nonsense.status === 502) {
  // 400 means OpenProject said no; 502 means something in front of it did. Both
  // are correct refusals to store — what would be wrong is a 200.
  pass(`a token that does not work is not stored (${nonsense.status})`);
} else fail('a token that does not work is not stored', `got ${nonsense.status}`);

// An endpoint may not smuggle a credential in its userinfo. `endpoint` is a
// plaintext column by design — it holds a hostname — so a secret placed there
// would sit unencrypted beside the encrypted one and surface in error messages.
const smuggled = await call('/api/settings/openproject', {
  method: 'PUT',
  body: { token: 'x', endpoint: 'https://apikey:SECRET@pms.example.com' },
});
if (smuggled.status === 400 && /unencrypted/i.test(smuggled.data?.detail ?? '')) {
  pass('an endpoint carrying a username or password is refused');
} else fail('an endpoint carrying credentials is refused', JSON.stringify(smuggled));

if (!TOKEN) {
  skip('storing a real credential', 'set TICVAI_OP_TOKEN to exercise it');
} else if (!me.data?.canStoreCredentials) {
  skip('storing a real credential', 'this deployment has no TICVAI_SECRET_KEY');
} else {
  const stored = await call('/api/settings/openproject', { method: 'PUT', body: { token: TOKEN } });
  if (stored.status === 200 && stored.data.connectedAs) {
    pass(`a real token is checked, then stored — connected as ${stored.data.connectedAs}`);
  } else fail('a real token is checked, then stored', JSON.stringify(stored));

  // **The one that matters.** Everything else is plumbing.
  const after = await call('/api/settings/me');
  const body = JSON.stringify(after.data);
  if (!body.includes(TOKEN)) pass('the stored credential is not in the settings payload');
  else fail('the stored credential is not in the settings payload', 'the token came back');

  if (after.data?.openproject?.configured && after.data.openproject.hint) {
    pass(`it comes back as a hint only (${after.data.openproject.hint})`);
  } else fail('it comes back as a hint only', JSON.stringify(after.data?.openproject));

  const gone = await call('/api/settings/openproject', { method: 'DELETE' });
  // Removing it here does not revoke it there, and the answer has to say so —
  // "removed" reading as "revoked" is how a live credential is left lying about.
  if (gone.status === 200 && /OpenProject/i.test(gone.data?.note ?? '')) {
    pass('removing it says plainly that it is still live in OpenProject');
  } else fail('removing it says it is still live in OpenProject', JSON.stringify(gone));

  const empty = await call('/api/settings/me');
  if (empty.data?.openproject?.configured === false) pass('and it is gone');
  else fail('and it is gone', JSON.stringify(empty.data?.openproject));
}

// ---- the verdict -------------------------------------------------------------

const failed = results.filter((ok) => !ok).length;
console.log(`\n${results.length - failed} of ${results.length} checks passed`);
process.exit(failed ? 1 : 0);
