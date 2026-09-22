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
    return json(res, 200, { _type: 'User', id: 5, name: 'Harness Person', login: 'harness' });
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
