// What a developer's agent is told about change requests, and how much of it.
//
// 6 November 2026: the agents' change-request work was about half of every tool
// call they made, and most of that was reading. Three things are tested here:
//
//   **A draft does the duplicate check itself.** It answers the open requests on
//   its target or on any artefact it names, and the ones settled on them lately
//   with their decision, so the agent need not page through the list first.
//
//   **A list can be asked for what was settled since a time, a page at a time.**
//   `total` still counts every match.
//
//   **The usage hook's answer lengths are kept and added up,** with how deep
//   into their sessions change requests were drafted.
//
//   TICVAI_DB=/tmp/crt.db python -m uvicorn api.main:app --port 8799
//   TICVAI_DB=/tmp/crt.db API=http://localhost:8799 node api/changes-tokens-check.mjs

import { execFileSync } from 'node:child_process';

const API = process.env.API ?? 'http://localhost:8787';
const STORE = process.env.TICVAI_DB ?? '';
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
  return took.status === 200 ? { ok: true } : { ok: false, why: `redeem: ${took.status}` };
}

const raise = (fields) => as('harness.dev', 'POST', '/api/changes', {
  target_kind: 'operation', target_id: 'orders#getOrder', tag: 'backend',
  title: 'A gap', problem: 'Something the ticket needs is missing.', ticket: '7001', ...fields,
});
const settle = (id, resolution) => as('boss', 'POST', `/api/changes/${id}/resolve`,
  { status: 'done', resolution, tell_ticket: false });

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
if (STORE) cli('owner', 'harness.boss@softlabsgroup.com');
check('a developer is invited', (await recruit('harness.dev', 'dev')).ok);

// ── requests on the same artefacts ───────────────────────────────────

const onTarget = await raise({ title: 'getOrder: personal fields are not gated' });
const viaArtefact = await raise({ target_id: 'orders#listOrders', artefacts: ['orders#getOrder'], title: 'listOrders and getOrder disagree' });
const elsewhere = await raise({ target_id: 'catalogue#searchCatalogue', title: 'Somewhere else entirely' });
const decided = await raise({ target_id: 'orders#modifyOrder', artefacts: ['orders#getOrder'], ticket: '7002', title: 'modifyOrder answers through getOrder' });
check('four requests are raised', [onTarget, viaArtefact, elsewhere, decided].every((r) => r.status === 200),
  [onTarget, viaArtefact, elsewhere, decided].map((r) => `${r.status} ${JSON.stringify(r.data?.detail ?? '')}`).join(' | '));
const settled = await settle(decided.data?.change?.id, 'Gate the personal fields with x-ticvai-personal-data: gated, as listOrders does.');
check('one of them is settled', settled.status === 200, `${settled.status} ${JSON.stringify(settled.data?.detail ?? '')}`);

const draft = await as('harness.dev', 'POST', '/api/changes/drafts', {
  target_kind: 'operation', target_id: 'orders#getOrder', title: 'getOrder has no personal-data gating',
  problem: 'Staff without GUEST_VIEW_PII get the holder name.', ticket: '7003',
});
check('a draft is made', draft.status === 200 && Boolean(draft.data?.draft), `${draft.status} ${JSON.stringify(draft.data?.detail ?? '')}`);
const openIds = (draft.data?.alreadyOpen ?? []).map((c) => c.id);
check('**alreadyOpen names the open request on the same target**', openIds.includes(onTarget.data?.change?.id), openIds.join(','));
check('**and the one that names it among its artefacts**', openIds.includes(viaArtefact.data?.change?.id), openIds.join(','));
check('but not one on something else', !openIds.includes(elsewhere.data?.change?.id), openIds.join(','));
const recent = draft.data?.recentlySettled ?? [];
check('**recentlySettled carries the settled one, with its decision**',
  recent.length === 1 && recent[0].id === decided.data?.change?.id && /x-ticvai-personal-data: gated/.test(recent[0].decision ?? ''),
  JSON.stringify(recent).slice(0, 200));
check('the rows are short: no problem, evidence or options',
  (draft.data?.alreadyOpen ?? []).every((c) => !('problem' in c) && !('evidence' in c) && !('options' in c)));

const byArtefact = await as('harness.dev', 'POST', '/api/changes/drafts', {
  target_kind: 'operation', target_id: 'orders#holdOrder', artefacts: ['orders#listOrders'],
  title: 'holdOrder and listOrders', problem: 'They disagree.',
});
check('**a draft whose own artefacts touch a request finds it too**',
  (byArtefact.data?.alreadyOpen ?? []).some((c) => c.id === viaArtefact.data?.change?.id),
  JSON.stringify(byArtefact.data?.alreadyOpen?.map((c) => c.id)));

// ── a list of what was settled, a page at a time ─────────────────────

const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10);
const since = await as('harness.dev', 'GET', `/api/changes?ticket=7002&settled_since=${yesterday}`);
check('**settled_since answers the decisions that reached the ticket**',
  since.status === 200 && since.data.items.length === 1 && since.data.items[0].id === decided.data?.change?.id,
  `${since.status} ${JSON.stringify(since.data?.items?.map((c) => c.id) ?? since.data?.detail)}`);
const tomorrow = new Date(Date.now() + 86_400_000).toISOString().replace(/\.\d+Z$/, 'Z');
const none = await as('harness.dev', 'GET', `/api/changes?settled_since=${tomorrow}`);
check('and nothing when nothing was settled since then', none.status === 200 && none.data.items.length === 0, `${none.status}`);
const bad = await as('harness.dev', 'GET', '/api/changes?settled_since=last-tuesday');
check('a time it cannot read is refused with the reason', bad.status === 400 && /settled_since/.test(bad.data?.detail ?? ''), `${bad.status}`);

const page = await as('harness.dev', 'GET', '/api/changes?limit=2');
check('**limit gives a page, and total still counts every match**',
  page.status === 200 && page.data.items.length === 2 && page.data.total === 4 && page.data.shown === 2,
  `${page.data?.items?.length} of ${page.data?.total}`);
const next = await as('harness.dev', 'GET', '/api/changes?limit=2&offset=2');
check('offset reads the next page, newest first throughout',
  next.data?.items?.length === 2 && page.data.items[0].number > page.data.items[1].number
    && page.data.items[1].number > next.data.items[0].number,
  JSON.stringify([...(page.data?.items ?? []), ...(next.data?.items ?? [])].map((c) => c.number)));
const whole = await as('harness.dev', 'GET', '/api/changes');
check('without limit the list is whole, as before', whole.data?.items?.length === 4 && whole.data.total === 4);

// ── what the answers cost to read ────────────────────────────────────

const T0 = (() => { const d = new Date(Date.now() - 86_400_000); d.setUTCHours(9, 0, 0, 0); return d.getTime(); })();
const at = (minutes) => new Date(T0 + minutes * 60_000).toISOString().replace(/\.\d+Z$/, 'Z');
const events = [{ at: at(0), kind: 'prompt' }];
for (let i = 1; i <= 6; i += 1) events.push({ at: at(i), kind: 'tool', tool: 'Read', ok: true, ms: 10, bytes: 1000 });
events.push({ at: at(7), kind: 'tool', tool: 'mcp__adam__adam_draft_change', ok: true, ms: 50, bytes: 3000 });
events.push({ at: at(8), kind: 'tool', tool: 'mcp__adam__adam_changes', ok: true, ms: 50 });
const sent = await as('harness.dev', 'POST', '/api/agent/flush', {
  key: 'sess-bytes', project_id: 'ticvai', started_at: at(0), ended_at: at(9), events,
});
check('a session with answer lengths is taken', sent.status === 200 && sent.data.events === 9, `${sent.status} ${JSON.stringify(sent.data)}`);
const usage = await as('harness.dev', 'GET', '/api/agent/usage');
const tool = (name) => (usage.data?.tools ?? []).find((t) => t.tool === name) ?? {};
check('**the lengths are added up per tool, over the calls that were measured**',
  tool('Read').bytes === 6000 && tool('Read').measured === 6 && tool('mcp__adam__adam_draft_change').bytes === 3000,
  JSON.stringify([tool('Read'), tool('mcp__adam__adam_draft_change')]).slice(0, 200));
check('a call sent with no length is not measured, rather than counted as nothing',
  tool('mcp__adam__adam_changes').measured === 0 && tool('mcp__adam__adam_changes').calls === 1);
check('**the draft is counted at its depth in the session**',
  usage.data?.drafting?.drafts === 1 && usage.data.drafting.medianDepth === 7, JSON.stringify(usage.data?.drafting));
const one = await as('harness.dev', 'GET', `/api/agent/sessions/${sent.data?.session}`);
check("and a session's events carry their lengths", one.data?.events?.find((e) => e.tool === 'Read')?.bytes === 1000);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
