// What changed in a ticket's artefacts between the tag it was pulled at and the
// tag being served (council C9), and whether a breaking contract change forces
// it onto the new tag.
//
// **A diff of what the developer was handed, not of the files.** Each side is
// the record the connector's own tool returns for that artefact — adam_screen,
// adam_contract with `operation`, adam_table, adam_service — run against the
// package at each tag. So "changed" means the answer `/ticket` writes into
// `.adam/work/<n>/` is different, which is the thing a developer builds from,
// and a reformatted YAML file with the same meaning is not a change.
//
// The older side is built from the release export (lib/releases.mjs) with the
// same builders the server uses for the served package, so both sides went
// through the same code. A view is a few seconds of work; the server keeps one.

import { readFile } from 'node:fs/promises';
import path from 'node:path';
import yaml from 'js-yaml';
import { buildIndex } from './indexer.mjs';
import { buildJourneys } from './journeys.mjs';
import { buildBackend } from './backend.mjs';
import { buildDomain } from './domain.mjs';
import { buildDecisions } from './decisions.mjs';
import { buildDiagrams, readDiagramDetail } from './diagrams.mjs';
import { splitDetail } from './detail.mjs';
import { BY_NAME, lookupFor } from '../mcp/tools.mjs';

/** The kinds a diff compares. The rest (platform, other) are listed as not compared. */
export const COMPARED = new Set(['screen', 'flow', 'contract', 'operation', 'schema', 'table', 'module', 'service', 'adr']);

export const BREAKING_FILE = 'docs/active/breaking-changes.yaml';

const contractsOf = (index) => [...new Set(index.nodes
  .filter((n) => n.type === 'file')
  .map((n) => path.basename(n.file ?? n.name ?? '', '.yaml'))
  .filter(Boolean))];

/** The parts of a package the connector's tools read, built from one root. */
export async function buildView(root, contractsDir = 'contracts') {
  const index = await buildIndex(root, contractsDir);
  const { slim, byFile } = splitDetail(index);
  const operationIds = new Set(index.nodes.filter((n) => n.type === 'operation').map((n) => n.name));
  const schemas = index.nodes.filter((n) => n.type === 'schema');
  const [journeys, backend, domain, decisions] = await Promise.all([
    buildJourneys(root, operationIds),
    buildBackend(root, schemas),
    buildDomain(root, { schemas, operationIds, files: index.nodes.filter((n) => n.type === 'file') }),
    buildDecisions(root),
  ]);
  const diagrams = await buildDiagrams(root, {
    tables: backend.tables ?? [],
    screens: journeys.screens ?? [],
    flows: journeys.flows ?? [],
    contracts: contractsOf(index),
    operations: index.nodes.filter((n) => n.type === 'operation'),
    stateModels: domain?.machines ?? [],
  });
  return { root, indexSlim: slim, detailByFile: byFile, journeys, backend, diagrams, decisions };
}

/**
 * A stand-in for the connector's ViewerClient over a view held in memory, so
 * the tools answer from a release exactly as they answer over HTTP. The served
 * package object has the same fields and is passed straight in.
 */
export function viewClient(view) {
  return {
    async layer(route) {
      if (route === 'index') return view.indexSlim ?? {};
      return view[route] ?? {};
    },
    async detail(file) { return view.detailByFile?.get(file) ?? {}; },
    async diagram(set, name) {
      const found = await readDiagramDetail(view.root, set, name);
      if (!found.ok) throw new Error(found.reason ?? `no ${set} ${name}`);
      return found;
    },
    async file() { return { ok: false, status: 404, text: '' }; },
    async projectId() { return null; },
    async service() { throw new Error('a release view has no accounts service'); },
  };
}

/** One artefact as the tool that answers for it returns it, at one view. */
export async function recordAt(view, kind, id) {
  const [toolName, args] = lookupFor(kind, id);
  const result = await BY_NAME.get(toolName).run(viewClient(view), args)
    .catch((error) => ({ found: false, error: error.message }));
  return { kind, id, from: toolName, ...result };
}

/**
 * The record as text for comparing. `line` is where a thing sits in its file,
 * which moves whenever anything above it does, so it is left out: a screen whose
 * neighbour grew is not a changed screen.
 */
function canonical(record) {
  return JSON.stringify(record, (key, value) => (key === 'line' ? undefined : value), 2);
}

// ---- a line diff ------------------------------------------------------------

/**
 * Unified-style hunks between two texts. Common head and tail are trimmed
 * first — nearly every change is one place in one record — and the middle is
 * an LCS table when it is small enough, a straight replacement when it is not.
 */
export function lineDiff(before, after, { context = 2, cap = 160 } = {}) {
  const a = before.split('\n');
  const b = after.split('\n');
  let head = 0;
  while (head < a.length && head < b.length && a[head] === b[head]) head += 1;
  let tail = 0;
  while (tail < a.length - head && tail < b.length - head
    && a[a.length - 1 - tail] === b[b.length - 1 - tail]) tail += 1;
  const midA = a.slice(head, a.length - tail);
  const midB = b.slice(head, b.length - tail);

  // ops: [' ' | '-' | '+', text, lineA, lineB]
  const ops = [];
  if (midA.length * midB.length <= 4_000_000) {
    const n = midA.length;
    const m = midB.length;
    const w = m + 1;
    const table = new Uint32Array((n + 1) * w);
    for (let i = n - 1; i >= 0; i -= 1) {
      for (let j = m - 1; j >= 0; j -= 1) {
        table[i * w + j] = midA[i] === midB[j]
          ? table[(i + 1) * w + j + 1] + 1
          : Math.max(table[(i + 1) * w + j], table[i * w + j + 1]);
      }
    }
    let i = 0;
    let j = 0;
    while (i < n || j < m) {
      // A removal before an addition where either would do, which is how a
      // diff is read: what was there, then what replaced it.
      if (i < n && j < m && midA[i] === midB[j]) { ops.push([' ', midA[i], i, j]); i += 1; j += 1; }
      else if (i < n && (j === m || table[(i + 1) * w + j] >= table[i * w + j + 1])) { ops.push(['-', midA[i], i, j]); i += 1; }
      else { ops.push(['+', midB[j], i, j]); j += 1; }
    }
  } else {
    midA.forEach((t, i) => ops.push(['-', t, i, 0]));
    midB.forEach((t, j) => ops.push(['+', t, midA.length, j]));
  }

  const removed = ops.filter((o) => o[0] === '-').length;
  const added = ops.filter((o) => o[0] === '+').length;
  if (!removed && !added) return { added, removed, text: '' };

  // Context from the trimmed head and tail, then the middle, cut into hunks.
  const full = [
    ...a.slice(Math.max(0, head - context), head).map((t) => [' ', t]),
    ...ops.map(([op, t]) => [op, t]),
    ...a.slice(a.length - tail, a.length - tail + context).map((t) => [' ', t]),
  ];
  const startA = Math.max(0, head - context) + 1;
  const lines = [];
  let keep = 0;
  let lineA = startA;
  let lineB = startA;
  for (let k = 0; k < full.length; k += 1) {
    const [op, text] = full[k];
    const near = full.slice(Math.max(0, k - context), k + context + 1).some(([o]) => o !== ' ');
    if (op !== ' ' || near) {
      if (!keep) lines.push(`@@ -${lineA} +${lineB} @@`);
      lines.push(`${op}${text}`);
      keep = 1;
    } else keep = 0;
    if (op !== '+') lineA += 1;
    if (op !== '-') lineB += 1;
  }
  const shown = lines.length > cap ? [...lines.slice(0, cap), `… ${lines.length - cap} more diff lines`] : lines;
  return { added, removed, text: shown.join('\n') };
}

// ---- breaking contract changes ----------------------------------------------

/**
 * `docs/active/breaking-changes.yaml`: a list of `{ id, contract, operation,
 * reason, approved-by }`. A top-level list, or one under `changes`, `entries` or
 * `breaking` — the file is authored by hand and the shape is not worth failing on.
 */
export async function readBreaking(root) {
  const text = await readFile(path.join(root, ...BREAKING_FILE.split('/')), 'utf8').catch(() => null);
  if (text == null) return { present: false, entries: [] };
  let doc;
  try {
    doc = yaml.load(text);
  } catch (error) {
    return { present: true, error: `${BREAKING_FILE} does not parse: ${error.message}`, entries: [] };
  }
  const list = Array.isArray(doc) ? doc
    : (doc?.changes ?? doc?.entries ?? doc?.breaking ?? doc?.breakingChanges ?? []);
  const entries = (Array.isArray(list) ? list : [])
    .filter((e) => e && typeof e === 'object')
    .map((e) => ({
      id: String(e.id ?? '').trim(),
      contract: String(e.contract ?? '').trim(),
      operation: String(e.operation ?? e.operationId ?? '').trim(),
      reason: String(e.reason ?? '').trim(),
      approvedBy: String(e['approved-by'] ?? e.approvedBy ?? e.approved_by ?? '').trim(),
    }))
    .filter((e) => e.operation);
  return { present: true, entries };
}

const fold = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '');
const stem = (c) => fold(String(c ?? '').split('/').pop().replace(/\.(ya?ml|json)$/i, ''));
const keyOf = (e) => e.id || `${stem(e.contract)}#${fold(e.operation)}`;

/** Entries at the newer tag that were not at the older one: what arrived in between. */
export function newBreaking(older, newer) {
  const had = new Set(older.entries.map(keyOf));
  return newer.entries.filter((e) => !had.has(keyOf(e)));
}

/**
 * Whether a ticket produces or consumes a breaking entry's operation, judged
 * from what it is linked to at the newer tag. A linked screen or journey that
 * calls the operation makes it a consumer; a linked operation, contract or
 * service that owns it makes it a producer. A frontend ticket is linked to the
 * operations its screen calls as well, so the consumer test goes first.
 */
export async function roleIn(view, touches, entry) {
  const op = fold(entry.operation);
  const contract = stem(entry.contract);
  let producer = null;
  for (const { kind, id } of touches) {
    if (kind === 'screen') {
      const screen = (view.journeys?.screens ?? []).find((s) => fold(s.id) === fold(id));
      if ((screen?.apis ?? []).some((api) => fold(api.operationId) === op)) {
        return { role: 'consumer', via: `screen ${id}` };
      }
    } else if (kind === 'flow') {
      const flow = (view.journeys?.flows ?? []).find((f) => fold(f.id) === fold(id));
      const calls = (flow?.steps ?? []).some((step) => (step.operations ?? [])
        .some((o) => fold(o?.operationId ?? o) === op));
      if (calls) return { role: 'consumer', via: `journey ${id}` };
    } else if (!producer && kind === 'operation') {
      const m = /^(.+)#(.+)$/.exec(String(id));
      const [c, o] = m ? [stem(m[1]), fold(m[2])] : ['', fold(id)];
      if (o === op && (!contract || !c || c === contract)) producer = { role: 'producer', via: `operation ${id}` };
    } else if (!producer && kind === 'contract' && contract && stem(id) === contract) {
      producer = { role: 'producer', via: `contract ${id}` };
    } else if (!producer && kind === 'service') {
      const answer = await BY_NAME.get('adam_service').run(viewClient(view), { name: id, operations: true })
        .catch(() => null);
      const owns = (answer?.service?.operationsByContract ?? []).some((c) => (c.operations ?? [])
        .some((o) => fold(o?.operationId ?? o?.id ?? o) === op));
      if (owns) producer = { role: 'producer', via: `service ${id}` };
    }
  }
  return producer;
}

/**
 * The whole answer for one ticket.
 *
 * `older` and `newer` are views; `touches` is what the ticket is linked to.
 * With `records`, each artefact carries both records, so the connector can write
 * the pinned version of a file without asking again.
 */
export async function diffTicket({ older, newer, touches, records = false }) {
  const artefacts = [];
  for (const { kind, id } of touches) {
    if (!COMPARED.has(kind)) {
      artefacts.push({ kind, id, status: 'not-compared', note: `a ${kind} is not compared between releases` });
      continue;
    }
    const [was, now] = await Promise.all([recordAt(older, kind, id), recordAt(newer, kind, id)]);
    const wasThere = was.found !== false;
    const isThere = now.found !== false;
    let status;
    let diff = { added: 0, removed: 0, text: '' };
    if (!wasThere && !isThere) status = 'missing';
    else if (!wasThere) status = 'added';
    else if (!isThere) status = 'removed';
    else {
      diff = lineDiff(canonical(was), canonical(now));
      status = diff.added || diff.removed ? 'changed' : 'unchanged';
    }
    artefacts.push({
      kind, id, status,
      ...(status === 'changed' ? { added: diff.added, removed: diff.removed, diff: diff.text } : {}),
      ...(records ? { was, now } : {}),
    });
  }

  const [before, after] = await Promise.all([readBreaking(older.root), readBreaking(newer.root)]);
  const breaking = [];
  for (const entry of newBreaking(before, after)) {
    const role = await roleIn(newer, touches, entry);
    if (role) breaking.push({ ...entry, ...role });
  }
  return {
    artefacts,
    changed: artefacts.filter((a) => ['changed', 'added', 'removed'].includes(a.status)).length,
    breaking,
    repinRequired: breaking.length > 0,
    ...(after.error ? { breakingFileError: after.error } : {}),
  };
}
