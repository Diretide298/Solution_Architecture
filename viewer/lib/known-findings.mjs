// The known findings of the package being served: what a pull lists as gaps already on the list.
//
// The lead, 3 November 2026: "a ticket's pull lists the package checks it already fails, so developers stop raising
// change requests for gaps we already know about" (r14 lane k, CHG-R14PUL-001). The package's gate keeps many
// findings in its checks' baselines (check-screen-wiring alone: 4,529); a developer's pull never showed them, so a
// developer met a known gap and raised a change request for it. TICVAI's tools/build-known-findings.py writes
// handoff/known-findings.json at every refresh, each known finding with the artefacts it is about in ADAM's link
// vocabulary (`screen:BO-087`, `operation:orders#createOrder`, `table:orders.sales_order`, `file:<path>`,
// `adr:ADR-0015`); this reads it for the package route `known-findings`, which the connector (mcp/tools.mjs) reads
// once per release as a layer (ETag, held) and filters by the ticket's links. It cannot import this file.
//
// A package without the file (another package, or a release before r14) answers `found: false`, and the pull writes
// no section, as before.

import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';

export const KNOWN_FILE = 'handoff/known-findings.json';

// Parsed once per file version (1.4 MB at r14): asked once per connector per release, and revalidated after.
const held = new Map();

/**
 * The known findings of the package at `root`: { found, stamp, counts, findings: [{ check, rule, key, message,
 * artefacts }] }, or { found: false, stamp: null, why }. `stamp` changes when the file does (its size and mtime), so
 * a caller can key what it builds from the answer on it.
 */
export async function knownFindings(root) {
  const abs = path.join(root, ...KNOWN_FILE.split('/'));
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) {
    held.delete(abs);
    return { found: false, stamp: null, why: `this package has no ${KNOWN_FILE}` };
  }
  const stamp = `${info.mtimeMs}:${info.size}`;
  const hit = held.get(abs);
  if (hit && hit.stamp === stamp) return hit.value;
  const value = await readFile(abs, 'utf8').then((text) => {
    const doc = JSON.parse(text);
    const findings = (Array.isArray(doc.findings) ? doc.findings : [])
      .filter((f) => f && Array.isArray(f.artefacts) && f.artefacts.length)
      .map((f) => ({ check: String(f.check ?? ''), rule: String(f.rule ?? ''), key: String(f.key ?? ''),
        message: String(f.message ?? ''), artefacts: f.artefacts.map(String) }));
    return { found: true, stamp, file: KNOWN_FILE, counts: doc.counts ?? null, findings };
  }).catch((error) => ({ found: false, stamp, why: `${KNOWN_FILE} would not read: ${error.message}` }));
  held.set(abs, { stamp, value });
  return value;
}
