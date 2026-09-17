#!/usr/bin/env node
/**
 * The ADAM context bridge — MCP server, phases 1 and 2. Read-only.
 *
 * Nine tools over the viewer's existing read routes. **No new server route in
 * either phase** — the plan listed `module` and `service` as missing and both
 * were already being served, under other names. No writes, no OpenProject.
 *
 * **Zero dependencies, on purpose.** MCP over stdio is newline-delimited
 * JSON-RPC 2.0 and the handshake is four methods, which is less code than the
 * README explaining how to install an SDK. It also matches the rest of this
 * codebase — `server.mjs` is raw `node:http` with no framework — and a
 * dependency-free folder is something a developer can be handed rather than
 * onboarded onto.
 *
 * **stdout carries protocol and nothing else.** A stray console.log corrupts
 * the stream and the failure presents as the client hanging, which is a
 * miserable thing to debug. Everything human goes to stderr, which the client
 * shows in its logs.
 */

import { createInterface } from 'node:readline';
import { ViewerClient, Forbidden } from './client.mjs';
import { TOOLS, BY_NAME } from './tools.mjs';

const NAME = 'adam';
const VERSION = '0.1.0';

/**
 * Protocol versions this server knows how to speak.
 *
 * The client names the one it wants in `initialize`. Echoing a version we
 * actually support is the contract; answering with our newest regardless is how
 * you get a client talking a dialect the server does not have. Newest first, so
 * the fallback for an unrecognised request is the best one we have.
 */
const SPEAK = ['2025-06-18', '2025-03-26', '2024-11-05'];

const log = (...parts) => process.stderr.write(`[${NAME}] ${parts.join(' ')}\n`);

const client = new ViewerClient({
  base: process.env.ADAM_VIEWER_URL,
  // Unset means the default package, which is what `/api/…` answers for. Named
  // only when somebody runs more than one.
  project: process.env.ADAM_PROJECT || null,
  email: process.env.ADAM_EMAIL,
  password: process.env.ADAM_PASSWORD,
});

// ---- JSON-RPC ---------------------------------------------------------------

function write(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

const reply = (id, result) => write({ jsonrpc: '2.0', id, result });
const fail = (id, code, message) => write({ jsonrpc: '2.0', id, error: { code, message } });

/**
 * The ceiling on a single tool result, in characters — roughly 30k tokens.
 *
 * The package holds one 756 KB contract, and a tool that returns the wrong
 * slice of it fills a context window in one call and leaves no room to act on
 * what it fetched. The tools are each shaped to answer well under this; the cap
 * exists so that a tool added later, or a package that grows, degrades into a
 * legible refusal rather than into a wedged session.
 */
const MAX_RESULT = 120_000;

/**
 * A tool result.
 *
 * MCP wants content blocks, and JSON pretty-printed as text is what a model
 * reads best — it is the same shape the package's own files are in, and an
 * agent that can see the whole record decides for itself what matters.
 *
 * Over the ceiling, the answer is thrown away and replaced by its own size and
 * a suggestion. Truncated JSON would be worse than none: it does not parse, and
 * a model will read the surviving half as the whole answer.
 */
function content(value, isError = false) {
  const text = JSON.stringify(value, null, 2);
  if (text.length > MAX_RESULT) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          error: 'that answer is too large to return',
          size: `${Math.round(text.length / 1024)} KB`,
          ceiling: `${Math.round(MAX_RESULT / 1024)} KB`,
          try: 'narrow it — name one schema or operation, add a `kind`, or lower `limit`',
        }, null, 2),
      }],
      isError: true,
    };
  }
  return {
    content: [{ type: 'text', text }],
    ...(isError ? { isError: true } : {}),
  };
}

async function callTool(params) {
  const tool = BY_NAME.get(params?.name);
  if (!tool) {
    return content({ error: `no tool called "${params?.name}"`, tools: [...BY_NAME.keys()] }, true);
  }
  try {
    return content(await tool.run(client, params.arguments ?? {}));
  } catch (error) {
    // A refusal by the audience filter is an answer, not a crash: the account
    // may not read that route. Said plainly, because "the tool failed" would
    // send somebody to look for a bug that is a permission.
    if (error instanceof Forbidden) {
      return content({ error: error.message, refusedRoute: error.route, forbidden: true }, true);
    }
    log(`${params.name} failed:`, error.message);
    return content({ error: error.message }, true);
  }
}

async function handle(message) {
  const { id, method, params } = message;
  // A notification has no id and takes no response — `notifications/initialized`
  // is the one that always arrives. Answering it is a protocol violation.
  const isRequest = id !== undefined && id !== null;

  switch (method) {
    case 'initialize': {
      const asked = params?.protocolVersion;
      const version = SPEAK.includes(asked) ? asked : SPEAK[0];
      log(`initialize from ${params?.clientInfo?.name ?? 'unknown'} — speaking ${version}`);
      return reply(id, {
        protocolVersion: version,
        capabilities: { tools: {} },
        serverInfo: { name: NAME, version: VERSION },
        instructions:
          'The ADAM design package (screens, journeys, contracts, tables, services, modules, '
          + 'decisions) and your OpenProject work in it. Prefer adam_search when you have a name '
          + 'but not a kind. These are the package\'s own records, so they outrank anything '
          + 'remembered. To work a ticket: adam_board, then adam_pull with the ticket and your '
          + 'working folder, then read the files under .adam/work/. When it is done, adam_propose '
          + 'the status change and a comment, show the person, and adam_apply only after they say yes.',
      });
    }

    case 'notifications/initialized':
    case 'notifications/cancelled':
      return;

    case 'ping':
      return reply(id, {});

    case 'tools/list':
      return reply(id, {
        tools: TOOLS.map(({ name, description, inputSchema }) =>
          ({ name, description, inputSchema })),
      });

    case 'tools/call':
      return reply(id, await callTool(params));

    default:
      // Notifications we do not know are ignored; requests get the standard
      // "no such method" so the client can fall back rather than wait.
      if (isRequest) fail(id, -32601, `method not found: ${method}`);
  }
}

// ---- the loop ---------------------------------------------------------------

const lines = createInterface({ input: process.stdin });

lines.on('line', async (line) => {
  const text = line.trim();
  if (!text) return;
  let message;
  try {
    message = JSON.parse(text);
  } catch {
    return fail(null, -32700, 'parse error');
  }
  try {
    await handle(message);
  } catch (error) {
    log('unhandled:', error.stack ?? error.message);
    if (message?.id !== undefined && message?.id !== null) {
      fail(message.id, -32603, error.message);
    }
  }
});

lines.on('close', () => process.exit(0));

log(`ready — ${TOOLS.length} tools, viewer at ${client.base}`
  + `${client.project ? `, project ${client.project}` : ''}`);
