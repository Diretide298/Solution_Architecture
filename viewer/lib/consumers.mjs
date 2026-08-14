// Reads the declared consumer ("which app calls this") column out of
// handoff/api-list.md.
//
// This is the only place in the repo that maps an individual endpoint to a
// front-end app — the contracts carry no `x-ticvai-consumer` extension — and it
// covers a small fraction of the operations. The viewer reports that coverage
// rather than guessing at the rest.

import { readFile, readdir } from 'node:fs/promises';

/**
 * The canonical platform roster is the app list in the frontend monorepo, not
 * whatever happens to be named in the docs — so apps with no declared endpoint
 * still appear, and the gap is visible.
 */
export async function loadPlatforms(root) {
  try {
    const entries = await readdir(`${root}/repos/ticvai-frontend/apps`, { withFileTypes: true });
    return entries
      .filter((e) => e.isDirectory() && !e.name.startsWith('.'))
      .map((e) => e.name)
      .sort();
  } catch {
    return [];
  }
}

const KNOWN_APPS = new Set([
  'pos', 'backoffice', 'scanner', 'guest', 'employee', 'webb2c', 'web-b2c', 'edge', 'kiosk', 'all',
]);

/** `/orders/{orderId}/refunds` -> `/orders/{}/refunds` so param names cannot break a match. */
export function normalisePath(urlPath) {
  return urlPath.replace(/\{[^}]*\}/g, '{}').replace(/\/+$/, '');
}

const canonicalApp = (name) => (name === 'webb2c' ? 'web-b2c' : name);

export async function loadDeclaredConsumers(root) {
  const path = `${root}/handoff/api-list.md`;
  let text;
  try {
    text = await readFile(path, 'utf8');
  } catch {
    return { map: new Map(), apps: [], source: null };
  }

  const map = new Map(); // "GET /orders/{}" -> [apps]
  const apps = new Set();

  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith('|')) continue;
    const cells = line.split('|').map((c) => c.trim());
    // | status | method | path | permission | offline | consumers |
    if (cells.length < 7) continue;

    const method = cells[2].toUpperCase();
    if (!/^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)$/.test(method)) continue;

    const urlPath = cells[3].replace(/`/g, '').trim();
    if (!urlPath.startsWith('/')) continue;

    const consumers = cells[6]
      .split(/[,/]/)
      .map((c) => c.trim().toLowerCase())
      .filter((c) => KNOWN_APPS.has(c))
      .map(canonicalApp);

    if (!consumers.length) continue;
    for (const app of consumers) apps.add(app);
    map.set(`${method} ${normalisePath(urlPath)}`, consumers);
  }

  return { map, apps: [...apps].sort(), source: 'handoff/api-list.md' };
}
