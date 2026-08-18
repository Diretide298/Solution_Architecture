// docs/ — the decisions, the registers, and the one spec that can be executed.
//
// Everything else the viewer reads is a machine-readable artefact: contracts,
// YAML, a workbook, CSV. This folder is prose, and prose is where the reasons
// live. The ADRs say *why* the shape is the shape; the registers say what was
// counted; `architecture/specs/permission-resolution.md` states the authorisation
// rule the whole platform rests on.
//
// Prose is not renderable as a graph and should not be forced into one. So this
// module does three specific things rather than trying to be a documentation
// browser:
//
//   1. Indexes the ADRs by number, with status, date and what each one closes
//      and constrains — so a reference to ADR-0013 anywhere in the viewer can
//      resolve to a title and a decision instead of a file name.
//
//   2. Pulls the tables out of the registers. `artefact-audit.md` classifies
//      3,297 requirements by the artefact each one needs and marks eight of the
//      fifteen classes as having nothing behind them. That is a finding, and it
//      belongs next to the findings the viewer computes itself.
//
//   3. RUNS the permission vectors.
//
// Point 3 is the one worth the effort. `permission-vectors.json` is marked
// NORMATIVE — "a failing vector is a build failure" — and it is executable:
// each vector is a set of grants, a query, and the verdict the platform must
// reach. A viewer that listed them would be a worse version of the file. A
// viewer that evaluates them is checking that the rule as written actually
// produces the answers the spec claims, which is the one thing reading it
// cannot tell you.

import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';

// ---- markdown helpers -------------------------------------------------------

/**
 * First `**Key:** value` line for a given key.
 *
 * A value may wrap onto following lines — ADR-0001's status is two lines and
 * carries a partial supersession — so continuation lines are joined until the
 * next `**Key:**` or a blank line.
 */
function field(text, key) {
  const match = new RegExp(`^\\*\\*${key}:\\*\\*\\s*(.+(?:\\n(?!\\*\\*|\\s*$).+)*)$`, 'im').exec(text);
  return match ? match[1].replace(/\s+/g, ' ').trim() : null;
}

/** `Proposed · 17 August 2026` — the date six ADRs write inline rather than as
 *  a field of its own. Long form only, which is the only form in use here. */
function dateFromStatus(status) {
  const m = /(\d{1,2}\s+[A-Za-z]+\s+\d{4})/.exec(status ?? '');
  return m ? m[1] : null;
}

/** Every pipe table in a document, as { headers, rows }. */
function tables(text) {
  const out = [];
  const lines = text.split(/\r?\n/);
  for (let i = 0; i < lines.length; i++) {
    if (!/^\s*\|.*\|\s*$/.test(lines[i])) continue;
    if (!/^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1] ?? '')) continue;
    const cells = (line) =>
      line.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
    const headers = cells(lines[i]);
    const rows = [];
    let j = i + 2;
    for (; j < lines.length && /^\s*\|.*\|\s*$/.test(lines[j]); j++) rows.push(cells(lines[j]));
    if (rows.length) out.push({ headers, rows });
    i = j;
  }
  return out;
}

/**
 * A block sitting under a lead-in sentence, flattened into that sentence: a
 * blockquote loses its `>` and joins up, a list becomes its items separated by
 * `; `. Inline emphasis is left as written — lead paragraphs already carry it
 * (sprint-1.md bolds a number mid-sentence) and the pages that show them cope.
 */
function payload(block) {
  const lines = block.split('\n');
  if (block.startsWith('>')) return lines.map((l) => l.replace(/^\s*>\s?/, '').trim()).join(' ');
  if (!/^\s*(?:[-*+]|\d+[.)])\s/.test(block)) return block;
  const items = [];
  for (const line of lines) {
    const item = /^\s*(?:[-*+]|\d+[.)])\s+(.*)$/.exec(line);
    // a wrapped line continues the item above it rather than starting a new one
    if (item) items.push(item[1].trim());
    else if (items.length) items[items.length - 1] += ` ${line.trim()}`;
  }
  // '; ' between items, except after one that already closed itself — sprint-1's
  // bullets are full sentences and ".;" is not punctuation
  return items.reduce((out, item) =>
    out ? `${out}${/[.!?]$/.test(out) ? ' ' : '; '}${item}` : item, '');
}

/** The lead paragraph — the sentence a document opens with, minus its heading. */
function lead(text) {
  const body = text.replace(/^#[^\n]*\n/, '');
  const blocks = body.split(/\n\s*\n/).map((b) => b.trim());
  const at = blocks.findIndex((b) => b && !/^[#|>*-]/.test(b));
  if (at < 0) return '';
  let para = blocks[at];
  // A paragraph ending in ':' is a promise, and what it promises is the block
  // below — which is exactly the shape the filter above just skipped. ADR-0012
  // opens its decision with "TICVAI builds:" and numbers the four things
  // underneath; ADR-0016 says a cost was named "plainly:" and then quotes it.
  // Stopping at the paragraph break printed the setup and dropped the point.
  if (para.endsWith(':')) {
    const next = blocks.slice(at + 1).find((b) => b && !/^([-*_])\1{2,}$/.test(b));
    // A table is not a sentence. Its meaning is in the columns, and every
    // one-line rendering of one reads worse than the bare colon does — ADR-0012's
    // context table would flatten to "Q1; Q2; Q3". Deliberately left dangling.
    if (next && !/^[|#]/.test(next) && !next.startsWith('```')) para += ` ${payload(next)}`;
  }
  const flat = para.replace(/\s+/g, ' ');
  if (flat.length <= 400) return flat;
  // Nothing reached the cap while a lead stopped at the colon; ADR-0012's four
  // numbered items and sprint-1's bullets both pass it. A hard cut lands
  // mid-word — "venue management carr" — which reads as corruption rather than
  // as a limit, so the cut falls back to the last whole word and says so.
  return `${flat.slice(0, 399).replace(/\s+\S*$/, '')}…`;
}

/** Markdown emphasis off a table cell. Not for data — `*` is a real value in a grant. */
const strip = (s) => String(s ?? '').replace(/[*`]/g, '').trim();
/** Data as written. */
const plain = (s) => String(s ?? '').trim();

// ---- the permission resolver ------------------------------------------------

/**
 * The rule, as `permission-resolution.md` states it and the vectors prove it.
 *
 * A grant applies when its permission matches (exactly, or the grant is `*`) and
 * its scope is the query scope or an ancestor of it. Then:
 *
 *   any applicable DENY  -> DENY, regardless of how specific the ALLOW is
 *   otherwise any ALLOW  -> PERMIT
 *   otherwise            -> DENY
 *
 * The middle clause is the one people get wrong. Deny does not merely win at
 * equal depth — V10 proves a venue-level ALLOW loses to a brand-level DENY, so
 * there is no "most specific wins" tie-break anywhere in this. And nothing
 * bubbles upward: a grant at a workstation says nothing about the venue (V04).
 */
function resolve(grants, query) {
  const applies = (grant) => {
    const permission = plain(grant.permission);
    if (permission !== '*' && permission !== query.permission) return false;
    const scope = plain(grant.scope);
    return query.scope === scope || query.scope.startsWith(`${scope}.`);
  };
  const applicable = (grants ?? []).filter(applies);
  if (applicable.some((g) => plain(g.effect).toUpperCase() === 'DENY')) return 'DENY';
  if (applicable.some((g) => plain(g.effect).toUpperCase() === 'ALLOW')) return 'PERMIT';
  return 'DENY';
}

async function runVectors(root, problems) {
  const rel = 'docs/architecture/specs/permission-vectors.json';
  const abs = path.join(root, rel);
  if (!(await stat(abs).catch(() => null))?.isFile()) return null;

  let doc;
  try {
    doc = JSON.parse(await readFile(abs, 'utf8'));
  } catch (err) {
    problems.push({
      severity: 'error', kind: 'vectors-unreadable', file: rel,
      message: `permission-vectors.json will not parse (${err.message}). It is marked NORMATIVE, so this is a build failure.`,
    });
    return null;
  }

  const results = (doc.vectors ?? []).map((vector) => {
    const actual = resolve(vector.grants, vector.query ?? {});
    return {
      id: vector.id,
      proves: vector.proves ?? '',
      grants: (vector.grants ?? []).map((g) => ({
        permission: strip(g.permission), scope: strip(g.scope), effect: strip(g.effect).toUpperCase(),
      })),
      query: { permission: vector.query?.permission ?? '', scope: vector.query?.scope ?? '' },
      expect: vector.expect,
      actual,
      pass: actual === vector.expect,
    };
  });

  const failed = results.filter((r) => !r.pass);
  if (failed.length) {
    problems.push({
      severity: 'error',
      kind: 'permission-vector-failed',
      file: rel,
      message:
        `${failed.length} of ${results.length} permission vectors do not produce the verdict the spec ` +
        `requires (${failed.map((f) => f.id).join(', ')}). The file says a failing vector is a build failure.`,
    });
  }

  return {
    file: rel,
    note: doc.$comment ?? null,
    fixture: doc.fixture ?? null,
    vectors: results,
    stats: { total: results.length, passed: results.length - failed.length, failed: failed.length },
  };
}

// ---- ADRs -------------------------------------------------------------------

async function readAdrs(root, problems) {
  const dir = path.join(root, 'docs', 'adr');
  const files = (await readdir(dir).catch(() => [])).filter((f) => /^\d{4}-.+\.md$/i.test(f));
  const adrs = [];

  for (const file of files.sort()) {
    const text = await readFile(path.join(dir, file), 'utf8').catch(() => '');
    if (!text) continue;
    const id = file.slice(0, 4);
    // ADR-0001..0015 head with a colon, 0016..0024 with an em dash. Matching
    // only the colon left the fallback capturing the whole heading including
    // the id, which app.js then prints a second time. Splitting on the first
    // colon instead is worse, not better: ADR-0021 is
    // "# ADR-0021 — Qdrant: one collection per embedding model", so a colon
    // split silently drops the word the title is about.
    const heading = /^#\s*(?:ADR-\d+\s*[:—–-]\s*)?(.+)$/im.exec(text);
    const status = field(text, 'Status');
    // "Accepted — split rule superseded by ADR-0014; isolation claim amended"
    // is one status line making three statements. The verdict is the first word;
    // the rest is the qualifier, and it is the part worth reading.
    //
    // The emphasis has to come off first. ADR-0001 was rewritten to
    // "**Superseded** by ADR-0014 and ADR-0017" precisely so its supersession
    // could not be missed, and a first-word match that cannot see past the
    // asterisks returned null — which made `qualifier` empty, which made
    // `partlySuperseded` false on every ADR, which removed the `part` badge
    // that was the only signal the viewer had. The edit that made the
    // supersession unmissable in the file made it invisible in the tool.
    // tools/check-package.py:190 has always stripped emphasis before the same
    // test, which is why the checker passed while the viewer did not.
    const plainStatus = status ? status.replace(/[*_`]/g, '') : null;
    const verdict = plainStatus ? (/^\s*([A-Za-z]+)/.exec(plainStatus)?.[1] ?? null) : null;
    const qualifier = plainStatus && verdict
      ? plainStatus.slice(plainStatus.indexOf(verdict) + verdict.length).replace(/^[\s—–·-]+/, '')
      : '';
    const supersededBy = [...(status ?? '').matchAll(/ADR-(\d{4})/g)].map((m) => m[1]);

    if (status && !/accepted|superseded|proposed|withdrawn/i.test(status)) {
      problems.push({
        severity: 'warning', kind: 'adr-unknown-status', file: `docs/adr/${file}`,
        message: `ADR-${id} has status "${status}", which is not one of Accepted, Proposed, Superseded or Withdrawn.`,
      });
    }
    if (!status) {
      problems.push({
        severity: 'warning', kind: 'adr-no-status', file: `docs/adr/${file}`,
        message: `ADR-${id} states no status, so whether it is binding cannot be told from the file.`,
      });
    }

    // the sentence after "## Decision" — the decision itself, not the context
    const decision = /##\s*Decision\s*\n+([\s\S]*?)(?=\n#{2,3}\s|\n---)/i.exec(text);
    adrs.push({
      id,
      number: Number(id),
      title: heading ? heading[1].trim() : file,
      file: `docs/adr/${file}`,
      status,
      verdict,
      qualifier,
      // an ADR that is Accepted *and* partly superseded is the case that misleads
      // — it reads as current in a list and is not current in the part that matters
      supersededBy,
      partlySuperseded: Boolean(qualifier && /supersede/i.test(qualifier)),
      // ADR-0019..0024 stopped writing a **Date:** field and put the date
      // inline after a `·` in the status line instead. Both shapes are read,
      // because six ADRs with no date is not a smaller problem than one.
      date: field(text, 'Date') ?? dateFromStatus(plainStatus),
      closes: field(text, 'Closes'),
      withdraws: field(text, 'Withdraws'),
      constrains: (field(text, 'Constrains') ?? '').split('·').map((s) => s.trim()).filter(Boolean),
      // Which domain lens this belongs to, stated rather than inferred. An ADR
      // is prose and reaches nothing, so the graph can only match it on mention
      // — and ADR-0021 decides how AI vectors are partitioned while discussing
      // Qdrant and RLS, naming no operation in its summary. Declaration is the
      // only thing that finds it.
      domains: (field(text, 'Domains') ?? '').split(/[·,]/).map((s) => s.trim().toLowerCase()).filter(Boolean),
      supersedes: field(text, 'Supersedes'),
      decision: decision ? lead(`#\n${decision[1]}`) : lead(text),
      lead: lead(text),
      // An ADR revised after acceptance is worth flagging, because the accepted
      // date is then not the date of what it now says. Matching only
      // "## Amendment" missed three same-day revisions written as "## Addendum",
      // "# Addendum" and "# History" — including ADR-0020's, which records two
      // cross-tenant defects found and fixed. Those read as never revised.
      amended: /^#{1,3}\s*(Amendment|Addendum|History|Revision)/im.test(text),
      bytes: text.length,
    });
  }
  return adrs;
}

// ---- registers --------------------------------------------------------------

const REGISTER_DIRS = [
  { dir: 'docs/registers', group: 'register' },
  { dir: 'docs/architecture', group: 'architecture' },
  { dir: 'docs/active', group: 'active' },
];
/** Narrative artefacts that live with the build outputs rather than in docs/. */
const HANDOFF_DOCS = [
  'artefact-audit.md', 'requirements-coverage.md', 'integration-register.md',
  'services-and-procedures.md', 'storage-design.md', 'deployment-models.md',
  'platform-deployment.md', 'screen-contract-linkage.md', 'schema-viewer-notes.md',
];

async function readDoc(root, rel, group) {
  const abs = path.join(root, rel);
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) return null;
  const text = await readFile(abs, 'utf8').catch(() => '');
  if (!text) return null;
  const heading = /^#\s*(.+)$/m.exec(text);
  const found = tables(text);
  return {
    id: path.basename(rel, '.md'),
    title: heading ? strip(heading[1]) : path.basename(rel),
    file: rel.replace(/\\/g, '/'),
    group,
    lead: lead(text),
    lines: text.split(/\r?\n/).length,
    // the tables are the register; the prose around them is the reason for it
    tables: found.map((t) => ({ headers: t.headers, rows: t.rows, count: t.rows.length })),
    rows: found.reduce((n, t) => n + t.rows.length, 0),
    modified: info.mtime.toISOString(),
  };
}

export async function buildDecisions(root) {
  const problems = [];

  const adrs = await readAdrs(root, problems);
  const permissions = await runVectors(root, problems);

  const documents = [];
  for (const { dir, group } of REGISTER_DIRS) {
    const files = (await readdir(path.join(root, dir)).catch(() => []))
      .filter((f) => /\.md$/i.test(f) && f.toLowerCase() !== 'readme.md');
    for (const file of files.sort()) {
      const doc = await readDoc(root, `${dir}/${file}`, group);
      if (doc) documents.push(doc);
    }
  }
  for (const file of ['docs/overview.md', 'docs/glossary.md', 'docs/gotchas.md', 'docs/STRUCTURE.md']) {
    const doc = await readDoc(root, file, 'guide');
    if (doc) documents.push(doc);
  }
  for (const file of HANDOFF_DOCS) {
    const doc = await readDoc(root, `handoff/${file}`, 'handoff');
    if (doc) documents.push(doc);
  }

  // The artefact audit is the one register that states what the package does NOT
  // have. Everything else in the viewer measures what is there, so this is the
  // only place a reader learns that 347 requirements need a report register and
  // no report register exists. Lifted out so it can be shown as findings.
  const audit = documents.find((d) => d.id === 'artefact-audit');
  const gaps = [];
  for (const table of audit?.tables ?? []) {
    const head = table.headers.map((h) => h.toLowerCase());
    const at = (name) => head.findIndex((h) => h.includes(name));
    const [reqs, klass, hold, artefact] = [at('req'), at('class'), at('hold'), at('artefact')];
    if (klass < 0 || artefact < 0) continue;
    for (const row of table.rows) {
      const verdict = row[artefact] ?? '';
      const open = /🔴|🟡/.test(verdict);
      gaps.push({
        requirements: Number(strip(row[reqs] ?? '').replace(/[^\d]/g, '')) || 0,
        class: strip(row[klass]),
        holding: strip(row[hold] ?? ''),
        verdict: strip(verdict),
        state: /🔴/.test(verdict) ? 'missing' : /🟡/.test(verdict) ? 'partial' : 'covered',
        open,
      });
    }
  }
  gaps.sort((a, b) => b.requirements - a.requirements);

  const missing = gaps.filter((g) => g.state === 'missing');
  if (missing.length) {
    problems.push({
      severity: 'warning',
      kind: 'artefact-class-missing',
      file: 'handoff/artefact-audit.md',
      message:
        `${missing.length} artefact class${missing.length > 1 ? 'es have' : ' has'} nothing behind ` +
        `${missing.length > 1 ? 'them' : 'it'} — ${missing.slice(0, 3).map((g) => `${g.class} (${g.requirements} reqs)`).join(', ')}` +
        `${missing.length > 3 ? '…' : ''}. Counted by the delivery's own audit, not by the viewer.`,
    });
  }

  return {
    present: adrs.length > 0 || documents.length > 0,
    adrs,
    documents,
    permissions,
    gaps,
    problems,
    stats: {
      adrs: adrs.length,
      accepted: adrs.filter((a) => /accepted/i.test(a.status ?? '')).length,
      amended: adrs.filter((a) => a.amended).length,
      documents: documents.length,
      registers: documents.filter((d) => d.group === 'register').length,
      architecture: documents.filter((d) => d.group === 'architecture').length,
      handoff: documents.filter((d) => d.group === 'handoff').length,
      rows: documents.reduce((n, d) => n + d.rows, 0),
      vectors: permissions?.stats.total ?? 0,
      vectorsPassed: permissions?.stats.passed ?? 0,
      vectorsFailed: permissions?.stats.failed ?? 0,
      artefactClasses: gaps.length,
      artefactGaps: gaps.filter((g) => g.open).length,
      requirementsUnserved: gaps.filter((g) => g.open).reduce((n, g) => n + g.requirements, 0),
    },
  };
}
