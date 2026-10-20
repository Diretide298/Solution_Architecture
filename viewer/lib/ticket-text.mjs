// The task text of the release ADAM serves, for one ticket: what a pull shows as the ticket's description.
//
// A started ticket keeps the description it started against: op-release.rb leaves it alone and posts a comment.
// A pull that showed only the OpenProject description therefore showed that older text for as long as the ticket
// stayed open, whatever the plan said since (r8 re-walk, `started-ticket-text-fix-not-delivered`: ARCH-TESTS,
// KERNEL-ID, SETUP-HOSTS and PLATFORM-RLS still read "Written at release r6" after CHG-R8WFC-008 rewrote them).
// Chinmay, 20 October 2026: "Whatever we find we should also fix the source so that next gen can clear those out by
// default". So the pull asks the package for the text of the release being served, for every ticket:
//
//   1. the release bundle, handoff/service-docs/op-release.json: each ticket's `pointer`, the exact description a
//      ticket made at that release carries (%ID% is its OpenProject number). Used when the bundle is the served
//      release's (or the package is served from its working tree);
//   2. otherwise the plan, handoff/service-docs/tasks.csv: the row's description, its "Done when" on its own line.
//
// Neither file (another package) is an answer too: `found: false`, and the pull shows the OpenProject text as before.
// The connector (mcp/tools.mjs) compares the answer with the OpenProject description; it cannot import this file.

import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';

export const BUNDLE_FILE = 'handoff/service-docs/op-release.json';
export const PLAN_FILE = 'handoff/service-docs/tasks.csv';
const RELEASE_PREFIX = '- Written at release ';

/** RFC 4180 rows: quoted fields may hold commas, quotes ("") and newlines. */
function csvRows(text) {
  const rows = [];
  let row = [], field = '', quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i += 1; }
      else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ',') { row.push(field); field = ''; }
    else if (ch === '\n' || ch === '\r') {
      if (ch === '\r' && text[i + 1] === '\n') i += 1;
      row.push(field); rows.push(row); row = []; field = '';
    } else field += ch;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows;
}

// Parsed once per file version: the bundle is ~16 MB of JSON and is asked once per pulled ticket.
const held = new Map();
async function cached(abs, parse) {
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) { held.delete(abs); return null; }
  const stamp = `${info.mtimeMs}:${info.size}`;
  const hit = held.get(abs);
  if (hit && hit.stamp === stamp) return hit.value;
  const value = await readFile(abs, 'utf8').then(parse).catch(() => null);
  held.set(abs, { stamp, value });
  return value;
}

function parseBundle(text) {
  const b = JSON.parse(text);
  const pointers = new Map();
  for (const t of b.tickets ?? []) if (t?.key && typeof t.pointer === 'string') pointers.set(t.key, t.pointer);
  const byId = new Map();
  for (const [k, v] of Object.entries(b.ids ?? {})) byId.set(String(v), k);
  return { release: String(b.release ?? ''), ids: b.ids ?? {}, byId, pointers };
}

function parsePlan(text) {
  const rows = csvRows(text);
  const head = rows.shift() ?? [];
  const at = (name) => head.indexOf(name);
  const [k, s, d] = [at('key'), at('subject'), at('description')];
  const out = new Map();
  if (k < 0 || d < 0) return out;
  for (const r of rows) if (r[k]) out.set(r[k], { subject: r[s] ?? '', description: r[d] ?? '' });
  return out;
}

/** A plan row as a ticket's text: its summary, key and release, then What and Done when (the pointer's shape). */
export function planText(key, row, release) {
  const summary = String(row.subject ?? '').replace(/^\[[^\]]+\]\s*/, '').replace(/\s+/g, ' ').trim() || key;
  const desc = String(row.description ?? '').replace(/\s+/g, ' ').trim();
  const at = desc.search(/\bDone when\b/);
  const what = (at >= 0 ? desc.slice(0, at) : desc).trim();
  const done = at >= 0 ? desc.slice(at + 'Done when'.length).replace(/^[\s,:]+/, '') : '';
  const lines = [`**${summary}**`, '', `- Key: \`${key}\``, ...(release ? [`${RELEASE_PREFIX}\`${release}\``] : []), ''];
  if (what) lines.push(`**What:** ${what}`, '');
  if (done) lines.push(`**Done when:** ${done}`, '');
  return lines.join('\n');
}

/**
 * The text of the release being served for one ticket.
 *   root    the served package's folder
 *   id      the OpenProject number (found through the bundle's ids)
 *   key     the plan key, when the caller knows it (a pointer's "Key:" line); used when the id is not in the bundle
 *   served  the tag being served, or null when the package is served from its working tree
 * Answers { found, release, key, id, text, source: 'bundle' | 'plan' }, or { found: false, why }.
 */
export async function ticketText(root, { id = '', key = '', served = null } = {}) {
  const bundle = await cached(path.join(root, ...BUNDLE_FILE.split('/')), parseBundle);
  const number = String(id ?? '').replace(/^#/, '');
  const planKey = (number && bundle?.byId.get(number)) || String(key ?? '') || null;
  if (!planKey) return { found: false, why: `#${number || '?'} is not a ticket of this package's plan` };
  // The bundle's text when it is the release being served (a working tree serves whatever bundle it has).
  if (bundle && (!served || bundle.release === served) && bundle.pointers.has(planKey)) {
    const ticketId = number || String(bundle.ids[planKey] ?? '');
    return {
      found: true, release: bundle.release || served, key: planKey, id: ticketId || null, source: 'bundle',
      file: BUNDLE_FILE, text: bundle.pointers.get(planKey).replace(/%ID%/g, ticketId || '%ID%'),
    };
  }
  const plan = await cached(path.join(root, ...PLAN_FILE.split('/')), parsePlan);
  const row = plan?.get(planKey);
  if (!row) return { found: false, key: planKey, why: `${planKey} is not in this release's plan` };
  const release = served || bundle?.release || null;
  return { found: true, release, key: planKey, id: number || null, source: 'plan', file: PLAN_FILE,
    text: planText(planKey, row, release) };
}
