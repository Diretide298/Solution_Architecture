#!/usr/bin/env node
/**
 * Pull every ticket as a developer's connector does, and log it (the rehearsal pull, release runbook section 4;
 * moved from the audit kit, CHG-RHS-001).
 *
 * Calls the connector's own `adam_pull` (the candidate's viewer/mcp, or a developer's install) against the ADAM at
 * ADAM_URL, once per ticket. Each pull writes the .adam/work/<ticket>/ folder a developer sees; one JSON line per
 * ticket records what came back: errors, links, dead links, the release. No Claude session runs.
 *
 *   node tools/rehearse/pull-direct.mjs --connector <viewer/mcp> --tickets <tickets.json> --out <folder>
 *                                       [--jobs 4] [--only 17788,21813]
 *
 * tickets.json: [{ "id": 17788, "key": "SVC-IDENTITY-SSO-1", "role": "backend", "kind": "Backend" }, ...]
 * Env: ADAM_URL (required: there is no default, so nothing reaches the live ADAM by accident), ADAM_EMAIL,
 * ADAM_PASSWORD, ADAM_PROJECT (default ticvai). Re-runs skip tickets already logged without an error. Nothing here
 * prints a credential.
 */
import { readFile, writeFile, appendFile, mkdir, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const arg = (name, dflt) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : dflt;
};
for (const name of ['ADAM_URL', 'ADAM_EMAIL', 'ADAM_PASSWORD']) {
  if (!process.env[name]) {
    console.error(`set ADAM_URL, ADAM_EMAIL and ADAM_PASSWORD: ${name} is empty (there is no default ADAM)`);
    process.exit(2);
  }
}
const connector = path.resolve(arg('connector'));
const out = path.resolve(arg('out'));
const jobs = Number(arg('jobs', 4));
const only = arg('only') ? new Set(arg('only').split(',')) : null;
const tickets = JSON.parse(await readFile(arg('tickets'), 'utf8')).filter((t) => !only || only.has(String(t.id)));

const { ViewerClient } = await import(pathToFileURL(path.join(connector, 'client.mjs')).href);
const { BY_NAME } = await import(pathToFileURL(path.join(connector, 'tools.mjs')).href);
const pull = BY_NAME.get('adam_pull');
const client = new ViewerClient({
  base: process.env.ADAM_URL,
  project: process.env.ADAM_PROJECT || 'ticvai',
  email: process.env.ADAM_EMAIL,
  password: process.env.ADAM_PASSWORD,
});

const work = path.join(out, 'workspace');
await mkdir(work, { recursive: true });
const log = path.join(out, 'pull-log.jsonl');
const done = new Set();
try {
  for (const line of (await readFile(log, 'utf8')).split('\n')) {
    if (!line.trim()) continue;
    const r = JSON.parse(line);
    if (!r.error) done.add(String(r.id));
  }
} catch { /* first run */ }

async function files(dir) {
  const list = [];
  for (const name of await readdir(dir).catch(() => [])) {
    const p = path.join(dir, name);
    const s = await stat(p);
    if (s.isDirectory()) for (const f of await files(p)) list.push({ ...f, path: `${name}/${f.path}` });
    else list.push({ path: name, bytes: s.size });
  }
  return list;
}

async function one(t) {
  const started = Date.now();
  const row = { id: t.id, key: t.key, role: t.role, kind: t.kind, at: new Date().toISOString() };
  try {
    const res = await pull.run(client, { key: String(t.id), dir: work });
    row.found = res?.found !== false;
    if (res?.error) row.error = String(res.error).slice(0, 500);
    row.result = JSON.parse(JSON.stringify(res, (k, v) => (typeof v === 'string' && v.length > 400 ? `${v.slice(0, 400)}…` : v)));
    row.files = await files(path.join(work, '.adam', 'work', String(t.id)));
  } catch (e) {
    row.error = String(e?.message || e).slice(0, 500);
  }
  row.ms = Date.now() - started;
  await appendFile(log, `${JSON.stringify(row)}\n`);
  return row;
}

const queue = tickets.filter((t) => !done.has(String(t.id)));
console.log(`${tickets.length} tickets, ${tickets.length - queue.length} already logged, ${queue.length} to pull (${jobs} at a time)`);
let n = 0;
let errors = 0;
await Promise.all(Array.from({ length: jobs }, async () => {
  while (queue.length) {
    const t = queue.shift();
    const r = await one(t);
    n += 1;
    if (r.error) errors += 1;
    if (n % 25 === 0 || r.error) console.log(`  ${n} pulled, ${errors} errors${r.error ? ` (last: #${r.id} ${r.error.slice(0, 120)})` : ''}`);
  }
}));
await writeFile(path.join(out, 'pull-done.json'), JSON.stringify({ pulled: n, errors, at: new Date().toISOString() }));
console.log(`done: ${n} pulled, ${errors} errors -> ${log}`);
