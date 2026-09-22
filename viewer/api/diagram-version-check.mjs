// A diagram somebody arranged by hand, kept and versioned.
//
// Three things this file is about:
//
//   **The package is never written to.** What is stored is where each box was
//   dropped, and the nodes still come from the package on every draw — so a
//   published diagram cannot disagree with the contracts about what exists.
//   There is no route here that touches a file.
//
//   **Nothing is ever deleted.** Saving retires the version before it and keeps
//   it; restoring an old one retires the current one and keeps that. "We just
//   do not show it" is a different thing from "it is gone", and the second is
//   how a rearrangement nobody liked becomes unrecoverable.
//
//   **A hand-arranged diagram keeps looking current after the package moves
//   on**, which is the real danger of free-form editing. The page sends a hash
//   of what it drew; the service compares it with what the arrangement was made
//   against and says so. Unknown is its own answer, separate from "no".
//
//   TICVAI_DB=/tmp/dv.db python -m uvicorn api.main:app --port 8799
//   API=http://localhost:8799 node api/diagram-version-check.mjs

const API = process.env.API ?? 'http://localhost:8787';
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
  const made = await as('boss', 'POST', '/api/invites',
    { email: `${handle}@softlabsgroup.com`, role });
  if (made.status !== 200) return { ok: false, why: `invite: ${made.status}` };
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  const took = await as(handle, 'POST', '/api/auth/redeem',
    { token, password: PASSWORD, name: handle });
  return took.status === 200 ? { ok: true } : { ok: false, why: `redeem: ${took.status}` };
}

const D = 'graph:spine';
const SHAPE_A = '17-9f2c1a3b';   // what the page drew when it was arranged
const SHAPE_B = '19-4d88e017';   // the package, later
const layout = (n) => ({
  nodes: Object.fromEntries(
    Array.from({ length: n }, (_, i) => [`node-${i}`, { x: i * 10, y: i * 5 }])),
});

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
check('a team lead is invited', (await recruit('harness.lead', 'lead')).ok);
check('and a developer', (await recruit('harness.dev', 'dev')).ok);

// ── before anybody has arranged anything ─────────────────────────────

const fresh = await as('harness.dev', 'GET', `/api/diagram-versions/${D}?source_hash=${SHAPE_A}`);
check('a diagram with no saved arrangement reads cleanly', fresh.status === 200,
  `${fresh.status} ${JSON.stringify(fresh.data?.detail ?? '')}`);
check('and says there is none rather than inventing one',
  fresh.data?.current === null, JSON.stringify(fresh.data?.current));
check('a developer is told they cannot publish one',
  fresh.data?.mayPublish === false, String(fresh.data?.mayPublish));

const junk = await as('harness.lead', 'GET', '/api/diagram-versions/not a diagram key');
check('a name that is not view:scope is refused, with the shape',
  junk.status === 400 && /graph:spine/.test(String(junk.data?.detail)),
  String(junk.data?.detail).slice(0, 70));

// ── who may publish ──────────────────────────────────────────────────

const byDev = await as('harness.dev', 'POST', `/api/diagram-versions/${D}`,
  { layout: layout(3), source_hash: SHAPE_A });
check('a developer cannot publish an arrangement for everybody',
  byDev.status === 403, `${byDev.status}`);
check('and is told their own still works, which is the part that matters',
  /stays on your screen/.test(String(byDev.data?.detail)), String(byDev.data?.detail));

const empty = await as('harness.lead', 'POST', `/api/diagram-versions/${D}`,
  { layout: { nodes: {} }, source_hash: SHAPE_A });
check('an arrangement with nothing arranged in it is refused',
  empty.status === 400, String(empty.data?.detail).slice(0, 60));

const first = await as('harness.lead', 'POST', `/api/diagram-versions/${D}`,
  { layout: layout(4), source_hash: SHAPE_A, note: 'Grouped by tier' });
check('a team lead can publish one', first.status === 200 && first.data?.version === 1,
  `${first.status} v${first.data?.version}`);

// ── everybody sees it, and it is not stale ───────────────────────────

const seen = await as('harness.dev', 'GET',
  `/api/diagram-versions/${D}?source_hash=${SHAPE_A}`);
check('everybody opening the diagram now gets that arrangement',
  seen.data?.current?.version === 1, String(seen.data?.current?.version));
check('with the positions, which is the thing being drawn',
  Object.keys(seen.data?.current?.layout?.nodes ?? {}).length === 4,
  String(Object.keys(seen.data?.current?.layout?.nodes ?? {}).length));
check('and who arranged it and why', seen.data?.current?.savedBy === 'harness.lead'
  && seen.data?.current?.note === 'Grouped by tier',
  `${seen.data?.current?.savedBy}: ${seen.data?.current?.note}`);
check('drawn against the package as it stands, so not stale',
  seen.data?.stale === false, String(seen.data?.stale));

// ── and the reason the hash is there ─────────────────────────────────

const moved = await as('harness.dev', 'GET',
  `/api/diagram-versions/${D}?source_hash=${SHAPE_B}`);
check('the same arrangement against a changed package reads as stale',
  moved.data?.stale === true, String(moved.data?.stale));
check('while still being served — a stale picture is better than no picture, '
  + 'as long as it says so',
  moved.data?.current?.version === 1, String(moved.data?.current?.version));

const silent = await as('harness.dev', 'GET', `/api/diagram-versions/${D}`);
check('a page that sends no hash gets "not known", not "fine"',
  silent.data?.stale === null, String(silent.data?.stale));

// ── versions accumulate and nothing is deleted ───────────────────────

const second = await as('harness.lead', 'POST', `/api/diagram-versions/${D}`,
  { layout: layout(6), source_hash: SHAPE_B, note: 'Redone after the contracts moved' });
check('saving again is a new version, not an edit of the old one',
  second.data?.version === 2, String(second.data?.version));
check('and says which one it retired', second.data?.retired === 1,
  String(second.data?.retired));

const history = await as('harness.lead', 'GET', `/api/diagram-versions/${D}/versions`);
check('both versions are listed, newest first',
  (history.data?.versions ?? []).map((v) => v.version).join(',') === '2,1',
  (history.data?.versions ?? []).map((v) => v.version).join(','));
check('one current, one retired',
  (history.data?.versions ?? []).map((v) => v.status).join(',') === 'current,retired',
  (history.data?.versions ?? []).map((v) => v.status).join(','));
check('the retired one records who retired it and when',
  Boolean(history.data.versions[1].retiredBy && history.data.versions[1].retiredAt),
  `${history.data.versions[1].retiredBy}`);
check('and the listing does not carry every coordinate, only how many',
  history.data.versions[0].layout === undefined
  && history.data.versions[0].nodes === 6,
  `${history.data.versions[0].nodes} boxes`);

// ── going back ───────────────────────────────────────────────────────

const back = await as('harness.lead', 'POST', `/api/diagram-versions/${D}/restore/1`, {});
check('an older version can be brought back', back.status === 200, `${back.status}`);
const now = await as('harness.dev', 'GET', `/api/diagram-versions/${D}?source_hash=${SHAPE_A}`);
check('and is what everybody sees again', now.data?.current?.version === 1,
  String(now.data?.current?.version));
const kept = await as('harness.lead', 'GET', `/api/diagram-versions/${D}/versions`);
check('the one it replaced is kept, not lost — so it can be restored back',
  (kept.data?.versions ?? []).length === 2
  && kept.data.versions.find((v) => v.version === 2)?.status === 'retired',
  kept.data.versions.map((v) => `${v.version}:${v.status}`).join(' '));

const again = await as('harness.lead', 'POST', `/api/diagram-versions/${D}/restore/1`, {});
check('restoring the one already showing is refused rather than churning',
  again.status === 409, `${again.status}`);
const nothere = await as('harness.lead', 'POST', `/api/diagram-versions/${D}/restore/9`, {});
check('and a version that never existed is a 404', nothere.status === 404, `${nothere.status}`);

// ── back to the generated diagram ────────────────────────────────────

const byDev2 = await as('harness.dev', 'POST', `/api/diagram-versions/${D}/retire`, {});
check('a developer cannot retire one either', byDev2.status === 403, `${byDev2.status}`);

const off = await as('harness.lead', 'POST', `/api/diagram-versions/${D}/retire`, {});
check('an admin or a lead can go back to the generated diagram',
  off.status === 200, `${off.status}`);
const generated = await as('harness.dev', 'GET',
  `/api/diagram-versions/${D}?source_hash=${SHAPE_A}`);
check('and then there is no arrangement to lay over it',
  generated.data?.current === null, JSON.stringify(generated.data?.current));
check('while both versions are still there to restore',
  generated.data?.retired === 2, String(generated.data?.retired));
const twice = await as('harness.lead', 'POST', `/api/diagram-versions/${D}/retire`, {});
check('retiring when nothing is showing says so rather than pretending',
  twice.status === 409, `${twice.status}`);

const revived = await as('harness.lead', 'POST', `/api/diagram-versions/${D}/restore/2`, {});
check('and an arrangement can come back from that', revived.status === 200,
  `${revived.status}`);

// ── one diagram's arrangement is not another's ───────────────────────

const other = await as('harness.dev', 'GET',
  `/api/diagram-versions/data:orders?source_hash=${SHAPE_A}`);
check('a different diagram has its own history, not this one',
  other.data?.current === null && other.data?.retired === 0,
  JSON.stringify(other.data?.current));
const scoped = await as('harness.lead', 'POST', '/api/diagram-versions/data:orders',
  { layout: layout(2) });
check('and versions there start at 1 again, not at 4',
  scoped.data?.version === 1, String(scoped.data?.version));

// ── an admin too, not only a lead ────────────────────────────────────

const byAdmin = await as('boss', 'POST', `/api/diagram-versions/${D}`,
  { layout: layout(5), note: 'An admin can publish as well' });
check('an admin publishes the same way a lead does', byAdmin.status === 200,
  `${byAdmin.status}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
