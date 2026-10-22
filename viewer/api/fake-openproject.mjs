// Enough OpenProject 10.0.2 to exercise the bridge's one create.
//
// Not a mock in the usual sense — nothing here is stubbed out inside the
// service. ADAM talks real HTTP, sends a real Basic header, and parses a real
// HAL document; this just answers as the instance would. That is the only way
// to test a create at all: the live instance holds the actual delivery plan,
// and a harness that files tickets into it is a harness nobody will run twice.
//
// It keeps what was created so the check can assert on the body ADAM sent —
// the parent link and the type link are the two things worth being sure about,
// and both are invisible from ADAM's side of the call.
import { createServer } from 'node:http';

const PORT = Number(process.env.PORT ?? 8798);
const PROJECT = { id: 42, identifier: 'ticvai-test', name: 'TICVAI (harness)' };

// Three, and only `isClosed` matters here: the testing gate counts a close
// because OpenProject said the status closes, never because of its name.
const STATUSES = [
  { id: 1, name: 'New', isClosed: false, isDefault: true },
  { id: 7, name: 'In progress', isClosed: false, isDefault: false },
  { id: 12, name: 'Closed', isClosed: true, isDefault: false },
  // Open, and not in progress: the team view counts these apart. On the live
  // instance finished work goes to Ready for QA and stays open.
  { id: 4, name: 'On hold', isClosed: false, isDefault: false },
  { id: 9, name: 'Ready for QA', isClosed: false, isDefault: false },
];

// FAKE_TEAM=1 fills the project with a whole team's sprint plan, for looking
// at the delivery overview (tasks.html) with something on it. Opt-in, because
// every other check counts this project's tickets and was written against the
// handful below; with the switch off nothing here changes.
const TEAM = process.env.FAKE_TEAM === '1';
if (TEAM) {
  STATUSES.push(
    { id: 13, name: 'On hold', isClosed: false, isDefault: false },
    { id: 14, name: 'Rejected', isClosed: true, isDefault: false },
    { id: 15, name: 'Ready for QA', isClosed: false, isDefault: false },
  );
}

const TYPES = [
  { id: 1, name: 'Task', isDefault: true, isMilestone: false },
  { id: 7, name: 'Bug', isDefault: false, isMilestone: false },
];

// The parent the change request will say it came out of.
const packages = new Map();
packages.set('880', {
  id: 880, subject: 'Checkout, phase two', lockVersion: 3, percentageDone: 40,
  createdAt: '2026-08-01T09:00:00Z', updatedAt: '2026-09-01T09:00:00Z',
  _links: {
    project: { href: `/api/v3/projects/${PROJECT.id}`, title: PROJECT.name },
    type: { href: '/api/v3/types/1', title: 'Task' },
    status: { href: '/api/v3/statuses/7', title: 'In progress' },
  },
});
// One in a different project, for the check that a child cannot be filed into
// somebody else's plan.
packages.set('991', {
  id: 991, subject: 'Something in another product', lockVersion: 1,
  _links: {
    project: { href: '/api/v3/projects/99', title: 'Not ours' },
    type: { href: '/api/v3/types/1', title: 'Task' },
    status: { href: '/api/v3/statuses/7', title: 'In progress' },
  },
});

/** Any number is a work package in the harness project.
 *
 *  The gate test closes a few dozen tickets and cares about none of them
 *  individually; writing them out would be a fixture nobody reads. 991 stays
 *  explicit above because being in *another* project is the whole point of it.
 */
function ensure(id) {
  if (packages.has(id)) return packages.get(id);
  const made = {
    id: Number(id), subject: `Harness ticket ${id}`, lockVersion: 1, percentageDone: 0,
    createdAt: '2026-09-01T09:00:00Z', updatedAt: '2026-09-01T09:00:00Z',
    _links: {
      project: { href: `/api/v3/projects/${PROJECT.id}`, title: PROJECT.name },
      type: { href: '/api/v3/types/1', title: 'Task' },
      status: { href: '/api/v3/statuses/1', title: 'New' },
    },
  };
  packages.set(id, made);
  return made;
}

/** Assign a ticket to the harness user and give it the shape a board and a
 *  timeline need: dates, an epic, a milestone, a percentage. */
const USERS = { 'harness-key': 5, 'other-key': 6 };
// The team dataset's people. Three of them can sign in, so a seed script can
// close tickets through ADAM and put something on the testing gate.
const TEAM_PEOPLE = [
  [20, 'Hrushikant Patkar', 'hrushi-key'], [21, 'Pradnya Yeram', 'pradnya-key'],
  [22, 'Chitrangi Mestry'], [23, 'Sanket Keluskar'], [24, 'Chinmay Patkar'],
  [25, 'Pallavi Sawant'], [26, 'Surendra Loke', 'surendra-key'], [27, 'Tanmay Dukhande'],
  [28, 'Deep Khanvilkar'], [29, 'Kalpita Mejari'],
];
if (TEAM) for (const [id, , key] of TEAM_PEOPLE) if (key) USERS[key] = id;
const userName = (id) => (NAMES[id] ?? (id === 5 ? 'Harness Person' : id === 6 ? 'Somebody Else'
  : TEAM_PEOPLE.find(([n]) => n === id)?.[1] ?? 'Somebody Else'));

// Who is who, by OpenProject user id: the names the team view matches a typed
// name against. 9 holds the epics and the subtasks; 12 holds nothing, so
// "harness" is ambiguous and the whole-team view has somebody idle in it.
const NAMES = { 5: 'Harness Person', 6: 'Somebody Else', 9: 'Hrushikant Patkar', 12: 'Harness Tester' };

/** Which user a token belongs to. The whole point of `assignee = me` is that
 *  the answer depends on who is asking, so a stand-in that ignored the
 *  credential would make "a board is only ever your own" untestable. */
function userOf(req) {
  const header = (req.headers.authorization ?? '').replace(/^Basic /, '');
  const token = Buffer.from(header, 'base64').toString().split(':')[1] ?? '';
  return USERS[token] ?? 0;
}

function own(id, { subject, status = 7, done = 0, start, due, parent, version, user = 5, updated, spent, estimate, order }) {
  const wp = ensure(String(id));
  wp.subject = subject;
  wp.percentageDone = done;
  // ISO 8601 durations, as OpenProject reports them. `spentTime` is absent
  // rather than zero when the token may not read time entries, and the costing
  // page counts those apart — so the fixture has one of each.
  if (spent !== undefined) wp.spentTime = spent;
  if (estimate !== undefined) wp.estimatedTime = estimate;
  wp.startDate = start ?? null;
  wp.dueDate = due ?? null;
  wp._links.status = { href: `/api/v3/statuses/${status}`, title: STATUSES.find((s) => s.id === status).name };
  wp._links.assignee = { href: `/api/v3/users/${user}`, title: userName(user) };
  // The line the delivery plan writes at the top of a task, which is where the
  // build order is read from on a project without the number field.
  if (order !== undefined) wp.description = { raw: `Build order: #${order}` };
  if (parent) wp._links.parent = { href: `/api/v3/work_packages/${parent}`, title: `Epic ${parent}` };
  if (version) wp._links.version = { href: '/api/v3/versions/1', title: version };
  // When it last changed, which for a closed ticket is when it was closed —
  // and that is what the board's "finished this week" window is measured on.
  // Defaulting it to the due date made a ticket due a fortnight ago look like
  // it was closed a fortnight ago, which is a different fact.
  wp.updatedAt = `${updated ?? due ?? '2026-09-01'}T09:00:00Z`;
  return wp;
}

// A board: one overdue, one due this week, one started, one in the backlog,
// one closed. The dates are relative so the assertions do not rot.
const day = (n) => new Date(Date.now() + n * 86400000).toISOString().slice(0, 10);
own(7001, { subject: 'Receipt totals are wrong', start: day(-20), due: day(-3), parent: 900, version: 'M1 Checkout', spent: 'PT12H', estimate: 'PT8H' });
own(7002, { subject: 'Tax rounding on the POS', start: day(-5), due: day(3), parent: 900, version: 'M1 Checkout', spent: 'PT4H30M', estimate: 'PT6H' });
own(7003, { subject: 'Refund flow', done: 40, start: day(-10), due: day(40), parent: 901, version: 'M2 Refunds', spent: 'P1DT1H', estimate: 'PT20H' });
// No time logged, and time that cannot be read, are different facts. 7004
// has a zero; 7100 has no spentTime field at all.
own(7004, { subject: 'Nothing has started here', parent: 901, version: 'M2 Refunds', spent: 'PT0S' });
own(7005, { subject: 'Already shipped', status: 12, done: 100, start: day(-30), due: day(-10), updated: day(-2), parent: 900, version: 'M1 Checkout' });
// A milestone with nothing left in it, so "hide what is finished" has
// something to hide. Without one the switch redraws the same chart and the
// assertion about it passes while proving nothing.
own(7006, { subject: 'Shipped and closed', status: 12, done: 100, start: day(-60), due: day(-40), updated: day(-40), parent: 902, version: 'M0 Groundwork' });

// The three epics the tickets above hang off. They exist as work packages in
// their own right, with no parent, which is what makes them modules on the
// plan — and until now they were only ever hrefs, so the plan had nothing to
// draw. 900 and 901 are scheduled automatically, the way OpenProject leaves a
// parent by default; 902 has been taken off it by hand, so the chart has one
// of each and "this bar will switch to manual scheduling" is testable.
// Assigned to a user nobody in the harness connects as, deliberately. An epic
// that belongs to a developer turns up on their board, and a board is a list of
// work to do rather than of the containers that work sits in -- which is
// exactly the distinction the module column exists to draw.
own(900, { subject: 'M1 Checkout', done: 30, start: day(-20), due: day(3), user: 9 });
own(901, { subject: 'M2 Refunds', done: 20, start: day(-10), due: day(40), user: 9 });
own(902, { subject: 'M0 Groundwork', status: 12, done: 100, start: day(-60), due: day(-40), user: 9 });
packages.get('902').scheduleManually = true;

// Subtasks under a board ticket, and one under a subtask. Assigned away from
// both harness users on purpose: if they were the developer's they would be
// board rows in their own right, and then "the board pulls subtasks without
// listing them" would be indistinguishable from "the board lists everything".
// 7013 is two levels down, so the walk has to be a walk and not one hop.
own(7011, { subject: 'Refund: partial amounts', parent: 7003, user: 9, due: day(12) });
own(7012, { subject: 'Refund: audit trail', parent: 7003, user: 9 });
own(7013, { subject: 'Refund audit: retention window', parent: 7012, user: 9 });

// Somebody else's, to prove a board is only ever your own.
own(7100, { subject: 'Not yours', start: day(-2), due: day(9), user: 6, spent: 'PT6H' });

// The team view's: one of Hrushikant's not started yet (New), so "in progress
// first" has something to put last, one he closed this week, one he moved to
// Ready for QA yesterday and one on hold.
own(7200, { subject: 'Refund reconciliation report', status: 1, parent: 901, user: 9, order: 3 });
own(7201, { subject: 'Refund API contract tests', status: 12, done: 100, parent: 901, user: 9, updated: day(-3) });
// Finished the way the live instance finishes things, moved to Ready for QA
// yesterday and still open; and one on hold, which is stalled, not in progress.
own(7202, { subject: 'Refund receipt template', status: 9, done: 100, parent: 901, user: 9, updated: day(-1) });
own(7203, { subject: 'Refund to gift card', status: 4, parent: 901, user: 9 });

// ── the sub-task dataset (FAKE_SUBTASKS=1) ───────────────────────────
//
// For api/subtasks-check.mjs (CHG-ADM-006): one person (sub-key, user 14) whose first ticket has sub-tasks two
// levels deep - one closed, one somebody else's - and a sub-task of theirs whose parent is somebody else's.
// Opt-in, like FAKE_TEAM: every other check counts this project's tickets and was written without these.
if (process.env.FAKE_SUBTASKS === '1') {
  USERS['sub-key'] = 14;
  NAMES[14] = 'Sub Tasker';
  own(7400, { subject: 'OrderService: claimCart, createCart, extendCart, getCart', status: 1, user: 14, order: 1 });
  own(7401, { subject: 'claimCart', status: 12, done: 100, parent: 7400, user: 14, updated: day(-1) });
  own(7402, { subject: 'createCart', status: 1, parent: 7400, user: 9 });
  own(7403, { subject: 'extendCart', status: 1, parent: 7400, user: 14 });
  own(7404, { subject: 'getCart', status: 1, parent: 7400, user: 14 });
  own(7405, { subject: 'getCart: expiry rule', status: 1, parent: 7404, user: 14 });
  own(7410, { subject: 'A ticket with nothing under it', status: 1, user: 14, order: 2 });
  own(7420, { subject: 'Parent held by someone else', status: 1, user: 9, order: 3 });
  own(7421, { subject: 'Your part of it', status: 1, parent: 7420, user: 14 });
  // OpenProject titles a parent link with the parent's subject; own() writes "Epic n".
  for (const id of ['7401', '7402', '7403', '7404', '7405', '7421']) {
    const link = packages.get(id)._links.parent;
    link.title = packages.get(link.href.split('/').pop()).subject;
  }
}

// ── the team dataset (FAKE_TEAM=1) ───────────────────────────────────
//
// Five blocks as epics, features under them, tasks under those and sub-tasks
// under some tasks — the shape TICVAI's plan has in OpenProject — spread over
// two-week sprints. Sprint 1 starts on the Monday a week before today, so the
// current sprint is always Sprint 1 and its dates never rot. The mix is the live
// project's a week into Sprint 1: nearly everything New, finished work moved to
// "Ready for QA" rather than closed, a couple On hold, nothing Closed (the seed
// script closes a few through ADAM for the testing gate). Seeded, so two runs
// draw the same picture.
// Time logged against each work package, by its number: [{spentOn, hours}].
// What `/api/v3/time_entries` answers with. The team dataset fills it below;
// a hand-written ticket with a `spentTime` and nothing here is answered with
// that time split into working days from its start (see `loggedOn`).
const LOGGED = new Map();
// "PT4H30M", "P1DT1H" -> hours, with a day as eight, the way the service reads them.
const durationHours = (text) => {
  const m = /^P(?:(\d+(?:\.\d+)?)D)?(?:T(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?)?$/.exec(text ?? '');
  if (!m) return null;
  const [, d = 0, h = 0, mi = 0, s = 0] = m;
  return Number(d) * 8 + Number(h) + Number(mi) / 60 + Number(s) / 3600;
};
const isoHours = (hours) => {
  const whole = Math.floor(hours);
  const minutes = Math.round((hours - whole) * 60);
  return `PT${whole}H${minutes ? `${minutes}M` : ''}`;
};

const VERSIONS = [];
// FAKE_SPRINTS_AGO=4 moves the whole plan four sprints into the past, so the
// sprint under way is Sprint 5 and Sprints 1-4 are over and mostly finished.
// For the costing page, whose cost-by-sprint line needs sprints behind it to
// be a line at all. Off by default: with it unset every sprint, status and
// date is exactly what it was, because every other check reads this dataset.
const AGO = Math.max(0, Number(process.env.FAKE_SPRINTS_AGO ?? 0));
if (TEAM) {
  let seed = 7;
  const rand = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
  const pick = (list) => list[Math.floor(rand() * list.length)];
  const iso = (d) => d.toISOString().slice(0, 10);
  const addDays = (d, n) => new Date(+d + n * 86400000);
  const now = new Date(); now.setUTCHours(0, 0, 0, 0);
  const s1 = addDays(now, -7 - 14 * AGO);
  s1.setUTCDate(s1.getUTCDate() - ((s1.getUTCDay() + 6) % 7));     // back to Monday
  for (let n = 1; n <= 8; n += 1) {
    VERSIONS.push({ id: 76 + n, name: `Sprint ${n}`, startDate: iso(addDays(s1, (n - 1) * 14)),
                    endDate: iso(addDays(s1, (n - 1) * 14 + 11)), status: 'open' });
  }
  const versionOf = (name) => VERSIONS.find((v) => v.name === name);
  const BLOCKS = [
    [5000, 'Block A1: the first release, first drop (Sprints 1-4)', ['Sprint 1', 'Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4']],
    [5001, 'Block A2: the rest of Block A (Sprint 5)', ['Sprint 5']],
    [5002, 'Block B (Sprints 3-6)', ['Sprint 3', 'Sprint 4', 'Sprint 5', 'Sprint 6']],
    [5003, 'Block C (Sprints 5-8)', ['Sprint 5', 'Sprint 6', 'Sprint 7', 'Sprint 8']],
    [5004, 'Block D (Sprints 6-8)', ['Sprint 6', 'Sprint 7', 'Sprint 8']],
  ];
  const FEATURES = ['Orders', 'Payments', 'Menu', 'Kitchen display', 'Loyalty', 'Reports', 'Inventory',
    'Staff', 'Tables', 'Receipts', 'Delivery', 'Promotions', 'Auth', 'Notifications', 'Search',
    'Audit', 'Settings', 'Exports'];
  const VERBS = ['Build', 'Wire', 'Test', 'Model', 'Validate', 'Migrate', 'Style', 'Document'];
  const NOUNS = ['list screen', 'detail screen', 'create form', 'API contract', 'state machine',
    'table schema', 'error states', 'empty state', 'permissions', 'events'];
  // How much each person gets and how quickly they finish it, so the roster
  // has a spread worth reading: one heavy finisher, one with work on hold, one
  // who is behind, one nearly idle.
  const WEIGHT = { 20: 9, 21: 6, 22: 6, 23: 5, 24: 5, 25: 5, 26: 4, 27: 4, 28: 3, 29: 1 };
  const PACE = { 20: 0.82, 21: 0.6, 22: 0.55, 23: 0.5, 24: 0.45, 25: 0.5, 26: 0.3, 27: 0.35, 28: 0.55, 29: 0.4 };
  const pool = Object.entries(WEIGHT).flatMap(([id, w]) => Array(w).fill(Number(id)));
  const typed = (wp, name, id) => { wp._links.type = { href: `/api/v3/types/${id}`, title: name }; };

  let key = 6000;
  const place = (subject, typeName, typeId, parent, parentTitle, version, user, sub) => {
    const v = versionOf(version);
    const start = new Date(`${v.startDate}T00:00:00Z`);
    const end = new Date(`${v.endDate}T00:00:00Z`);
    const due = addDays(start, 2 + Math.floor(rand() * 10));
    const pace = PACE[user] ?? 0.5;
    let status = 1;
    let updated = addDays(start, -3);
    const r = rand();
    // The sprint under way is Sprint 1 + AGO. Before it, the work is done; the
    // branches below are the original ones, renumbered, and with AGO at 0 they
    // are the original ones exactly. No extra draws from `rand`, so the rest of
    // the dataset is the same tickets either way.
    const nth = Number(version.split(' ')[1]) - AGO;
    if (nth < 1) {
      status = r < 0.8 ? 12 : r < 0.95 ? 15 : 1;
    } else if (nth === 1) {
      status = r < pace * 0.42 ? 15 : r > 0.985 ? 13 : 1;
      if (user === 26 && r > 0.9) status = 13;        // the one with work on hold
    } else if (nth === 2) {
      status = r < pace * 0.04 ? 15 : 1;
    }
    if (status === 15 || (status === 12 && nth < 1)) {
      // Moved to QA (or, in a sprint that is over, closed) some time since the
      // sprint began, and no later than its end.
      const lo = +start;
      updated = new Date(lo + rand() * Math.max(0, Math.min(+now, +end) - lo));
    } else if (status !== 1) {
      updated = addDays(now, -Math.floor(rand() * 6));
    }
    const id = key++;
    const wp = ensure(String(id));
    wp.subject = subject;
    typed(wp, typeName, typeId);
    wp._links.status = { href: `/api/v3/statuses/${status}`, title: STATUSES.find((st) => st.id === status).name };
    if (user) wp._links.assignee = { href: `/api/v3/users/${user}`, title: userName(user) };
    wp._links.parent = { href: `/api/v3/work_packages/${parent}`, title: parentTitle };
    wp._links.version = { href: `/api/v3/versions/${v.id}`, title: v.name };
    wp.startDate = iso(start);
    wp.dueDate = iso(due);
    wp.percentageDone = status === 12 || status === 15 ? 100 : 0;
    wp.createdAt = `${iso(addDays(start, -10))}T09:00:00Z`;
    wp.updatedAt = `${iso(updated)}T${String(8 + Math.floor(rand() * 9)).padStart(2, '0')}:15:00Z`;
    if (!sub) { wp.storyPoints = pick([1, 2, 3, 5, 8]); wp.estimatedTime = `PT${pick([4, 6, 8, 12, 16])}H`; }
    return wp;
  };

  for (const [id, subject, sprints] of BLOCKS) {
    const epic = ensure(String(id));
    epic.subject = subject;
    typed(epic, 'Epic', 5);
    epic._links.assignee = { href: '/api/v3/users/24', title: userName(24) };
    epic.startDate = versionOf(sprints[0]).startDate;
    epic.dueDate = versionOf(sprints.at(-1)).endDate;
    epic.updatedAt = `${iso(addDays(now, -20))}T09:00:00Z`;
  }
  let f = 0;
  const sprintsOf = new Map();   // feature id -> its block's sprints, for FAKE_BULK below
  for (const [blockId, blockSubject, sprints] of BLOCKS) {
    const features = blockId === 5000 ? 6 : 3;
    for (let n = 0; n < features; n += 1) {
      const featureId = 5100 + f;
      const name = FEATURES[f % FEATURES.length];
      f += 1;
      const feature = ensure(String(featureId));
      sprintsOf.set(featureId, sprints);
      feature.subject = name;
      typed(feature, 'Feature', 4);
      feature._links.parent = { href: `/api/v3/work_packages/${blockId}`, title: blockSubject };
      feature._links.assignee = { href: '/api/v3/users/24', title: userName(24) };
      feature.updatedAt = `${iso(addDays(now, -15))}T09:00:00Z`;
      const tasks = blockId === 5000 ? 22 : 9;
      for (let t = 0; t < tasks; t += 1) {
        const version = sprints[Math.min(sprints.length - 1, Math.floor(rand() * sprints.length))];
        const user = rand() < 0.03 ? 0 : pick(pool);
        const task = place(`${pick(VERBS)} ${name.toLowerCase()} ${pick(NOUNS)}`, 'Task', 1,
          featureId, name, version, user, false);
        if (rand() < 0.45) {
          const parts = 1 + Math.floor(rand() * 2);
          for (let k = 0; k < parts; k += 1) {
            place(`${task.subject}: part ${k + 1}`, 'Sub Task', 6, task.id, task.subject,
              version, user || pick(pool), true);
          }
        }
      }
    }
  }

  // FAKE_BULK=8000 pads the same project out to that many work packages, so a
  // read of it is the size of TICVAI's release project (8,015 on 13 October)
  // rather than a few hundred. Tasks under the features above, in the same
  // sprints, by the same people, a third of them with a sub-task. Numbered from
  // 20000 so they can never land on one of the hand-written tickets above,
  // which `ensure` would otherwise hand back and `place` overwrite. Off unless
  // asked for, like FAKE_TEAM, because every other check counts this project.
  const BULK = Number(process.env.FAKE_BULK ?? 0);
  if (BULK > packages.size) {
    key = 20000;
    while (packages.size < BULK) {
      const featureId = 5100 + Math.floor(rand() * f);
      const sprints = sprintsOf.get(featureId);
      const version = sprints[Math.floor(rand() * sprints.length)];
      const user = rand() < 0.03 ? 0 : pick(pool);
      const name = FEATURES[(featureId - 5100) % FEATURES.length];
      const task = place(`${pick(VERBS)} ${name.toLowerCase()} ${pick(NOUNS)}`, 'Task', 1,
        featureId, name, version, user, false);
      if (rand() < 0.33 && packages.size < BULK) {
        place(`${task.subject}: part 1`, 'Sub Task', 6, task.id, task.subject, version,
          user || pick(pool), true);
      }
    }
  }

  // Time logged, for the costing page: by the ticket's holder, on working days
  // inside its sprint and never after today. Finished work has about its
  // estimate logged (seventy to a hundred and forty per cent of it); about half
  // of what is open in a sprint that has begun has some; nothing in a sprint
  // still to come has any. Its own seeded sequence, so adding it moved no
  // ticket, status or date above. Every team ticket with nothing logged says
  // PT0S, which is "nobody logged any" and not "this token may not see it".
  let tseed = 11;
  const trand = () => { tseed = (tseed * 16807) % 2147483647; return (tseed - 1) / 2147483646; };
  const weekdays = (from, to) => {
    const out = [];
    for (let d = new Date(from); d <= to; d = addDays(d, 1)) if (d.getUTCDay() % 6) out.push(new Date(d));
    return out;
  };
  for (const wp of packages.values()) {
    if (wp.id < 5000) continue;
    const kind = wp._links?.type?.title;
    const v = VERSIONS.find((x) => x.name === wp._links?.version?.title);
    const start = v ? new Date(`${v.startDate}T00:00:00Z`) : null;
    if ((kind !== 'Task' && kind !== 'Sub Task') || !v || !wp._links?.assignee || start > now) {
      wp.spentTime = 'PT0S';
      continue;
    }
    const end = new Date(Math.min(+new Date(`${v.endDate}T00:00:00Z`), +now));
    const status = Number((wp._links.status.href.match(/(\d+)$/) ?? [])[1]);
    const estimate = durationHours(wp.estimatedTime) ?? (kind === 'Sub Task' ? 4 : 8);
    let total = 0;
    if (status === 12 || status === 15) total = estimate * (0.7 + trand() * 0.7);
    else if (trand() < 0.5) total = estimate * (0.15 + trand() * 0.5);
    total = Math.round(total * 2) / 2;
    const days = weekdays(start, end);
    if (!total || !days.length) { wp.spentTime = 'PT0S'; continue; }
    const list = [];
    for (let left = total; left > 0;) {
      const chunk = Math.min(left, 1 + Math.floor(trand() * 4) + (trand() < 0.5 ? 0.5 : 0));
      list.push({ spentOn: iso(days[Math.floor(trand() * days.length)]), hours: chunk });
      left -= chunk;
    }
    list.sort((a, b) => a.spentOn.localeCompare(b.spentOn));
    LOGGED.set(String(wp.id), list);
    wp.spentTime = isoHours(total);
  }
}

/** A hand-written ticket's logged time as entries: its `spentTime` in days of
 *  at most eight hours, one working day after another from its start. */
function loggedOn(wp) {
  if (LOGGED.has(String(wp.id))) return LOGGED.get(String(wp.id));
  let left = durationHours(wp.spentTime) ?? 0;
  const out = [];
  let d = new Date(`${wp.startDate ?? '2026-09-01'}T00:00:00Z`);
  while (left > 0) {
    while (!(d.getUTCDay() % 6)) d = new Date(+d + 86400000);
    const chunk = Math.min(8, left);
    out.push({ spentOn: d.toISOString().slice(0, 10), hours: chunk });
    left -= chunk;
    d = new Date(+d + 86400000);
  }
  return out;
}

// FAKE_NO_TIME_ENTRIES=1 answers the time-entry list with OpenProject's 403,
// as an instance does to a role without "View time entries"; the costing page
// then falls back to each ticket's spentTime by sprint. `/_time-entries?refuse=`
// turns it on and off while running, for a check that tests both paths.
let REFUSE_TIME = process.env.FAKE_NO_TIME_ENTRIES === '1';

// FAKE_PAGE_MS and FAKE_CALL_MS make this answer as slowly as the live
// instance, for timing ADAM's pages against something honest. OpenProject 10
// takes a second and a half or more for a page of 200 work packages; the
// collection read is charged FAKE_PAGE_MS per 200 rows asked for (a quarter of
// it at least, because a small page is not free either), and every other
// request FAKE_CALL_MS. Concurrent requests are not queued behind each other,
// so this models an instance with room for every page asked at once — the
// live one has fewer workers than that, and a read with more pages in flight
// gains less there than it does here. Both default to 0: every check runs at
// full speed unless somebody asks for the slow one.
//
// `/_slow?page=&call=` changes them while running, for a check that has to
// catch a read in the middle — board-check's "Refresh does not wait" — and
// puts them back afterwards.
let PAGE_MS = Number(process.env.FAKE_PAGE_MS ?? 0);
let CALL_MS = Number(process.env.FAKE_CALL_MS ?? 0);
const pause = (ms) => (ms > 0 ? new Promise((resolve) => setTimeout(resolve, ms)) : null);

let nextId = 1200;
const created = [];
// Comments posted to each work package, by its number: read back by GET
// .../activities and listed whole at /_comments.
const comments = new Map();
// How many of the next creates to make and then answer 502 (/_lose-create).
let LOSE_CREATES = 0;
// `/_break?project=503&children=400`: answer the whole-project read (a project filter with every status and no
// parent filter) or the sub-task read (a parent filter) with that status, as a refusing or overloaded instance
// would; 0 or `off=1` heals. 400 on the sub-task read is an instance that does not know the parent filter.
const BREAK = { project: 0, children: 0, ignoreParent: 0 };

const read = (req) => new Promise((resolve) => {
  const parts = [];
  req.on('data', (c) => parts.push(c));
  req.on('end', () => { try { resolve(JSON.parse(Buffer.concat(parts).toString())); } catch { resolve({}); } });
});

const json = (res, code, body) => {
  res.writeHead(code, { 'content-type': 'application/json' });
  res.end(JSON.stringify(body));
};

createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const path = url.pathname;

  // What the check reads afterwards. Outside /api/v3 so it cannot be mistaken
  // for something OpenProject offers.
  if (path === '/_created') return json(res, 200, { created });
  // A work package made on the server, the way tools/op-create.rb makes one: ADAM never sees
  // the create. Kept out of `created`, which is what ADAM sent (CHG-ADM-003).
  // `id` and `description` make a ticket under its live number and text (mcp/pull-files-check.mjs pulls
  // #31848 and #36194 as they are on the instance); without them, the next number and no description.
  if (path === '/_make') {
    const id = Number(url.searchParams.get('id')) || nextId++;
    const parent = url.searchParams.get('parent');
    const description = url.searchParams.get('description');
    packages.set(String(id), {
      id, subject: url.searchParams.get('subject') ?? `Made on the server ${id}`, lockVersion: 1, percentageDone: 0,
      ...(description !== null ? { description: { raw: description } } : {}),
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
      _links: {
        project: { href: `/api/v3/projects/${url.searchParams.get('project') ?? PROJECT.id}`, title: PROJECT.name },
        type: { href: '/api/v3/types/1', title: 'Task' },
        status: { href: '/api/v3/statuses/1', title: 'New' },
        ...(parent ? { parent: { href: `/api/v3/work_packages/${parent}`, title: `Ticket ${parent}` } } : {}),
      },
    });
    return json(res, 200, { id });
  }
  // The next N creates are made, and answered 502 as a proxy that timed out would: the
  // ticket exists and the caller is told it does not (CHG-ADM-003).
  if (path === '/_lose-create') {
    LOSE_CREATES = Number(url.searchParams.get('n') ?? 1);
    return json(res, 200, { lose: LOSE_CREATES });
  }
  if (path === '/_comments') {
    return json(res, 200, { comments: Object.fromEntries([...comments].map(([k, list]) =>
      [k, list.map((c) => ({ text: c.comment.raw, notify: c.notify }))])) });
  }
  if (path === '/_time-entries') {
    if (url.searchParams.has('refuse')) REFUSE_TIME = url.searchParams.get('refuse') === '1';
    return json(res, 200, { refuse: REFUSE_TIME });
  }
  if (path === '/_slow') {
    if (url.searchParams.has('page')) PAGE_MS = Number(url.searchParams.get('page')) || 0;
    if (url.searchParams.has('call')) CALL_MS = Number(url.searchParams.get('call')) || 0;
    return json(res, 200, { pageMs: PAGE_MS, callMs: CALL_MS });
  }
  if (path === '/_status') {
    // `/_status?id=7403&status=9`: move a ticket to another status, as somebody working it would.
    const wp = packages.get(String(url.searchParams.get('id')));
    const st = STATUSES.find((s) => s.id === Number(url.searchParams.get('status')));
    if (!wp || !st) return json(res, 404, { message: 'no such ticket or status' });
    wp._links.status = { href: `/api/v3/statuses/${st.id}`, title: st.name };
    return json(res, 200, { id: wp.id, status: st.name });
  }
  if (path === '/_break') {
    if (url.searchParams.has('off')) { BREAK.project = 0; BREAK.children = 0; BREAK.ignoreParent = 0; }
    // An instance that accepts the parent filter and ignores it: every ticket comes back, whatever was asked.
    if (url.searchParams.has('ignoreparent')) BREAK.ignoreParent = Number(url.searchParams.get('ignoreparent')) || 0;
    if (url.searchParams.has('project')) BREAK.project = Number(url.searchParams.get('project')) || 0;
    if (url.searchParams.has('children')) BREAK.children = Number(url.searchParams.get('children')) || 0;
    return json(res, 200, BREAK);
  }

  if (!(req.headers.authorization ?? '').startsWith('Basic ')) {
    return json(res, 401, { message: 'no credential' });
  }

  if (PAGE_MS || CALL_MS) {
    const rows = Number(url.searchParams.get('pageSize') ?? 100);
    await pause(path === '/api/v3/work_packages' && req.method === 'GET'
      ? PAGE_MS * Math.max(0.25, rows / 200) : CALL_MS);
  }

  if (path === '/api/v3/users/me') {
    const me = userOf(req);
    return json(res, 200, { _type: 'User', id: me || 5,
                            name: userName(me || 5), login: `u${me}` });
  }

  if (path === '/api/v3/projects') {
    return json(res, 200, {
      total: 1, count: 1,
      _embedded: { elements: [{ ...PROJECT, _type: 'Project' }] },
    });
  }

  // Who a ticket in the project can be assigned to: the members the team view
  // matches a typed name against.
  const assignees = path.match(/^\/api\/v3\/projects\/(\d+)\/available_assignees$/);
  if (assignees) {
    if (assignees[1] !== String(PROJECT.id)) return json(res, 404, { message: 'no such project' });
    const elements = Object.entries(NAMES).map(([id, name]) => ({ _type: 'User', id: Number(id), name }));
    return json(res, 200, { total: elements.length, count: elements.length, _embedded: { elements } });
  }

  const types = path.match(/^\/api\/v3\/projects\/(\d+)\/types$/);
  if (types) {
    if (types[1] !== String(PROJECT.id)) return json(res, 404, { message: 'no such project' });
    return json(res, 200, { total: TYPES.length, _embedded: { elements: TYPES } });
  }

  // The collection, filtered. Enough of OpenProject's filter language for the
  // board and the overview to be exercised for real: assignee=me, the built-in
  // open/closed status sets, and the project. Everything else is ignored rather
  // than refused — a stand-in that argued about filters would fail tests about
  // something other than what they test.
  if (path === '/api/v3/work_packages' && req.method === 'GET') {
    let want = [];
    try { want = JSON.parse(url.searchParams.get('filters') ?? '[]'); } catch { want = []; }
    const filterOf = (name) => want.find((f) => Object.keys(f)[0] === name)?.[name];
    if (BREAK.children && filterOf('parent')) {
      return json(res, BREAK.children, { message: 'The sub-task read was refused (harness).' });
    }
    if (BREAK.project && filterOf('project') && filterOf('status')?.operator === '*' && !filterOf('parent')) {
      return json(res, BREAK.project, { message: 'The project read was refused (harness).' });
    }
    const closedOf = (wp) => {
      const href = wp._links?.status?.href ?? '';
      return STATUSES.find((st) => href.endsWith(`/${st.id}`))?.isClosed ?? false;
    };
    let rows = [...packages.values()];
    for (const f of want) {
      const [field, spec] = Object.entries(f)[0] ?? [];
      if (field === 'assignee' && spec.values?.includes('me')) {
        const me = userOf(req);
        rows = rows.filter((wp) => (wp._links?.assignee?.href ?? '') === `/api/v3/users/${me}`);
      } else if (field === 'assignee' && spec.operator === '=') {
        // By user id, which is how the team view asks about somebody else.
        rows = rows.filter((wp) => spec.values.some((v) => (wp._links?.assignee?.href ?? '') === `/api/v3/users/${v}`));
      } else if (field === 'status' && spec.operator === '=') {
        rows = rows.filter((wp) => spec.values.some((v) => (wp._links?.status?.href ?? '').endsWith(`/${v}`)));
      } else if (field === 'status' && spec.operator === 'o') {
        rows = rows.filter((wp) => !closedOf(wp));
      } else if (field === 'status' && spec.operator === 'c') {
        rows = rows.filter((wp) => closedOf(wp));
      } else if (field === 'project') {
        rows = rows.filter((wp) => (wp._links?.project?.href ?? '').endsWith(`/${spec.values[0]}`));
      } else if (field === 'parent' && BREAK.ignoreParent) {
        // ignored on purpose (/_break?ignoreparent=1)
      } else if (field === 'parent') {
        // The work packages directly under any of the numbers given, as OpenProject's parent filter answers.
        rows = rows.filter((wp) => spec.values.some((v) => (wp._links?.parent?.href ?? '') === `/api/v3/work_packages/${v}`));
      }
    }
    rows.sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)));
    const size = Number(url.searchParams.get('pageSize') ?? 100);
    // `offset` is OpenProject's page number, from 1.
    const from = (Math.max(1, Number(url.searchParams.get('offset') ?? 1)) - 1) * size;
    const page = rows.slice(from, from + size);
    // `groupBy=assignee`: the instance counts every matching row per assignee,
    // whatever the page size, and says so under `groups` (OpenProject 10's
    // shape: the name as `value`, the user under `_links.valueLink`).
    let groups;
    if (url.searchParams.get('groupBy') === 'assignee') {
      const by = new Map();
      for (const wp of rows) {
        const href = wp._links?.assignee?.href ?? '';
        const held = by.get(href) ?? { value: wp._links?.assignee?.title ?? null, count: 0,
          _links: { valueLink: href ? [{ href }] : [] } };
        held.count += 1;
        by.set(href, held);
      }
      groups = [...by.values()].map((g) => ({ _type: 'Group', ...g }));
    }
    return json(res, 200, {
      total: rows.length, count: page.length, pageSize: size,
      ...(groups ? { groups } : {}),
      _embedded: { elements: page },
    });
  }

  // Time entries, filtered by project, paged like the work packages. Who logged
  // the time is the ticket's holder; that is a simplification the live
  // instance does not make, and the costing page reads `user` either way.
  if (path === '/api/v3/time_entries' && req.method === 'GET') {
    if (REFUSE_TIME) {
      return json(res, 403, {
        _type: 'Error', errorIdentifier: 'urn:openproject-org:api:v3:errors:MissingPermission',
        message: 'You are not authorized to access this resource.',
      });
    }
    let want = [];
    try { want = JSON.parse(url.searchParams.get('filters') ?? '[]'); } catch { want = []; }
    const project = want.map((f) => f.project?.values?.[0]).find(Boolean);
    const rows = [];
    for (const wp of packages.values()) {
      if (project && !(wp._links?.project?.href ?? '').endsWith(`/${project}`)) continue;
      loggedOn(wp).forEach((e, n) => rows.push({
        _type: 'TimeEntry', id: wp.id * 100 + n, hours: isoHours(e.hours), spentOn: e.spentOn,
        comment: { raw: '' },
        _links: {
          project: wp._links.project,
          workPackage: { href: `/api/v3/work_packages/${wp.id}`, title: wp.subject },
          user: wp._links.assignee ?? { href: '/api/v3/users/5', title: 'Harness Person' },
        },
      }));
    }
    rows.sort((a, b) => a.id - b.id);
    const size = Number(url.searchParams.get('pageSize') ?? 100);
    const from = (Math.max(1, Number(url.searchParams.get('offset') ?? 1)) - 1) * size;
    const page = rows.slice(from, from + size);
    return json(res, 200, { _type: 'Collection', total: rows.length, count: page.length,
                            pageSize: size, _embedded: { elements: page } });
  }

  // A project's versions, with their dates. The harness milestones have none
  // of their own and are listed by name; the team dataset's sprints have dates.
  const versionList = path.match(/^\/api\/v3\/projects\/(\d+)\/versions$/);
  if (versionList) {
    if (versionList[1] !== String(PROJECT.id)) return json(res, 404, { message: 'no such project' });
    const named = [...new Set([...packages.values()].map((wp) => wp._links?.version?.title).filter(Boolean))];
    const elements = [
      ...VERSIONS,
      ...named.filter((n) => !VERSIONS.some((v) => v.name === n))
        .map((name, i) => ({ id: 300 + i, name, startDate: null, endDate: null, status: 'open' })),
    ].map((v) => ({ _type: 'Version', ...v }));
    return json(res, 200, { total: elements.length, _embedded: { elements } });
  }

  if (path === '/api/v3/statuses') {
    return json(res, 200, { total: STATUSES.length, _embedded: { elements: STATUSES } });
  }

  const one = path.match(/^\/api\/v3\/work_packages\/(\d+)$/);
  if (one && req.method === 'GET') {
    // With its children's links, titled with their subjects, as OpenProject sends them.
    const wp = ensure(one[1]);
    const href = `/api/v3/work_packages/${one[1]}`;
    const kids = [...packages.values()].filter((p) => p._links?.parent?.href === href)
      .map((p) => ({ href: `/api/v3/work_packages/${p.id}`, title: p.subject }));
    return json(res, 200, { ...wp, _links: { ...wp._links, ...(kids.length ? { children: kids } : {}) } });
  }
  if (one && req.method === 'PATCH') {
    const found = ensure(one[1]);
    const body = await read(req);
    // OpenProject refuses a stale lockVersion with a 409, and the bridge relies
    // on that being real — a stand-in that accepted anything would let the
    // optimistic-locking path pass without ever being exercised.
    if (body.lockVersion !== found.lockVersion) {
      return json(res, 409, { message: 'Invalid lock version' });
    }
    if (body.percentageDone !== undefined) found.percentageDone = body.percentageDone;
    // Dates, and the rule that makes them interesting. OpenProject derives a
    // parent's dates from its children while `scheduleManually` is false, and
    // refuses a PATCH that sets them with a 422 naming the field. The plan page
    // sends the flag in the same request for exactly this reason, so the
    // stand-in has to refuse the request that does not — otherwise the bridge
    // could stop sending it and every test would still pass.
    const setsDates = body.startDate !== undefined || body.dueDate !== undefined;
    if (setsDates && !found.scheduleManually && body.scheduleManually !== true) {
      return json(res, 422, {
        message: 'Start date cannot be set on an automatically scheduled parent.',
      });
    }
    if (body.scheduleManually !== undefined) found.scheduleManually = body.scheduleManually;
    if (body.startDate !== undefined) found.startDate = body.startDate;
    if (body.dueDate !== undefined) found.dueDate = body.dueDate;
    const href = body?._links?.status?.href ?? '';
    const status = STATUSES.find((st) => href.endsWith(`/${st.id}`));
    if (status) found._links.status = { href, title: status.name };
    found.lockVersion += 1;
    found.updatedAt = new Date().toISOString();
    return json(res, 200, found);
  }
  const activity = path.match(/^\/api\/v3\/work_packages\/(\d+)\/activities$/);
  if (activity && req.method === 'POST') {
    const body = await read(req);
    // Kept, so a second read of the thread sees it: a settled change request's
    // comment is posted once (cr_notice.py), and that is only testable if the
    // stand-in remembers what it was sent. `notify` is kept too, for the check
    // that settlement comments are sent without mail.
    const id = nextId++;
    if (!comments.has(activity[1])) comments.set(activity[1], []);
    comments.get(activity[1]).push({
      _type: 'Activity::Comment', id, createdAt: new Date().toISOString(),
      comment: { raw: body?.comment?.raw ?? '' }, notify: url.searchParams.get('notify'),
      _links: { user: { href: `/api/v3/users/${userOf(req) || 5}`, title: userName(userOf(req) || 5) } },
    });
    return json(res, 201, { _type: 'Activity', id });
  }
  // The thread under a ticket. Only a held ticket says anything of its own: it
  // is the reason the delivery overview shows beside it (main.py
  // `_held_reasons`). Then whatever was posted to it.
  if (activity && req.method === 'GET') {
    const wp = packages.get(activity[1]);
    const held = /hold/i.test(wp?._links?.status?.title ?? '');
    return json(res, 200, { _type: 'Collection', _embedded: { elements: [...(held ? [{
      _type: 'Activity::Comment', createdAt: '2026-10-07T07:29:15Z',
      comment: { raw: 'Waiting on the payments provider to confirm gift-card refunds.' },
      _links: { user: { href: '/api/v3/users/9', title: 'Hrushikant Patkar' } },
    }] : []), ...(comments.get(activity[1]) ?? [])] } });
  }

  const make = path.match(/^\/api\/v3\/projects\/(\d+)\/work_packages$/);
  if (make && req.method === 'POST') {
    const body = await read(req);
    if (!String(body.subject ?? '').trim()) {
      return json(res, 422, { message: 'Subject cannot be blank' });
    }
    const typeHref = body?._links?.type?.href ?? '';
    const type = TYPES.find((t) => typeHref.endsWith(`/${t.id}`)) ?? TYPES[0];
    const id = nextId++;
    const made = {
      id, subject: body.subject, lockVersion: 1, percentageDone: 0,
      createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
      _links: {
        project: { href: `/api/v3/projects/${make[1]}`, title: PROJECT.name },
        type: { href: `/api/v3/types/${type.id}`, title: type.name },
        status: { href: '/api/v3/statuses/1', title: 'New' },
        ...(body?._links?.parent ? { parent: { href: body._links.parent.href, title: 'Checkout, phase two' } } : {}),
      },
    };
    packages.set(String(id), made);
    created.push({
      id,
      subject: body.subject,
      description: body?.description?.raw ?? '',
      parent: body?._links?.parent?.href ?? null,
      type: typeHref || null,
      project: Number(make[1]),
    });
    if (LOSE_CREATES > 0) {
      LOSE_CREATES -= 1;
      return json(res, 502, { message: 'Bad gateway: the origin did not answer in time' });
    }
    return json(res, 201, made);
  }

  return json(res, 404, { message: `nothing at ${path}` });
}).listen(PORT, '127.0.0.1', () => console.log(`fake OpenProject on ${PORT}`));
