// Local viewer for the TICVAI contracts.
//   node server.mjs [--port 4173] [--dir contracts] [--open]
//
// Re-indexes on any change under the watched directory and pushes a reload to
// connected browsers over SSE.

import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { watch } from 'node:fs';
import { gzipSync } from 'node:zlib';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildIndex } from './lib/indexer.mjs';
import { buildStructure } from './lib/structure.mjs';
import { buildJourneys } from './lib/journeys.mjs';
import { buildBackend } from './lib/backend.mjs';
import { buildDomain } from './lib/domain.mjs';
import { buildLineage } from './lib/lineage.mjs';
import { buildTooltips } from './lib/tooltips.mjs';
import { buildDecisions } from './lib/decisions.mjs';
import { buildDomains } from './lib/domains.mjs';
import { extractFrame } from './lib/wireframes.mjs';
import { gate } from './lib/session.mjs';
import { clientMayCall, decisionFiles, isDecisionFile, layersFor, modesFor } from './lib/audience.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(here, '..');
const PUBLIC = path.join(here, 'public');

// Where the accounts service listens. Same host in every deployment — this is
// a loopback call, not a trip over the network.
const AUTH_BASE = process.env.TICVAI_AUTH ?? 'http://127.0.0.1:8787';

/**
 * Where the *browser* should call the accounts service, when that is not here.
 *
 * AUTH_BASE above is this process talking to that one, over loopback, and stays
 * loopback in every arrangement. This is the separate question of what address
 * to put in front of a visitor, and it only has an answer in the split
 * deployment — the reading server on atlas.example.com and the accounts service
 * on atlasapi.example.com.
 *
 * Unset, every page keeps calling this origin and server.mjs proxies onward,
 * which is what a workstation and the one-origin deployment both want.
 *
 * Handed to the client as a meta tag rather than baked into the eight HTML
 * files, because the address belongs to a deployment and those files are the
 * same in all of them. Trailing slash trimmed: validation.js joins it to paths
 * that already start with one.
 */
/**
 * Which origins may read the package across an origin boundary.
 *
 * The deployed front end, and the two workstation spellings — localhost and
 * 127.0.0.1 are different origins to a browser, and a check harness that runs
 * against one while a person reads the other is a confusing afternoon.
 * TICVAI_ORIGINS adds to it, the same variable and the same spelling the
 * accounts service uses, so the two halves are configured once.
 */
const ALLOWED_ORIGINS = new Set([
  'https://atlas.ainfinite.ai',
  'http://localhost:4173', 'http://127.0.0.1:4173',
  ...(process.env.TICVAI_ORIGINS ?? '').split(',').map((o) => o.trim()).filter(Boolean),
]);

const API_PUBLIC = (process.env.TICVAI_API_PUBLIC ?? '').trim().replace(/\/+$/, '');
const API_META = API_PUBLIC
  ? `<meta name="ticvai-api" content="${API_PUBLIC.replace(/"/g, '&quot;')}" />`
  : '';

/**
 * What the accounts service owns. Deliberately a list rather than "anything
 * under /api": the viewer answers most of /api itself, and /api/events is a
 * long-lived stream that must not be forwarded.
 *
 * The thirteen this server answers for itself are /api/index, /api/detail,
 * /api/session, /api/tooltips, /api/domains, /api/domain, /api/journeys,
 * /api/backend, /api/decisions, /api/events, /api/file, /api/lineage and
 * /api/tree. None of them exist in the accounts service, so adding one to this
 * pattern does not move it — it deletes it, and the symptom is a 404 carrying
 * FastAPI's `{"detail":"Not Found"}` from a route this file plainly defines.
 * `session` was in here and is the reason /api/session was 404ing.
 */
const API_ROUTES =
  /^\/(api\/(auth|accounts|invites|validation|verdicts|mentions|mentionable|health)(\/|$)|docs|openapi\.json)/;

/**
 * Hand a request to the accounts service and give its answer back unchanged.
 *
 * The header that matters is set-cookie: sign-in, sign-out and redeem all work
 * by setting one, and a proxy that drops it produces a login that returns 200
 * and leaves you signed out. getSetCookie() is used rather than reading the
 * header directly because there can be more than one and the plain accessor
 * folds them into a single comma-joined string that no browser will parse.
 */
async function proxyToApi(req, res, url) {
  const body = ['GET', 'HEAD'].includes(req.method)
    ? undefined
    : await new Promise((resolve, reject) => {
      const parts = [];
      req.on('data', (c) => parts.push(c));
      req.on('end', () => resolve(Buffer.concat(parts)));
      req.on('error', reject);
    });

  const headers = {};
  for (const name of ['cookie', 'content-type', 'accept', 'user-agent']) {
    if (req.headers[name]) headers[name] = req.headers[name];
  }

  try {
    const answer = await fetch(`${AUTH_BASE}${url.pathname}${url.search}`, {
      method: req.method,
      headers,
      body: body && body.length ? body : undefined,
      redirect: 'manual',
    });

    const out = {
      'Content-Type': answer.headers.get('content-type') ?? 'application/json',
      'Cache-Control': 'no-store',
    };
    const cookies = answer.headers.getSetCookie?.() ?? [];
    if (cookies.length) out['Set-Cookie'] = cookies;
    const location = answer.headers.get('location');
    if (location) out.Location = location;

    res.writeHead(answer.status, out);
    res.end(Buffer.from(await answer.arrayBuffer()));
  } catch (error) {
    // The viewer is up and the accounts service is not. Say which, because
    // "500" here sends somebody to read the wrong log.
    res.writeHead(502, { 'Content-Type': MIME['.json'], 'Cache-Control': 'no-store' });
    res.end(JSON.stringify({
      error: 'the accounts service is not answering',
      detail: error.message,
      upstream: AUTH_BASE,
    }));
  }
}
// Named for what it does rather than what it undoes, and deliberately not
// TICVAI_OPEN — there is already an --open flag that opens a browser, and a
// switch that turns off authentication must not be one letter from it.
const NO_GATE = process.env.TICVAI_NO_GATE === '1';

function parseArgs(argv) {
  // host defaults to every interface, which is right on a workstation and
  // wrong on a server — there nginx is the only way in, so the deployment
  // passes --host 127.0.0.1 and port 4173 is unreachable from outside.
  const args = { port: 4173, dir: 'contracts', open: false, host: undefined };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--port') args.port = Number(argv[++i]);
    else if (argv[i] === '--dir') args.dir = argv[++i];
    else if (argv[i] === '--host') args.host = argv[++i];
    else if (argv[i] === '--open') args.open = true;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

let index = null;
let journeys = null;
let backend = null;
let domain = null;
let lineage = null;
let tooltips = null;
let decisions = null;
let domains = null;
let indexing = null;

// ---- the boot payload, and what is held back from it -----------------------
// /api/index was 1.9 MB of the 3.0 MB the viewer fetched to open, and unlike
// the other parts every layer needs it — so the per-layer lazy loading could
// not touch it. Two fields are three tenths of that weight on their own:
//
//   properties   0.39 MB   the fields of all 554 schemas
//   description  0.20 MB   the prose on every node
//
// Neither is ever read for more than one file at a time. `properties` is read
// by the ER diagram, which draws one contract; `description` by the reader,
// which shows one node. So they are cut out of the index and served per file,
// and the client merges them back into the node it already has. What arrives
// at boot is what the tree, the graph and the search need — names, kinds,
// files and counts — and nothing that only a detail view will ask for.
const DETAIL_FIELDS = ['description', 'properties'];

let indexSlim = null;
/** file -> { [nodeId]: { description, properties } } */
let detailByFile = null;

function splitDetail(full) {
  const slim = { ...full, nodes: [] };
  const byFile = new Map();
  for (const node of full.nodes) {
    const lean = {};
    const heavy = {};
    for (const [key, value] of Object.entries(node)) {
      if (DETAIL_FIELDS.includes(key)) heavy[key] = value;
      else lean[key] = value;
    }
    slim.nodes.push(lean);
    if (!Object.keys(heavy).length) continue;
    if (!byFile.has(node.file)) byFile.set(node.file, {});
    byFile.get(node.file)[node.id] = heavy;
  }
  return { slim, byFile };
}

async function refreshIndex(reason = 'startup') {
  if (indexing) return indexing; // coalesce concurrent rebuilds
  indexing = (async () => {
    const started = Date.now();
    try {
      index = await buildIndex(ROOT, args.dir);
      // split once per rebuild, not once per request
      ({ slim: indexSlim, byFile: detailByFile } = splitDetail(index));
      // everything stringified and compressed against the old index is stale
      packedCache.clear();

      // both other layers resolve against the contracts, so all three rebuild
      // together — the API is the join between the frontend and the backend
      const operationIds = new Set(
        index.nodes.filter((n) => n.type === 'operation').map((n) => n.name)
      );
      const schemas = index.nodes.filter((n) => n.type === 'schema');

      [journeys, backend, domain, decisions] = await Promise.all([
        buildJourneys(ROOT, operationIds),
        buildBackend(ROOT, schemas),
        // the state models and the event catalogue resolve against the contract
        // enums and operationIds, so they are built from the same index
        buildDomain(ROOT, {
          schemas,
          operationIds,
          files: index.nodes.filter((n) => n.type === 'file'),
        }),
        // prose — resolves against nothing, so it can build alongside
        buildDecisions(ROOT),
      ]);

      // The lineage joins the contracts to the tables and the screens to both,
      // so it needs all three of the above to have finished before it can say
      // which of its rows point at something that no longer exists. Same for the
      // tooltips, which are generated and therefore have to be checked.
      const operations = index.nodes.filter((n) => n.type === 'operation');
      [lineage, tooltips] = await Promise.all([
        buildLineage(ROOT, {
          operations,
          tables: backend.tables ?? [],
          screens: journeys.screens ?? [],
          // the workbook states the same join and states more of it, so the
          // lineage is built from both and reports where they differ
          dataLineage: backend.dataLineage ?? [],
          whereUsed: backend.whereUsed ?? [],
        }),
        buildTooltips(ROOT, {
          tables: (backend.tables ?? []).map((t) => t.name),
          // keyed by contract file stem — `access`, `marketing-crm` — not by the
          // module's display name, which is what `x-ticvai-module` carries
          contracts: [
            ...new Set(
              index.nodes
                .filter((n) => n.type === 'file')
                .map((n) => path.basename(n.file ?? n.name ?? '', '.yaml'))
                .filter(Boolean)
            ),
          ],
          modules: (backend.modules ?? []).map((m) => m.name),
          platforms: (journeys.platforms ?? []).map((p) => p.code),
          flows: (journeys.flows ?? []).map((f) => f.id),
        }),
      ]);

      // A domain lens gathers one subject across every other payload, so it is
      // the only build that needs all of them — it goes last, after the lineage
      // has joined the operations to the tables and the screens to both.
      // The declared half of every lens, as the package now ships it: one
      // sidecar keyed `kind:id`, regenerated with the dump rather than edited
      // into sixty files. Absent is fine — the lens then derives and says so.
      const markers = await readFile(path.join(ROOT, 'handoff/domain-markers.json'), 'utf8')
        .then(JSON.parse)
        .catch(() => null);

      domains = buildDomains({
        markers,
        operations: index.nodes.filter((n) => n.type === 'operation'),
        machines: domain.machines ?? [],
        events: domain.events ?? [],
        screens: journeys.screens ?? [],
        adrs: decisions.adrs ?? [],
        lineage,
        journeys,
      });

      const { stats } = index;
      const j = journeys.stats;
      const b = backend.stats;
      const d = domain.stats;
      console.log(
        `[index] ${reason}: ${stats.files} files · ${stats.operations} operations · ` +
          `${stats.schemas} schemas · ${stats.links} links · ${stats.errors} errors | ` +
          `frontend ${j.flows} flows · ${j.screens} screens · ${j.apps} apps | ` +
          `domain ${d.machines} machines · ${d.transitions} transitions · ${d.events} events | ` +
          `backend ${b.tables ?? 0} tables · ${b.columns ?? 0} columns · ${b.linked ?? 0} linked | ` +
          `lineage ${lineage?.stats.resolved ?? 0}/${lineage?.stats.operations ?? 0} resolved · ` +
          `${tooltips?.stats.total ?? 0} tips | ` +
          `decisions ${decisions?.stats.adrs ?? 0} ADRs · ` +
          `${decisions?.stats.vectorsPassed ?? 0}/${decisions?.stats.vectors ?? 0} vectors | ` +
          `lenses ${(domains?.lenses ?? [])
            .map((l) => `${l.key} ${l.stats.total} (${l.stats.gaps} undeclared)`)
            .join(' · ') || 'none'} ` +
          `(${Date.now() - started}ms)`
      );
    } catch (err) {
      console.error('[index] failed:', err.message);
    } finally {
      indexing = null;
    }
  })();
  return indexing;
}

// ---- live reload ----------------------------------------------------------
const clients = new Set();
/** New on every start, so a client can tell a restart from a dropped connection. */
const BOOT_ID = `${process.pid}-${Date.now()}`;

function broadcast(event) {
  const payload = `data: ${JSON.stringify(event)}\n\n`;
  for (const res of clients) res.write(payload);
}

let debounce = null;
function scheduleRebuild(file) {
  clearTimeout(debounce);
  debounce = setTimeout(async () => {
    await refreshIndex(`changed ${file}`);
    broadcast({ type: 'reload', file, stats: index?.stats });
  }, 150);
}

// ---- static file serving ---------------------------------------------------
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
};

/**
 * Compression is worth more here than any amount of trimming: the payloads are
 * JSON full of repeated keys and repeated contract paths, which is close to the
 * best case for it. The index goes from 1.9 MB to about a tenth of that on the
 * wire. It is applied only above a size where the compression costs more than
 * it saves, and only where the client asked for it.
 *
 * This is a different saving from the slim index above, and the two do not
 * overlap: gzip makes the bytes cheaper to move, the split makes them cheaper
 * to parse and hold. A browser still has to build every object it is sent,
 * compressed or not.
 */
const GZIP_ABOVE = 4096;

function send(res, status, body, type = 'text/plain; charset=utf-8', req = null) {
  const headers = { 'Content-Type': type, 'Cache-Control': 'no-store' };
  const wants = /\bgzip\b/.test(req?.headers['accept-encoding'] ?? '');
  const size = Buffer.byteLength(body ?? '');
  if (wants && size > GZIP_ABOVE && !COMPRESSED.test(type)) {
    const packed = gzipSync(body);
    headers['Content-Encoding'] = 'gzip';
    headers['Vary'] = 'Accept-Encoding';
    res.writeHead(status, headers);
    return res.end(packed);
  }
  res.writeHead(status, headers);
  res.end(body);
}

/** Already-compressed formats only get bigger. */
const COMPRESSED = /^(image\/(png|jpeg|gif|webp)|font\/woff)/;

/** JSON that has already been stringified once and will not change until the
 *  next rebuild, so it is compressed once rather than on every request. */
const packedCache = new Map();
function sendCachedJson(res, req, key, value) {
  let entry = packedCache.get(key);
  if (!entry) {
    // A thunk, so a filtered variant is built once on the miss rather than
    // rebuilt on every hit and then thrown away.
    const body = Buffer.from(JSON.stringify(typeof value === 'function' ? value() : value));
    entry = { body, packed: gzipSync(body) };
    packedCache.set(key, entry);
  }
  const wants = /\bgzip\b/.test(req.headers['accept-encoding'] ?? '');
  res.writeHead(200, {
    'Content-Type': MIME['.json'],
    'Cache-Control': 'no-store',
    Vary: 'Accept-Encoding',
    ...(wants ? { 'Content-Encoding': 'gzip' } : {}),
  });
  res.end(wants ? entry.packed : entry.body);
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  // The deployment gives the browser one API host and sends the thirteen paths
  // this process owns on to it, so requests for the package now arrive from the
  // front end's origin rather than from this one. That makes them cross-origin,
  // and a cross-origin read of a gated route needs three things said out loud:
  // the origin is allowed, credentials are allowed, and — because these carry a
  // cookie — the allowed origin is named rather than "*", which a browser
  // refuses to accept alongside credentials.
  //
  // Named here rather than reflected back: reflecting whatever arrives is the
  // same as allowing everyone, and the package is the thing behind the gate.
  const origin = req.headers.origin;
  if (origin && ALLOWED_ORIGINS.has(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Access-Control-Allow-Credentials', 'true');
    res.setHeader('Vary', 'Origin');
  }
  // The preflight. It never reaches the gate: a browser sends it without the
  // cookie by definition, so gating it would 401 every request that follows.
  if (req.method === 'OPTIONS') {
    res.writeHead(origin && ALLOWED_ORIGINS.has(origin) ? 204 : 403, {
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '600',
    });
    return res.end();
  }

  try {
    // --- the accounts service, on this origin -------------------------------
    // Everything the accounts service owns is answered here by forwarding it,
    // so one port serves the whole application. That is the only thing nginx
    // was doing: not load, not TLS, just putting both halves on one origin.
    //
    // It has to be one origin. Split across two ports the browser calls it
    // cross-site, and a cross-site cookie needs SameSite=None, which needs
    // Secure, which needs HTTPS — and this deployment is deliberately on plain
    // http for now. So the session would simply stop being sent.
    //
    // Before the gate, because the gate asks this service who you are, and
    // /api/auth/login is how you become anybody.
    if (API_ROUTES.test(url.pathname)) {
      return proxyToApi(req, res, url);
    }

    // --- the gate ----------------------------------------------------------
    // Before anything is read from disk. The sign-in page and the two files it
    // needs are the only things a stranger is given; everything else — every
    // payload and every page — waits for a session.
    let role = null;
    if (!NO_GATE) {
      const seen = await gate(req, res, url, AUTH_BASE);
      if (seen.answered) return;
      role = seen.role;

      // A client reads everything except the decisions, so the refusal is
      // narrow and it happens here, at the door. The honest answer is 403 and
      // not a hollowed-out payload: they either may read a thing or may not.
      if (role === 'client' && !clientMayCall(url.pathname)) {
        return send(res, 403, JSON.stringify({ error: 'not for a client account' }), MIME['.json']);
      }
    }

    // What this account may open, so the tab strip and the payload cannot
    // disagree. The browser is told what it has rather than asked to guess.
    if (url.pathname === '/api/session') {
      return send(res, 200, JSON.stringify({
        role: role ?? 'reviewer',
        layers: layersFor(role ?? 'reviewer'),
        modes: modesFor(role ?? 'reviewer'),
      }), MIME['.json']);
    }

    // --- API ---------------------------------------------------------------
    if (url.pathname === '/api/index') {
      if (!index) await refreshIndex('on demand');
      // ?full=1 puts the held-back fields back in one payload. Nothing in the
      // viewer asks for it; it is there so a script that wants the whole index
      // in one piece does not have to reassemble it from the detail endpoint.
      const full = url.searchParams.get('full') === '1';
      return sendCachedJson(res, req, full ? 'index-full' : 'index', full ? index : indexSlim);
    }

    // The fields held back from the index, for the one contract being read.
    if (url.pathname === '/api/detail') {
      if (!index) await refreshIndex('on demand');
      const file = url.searchParams.get('file') ?? '';
      const detail = detailByFile?.get(file);
      // A contract with nothing held back is not an error — an enum-only file
      // has no properties and no prose — so an empty object is the answer.
      return sendCachedJson(res, req, `detail:${file}`, detail ?? {});
    }

    if (url.pathname === '/api/journeys') {
      if (!journeys) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'journeys', journeys);
    }

    if (url.pathname === '/api/backend') {
      if (!backend) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'backend', backend);
    }

    if (url.pathname === '/api/domain') {
      if (!domain) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'domain', domain);
    }

    if (url.pathname === '/api/lineage') {
      if (!lineage) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'lineage', lineage);
    }

    if (url.pathname === '/api/tooltips') {
      if (!tooltips) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'tooltips', tooltips);
    }

    if (url.pathname === '/api/decisions') {
      if (!decisions) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'decisions', decisions);
    }

    if (url.pathname === '/api/domains') {
      if (!domains) await refreshIndex('on demand');
      return sendCachedJson(res, req, 'domains', domains);
    }

    if (url.pathname === '/api/file' || url.pathname === '/api/tree') {
      const rel = url.searchParams.get('path') ?? '';
      // contain reads to the project root
      const abs = path.resolve(ROOT, rel);
      // /api/tree parses YAML into a structure; /api/file just shows the source,
      // so it can also hand back the prose the decisions view links to
      const allowed = url.pathname === '/api/file' ? /\.(ya?ml|md|json|csv)$/i : /\.ya?ml$/i;
      if (!abs.startsWith(ROOT + path.sep) || !allowed.test(abs)) {
        return send(res, 403, 'refused');
      }
      // The endpoint list alone does not hold the line here. An ADR is a .md
      // file, so refusing /api/decisions and leaving this open lets a client
      // read every decision one path at a time — which is the whole of what
      // they are not supposed to have.
      if (role === 'client') {
        // Built on demand rather than trusted to be there: the registers are
        // only known from this payload, and an unbuilt one would narrow the
        // check to the ADR directory without saying so.
        if (!decisions) await refreshIndex('on demand');
        if (isDecisionFile(rel, decisionFiles(decisions))) return send(res, 403, 'refused');
      }
      const text = await readFile(abs, 'utf8');

      if (url.pathname === '/api/file') return send(res, 200, text);

      const structure = buildStructure(text);
      return send(res, 200, JSON.stringify({ file: rel, ...structure }), MIME['.json']);
    }

    if (url.pathname === '/api/events') {
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        Connection: 'keep-alive',
      });
      res.write('retry: 2000\n\n');
      // Which server process this is. The browser reconnects on its own when
      // the server restarts, but a reconnect delivers no `reload` event — so
      // the page went on running the JavaScript it was served before the
      // restart, and looked simply broken: new views absent, new sections
      // missing, and nothing to say why. Sending the boot id means the client
      // can tell "the connection blinked" from "this is a different server".
      res.write(`data: ${JSON.stringify({ type: 'hello', boot: BOOT_ID })}\n\n`);
      clients.add(res);
      req.on('close', () => clients.delete(res));
      return;
    }

    // A board framed on its own has no icon of its own, so the browser asks for
    // this and logs a 404 that looks like the viewer is broken. It is not.
    if (url.pathname === '/favicon.ico') {
      res.writeHead(204);
      return res.end();
    }

    // --- design boards -----------------------------------------------------
    // The exported UI/UX boards, served so the frontend layer can frame them.
    // They pull in their own script and images by relative path, so the whole
    // folder is served — read-only, and contained to it. Which folder that is
    // comes from the boards reader, so a rename does not need a change here.
    if (url.pathname.startsWith('/designs/')) {
      const boardRoot = path.join(ROOT, journeys?.boardDir ?? 'designs');
      const target = path.resolve(boardRoot, decodeURIComponent(url.pathname.slice('/designs/'.length)));
      if (!target.startsWith(boardRoot + path.sep)) return send(res, 403, 'refused');

      const boardFile = await stat(target).catch(() => null);
      if (!boardFile?.isFile()) return send(res, 404, 'not found');

      const body = await readFile(target);
      return send(res, 200, body, MIME[path.extname(target).toLowerCase()] ?? 'application/octet-stream');
    }

    // --- one frame out of a board ------------------------------------------
    // /frame?board=P01%20Guest%20Web.dc.html&anchor=web-002
    //
    // A board holds every screen on a platform in one 233KB file. A screen's own
    // page wants that screen, not the board scrolled to it — so the element is
    // lifted out and served as a document of its own. The frames carry their
    // styling inline, so nothing is lost by moving one.
    if (url.pathname === '/frame') {
      const boardName = url.searchParams.get('board') ?? '';
      const anchor = (url.searchParams.get('anchor') ?? '').toLowerCase();
      if (!/^[a-z0-9-]{2,24}$/.test(anchor)) return send(res, 400, 'bad anchor');

      const wireframeRoot = path.join(ROOT, 'wireframes');
      const target = path.resolve(wireframeRoot, boardName);
      if (!target.startsWith(wireframeRoot + path.sep) || !/\.html?$/i.test(target)) {
        return send(res, 403, 'refused');
      }
      const info = await stat(target).catch(() => null);
      if (!info?.isFile()) return send(res, 404, 'no such board');

      const frame = extractFrame(await readFile(target, 'utf8'), anchor);
      if (!frame) return send(res, 404, `${boardName} has no frame #${anchor}`);

      // the boards are drawn on white; the wrapper must not inherit the viewer's
      // theme or half the strokes disappear
      return send(res, 200,
        `<!doctype html><html><head><meta charset="utf-8">` +
        `<script src="/wireframes/support.js"></script>` +
        `<style>html,body{margin:0;background:#fff;}` +
        `body{padding:18px 20px;font-family:system-ui,sans-serif;}</style>` +
        `</head><body>${frame}</body></html>`,
        MIME['.html']);
    }

    // --- wireframes --------------------------------------------------------
    // A rendered wireframe per screen, flow and platform. Self-contained HTML
    // with inline CSS, so serving the folder read-only is the whole job.
    if (url.pathname.startsWith('/wireframes/')) {
      const wireframeRoot = path.join(ROOT, 'wireframes');
      const target = path.resolve(
        wireframeRoot,
        decodeURIComponent(url.pathname.slice('/wireframes/'.length))
      );
      if (!target.startsWith(wireframeRoot + path.sep)) return send(res, 403, 'refused');

      const file = await stat(target).catch(() => null);
      if (!file?.isFile()) return send(res, 404, 'not found');

      const body = await readFile(target);
      return send(res, 200, body, MIME[path.extname(target).toLowerCase()] ?? 'application/octet-stream');
    }

    // --- static ------------------------------------------------------------
    const rel = url.pathname === '/' ? '/index.html' : url.pathname;
    const file = path.join(PUBLIC, rel);
    if (!file.startsWith(PUBLIC)) return send(res, 403, 'refused');

    const info = await stat(file).catch(() => null);
    if (!info?.isFile()) return send(res, 404, 'not found');

    const body = await readFile(file);

    // The one thing a page cannot know for itself: which address the accounts
    // service answers on. Inserted high in <head> so it is in place long before
    // the module scripts at the foot of the page read it, but after the charset
    // declaration — that one has to stay inside the first 1024 bytes or the
    // browser starts sniffing. Only html; every other file goes out untouched.
    if (API_META && path.extname(file) === '.html') {
      const html = body.toString('utf8');
      const anchor = /<meta\s+charset=[^>]*>/i.test(html)
        ? /<meta\s+charset=[^>]*>/i
        : /<head(\s[^>]*)?>/i;
      return send(res, 200, html.replace(anchor, (m) => `${m}\n    ${API_META}`), MIME['.html'], req);
    }

    // app.js alone is 270 KB of text, and the boards are larger still
    return send(res, 200, body, MIME[path.extname(file)] ?? 'application/octet-stream', req);
  } catch (err) {
    console.error(err);
    return send(res, 500, String(err.message ?? err));
  }
});

await refreshIndex();

// every layer resolves against the contracts, so every layer is watched
const WATCH_DIRS = [
  args.dir, 'flows', 'screens', 'frontend', 'backend', 'designs', 'UIUX_html', 'states', 'events',
  'wireframes', 'handoff', 'docs',
];
// json and csv joined the list when handoff/ started shipping the joins as data
// — tooltips.json, api-data-lineage.json, screen-index.json, relationships.csv
const WATCHABLE = /\.(ya?ml|xlsx|md|html?|json|csv)$/i;
const watched = [];
for (const dir of WATCH_DIRS) {
  const target = path.join(ROOT, dir);
  try {
    watch(target, { recursive: true }, (_event, filename) => {
      // Excel writes through a lock file and a temp copy; neither is the workbook
      if (filename && WATCHABLE.test(filename) && !/^~\$|^\./.test(path.basename(filename))) {
        scheduleRebuild(`${dir}/${filename}`);
      }
    });
    watched.push(dir);
  } catch {
    // a directory that does not exist yet simply is not watched
  }
}

server.listen(args.port, args.host, () => {
  const url = `http://localhost:${args.port}`;
  console.log(`\n  TICVAI contract viewer  →  ${url}`);
  console.log(`  watching ${watched.join(', ') || 'nothing'} for changes\n`);
  if (args.open) {
    const cmd =
      process.platform === 'win32' ? `start "" "${url}"`
      : process.platform === 'darwin' ? `open "${url}"`
      : `xdg-open "${url}"`;
    import('node:child_process').then(({ exec }) => exec(cmd));
  }
});
