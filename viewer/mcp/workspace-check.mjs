#!/usr/bin/env node
// ADAM's own files in a developer's workspace are refreshed, and the team's are not (CHG-ADM-006, lane A ruling 4).
//
//   node viewer/mcp/workspace-check.mjs
//
// Found on 18 October: a new /ticket, /board and CLAUDE.md reached nobody who already had a workspace, because setup
// only adds files that are missing and /update-adam only replaces the connector. So now:
//   - /update-adam (update.mjs) and a re-run of setup replace ADAM's five command files in the workspace;
//   - CLAUDE.md is the team's: only a section between ADAM markers is replaced; a CLAUDE.md with no markers is left
//     exactly as it is, with one line saying which section to replace and where the new text is;
//   - (20 October) a new section a CLAUDE.md never had ("A [DB] ticket") is added whole with its markers, and ADAM's
//     script .claude/scripts/db-ticket.mjs is added or refreshed, kept out of git like setup's own files.
//
// Self-contained: its own viewer on port 8861 (the route is answered before the sign-in, so no accounts service), a
// stand-in that lies about file names on 8862, and temporary workspaces. Nothing of the developer's is touched: the
// updater runs with a throwaway home folder.

import { spawn, spawnSync } from 'node:child_process';
import { createServer } from 'node:http';
import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { FILES } from './version.mjs';

const MCP = path.dirname(fileURLToPath(import.meta.url));
const VIEWER_DIR = path.resolve(MCP, '..');
const STARTERS = path.join(MCP, 'setup', 'starters');
const PORTS = { viewer: 8861, liar: 8862 };
const COMMANDS = ['ticket.md', 'board.md', 'cr.md', 'done.md', 'update-adam.md'];

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` — ${detail}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};

const T = mkdtempSync(path.join(os.tmpdir(), 'adam-workspace-'));
const HOME = path.join(T, 'home');
mkdirSync(HOME, { recursive: true });
// The updater as it is installed on a developer's machine: a copy of the connector's files and nothing else. Run from
// the source folder it would find the plugin manifest beside it and refuse to write, as it should for a plugin.
const INSTALLED = path.join(T, 'connector');
mkdirSync(INSTALLED, { recursive: true });
for (const file of FILES) copyFileSync(path.join(MCP, file), path.join(INSTALLED, file));
const UPDATE = path.join(INSTALLED, 'update.mjs');
const read = (...p) => readFileSync(path.join(...p), 'utf8');
const starter = (role, ...p) => read(STARTERS, role, ...p);
const lf = (text) => text.replace(/\r\n/g, '\n');
const children = [];

/** The updater as a developer runs it: from the workspace, with a throwaway home so its usage-hook step has no
 *  settings.json of anyone's to touch. */
function updater(cwd, args = [], extra = {}) {
  const env = { ...process.env, USERPROFILE: HOME, HOME, ...extra };
  delete env.ADAM_VIEWER_URL;
  Object.assign(env, extra);
  const run = spawnSync(process.execPath, [UPDATE, ...args], { cwd, env, encoding: 'utf8', timeout: 60_000 });
  return { code: run.status, text: `${run.stdout ?? ''}${run.stderr ?? ''}` };
}

/** A workspace of the given role as it was before this change: old command files, and a CLAUDE.md whose section is
 *  old text, with ADAM markers or without. */
function oldWorkspace(name, role, { markers }) {
  const dir = path.join(T, name);
  mkdirSync(path.join(dir, '.claude', 'commands'), { recursive: true });
  for (const file of COMMANDS) writeFileSync(path.join(dir, '.claude', 'commands', file), `OLD ${file} adam_board\n`);
  writeFileSync(path.join(dir, '.claude', 'commands', 'ticket.md'), role === 'backend'
    ? 'adam_pull. Run `dotnet test TICVAI-Backend.slnx` until it passes.\nargument-hint: <ticket number>\n'
    : 'adam_pull. Run that repository\'s lint, typecheck and test\nargument-hint: <ticket number>\n');
  writeFileSync(path.join(dir, '.claude', 'settings.json'), '{ "team": "own" }\n');
  let md = lf(starter(role, 'CLAUDE.md'));
  md = md.replace(/(<!-- ADAM:start working-a-ticket -->\n)[\s\S]*?(<!-- ADAM:end working-a-ticket -->)/,
    `$1## Working a ticket (ADAM)\n\nOLD TEXT. Ask for a ticket number.\n\n$2`);
  md = `# The team's own heading\n\nTeam text above.\n\n${md}\nTeam text below.\n`;
  if (!markers) md = md.replace(/<!-- ADAM:(start|end) [a-z-]+ -->\n/g, '');
  writeFileSync(path.join(dir, 'CLAUDE.md'), md);
  return dir;
}

/** Async, for the one case whose ADAM lives in this process: a blocking spawn would keep it from answering. */
function updaterAsync(cwd, args, extra) {
  return new Promise((resolve) => {
    const env = { ...process.env, USERPROFILE: HOME, HOME, ...extra };
    const child = spawn(process.execPath, [UPDATE, ...args], { cwd, env, windowsHide: true });
    let text = '';
    child.stdout.on('data', (x) => { text += x; });
    child.stderr.on('data', (x) => { text += x; });
    child.on('close', (code) => resolve({ code, text }));
  });
}

function tree(dir) {
  const out = {};
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p); else out[path.relative(dir, p)] = readFileSync(p, 'utf8');
    }
  };
  walk(dir);
  return out;
}
const changed = (a, b) => [...new Set([...Object.keys(a), ...Object.keys(b)])].filter((k) => a[k] !== b[k]);

async function waitFor(url) {
  for (let i = 0; i < 160; i += 1) {
    try { if ((await fetch(url)).status < 500) return; } catch { /* not yet */ }
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error(`nothing answered at ${url}`);
}

try {
  // ── 1. the starters carry the markers the refresh looks for ────────
  for (const role of ['backend', 'frontend', 'ai']) {
    const md = lf(starter(role, 'CLAUDE.md'));
    check(`the ${role} starter CLAUDE.md marks "Working a ticket (ADAM)" as ADAM's`,
      /<!-- ADAM:start working-a-ticket -->\n\n?## Working a ticket \(ADAM\)[\s\S]*<!-- ADAM:end working-a-ticket -->/.test(md));
  }
  check('and the frontend one marks the "open the workspace folder" paragraph',
    /<!-- ADAM:start open-the-workspace -->[\s\S]*open the workspace folder[\s\S]*<!-- ADAM:end open-the-workspace -->/.test(
      lf(starter('frontend', 'CLAUDE.md'))));

  // ── 2. from the starters on disk (what setup does on a re-run) ─────
  const fe = oldWorkspace('fe-marked', 'frontend', { markers: true });
  const feBefore = tree(fe);
  const a = updater(fe, ['--refresh-workspace', fe, '--from', STARTERS]);
  check('the refresh finishes with 0', a.code === 0, a.text);
  for (const file of COMMANDS) {
    check(`.claude/commands/${file} is now the frontend starter's`,
      lf(read(fe, '.claude', 'commands', file)) === lf(starter('frontend', '.claude', 'commands', file)),
      read(fe, '.claude', 'commands', file).slice(0, 120));
  }
  check('the team\'s .claude/settings.json is untouched', read(fe, '.claude', 'settings.json') === feBefore[path.join('.claude', 'settings.json')]);
  const md = lf(read(fe, 'CLAUDE.md'));
  const want = lf(starter('frontend', 'CLAUDE.md'));
  check('**the section between ADAM markers is the starter\'s again**',
    md.includes(want.match(/<!-- ADAM:start working-a-ticket -->[\s\S]*?<!-- ADAM:end working-a-ticket -->/)[0]) && !md.includes('OLD TEXT'),
    md.slice(0, 300));
  check('**and the team\'s text above and below it is exactly as it was**',
    md.startsWith('# The team\'s own heading\n\nTeam text above.\n\n') && md.endsWith('\nTeam text below.\n'));
  check('the old files are kept beside, in .adam', Object.keys(tree(fe)).some((k) => /^\.adam[\\/]backup-workspace-.*ticket\.md$/.test(k))
    && Object.keys(tree(fe)).some((k) => /^\.adam[\\/]backup-workspace-.*CLAUDE\.md$/.test(k)), Object.keys(tree(fe)).join(' | '));
  check('it says what it did, in a line each', /ticket\.md/.test(a.text) && /Working a ticket \(ADAM\)/.test(a.text), a.text);

  const settled = tree(fe);
  const b = updater(fe, ['--refresh-workspace', fe, '--from', STARTERS]);
  check('**run again it changes nothing and makes no second backup**', b.code === 0 && changed(settled, tree(fe)).length === 0,
    changed(settled, tree(fe)).join(', '));
  check('and says so', /already current|nothing to refresh/i.test(b.text), b.text);

  // ── 3. a CLAUDE.md with no markers is the team's: left alone ───────
  const un = oldWorkspace('fe-unmarked', 'frontend', { markers: false });
  const unMd = read(un, 'CLAUDE.md');
  const c = updater(un, ['--refresh-workspace', un, '--from', STARTERS]);
  check('**a CLAUDE.md with no ADAM markers is left byte for byte as it is**', read(un, 'CLAUDE.md') === unMd, c.text);
  check('while its command files are refreshed',
    lf(read(un, '.claude', 'commands', 'ticket.md')) === lf(starter('frontend', '.claude', 'commands', 'ticket.md')));
  const fresh = path.join(un, '.adam', 'new-claude-sections.md');
  check('**one line says which section to replace and where the new text is**',
    /no ADAM markers/.test(c.text) && /Working a ticket \(ADAM\)/.test(c.text) && c.text.includes(fresh), c.text);
  check('and the new text is there to copy', existsSync(fresh) && /Do not ask for a number/.test(read(fresh)) && /startHere/.test(read(fresh)),
    existsSync(fresh) ? read(fresh).slice(0, 200) : 'no file');

  // ── 4. a CLAUDE.md that is not ADAM's at all is not talked about ──
  const own = path.join(T, 'own');
  mkdirSync(path.join(own, '.claude', 'commands'), { recursive: true });
  writeFileSync(path.join(own, 'CLAUDE.md'), '# the team\'s own\n');
  writeFileSync(path.join(own, '.claude', 'commands', 'ticket.md'), 'adam_pull. lint, typecheck\n');
  const d = updater(own, ['--refresh-workspace', own, '--from', STARTERS]);
  check('a CLAUDE.md that never had ADAM\'s section gets no line about markers and no new file',
    !/markers/.test(d.text) && !existsSync(path.join(own, '.adam', 'new-claude-sections.md')) && read(own, 'CLAUDE.md') === '# the team\'s own\n', d.text);

  // ── 4b. a team's own command files are theirs (I-3) ───────────────
  // An app clone with a board.md and done.md of its own, and a CLAUDE.md that mentions package.json: not an ADAM
  // workspace, nothing in it is touched.
  const app = path.join(T, 'app-clone');
  mkdirSync(path.join(app, '.claude', 'commands'), { recursive: true });
  writeFileSync(path.join(app, '.claude', 'commands', 'board.md'), 'Show the team board from Trello.\n');
  writeFileSync(path.join(app, '.claude', 'commands', 'done.md'), 'Run package.json scripts and tag the release.\n');
  writeFileSync(path.join(app, 'CLAUDE.md'), '# app\nuses package.json and pnpm\n');
  const appBefore = tree(app);
  const j = updater(app, ['--refresh-workspace', app, '--from', STARTERS]);
  check('**a folder whose command files are the team\'s own is not treated as an ADAM workspace, and nothing in it changes**',
    changed(appBefore, tree(app)).length === 0 && /not an ADAM workspace/.test(j.text), j.text);
  const k = updater(app, ['--refresh-workspace', app, '--role', 'frontend', '--from', STARTERS]);
  check('even when told the role', changed(appBefore, tree(app)).length === 0, k.text);
  // An ADAM workspace in which one command file was replaced by the team's own: that one stays.
  const mixed = oldWorkspace('fe-mixed', 'frontend', { markers: true });
  writeFileSync(path.join(mixed, '.claude', 'commands', 'done.md'), 'Our own done command, nothing to do with ADAM.\n');
  const l = updater(mixed, ['--refresh-workspace', mixed, '--from', STARTERS]);
  check('**inside an ADAM workspace a command file that is not ADAM\'s is left alone, while ADAM\'s are refreshed**',
    read(mixed, '.claude', 'commands', 'done.md') === 'Our own done command, nothing to do with ADAM.\n'
      && lf(read(mixed, '.claude', 'commands', 'ticket.md')) === lf(starter('frontend', '.claude', 'commands', 'ticket.md')), l.text);

  // ── 5. line endings and the backend ────────────────────────────────
  const be = oldWorkspace('be-crlf', 'backend', { markers: true });
  writeFileSync(path.join(be, 'CLAUDE.md'), read(be, 'CLAUDE.md').replace(/\n/g, '\r\n'));
  const e = updater(be, ['--refresh-workspace', be, '--from', STARTERS]);
  const beMd = read(be, 'CLAUDE.md');
  check('the backend is told from the frontend by its own /ticket, and gets the backend files',
    e.code === 0 && lf(read(be, '.claude', 'commands', 'ticket.md')) === lf(starter('backend', '.claude', 'commands', 'ticket.md')), e.text);
  check('a CLAUDE.md written with Windows line endings keeps them', /\r\n/.test(beMd) && !/[^\r]\n/.test(beMd), JSON.stringify(beMd.slice(0, 80)));
  check('and gets the backend section', lf(beMd).includes('No ticket named? Do not ask for a number') && !beMd.includes('OLD TEXT'));

  // ── 5b. the [DB] ticket's section and script reach a backend folder made before them (20 October 2026) ──
  const DB_RE = /<!-- ADAM:start db-ticket -->\r?\n[\s\S]*?<!-- ADAM:end db-ticket -->\r?\n/;
  const SCRIPT = ['.claude', 'scripts', 'db-ticket.mjs'];
  const dbInner = lf(starter('backend', 'CLAUDE.md')).match(/<!-- ADAM:start db-ticket -->\n([\s\S]*?)<!-- ADAM:end db-ticket -->/)?.[1];
  check('the backend starter CLAUDE.md marks "A [DB] ticket" as ADAM\'s', Boolean(dbInner) && dbInner.startsWith('## A [DB] ticket'));
  const noDb = oldWorkspace('be-no-db', 'backend', { markers: true });
  writeFileSync(path.join(noDb, 'CLAUDE.md'), read(noDb, 'CLAUDE.md').replace(DB_RE, ''));
  spawnSync('git', ['init', '-q'], { cwd: noDb });
  const noDbMd = read(noDb, 'CLAUDE.md');
  const h = updater(noDb, ['--refresh-workspace', noDb, '--from', STARTERS]);
  const withDb = read(noDb, 'CLAUDE.md');
  check('**a backend CLAUDE.md that never had "A [DB] ticket" gets it, with its markers, after "Working a ticket (ADAM)"**',
    withDb.includes(`<!-- ADAM:end working-a-ticket -->\n\n<!-- ADAM:start db-ticket -->\n${dbInner}<!-- ADAM:end db-ticket -->\n`)
      && (withDb.match(/<!-- ADAM:start db-ticket -->/g) ?? []).length === 1
      // Everything after the working-a-ticket section, the team's "Ticket kinds" and the rest, is as it was.
      && withDb.replace(DB_RE, '').split('<!-- ADAM:end working-a-ticket -->\n\n')[1]
        === noDbMd.split('<!-- ADAM:end working-a-ticket -->\n')[1],
    h.text);
  check('and the team\'s own text above and below is where it was', withDb.startsWith('# The team\'s own heading\n\nTeam text above.') && withDb.endsWith('Team text below.\n'));
  check('**the [DB] check script is added to .claude/scripts**', existsSync(path.join(noDb, ...SCRIPT))
    && read(noDb, ...SCRIPT) === starter('backend', ...SCRIPT) && /added \.claude\/scripts\/db-ticket\.mjs/.test(h.text), h.text);
  check('and kept out of git like setup\'s own files', read(noDb, '.git', 'info', 'exclude').split(/\r?\n/).includes('/.claude/scripts/db-ticket.mjs'));
  const dbSettled = tree(noDb);
  updater(noDb, ['--refresh-workspace', noDb, '--from', STARTERS]);
  check('a second refresh changes nothing', changed(dbSettled, tree(noDb)).length === 0, changed(dbSettled, tree(noDb)).join(', '));
  writeFileSync(path.join(noDb, ...SCRIPT), `${starter('backend', ...SCRIPT)}\n// an older build\n`);
  const k2 = updater(noDb, ['--refresh-workspace', noDb, '--from', STARTERS]);
  check('an older ADAM script is replaced, the old one kept in .adam, and the line says where', read(noDb, ...SCRIPT) === starter('backend', ...SCRIPT)
    && /refreshed \.claude\/scripts\/db-ticket\.mjs \(the old one is in [^)]*backup-workspace-/.test(k2.text)
    && Object.keys(tree(noDb)).some((n) => /^\.adam[\\/]backup-workspace-.*db-ticket\.mjs$/.test(n)), k2.text);
  writeFileSync(path.join(noDb, ...SCRIPT), 'console.log("the team\'s own");\n');
  updater(noDb, ['--refresh-workspace', noDb, '--from', STARTERS]);
  check('a script of the team\'s under the same name is theirs, and stays', read(noDb, ...SCRIPT) === 'console.log("the team\'s own");\n');
  const bareDb = oldWorkspace('be-bare-db', 'backend', { markers: false });
  writeFileSync(path.join(bareDb, 'CLAUDE.md'), read(bareDb, 'CLAUDE.md').replace(/## A \[DB\] ticket[\s\S]*?(?=## Searching pulled files)/, ''));
  const bareBefore = read(bareDb, 'CLAUDE.md');
  const bareRun = updater(bareDb, ['--refresh-workspace', bareDb, '--from', STARTERS]);
  const bareAfter = read(bareDb, 'CLAUDE.md');
  check('**a backend CLAUDE.md from before the markers gets "A [DB] ticket" added at its end, every line of it unchanged**',
    bareAfter.startsWith(bareBefore) && bareAfter.endsWith(`<!-- ADAM:start db-ticket -->\n${dbInner}<!-- ADAM:end db-ticket -->\n`), bareAfter.slice(-200));
  check('and one line on what has no markers: that section was left as it is, not the whole file',
    /CLAUDE\.md's "Working a ticket \(ADAM\)" section has no ADAM markers, so it was left as it is/.test(bareRun.text)
      && !/left exactly as it is/.test(bareRun.text) && /"A \[DB\] ticket" refreshed between its ADAM markers/.test(bareRun.text), bareRun.text);

  // ── 5c. the frontend's "Building a screen to its wireframe" reaches a workspace made before it (21 October 2026) ──
  const LOOK_RE = /<!-- ADAM:start screen-look -->\r?\n[\s\S]*?<!-- ADAM:end screen-look -->\r?\n/;
  const lookInner = lf(starter('frontend', 'CLAUDE.md')).match(/<!-- ADAM:start screen-look -->\n([\s\S]*?)<!-- ADAM:end screen-look -->/)?.[1];
  check('the frontend starter CLAUDE.md marks "Building a screen to its wireframe" as ADAM\'s, and a frame the pull wrote '
    + 'came through ADAM', Boolean(lookInner) && lookInner.startsWith('## Building a screen to its wireframe')
      && /That frame came through ADAM, and it is the design/.test(lookInner) && /placeholder layout only when no frame was written/i.test(lookInner));
  check('and the theme is the app\'s: SETUP-SHELL-<APP> and its tokens file, never a colour or font of the screen\'s own '
    + '(and the starter\'s design-tokens package says it holds the shared tokens only)',
  /`SETUP-SHELL-<APP>` ticket/.test(lookInner) && /handoff\/design-tokens\/guest-web\.yaml/.test(lookInner)
      && /never invents or hard-codes a colour, font, radius or shadow/.test(lookInner)
      && /Each state's look/.test(lookInner)
      && /\*\*shared\*\* design tokens/.test(starter('frontend', 'packages', 'design-tokens', 'src', 'index.ts'))
      && /SETUP-SHELL-<APP>/.test(starter('frontend', 'packages', 'design-tokens', 'src', 'index.ts')));
  const noLook = oldWorkspace('fe-no-look', 'frontend', { markers: true });
  writeFileSync(path.join(noLook, 'CLAUDE.md'), read(noLook, 'CLAUDE.md').replace(LOOK_RE, ''));
  const noLookMd = read(noLook, 'CLAUDE.md');
  const lk = updater(noLook, ['--refresh-workspace', noLook, '--from', STARTERS]);
  const withLook = read(noLook, 'CLAUDE.md');
  check('**a frontend CLAUDE.md that never had it gets it, with its markers, after "Working a ticket (ADAM)"**',
    withLook.includes(`<!-- ADAM:end working-a-ticket -->\n\n<!-- ADAM:start screen-look -->\n${lookInner}<!-- ADAM:end screen-look -->\n`)
      && withLook.replace(LOOK_RE, '').split('<!-- ADAM:end working-a-ticket -->\n\n')[1] === noLookMd.split('<!-- ADAM:end working-a-ticket -->\n')[1]
      && /"Building a screen to its wireframe"/.test(lk.text), lk.text);

  // ── 6. a folder that is not an ADAM workspace is not written to ────
  const empty = path.join(T, 'empty');
  mkdirSync(empty, { recursive: true });
  const f = updater(empty, ['--refresh-workspace', empty, '--from', STARTERS]);
  check('**a folder with none of ADAM\'s command files gets nothing created in it**', readdirSync(empty).length === 0, readdirSync(empty).join(', '));
  check('and is told why', /not an ADAM workspace|no ADAM command files/i.test(f.text), f.text);

  // ── 7. from ADAM itself, which is what /update-adam does ───────────
  const viewer = spawn(process.execPath, ['server.mjs', '--port', String(PORTS.viewer), '--host', '127.0.0.1'],
    { cwd: VIEWER_DIR, env: { ...process.env }, windowsHide: true });
  let viewerLog = '';
  viewer.stdout.on('data', (x) => { viewerLog += x; });
  viewer.stderr.on('data', (x) => { viewerLog += x; });
  children.push(viewer);
  await waitFor(`http://127.0.0.1:${PORTS.viewer}/connector/version`);
  const route = await (await fetch(`http://127.0.0.1:${PORTS.viewer}/connector/workspace?role=frontend`)).json();
  check('the viewer answers /connector/workspace before any sign-in, with the five commands and the CLAUDE.md',
    JSON.stringify(route.commands?.map((x) => x.name)) === JSON.stringify(COMMANDS) && route.role === 'frontend'
      && lf(route.claudeMd) === lf(starter('frontend', 'CLAUDE.md')), JSON.stringify(route).slice(0, 200));
  const backendRoute = await (await fetch(`http://127.0.0.1:${PORTS.viewer}/connector/workspace?role=backend`)).json();
  check('for the backend it also sends ADAM\'s script, .claude/scripts/db-ticket.mjs',
    JSON.stringify(backendRoute.scripts?.map((x) => x.name)) === '["db-ticket.mjs"]'
      && lf(backendRoute.scripts[0].text) === lf(starter('backend', '.claude', 'scripts', 'db-ticket.mjs')), JSON.stringify(backendRoute.scripts?.map((x) => x.name)));
  check('a role that is neither is refused',
    (await fetch(`http://127.0.0.1:${PORTS.viewer}/connector/workspace?role=..%2Fx`)).status === 400);

  const live = oldWorkspace('fe-live', 'frontend', { markers: true });
  const g = updater(live, [], { ADAM_VIEWER_URL: `http://127.0.0.1:${PORTS.viewer}` });
  check('**/update-adam on a connector that is already current still refreshes the workspace it is run in**',
    /already current/.test(g.text) && lf(read(live, '.claude', 'commands', 'ticket.md')) === lf(starter('frontend', '.claude', 'commands', 'ticket.md'))
      && !read(live, 'CLAUDE.md').includes('OLD TEXT'), g.text);
  const checkOnly = oldWorkspace('fe-check', 'frontend', { markers: true });
  const before = tree(checkOnly);
  updater(checkOnly, ['--check'], { ADAM_VIEWER_URL: `http://127.0.0.1:${PORTS.viewer}` });
  check('and --check leaves an old workspace as it was', changed(before, tree(checkOnly)).length === 0, changed(before, tree(checkOnly)).join(', '));

  // ── 8. an ADAM that names a file it should not ─────────────────────
  const liar = createServer((req, res) => {
    res.setHeader('content-type', 'application/json');
    if (req.url.startsWith('/connector/workspace')) {
      res.end(JSON.stringify({ role: 'frontend', claudeMd: '', commands: [{ name: '../../escaped.md', text: 'x' }, { name: 'ticket.md', text: 'ok' }] }));
    } else res.end('{}');
  });
  await new Promise((r) => liar.listen(PORTS.liar, '127.0.0.1', r));
  const trap = oldWorkspace('fe-trap', 'frontend', { markers: true });
  const trapBefore = tree(trap);
  const i = await updaterAsync(trap, ['--refresh-workspace', trap], { ADAM_VIEWER_URL: `http://127.0.0.1:${PORTS.liar}` });
  check('**a file name that is not one of ADAM\'s five is refused, and nothing at all is written**',
    changed(trapBefore, tree(trap)).length === 0 && !existsSync(path.join(T, 'escaped.md')) && /refused/i.test(i.text), i.text);
  liar.close();
} catch (error) {
  check('the check ran to the end', false, error.stack ?? String(error));
} finally {
  for (const child of children) {
    if (child.exitCode === null) spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], { windowsHide: true });
  }
  rmSync(T, { recursive: true, force: true });
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
