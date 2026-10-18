#!/usr/bin/env node
// The stand-in OpenProject for the rehearsal pull (release runbook section 4; CHG-RHS-001): OpenProject 10's REST
// answers for one project, from the state tools/rehearse/simulate.py writes (the project as the release's apply will
// leave it). Listens on 127.0.0.1 only; nothing it is sent leaves the process; comments ADAM posts are kept in memory.
//
// **It answers only what it knows.** A route, a method, a filter or a sort it does not know is a 501 naming it, so a
// connector that starts asking something new fails the rehearsal instead of reading a wrong answer: the r6 stand-in
// ignored filters, and "the children of #1" would have come back as the whole project.
//
//   PORT=8998 TOKEN=<token> node tools/rehearse/stand-in-openproject.mjs <op-state.json>
//   node tools/rehearse/stand-in-openproject.mjs --self-test
//
// GET /__rehearsal/stats (no credential): how many OpenProject calls it answered, by route. The judge requires more
// than none: a rehearsal whose ADAM read some other OpenProject proves nothing. The self-tests run first, every time.
import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';

const idOf = (link) => (link?.href ? String(link.href).split('/').pop() : null);
const collection = (elements) => ({
  _type: 'Collection', total: elements.length, count: elements.length, _embedded: { elements },
});
const SORTS = {
  id: (a, b) => a.id - b.id,
  updatedAt: (a, b) => String(a.updatedAt ?? '').localeCompare(String(b.updatedAt ?? '')),
};

function load(S, token) {
  const kids = new Map();
  for (const wp of Object.values(S.packages)) {
    const p = idOf(wp._links?.parent);
    if (p) kids.set(p, [...(kids.get(p) ?? []), { href: `/api/v3/work_packages/${wp.id}`, title: wp.subject }]);
  }
  for (const [p, list] of kids) if (S.packages[p]) S.packages[p]._links.children = list;
  return {
    S, token,
    me: S.users['Rehearsal Account'],
    names: Object.fromEntries(Object.entries(S.users).map(([n, i]) => [String(i), n])),
    closed: new Set(S.statuses.filter((s) => s.isClosed).map((s) => s.name)),
    posted: new Map(),
    stats: { total: 0, byRoute: {} },
  };
}

function compile(filters, ctx) {
  const tests = [];
  for (const f of Array.isArray(filters) ? filters : [filters]) {
    const entries = Object.entries(f ?? {});
    if (entries.length !== 1) return { error: `a filter names one field: ${JSON.stringify(f)}` };
    const [name, spec] = entries[0];
    const op = spec?.operator;
    const vals = (spec?.values ?? []).map(String);
    if (name === 'project' && op === '=') tests.push(() => vals.includes(String(ctx.S.project.id)));
    else if (name === 'status' && op === '*') tests.push(() => true);
    else if (name === 'status' && op === 'o') tests.push((wp) => !ctx.closed.has(wp._links.status.title));
    else if (name === 'status' && op === 'c') tests.push((wp) => ctx.closed.has(wp._links.status.title));
    else if (name === 'status' && op === '=') tests.push((wp) => vals.includes(idOf(wp._links.status)));
    else if (name === 'parent' && op === '=') tests.push((wp) => vals.includes(idOf(wp._links.parent)));
    else if (name === 'assignee' && op === '=') {
      const who = vals.map((v) => (v === 'me' ? String(ctx.me) : v));
      tests.push((wp) => who.includes(idOf(wp._links.assignee)));
    } else return { error: `the stand-in OpenProject does not answer the filter ${name} ${op}` };
  }
  return { test: (wp) => tests.every((t) => t(wp)) };
}

function list(ctx, url) {
  const q = url.searchParams;
  if (q.has('groupBy')) return [501, { message: `the stand-in OpenProject does not answer groupBy=${q.get('groupBy')}` }];
  let filters;
  try { filters = JSON.parse(q.get('filters') ?? '[]'); } catch { return [400, { message: 'filters is not JSON' }]; }
  const f = compile(filters, ctx);
  if (f.error) return [501, { message: f.error }];
  let rows = Object.values(ctx.S.packages).filter(f.test).sort(SORTS.id);
  if (q.has('sortBy')) {
    let sort;
    try { sort = JSON.parse(q.get('sortBy')); } catch { return [400, { message: 'sortBy is not JSON' }]; }
    for (const [field, dir] of [...sort].reverse()) {
      const by = SORTS[field];
      if (!by || !['asc', 'desc'].includes(dir)) {
        return [501, { message: `the stand-in OpenProject does not sort by ${field} ${dir}` }];
      }
      rows = [...rows].sort((a, b) => (dir === 'asc' ? by(a, b) : by(b, a)));
    }
  }
  const size = Math.max(1, Number(q.get('pageSize') ?? 20));
  const page = Math.max(1, Number(q.get('offset') ?? 1));
  const slice = rows.slice((page - 1) * size, page * size);
  return [200, { _type: 'WorkPackageCollection', total: rows.length, count: slice.length, pageSize: size,
    offset: page, _embedded: { elements: slice } }];
}

function activities(ctx, method, id, body) {
  if (!ctx.S.packages[id]) return [404, { message: 'The requested resource could not be found.' }];
  if (method === 'POST') {
    let text = '';
    try { text = JSON.parse(body || '{}')?.comment?.raw ?? ''; } catch { /* kept empty */ }
    ctx.posted.set(id, [...(ctx.posted.get(id) ?? []),
      { author: 'Rehearsal Account', at: new Date().toISOString(), text }]);
    return [201, { _type: 'Activity::Comment', id: 5000000 + ctx.stats.total }];
  }
  if (method !== 'GET') return [501, { message: `the stand-in OpenProject does not answer ${method} on activities` }];
  const all = [...(ctx.S.comments?.[id] ?? []), ...(ctx.posted.get(id) ?? [])];
  return [200, collection(all.map((c, n) => ({
    _type: 'Activity::Comment', id: n + 1, createdAt: c.at, comment: { format: 'markdown', raw: c.text ?? '' },
    _links: { user: { href: `/api/v3/users/${ctx.S.users[c.author] ?? 0}`, title: c.author ?? '' } },
  })))];
}

function answer(ctx, method, rawUrl, authorization, body = '') {
  const url = new URL(rawUrl, 'http://stand-in');
  const p = url.pathname;
  if (p === '/__rehearsal/stats') return [200, ctx.stats];
  const route = `${method} ${p.replace(/\/\d+(?=\/|$)/g, '/:n')}`;
  ctx.stats.total += 1;
  ctx.stats.byRoute[route] = (ctx.stats.byRoute[route] ?? 0) + 1;
  if (!String(authorization ?? '').startsWith('Basic ')) return [401, { message: 'no credential' }];
  const token = Buffer.from(authorization.slice(6), 'base64').toString().split(':').slice(1).join(':');
  if (token !== ctx.token) return [401, { message: 'bad token' }];
  const { S } = ctx;
  const P = S.project.id;
  let m;
  if (method === 'GET') {
    if (p === '/api/v3/users/me') return [200, { _type: 'User', id: ctx.me, name: 'Rehearsal Account', login: 'rehearsal' }];
    if ((m = p.match(/^\/api\/v3\/users\/(\d+)$/))) {
      return ctx.names[m[1]] ? [200, { _type: 'User', id: Number(m[1]), name: ctx.names[m[1]] }]
        : [404, { message: 'The requested resource could not be found.' }];
    }
    if (p === '/api/v3/projects') return [200, collection([{ _type: 'Project', ...S.project }])];
    if (p === '/api/v3/statuses') return [200, collection(S.statuses.map((s) => ({ _type: 'Status', ...s })))];
    if (p === `/api/v3/projects/${P}/versions`) {
      return [200, collection(S.versions.map((v) => ({ _type: 'Version', ...v, status: 'open' })))];
    }
    if (p === `/api/v3/projects/${P}/available_assignees`) {
      return [200, collection(Object.entries(S.users).map(([name, id]) => ({ _type: 'User', id, name })))];
    }
    if (/^\/api\/v3\/work_packages\/schemas\/\d+-\d+$/.test(p)) {
      return [200, { _type: 'Schema', [S.field]: { type: 'Integer', name: 'Priority_No.' } }];
    }
    if ((m = p.match(/^\/api\/v3\/work_packages\/(\d+)$/))) {
      const wp = S.packages[m[1]];
      return wp ? [200, wp] : [404, { message: 'The requested resource could not be found.' }];
    }
    if (p === '/api/v3/work_packages' || p === `/api/v3/projects/${P}/work_packages`) return list(ctx, url);
  }
  if ((m = p.match(/^\/api\/v3\/work_packages\/(\d+)\/activities$/))) return activities(ctx, method, m[1], body);
  return [501, { message: `the stand-in OpenProject does not answer ${method} ${p}` }];
}

function selfTest() {
  const fails = [];
  const st = (id, name, isClosed = false) => ({ id, name, isClosed, isDefault: id === 1 });
  const NEW = st(1, 'New');
  const REJ = st(14, 'Rejected', true);
  const wp = (id, status, parent, assignee) => ({
    _type: 'WorkPackage', id, subject: `ticket ${id}`, updatedAt: `2026-10-1${id}T09:00:00Z`, customField9: id,
    description: { format: 'markdown', raw: `text ${id}` },
    _links: {
      status: { href: `/api/v3/statuses/${status.id}`, title: status.name },
      ...(parent ? { parent: { href: `/api/v3/work_packages/${parent}`, title: `ticket ${parent}` } } : {}),
      ...(assignee ? { assignee: { href: `/api/v3/users/${assignee}`, title: 'Pranay Shinde' } } : {}),
    },
  });
  const ctx = load({
    project: { id: 153, identifier: 'ticvai', name: 'TICVAI' }, field: 'customField9', statuses: [NEW, REJ],
    users: { 'Rehearsal Account': 101, 'Pranay Shinde': 102 }, versions: [{ id: 77, name: 'Sprint 1' }],
    packages: { 1: wp(1, NEW), 2: wp(2, NEW, 1, 102), 3: wp(3, REJ, 1) },
    comments: { 2: [{ author: 'Pranay Shinde', at: '2026-10-16T09:00:00Z', text: 'hello' }] },
  }, 'k');
  const auth = `Basic ${Buffer.from('apikey:k').toString('base64')}`;
  const get = (u) => answer(ctx, 'GET', u, auth);
  const ids = (u) => { const [code, b] = get(u); return code === 200 ? b._embedded.elements.map((e) => e.id) : code; };
  const q = (filters, extra = '') => `/api/v3/work_packages?filters=${encodeURIComponent(JSON.stringify(filters))}${extra}`;
  const check = (what, got, want) => {
    if (JSON.stringify(got) !== JSON.stringify(want)) fails.push(`${what}: got ${JSON.stringify(got)}, want ${JSON.stringify(want)}`);
  };
  check('no credential', answer(ctx, 'GET', '/api/v3/users/me', '')[0], 401);
  check('another token', answer(ctx, 'GET', '/api/v3/users/me', `Basic ${Buffer.from('apikey:x').toString('base64')}`)[0], 401);
  check('me', get('/api/v3/users/me')[1].id, 101);
  check('a parent lists its children', get('/api/v3/work_packages/1')[1]._links.children.map((c) => c.href),
    ['/api/v3/work_packages/2', '/api/v3/work_packages/3']);
  check('an unknown ticket', get('/api/v3/work_packages/9')[0], 404);
  check('children by filter', ids(q([{ parent: { operator: '=', values: ['1'] } }])), [2, 3]);
  check('open children', ids(q([{ parent: { operator: '=', values: ['1'] } }, { status: { operator: 'o', values: [] } }])), [2]);
  check('closed', ids(q([{ status: { operator: 'c', values: [''] } }])), [3]);
  check('every status', ids(q([{ project: { operator: '=', values: ['153'] } }, { status: { operator: '*', values: [] } }])), [1, 2, 3]);
  check('assigned to 102', ids(q([{ assignee: { operator: '=', values: ['102'] } }])), [2]);
  check('assigned to me', ids(q([{ assignee: { operator: '=', values: ['me'] } }])), []);
  check('a filter it does not know', get(q([{ subject: { operator: '~', values: ['x'] } }]))[0], 501);
  check('newest first', ids(q([], `&sortBy=${encodeURIComponent('[["id","desc"]]')}`)), [3, 2, 1]);
  check('a sort it does not know', get(q([], `&sortBy=${encodeURIComponent('[["priority","asc"]]')}`))[0], 501);
  check('grouped', get(q([], '&groupBy=assignee'))[0], 501);
  check('page 2 of 1', ids(q([], '&pageSize=1&offset=2')), [2]);
  check('the project path', ids('/api/v3/projects/153/work_packages?pageSize=10'), [1, 2, 3]);
  check('comments', get('/api/v3/work_packages/2/activities')[1]._embedded.elements.map((e) => [e.comment.raw, e._links.user.title]),
    [['hello', 'Pranay Shinde']]);
  check('a comment ADAM posts', answer(ctx, 'POST', '/api/v3/work_packages/2/activities', auth,
    JSON.stringify({ comment: { raw: 'from ADAM' } }))[0], 201);
  check('kept in memory', get('/api/v3/work_packages/2/activities')[1]._embedded.elements.map((e) => e.comment.raw),
    ['hello', 'from ADAM']);
  check('a write it does not do', answer(ctx, 'PATCH', '/api/v3/work_packages/2', auth, '{}')[0], 501);
  check('the build order field', get('/api/v3/work_packages/schemas/153-1')[1].customField9.name, 'Priority_No.');
  check('statuses', get('/api/v3/statuses')[1]._embedded.elements.map((s) => [s.name, s.isClosed]), [['New', false], ['Rejected', true]]);
  check('versions', get('/api/v3/projects/153/versions')[1]._embedded.elements.map((v) => v.name), ['Sprint 1']);
  check('assignable', get('/api/v3/projects/153/available_assignees')[1]._embedded.elements.length, 2);
  check('a user', get('/api/v3/users/102')[1].name, 'Pranay Shinde');
  const s = answer(ctx, 'GET', '/__rehearsal/stats', '')[1];
  check('it counts what it answered', s.total > 20 && s.byRoute['GET /api/v3/work_packages/:n'] >= 2, true);
  return fails;
}

const fails = selfTest();
for (const f of fails) console.log(`  SELF-TEST    ${f}`);
if (fails.length) {
  console.log(`FAIL ${fails.length} self-test(s)`);
  process.exit(1);
}
if (process.argv[2] === '--self-test') {
  console.log('PASS - the stand-in answers as OpenProject 10 does, and refuses what it does not know');
  process.exit(0);
}
if (!process.env.TOKEN || !process.argv[2]) {
  console.error('usage: PORT=<port> TOKEN=<token> node stand-in-openproject.mjs <op-state.json>');
  process.exit(2);
}
const ctx = load(JSON.parse(readFileSync(process.argv[2], 'utf8')), process.env.TOKEN);
const PORT = Number(process.env.PORT ?? 8998);
createServer((req, res) => {
  let body = '';
  req.on('data', (c) => { body += c; if (body.length > 1e6) req.destroy(); });
  req.on('end', () => {
    const [code, out] = answer(ctx, req.method, req.url, req.headers.authorization, body);
    res.writeHead(code, { 'content-type': 'application/json' });
    res.end(JSON.stringify(out));
  });
}).listen(PORT, '127.0.0.1', () => console.log(
  `stand-in OpenProject on 127.0.0.1:${PORT}: ${Object.keys(ctx.S.packages).length} work packages, release ${ctx.S.release}`));
