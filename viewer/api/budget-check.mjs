// The budget, the default rate, dated hours and the projection on the costing
// page: what it rests on, and the ways it refuses to say more than it knows.
//
//   **A budget is never edited, only replaced.** Every change is a new row and
//   the reply carries the history with what each one replaced, because a
//   budget that moved silently makes every "over by" meaningless.
//
//   **A default rate is a stand-in and says so.** Anybody priced by it is
//   marked `atDefault`, and the part of the total it produced is reported
//   apart, so it is never read as what somebody costs.
//
//   **Two sources of hours, named.** Time entries when the token may read
//   them (dated: by sprint and by week), each ticket's total by its sprint
//   when it may not. The fallback is not an error; it is said.
//
//   **The projection is arithmetic anybody can redo.** The figures it rests on
//   come back with it, and this redoes the sum from them.
//
// Runs against the team dataset with four sprints behind it:
//
//   PORT=8798 FAKE_TEAM=1 FAKE_SPRINTS_AGO=4 node api/fake-openproject.mjs
//   TICVAI_DB=/tmp/budget.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   API=http://localhost:8799 PMS=http://127.0.0.1:8798 node api/budget-check.mjs

const API = process.env.API ?? 'http://localhost:8787';
const PMS = process.env.PMS ?? 'http://127.0.0.1:8798';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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
  const made = await as('boss', 'POST', '/api/invites', { email: `${handle}@softlabsgroup.com`, role });
  if (made.status !== 200) return false;
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  return (await as(handle, 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: handle })).status === 200;
}
const connect = (who) => as(who, 'PUT', '/api/settings/openproject', { token: 'hrushi-key', endpoint: PMS });

/** The costing once nothing is still being read behind it. */
async function settled(query = '', { refresh = false, until = () => true } = {}) {
  let first = refresh;
  for (let n = 0; n < 40; n += 1) {
    const got = await as('boss', 'GET', `/api/costing?${first ? 'refresh=1&' : ''}${query}`);
    first = false;
    if (got.status === 200 && !got.data.refreshing && until(got.data)) return got;
    await sleep(500);
  }
  return as('boss', 'GET', `/api/costing?${query}`);
}

const working = (from, to) => {
  let n = 0;
  for (let d = new Date(`${from}T00:00:00Z`); d <= new Date(`${to}T00:00:00Z`); d = new Date(+d + 86400000)) {
    if (d.getUTCDay() % 6) n += 1;
  }
  return n;
};

// ── the cast ─────────────────────────────────────────────────────────

check('an admin exists', (await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD })).status === 200);
check('connected to OpenProject', (await connect('boss')).status === 200);
check('the project is mapped',
  (await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);
check('a project manager and a developer are invited',
  (await recruit('harness.pm', 'pm')) && (await recruit('harness.dev', 'dev')));
await connect('harness.pm');
await connect('harness.dev');

// ── the budget ───────────────────────────────────────────────────────

const none = await as('boss', 'GET', '/api/budget');
check('with no budget set the answer says so, rather than a zero',
  none.status === 200 && none.data.budget === null && none.data.history.length === 0,
  JSON.stringify(none.data));
check('and offers the same currencies rates are set in',
  (none.data?.currencyChoices ?? []).includes('INR') && (none.data?.currencyChoices ?? []).includes('USD'));

check('a developer cannot set a budget',
  (await as('harness.dev', 'PUT', '/api/budget', { amount: 100, currency: 'INR' })).status === 403);
check('nor can a project manager, who reads it',
  (await as('harness.pm', 'PUT', '/api/budget', { amount: 100, currency: 'INR' })).status === 403);
const zero = await as('boss', 'PUT', '/api/budget', { amount: 0, currency: 'INR' });
check('a budget of nothing is refused, with a sentence', zero.status === 400 && /above zero/.test(zero.data?.detail),
  `${zero.status} ${zero.data?.detail}`);
const odd = await as('boss', 'PUT', '/api/budget', { amount: 100, currency: 'Rs' });
check('a currency off the list is refused', odd.status === 400, `${odd.status} ${odd.data?.detail}`);

const first = await as('boss', 'PUT', '/api/budget',
  { amount: 5_000_000_00, currency: 'INR', note: 'Signed scope, block A' });
check('an admin sets one', first.status === 200 && first.data.budget.amount === 5_000_000_00,
  JSON.stringify(first.data?.budget));
const second = await as('boss', 'PUT', '/api/budget',
  { amount: 6_000_000_00, currency: 'inr', note: 'CR-031 added the loyalty module' });
const history = second.data?.history ?? [];
check('a second is a new row, not an edit: both are kept, newest first',
  history.length === 2 && history[0].amount === 6_000_000_00 && history[1].amount === 5_000_000_00,
  JSON.stringify(history.map((h) => h.amount)));
check('each says what it replaced, so a move is never silent',
  history[0].from?.amount === 5_000_000_00 && history[0].from?.currency === 'INR' && history[1].from === null,
  JSON.stringify(history.map((h) => h.from)));
check('and who set it', history[0].setBy === 'Harness Boss', history[0].setBy);
check('the currency is kept in one spelling', history[0].currency === 'INR', history[0].currency);
check('a project manager reads it',
  (await as('harness.pm', 'GET', '/api/budget')).data?.budget?.amount === 6_000_000_00);
check('a developer does not, as with the costing',
  (await as('harness.dev', 'GET', '/api/budget')).status === 403);

// ── dated hours ──────────────────────────────────────────────────────

const dated = await settled('', { until: (d) => d.hoursSource === 'time-entries' });
const d = dated.data ?? {};
check('the costing reads time entries when the token may', d.hoursSource === 'time-entries',
  `${dated.status} ${d.hoursSource} ${d.hoursSays ?? ''}`);
check('and gives a week-by-week line from them', (d.byWeek ?? []).length >= 4,
  `${(d.byWeek ?? []).length} weeks`);

// The same hours, asked of OpenProject directly.
const auth = { authorization: `Basic ${Buffer.from('apikey:hrushi-key').toString('base64')}` };
let logged = 0;
for (let page = 1; ; page += 1) {
  const r = await (await fetch(`${PMS}/api/v3/time_entries?pageSize=200&offset=${page}&filters=${encodeURIComponent(JSON.stringify([{ project: { operator: '=', values: ['42'] } }]))}`, { headers: auth })).json();
  for (const e of r._embedded.elements) {
    const m = /^PT(\d+)H(?:(\d+)M)?$/.exec(e.hours);
    logged += Number(m[1]) + Number(m[2] ?? 0) / 60;
  }
  if (page * 200 >= r.total) break;
}
check('every logged hour is counted, no more and no fewer',
  Math.abs(d.totalHours - logged) < 0.05, `${d.totalHours} against ${logged.toFixed(2)} logged`);
const sprints = (d.bySprint ?? []).filter((s) => !s.outside);
check('by sprint, in the order they run, with which are over and which is under way',
  sprints.map((s) => s.name).slice(0, 6).join(',') === 'Sprint 1,Sprint 2,Sprint 3,Sprint 4,Sprint 5,Sprint 6'
  && sprints[0].state === 'done' && sprints[4].state === 'current' && sprints[5].state === 'ahead',
  sprints.map((s) => `${s.name}:${s.state}`).join(' '));
check('nothing is logged in a sprint still to come', sprints.filter((s) => s.state === 'ahead').every((s) => !s.hours));
check('the hours by sprint add up to the hours',
  Math.abs((d.bySprint ?? []).reduce((t, s) => t + s.hours, 0) - d.totalHours) < 0.05);

// ── the default rate ─────────────────────────────────────────────────

check('before any rate, everybody with hours is named as unpriced',
  (d.peopleWithoutRate ?? []).length >= 5 && d.totalCost === null,
  `${(d.peopleWithoutRate ?? []).length} unpriced, total ${d.totalCost}`);
check('a developer cannot set a default rate',
  (await as('harness.dev', 'PUT', '/api/rates/default', { hourly: 1, currency: 'INR' })).status === 403);
const nothing = await as('boss', 'PUT', '/api/rates/default', { hourly: 0, currency: 'INR' });
check('a default of nothing is refused, since it would price people as free', nothing.status === 400,
  `${nothing.status} ${nothing.data?.detail}`);
check('an admin sets one',
  (await as('boss', 'PUT', '/api/rates/default', { hourly: 1_500_00, currency: 'INR', note: 'blended' })).status === 200);
check('one person is given a rate of their own', (await as('boss', 'PUT', '/api/rates',
  { person: 'Hrushikant Patkar', hourly: 2_400_50, currency: 'INR' })).status === 200);
const rates = await as('boss', 'GET', '/api/rates');
check('the rates list carries the default and the currencies',
  rates.data?.default?.hourly === 1_500_00 && (rates.data?.currencyChoices ?? []).length >= 5);

const priced = (await settled()).data ?? {};
const hrushi = (priced.people ?? []).find((p) => p.person === 'Hrushikant Patkar');
const someone = (priced.people ?? []).find((p) => p.person !== 'Hrushikant Patkar' && p.hours);
check('somebody with their own rate is not at the default',
  hrushi && hrushi.atDefault === false && hrushi.hourly === 2_400_50, JSON.stringify(hrushi));
check('somebody without one is priced at the default, and marked so',
  someone && someone.atDefault === true && someone.hourly === 1_500_00, JSON.stringify(someone));
check('at the default is hours times the default, to the unit',
  someone && someone.cost === Math.round(someone.hours * 1_500_00), `${someone?.cost} for ${someone?.hours} h`);
check('nobody with hours is left unpriced now',
  (priced.peopleWithoutRate ?? []).length === 0, (priced.peopleWithoutRate ?? []).join(', '));
check('and the part of the total that is the default is said apart',
  priced.costAtDefault > 0 && priced.costAtDefault < priced.totalCost
  && priced.peopleAtDefault.includes(someone?.person) && !priced.peopleAtDefault.includes('Hrushikant Patkar'),
  `${priced.costAtDefault} of ${priced.totalCost}`);
check('the running total by sprint ends at the total, exactly',
  priced.bySprint.at(-1).cumulative === priced.totalCost, `${priced.bySprint.at(-1).cumulative} vs ${priced.totalCost}`);
check('and the sprints add up to it, within a unit each for rounding',
  Math.abs(priced.bySprint.reduce((t, s) => t + s.cost, 0) - priced.totalCost) <= priced.bySprint.length);
check('the work still open is estimated apart and never added to the spend',
  priced.estimateRemaining?.hours > 0 && priced.estimateRemaining?.cost > 0,
  JSON.stringify(priced.estimateRemaining));

// ── the projection, redone ───────────────────────────────────────────

const p = priced.projection ?? {};
const dates = priced.bySprint.filter((s) => s.startDate);
const elapsed = working(dates[0].startDate, priced.today);
const total = working(dates[0].startDate, dates.at(-1).endDate);
check('dated hours are projected per working day', p.basis === 'working-days' && p.unit === 'working day',
  `${p.basis} ${p.says}`);
check('counting the working days since the first sprint began',
  p.elapsed === elapsed && p.total === total, `${p.elapsed}/${p.total} against ${elapsed}/${total}`);
const expected = Math.round(priced.totalCost * total / elapsed);
check('the projection is the spend carried at that pace to the last sprint',
  Math.abs(p.projected - expected) <= Math.ceil(total / elapsed) + 1, `${p.projected} against ${expected}`);
check('to the last sprint, by name', p.lastSprint === 'Sprint 8', p.lastSprint);
check('and against the budget, positive for over and negative for under',
  p.overBudget === p.projected - 6_000_000_00, `${p.overBudget}`);
check('the dashed line ends where the projection does',
  p.path?.at(-1)?.name === 'Sprint 8' && Math.abs(p.path.at(-1).cost - p.projected) <= 1);

const oneSprint = (await settled('sprint=Sprint%202')).data ?? {};
check('one sprint has no pace to carry forward, and says so',
  oneSprint.projection?.projected === null && /One sprint/.test(oneSprint.projection?.says)
  && oneSprint.bySprint.length === 1 && oneSprint.bySprint[0].name === 'Sprint 2',
  oneSprint.projection?.says);
const onePerson = (await settled(`person=${encodeURIComponent('Hrushikant Patkar')}`)).data ?? {};
check('a person filter narrows every figure to them',
  onePerson.people.every((x) => x.person === 'Hrushikant Patkar') && onePerson.totalCost === hrushi.cost,
  `${onePerson.totalCost} vs ${hrushi?.cost}`);
check('while the budget stays the whole project\'s', onePerson.budget?.amount === 6_000_000_00);

// ── two currencies ───────────────────────────────────────────────────

await as('boss', 'PUT', '/api/rates', { person: 'Pradnya Yeram', hourly: 40_00, currency: 'USD' });
const mixed = (await settled()).data ?? {};
check('with two currencies in play there is no total and no projection',
  mixed.totalCost === null && mixed.projection?.projected === null
  && mixed.bySprint.every((s) => s.cost === null && s.cumulative === null),
  `${mixed.totalCost} ${mixed.projection?.says}`);
check('and both currencies are named', (mixed.currencies ?? []).join(',') === 'INR,USD');
const usd = (await as('boss', 'GET', '/api/rates')).data.rates.find((r) => r.currency === 'USD');
await as('boss', 'DELETE', `/api/rates/${usd.id}`);
await as('boss', 'PUT', '/api/budget', { amount: 70_000_00, currency: 'USD', note: 'wrong currency on purpose' });
const apart = (await settled()).data ?? {};
check('a budget in another currency is never subtracted from the spend',
  apart.totalCost !== null && apart.projection?.projected !== null && apart.projection?.overBudget === null,
  `over ${apart.projection?.overBudget}`);
await as('boss', 'PUT', '/api/budget', { amount: 6_000_000_00, currency: 'INR', note: 'back in rupees' });

// ── when time entries are refused ────────────────────────────────────

await fetch(`${PMS}/_time-entries?refuse=1`);
await sleep(1100);  // a new read needs a new `asOf`, which is to the second
const before = priced.asOf;
const fallback = (await settled('', { refresh: true,
  until: (x) => x.asOf !== before && x.hoursSource === 'tickets-by-sprint' })).data ?? {};
check('a refused read falls back to the tickets, and says which',
  fallback.hoursSource === 'tickets-by-sprint' && /may not view time entries/.test(fallback.hoursSays ?? ''),
  `${fallback.hoursSource} ${fallback.hoursSays}`);
check('with no week-by-week line, since a ticket total has no date', (fallback.byWeek ?? []).length === 0);
check('the same hours, since each ticket\'s total is its entries',
  Math.abs(fallback.totalHours - priced.totalHours) < 0.05, `${fallback.totalHours} vs ${priced.totalHours}`);
const fp = fallback.projection ?? {};
check('undated hours are projected per sprint', fp.basis === 'sprints' && fp.unit === 'sprint', fp.says);
check('the sprint under way counted as the part of it that has gone',
  fp.elapsed > 400 && fp.elapsed < 500 && fp.total === 800, `${fp.elapsed}/${fp.total} hundredths`);
check('and the projection is the spend over sprints gone, times all of them',
  Math.abs(fp.projected - Math.round(fallback.totalCost * fp.total / fp.elapsed)) <= 2,
  `${fp.projected} vs ${Math.round(fallback.totalCost * fp.total / fp.elapsed)}`);
await fetch(`${PMS}/_time-entries?refuse=0`);

// ── removing the default ─────────────────────────────────────────────

check('the default is removed', (await as('boss', 'DELETE', '/api/rates/default')).status === 200);
check('and a second removal says there is none', (await as('boss', 'DELETE', '/api/rates/default')).status === 404);
const after = (await settled()).data ?? {};
check('whereupon the people it priced are unpriced again, and named',
  (after.peopleWithoutRate ?? []).length >= 5 && (after.peopleAtDefault ?? []).length === 0);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
