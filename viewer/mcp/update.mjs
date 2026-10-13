/**
 * Bring this connector up to what ADAM is serving.
 *
 *     node update.mjs                  # from the connector folder
 *     node update.mjs --check          # say whether an update exists, write nothing
 *     node update.mjs --install-hooks  # put the usage hooks into settings.json (setup runs this)
 *     node update.mjs --remove-hooks   # take ADAM's hooks out again (uninstall runs this)
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

async function main() {
  if (INSTALL_HOOKS || REMOVE_HOOKS) return hooksOnly();
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
    else await ensureHooks();
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
  say('Restart Claude Code to load it — the running connector is still the old one.');
}

main().catch((error) => {
  say('update failed —', error.message);
  process.exit(1);
});
