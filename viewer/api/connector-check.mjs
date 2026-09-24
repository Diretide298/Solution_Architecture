// Which connector build somebody is running, and who is allowed to see it.
//
// The reporting itself is two lines of SQL and not worth a harness. What is
// worth one is everything around it:
//
//   **A developer cannot see the fleet.** This names people and machines. The
//   line is the same one the agent usage draws — your own, unless you oversee —
//   and it is the kind of line that quietly moves when somebody adds a
//   convenience later.
//
//   **Nobody can report a build against somebody else.** There is no account in
//   the body, on purpose. This proves that staying true: the only thing a caller
//   can influence is their own row, whatever they send.
//
//   **Two machines are two rows; the same machine twice is one.** A developer
//   with a laptop and a desktop updates them separately, and collapsing them
//   would report whichever they last started. Restarting Claude Code four times
//   in an afternoon must not make four rows.
//
//   **The service does not answer which build is current.** It has no connector
//   files to hash. If it ever starts guessing, the page has two sources for one
//   number and they will disagree.
//
//   TICVAI_DB=/tmp/conn.db TICVAI_SECRET_KEY=... python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/conn.db API=http://localhost:8799 node api/connector-check.mjs

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
  try { data = await res.json(); } catch { /* an empty body is an answer */ }
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

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an account exists', boot.status === 200, `${boot.status}`);
check('a developer is invited', (await recruit('harness.dev', 'dev')).ok);
check('and a project manager, who oversees', (await recruit('harness.pm', 'pm')).ok);

// ── reporting ────────────────────────────────────────────────────────

const said = await as('harness.dev', 'POST', '/api/connector/seen',
  { build: 'aaaaaaaaaaaa', host: 'DEV-LAPTOP', agent: 'claude-code' });
check('a connector can say which build it is', said.status === 200, `${said.status}`);

const again = await as('harness.dev', 'POST', '/api/connector/seen',
  { build: 'bbbbbbbbbbbb', host: 'DEV-LAPTOP', agent: 'claude-code' });
check('and saying it again updates rather than appends', again.status === 200);

const second = await as('harness.dev', 'POST', '/api/connector/seen',
  { build: 'cccccccccccc', host: 'DEV-DESKTOP', agent: 'claude-code' });
check('a second machine is a second install', second.status === 200);

const mine = await as('harness.dev', 'GET', '/api/connector/fleet');
check('a developer sees their own installs', mine.status === 200, `${mine.status}`);
check('both machines, and only two of them',
  (mine.data?.installs ?? []).length === 2,
  (mine.data?.installs ?? []).map((i) => `${i.host}:${i.build}`).join(' '));
check('the second report replaced the first, it did not add to it',
  (mine.data?.installs ?? []).some((i) => i.host === 'DEV-LAPTOP' && i.build === 'bbbbbbbbbbbb'),
  JSON.stringify(mine.data?.installs ?? []));
check('and it is not presented as the whole fleet', mine.data?.whole === false,
  String(mine.data?.whole));
check('every row is marked as theirs',
  (mine.data?.installs ?? []).every((i) => i.mine === true));

// ── the door ─────────────────────────────────────────────────────────

// The interesting case: a developer reporting in, then asking who else has.
// A page that simply does not draw the column is not a rule.
const devSees = (mine.data?.installs ?? []).map((i) => i.email);
check('a developer is not told about anybody else',
  devSees.every((e) => e === 'harness.dev@softlabsgroup.com'),
  devSees.join(' '));

await as('harness.pm', 'POST', '/api/connector/seen',
  { build: 'bbbbbbbbbbbb', host: 'PM-BOX', agent: 'claude-code' });
const whole = await as('harness.pm', 'GET', '/api/connector/fleet');
check('oversight sees every install', whole.status === 200 && whole.data?.whole === true,
  `${whole.status} whole=${whole.data?.whole}`);
check('which is three: two of the developer\'s and their own',
  (whole.data?.installs ?? []).length === 3,
  (whole.data?.installs ?? []).map((i) => i.host).join(' '));
check('and their own row is the only one marked theirs',
  (whole.data?.installs ?? []).filter((i) => i.mine).length === 1);

// ── what cannot be forged ────────────────────────────────────────────

// An account id in the body is ignored rather than honoured. The route takes no
// such field, so this is really a test that it never grows one: if somebody adds
// `account_id` to the model, this fails.
const forged = await as('harness.dev', 'POST', '/api/connector/seen',
  { build: 'dddddddddddd', host: 'PM-BOX', agent: 'claude-code', account_id: 1, email: 'harness.pm@softlabsgroup.com' });
check('a report naming somebody else is accepted, as the caller', forged.status === 200);
const after = await as('harness.pm', 'GET', '/api/connector/fleet');
const pmBox = (after.data?.installs ?? []).filter((i) => i.host === 'PM-BOX');
check('and it did not touch their row',
  pmBox.some((i) => i.email === 'harness.pm@softlabsgroup.com' && i.build === 'bbbbbbbbbbbb'),
  JSON.stringify(pmBox));
check('it made one of the caller\'s own instead',
  pmBox.some((i) => i.email === 'harness.dev@softlabsgroup.com' && i.build === 'dddddddddddd'),
  JSON.stringify(pmBox));

// ── what the service declines to know ────────────────────────────────

check('the fleet never claims which build is current',
  !('serving' in (whole.data ?? {})) && !('current' in (whole.data ?? {})),
  Object.keys(whole.data ?? {}).join(' '));

// A build it cannot read is stored as empty rather than refused: seeing that an
// install reported in and could not hash itself is worth more than a 422 that
// disappears into the connector's silent catch.
const blank = await as('harness.dev', 'POST', '/api/connector/seen', { host: 'DEV-LAPTOP' });
check('a connector that cannot read its own files still reports', blank.status === 200,
  `${blank.status}`);
const blanked = await as('harness.dev', 'GET', '/api/connector/fleet');
check('and is shown as an install with no build',
  (blanked.data?.installs ?? []).some((i) => i.host === 'DEV-LAPTOP' && i.build === ''),
  JSON.stringify(blanked.data?.installs ?? []));

// Signed out is signed out. Reporting a build is not public: the list of
// machines and who owns them is exactly what it would leak.
const anon = await fetch(`${API}/api/connector/fleet`);
check('signed out cannot read the fleet', anon.status === 401 || anon.status === 403,
  `${anon.status}`);
const anonPost = await fetch(`${API}/api/connector/seen`, {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ build: 'eeeeeeeeeeee', host: 'NOBODY' }),
});
check('nor report one', anonPost.status === 401 || anonPost.status === 403, `${anonPost.status}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
