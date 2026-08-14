// Local viewer for the TICVAI contracts.
//   node server.mjs [--port 4173] [--dir contracts] [--open]
//
// Re-indexes on any change under the watched directory and pushes a reload to
// connected browsers over SSE.

import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { watch } from 'node:fs';
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
import { extractFrame } from './lib/wireframes.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(here, '..');
const PUBLIC = path.join(here, 'public');

function parseArgs(argv) {
  const args = { port: 4173, dir: 'contracts', open: false };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--port') args.port = Number(argv[++i]);
    else if (argv[i] === '--dir') args.dir = argv[++i];
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
let indexing = null;

async function refreshIndex(reason = 'startup') {
  if (indexing) return indexing; // coalesce concurrent rebuilds
  indexing = (async () => {
    const started = Date.now();
    try {
      index = await buildIndex(ROOT, args.dir);

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
          `${decisions?.stats.vectorsPassed ?? 0}/${decisions?.stats.vectors ?? 0} vectors ` +
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

function send(res, status, body, type = 'text/plain; charset=utf-8') {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(body);
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  try {
    // --- API ---------------------------------------------------------------
    if (url.pathname === '/api/index') {
      if (!index) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(index), MIME['.json']);
    }

    if (url.pathname === '/api/journeys') {
      if (!journeys) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(journeys), MIME['.json']);
    }

    if (url.pathname === '/api/backend') {
      if (!backend) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(backend), MIME['.json']);
    }

    if (url.pathname === '/api/domain') {
      if (!domain) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(domain), MIME['.json']);
    }

    if (url.pathname === '/api/lineage') {
      if (!lineage) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(lineage), MIME['.json']);
    }

    if (url.pathname === '/api/tooltips') {
      if (!tooltips) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(tooltips), MIME['.json']);
    }

    if (url.pathname === '/api/decisions') {
      if (!decisions) await refreshIndex('on demand');
      return send(res, 200, JSON.stringify(decisions), MIME['.json']);
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
    return send(res, 200, body, MIME[path.extname(file)] ?? 'application/octet-stream');
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

server.listen(args.port, () => {
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
