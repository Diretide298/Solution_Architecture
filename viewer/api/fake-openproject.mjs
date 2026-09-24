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
  { id: 1, name: 'New', isClosed: false },
  { id: 7, name: 'In progress', isClosed: false },
  { id: 12, name: 'Closed', isClosed: true },
];

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

/** Which user a token belongs to. The whole point of `assignee = me` is that
 *  the answer depends on who is asking, so a stand-in that ignored the
 *  credential would make "a board is only ever your own" untestable. */
function userOf(req) {
  const header = (req.headers.authorization ?? '').replace(/^Basic /, '');
  const token = Buffer.from(header, 'base64').toString().split(':')[1] ?? '';
  return USERS[token] ?? 0;
}

function own(id, { subject, status = 7, done = 0, start, due, parent, version, user = 5, updated, spent, estimate }) {
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
  wp._links.assignee = { href: `/api/v3/users/${user}`, title: user === 5 ? 'Harness Person' : 'Somebody Else' };
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

let nextId = 1200;
const created = [];

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

  if (!(req.headers.authorization ?? '').startsWith('Basic ')) {
    return json(res, 401, { message: 'no credential' });
  }

  if (path === '/api/v3/users/me') {
    const me = userOf(req);
    return json(res, 200, { _type: 'User', id: me || 5,
                            name: me === 6 ? 'Somebody Else' : 'Harness Person', login: `u${me}` });
  }

  if (path === '/api/v3/projects') {
    return json(res, 200, {
      total: 1, count: 1,
      _embedded: { elements: [{ ...PROJECT, _type: 'Project' }] },
    });
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
      } else if (field === 'status' && spec.operator === 'o') {
        rows = rows.filter((wp) => !closedOf(wp));
      } else if (field === 'status' && spec.operator === 'c') {
        rows = rows.filter((wp) => closedOf(wp));
      } else if (field === 'project') {
        rows = rows.filter((wp) => (wp._links?.project?.href ?? '').endsWith(`/${spec.values[0]}`));
      }
    }
    rows.sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)));
    const size = Number(url.searchParams.get('pageSize') ?? 100);
    return json(res, 200, {
      total: rows.length, count: Math.min(rows.length, size),
      _embedded: { elements: rows.slice(0, size) },
    });
  }

  if (path === '/api/v3/statuses') {
    return json(res, 200, { total: STATUSES.length, _embedded: { elements: STATUSES } });
  }

  const one = path.match(/^\/api\/v3\/work_packages\/(\d+)$/);
  if (one && req.method === 'GET') {
    return json(res, 200, ensure(one[1]));
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
    await read(req);
    return json(res, 201, { _type: 'Activity', id: nextId++ });
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
    return json(res, 201, made);
  }

  return json(res, 404, { message: `nothing at ${path}` });
}).listen(PORT, '127.0.0.1', () => console.log(`fake OpenProject on ${PORT}`));
