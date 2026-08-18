// Does the gate hold, and does a guest actually get less?
//
// The claim being tested is not "the tab is hidden". It is that the payload a
// guest receives does not contain the branch at all — because a client handed a
// login can open devtools and fetch whatever the server will answer. So this
// asks the server directly, with a guest's cookie, the way a curious client
// would.
//
//   node checks/guest-check.mjs
//
// Needs both services up: server.mjs on 4173 and uvicorn on 8787.

const V = process.env.TICVAI_VIEWER ?? 'http://localhost:4173';
const API = process.env.TICVAI_API ?? 'http://localhost:8787';
const ADMIN = process.env.TICVAI_USER ?? 'chinmay.parab@softlabsgroup.com';
const PASS = process.env.TICVAI_PASS ?? 'the-first-administrator';

// Deliberately outside softlabsgroup.com — the whole point of the role.
const GUEST_EMAIL = process.env.TICVAI_GUEST ?? 'a.client@example.com';
const GUEST_PASS = 'a-guest-password-long-enough';

// The harness creates a real account, so it has to be able to remove one. There
// is deliberately no delete endpoint — a verdict points at the person who gave
// it — so this reaches the database directly, and only ever for the one address
// it made up. Anything else here goes through the API like a client would.
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const DB = process.env.TICVAI_DB
  ?? path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'api', 'ticvai.db');

function forgetTestGuest(why) {
  try {
    const db = new DatabaseSync(DB);
    const folded = GUEST_EMAIL.trim().toLowerCase();
    const row = db.prepare('SELECT id FROM account WHERE email_folded = ?').get(folded);
    if (row) {
      db.prepare('DELETE FROM verdict WHERE account_id = ?').run(row.id);
      db.prepare('DELETE FROM session WHERE account_id = ?').run(row.id);
      db.prepare('DELETE FROM account WHERE id = ?').run(row.id);
    }
    db.prepare('DELETE FROM invite WHERE email_folded = ?').run(folded);
    db.close();
    console.log(`  ${why}: ${GUEST_EMAIL} removed`);
  } catch (e) {
    console.log(`  ${why}: could not tidy up — ${e.message}`);
  }
}

let failures = 0;
const ok = (cond, what) => {
  console.log(`  ${cond ? 'ok  ' : 'FAIL'}  ${what}`);
  if (!cond) failures += 1;
};

const cookieOf = (res) => {
  const raw = res.headers.getSetCookie?.() ?? [];
  for (const line of raw) {
    const [pair] = line.split(';');
    if (pair.startsWith('ticvai_session=')) return pair;
  }
  return null;
};

const get = (base, path, cookie) =>
  fetch(`${base}${path}`, {
    headers: cookie ? { cookie } : {},
    redirect: 'manual',
  });

console.log('\nbefore anything, clear any guest left by an earlier run');
forgetTestGuest('pre-clean');

// ── 1. the gate ───────────────────────────────────────────────────────
console.log('\nthe gate — nothing without a session');
{
  for (const path of ['/api/index', '/api/backend', '/api/decisions', '/api/file?path=README.md']) {
    const res = await get(V, path);
    ok(res.status === 401, `${path} → ${res.status} (want 401)`);
  }
  const page = await get(V, '/index.html');
  ok(page.status === 302, `/index.html → ${page.status} (want 302 to the sign-in page)`);
  const login = await get(V, '/login.html');
  ok(login.status === 200, `/login.html → ${login.status} (want 200 — the one public page)`);
}

// ── 2. sign in as the admin ───────────────────────────────────────────
console.log('\nadmin');
const adminRes = await fetch(`${API}/api/auth/login`, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: ADMIN, password: PASS }),
});
const adminCookie = cookieOf(adminRes);
ok(adminRes.ok && adminCookie, `signed in as ${ADMIN}`);
if (!adminCookie) {
  console.log('\ncannot continue without an admin session');
  process.exit(1);
}
{
  const res = await get(V, '/api/decisions', adminCookie);
  ok(res.status === 200, `/api/decisions → ${res.status} (want 200 — an admin may read it)`);
}

// ── 3. an outside address can only be a guest ─────────────────────────
console.log('\nthe domain rule, and its one exception');
{
  const asReviewer = await fetch(`${API}/api/invites`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', cookie: adminCookie },
    body: JSON.stringify({ email: GUEST_EMAIL, role: 'reviewer' }),
  });
  ok(asReviewer.status === 400,
     `invite ${GUEST_EMAIL} as reviewer → ${asReviewer.status} (want 400 — off-domain)`);

  const asGuest = await fetch(`${API}/api/invites`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', cookie: adminCookie },
    body: JSON.stringify({ email: GUEST_EMAIL, role: 'guest' }),
  });
  ok(asGuest.ok, `invite ${GUEST_EMAIL} as guest → ${asGuest.status} (want 200)`);
  if (!asGuest.ok) { console.log(await asGuest.text()); process.exit(1); }

  const invite = await asGuest.json();
  // security.stamp() is isoformat(), which already carries the offset —
  // appending a Z made it unparseable and the check silently read NaN.
  const days = Math.round((new Date(invite.expires_at) - Date.now()) / 86_400_000);
  ok(days <= 3, `guest invite expires in ~${days} days (want 3 or fewer)`);

  // redeem it
  const redeemed = await fetch(`${API}/api/auth/redeem`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ token: invite.token, name: 'A Client', password: GUEST_PASS }),
  });
  ok(redeemed.ok, `redeemed → ${redeemed.status}`);
  var guestCookie = cookieOf(redeemed);
  ok(Boolean(guestCookie), 'guest has a session');
}

// ── 4. what the guest may read ────────────────────────────────────────
console.log('\nthe guest boundary — asked of the server, not the browser');
{
  const allowed = ['/api/index', '/api/journeys', '/api/tooltips'];
  const refused = ['/api/decisions', '/api/backend', '/api/lineage', '/api/domain',
                   '/api/domains', '/api/tree?path=states/order.yaml',
                   '/api/file?path=docs/adr/0025-one-audience-field.md'];

  for (const path of allowed) {
    const res = await get(V, path, guestCookie);
    ok(res.status === 200, `${path} → ${res.status} (want 200)`);
  }
  for (const path of refused) {
    const res = await get(V, path, guestCookie);
    ok(res.status === 403, `${path} → ${res.status} (want 403)`);
  }

  // The audit travels inside the index rather than as its own endpoint, so
  // hiding the Audit view would have left the defect list in the payload.
  const index = await get(V, '/api/index', guestCookie).then((r) => r.json());
  ok(Array.isArray(index.problems) && index.problems.length === 0,
     `the guest index carries ${index.problems?.length ?? '?'} problems (want 0)`);
  ok(index.guest === true, 'the guest index says it is one');

  const session = await get(V, '/api/session', guestCookie).then((r) => r.json());
  ok(session.role === 'guest', `/api/session says role=${session.role}`);
  ok(JSON.stringify(session.layers) === '["frontend","contracts"]',
     `layers = ${JSON.stringify(session.layers)} (want frontend, contracts)`);
}

// ── 5. read-only, enforced on the server ──────────────────────────────
console.log('\nread-only');
{
  const wrote = await fetch(`${API}/api/validation`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', cookie: guestCookie },
    body: JSON.stringify({
      target_kind: 'screen', target_id: 'GST-001',
      verdict: 'approved', note: 'a guest should not be able to say this',
    }),
  });
  ok(wrote.status === 403, `POST /api/validation as a guest → ${wrote.status} (want 403)`);
}

// ── tidy up ───────────────────────────────────────────────────────────
console.log('\ncleaning up');
forgetTestGuest('post-clean');

console.log(`\n${failures ? `${failures} FAILURES` : 'all checks passed'}\n`);
process.exit(failures ? 1 : 0);
