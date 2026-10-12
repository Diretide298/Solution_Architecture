// A developer's own board, and the fact that it is only ever their own.
//
// Two properties:
//
//   **`assignee = me` means the caller.** Every PMS call is made with the
//   caller's own OpenProject token, so the board cannot be asked for somebody
//   else's — there is no id in the request to change. The stand-in answers
//   differently per token precisely so this can be asserted rather than assumed
//   from the absence of a parameter.
//
//   **A teammate's work is readable, and still read as the caller.** Anyone on
//   the delivery team can ask what somebody else holds (`/api/board/person`)
//   or what everybody has started (`/api/board/team`). Both run on the
//   caller's own token, so they show only what that OpenProject account sees;
//   a client is refused, and nothing on either route writes.
//
//   **The gate is on the board.** The testing rule shipped with the Claude
//   connector as its only interface, which meant somebody not using Claude Code
//   could be refused a close by a rule they had no way to satisfy. What the
//   board says about it has to match what the service will do.
//
//   node api/fake-openproject.mjs                           # port 8798
//   TICVAI_DB=/tmp/board.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/board.db API=http://localhost:8799 PMS=http://127.0.0.1:8798 \
//     node api/board-check.mjs

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

const keys = (board) => (board.data?.items ?? []).map((t) => t.key).sort();

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
// Two people with two OpenProject accounts, which is the arrangement the whole
// "your own token, never a shared one" rule exists for.
check('the admin connects as one OpenProject user',
  (await connect('boss', 'other-key')).status === 200);
check('the project is pointed at OpenProject',
  (await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 })).status === 200);

check('a developer is invited', (await recruit('harness.dev', 'dev')).ok);
check('and connects as a different one',
  (await connect('harness.dev', 'harness-key')).status === 200);
check('and a second developer, to do the checking', (await recruit('harness.dev2', 'dev')).ok);
check('who connects too', (await connect('harness.dev2', 'harness-key')).status === 200);

// ── a board is only ever your own ────────────────────────────────────

const mine = await as('harness.dev', 'GET', '/api/board/mine');
check('a developer has a board', mine.status === 200,
  `${mine.status} ${JSON.stringify(mine.data?.detail ?? '')}`);
check('with the tickets assigned to them', keys(mine).join(' ') === '7001 7002 7003 7004',
  keys(mine).join(' '));
check('and not the one assigned to somebody else',
  !keys(mine).includes('7100'), keys(mine).join(' '));
check('the closed one is not on the open list', !keys(mine).includes('7005'),
  keys(mine).join(' '));

const theirs = await as('boss', 'GET', '/api/board/mine');
check('somebody else asking the same route gets their own instead',
  keys(theirs).join(' ') === '7100', keys(theirs).join(' '));

// ── and it says what was finished ────────────────────────────────────

const done = (mine.data?.finished ?? []).map((t) => t.key);
check('what they closed recently comes back too', done.includes('7005'), done.join(' ') || 'none');
check('and is kept apart from what is open',
  !keys(mine).includes('7005'), 'open list is open only');

// ── what the board needs to draw itself ──────────────────────────────
//
// The grouping is overdue / this week / started / backlog, and it is built
// from two fields rather than from status names, because a status name is a
// thing a team renames on a Tuesday.

const byKey = Object.fromEntries((mine.data?.items ?? []).map((t) => [t.key, t]));
check('every ticket carries the dates the grouping needs',
  byKey['7001']?.dueDate && byKey['7002']?.dueDate,
  `${byKey['7001']?.dueDate} ${byKey['7002']?.dueDate}`);
check('and the percentage that says work has started',
  byKey['7003']?.percentDone === 40, String(byKey['7003']?.percentDone));
check('and the backlog one has neither', !byKey['7004']?.dueDate && !byKey['7004']?.percentDone,
  `${byKey['7004']?.dueDate} ${byKey['7004']?.percentDone}`);
check('one is genuinely overdue, so the first section is not vacuous',
  new Date(byKey['7001'].dueDate) < new Date(), byKey['7001'].dueDate);

// ── the module a ticket is from, and the subtasks under it ───────────
//
// "What is on my board" is answered as a table of tasks against the epic each
// belongs to, so the epic has to be resolved by walking the parent chain to
// the top — OpenProject's `parent` link is one hop and names the feature, not
// the module.

check('every ticket says which module it is from',
  byKey['7001']?.module?.key === '900' && byKey['7003']?.module?.key === '901',
  `7001 -> ${byKey['7001']?.module?.key}, 7003 -> ${byKey['7003']?.module?.key}`);
check('and names it, because a number is not a module',
  byKey['7001']?.module?.subject === 'M1 Checkout', byKey['7001']?.module?.subject);
check('the board says the tree was read, so a blank module is never ambiguous',
  mine.data?.modulesKnown === true, String(mine.data?.modulesKnown));

// Pulled with the board rather than fetched later, and reaching past the first
// hop: 7013 hangs off 7012 which hangs off 7003.
const under = byKey['7003']?.subtasks ?? [];
check('subtasks come back with the ticket', under.length === 3,
  under.map((t) => t.key).join(' ') || 'none');
check('including one two levels down',
  under.find((t) => t.key === '7013')?.depth === 2,
  under.map((t) => `${t.key}:${t.depth}`).join(' '));
check('a ticket with nothing under it gets an empty list, not a missing field',
  Array.isArray(byKey['7001']?.subtasks) && byKey['7001'].subtasks.length === 0,
  JSON.stringify(byKey['7001']?.subtasks));
// The distinction the whole thing rests on: the subtasks are carried, and they
// are still not rows on the board.
check('and the subtasks are not board rows themselves',
  !keys(mine).includes('7011') && !keys(mine).includes('7013'), keys(mine).join(' '));

// The timeline needs these two, and they are the reason it can be drawn at all
// without ADAM storing a schedule of its own.
const overview = await as('boss', 'GET', '/api/board/overview');
check('the overview carries milestones for the timeline to group by',
  (overview.data?.items ?? []).some((t) => t.version === 'M1 Checkout'),
  [...new Set((overview.data?.items ?? []).map((t) => t.version).filter(Boolean))].join(' '));
check('and epics for it to draw a bar per',
  (overview.data?.items ?? []).some((t) => t.parent),
  [...new Set((overview.data?.items ?? []).map((t) => t.parent).filter(Boolean))].join(' '));

// ── a teammate's work, and the whole team's ──────────────────────────
//
// "What is Hrushikant working on", asked by another developer, by a partial
// first name, in the wrong case. The fixture gives him five started tickets
// (two epics and three subtasks), one still New, one closed three days ago and
// one closed forty days ago.

const sortedKeys = (list) => (list ?? []).map((t) => t.key).sort();
const hr = await as('harness.dev', 'GET', '/api/board/person?who=hrushi');
check('a developer can ask what a teammate is working on', hr.status === 200,
  `${hr.status} ${JSON.stringify(hr.data?.detail ?? '')}`);
check('a partial first name finds them', hr.data?.person?.name === 'Hrushikant Patkar'
  && hr.data?.match === 'partial', `${hr.data?.match} ${hr.data?.person?.name}`);
check('with every open ticket they hold',
  sortedKeys(hr.data?.items).join(' ') === '7011 7012 7013 7200 900 901', sortedKeys(hr.data?.items).join(' '));
const hrItems = hr.data?.items ?? [];
check('started ones first, and the New one after them',
  hrItems.at(-1)?.key === '7200' && hrItems.slice(0, -1).every((t) => t.started) && hrItems.at(-1)?.started === false,
  hrItems.map((t) => `${t.key}:${t.status}`).join(' '));
check('and says how many are in progress', hr.data?.inProgress === 5, String(hr.data?.inProgress));
check('with what they closed in the last fourteen days, and not before',
  sortedKeys(hr.data?.finished).join(' ') === '7201', sortedKeys(hr.data?.finished).join(' ') || 'none');
check('each closed one carries its type, parent and the date, said to be updatedAt',
  hr.data?.finished?.[0]?.type === 'Task' && hr.data?.finished?.[0]?.parentSubject === 'Epic 901'
  && hr.data?.finished?.[0]?.closedAt && /updatedAt/.test(hr.data?.closedAtIs ?? '') && hr.data?.finishedTotal === 1,
  JSON.stringify(hr.data?.finished?.[0] ?? {}).slice(0, 160));
const wider = await as('harness.dev', 'GET', '/api/board/person?who=hrushi&days=60');
check('a wider window reaches further back, most recent first',
  (wider.data?.finished ?? []).map((t) => t.key).join(' ') === '7201 902' && wider.data?.windowDays === 60,
  (wider.data?.finished ?? []).map((t) => t.key).join(' '));
check('and the window is capped at sixty days',
  (await as('harness.dev', 'GET', '/api/board/person?who=hrushi&days=61')).status === 422);
check("and nobody else's tickets", hrItems.every((t) => t.assignee === 'Hrushikant Patkar'),
  [...new Set(hrItems.map((t) => t.assignee))].join(', '));

const exact = await as('boss', 'GET', '/api/board/person?who=HRUSHIKANT%20PATKAR');
check('the whole name in capitals is the same person, asked with a different token',
  exact.data?.match === 'exact' && sortedKeys(exact.data?.items).join(' ') === sortedKeys(hr.data?.items).join(' '),
  `${exact.status} ${exact.data?.match}`);
const surname = await as('harness.dev', 'GET', '/api/board/person?who=patkar');
check('a surname is enough too', surname.data?.person?.name === 'Hrushikant Patkar', String(surname.data?.person?.name));

const amb = await as('harness.dev', 'GET', '/api/board/person?who=harness');
check('a name that fits two people answers with both, and no tickets',
  amb.status === 200 && amb.data?.match === 'ambiguous' && amb.data?.person === null
  && (amb.data?.candidates ?? []).map((c) => c.name).sort().join(', ') === 'Harness Person, Harness Tester'
  && !amb.data?.items,
  `${amb.data?.match} ${(amb.data?.candidates ?? []).map((c) => c.name).join(', ')}`);
const narrowed = await as('harness.dev', 'GET', '/api/board/person?who=harness%20p');
check('and a second word narrows it', narrowed.data?.person?.name === 'Harness Person'
  && sortedKeys(narrowed.data?.items).join(' ') === '7001 7002 7003 7004', sortedKeys(narrowed.data?.items).join(' '));
const nobody = await as('harness.dev', 'GET', '/api/board/person?who=zebedee');
check('a name that fits nobody says so', nobody.status === 200 && nobody.data?.match === 'unknown'
  && nobody.data?.person === null && /matches 'zebedee'/.test(nobody.data?.note ?? ''), JSON.stringify(nobody.data).slice(0, 160));

const team = await as('harness.dev', 'GET', '/api/board/team');
check('a developer can see the whole team', team.status === 200,
  `${team.status} ${JSON.stringify(team.data?.detail ?? '')}`);
const who = Object.fromEntries((team.data?.people ?? []).map((p) => [p.name, p]));
const counts = (p) => (p ? `${p.open}/${p.inProgress}/${p.closedRecently}` : 'missing');
check('each person with open, in progress and closed in fourteen days',
  counts(who['Harness Person']) === '4/4/1' && counts(who['Hrushikant Patkar']) === '6/5/1'
  && counts(who['Somebody Else']) === '1/1/0',
  ['Harness Person', 'Hrushikant Patkar', 'Somebody Else'].map((n) => `${n} ${counts(who[n])}`).join('; '));
check('and a member holding nothing is listed with zeros', counts(who['Harness Tester']) === '0/0/0',
  counts(who['Harness Tester']));
check("each person's current tickets are the started ones",
  sortedKeys(who['Harness Person']?.current).join(' ') === '7001 7002 7003 7004', sortedKeys(who['Harness Person']?.current).join(' '));
check('and a New ticket is not current work',
  !(team.data?.people ?? []).some((p) => (p.current ?? []).some((t) => t.key === '7200')), 'no 7200');
check('in progress means open and past New, said out loud',
  (team.data?.startedStatuses ?? []).join(',') === 'In progress', (team.data?.startedStatuses ?? []).join(','));
check('unassigned started work is counted apart', team.data?.unassigned?.inProgress >= 1,
  JSON.stringify(team.data?.unassigned));
const again = await as('harness.dev', 'GET', '/api/board/team');
check('a second read inside two minutes is the held one', again.data?.fromCache === true
  || again.data?.asOf === team.data?.asOf, `${again.data?.fromCache} ${again.data?.ageSeconds}`);
const fresh = await as('harness.dev', 'GET', '/api/board/team?refresh=1');
check('and refresh reads again', fresh.status === 200 && fresh.data?.ageSeconds === 0, String(fresh.data?.ageSeconds));

// The connector's tool, run against the same service: the answer a developer's
// Claude gets for "what is Hrushikant working on" and "what's everyone doing".
const { ViewerClient } = await import('../mcp/client.mjs');
const { BY_NAME } = await import('../mcp/tools.mjs');
const devClient = new ViewerClient({ base: API, project: 'ticvai',
  email: 'harness.dev@softlabsgroup.com', password: PASSWORD });
const askHr = await BY_NAME.get('adam_team').run(devClient, { person: 'Hrushi' });
check('adam_team with a person answers with a table of their tickets',
  askHr.found && askHr.person === 'Hrushikant Patkar' && askHr.rows?.length === 6
  && String(askHr.columns) === 'ticket,task,partOf,status,due,order' && askHr.rows.at(-1)?.ticket === '7200',
  JSON.stringify(askHr).slice(0, 200));
check('and what they closed lately, as a list with type, date and parent',
  (askHr.closed ?? []).map((t) => t.ticket).join(' ') === '7201' && askHr.closedTotal === 1
  && String(askHr.closedColumns) === 'ticket,task,type,closed,partOf' && askHr.closed[0].partOf === '901 — Epic 901'
  && /updatedAt/.test(askHr.closedNote ?? ''),
  JSON.stringify(askHr.closed));
const askHr60 = await BY_NAME.get('adam_team').run(devClient, { person: 'Hrushi', days: 60, limit: 1 });
check('with `days` it reaches further, and says how many it left out',
  askHr60.closedTotal === 2 && askHr60.closed?.length === 1 && /1 more closed/.test(askHr60.moreClosed ?? ''),
  JSON.stringify({ t: askHr60.closedTotal, c: askHr60.closed, m: askHr60.moreClosed }));
const askAmb = await BY_NAME.get('adam_team').run(devClient, { person: 'harness' });
check('adam_team with an ambiguous name lists the names to choose from',
  askAmb.found === false && askAmb.ambiguous && askAmb.candidates?.length === 2, JSON.stringify(askAmb).slice(0, 200));
const askAll = await BY_NAME.get('adam_team').run(devClient, {});
check('adam_team without a person answers with one row per busy person, busiest first',
  askAll.found && askAll.rows?.[0]?.person === 'Hrushikant Patkar' && askAll.rows.length === 3
  && (askAll.nothingAssigned ?? []).join() === 'Harness Tester',
  JSON.stringify(askAll.rows ?? askAll).slice(0, 240));
if (process.env.SHOW_TEAM) console.log(JSON.stringify({ askHr, askAmb, askAll }, null, 2));

// A client account sees the package, not the team's workload.
check('a client is invited', (await recruit('harness.client', 'client')).ok);
const clientTeam = await as('harness.client', 'GET', '/api/board/team');
const clientPerson = await as('harness.client', 'GET', '/api/board/person?who=hrushi');
check('and is refused both team routes', clientTeam.status === 403 && clientPerson.status === 403,
  `${clientTeam.status} ${clientPerson.status}`);

// ── the gate, on the board ───────────────────────────────────────────

check('a board with nothing closed says nothing about testing',
  mine.data?.testing === null, JSON.stringify(mine.data?.testing));

// Close ten, which is what it takes.
for (let n = 0; n < 10; n += 1) {
  const key = 8000 + n;
  const made = await as('harness.dev', 'POST', `/api/work-packages/${key}/proposals`,
    { status: 'Closed', comment: 'Done.' });
  if (made.status !== 200) { check(`close ${n} proposes`, false, `${made.status}`); break; }
  const sent = await as('harness.dev', 'POST',
    `/api/work-packages/${key}/proposals/${made.data.proposal}/apply`, {});
  if (sent.status !== 200) { check(`close ${n} applies`, false, `${sent.status}`); break; }
}
const blocked = await as('harness.dev', 'GET', '/api/board/mine');
check('once the batch is full the board says so before anything is refused',
  blocked.data?.testing?.full === true, JSON.stringify(blocked.data?.testing));
check('and names the number, so it matches the refusal that is coming',
  blocked.data?.testing?.closed === 10, String(blocked.data?.testing?.closed));

// What the board offers has to be what the service will accept.
const batches = await as('harness.dev', 'GET', '/api/test-batches');
check('the batch is readable from the page as well as the connector',
  batches.data?.mine?.id === blocked.data?.testing?.id,
  `${batches.data?.mine?.id} vs ${blocked.data?.testing?.id}`);
check('and nobody else is offered it to check while it is unsubmitted',
  !(await as('harness.dev2', 'GET', '/api/test-batches')).data?.waiting?.length,
  'nothing waiting yet');

const submitted = await as('harness.dev', 'POST',
  `/api/test-batches/${batches.data.mine.id}/submit`,
  { notes: 'Ran the POS pack against staging: 96 passed, nothing failed.' });
check('submitting from the page works', submitted.status === 200, `${submitted.status}`);

const waiting = await as('harness.dev2', 'GET', '/api/test-batches');
check('and it appears for a teammate to check',
  (waiting.data?.waiting ?? []).length === 1,
  String((waiting.data?.waiting ?? []).length));
check('carrying what they said they ran, which is the thing being checked',
  /96 passed/.test(waiting.data.waiting[0].notes ?? ''), waiting.data.waiting[0].notes ?? '');
check('the maker is not offered their own',
  !((await as('harness.dev', 'GET', '/api/test-batches')).data?.waiting ?? []).length,
  'not offered');

const passed = await as('harness.dev2', 'POST',
  `/api/test-batches/${batches.data.mine.id}/check`, { verdict: 'passed', note: 'Fine.' });
check('a teammate passes it', passed.status === 200, `${passed.status}`);

const freed = await as('harness.dev', 'GET', '/api/board/mine');
check('and the board stops warning', freed.data?.testing === null,
  JSON.stringify(freed.data?.testing));

// ── not connected is a setup step, not a failure ─────────────────────

const stranger = await recruit('harness.new', 'dev');
check('somebody new is invited', stranger.ok, stranger.why ?? '');
const noToken = await as('harness.new', 'GET', '/api/board/mine');
check('a board without an OpenProject token answers 428, not 500',
  noToken.status === 428, `${noToken.status}`);
check('and says which half is missing',
  /token|OpenProject/i.test(String(noToken.data?.detail)), String(noToken.data?.detail));
check('the team routes say the same, not 500',
  (await as('harness.new', 'GET', '/api/board/team')).status === 428
  && (await as('harness.new', 'GET', '/api/board/person?who=hrushi')).status === 428);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
