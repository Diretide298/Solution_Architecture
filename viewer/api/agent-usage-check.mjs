// What the agent did, and what this refuses to be told.
//
// Two things worth testing, and the second is the one that will matter in a
// year:
//
//   **Active time is not wall clock.** A session left open over lunch is not
//   two hours of agent use, and a number that says it is will end up in a
//   report. Gaps longer than the idle threshold are not counted.
//
//   **The service decides what it keeps, not the hook.** The hook is a file on
//   somebody's laptop that anybody can edit, so the narrowness has to be
//   enforced here or it is not enforced. Sending a prompt, a diff or an
//   invented error word must not widen the table.
//
//   TICVAI_DB=/tmp/agent.db python -m uvicorn api.main:app --port 8799
//   API=http://localhost:8799 node api/agent-usage-check.mjs

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
  const took = await as(handle, 'POST', '/api/auth/redeem',
    { token, password: PASSWORD, name: handle });
  return took.status === 200 ? { ok: true } : { ok: false, why: `redeem: ${took.status}` };
}

// Two days ago at nine, not a fixed date. This was 20 September, which fell out
// of the default fortnight on 4 October and failed seven checks for a reason
// that had nothing to do with the code: the window is "the last 14 days" of
// the real clock, so the sessions have to be recent on the real clock too.
const T0 = (() => { const d = new Date(Date.now() - 2 * 86_400_000); d.setUTCHours(9, 0, 0, 0); return d.getTime(); })();
const at = (minutes) => new Date(T0 + minutes * 60_000).toISOString().replace(/\.\d+Z$/, 'Z');

// ── the cast ─────────────────────────────────────────────────────────

const boot = await as('boss', 'POST', '/api/auth/bootstrap', {
  email: 'harness.boss@softlabsgroup.com', name: 'Harness Boss', password: PASSWORD,
});
check('an admin exists', boot.status === 200, `${boot.status}`);
check('a developer is invited', (await recruit('harness.dev', 'dev')).ok);
check('and a second developer', (await recruit('harness.dev2', 'dev')).ok);
check('and a project manager, who oversees', (await recruit('harness.pm', 'pm')).ok);

// ── a session arrives ────────────────────────────────────────────────

const sent = await as('harness.dev', 'POST', '/api/agent/flush', {
  key: 'sess-aaa', project_id: 'ticvai', external_key: '6046',
  repo: 'ticvai-ai', host: 'dev-laptop', agent: 'claude-code',
  started_at: at(0), ended_at: at(70),
  events: [
    { at: at(0), kind: 'prompt' },
    { at: at(1), kind: 'tool', tool: 'Read', ok: true, ms: 400 },
    { at: at(2), kind: 'tool', tool: 'Edit', ok: true, ms: 1200 },
    { at: at(3), kind: 'tool', tool: 'Bash', ok: false, error_kind: 'timeout', ms: 30_000 },
    { at: at(4), kind: 'tool', tool: 'Edit', ok: false, error_kind: 'not-found', ms: 300 },
    // Lunch. An hour of nothing, which is not an hour of agent use.
    { at: at(64), kind: 'tool', tool: 'Read', ok: true, ms: 500 },
    { at: at(65), kind: 'stop' },
  ],
});
check('a finished session is accepted', sent.status === 200,
  `${sent.status} ${JSON.stringify(sent.data?.detail ?? '')}`);
check('and every event kept', sent.data?.events === 7, String(sent.data?.events));

// Four one-minute gaps plus the durations, and the hour is not in it.
check('active time skips the hour nobody was there',
  sent.data?.activeMs > 4 * 60_000 && sent.data?.activeMs < 10 * 60_000,
  `${Math.round((sent.data?.activeMs ?? 0) / 1000)}s of a 65 minute session`);

// ── flushing twice is one session ────────────────────────────────────

const again = await as('harness.dev', 'POST', '/api/agent/flush', {
  key: 'sess-aaa', project_id: 'ticvai', external_key: '6046',
  started_at: at(0), ended_at: at(70),
  events: [{ at: at(1), kind: 'tool', tool: 'Read', ok: true, ms: 400 }],
});
check('a second flush of the same session updates rather than doubling',
  again.status === 200 && again.data?.session === sent.data?.session,
  `${again.data?.session} vs ${sent.data?.session}`);
const afterRetry = await as('harness.dev', 'GET', '/api/agent/sessions/' + sent.data.session);
check('and replaces its events rather than appending them',
  (afterRetry.data?.events ?? []).length === 1,
  String((afterRetry.data?.events ?? []).length));

// Put the real one back for the rest of the file.
await as('harness.dev', 'POST', '/api/agent/flush', {
  key: 'sess-aaa', project_id: 'ticvai', external_key: '6046',
  repo: 'ticvai-ai', host: 'dev-laptop', agent: 'claude-code',
  started_at: at(0), ended_at: at(70),
  events: [
    { at: at(0), kind: 'prompt' },
    { at: at(1), kind: 'tool', tool: 'Read', ok: true, ms: 400 },
    { at: at(2), kind: 'tool', tool: 'Edit', ok: true, ms: 1200 },
    { at: at(3), kind: 'tool', tool: 'Bash', ok: false, error_kind: 'timeout', ms: 30_000 },
    { at: at(4), kind: 'tool', tool: 'Edit', ok: false, error_kind: 'not-found', ms: 300 },
    { at: at(64), kind: 'tool', tool: 'Read', ok: true, ms: 500 },
    { at: at(65), kind: 'stop' },
  ],
});
await as('harness.dev2', 'POST', '/api/agent/flush', {
  key: 'sess-bbb', project_id: 'ticvai', external_key: '6050',
  repo: 'ticvai-ai', agent: 'claude-code', started_at: at(120), ended_at: at(140),
  events: [
    { at: at(120), kind: 'tool', tool: 'Edit', ok: false, error_kind: 'conflict', ms: 900 },
    { at: at(121), kind: 'tool', tool: 'Edit', ok: true, ms: 800 },
  ],
});

// ── the narrowness is the service's, not the hook's ──────────────────
//
// The hook is a file on a laptop. If the rule lived only there, one edited copy
// would put prompts in the database for everybody.

const nosy = await as('harness.dev', 'POST', '/api/agent/flush', {
  key: 'sess-ccc', project_id: 'ticvai', started_at: at(200), ended_at: at(201),
  events: [{
    at: at(200), kind: 'tool', tool: 'Bash', ok: false,
    error_kind: 'sk-ant-secret-leaked-in-an-error-message',
    // Fields the service has never heard of, sent anyway.
    prompt: 'here is the production database password',
    command: 'psql -h prod -U admin',
    diff: '--- a/secrets.env\n+++ b/secrets.env',
    ms: 100,
  }],
});
check('an unknown error word is not stored as sent', nosy.status === 200, `${nosy.status}`);
const stored = await as('harness.dev', 'GET', `/api/agent/sessions/${nosy.data.session}`);
const only = stored.data?.events?.[0] ?? {};
check('it becomes the one word the service knows',
  only.why === 'error', String(only.why));
check('and nothing else survives the trip',
  JSON.stringify(Object.keys(only).sort()) === JSON.stringify(['at', 'kind', 'ms', 'ok', 'tool', 'why']),
  Object.keys(only).sort().join(' '));
check('no prompt, no command, no diff anywhere in the answer',
  !/production database password|psql|secrets\.env/.test(JSON.stringify(stored.data)),
  'checked the whole payload');

const madeUp = await as('harness.dev', 'POST', '/api/agent/flush', {
  key: 'sess-ddd', project_id: 'ticvai', started_at: at(300), ended_at: at(301),
  events: [{ at: at(300), kind: 'whatever-i-like', tool: 'Read', ok: true, ms: 10 }],
});
const kinds = await as('harness.dev', 'GET', `/api/agent/sessions/${madeUp.data.session}`);
check('an invented event kind lands as a known one',
  kinds.data?.events?.[0]?.kind === 'tool', kinds.data?.events?.[0]?.kind);

// ── reading it ───────────────────────────────────────────────────────

const usage = await as('boss', 'GET', '/api/agent/usage');
check('an administrator sees the whole project', usage.data?.whole === true);
check('grouped by person', (usage.data?.people ?? []).length === 2,
  String((usage.data?.people ?? []).length));

const tools = usage.data?.tools ?? [];
const edit = tools.find((t) => t.tool === 'Edit');
check('and by tool, with the failures counted',
  edit?.calls === 4 && edit?.failed === 2, JSON.stringify(edit ?? null));
check('the failures say what kind, which is the point of collecting them',
  edit && edit.why['not-found'] === 1 && edit.why.conflict === 1,
  JSON.stringify(edit?.why ?? null));
check('the worst duration is kept, because a slow tool is a different problem',
  tools.find((t) => t.tool === 'Bash')?.worstMs === 30_000,
  String(tools.find((t) => t.tool === 'Bash')?.worstMs));
check('and the broken tool is listed before the busy one',
  tools[0]?.tool === 'Edit', tools.map((t) => t.tool).join(' '));

const mine = await as('harness.dev', 'GET', '/api/agent/usage');
check('a developer sees their own and says so', mine.data?.whole === false);
check('and only their own', (mine.data?.people ?? []).length === 1
  && mine.data.people[0].name === 'harness.dev',
  (mine.data?.people ?? []).map((p) => p.name).join(' '));
check('their sessions are theirs alone',
  (mine.data?.sessions ?? []).every((s) => s.who === 'harness.dev'),
  [...new Set((mine.data?.sessions ?? []).map((s) => s.who))].join(' '));

const pm = await as('harness.pm', 'GET', '/api/agent/usage');
check('a project manager sees everybody, being the role that oversees',
  pm.data?.whole === true && (pm.data?.people ?? []).length === 2,
  `${pm.data?.whole} ${(pm.data?.people ?? []).length}`);

const peeking = await as('harness.dev2', 'GET', `/api/agent/sessions/${sent.data.session}`);
check('one developer cannot read another\'s session', peeking.status === 403,
  `${peeking.status}`);
const own = await as('harness.dev', 'GET', `/api/agent/sessions/${sent.data.session}`);
check('but can read their own, event by event',
  own.status === 200 && (own.data?.events ?? []).length === 7,
  `${own.status} ${(own.data?.events ?? []).length}`);
check('which names the ticket, so the time is attached to something',
  own.data?.ticket === '6046', own.data?.ticket);

// ── the counts are the window's, not the list's ──────────────────────
//
// The page's "sessions" figure used to be the length of a list capped at 100,
// while the per-person totals summed a read capped at 500, so the two
// disagreed past a hundred sessions and every total was quietly short past
// five hundred. Enough sessions to cross both caps, then the counts again.

check('a third developer is invited, who never runs the agent',
  (await recruit('harness.dev3', 'dev')).ok);
const MANY = 520;
for (let i = 0; i < MANY; i += 26) {
  await Promise.all(Array.from({ length: Math.min(26, MANY - i) }, (_, j) => {
    const n = i + j;
    return as('harness.dev2', 'POST', '/api/agent/flush', {
      key: `bulk-${n}`, project_id: 'ticvai', external_key: String(7000 + (n % 30)),
      started_at: at(400 + n), ended_at: at(400 + n),
      events: [{ at: at(400 + n), kind: 'tool', tool: 'Grep', ok: n % 10 !== 0,
        error_kind: n % 10 ? '' : 'not-found', ms: 50 }],
    });
  }));
}
const busy = await as('boss', 'GET', '/api/agent/usage');
const listed = busy.data?.sessions ?? [];
const second = (busy.data?.people ?? []).find((p) => p.name === 'harness.dev2');
check('the list is still capped, because nobody scrolls a quarter of sessions',
  listed.length === 100, String(listed.length));
check('but the true count comes with it',
  busy.data?.sessionCount === busy.data?.totals?.sessions && busy.data?.sessionCount > 500,
  `${busy.data?.sessionCount} counted, ${busy.data?.totals?.sessions} in the totals`);
check("and every person's sessions add up to it, past the old 500-row read",
  (busy.data?.people ?? []).reduce((n, p) => n + p.sessions, 0) === busy.data?.sessionCount,
  (busy.data?.people ?? []).map((p) => `${p.name} ${p.sessions}`).join(', '));
check("one developer's five hundred and twenty-one sessions are all counted",
  second?.sessions === MANY + 1, String(second?.sessions));
const grep = (busy.data?.tools ?? []).find((t) => t.tool === 'Grep');
check('and every one of their calls reaches the tool table',
  grep?.calls === MANY && grep?.failed === MANY / 10 && grep?.why['not-found'] === MANY / 10,
  JSON.stringify(grep ?? null));
check('their tickets are named, newest first, and counted whole',
  second?.tickets === 31 && second?.ticketKeys?.length === 12,
  `${second?.tickets} tickets, ${second?.ticketKeys?.length} named`);
check('the totals agree with the tools',
  busy.data?.totals?.calls === (busy.data?.tools ?? []).reduce((n, t) => n + t.calls, 0)
  && busy.data?.totals?.failed === (busy.data?.tools ?? []).reduce((n, t) => n + t.failed, 0),
  JSON.stringify(busy.data?.totals));
check('the developer who never ran it is named as not having used it',
  (busy.data?.quiet ?? []).includes('harness.dev3') && !(busy.data?.quiet ?? []).includes('harness.dev'),
  JSON.stringify(busy.data?.quiet));
check('out of everybody who could have',
  busy.data?.expected === 3, String(busy.data?.expected));

// ── one person, for somebody who oversees ────────────────────────────

const firstDev = (busy.data?.people ?? []).find((p) => p.name === 'harness.dev');
const narrowed = await as('harness.pm', 'GET', `/api/agent/usage?person=${firstDev?.id}`);
check('a pm can narrow the page to one person',
  narrowed.data?.person === firstDev?.id
  && (narrowed.data?.sessions ?? []).every((s) => s.who === 'harness.dev')
  && !(narrowed.data?.tools ?? []).some((t) => t.tool === 'Grep'),
  (narrowed.data?.tools ?? []).map((t) => t.tool).join(' '));
check('and the roster stays whole, so the picker can be changed back',
  (narrowed.data?.people ?? []).length === 2, String((narrowed.data?.people ?? []).length));
check("the narrowed totals are that person's",
  narrowed.data?.totals?.sessions === firstDev?.sessions, JSON.stringify(narrowed.data?.totals));
const widened = await as('harness.dev', 'GET', `/api/agent/usage?person=${second?.id}`);
check('a developer asking for somebody else still sees only themselves',
  widened.data?.whole === false && widened.data?.person === 0
  && (widened.data?.sessions ?? []).every((s) => s.who === 'harness.dev')
  && (widened.data?.quiet ?? []).length === 0,
  [...new Set((widened.data?.sessions ?? []).map((s) => s.who))].join(' '));
check('the session list carries where it ran and when it ended',
  listed.every((s) => 'host' in s && 'endedAt' in s && 'agent' in s), Object.keys(listed[0] ?? {}).join(' '));

// ── and somebody who was never there ─────────────────────────────────

const quiet = await as('harness.pm', 'GET', '/api/agent/usage?days=1');
check('a window with nothing in it is empty rather than wrong',
  (quiet.data?.people ?? []).length === 0 && (quiet.data?.tools ?? []).length === 0,
  `${(quiet.data?.people ?? []).length} people`);

const stranger = await fetch(`${API}/api/agent/usage`);
check('and a stranger is asked to sign in', stranger.status === 401, `${stranger.status}`);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
