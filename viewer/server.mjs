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

      [journeys, backend] = await Promise.all([
        buildJourneys(ROOT, operationIds),
        buildBackend(ROOT, schemas),
      ]);

      const { stats } = index;
      const j = journeys.stats;
      const b = backend.stats;
      console.log(
        `[index] ${reason}: ${stats.files} files · ${stats.operations} operations · ` +
          `${stats.schemas} schemas · ${stats.links} links · ${stats.errors} errors | ` +
          `frontend ${j.flows} flows · ${j.screens} screens · ${j.apps} apps | ` +
          `backend ${b.tables ?? 0} tables · ${b.columns ?? 0} columns · ${b.linked ?? 0} linked ` +
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
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
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

    if (url.pathname === '/api/file' || url.pathname === '/api/tree') {
      const rel = url.searchParams.get('path') ?? '';
      // contain reads to the project root
      const abs = path.resolve(ROOT, rel);
      if (!abs.startsWith(ROOT + path.sep) || !/\.ya?ml$/i.test(abs)) {
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
      clients.add(res);
      req.on('close', () => clients.delete(res));
      return;
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
const WATCH_DIRS = [args.dir, 'flows', 'screens', 'frontend', 'backend'];
const WATCHABLE = /\.(ya?ml|xlsx|md)$/i;
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
