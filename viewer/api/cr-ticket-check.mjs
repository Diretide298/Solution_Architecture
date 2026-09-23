// A change request becoming a ticket, under the ticket it came out of.
//
// The one create in the whole service, so most of this file is about the ways
// it must not happen: twice for one request, into another product's plan, for
// something that was rejected, or by somebody the request is not theirs.
//
// **Run against a stand-in OpenProject**, not the live instance — the live one
// holds the actual delivery plan, and a harness that files tickets into it is a
// harness nobody runs twice. The stand-in speaks real HTTP and returns real HAL,
// so nothing inside the service is stubbed; it also keeps what it was sent,
// which is the only way to assert on the parent and type links ADAM built.
//
//   node <scratch>/fake-openproject.mjs                     # port 8798
//   TICVAI_DB=/tmp/crt.db TICVAI_SECRET_KEY=... \
//     python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/crt.db API=http://localhost:8799 \
//     PMS=http://127.0.0.1:8798 node api/cr-ticket-check.mjs

import { execFileSync } from 'node:child_process';

const API = process.env.API ?? 'http://localhost:8787';
const STORE = process.env.TICVAI_DB ?? '';
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

/** The CLI, against the same store. Granting a platform is the owner's alone,
 *  and owner exists only through here. */
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
  return took.status === 200 ? { ok: true, email } : { ok: false, why: `redeem: ${took.status}` };
}

const connect = (who) =>
  as(who, 'PUT', '/api/settings/openproject', { token: 'harness-key', endpoint: PMS });

const file = (who, fields) => as(who, 'POST', '/api/changes', {
  target_kind: 'screen', target_id: 'POS-002',
  title: fields.title ?? 'The total is wrong on the receipt',
  problem: 'The printed total excludes service charge, and the screen includes it.',
  ...fields,
});

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
check('and is made the super admin, because granting a platform is theirs',
  /is now System Architect/.test(STORE ? cli('owner', 'harness.boss@softlabsgroup.com') : ''),
  STORE ? '' : 'no TICVAI_DB given');
check('and connects to the stand-in OpenProject',
  (await connect('boss')).status === 200);

const mapped = await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 });
check('the ADAM project is pointed at an OpenProject project', mapped.status === 200,
  `${mapped.status} ${JSON.stringify(mapped.data?.detail ?? '')}`);

const lead = await recruit('harness.lead', 'lead');
check('a team lead is invited', lead.ok, lead.why ?? '');
check('and connects too, because every call is made as the person',
  (await connect('harness.lead')).status === 200);
const leadId = (await as('boss', 'GET', '/api/accounts'))
  .data?.accounts?.find((a) => a.email.startsWith('harness.lead'))?.id;
const granted = await as('boss', 'POST', `/api/accounts/${leadId}/scopes`,
  { project_id: 'ticvai', tag: 'frontend', platform: '' });
// Asserted rather than assumed. A silent refusal here leaves the lead with no
// slice, and then every assertion below fails for a reason that has nothing to
// do with tickets — which is how a setup bug reads as a broken feature.
check('and is given the whole of the frontend', granted.status === 200,
  `${granted.status} ${JSON.stringify(granted.data?.detail ?? '')}`);

const outsider = await recruit('harness.rev', 'reviewer');
check('and a reviewer, who has no platform', outsider.ok, outsider.why ?? '');
await connect('harness.rev');

const hand = await recruit('harness.dev', 'dev');
check('and a developer', hand.ok, hand.why ?? '');
await connect('harness.dev');

// ── the ordinary path ────────────────────────────────────────────────

const raised = await file('harness.lead', { ticket: '880' });
check('a request is raised against the ticket it came up in',
  raised.status === 200 && raised.data?.change?.ticket === '880',
  `${raised.status} ${raised.data?.change?.ticket}`);
const CR = raised.data.change.id;

const preview = await as('harness.lead', 'POST', `/api/changes/${CR}/ticket/preview`, {});
check('the preview works out a ticket without creating one', preview.status === 200,
  `${preview.status} ${JSON.stringify(preview.data?.detail ?? '')}`);
check('and names the parent it will hang under, by subject and not only by number',
  preview.data?.willCreate?.parent?.key === '880'
  && /Checkout/.test(preview.data?.willCreate?.parent?.subject ?? ''),
  JSON.stringify(preview.data?.willCreate?.parent ?? null));
check('the subject is the request\'s title, so nobody retypes it',
  preview.data?.willCreate?.subject === 'The total is wrong on the receipt',
  preview.data?.willCreate?.subject);
check('the type is the project\'s own default rather than a name hardcoded here',
  preview.data?.willCreate?.type === 'Task', preview.data?.willCreate?.type);
check('and the offered types come from the project',
  (preview.data?.types ?? []).map((t) => t.name).join(',') === 'Task,Bug',
  (preview.data?.types ?? []).map((t) => t.name).join(','));
check('the description carries the problem across',
  /service charge/.test(preview.data?.willCreate?.description ?? ''), '');
check('and points back at the request it came from',
  new RegExp(`Raised in ADAM as ${CR}`).test(preview.data?.willCreate?.description ?? ''),
  (preview.data?.willCreate?.description ?? '').slice(-70));
check('it says plainly that nothing has happened yet',
  /Nothing has been created/.test(preview.data?.note ?? ''), preview.data?.note);

// Nothing was sent. The assertion the whole propose-then-confirm pattern is for.
const quietSoFar = await (await fetch(`${PMS}/_created`)).json();
check('and the preview really sent nothing', (quietSoFar.created ?? []).length === 0,
  `${(quietSoFar.created ?? []).length} created`);

const made = await as('harness.lead', 'POST',
  `/api/changes/${CR}/ticket/${preview.data.proposal}/apply`, {});
check('applying creates it', made.status === 200 && made.data?.ticket?.key,
  `${made.status} ${JSON.stringify(made.data?.detail ?? made.data?.ticket ?? '')}`);
// Read once per block rather than inline three times, so a failure earlier
// cannot take the file down on `.at(-1)` of an empty list — a crash hides
// every assertion after it, which is worse than the failure it came from.
const sent = async () => (await (await fetch(`${PMS}/_created`)).json()).created ?? [];
const last = (await sent()).at(-1) ?? {};
check('as a child of the original, which is the whole point',
  last.parent === '/api/v3/work_packages/880', String(last.parent));
check('in this ADAM project\'s OpenProject project and no other',
  last.project === 42, String(last.project));
check('the request now carries the ticket it produced',
  made.data?.change?.childTicket === made.data?.ticket?.key,
  `${made.data?.change?.childTicket}`);
check('which is a different field from the one it came out of',
  made.data?.change?.ticket === '880' && made.data?.change?.childTicket !== '880',
  `${made.data?.change?.ticket} vs ${made.data?.change?.childTicket}`);

const linked = await as('harness.lead', 'GET',
  `/api/links?target_kind=screen&target_id=POS-002&project_id=ticvai`);
check('and the artefact is linked to it, which is the question the boards ask',
  (linked.data?.links ?? []).some((l) => l.key === made.data.ticket.key),
  (linked.data?.links ?? []).map((l) => l.key).join(' ') || 'none');

// ── once, and only once ──────────────────────────────────────────────

const twice = await as('harness.lead', 'POST',
  `/api/changes/${CR}/ticket/${preview.data.proposal}/apply`, {});
check('the same proposal cannot be applied twice', twice.status === 409, `${twice.status}`);

const again = await as('harness.lead', 'POST', `/api/changes/${CR}/ticket/preview`, {});
check('and a second preview is refused, naming the ticket that already exists',
  again.status === 409 && String(again.data?.detail).includes(made.data.ticket.key),
  `${again.status} ${String(again.data?.detail)}`);

const countNow = (await sent()).length;
check('so OpenProject holds exactly one ticket for this request', countNow === 1,
  `${countNow}`);

// ── the ways it must not happen ──────────────────────────────────────

const elsewhere = await file('harness.lead', { ticket: '991', title: 'Raised from another product' });
const crossed = await as('harness.lead', 'POST',
  `/api/changes/${elsewhere.data.change.id}/ticket/preview`, {});
check('a child cannot be filed under a ticket in another OpenProject project',
  crossed.status >= 400, `${crossed.status} ${String(crossed.data?.detail).slice(0, 70)}`);

// Who may file one follows who may settle it, and that is a decision rather
// than a coincidence: filing the ticket is the act of saying this becomes work.
// So the line is not "whose platform is it" — a reviewer settles anything on
// the project and therefore schedules anything on it — it is between the people
// who decide and the people who carry it out.
const notMine = await file('harness.lead', { ticket: '880', title: 'Somebody has to decide' });
const byDev = await as('harness.dev', 'POST',
  `/api/changes/${notMine.data.change.id}/ticket/preview`, {});
check('a developer cannot schedule work for themselves',
  byDev.status === 403, `${byDev.status} ${String(byDev.data?.detail).slice(0, 60)}`);

const byReviewer = await as('harness.rev', 'POST',
  `/api/changes/${notMine.data.change.id}/ticket/preview`, {});
check('but a reviewer can, because a reviewer settles anything on the project',
  byReviewer.status === 200, `${byReviewer.status} ${JSON.stringify(byReviewer.data?.detail ?? '')}`);

const rejected = await file('harness.lead', { ticket: '880', title: 'This one was wrong' });
await as('boss', 'POST', `/api/changes/${rejected.data.change.id}/resolve`,
  { status: 'rejected', resolution: 'The receipt is right; the screen is wrong.' });
const noBuild = await as('harness.lead', 'POST',
  `/api/changes/${rejected.data.change.id}/ticket/preview`, {});
check('a rejected request has nothing to build',
  noBuild.status === 409 && /nothing to build/i.test(String(noBuild.data?.detail)),
  String(noBuild.data?.detail));

const borrowed = await file('harness.lead', { ticket: '880', title: 'A proposal is for one request' });
const forOne = await as('harness.lead', 'POST',
  `/api/changes/${borrowed.data.change.id}/ticket/preview`, {});
const stolen = await as('harness.lead', 'POST',
  `/api/changes/${notMine.data.change.id}/ticket/${forOne.data.proposal}/apply`, {});
check('a proposal made for one request cannot be applied to another',
  stolen.status === 404, `${stolen.status}`);

const strangerToken = await as('boss', 'POST',
  `/api/changes/${borrowed.data.change.id}/ticket/${forOne.data.proposal}/apply`, {});
check('nor can somebody else apply the proposal you were shown',
  strangerToken.status === 404, `${strangerToken.status}`);

// ── a request that came from no ticket at all ────────────────────────
//
// Allowed, because refusing it would leave the most common kind of request —
// one raised from the viewer, reading the package — with no way to be
// scheduled. It is said out loud instead, because a top-level ticket is not
// what anybody asking for this had in mind.

const loose = await file('harness.lead', { title: 'Found while reading the package' });
const looseView = await as('harness.lead', 'POST',
  `/api/changes/${loose.data.change.id}/ticket/preview`, { type_id: 7 });
check('a request with no ticket can still be scheduled', looseView.status === 200,
  `${looseView.status} ${JSON.stringify(looseView.data?.detail ?? '')}`);
check('and is told it will be top level rather than finding out afterwards',
  looseView.data?.topLevel === true && looseView.data?.willCreate?.parent === null,
  `topLevel:${looseView.data?.topLevel}`);
check('a named type is honoured over the default',
  looseView.data?.willCreate?.type === 'Bug', looseView.data?.willCreate?.type);

const looseMade = await as('harness.lead', 'POST',
  `/api/changes/${loose.data.change.id}/ticket/${looseView.data.proposal}/apply`, {});
check('and it is created with no parent link at all',
  looseMade.status === 200 && ((await sent()).at(-1) ?? {}).parent === null,
  `${looseMade.status} ${String(((await sent()).at(-1) ?? {}).parent)}`);
check('as the type that was asked for', looseMade.data?.ticket?.type === 'Bug',
  looseMade.data?.ticket?.type);

const badType = await as('harness.lead', 'POST',
  `/api/changes/${notMine.data.change.id}/ticket/preview`, { type_id: 404 });
check('a type the project does not offer is refused, and the real ones listed',
  badType.status === 400 && /Task/.test(String(badType.data?.detail)),
  String(badType.data?.detail));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
