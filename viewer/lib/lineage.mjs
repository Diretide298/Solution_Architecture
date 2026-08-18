// handoff/api-data-lineage.json and handoff/screen-index.json — the join the
// viewer could not make for itself.
//
// Until these arrived, the four layers were four separate universes. A contract
// operation knew its permission and its scope; a table knew its columns and its
// foreign keys; nothing knew that `validateAccess` writes `access.scan_event`.
// The link is not derivable from the contracts — `x-ticvai-persistence` marks
// which schemas become tables, not which operations touch them — so the viewer
// was right not to guess it, and wrong only in having nothing to show.
//
//   api-data-lineage.json   every operation -> tables read, tables written,
//                           service, routing, scope, permission, offline
//   screen-index.json       every screen -> board anchor, operations, services,
//                           tables, stored procedures, wave
//
// Counts are deliberately not written here. They were, and they rotted: this
// comment said 654 operations and 347 screens against a package that had moved
// to 776 and 376. A number in a comment is a claim nothing checks.
//
// wireframes/LINKAGE.md draws the whole chain in one line, and it is worth
// keeping in view because every hop is a different file:
//
//   board anchor -> screen definition -> operations -> service -> tables · sproc
//
// ---- what `unresolved` means, and what it does not --------------------------
//
// 336 of the 654 resolve to a table: 299 derived from `x-ticvai-persistence`
// markers, 37 projections mapped by hand. The other 318 carry
// `"source": "unresolved"`.
//
// That is NOT a defect list, and drawing it as one would be the easy mistake.
// The sheet's own footnote says why: "Grey rows resolve to no table — most
// return a computed view, a command with no body, or a health check, and that
// is correct." An operation returning `OrderSummary` or `MediaEntitlements`
// computes it across tables rather than reading one, so there is no persistence
// marker because there is nothing to mark.
//
// So unresolved is a first-class state here — counted, filterable and drawn
// differently — but it is drawn as *not applicable*, not as *missing*. A view
// that quietly showed 336 operations would imply those are all there are; a
// view that flagged 318 as gaps would be worse, because it would invent 318
// pieces of work that do not exist.

import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const LINEAGE = path.join('handoff', 'api-data-lineage.json');
const SCREEN_INDEX = path.join('handoff', 'screen-index.json');

async function readJson(root, rel, problems, what) {
  const abs = path.join(root, rel);
  const info = await stat(abs).catch(() => null);
  if (!info?.isFile()) return null;
  try {
    return JSON.parse(await readFile(abs, 'utf8'));
  } catch (err) {
    problems.push({
      severity: 'error',
      kind: 'lineage-unreadable',
      file: rel.replace(/\\/g, '/'),
      message: `${what} will not parse (${err.message}).`,
    });
    return null;
  }
}

const list = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);

/**
 * @param root
 * @param subjects  { operations, tables, screens } from the contracts, the
 *                  workbook and screens/ — so a lineage row pointing at
 *                  something that does not exist is reported rather than drawn
 */
export async function buildLineage(root, subjects = {}) {
  const problems = [];
  const rawOps = await readJson(root, LINEAGE, problems, 'api-data-lineage.json');
  const rawScreens = await readJson(root, SCREEN_INDEX, problems, 'screen-index.json');

  if (!rawOps && !rawScreens) {
    return { present: false, operations: [], screens: [], problems, stats: { operations: 0 } };
  }

  const contractOps = new Map((subjects.operations ?? []).map((o) => [o.name, o]));
  const knownTables = new Set((subjects.tables ?? []).map((t) => t.name));
  const knownScreens = new Map((subjects.screens ?? []).map((s) => [s.id, s]));

  // ---- the workbook's own version of this join -----------------------------
  // The Data lineage sheet states the same thing as api-data-lineage.json, and
  // it is not the same data. Two places worth knowing about:
  //
  //   routing   the sheet says `write` on 399 rows where the JSON has an empty
  //             string. The export lost the value, so a viewer reading only the
  //             JSON reports 399 operations as having no routing decided when
  //             the workbook has decided all of them.
  //
  //   stored procedure
  //             the sheet has a column for it; the JSON has no field at all.
  //
  // So the sheet is the fuller statement and is merged in, with a disagreement
  // between the two reported rather than silently resolved.
  const sheetRows = new Map((subjects.dataLineage ?? []).map((r) => [r.operation, r]));
  const disagreesWithSheet = [];

  // ---- operations ----------------------------------------------------------
  const operations = [];
  const byTable = new Map(); // table -> { reads: [opId], writes: [opId] }
  const services = new Map();
  const missingTables = new Set();

  const touch = (table, opName, direction) => {
    if (!byTable.has(table)) byTable.set(table, { table, reads: [], writes: [] });
    byTable.get(table)[direction].push(opName);
  };

  for (const [name, row] of Object.entries(rawOps ?? {})) {
    const contract = contractOps.get(name) ?? null;
    if (contractOps.size && !contract) {
      problems.push({
        severity: 'warning',
        kind: 'lineage-unknown-operation',
        file: LINEAGE,
        message: `The lineage has a row for ${name}, which no contract declares. It was generated against a different set of contracts.`,
      });
    }

    const reads = list(row?.reads);
    const writes = list(row?.writes);
    for (const t of reads) {
      if (knownTables.size && !knownTables.has(t)) missingTables.add(t);
      touch(t, name, 'reads');
    }
    for (const t of writes) {
      if (knownTables.size && !knownTables.has(t)) missingTables.add(t);
      touch(t, name, 'writes');
    }

    // Does the lineage agree with the contract it was generated from? These are
    // two independent statements about the same operation, so a disagreement is
    // a real finding rather than a formatting difference.
    const disagreements = [];
    if (contract) {
      if (row?.perm && contract.permission && row.perm !== contract.permission) {
        disagreements.push(`permission ${row.perm} vs ${contract.permission}`);
      }
      if (row?.scope && contract.scopeLevel && row.scope !== contract.scopeLevel) {
        disagreements.push(`scope ${row.scope} vs ${contract.scopeLevel}`);
      }
      if (typeof row?.offline === 'boolean' && Boolean(contract.offlineCapable) !== row.offline) {
        disagreements.push(`offline ${row.offline} vs ${Boolean(contract.offlineCapable)}`);
      }
    }
    if (disagreements.length) {
      problems.push({
        severity: 'warning',
        kind: 'lineage-contradicts-contract',
        file: LINEAGE,
        message:
          `${name}: the lineage and the contract disagree — ${disagreements.join(', ')}. ` +
          `The contract is the source of truth, so the lineage is stale.`,
      });
    }

    // where the two sources differ, the workbook wins on the fields the export
    // dropped, and the difference is recorded rather than smoothed over
    const sheet = sheetRows.get(name) ?? null;
    if (sheet) {
      for (const [field, fromJson, fromSheet] of [
        ['routing', row?.routing || null, sheet.routing],
        ['scope', row?.scope || null, sheet.scope],
        ['service', row?.service || null, sheet.service],
      ]) {
        if (fromJson && fromSheet && fromJson !== fromSheet) {
          disagreesWithSheet.push(`${name} ${field}: json ${fromJson}, sheet ${fromSheet}`);
        }
      }
    }

    const service = row?.service ?? null;
    if (service) {
      if (!services.has(service)) {
        services.set(service, { name: service, operations: [], reads: new Set(), writes: new Set() });
      }
      const entry = services.get(service);
      entry.operations.push(name);
      reads.forEach((t) => entry.reads.add(t));
      writes.forEach((t) => entry.writes.add(t));
    }

    operations.push({
      name,
      contract: row?.contract ?? contract?.module ?? null,
      verb: row?.verb ?? contract?.method ?? null,
      path: row?.path ?? contract?.path ?? null,
      summary: row?.summary ?? contract?.title ?? '',
      reads,
      writes,
      // The JSON's '' is a lost value, not a decision: the workbook says `write`
      // on all 399 of them. So the sheet fills the gap where it has one, and
      // only a field neither source states stays null.
      routing: row?.routing || sheet?.routing || null,
      routingFrom: row?.routing ? 'json' : sheet?.routing ? 'workbook' : null,
      scope: row?.scope || sheet?.scope || null,
      permission: row?.perm || null,
      offline: Boolean(row?.offline || sheet?.offline),
      // the JSON has no field for this at all
      procedure: sheet?.procedure ?? null,
      service,
      // derived | hand-mapped | unresolved — the file's own confidence
      source: row?.source ?? 'unresolved',
      resolved: reads.length > 0 || writes.length > 0,
      known: Boolean(contract),
      disagreements,
    });
  }

  // ---- the two sources, compared -------------------------------------------
  const filledFromSheet = operations.filter((o) => o.routingFrom === 'workbook').length;
  if (filledFromSheet) {
    problems.push({
      severity: 'info',
      kind: 'lineage-json-incomplete',
      file: LINEAGE,
      message:
        `${filledFromSheet} operations carry no routing in api-data-lineage.json and do carry one on ` +
        `the workbook's Data lineage sheet. The export dropped the value; the sheet is the fuller ` +
        `statement, so it is used. Reading the JSON alone reports these as undecided.`,
    });
  }
  if (disagreesWithSheet.length) {
    problems.push({
      severity: 'warning',
      kind: 'lineage-sources-disagree',
      file: LINEAGE,
      message:
        `${disagreesWithSheet.length} operations are described differently by ` +
        `api-data-lineage.json and the workbook's Data lineage sheet ` +
        `(${disagreesWithSheet.slice(0, 3).join('; ')}${disagreesWithSheet.length > 3 ? '…' : ''}). ` +
        `They are generated from the same source, so they should not differ at all.`,
    });
  }
  // the sheet's own footnote says "Blue rows are the ten stored procedures"
  const namedProcedures = new Set(operations.map((o) => o.procedure).filter(Boolean));
  if (namedProcedures.size && namedProcedures.size !== 10) {
    problems.push({
      severity: 'info',
      kind: 'stored-procedure-count',
      file: 'handoff/TICVAI_Schema_Reference.xlsx',
      message:
        `The Data lineage sheet names ${namedProcedures.size} stored procedures and its own footnote ` +
        `calls them "the ten stored procedures" — as does services-and-procedures.md. ` +
        `${10 - namedProcedures.size} are argued for in prose and marked against no operation.`,
    });
  }

  if (missingTables.size) {
    const sample = [...missingTables].slice(0, 4).join(', ');
    problems.push({
      severity: 'warning',
      kind: 'lineage-unknown-table',
      file: LINEAGE,
      message:
        `The lineage names ${missingTables.size} table${missingTables.size > 1 ? 's' : ''} the schema ` +
        `workbook does not list (${sample}${missingTables.size > 4 ? '…' : ''}).`,
    });
  }

  // contract operations the lineage says nothing at all about
  const covered = new Set(operations.map((o) => o.name));
  const uncovered = [...contractOps.keys()].filter((n) => !covered.has(n));
  if (uncovered.length) {
    problems.push({
      severity: 'info',
      kind: 'lineage-missing-operation',
      file: LINEAGE,
      message:
        `${uncovered.length} contract operation${uncovered.length > 1 ? 's have' : ' has'} no lineage row at all ` +
        `(${uncovered.slice(0, 4).join(', ')}${uncovered.length > 4 ? '…' : ''}).`,
    });
  }

  // ---- screens -------------------------------------------------------------
  const screens = [];
  const procedures = new Map();
  for (const [id, row] of Object.entries(rawScreens ?? {})) {
    const defined = knownScreens.get(id) ?? null;
    if (knownScreens.size && !defined) {
      problems.push({
        severity: 'warning',
        kind: 'screen-index-unknown-screen',
        file: SCREEN_INDEX,
        message: `screen-index.json has an entry for ${id}, which no platform file defines.`,
      });
    }

    const ops = list(row?.operations);
    // the index and the screen definition are two statements about the same
    // screen; where they differ, the definition is the one under version control
    if (defined) {
      const declared = new Set(defined.apis.map((a) => a.operationId).filter(Boolean));
      const extra = ops.filter((o) => !declared.has(o));
      if (extra.length && declared.size) {
        problems.push({
          severity: 'info',
          kind: 'screen-index-extra-operation',
          file: SCREEN_INDEX,
          message:
            `screen-index.json says ${id} calls ${extra.join(', ')}, which its own screen definition ` +
            `does not declare.`,
        });
      }
    }

    for (const proc of list(row?.storedProcedures)) {
      if (!procedures.has(proc)) procedures.set(proc, { name: proc, screens: [] });
      procedures.get(proc).screens.push(id);
    }

    screens.push({
      id,
      name: row?.name ?? defined?.name ?? id,
      platform: row?.platform ?? defined?.platform ?? null,
      platformName: row?.platformName ?? defined?.platformName ?? null,
      app: row?.app ?? null,
      route: row?.route ?? null,
      board: row?.board ?? null,
      operations: ops,
      services: list(row?.services),
      reads: list(row?.reads),
      writes: list(row?.writes),
      storedProcedures: list(row?.storedProcedures),
      wave: row?.wave ?? defined?.wave ?? null,
      offline: Boolean(row?.offline),
      defined: Boolean(defined),
    });
  }

  // ---- where used ----------------------------------------------------------
  // The workbook's reverse index, and its subtitle is the reason to have it:
  // "what breaks if this table changes". It reaches further than the lineage
  // alone, because it carries the screens too.
  const whereUsed = (subjects.whereUsed ?? []).map((row) => ({
    table: row.table,
    operations: row.operations,
    screens: row.screens,
    operationCount: row.operationCount ?? row.operations.length,
    screenCount: row.screenCount ?? row.screens.length,
    reached: (row.operationCount ?? row.operations.length) > 0,
  }));
  const unreached = whereUsed.filter((t) => !t.reached);
  if (unreached.length) {
    problems.push({
      severity: 'info',
      kind: 'table-reached-by-nothing',
      file: 'handoff/TICVAI_Schema_Reference.xlsx',
      message:
        `${unreached.length} of ${whereUsed.length} tables are reached by no operation at all ` +
        `(${unreached.slice(0, 4).map((t) => t.table).join(', ')}${unreached.length > 4 ? '…' : ''}). ` +
        `Written by a job, a migration or a trigger — or by nothing yet.`,
    });
  }

  // ---- waves ---------------------------------------------------------------
  // Delivery sequencing, which nothing else in the viewer represents. Held here
  // rather than in journeys.mjs because the index is the only file that states
  // a wave for every screen — the YAML states it for some.
  const waves = new Map();
  for (const screen of screens) {
    const key = screen.wave ?? 'unsequenced';
    if (!waves.has(key)) waves.set(key, { wave: key, screens: [], platforms: new Map() });
    const bucket = waves.get(key);
    bucket.screens.push(screen.id);
    const platform = screen.platform ?? '—';
    bucket.platforms.set(platform, (bucket.platforms.get(platform) ?? 0) + 1);
  }

  const bySource = {};
  for (const op of operations) bySource[op.source] = (bySource[op.source] ?? 0) + 1;
  const byRouting = {};
  for (const op of operations) byRouting[op.routing ?? 'undecided'] = (byRouting[op.routing ?? 'undecided'] ?? 0) + 1;
  const byScope = {};
  for (const op of operations) byScope[op.scope ?? 'unstated'] = (byScope[op.scope ?? 'unstated'] ?? 0) + 1;

  return {
    present: true,
    files: { lineage: LINEAGE.replace(/\\/g, '/'), screenIndex: SCREEN_INDEX.replace(/\\/g, '/') },
    operations: operations.sort((a, b) => a.name.localeCompare(b.name)),
    screens: screens.sort((a, b) => a.id.localeCompare(b.id)),
    tables: [...byTable.values()].sort((a, b) => b.reads.length + b.writes.length - (a.reads.length + a.writes.length)),
    services: [...services.values()]
      .map((s) => ({ ...s, reads: [...s.reads].sort(), writes: [...s.writes].sort() }))
      .sort((a, b) => b.operations.length - a.operations.length),
    procedures: [...procedures.values()].sort((a, b) => a.name.localeCompare(b.name)),
    whereUsed: whereUsed.sort((a, b) => b.operationCount - a.operationCount),
    waves: [...waves.values()]
      .sort((a, b) => String(a.wave).localeCompare(String(b.wave)))
      .map((w) => ({ ...w, platforms: Object.fromEntries(w.platforms) })),
    problems,
    stats: {
      operations: operations.length,
      resolved: operations.filter((o) => o.resolved).length,
      unresolved: operations.filter((o) => !o.resolved).length,
      derived: bySource.derived ?? 0,
      handMapped: bySource['hand-mapped'] ?? 0,
      offline: operations.filter((o) => o.offline).length,
      reading: operations.filter((o) => o.reads.length).length,
      writing: operations.filter((o) => o.writes.length).length,
      tablesTouched: byTable.size,
      routingFromWorkbook: filledFromSheet,
      sourcesDisagree: disagreesWithSheet.length,
      services: services.size,
      procedures: procedures.size,
      storedProcedures: namedProcedures.size,
      tablesIndexed: whereUsed.length,
      tablesReachedByAnOperation: whereUsed.filter((t) => t.reached).length,
      tablesReachedByAScreen: whereUsed.filter((t) => t.screenCount > 0).length,
      screens: screens.length,
      screensWithOperations: screens.filter((s) => s.operations.length).length,
      screensReachingATable: screens.filter((s) => s.reads.length || s.writes.length).length,
      waves: waves.size,
      byRouting,
      byScope,
    },
  };
}
