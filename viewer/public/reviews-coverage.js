/**
 * What there is to review, and where each piece of it stands.
 *
 * This is the half of the Reviews page that used to be its own page ("What has
 * been signed off", validation.html). It answers the question a delivery is
 * reviewed against: what is still untouched. That needs two servers. The
 * population comes from the Node reader (every operation, table, screen,
 * board, state model and schema in the package); the verdicts come from the
 * accounts service. An artefact nobody has looked at exists in the first and
 * not the second, so everything here is a join across that gap, and "never
 * reviewed" is a row like any other rather than an absence to notice.
 *
 * **One standing per artefact, from the verdicts the page's filter lets
 * through.** Four values, in the order they win:
 *
 *   open      somebody asked for work (needs work or rejected) and nobody has
 *             answered it, or the answer was sent back
 *   fixed     the latest verdict asked for work and somebody has since
 *             answered it (built, wired, answered, accepted). The old sign-off
 *             list kept saying "Needs work" after the fix, which is the bug
 *             this word exists for
 *   approved  everything current says approved
 *   none      no verdict at all
 *
 * "Open" looks at every row, not only the newest: an ask for work is an item
 * in a worklist, and a later approval from somebody else does not answer it.
 * A later verdict from the *same* person does: somebody who asked for work and
 * then approved has withdrawn the ask, and counting it would keep a worklist
 * item open that its own author has closed. `isOpenAsk` is that rule, and the
 * worklist counts by it too, so the headline's "23 open" and the bar's amber
 * are the same rows.
 */
import * as auth from '/validation.js';

/**
 * The kinds a verdict can be about, each with where its population comes from
 * and how to link to one. The `id` is what the verdict was recorded against:
 * it has to match the viewer exactly, or an artefact would appear twice, once
 * judged and once not.
 *
 * `group` is what the coverage chart breaks a kind into once the page is
 * filtered to it ("Tables by module").
 */
export const KINDS = [
  {
    key: 'operation', label: 'APIs', one: 'API operation', many: 'API operations',
    group: 'contract file',
    async load(read) {
      const index = await read('/api/index');
      return index.nodes
        .filter((n) => n.type === 'operation')
        .map((n) => ({
          id: n.name,
          name: n.name,
          detail: `${n.method} ${n.path}`,
          group: n.file.split('/').pop().replace(/\.ya?ml$/, ''),
          nodeId: n.id,
        }));
    },
  },
  {
    key: 'table', label: 'Tables', one: 'table', many: 'tables', group: 'module',
    async load(read) {
      const backend = await read('/api/backend');
      return (backend.tables ?? []).map((t) => ({
        id: t.name,
        name: t.name,
        // `ddl` is the written-as-SQL marker. `t.migration` names the migration
        // a table is *planned* for, which every table carries, so reading it
        // reported every table as built.
        detail: `${t.columns} columns${t.ddl ? ` · ${t.migration}` : ' · planned'}`,
        group: t.module,
      }));
    },
  },
  {
    key: 'screen', label: 'Wireframes', one: 'wireframe', many: 'wireframes', group: 'platform',
    async load(read) {
      const journeys = await read('/api/journeys');
      return (journeys.screens ?? []).map((s) => ({
        id: s.id,
        name: `${s.id} ${s.name}`,
        detail: s.route ?? '',
        group: s.platformName ?? s.platform ?? 'no platform',
      }));
    },
  },
  {
    key: 'board', label: 'Design boards', one: 'design board', many: 'design boards', group: 'platform',
    async load(read) {
      const journeys = await read('/api/journeys');
      return (journeys.boards ?? []).map((b) => ({
        id: b.id,
        name: b.name,
        detail: b.file ?? '',
        group: b.platformName ?? b.platform ?? 'no platform',
      }));
    },
  },
  {
    // A state model, not a state. Which moves are legal is decided once for the
    // whole entity, so the entity is the unit somebody signs off.
    key: 'state', label: 'State models', one: 'state model', many: 'state models', group: 'contract',
    async load(read) {
      const domain = await read('/api/domain');
      return (domain.machines ?? []).map((m) => ({
        id: m.id,
        name: `${m.entity}, ${m.stats.states} states`,
        detail: `${m.contract}.${m.enum} · ${m.stats.transitions} transitions`,
        group: m.contract ?? 'no contract',
      }));
    },
  },
  {
    // The schema, not its tables. Whether the boundary is in the right place is
    // not the sum of separate opinions about each table inside it.
    key: 'schema', label: 'Schemas', one: 'schema', many: 'schemas', group: 'tier',
    async load(read) {
      const backend = await read('/api/backend');
      const tables = backend.tables ?? [];
      return (backend.modules ?? []).map((m) => {
        const mine = tables.filter((t) => t.module === m.name);
        return {
          id: m.name,
          name: m.name,
          detail: `${mine.length} tables · ${mine.filter((t) => t.ddl).length} written`,
          group: m.tier ?? 'no tier',
        };
      });
    },
  },
];

/**
 * `module` is a kind the service accepts and nothing in the viewer offers a
 * verdict on any more. It has no population, so it never gets a coverage bar;
 * it is still a kind in the filter when old rows of it exist, because a
 * verdict nobody can find is worse than one with no denominator.
 */
export const MODULE_KIND = { key: 'module', label: 'Modules', one: 'module', many: 'modules', group: 'module' };

export const kindOf = (key) => KINDS.find((k) => k.key === key) ?? (key === 'module' ? MODULE_KIND : null);
export const kindLabel = (key) => kindOf(key)?.label ?? key;

export const artefactKey = (kind, id) => `${kind} ${id}`;

/** Where the viewer shows one artefact. An operation routes by its node id,
 *  which only the population knows; without it, by name, as the verdict block
 *  records it. */
export function viewerHref(kind, id, nodeId) {
  if (kind === 'operation') return `/#${encodeURIComponent(nodeId ?? id)}`;
  return `/#${encodeURIComponent(`${kind}:${id}`)}`;
}

/**
 * Read every kind's population. One request per payload, shared: two kinds
 * read `/api/journeys` (21 MB on TICVAI) and two read `/api/backend`, and the
 * old page asked twice and hoped the browser cache answered.
 *
 * A kind that cannot be read is *said*, not counted as empty. The old page
 * turned a failed read into `[]`, which showed as "0 of 0 wireframes" and
 * read as a finished review of nothing.
 *
 * @returns {Promise<Map<string, {rows: object[], error: string|null}>>}
 */
export async function loadPopulations() {
  const asked = new Map();
  const read = (path) => {
    if (!asked.has(path)) {
      asked.set(path, auth.apiFetch(path).then(async (r) => {
        if (!r.ok) throw new Error(`the reader answered ${r.status} for ${path}`);
        return r.json();
      }));
    }
    return asked.get(path);
  };
  const out = new Map();
  await Promise.all(KINDS.map(async (kind) => {
    try {
      out.set(kind.key, { rows: (await kind.load(read)).map((r) => ({ ...r, kind: kind.key })), error: null });
    } catch (error) {
      out.set(kind.key, { rows: [], error: error.message || String(error) });
    }
  }));
  return out;
}

/**
 * The standing of one artefact from its verdict rows (already filtered), with
 * `all` its rows in the whole store, which is what decides whether an ask was
 * withdrawn. See the header for the order.
 *
 * @returns {{standing:'none'|'approved'|'open'|'fixed', latest:object|null, open:object[], current:object[]}}
 */
export function isOpenAsk(v, rows) {
  if (!auth.asksForWork(v.verdict) || auth.isSettled(v)) return false;
  return !rows.some((w) => w.account_id === v.account_id && w.id > v.id);
}

export function standingOf(rows, all = rows) {
  if (!rows?.length) return { standing: 'none', latest: null, open: [], current: [] };
  const open = rows.filter((v) => isOpenAsk(v, all));
  // The newest row per audience: the team's verdict and the client's are two
  // reviews, and the newer of the two is not the answer to both.
  const newest = new Map();
  for (const v of rows) {
    const who = v.audience || 'internal';
    if (!newest.has(who) || newest.get(who).id < v.id) newest.set(who, v);
  }
  const current = [...newest.values()];
  const latest = current.reduce((a, b) => (a.id > b.id ? a : b));
  if (open.length) return { standing: 'open', latest, open, current };
  if (current.some((v) => auth.asksForWork(v.verdict))) return { standing: 'fixed', latest, open, current };
  return { standing: 'approved', latest, open, current };
}

/** The four standings, each with the one state colour it is drawn in. */
export const STANDINGS = [
  { key: 'approved', label: 'Approved', fill: 'done' },
  { key: 'open', label: 'Asked for work, open', fill: 'stalled' },
  { key: 'fixed', label: 'Fixed', fill: 'qa' },
  { key: 'none', label: 'Never reviewed', fill: 'fresh' },
];
