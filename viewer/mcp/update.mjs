/**
 * Bring this connector up to what ADAM is serving.
 *
 *     node update.mjs                  # from the connector folder
 *     node update.mjs --check          # say whether an update exists, write nothing
 *     node update.mjs --install-hooks  # put the usage hooks into settings.json (setup runs this)
 *     node update.mjs --remove-hooks   # take ADAM's hooks out again (uninstall runs this)
 *     node update.mjs --refresh-workspace <folder> [--role backend|frontend|ai] [--from <starters>]
 *                                      # replace ADAM's command files, and CLAUDE.md between ADAM's markers
 *
 * **This downloads code and runs it afterwards, so it is written like something
 * that does.** Four rules, and each one closes a way this could go wrong:
 *
 *   **One address, and it is the one already configured.** The bundle is
 *   fetched from `ADAM_VIEWER_URL` — the same server this connector already
 *   reads the package from. There is no URL argument, so there is nothing to
 *   talk somebody into passing.
 *
 *   **Only the files that are already the connector.** A bundle entry whose
 *   path is not in `FILES` is refused. That list has no directories in it, so
 *   `../`, an absolute path, a drive letter and a backslash are all rejected by
 *   the same check rather than by three regexes that each miss something.
 *
 *   **Nothing is executed.** The bundle is text written to disk. There is no
 *   install script in it and no hook that runs one; the new code runs when the
 *   person restarts Claude Code, which is a thing they do knowingly. That holds
 *   for the usage hooks too: what this does about them is done by the code
 *   already running, never by the file that just arrived, and what it writes
 *   into settings.json only runs in sessions started after it.
 *
 *   **The old build is kept.** Replaced files are copied next door first, so a
 *   bad update is undone by copying them back, with no network involved.
 *
 * The connector cannot replace itself while it is running — the MCP server is
 * this process's own source — so the last thing this prints is the one manual
 * step: restart Claude Code.
 */

import { readFile, writeFile, mkdir, rename, copyFile, access } from 'node:fs/promises';
import { readFileSync, realpathSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { FILES, HERE, buildOf } from './version.mjs';

// **The address the connector was registered with, not a guess.** Setup hands
// ADAM_VIEWER_URL to the connector's own process (`claude mcp add -e`), so a
// shell running /update-adam does not have it and used to fall back to
// localhost, which is not where ADAM is for anybody but its own developer
// (7 October 2026). In order: the environment, the viewer-url.txt setup writes
// beside the connector, then the registration Claude Code keeps in
// ~/.claude.json for this connector's server.mjs (its URL only; nothing else
// in that entry is read). Still one configured address and no URL argument.
function configuredBase() {
  if (process.env.ADAM_VIEWER_URL) return [process.env.ADAM_VIEWER_URL, 'ADAM_VIEWER_URL'];
  try {
    const url = readFileSync(path.join(HERE, 'viewer-url.txt'), 'utf8').trim();
    if (/^https?:\/\//.test(url)) return [url, 'viewer-url.txt'];
  } catch { /* an install from before 7 October has none */ }
  try {
    const cfg = JSON.parse(readFileSync(path.join(os.homedir(), '.claude.json'), 'utf8'));
    // Resolved on both sides: a registration may spell the folder in Windows'
    // short form (CHINMA~1.PAR) where this file sees the long one.
    const real = (f) => { try { return realpathSync.native(f); } catch { return f; } };
    const norm = (f) => real(String(f)).toLowerCase().replace(/\\/g, '/');
    const mine = norm(path.join(HERE, 'server.mjs'));
    const servers = [cfg.mcpServers ?? {}, ...Object.values(cfg.projects ?? {}).map((p) => p?.mcpServers ?? {})];
    for (const group of servers) {
      for (const s of Object.values(group)) {
        const args = (s?.args ?? []).map(norm);
        const url = s?.env?.ADAM_VIEWER_URL;
        if (url && args.some((a) => a === mine)) return [url, 'the connector registration in ~/.claude.json'];
      }
    }
  } catch { /* no readable registration */ }
  return ['http://127.0.0.1:4173', 'the default'];
}
const [CONFIGURED, FROM] = configuredBase();
const BASE = CONFIGURED.replace(/\/+$/, '');
const CHECK_ONLY = process.argv.includes('--check');
const INSTALL_HOOKS = process.argv.includes('--install-hooks');
const REMOVE_HOOKS = process.argv.includes('--remove-hooks');

// Which files this build is made of, sent with every question so the viewer
// answers about the same set. An updater that sends nothing is taken to be one
// from before the hooks joined, and is offered only what it accepts.
const ACCEPT = `?accept=${FILES.join(',')}`;

// Long enough for a server on the other side of a VPN, short enough that a
// machine which cannot reach ADAM says so rather than appearing to hang.
const PATIENCE = 15000;

const say = (...parts) => console.log('[adam]', ...parts);

async function ask(route) {
  const res = await fetch(`${BASE}${route}`, {
    signal: AbortSignal.timeout(PATIENCE),
    headers: { accept: 'application/json' },
  });
  if (!res.ok) throw new Error(`${route} answered ${res.status}`);
  return res.json();
}

/** Every path a bundle is allowed to carry. Membership, not pattern matching:
 *  the list holds bare file names, so anything with a separator in it fails by
 *  not being in the list rather than by being caught. */
const ALLOWED = new Set(FILES);

/**
 * Whether these files are a plugin's copy rather than a zip install.
 *
 * **Checked on disk, not from the environment.** `CLAUDE_PLUGIN_ROOT` reaches
 * the MCP server process, but this script is run by hand from a shell, where
 * that variable is not set — so asking the environment would answer "not a
 * plugin" every time and the guard would never fire. A zip install is a copy of
 * the six files in `FILES` and carries no manifest, so the manifest sitting
 * beside them is the honest signal.
 */
async function installedAsPlugin() {
  return readFile(path.join(HERE, '.claude-plugin', 'plugin.json'), 'utf8')
    .then(() => true, () => false);
}

// ── the usage hooks ──────────────────────────────────────────────────
//
// adam-hook.mjs is what fills the Agents page, and a hook does nothing until
// Claude Code's settings name it. The plugin names it in hooks/hooks.json; a
// zip install has no such file, so the hooks go into the user's own
// settings.json. User scope rather than a project's: one entry covers every
// folder, and the hook itself drops sessions from folders ADAM is not
// connected to, so nothing outside ADAM's folders is ever sent.
//
// **Somebody else's file, edited like one.** Read whole, ADAM's own entries
// taken out, ADAM's five put back, written whole — every other setting and
// every other hook stays as it was. Ours are recognised by the script they
// run, adam-hook.mjs, wherever it lives: that also catches an entry pasted by
// hand from the old README or left by an install elsewhere, which would
// otherwise record every tool call twice. A file that is not a JSON object is
// not touched at all; a settings file half-rewritten by a script that guessed
// is a broken Claude Code, which is worse than a missing statistic.

const SETTINGS = path.join(os.homedir(), '.claude', 'settings.json');
const HOOK = path.join(HERE, 'adam-hook.mjs');
// Written the first time the hooks go in. Without it, an update could not tell
// "never installed" from "somebody took them out on purpose", and would put
// them back on every update, overruling somebody who turned them off.
const MARK = path.join(HERE, 'hooks-installed.txt');

/** The five events and the mode each runs, as hooks/hooks.json has them. */
const EVENTS = [
  ['PreToolUse', 'record'],
  ['PostToolUse', 'record'],
  ['UserPromptSubmit', 'record'],
  ['Stop', 'record'],
  ['SessionEnd', 'flush'],
];

/**
 * The command a hook runs, as one string Claude Code hands to a shell.
 *
 * **Forward slashes, in single quotes.** On Windows Claude Code runs a hook
 * through Git Bash when there is one and PowerShell when there is not, so the
 * line has to mean the same in both. Single quotes are literal in both — no
 * `$`, backtick or backslash is read — and node takes forward slashes on
 * Windows, so `C:/Users/A B/.adam/connector/adam-hook.mjs` survives a space in
 * the user name and either shell. A quote in the path itself (O'Brien) cannot
 * be single-quoted in a way both shells agree on, so that one falls back to
 * double quotes, which a Windows path can never contain.
 *
 * Not exec form (`command` + `args`), which avoids a shell altogether: the
 * plugin uses it, but a Claude Code too old to know `args` would run a bare
 * `node` with the hook's JSON on its standard input, on every tool call.
 */
function commandFor(mode) {
  const file = HOOK.replace(/\\/g, '/');
  const quoted = file.includes("'") ? `"${file}"` : `'${file}'`;
  return `node ${quoted} ${mode}`;
}

/** Timeouts and async as hooks/hooks.json: `record` never makes a tool call
 *  wait, `flush` is the one network call and gets the session's last 30s. */
function entryFor(mode) {
  return mode === 'flush'
    ? { type: 'command', command: commandFor(mode), timeout: 30 }
    : { type: 'command', command: commandFor(mode), timeout: 10, async: true };
}

const isOurs = (hook) => [hook?.command, ...(Array.isArray(hook?.args) ? hook.args : [])]
  .some((part) => typeof part === 'string' && /adam-hook\.mjs(?=$|['"\s])/.test(part.replace(/\\/g, '/')));

/** The settings, or why they cannot be edited safely. A missing file is an
 *  empty one; Claude Code creates it the same way. */
async function readSettings() {
  let text;
  try {
    text = await readFile(SETTINGS, 'utf8');
  } catch (error) {
    if (error.code === 'ENOENT') return { settings: {}, existed: false };
    return { problem: `could not be read (${error.code ?? error.message})` };
  }
  let settings;
  try {
    // A byte-order mark is what PowerShell leaves when it writes the file; it
    // is not part of the JSON and JSON.parse refuses it.
    settings = JSON.parse(text.replace(/^\uFEFF/, ''));
  } catch {
    return { problem: 'is not valid JSON' };
  }
  if (!settings || typeof settings !== 'object' || Array.isArray(settings)) {
    return { problem: 'is not a JSON object' };
  }
  const hooks = settings.hooks;
  if (hooks !== undefined && (!hooks || typeof hooks !== 'object' || Array.isArray(hooks))) {
    return { problem: 'has a "hooks" that is not an object' };
  }
  if (hooks && Object.values(hooks).some((groups) => !Array.isArray(groups))) {
    return { problem: 'has a hook event that is not a list' };
  }
  return { settings, existed: true };
}

/** The settings without ADAM's entries. A group or an event is dropped only
 *  when taking ours out emptied it; one that was already empty is left. */
function withoutOurs(settings) {
  const out = structuredClone(settings);
  if (!out.hooks) return out;
  for (const [event, groups] of Object.entries(out.hooks)) {
    const kept = [];
    for (const group of groups) {
      if (!Array.isArray(group?.hooks)) { kept.push(group); continue; }
      const left = group.hooks.filter((hook) => !isOurs(hook));
      if (left.length === group.hooks.length) kept.push(group);
      else if (left.length) kept.push({ ...group, hooks: left });
    }
    if (kept.length || !groups.length) out.hooks[event] = kept;
    else delete out.hooks[event];
  }
  if (!Object.keys(out.hooks).length && Object.keys(settings.hooks).length) delete out.hooks;
  return out;
}

function withOurs(settings) {
  const out = withoutOurs(settings);
  out.hooks ??= {};
  for (const [event, mode] of EVENTS) {
    out.hooks[event] = [...(out.hooks[event] ?? []), { hooks: [entryFor(mode)] }];
  }
  return out;
}

/** 'on' when exactly ADAM's five are there and run this folder's hook;
 *  'stale' when some of ours are there but not those; 'off' when none are. */
function hooksState(settings) {
  const ours = Object.entries(settings.hooks ?? {}).flatMap(([event, groups]) => groups
    .flatMap((group) => (Array.isArray(group?.hooks) ? group.hooks : []))
    .filter(isOurs)
    .map((hook) => [event, hook]));
  if (!ours.length) return 'off';
  const exact = EVENTS.every(([event, mode]) => ours.some(([e, hook]) => e === event
    && JSON.stringify(hook) === JSON.stringify(entryFor(mode))));
  return exact && ours.length === EVENTS.length ? 'on' : 'stale';
}

/**
 * Write the settings back, keeping the file as it was beside it first.
 *
 * Only when something changed, so running setup twice leaves one backup and
 * not a drawer full. Written beside and renamed into place: Claude Code reads
 * this file on every start, and half a file is a Claude Code that will not.
 */
async function writeSettings(next, existed) {
  await mkdir(path.dirname(SETTINGS), { recursive: true });
  let backup = '';
  if (existed) {
    const at = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 15);
    backup = `${SETTINGS}.adam-${at}.bak`;
    await copyFile(SETTINGS, backup);
  }
  const temporary = `${SETTINGS}.adam-incoming`;
  await writeFile(temporary, `${JSON.stringify(next, null, 2)}\n`, 'utf8');
  await rename(temporary, SETTINGS);
  return backup;
}

/** The one line for a settings file this will not edit: what to fix, and
 *  exactly what to add by hand if they would rather. */
function byHand(problem) {
  say(`${SETTINGS} ${problem}, so it was left exactly as it is. To turn on the usage hooks, `
    + `fix it and run  node "${path.join(HERE, 'update.mjs')}" --install-hooks  , or add them by hand `
    + `under "hooks": PreToolUse, PostToolUse, UserPromptSubmit and Stop running  ${commandFor('record')}  `
    + `and SessionEnd running  ${commandFor('flush')}`);
}

/**
 * Put ADAM's hooks in, replacing any of ours already there. `why` is printed
 * with the result; the return is whether settings.json now has them.
 */
async function installHooks() {
  if (!await access(HOOK).then(() => true, () => false)) {
    say(`adam-hook.mjs is not in ${HERE}, so there is no hook to install yet. Run /update-adam.`);
    return false;
  }
  const { settings, existed, problem } = await readSettings();
  if (problem) { byHand(problem); return false; }
  const next = withOurs(settings);
  if (JSON.stringify(next) === JSON.stringify(settings)) {
    say('usage hooks: already on in', SETTINGS);
  } else {
    const backup = await writeSettings(next, existed);
    say(`usage hooks: on, in ${SETTINGS}${backup ? ` (the file as it was is ${path.basename(backup)})` : ''}.`);
    say('They start with the next Claude Code session. What they send is listed in README.txt in the setup zip.');
  }
  await writeFile(MARK, `${new Date().toISOString()}\n`, 'utf8').catch(() => {});
  return true;
}

async function removeHooks() {
  const { settings, existed, problem } = await readSettings();
  if (problem) {
    say(`${SETTINGS} ${problem}, so it was left as it is. Remove any hook running adam-hook.mjs from it by hand.`);
    return false;
  }
  if (!existed || hooksState(settings) === 'off') {
    say('usage hooks: none of ADAM\'s in', SETTINGS);
    return true;
  }
  const backup = await writeSettings(withoutOurs(settings), existed);
  say(`usage hooks: removed from ${SETTINGS}; nothing else in it changed (the file as it was is ${path.basename(backup)}).`);
  return true;
}

/**
 * After an update, or finding none: make sure the hooks are there.
 *
 * **Installed, not just suggested, the first time** — the developer asked for
 * the build ADAM is serving, the hooks are part of it, and a line telling them
 * to run a second command is a line that gets read and not run (the hooks sat
 * in a README for weeks and reached nobody). It is the same edit setup makes,
 * with the same backup and the same refusal to touch a file it cannot read.
 *
 * **Never put back once taken out.** If this machine had them and somebody
 * removed them, that was a decision, and an updater that reverses it on every
 * run is one people learn to stop running. Said in one line, with the command.
 */
async function ensureHooks() {
  if (!await access(HOOK).then(() => true, () => false)) return;
  const { settings, problem } = await readSettings();
  if (problem) { byHand(problem); return; }
  const state = hooksState(settings);
  if (state === 'on') return;
  if (state === 'off' && await access(MARK).then(() => true, () => false)) {
    say(`usage hooks: off on this machine (taken out of settings.json). To turn them back on: node "${path.join(HERE, 'update.mjs')}" --install-hooks`);
    return;
  }
  await installHooks();
}

/** --check: where the hooks stand, written nowhere. */
async function sayHooks() {
  if (!await access(HOOK).then(() => true, () => false)) return;
  if (await installedAsPlugin()) { say('usage hooks: wired by the plugin itself'); return; }
  const { settings, problem } = await readSettings();
  if (problem) { say(`usage hooks: cannot tell — ${SETTINGS} ${problem}`); return; }
  const state = hooksState(settings);
  say(`usage hooks: ${state === 'stale' ? 'present, but not this build\'s; an update replaces them' : state}`);
}

async function hooksOnly() {
  // A plugin wires the hook through its own hooks.json; ADAM's entries in
  // settings.json as well would record every tool call twice.
  if (await installedAsPlugin()) {
    say('this is the ADAM plugin, whose hooks come with it. Nothing to do here.');
    process.exit(2);
  }
  const done = INSTALL_HOOKS ? await installHooks() : await removeHooks();
  process.exit(done ? 0 : 5);
}

// ── ADAM's own files in the workspace ────────────────────────────────
//
// Setup only ever added the files a folder lacked, and this script only replaced the connector, so a workspace made
// before a change kept its old /ticket, /board and CLAUDE.md for good (18 October 2026, CHG-ADM-006). Now:
//
//   **The five command files are ADAM's** (`.claude/commands/ticket|board|cr|done|update-adam.md`): an existing one
//   that differs is replaced, the old one kept in `.adam/backup-workspace-<time>/`. One that is missing is not
//   created here - setup adds missing files and keeps them out of git, and this does not know the repository.
//
//   **ADAM's scripts are ADAM's too** (the backend's `.claude/scripts/db-ticket.mjs`, 20 October 2026): one that
//   differs is replaced (the old one kept), and one that is missing is added, because the [DB] rule in the new
//   /ticket and /done runs it. In a git repository the added file goes into `.git/info/exclude`, as setup does.
//
//   **CLAUDE.md is the team's.** Only a section between ADAM's markers (`<!-- ADAM:start name -->` ...
//   `<!-- ADAM:end name -->`, in the starters) is replaced, and the text around it is never touched. A CLAUDE.md
//   that has ADAM's section but no markers (made before them) keeps that section as it is: one line says which
//   section to replace, and the new text is written to `.adam/new-claude-sections.md` to copy from.
//   A section that is new (`add`: "A [DB] ticket") and nowhere in the file yet, marked or not, is added whole with
//   its markers - after the "Working a ticket (ADAM)" section's end marker when there is one, else at the end -
//   so nobody copies it by hand; no line of the team's is changed.
//
// Where the new text comes from: the same ADAM this connector already reads (`/connector/workspace`), or - setup,
// which has the starters in the unzipped folder - `--from <starters folder>`. Names are taken only from the lists
// below, so an answer naming anything else is refused whole, as for the connector's own files.

const COMMAND_NAMES = ['ticket.md', 'board.md', 'cr.md', 'done.md', 'update-adam.md'];
const SECTIONS = {
  'working-a-ticket': {
    title: 'Working a ticket (ADAM)', seen: '## Working a ticket (ADAM)',
  },
  'open-the-workspace': {
    title: 'the paragraph that starts "Open Claude Code in this folder"',
    seen: 'Open Claude Code in this folder, not in a repository folder',
  },
  'db-ticket': {
    title: 'A [DB] ticket', seen: '## A [DB] ticket', add: true,
  },
};
/** Scripts ADAM owns under .claude/scripts, per role; any other name in an answer is refused. */
const SCRIPT_NAMES = { backend: ['db-ticket.mjs'], frontend: [], ai: [] };
/** Whether a script's text is ADAM's (its own header names it), so one of the team's under the same name stays. */
const isAdamsScript = (name, text) => text.includes(`.claude/scripts/${name}`) && text.includes('expected-schema.json');
const argAfter = (flag) => {
  const at = process.argv.indexOf(flag);
  return at >= 0 ? process.argv[at + 1] : undefined;
};
const REFRESH_DIR = argAfter('--refresh-workspace');
const lf = (text) => String(text).replace(/\r\n/g, '\n');
const readOrNull = (file) => readFile(file, 'utf8').catch(() => null);

/** backend, frontend or ai, from the folder's own files; null when they do not say. */
async function roleOf(folder) {
  const ticket = await readOrNull(path.join(folder, '.claude', 'commands', 'ticket.md')) ?? '';
  const claude = await readOrNull(path.join(folder, 'CLAUDE.md')) ?? '';
  if (/dotnet test/i.test(ticket)) return 'backend';
  // An AI engineer's folder (the `ai` role, 20 Oct 2026): its /ticket runs pytest.
  if (/`pytest`/.test(ticket)) return 'ai';
  if (/lint, typecheck|screen or contract|repository for the ticket's platform/i.test(ticket)) return 'frontend';
  if (/dotnet/i.test(claude)) return 'backend';
  if (/workspace|pnpm|package\.json/i.test(claude)) return 'frontend';
  return null;
}

/**
 * Keeps a file this added out of git, as setup does: a line in the repository's own `info/exclude`, which is never
 * committed. Only at the top of a repository; a folder that is not one is left as it is.
 */
async function excludeInGit(folder, line) {
  try {
    const dotGit = path.join(folder, '.git');
    let gitDir = dotGit;
    const asFile = await readOrNull(dotGit);
    if (asFile !== null) {
      // A worktree or submodule: `.git` is a file naming the real one, whose common folder holds info/exclude.
      const named = /^gitdir:\s*(.+)$/m.exec(asFile)?.[1]?.trim();
      if (!named) return;
      gitDir = path.resolve(folder, named);
      const common = (await readOrNull(path.join(gitDir, 'commondir')))?.trim();
      if (common) gitDir = path.resolve(gitDir, common);
    }
    await access(gitDir);
    const file = path.join(gitDir, 'info', 'exclude');
    const have = (await readOrNull(file)) ?? '';
    if (have.split(/\r?\n/).includes(line)) return;
    await mkdir(path.dirname(file), { recursive: true });
    await writeFile(file, `${have}${have && !have.endsWith('\n') ? '\n' : ''}${line}\n`, 'utf8');
  } catch { /* not a repository, or one this cannot write: the file is still there */ }
}

/** Whether a command file's text is ADAM's: they all call ADAM's tools (adam_*) or its updater (update-adam.md). */
const isAdamsCommand = (text) => /adam_|update\.mjs/.test(text);

/**
 * Whether this folder is an ADAM workspace: its /ticket calls ADAM's tools. A generic board.md or done.md is not
 * enough - an app clone can have its own, and those are the team's (found in review, 18 October 2026).
 */
async function hasAdamCommands(folder) {
  const ticket = await readOrNull(path.join(folder, '.claude', 'commands', 'ticket.md'));
  return ticket !== null && ticket.includes('adam_pull');
}

/** What the workspace should hold, from ADAM or from a starters folder; refused whole if it names anything else. */
async function workspaceSource(role, startersDir) {
  let got;
  if (startersDir) {
    const commands = [];
    for (const name of COMMAND_NAMES) {
      const text = await readOrNull(path.join(startersDir, role, '.claude', 'commands', name));
      if (text !== null) commands.push({ name, text });
    }
    const scripts = [];
    for (const name of SCRIPT_NAMES[role] ?? []) {
      const text = await readOrNull(path.join(startersDir, role, '.claude', 'scripts', name));
      if (text !== null) scripts.push({ name, text });
    }
    got = { role, commands, scripts, claudeMd: await readOrNull(path.join(startersDir, role, 'CLAUDE.md')) ?? '' };
  } else {
    got = await ask(`/connector/workspace?role=${role}`);
  }
  const commands = Array.isArray(got?.commands) ? got.commands : [];
  // An ADAM from before scripts sends none: then there is simply nothing to refresh.
  const scripts = Array.isArray(got?.scripts) ? got.scripts : [];
  const odd = [
    ...commands.filter((c) => !COMMAND_NAMES.includes(c?.name) || typeof c.text !== 'string'),
    ...scripts.filter((c) => !(SCRIPT_NAMES[role] ?? []).includes(c?.name) || typeof c.text !== 'string'),
  ];
  if (odd.length || typeof got?.claudeMd !== 'string') {
    const error = new Error('refused: the workspace files name something that is not one of ADAM\'s: '
      + `${odd.map((c) => String(c?.name)).join(', ') || 'CLAUDE.md'}`);
    error.refused = true;
    throw error;
  }
  return { commands, scripts, claudeMd: got.claudeMd };
}

const markedRe = (name) => new RegExp(`(<!-- ADAM:start ${name} -->\\r?\\n)([\\s\\S]*?)(<!-- ADAM:end ${name} -->)`);

/** The marked sections of a starter CLAUDE.md that this updater knows, as name -> text between the markers. */
function sectionsOf(markdown) {
  const out = {};
  for (const m of lf(markdown).matchAll(/<!-- ADAM:start ([a-z0-9-]+) -->\n([\s\S]*?)<!-- ADAM:end \1 -->/g)) {
    if (m[1] in SECTIONS) out[m[1]] = m[2];
  }
  return out;
}

/**
 * Bring the workspace's ADAM-owned files up to `source`. Says what it did; `quiet` says nothing when there was
 * nothing to do (the update's own path, which has already said "already current"). Returns what changed.
 */
async function refreshWorkspace(folder, source, quiet) {
  const stamp = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 15);
  const kept = path.join(folder, '.adam', `backup-workspace-${stamp}`);
  const keep = async (name, text) => {
    await mkdir(kept, { recursive: true });
    await writeFile(path.join(kept, name), text, 'utf8');
  };
  const changed = [];

  for (const name of COMMAND_NAMES) {
    const target = path.join(folder, '.claude', 'commands', name);
    const have = await readOrNull(target);
    const want = source.commands.find((c) => c.name === name);
    // Only a file that is ADAM's: one the team wrote under the same name stays theirs.
    if (have === null || !want || !isAdamsCommand(have) || lf(have) === lf(want.text)) continue;
    await keep(name, have);
    await writeFile(target, want.text, 'utf8');
    changed.push(name);
  }
  if (changed.length) {
    say(`workspace: refreshed ${changed.map((n) => `.claude/commands/${n}`).join(', ')} in ${folder} `
      + `(the old ones are in ${kept}).`);
  }

  // ADAM's scripts: replaced when they differ, added when missing (the new /ticket and /done run them).
  const scriptsDone = [];
  for (const { name, text } of source.scripts ?? []) {
    const target = path.join(folder, '.claude', 'scripts', name);
    const have = await readOrNull(target);
    if (have !== null && (lf(have) === lf(text) || !isAdamsScript(name, have))) continue;
    if (have !== null) await keep(name, have);
    await mkdir(path.dirname(target), { recursive: true });
    await writeFile(target, text, 'utf8');
    if (have === null) await excludeInGit(folder, `/.claude/scripts/${name}`);
    scriptsDone.push(have === null ? `added .claude/scripts/${name}`
      : `refreshed .claude/scripts/${name} (the old one is in ${kept})`);
    changed.push(name);
  }
  if (scriptsDone.length) say(`workspace: ${scriptsDone.join(', ')} in ${folder}.`);

  const mdPath = path.join(folder, 'CLAUDE.md');
  const local = await readOrNull(mdPath);
  const unmarked = [];
  if (local !== null) {
    // The file's own bytes stay as they are: only the text between ADAM's markers is swapped, written with the
    // file's line endings, so a team's lines are never re-ended.
    const crlf = /\r\n/.test(local);
    const eol = (s) => (crlf ? s.replace(/\n/g, '\r\n') : s);
    let text = local;
    const done = [];
    for (const [name, inner] of Object.entries(sectionsOf(source.claudeMd))) {
      const re = markedRe(name);
      const at = text.match(re);
      if (at) {
        if (lf(at[2]) !== inner) {
          const put = eol(inner);
          text = text.replace(re, (_, a, _old, b) => a + put + b);
          done.push(name);
        }
      } else if (text.includes(SECTIONS[name].seen)) {
        unmarked.push(name);
      } else if (SECTIONS[name].add) {
        // A new section the file has never had: added whole, with its markers, so /update-adam keeps it
        // current from then on. After "Working a ticket (ADAM)" when that is marked, else at the end.
        const block = eol(`<!-- ADAM:start ${name} -->\n${inner}<!-- ADAM:end ${name} -->\n`);
        const after = text.match(/<!-- ADAM:end working-a-ticket -->\r?\n/);
        if (after) {
          const at2 = after.index + after[0].length;
          text = `${text.slice(0, at2)}${eol('\n')}${block}${text.slice(at2)}`;
        } else {
          text = `${text}${/\n$/.test(text) ? '' : eol('\n')}${eol('\n')}${block}`;
        }
        done.push(name);
      }
    }
    if (done.length) {
      await keep('CLAUDE.md', local);
      await writeFile(mdPath, text, 'utf8');
      say(`workspace: CLAUDE.md ${done.map((n) => `"${SECTIONS[n].title}"`).join(' and ')} refreshed between its ADAM `
        + `markers (a section it did not have yet is added with them); the rest of the file is yours and was not `
        + `touched (the old file is in ${kept}).`);
      changed.push('CLAUDE.md');
    }
  }
  if (unmarked.length) {
    const fresh = path.join(folder, '.adam', 'new-claude-sections.md');
    const sections = sectionsOf(source.claudeMd);
    await mkdir(path.dirname(fresh), { recursive: true });
    await writeFile(fresh, '# New text for CLAUDE.md\n\nReplace each section in CLAUDE.md with the text under its '
      + 'heading here. Keep the ADAM:start and ADAM:end comment lines around it: with them, /update-adam refreshes '
      + 'the section for you from then on.\n\n'
      + unmarked.map((n) => `<!-- section: ${SECTIONS[n].title} -->\n${sections[n]}`).join('\n'), 'utf8');
    // One wording whether or not another section was added on the same run: it names only what has no markers.
    const titles = unmarked.map((n) => `"${SECTIONS[n].title}"`).join(' and ');
    const one = unmarked.length === 1;
    say(`workspace: CLAUDE.md's ${titles} ${one ? 'section has' : 'sections have'} no ADAM markers, so `
      + `${one ? 'it was' : 'they were'} left as ${one ? 'it is' : 'they are'}. Replace ${one ? 'it' : 'them'} with the `
      + `new text in ${fresh}.`);
  }
  if (!changed.length && !unmarked.length && !quiet) {
    say(`workspace: already current - nothing to refresh in ${folder}.`);
  }
  return changed;
}

/** `--refresh-workspace <folder> [--role r] [--from <starters>]`: setup's call, and the same code /update-adam runs. */
async function refreshOnly() {
  const folder = path.resolve(REFRESH_DIR);
  if (!await hasAdamCommands(folder)) {
    say(`workspace: ${folder} is not an ADAM workspace (its .claude/commands/ticket.md does not call adam_pull), so nothing was written.`);
    return;
  }
  const role = argAfter('--role') ?? await roleOf(folder);
  if (!['backend', 'frontend', 'ai'].includes(role)) {
    say(`workspace: could not tell a backend, frontend or AI folder in ${folder}. `
      + 'Run again with  --role backend,  --role frontend  or  --role ai.');
    process.exit(2);
  }
  let source;
  try {
    source = await workspaceSource(role, argAfter('--from'));
  } catch (error) {
    say(error.refused ? error.message
      : `could not read the workspace files from ADAM at ${BASE} (from ${FROM}) - ${error.message}`);
    process.exit(error.refused ? 3 : 2);
  }
  await refreshWorkspace(folder, source, false);
}

/** After an update, or finding none: the workspace this was run in, when it is one. Never fails the update. */
async function refreshHere() {
  try {
    const folder = process.cwd();
    if (!await hasAdamCommands(folder)) return;
    const role = await roleOf(folder);
    if (!role) return;
    await refreshWorkspace(folder, await workspaceSource(role), true);
  } catch (error) {
    say(`workspace files not refreshed - ${error.message}`);
  }
}

async function main() {
  if (INSTALL_HOOKS || REMOVE_HOOKS) return hooksOnly();
  if (REFRESH_DIR) return refreshOnly();
  const mine = await buildOf(HERE);

  // **A plugin updates through the marketplace and must not be written here.**
  // Claude Code replaces the whole plugin directory when the plugin updates, so
  // anything this wrote would work until the next `/plugin update` silently
  // reverted it — and the developer would be on a build ADAM thinks they are
  // not. `--check` still reports, because answering "which build am I on" is
  // useful in both installs and writes nothing.
  if (await installedAsPlugin() && !CHECK_ONLY) {
    say(`this is the ADAM plugin (build ${mine}), which updates through the marketplace.`);
    say('Run:  /plugin update adam@adam');
    say('Then restart Claude Code. Use --check here if you only want the build.');
    process.exit(2);
  }

  let theirs;
  try {
    theirs = await ask(`/connector/version${ACCEPT}`);
  } catch (error) {
    say(`could not reach ADAM at ${BASE} (from ${FROM}) — ${error.message}`);
    say('If ADAM is on another machine, set ADAM_VIEWER_URL and try again.');
    process.exit(2);
  }

  if (!theirs?.build) {
    say(`${BASE} does not serve connector updates. It may be an older ADAM.`);
    process.exit(2);
  }

  if (theirs.build === mine) {
    say(`already current — build ${mine}`);
    // Still worth a look: an install that took the hook when settings.json
    // could not be read gets it now that it can.
    if (CHECK_ONLY) await sayHooks();
    else { await ensureHooks(); await refreshHere(); }
    return;
  }

  say(`an update is available: ${mine} -> ${theirs.build}`);
  if (CHECK_ONLY) { await sayHooks(); return; }

  const bundle = await ask(`/connector/bundle${ACCEPT}`);
  const files = bundle?.files ?? [];
  const refused = files.filter((f) => !ALLOWED.has(f?.path));
  if (refused.length) {
    // Refused whole rather than partly applied. A bundle carrying a path this
    // connector does not recognise is not a bundle to take the good half of.
    say('refused: the bundle names files that are not part of the connector —',
      refused.map((f) => String(f?.path)).join(', '));
    process.exit(3);
  }
  if (!files.length) {
    say('refused: the bundle is empty.');
    process.exit(3);
  }
  // Every file, or none. Half a connector does not start.
  const missing = FILES.filter((name) => !files.some((f) => f.path === name));
  if (missing.length) {
    say('refused: the bundle is missing', missing.join(', '));
    process.exit(3);
  }

  const backup = path.join(HERE, `backup-${mine}`);
  await mkdir(backup, { recursive: true });
  for (const name of FILES) {
    await copyFile(path.join(HERE, name), path.join(backup, name)).catch(() => {});
  }

  // Written beside the target and renamed into place: a half-written tools.mjs
  // is a connector that will not start, and a crash mid-write is exactly when
  // somebody least wants to debug one.
  for (const file of files) {
    const target = path.join(HERE, file.path);
    const temporary = `${target}.incoming`;
    await writeFile(temporary, file.text, 'utf8');
    await rename(temporary, target);
  }

  const now = await buildOf(HERE);
  if (now !== theirs.build) {
    // Said rather than swallowed. The backup is right there, and a connector
    // that hashes to something nobody expected should not be trusted silently.
    say(`warning: after writing, this reads as ${now} and ADAM offered ${theirs.build}.`);
    say(`The previous build is in ${backup} if you want it back.`);
    process.exit(4);
  }

  say(`updated to ${now}. The previous build is in ${backup}.`);
  await ensureHooks();
  // The code running is the one just replaced, so a refresh that arrived with this update is made by the next run.
  await refreshHere();
  say('This update also brings the part that refreshes the ADAM files in your workspace, and it can only start on the next run: '
    + 'run /update-adam once more, from your workspace folder (or re-run setup.cmd).');
  say('Restart Claude Code to load it — the running connector is still the old one.');
}

main().catch((error) => {
  say('update failed —', error.message);
  process.exit(1);
});
