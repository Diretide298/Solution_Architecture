// handoff/relationships.csv — the relationships as the schema owners state them.
//
// This supersedes guessing. The viewer used to work every relationship out from
// column names; the delivery now ships the answer, and with it something the
// inference could never produce: what *kind* of relationship each one is.
//
// handoff/schema-viewer-notes.md is explicit about why that matters:
//
//   platform.scope_node is referenced by 64 tables. identity.principal by 69.
//   Every table that belongs to a venue carries venue_id; every table that
//   records who did something carries a *_by_principal_id. 163 of 406 edges
//   point at one of four hub tables. They are true of nearly every table and
//   therefore say nothing about *this* one.
//
// So an `ambient` edge is hidden unless asked for, a `child` edge is drawn
// strongly, and a `reference` edge is the ordinary case.

import { readFile } from 'node:fs/promises';
import path from 'node:path';

const FILE = path.join('handoff', 'relationships.csv');

/** Minimal RFC-4180 reader — quoted fields, embedded commas, CRLF. */
function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;

  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else quoted = false;
      } else field += c;
    } else if (c === '"') {
      quoted = true;
    } else if (c === ',') {
      row.push(field); field = '';
    } else if (c === '\n') {
      row.push(field); field = '';
      if (row.some((f) => f !== '')) rows.push(row);
      row = [];
    } else if (c !== '\r') {
      field += c;
    }
  }
  row.push(field);
  if (row.some((f) => f !== '')) rows.push(row);
  return rows;
}

/**
 * `how` says what the relationship was read from. Three of these are the
 * database or a person saying so; the rest are the deriver's own inference,
 * and the viewer keeps drawing that distinction.
 */
const DECLARED_HOW = new Set(['DDL foreign key', 'DDL composite FK', 'manual']);

export async function buildRelationships(root) {
  const abs = path.join(root, FILE);
  const text = await readFile(abs, 'utf8').catch(() => null);
  if (text == null) {
    return { present: false, file: FILE, edges: [], byTable: {}, stats: { edges: 0 } };
  }

  const rows = parseCsv(text.replace(/^﻿/, ''));
  const header = rows.shift()?.map((h) => h.trim()) ?? [];
  const at = (name) => header.indexOf(name);
  const iFrom = at('from_table');
  const iColumn = at('from_column');
  const iTo = at('to_table');
  const iKind = at('edge_kind');
  const iHow = at('how');
  const iCross = at('cross_schema');
  const iRequired = at('required');

  const problems = [];
  if (iFrom < 0 || iTo < 0 || iKind < 0) {
    problems.push({
      severity: 'warning',
      kind: 'relationships-unreadable',
      file: FILE,
      message:
        `relationships.csv is missing one of from_table, to_table or edge_kind — ` +
        `columns are: ${header.join(', ')}. Falling back to inference from column names.`,
    });
    return { present: false, file: FILE, edges: [], byTable: {}, problems, stats: { edges: 0 } };
  }

  const edges = [];
  const byTable = {};
  for (const row of rows) {
    const from = (row[iFrom] ?? '').trim();
    const to = (row[iTo] ?? '').trim();
    if (!from || !to) continue;
    const how = (row[iHow] ?? '').trim();
    const edge = {
      from,
      to,
      column: (row[iColumn] ?? '').trim(),
      kind: (row[iKind] ?? 'reference').trim() || 'reference',
      how,
      declared: DECLARED_HOW.has(how),
      crossSchema: /yes/i.test(row[iCross] ?? ''),
      required: /yes/i.test(row[iRequired] ?? ''),
    };
    edges.push(edge);
    (byTable[from] ??= []).push(edge);
  }

  const count = (test) => edges.filter(test).length;
  return {
    present: true,
    file: FILE,
    edges,
    byTable,
    problems,
    stats: {
      edges: edges.length,
      ambient: count((e) => e.kind === 'ambient'),
      child: count((e) => e.kind === 'child'),
      reference: count((e) => e.kind === 'reference'),
      declared: count((e) => e.declared),
      inferred: count((e) => !e.declared),
      crossSchema: count((e) => e.crossSchema),
    },
  };
}
