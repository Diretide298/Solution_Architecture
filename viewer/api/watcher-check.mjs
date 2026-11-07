// The watcher's decision API (api/watcher.py, PHONE-SPEC.md section 2): the
// System Architect (the owner) decides on a phone what the change-request
// watcher drafted, the way he marks REVIEW.md by hand, and settles after seeing
// the dry run.
//
// What this spends its time on is what must NOT happen: a decision bound to a
// draft that has moved since it was read, a decision on a request with no
// draft, a settle of marks that changed after the preview, a phone's background
// token reading more than the counts, and anybody but the owner deciding (a
// Team Lead included, since 6 November 2026).
//
// Self-contained: it starts its own accounts service on a temporary store, a
// watcher folder built from a two-request fixture with the watcher's own
// render_review (so the REVIEW.md format is the real one, never restated here),
// and a stand-in `claude` for the ask-back turn. Settling runs the real
// `cr-watch.py settle` and settle_changes.py against this same service, on
// requests with no ticket, so OpenProject is never called (TICVAI_PMS_URL points
// at a closed port in case it ever were). No real credential is used.
//
//   node api/watcher-check.mjs            # from viewer/

import { spawn, spawnSync, execFileSync } from 'node:child_process';
import { chmodSync, mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync, existsSync, appendFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { createHash } from 'node:crypto';
import { request as httpRequest } from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const VIEWER = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = path.resolve(VIEWER, '..', 'ticvai', 'tools', 'cr-watch.py');
const PORT = 8891, BARE_PORT = 8892, VIEWER_PORT = 8893;
const API = `http://127.0.0.1:${PORT}`;
const BARE = `http://127.0.0.1:${BARE_PORT}`;
const VIEWER_URL = `http://127.0.0.1:${VIEWER_PORT}`;
const PREVIEW_EVERY = 4;   // seconds between one account's settle previews, shortened from 10 for the check
const T = mkdtempSync(path.join(tmpdir(), 'watcher-check-'));
const STORE = path.join(T, 'check.db');
const OUT = path.join(T, 'out');
const RELEASE = path.join(T, 'release');
const ENV_FILE = path.join(T, 'cr-watch.env');
const PASSWORD = 'a-long-enough-passphrase';
mkdirSync(OUT, { recursive: true });
mkdirSync(RELEASE, { recursive: true });

let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

// ── a stand-in for Claude Code ───────────────────────────────────────
//
// It writes down what it was started with (its arguments, the names of its
// environment variables, its prompt) and answers the way `claude -p
// --output-format json` does, cost included.
const CALLS = path.join(T, 'claude-calls.jsonl');
const FAKE = path.join(T, 'fake-claude.mjs');
writeFileSync(FAKE, `#!/usr/bin/env node
import { appendFileSync, readFileSync } from 'node:fs';
const prompt = readFileSync(0, 'utf8');
appendFileSync(${JSON.stringify(CALLS)}, JSON.stringify({ argv: process.argv.slice(2), env: Object.keys(process.env), prompt }) + '\\n');
const result = 'Because the contract says so (contracts/orders.yaml:12).\\n\`\`\`json\\n'
  + JSON.stringify({ resolution: 'Decided (Chinmay, 4 November 2026): use the queue. Build now: the queue.', status: 'done' })
  + '\\n\`\`\`';
process.stdout.write(JSON.stringify({ type: 'result', is_error: false, result, total_cost_usd: 0.42 }));
`);
let CLAUDE = FAKE;
if (process.platform === 'win32') {
  CLAUDE = path.join(T, 'fake-claude.cmd');
  writeFileSync(CLAUDE, `@node "${FAKE}" %*\r\n`);
} else {
  chmodSync(FAKE, 0o755);
}

// ── the fixture, written by the watcher's own code ───────────────────
const HELPER = path.join(T, 'fixture.py');
writeFileSync(HELPER, `
import importlib.util, json, sqlite3, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("cr_watch", ${JSON.stringify(SCRIPT)})
cw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cw)
out = Path(${JSON.stringify(OUT)})
mode = sys.argv[1]
if mode == "build":
    pending = {}
    for i, (ref, blocking, needs) in enumerate(json.loads(sys.argv[2]), 1):
        row = {"id": i, "ref": ref, "raised": f"2026-11-04T0{i}:00:00Z", "project": "ticvai", "status": "Open",
               "blocking": "yes" if blocking else "", "kind": "Operation", "artefact": f"orders#op{i}",
               "title": f"Harness request {i}", "raised by": "Harness Dev", "ticket": "", "problem": "p",
               "evidence": "", "options": "", "recommendation": ""}
        p = cw._item(row)
        d = {"verdict": "NOT FIXED", "class": "Harness class", "recommendation": f"Option A for {ref}",
             "resolution": f"Decided (Chinmay, 4 November 2026): harness {i}. Build now: x{i}.", "needs": needs,
             "misread": "nothing", "question": "", "new_ticket": None}
        p.update(facts={"class_name": "Harness class"}, facts_lines=["Ticket #none"], draft=d,
                 drafted_at=f"2026-11-04T1{i}:00:00Z", status="done", ref_to="", resolution=d["resolution"])
        pending[ref] = p
        (out / "drafts").mkdir(parents=True, exist_ok=True)
        cw._draft_file(out, p, f"The agent's full answer for {ref}.")
    state = {"project": "ticvai", "last_id": 2, "pending": pending, "last_run_at": "2026-11-04T13:23:10Z",
             "last_error": "", "paused": "", "daily_cap_usd": 50.0, "release": "r14", "next": "r15"}
    cw.save_state(out, state)
    cw._write(out / "REVIEW.md", cw.render_review(pending, "Last run 2026-11-04T13:23:10Z: harness."))
elif mode == "redraft":
    # what a run does when it drafts a request again: the lead's marks taken in, a new draft, REVIEW.md rendered
    ref = sys.argv[2]
    state = cw.load_state(out)
    cw.absorb_marks(state["pending"], cw.parse_review((out / "REVIEW.md").read_text(encoding="utf-8")))
    p = state["pending"][ref]
    p.update(draft=dict(p["draft"], verdict="FIXED IN R14", resolution="Decided: redrafted. Build now: y."),
             resolution="Decided: redrafted. Build now: y.", decision="", drafted_at="2026-11-04T15:00:00Z")
    cw.save_state(out, state)
    cw._write(out / "REVIEW.md", cw.render_review(state["pending"], "Last run: redrafted."))
elif mode == "marks":
    print(json.dumps(cw.parse_review((out / "REVIEW.md").read_text(encoding="utf-8"))))
elif mode == "state":
    print(json.dumps(cw.load_state(out)))
elif mode == "sql":
    con = sqlite3.connect(sys.argv[2])
    con.row_factory = sqlite3.Row
    print(json.dumps([dict(r) for r in con.execute(sys.argv[3]).fetchall()]))
elif mode == "sqlw":
    con = sqlite3.connect(sys.argv[2])
    con.execute(sys.argv[3], json.loads(sys.argv[4]) if len(sys.argv) > 4 else [])
    con.commit()
    print("null")
elif mode == "digest":
    # the watcher's own digest of a request's mark as REVIEW.md holds it now
    print(json.dumps(cw.mark_digest(cw.parse_review((out / "REVIEW.md").read_text(encoding="utf-8")).get(sys.argv[2]))))
elif mode == "poison":
    # what a failed draft or a failed read could carry back: the env file's values, encoded, and token-shaped strings
    state = cw.load_state(out)
    state["pending"][sys.argv[2]]["draft_error"] = sys.argv[3]
    state["pending"][sys.argv[2]]["draft_reason"] = sys.argv[3]
    state["last_error"] = sys.argv[4]
    state["paused"] = "Drafting failed: " + sys.argv[4]
    cw.save_state(out, state)
elif mode == "unpoison":
    state = cw.load_state(out)
    for p in state["pending"].values():
        p["draft_error"] = p["draft_reason"] = ""
    state["last_error"] = state["paused"] = ""
    cw.save_state(out, state)
elif mode == "addfailed":
    # requests whose drafting failed on the server (6 November 2026: an invalid API key), with no draft
    state = cw.load_state(out)
    for i, ref in enumerate(json.loads(sys.argv[2]), 1):
        row = {"id": 7000 + i, "ref": ref, "raised": f"2026-11-06T0{i}:00:00Z", "project": "ticvai", "status": "Open",
               "blocking": "yes", "kind": "Operation", "artefact": f"orders#f{i}", "title": f"Undrafted request {i}",
               "raised by": "Harness Dev", "ticket": "31567", "problem": f"The developer's own words {i}.",
               "evidence": "the log", "options": "A or B", "recommendation": "A"}
        p = cw._item(row)
        reason = "claude reported an error (exit 1): Invalid API key · Please run /login"
        p.update(facts={"class_name": ""}, facts_lines=["Ticket #31567"], draft_tries=2, draft_reason=reason,
                 draft_error=f"draft failed twice: draft it again from Decide ({reason})")
        state["pending"][ref] = p
        cw._draft_file(out, p, "")
    state["paused"] = "Drafting is held: 2 requests failed 2 times (" + reason + ")."
    cw.save_state(out, state)
    cw._write(out / "REVIEW.md", cw.render_review(state["pending"], "Last run: failed."))
elif mode == "running":
    # a run drafting now: its start in state.json, and the run lock held by a live process (argv 2), or neither
    state = cw.load_state(out)
    state["running_since"] = sys.argv[3] if len(sys.argv) > 3 else ""
    cw.save_state(out, state)
    lock = out / "cr-watch.lock"
    if sys.argv[2] == "0":
        lock.unlink(missing_ok=True) if sys.version_info >= (3, 8) else None
    else:
        lock.write_text(f"pid {sys.argv[2]} thread 1 since {state['running_since']}", encoding="utf-8")
    print("null")
`);
const py = (...args) => JSON.parse(execFileSync('python', [HELPER, ...args], { encoding: 'utf8' }) || 'null');
const marks = () => py('marks');
const sql = (q) => py('sql', STORE, q);
const reviewText = () => readFileSync(path.join(OUT, 'REVIEW.md'), 'utf8');

// ── the services ─────────────────────────────────────────────────────
const key = spawnSync('python', ['-c', 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'],
  { encoding: 'utf8' }).stdout.trim();
const env = { ...process.env, TICVAI_DB: STORE, TICVAI_SECRET_KEY: key, PYTHONUNBUFFERED: '1' };
// Nothing of the machine's own: no real login, token or watcher folder reaches the service or its children.
for (const k of Object.keys(env)) {
  if (/^(ADAM_|TICVAI_OP|CR_WATCH_|ANTHROPIC_)/.test(k)) delete env[k];
}
const watcherEnv = {
  CR_WATCH_OUT: OUT, CR_WATCH_RELEASE_DIR: RELEASE, CR_WATCH_ENV_FILE: ENV_FILE, CR_WATCH_CLAUDE: CLAUDE,
  CR_WATCH_SCRIPT: SCRIPT, CR_WATCH_FETCH: '0', ADAM_API_URL: API, TICVAI_PMS_URL: 'http://127.0.0.1:9',
  CR_WATCH_PREVIEW_EVERY: String(PREVIEW_EVERY),
};
const children = [];
function start(port, extra, argv = ['-m', 'uvicorn', 'api.main:app', '--host', '127.0.0.1', '--port', String(port)],
  cmd = 'python') {
  const child = spawn(cmd, argv, { cwd: VIEWER, env: { ...env, ...extra }, windowsHide: true });
  let log = '';
  child.stdout.on('data', (c) => { log += c; });
  child.stderr.on('data', (c) => { log += c; });
  child.log = () => log;
  children.push(child);
  return child;
}
async function up(base, child, probe = '/api/auth/me', tries = 120) {
  for (let i = 0; i < tries; i++) {
    try { const r = await fetch(`${base}${probe}`); if (r.status < 500) return true; } catch {}
    if (child.exitCode !== null) break;
    await new Promise((r) => setTimeout(r, 250));
  }
  console.log(child.log());
  return false;
}
function stopAll() {
  for (const c of children) {
    if (c.exitCode !== null) continue;
    if (process.platform === 'win32') spawnSync('taskkill', ['/pid', String(c.pid), '/T', '/F'], { windowsHide: true });
    else c.kill();
  }
}

// One after the other: two services making the same new store at once lock each other out.
const main = start(PORT, watcherEnv);
const mainUp = await up(API, main);
const bare = start(BARE_PORT, {});
// The viewer in front of it, for its own cap on what it forwards to the watcher's routes.
const viewer = start(VIEWER_PORT, { TICVAI_AUTH: API },
  ['server.mjs', '--port', String(VIEWER_PORT), '--host', '127.0.0.1'], process.execPath);
try {
  if (!mainUp || !(await up(BARE, bare)) || !(await up(VIEWER_URL, viewer, '/login.html', 480))) {
    check('the services start', false);
  } else {
    await run();
  }
} catch (e) {
  check('the check ran to the end', false, e.stack);
} finally {
  stopAll();
  try { rmSync(T, { recursive: true, force: true }); } catch {}
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);

async function run() {
  const OWNER = 'harness.chief';          // the System Architect: the one who decides
  const OTHER_OWNER = 'harness.boss';
  const jars = new Map();
  async function as(who, method, p, body, { base = API, bearer } = {}) {
    const cookie = who ? jars.get(who) : '';
    const go = () => fetch(`${base}${p}`, {
      method,
      headers: {
        'content-type': 'application/json',
        ...(cookie ? { cookie } : {}),
        ...(bearer ? { authorization: `Bearer ${bearer}` } : {}),
      },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    let res;
    try {
      res = await go();
    } catch (e) {
      // A kept-alive socket the service closed while this process was busy in a helper: the request never reached
      // it, so it is sent once more on a new one.
      if (!['UND_ERR_SOCKET', 'ECONNRESET'].includes(e.cause?.code)) throw e;
      res = await go();
    }
    const set = res.headers.get('set-cookie');
    if (set && who) jars.set(who, set.split(';')[0]);
    let data = null;
    try { data = await res.json(); } catch {}
    return { status: res.status, data };
  }
  const detail = (r) => `${r.status} ${JSON.stringify(r.data?.detail ?? '')}`;
  const plain = (r) => typeof r.data?.detail === 'string' && /^[A-Z].*[.?]$/.test(r.data.detail);

  async function recruit(handle, role) {
    const email = `${handle}@softlabsgroup.com`;
    const made = await as('admin', 'POST', '/api/invites', { email, role });
    if (made.status !== 200) return `invite ${detail(made)}`;
    const token = (made.data.url ?? made.data.link ?? '').split('#')[1];
    const took = await as(handle, 'POST', '/api/auth/redeem', { token, password: PASSWORD, name: handle });
    return took.status === 200 ? '' : `redeem ${detail(took)}`;
  }

  // ── accounts ─────────────────────────────────────────────────────
  const boot = await as('admin', 'POST', '/api/auth/bootstrap',
    { email: 'harness.admin@softlabsgroup.com', name: 'Harness Admin', password: PASSWORD });
  check('an admin exists', boot.status === 200, detail(boot));
  for (const [who, role] of [['harness.lead', 'lead'], ['harness.dev', 'dev'], [OWNER, 'admin'], [OTHER_OWNER, 'admin']]) {
    const why = await recruit(who, role);
    check(`a ${role} is invited`, !why, why);
  }
  // Two System Architects: the one who decides, and a second for the one-settle-at-a-time check.
  const cli = (...args) => execFileSync('python', ['-m', 'api.cli', ...args],
    { cwd: VIEWER, env: { ...env, TICVAI_DB: STORE }, encoding: 'utf8' });
  const said = cli('owner', 'harness.chief@softlabsgroup.com');
  check('the CLI makes the owner', /System Architect/.test(said), said.trim());
  cli('owner', 'harness.boss@softlabsgroup.com');
  // Settling logs in to this service as the owner, from the env file the watcher reads (never printed).
  writeFileSync(ENV_FILE, [
    'ADAM_EMAIL=harness.chief@softlabsgroup.com', `ADAM_PASSWORD=${PASSWORD}`,
    'TICVAI_OP_TOKEN=harness-not-a-token', 'ANTHROPIC_API_KEY=harness-not-a-key', '',
  ].join('\n'));

  // ── two change requests in ADAM, and the watcher's folder for them ─
  const refs = [];
  for (const [title, blocking] of [['Harness request one, blocking', true], ['Harness request two', false]]) {
    const r = await as('admin', 'POST', '/api/changes', {
      target_kind: 'operation', target_id: 'POST /orders', title, blocking,
      problem: 'Raised by the watcher check so there is something to settle.', options: ['A', 'B'],
    });
    check(`${title} is filed`, r.status === 200, detail(r));
    refs.push(r.data?.change?.id);
  }
  const [A, B] = refs;
  py('build', JSON.stringify([[A, true, 'lead'], [B, false, 'client']]));
  check('the fixture has two blocks', Object.keys(marks()).length === 2, JSON.stringify(Object.keys(marks())));

  // ── who may ask ──────────────────────────────────────────────────
  const anon = await as(null, 'GET', '/api/watcher/summary');
  check('a stranger is refused the summary', anon.status === 401, detail(anon));
  const routes = [
    ['GET', '/api/watcher/summary'], ['GET', '/api/watcher/requests'], ['GET', `/api/watcher/requests/${A}`],
    ['POST', `/api/watcher/requests/${A}/decision`, { decision: 'approve', draft_hash: 'x', expected_mark: 'x' }],
    ['DELETE', `/api/watcher/requests/${A}/decision`, { draft_hash: 'x', expected_mark: 'x' }],
    ['POST', `/api/watcher/requests/${A}/ask`, { question: 'Why?' }],
    ['POST', '/api/watcher/settle/preview', {}], ['POST', '/api/watcher/settle/apply', { fingerprint: 'f'.repeat(32) }],
    ['POST', '/api/watcher/device-token', { device: 'Pixel 8' }],
    ['POST', `/api/watcher/requests/${A}/redraft`, {}], ['POST', '/api/watcher/redraft', { all_failed: true }],
    ['GET', '/api/watcher/history'], ['GET', '/api/watcher/health'], ['GET', '/api/watcher/device-tokens'],
    ['DELETE', '/api/watcher/device-token/1'],
  ];
  for (const [who, name] of [['harness.lead', 'Team Lead'], ['harness.dev', 'dev'], ['admin', 'admin']]) {
    const got = [];
    for (const [m, p, b] of routes) got.push((await as(who, m, p, b)).status);
    check(`a ${name} is refused every watcher route, the device-token routes too (403)`, got.every((s) => s === 403),
      got.join(','));
  }
  const leadSaid = await as('harness.lead', 'GET', '/api/watcher/requests');
  check('the Team Lead is told only the System Architect decides',
    /^Only the System Architect can decide change requests\.$/.test(leadSaid.data?.detail ?? ''), detail(leadSaid));
  // A phone token a Team Lead made while a lead could still decide reads nothing now.
  const oldLeadToken = 'harness-lead-phone-token-made-before-6-november';
  const leadRow = sql("SELECT id FROM account WHERE email = 'harness.lead@softlabsgroup.com'")[0]?.id;
  py('sqlw', STORE, 'INSERT INTO watcher_device (account_id, device, token_hash, made_at) VALUES (?, ?, ?, ?)',
    JSON.stringify([leadRow, 'Lead phone', createHash('sha256').update(oldLeadToken).digest('hex'),
      new Date().toISOString().replace(/\.\d+Z$/, '+00:00')]));
  const oldLead = await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: oldLeadToken });
  check('a device token a Team Lead made earlier reads nothing (401)', oldLead.status === 401, detail(oldLead));
  const devSaid = await as('harness.dev', 'GET', '/api/watcher/summary');
  check('the refusal is a plain sentence', plain(devSaid), JSON.stringify(devSaid.data?.detail));
  check('the reviews were not touched by the refusals', marks()[A].decision === '', JSON.stringify(marks()[A]));
  const ownerSum = await as('harness.chief', 'GET', '/api/watcher/summary');
  check('the owner may read the summary', ownerSum.status === 200, detail(ownerSum));

  // ── not set up ───────────────────────────────────────────────────
  await as(OWNER, 'GET', '/api/auth/me');
  const notSet = await fetch(`${BARE}/api/watcher/summary`, { headers: { cookie: jars.get(OWNER) } });
  const notSetBody = await notSet.json().catch(() => ({}));
  check('with no CR_WATCH_OUT the routes answer 503', notSet.status === 503, `${notSet.status}`);
  check('and say the watcher is not set up', /The watcher is not set up on this server/.test(notSetBody.detail ?? ''),
    notSetBody.detail ?? '');

  // ── the summary ──────────────────────────────────────────────────
  const sum = await as(OWNER, 'GET', '/api/watcher/summary');
  const s = sum.data ?? {};
  check('the owner reads the summary', sum.status === 200, detail(sum));
  const keys = ['waiting', 'blocking', 'needs_lead', 'needs_client', 'new', 'last_run_at', 'last_error', 'paused',
    'spend_today_usd', 'daily_cap_usd', 'decided'];
  check('it has the contract\'s fields', keys.every((k) => k in s), Object.keys(s).join(','));
  check('the counts are the fixture\'s', s.waiting === 2 && s.blocking === 1 && s.needs_lead === 1
    && s.needs_client === 1 && s.decided === 0, JSON.stringify(s));
  check('the run and the cap are the state\'s', s.last_run_at === '2026-11-04T13:23:10Z' && s.daily_cap_usd === 50
    && s.last_error === '' && s.paused === '' && s.spend_today_usd === 0, JSON.stringify(s));
  const n0 = s.new ?? [];
  check('with no since, new holds every waiting request', n0.length === 2, JSON.stringify(n0));
  const one = n0.find((x) => x.cr === A) ?? {};
  check('a new entry has the contract\'s shape', one.title === 'Harness request 1' && one.blocking === true
    && one.needs === 'lead' && one.raised_at === '2026-11-04T01:00:00Z', JSON.stringify(one));
  const since = await as(OWNER, 'GET', '/api/watcher/summary?since=2026-11-04T11:30:00Z');
  check('new holds what was drafted after since', JSON.stringify((since.data?.new ?? []).map((x) => x.cr)) === JSON.stringify([B]),
    JSON.stringify(since.data?.new));
  const badSince = await as(OWNER, 'GET', '/api/watcher/summary?since=yesterday');
  check('a since that is not a time is refused', badSince.status === 400 && plain(badSince), detail(badSince));

  // ── the list and one request ─────────────────────────────────────
  const list = await as(OWNER, 'GET', '/api/watcher/requests');
  const items = list.data?.items ?? [];
  check('the list answers', list.status === 200 && items.length === 2, detail(list));
  check('in REVIEW.md\'s order, blocking first', items[0]?.cr === A, items.map((x) => x.cr).join(','));
  const row = items[0] ?? {};
  check('a row has the table\'s fields', row.title === 'Harness request 1' && row.verdict === 'NOT FIXED'
    && row.class === 'Harness class' && row.blocking === true && row.needs === 'lead' && row.decision === ''
    && row.ticket === '' && row.developer === 'Harness Dev' && row.raised_at === '2026-11-04T01:00:00Z',
    JSON.stringify(row));
  check('a row says what approving it as drafted would settle', row.settle_status === 'done' && row.settle_ref === '',
    JSON.stringify({ settle_status: row.settle_status, settle_ref: row.settle_ref }));
  const got = await as(OWNER, 'GET', `/api/watcher/requests/${A}`);
  const g = got.data ?? {};
  check('one request answers', got.status === 200, detail(got));
  check('with its draft', g.draft?.recommendation === `Option A for ${A}` && /Build now: x1/.test(g.draft?.resolution ?? '')
    && g.draft?.misread === 'nothing' && Array.isArray(g.draft?.facts) && /full answer/.test(g.draft?.answer ?? ''),
    JSON.stringify(g.draft));
  check('its draft hash is REVIEW.md\'s', /^[0-9a-f]{12}$/.test(g.draft_hash ?? '') && g.draft_hash === marks()[A].draft_hash,
    `${g.draft_hash} vs ${marks()[A].draft_hash}`);
  check('one request says it too', got.data?.settle_status === 'done' && got.data?.settle_ref === '',
    JSON.stringify({ settle_status: got.data?.settle_status, settle_ref: got.data?.settle_ref }));
  check('its mark and an empty thread', g.mark?.decision === '' && Array.isArray(g.thread) && g.thread.length === 0,
    JSON.stringify({ mark: g.mark, thread: g.thread }));
  const missing = await as(OWNER, 'GET', '/api/watcher/requests/CR-999');
  check('a request the watcher does not hold is 404', missing.status === 404 && plain(missing), detail(missing));
  const junk = await as(OWNER, 'GET', '/api/watcher/requests/XYZ');
  check('a number that is not one is 400', junk.status === 400 && plain(junk), detail(junk));
  const arabic = await as(OWNER, 'GET', `/api/watcher/requests/${encodeURIComponent('CR-\u0661\u0662')}`);
  check('a number in other digits is not one (ASCII digits only)', arabic.status === 400, detail(arabic));
  check('one request carries the digest of its mark, the watcher\'s own', /^[0-9a-f]{16}$/.test(g.mark_digest ?? '')
    && g.mark_digest === py('digest', A) && row.mark_digest === g.mark_digest, `${g.mark_digest} ${py('digest', A)}`);

  // ── what no answer may carry (security review, L3) ───────────────
  const b64 = (x) => Buffer.from(x, 'utf8').toString('base64');
  const secretForms = [b64(PASSWORD), b64(PASSWORD).replace(/=+$/, ''), encodeURIComponent(PASSWORD),
    b64(`harness.chief@softlabsgroup.com:${PASSWORD}`), b64('apikey:harness-not-a-token'),
    'sk-ant-api03-abcdefghijklmnopqrstuvwxyz', 'a1b2c3d4e5f6a7b8c9d0a1b2c3d4e5f6a7b8c9d0a1b2c3d4e5f6a7b8c9d0a1b2'];
  py('poison', A, `claude exited 1: ${secretForms.slice(0, 3).join(' ')} ${secretForms[5]}`,
    `ADAM could not be read (Authorization: Basic ${secretForms[3]}; op ${secretForms[4]}; ${secretForms[6]})`);
  const poisoned = JSON.stringify([(await as(OWNER, 'GET', '/api/watcher/requests')).data,
    (await as(OWNER, 'GET', `/api/watcher/requests/${A}`)).data,
    (await as(OWNER, 'GET', '/api/watcher/summary')).data]);
  const leaked = secretForms.filter((x) => poisoned.includes(x));
  check('a draft error and a run error carry no credential: plain, base64, URL-encoded or token-shaped',
    leaked.length === 0 && /\[hidden\]/.test(poisoned), leaked.map((x) => x.slice(0, 6)).join(','));
  py('unpoison');

  // ── deciding ─────────────────────────────────────────────────────
  const hashA = g.draft_hash;
  const markA0 = g.mark_digest;
  const before = reviewText();
  const wrong = await as(OWNER, 'POST', `/api/watcher/requests/${A}/decision`,
    { decision: 'approve', draft_hash: '000000000000', expected_mark: markA0 });
  check('a decision on another draft is refused 409', wrong.status === 409 && plain(wrong)
    && wrong.data?.reason === 'draft-moved', `${detail(wrong)} ${wrong.data?.reason}`);
  check('and REVIEW.md is untouched', reviewText() === before);
  const noMark = await as(OWNER, 'POST', `/api/watcher/requests/${A}/decision`,
    { decision: 'approve', draft_hash: hashA });
  check('a decision that does not say which mark it was made over is refused 409', noMark.status === 409
    && noMark.data?.reason === 'mark-moved' && reviewText() === before, `${detail(noMark)} ${noMark.data?.reason}`);
  const ok = await as(OWNER, 'POST', `/api/watcher/requests/${A}/decision`,
    { decision: 'approve', draft_hash: hashA, expected_mark: markA0 });
  check('the owner approves the draft they read', ok.status === 200 && ok.data?.mark?.decision === 'approve', detail(ok));
  let m = marks();
  check('REVIEW.md says approve on its decision line', m[A].decision === 'approve' && m[A].draft_hash === hashA
    && m[B].decision === '', JSON.stringify(m));
  check('the drafted resolution stays as it was', /Build now: x1/.test(m[A].resolution), m[A].resolution);
  const markA1 = ok.data?.mark_digest;
  check('the answer carries the new mark\'s digest', markA1 === py('digest', A) && markA1 !== markA0, `${markA1}`);
  const again = await as(OWNER, 'POST', `/api/watcher/requests/${A}/decision`,
    { decision: 'approve', draft_hash: hashA, expected_mark: markA0 });
  check('the same decision sent again (offline replay of itself) is answered as done and changes nothing',
    again.status === 200 && again.data?.unchanged === true && marks()[A].decision === 'approve', detail(again));
  const before2 = reviewText();
  const replay = await as(OWNER, 'POST', `/api/watcher/requests/${A}/decision`,
    { decision: 'reject', draft_hash: hashA, expected_mark: markA0, note: 'made offline before the approve' });
  check('a different decision made over the older mark (an offline replay after a newer mark) is refused 409',
    replay.status === 409 && plain(replay) && replay.data?.reason === 'mark-moved', `${detail(replay)} ${replay.data?.reason}`);
  check('and the newer mark stays', reviewText() === before2 && marks()[A].decision === 'approve');
  const backNoHash = await as(OWNER, 'DELETE', `/api/watcher/requests/${A}/decision`, { expected_mark: markA1 });
  check('a take-back without the draft hash is refused', backNoHash.status === 400 && marks()[A].decision === 'approve',
    detail(backNoHash));
  const backOld = await as(OWNER, 'DELETE', `/api/watcher/requests/${A}/decision`,
    { draft_hash: hashA, expected_mark: markA0 });
  check('a take-back made over an older mark is refused 409', backOld.status === 409 && backOld.data?.reason === 'mark-moved'
    && marks()[A].decision === 'approve', `${detail(backOld)} ${backOld.data?.reason}`);
  const back = await as(OWNER, 'DELETE', `/api/watcher/requests/${A}/decision`,
    { draft_hash: hashA, expected_mark: markA1 });
  check('the owner takes the approve back', back.status === 200 && back.data?.mark?.decision === '', detail(back));
  m = marks();
  check('REVIEW.md\'s decision line is empty again, the drafted lines as they were', m[A].decision === ''
    && /Build now: x1/.test(m[A].resolution) && m[A].status === 'done' && m[A].draft_hash === hashA, JSON.stringify(m[A]));
  const backAgain = await as(OWNER, 'DELETE', `/api/watcher/requests/${A}/decision`,
    { draft_hash: hashA, expected_mark: markA1 });
  check('taking back what is not marked changes nothing', backAgain.status === 200 && marks()[A].decision === '',
    detail(backAgain));
  const takeBacks = sql("SELECT cr, decision, draft_hash FROM watcher_event WHERE kind = 'take-back'");
  check('the take-back is in the audit trail, once', takeBacks.length === 1 && takeBacks[0].cr === A
    && takeBacks[0].decision === 'approve' && takeBacks[0].draft_hash === hashA, JSON.stringify(takeBacks));
  const reapprove = await as(OWNER, 'POST', `/api/watcher/requests/${A}/decision`,
    { decision: 'approve', draft_hash: hashA, expected_mark: back.data?.mark_digest });
  check('and approves it again', reapprove.status === 200 && marks()[A].decision === 'approve', detail(reapprove));
  const badStatus = await as(OWNER, 'POST', `/api/watcher/requests/${B}/decision`,
    { decision: 'change', draft_hash: marks()[B].draft_hash, expected_mark: py('digest', B), status: 'maybe', resolution: 'x' });
  check('a status outside the four is refused', badStatus.status === 400 && plain(badStatus), detail(badStatus));
  const badDecision = await as(OWNER, 'POST', `/api/watcher/requests/${B}/decision`,
    { decision: 'later', draft_hash: marks()[B].draft_hash, expected_mark: py('digest', B) });
  check('a decision outside approve, change, reject is refused', badDecision.status === 400, detail(badDecision));
  const events = sql("SELECT who, kind, cr, decision, draft_hash FROM watcher_event WHERE kind = 'decision'");
  check('every decision is in the audit trail, a replay that changed nothing not', events.length === 2
    && events.every((e) => e.cr === A && e.decision === 'approve' && e.draft_hash === hashA
      && e.who === 'harness.chief@softlabsgroup.com'), JSON.stringify(events));

  // a moved draft: the watcher drafted B again after the phone read it
  const hashB = marks()[B].draft_hash;
  const markB0 = py('digest', B);
  py('redraft', B);
  const moved = await as(OWNER, 'POST', `/api/watcher/requests/${B}/decision`,
    { decision: 'change', draft_hash: hashB, expected_mark: markB0, status: 'done', resolution: 'Offline words.' });
  check('a decision made on the old draft is refused 409 (offline replay after a redraft)',
    moved.status === 409 && plain(moved) && moved.data?.reason === 'draft-moved', detail(moved));
  check('and nothing was written', marks()[B].decision === '' && !/Offline words/.test(reviewText()));
  check('the lead\'s approve of the other request survived the redraft', marks()[A].decision === 'approve');
  const redrafted = await as(OWNER, 'GET', `/api/watcher/requests/${B}`);
  check('a draft FIXED IN the release would settle done at it', redrafted.data?.settle_status === 'done'
    && redrafted.data?.settle_ref === 'r14', JSON.stringify({ s: redrafted.data?.settle_status, r: redrafted.data?.settle_ref }));
  const changedB = await as(OWNER, 'POST', `/api/watcher/requests/${B}/decision`,
    { decision: 'change', draft_hash: redrafted.data?.draft_hash, expected_mark: redrafted.data?.mark_digest,
      status: 'rejected', ref: 'r9', resolution: 'Second thoughts.' });
  check('the owner changes the redraft', changedB.status === 200 && marks()[B].resolution === 'Second thoughts.', detail(changedB));
  const approvedB = await as(OWNER, 'POST', `/api/watcher/requests/${B}/decision`,
    { decision: 'approve', draft_hash: redrafted.data?.draft_hash, expected_mark: changedB.data?.mark_digest });
  const ma = marks()[B];
  check('approving after a change settles the draft as drafted: its status, ref and resolution come back (L6)',
    approvedB.status === 200 && ma.decision === 'approve' && ma.status === 'done' && ma.ref_to === 'r14'
    && ma.resolution === 'Decided: redrafted. Build now: y.', JSON.stringify(ma));
  const backB = await as(OWNER, 'DELETE', `/api/watcher/requests/${B}/decision`,
    { draft_hash: redrafted.data?.draft_hash, expected_mark: approvedB.data?.mark_digest });
  const mb = marks()[B];
  check('taking a mark back puts the drafted status, ref and resolution back', backB.status === 200
    && mb.decision === '' && mb.status === 'done' && mb.ref_to === 'r14' && mb.resolution === 'Decided: redrafted. Build now: y.',
  JSON.stringify(mb));
  const backMissing = await as(OWNER, 'DELETE', '/api/watcher/requests/CR-999/decision',
    { draft_hash: 'x', expected_mark: 'x' });
  check('taking back on a request the watcher does not hold is 404', backMissing.status === 404, detail(backMissing));

  // ── ask back ─────────────────────────────────────────────────────
  const asked = await as(OWNER, 'POST', `/api/watcher/requests/${A}/ask`, { question: 'Why option A, not B?' });
  check('an ask answers 202 with its thread entry', asked.status === 202 && asked.data?.state === 'asking'
    && asked.data?.question === 'Why option A, not B?', detail(asked));
  let entry = null;
  for (let i = 0; i < 120; i++) {
    const d = await as(OWNER, 'GET', `/api/watcher/requests/${A}`);
    entry = (d.data?.thread ?? [])[0];
    if (entry && entry.state !== 'asking') break;
    await new Promise((r) => setTimeout(r, 250));
  }
  check('the thread entry is answered when the turn ends', entry?.state === 'answered'
    && /contracts\/orders\.yaml:12/.test(entry?.answer ?? ''), JSON.stringify(entry));
  check('with the resolution it proposes, for "Use this answer"', /use the queue/.test(entry?.proposal?.resolution ?? '')
    && entry?.proposal?.status === 'done', JSON.stringify(entry?.proposal));
  check('and its cost', entry?.cost_usd === 0.42, `${entry?.cost_usd}`);
  check('asking changed no decision', marks()[A].decision === 'approve' && marks()[B].decision === '');
  const calls = existsSync(CALLS) ? readFileSync(CALLS, 'utf8').trim().split('\n').map((l) => JSON.parse(l)) : [];
  const call = calls[0] ?? { argv: [], env: [], prompt: '' };
  const after = (f) => call.argv[call.argv.indexOf(f) + 1];
  check('the ask is one turn at $2 and 30 turns', calls.length === 1 && after('--max-budget-usd') === '2.00'
    && after('--max-turns') === '30', JSON.stringify(call.argv.slice(0, 14)));
  check('with read-only tools', after('--tools') === 'Read,Grep,Glob' && call.argv.includes('Bash')
    && call.argv.includes('--restricted'), JSON.stringify(call.argv));
  check('holding no credential but Claude\'s own', call.env.includes('ANTHROPIC_API_KEY')
    && !call.env.some((k) => /^(ADAM_|TICVAI_)|PASSWORD|SECRET/i.test(k)), call.env.filter((k) => /ADAM|TICVAI|KEY|PASS/i.test(k)).join(','));
  check('its prompt is the draft, the thread and the question', /Why option A, not B\?/.test(call.prompt)
    && /Build now: x1/.test(call.prompt), call.prompt.slice(0, 200));
  const sum2 = await as(OWNER, 'GET', '/api/watcher/summary');
  check('the ask\'s cost is in today\'s spend', sum2.data?.spend_today_usd === 0.42, JSON.stringify(sum2.data?.spend_today_usd));
  check('the tray counts the one approve', sum2.data?.decided === 1, JSON.stringify(sum2.data?.decided));
  const reserved = readFileSync(path.join(OUT, 'spend.jsonl'), 'utf8').trim().split('\n').map((l) => JSON.parse(l));
  check('the ask reserved its $2 before it ran and was reconciled to its cost after (M2)',
    reserved.length === 2 && reserved[0].state === 'reserved' && reserved[0].usd === 2
    && reserved[1].state === 'settled' && reserved[1].reserve === reserved[0].reserve && reserved[1].cost === 0.42,
    JSON.stringify(reserved));
  const leadId = sql("SELECT id FROM account WHERE email = 'harness.chief@softlabsgroup.com'")[0]?.id;
  const nowIso = new Date().toISOString().replace(/\.\d+Z$/, '+00:00');
  py('sqlw', STORE, `INSERT INTO watcher_thread (cr, account_id, asked_by, asked_at, question, state) VALUES ${
    Array(9).fill("('CR-0', ?, 'x', ?, 'q', 'answered')").join(', ')}`, JSON.stringify(Array(9).fill([leadId, nowIso]).flat()));
  const limited = await as(OWNER, 'POST', `/api/watcher/requests/${A}/ask`, { question: 'An eleventh?' });
  check('ten questions an hour, then 429 (L1)', limited.status === 429 && plain(limited) && /hour/.test(limited.data?.detail ?? ''),
    detail(limited));
  py('sqlw', STORE, "DELETE FROM watcher_thread WHERE cr = 'CR-0'");
  const huge = 'x'.repeat(70 * 1024);
  const bigBody = await as(OWNER, 'POST', `/api/watcher/requests/${A}/ask`, { question: huge });
  check('a body over 64 KB is refused 413 by the API, before any route reads it (M6)', bigBody.status === 413, detail(bigBody));
  const chunked = await new Promise((resolve) => {
    const req = httpRequest(`${API}/api/watcher/requests/${A}/ask`, {
      method: 'POST', headers: { 'content-type': 'application/json', cookie: jars.get(OWNER) } }, (res) => {
      res.resume();
      res.on('end', () => resolve(res.statusCode));
    });
    req.on('error', () => resolve(0));
    for (let i = 0; i < 3; i++) req.write('x'.repeat(30 * 1024));
    req.end();
  });
  check('and so is one that streams in chunks with no length', chunked === 413, `${chunked}`);
  const viaViewer = await fetch(`${VIEWER_URL}/api/watcher/requests/${A}/ask`, {
    method: 'POST', headers: { 'content-type': 'application/json', cookie: jars.get(OWNER) },
    body: JSON.stringify({ question: huge }) });
  check('the viewer refuses it too, without forwarding it (M6)', viaViewer.status === 413, `${viaViewer.status}`);
  const viaViewerChunked = await new Promise((resolve) => {
    const req = httpRequest(`${VIEWER_URL}/api/watcher/requests/${A}/ask`, {
      method: 'POST', headers: { 'content-type': 'application/json' } }, (res) => {
      res.resume();
      res.on('end', () => resolve(res.statusCode));
    });
    req.on('error', () => resolve(-1));
    for (let i = 0; i < 3; i++) req.write('x'.repeat(30 * 1024));
    req.end();
  });
  check('the viewer stops a chunked one past 64 KB', viaViewerChunked === 413 || viaViewerChunked === -1, `${viaViewerChunked}`);
  const small = await fetch(`${VIEWER_URL}/api/watcher/summary`, { headers: { cookie: jars.get(OWNER) } });
  check('and forwards the ordinary ones', small.status === 200, `${small.status}`);
  const today = new Date();
  const day = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  appendFileSync(path.join(OUT, 'spend.jsonl'), JSON.stringify({ at: 'x', day, kind: 'draft', usd: 60, refs: [] }) + '\n');
  const capped = await as(OWNER, 'POST', `/api/watcher/requests/${A}/ask`, { question: 'And now?' });
  check('at the daily cap an ask is refused', capped.status === 429 && plain(capped), detail(capped));
  const tooLong = await as(OWNER, 'POST', `/api/watcher/requests/${A}/ask`, { question: 'x'.repeat(5000) });
  check('an over-long question is refused', tooLong.status === 400 || tooLong.status === 422, detail(tooLong));

  // ── settle: the preview, its fingerprint, the apply ──────────────
  const both = await Promise.all([as(OWNER, 'POST', '/api/watcher/settle/preview', {}),
    as(OTHER_OWNER, 'POST', '/api/watcher/settle/preview', {})]);
  check('one settle at a time: of two previews at once one runs, the other is told to wait (M1)',
    JSON.stringify(both.map((r) => r.status).sort()) === JSON.stringify([200, 423]), both.map(detail).join(' / '));
  const tooSoon = await as(OWNER, 'POST', '/api/watcher/settle/preview', {});
  check('a preview again within seconds is refused 429 (L1)', tooSoon.status === 429 && plain(tooSoon), detail(tooSoon));
  const pause = () => new Promise((r) => setTimeout(r, PREVIEW_EVERY * 1000 + 200));
  await pause();
  const preview = await as(OWNER, 'POST', '/api/watcher/settle/preview', {});
  const lines = (preview.data?.lines ?? []).join('\n');
  check('the preview answers', preview.status === 200, detail(preview));
  check('with the dry run\'s lines', /dry run/.test(lines) && lines.includes(A) && !lines.includes(PASSWORD), lines.slice(0, 400));
  check('and a fingerprint', /^[0-9a-f]{32}$/.test(preview.data?.fingerprint ?? ''), preview.data?.fingerprint ?? '');
  check('a preview settles nothing', marks()[A].decision === 'approve'
    && (await as('admin', 'GET', '/api/changes')).data?.items?.find((c) => c.id === A)?.status === 'open');
  const readB = (await as(OWNER, 'GET', `/api/watcher/requests/${B}`)).data ?? {};
  const late = await as(OWNER, 'POST', `/api/watcher/requests/${B}/decision`,
    { decision: 'change', draft_hash: readB.draft_hash, expected_mark: readB.mark_digest, status: 'done', resolution: 'Phone words for two.' });
  check('the owner decides one more after the preview', late.status === 200, detail(late));
  const stale = await as(OWNER, 'POST', '/api/watcher/settle/apply', { fingerprint: preview.data?.fingerprint });
  check('an apply with the fingerprint from before that is refused 409', stale.status === 409 && plain(stale), detail(stale));
  const still = (await as('admin', 'GET', '/api/changes')).data?.items ?? [];
  check('and nothing reached ADAM', still.every((c) => c.status === 'open'), still.map((c) => c.status).join(','));
  await pause();
  const preview2 = await as(OWNER, 'POST', '/api/watcher/settle/preview', {});
  check('a new preview has a new fingerprint', preview2.status === 200
    && preview2.data?.fingerprint !== preview.data?.fingerprint, detail(preview2));
  const applied = await as(OWNER, 'POST', '/api/watcher/settle/apply', { fingerprint: preview2.data?.fingerprint });
  check('the apply with the previewed fingerprint settles', applied.status === 200 && applied.data?.applied === true,
    `${detail(applied)} ${(applied.data?.lines ?? []).join(' | ').slice(0, 400)}`);
  const settled = Object.fromEntries(((await as('admin', 'GET', '/api/changes')).data?.items ?? []).map((c) => [c.id, c]));
  check('both requests are settled in ADAM', settled[A]?.status === 'done' && settled[B]?.status === 'done',
    `${settled[A]?.status} ${settled[B]?.status}`);
  check('with the lead\'s words where they changed it', settled[B]?.resolution === 'Phone words for two.',
    settled[B]?.resolution ?? '');
  check('and they leave the watcher\'s list', Object.keys(py('state').pending).length === 0,
    JSON.stringify(Object.keys(py('state').pending)));
  const settleEvents = sql("SELECT cr, decision, draft_hash, detail FROM watcher_event WHERE kind = 'settle' ORDER BY cr");
  check('every settled request is in the audit trail', JSON.stringify(settleEvents.map((e) => e.cr)) === JSON.stringify([A, B].sort()),
    JSON.stringify(settleEvents));
  check('each from the fingerprinted marks: its fingerprint, mark and draft hash (L2)', settleEvents.every((e) => {
    const d = JSON.parse(e.detail || '{}');
    return d.fingerprint === preview2.data?.fingerprint && /^[0-9a-f]{16}$/.test(d.mark ?? '') && /^[0-9a-f]{12}$/.test(e.draft_hash);
  }), JSON.stringify(settleEvents));
  check('applied says which it settled', JSON.stringify([...(applied.data?.settled ?? [])].sort()) === JSON.stringify([A, B].sort()),
    JSON.stringify(applied.data?.settled));
  await pause();
  const emptyPreview = await as(OWNER, 'POST', '/api/watcher/settle/preview', {});
  const emptyApply = await as(OWNER, 'POST', '/api/watcher/settle/apply', { fingerprint: emptyPreview.data?.fingerprint });
  check('settling with nothing marked does not say it applied anything (L2)', emptyApply.status === 200
    && emptyApply.data?.applied === false && (emptyApply.data?.settled ?? []).length === 0 && plain(emptyApply),
  `preview ${detail(emptyPreview)}; apply ${detail(emptyApply)} ${JSON.stringify(emptyApply.data?.applied)}`);

  // ── History: what was settled from Decide ────────────────────────
  const hist = await as(OWNER, 'GET', '/api/watcher/history');
  const hItems = hist.data?.items ?? [];
  check('History lists the settled requests, newest first', hist.status === 200 && hItems.length === 2
    && hItems[0].id > hItems[1].id && hItems.every((h) => !h.failed && h.status === 'done' && h.at),
  JSON.stringify(hItems.map((h) => [h.id, h.cr, h.status])));
  const hB = hItems.find((h) => h.cr === B) ?? {};
  check('each with its decision, what it posted, its title and the ticket it told (none here)',
    hB.decision === 'change' && hB.resolution === 'Phone words for two.' && hB.title === 'Harness request 2'
    && hB.ticket === '' && hB.who === 'harness.chief@softlabsgroup.com', JSON.stringify(hB));

  // ── requests with no draft (6 November 2026: every turn failed on an invalid API key) ─
  const F1 = 'CR-7001', F2 = 'CR-7002';
  py('addfailed', JSON.stringify([F1, F2]));
  const fSum = (await as(OWNER, 'GET', '/api/watcher/summary')).data ?? {};
  check('the summary counts the requests with no draft and the failed ones', fSum.not_drafted === 2
    && fSum.draft_failed === 2 && fSum.waiting === 2, JSON.stringify(fSum));
  const fRow = ((await as(OWNER, 'GET', '/api/watcher/requests')).data?.items ?? []).find((r) => r.cr === F1) ?? {};
  check('a row with no draft says why, and that the watcher gave up on it until Draft again', fRow.draft_hash === ''
    && fRow.gave_up === true && fRow.draft_tries === 2
    && fRow.draft_reason === 'claude reported an error (exit 1): Invalid API key · Please run /login', JSON.stringify(fRow));
  const fOne = (await as(OWNER, 'GET', `/api/watcher/requests/${F1}`)).data ?? {};
  check('one request carries the developer\'s own words and the ticket', fOne.draft === null
    && fOne.request?.problem === 'The developer\'s own words 1.' && fOne.request?.options === 'A or B'
    && fOne.ticket === '31567' && fOne.developer === 'Harness Dev', JSON.stringify({ d: fOne.draft, r: fOne.request }));
  const beforeF = reviewText();
  const noDraft = [];
  for (const b of [{ decision: 'approve' }, { decision: 'change', status: 'done', resolution: 'My own words.' },
    { decision: 'reject', note: 'no' }]) {
    noDraft.push(await as(OWNER, 'POST', `/api/watcher/requests/${F1}/decision`,
      { ...b, draft_hash: '', expected_mark: fOne.mark_digest }));
  }
  check('a decision on a request with no draft hash is refused 409 (not-drafted): approve, change and reject',
    noDraft.every((r) => r.status === 409 && r.data?.reason === 'not-drafted' && plain(r)),
    noDraft.map((r) => `${r.status} ${r.data?.reason}`).join(', '));
  check('and nothing is written', reviewText() === beforeF && marks()[F1].decision === '');
  const callsBefore = existsSync(CALLS) ? readFileSync(CALLS, 'utf8').trim().split('\n').length : 0;
  const again1 = await as(OWNER, 'POST', `/api/watcher/requests/${F1}/redraft`, {});
  let st = py('state');
  check('Draft again resets the request so the next run drafts it', again1.status === 200
    && JSON.stringify(again1.data?.redraft) === JSON.stringify([F1]) && st.pending[F1].draft_tries === 0
    && st.pending[F1].draft_error === '' && st.pending[F2].draft_tries === 2, detail(again1));
  const queued = existsSync(path.join(OUT, 'redraft.json')) ? JSON.parse(readFileSync(path.join(OUT, 'redraft.json'), 'utf8')) : [];
  check('it starts no Claude turn, and queues the request for a run drafting now',
    (existsSync(CALLS) ? readFileSync(CALLS, 'utf8').trim().split('\n').length : 0) === callsBefore
    && JSON.stringify(queued) === JSON.stringify([F1]), JSON.stringify(queued));
  const allAgain = await as(OWNER, 'POST', '/api/watcher/redraft', { all_failed: true });
  st = py('state');
  check('Draft all again takes every failed request', allAgain.status === 200
    && JSON.stringify(allAgain.data?.redraft) === JSON.stringify([F2]) && st.pending[F2].draft_tries === 0, detail(allAgain));
  const redraftEvents = sql("SELECT cr, who FROM watcher_event WHERE kind = 'redraft' ORDER BY id");
  check('each Draft again is in the audit trail', JSON.stringify(redraftEvents.map((e) => e.cr)) === JSON.stringify([F1, F2])
    && redraftEvents.every((e) => e.who === 'harness.chief@softlabsgroup.com'), JSON.stringify(redraftEvents));
  const notHeld = await as(OWNER, 'POST', '/api/watcher/requests/CR-999/redraft', {});
  check('Draft again on a request the watcher does not hold is 404', notHeld.status === 404 && plain(notHeld), detail(notHeld));
  const badMany = await as(OWNER, 'POST', '/api/watcher/redraft', {});
  check('Draft again naming nothing is refused 400', badMany.status === 400, detail(badMany));
  const presses = [];
  for (let i = 0; i < 20; i++) presses.push((await as(OWNER, 'POST', `/api/watcher/requests/${F1}/redraft`, {})).status);
  check('Draft again is rate-limited: twenty a minute, then 429', presses.slice(0, 16).every((x) => x === 200)
    && presses.at(-1) === 429, presses.join(','));

  // ── Health, and a run drafting now ───────────────────────────────
  appendFileSync(path.join(OUT, 'runs.log'), [
    '2026-11-06T09:07:02Z 16 new, 0 closed on their own, 16 waiting, 16 to draft, 0 drafted, 16 failed; first failure: claude reported an error (exit 1): Invalid API key',
    '2026-11-06T10:07:03Z 0 new, 0 closed on their own, 16 waiting, 0 to draft', ''].join('\n'));
  const hl = await as(OWNER, 'GET', '/api/watcher/health');
  const hd = hl.data ?? {};
  const next = Date.parse(hd.next_run_at ?? '');
  check('Health: the last runs, newest first, with their time and counts line', hl.status === 200
    && hd.runs?.[0]?.at === '2026-11-06T10:07:03Z' && /0 to draft/.test(hd.runs?.[0]?.line ?? '')
    && /16 failed/.test(hd.runs?.[1]?.line ?? ''), JSON.stringify(hd.runs));
  check('Health: when the next hourly run is due, within the hour', next > Date.now() && next - Date.now() <= 3600e3,
    hd.next_run_at);
  check('Health: today\'s spend against the cap, the paused reason and the last error', typeof hd.spend_today_usd === 'number'
    && hd.daily_cap_usd === 50 && /Drafting is held/.test(hd.paused ?? '') && 'last_error' in hd && hd.batch_usd === 10,
  JSON.stringify({ ...hd, runs: undefined }));
  const startedAt = '2026-11-06T11:07:01Z';
  py('running', String(process.pid), startedAt);
  const during = (await as(OWNER, 'GET', '/api/watcher/summary')).data ?? {};
  check('while a run drafts, the summary says since when and not the last run\'s note', during.running_since === startedAt
    && during.paused === '', JSON.stringify({ r: during.running_since, p: during.paused }));
  py('running', '0', startedAt);
  const afterRun = (await as(OWNER, 'GET', '/api/watcher/summary')).data ?? {};
  check('a run whose lock is gone (killed) is not drafting, and the note stands again', afterRun.running_since === ''
    && /Drafting is held/.test(afterRun.paused ?? ''), JSON.stringify({ r: afterRun.running_since, p: afterRun.paused }));
  py('running', '0', '');

  // ── the watcher stopped on this server (6 November 2026: its job deleted, its env file shredded) ─
  const envKept = readFileSync(ENV_FILE, 'utf8');
  py('poison', F2, 'claude reported an error (exit 1): Invalid API key', 'ADAM could not be read (HTTP 502)');
  rmSync(ENV_FILE);
  const offSum = (await as(OWNER, 'GET', '/api/watcher/summary')).data ?? {};
  check('with no watcher running here, the summary says so, with no stale error or pause', offSum.watching === false
    && offSum.paused === '' && offSum.last_error === '' && offSum.running_since === '' && offSum.waiting === 2,
  JSON.stringify({ w: offSum.watching, p: offSum.paused, e: offSum.last_error }));
  const offHealth = (await as(OWNER, 'GET', '/api/watcher/health')).data ?? {};
  check('and Health gives no next run', offHealth.watching === false && offHealth.next_run_at === '' && offHealth.paused === '',
    JSON.stringify({ w: offHealth.watching, n: offHealth.next_run_at }));
  const offAgain = await as(OWNER, 'POST', `/api/watcher/requests/${F2}/redraft`, {});
  const offAll = await as(OWNER, 'POST', '/api/watcher/redraft', { all_failed: true });
  check('Draft again is refused 409 (not-running), and nothing is reset', offAgain.status === 409
    && offAgain.data?.reason === 'not-running' && /not running on this server/.test(offAgain.data?.detail ?? '')
    && offAll.status === 409 && py('state').pending[F2].draft_error !== '', `${detail(offAgain)} ${detail(offAll)}`);
  const offHist = await as(OWNER, 'GET', '/api/watcher/history');
  check('History still reads what was settled', offHist.status === 200 && (offHist.data?.items ?? []).length === 2, detail(offHist));
  writeFileSync(ENV_FILE, envKept);
  py('unpoison');
  const on = (await as(OWNER, 'GET', '/api/watcher/summary')).data ?? {};
  check('with its env file back, it is running again', on.watching === true, JSON.stringify(on.watching));

  // a settle that fails: a request ADAM does not have, marked approve
  py('build', JSON.stringify([['CR-9999', true, 'lead']]));
  const lost = await as(OWNER, 'GET', '/api/watcher/requests/CR-9999');
  const lostMark = await as(OWNER, 'POST', '/api/watcher/requests/CR-9999/decision',
    { decision: 'approve', draft_hash: lost.data?.draft_hash, expected_mark: lost.data?.mark_digest });
  check('a request ADAM does not have is marked', lostMark.status === 200, detail(lostMark));
  await pause();
  const lostPreview = await as(OWNER, 'POST', '/api/watcher/settle/preview', {});
  const lostApply = await as(OWNER, 'POST', '/api/watcher/settle/apply', { fingerprint: lostPreview.data?.fingerprint });
  check('a settle that fails answers 502 and keeps the request on the list', lostApply.status === 502
    && Object.keys(py('state').pending).includes('CR-9999'), detail(lostApply));
  const failedEvents = sql("SELECT cr, detail FROM watcher_event WHERE kind = 'settle-failed'");
  check('and the audit trail records what it was attempting (L2)', failedEvents.length === 1 && failedEvents[0].cr === 'CR-9999'
    && JSON.parse(failedEvents[0].detail).fingerprint === lostPreview.data?.fingerprint, JSON.stringify(failedEvents));

  // ── the phone's device token ─────────────────────────────────────
  const made = await as(OWNER, 'POST', '/api/watcher/device-token', { device: 'Pixel 8' });
  const token = made.data?.token ?? '';
  check('the owner makes a device token', made.status === 200 && token.length >= 20 && Number.isInteger(made.data?.id),
    detail(made));
  const stored = sql("SELECT token_hash FROM watcher_device WHERE device = 'Pixel 8'");
  check('only its hash is stored', stored.length === 1 && stored[0].token_hash !== token
    && !JSON.stringify(stored).includes(token), JSON.stringify(stored));
  const viaToken = await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: token });
  check('the token reads the summary', viaToken.status === 200 && 'waiting' in (viaToken.data ?? {}), detail(viaToken));
  const tokenNew = viaToken.data?.new ?? [];
  check('counts only: no title, but the fields the app\'s check reads (cr, blocking, raised_at) (M3)', tokenNew.length === 1
    && tokenNew[0].cr === 'CR-9999' && tokenNew[0].title === '' && tokenNew[0].blocking === true && !!tokenNew[0].raised_at,
  JSON.stringify(tokenNew));
  const sessionNew = (await as(OWNER, 'GET', '/api/watcher/summary')).data?.new ?? [];
  check('a session still reads the titles', sessionNew[0]?.title === 'Harness request 1', JSON.stringify(sessionNew));
  const madeEvents = sql("SELECT who, detail FROM watcher_event WHERE kind = 'device-token'");
  check('making a token is in the audit trail (M3)', madeEvents.length === 1 && JSON.parse(madeEvents[0].detail).device === 'Pixel 8'
    && madeEvents[0].who === 'harness.chief@softlabsgroup.com' && !madeEvents[0].detail.includes(token), JSON.stringify(madeEvents));
  const reach = [];
  for (const [mth, p, b] of routes.slice(1)) reach.push((await as(null, mth, p, b, { bearer: token })).status);
  reach.push((await as(null, 'GET', '/api/changes', undefined, { bearer: token })).status);
  reach.push((await as(null, 'GET', '/api/auth/me', undefined, { bearer: token })).data?.account ? 200 : 401);
  check('and nothing else (401 everywhere)', reach.every((x) => x === 401), reach.join(','));
  const forged = await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: 'not-a-real-token-at-all' });
  check('a made-up token is refused', forged.status === 401, detail(forged));
  const second = await as(OWNER, 'POST', '/api/watcher/device-token', { device: 'Pixel 8' });
  const firstNow = await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: token });
  check('one per device: a new token for the same phone revokes the old', second.status === 200 && firstNow.status === 401,
    `${second.status} ${firstNow.status}`);
  const token2 = second.data?.token ?? '';
  const devRevoke = await as('harness.dev', 'DELETE', `/api/watcher/device-token/${second.data?.id}`);
  check('a dev cannot revoke the lead\'s token', devRevoke.status === 403, detail(devRevoke));
  const ownerRevokeOther = await as(OWNER, 'DELETE', '/api/watcher/device-token/99999');
  check('revoking a token that does not exist is 404', ownerRevokeOther.status === 404, detail(ownerRevokeOther));
  const revoke = await as(OWNER, 'DELETE', `/api/watcher/device-token/${second.data?.id}`);
  check('the owner revokes it', revoke.status === 200, detail(revoke));
  const gone = await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: token2 });
  check('a revoked token reads nothing', gone.status === 401, detail(gone));
  const revokedEvents = sql("SELECT detail FROM watcher_event WHERE kind = 'device-revoke'").map((e) => JSON.parse(e.detail).reason);
  check('every revocation is in the audit trail, with why', JSON.stringify(revokedEvents)
    === JSON.stringify(['a new token for the same device', 'revoked by hand']), JSON.stringify(revokedEvents));

  // ── how long a device token lives (M3) ───────────────────────────
  const mint = async (device) => (await as(OWNER, 'POST', '/api/watcher/device-token', { device })).data ?? {};
  const reads = async (t) => (await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: t })).status;
  const six = [];
  for (let i = 1; i <= 6; i++) six.push(await mint(`Phone ${i}`));
  const sixReads = [];
  for (const t of six) sixReads.push(await reads(t.token));
  check('five live tokens per account: a sixth revokes the longest unused', JSON.stringify(sixReads)
    === JSON.stringify([401, 200, 200, 200, 200, 200]), sixReads.join(','));
  const live = (await as(OWNER, 'GET', '/api/watcher/device-tokens')).data?.items ?? [];
  check('and five are listed', live.length === 5, JSON.stringify(live.map((x) => x.device)));
  const daysAgo = (n) => new Date(Date.now() - n * 86400000).toISOString().replace(/\.\d+Z$/, '+00:00');
  py('sqlw', STORE, 'UPDATE watcher_device SET made_at = ?, last_used_at = ? WHERE id = ?', JSON.stringify([daysAgo(91), daysAgo(1), six[1].id]));
  const old = await as(null, 'GET', '/api/watcher/summary', undefined, { bearer: six[1].token });
  check('a token older than 90 days is refused', old.status === 401 && /expired/.test(old.data?.detail ?? ''), detail(old));
  py('sqlw', STORE, 'UPDATE watcher_device SET made_at = ?, last_used_at = ? WHERE id = ?', JSON.stringify([daysAgo(40), daysAgo(31), six[2].id]));
  check('so is one unused for more than 30 days', (await reads(six[2].token)) === 401);
  py('sqlw', STORE, 'UPDATE watcher_device SET made_at = ?, last_used_at = NULL WHERE id = ?', JSON.stringify([daysAgo(31), six[3].id]));
  check('and one never used in the 30 days since it was made', (await reads(six[3].token)) === 401);
  check('one used yesterday still reads', (await reads(six[4].token)) === 200);
  const expiredEvents = sql("SELECT detail FROM watcher_event WHERE kind = 'device-revoke'").map((e) => JSON.parse(e.detail).reason)
    .filter((r) => r === 'expired');
  check('each expiry is in the audit trail', expiredEvents.length === 3, JSON.stringify(expiredEvents));

  // ── a device token ends with the account's sessions (M3) ─────────
  const leadEmail = 'harness.chief@softlabsgroup.com';
  let leadPassword = PASSWORD;
  const signIn = async () => (await as(OWNER, 'POST', '/api/auth/login', { email: leadEmail, password: leadPassword })).status;
  const ends = [];
  let t = await mint('Ends 1');
  await as(OWNER, 'POST', '/api/auth/logout-all');
  ends.push(['sign out everywhere', await reads(t.token)]);
  check('the System Architect signs in again', (await signIn()) === 200);
  t = await mint('Ends 2');
  const changed = await as(OWNER, 'POST', '/api/auth/password', { current: leadPassword, replacement: `${PASSWORD}-2` });
  leadPassword = `${PASSWORD}-2`;
  ends.push(['a password change', changed.status === 200 ? await reads(t.token) : `change ${changed.status}`]);
  t = await mint('Ends 3');
  const link = await as('admin', 'POST', `/api/accounts/${leadId}/reset`);
  const resetToken = (link.data?.link ?? '').split('#reset=')[1] ?? '';
  const reset = await as(OWNER, 'POST', '/api/auth/reset', { token: resetToken, password: `${PASSWORD}-3` });
  leadPassword = `${PASSWORD}-3`;
  ends.push(['a password reset', reset.status === 200 ? await reads(t.token) : `reset ${reset.status}`]);
  t = await mint('Ends 4');
  await as('admin', 'POST', `/api/accounts/${leadId}/logout-all`);
  ends.push(['an admin signing them out everywhere', await reads(t.token)]);
  check('and signs in again', (await signIn()) === 200);
  t = await mint('Ends 5');
  // The System Architect cannot be disabled from the site: the role is taken away on the machine first (the token
  // then reads nothing, its account no longer deciding), and the account disabled after.
  cli('owner', leadEmail, '--revoke', '--to', 'lead');
  ends.push(['the role taken away (a Team Lead now)', await reads(t.token)]);
  const off = await as('admin', 'POST', `/api/accounts/${leadId}/active?active=false`);
  ends.push(['deactivation', off.status === 200 ? await reads(t.token) : `deactivate ${off.status}`]);
  await as('admin', 'POST', `/api/accounts/${leadId}/active?active=true`);
  check('every one of them ends the phone\'s token (401)', ends.every(([, s]) => s === 401), JSON.stringify(ends));
  const withSessions = sql("SELECT detail FROM watcher_event WHERE kind = 'device-revoke'").map((e) => JSON.parse(e.detail).reason)
    .filter((r) => /signed out|password|disabled/.test(r));
  check('and says so in the audit trail', withSessions.length >= 5, JSON.stringify(withSessions));
}
