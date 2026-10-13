#!/usr/bin/env node
/**
 * What Claude Code did, recorded locally and sent to ADAM when the session ends.
 *
 * Claude Code runs on the developer's machine and ADAM does not, so the only
 * way ADAM can say how much the agent is being used — and which tools keep
 * failing — is for this to tell it.
 *
 * **Two modes, and the split is the whole design.** `record` is called on every
 * hook and does nothing but append a line to a file: no network, no sign-in, no
 * waiting, because it sits in the path of every tool call and a hook that costs
 * 200ms is a hook somebody removes. `flush` runs once when the session ends and
 * sends the file in one request.
 *
 * **It is deliberately narrow about what it writes down.** Which tool ran,
 * whether it worked, how long it took, and which ticket was open. Never the
 * prompt, never tool arguments, never file contents, never a command line.
 * Those are what would make this uncomfortable to keep, and a log that is
 * uncomfortable to keep gets turned off. The service drops anything else it is
 * sent, so this file being edited on somebody's laptop does not widen it.
 *
 * Nothing here may ever fail loudly. A hook that exits non-zero interrupts the
 * developer's work to report that a *statistics* upload did not happen, which
 * is a bad trade in every direction — so every path ends in exit 0.
 *
 * Install: setup.cmd and /update-adam put it into `~/.claude/settings.json`
 * (see hooks/README.md); the plugin wires it through hooks/hooks.json.
 *
 * **It sits beside client.mjs, not in hooks/.** The zip install is a flat copy
 * of the files `version.mjs` lists, and that list holds bare names so the
 * updater can refuse any path with a separator in it. One layout for both
 * installs means one import below, rather than a guess at which one this is.
 */

import { appendFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { realpathSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const MODE = process.argv[2] ?? 'record';

/** The connector folder: this file's own, in both installs. */
const HERE = path.dirname(fileURLToPath(import.meta.url));

/** Where the session's lines live until they are sent. Under the user's home
 *  rather than the repository: this is not the project's data and must not
 *  turn up in somebody's `git status`. */
const HOME = path.join(os.homedir(), '.adam', 'agent');

const stamp = (d = new Date()) => d.toISOString().replace(/\.\d+Z$/, 'Z');

/** A path as something two spellings of it can be compared on: resolved where
 *  it exists (a registration may spell the folder in Windows' short form,
 *  CHINMA~1.PAR, where Claude Code hands the long one), forward slashes, lower
 *  case, no trailing slash. Windows paths are case-blind, and VS Code and a
 *  terminal disagree about the drive letter. */
const real = (f) => { try { return realpathSync.native(f); } catch { return f; } };
const norm = (f) => real(String(f)).toLowerCase().replace(/\\/g, '/').replace(/\/+$/, '');

/**
 * Who to sign in as, and which folder the session belongs to.
 *
 * **The environment first, from whichever install exported it.** The plugin
 * collects the four values as `userConfig` and exports them to hook processes
 * as `CLAUDE_PLUGIN_OPTION_<KEY>`, the password out of the OS credential store.
 * `ADAM_*` is preferred over those so somebody debugging can override by hand.
 *
 * **Then the zip install's registration, which is where its password already
 * is.** A plain hook in settings.json gets no `ADAM_*`: setup hands them to the
 * connector's own process (`claude mcp add -e`), and Claude Code keeps that
 * registration in `~/.claude.json`. Reading it from there means the password
 * stays in the one place setup already put it, rather than being copied into
 * settings.json or a file of ours. Only an entry that launches *this*
 * connector's server.mjs counts — the same rule update.mjs uses for the
 * address — so a stranger's MCP server is never read.
 *
 * Which entry: the one registered for the session's folder, or for a folder it
 * is inside (Claude may have cd'd into `src`); else the every-folder one.
 *
 * Answers one of three things, because flush does three different things:
 * `{ creds, folder }` to send; `{ elsewhere: true }` when ADAM is set up on this
 * machine but not for this folder; `{}` when nothing says who you are at all.
 */
async function credentials(cwd) {
  const pick = (name, option) => process.env[name] || process.env[`CLAUDE_PLUGIN_OPTION_${option}`] || '';
  const fromEnv = {
    base: pick('ADAM_VIEWER_URL', 'VIEWER_URL'),
    project: pick('ADAM_PROJECT', 'PROJECT') || null,
    email: pick('ADAM_EMAIL', 'EMAIL'),
    password: pick('ADAM_PASSWORD', 'PASSWORD'),
  };
  if (fromEnv.email && fromEnv.password) return { creds: fromEnv, folder: cwd };

  let cfg;
  try {
    cfg = JSON.parse(await readFile(path.join(os.homedir(), '.claude.json'), 'utf8'));
  } catch {
    return {};
  }
  const server = norm(path.join(HERE, 'server.mjs'));
  const ours = (s) => Boolean(s?.env?.ADAM_EMAIL && s?.env?.ADAM_PASSWORD)
    && (s?.args ?? []).some((a) => norm(a) === server);
  const toCreds = (env) => ({
    base: env.ADAM_VIEWER_URL || '',
    project: env.ADAM_PROJECT || null,
    email: env.ADAM_EMAIL,
    password: env.ADAM_PASSWORD,
  });

  const here = norm(cwd);
  let best = null;
  let anywhere = false;
  for (const [folder, entry] of Object.entries(cfg.projects ?? {})) {
    const mine = Object.values(entry?.mcpServers ?? {}).find(ours);
    if (!mine) continue;
    anywhere = true;
    const f = norm(folder);
    if ((here === f || here.startsWith(`${f}/`)) && (!best || f.length > best.length)) {
      best = { length: f.length, folder, env: mine.env };
    }
  }
  if (best) return { creds: toCreds(best.env), folder: best.folder };
  const everywhere = Object.values(cfg.mcpServers ?? {}).find(ours);
  if (everywhere) return { creds: toCreds(everywhere.env), folder: cwd };
  return anywhere ? { elsewhere: true } : {};
}

async function readStdin() {
  const parts = [];
  for await (const chunk of process.stdin) parts.push(chunk);
  try { return JSON.parse(Buffer.concat(parts).toString('utf8')); } catch { return {}; }
}

/**
 * A word for what went wrong, from a tool result — never the message itself.
 *
 * The classification is here as well as in the service because the service
 * only ever sees the word: sending the message so it could be classified
 * centrally would be sending exactly the thing this is for not sending.
 */
function classify(response) {
  const text = typeof response === 'string' ? response : JSON.stringify(response ?? '');
  const low = text.toLowerCase();
  if (!low) return '';
  if (/timed? ?out|etimedout|deadline/.test(low)) return 'timeout';
  if (/permission|denied|not allowed|forbidden|refus/.test(low)) return 'refused';
  if (/enoent|no such file|not found|does not exist|404/.test(low)) return 'not-found';
  if (/conflict|already exists|409|merge conflict/.test(low)) return 'conflict';
  if (/abort|cancel|interrupt/.test(low)) return 'cancelled';
  return 'error';
}

/** Whether a tool result says it failed. Claude Code reports this differently
 *  per tool, so this asks the two questions that hold across all of them and
 *  treats anything else as success — over-reporting failure would make the
 *  page useless faster than under-reporting it. */
function failed(hook) {
  const r = hook.tool_response;
  if (r && typeof r === 'object') {
    if (r.is_error === true || r.isError === true || r.success === false) return true;
    if (typeof r.error === 'string' && r.error) return true;
  }
  if (typeof r === 'string' && /^\s*(error|exception)[: ]/i.test(r)) return true;
  return false;
}

/** The ticket being worked on, when the folder says so.
 *
 *  `adam_pull` writes .adam/work/<key>/, and ADAM_TICKET overrides it for
 *  somebody working outside that. No guessing beyond those two: a wrong ticket
 *  on a session is worse than none, because it is a number somebody will act on.
 */
async function ticketOf(cwd) {
  if (process.env.ADAM_TICKET) return String(process.env.ADAM_TICKET).replace(/^#/, '');
  try {
    const { readdir } = await import('node:fs/promises');
    const dirs = await readdir(path.join(cwd, '.adam', 'work'), { withFileTypes: true });
    const keys = dirs.filter((d) => d.isDirectory() && /^\d+$/.test(d.name)).map((d) => d.name);
    return keys.length === 1 ? keys[0] : '';
  } catch {
    return '';
  }
}

const fileFor = (key) => path.join(HOME, `${String(key ?? 'unknown').replace(/[^\w.-]/g, '_')}.jsonl`);

// ── record ───────────────────────────────────────────────────────────

async function record(hook) {
  const key = hook.session_id ?? 'unknown';
  const event = hook.hook_event_name ?? '';
  const now = Date.now();
  const line = { at: stamp(new Date(now)) };

  if (event === 'PreToolUse') {
    // Remembered so PostToolUse can say how long it took. Claude Code hands the
    // result without a start time, and a duration is most of what makes this
    // worth collecting — "Edit is failing" and "Edit takes 40 seconds" are
    // different problems with the same tool name.
    await writeFile(`${fileFor(key)}.pending`,
      JSON.stringify({ tool: hook.tool_name ?? '', at: now }), 'utf8').catch(() => {});
    return;
  }
  if (event === 'PostToolUse') {
    let began = now;
    try {
      const pending = JSON.parse(await readFile(`${fileFor(key)}.pending`, 'utf8'));
      if (pending.tool === (hook.tool_name ?? '')) began = pending.at;
    } catch { /* first tool of the session, or a pre that never landed */ }
    const bad = failed(hook);
    Object.assign(line, {
      kind: 'tool',
      tool: hook.tool_name ?? '',
      ok: !bad,
      error_kind: bad ? classify(hook.tool_response) : '',
      ms: Math.max(0, now - began),
    });
  } else if (event === 'UserPromptSubmit') {
    // That there was one, and when. Not a word of it — see the header.
    line.kind = 'prompt';
  } else if (event === 'Stop' || event === 'SubagentStop') {
    line.kind = 'stop';
  } else if (event === 'Notification') {
    line.kind = 'notify';
  } else {
    return;
  }

  await mkdir(HOME, { recursive: true }).catch(() => {});
  await appendFile(fileFor(key), `${JSON.stringify(line)}\n`, 'utf8').catch(() => {});
}

// ── flush ────────────────────────────────────────────────────────────

async function flush(hook) {
  const key = hook.session_id ?? 'unknown';
  const file = fileFor(key);
  let events = [];
  try {
    events = (await readFile(file, 'utf8')).split('\n').filter(Boolean)
      .map((l) => { try { return JSON.parse(l); } catch { return null; } })
      .filter(Boolean);
  } catch {
    return; // nothing recorded, nothing to send
  }
  if (!events.length) return;

  const cwd = hook.cwd || process.cwd();
  const { creds, folder, elsewhere } = await credentials(cwd);

  // **A folder ADAM is not connected to is not ADAM's session.** The hooks are
  // in the user's settings, so they run in every folder, but setup connects
  // ADAM to chosen folders only; a session in some other repository would
  // otherwise be filed against an ADAM project it has nothing to do with, and
  // read on the Agents page as work on it. Removed rather than kept: nothing
  // will ever send it, and a file that waits forever is a slow leak.
  if (elsewhere) {
    await rm(file, { force: true }).catch(() => {});
    await rm(`${file}.pending`, { force: true }).catch(() => {});
    return;
  }
  // Nobody to sign in as at all: kept, so connecting ADAM later is not too late.
  if (!creds) return;

  // The same client the connector uses, signing in as the same developer. That
  // is what makes the session land against the right person: there is no way to
  // file somebody else's time.
  const { ViewerClient } = await import('./client.mjs').catch(() => ({}));
  if (!ViewerClient) return;

  // `|| undefined`, not the empty string: the client defaults only a missing
  // address, and an empty one would send the request nowhere.
  const client = new ViewerClient({ ...creds, base: creds.base || undefined });
  const answer = await client.service('/api/agent/flush', {
    method: 'POST',
    body: {
      key,
      project_id: (await client.projectId().catch(() => '')) ?? '',
      // From the connected folder rather than wherever Claude last cd'd to:
      // .adam/work/ is at its top, and `src` is not the repository's name.
      external_key: await ticketOf(folder),
      // The folder's name, never its path: a path carries somebody's home
      // directory and sometimes a client's name.
      repo: path.basename(folder),
      host: os.hostname(),
      agent: 'claude-code',
      started_at: events[0].at,
      ended_at: stamp(),
      events,
    },
  }).catch(() => null);

  // Kept when the send failed, so an offline afternoon is a delay and not a
  // hole. Sending is idempotent on `key`, so a file that goes twice is one
  // session either way.
  if (answer?.ok) {
    await rm(file, { force: true }).catch(() => {});
    await rm(`${file}.pending`, { force: true }).catch(() => {});
  }
}

// Every path ends here, whatever happened. See the header: this must never be
// the reason somebody's session reports an error.
try {
  const hook = await readStdin();
  if (MODE === 'flush') await flush(hook);
  else await record(hook);
} catch { /* a statistics hook does not get to interrupt the work */ }
process.exit(0);
