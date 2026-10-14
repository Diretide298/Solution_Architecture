// Giving an existing account another project, and taking one away.
//
// Until this route, the only thing that wrote `account_project` was redeeming
// an invite, so somebody already on TICVAI who was needed on a second package
// had no way in short of a second account under a second address. These are
// the checks that the new door opens the right amount and no further:
//
//   **The project role is derived, never chosen.** A client given a second
//   project is a client there too; a reviewer, developer or lead lands as a
//   reviewer, exactly as redemption does. A caller cannot ask for more.
//
//   **Only an administrator**, and an administrator's own grants are refused
//   rather than stored, because they already open every project and a row
//   that changes nothing reads as one that did something.
//
//   **The access is real.** `/api/auth/me` is the whole of the reading
//   server's access check, so the grant has to show up there and the revoke
//   has to take it away there, not just in the admin page's list.
//
// Wants a service with an empty store, and a second project registered in
// projects.json (greenleaf-demo is, in this repository):
//   TICVAI_DB=/tmp/ap.db python -m uvicorn api.main:app --port 8799
//   API=http://localhost:8799 node api/account-projects-check.mjs

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

async function recruit(handle, role, email = `${handle}@softlabsgroup.com`) {
  const made = await as('boss', 'POST', '/api/invites', { email, role });
  if (made.status !== 200) return { ok: false, why: `invite: ${made.status} ${made.data?.detail ?? ''}` };
  const token = (made.data.link ?? '').split('#')[1];
  const took = await as(handle, 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: handle });
  return took.status === 200 ? { ok: true } : { ok: false, why: `redeem: ${took.status}` };
}

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
for (const [handle, role, email] of [
  ['harness.dev', 'dev'], ['harness.client', 'client', 'someone@client-company.example'],
  ['harness.second', 'admin'], ['harness.pm', 'pm'],
]) {
  const r = await recruit(handle, role, email);
  check(`${role === 'admin' ? 'an' : 'a'} ${role} is invited and signs up`, r.ok, r.why ?? '');
}

const projects = (await as('boss', 'GET', '/api/pms/projects')).data?.projects ?? [];
const first = projects.find((p) => p.id === 'ticvai');
const other = projects.find((p) => p.id !== 'ticvai' && p.active);
check('there is a second project to give', Boolean(first && other),
  projects.map((p) => p.id).join(' ') || 'none');

const roster = async () => (await as('boss', 'GET', '/api/accounts')).data?.accounts ?? [];
const byName = async (name) => (await roster()).find((a) => a.name === name);
const dev = await byName('harness.dev');
const client = await byName('harness.client');
const second = await byName('harness.second');
const opens = async (who) => ((await as(who, 'GET', '/api/auth/me')).data?.projects ?? []);

// ── the list says who opens what ─────────────────────────────────────

check('the accounts list names the projects each account opens',
  JSON.stringify(dev?.projects?.map((p) => p.id)) === '["ticvai"]', JSON.stringify(dev?.projects));

// ── giving one ───────────────────────────────────────────────────────

check('before the grant, the developer cannot open the second project',
  !(await opens('harness.dev')).some((p) => p.id === other.id),
  JSON.stringify(await opens('harness.dev')));
const gave = await as('boss', 'PUT', `/api/accounts/${dev.id}/projects/${other.id}`);
check('an administrator gives a developer the second project', gave.status === 200,
  `${gave.status} ${JSON.stringify(gave.data)}`);
check('as a reviewer there, which is what every non-client is on a project',
  gave.data?.project?.role === 'reviewer', gave.data?.project?.role);
const devOpens = await opens('harness.dev');
check('and the developer can open it now, in the access check itself',
  devOpens.some((p) => p.id === other.id && p.role === 'reviewer'), JSON.stringify(devOpens));
check('while keeping the first',
  devOpens.some((p) => p.id === 'ticvai'), JSON.stringify(devOpens));
check('the accounts list says so too',
  (await byName('harness.dev'))?.projects?.some((p) => p.id === other.id));

const twice = await as('boss', 'PUT', `/api/accounts/${dev.id}/projects/${other.id}`);
check('giving it twice is refused rather than stored twice', twice.status === 409,
  `${twice.status} ${twice.data?.detail ?? ''}`);

const gaveClient = await as('boss', 'PUT', `/api/accounts/${client.id}/projects/${other.id}`);
check('a client given a project is a client there',
  gaveClient.status === 200 && gaveClient.data?.project?.role === 'client',
  `${gaveClient.status} ${gaveClient.data?.project?.role}`);
check('and the access check agrees',
  (await opens('harness.client')).some((p) => p.id === other.id && p.role === 'client'));

const toAdmin = await as('boss', 'PUT', `/api/accounts/${second.id}/projects/${other.id}`);
check('an administrator is not given a project, because they already open every one',
  toAdmin.status === 409, `${toAdmin.status} ${toAdmin.data?.detail ?? ''}`);

const nowhere = await as('boss', 'PUT', `/api/accounts/${dev.id}/projects/no-such-project`);
check('a project that does not exist is refused', nowhere.status === 400, `${nowhere.status}`);
const nobody = await as('boss', 'PUT', `/api/accounts/999999/projects/${other.id}`);
check('an account that does not exist is refused', nobody.status === 404, `${nobody.status}`);

// ── nobody else may ──────────────────────────────────────────────────

const pmTries = await as('harness.pm', 'PUT', `/api/accounts/${client.id}/projects/ticvai`);
check('a project manager may not give a project', pmTries.status === 403, `${pmTries.status}`);
const selfServe = await as('harness.client', 'PUT', `/api/accounts/${client.id}/projects/ticvai`);
check('nor may anybody give one to themselves', selfServe.status === 403, `${selfServe.status}`);
const pmTakes = await as('harness.pm', 'DELETE', `/api/accounts/${dev.id}/projects/${other.id}`);
check('nor take one away', pmTakes.status === 403, `${pmTakes.status}`);
const stranger = await fetch(`${API}/api/accounts/${dev.id}/projects/${other.id}`, { method: 'PUT' });
check('and a stranger is asked to sign in', stranger.status === 401, `${stranger.status}`);

// ── taking one away ──────────────────────────────────────────────────

const took = await as('boss', 'DELETE', `/api/accounts/${dev.id}/projects/${other.id}`);
check('an administrator takes the project away', took.status === 200, `${took.status}`);
check('and the developer can no longer open it',
  !(await opens('harness.dev')).some((p) => p.id === other.id), JSON.stringify(await opens('harness.dev')));
const again = await as('boss', 'DELETE', `/api/accounts/${dev.id}/projects/${other.id}`);
check('taking it twice says they could not open it anyway', again.status === 404, `${again.status}`);

const last = await as('boss', 'DELETE', `/api/accounts/${dev.id}/projects/ticvai`);
check('the last one may be taken too: a missing row is no access, by design',
  last.status === 200 && (await opens('harness.dev')).length === 0,
  `${last.status} ${JSON.stringify(await opens('harness.dev'))}`);
check('and the account is still there, only with nothing to open',
  (await byName('harness.dev'))?.active === 1 && (await byName('harness.dev'))?.projects?.length === 0);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
