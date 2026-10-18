#!/usr/bin/env node
/**
 * The setup zip, run against project folders on a throwaway machine.
 *
 *   node viewer/mcp/setup-check.mjs
 *
 * **Why this exists.** On 13 October 2026 a frontend developer ran setup on her
 * app's clone and got no CLAUDE.md, no .claude\ and no project-bible\: a folder
 * that already had files was "only connected". Nothing failed, so nothing said
 * so. The same day the frontend became one repository per app, and the lead's
 * order became "first we run adam setup and then within that git clone": a new
 * frontend folder is a workspace holding ADAM's files, and the app repositories
 * are cloned inside it. This runs both orders the way a developer would -- the
 * zip as build-zip.ps1 makes it, its setup.ps1, a real `git clone` -- and checks
 * what lands where, what is left alone, and that a second run adds nothing.
 *
 *   1. a new frontend folder: a workspace with ADAM's files only, the clone
 *      lines printed, then a real clone inside it whose tree stays clean,
 *      and a usage-hook session from inside the clone filed under the workspace;
 *   2. a frontend repository cloned first: ADAM's files added, no existing file
 *      changed, nothing staged or committed, and what was added - with .adam/
 *      and .claude/settings.local.json - in .git\info\exclude, so git status
 *      stays clean; a repository with its own CLAUDE.md and
 *      .claude\settings.json keeps both;
 *   3. backend: an existing folder gets the same additions; an empty one is
 *      still cloned (here from a local stand-in of the team repository) or
 *      made from the starter;
 *   4. -UseStarter still makes the old frontend starter;
 *   5. the zip carries the new CLAUDE.md, README.txt and setup.ps1.
 *
 * **Nothing real is touched.** USERPROFILE and HOME point at a folder made
 * here; Claude Code is a stand-in that records the registration; ADAM is a
 * stand-in HTTP server in this process that answers the five routes setup and
 * the hook use; every git repository is a local one made here. No network,
 * no GitLab, no account anywhere.
 *
 * Windows only, like setup.ps1.
 */

import { spawn, execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { createServer } from 'node:http';
import { existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, rmSync, statSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const STARTERS = path.join(HERE, 'setup', 'starters');

if (process.platform !== 'win32') {
  console.log('setup-check runs setup.ps1, so it runs on Windows only.');
  process.exit(2);
}

const results = [];
const pass = (what) => { results.push(true); console.log(`  ok    ${what}`); };
const fail = (what, why = '') => { results.push(false); console.log(`  FAIL  ${what}${why ? `\n        ${String(why).slice(0, 1500)}` : ''}`); };
const ok = (cond, what, why) => (cond ? pass(what) : fail(what, why));
const section = (title) => console.log(`\n${title}`);

// ── the throwaway machine ─────────────────────────────────────────────

// The long spelling: %TEMP% is often an 8.3 name (CHINMA~1.PAR), and setup registers the folder as
// the disk spells it, so the two have to agree for the checks below to compare them.
const WORK = path.join(realpathSync.native(os.tmpdir()), `adam-setup-check-${Date.now()}`);
const HOME = path.join(WORK, 'home');
const BIN = path.join(WORK, 'bin');
const PLACES = path.join(WORK, 'work');
for (const d of [HOME, BIN, PLACES]) mkdirSync(d, { recursive: true });

// A stand-in for Claude Code, as in hooks-check: answers --version, keeps what
// `mcp add` was told and reads it back on `mcp get`. ASCII and CRLF for cmd.exe.
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
  '  echo Scope: Local config',
  '  type "%~dp0registered.txt"',
  '  exit /b 0',
  ')',
  'exit /b 1',
  '',
].join('\r\n'), 'ascii');

const SYSTEM = process.env.SystemRoot ?? 'C:\\Windows';
const POWERSHELL = path.join(SYSTEM, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe');
const GIT = execFileSync('where', ['git'], { encoding: 'utf8' }).split(/\r?\n/).map((l) => l.trim())
  .find((l) => /\\cmd\\git\.exe$/i.test(l)) ?? execFileSync('where', ['git'], { encoding: 'utf8' }).split(/\r?\n/)[0].trim();

/** A machine whose home is HOME: no ADAM_* inherited, the stand-in first on
 *  the PATH, git there too (setup clones and commits with it), and a git
 *  identity so a starter's first commit can be made. */
function machine(extra = {}) {
  const env = {};
  for (const [k, v] of Object.entries(process.env)) {
    if (/^(ADAM_|CLAUDE_PLUGIN_OPTION_|CLAUDE_PLUGIN_ROOT|GIT_)/i.test(k)) continue;
    if (/^path$/i.test(k)) continue;
    env[k] = v;
  }
  Object.assign(env, {
    USERPROFILE: HOME, HOME,
    PATH: [BIN, path.dirname(process.execPath), path.dirname(GIT), path.join(SYSTEM, 'System32'),
      path.join(SYSTEM, 'System32', 'WindowsPowerShell', 'v1.0'), path.join(SYSTEM, 'System32', 'Wbem')].join(';'),
    GIT_AUTHOR_NAME: 'Setup Check', GIT_AUTHOR_EMAIL: 'setup-check@example.invalid',
    GIT_COMMITTER_NAME: 'Setup Check', GIT_COMMITTER_EMAIL: 'setup-check@example.invalid',
  });
  return { ...env, ...extra };
}

/** Async on purpose: the stand-in ADAM below lives in this process, and a
 *  blocking spawn would keep it from answering setup. */
function run(file, args, { env = machine(), cwd = WORK, input } = {}) {
  return new Promise((resolve) => {
    const child = spawn(file, args, { env, cwd, windowsHide: true });
    let text = '';
    child.stdout.on('data', (d) => { text += d; });
    child.stderr.on('data', (d) => { text += d; });
    const timer = setTimeout(() => child.kill(), 240_000);
    child.on('close', (code) => { clearTimeout(timer); resolve({ code, text }); });
    child.stdin.end(input ?? '');
  });
}
const ps = (script, args, env) => run(POWERSHELL,
  ['-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', script, ...args], { env });
const git = (args, cwd) => execFileSync(GIT, args,
  { cwd, env: machine(), encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });

/** Every file under `root`, outside .git, with its hash. */
function hashes(root, { skip = [] } = {}) {
  const out = {};
  const walk = (dir) => {
    for (const name of readdirSync(dir)) {
      const full = path.join(dir, name);
      const rel = path.relative(root, full).replace(/\\/g, '/');
      if (name === '.git' || skip.some((s) => rel === s || rel.startsWith(`${s}/`))) continue;
      if (statSync(full).isDirectory()) walk(full);
      else out[rel] = createHash('sha256').update(readFileSync(full)).digest('hex');
    }
  };
  walk(root);
  return out;
}
const sameFiles = (before, after, keys = Object.keys(before)) => keys.filter((k) => before[k] !== after[k]);
const top = (dir) => readdirSync(dir).sort();
const lines = (text) => text.split(/\r?\n/).map((l) => l.replace(/\s+$/, '')).filter(Boolean);

// ── a stand-in ADAM ──────────────────────────────────────────────────

const flushed = [];
const server = createServer((req, res) => {
  let body = '';
  req.on('data', (d) => { body += d; });
  req.on('end', () => {
    const send = (status, data, headers = {}) => {
      res.writeHead(status, { 'content-type': 'application/json', ...headers });
      res.end(JSON.stringify(data));
    };
    const url = req.url.split('?')[0];
    if (url === '/api/auth/login' && req.method === 'POST') {
      return send(200, { ok: true }, { 'set-cookie': 'ticvai_session=setup-check; Path=/; HttpOnly' });
    }
    if (url === '/api/auth/me') return send(200, { account: { name: 'Setup Check', role: 'developer' } });
    if (url === '/api/auth/logout') return send(200, { ok: true });
    if (url === '/api/projects') {
      return send(200, { default: 'ticvai', projects: [{ id: 'ticvai', name: 'TICVAI' }, { id: 'demo-shop', name: 'Demo Shop' }] });
    }
    if (url === '/api/agent/flush' && req.method === 'POST') {
      try { flushed.push(JSON.parse(body)); } catch { flushed.push(null); }
      return send(200, { ok: true });
    }
    return send(404, { error: 'not here' });
  });
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const VIEWER = `http://127.0.0.1:${server.address().port}`;

// ── the zip ──────────────────────────────────────────────────────────

section('the zip');
const zip = path.join(WORK, 'adam-connector-setup.zip');
const built = await ps(path.join(HERE, 'setup', 'build-zip.ps1'), ['-Out', zip]);
ok(built.code === 0 && existsSync(zip), 'build-zip.ps1 builds', built.text.trim().split('\n').slice(-3).join(' | '));
const unzipped = path.join(WORK, 'unzipped');
await run(POWERSHELL, ['-NoProfile', '-NonInteractive', '-Command',
  `Expand-Archive -LiteralPath '${zip}' -DestinationPath '${unzipped}' -Force`]);
const ZIPPED = path.join(unzipped, 'adam-setup', 'adam-connector');
const SETUP = path.join(ZIPPED, 'setup.ps1');
const norm = (text) => text.replace(/\r\n/g, '\n');
const zippedText = (rel) => (existsSync(rel) ? norm(readFileSync(rel, 'utf8')) : '');
ok(zippedText(SETUP) === norm(readFileSync(path.join(HERE, 'setup', 'setup.ps1'), 'utf8')), 'the zip carries this setup.ps1');
ok(/function Add-AdamFiles/.test(zippedText(SETUP)) && /\[switch\]\$UseStarter/.test(zippedText(SETUP)),
  'which has Add-AdamFiles and -UseStarter');
ok(zippedText(path.join(ZIPPED, 'starters', 'frontend', 'CLAUDE.md')) === norm(readFileSync(path.join(STARTERS, 'frontend', 'CLAUDE.md'), 'utf8')),
  'the zip carries this frontend CLAUDE.md');
ok(/frontend workspace/.test(zippedText(path.join(ZIPPED, 'starters', 'frontend', 'CLAUDE.md'))),
  'which is the workspace one, not the 13-app one');
const readme = zippedText(path.join(unzipped, 'adam-setup', 'README.txt'));
const SIX = ['ticvai-venue-management', 'ticvai-guest-web', 'ticvai-employee-app', 'ticvai-kiosk', 'ticvai-guest-app', 'ticvai-pos'];
ok(SIX.every((r) => readme.includes(`http://gitlab.softlabsgroup.in/ticvai-frontend/${r}.git`)) && !readme.includes('{{BUILD}}'),
  'README.txt names the six frontend repositories and carries the build stamp');
ok(/SETUP FIRST, THEN CLONE YOUR APP INSIDE/.test(readme), 'and says to run setup first and clone inside');

const base = ['-ViewerUrl', VIEWER, '-Email', 'setup.check@example.invalid', '-Project', 'ticvai', '-Test', 'no'];
const ENV = machine({ ADAM_PASSWORD: 'a-long-enough-passphrase' });
const setup = (args) => ps(SETUP, [...base, ...args], ENV);
const registeredFor = () => (existsSync(path.join(BIN, 'registered.txt')) ? readFileSync(path.join(BIN, 'registered.txt'), 'utf8') : '');
const ADAM_ITEMS = ['.claude', 'CLAUDE.md', 'project-bible'];
const STARTER_CODE = ['apps', 'packages', 'nx.json', 'package.json', 'pnpm-lock.yaml', 'tsconfig.base.json', '.eslintrc.cjs',
  '.github', '.gitignore', 'README.md', 'src', 'tests', 'TICVAI-Backend.slnx', 'Directory.Build.props', 'BannedSymbols.txt', 'docs'];

/** A bare "team repository" with one commit, standing in for GitLab. */
function teamRepo(name, files) {
  const src = path.join(WORK, 'team-src', name);
  mkdirSync(src, { recursive: true });
  git(['init', '-q', '-b', 'main', src]);
  for (const [rel, text] of Object.entries(files)) {
    mkdirSync(path.dirname(path.join(src, rel)), { recursive: true });
    writeFileSync(path.join(src, rel), text, 'utf8');
  }
  git(['add', '-A'], src);
  git(['commit', '-q', '-m', 'first'], src);
  const bare = path.join(WORK, 'gitlab', `${name}.git`);
  git(['clone', '-q', '--bare', src, bare]);
  return bare;
}
const APP_FILES = {
  'package.json': '{\n  "name": "ticvai-pos",\n  "private": true,\n  "scripts": { "test": "vitest run" }\n}\n',
  'src/index.ts': 'export const pos = 1;\n',
  'README.md': '# ticvai-pos\n\nnpm install, npm test.\n',
  '.gitignore': 'node_modules/\n',
};

// ── 1. a new frontend folder is a workspace ──────────────────────────

section('frontend, a new folder: a workspace with ADAM\'s files, then a clone inside it');
const WS = path.join(PLACES, 'ticvai-frontend');
const first = await setup(['-Role', 'frontend', '-Folder', WS, '-GitUser', 'chitrangi']);
// SHOW=1 prints what the developer sees, to read it rather than match it.
if (process.env.SHOW) console.log(first.text);
ok(first.code === 0, 'setup finishes with 0', first.text.slice(-1500));
ok(!/!!/.test(first.text), 'and says nothing in the error style', first.text.split('\n').filter((l) => /!!/.test(l)).join(' | '));
ok(existsSync(WS) && JSON.stringify(top(WS)) === JSON.stringify(ADAM_ITEMS),
  'the workspace holds CLAUDE.md, .claude and project-bible only', existsSync(WS) ? top(WS).join(', ') : 'no folder');
ok(!existsSync(path.join(WS, '.git')), 'and is not a git repository');
ok(STARTER_CODE.every((n) => !existsSync(path.join(WS, n))), 'no starter code: no apps, packages, nx.json, package.json, lock file');
ok(readFileSync(path.join(WS, 'CLAUDE.md'), 'utf8') === readFileSync(path.join(ZIPPED, 'starters', 'frontend', 'CLAUDE.md'), 'utf8'),
  'CLAUDE.md is the starter\'s frontend one, unchanged');
for (const f of ['commands/ticket.md', 'commands/board.md', 'commands/done.md', 'commands/cr.md', 'commands/update-adam.md', 'settings.json']) {
  ok(existsSync(path.join(WS, '.claude', f)), `.claude/${f} is there`);
}
ok(existsSync(path.join(WS, 'project-bible', 'setup', 'frontend-patterns.md'))
  && existsSync(path.join(WS, 'project-bible', 'setup', 'README.md'))
  && !existsSync(path.join(WS, 'project-bible', 'setup', 'backend-patterns.md')),
  'project-bible/setup holds the frontend standards and their index');
const cloneLines = lines(first.text).filter((l) => /git -c http\.proactiveAuth=basic clone /.test(l));
ok(cloneLines.length === 6 && SIX.every((r) => cloneLines.some((l) => l.endsWith(`http://chitrangi@gitlab.softlabsgroup.in/ticvai-frontend/${r}.git`))),
  'the six clone lines are printed, one per repository, with the GitLab username', cloneLines.join('\n'));
ok(first.text.includes(`Open VS Code / Claude Code in ${WS}, not inside the repo folder`)
  && /so ADAM and the project bible load/.test(first.text), 'and where to open Claude Code', first.text.slice(-1500));
ok(registeredFor().includes(`ADAM_WORKDIR=${WS}`), 'ADAM is registered for the workspace', registeredFor());

const POS = teamRepo('ticvai-pos', APP_FILES);
git(['clone', '-q', POS, path.join(WS, 'ticvai-pos')], WS);
const clone = path.join(WS, 'ticvai-pos');
ok(existsSync(path.join(clone, 'package.json')), 'a real git clone inside the workspace works');
ok(git(['status', '--porcelain', '--ignored', '--untracked-files=all'], clone) === '',
  'and its tree is clean: nothing of ADAM\'s is in it', git(['status', '--porcelain', '--ignored'], clone));
ok(JSON.stringify(top(clone).filter((n) => n !== '.git')) === JSON.stringify(Object.keys(APP_FILES).map((f) => f.split('/')[0]).sort()),
  'it holds exactly the repository\'s files', top(clone).join(', '));

const wsBefore = hashes(WS);
const again = await setup(['-Role', 'frontend', '-Folder', WS, '-GitUser', 'chitrangi']);
ok(again.code === 0, 'setup on the workspace again finishes with 0', again.text.slice(-800));
ok(/nothing was missing/.test(again.text), 'it says nothing was missing', again.text.slice(-1500));
ok(sameFiles(wsBefore, hashes(WS)).length === 0 && Object.keys(hashes(WS)).length === Object.keys(wsBefore).length,
  'and adds and changes nothing, in the workspace or the clone', sameFiles(wsBefore, hashes(WS)).join(', '));
ok(git(['status', '--porcelain', '--ignored', '--untracked-files=all'], clone) === '', 'the clone is still clean');
ok(/Already cloned here: ticvai-pos/.test(again.text), 'and the clone lines say ticvai-pos is already here');

const WS2 = path.join(PLACES, 'nobody-frontend');
const anon = await setup(['-Role', 'frontend', '-Folder', WS2]);
ok(anon.code === 0 && lines(anon.text).filter((l) => l.includes('http://YOUR-GITLAB-USERNAME@gitlab.softlabsgroup.in/ticvai-frontend/')).length === 6,
  'with no console to ask the GitLab username on, the lines carry a placeholder and setup still ends with 0', anon.text.slice(-1200));

section('the usage hook, from inside the clone');
// What `claude mcp add -s local` leaves in ~/.claude.json for the workspace;
// the stand-in does not write it, so it is written here in the same shape.
const INSTALL = path.join(HOME, '.adam', 'connector');
mkdirSync(path.join(WS, '.adam', 'work', '6046'), { recursive: true });
writeFileSync(path.join(HOME, '.claude.json'), JSON.stringify({
  projects: {
    [WS.replace(/\\/g, '/')]: {
      mcpServers: {
        adam: {
          type: 'stdio', command: 'node', args: [path.join(INSTALL, 'server.mjs')],
          env: { ADAM_VIEWER_URL: VIEWER, ADAM_PROJECT: 'ticvai', ADAM_WORKDIR: WS, ADAM_EMAIL: 'setup.check@example.invalid', ADAM_PASSWORD: 'a-long-enough-passphrase' },
        },
      },
    },
  },
}, null, 2), 'utf8');
const hook = path.join(INSTALL, 'adam-hook.mjs');
const KEY = `setup-check-${Date.now()}`;
const say = (mode, body) => run(process.execPath, [hook, mode], { input: JSON.stringify({ session_id: KEY, cwd: clone, ...body }) });
await say('record', { hook_event_name: 'UserPromptSubmit' });
await say('record', { hook_event_name: 'PreToolUse', tool_name: 'Edit' });
await say('record', { hook_event_name: 'PostToolUse', tool_name: 'Edit', tool_response: { success: true } });
await say('flush', { hook_event_name: 'SessionEnd' });
const session = flushed.find((b) => b?.key === KEY);
ok(Boolean(session), 'a session whose folder is inside the clone reaches ADAM', JSON.stringify(flushed));
ok(session?.repo === 'ticvai-frontend', 'filed under the workspace\'s name, not the clone\'s', session?.repo);
ok(session?.external_key === '6046', 'with the ticket open in the workspace\'s .adam/work', session?.external_key);
rmSync(path.join(HOME, '.claude.json'), { force: true });

// ── 2. a frontend repository cloned first ────────────────────────────

section('frontend, a repository cloned first');
const REPO = path.join(PLACES, 'ticvai-guest-web');
mkdirSync(REPO, { recursive: true });
git(['init', '-q', '-b', 'main'], REPO);
for (const [rel, text] of Object.entries(APP_FILES)) {
  mkdirSync(path.dirname(path.join(REPO, rel)), { recursive: true });
  writeFileSync(path.join(REPO, rel), text, 'utf8');
}
git(['add', '-A'], REPO);
git(['commit', '-q', '-m', 'first'], REPO);
const head = git(['rev-parse', 'HEAD'], REPO).trim();
const repoBefore = hashes(REPO);
const excludeBefore = readFileSync(path.join(REPO, '.git', 'info', 'exclude'), 'utf8');
const onRepo = await setup(['-Role', 'frontend', '-Folder', REPO]);
ok(onRepo.code === 0, 'setup on the clone finishes with 0', onRepo.text.slice(-1500));
ok(/already has code\. Setup will not change any existing file; it adds ADAM's files where they are missing/.test(onRepo.text),
  'it says it changes no existing file and adds what is missing');
ok(ADAM_ITEMS.every((n) => existsSync(path.join(REPO, n))), 'CLAUDE.md, .claude and project-bible/setup are added');
ok(/added what ADAM needs and the folder lacked, not committed: CLAUDE\.md, \.claude, project-bible\\setup/.test(onRepo.text),
  'and setup says which', onRepo.text.split('\n').filter((l) => /added|missing/.test(l)).join(' | '));
ok(['apps', 'packages', 'nx.json', 'pnpm-lock.yaml', 'tsconfig.base.json'].every((n) => !existsSync(path.join(REPO, n))),
  'none of the starter code comes along');
ok(sameFiles(repoBefore, hashes(REPO)).length === 0, 'no existing file changed (by hash)', sameFiles(repoBefore, hashes(REPO)).join(', '));
ok(git(['rev-parse', 'HEAD'], REPO).trim() === head && git(['diff', '--cached', '--name-only'], REPO) === '',
  'nothing is staged or committed');
const status = git(['status', '--porcelain', '--untracked-files=all'], REPO);
ok(status === '', 'git status is clean: ADAM\'s files are kept out of the team\'s repository', status);
const ignored = lines(git(['status', '--porcelain', '--ignored'], REPO)).sort();
ok(JSON.stringify(ignored) === JSON.stringify(['!! .claude/', '!! CLAUDE.md', '!! project-bible/']),
  'and shows them as ignored, nothing else', ignored.join(' | '));
const exclude = readFileSync(path.join(REPO, '.git', 'info', 'exclude'), 'utf8');
const excluded = lines(exclude).filter((l) => !l.startsWith('#'));
ok(exclude.startsWith(excludeBefore)
  && ['.adam/', '.claude/settings.local.json', '/CLAUDE.md', '/.claude/', '/project-bible/setup/'].every((l) => excluded.includes(l)),
  '.git/info/exclude gains .adam/, .claude/settings.local.json and what was added, and keeps what it had', exclude);
ok(!existsSync(path.join(REPO, '.gitignore')) || readFileSync(path.join(REPO, '.gitignore'), 'utf8') === APP_FILES['.gitignore'],
  'the tracked .gitignore is untouched');
mkdirSync(path.join(REPO, '.adam', 'work', '1'), { recursive: true });
writeFileSync(path.join(REPO, '.adam', 'work', '1', 'README.md'), 'x', 'utf8');
writeFileSync(path.join(REPO, '.claude', 'settings.local.json'), '{}', 'utf8');
ok(JSON.stringify(lines(git(['status', '--porcelain', '--untracked-files=all'], REPO)).filter((l) => /\.adam|settings\.local/.test(l))) === '[]',
  'a pull into .adam/ and a personal settings.local.json stay out of git status');
rmSync(path.join(REPO, '.adam'), { recursive: true, force: true });
rmSync(path.join(REPO, '.claude', 'settings.local.json'), { force: true });

const repoAfterFirst = hashes(REPO);
const excludeAfterFirst = readFileSync(path.join(REPO, '.git', 'info', 'exclude'), 'utf8');
const onRepoAgain = await setup(['-Role', 'frontend', '-Folder', REPO]);
ok(onRepoAgain.code === 0 && /nothing was missing/.test(onRepoAgain.text), 'a second run says nothing was missing', onRepoAgain.text.slice(-800));
ok(sameFiles(repoAfterFirst, hashes(REPO)).length === 0 && Object.keys(hashes(REPO)).length === Object.keys(repoAfterFirst).length,
  'and adds or changes nothing', sameFiles(repoAfterFirst, hashes(REPO)).join(', '));
ok(readFileSync(path.join(REPO, '.git', 'info', 'exclude'), 'utf8') === excludeAfterFirst, 'not even a second line in .git/info/exclude');
ok(!/Clone your app/.test(onRepoAgain.text), 'a folder that is itself a repository gets no clone lines');

section('frontend, a repository with its own CLAUDE.md and .claude/settings.json');
const OWN = path.join(PLACES, 'ticvai-kiosk');
mkdirSync(path.join(OWN, '.claude'), { recursive: true });
git(['init', '-q', '-b', 'main'], OWN);
writeFileSync(path.join(OWN, 'CLAUDE.md'), '# the team\'s own\n', 'utf8');
writeFileSync(path.join(OWN, '.claude', 'settings.json'), '{ "permissions": { "allow": [] } }\n', 'utf8');
writeFileSync(path.join(OWN, 'package.json'), '{ "name": "ticvai-kiosk" }\n', 'utf8');
git(['add', '-A'], OWN);
git(['commit', '-q', '-m', 'first'], OWN);
const ownBefore = hashes(OWN);
const onOwn = await setup(['-Role', 'frontend', '-Folder', OWN]);
ok(onOwn.code === 0, 'setup finishes with 0', onOwn.text.slice(-800));
ok(sameFiles(ownBefore, hashes(OWN)).length === 0, 'their CLAUDE.md and .claude/settings.json are kept as they were');
ok(existsSync(path.join(OWN, '.claude', 'commands', 'ticket.md')) && existsSync(path.join(OWN, 'project-bible', 'setup', 'README.md')),
  'and the commands and the standards are added beside them');
ok(git(['status', '--porcelain', '--untracked-files=all'], OWN) === '', 'git status is clean');
const ownExcluded = lines(readFileSync(path.join(OWN, '.git', 'info', 'exclude'), 'utf8'));
ok(ownExcluded.includes('/.claude/commands/ticket.md') && !ownExcluded.includes('/.claude/') && !ownExcluded.includes('/CLAUDE.md'),
  'only the files setup added are excluded: their own .claude/ and CLAUDE.md stay visible to git', ownExcluded.join(' | '));
writeFileSync(path.join(OWN, '.claude', 'team-new.md'), 'x', 'utf8');
ok(/\.claude\/team-new\.md/.test(git(['status', '--porcelain', '--untracked-files=all'], OWN)),
  'and a file the team adds to .claude/ later still shows up');

// ── 3. backend ───────────────────────────────────────────────────────

section('backend, an existing folder');
const BE = path.join(PLACES, 'my-backend');
mkdirSync(path.join(BE, 'src'), { recursive: true });
git(['init', '-q', '-b', 'main'], BE);
writeFileSync(path.join(BE, 'README.md'), '# backend\n', 'utf8');
writeFileSync(path.join(BE, 'src', 'Program.cs'), 'class P {}\n', 'utf8');
git(['add', '-A'], BE);
git(['commit', '-q', '-m', 'first'], BE);
const beBefore = hashes(BE);
const onBe = await setup(['-Role', 'backend', '-Folder', BE]);
ok(onBe.code === 0, 'setup finishes with 0', onBe.text.slice(-800));
ok(ADAM_ITEMS.every((n) => existsSync(path.join(BE, n))), 'it gets the same additions');
ok(readFileSync(path.join(BE, 'CLAUDE.md'), 'utf8') === readFileSync(path.join(ZIPPED, 'starters', 'backend', 'CLAUDE.md'), 'utf8')
  && existsSync(path.join(BE, 'project-bible', 'setup', 'backend-patterns.md')), 'the backend ones');
ok(sameFiles(beBefore, hashes(BE)).length === 0 && !existsSync(path.join(BE, 'TICVAI-Backend.slnx')) && !existsSync(path.join(BE, 'tests')),
  'no existing file changed and no starter code came along');
ok(git(['status', '--porcelain', '--untracked-files=all'], BE) === '', 'git status is clean: ADAM\'s files are excluded');
const beAgain = await setup(['-Role', 'backend', '-Folder', BE]);
ok(beAgain.code === 0 && /nothing was missing/.test(beAgain.text), 'a second run adds nothing');

section('backend, an empty folder: still the team repository, or the starter');
const BEREPO = teamRepo('ticvai-backend', { 'README.md': '# ticvai-backend\n', 'src/Api.cs': 'class Api {}\n' });
const BECLONE = path.join(PLACES, 'ticvai-backend');
const cloned = await setup(['-Role', 'backend', '-Folder', BECLONE, '-RepoUrl', BEREPO]);
ok(cloned.code === 0 && existsSync(path.join(BECLONE, 'src', 'Api.cs')), 'an empty folder is cloned from the repository', cloned.text.slice(-1200));
ok(ADAM_ITEMS.every((n) => existsSync(path.join(BECLONE, n))) && !existsSync(path.join(BECLONE, 'TICVAI-Backend.slnx')),
  'with ADAM\'s files added and no starter code');
ok(git(['log', '--oneline'], BECLONE).trim().split('\n').length === 1, 'and nothing committed on top of the team\'s code');
ok(git(['status', '--porcelain', '--untracked-files=all'], BECLONE) === '', 'and the clone\'s git status is clean');
const STARTED = path.join(PLACES, 'demo-shop-backend');
const fromStarter = await ps(SETUP, ['-ViewerUrl', VIEWER, '-Email', 'setup.check@example.invalid', '-Project', 'demo-shop',
  '-Test', 'no', '-Role', 'backend', '-Folder', STARTED], ENV);
ok(fromStarter.code === 0 && existsSync(path.join(STARTED, 'DemoShop-Backend.slnx')),
  'a project with no team repository gets the starter, renamed (DemoShop)', fromStarter.text.slice(-1200));
ok(existsSync(path.join(STARTED, '.git')) && git(['log', '--oneline'], STARTED).trim().split('\n').length === 1,
  'as a new git repository with the starter as its first commit');
ok(!readFileSync(path.join(STARTED, 'CLAUDE.md'), 'utf8').includes('TICVAI'), 'its CLAUDE.md is renamed too');

// ── 4. -UseStarter ───────────────────────────────────────────────────

section('frontend, -UseStarter');
const OLD = path.join(PLACES, 'old-frontend');
const old = await setup(['-Role', 'frontend', '-Folder', OLD, '-UseStarter']);
ok(old.code === 0, 'setup finishes with 0', old.text.slice(-1200));
ok(['apps', 'packages', 'nx.json', 'package.json', 'CLAUDE.md', '.claude', 'project-bible'].every((n) => existsSync(path.join(OLD, n)))
  && readdirSync(path.join(OLD, 'apps')).length === 13, 'the old starter: 13 apps, packages, nx.json, ADAM\'s files');
ok(existsSync(path.join(OLD, '.git')) && !/Clone your app/.test(old.text), 'as a git repository, with no clone lines');

// ── 5. a workspace from before a change ────────────────────────────

section('a re-run refreshes ADAM\'s command files, and CLAUDE.md only between ADAM\'s markers (CHG-ADM-006)');
const OLDWS = path.join(PLACES, 'ticvai-old-workspace');
const madeNow = await setup(['-Role', 'frontend', '-Folder', OLDWS]);
ok(madeNow.code === 0, 'a workspace is made', madeNow.text.slice(-600));
const starterMd = readFileSync(path.join(OLDWS, 'CLAUDE.md'), 'utf8');
ok(/<!-- ADAM:start working-a-ticket -->/.test(starterMd) && /<!-- ADAM:end working-a-ticket -->/.test(starterMd),
  'its CLAUDE.md carries ADAM\'s markers');
// As a workspace made before this change has it: the old /ticket and /board, and an old section in a CLAUDE.md
// the team has added its own text to.
const wsCmd = (f) => path.join(OLDWS, '.claude', 'commands', f);
const newTicket = readFileSync(wsCmd('ticket.md'), 'utf8');
writeFileSync(wsCmd('ticket.md'), 'Run that repository\'s lint, typecheck and test\nargument-hint: <ticket number>\n');
writeFileSync(wsCmd('board.md'), 'old board\n');
writeFileSync(path.join(OLDWS, 'CLAUDE.md'), `# Our team\n\nOur own rule.\n\n${starterMd.replace(
  /(<!-- ADAM:start working-a-ticket -->\r?\n)[\s\S]*?(<!-- ADAM:end working-a-ticket -->)/, '$1## Working a ticket (ADAM)\n\nOLD TEXT\n\n$2')}`);
const oldSettings = readFileSync(path.join(OLDWS, '.claude', 'settings.json'), 'utf8');
const rerun = await setup(['-Role', 'frontend', '-Folder', OLDWS]);
ok(rerun.code === 0, 'setup on it again finishes with 0', rerun.text.slice(-800));
ok(readFileSync(wsCmd('ticket.md'), 'utf8') === newTicket && /startHere/.test(readFileSync(wsCmd('board.md'), 'utf8')),
  '**/ticket and /board are the starters\' again**', readFileSync(wsCmd('ticket.md'), 'utf8').slice(0, 200));
const refreshedMd = readFileSync(path.join(OLDWS, 'CLAUDE.md'), 'utf8');
ok(!refreshedMd.includes('OLD TEXT') && refreshedMd.startsWith('# Our team\n\nOur own rule.\n\n'),
  '**CLAUDE.md has the new section and still has the team\'s own text**', refreshedMd.slice(0, 200));
ok(readFileSync(path.join(OLDWS, '.claude', 'settings.json'), 'utf8') === oldSettings, 'settings.json is not touched');
ok(/refreshed .*ticket\.md/.test(rerun.text) && /Working a ticket \(ADAM\)/.test(rerun.text), 'and setup says what it refreshed', rerun.text.slice(-900));
ok(readdirSync(path.join(OLDWS, '.adam')).some((n) => n.startsWith('backup-workspace-')), 'the old files are kept in .adam');
const settledWs = hashes(OLDWS);
const thirdRun = await setup(['-Role', 'frontend', '-Folder', OLDWS]);
ok(thirdRun.code === 0 && sameFiles(settledWs, hashes(OLDWS)).length === 0 && Object.keys(hashes(OLDWS)).length === Object.keys(settledWs).length,
  'a third run changes nothing', sameFiles(settledWs, hashes(OLDWS)).join(', '));

// The same, with a CLAUDE.md from before the markers: left alone, with a line saying what to do.
const bareMd = starterMd.replace(/<!-- ADAM:(start|end) [a-z-]+ -->\r?\n/g, '').replace('Do not ask for a number', 'Ask for a number');
writeFileSync(path.join(OLDWS, 'CLAUDE.md'), bareMd);
writeFileSync(wsCmd('ticket.md'), 'Run that repository\'s lint, typecheck and test\n');
const noMarks = await setup(['-Role', 'frontend', '-Folder', OLDWS]);
ok(readFileSync(path.join(OLDWS, 'CLAUDE.md'), 'utf8') === bareMd, '**a CLAUDE.md with no markers is left exactly as it is**');
ok(readFileSync(wsCmd('ticket.md'), 'utf8') === newTicket, 'while the command files are still refreshed');
ok(/no ADAM markers/.test(noMarks.text) && /Working a ticket \(ADAM\)/.test(noMarks.text)
  && noMarks.text.includes(path.join(OLDWS, '.adam', 'new-claude-sections.md')),
  'and one line says which section to replace and where the new text is', noMarks.text.slice(-900));

// ── done ─────────────────────────────────────────────────────────────

server.close();
const failed = results.filter((r) => !r).length;
console.log(`\n${results.length - failed} of ${results.length} checks passed`);
if (!failed) rmSync(WORK, { recursive: true, force: true });
else console.log(`the throwaway machine is kept for a look: ${WORK}`);
process.exit(failed ? 1 : 0);
