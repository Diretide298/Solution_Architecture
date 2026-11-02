#!/usr/bin/env node
// Why a pull is not slower than its reads (2 November 2026: #27764 took 44 to 172 s, #27646 26 s, the foundation
// tickets 80 to 105 s on live ADAM). No services: a stand-in viewer on 127.0.0.1, on a port the system picks.
//
//   node viewer/mcp/pull-speed-check.mjs
//
//   1. ViewerClient reads a layer once however many lookups ask for it at the same time: eight at once are one
//      request, and all eight get the same body;
//   2. once that read has landed the next one still asks the server (a 304 then, the body held), and a changed
//      package is read anew: sharing a read never serves what the server was not asked about;
//   3. a read that fails fails for everyone who shared it and is not held, so the next one asks again;
//   4. pool(n) runs at most n tasks at once, answers each in the order given, and a failing task fails its own
//      call only.

import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { ViewerClient } from './client.mjs';
import { pool } from './tools.mjs';

let pass = 0;
let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${!ok && detail ? ` - ${detail}` : ''}`);
  if (ok) pass += 1; else fail += 1;
};
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// The stand-in: a sign-in, and one layer with an ETag that answers slowly, as live ADAM does for 21 MB.
let layer = { screens: [{ id: 'WEB-001' }] };
let failNext = false;
const asked = [];
const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/api/auth/login') {
    res.writeHead(200, { 'set-cookie': 'ticvai_session=s1; Path=/', 'content-type': 'application/json' });
    return res.end('{"ok":true}');
  }
  if (url.pathname === '/pkg/t/journeys') {
    asked.push(req.headers['if-none-match'] ? 'revalidate' : 'fetch');
    await wait(150);
    if (failNext) {
      failNext = false;
      res.writeHead(500, { 'content-type': 'application/json' });
      return res.end('{"error":"down"}');
    }
    const body = JSON.stringify(layer);
    const etag = `"${createHash('sha1').update(body).digest('base64url')}"`;
    if (req.headers['if-none-match'] === etag) {
      res.writeHead(304, { etag });
      return res.end();
    }
    res.writeHead(200, { etag, 'content-type': 'application/json' });
    return res.end(body);
  }
  res.writeHead(404);
  res.end();
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}`;

try {
  const client = new ViewerClient({ base, project: 't', email: 'a@b.c', password: 'x' });

  // 1
  const eight = await Promise.all(Array.from({ length: 8 }, () => client.layer('journeys')));
  check('1. eight lookups at once read the layer once', asked.length === 1 && asked[0] === 'fetch', JSON.stringify(asked));
  check('1. all eight get the same body', eight.every((b) => b === eight[0]) && eight[0].screens[0].id === 'WEB-001');

  // 2
  asked.length = 0;
  const again = await Promise.all([client.layer('journeys'), client.layer('journeys')]);
  check('2. the next read still asks the server, once, and is told it holds the current one',
    asked.length === 1 && asked[0] === 'revalidate' && again[0] === eight[0], JSON.stringify(asked));
  layer = { screens: [{ id: 'WEB-002' }] };
  asked.length = 0;
  const changed = await client.layer('journeys');
  check('2. a changed package is read anew', changed.screens[0].id === 'WEB-002' && asked.length === 1, JSON.stringify(asked));

  // 3
  const fresh = new ViewerClient({ base, project: 't', email: 'a@b.c', password: 'x' });
  failNext = true;
  asked.length = 0;
  const shared = await Promise.allSettled(Array.from({ length: 4 }, () => fresh.layer('journeys')));
  check('3. a failed read fails all four that shared it, in one request',
    shared.every((r) => r.status === 'rejected') && asked.length === 1, JSON.stringify(asked));
  const after = await fresh.layer('journeys').catch((error) => ({ error: error.message }));
  check('3. and is not held: the next read asks again and gets the layer', after?.screens?.[0]?.id === 'WEB-002',
    JSON.stringify(after));

  // 4
  const gate = pool(3);
  let running = 0;
  let most = 0;
  const answers = await Promise.allSettled(Array.from({ length: 10 }, (_, i) => gate(async () => {
    running += 1;
    most = Math.max(most, running);
    await wait(20 + ((i * 7) % 30));
    running -= 1;
    if (i === 4) throw new Error('four');
    return i;
  })));
  check('4. pool(3) runs at most three at once', most === 3, `most ${most}`);
  check('4. each call answers its own task, in order, and one failure stays its own',
    answers.every((r, i) => (i === 4 ? r.status === 'rejected' && r.reason.message === 'four' : r.value === i)));
} finally {
  server.close();
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
