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
let indexing = null;

async function refreshIndex(reason = 'startup') {
  if (indexing) return indexing; // coalesce concurrent rebuilds
  indexing = (async () => {
    const started = Date.now();
    try {
      index = await buildIndex(ROOT, args.dir);
      const { stats } = index;
      console.log(
        `[index] ${reason}: ${stats.files} files · ${stats.operations} operations · ` +
          `${stats.schemas} schemas · ${stats.links} links · ${stats.errors} errors ` +
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

const watchTarget = path.join(ROOT, args.dir);
try {
  watch(watchTarget, { recursive: true }, (_event, filename) => {
    if (filename && /\.ya?ml$/i.test(filename)) scheduleRebuild(filename);
  });
} catch (err) {
  console.warn(`[watch] disabled: ${err.message}`);
}

server.listen(args.port, () => {
  const url = `http://localhost:${args.port}`;
  console.log(`\n  TICVAI contract viewer  →  ${url}`);
  console.log(`  watching ${watchTarget} for changes\n`);
  if (args.open) {
    const cmd =
      process.platform === 'win32' ? `start "" "${url}"`
      : process.platform === 'darwin' ? `open "${url}"`
      : `xdg-open "${url}"`;
    import('node:child_process').then(({ exec }) => exec(cmd));
  }
});
