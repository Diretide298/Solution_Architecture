// What a change request's ticket says, and telling an open ticket by hand.
//
// The changes page asks, before Accept is pressed, what settling would do to
// the ticket the request came out of (`ticket/source`, which reads only), and
// offers "Add a comment to #NNNN" for an accepted request whose open ticket was
// never told - settled before 14 October, through the spreadsheet, or by
// somebody with no OpenProject token. That comment goes through the same
// propose-then-confirm as the ticket: the preview sends nothing.
//
// **Run against a stand-in OpenProject**, as cr-ticket-check is: the stand-in
// keeps every comment it was sent at /_comments, which is the only way to
// assert that a preview sent nothing and an apply sent exactly one.
//
//   PORT=8798 node api/fake-openproject.mjs
//   TICVAI_DB=/tmp/crc.db TICVAI_SECRET_KEY=... TICVAI_PMS_URL=http://127.0.0.1:8798 \
//     python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/crc.db API=http://localhost:8799 \
//     PMS=http://127.0.0.1:8798 node api/cr-comment-check.mjs

import { execFileSync } from 'node:child_process';

const API = process.env.API ?? 'http://localhost:8787';
const STORE = process.env.TICVAI_DB ?? '';
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

function cli(...args) {
  return execFileSync('python', ['-m', 'api.cli', ...args], {
    cwd: new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'),
    env: { ...process.env, TICVAI_DB: STORE },
    encoding: 'utf8',
  });
}

const PASSWORD = 'a-long-enough-passphrase';
async function recruit(handle, role) {
  const email = `${handle}@softlabsgroup.com`;
  const made = await as('boss', 'POST', '/api/invites', { email, role });
  if (made.status !== 200) return { ok: false, why: `invite: ${made.status}` };
  const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
  const took = await as(handle, 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: handle });
  return took.status === 200 ? { ok: true, email } : { ok: false, why: `redeem: ${took.status}` };
}
const connect = (who) => as(who, 'PUT', '/api/settings/openproject', { token: 'harness-key', endpoint: PMS });
const file = (who, fields) => as(who, 'POST', '/api/changes', {
  target_kind: 'screen', target_id: 'POS-002', tag: 'frontend',
  title: fields.title ?? 'The total is wrong on the receipt',
  problem: 'The printed total excludes service charge, and the screen includes it.',
  ...fields,
});
const thread = async (key) => ((await (await fetch(`${PMS}/_comments`)).json()).comments ?? {})[key] ?? [];

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
check('and is made the super admin', /is now System Architect/.test(STORE ? cli('owner', 'harness.boss@softlabsgroup.com') : ''),
  STORE ? '' : 'no TICVAI_DB given');
check('and connects to the stand-in OpenProject', (await connect('boss')).status === 200);
const mapped = await as('boss', 'PUT', '/api/pms/projects/ticvai', { pms_project_id: 42 });
check('the ADAM project is pointed at an OpenProject project', mapped.status === 200, `${mapped.status}`);
const hand = await recruit('harness.dev', 'dev');
check('and a developer', hand.ok, hand.why ?? '');
await connect('harness.dev');

// ── reading the ticket, before deciding ─────────────────────────────

const raised = await file('harness.dev', { ticket: '880' });
const CR = raised.data?.change?.id;
check('a request raised from a ticket carries a link to it',
  /\/work_packages\/880$/.test(raised.data?.change?.ticketUrl ?? ''), raised.data?.change?.ticketUrl);

const before = (await thread('880')).length;
const src = await as('boss', 'GET', `/api/changes/${CR}/ticket/source?project_id=ticvai`);
check('the source reads the ticket it came out of', src.status === 200 && src.data?.read === true
  && src.data?.key === '880' && src.data?.closed === false && /Checkout/.test(src.data?.subject ?? ''),
  JSON.stringify({ s: src.status, read: src.data?.read, key: src.data?.key, closed: src.data?.closed }));
check('and says accepting would comment on it, because it is open',
  src.data?.onSettle?.accepted?.action === 'comment', JSON.stringify(src.data?.onSettle?.accepted));
check('and that nothing has told it yet', Array.isArray(src.data?.told) && src.data.told.length === 0,
  JSON.stringify(src.data?.told));
check('and reading it sent nothing', (await thread('880')).length === before);

const closedOne = await file('harness.dev', { ticket: '7005', title: 'Raised from a shipped ticket' });
const closedSrc = await as('boss', 'GET', `/api/changes/${closedOne.data.change.id}/ticket/source?project_id=ticvai`);
check('a closed ticket is read as closed, and accepting it would file a ticket instead',
  closedSrc.data?.closed === true && closedSrc.data?.onSettle?.accepted?.action === 'ticket',
  JSON.stringify(closedSrc.data?.onSettle?.accepted));

const loose = await file('harness.dev', { title: 'Found while reading the package' });
const looseSrc = await as('boss', 'GET', `/api/changes/${loose.data.change.id}/ticket/source?project_id=ticvai`);
check('a request from no ticket is answered, not refused', looseSrc.status === 200 && looseSrc.data?.read === false
  && /no ticket/.test(looseSrc.data?.why ?? ''), JSON.stringify(looseSrc.data?.why));

// ── the comment, by hand ─────────────────────────────────────────────

const early = await as('boss', 'POST', `/api/changes/${CR}/comment/preview`, {});
check('an open request has nothing to tell yet', early.status === 409, `${early.status} ${early.data?.detail}`);

// Settled without telling the ticket: what the spreadsheet and settle_changes.py do.
const settled = await as('boss', 'POST', `/api/changes/${CR}/resolve`,
  { status: 'accepted', resolution: 'The receipt prints the service charge as its own line.', tell_ticket: false });
check('it is accepted without the ticket being told', settled.status === 200
  && (await thread('880')).length === before, `${settled.status}`);

const byDev = await as('harness.dev', 'POST', `/api/changes/${CR}/comment/preview`, {});
check('a developer cannot tell the ticket', byDev.status === 403, `${byDev.status}`);

const preview = await as('boss', 'POST', `/api/changes/${CR}/comment/preview`, {});
check('the preview words the comment', preview.status === 200 && preview.data?.key === '880'
  && /ADAM .* · accepted/.test(preview.data?.text ?? '') && /own line/.test(preview.data?.text ?? ''),
  `${preview.status} ${JSON.stringify(preview.data?.detail ?? '')}`);
check('and sends nothing', (await thread('880')).length === before);

const theft = await as('harness.dev', 'POST', `/api/changes/${CR}/comment/${preview.data?.proposal}/apply`, {});
check('nobody else applies the proposal you were shown', theft.status === 403 || theft.status === 404, `${theft.status}`);

const posted = await as('boss', 'POST', `/api/changes/${CR}/comment/${preview.data?.proposal}/apply`, {});
const after = await thread('880');
check('applying posts exactly one comment', posted.status === 200 && posted.data?.already === false
  && after.length === before + 1, `${posted.status} ${after.length - before}`);
check('without mail, like the settle\'s own comment', after.at(-1)?.notify === 'false', String(after.at(-1)?.notify));

const twice = await as('boss', 'POST', `/api/changes/${CR}/comment/${preview.data?.proposal}/apply`, {});
check('the same proposal cannot be applied twice', twice.status === 409, `${twice.status}`);
const again = await as('boss', 'POST', `/api/changes/${CR}/comment/preview`, {});
check('and a second preview is refused: the ticket already has it', again.status === 409
  && /already has/.test(String(again.data?.detail)), `${again.status} ${again.data?.detail}`);
const told = await as('boss', 'GET', `/api/changes/${CR}/ticket/source?project_id=ticvai`);
check('and the source now says it was told', (told.data?.told ?? []).includes('accepted'), JSON.stringify(told.data?.told));

// A request whose ticket is closed gets a ticket, not a comment nobody pulls.
await as('boss', 'POST', `/api/changes/${closedOne.data.change.id}/resolve`,
  { status: 'accepted', resolution: 'Built as new work.', tell_ticket: false });
const onClosed = await as('boss', 'POST', `/api/changes/${closedOne.data.change.id}/comment/preview`, {});
check('a closed ticket is not commented on: make a ticket instead', onClosed.status === 409
  && /Make a ticket/.test(String(onClosed.data?.detail)), `${onClosed.status} ${onClosed.data?.detail}`);

// A preview worded for one settlement is not posted after another.
const moving = await file('harness.dev', { ticket: '880', title: 'Settled twice' });
const M = moving.data.change.id;
await as('boss', 'POST', `/api/changes/${M}/resolve`, { status: 'accepted', resolution: 'Yes.', tell_ticket: false });
const stale = await as('boss', 'POST', `/api/changes/${M}/comment/preview`, {});
await as('boss', 'POST', `/api/changes/${M}/resolve`, { status: 'rejected', resolution: 'No after all.', tell_ticket: false });
const late = await as('boss', 'POST', `/api/changes/${M}/comment/${stale.data?.proposal}/apply`, {});
check('a comment previewed for "accepted" is refused once the request is rejected', late.status === 409
  && /changed since that preview/.test(String(late.data?.detail)), `${late.status} ${late.data?.detail}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
