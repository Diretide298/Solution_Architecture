// Local viewer for one or more delivery packages.
//   node server.mjs [--port 4173] [--open]
//
// Which packages, and where they are, is viewer/projects.json. Each is read
// under its own id:
//
//   /pkg/ticvai/index      the project, then the route
//   /api/index             the same route on the default project
//
// The second spelling is what every client used before projects existed and is
// kept until they have moved. `/api/` is also the accounts service's namespace,
// which is the whole reason the reads moved out of it: two processes sharing one
// prefix is why nginx has to name each package route, and why forgetting two of
// them made the landing page draw zeroes for weeks. `/pkg/` needs one rule and
// no list.
//
// Re-indexes on any change under a package and pushes a reload naming it to
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
import { buildPlatforms } from './lib/platforms.mjs';
import { buildUiux } from './lib/uiux.mjs';
import { buildSearch } from './lib/search.mjs';
import { buildDiagrams, readDiagramDetail } from './lib/diagrams.mjs';
import { frameDocument } from './lib/wireframes.mjs';
import { gate } from './lib/session.mjs';
import { clientMayCall, decisionFiles, isDecisionFile, layersFor, modesFor } from './lib/audience.mjs';
import { loadProjects } from './lib/projects.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
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
 * deployment — the reading server on aster.example.com and the accounts service
 * on asterapi.example.com.
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
  'https://aster.ainfinite.ai',
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
  /^\/(api\/(auth|accounts|invites|reset|validation|verdicts|mentions|mentionable|health)(\/|$)|docs|openapi\.json)/;

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
  const args = { port: 4173, open: false, host: undefined };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--port') args.port = Number(argv[++i]);
    // --dir said which folder held the contracts, which is a property of a
    // package rather than of the process. projects.json carries it per project;
    // the flag is accepted and ignored so an old command line does not die.
    else if (argv[i] === '--dir') argv[++i];
    else if (argv[i] === '--host') args.host = argv[++i];
    else if (argv[i] === '--open') args.open = true;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));

/**
 * Everything this process holds about one package.
 *
 * These were nine module-level `let`s, which was the honest shape while the
 * viewer lived inside the only package it could read. They are the same nine
 * fields; the difference is that there is now one set of them per project and
 * every route has to say which set it means.
 *
 * `packed` is per package for the same reason: its keys are route names, so two
 * projects sharing one cache would serve each other's index.
 */
function newPackage(project) {
  return {
    id: project.id,
    name: project.name,
    root: project.root,
    contracts: project.contracts,
    index: null,
    indexSlim: null,
    /** file -> { [nodeId]: { description, properties } } */
    detailByFile: null,
    journeys: null,
    backend: null,
    domain: null,
    lineage: null,
    tooltips: null,
    decisions: null,
    domains: null,
    platforms: null,
    uiux: null,
    search: null,
    diagrams: null,
    /** the in-flight rebuild, so concurrent requests coalesce onto one */
    indexing: null,
    /** JSON stringified and gzipped once per rebuild rather than per request */
    packed: new Map(),
    /** debounce timer for this package's watcher */
    debounce: null,
  };
}

/** project id -> the package above. Populated at startup from projects.json. */
const packages = new Map();
let defaultProjectId = null;

/** The package a request means, or null — which is a 404 and not a crash. */
const packageFor = (id) => packages.get(id) ?? null;

/** `/pkg/<id>/…` — the same character class projects.mjs validates ids against. */
const PKG_PREFIX = /^\/pkg\/([a-z0-9][a-z0-9-]{0,38})(?=\/|$)/;

/**
 * Which package this request is about, and which route of it.
 *
 * Two spellings resolve to one answer:
 *
 *     /pkg/ticvai/index   →  { id: 'ticvai',  route: 'index' }
 *     /api/index          →  { id: <default>, route: 'index' }
 *
 * `rest` is the path with any project prefix removed, which is what the asset
 * routes and the static handler below want — they are the same files under
 * either spelling.
 *
 * `route` is null for anything that is not a package read, and that is the
 * signal the static handler uses rather than a second list of names.
 */
function resolveRoute(pathname) {
  const named = PKG_PREFIX.exec(pathname);
  const id = named ? named[1] : defaultProjectId;
  const rest = named ? pathname.slice(named[0].length) || '/' : pathname;
  const route = named
    ? (rest.startsWith('/') ? rest.slice(1) : rest) || null
    // The pre-project spelling. Only `/api/` is rewritten — `/wireframes/` and
    // `/designs/` are already unprefixed and are handled off `rest`.
    : (rest.startsWith('/api/') ? rest.slice('/api/'.length) : null);
  return { id, rest, route: route || null, prefixed: Boolean(named) };
}

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

/**
 * Rebuild one package.
 *
 * The builds land in locals and are published to `pkg` in a single statement at
 * the end. That is not tidiness: the old version assigned each singleton as its
 * build finished, so a request arriving mid-rebuild could be answered with a new
 * index and an old backend — two halves of two different packages, which is the
 * exact class of disagreement this viewer exists to catch.
 */
async function refreshIndex(pkg, reason = 'startup') {
  if (pkg.indexing) return pkg.indexing; // coalesce concurrent rebuilds
  const ROOT = pkg.root;
  pkg.indexing = (async () => {
    const started = Date.now();
    let index = null, indexSlim = null, detailByFile = null;
    let journeys = null, backend = null, domain = null, decisions = null;
    let lineage = null, tooltips = null, diagrams = null, domains = null;
    let platforms = null, uiux = null, search = null;
    try {
      index = await buildIndex(ROOT, pkg.contracts);
      // split once per rebuild, not once per request
      ({ slim: indexSlim, byFile: detailByFile } = splitDetail(index));

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
      [lineage, tooltips, diagrams] = await Promise.all([
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
        // What ships together. Every name in it is checked against the artefact
        // that already states the same thing from the other end — which is why
        // it waits for the tables and the screens rather than building beside
        // them.
        buildDiagrams(ROOT, {
          tables: backend.tables ?? [],
          screens: journeys.screens ?? [],
          flows: journeys.flows ?? [],
          contracts: [
            ...new Set(
              index.nodes
                .filter((n) => n.type === 'file')
                .map((n) => path.basename(n.file ?? n.name ?? '', '.yaml'))
                .filter(Boolean)
            ),
          ],
          // The two that let the other three subjects be checked rather than
          // believed: the operations behind 03-contracts.yaml's counts, and the
          // state models behind 04-lifecycles.yaml's. `domain` resolves in the
          // first pass above, so it is in hand by the time this one runs.
          operations: index.nodes.filter((n) => n.type === 'operation'),
          stateModels: domain?.machines ?? [],
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

      // **Reads, derives nothing.** `tools/derive-platform.py` emits one
      // `handoff/platform-<code>.json` per platform and this rolls them up —
      // the one thing it adds is the completeness check against `screens/`,
      // because a platform whose derived page is missing would otherwise read
      // as "no gaps" rather than "never looked at".
      platforms = await buildPlatforms(ROOT).catch(() => null);

      // Every board on disk, which is a different question from the one
      // `buildWireframes` answers. That describes the boards a screen points
      // at, because its job is putting a frame on a screen's page — so a board
      // nobody has wired up is absent from the payload entirely, and 23 of the
      // 58 were. Reads the two directories instead.
      uiux = await buildUiux(ROOT, journeys?.screens ?? []).catch(() => null);

      // What the palette can find. It searched `index.nodes` and nothing
      // else — 1,979 contract nodes — so a reviewer looking for a screen id,
      // an ADR or a table got "No match", which reads as "not in this
      // package" and meant "not a contract". Last, because it is built from
      // the others.
      search = await buildSearch(ROOT, {
        journeys, domain, decisions, backend, uiux, platforms,
      }).catch(() => null);

      // Published together. Until this line the package still answers with the
      // last good build; after it, every part is from this one.
      Object.assign(pkg, {
        index, indexSlim, detailByFile,
        journeys, backend, domain, decisions, lineage, tooltips, diagrams, domains,
        platforms, uiux, search,
      });
      // everything stringified and compressed against the old build is stale
      pkg.packed.clear();

      const { stats } = index;
      const j = journeys.stats;
      const b = backend.stats;
      const d = domain.stats;
      console.log(
        `[${pkg.id}] ${reason}: ${stats.files} files · ${stats.operations} operations · ` +
          `${stats.schemas} schemas · ${stats.links} links · ${stats.errors} errors | ` +
          `frontend ${j.flows} flows · ${j.screens} screens · ${j.apps} apps | ` +
          `domain ${d.machines} machines · ${d.transitions} transitions · ${d.events} events | ` +
          `backend ${b.tables ?? 0} tables · ${b.columns ?? 0} columns · ${b.linked ?? 0} linked | ` +
          `lineage ${lineage?.stats.resolved ?? 0}/${lineage?.stats.operations ?? 0} resolved · ` +
          `${tooltips?.stats.total ?? 0} tips | ` +
          `decisions ${decisions?.stats.adrs ?? 0} ADRs · ` +
          `${decisions?.stats.vectorsPassed ?? 0}/${decisions?.stats.vectors ?? 0} vectors | ` +
          `services ${diagrams?.stats.services ?? 0} in ${diagrams?.stats.tiers ?? 0} tiers · ` +
          `${Object.values(diagrams?.lld ?? {}).reduce((a, list) => a + list.length, 0)} LLDs ` +
          `(${diagrams?.layout ?? 'none'}) · ` +
          `${diagrams?.stats.tablesOwned ?? 0}/${(diagrams?.stats.tablesOwned ?? 0) + (diagrams?.stats.tablesUnowned ?? 0)} tables shipped | ` +
          `lenses ${(domains?.lenses ?? [])
            .map((l) => `${l.key} ${l.stats.total} (${l.stats.gaps} undeclared)`)
            .join(' · ') || 'none'} ` +
          `(${Date.now() - started}ms)`
      );
    } catch (err) {
      console.error(`[${pkg.id}] failed:`, err.message);
    } finally {
      pkg.indexing = null;
    }
  })();
  return pkg.indexing;
}

/** Every registered package, built at once. A slow one does not hold up the rest. */
const refreshAll = (reason) =>
  Promise.all([...packages.values()].map((pkg) => refreshIndex(pkg, reason)));

// ---- live reload ----------------------------------------------------------
const clients = new Set();
/** New on every start, so a client can tell a restart from a dropped connection. */
const BOOT_ID = `${process.pid}-${Date.now()}`;

function broadcast(event) {
  const payload = `data: ${JSON.stringify(event)}\n\n`;
  for (const res of clients) res.write(payload);
}

function scheduleRebuild(pkg, file) {
  clearTimeout(pkg.debounce);
  pkg.debounce = setTimeout(async () => {
    await refreshIndex(pkg, `changed ${file}`);
    // The project is on the event now. A reader looking at another package has
    // no reason to reload because this one changed, and could not tell before.
    broadcast({ type: 'reload', project: pkg.id, file, stats: pkg.index?.stats });
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
 *  next rebuild, so it is compressed once rather than on every request. The
 *  cache is the package's own: these keys are route names, and two projects
 *  sharing one would serve each other's index. */
function sendCachedJson(res, req, cache, key, value) {
  let entry = cache.get(key);
  if (!entry) {
    // A thunk, so a filtered variant is built once on the miss rather than
    // rebuilt on every hit and then thrown away.
    const body = Buffer.from(JSON.stringify(typeof value === 'function' ? value() : value));
    entry = { body, packed: gzipSync(body) };
    cache.set(key, entry);
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

    // Which package, and which route of it. Before the gate, because the gate's
    // client check is by route name and the layer a session may open is a
    // question about one project.
    const { id: projectId, rest, route } = resolveRoute(url.pathname);
    const pkg = packageFor(projectId);

    // --- the gate ----------------------------------------------------------
    // Before anything is read from disk. The sign-in page and the two files it
    // needs are the only things a stranger is given; everything else — every
    // payload and every page — waits for a session.
    let role = null;
    let grants = null;
    if (!NO_GATE) {
      const seen = await gate(req, res, url, AUTH_BASE);
      if (seen.answered) return;
      role = seen.role;
      grants = seen.projects;

      // Which package, decided per package. `role` above is the account's, and
      // the account's role is only about administering the installation now —
      // reviewer-or-client is a fact about a person on a project.
      //
      // `grants` is null when the accounts service predates the projects tables.
      // That is "cannot tell", and it is treated as the old behaviour rather
      // than as "no access", so upgrading the two halves in the wrong order does
      // not lock everybody out of everything.
      if (grants && pkg) {
        const grant = grants.find((g) => g.id === pkg.id);
        if (!grant) {
          return send(res, 403, JSON.stringify({
            error: `this account may not read "${pkg.id}"`,
          }), MIME['.json']);
        }
        role = grant.role ?? 'reviewer';
      }

      // A client reads everything except the decisions, so the refusal is
      // narrow and it happens here, at the door. The honest answer is 403 and
      // not a hollowed-out payload: they either may read a thing or may not.
      if (role === 'client' && route && !clientMayCall(route)) {
        return send(res, 403, JSON.stringify({ error: 'not for a client account' }), MIME['.json']);
      }
    }

    // Which packages there are. Not per-package, so it sits outside the prefix
    // — it is the thing a client reads *before* it can name a project.
    //
    // Every active project, for now. Which of them an account may read is a
    // question the accounts service will answer once the permission tables
    // land; until then a signed-in reader sees the registry, which is the same
    // access they have today and no more.
    if (url.pathname === '/pkg/projects' || url.pathname === '/api/projects') {
      // Only what this account may open. A listing that names a package
      // somebody cannot read is a picker with a door that 403s.
      const mine = grants
        ? [...packages.values()].filter((p) => grants.some((g) => g.id === p.id))
        : [...packages.values()];
      return send(res, 200, JSON.stringify({
        default: mine.some((p) => p.id === defaultProjectId) ? defaultProjectId : mine[0]?.id ?? null,
        projects: mine.map((p) => ({
          id: p.id,
          name: p.name,
          // Counts, so a picker can say what is behind each one without
          // fetching six payloads. Null until that package has built.
          artefacts: p.index ? p.index.stats.files : null,
          generatedAt: p.index?.generatedAt ?? null,
        })),
      }), MIME['.json']);
    }

    // A name nobody registered. 404 rather than falling through to the static
    // handler, which would answer a mistyped project with index.html and a
    // reader with a viewer that never loads and never says why.
    if (!pkg && (route || rest.startsWith('/wireframes/') || rest.startsWith('/designs/')
                 || rest.startsWith('/ui-design/'))) {
      return send(res, 404, JSON.stringify({
        error: projectId ? `no project called "${projectId}"` : 'no projects are registered',
        projects: [...packages.keys()],
      }), MIME['.json']);
    }

    // What this account may open, so the tab strip and the payload cannot
    // disagree. The browser is told what it has rather than asked to guess.
    if (route === 'session') {
      return send(res, 200, JSON.stringify({
        project: pkg.id,
        role: role ?? 'reviewer',
        layers: layersFor(role ?? 'reviewer'),
        modes: modesFor(role ?? 'reviewer'),
      }), MIME['.json']);
    }

    // --- API ---------------------------------------------------------------
    // The landing page's whole payload: five counts and two totals.
    //
    // Every number here is already sitting in an object this process built at
    // startup, so this is a projection and not a second index. It is separate
    // from /api/index because the door needs six integers and /api/index is
    // over a megabyte — asking for the whole thing to draw a count is the kind
    // of shortcut that makes a landing page slower than the thing it fronts.
    //
    // `artefacts` is the sum of the five, deliberately: it is what the reader
    // can count on the screen, so it must be what the screen adds up to.
    if (route === 'summary') {
      if (!pkg.index) await refreshIndex(pkg, 'on demand');
      // Taken off the package once. Every name below is the same name it was
      // when there was one package, which is the point — what changed is where
      // the payloads come from, not what any of them says.
      const { index, journeys, backend, domain, decisions, diagrams, uiux } = pkg;
      const counts = {
        frontend: journeys?.screens?.length ?? 0,
        // Boards, not screens. The Frontend layer counts screens and UI/UX
        // counts what has been *drawn* of them — two numbers about the same
        // product that differ, which is the whole reason the layer exists.
        uiux: uiux?.stats?.boards ?? 0,
        contracts: index?.stats?.files ?? 0,
        // State models, not status enums — the layer is named Lifecycles and a
        // status enum is not one. 114 here against 113 in
        // diagrams/hld/04-lifecycles.yaml: two derivations of the same fact
        // that differ by one, which the Audit should be saying out loud.
        domain: domain?.stats?.machines ?? 0,
        backend: backend?.tables?.length ?? 0,
        decisions: decisions?.stats?.adrs ?? 0,
        // The designs in diagrams/, not the services one of them describes —
        // the tab, the door and this all count the same thing or none of them
        // can be trusted.
        services: diagrams?.present
          ? 1 + ['platform', 'hierarchy', 'contracts', 'lifecycles']
            .filter((k) => diagrams[k]?.present).length
            + Object.values(diagrams.lld ?? {}).reduce((a, list) => a + list.length, 0)
          : 0,
      };
      // What is actually in each layer, by name, for the landing page to put
      // inside its clusters once a reader zooms in far enough to ask. Capped:
      // past a few hundred the payload is bigger than the page and the cluster
      // could not draw them all anyway.
      const NAMES = 420;
      const take = (list, of) => (list ?? []).slice(0, NAMES).map(of).filter(Boolean);
      const items = {
        frontend: take(journeys?.screens, (s2) => s2.name || s2.id),
        uiux: take(uiux?.boards, (b) => b.name || b.file),
        contracts: take(index?.nodes?.filter((n) => n.type === 'file'), (n) => n.name),
        domain: take(domain?.machines, (m) => m.entity || m.id),
        backend: take(backend?.tables, (t) => t.name),
        decisions: take(decisions?.adrs, (a) => (a.id ? `ADR-${a.id}` : a.title)),
        services: take(diagrams?.services, (s2) => s2.name),
      };

      return sendCachedJson(res, req, pkg.packed, 'summary', {
        generatedAt: index?.generatedAt ?? null,
        counts,
        items,
        artefacts: Object.values(counts).reduce((a, n) => a + n, 0),
        operations: index?.stats?.operations ?? 0,
        // What each layer holds beyond its headline number, for the panel that
        // opens when one is focused. Counts only — the prose lives in core.js
        // with the layer it describes, and duplicating it here would give it
        // two homes.
        detail: {
          frontend: { flows: journeys?.flows?.length ?? 0, apps: journeys?.apps?.length ?? 0 },
          uiux: {
            frames: uiux?.stats?.frames ?? 0,
            // The number worth putting on the front: a board nobody has wired
            // up is the one most worth looking at.
            unclaimed: uiux?.stats?.unwired ?? 0,
          },
          contracts: {
            operations: index?.stats?.operations ?? 0,
            schemas: index?.stats?.schemas ?? 0,
          },
          domain: { machines: domain?.stats?.machines ?? 0, events: domain?.events?.length ?? 0 },
          backend: {
            schemas: backend?.modules?.length ?? 0,
            columns: backend?.columns?.length ?? 0,
          },
          decisions: {
            documents: decisions?.stats?.documents ?? 0,
            permissions: decisions?.stats?.vectors ?? 0,
          },
        },
      });
    }

    if (route === 'index') {
      if (!pkg.index) await refreshIndex(pkg, 'on demand');
      const { index, indexSlim } = pkg;
      // ?full=1 puts the held-back fields back in one payload. Nothing in the
      // viewer asks for it; it is there so a script that wants the whole index
      // in one piece does not have to reassemble it from the detail endpoint.
      const full = url.searchParams.get('full') === '1';
      return sendCachedJson(res, req, pkg.packed, full ? 'index-full' : 'index',
        full ? index : indexSlim);
    }

    // The fields held back from the index, for the one contract being read.
    if (route === 'detail') {
      if (!pkg.index) await refreshIndex(pkg, 'on demand');
      const file = url.searchParams.get('file') ?? '';
      const detail = pkg.detailByFile?.get(file);
      // A contract with nothing held back is not an error — an enum-only file
      // has no properties and no prose — so an empty object is the answer.
      return sendCachedJson(res, req, pkg.packed, `detail:${file}`, detail ?? {});
    }

    if (route === 'journeys') {
      if (!pkg.journeys) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'journeys', pkg.journeys);
    }

    if (route === 'backend') {
      if (!pkg.backend) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'backend', pkg.backend);
    }

    if (route === 'domain') {
      if (!pkg.domain) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'domain', pkg.domain);
    }

    if (route === 'diagrams') {
      if (!pkg.diagrams) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'diagrams', pkg.diagrams);
    }

    // One low-level file. The payload above carries an index row for each of the
    // 172 and none of their bodies, so the view that opens one comes here.
    //
    // Straight off disk, without waiting on the index: nothing in these files is
    // joined to anything the index holds, and a 25 KB read on demand costs less
    // than 172 of them held for a reader who opens two.
    //
    // No validation here on purpose. The reader checks the set against four
    // literals, the name against a character class, and the resolved path for
    // containment, all before it touches the disk — and one place deciding what
    // is reachable is a rule, while two places is somewhere for them to
    // disagree. Its status comes straight through: 400 for a name that is not
    // one, 404 for a name that is one and is not there, 422 for a file that will
    // not parse. Sending somebody to hunt a typo in a correct name is its own
    // wrong answer.
    if (route === 'diagrams/detail') {
      const found = await readDiagramDetail(
        pkg.root, url.searchParams.get('set'), url.searchParams.get('name'));
      if (!found.ok) {
        res.writeHead(found.status, {
          'Content-Type': 'application/json', 'Cache-Control': 'no-store',
        });
        return res.end(JSON.stringify({ error: found.reason }));
      }
      return sendCachedJson(res, req, pkg.packed, `diagram:${found.set}:${found.name}`, found);
    }

    if (route === 'lineage') {
      if (!pkg.lineage) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'lineage', pkg.lineage);
    }

    if (route === 'tooltips') {
      if (!pkg.tooltips) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'tooltips', pkg.tooltips);
    }

    if (route === 'decisions') {
      if (!pkg.decisions) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'decisions', pkg.decisions);
    }

    if (route === 'domains') {
      if (!pkg.domains) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'domains', pkg.domains);
    }

    if (route === 'platforms') {
      if (!pkg.platforms) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'platforms', pkg.platforms);
    }

    if (route === 'uiux') {
      if (!pkg.uiux) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'uiux', pkg.uiux);
    }

    if (route === 'search') {
      if (!pkg.search) await refreshIndex(pkg, 'on demand');
      return sendCachedJson(res, req, pkg.packed, 'search', pkg.search);
    }

    if (route === 'file' || route === 'tree') {
      const rel = url.searchParams.get('path') ?? '';
      // contain reads to the project root
      const abs = path.resolve(pkg.root, rel);
      // /api/tree parses YAML into a structure; /api/file just shows the source,
      // so it can also hand back the prose the decisions view links to.
      //
      // `.sql` was not on this list, which was fine while nothing pointed at a
      // migration. Search does: a table's definition is `CREATE TABLE` in
      // `backend/V*.sql` and that is the only place 39 of the 379 are actually
      // written down. Refusing it would leave the one kind of result whose line
      // is exact as the one kind that cannot be opened.
      const allowed = route === 'file' ? /\.(ya?ml|md|json|csv|sql)$/i : /\.ya?ml$/i;
      if (!abs.startsWith(pkg.root + path.sep) || !allowed.test(abs)) {
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
        if (!pkg.decisions) await refreshIndex(pkg, 'on demand');
        if (isDecisionFile(rel, decisionFiles(pkg.decisions))) return send(res, 403, 'refused');
      }
      const text = await readFile(abs, 'utf8');

      if (route === 'file') return send(res, 200, text);

      const structure = buildStructure(text);
      return send(res, 200, JSON.stringify({ file: rel, ...structure }), MIME['.json']);
    }

    if (route === 'events') {
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
    // `rest` and not `url.pathname`: these answer at /designs/… and at
    // /pkg/<project>/designs/…, and the second is the one a picker will use.
    if (rest.startsWith('/designs/')) {
      const boardRoot = path.join(pkg.root, pkg.journeys?.boardDir ?? 'designs');
      const target = path.resolve(boardRoot, decodeURIComponent(rest.slice('/designs/'.length)));
      if (!target.startsWith(boardRoot + path.sep)) return send(res, 403, 'refused');

      const boardFile = await stat(target).catch(() => null);
      if (!boardFile?.isFile()) return send(res, 404, 'not found');

      const body = await readFile(target);
      return send(res, 200, body, MIME[path.extname(target).toLowerCase()] ?? 'application/octet-stream');
    }

    // The drawn product design, one level down in `ui-design/designs/`. Served
    // under a single-segment prefix rather than its own path, because the
    // folder id is what a board's URL is keyed on and a nested id would put a
    // slash inside it.
    //
    // The whole folder again, not just the boards: these pull `support.js`,
    // `softlabs-logo.webp` and `brand/*.png` by relative path, so serving the
    // documents alone renders a column of unstyled text with broken images.
    if (rest.startsWith('/ui-design/')) {
      const designRoot = path.join(pkg.root, 'ui-design', 'designs');
      const target = path.resolve(designRoot, decodeURIComponent(rest.slice('/ui-design/'.length)));
      if (!target.startsWith(designRoot + path.sep)) return send(res, 403, 'refused');

      const file = await stat(target).catch(() => null);
      if (!file?.isFile()) return send(res, 404, 'not found');

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
    if (rest === '/frame') {
      const boardName = url.searchParams.get('board') ?? '';
      const anchor = (url.searchParams.get('anchor') ?? '').toLowerCase();
      if (!/^[a-z0-9-]{2,24}$/.test(anchor)) return send(res, 400, 'bad anchor');

      const wireframeRoot = path.join(pkg.root, 'wireframes');
      const target = path.resolve(wireframeRoot, boardName);
      if (!target.startsWith(wireframeRoot + path.sep) || !/\.html?$/i.test(target)) {
        return send(res, 403, 'refused');
      }
      const info = await stat(target).catch(() => null);
      if (!info?.isFile()) return send(res, 404, 'no such board');

      // The whole document, not just the element: the boards that came with
      // the second dump keep their styling in one <style> block and give the
      // frames classes, so an element lifted out on its own renders as a column
      // of unstyled text. frameDocument carries the stylesheet and the ancestor
      // classes out with it.
      const doc = frameDocument(await readFile(target, 'utf8'), anchor);
      if (!doc) return send(res, 404, `${boardName} has no frame #${anchor}`);

      // `?still=1` — the same frame with its scripts taken out, for the canvas,
      // which mounts a few dozen of these at thumbnail size.
      //
      // The alternative was `allow-scripts` on the iframe, and that is the
      // wrong trade twice over: a thumbnail has no behaviour to run, and
      // `allow-scripts` beside `allow-same-origin` is a sandbox that can remove
      // its own sandbox. Left sandboxed with the scripts still in the document,
      // the browser blocks each one and logs it — a real console error, on
      // every tile, for a file doing exactly what was intended.
      if (url.searchParams.get('still') === '1') {
        return send(res, 200, doc.replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi, ''), MIME['.html']);
      }
      return send(res, 200, doc, MIME['.html']);
    }

    // --- wireframes --------------------------------------------------------
    // A rendered wireframe per screen, flow and platform. Self-contained HTML
    // with inline CSS, so serving the folder read-only is the whole job.
    if (rest.startsWith('/wireframes/')) {
      const wireframeRoot = path.join(pkg.root, 'wireframes');
      const target = path.resolve(
        wireframeRoot,
        decodeURIComponent(rest.slice('/wireframes/'.length))
      );
      if (!target.startsWith(wireframeRoot + path.sep)) return send(res, 403, 'refused');

      const file = await stat(target).catch(() => null);
      if (!file?.isFile()) return send(res, 404, 'not found');

      const body = await readFile(target);
      return send(res, 200, body, MIME[path.extname(target).toLowerCase()] ?? 'application/octet-stream');
    }

    // --- static ------------------------------------------------------------
    // The viewer's own files, which belong to no project — so `url.pathname`
    // and not `rest`. A project prefix in front of app.js would be one URL per
    // project for one file, and a cache that has to be told they are the same.
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

// ---- the registry -----------------------------------------------------------
// Read before anything is built, because it is what decides what there is to
// build. A broken entry is reported and skipped rather than fatal: a viewer that
// will not start because one of four packages moved is a viewer that cannot tell
// you which one, and the other three are still worth serving.
const registry = await loadProjects(here);
for (const problem of registry.problems) console.warn(`[projects] ${problem}`);
defaultProjectId = registry.defaultId;
for (const project of registry.projects) {
  if (project.active) packages.set(project.id, newPackage(project));
}
if (!packages.size) {
  console.warn('[projects] nothing is registered — every package read will 404');
}

await refreshAll();

// every layer resolves against the contracts, so every layer is watched
const WATCH_DIRS = [
  'flows', 'screens', 'frontend', 'backend', 'designs', 'UIUX_html', 'states', 'events',
  // diagrams/ is generated by tools/derive-diagrams.py rather than hand-authored,
  // which makes it more likely to be rewritten mid-session than the rest, not less
  'wireframes', 'handoff', 'docs', 'diagrams',
];
// json and csv joined the list when handoff/ started shipping the joins as data
// — tooltips.json, api-data-lineage.json, screen-index.json, relationships.csv
const WATCHABLE = /\.(ya?ml|xlsx|md|html?|json|csv)$/i;

// One set of watchers per package, and a rebuild of that package only. A change
// under one project has no bearing on another and must not cost them a rebuild
// or tell their readers to reload.
const watching = new Map();
for (const pkg of packages.values()) {
  const watched = [];
  // The contracts folder is per package, so it comes off the package rather
  // than off a flag that could only ever describe one of them.
  for (const dir of [pkg.contracts, ...WATCH_DIRS]) {
    const target = path.join(pkg.root, dir);
    try {
      watch(target, { recursive: true }, (_event, filename) => {
        // Excel writes through a lock file and a temp copy; neither is the workbook
        if (filename && WATCHABLE.test(filename) && !/^~\$|^\./.test(path.basename(filename))) {
          scheduleRebuild(pkg, `${dir}/${filename}`);
        }
      });
      watched.push(dir);
    } catch {
      // a directory that does not exist yet simply is not watched
    }
  }
  watching.set(pkg.id, watched);
}

server.listen(args.port, args.host, () => {
  const url = `http://localhost:${args.port}`;
  console.log(`\n  Aster package viewer  →  ${url}`);
  for (const pkg of packages.values()) {
    console.log(`  ${pkg.id.padEnd(14)} ${pkg.root}`);
    console.log(`  ${''.padEnd(14)} /pkg/${pkg.id}/… · watching `
      + `${(watching.get(pkg.id) ?? []).length} folders`
      + `${pkg.id === defaultProjectId ? ' · answers /api/* as well' : ''}`);
  }
  if (!packages.size) console.log('  no packages registered — see viewer/projects.json');
  console.log('');
  if (args.open) {
    const cmd =
      process.platform === 'win32' ? `start "" "${url}"`
      : process.platform === 'darwin' ? `open "${url}"`
      : `xdg-open "${url}"`;
    import('node:child_process').then(({ exec }) => exec(cmd));
  }
});
