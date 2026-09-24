/**
 * Choosing what to send with a question.
 *
 * Lifted out of `chat.js` so the floating panel and the full page ask the same
 * way. They were always going to be two places asking one question, and two
 * copies of a scoring function is how the panel comes to give a different answer
 * from the page for the same words — which nobody would report as a bug, because
 * both answers look plausible.
 *
 * Nothing here talks to a model. It reads the package's own search index and
 * picks the excerpts worth paying to send.
 */

import * as auth from '/validation.js';

let cached = null;

/** The package's search index, fetched once per page. */
export async function index() {
  if (cached) return cached;
  const res = await auth.apiFetch('/api/search');
  if (!res.ok) throw new Error(`could not read the package (${res.status})`);
  cached = (await res.json()).entries ?? [];
  return cached;
}

/** The words worth matching on. Short ones and the obvious question words carry
 *  no signal and would match half the package. */
const STOP = new Set(['what', 'which', 'where', 'when', 'does', 'this', 'that', 'with',
  'from', 'into', 'have', 'has', 'the', 'and', 'for', 'are', 'how', 'why', 'who',
  'can', 'does', 'is', 'to', 'of', 'in', 'on', 'a', 'an', 'it', 'do', 'me']);

export function terms(question) {
  return [...new Set(String(question).toLowerCase().match(/[a-z0-9_.]{3,}/g) ?? [])]
    .filter((w) => !STOP.has(w));
}

/**
 * The excerpts to send with a question.
 *
 * Scored rather than filtered: an entry matching three of the question's words
 * beats one matching one, which is the difference between the right table and
 * the first table alphabetically. Capped at a handful, because the service caps
 * the total anyway and a bigger pile is somebody's money.
 */
export async function gather(question) {
  const words = terms(question);
  if (!words.length) return [];
  const entries = await index();
  const scored = [];
  for (const entry of entries) {
    const hay = `${entry.id} ${entry.name} ${entry.sub ?? ''} ${entry.terms ?? ''}`.toLowerCase();
    let score = 0;
    for (const word of words) if (hay.includes(word)) score += 1;
    // An exact id match is worth more than three loose word hits: somebody who
    // types POS-002 means that screen.
    if (words.includes(String(entry.id).toLowerCase())) score += 4;
    if (score) scored.push([score, entry]);
  }
  scored.sort((a, b) => b[0] - a[0]);

  const picked = scored.slice(0, 12).map(([, e]) => e);
  const bits = [];
  for (const entry of picked) {
    const lines = [
      `kind: ${entry.kind}`,
      `id: ${entry.id}`,
      entry.name && entry.name !== entry.id ? `name: ${entry.name}` : '',
      entry.sub ? `about: ${entry.sub}` : '',
      entry.file ? `file: ${entry.file}${entry.line ? `:${entry.line}` : ''}` : '',
      entry.terms ? `\n${entry.terms}` : '',
    ].filter(Boolean);
    bits.push({ title: `${entry.kind} ${entry.id}`, text: lines.join('\n') });
  }
  return bits;
}
