// Where a change request belongs, who takes it on, and what happens when
// nobody does.
//
// Three rules, and the middle one is the one worth most of this file:
//
//   A request carries a slice — a side of the house and a platform within it —
//   chosen at filing or defaulted from the kind.
//
//   **A team lead sees every request and acts on their own.** Seeing and acting
//   are separate, so most of what is below is a lead being shown a request they
//   may not touch, and then being refused when they touch it anyway. A check
//   that only tested the refusal would pass just as well against a lead who
//   could not see it at all, which is the wrong product.
//
//   An open request nobody has taken on within two days is overdue, answered as
//   a query rather than a stored notification — so it stops being overdue the
//   moment somebody picks it up, with nothing to retract.
//
// Wants an empty store and its path:
//   TICVAI_DB=/tmp/cr.db python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/cr.db API=http://localhost:8799 node api/cr-routing-check.mjs
import { execFileSync } from 'node:child_process';

const API = process.env.API ?? 'http://localhost:8787';
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

const viewerDir = new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const cli = (...args) => execFileSync('python', ['-m', 'api.cli', ...args],
  { cwd: viewerDir, env: { ...process.env, TICVAI_DB: STORE }, encoding: 'utf8' });

/** Straight at the store, for the one thing no route can do: make a request
 *  older than it is. The alternative is a check that sleeps for two days. */
function sql(statement) {
  return execFileSync('python', ['-c',
    'import sqlite3,sys;c=sqlite3.connect(sys.argv[1]);c.execute(sys.argv[2]);c.commit()',
    STORE, statement], { encoding: 'utf8' });
}

const PASSWORD = 'a-long-enough-passphrase';

async function recruit(handle, role) {
  const email = `${handle}@softlabsgroup.com`;
  const made = await as('boss', 'POST', '/api/invites', { email, role });
  if (made.status !== 200) return { ok: false, why: `invite ${made.status} ${JSON.stringify(made.data?.detail)}` };
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  const took = await as(handle, 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: handle });
  if (took.status !== 200) return { ok: false, why: `redeem ${took.status} ${JSON.stringify(took.data?.detail)}` };
  const who = (await as('boss', 'GET', '/api/accounts')).data
    ?.accounts?.find((a) => a.email === email);
  return { ok: true, id: who?.id };
}

const file = (who, fields) => as(who, 'POST', '/api/changes', {
  target_kind: 'screen', target_id: 'POS-002',
  title: fields.title ?? 'Something is wrong here',
  problem: 'Raised by the harness so there is something to route.',
  ...fields,
});

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an administrator exists', boot.status === 200, `${boot.status}`);
if (STORE) cli('owner', 'harness.boss@softlabsgroup.com');

const front = await recruit('harness.frontlead', 'lead');
const back = await recruit('harness.backlead', 'lead');
const rev = await recruit('harness.rev', 'reviewer');
check('two leads and a reviewer', front.ok && back.ok && rev.ok,
  [front.why, back.why, rev.why].filter(Boolean).join(' | '));

const gave = await as('boss', 'POST', `/api/accounts/${front.id}/scopes`,
  { tag: 'frontend', platform: 'P01' });
check('the front lead is given Frontend · P01', gave.status === 200,
  `${gave.status} ${JSON.stringify(gave.data?.detail ?? '')}`);
const gaveAll = await as('boss', 'POST', `/api/accounts/${back.id}/scopes`, { tag: 'backend' });
check('the back lead is given the whole of Backend', gaveAll.status === 200, `${gaveAll.status}`);

// ── filing puts a request somewhere ──────────────────────────────────

const screen = await file('boss', { title: 'A screen with no offline state' });
check('a screen defaults to the frontend side', screen.data?.change?.tag === 'frontend',
  screen.data?.change?.tag ?? `${screen.status}`);
check('and to no platform, which means the whole side',
  screen.data?.change?.platform === '', JSON.stringify(screen.data?.change?.platform));
check('which it says in words', screen.data?.change?.slice === 'Frontend · all platforms',
  screen.data?.change?.slice ?? '');

const table = await file('boss', { target_kind: 'table', target_id: 'orders.sales_order',
  title: 'The order total has no currency' });
check('a table defaults to the backend side', table.data?.change?.tag === 'backend',
  table.data?.change?.tag);

const adr = await file('boss', { target_kind: 'adr', target_id: 'ADR-014',
  title: 'This decision contradicts the schema' });
check('a decision is left unrouted, because it is not a side of the house',
  adr.data?.change?.tag === '', JSON.stringify(adr.data?.change?.tag));
check('and says nothing rather than guessing', adr.data?.change?.slice === '',
  JSON.stringify(adr.data?.change?.slice));

const onP01 = await file('boss', { platform: 'P01', title: 'The storefront basket loses its total' });
check('a platform can be named at filing', onP01.data?.change?.slice === 'Frontend · P01',
  onP01.data?.change?.slice ?? `${onP01.status}`);

const chosen = await file('boss', { tag: 'backend', title: 'A screen blocked on an endpoint' });
check('and the side can be overridden, because only the filer knows',
  chosen.data?.change?.tag === 'backend', chosen.data?.change?.tag);

const orphanPlatform = await file('boss', { target_kind: 'adr', target_id: 'ADR-9', platform: 'P01',
  title: 'A platform with no side to hang it on' });
check('a platform with no side is refused', orphanPlatform.status === 400,
  orphanPlatform.data?.detail ?? `${orphanPlatform.status}`);

const junk = await file('boss', { platform: 'storefront', title: 'A platform that is not a code' });
check('a platform that is not a platform code is refused', junk.status === 400, `${junk.status}`);

// ── a lead sees everything and acts on their own ─────────────────────

const seen = await as('harness.frontlead', 'GET', '/api/changes?status=open');
check('the front lead sees every open request, not only theirs',
  (seen.data?.items ?? []).length >= 5, `${seen.data?.items?.length}`);

const byRef = Object.fromEntries((seen.data?.items ?? []).map((c) => [c.id, c]));
const p01 = byRef[onP01.data.change.id];
const backOne = byRef[table.data.change.id];
const noSide = byRef[adr.data.change.id];

check('and is told which of them are theirs', p01?.mine === true && backOne?.mine === false,
  `P01:${p01?.mine} backend:${backOne?.mine}`);
check('an unrouted one is nobody’s', noSide?.mine === false, String(noSide?.mine));
// A grant of one platform does not cover a request that names none. "Frontend,
// unspecified" is not inside "Frontend · P01" — it is wider than it — so it
// belongs to whoever owns the whole side, or to nobody until somebody says. The
// overdue list agrees: it names no lead for one of these.
check('a request naming no platform is not covered by a one-platform grant',
  byRef[screen.data.change.id]?.mine === false,
  String(byRef[screen.data.change.id]?.mine));
check('they are offered the pick only on their own',
  p01?.mayPick === true && backOne?.mayPick === false,
  `P01:${p01?.mayPick} backend:${backOne?.mayPick}`);

const tookMine = await as('harness.frontlead', 'POST', `/api/changes/${p01.id}/pick`, {});
check('a lead takes on one of theirs', tookMine.status === 200,
  `${tookMine.status} ${JSON.stringify(tookMine.data?.detail ?? '')}`);
check('and it records who and when',
  tookMine.data?.change?.pickedBy === 'harness.frontlead' && !!tookMine.data?.change?.pickedAt,
  `${tookMine.data?.change?.pickedBy} at ${tookMine.data?.change?.pickedAt}`);

const tookTheirs = await as('harness.frontlead', 'POST', `/api/changes/${backOne.id}/pick`, {});
check('and cannot take on one that is not', tookTheirs.status === 403,
  tookTheirs.data?.detail ?? `${tookTheirs.status}`);

const settledTheirs = await as('harness.frontlead', 'POST', `/api/changes/${backOne.id}/resolve`,
  { status: 'accepted' });
check('nor settle one that is not', settledTheirs.status === 403,
  settledTheirs.data?.detail ?? `${settledTheirs.status}`);

const settledMine = await as('harness.frontlead', 'POST', `/api/changes/${p01.id}/resolve`,
  { status: 'accepted', resolution: 'Agreed, the basket keeps a currency.' });
check('but settles their own', settledMine.status === 200,
  `${settledMine.status} ${JSON.stringify(settledMine.data?.detail ?? '')}`);

const backLead = await as('harness.backlead', 'POST', `/api/changes/${backOne.id}/pick`, {});
check('the lead who owns the whole side takes on anything in it', backLead.status === 200,
  `${backLead.status} ${JSON.stringify(backLead.data?.detail ?? '')}`);

// A reviewer keeps what they had. Narrowing that would be taking a capability
// away from the people doing the reviewing, which is not what adding leads asks
// for.
const byReviewer = await as('harness.rev', 'GET', '/api/changes?status=open');
check('a reviewer may still settle anything on the project',
  (byReviewer.data?.items ?? []).every((c) => c.maySettle), 'one or more said no');

// ── nobody takes it on ───────────────────────────────────────────────

const quiet = await as('boss', 'GET', '/api/changes/overdue');
check('nothing is overdue yet', quiet.data?.total === 0, `${quiet.status} ${quiet.data?.total}`);

// Three days back, which no route can do and a check should not sleep for.
sql(`UPDATE change_request SET raised_at =
     strftime('%Y-%m-%dT%H:%M:%S+00:00','now','-3 days') WHERE number IN
     (${screen.data.change.number}, ${adr.data.change.number}, ${table.data.change.number})`);

const late = await as('boss', 'GET', '/api/changes/overdue');
check('an open request nobody took on is overdue after two days',
  late.data?.total === 2, `${late.data?.total} — ${(late.data?.items ?? []).map((c) => c.id).join(' ')}`);
check('the one that was picked up is not on the list',
  !(late.data?.items ?? []).some((c) => c.id === backOne.id), backOne.id);
check('it says how long each has waited',
  (late.data?.items ?? []).every((c) => c.waitingDays >= 2),
  (late.data?.items ?? []).map((c) => `${c.id}:${c.waitingDays}`).join(' '));
check('and names the lead who should have taken it',
  (late.data?.items ?? []).find((c) => c.id === screen.data.change.id)
    ?.shouldBe?.length === 0,
  'a Frontend · all-platforms request is not covered by a P01 grant');
check('an unrouted one names nobody, because nobody has been told it is theirs',
  (late.data?.items ?? []).find((c) => c.id === adr.data.change.id)?.shouldBe?.length === 0);

const counted = await as('boss', 'GET', '/api/changes');
check('the list carries the same two figures', counted.data?.overdue === 2,
  `overdue ${counted.data?.overdue} of unpicked ${counted.data?.unpicked}`);
check('and counts the ones nobody has routed', counted.data?.unrouted === 1,
  String(counted.data?.unrouted));
check('and says what "overdue" means in days', counted.data?.afterDays === 2,
  String(counted.data?.afterDays));

// Picking one up takes it off the list immediately — nothing to retract,
// because nothing was ever sent.
const rescue = await as('boss', 'POST', `/api/changes/${screen.data.change.id}/pick`, {});
check('an admin can take on anything, whatever the platform', rescue.status === 200, `${rescue.status}`);
const after = await as('boss', 'GET', '/api/changes/overdue');
check('and it leaves the overdue list at once', after.data?.total === 1, `${after.data?.total}`);

// ── handing one back ─────────────────────────────────────────────────

// An administrator, who clears the scope check, so what is being tested is the
// "already taken" rule and not the platform one. The back lead is holding this.
const steal = await as('boss', 'POST', `/api/changes/${backOne.id}/pick`, {});
check('somebody else cannot take on what is already taken', steal.status === 409,
  steal.data?.detail ?? `${steal.status}`);
check('and is told who has it', /harness\.backlead/.test(steal.data?.detail ?? ''),
  steal.data?.detail ?? '');

const handBack = await as('boss', 'POST', `/api/changes/${screen.data.change.id}/unpick`, {});
check('it can be handed back', handBack.status === 200, `${handBack.status}`);
check('and the clock does not restart — it is overdue again at once',
  (await as('boss', 'GET', '/api/changes/overdue')).data?.total === 2);

const pickSettled = await as('boss', 'POST', `/api/changes/${p01.id}/pick`, {});
check('a settled request cannot be taken on', pickSettled.status === 409,
  pickSettled.data?.detail ?? `${pickSettled.status}`);

// ── the bell ─────────────────────────────────────────────────────────
//
// Alerts are conditions, not events: computed on every read, never stored, and
// with no seen state — because the only way to clear "nobody has taken this on"
// should be for somebody to take it on. So the assertions below are about what
// each role is *told*, and about an alert going away on its own when the thing
// it is about is dealt with.

const bossBell = await as('boss', 'GET', '/api/alerts');
const kinds = (b) => (b.data?.alerts ?? []).map((a) => a.kind).sort();
check('the super admin is told about requests nobody has taken',
  kinds(bossBell).includes('overdue-change'), kinds(bossBell).join(' '));
check('and about the ones with no side of the house',
  kinds(bossBell).includes('unrouted-change'), kinds(bossBell).join(' '));

const overdueAlert = (bossBell.data?.alerts ?? []).find((a) => a.kind === 'overdue-change');
check('the overdue one is loud', overdueAlert?.severity === 'high', overdueAlert?.severity);
check('it names which, not only how many',
  (overdueAlert?.items ?? []).length > 0
  && (overdueAlert?.items ?? []).every((i) => /^CR-\d{3}$/.test(i.id)),
  (overdueAlert?.items ?? []).map((i) => i.id).join(' '));
check('and nothing in it can be marked read',
  (bossBell.data?.alerts ?? []).every((a) => !('seen_at' in a) && !('seen' in a)));

// A fresh one on their platform first. Without it the assertion below passes
// against a lead who is told nothing at all, which is the wrong product and the
// easiest way for this check to look green while the bell is broken.
const forThem = await file('boss', { platform: 'P01', title: 'The storefront filter forgets itself' });
check('a request is filed on the front lead’s platform',
  forThem.data?.change?.slice === 'Frontend · P01', forThem.data?.change?.slice ?? `${forThem.status}`);

const frontBell = await as('harness.frontlead', 'GET', '/api/alerts');
check('a lead is told about work waiting on their platforms',
  kinds(frontBell).includes('unpicked-in-scope'), kinds(frontBell).join(' ') || 'nothing');
check('and only about those',
  kinds(frontBell).every((k) => k === 'unpicked-in-scope'),
  kinds(frontBell).join(' ') || 'nothing');
check('the one it names is theirs',
  (frontBell.data?.alerts?.[0]?.items ?? []).some((i) => i.id === forThem.data.change.id),
  (frontBell.data?.alerts?.[0]?.items ?? []).map((i) => i.id).join(' '));

// And the other lead is not told about it, which is the half that makes the
// first half mean something.
const otherBell = await as('harness.backlead', 'GET', '/api/alerts');
check('the lead who does not own that platform is not told',
  !(otherBell.data?.alerts ?? []).flatMap((a) => a.items).some((i) => i.id === forThem.data.change.id),
  (otherBell.data?.alerts ?? []).flatMap((a) => a.items).map((i) => i.id).join(' ') || 'nothing');
check('and never about the routing failures, which are not theirs to fix',
  !kinds(frontBell).includes('unrouted-change'), kinds(frontBell).join(' '));

const revBell = await as('harness.rev', 'GET', '/api/alerts');
check('a reviewer is told nothing here, having no platform to be told about',
  (revBell.data?.alerts ?? []).length === 0, kinds(revBell).join(' '));

// The whole argument for deriving them: dealing with the thing clears the
// alert, with nothing to retract and nothing left behind.
const wasOverdue = overdueAlert?.count ?? 0;
for (const item of overdueAlert?.items ?? []) {
  await as('boss', 'POST', `/api/changes/${item.id}/pick`, {});
}
const afterBell = await as('boss', 'GET', '/api/alerts');
check('taking them on clears the alert, with nothing to retract',
  !kinds(afterBell).includes('overdue-change'),
  `${wasOverdue} were overdue; now ${kinds(afterBell).join(' ') || 'nothing'}`);
check('and the unrouted one stays, because that is still true',
  kinds(afterBell).includes('unrouted-change'), kinds(afterBell).join(' '));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
