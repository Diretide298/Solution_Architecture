// The allowlist: off until somebody turns it on, and refusing to be turned on
// in a way that strands them.
//
// Three properties, and the second is what most of this file is about:
//
//   **It ships permissive and watching.** No rules, nobody refused, and a row
//   per account and address from the first request — so the rules can be
//   written from where people have actually been rather than from memory.
//
//   **Arming is refused unless it is safe.** No rules, no address, no rule
//   covering the address asking, no typed confirmation: four separate refusals,
//   because an allowlist that locks out the person who installed it is the
//   characteristic failure of the whole idea, not an edge case.
//
//   **A refusal says what happened.** 403 naming the address, not a silent
//   redirect to a sign-in page that will not work either.
//
// Every request below carries X-Real-IP. The harness is on loopback, which the
// service trusts, so the header is believed — that is how one process pretends
// to be an office, a hotel and a stranger in turn. The trust rule itself is not
// testable from here and lives in api/netaddr-check.py.
//
// Wants an empty store and its path:
//   TICVAI_DB=/tmp/ip.db python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/ip.db API=http://localhost:8799 node api/ip-check.mjs
import { execFileSync } from 'node:child_process';

const API = process.env.API ?? 'http://localhost:8787';
const STORE = process.env.TICVAI_DB ?? '';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

// Somewhere to be. OFFICE is the address the allowlist will end up naming;
// HOTEL is a real colleague somewhere else, which is the case that makes arming
// a decision rather than a formality; STRANGER never gets a rule.
const OFFICE = '203.0.113.7';
const HOTEL = '198.51.100.22';
const STRANGER = '192.0.2.99';

const jars = new Map();
async function as(who, method, path, body, ip = OFFICE) {
  const cookie = jars.get(who);
  const res = await fetch(`${API}${path}`, {
    method,
    headers: {
      'content-type': 'application/json',
      // Always sent. A request without one is answered as loopback, which no
      // rule covers, so a single omission after arming would fail the rest of
      // the file for a reason that has nothing to do with what it is testing.
      'x-real-ip': ip,
      ...(cookie ? { cookie } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) jars.set(who, set.split(';')[0]);
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data };
}

// Only for the subcommands that do not prompt. `admin` and `passwd` read the
// password with getpass, which on Windows talks to the console rather than to
// stdin — a piped answer is ignored and the harness hangs instead of failing.
function cli(...args) {
  return execFileSync('python', ['-m', 'api.cli', ...args], {
    cwd: new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'),
    env: { ...process.env, TICVAI_DB: STORE },
    encoding: 'utf8',
  });
}

const PASSWORD = 'a-long-enough-passphrase';

async function recruit(handle, role, ip = OFFICE) {
  const email = `${handle}@softlabsgroup.com`;
  const made = await as('boss', 'POST', '/api/invites', { email, role }, ip);
  if (made.status !== 200) return { ok: false, why: `invite: ${made.status}` };
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  if (!token) return { ok: false, why: 'no token' };
  const took = await as(handle, 'POST', '/api/auth/redeem',
    { token, password: PASSWORD, name: handle }, ip);
  if (took.status !== 200) return { ok: false, why: `redeem: ${took.status}` };
  return { ok: true, email };
}

// ── it ships off ─────────────────────────────────────────────────────
//
// Before anything else, because "all IPs allowed at the start" is the thing
// that was asked for and the thing a later change is most likely to break.

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('the first account is made with no allowlist in the way', boot.status === 200,
  `${boot.status}`);
check('the CLI makes them the super admin',
  /is now owner/.test(STORE ? cli('owner', 'harness.boss@softlabsgroup.com') : ''),
  STORE ? '' : 'no TICVAI_DB given');

const first = await as('boss', 'GET', '/api/ips');
check('the policy starts disarmed', first.data?.armed === false, String(first.data?.armed));
check('with no rules at all', (first.data?.rules ?? []).length === 0,
  String((first.data?.rules ?? []).length));
check('and the service knows where the caller is', first.data?.you === OFFICE,
  first.data?.you ?? 'nothing');

// A stranger, with no rule anywhere near them, signs in and is not stopped.
const outsider = await recruit('harness.far', 'reviewer', STRANGER);
check('somebody from an address nobody has named can still be invited and sign in',
  outsider.ok, outsider.why ?? '');

// ── it watches from the first request ────────────────────────────────

await as('harness.far', 'GET', '/api/auth/me', undefined, STRANGER);
await as('harness.far', 'GET', '/api/auth/me', undefined, STRANGER);
const seen = await as('boss', 'GET', '/api/ips/sightings');
const far = (seen.data?.items ?? []).find((i) => i.account.email.startsWith('harness.far'));
check('every account is logged against every address it is seen at',
  far?.ip === STRANGER, far?.ip ?? 'not logged');
check('and the same address twice is one row with a count, not two rows',
  far?.hits >= 2 && (seen.data?.items ?? [])
    .filter((i) => i.account.email === far.account.email && i.ip === STRANGER).length === 1,
  `hits ${far?.hits}`);
check('the log says when, first and last', Boolean(far?.firstSeen && far?.lastSeen),
  `${far?.firstSeen} → ${far?.lastSeen}`);

// The same person somewhere else is a second row, which is the point of the
// table: it is a record of places, not of people.
await as('harness.far', 'GET', '/api/auth/me', undefined, HOTEL);
const twice = await as('boss', 'GET', '/api/ips/sightings');
check('and the same person from a second address is a second row',
  (twice.data?.items ?? []).filter((i) => i.account.email.startsWith('harness.far')).length === 2,
  String((twice.data?.items ?? []).filter((i) => i.account.email.startsWith('harness.far')).length));

// ── the log is the owner's, and only the owner's ─────────────────────
//
// Not caution about the controls — a record of where every colleague has opened
// their laptop for six months is a different kind of object from a list of
// rules, and this is the assertion that says so.

const nosy = await recruit('harness.admin2', 'admin');
check('a second admin exists to ask with', nosy.ok, nosy.why ?? '');
for (const [what, method, path] of [
  ['the rules', 'GET', '/api/ips'],
  ['where people have been', 'GET', '/api/ips/sightings'],
  ['who was turned away', 'GET', '/api/ips/refusals'],
  ['the dry run', 'GET', '/api/ips/dry-run'],
]) {
  const r = await as('harness.admin2', method, path);
  check(`an admin cannot read ${what}`, r.status === 403, `${r.status}`);
}
const pushy = await as('harness.admin2', 'POST', '/api/ips/rules', { cidr: '0.0.0.0/0' });
check('nor let the whole internet in', pushy.status === 403, `${pushy.status}`);
const stranger = await fetch(`${API}/api/ips`, { headers: { 'x-real-ip': OFFICE } });
check('and somebody signed out is asked to sign in, not told what is configured',
  stranger.status === 401, `${stranger.status}`);

// ── writing the rules ────────────────────────────────────────────────

const junk = await as('boss', 'POST', '/api/ips/rules', { cidr: 'the office' });
check('a label is not a network, and the refusal shows the two shapes',
  junk.status === 400 && /203\.0\.113/.test(String(junk.data?.detail)),
  String(junk.data?.detail));

const bare = await as('boss', 'POST', '/api/ips/rules', { cidr: OFFICE, label: 'The office' });
check('a bare address is accepted and stored as a network',
  bare.status === 200 && bare.data?.cidr === `${OFFICE}/32`, bare.data?.cidr);
check('and says so, because the stored form is not what was typed',
  /Stored as/.test(String(bare.data?.note)), String(bare.data?.note));

const again = await as('boss', 'POST', '/api/ips/rules', { cidr: `${OFFICE}/32` });
check('the same rule in the other spelling is a duplicate, not a second rule',
  again.status === 409, `${again.status}`);

// ── arming, and the four ways it is refused ──────────────────────────
//
// The rule above covers the harness, so these are about everything else that
// has to be true.

const noConfirm = await as('boss', 'POST', '/api/ips/arm', {});
check('arming without typing the confirmation is refused', noConfirm.status === 400,
  `${noConfirm.status}`);

const elsewhere = await as('boss', 'POST', '/api/ips/arm', { confirm: 'arm' }, HOTEL);
check('and arming from an address no rule covers is refused, naming it',
  elsewhere.status === 409 && String(elsewhere.data?.detail).includes(HOTEL),
  String(elsewhere.data?.detail));

// ── the dry run, before anything is switched on ──────────────────────
//
// The question is about people, not requests: an account whose every known
// address is uncovered has nowhere to sign in from.

// Somebody the feature has never seen. Not a contrived case: on an existing
// store *every* account is unseen until its owner next signs in, so this is the
// state the first deploy puts the whole company in — and an account with no
// known address is precisely the one that reads as fine and is not.
//
// Redeeming an invite leaves no sighting, which is not a gap: the request that
// redeems carries no cookie yet — the session is in its *response* — so there
// is nobody to hold the address against. One recruit and no second request is
// therefore an account that exists and has never been anywhere.
const ghost = await recruit('harness.ghost', 'reviewer');
check('an account can exist without ever having been seen anywhere',
  ghost.ok, ghost.why ?? '');

const dry = await as('boss', 'GET', '/api/ips/dry-run');
const out = (dry.data?.wouldBeLockedOut ?? []).map((p) => p.email);
check('the dry run names who has nowhere to sign in from',
  out.some((e) => e.startsWith('harness.far')), out.join(' ') || 'nobody');
check('and does not name somebody who has been seen at a covered address',
  !out.some((e) => e.startsWith('harness.boss')), out.join(' '));
check('it also names accounts nobody has seen anywhere, which read as fine otherwise',
  (dry.data?.unseen ?? []).some((p) => p.email.startsWith('harness.ghost')),
  (dry.data?.unseen ?? []).map((p) => p.email).join(' ') || 'nobody');
check('and does not confuse those with the ones it has seen somewhere uncovered',
  !(dry.data?.unseen ?? []).some((p) => p.email.startsWith('harness.far')),
  (dry.data?.unseen ?? []).map((p) => p.email).join(' '));

const wouldBe = await as('boss', 'GET', '/api/ips/refusals');
const dryRows = (wouldBe.data?.items ?? []).filter((r) => r.armed === false);
check('and the refusal log is already carrying would-have-been rows',
  dryRows.length > 0, `${dryRows.length} of ${(wouldBe.data?.items ?? []).length}`);
check('which are recorded against the person, not just the address',
  dryRows.some((r) => r.who && r.who !== 'nobody signed in'),
  dryRows.map((r) => r.who).join(' '));

// ── switched on ──────────────────────────────────────────────────────

const armed = await as('boss', 'POST', '/api/ips/arm', { confirm: 'arm' });
check('arming works from a covered address with the word typed',
  armed.status === 200 && armed.data?.armed === true,
  `${armed.status} ${JSON.stringify(armed.data?.detail ?? '')}`);

const stillIn = await as('boss', 'GET', '/api/ips');
check('the covered address is still let through', stillIn.status === 200, `${stillIn.status}`);

const shutOut = await as('harness.far', 'GET', '/api/auth/me', undefined, STRANGER);
check('and the uncovered one is refused', shutOut.status === 403, `${shutOut.status}`);
check('with a message that names the address rather than blaming the password',
  String(shutOut.data?.detail).includes(STRANGER),
  String(shutOut.data?.detail));

const noLogin = await fetch(`${API}/api/auth/login`, {
  method: 'POST',
  headers: { 'content-type': 'application/json', 'x-real-ip': STRANGER },
  body: JSON.stringify({ email: 'harness.boss@softlabsgroup.com', password: PASSWORD }),
});
check('signing in from there is refused too, which is the point of an allowlist',
  noLogin.status === 403, `${noLogin.status}`);

const health = await fetch(`${API}/api/health`, { headers: { 'x-real-ip': STRANGER } });
check('health is answered anyway, so monitoring does not read as an outage',
  health.status === 200, `${health.status}`);

// ── and it will not let you lock the door behind you ─────────────────

const rules = (await as('boss', 'GET', '/api/ips')).data?.rules ?? [];
const mine = rules.find((r) => r.cidr === `${OFFICE}/32`);
const cutOff = await as('boss', 'DELETE', `/api/ips/rules/${mine.id}`);
check('the one rule keeping you in cannot be deleted while it is armed',
  cutOff.status === 409 && String(cutOff.data?.detail).includes(OFFICE),
  `${cutOff.status} ${String(cutOff.data?.detail)}`);

const other = await as('boss', 'POST', '/api/ips/rules', { cidr: '203.0.113.0/24', label: 'All of it' });
check('a wider rule covering the same address is allowed', other.status === 200, `${other.status}`);
const nowFine = await as('boss', 'DELETE', `/api/ips/rules/${mine.id}`);
check('and then the narrow one can go, because something else still covers you',
  nowFine.status === 200, `${nowFine.status}`);

// ── switching off asks nothing ───────────────────────────────────────

const off = await as('boss', 'POST', '/api/ips/disarm', {});
check('disarming takes no confirmation, being the direction that strands nobody',
  off.status === 200 && off.data?.armed === false, `${off.status}`);
const backIn = await as('harness.far', 'GET', '/api/auth/me', undefined, STRANGER);
check('and the shut-out address is immediately back in', backIn.status === 200,
  `${backIn.status}`);

// Left armed on purpose. api/ip-breakglass-check.mjs runs next against this
// same store with ADAM_IP_ALLOWLIST=off, which is the one behaviour that cannot
// be reached from inside a service that is already running.
const rearm = await as('boss', 'POST', '/api/ips/arm', { confirm: 'arm' });
check('and switched back on, which leaves the store armed for the break-glass check',
  rearm.data?.armed === true, `${rearm.status}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
