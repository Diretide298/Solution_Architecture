// What the delivery cost, and the three ways that number is an understatement.
//
// The arithmetic is the easy part. What this file is really about is that the
// page never says a confident total it cannot defend:
//
//   **Money is integer maths on the smallest unit.** A float rate times a float
//   hour count, summed, is a total that disagrees with itself between two
//   readers of the same page.
//
//   **Absent is not zero.** A ticket with no logged time, a ticket whose time
//   this token may not read, and a person with hours but no rate each reduce
//   the total in a different way and are fixed by different people, so they are
//   counted apart rather than added up as nothing.
//
//   **Two currencies cannot be added**, and a page that added them would be
//   wrong in the most expensive possible way.
//
//   node api/fake-openproject.mjs                           # port 8798
//   TICVAI_DB=/tmp/cost.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/cost.db API=http://localhost:8799 PMS=http://127.0.0.1:8798 \
//     node api/costing-check.mjs

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

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
check('connected to OpenProject', (await connect('boss', 'harness-key')).status === 200);
check('the project is mapped',
  (await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);
check('a project manager is invited', (await recruit('harness.pm', 'pm')).ok);
await connect('harness.pm', 'harness-key');
check('and a developer', (await recruit('harness.dev', 'dev')).ok);
await connect('harness.dev', 'harness-key');

// ── hours before rates ───────────────────────────────────────────────

const bare = await as('boss', 'GET', '/api/costing');
check('costing reads without any rates set', bare.status === 200,
  `${bare.status} ${JSON.stringify(bare.data?.detail ?? '')}`);
// Not zero. With no rates set the cost is *unknown*, and a zero is a claim —
// somebody reading it would take it for "this has cost us nothing so far".
check('and says the cost is unknown rather than zero',
  bare.data?.totalCost === null, String(bare.data?.totalCost));
check('with no currency in play, which is how the page tells "nothing priced" '
  + 'apart from "two currencies cannot be added"',
  (bare.data?.currencies ?? []).length === 0,
  (bare.data?.currencies ?? []).join(','));
check('while the hours are real', bare.data?.totalHours > 0, String(bare.data?.totalHours));

// PT12H + PT4H30M + P1DT1H = 12 + 4.5 + 9 = 25.5, and P1D is a working day.
const harness = (bare.data?.people ?? []).find((p) => p.person === 'Harness Person');
check('durations are parsed, including a working day as eight hours',
  harness?.hours === 25.5, String(harness?.hours));
check('estimates are carried separately and never substituted',
  harness?.estimated === 34 && harness?.cost === null,
  `est ${harness?.estimated} cost ${harness?.cost}`);
check('somebody with hours and no rate is named, not silently dropped',
  (bare.data?.peopleWithoutRate ?? []).includes('Harness Person'),
  (bare.data?.peopleWithoutRate ?? []).join(' ') || 'nobody');

// ── absent is not zero ───────────────────────────────────────────────

check('a ticket with a logged zero is counted as having no time',
  bare.data?.ticketsWithoutHours >= 1, String(bare.data?.ticketsWithoutHours));
check('and a ticket whose time cannot be read is counted apart from it',
  bare.data?.ticketsHoursUnreadable >= 1, String(bare.data?.ticketsHoursUnreadable));
check('which are two different numbers, because they are two different problems',
  bare.data?.ticketsWithoutHours !== undefined
  && bare.data?.ticketsHoursUnreadable !== undefined
  && bare.data.ticketsWithoutHours + bare.data.ticketsHoursUnreadable > 0,
  `${bare.data?.ticketsWithoutHours} logged nothing, ${bare.data?.ticketsHoursUnreadable} unreadable`);

// ── a rate, and the multiplication ───────────────────────────────────

const junk = await as('harness.dev', 'PUT', '/api/rates',
  { person: 'Harness Person', hourly: 400000 });
check('a developer cannot set a rate', junk.status === 403, `${junk.status}`);

const set = await as('boss', 'PUT', '/api/rates',
  { person: 'Harness Person', hourly: 450050, currency: 'INR', note: 'Senior' });
check('an admin can', set.status === 200, `${set.status}`);

const priced = await as('boss', 'GET', '/api/costing?refresh=1');
const person = (priced.data?.people ?? []).find((p) => p.person === 'Harness Person');
// 25.5 hours at 4,500.50 is 114,762.75 — 11476275 in the smallest unit, and
// the point of integer maths is that it is exactly that and not .74999.
check('the cost is the hours times the rate, to the smallest unit',
  person?.cost === 11476275, String(person?.cost));
check('and the total agrees with the row', priced.data?.totalCost === 11476275,
  `${priced.data?.totalCost}`);
check('the currency is named once, not per row', priced.data?.currency === 'INR',
  String(priced.data?.currency));
// Somebody Else has six logged hours on the same OpenProject project and no
// rate yet, so the total is still a floor — which is the state a real project
// is in almost all the time, and the reason the page says "at least".
check('the one still unpriced is named, so the total is known to be a floor',
  (priced.data?.peopleWithoutRate ?? []).join(' ') === 'Somebody Else',
  (priced.data?.peopleWithoutRate ?? []).join(' ') || 'nobody');
check('and their hours are absent from the total rather than counted at zero',
  priced.data?.totalCost === person?.cost, `${priced.data?.totalCost} vs ${person?.cost}`);

// ── two currencies cannot be added ───────────────────────────────────

await as('boss', 'PUT', '/api/rates',
  { person: 'Somebody Else', hourly: 8000, currency: 'GBP' });
// Somebody Else's ticket is in the same OpenProject project, so it is in the
// overview even though it is on nobody's board here.
const mixed = await as('boss', 'GET', '/api/costing?refresh=1');
check('with two currencies in play there is no total',
  mixed.data?.totalCost === null, String(mixed.data?.totalCost));
check('and both are named, so the page can say why',
  (mixed.data?.currencies ?? []).join(',') === 'GBP,INR',
  (mixed.data?.currencies ?? []).join(','));
check('each row still carries its own cost, which is defensible',
  (mixed.data?.people ?? []).every((p) => !p.hours || p.cost !== null || !p.hourly),
  JSON.stringify((mixed.data?.people ?? []).map((p) => [p.person, p.cost])));

await as('boss', 'DELETE',
  `/api/rates/${(await as('boss', 'GET', '/api/rates')).data.rates.find((r) => r.currency === 'GBP').id}`);
const single = await as('boss', 'GET', '/api/costing?refresh=1');
check('removing one brings the total back', single.data?.totalCost === 11476275,
  String(single.data?.totalCost));

// ── replacing rather than duplicating ────────────────────────────────

const again = await as('boss', 'PUT', '/api/rates',
  { person: 'harness person', hourly: 500000, currency: 'INR' });
check('the same person in different case replaces rather than adds',
  again.data?.replaced === true, JSON.stringify(again.data));
check('and there is still one rate for them',
  (await as('boss', 'GET', '/api/rates')).data.rates
    .filter((r) => r.person.toLowerCase() === 'harness person').length === 1);

// ── who may look ─────────────────────────────────────────────────────

const pm = await as('harness.pm', 'GET', '/api/costing');
check('a project manager reads the costing, being the oversight role',
  pm.status === 200, `${pm.status}`);
const dev = await as('harness.dev', 'GET', '/api/costing');
check('a developer does not — this is the delivery, not their board',
  dev.status === 403, `${dev.status}`);
const pmSets = await as('harness.pm', 'PUT', '/api/rates',
  { person: 'Harness Person', hourly: 1 });
check('and a pm reads rates without being able to change one',
  pmSets.status === 403 && (await as('harness.pm', 'GET', '/api/rates')).status === 200,
  `${pmSets.status}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
