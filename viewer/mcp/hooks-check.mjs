#!/usr/bin/env node
/**
 * The usage hooks, from the zip to the Agents page, on a throwaway home.
 *
 *   TICVAI_DB=<scratch>.db python -m uvicorn api.main:app --port 8799        (from viewer/)
 *   TICVAI_AUTH=http://127.0.0.1:8799 node server.mjs --port 4199             (from viewer/)
 *   VIEWER=http://127.0.0.1:4199 node viewer/mcp/hooks-check.mjs
 *
 * **Why this exists.** The Agents page showed nothing for weeks, and nothing
 * failed: the hooks were wired only for a plugin install, every developer was on
 * the zip, and a hook that is never installed raises no error anywhere. So this
 * runs the real path end to end — the zip as build-zip.ps1 makes it, its
 * setup.ps1, the settings.json it edits, the hook as Claude Code would call it,
 * and the API the page reads — and says which link broke.
 *
 * **Nothing real is touched.** `USERPROFILE` and `HOME` point at a folder made
 * here, so settings.json, ~/.claude.json, ~/.adam and the installed connector
 * are all throwaway copies. Claude Code itself is replaced by a stand-in on the
 * PATH that records the registration instead of writing it, because the real
 * one writes ~/.claude.json wherever it decides home is. It refuses a viewer
 * that is not on this machine, and it writes an account, so the API behind the
 * viewer must be on a scratch TICVAI_DB.
 *
 * Windows only, like setup.ps1.
 */

import { spawnSync, execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, readdirSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FILES, BEFORE_HOOKS } from './version.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..');
const VIEWER = (process.env.VIEWER ?? 'http://127.0.0.1:4173').replace(/\/+$/, '');
const EMAIL = process.env.HOOKS_EMAIL ?? 'harness.hooks@softlabsgroup.com';
const PASSWORD = process.env.HOOKS_PASSWORD ?? 'a-long-enough-passphrase';
// The last build before the hook joined the connector: what is on every
// developer's machine today, and what /update-adam has to start from.
const OLD_BUILD = process.env.OLD_BUILD ?? 'b4f56611';

if (process.platform !== 'win32') {
  console.log('hooks-check runs setup.ps1, so it runs on Windows only.');
  process.exit(2);
}
if (!/^https?:\/\/(127\.0\.0\.1|localhost)(:\d+)?$/.test(VIEWER)) {
  console.log(`refused: ${VIEWER} is not on this machine. This check writes an account; point VIEWER at a local viewer.`);
  process.exit(2);
}

const results = [];
const pass = (what) => { results.push(true); console.log(`  ok    ${what}`); };
const fail = (what, why = '') => { results.push(false); console.log(`  FAIL  ${what}${why ? `\n        ${why}` : ''}`); };
const ok = (cond, what, why) => (cond ? pass(what) : fail(what, why));
const section = (title) => console.log(`\n${title}`);

// ── the throwaway machine ─────────────────────────────────────────────

const WORK = path.join(os.tmpdir(), `adam-hooks-check-${Date.now()}`);
const HOME = path.join(WORK, 'home');
const BIN = path.join(WORK, 'bin');
mkdirSync(HOME, { recursive: true });
mkdirSync(BIN, { recursive: true });

// A stand-in for Claude Code: answers --version, keeps what `mcp add` was told
// and reads it back on `mcp get`, which is all setup asks of it. ASCII and CRLF
// because cmd.exe reads it.
writeFileSync(path.join(BIN, 'claude.cmd'), [
  '@echo off',
  'if "%~1"=="--version" (',
  '  echo 2.1.0 ^(Claude Code^)',
  '  exit /b 0',
  ')',
  'if "%~2"=="add" (',
  '  echo %* > "%~dp0registered.txt"',
  '  exit /b 0',
  ')',
  'if "%~2"=="get" (',
  '  echo Scope: User config',
  '  type "%~dp0registered.txt"',
  '  exit /b 0',
  ')',
  'exit /b 1',
  '',
].join('\r\n'), 'ascii');

const SYSTEM = process.env.SystemRoot ?? 'C:\\Windows';
const POWERSHELL = path.join(SYSTEM, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe');

/** The environment of a machine whose home is `home`: no ADAM_* and no plugin
 *  options inherited from whoever runs this, and a PATH where the only Claude
 *  Code is the stand-in. */
function machine(home, extra = {}) {
  const env = {};
  for (const [k, v] of Object.entries(process.env)) {
    if (/^(ADAM_|CLAUDE_PLUGIN_OPTION_|CLAUDE_PLUGIN_ROOT)/i.test(k)) continue;
    if (/^path$/i.test(k)) continue;
    env[k] = v;
  }
  env.USERPROFILE = home;
  env.HOME = home;
  env.PATH = [BIN, path.dirname(process.execPath), path.join(SYSTEM, 'System32'),
    path.join(SYSTEM, 'System32', 'WindowsPowerShell', 'v1.0'), path.join(SYSTEM, 'System32', 'Wbem')].join(';');
  return { ...env, ...extra };
}

function run(file, args, { env, input, cwd } = {}) {
  const out = spawnSync(file, args, { env, input, cwd, encoding: 'utf8', timeout: 180_000 });
  return { code: out.status, text: `${out.stdout ?? ''}${out.stderr ?? ''}` };
}
const ps = (script, args, env) => run(POWERSHELL,
  ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', script, ...args], { env });
const nodeRun = (script, args, env, input) => run(process.execPath, [script, ...args], { env, input });

const readJson = (file) => JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const slashed = (p) => p.replace(/\\/g, '/');

/** ADAM's entries in a settings object: [event, hook] for each command that
 *  runs adam-hook.mjs. */
const oursIn = (settings) => Object.entries(settings.hooks ?? {}).flatMap(([event, groups]) => groups
  .flatMap((g) => g.hooks ?? []).filter((h) => /adam-hook\.mjs/.test(h.command ?? ''))
  .map((h) => [event, h]));

/** What somebody already has: a setting or two and hooks of their own, one of
 *  them on an event ADAM also uses. All of it must come through untouched. */
const THEIRS = {
  theme: 'dark',
  permissions: { allow: ['Bash(ls:*)'], deny: [] },
  env: { SOMETHING: 'theirs' },
  hooks: {
    PreToolUse: [{ matcher: 'Bash', hooks: [{ type: 'command', command: 'echo theirs-pre' }] }],
    Notification: [{ hooks: [{ type: 'command', command: 'echo theirs-notify', timeout: 5 }] }],
  },
};
const settingsOf = (home) => path.join(home, '.claude', 'settings.json');
function seed(home) {
  mkdirSync(path.join(home, '.claude'), { recursive: true });
  writeFileSync(settingsOf(home), `${JSON.stringify(THEIRS, null, 4)}\n`, 'utf8');
}
const backupsOf = (home) => readdirSync(path.join(home, '.claude')).filter((f) => /^settings\.json\.adam-.*\.bak$/.test(f));

/** The settings carry ADAM's five, pointing at `install`, and everything of theirs. */
function checkMerged(home, install, label) {
  const now = readJson(settingsOf(home));
  const { hooks: _a, ...restNow } = now;
  const { hooks: _b, ...restTheirs } = THEIRS;
  ok(same(restNow, restTheirs), `${label}: every other setting is as it was`, JSON.stringify(restNow));
  ok(same(now.hooks?.PreToolUse?.[0], THEIRS.hooks.PreToolUse[0]),
    `${label}: their own PreToolUse hook is kept, first`, JSON.stringify(now.hooks?.PreToolUse));
  ok(same(now.hooks?.Notification, THEIRS.hooks.Notification),
    `${label}: their Notification hook is untouched`, JSON.stringify(now.hooks?.Notification));
  const ours = oursIn(now);
  ok(ours.length === 5, `${label}: exactly five ADAM hooks`, `${ours.length}: ${JSON.stringify(ours)}`);
  const script = `'${slashed(path.join(install, 'adam-hook.mjs'))}'`;
  for (const [event, mode] of [['PreToolUse', 'record'], ['PostToolUse', 'record'],
    ['UserPromptSubmit', 'record'], ['Stop', 'record'], ['SessionEnd', 'flush']]) {
    const mine = ours.filter(([e]) => e === event).map(([, h]) => h);
    const want = mode === 'flush'
      ? { type: 'command', command: `node ${script} flush`, timeout: 30 }
      : { type: 'command', command: `node ${script} record`, timeout: 10, async: true };
    ok(mine.length === 1 && same(mine[0], want), `${label}: ${event} runs ${mode}, quoted, as hooks.json times it`,
      JSON.stringify(mine));
  }
  return now;
}

// ── the viewer and an account ────────────────────────────────────────

let cookie = '';
async function call(route, { method = 'GET', body } = {}) {
  const once = () => fetch(`${VIEWER}${route}`, {
    method,
    headers: { ...(cookie ? { cookie } : {}), ...(body ? { 'content-type': 'application/json' } : {}) },
    body: body ? JSON.stringify(body) : undefined,
    redirect: 'manual',
  });
  // Once more on a dropped connection: setup runs for a minute between two
  // calls here, and the viewer closes a kept-alive socket long before that.
  const res = await once().catch(() => once());
  const set = res.headers.getSetCookie?.() ?? [];
  const session = set.map((l) => /^ticvai_session=[^;]+/.exec(l)?.[0]).find(Boolean);
  if (session) cookie = session;
  let data = null;
  try { data = await res.json(); } catch { /* empty */ }
  return { status: res.status, data };
}

section('the local stack');
try {
  const probe = await fetch(`${VIEWER}/login.html`, { signal: AbortSignal.timeout(3000) });
  ok(probe.ok, `the viewer answers at ${VIEWER}`, `${probe.status}`);
} catch (error) {
  fail(`the viewer answers at ${VIEWER}`, `${error.message} — start it (see the header)`);
  process.exit(1);
}
let signedIn = await call('/api/auth/bootstrap', { method: 'POST', body: { email: EMAIL, name: 'Harness Hooks', password: PASSWORD } });
if (signedIn.status !== 200) signedIn = await call('/api/auth/login', { method: 'POST', body: { email: EMAIL, password: PASSWORD } });
ok(signedIn.status === 200, `signed in as ${EMAIL}`,
  `${signedIn.status} — on a scratch database the first account is made here; otherwise create ${EMAIL} with HOOKS_PASSWORD`);
if (signedIn.status !== 200) process.exit(1);
const listed = await call('/api/projects');
const projects = (listed.data?.projects ?? []).map((p) => p.id);
const PROJECT = projects.includes('ticvai') ? 'ticvai' : projects[0];
ok(Boolean(PROJECT), `the account can open a project (${PROJECT})`, JSON.stringify(listed.data));

// ── 1. the zip carries the hook ──────────────────────────────────────

section('the zip');
const zip = path.join(WORK, 'adam-connector-setup.zip');
const built = ps(path.join(HERE, 'setup', 'build-zip.ps1'), ['-Out', zip], machine(HOME));
ok(built.code === 0 && existsSync(zip), 'build-zip.ps1 builds', built.text.trim().split('\n').slice(-3).join(' | '));
const unzipped = path.join(WORK, 'unzipped');
run(POWERSHELL, ['-NoProfile', '-NonInteractive', '-Command',
  `Expand-Archive -LiteralPath '${zip}' -DestinationPath '${unzipped}' -Force`], { env: machine(HOME) });
const zipped = path.join(unzipped, 'adam-setup', 'adam-connector');
for (const name of FILES) {
  ok(existsSync(path.join(zipped, name)), `the zip carries ${name}`);
}
const norm = (text) => text.replace(/\r\n/g, '\n');
ok(existsSync(path.join(zipped, 'adam-hook.mjs'))
  && norm(readFileSync(path.join(zipped, 'adam-hook.mjs'), 'utf8')) === norm(readFileSync(path.join(HERE, 'adam-hook.mjs'), 'utf8')),
  'the zipped hook is this one');

// ── 2. setup installs it, and leaves the rest alone ──────────────────

section('setup, into a throwaway home');
seed(HOME);
const original = readFileSync(settingsOf(HOME), 'utf8');
const INSTALL = path.join(HOME, '.adam', 'connector');
const setupArgs = ['-ViewerUrl', VIEWER, '-Email', EMAIL, '-Project', PROJECT, '-Folder', 'all', '-Test', 'no'];
const first = ps(path.join(zipped, 'setup.ps1'), setupArgs, machine(HOME, { ADAM_PASSWORD: PASSWORD }));
ok(first.code === 0, 'setup.ps1 finishes', first.text.split('\n').filter((l) => /!!|ok|usage/.test(l)).join(' | '));
ok(/usage hooks on/.test(first.text), 'setup says the usage hooks are on', first.text.slice(-600));
ok(existsSync(path.join(INSTALL, 'adam-hook.mjs')), 'the hook is installed beside the connector');
checkMerged(HOME, INSTALL, 'first run');
const backups = backupsOf(HOME);
ok(backups.length === 1 && readFileSync(path.join(HOME, '.claude', backups[0]), 'utf8') === original,
  'the file as it was is kept beside it, byte for byte', backups.join(', '));
ok(existsSync(path.join(INSTALL, 'hooks-installed.txt')), 'the install is remembered, so a later removal is respected');

const afterFirst = readFileSync(settingsOf(HOME), 'utf8');
const second = ps(path.join(zipped, 'setup.ps1'), setupArgs, machine(HOME, { ADAM_PASSWORD: PASSWORD }));
ok(second.code === 0, 'setup runs a second time');
checkMerged(HOME, INSTALL, 'second run');
ok(readFileSync(settingsOf(HOME), 'utf8') === afterFirst, 'a second run changes nothing in settings.json');
ok(backupsOf(HOME).length === 1, 'and leaves no second backup', backupsOf(HOME).join(', '));

section('a settings.json that is not JSON');
writeFileSync(settingsOf(HOME), '{ "theme": "dark", oops }\n', 'utf8');
const broken = nodeRun(path.join(INSTALL, 'update.mjs'), ['--install-hooks'], machine(HOME));
ok(readFileSync(settingsOf(HOME), 'utf8') === '{ "theme": "dark", oops }\n', 'is left exactly as it is');
const lines = broken.text.trim().split('\n').filter(Boolean);
ok(lines.length === 1 && /not valid JSON/.test(lines[0]) && /by hand/.test(lines[0]) && /SessionEnd/.test(lines[0]),
  'and gets one line saying how to add the hooks by hand', broken.text);
ok(broken.code !== 0, 'and the run says it did not install them', `exit ${broken.code}`);
writeFileSync(settingsOf(HOME), afterFirst, 'utf8');

// ── 3. the hook signs in from the registration, and the session lands ─

section('the hook, as Claude Code calls it');
// What `claude mcp add -s local` leaves in ~/.claude.json for a folder: the
// stand-in does not write it, so it is written here in the same shape.
const FOLDER = path.join(WORK, 'work', 'ticvai-backend');
mkdirSync(path.join(FOLDER, '.adam', 'work', '6046'), { recursive: true });
mkdirSync(path.join(FOLDER, 'src'), { recursive: true });
const claudeJson = path.join(HOME, '.claude.json');
writeFileSync(claudeJson, JSON.stringify({
  projects: {
    [slashed(FOLDER)]: {
      mcpServers: {
        adam: {
          type: 'stdio', command: 'node', args: [path.join(INSTALL, 'server.mjs')],
          env: {
            ADAM_VIEWER_URL: VIEWER, ADAM_PROJECT: PROJECT, ADAM_WORKDIR: FOLDER,
            ADAM_EMAIL: EMAIL, ADAM_PASSWORD: PASSWORD,
          },
        },
      },
    },
    'C:/somewhere/else': { mcpServers: { other: { command: 'node', args: ['x.mjs'], env: { ADAM_EMAIL: 'nobody@x', ADAM_PASSWORD: 'no' } } } },
  },
}, null, 2), 'utf8');

const HOOK = path.join(INSTALL, 'adam-hook.mjs');
const agentDir = path.join(HOME, '.adam', 'agent');
function session(key, cwd, { flushToo = true } = {}) {
  const env = machine(HOME);
  const send = (mode, body) => nodeRun(HOOK, [mode], env, JSON.stringify({ session_id: key, cwd, ...body }));
  const codes = [
    send('record', { hook_event_name: 'UserPromptSubmit', prompt: 'a secret prompt' }),
    send('record', { hook_event_name: 'PreToolUse', tool_name: 'Edit', tool_input: { file_path: 'x' } }),
    send('record', { hook_event_name: 'PostToolUse', tool_name: 'Edit', tool_response: { success: true } }),
    send('record', { hook_event_name: 'PreToolUse', tool_name: 'Bash', tool_input: { command: 'rm -rf /' } }),
    send('record', { hook_event_name: 'PostToolUse', tool_name: 'Bash', tool_response: { is_error: true, error: 'Permission denied: /etc/shadow' } }),
    send('record', { hook_event_name: 'Stop' }),
  ].map((r) => r.code);
  if (flushToo) codes.push(send('flush', { hook_event_name: 'SessionEnd', reason: 'exit' }).code);
  return codes;
}
const fileOf = (key) => path.join(agentDir, `${key}.jsonl`);

const KEY = `hooks-check-${Date.now()}`;
const recorded = session(KEY, path.join(FOLDER, 'src'), { flushToo: false });
ok(recorded.every((c) => c === 0), 'every record exits 0', recorded.join(','));
const kept = existsSync(fileOf(KEY)) ? readFileSync(fileOf(KEY), 'utf8') : '';
ok(kept.split('\n').filter(Boolean).length === 4, 'four lines recorded: the prompt, two tools, the stop', kept);
ok(!/secret|shadow|rm -rf|file_path/.test(kept), 'none of them holds the prompt, an argument or the error text', kept);
const flushed = nodeRun(HOOK, ['flush'], machine(HOME),
  JSON.stringify({ session_id: KEY, cwd: path.join(FOLDER, 'src'), hook_event_name: 'SessionEnd' }));
ok(flushed.code === 0, 'flush exits 0');
ok(!existsSync(fileOf(KEY)), 'and the file is gone, which it only is once ADAM has it');

section('the Agents page\'s API');
// agents.js asks auth.agentUsage, which is /api/agent/usage for the default project.
const usage = await call(`/api/agent/usage?days=30&project_id=${PROJECT}`);
ok(usage.status === 200, '/api/agent/usage answers', `${usage.status}`);
const row = (usage.data?.sessions ?? []).find((s) => s.repo === 'ticvai-backend');
ok(Boolean(row), 'the session is listed, under the connected folder\'s name (not src)', JSON.stringify(usage.data?.sessions?.slice(0, 3)));
ok(row?.ticket === '6046', 'with the ticket open in that folder', JSON.stringify(row));
ok((usage.data?.people ?? []).some((p) => p.calls >= 2 && p.failures >= 1), 'the person has calls and a failure',
  JSON.stringify(usage.data?.people));
const bash = (usage.data?.tools ?? []).find((t) => t.tool === 'Bash');
ok(bash?.failed >= 1 && bash?.why?.refused >= 1, 'Bash failed, classified as refused, without the message', JSON.stringify(bash));
if (row) {
  const detail = await call(`/api/agent/sessions/${row.id}`);
  ok(detail.data?.events?.length === 4, 'the session holds its four events', JSON.stringify(detail.data?.events));
}

section('folders the hook must not send from');
const ELSEWHERE = `hooks-check-elsewhere-${Date.now()}`;
mkdirSync(path.join(WORK, 'elsewhere'), { recursive: true });
const away = session(ELSEWHERE, path.join(WORK, 'elsewhere'));
ok(away.every((c) => c === 0), 'a folder ADAM is not connected to: every call exits 0', away.join(','));
ok(!existsSync(fileOf(ELSEWHERE)), 'its session is dropped, not kept to pile up');
const after = await call(`/api/agent/usage?days=30&project_id=${PROJECT}`);
ok(!(after.data?.sessions ?? []).some((s) => s.repo === 'elsewhere'), 'and never reaches ADAM');

renameSync(claudeJson, `${claudeJson}.away`);
const NOBODY = `hooks-check-nobody-${Date.now()}`;
const lost = session(NOBODY, FOLDER);
ok(lost.every((c) => c === 0), 'no credentials anywhere: every call exits 0', lost.join(','));
ok(existsSync(fileOf(NOBODY)), 'and the session is kept for later');
renameSync(`${claudeJson}.away`, claudeJson);

// ── 4. uninstall takes ADAM's hooks out and nothing else ─────────────

section('uninstall');
const gone = ps(path.join(INSTALL, 'setup.ps1'), ['-Uninstall'], machine(HOME));
ok(gone.code === 0, 'setup.ps1 -Uninstall finishes', gone.text.slice(-400));
const left = readJson(settingsOf(HOME));
ok(oursIn(left).length === 0, 'no ADAM hook is left', JSON.stringify(left.hooks));
ok(same(left, THEIRS), 'and settings.json holds exactly what it held before ADAM', JSON.stringify(left));
ok(!existsSync(INSTALL), 'the connector folder is gone');

// ── 5. /update-adam, from the build every developer has today ────────

section(`/update-adam from ${OLD_BUILD}, the last build without the hook`);
const HOME2 = path.join(WORK, 'home2');
const OLD = path.join(HOME2, '.adam', 'connector');
mkdirSync(OLD, { recursive: true });
for (const name of BEFORE_HOOKS) {
  writeFileSync(path.join(OLD, name),
    execFileSync('git', ['-C', REPO, 'show', `${OLD_BUILD}:viewer/mcp/${name}`], { encoding: 'utf8', maxBuffer: 1 << 26 }));
}
writeFileSync(path.join(OLD, 'viewer-url.txt'), `${VIEWER}\n`, 'ascii');
seed(HOME2);
const env2 = machine(HOME2);

const hop1 = nodeRun(path.join(OLD, 'update.mjs'), [], env2);
ok(hop1.code === 0 && /updated to/.test(hop1.text), 'the old updater takes the update cleanly (no refusal, no warning)',
  hop1.text.trim());
ok(!existsSync(path.join(OLD, 'adam-hook.mjs')), 'it could not take the hook — it does not know the name');
ok(readFileSync(settingsOf(HOME2), 'utf8') === `${JSON.stringify(THEIRS, null, 4)}\n`, 'and did not touch settings.json');

const hop2 = nodeRun(path.join(OLD, 'update.mjs'), [], env2);
ok(hop2.code === 0 && /updated to/.test(hop2.text), 'the second run takes the rest', hop2.text.trim());
ok(existsSync(path.join(OLD, 'adam-hook.mjs')), 'the hook arrives');
ok(/usage hooks: on/.test(hop2.text), 'and is turned on', hop2.text.trim());
checkMerged(HOME2, OLD, '/update-adam');

const hop3 = nodeRun(path.join(OLD, 'update.mjs'), [], env2);
const settled = readFileSync(settingsOf(HOME2), 'utf8');
ok(hop3.code === 0 && /already current/.test(hop3.text), 'a third run has nothing to do', hop3.text.trim());
checkMerged(HOME2, OLD, 'third run');

const off = nodeRun(path.join(OLD, 'update.mjs'), ['--remove-hooks'], env2);
ok(off.code === 0 && oursIn(readJson(settingsOf(HOME2))).length === 0, '--remove-hooks takes them out', off.text.trim());
const respected = nodeRun(path.join(OLD, 'update.mjs'), [], env2);
ok(oursIn(readJson(settingsOf(HOME2))).length === 0 && /off on this machine/.test(respected.text),
  'and the next update leaves them out, saying how to turn them back on', respected.text.trim());
ok(settled.length > 0, 'settings.json was never left empty');

// ── done ─────────────────────────────────────────────────────────────

const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} of ${results.length} checks passed`);
if (!failed) rmSync(WORK, { recursive: true, force: true });
else console.log(`the throwaway machine is kept for a look: ${WORK}`);
process.exit(failed ? 1 : 0);
