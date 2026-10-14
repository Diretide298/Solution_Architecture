/**
 * AI capabilities: who can use them.
 *
 * `lib/domains.mjs` says why the lens is derived rather than written down: the
 * package is organised by kind, the file that gathered AI into prose went stale
 * in six ways inside one dump, and prose cannot track a moving package. This is
 * the front of that. It asks one question and refuses to be a directory:
 *
 *   For each AI capability — who may call it, which screen does, and what does
 *   it change — and which of those is missing?
 *
 * The page opens on the answer (how many AI operations no screen reaches, and
 * how many permissions have never had one) and its body is the Reach table, one
 * row per operation, every cell a way back into the viewer. How membership was
 * worked out is the last section, for the reader who wants to check the join
 * rather than take it.
 *
 * **It was "Domain lenses", and the flash sale was the second lens.** The page
 * was written around the AI question, and the flash sale did not fit it: no
 * services were shown, and the copy told a flash-sale reader that "the assistant
 * is open to the public". The deployment map answers the flash sale, so the
 * lens left this page (the viewer's lens chips still carry it, from the same
 * /api/domains) and an old link that names it is sent to the map.
 *
 * /api/domains carries membership and the derived-versus-declared disagreement,
 * and nothing else — it is deliberately a lens over the other payloads, not a
 * copy of them. So the joins that answer the question are read from the same
 * places every other view reads them:
 *
 *   /api/index      the operation itself — its title, and whether a guest may
 *                   call it, which is the one governance fact the lens drops
 *   /api/journeys   operationUsage: which screens and flows reach an operation
 *   /api/lineage    which tables it reads and writes
 *   /api/domain     which state model a transition names it on
 *   /api/detail     the contract's own prose, so the page can quote the rule an
 *                   operation is supposed to enforce instead of retyping it
 *
 * Six requests for one page, more than any other standalone view asks for. It
 * is the honest cost of a cross-layer question: the answer does not live in any
 * single layer, and computing it in the browser is what keeps it from going
 * stale the way the prose did. They are served gzipped and fetched in parallel.
 *
 * Every number on this page is counted from those payloads. Nothing is typed.
 * The prose is typed and says only things that stay true when the counts move.
 */

// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer. It also stamps the saved theme.
import '/page-chrome.js';
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';
import { mountPanels } from '/panels.js';
import {
  el, fmt, plural, param, verdict, next, mountScope, legend, badge, stack, table,
} from '/sheet.js';

const $ = (id) => document.getElementById(id);

// ── a link that names the retired lens goes to the deployment map ────
// Before anything is fetched: there is nothing on this page for that reader.
const RETIRED = new Set(['burst', 'flash-sale', 'flashsale', 'flash']);
if (RETIRED.has(param('lens').toLowerCase()) || RETIRED.has(location.hash.slice(1).toLowerCase())) {
  location.replace('/burst.html');
}

const KIND_LABEL = {
  operation: 'Operations',
  state: 'State models',
  event: 'Events',
  table: 'Tables',
  screen: 'Screens',
  flow: 'Journeys',
  decision: 'Decisions',
};

/** Contract outwards: what the API offers, what moves, what it stores, what a
 *  person sees, what path they walk, what was decided. */
const KIND_ORDER = ['operation', 'state', 'event', 'table', 'screen', 'flow', 'decision'];

/**
 * Three states, and the first is the one this page was built to show.
 *
 *   unreachable  something says who may call it, and no screen does
 *   ungoverned   a screen calls it, and nothing says who may
 *   ok           a screen calls it, and something says who may
 *
 * A guest-callable operation counts as governed: being open to a guest is a
 * decision written down, not the absence of one.
 *
 * The colours are the sheet's, one meaning each. No screen yet is "not
 * started" (the work of building one has not begun), a missing permission is
 * "waiting" (on a decision), and reachable and governed is "done". The words
 * are always beside them.
 */
const STATUS = {
  unreachable: { label: 'Reaches no screen', short: 'No screen', kind: 'fresh' },
  ungoverned: { label: 'On a screen, no permission named', short: 'No permission named', kind: 'stalled' },
  ok: { label: 'On a screen, with a permission', short: 'On a screen', kind: 'done' },
};
const STATUS_RANK = { unreachable: 0, ungoverned: 1, ok: 2 };

const state = {
  lenses: [],
  lens: null,
  ctx: null,
  rows: [],
  scope: null,
};

// ── reading ──────────────────────────────────────────────────────────

async function json(path) {
  // Every caller passes a /api/… path the reading server owns, and the reading
  // server is behind the API host now, so this joins the base and carries the
  // session cookie across the origin.
  const res = await auth.apiFetch(path);
  if (!res.ok) throw new Error(`${path} answered ${res.status}`);
  return res.json();
}

/**
 * The joins, keyed for lookup. Built once per load and shared by every lens,
 * because a second lens would ask the same questions of the same payloads.
 */
function buildContext({ index, journeys, lineage, domain }) {
  const movedBy = new Map();
  for (const machine of domain?.machines ?? []) {
    for (const t of machine.transitions ?? []) {
      if (!t.operation) continue;
      if (!movedBy.has(t.operation)) movedBy.set(t.operation, new Map());
      movedBy.get(t.operation).set(machine.id, machine);
    }
  }

  return {
    nodes: new Map(
      (index?.nodes ?? []).filter((n) => n.type === 'operation').map((n) => [n.name, n])
    ),
    usage: journeys?.operationUsage ?? {},
    screens: new Map((journeys?.screens ?? []).map((s) => [s.id, s])),
    flows: new Map((journeys?.flows ?? []).map((f) => [f.id, f])),
    lineage: new Map((lineage?.operations ?? []).map((r) => [r.name, r])),
    machines: new Map((domain?.machines ?? []).map((m) => [m.id, m])),
    movedBy,
    // filled in after the lens is known, since it is keyed by seed contract
    prose: new Map(),
  };
}

/**
 * The contract's own prose for the operations in this lens. Fetched per seed
 * file rather than in one go, because /api/detail is what holds back the long
 * descriptions so the index can stay small — asking for the whole package here
 * would undo that for the sake of two dozen paragraphs.
 */
async function loadProse(lens, ctx) {
  const files = [...new Set(
    (lens.byKind.operation ?? []).map((o) => o.file).filter(Boolean)
  )];
  const parts = await Promise.all(files.map((f) =>
    json(`/api/detail?file=${encodeURIComponent(f)}`).catch(() => ({}))
  ));
  for (const part of parts) {
    for (const [key, value] of Object.entries(part)) {
      if (key.startsWith('op:') && value?.description) {
        ctx.prose.set(key.slice(key.indexOf('#') + 1), value.description);
      }
    }
  }
}

// ── the join, one row per operation ──────────────────────────────────

/**
 * `cache:answer` is Redis, `qdrant:knowledge` is the vector store, and
 * `ai.conversation` is a Postgres table in the `ai` schema. The workbook writes
 * the prefix for everything that is not Postgres and writes nothing for what
 * is, so the absence of a prefix is the signal. Named here rather than inferred
 * at each call site, because it is an assumption and assumptions should be
 * findable.
 */
const storeOf = (table) => {
  const at = String(table).indexOf(':');
  return at < 0 ? 'postgres' : String(table).slice(0, at);
};

function tally(tables) {
  const out = new Map();
  for (const t of tables ?? []) out.set(storeOf(t), (out.get(storeOf(t)) ?? 0) + 1);
  return [...out.entries()].sort((a, b) => b[1] - a[1]);
}

function statusOf(row) {
  const governed = Boolean(row.permission) || row.guest;
  if (!row.screens.length) return 'unreachable';
  return governed ? 'ok' : 'ungoverned';
}

function reachRows(lens, ctx) {
  const rows = (lens.byKind.operation ?? []).map((op) => {
    const node = ctx.nodes.get(op.id) ?? {};
    const usage = ctx.usage[op.id] ?? {};
    const line = ctx.lineage.get(op.id) ?? {};
    const ids = (list) => (list ?? []).map((v) => (typeof v === 'string' ? v : v?.id)).filter(Boolean);

    const row = {
      id: op.id,
      title: node.title ?? '',
      method: op.method ?? node.method ?? '',
      path: op.path ?? node.path ?? '',
      file: op.file ?? node.file ?? '',
      permission: op.permission ?? node.permission ?? null,
      scope: op.scopeLevel ?? node.scopeLevel ?? null,
      // `guestCallable` is null on almost everything and true where somebody
      // meant it, so only an explicit true counts.
      guest: node.guestCallable === true,
      screens: ids(usage.screens),
      flows: ids(usage.flows),
      machines: [...(ctx.movedBy.get(op.id)?.values() ?? [])],
      reads: line.reads ?? [],
      writes: line.writes ?? [],
      claim: claim(ctx.prose.get(op.id)),
    };
    row.status = statusOf(row);
    // Everything the search box can match, said once.
    row.hay = [row.id, row.title, row.permission, row.path, ...row.screens, ...row.flows,
      ...row.machines.map((m) => m.id), ...row.writes, ...row.reads].join(' ').toLowerCase();
    return row;
  });

  // No screen first: the whole point of the table is the top of it.
  return rows.sort((a, b) =>
    STATUS_RANK[a.status] - STATUS_RANK[b.status] ||
    String(a.permission).localeCompare(String(b.permission)) ||
    a.id.localeCompare(b.id));
}

/**
 * The sentence an operation's own contract prose leads with.
 *
 * Authors bold the load-bearing clause, so that is taken first. Where nothing
 * is bolded the first real sentence is used — "real" excluding the bare
 * requirement references some descriptions open with, which are a citation
 * rather than a claim and read as noise pulled out of context.
 */
function claim(text) {
  const source = String(text ?? '').trim();
  if (!source) return '';
  const tidy = (s) => s.replace(/[*`]/g, '').replace(/\s+/g, ' ').trim();

  const bold = /\*\*([^*]{20,})\*\*/.exec(source);
  if (bold) return tidy(bold[1]);

  for (const sentence of source.split(/(?<=[.!?])\s+/)) {
    const clean = tidy(sentence);
    if (clean.length >= 40) return clean;
  }
  return tidy(source).slice(0, 180);
}

/**
 * A permission every one of whose operations reaches no screen is not a gap in
 * a screen list — it is a control that exists in the contract, in the database
 * and in the permission register, and nowhere a person could use it. Computed
 * rather than chosen, so it names a different permission the day one is wired
 * up and another goes dark.
 */
function darkPermissions(rows) {
  const byPermission = new Map();
  for (const row of rows) {
    if (!row.permission) continue;
    if (!byPermission.has(row.permission)) byPermission.set(row.permission, []);
    byPermission.get(row.permission).push(row);
  }
  return [...byPermission.entries()]
    .filter(([, list]) => list.every((r) => r.status === 'unreachable'))
    .sort((a, b) => b[1].length - a[1].length);
}

/**
 * A state model whose every person-driven transition names an operation no
 * screen reaches is the same defect seen from the data side, and the more
 * convincing half: the states were drawn, the transitions were argued, and
 * nothing can take the first step.
 */
function stuckModels(lens, ctx, rows) {
  const unreachable = new Set(rows.filter((r) => r.status === 'unreachable').map((r) => r.id));
  const stuck = [];
  for (const member of lens.byKind.state ?? []) {
    const machine = ctx.machines.get(member.id);
    const driven = (machine?.transitions ?? []).filter((t) => t.operation);
    if (driven.length && driven.every((t) => unreachable.has(t.operation))) {
      stuck.push({ member, machine, drivers: [...new Set(driven.map((t) => t.operation))] });
    }
  }
  return stuck;
}

// ── links back into the viewer ───────────────────────────────────────

/** Where the viewer draws one artefact. The viewer keys an operation by its
 *  file and name, so a link built from anything less lands on the graph. */
function hrefFor(kind, id, file) {
  const hash = {
    operation: file ? `op:${file}#${id}` : null,
    state: `machine:${id}`,
    event: `event:${id}`,
    table: `table:${id}`,
    screen: `screen:${id}`,
    flow: `flow:${id}`,
    decision: `adr:${id}`,
  }[kind];
  return hash ? `/#${encodeURIComponent(hash)}` : null;
}

function link(kind, id, { file, text, title, className = 'sh-key' } = {}) {
  const href = hrefFor(kind, id, file);
  const node = el(href ? 'a' : 'span', className, text ?? id);
  if (href) node.href = href;
  if (title) node.title = title;
  return node;
}

/** A short run of links, the rest counted rather than listed. */
function links(items, max = 4) {
  const box = el('span', 'ai-links');
  for (const item of items.slice(0, max)) box.append(item);
  if (items.length > max) box.append(el('span', 'sh-quiet', `and ${fmt(items.length - max)} more`));
  return box;
}

// ── the filter ───────────────────────────────────────────────────────

const matches = (text, q) => !q || String(text).toLowerCase().includes(q.toLowerCase());
const shownRows = (s = state.scope?.state ?? {}) => state.rows.filter((r) =>
  (!s.reach || r.status === s.reach) && matches(r.hay, s.q));

function mountFilter() {
  const counts = {};
  for (const key of Object.keys(STATUS)) counts[key] = state.rows.filter((r) => r.status === key).length;
  const fields = [];
  // Only a choice when there is one. Today there is one lens, and a select
  // with one option is a control that does nothing.
  if (state.lenses.length > 1) {
    fields.push({ key: 'lens', label: 'Subject', sticky: true,
      options: state.lenses.map((l) => [l.key, l.label]) });
  }
  fields.push(
    { key: 'reach', label: 'Show', all: `Every operation (${state.rows.length})`,
      options: Object.entries(STATUS).map(([k, s]) => [k, `${s.label} (${counts[k]})`]) },
    { key: 'q', label: 'Search this page', kind: 'search',
      placeholder: 'an operation, permission, screen or table' },
  );
  $('ai-scope').hidden = false;
  state.scope = mountScope({
    root: $('ai-scope'),
    fields,
    says: (s) => {
      const shown = shownRows(s).length;
      if (!s.reach && !s.q) return '';
      const what = {
        unreachable: 'those no screen reaches',
        ungoverned: 'those on a screen with no permission named',
        ok: 'those on a screen with a permission',
      }[s.reach] ?? '';
      return `Showing ${shown} of ${plural(state.rows.length, 'operation')}`
        + `${what ? `: ${what}` : ''}`
        + `${s.q ? `${what ? ',' : ':'} matching “${s.q}”` : ''}. The opening counts every operation.`;
    },
    onChange: async (s) => {
      if (s.lens && s.lens !== state.lens.key) {
        state.lens = state.lenses.find((l) => l.key === s.lens) ?? state.lens;
        await loadProse(state.lens, state.ctx);
        state.rows = reachRows(state.lens, state.ctx);
        drawOpening();
      }
      drawLists();
      nameSearch();
    },
  });
  nameSearch();
}

/** The search box gets a stable id, for the checks that type into it. The
 *  scope redraws its controls on a change, so this runs after each one. */
function nameSearch() {
  const input = $('ai-scope').querySelector('input[type="search"]');
  if (input) input.id = 'ai-search';
}

// ── the opening ──────────────────────────────────────────────────────

function drawOpening() {
  const lens = state.lens;
  const rows = state.rows;
  const n = rows.length;
  const count = (key) => rows.filter((r) => r.status === key).length;
  const unreachable = rows.filter((r) => r.status === 'unreachable');
  const dark = darkPermissions(rows);
  const stuck = stuckModels(lens, state.ctx, rows);
  const guests = rows.filter((r) => r.guest);
  const kinds = KIND_ORDER.filter((k) => (lens.byKind[k] ?? []).length);

  $('ai-lede').textContent =
    `Every ${lens.label} operation in the package: who may call it, which screens do, and what it changes. `
    + `Counted from the contracts, screens, state models and lineage each time this page opens; `
    + `${plural(lens.stats.total, 'artefact')} across ${plural(kinds.length, 'kind')}, `
    + `reached from ${lens.seed.map((s) => `${s}.yaml`).join(', ')}.`;

  // Counted rather than asserted. The sentence has to survive an operation
  // losing its permission, and a claim about "every one of them" that nobody
  // recounts is how the prose this page replaced went wrong.
  const some = (k, many, one) => `${fmt(k)} ${k === 1 ? one : many}`;
  const governed = unreachable.filter((r) => r.permission || r.guest).length;
  const writing = unreachable.filter((r) => r.writes.length).length;
  const moving = unreachable.filter((r) => r.machines.length).length;

  const headline = unreachable.length
    ? `${fmt(unreachable.length)} of ${fmt(n)} ${lens.label} operations reach no screen`
      + (dark.length
        ? `; ${plural(dark.length, 'permission')} ${dark.length === 1 ? 'has' : 'have'} never had a screen.`
        : '.')
    : `All ${fmt(n)} ${lens.label} operations are reachable from a screen.`;

  verdict($('ai-verdict'), {
    headlineId: 'ai-headline',
    when: [el('strong', '', lens.label), ` · ${plural(n, 'operation')} in the contract`],
    headline,
    pill: unreachable.length
      ? { tone: 'bad', text: `${fmt(unreachable.length)} with no screen` }
      : { tone: 'ok', text: 'Every one reachable' },
    pace: unreachable.length
      ? `${governed === unreachable.length ? 'Every one of them names a permission' : some(governed, 'name a permission', 'names a permission')}, `
        + `${some(writing, 'write at least one table', 'writes at least one table')}, and `
        + `${some(moving, 'are named on a state model\'s transitions', 'is named on a state model\'s transitions')}. `
        + 'What none of them has is a screen, so the rule each one carries can be neither used nor broken.'
      : 'Every operation in the lens has somewhere a person can call it from.',
    ledger: [
      { label: 'Operations', value: n },
      { label: STATUS.unreachable.label, value: count('unreachable'), swatch: STATUS.unreachable.kind, bad: count('unreachable') > 0 },
      // The middle state only when it holds something: its zero is in the key
      // under the bar already, and a ledger of zeros buries the one that is not.
      ...(count('ungoverned') ? [{ label: STATUS.ungoverned.label, value: count('ungoverned'), swatch: STATUS.ungoverned.kind }] : []),
      { label: 'A guest may call', value: guests.length },
      { label: 'Permissions never on a screen', value: dark.length },
      { label: 'State models nobody can move', value: stuck.length },
    ],
    saying: guests.length
      ? `${guests.map((g) => g.id).join(', ')} ${guests.length === 1 ? 'is' : 'are'} open to a guest: `
        + 'anybody may call it, signed in or not.'
      : 'Every operation here needs somebody signed in.',
  });

  // The one picture: the operations as one bar, by state, with its key and
  // its table twin.
  const parts = Object.entries(STATUS).map(([key, s]) => ({ kind: s.kind, value: count(key), label: s.label }));
  const fig = $('ai-chart');
  fig.replaceChildren(
    stack(parts, true),
    legend(parts.map((p) => ({ kind: p.kind, label: p.label, value: p.value }))),
    table({
      caption: 'Operations by whether a screen reaches them',
      srOnly: true,
      columns: [{ key: 'label', label: 'State' }, { key: 'value', label: 'Operations', num: true }],
      rows: parts,
    }),
  );
  $('ai-figure').hidden = !n;

  const nextLine = $('ai-next');
  if (dark.length) {
    const [permission, list] = dark[0];
    const first = list[0];
    next(nextLine, [
      'Give ', el('strong', '', permission), ' a screen: no screen calls ',
      list.length === 1 ? 'its one operation, ' : `any of its ${list.length} operations, starting with `,
      link('operation', first.id, { file: first.file, className: 'sh-link' }), '.',
    ]);
  } else if (unreachable.length) {
    const first = unreachable[0];
    next(nextLine, ['Put ', link('operation', first.id, { file: first.file, className: 'sh-link' }),
      ' on a screen: it is the first of the operations nobody can call.']);
  } else if (count('ungoverned')) {
    const first = rows.find((r) => r.status === 'ungoverned');
    next(nextLine, ['Name a permission for ', link('operation', first.id, { file: first.file, className: 'sh-link' }),
      ': a screen calls it and nothing says who may.']);
  } else {
    next(nextLine, 'Nothing to do here: every operation is on a screen and says who may call it.');
  }
}

// ── the reach table ──────────────────────────────────────────────────

function drawReach() {
  const rows = shownRows();
  $('ai-reach-note').textContent =
    'One row per operation. Who may call it is the permission the contract names; the screens '
    + 'are who actually does; the state model and the tables are what changes when they do. '
    + 'An operation with no screen is a capability the package describes and nobody can use. '
    + 'Every name is a link to it in the viewer.';

  const host = $('ai-reach');
  host.replaceChildren(table({
    caption: `${plural(rows.length, 'operation')}, those with no screen first. Select a heading to sort.`,
    rowClass: (r) => `ai-op-row is-${r.status}`,
    empty: state.rows.length
      ? 'No operation matches this filter. Choose Show everything to see them all.'
      : 'This lens has no operations yet.',
    rows,
    columns: [
      { key: 'id', label: 'Operation', sort: (r) => r.id,
        render: (r) => {
          const box = el('div', 'ai-op');
          box.append(link('operation', r.id, { file: r.file, title: `${r.method} ${r.path}` }));
          if (r.title) box.append(el('span', 'ai-op-title', r.title));
          return box;
        } },
      { key: 'status', label: 'State', sort: (r) => STATUS_RANK[r.status], nowrap: true,
        render: (r) => badge(STATUS[r.status].kind, STATUS[r.status].short) },
      { key: 'permission', label: 'Who may call it', sort: (r) => r.permission ?? '',
        render: (r) => {
          const box = el('div', 'ai-who');
          box.append(r.permission ? el('code', 'ai-perm', r.permission) : el('span', 'sh-quiet', 'no permission named'));
          if (r.scope) box.append(el('span', 'sh-quiet', `at ${r.scope} level`));
          if (r.guest) box.append(el('span', 'ai-guest', 'a guest may call it'));
          return box;
        } },
      { key: 'screens', label: 'Screens that call it', sort: (r) => r.screens.length,
        render: (r) => (r.screens.length
          ? links(r.screens.map((id) => {
            const s = state.ctx.screens.get(id);
            return link('screen', id, { title: s ? `${s.name} · ${s.platformName ?? s.platform ?? ''}` : '' });
          }))
          : el('span', 'ai-none', 'none')) },
      { key: 'machines', label: 'State it moves',
        render: (r) => (r.machines.length
          ? links(r.machines.map((m) => link('state', m.id, { title: `${m.entity ?? ''} ${m.enum ?? ''}`.trim() })))
          : el('span', 'sh-quiet', '—')) },
      { key: 'writes', label: 'What it writes', sort: (r) => r.writes.length,
        render: (r) => {
          const box = el('div', 'ai-data');
          const writes = el('span', r.writes.length ? '' : 'sh-quiet', r.writes.length
            ? tally(r.writes).map(([store, k]) => `${k} ${store}`).join(', ')
            : 'nothing');
          if (r.writes.length) writes.title = `Writes ${r.writes.join(', ')}`;
          const reads = el('span', 'sh-quiet', `reads ${fmt(r.reads.length)}`);
          reads.title = r.reads.length ? `Reads ${r.reads.join(', ')}` : 'Reads nothing';
          box.append(writes, reads);
          return box;
        } },
      { key: 'flows', label: 'Journeys',
        render: (r) => (r.flows.length
          ? links(r.flows.map((id) => link('flow', id, { title: state.ctx.flows.get(id)?.name ?? '' })), 3)
          : el('span', 'sh-quiet', '—')) },
    ],
  }));
}

// ── never had a screen ───────────────────────────────────────────────

function drawDark() {
  const q = state.scope.state.q;
  const dark = darkPermissions(state.rows)
    .map(([permission, list]) => [permission, list.filter((r) => matches(`${permission} ${r.hay}`, q))])
    .filter(([, list]) => list.length);
  const stuck = stuckModels(state.lens, state.ctx, state.rows)
    .filter((s) => matches(`${s.member.id} ${s.drivers.join(' ')}`, q));

  $('ai-dark-note').textContent =
    'A permission whose every operation reaches no screen exists in the contract, the database and '
    + 'the permission register, and nowhere a person could use it. Each operation is quoted in its '
    + 'contract\'s own words, so if the rule changes the quote changes with it.';

  const host = $('ai-dark');
  host.replaceChildren();
  if (!dark.length && !stuck.length) {
    host.append(el('p', 'sh-empty', q
      ? 'Nothing here matches the search. Clear it to see every permission.'
      : 'Every permission in the lens has at least one operation a screen calls, and every state model has a step a person can take.'));
    return;
  }

  for (const [permission, list] of dark) {
    const part = el('section', 'sh-part ai-dark-part');
    const head = el('h3', 'ai-dark-head');
    head.append(el('code', 'ai-perm', permission), ' ',
      el('span', 'sh-quiet', list.length === 1 ? 'one operation, and no screen calls it'
        : `${list.length} operations, and no screen calls any of them`));
    part.append(head);
    const ul = el('ul', 'ai-dark-list');
    for (const row of list) {
      const li = el('li');
      li.append(link('operation', row.id, { file: row.file }));
      if (row.title) li.append(el('span', 'ai-op-title', row.title));
      if (row.claim) li.append(el('blockquote', 'ai-claim', row.claim));
      ul.append(li);
    }
    part.append(ul);
    host.append(part);
  }

  if (stuck.length) {
    const part = el('section', 'sh-part');
    part.append(el('h3', 'sh-part-title', 'State models nobody can move'));
    part.append(el('p', 'sh-note', `${plural(stuck.length, 'state model')} in the lens ${stuck.length === 1 ? 'has' : 'have'} `
      + 'no transition a person can trigger: every operation named on one of their transitions reaches no screen.'));
    part.append(table({
      rows: stuck,
      columns: [
        { key: 'id', label: 'State model', render: (s) => link('state', s.member.id) },
        { key: 'states', label: 'States', num: true, render: (s) => fmt(s.machine.states?.length ?? 0) },
        { key: 'transitions', label: 'Transitions', num: true, render: (s) => fmt(s.machine.transitions?.length ?? 0) },
        { key: 'drivers', label: 'Operations that would move it',
          render: (s) => links(s.drivers.map((id) => {
            const row = state.rows.find((r) => r.id === id);
            return link('operation', id, { file: row?.file });
          }), 6) },
      ],
    }));
    host.append(part);
  }
}

// ── how this was worked out ──────────────────────────────────────────

const sourceOf = (m) => (m.derived && m.declared ? 'both' : m.derived ? 'derived' : 'declared');
const SOURCE_WORDS = {
  both: 'found and tagged',
  derived: 'found by the graph',
  declared: 'tagged by hand',
};

/** The one fact per kind that is worth a column. */
function extraOf(member) {
  if (member.kind === 'operation') {
    return [member.method, member.path, member.permission].filter(Boolean).join(' · ');
  }
  if (member.kind === 'state') {
    if (!member.derived) return '';
    return `${plural(member.states ?? 0, 'state')}, ${plural(member.transitions ?? 0, 'transition')}`;
  }
  if (member.kind === 'event') {
    if (!member.derived) return '';
    return `published by ${member.publisher ?? 'nobody named'}, ${plural(member.consumers ?? 0, 'consumer')}`;
  }
  if (member.kind === 'table') {
    return `${storeOf(member.id)}, ${member.reads ?? 0} read, ${member.writes ?? 0} written`;
  }
  if (member.kind === 'screen') {
    const screen = state.ctx.screens.get(member.id);
    return screen ? `${screen.name} · ${screen.platformName ?? ''}`.trim() : '';
  }
  if (member.kind === 'flow') return state.ctx.flows.get(member.id)?.name ?? '';
  if (member.kind === 'decision') return member.label && member.label !== member.id ? member.label : (member.status ?? '');
  return '';
}

/** A folded part: a real <details>, so it opens with the keyboard and says so. */
function fold(summary, body, open = false) {
  const box = el('details', 'ai-fold');
  box.open = open;
  box.append(el('summary', '', summary), body);
  return box;
}

function memberTable(list, { why = true } = {}) {
  return table({
    rows: list,
    columns: [
      { key: 'id', label: 'Artefact', sort: (m) => m.id,
        render: (m) => link(m.kind, m.id, { file: m.file }) },
      { key: 'extra', label: 'What it is', render: (m) => extraOf(m) || '—' },
      { key: 'source', label: 'How it got here', sort: (m) => sourceOf(m), nowrap: true,
        render: (m) => SOURCE_WORDS[sourceOf(m)] },
      ...(why ? [{ key: 'why', label: 'Why', render: (m) => m.why ?? m.note ?? '' }] : []),
    ],
  });
}

function drawHow() {
  const lens = state.lens;
  const q = state.scope.state.q;
  const hay = (m) => `${m.id} ${m.label ?? ''} ${extraOf(m)} ${m.why ?? ''} ${m.note ?? ''}`;

  $('ai-how-note').textContent =
    'Membership has two sources and neither is enough on its own. The graph finds an artefact by '
    + `following the joins out from ${lens.seed.map((s) => `${s}.yaml`).join(', ')}: an operation to the `
    + 'state model it moves, the events that move publishes, the tables it writes, the screens that '
    + 'call it. A person finds one by tagging it. Each row says which happened and why, so the join '
    + 'can be checked rather than taken. Where the two disagree, both halves are listed below.';

  const host = $('ai-how');
  host.replaceChildren();

  // ── what the lens gathered
  const gathered = el('section', 'sh-part');
  gathered.append(el('h3', 'sh-part-title', 'What the lens gathered'));
  gathered.append(el('p', 'sh-note',
    `${plural(lens.stats.total, 'artefact')}: ${fmt(lens.stats.derived)} found by the graph, `
    + `${fmt(lens.stats.declared)} tagged by hand, ${fmt(lens.stats.both)} both.`));
  let any = false;
  for (const kind of KIND_ORDER) {
    const list = (lens.byKind[kind] ?? []).filter((m) => matches(hay(m), q));
    if (!list.length) continue;
    any = true;
    // Operations open, because they are the kind the page is about; the rest
    // are reference, and every row of them at once is a wall. A search opens
    // whatever it found something in.
    gathered.append(fold(`${KIND_LABEL[kind]} (${fmt(list.length)})`, memberTable(list),
      kind === 'operation' || !!q));
  }
  if (!any) gathered.append(el('p', 'sh-empty', 'Nothing the lens gathered matches the search.'));
  host.append(gathered);

  // ── the two halves of the disagreement
  const declaredOnly = lens.gaps.filter((g) => g.gap === 'declared-not-derived' && matches(hay(g), q));
  const derivedOnly = lens.gaps.filter((g) => g.gap === 'derived-not-declared' && matches(hay(g), q));

  const tagged = el('section', 'sh-part');
  tagged.append(el('h3', 'sh-part-title', 'Tagged by hand, and the graph does not reach them'));
  tagged.append(el('p', 'sh-note', declaredOnly.length
    ? 'Somebody decided these belong here and wrote it down; following the joins does not find them. '
      + 'Either the artefact has drifted out of the graph and the tag is the only thing holding it, or '
      + 'the join is real and no rule can see it, which is what tagging is for. Each is a question to '
      + 'ask whoever tagged it.'
    : q ? 'Nothing here matches the search.' : 'None: every tag in this lens is one the graph also finds.'));
  if (declaredOnly.length) {
    tagged.append(table({
      rows: declaredOnly,
      columns: [
        { key: 'kind', label: 'Kind', render: (g) => KIND_LABEL[g.kind] ?? g.kind },
        { key: 'id', label: 'Artefact', render: (g) => link(g.kind, g.id) },
        { key: 'note', label: 'What is known', render: (g) => g.note },
      ],
    }));
  }
  host.append(tagged);

  const found = el('section', 'sh-part');
  found.append(el('h3', 'sh-part-title', `Found by the graph, and nobody tagged them (${fmt(derivedOnly.length)})`));
  found.append(el('p', 'sh-note',
    'Almost all of these are right: the graph found the table because an operation writes it and the '
    + 'screen because it calls the operation, and a tag would only repeat what the join already shows. '
    + 'Read the list for the one entry that surprises you, not for something to clear.'));
  const byKind = new Map();
  for (const gap of derivedOnly) {
    if (!byKind.has(gap.kind)) byKind.set(gap.kind, []);
    byKind.get(gap.kind).push(gap);
  }
  for (const kind of KIND_ORDER.filter((k) => byKind.has(k))) {
    found.append(fold(`${KIND_LABEL[kind]} (${fmt(byKind.get(kind).length)})`, table({
      rows: byKind.get(kind),
      columns: [
        { key: 'id', label: 'Artefact', render: (g) => link(g.kind, g.id) },
        { key: 'note', label: 'How the graph reached it', render: (g) => g.note },
      ],
    }), !!q));
  }
  host.append(found);

  // ── the prose that names no operation
  if (lens.docs?.length) {
    const docs = el('section', 'sh-part');
    docs.append(el('h3', 'sh-part-title', 'Pages of prose that belong here'));
    docs.append(el('p', 'sh-note',
      'Nothing reaches these by following joins, because a page of prose calls no operation. They are '
      + 'listed by hand in lib/domains.mjs: a missing page is worse than a short list somebody keeps.'));
    const ul = el('ul', 'ai-docs');
    for (const doc of lens.docs.filter((d) => matches(d, q))) {
      const li = el('li');
      const a = el('a', 'sh-key', doc);
      a.href = `${auth.apiUrl('')}/api/file?path=${encodeURIComponent(doc)}`;
      a.target = '_blank';
      a.rel = 'noopener';
      li.append(a);
      ul.append(li);
    }
    docs.append(ul);
    host.append(docs);
  }
}

function drawLists() {
  drawReach();
  drawDark();
  drawHow();
}

// ── shell ────────────────────────────────────────────────────────────

function fail(message) {
  $('ai-error').textContent = message;
  $('ai-error').hidden = false;
  $('ai-lede').textContent = '';
  for (const id of ['reach', 'dark', 'how']) $(id).hidden = true;
}

(async () => {
  // The two panes this page used to have under other names land on the
  // section that holds them now, so an old link opens on the right thing.
  if (['#members', '#gaps'].includes(location.hash)) history.replaceState(null, '', `${location.search}#how`);

  try {
    const [domains, index, journeys, lineage, domain] = await Promise.all([
      json('/api/domains'),
      json('/api/index'),
      json('/api/journeys'),
      json('/api/lineage'),
      json('/api/domain'),
    ]);

    // Every lens but the flash sale's, which the deployment map answers.
    state.lenses = (domains.lenses ?? []).filter((l) => l.stats.total > 0 && !RETIRED.has(l.key));
    if (!domains.present || !state.lenses.length) {
      // The curtain comes down first: returning before it left a twelve-second
      // loader over a page that had already decided it had nothing to show.
      hideLoader();
      fail('The package has no AI operations to show yet: nothing in it has been gathered into this view. '
        + 'It fills in once a contract named ai.yaml is in the package.');
      return;
    }
    state.lens = state.lenses.find((l) => l.key === param('lens')) ?? state.lenses[0];
    state.ctx = buildContext({ index, journeys, lineage, domain });
    await loadProse(state.lens, state.ctx);
  } catch (error) {
    hideLoader();
    fail(`The package could not be read (${error.message}). Reload the page; if it keeps happening, `
      + 'the viewer may still be reading the package after a restart.');
    return;
  }

  state.rows = reachRows(state.lens, state.ctx);
  mountFilter();
  drawOpening();
  drawLists();
  mountPanels({ nav: document.querySelector('.set-nav'), fallback: 'reach' });
  hideLoader();
})();
