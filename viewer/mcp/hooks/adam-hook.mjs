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
 * Install: see hooks/README.md.
 */

import { appendFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

const MODE = process.argv[2] ?? 'record';

/** Where the session's lines live until they are sent. Under the user's home
 *  rather than the repository: this is not the project's data and must not
 *  turn up in somebody's `git status`. */
const HOME = path.join(os.homedir(), '.adam', 'agent');

const stamp = (d = new Date()) => d.toISOString().replace(/\.\d+Z$/, 'Z');

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

  // The same client the connector uses, signing in as the same developer with
  // the same ADAM_EMAIL / ADAM_PASSWORD. That is what makes the session land
  // against the right person: there is no way to file somebody else's time.
  const { ViewerClient } = await import('../client.mjs').catch(() => ({}));
  if (!ViewerClient) return;

  const cwd = hook.cwd || process.cwd();
  const client = new ViewerClient({
    base: process.env.ADAM_VIEWER_URL,
    project: process.env.ADAM_PROJECT || null,
    email: process.env.ADAM_EMAIL,
    password: process.env.ADAM_PASSWORD,
  });
  const answer = await client.service('/api/agent/flush', {
    method: 'POST',
    body: {
      key,
      project_id: (await client.projectId().catch(() => '')) ?? '',
      external_key: await ticketOf(cwd),
      // The folder's name, never its path: a path carries somebody's home
      // directory and sometimes a client's name.
      repo: path.basename(cwd),
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
