/**
 * Reads diagrams/ — what ships together, and what each thing is made of.
 *
 * The rest of the package describes the system by what things *are*: a contract
 * defines operations, a schema becomes tables, a screen names operations. None
 * of that says what is deployed as one unit, and the answer is not derivable
 * from any of it — two contracts can belong to one service and one schema can
 * be read by twelve. So it arrives as its own artefact: five high-level files,
 * one per subject, each of whose nodes carries a `ref` at the file below it.
 *
 * ── the join, stated twice ────────────────────────────────────────────────
 *
 * Every fact here is also stated somewhere the viewer already reads:
 *
 *   which service owns a table     diagrams/lld/services/*.yaml and the
 *                                  workbook's Tables sheet
 *   which service writes another   the HLD's crossServiceWrites, and each
 *                                  LLD's own writesOutside
 *   how many operations a          hld/03-contracts.yaml, the LLD file below
 *   contract has                   it, and contracts/ itself
 *   which entities have            hld/04-lifecycles.yaml and states/
 *   a lifecycle
 *
 * That is the point rather than a redundancy to be tidied away. Two independent
 * statements of one fact can be checked against each other; one statement can
 * only be believed. So this file reads both ends and reports where they differ,
 * and it resolves nothing silently — a disagreement is a finding, not a bug in
 * the reader.
 *
 * ── why the folder is located rather than known ───────────────────────────
 *
 * On 25 August the folder was restructured: `hld.yaml` became
 * `hld/02-services.yaml`, `hierarchy.yaml` became `hld/01-hierarchy.yaml`, and
 * the sixteen loose `lld/*.yaml` moved into `lld/services/`. The old files were
 * left on disk. Nothing failed. This reader went on opening `diagrams/hld.yaml`,
 * which still parsed, still named sixteen services, and was three quarters of an
 * hour out of date — and the viewer rendered superseded data with every
 * validator green.
 *
 * That is the failure the folder's own README is about, and it is the reason
 * nothing below hard-codes a path. `diagrams/README.yaml` is the index: it names
 * the five HLD files and the four LLD folders, and everything is read through
 * it. A package with no README.yaml is a package from before the split, and the
 * old flat layout is read instead — `layout` says which was found, so a caller
 * can never mistake one for the other.
 *
 * And because the same thing will happen again, a file sitting in diagrams/ that
 * README.yaml does not list, whose subject *is* listed under another name, is
 * reported as `diagram-superseded` rather than ignored. A stale file nobody
 * reads is harmless; a stale file a reader might pick up instead is the whole
 * defect.
 *
 * ── how the subjects are recognised ───────────────────────────────────────
 *
 * By shape, not by filename. The numeric prefixes (`00-`, `02-`) are an ordering
 * convenience and two of the five files carry the same `id: HLD`, so neither is
 * a key. A file with `stateModels` is the lifecycles subject wherever it is
 * filed and whatever it is numbered; the filename is the fallback, used only
 * where the shape says nothing.
 *
 * ── naming ────────────────────────────────────────────────────────────────
 *
 * The two ends do not spell the services the same way. The diagrams say
 * `OrderService`; the workbook says `Order`. Neither is wrong and neither is
 * going to change, so both fold to a key — lowercased, with a trailing
 * "service" dropped — and the display name comes from the diagrams, which are
 * the artefact whose subject this is.
 *
 * ── the low level is indexed, not inlined ─────────────────────────────────
 *
 * 113 lifecycles, 28 contracts, 16 services and 15 platforms is a megabyte of
 * YAML, and one payload carrying all of it would be a payload nobody can afford
 * to send on every page load. Each set is read once, checked against the HLD
 * that claims to summarise it, and reduced to an index row — filename, id,
 * title, and the two or three numbers a list needs to be worth looking at. The
 * body of one file is fetched on demand through `readDiagramDetail`.
 */

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import yaml from 'js-yaml';

/** The four low-level sets. Also the allow-list `readDiagramDetail` validates against. */
export const DIAGRAM_SETS = ['services', 'platforms', 'contracts', 'lifecycles'];

/** The five high-level subjects, in the order the README reads them. */
export const DIAGRAM_SUBJECTS = ['platform', 'hierarchy', 'services', 'contracts', 'lifecycles'];

/** `OrderService`, `Order`, `order service` → `order`. */
const keyOf = (name) =>
  String(name ?? '').trim().toLowerCase().replace(/\s*service$/, '').replace(/[^a-z0-9]/g, '');

/** A cell or key the workbook leaves as an em dash means "nobody". */
const named = (value) => {
  const text = String(value ?? '').trim();
  return text && text !== '—' && text !== '-' ? text : null;
};

/** `55%` → 55, `null` → null. Kept as a number so it can be compared and drawn. */
const percent = (value) => {
  const match = /(\d+(?:\.\d+)?)\s*%/.exec(String(value ?? ''));
  return match ? Number(match[1]) : null;
};

const list = (value) => (Array.isArray(value) ? value : []);
const posix = (rel) => String(rel).split(path.sep).join('/');

async function readYaml(file) {
  try {
    return yaml.load(await readFile(file, 'utf8')) ?? null;
  } catch (err) {
    return { __error: err.message, __missing: err.code === 'ENOENT' };
  }
}

/**
 * Not there at all, as against there and broken.
 *
 * The distinction runs through the whole module. A package with no diagrams/ has
 * not been asked this question yet and gets silence; a diagram that exists and
 * will not parse is somebody's afternoon and gets a finding. Conflating the two
 * puts an error on every package that simply does not ship the folder, and a
 * validator that cries on healthy input is a validator people switch off.
 */
const absent = (doc) => Boolean(doc?.__missing);

/**
 * Every `.yaml` under diagrams/, relative to the package root, posix-separated.
 *
 * The listing is what is actually on disk, which is the only half of the
 * superseded check that cannot be got from the README — the README states what
 * *should* be there, and the disagreement between the two is the finding.
 */
async function walkYaml(root, rel, out = []) {
  let entries = [];
  try {
    entries = await readdir(path.join(root, rel), { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    const child = `${rel}/${entry.name}`;
    if (entry.isDirectory()) await walkYaml(root, child, out);
    else if (entry.isFile() && /\.ya?ml$/i.test(entry.name)) out.push(child);
  }
  return out;
}

/**
 * Which of the five subjects a high-level document is, decided by what it holds.
 *
 * Order matters here. `02-services.yaml` and `03-contracts.yaml` both carry a
 * `tiers` key and they mean different things by it — services is a list of tier
 * objects, contracts is a map from tier name to prose — so contracts is tested
 * first, by the presence of its own `contracts` array, and services is
 * recognised only once that has not matched.
 */
function subjectOf(doc) {
  if (!doc || typeof doc !== 'object') return null;
  if (Array.isArray(doc.stateModels)) return 'lifecycles';
  if (Array.isArray(doc.contracts)) return 'contracts';
  if (Array.isArray(doc.tiers) || Array.isArray(doc.crossServiceWrites)) return 'services';
  if (Array.isArray(doc.levels) || Array.isArray(doc.spine)) return 'hierarchy';
  if (Array.isArray(doc.actors) || Array.isArray(doc.surfaces)) return 'platform';
  return null;
}

/** The filename's opinion, used only where the shape has none. `02-services.yaml` → `services`. */
function subjectFromName(file) {
  const stem = path.basename(String(file), path.extname(String(file))).replace(/^\d+[-_]/, '');
  const folded = stem.toLowerCase();
  if (DIAGRAM_SUBJECTS.includes(folded)) return folded;
  if (folded === 'hld') return 'services';
  return null;
}

/**
 * One index row per low-level file. The headline fields differ by set because
 * the sets are not the same kind of thing — a lifecycle is summarised by how
 * many ways it can move, a platform by how many screens sit on it — and a row
 * carrying the union of all four would be four fifths empty in every case.
 */
function headline(set, doc) {
  if (set === 'lifecycles') {
    return {
      entity: doc.entity ?? null,
      contract: doc.contract ?? null,
      owner: doc.owner ?? null,
      enum: doc.enum ?? null,
      initial: list(doc.initial),
      terminal: list(doc.terminal),
      transitions: list(doc.transitions).length,
      guarded: list(doc.transitions).filter((t) => t?.guard).length,
      emits: list(doc.transitions).reduce((a, t) => a + list(t?.emits).length, 0),
      source: doc.source ?? null,
    };
  }
  if (set === 'contracts') {
    return {
      tier: doc.tier ?? null,
      service: doc.service ?? null,
      operations: list(doc.operations).length,
      offline: list(doc.operations).filter((o) => o?.offline).length,
      // `audience` is a list on the operations and a scalar count on the tier
      // row above them; both say the same thing and the two are compared below.
      guestCallable: list(doc.operations).filter((o) => list(o?.audience).includes('guest')).length,
    };
  }
  if (set === 'platforms') {
    return {
      audience: doc.audience ?? null,
      operator: doc.operator ?? null,
      app: doc.app ?? null,
      formFactor: doc.formFactor ?? null,
      runtime: doc.runtime ?? null,
      offlineCapable: doc.offlineCapable ?? null,
      screens: list(doc.screens).length,
      modules: list(doc.modulesUsed).length,
      services: list(doc.servicesCalled).length,
    };
  }
  // Services. `operationsByContract` is a list of `{contract, count, operations[]}`
  // — the count is the summary and the array is the detail, and it is the count
  // that belongs in an index row.
  return {
    tier: doc.tier ?? null,
    contracts: list(doc.operationsByContract).length,
    operations: list(doc.operationsByContract).reduce((a, c) => a + (c?.count ?? 0), 0),
    tables: list(doc.tables).length,
    schemas: list(doc.schemas).length,
    screens: list(doc.screens).length,
    flows: list(doc.flows).length,
    flowCoverage: percent(doc.coverage?.percent),
  };
}

/**
 * Reads one low-level file by set and name.
 *
 * This is reached over HTTP with both arguments coming off a query string, so
 * neither is trusted. The set must be one of four literals — not a folder that
 * happens to exist, one of *these four* — and the name must be a bare filename
 * with no separator in it at all. The character class permits a dot, because
 * filenames have extensions, which means it also permits `..`; that is rejected
 * explicitly rather than left to a reader to notice. And after all of that the
 * resolved path is checked to still be inside the folder it was built from,
 * because a validation argued for in a comment is a validation that can be
 * wrong, and the last line of defence should not be an argument.
 *
 * @param root  the package root
 * @param set   one of DIAGRAM_SETS
 * @param name  a bare filename, with or without its `.yaml`
 * @returns {{ok: true, set, name, file, doc}} or {{ok: false, status, reason}}
 */
export async function readDiagramDetail(root, set, name) {
  const which = String(set ?? '');
  if (!DIAGRAM_SETS.includes(which)) {
    return {
      ok: false,
      status: 400,
      reason: `Unknown set "${which}". One of: ${DIAGRAM_SETS.join(', ')}.`,
    };
  }

  const bare = String(name ?? '').replace(/\.ya?ml$/i, '');
  if (!bare || !/^[A-Za-z0-9._-]+$/.test(bare) || bare.includes('..') || bare.startsWith('.')) {
    return { ok: false, status: 400, reason: `"${name}" is not a diagram name.` };
  }

  const folder = path.join(root, 'diagrams', 'lld', which);
  const file = path.join(folder, `${bare}.yaml`);
  const inside = path.relative(folder, file);
  if (!inside || inside.startsWith('..') || path.isAbsolute(inside)) {
    return { ok: false, status: 400, reason: `"${name}" is not a diagram name.` };
  }

  const doc = await readYaml(file);
  if (!doc) {
    return { ok: false, status: 404, reason: `diagrams/lld/${which}/${bare}.yaml is empty.` };
  }
  if (doc.__error) {
    // A file that exists and will not parse is not the same answer as a file
    // that is not there, and a caller conflating them will send somebody looking
    // for a typo in a name that is spelled correctly.
    return absent(doc)
      ? { ok: false, status: 404, reason: `No diagrams/lld/${which}/${bare}.yaml in this package.` }
      : {
          ok: false,
          status: 422,
          reason: `diagrams/lld/${which}/${bare}.yaml will not parse: ${doc.__error}`,
        };
  }

  return { ok: true, set: which, name: bare, file: `diagrams/lld/${which}/${bare}.yaml`, doc };
}

/**
 * @param root       the package root
 * @param context    what the rest of the index already knows, so the names in
 *                   here can be resolved rather than trusted:
 *                   { tables, contracts, screens, flows, operations, stateModels }
 *
 *                   `operations` is the indexer's operation nodes — anything
 *                   carrying a `.file` — and lets the contract counts be checked
 *                   against contracts/ rather than only against each other.
 *                   `stateModels` is the domain layer's `machines`, and lets the
 *                   lifecycle entities be checked against states/. Both are
 *                   optional; the checks needing them stand down and say nothing
 *                   rather than inventing a source to check against.
 */
export async function buildDiagrams(root, context = {}) {
  const dir = path.join(root, 'diagrams');
  const problems = [];

  // ---- locate -------------------------------------------------------------
  //
  // Nothing below opens a path this function did not first find. `README.yaml`
  // names the five subjects and the four folders; where it is absent the old
  // flat layout is assumed, so a package cut before the split still opens.
  const readme = await readYaml(path.join(dir, 'README.yaml'));
  const indexed = Boolean(readme) && !readme.__error;
  if (readme?.__error && !absent(readme)) {
    problems.push({
      severity: 'error',
      kind: 'diagram-unreadable',
      file: 'diagrams/README.yaml',
      message:
        `The diagram index will not parse: ${readme.__error}. ` +
        `Falling back to the flat layout, which may be superseded.`,
    });
  }

  const declaredHld = indexed
    ? list(readme.hld)
        .map((e) => ({
          file: posix(e?.file ?? ''),
          id: e?.id ?? null,
          title: e?.title ?? null,
        }))
        .filter((e) => e.file)
    : [
        { file: 'diagrams/hld.yaml', id: null, title: null },
        { file: 'diagrams/hierarchy.yaml', id: null, title: null },
      ];

  const declaredSets = indexed
    ? list(readme.lld)
        .map((e) => ({
          set: String(e?.set ?? ''),
          folder: posix(String(e?.folder ?? '').replace(/\/+$/, '')),
          files: e?.files ?? null,
        }))
        .filter((e) => DIAGRAM_SETS.includes(e.set) && e.folder)
    : [{ set: 'services', folder: 'diagrams/lld', files: null }];

  // ---- the high-level subjects --------------------------------------------
  const subjects = {};
  const subjectFiles = {};
  for (const entry of declaredHld) {
    const doc = await readYaml(path.join(root, entry.file));
    if (!doc || doc.__error) {
      // In the indexed layout a listed file that is not there is a real fault:
      // the index is generated alongside the files it names. In the flat layout
      // these two names are guesses, so a miss is only a miss.
      if (indexed) {
        problems.push({
          severity: 'error',
          kind: 'diagram-unreadable',
          file: entry.file,
          message:
            `README.yaml lists ${entry.file} and it ` +
            `${absent(doc) ? 'is not there' : doc?.__error ? `will not read: ${doc.__error}` : 'is empty'}.`,
        });
      }
      continue;
    }
    const subject = subjectOf(doc) ?? subjectFromName(entry.file);
    if (!subject) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-unknown-subject',
        file: entry.file,
        message:
          `${entry.file} is listed as a high-level diagram and holds none of the five ` +
          `subjects this reader knows — so it is indexed and not drawn.`,
      });
      continue;
    }
    if (subjects[subject]) {
      // Two files claiming one subject is the restructure caught in the act, and
      // it is not resolved here: the first is drawn, both are named, and which
      // is current is a question for whoever generated them.
      problems.push({
        severity: 'warning',
        kind: 'diagram-unknown-subject',
        file: entry.file,
        message:
          `${entry.file} and ${subjectFiles[subject]} both describe **${subject}**. ` +
          `The first is drawn and the second is not — which of the two is current is not ` +
          `something this reader can decide.`,
      });
      continue;
    }
    // The README states each file's id and title too, which is one more pair of
    // facts stated at both ends and therefore one more pair worth comparing.
    if (entry.id && doc.id && String(entry.id) !== String(doc.id)) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-name-mismatch',
        file: entry.file,
        message: `README.yaml calls this ${entry.id}; the file declares id ${doc.id}.`,
      });
    }
    subjects[subject] = doc;
    subjectFiles[subject] = entry.file;
  }

  const hld = subjects.services ?? null;
  const servicesFile = subjectFiles.services ?? 'diagrams/hld.yaml';

  if (!hld) {
    // Absent is not a fault: a package without diagrams/ is a package that has
    // not been asked this question yet, and the layer simply does not open. The
    // layout is still reported, because "there is a README and no services in
    // it" and "there is no diagrams/ at all" are different situations and the
    // caller should be able to tell them apart.
    return {
      present: false,
      layout: indexed ? 'indexed' : null,
      services: [],
      tiers: [],
      problems,
      stats: {},
    };
  }

  // ---- the low-level sets --------------------------------------------------
  //
  // Every file in all four folders is read. It is a megabyte and it costs under
  // a tenth of a second, and it buys the second half of every count in the HLD:
  // a summary saying 77 operations can be compared with a file that lists them.
  // None of the bodies survive into the payload — only the index rows.
  const lld = {};
  const detail = new Map(); // services only: the existing joins are built off this
  const setStats = {};

  for (const { set, folder, files: declaredCount } of declaredSets) {
    const rows = [];
    let entries = [];
    try {
      entries = await readdir(path.join(root, folder), { withFileTypes: true });
    } catch {
      // An index with no detail beside it is still an index. In the flat layout
      // this is routine; in the indexed layout the README named the folder.
      if (indexed) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-no-detail',
          file: 'diagrams/README.yaml',
          message: `README.yaml names ${folder}/ as the ${set} set and there is no such folder.`,
        });
      }
    }

    for (const entry of entries) {
      if (!entry.isFile() || !/\.ya?ml$/i.test(entry.name)) continue;
      const rel = `${folder}/${entry.name}`;
      const doc = await readYaml(path.join(root, folder, entry.name));
      if (!doc || doc.__error) {
        problems.push({
          severity: 'error',
          kind: 'diagram-unreadable',
          file: rel,
          message: `Could not read the ${set} detail: ${doc?.__error ?? 'empty file'}`,
        });
        continue;
      }

      // The id is authoritative and the filename is a convenience, but a file
      // whose name disagrees with its id is a file somebody has copied and half
      // edited — worth saying before either is believed.
      //
      // Three of the four sets name the file after the id: `LLD-OrderService` in
      // `OrderService.yaml`, `LLD-orders` in `orders.yaml`, `LLD-P01` in
      // `P01.yaml`. The lifecycles do not, deliberately — the id carries the
      // entity's display name (`LLD-Operational alert`) and the file is named
      // for the enum it hangs off (`alert.yaml`), and 22 of the 113 differ that
      // way. Running the rule over them would produce 22 warnings about a
      // convention working as intended, which is how a check earns its way onto
      // the list of checks people stop reading. The lifecycles are joined to the
      // high level by `entity` further down instead, which is the pair that is
      // actually meant to agree.
      const fromId = String(doc.id ?? '').replace(/^LLD-/, '');
      const fromName = entry.name.replace(/\.ya?ml$/i, '');
      if (set !== 'lifecycles' && fromId && keyOf(fromId) !== keyOf(fromName)) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-name-mismatch',
          file: rel,
          message: `${entry.name} declares id ${doc.id}, which is not the file it is in.`,
        });
      }

      rows.push({
        set,
        name: fromName,
        file: rel,
        id: doc.id ?? null,
        title: doc.title ?? null,
        ...headline(set, doc),
      });

      if (set === 'services') {
        detail.set(keyOf(fromId || fromName), { ...doc, file: rel, name: fromId || fromName });
      }
    }

    rows.sort((a, b) => String(a.name).localeCompare(String(b.name)));
    lld[set] = rows;
    setStats[set] = rows.length;

    // The README states the size of each set. It is generated from the folder,
    // so a disagreement means one of the two was written and the other was not.
    if (declaredCount != null && Number(declaredCount) !== rows.length) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-set-count',
        file: 'diagrams/README.yaml',
        message:
          `README.yaml says the ${set} set holds ${declaredCount} file(s); ` +
          `${folder}/ holds ${rows.length}.`,
      });
    }
  }
  for (const set of DIAGRAM_SETS) if (!lld[set]) lld[set] = [];

  // ---- the services, tier by tier -----------------------------------------
  const services = [];
  const tiers = [];
  const placed = new Set();

  for (const tier of hld.tiers ?? []) {
    const row = { tier: tier.tier, meaning: tier.meaning ?? null, services: [] };
    for (const entry of tier.services ?? []) {
      const key = keyOf(entry.service);
      placed.add(key);
      const lldDoc = detail.get(key) ?? null;
      if (!lldDoc) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-no-detail',
          file: servicesFile,
          message:
            `${entry.service} is placed in the ${tier.tier} tier but has no detail file ` +
            `beside it, so it is a name without a description.`,
        });
      }
      // The tier row says how many operations the service has and the file below
      // it counts them contract by contract. Same shape as the tables check
      // further down, and the same reason for it: a total that is right for the
      // wrong reasons is not something a reader can tell from a total that is
      // right.
      const counted = list(lldDoc?.operationsByContract).reduce((a, c) => a + (c?.count ?? 0), 0);
      if (lldDoc && entry.operations != null && counted && counted !== entry.operations) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-operation-count',
          file: lldDoc.file,
          message:
            `${entry.service}: ${servicesFile} says ${entry.operations} operations, ` +
            `${lldDoc.file} counts ${counted} across its contracts.`,
        });
      }

      const service = {
        key,
        name: entry.service,
        tier: tier.tier,
        tierMeaning: tier.meaning ?? null,
        operations: entry.operations ?? null,
        tables: entry.tables ?? null,
        schemas: entry.schemas ?? [],
        contracts: entry.contracts ?? [],
        flowCoverage: percent(entry.flowCoverage),
        scale: entry.scale ?? null,
        ifDown: entry.ifDown ?? lldDoc?.ifDown ?? null,
        ref: entry.ref ?? null,
        // everything below is only in the detail file
        why: lldDoc?.why ?? null,
        detailFile: lldDoc?.file ?? null,
        coverage: lldDoc?.coverage ?? null,
        schemaDetail: lldDoc?.schemas ?? [],
        operationsByContract: lldDoc?.operationsByContract ?? [],
        tableDetail: lldDoc?.tables ?? [],
        readsFrom: lldDoc?.readsFrom ?? [],
        writesOutside: lldDoc?.writesOutside ?? [],
        screens: lldDoc?.screens ?? [],
        flows: lldDoc?.flows ?? [],
      };
      row.services.push(service.key);
      services.push(service);
    }
    tiers.push(row);
  }

  // A detail file for a service no tier places is the more serious direction of
  // the same mismatch: it will never be drawn, so nobody will notice it is there.
  for (const [key, lldDoc] of detail) {
    if (placed.has(key)) continue;
    problems.push({
      severity: 'warning',
      kind: 'diagram-unplaced',
      file: lldDoc.file,
      message:
        `${lldDoc.name} describes itself as tier "${lldDoc.tier ?? 'none'}" but no tier ` +
        `in ${servicesFile} lists it.`,
    });
  }

  const byKey = new Map(services.map((s) => [s.key, s]));

  // ---- cross-service writes, stated from both ends -------------------------
  //
  // The index says who writes whom; each detail file says the same thing about
  // itself. Where they agree the edge is drawn once; where they disagree the
  // edge is still drawn, and flagged, because an undrawn boundary is worse than
  // a disputed one.
  const crossServiceWrites = [];
  const seen = new Set();
  for (const edge of hld.crossServiceWrites ?? []) {
    const from = keyOf(edge.from);
    const to = keyOf(edge.to);
    seen.add(`${from}>${to}`);
    const mine = byKey.get(from)?.writesOutside?.find((w) => keyOf(w.service) === to) ?? null;
    if (mine && mine.operations != null && edge.writes != null && mine.operations !== edge.writes) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-write-disagreement',
        file: servicesFile,
        message:
          `${edge.from} → ${edge.to}: the index says ${edge.writes} writes, ` +
          `${byKey.get(from)?.detailFile ?? 'the detail file'} says ${mine.operations}.`,
      });
    }
    crossServiceWrites.push({
      from, to,
      fromName: edge.from,
      toName: edge.to,
      writes: edge.writes ?? null,
      reads: edge.reads ?? null,
      kind: edge.kind ?? null,
      why: mine?.why ?? null,
      inDetail: Boolean(mine),
    });
  }
  // An edge a service claims that the index does not list.
  for (const service of services) {
    for (const out of service.writesOutside ?? []) {
      const to = keyOf(out.service);
      if (seen.has(`${service.key}>${to}`)) continue;
      problems.push({
        severity: 'warning',
        kind: 'diagram-write-unlisted',
        file: service.detailFile ?? 'diagrams/lld/services/',
        message:
          `${service.name} says it writes ${out.service}, and ${servicesFile} does not ` +
          `list that edge — so the map does not draw a boundary the service declares.`,
      });
      crossServiceWrites.push({
        from: service.key, to,
        fromName: service.name,
        toName: out.service,
        writes: out.operations ?? null,
        reads: null,
        kind: null,
        why: out.why ?? null,
        inDetail: true,
        unlisted: true,
      });
    }
  }

  // ---- against what the rest of the package already knows ------------------
  const contractNames = new Set((context.contracts ?? []).map((c) => String(c).toLowerCase()));
  const flowIds = new Set((context.flows ?? []).map((f) => String(f.id ?? f).toUpperCase()));
  const screenIds = new Set((context.screens ?? []).map((s) => String(s.id ?? s).toUpperCase()));

  // Tables are the join the workbook now states too, so it is checked service
  // by service rather than in total: a count that matches by accident across
  // sixteen services is not a match worth having.
  const ownedInWorkbook = new Map();
  for (const table of context.tables ?? []) {
    const owner = keyOf(named(table.service));
    if (!owner) continue;
    if (!ownedInWorkbook.has(owner)) ownedInWorkbook.set(owner, []);
    ownedInWorkbook.get(owner).push(table.name);
  }

  const unowned = (context.tables ?? []).filter((t) => !named(t.service)).map((t) => t.name);
  if (unowned.length) {
    problems.push({
      severity: 'warning',
      kind: 'diagram-table-unowned',
      file: 'handoff/',
      message:
        `${unowned.length} table(s) name no service on the workbook's Tables sheet ` +
        `(${unowned.slice(0, 6).join(', ')}${unowned.length > 6 ? '…' : ''}) — ` +
        `so nothing ships them.`,
    });
  }

  for (const service of services) {
    const owned = ownedInWorkbook.get(service.key) ?? [];
    service.workbookTables = owned;
    if (service.tables != null && owned.length && service.tables !== owned.length) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-table-count',
        file: service.detailFile ?? servicesFile,
        message:
          `${service.name} claims ${service.tables} tables; the workbook assigns it ` +
          `${owned.length}.`,
      });
    }
    if (service.tables != null && !owned.length && ownedInWorkbook.size) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-table-count',
        file: 'handoff/',
        message: `${service.name} claims ${service.tables} tables and the workbook assigns it none.`,
      });
    }

    for (const contract of service.contracts ?? []) {
      if (contractNames.size && !contractNames.has(String(contract).toLowerCase())) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-unknown-contract',
          file: service.detailFile ?? servicesFile,
          message: `${service.name} names contract "${contract}", which is not in contracts/.`,
        });
      }
    }

    // `F01 Guest buys a ticket online` — the id is the first word.
    for (const flow of service.flows ?? []) {
      const id = String(flow).trim().split(/\s+/)[0].toUpperCase();
      if (flowIds.size && !flowIds.has(id)) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-unknown-flow',
          file: service.detailFile ?? 'diagrams/lld/services/',
          message: `${service.name} names flow "${flow}", which is not in flows/.`,
        });
      }
    }

    // `P01:WEB-008 Add-ons & Upsell` — platform, colon, screen id, then a label.
    for (const screen of service.screens ?? []) {
      const id = /^[A-Za-z0-9]+:([A-Za-z0-9-]+)/.exec(String(screen).trim())?.[1]?.toUpperCase();
      if (id && screenIds.size && !screenIds.has(id)) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-unknown-screen',
          file: service.detailFile ?? 'diagrams/lld/services/',
          message: `${service.name} names screen "${screen}", which is not in screens/.`,
        });
      }
    }
  }

  // Every service the workbook ships should be a service the diagrams describe.
  for (const [key, owned] of ownedInWorkbook) {
    if (byKey.has(key)) continue;
    problems.push({
      severity: 'warning',
      kind: 'diagram-service-undescribed',
      file: 'handoff/',
      message:
        `The workbook assigns ${owned.length} table(s) to "${key}", which no tier ` +
        `in ${servicesFile} describes.`,
    });
  }

  // ---- deploy order --------------------------------------------------------
  const deployOrder = (hld.deployOrder ?? []).map((step) => ({
    order: step.order ?? null,
    tier: step.tier ?? null,
    rule: step.rule ?? null,
    services: tiers.find((t) => t.tier === step.tier)?.services ?? [],
  }));
  const ordered = new Set(deployOrder.map((s) => s.tier));
  for (const tier of tiers) {
    if (ordered.has(tier.tier)) continue;
    problems.push({
      severity: 'warning',
      kind: 'diagram-tier-unordered',
      file: servicesFile,
      message: `The ${tier.tier} tier has no place in the deploy order.`,
    });
  }

  const survivable = (hld.canBeDownWithoutStoppingASale ?? []).map((name) => {
    const key = keyOf(name);
    if (!byKey.has(key)) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-unknown-service',
        file: servicesFile,
        message: `"${name}" may be down without stopping a sale, and is not a service in any tier.`,
      });
    }
    return key;
  });

  // ---- the platform subject ------------------------------------------------
  //
  // Fifteen surfaces at the top and fifteen files under them, and the only thing
  // that joins the two is the `ref`. Left unchecked the platform view would be
  // the one subject in this folder whose halves are never compared — which is
  // precisely the state the services view was in before this module existed.
  const platformFile = subjectFiles.platform ?? null;
  const platformDetailByFile = new Map(lld.platforms.map((r) => [r.file, r]));
  for (const surface of list(subjects.platform?.surfaces)) {
    const below = surface?.ref ? platformDetailByFile.get(posix(surface.ref)) : null;
    if (!below) continue;
    if (surface.screens != null && below.screens && below.screens !== surface.screens) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-screen-count',
        file: below.file,
        message:
          `${surface.platform}: the platform diagram says ${surface.screens} screens, ` +
          `${below.file} lists ${below.screens}.`,
      });
    }
    if (surface.app && below.app && String(surface.app) !== String(below.app)) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-name-mismatch',
        file: below.file,
        message:
          `${surface.platform}: the platform diagram calls the app "${surface.app}", ` +
          `${below.file} calls it "${below.app}".`,
      });
    }
    for (const service of list(surface.callsServices)) {
      if (byKey.size && !byKey.has(keyOf(service))) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-unknown-service',
          file: platformFile,
          message: `${surface.platform} calls "${service}", which no tier places.`,
        });
      }
    }
  }

  // The outside systems, against the same tiers. `external[].via` is one service
  // or a list of them, and a name that places nowhere is a boundary the overview
  // silently declines to draw — which is the failure mode this list is least
  // able to show, since a missing line on a diagram of lines looks like a system
  // that simply reaches nothing.
  for (const outside of list(subjects.platform?.external)) {
    // One or many: `list` here means an array or nothing, and half of these are
    // still written as a scalar.
    const via = Array.isArray(outside?.via) ? outside.via : [outside?.via];
    for (const service of via.filter(Boolean)) {
      if (byKey.size && !byKey.has(keyOf(service))) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-unknown-service',
          file: platformFile,
          message: `${outside.system} reaches "${service}", which no tier places.`,
        });
      }
    }
  }

  // ---- the contracts subject ----------------------------------------------
  //
  // 28 rows saying how many operations each contract has, which contracts/ also
  // says and which the file below each row also says. Three statements of one
  // number is two chances to catch a generator that ran against an older tree.
  const contractsDoc = subjects.contracts ?? null;
  const contractsFile = subjectFiles.contracts ?? null;
  const contractRows = list(contractsDoc?.contracts);

  const realOperations = new Map();
  for (const op of list(context.operations)) {
    const file = op?.file ?? op?.contract ?? null;
    if (!file) continue;
    const stem = path.basename(String(file), '.yaml').toLowerCase();
    realOperations.set(stem, (realOperations.get(stem) ?? 0) + 1);
  }

  const contractDetailByName = new Map(lld.contracts.map((r) => [String(r.name).toLowerCase(), r]));
  for (const row of contractRows) {
    const name = String(row?.contract ?? '').toLowerCase();
    if (!name) continue;

    if (contractNames.size && !contractNames.has(name)) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-unknown-contract',
        file: contractsFile,
        message: `The contracts diagram names "${row.contract}", which is not in contracts/.`,
      });
    }

    // Against contracts/ itself, where the caller has handed the operations over.
    const real = realOperations.get(name);
    if (real != null && row.operations != null && real !== row.operations) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-operation-count',
        file: contractsFile,
        message:
          `${row.contract}: the diagram says ${row.operations} operations, ` +
          `contracts/ defines ${real}.`,
      });
    }

    // And against the file below it, which lists them one by one.
    const below = contractDetailByName.get(name);
    if (below && row.operations != null && below.operations !== row.operations) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-operation-count',
        file: below.file,
        message:
          `${row.contract}: the diagram says ${row.operations} operations, ` +
          `${below.file} lists ${below.operations}.`,
      });
    }

    // The two counts on the row that say who may call an operation and where.
    // They are the reason the contracts view exists — a guest-callable operation
    // and an offline-capable one are the two facts that decide what a surface can
    // be built out of — so they are checked against the operations themselves
    // rather than taken on the summary's word.
    for (const [claim, counted, what] of [
      [row.guestCallable, below?.guestCallable, 'guest-callable'],
      [row.offlineCapable, below?.offline, 'offline-capable'],
    ]) {
      if (below && claim != null && counted != null && claim !== counted) {
        problems.push({
          severity: 'warning',
          kind: 'diagram-operation-count',
          file: below.file,
          message:
            `${row.contract}: the diagram says ${claim} ${what} operation(s), ` +
            `${below.file} marks ${counted}.`,
        });
      }
    }

    // The service a contract names has to be a service some tier places, or the
    // contracts view and the services view are drawing two different platforms.
    if (row.service && byKey.size && !byKey.has(keyOf(row.service))) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-unknown-service',
        file: contractsFile,
        message: `Contract ${row.contract} is assigned to "${row.service}", which no tier places.`,
      });
    }
  }

  // ---- and the direction that matters more ---------------------------------
  //
  // Above catches a contract the diagram names that the package does not have.
  // This catches the reverse, which is the harder one to see: nothing on a
  // diagram announces what it left out, so a reader counting boxes simply gets
  // a smaller number and no reason to doubt it.
  if (contractsDoc && contractNames.size && contractRows.length) {
    const drawn = new Set(contractRows.map((row) => String(row?.contract ?? '').toLowerCase()));
    const missing = [...contractNames].filter((name) => !drawn.has(name)).sort();
    if (missing.length) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-contract-missing',
        file: contractsFile,
        paths: missing,
        message:
          `${missing.length} contract(s) in contracts/ are not in the contracts diagram ` +
          `(${missing.join(', ')}), so it draws ${drawn.size} of ${contractNames.size}.`,
      });
    }

    // The same omission from the other end, and the end that says it was not
    // deliberate: nobody writes a description for a category they meant to
    // leave empty.
    const used = new Set(contractRows.map((row) => String(row?.tier ?? '').toLowerCase()));
    const idle = Object.keys(contractsDoc.tiers ?? {})
      .filter((tier) => !used.has(String(tier).toLowerCase()));
    if (idle.length) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-tier-empty',
        file: contractsFile,
        paths: idle,
        message:
          `The contracts diagram describes ${idle.length} tier(s) it puts nothing in ` +
          `(${idle.join(', ')}) \u2014 a described tier with no members is a category ` +
          `somebody meant to fill.`,
      });
    }
  }

  // ---- the lifecycles subject ----------------------------------------------
  const lifecyclesDoc = subjects.lifecycles ?? null;
  const lifecyclesFile = subjectFiles.lifecycles ?? null;
  const stateModels = list(lifecyclesDoc?.stateModels);

  // The domain layer reads states/ and is the other end of this. It is optional
  // because it is not this module's to build — where the caller does not hand it
  // over the entity names are simply not checked, and this says nothing rather
  // than inventing a second source to check them against.
  const knownEntities = new Set(
    list(context.stateModels).map((m) => String(m?.entity ?? m).trim().toLowerCase()).filter(Boolean)
  );
  const lifecycleDetailByFile = new Map(lld.lifecycles.map((r) => [r.file, r]));

  for (const model of stateModels) {
    const entity = String(model?.entity ?? '').trim();
    if (entity && knownEntities.size && !knownEntities.has(entity.toLowerCase())) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-unknown-entity',
        file: lifecyclesFile,
        message: `The lifecycles diagram draws "${entity}", which no state model in states/ defines.`,
      });
    }
    const below = model?.ref ? lifecycleDetailByFile.get(posix(model.ref)) : null;
    // The lifecycles' id does not name their file, so `entity` is the join that
    // has to hold: the row and the file it points at are supposed to be about
    // the same thing, and a ref that lands on a different entity is a ref that
    // was written by hand or generated against an older tree.
    if (below && entity && below.entity && keyOf(entity) !== keyOf(below.entity)) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-name-mismatch',
        file: below.file,
        message:
          `The lifecycles diagram draws "${entity}" and points at ${below.file}, ` +
          `which is about "${below.entity}".`,
      });
    }
    if (below && model.transitions != null && below.transitions !== model.transitions) {
      problems.push({
        severity: 'warning',
        kind: 'diagram-transition-count',
        file: below.file,
        message:
          `${entity || below.name}: the diagram says ${model.transitions} transitions, ` +
          `${below.file} lists ${below.transitions}.`,
      });
    }
  }
  if (knownEntities.size && stateModels.length && list(context.stateModels).length !== stateModels.length) {
    // Not the same check as the one above and it catches a different thing: two
    // state models in states/ sharing an entity name fold to one row here, so
    // every name resolves while the totals do not. A model the diagram has
    // quietly merged is a model that will never be drawn on its own.
    problems.push({
      severity: 'warning',
      kind: 'diagram-lifecycle-count',
      file: lifecyclesFile,
      message:
        `The lifecycles diagram draws ${stateModels.length} state models; states/ defines ` +
        `${list(context.stateModels).length} under ${knownEntities.size} distinct entity name(s).`,
    });
  }

  // ---- every ref, against the folder it points into ------------------------
  //
  // A `ref` is the whole navigation model of this folder: the high level is only
  // usable because each node names the file below it. One pointing at nothing is
  // a dead end in the only direction anybody travels, and it is exactly what a
  // restructure produces — the refs in the superseded `hld.yaml` still name
  // `diagrams/lld/OrderService.yaml`, which is how that file was spotted.
  const onDisk = new Set(await walkYaml(root, 'diagrams'));
  const refs = new Set();
  const collectRefs = (node) => {
    if (Array.isArray(node)) {
      for (const child of node) collectRefs(child);
      return;
    }
    if (!node || typeof node !== 'object') return;
    for (const [key, value] of Object.entries(node)) {
      if (key === 'ref' && typeof value === 'string' && value.trim()) refs.add(posix(value.trim()));
      else collectRefs(value);
    }
  };
  for (const subject of Object.keys(subjects)) collectRefs(subjects[subject]);

  const brokenRefs = [...refs].filter((ref) => !onDisk.has(ref)).sort();
  for (const ref of brokenRefs) {
    problems.push({
      severity: 'error',
      kind: 'diagram-ref-missing',
      file: ref,
      message: `A high-level node points at ${ref}, and there is no such file.`,
    });
  }

  // ---- what the index does not list ----------------------------------------
  //
  // The defect this module was rewritten for. A file left behind by a
  // restructure does not fail — it parses, it is plausible, and it is stale. The
  // index is the only thing that knows which of two files with the same subject
  // is current, so anything on disk the index does not list is either superseded
  // by something it does list, or unaccounted for. Both are said out loud and
  // neither is deleted, because deciding that is not a reader's job.
  const listedFiles = new Set(declaredHld.map((e) => e.file));
  listedFiles.add('diagrams/README.yaml');
  const listedFolders = declaredSets.map((s) => s.folder);
  const byBasename = new Map();
  for (const set of declaredSets) {
    for (const row of lld[set.set] ?? []) {
      listedFiles.add(row.file);
      const base = path.basename(row.file).toLowerCase();
      if (!byBasename.has(base)) byBasename.set(base, row.file);
    }
  }

  const superseded = [];
  const unaccounted = [];
  for (const file of [...onDisk].sort()) {
    if (listedFiles.has(file)) continue;
    if (listedFolders.some((folder) => file.startsWith(`${folder}/`))) continue;

    // A loose `lld/OrderService.yaml` beside `lld/services/OrderService.yaml` is
    // the same file one drop older; the basename is the join.
    const twin = byBasename.get(path.basename(file).toLowerCase());
    if (twin) {
      superseded.push({ file, supersededBy: twin });
      continue;
    }

    // Otherwise the file has to say what it is. `hld.yaml` and
    // `hld/02-services.yaml` carry the same id and the same title, which is a
    // stronger statement than any guess from a filename — the old file names
    // itself the current one. Only the handful that got this far are parsed.
    const doc = await readYaml(path.join(root, file));
    const subject = subjectOf(doc) ?? subjectFromName(file);
    const current = subject ? subjectFiles[subject] : null;
    if (current && current !== file) {
      superseded.push({ file, supersededBy: current });
      continue;
    }
    unaccounted.push(file);
  }

  if (superseded.length) {
    problems.push({
      severity: 'warning',
      kind: 'diagram-superseded',
      file: 'diagrams/README.yaml',
      paths: superseded,
      message:
        `${superseded.length} file(s) in diagrams/ are not in README.yaml and are superseded ` +
        `by files that are: ` +
        `${superseded.slice(0, 4).map((s) => `${s.file} → ${s.supersededBy}`).join(', ')}` +
        `${superseded.length > 4 ? `, and ${superseded.length - 4} more` : ''}. ` +
        `**They parse, so nothing fails when a reader opens one instead** — which is exactly ` +
        `what this reader did until it was rewritten to read the index.`,
    });
  }
  if (unaccounted.length) {
    problems.push({
      severity: 'warning',
      kind: 'diagram-unlisted',
      file: 'diagrams/README.yaml',
      paths: unaccounted,
      message:
        `${unaccounted.length} file(s) in diagrams/ are in no part of README.yaml and nothing ` +
        `listed supersedes them: ${unaccounted.slice(0, 6).join(', ')}` +
        `${unaccounted.length > 6 ? '…' : ''}.`,
    });
  }

  return {
    present: true,
    // 'indexed' — README.yaml, five subjects, four sets. 'flat' — the pre-split
    // layout. A caller showing one and meaning the other is the bug this names.
    layout: indexed ? 'indexed' : 'flat',
    readme: indexed
      ? {
          id: readme.id ?? null,
          title: readme.title ?? null,
          about: readme.about ?? null,
          howToRead: readme.howToRead ?? null,
          notCovered: readme.notCovered ?? null,
          generatedBy: readme.generatedBy ?? null,
        }
      : null,

    // ---- the services subject, unchanged in shape and in name -------------
    title: hld.title ?? 'Services',
    about: hld.about ?? null,
    notes: hld.notes ?? null,
    decision: hld.decision ?? null,
    generatedBy: hld.generatedBy ?? null,
    servicesFile,
    tiers,
    services,
    crossServiceWrites,
    deployOrder,
    survivable,

    // ---- the four other subjects, each close to its own file's shape ------
    //
    // Passed through rather than reshaped. These files are generated from the
    // same decomposition every other layer is generated from, and a reader that
    // renamed their keys would be a third statement of facts already stated
    // twice — which is the one thing this module exists not to add.
    platform: subjects.platform
      ? { present: true, file: subjectFiles.platform, ...subjects.platform }
      : { present: false, file: null },
    hierarchy: subjects.hierarchy
      ? { present: true, file: subjectFiles.hierarchy, ...subjects.hierarchy }
      : { present: false, file: null },
    contracts: contractsDoc
      ? { present: true, file: contractsFile, ...contractsDoc }
      : { present: false, file: null },
    lifecycles: lifecyclesDoc
      ? { present: true, file: lifecyclesFile, ...lifecyclesDoc }
      : { present: false, file: null },

    // ---- the low level, as four indexes ------------------------------------
    // One row per file. The body is fetched by name through readDiagramDetail.
    lld,
    sets: DIAGRAM_SETS,

    problems,
    stats: {
      // the eight the caller already reads
      services: services.length,
      tiers: tiers.length,
      withDetail: services.filter((s) => s.detailFile).length,
      operations: services.reduce((a, s) => a + (s.operations ?? 0), 0),
      tables: services.reduce((a, s) => a + (s.tables ?? 0), 0),
      crossWrites: crossServiceWrites.length,
      tablesOwned: [...ownedInWorkbook.values()].reduce((a, owned) => a + owned.length, 0),
      tablesUnowned: unowned.length,

      // what the folder holds
      layout: indexed ? 'indexed' : 'flat',
      hldSubjects: DIAGRAM_SUBJECTS.filter((s) => subjects[s]),
      hldFiles: Object.keys(subjectFiles).length,
      lld: { ...setStats },
      lldFiles: DIAGRAM_SETS.reduce((a, s) => a + (lld[s]?.length ?? 0), 0),
      diagramFiles: onDisk.size,

      // the subjects, in their own units
      surfaces: list(subjects.platform?.surfaces).length,
      actors: list(subjects.platform?.actors).length,
      levels: list(subjects.hierarchy?.levels).length,
      contracts: contractRows.length,
      contractOperations: contractRows.reduce((a, c) => a + (c?.operations ?? 0), 0),
      stateModels: stateModels.length,
      transitions: stateModels.reduce((a, m) => a + (m?.transitions ?? 0), 0),
      events: list(lifecyclesDoc?.events).length,

      // and what the folder carries that the index does not claim
      superseded: superseded.length,
      unlisted: unaccounted.length,
      brokenRefs: brokenRefs.length,
    },
  };
}
