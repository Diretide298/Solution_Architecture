// The role model: seven roles, three axes, and one hazard worth most of this
// file.
//
// **The hazard is the owner seeing less than an admin.** Every one of these
// checks used to be `role == "admin"`, which was exact while "administers" had
// one spelling. Adding a super admin above the admin turns each one left behind
// into a refusal of the person who is supposed to be able to do everything —
// and it fails quietly, one route at a time, in whatever order somebody happens
// to click. So most of what is below is the owner doing ordinary administrative
// things and being allowed to.
//
// The rest is the other direction: the things that are the owner's alone, and
// the doors the role must not be reachable through.
//
// Wants a service with an empty store, and the store's path, because making an
// owner is deliberately not something the API can do:
//   TICVAI_DB=/tmp/roles.db python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/roles.db API=http://localhost:8799 node api/roles-check.mjs
import { execFileSync } from 'node:child_process';
import { layersFor, mayCall } from '../lib/audience.mjs';

const API = process.env.API ?? 'http://localhost:8787';
const STORE = process.env.TICVAI_DB ?? '';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

// One jar per person, because most of this is about two people disagreeing
// about what they may do.
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

/** The CLI, against the same store the service has open. This is the only way
 *  an owner comes into existence, so exercising it here is not incidental —
 *  it is the grant path itself under test. */
function cli(...args) {
  return execFileSync('python', ['-m', 'api.cli', ...args], {
    cwd: new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'),
    env: { ...process.env, TICVAI_DB: STORE },
    encoding: 'utf8',
  });
}

const PASSWORD = 'a-long-enough-passphrase';

/** Invite somebody and redeem it, so the account exists with the role asked
 *  for. The admin does the inviting, which is the only way accounts are made. */
async function recruit(handle, role) {
  const email = `${handle}@softlabsgroup.com`;
  const made = await as('admin', 'POST', '/api/invites', { email, role });
  if (made.status !== 200) return { ok: false, why: `invite: ${made.status} ${JSON.stringify(made.data?.detail)}` };
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  if (!token) return { ok: false, why: `no token in ${JSON.stringify(made.data)}` };
  const took = await as(handle, 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: handle });
  if (took.status !== 200) return { ok: false, why: `redeem: ${took.status} ${JSON.stringify(took.data?.detail)}` };
  return { ok: true, email };
}

// ── the first admin, then the owner above them ───────────────────────

const boot = await as('admin', 'POST', '/api/auth/bootstrap', {
  email: 'harness.admin@softlabsgroup.com', name: 'Harness Admin', password: PASSWORD,
});
check('the first account is an admin', boot.status === 200 && boot.data?.role === 'admin',
  `${boot.status} ${boot.data?.role}`);

const chief = await recruit('harness.chief', 'admin');
check('a second admin is invited', chief.ok, chief.why ?? '');

// The CLI is the only door. Everything below leans on this having worked.
const said = STORE ? cli('owner', 'harness.chief@softlabsgroup.com') : '';
check('the CLI makes them the super admin', /is now owner/.test(said), said.trim() || 'no TICVAI_DB given');

const me = await as('harness.chief', 'GET', '/api/auth/me');
check('and they are an owner on their next request', me.data?.account?.role === 'owner',
  me.data?.account?.role ?? 'not signed in');

// ── an owner may do everything an admin may ──────────────────────────
//
// One per guard that used to compare to the string. A failure here is the
// hazard this file exists for.

for (const [what, method, path] of [
  ['read the roster', 'GET', '/api/accounts'],
  ['read the invites', 'GET', '/api/invites'],
  ['download the register', 'GET', '/api/export/verdicts'],
  ['download the change requests', 'GET', '/api/export/changes'],
  ['read who owns what', 'GET', '/api/scopes'],
]) {
  const r = await as('harness.chief', method, path);
  check(`an owner can ${what}`, r.status === 200, `${r.status} ${JSON.stringify(r.data?.detail ?? '')}`);
}

const invited = await as('harness.chief', 'POST', '/api/invites',
  { email: 'harness.byowner@softlabsgroup.com', role: 'reviewer' });
check('an owner can invite', invited.status === 200, `${invited.status}`);

// ── and the things that are the owner's alone ────────────────────────

const lead = await recruit('harness.lead', 'lead');
check('a team lead is invited', lead.ok, lead.why ?? '');
const leadId = (await as('admin', 'GET', '/api/accounts')).data
  ?.accounts?.find((a) => a.email === 'harness.lead@softlabsgroup.com')?.id;
check('and can be found on the roster', Number.isInteger(leadId), String(leadId));

const byAdmin = await as('admin', 'POST', `/api/accounts/${leadId}/scopes`,
  { tag: 'frontend', platform: 'P01' });
check('an admin cannot hand out a platform', byAdmin.status === 403, `${byAdmin.status}`);

const byOwner = await as('harness.chief', 'POST', `/api/accounts/${leadId}/scopes`,
  { tag: 'frontend', platform: 'P01' });
check('the owner can', byOwner.status === 200,
  `${byOwner.status} ${JSON.stringify(byOwner.data?.detail ?? '')}`);
check('and it says what it is in words', byOwner.data?.scope?.says === 'Frontend · P01',
  byOwner.data?.scope?.says ?? '');

const whole = await as('harness.chief', 'POST', `/api/accounts/${leadId}/scopes`,
  { tag: 'backend' });
check('a side with no platform is the whole side', whole.data?.scope?.says === 'Backend · all platforms',
  whole.data?.scope?.says ?? `${whole.status}`);
check('which is a different grant from a named platform',
  whole.status === 200 && whole.data.scope.id !== byOwner.data.scope.id);

const twice = await as('harness.chief', 'POST', `/api/accounts/${leadId}/scopes`,
  { tag: 'frontend', platform: 'P01' });
check('the same grant twice is refused', twice.status === 409, `${twice.status}`);

const junk = await as('harness.chief', 'POST', `/api/accounts/${leadId}/scopes`,
  { tag: 'frontend', platform: 'the storefront' });
check('a platform that is not a platform code is refused', junk.status === 400,
  junk.data?.detail ?? `${junk.status}`);

const badTag = await as('harness.chief', 'POST', `/api/accounts/${leadId}/scopes`,
  { tag: 'sideways' });
check('a side that is neither frontend nor backend is refused', badTag.status === 400, `${badTag.status}`);

// An admin is whole rather than scoped, so a scope row on one is meaningless.
const adminId = (await as('admin', 'GET', '/api/accounts')).data
  ?.accounts?.find((a) => a.email === 'harness.admin@softlabsgroup.com')?.id;
const onAdmin = await as('harness.chief', 'POST', `/api/accounts/${adminId}/scopes`,
  { tag: 'frontend' });
check('an admin cannot be given a platform, because they already have all of them',
  onAdmin.status === 409, onAdmin.data?.detail ?? `${onAdmin.status}`);

const seen = await as('admin', 'GET', `/api/accounts/${leadId}/scopes`);
check('an admin may read who owns what', seen.status === 200 && seen.data.scopes.length === 2,
  `${seen.status} ${seen.data?.scopes?.length}`);

const gone = await as('harness.chief', 'DELETE', `/api/scopes/${byOwner.data.scope.id}`);
check('and the owner can take one back', gone.status === 200, `${gone.status}`);

// ── the role cannot be reached through the API, by any door ──────────

const grant = await as('harness.chief', 'POST', `/api/accounts/${leadId}/role?role=owner`);
check('not even an owner can grant owner through the API', grant.status === 403,
  grant.data?.detail ?? `${grant.status}`);

const chiefId = (await as('admin', 'GET', '/api/accounts')).data
  ?.accounts?.find((a) => a.email === 'harness.chief@softlabsgroup.com')?.id;
const demote = await as('admin', 'POST', `/api/accounts/${chiefId}/role?role=reviewer`);
check('an admin cannot demote the owner', demote.status === 403, `${demote.status}`);

const disable = await as('admin', 'POST', `/api/accounts/${chiefId}/active?active=false`);
check('nor disable them', disable.status === 409, disable.data?.detail ?? `${disable.status}`);

const ownerInvite = await as('harness.chief', 'POST', '/api/invites',
  { email: 'harness.sneak@softlabsgroup.com', role: 'owner' });
check('an invite cannot carry the role either', ownerInvite.status === 403,
  ownerInvite.data?.detail ?? `${ownerInvite.status}`);

// ── the last administrator ───────────────────────────────────────────
//
// The count has to include owners, or a store with an owner and one admin
// refuses to demote the admin on the grounds that nobody would be left — which
// is false, and blocks a change that is perfectly safe.

const selfDemote = await as('admin', 'POST', `/api/accounts/${adminId}/role?role=reviewer`);
check('you cannot take administration away from yourself', selfDemote.status === 409,
  selfDemote.data?.detail ?? `${selfDemote.status}`);

const demoteOther = await as('harness.chief', 'POST', `/api/accounts/${adminId}/role?role=pm`);
check('the owner can demote the only admin, because an owner still administers',
  demoteOther.status === 200, demoteOther.data?.detail ?? `${demoteOther.status}`);

// ── a pm watches, and does not settle ────────────────────────────────
//
// **A pm has a voice.** require_voice is open to everybody, client included, on
// the argument that a reader who finds a fault and cannot say so will say it
// somewhere nobody is reading — and a pm is no exception to that. What they may
// not do is declare the matter dealt with: close a review item, or settle a
// change request. Saying what you think and saying it is handled are two acts,
// and only the second is withheld.

const pmSaw = await as('admin', 'GET', '/api/auth/me');
check('the demoted admin is now a pm', pmSaw.data?.account?.role === 'pm', pmSaw.data?.account?.role);

const pmSpoke = await as('admin', 'POST', '/api/validation',
  { target_kind: 'table', target_id: 'orders.sales_order', verdict: 'needs-work',
    note: 'A pm can still say a thing is wrong.' });
check('a pm can record a verdict, like everybody else', pmSpoke.status === 200,
  `${pmSpoke.status} ${JSON.stringify(pmSpoke.data?.detail ?? '')}`);

const changes = await as('admin', 'GET', '/api/changes');
check('a pm reads the change requests', changes.status === 200, `${changes.status}`);
check('but is not offered the decision on one', changes.data?.mayResolve === false,
  String(changes.data?.mayResolve));

const reviewerSees = await as('harness.lead', 'GET', '/api/changes');
check('a lead is', reviewerSees.data?.mayResolve === true, String(reviewerSees.data?.mayResolve));

const pmAdmin = await as('admin', 'GET', '/api/accounts');
check('and a pm cannot read the roster, being no longer an admin', pmAdmin.status === 403,
  `${pmAdmin.status}`);

// ── the Build layer, which is the owner's ────────────────────────────
//
// Two halves and both matter: the tab strip is told what it may open, and the
// route refuses anybody else regardless of what the strip was told.

// Both take two roles, and the pair is the point. The server narrows `role` to
// the project grant — reviewer or client, never owner — before the gate runs,
// so a version of these that asked one role asked the project one, and refused
// the super admin the layer that is theirs while blaming a reviewer they were
// not. Every call below names both, in that order.

check('only an owner is offered the Build layer',
  layersFor('owner', 'reviewer').includes('build')
  && !['admin', 'pm', 'lead', 'dev', 'reviewer'].some((r) => layersFor(r, 'reviewer').includes('build')),
  ['owner', 'admin', 'reviewer'].map((r) => `${r}:${layersFor(r, 'reviewer').includes('build')}`).join(' '));

check('and only an owner may call for it',
  mayCall('owner', 'reviewer', 'build')
  && !mayCall('admin', 'reviewer', 'build')
  && !mayCall('reviewer', 'client', 'build'));

check('the rest of the strip is unchanged for everybody else',
  layersFor('reviewer', 'reviewer').join(' ') === 'frontend uiux contracts domain backend services cicd decisions',
  layersFor('reviewer', 'reviewer').join(' '));

check('a client still cannot reach the decisions',
  !mayCall('reviewer', 'client', 'decisions') && mayCall('reviewer', 'reviewer', 'decisions'));

// The two axes compose rather than override. An owner who is a client on this
// particular package keeps Build, which is about the installation, and loses
// Decisions, which is about the package.
const ownerAsClient = layersFor('owner', 'client');
check('the two axes compose: an owner who is a client here keeps Build',
  ownerAsClient.includes('build'), ownerAsClient.join(' '));
check('and still loses the Decisions, which is the project’s question',
  !ownerAsClient.includes('decisions'), ownerAsClient.join(' '));

check('the strip keeps its order whoever is reading',
  layersFor('owner', 'reviewer').indexOf('build')
    === layersFor('owner', 'reviewer').indexOf('cicd') - 1,
  layersFor('owner', 'reviewer').join(' '));

// ── and the CLI will not strand the store ────────────────────────────

if (STORE) {
  let refused = '';
  try { cli('owner', 'harness.chief@softlabsgroup.com', '--revoke', '--to', 'reviewer'); }
  catch (error) { refused = String(error.stderr ?? error.stdout ?? error.message); }
  check('the CLI refuses to leave nobody able to administer',
    /last account that can administer/.test(refused), refused.trim().slice(0, 120));
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
