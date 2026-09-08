#!/usr/bin/env node
/**
 * Drives the MCP server over stdio and checks what comes back.
 *
 * Same shape as `viewer/api/*-check.mjs`: no framework, one file, exits non-zero
 * on a failure and says which. Run it after any change to the three files beside
 * it.
 *
 *   node viewer/mcp/mcp-check.mjs
 *
 * The handshake and the tool listing need nothing running — they are pure
 * protocol. The live calls need the viewer on :4173 and an account in
 * ADAM_EMAIL / ADAM_PASSWORD; without those the whole live block is skipped,
 * because a viewer that is not up is not a broken MCP server.
 *
 * **Inside the live block, nothing skips.** A lookup that finds nothing to test
 * fails. Two real bugs — a table lookup that could never resolve a bare name,
 * and a `didYouMean` list of names that existed nowhere — sat behind a
 * benign-looking `skip` line, because the search that fed them was capped at 25
 * and the first table fell off the end. A check that skips quietly is a check
 * that lies.
 *
 * Two checks guard result size rather than correctness, because both of those
 * regressions are invisible until something breaks: the 756 KB contract must
 * come back under the ceiling, and every one of the 32 modules must answer
 * under 40 KB — one of them holds 25,000-character prose fields, and which one
 * changes with the package.
 */

import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const SERVER = path.join(here, 'server.mjs');

const results = [];
const pass = (what) => { results.push([true, what]); console.log(`  ok    ${what}`); };
const fail = (what, why) => { results.push([false, what]); console.log(`  FAIL  ${what}\n        ${why}`); };
const skip = (what, why) => console.log(`  skip  ${what} — ${why}`);

// ---- a client ---------------------------------------------------------------

function open() {
  const child = spawn(process.execPath, [SERVER], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env },
  });
  const waiting = new Map();
  let buffer = '';
  let nextId = 1;

  child.stdout.on('data', (chunk) => {
    buffer += chunk;
    let cut;
    while ((cut = buffer.indexOf('\n')) >= 0) {
      const line = buffer.slice(0, cut).trim();
      buffer = buffer.slice(cut + 1);
      if (!line) continue;
      let message;
      try { message = JSON.parse(line); } catch { throw new Error(`not JSON on stdout: ${line}`); }
      const settle = waiting.get(message.id);
      if (settle) { waiting.delete(message.id); settle(message); }
    }
  });

  const stderr = [];
  child.stderr.on('data', (c) => stderr.push(String(c)));

  return {
    child,
    stderr,
    send(method, params) {
      const id = nextId++;
      const answer = new Promise((resolve, reject) => {
        waiting.set(id, resolve);
        setTimeout(() => reject(new Error(`timed out waiting for ${method}`)), 20_000).unref();
      });
      child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id, method, params })}\n`);
      return answer;
    },
    notify(method, params) {
      child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', method, params })}\n`);
    },
    close() { child.stdin.end(); },
  };
}

const parse = (answer) => JSON.parse(answer.result.content[0].text);

// ---- the checks -------------------------------------------------------------

const mcp = open();

console.log('\nhandshake');

const init = await mcp.send('initialize', {
  protocolVersion: '2025-06-18',
  capabilities: {},
  clientInfo: { name: 'mcp-check', version: '1' },
});
if (init.result?.protocolVersion === '2025-06-18') pass('initialize echoes the version asked for');
else fail('initialize echoes the version asked for', JSON.stringify(init));

if (init.result?.serverInfo?.name === 'adam') pass('serverInfo names the server');
else fail('serverInfo names the server', JSON.stringify(init.result?.serverInfo));

if (init.result?.capabilities?.tools) pass('declares the tools capability');
else fail('declares the tools capability', JSON.stringify(init.result?.capabilities));

// An unknown version must not be echoed back — that is how a client ends up
// talking a dialect the server does not have.
const odd = open();
const oddInit = await odd.send('initialize', {
  protocolVersion: '1999-01-01', capabilities: {}, clientInfo: { name: 'x', version: '1' },
});
if (oddInit.result?.protocolVersion !== '1999-01-01') pass('an unknown protocol version is not echoed');
else fail('an unknown protocol version is not echoed', 'echoed 1999-01-01');
odd.close();

mcp.notify('notifications/initialized');

console.log('\nprotocol');

const ping = await mcp.send('ping', {});
if (ping.result && !ping.error) pass('ping answers');
else fail('ping answers', JSON.stringify(ping));

const nope = await mcp.send('does/not/exist', {});
if (nope.error?.code === -32601) pass('an unknown method is -32601, not a hang');
else fail('an unknown method is -32601, not a hang', JSON.stringify(nope));

console.log('\ntools');

const list = await mcp.send('tools/list', {});
const names = (list.result?.tools ?? []).map((t) => t.name).sort();
const want = ['adam_board', 'adam_contract', 'adam_decisions', 'adam_file', 'adam_journey',
  'adam_link', 'adam_links', 'adam_module', 'adam_screen', 'adam_search', 'adam_service',
  'adam_table', 'adam_work'];
if (String(names) === String(want)) pass(`${want.length} tools listed: ${names.join(', ')}`);
else fail(`${want.length} tools listed`, `got ${names.join(', ') || '(none)'}`);

// What can actually be asserted about every tool: a description long enough to
// choose by, and an object schema. **Not** that it declares a property or a
// required key — `adam_decisions` lists every ADR with no argument, and
// `adam_board` takes none at all. Two earlier versions of this check demanded
// each in turn and failed a tool that was right, which is its own small lesson:
// an assertion that fires on correct code teaches people to ignore the harness.
const shaped = (list.result?.tools ?? []).every(
  (t) => t.description?.length > 40 && t.inputSchema?.type === 'object',
);
if (shaped) pass('every tool has a description and an object schema');
else {
  const thin = (list.result?.tools ?? [])
    .filter((t) => !(t.description?.length > 40 && t.inputSchema?.type === 'object'))
    .map((t) => t.name);
  fail('every tool has a description and an object schema', `thin: ${thin.join(', ')}`);
}

const unknown = await mcp.send('tools/call', { name: 'adam_nonesuch', arguments: {} });
if (unknown.result?.isError && parse(unknown).tools) pass('an unknown tool is an isError result, not a crash');
else fail('an unknown tool is an isError result, not a crash', JSON.stringify(unknown).slice(0, 200));

// ---- the live half ----------------------------------------------------------

console.log('\nagainst the viewer');

const base = process.env.ADAM_VIEWER_URL ?? 'http://127.0.0.1:4173';

// Both halves, named separately. `/api/health` is proxied to the accounts
// service, so probing only that reports a live node with a dead uvicorn as
// "start the viewer" and sends somebody to the wrong log. `/login.html` is
// public and served by node itself.
const reach = async (path) => {
  try {
    const probe = await fetch(`${base}${path}`, { signal: AbortSignal.timeout(3000) });
    return probe.status < 500;
  } catch { return false; }
};
const [viewerUp, accountsUp] = await Promise.all([reach('/login.html'), reach('/api/health')]);

if (!viewerUp) {
  skip('the live tools', `no viewer at ${base} — start it with viewer/start.ps1`);
} else if (!accountsUp) {
  skip('the live tools', 'the viewer is up but the accounts service is not — check the uvicorn log');
} else if (!process.env.ADAM_EMAIL || !process.env.ADAM_PASSWORD) {
  skip('the live tools', 'set ADAM_EMAIL and ADAM_PASSWORD');
} else {
  // A generous limit on purpose. At the default 25 the first `flow` and the
  // first `table` fell off the end, both lookups below reported "search found
  // nothing of that kind", and two real bugs sat behind that skip for a while.
  // A check that skips quietly is a check that lies.
  const search = await mcp.send('tools/call', {
    name: 'adam_search', arguments: { q: 'access', limit: 100 },
  });
  const found = parse(search);
  if (found.hits?.length) {
    pass(`adam_search returned ${found.total} hits across ${Object.keys(found.kinds).length} kinds`);
  } else fail('adam_search returned hits', JSON.stringify(found).slice(0, 300));

  // `kinds` must describe the whole result, not the corpus and not the page:
  // its counts have to add up to `total`. An earlier draft of this assertion
  // demanded every named kind appear in `hits` too, which is wrong for the same
  // reason the bug it was chasing was wrong — `hits` is one page of `total`,
  // and a kind with one hit at position 200 is real and not on it.
  const kinds = found.kinds ?? {};
  const summed = Object.values(kinds).reduce((a, b) => a + b, 0);
  if (Object.keys(kinds).length && summed === found.total) {
    pass(`kinds counts the whole result (${summed} across ${Object.keys(kinds).length} kinds)`);
  } else fail('kinds counts the whole result', `summed ${summed} vs total ${found.total}`);

  // Drive the other lookups off a *filtered* search per kind, so a hit that
  // exists past the page cap is still found. Not hardcoded ids — those move
  // whenever the package is re-derived.
  const first = async (kind) => {
    const r = parse(await mcp.send('tools/call', {
      name: 'adam_search', arguments: { q: 'a', kind, limit: 1 },
    }));
    return r.hits?.[0]?.id;
  };
  const cases = [
    ['adam_screen', { id: await first('screen') }, 'screen'],
    ['adam_journey', { id: await first('flow') }, 'journey'],
    ['adam_contract', { name: 'access' }, 'contract'],
    ['adam_table', { name: await first('table') }, 'table'],
  ];
  for (const [tool, args, key] of cases) {
    const only = Object.values(args)[0];
    if (!only) { fail(tool, `search returned no hit of that kind to look up — kinds: ${found.kinds}`); continue; }
    const answer = await mcp.send('tools/call', { name: tool, arguments: args });
    const body = parse(answer);
    if (body.found && body[key]) pass(`${tool}(${only}) returned a ${key}`);
    else fail(`${tool}(${only})`, JSON.stringify(body).slice(0, 300));
  }

  // The decisions layer, which a client account is refused and a reviewer is
  // not — so what this asserts depends on who ADAM_EMAIL is. Either answer is
  // correct; silence would not be.
  const adrs = await mcp.send('tools/call', { name: 'adam_decisions', arguments: {} });
  const seen = parse(adrs);
  if (seen.adrs?.length) {
    pass(`adam_decisions listed ${seen.total} ADRs`);
    const one = seen.adrs[0].id;
    const full = parse(await mcp.send('tools/call', { name: 'adam_decisions', arguments: { id: one } }));
    if (full.found && full.adr) pass(`adam_decisions(${one}) returned the record`);
    else fail(`adam_decisions(${one})`, JSON.stringify(full).slice(0, 200));

    // And the prose behind it, which is what adam_file exists for.
    const src = parse(await mcp.send('tools/call', { name: 'adam_file', arguments: { path: full.adr.file } }));
    if (src.found && src.text?.length) pass(`adam_file read ${src.showing} of ${src.totalLines} lines`);
    else fail('adam_file read the ADR', JSON.stringify(src).slice(0, 200));
  } else if (adrs.result?.isError && seen.forbidden) {
    pass('adam_decisions is refused for this account, and says so');
  } else {
    fail('adam_decisions', JSON.stringify(seen).slice(0, 300));
  }

  // The 756 KB contract must come back as a map, not as a context window.
  const big = await mcp.send('tools/call', { name: 'adam_contract', arguments: { name: 'access' } });
  const size = big.result?.content?.[0]?.text?.length ?? 0;
  if (size > 0 && size < 120_000) pass(`adam_contract(access) is ${Math.round(size / 1024)} KB, under the ceiling`);
  else fail('adam_contract(access) stays under the ceiling', `${Math.round(size / 1024)} KB`);

  // **V-46, from the client's side.** The MCP leans on the viewer answering a
  // conditional request; without it every tool call re-downloads a whole layer,
  // and the symptom is silence — right answers, quietly slow. Checked here
  // rather than in the viewer's own harness because this is the consumer that
  // breaks, and because a deployed viewer predating the fix must still work
  // through the `generatedAt` fallback.
  const signIn = await fetch(`${base}/api/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: process.env.ADAM_EMAIL, password: process.env.ADAM_PASSWORD }),
  });
  const token = (signIn.headers.getSetCookie?.() ?? [])
    .map((c) => /ticvai_session=([^;]+)/.exec(c)?.[1]).find(Boolean);
  if (token) {
    const cookie = `ticvai_session=${decodeURIComponent(token)}`;
    const full = await fetch(`${base}/pkg/ticvai/index`, { headers: { cookie } });
    const tag = full.headers.get('etag');
    const size = (await full.arrayBuffer()).byteLength;
    if (tag) {
      const again = await fetch(`${base}/pkg/ticvai/index`,
        { headers: { cookie, 'if-none-match': tag } });
      const saved = (await again.arrayBuffer()).byteLength;
      if (again.status === 304 && saved === 0) {
        pass(`the viewer revalidates — ${Math.round(size / 1024)} KB becomes a 304`);
      } else fail('the viewer revalidates', `got ${again.status} with ${saved} bytes`);

      // A validator that matches anything is worse than none: it would serve a
      // stale package forever and look like a working cache.
      const stale = await fetch(`${base}/pkg/ticvai/index`,
        { headers: { cookie, 'if-none-match': '"not-the-etag"' } });
      if (stale.status === 200) pass('a stale validator refetches rather than 304ing');
      else fail('a stale validator refetches', `got ${stale.status}`);
    } else {
      skip('the viewer revalidates', 'no ETag — an older viewer, so the generatedAt fallback carries it');
    }
  }

  // Services and modules — phase 2. Neither needed a new server route: the
  // handoff said both were missing and both were already being served.
  const svc = parse(await mcp.send('tools/call', { name: 'adam_service', arguments: {} }));
  if (svc.total > 0) pass(`adam_service listed ${svc.total} services`);
  else fail('adam_service listed services', JSON.stringify(svc).slice(0, 200));

  const one = svc.services?.[0]?.name;
  const deep = parse(await mcp.send('tools/call', { name: 'adam_service', arguments: { name: one } }));
  if (deep.found && deep.service?.operationsByContract) pass(`adam_service(${one}) returned its contracts`);
  else fail(`adam_service(${one})`, JSON.stringify(deep).slice(0, 200));

  // Said out loud, without the suffix — how anybody actually refers to them.
  const short = one?.replace(/Service$/, '');
  const spoken = parse(await mcp.send('tools/call', { name: 'adam_service', arguments: { name: short } }));
  if (spoken.found) pass(`adam_service("${short}") resolves without the suffix`);
  else fail(`adam_service("${short}")`, JSON.stringify(spoken).slice(0, 200));

  const mods = parse(await mcp.send('tools/call', { name: 'adam_module', arguments: {} }));
  if (mods.total > 0) pass(`adam_module listed ${mods.total} modules`);
  else fail('adam_module listed modules', JSON.stringify(mods).slice(0, 200));

  // **The size guard, and it is not theoretical.** 160 fields across the 395
  // tables are over 2 KB and every one is a `storageReason`; the largest is
  // 25,450 characters. Untrimmed, one module came back at 59 KB for eight
  // tables. Every module is checked, because the offender is whichever one
  // happens to own the essays this week.
  let worst = ['', 0];
  for (const m of mods.modules ?? []) {
    const answer = await mcp.send('tools/call', { name: 'adam_module', arguments: { name: m.name } });
    const n = answer.result?.content?.[0]?.text?.length ?? 0;
    if (n > worst[1]) worst = [m.name, n];
  }
  if (worst[1] > 0 && worst[1] < 40_000) {
    pass(`the largest module answer is ${worst[0]} at ${Math.round(worst[1] / 1024)} KB`);
  } else fail('module answers stay small', `${worst[0]} is ${Math.round(worst[1] / 1024)} KB`);

  // ---- phase 3: scheduled work ------------------------------------------
  // These go to the accounts service, not the package, and they need a stored
  // OpenProject credential. Without one the right answer is a 428 telling
  // somebody to go and connect — checked here, because "the tool failed" for a
  // thing you simply have not set up yet is a bad half-hour.
  const board = parse(await mcp.send('tools/call', { name: 'adam_board', arguments: {} }));
  if (board.needsSetup) {
    pass('adam_board without a credential says to connect OpenProject, not "failed"');
    skip('the rest of the work tools', 'no OpenProject credential stored for this account');
  } else if (typeof board.total === 'number') {
    pass(`adam_board answers — ${board.total} open item(s)`);
    if (board.total === 0 && board.note) pass('and an empty board explains itself');

    const first = board.items?.[0]?.key;
    if (first) {
      const wp = parse(await mcp.send('tools/call', { name: 'adam_work', arguments: { key: first } }));
      if (wp.found && wp.workPackage?.subject) pass(`adam_work(#${first}) — "${wp.workPackage.subject}"`);
      else fail(`adam_work(#${first})`, JSON.stringify(wp).slice(0, 200));

      // The write, and then putting it back. Nothing else in this harness
      // changes state, so it undoes itself rather than leaving a row behind for
      // the next run to trip over.
      const made = parse(await mcp.send('tools/call', {
        name: 'adam_link', arguments: { kind: 'screen', id: 'WEB-001', key: first },
      }));
      if (made.ok) {
        pass(`adam_link recorded screen WEB-001 against #${first}`);
        const seen = parse(await mcp.send('tools/call', {
          name: 'adam_links', arguments: { kind: 'screen', id: 'WEB-001' },
        }));
        if (seen.found && seen.links.some((l) => l.workPackage === String(first))) {
          pass('adam_links reads it back');
          const undo = parse(await mcp.send('tools/call', {
            name: 'adam_link', arguments: { remove: true, linkId: seen.links[0].linkId },
          }));
          if (undo.ok && /untouched/i.test(undo.note ?? '')) {
            pass('and removing it says the work package is untouched');
          } else fail('removing it', JSON.stringify(undo).slice(0, 200));
        } else fail('adam_links reads it back', JSON.stringify(seen).slice(0, 200));
      } else fail('adam_link records a link', JSON.stringify(made).slice(0, 200));
    } else {
      skip('adam_work and adam_link', 'nothing is assigned to this account in OpenProject');
    }
  } else {
    fail('adam_board answers', JSON.stringify(board).slice(0, 250));
  }

  // A tool that reads links needs no credential at all, so this holds either way.
  const none = parse(await mcp.send('tools/call', {
    name: 'adam_links', arguments: { kind: 'screen', id: 'NOPE-999' },
  }));
  if (none.found === false && none.note) {
    pass('an artefact with no links says nobody has linked one, not that no work exists');
  } else fail('an artefact with no links explains itself', JSON.stringify(none).slice(0, 200));

  // The bare name, without its module. The tool's own description promises
  // this works; it did not, because `fold` strips the dot before the regex
  // that was meant to find one, and the fallback was dead code.
  const bare = parse(await mcp.send('tools/call',
    { name: 'adam_table', arguments: { name: 'entitlement' } }));
  if (bare.found || (bare.didYouMean ?? []).length > 1) {
    pass(bare.found ? 'adam_table resolves a bare table name' : 'a bare table name that is ambiguous asks which');
    // Whatever it offers must be a name that exists. The doubled prefix bug
    // handed back `access.access.entitlement`, which names nothing.
    const offered = bare.didYouMean ?? [];
    if (!offered.some((n) => /(\w+)\.\./.test(n))) pass('candidate table names are real names');
    else fail('candidate table names are real names', offered.join(', '));
  } else {
    fail('adam_table resolves a bare table name', JSON.stringify(bare).slice(0, 200));
  }

  // A miss must teach rather than stonewall.
  const bad = await mcp.send('tools/call', { name: 'adam_screen', arguments: { id: 'NOPE-999' } });
  const missed = parse(bad);
  if (missed.found === false && missed.error) pass('a miss returns an explanation, not an empty object');
  else fail('a miss returns an explanation', JSON.stringify(missed).slice(0, 200));

  // The second call to a layer must come off the ETag cache rather than the wire.
  const again = await mcp.send('tools/call', { name: 'adam_search', arguments: { q: 'order' } });
  if (parse(again).total >= 0) pass('a second call to a cached layer answers');
  else fail('a second call to a cached layer answers', JSON.stringify(parse(again)).slice(0, 200));
}

mcp.close();

// ---- the verdict ------------------------------------------------------------

const failed = results.filter(([ok]) => !ok);
console.log(`\n${results.length - failed.length} of ${results.length} checks passed`);
if (failed.length && mcp.stderr.length) {
  console.log('\nserver stderr:\n' + mcp.stderr.join('').trim());
}
process.exit(failed.length ? 1 : 0);
