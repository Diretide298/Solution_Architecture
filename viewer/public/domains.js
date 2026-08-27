/**
 * One subject, seen across every layer at once.
 *
 * `lib/domains.mjs` says why the lens is derived rather than written down: the
 * package is organised by kind, the file that gathered AI into prose went stale
 * in six ways inside one dump, and prose cannot track a moving package. This is
 * the front of that. It asks one question and refuses to be a directory:
 *
 *   For each AI capability — who can invoke it, what does it touch, and who can
 *   stop it — and which of those three is missing?
 *
 * "Where is the AI stuff" is the question `handoff/ai-index.md` already
 * answered, and a list of 77 things is not an answer anybody acts on. The three
 * columns above are the ones that produce an action, because a capability
 * missing any of them is a defect somebody has to fix rather than a fact
 * somebody has to remember.
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
 * That is six requests for one page, which is more than any other standalone
 * view asks for. It is the honest cost of a cross-layer question: the answer
 * does not live in any single layer, and computing it in the browser is what
 * keeps it from going stale the way the prose did. They are served gzipped —
 * the whole set is a few hundred kilobytes — and fetched in parallel.
 *
 * Every number on this page is counted from those payloads. Nothing is typed.
 * The prose is typed and says only things that stay true when the counts move.
 */

import '/theme.js';   // the saved day/night choice, before anything paints
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';
import { attachSubSearch } from '/subsearch.js';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const KIND_LABEL = {
  operation: 'Operations',
  state: 'State models',
  event: 'Events',
  table: 'Tables',
  screen: 'Screens',
  flow: 'Flows',
  decision: 'Decisions',
};

/** The same words in the singular, for the sentences that count one of them. */
const KIND_ONE = {
  operation: 'operation',
  state: 'state model',
  event: 'event',
  table: 'table',
  screen: 'screen',
  flow: 'flow',
  decision: 'decision',
};

/** Contract outwards: what the API offers, what moves, what it stores, what a
 *  person sees, what path they walk, what was decided. Same order the sign-off
 *  page uses, extended to the kinds only a lens has. */
const KIND_ORDER = ['operation', 'state', 'event', 'table', 'screen', 'flow', 'decision'];

const PANES = [
  ['reach', 'Reach'],
  ['members', 'Members'],
  ['gaps', 'Gaps'],
];

const plural = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;

/** 12 → "Twelve", so a headline can open on a word rather than a digit. Falls
 *  back to the digits above twenty, where the word is harder to read. */
const WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
  'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
  'eighteen', 'nineteen', 'twenty'];
const spell = (n) => (WORDS[n] ? WORDS[n] : String(n));
const Spell = (n) => { const w = spell(n); return w[0].toUpperCase() + w.slice(1); };

const state = {
  lenses: [],
  lens: null,
  ctx: null,
  pane: 'reach',
  reachFilter: 'all',
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

/**
 * Three states, and the third is the one this page was built to show.
 *
 *   ok           somebody can call it and something says who may
 *   ungoverned   somebody can call it and nothing says who may
 *   unreachable  something says who may and nobody can call it
 *
 * A guest-callable operation counts as governed: being open to a guest is a
 * decision written down, not the absence of one.
 */
function statusOf(row) {
  const governed = Boolean(row.permission) || row.guest;
  if (!row.screens.length) return 'unreachable';
  return governed ? 'ok' : 'ungoverned';
}

const STATUS = {
  unreachable: 'Governed, and unreachable',
  ungoverned: 'Reachable, and ungoverned',
  ok: 'Reachable, and governed',
};
const STATUS_RANK = { unreachable: 0, ungoverned: 1, ok: 2 };

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
      routing: line.routing ?? null,
      service: line.service ?? null,
      claim: claim(ctx.prose.get(op.id)),
    };
    row.status = statusOf(row);
    return row;
  });

  // Unreachable first: the whole point of the pane is the top of it.
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

// ── the finding ──────────────────────────────────────────────────────

/**
 * A permission every one of whose operations is unreachable is not a gap in a
 * screen list — it is a control that exists in the contract, in the database
 * and in the permission register, and nowhere a person could use it. That is
 * worth the top of the page on its own, and it is computed rather than chosen,
 * so it will name a different permission the day one is wired up and a
 * different one goes dark.
 */
function renderFinding(rows) {
  const box = $('finding');
  box.innerHTML = '';
  box.hidden = false;

  const unreachable = rows.filter((r) => r.status === 'unreachable');
  if (!unreachable.length) {
    box.classList.add('finding-clear');
    box.append(el('h2', 'finding-title',
      `Every one of the ${plural(rows.length, 'operation')} in this lens is reachable from a screen.`));
    box.append(el('p', 'finding-body',
      'That was not true when this page was written. Whoever closed the last one, thank you.'));
    return;
  }
  box.classList.remove('finding-clear');

  // permissions where nothing at all can be invoked
  const byPermission = new Map();
  for (const row of rows) {
    if (!row.permission) continue;
    if (!byPermission.has(row.permission)) byPermission.set(row.permission, []);
    byPermission.get(row.permission).push(row);
  }
  const dark = [...byPermission.entries()]
    .filter(([, list]) => list.every((r) => r.status === 'unreachable'))
    .sort((a, b) => b[1].length - a[1].length);

  box.append(el('h2', 'finding-title',
    `${Spell(unreachable.length)} of the ${plural(rows.length, 'operation')} in this lens ` +
    'reach no screen at all.'));

  // Counted rather than asserted. The sentence has to survive an operation
  // losing its permission, and a claim about "every one of them" that nobody
  // recounts is how the prose this page replaced went wrong.
  const governed = unreachable.filter((r) => r.permission || r.guest).length;
  const writing = unreachable.filter((r) => r.writes.length).length;
  const moving = unreachable.filter((r) => r.machines.length).length;
  const some = (n, verb, verbOne) => `${n} ${n === 1 ? verbOne : verb}`;
  box.append(el('p', 'finding-body',
    `${governed === unreachable.length ? 'Every one of them names a permission' : some(governed, 'name a permission', 'names a permission')}, ` +
    `${some(writing, 'write at least one table', 'writes at least one table')}, and ` +
    `${some(moving, 'are named on the transitions of a state model', 'is named on the transitions of a state model')}. ` +
    'What none of them has is somewhere a person could stand. A rule that only exists in ' +
    'the contract cannot be obeyed and cannot be broken, because nobody can get to it.'));

  if (dark.length) {
    box.append(el('p', 'finding-body finding-emphasis',
      `${Spell(dark.length)} ${dark.length === 1 ? 'permission is' : 'permissions are'} ` +
      'dark end to end — every operation they guard is unreachable, so the permission ' +
      'itself has never had a user interface:'));

    for (const [permission, list] of dark) {
      const card = el('div', 'dark-perm');
      const head = el('div', 'dark-perm-head');
      head.append(el('span', 'perm-chip perm-chip-dark', permission));
      head.append(el('span', 'dark-perm-count', list.length === 1
        ? 'one operation, and no screen calls it'
        : `${list.length} operations, and no screen calls any of them`));
      card.append(head);

      for (const row of list) {
        const item = el('div', 'dark-op');
        item.append(opLink(row, 'dark-op-name'));
        if (row.title) item.append(el('span', 'dark-op-title', row.title));
        // The contract's own words, not the page's. If the rule changes, the
        // quote changes with it.
        if (row.claim) item.append(el('blockquote', 'dark-op-claim', row.claim));
        card.append(item);
      }
      box.append(card);
    }
  }

  // A state model whose every human-driven transition names an unreachable
  // operation is the same defect seen from the data side, and it is the more
  // convincing half: the states were drawn, the transitions were argued, and
  // nothing can take the first step.
  const unreachableIds = new Set(unreachable.map((r) => r.id));
  const stuck = [];
  for (const member of state.lens.byKind.state ?? []) {
    const machine = state.ctx.machines.get(member.id);
    const driven = (machine?.transitions ?? []).filter((t) => t.operation);
    if (!driven.length) continue;
    if (driven.every((t) => unreachableIds.has(t.operation))) {
      stuck.push({ member, machine, driven });
    }
  }

  if (stuck.length) {
    box.append(el('p', 'finding-body finding-emphasis',
      `The same hole seen from the data: ${plural(stuck.length, 'state model')} in this lens ` +
      `${stuck.length === 1 ? 'has' : 'have'} no transition a person can trigger, because ` +
      'every operation named on one of their transitions is in the list above.'));

    const list = el('div', 'stuck-list');
    for (const { member, machine, driven } of stuck) {
      const drivers = [...new Set(driven.map((t) => t.operation))];
      const row = el('div', 'stuck-row');
      row.append(el('span', 'stuck-name', member.id));
      row.append(el('span', 'stuck-detail',
        `${plural(machine.states?.length ?? 0, 'state')} · ` +
        `${plural(machine.transitions?.length ?? 0, 'transition')} · ` +
        `${plural(drivers.length, 'operation')} ${drivers.length === 1 ? 'drives' : 'drive'} it`));
      row.append(el('span', 'stuck-ops', drivers.join(', ')));
      list.append(row);
    }
    box.append(list);
  }
}

// ── headline numbers ─────────────────────────────────────────────────

function renderHeadline(lens, rows) {
  const box = $('headline');
  box.innerHTML = '';

  const stat = (value, label, hint) => {
    const card = el('div', 'stat-card');
    card.append(el('div', 'stat-value', String(value)));
    card.append(el('div', 'stat-label', label));
    if (hint) card.append(el('div', 'stat-hint', hint));
    return card;
  };

  const kinds = KIND_ORDER.filter((k) => (lens.byKind[k] ?? []).length);
  const unreachable = rows.filter((r) => r.status === 'unreachable').length;
  const guests = rows.filter((r) => r.guest);
  const declaredOnly = lens.members.filter((m) => m.declared && !m.derived).length;
  const derivedOnly = lens.members.filter((m) => m.derived && !m.declared).length;

  box.append(stat(lens.stats.total, 'artefacts in the lens',
    `${plural(kinds.length, 'kind')}, reached from ${plural(lens.seed.length, 'seed contract')}`));

  box.append(stat(`${unreachable} of ${rows.length}`, 'operations with no screen',
    unreachable
      ? 'Nobody can invoke them. Start on the Reach pane.'
      : 'Every operation has somewhere a person could stand.'));

  box.append(stat(`${guests.length} of ${rows.length}`, 'callable by a guest',
    guests.length
      ? `${guests.map((g) => g.id).join(', ')} — the assistant is open to the public here.`
      : 'Everything in this lens needs a signed-in principal.'));

  box.append(stat(declaredOnly, 'declared, and unreachable',
    declaredOnly
      ? `Somebody tagged these by hand. The other ${derivedOnly} the graph found on its own.`
      : `Every tag is corroborated by the graph; ${derivedOnly} more went untagged.`));
}

// ── reach pane ───────────────────────────────────────────────────────

function opLink(row, className) {
  // The viewer keys an operation node by its file and name, so a link built
  // from anything less will land on the graph rather than the operation.
  const link = el('a', className, row.id);
  link.href = `/#${encodeURIComponent(`op:${row.file}#${row.id}`)}`;
  link.title = `${row.method} ${row.path}`;
  return link;
}

function screenPill(id) {
  const screen = state.ctx.screens.get(id);
  const pill = el('a', 'nav-pill reach-pill', id);
  pill.href = `/#${encodeURIComponent(`screen:${id}`)}`;
  if (screen) pill.title = `${screen.name} · ${screen.platformName ?? screen.platform ?? ''}`.trim();
  return pill;
}

function renderReach(lens, rows) {
  const host = $('reach');
  host.innerHTML = '';

  const counts = { all: rows.length };
  for (const key of Object.keys(STATUS)) counts[key] = rows.filter((r) => r.status === key).length;

  $('reach-note').textContent =
    `${plural(rows.length, 'operation')} · sorted so the unreachable come first`;
  $('reach-lead').textContent =
    'One row per operation. The principal is who may call it, the screens are who does, ' +
    'and the state model and the tables are what happens when they do. An operation ' +
    'missing the middle column is a capability the package describes and nobody can use.';

  // The filter names the three states rather than hiding them behind "all",
  // so a state with nothing in it still says so — a zero here is a finding.
  const filter = $('reach-filter');
  filter.innerHTML = '';
  for (const [key, label] of [['all', 'Every operation'], ...Object.entries(STATUS)]) {
    const button = el('button', null, `${label} · ${counts[key]}`);
    button.type = 'button';
    if (state.reachFilter === key) button.classList.add('active');
    button.onclick = () => { state.reachFilter = key; draw(); };
    filter.append(button);
  }

  const legend = $('reach-legend');
  legend.innerHTML = '';
  for (const [key, label] of Object.entries(STATUS)) {
    const item = el('span', 'reach-legend-item');
    item.append(el('span', `reach-dot ${key}`));
    item.append(el('span', null, `${label} — ${counts[key]}`));
    if (!counts[key]) item.classList.add('reach-legend-empty');
    legend.append(item);
  }
  // A zero on the middle state is worth a sentence rather than a blank. It is
  // the answer to "is the governance missing?" and the answer is no — which is
  // what makes the twelve on the left the finding rather than a symptom.
  if (!counts.ungoverned) {
    const ungoverned = rows.filter((r) => !r.permission && !r.guest).length;
    legend.append(el('span', 'reach-legend-note',
      (ungoverned
        ? `Nothing reachable is ungoverned, though ${plural(ungoverned, 'operation')} names no permission at all. `
        : 'Nothing here is ungoverned: every operation in the lens names a permission. ') +
      'What is missing is not the rule — it is the screen.'));
  }

  const shown = state.reachFilter === 'all'
    ? rows
    : rows.filter((r) => r.status === state.reachFilter);

  // Column headings over nothing are furniture, so the empty case gets the
  // sentence instead.
  if (!shown.length) {
    host.append(el('p', 'pane-empty', 'No operation in this lens is in that state.'));
    return;
  }

  const head = el('div', 'reach-row reach-head');
  for (const label of ['Operation', 'Principal', 'Screens that call it',
    'State it moves', 'What it writes', 'Flow']) {
    head.append(el('span', null, label));
  }
  host.append(head);

  for (const row of shown) host.append(reachRow(row));
}

function reachRow(row) {
  const node = el('div', `reach-row reach-${row.status}`);

  const name = el('span', 'reach-op');
  name.append(opLink(row, 'reach-op-name'));
  if (row.title) name.append(el('span', 'reach-op-title', row.title));
  node.append(name);

  const principal = el('span', 'reach-principal');
  if (row.permission) principal.append(el('span', 'perm-chip', row.permission));
  else principal.append(el('span', 'perm-chip perm-chip-none', 'no permission'));
  if (row.scope) principal.append(el('span', 'reach-scope', `${row.scope} scope`));
  if (row.guest) principal.append(el('span', 'guest-chip', 'a guest may call this'));
  node.append(principal);

  const screens = el('span', 'reach-screens');
  if (row.screens.length) {
    for (const id of row.screens.slice(0, 4)) screens.append(screenPill(id));
    if (row.screens.length > 4) {
      screens.append(el('span', 'reach-more', `+${row.screens.length - 4}`));
    }
  } else {
    screens.append(el('span', 'reach-none', 'no screen declares it'));
  }
  node.append(screens);

  const machines = el('span', 'reach-machines');
  if (row.machines.length) {
    for (const m of row.machines) {
      const pill = el('span', 'reach-machine', m.id);
      pill.title = `${m.entity} · ${m.enum ?? ''}`.trim();
      machines.append(pill);
    }
  } else {
    machines.append(el('span', 'reach-quiet', '—'));
  }
  node.append(machines);

  // Reads are a fact about the operation; writes are a fact about the blast
  // radius, so the writes are the ones named and the reads trail behind.
  const data = el('span', 'reach-data');
  if (row.writes.length) {
    const stores = tally(row.writes)
      .map(([store, n]) => `${n} ${store}`)
      .join(' · ');
    const line = el('span', 'reach-writes', stores);
    line.title = `writes ${row.writes.join(', ')}`;
    data.append(line);
  } else {
    data.append(el('span', 'reach-quiet', 'writes nothing'));
  }
  const reads = el('span', 'reach-reads', `${row.reads.length} read`);
  reads.title = row.reads.length ? `reads ${row.reads.join(', ')}` : 'reads nothing';
  data.append(reads);
  node.append(data);

  const flows = el('span', 'reach-flows');
  if (row.flows.length) {
    for (const id of row.flows) {
      const pill = el('span', 'reach-flow', id);
      const flow = state.ctx.flows.get(id);
      if (flow) pill.title = flow.name;
      flows.append(pill);
    }
  } else {
    flows.append(el('span', 'reach-quiet', '—'));
  }
  node.append(flows);

  return node;
}

// ── members pane ─────────────────────────────────────────────────────

/**
 * A heading that folds its own content away, the way every section heading in
 * the viewer does. The whole label is the target rather than a marker beside
 * it, which is what makes it usable with a thumb — and it takes the keyboard,
 * because a div that behaves like a button has to behave like one throughout.
 */
function foldable(text) {
  const label = el('div', 'journey-section-label', text);
  const body = el('div', 'member-body');
  label.tabIndex = 0;
  label.setAttribute('role', 'button');
  const fold = () => {
    const closed = label.classList.toggle('collapsed');
    body.hidden = closed;
    label.setAttribute('aria-expanded', String(!closed));
  };
  label.setAttribute('aria-expanded', 'true');
  label.onclick = fold;
  label.onkeydown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fold(); }
  };
  return [label, body];
}

const sourceOf = (m) => (m.derived && m.declared ? 'both' : m.derived ? 'derived' : 'declared');
const SOURCE_LABEL = { both: 'both', derived: 'derived', declared: 'declared' };

function renderMembers(lens) {
  const host = $('members');
  host.innerHTML = '';

  $('members-note').textContent =
    `${plural(lens.stats.total, 'artefact')} · ${lens.stats.derived} reached, ` +
    `${lens.stats.declared} tagged, ${lens.stats.both} both`;
  $('members-lead').textContent =
    'Membership has two sources and neither is enough on its own. The graph reaches an ' +
    'artefact by closure from the seed contract; a person reaches one by writing the tag. ' +
    'Each row says which happened and why, so a reader can check the join rather than ' +
    'take it.';

  for (const kind of KIND_ORDER) {
    const list = lens.byKind[kind] ?? [];
    if (!list.length) continue;

    const section = el('div', 'member-section');
    const [label, body] = foldable(`${KIND_LABEL[kind]} · ${list.length}`);
    // Operations are left open because they are the kind the whole page is
    // about; the other six are reference, and 77 rows at once is a wall.
    if (kind !== 'operation') label.click();

    const sorted = [...list].sort((a, b) =>
      (a.derived === b.derived ? 0 : a.derived ? 1 : -1) || a.id.localeCompare(b.id));

    for (const member of sorted) {
      const row = el('div', 'member-row');
      const source = sourceOf(member);
      row.append(el('span', `source-chip source-${source}`, SOURCE_LABEL[source]));

      const main = el('span', 'member-main');
      main.append(el('span', 'member-id', member.id));
      if (member.label && member.label !== member.id) {
        main.append(el('span', 'member-label', member.label));
      }
      row.append(main);

      row.append(el('span', 'member-extra', extraOf(member)));
      row.append(el('span', 'member-why', member.why ?? ''));
      body.append(row);
    }

    section.append(label, body);
    host.append(section);
  }

  if (lens.docs?.length) {
    const section = el('div', 'member-section');
    const [label, body] = foldable(
      `Prose that belongs here and names no operation · ${lens.docs.length}`);
    body.append(el('p', 'pane-note',
      'Nothing reaches these by closure, because a page of prose calls no operation. ' +
      'They are listed by hand in lib/domains.mjs, which is a cost worth paying: a ' +
      'missing page is worse than a short list somebody has to maintain.'));
    for (const doc of lens.docs) {
      const row = el('div', 'member-row member-doc');
      const link = el('a', 'member-id', doc);
      link.href = `${auth.apiUrl('')}/api/file?path=${encodeURIComponent(doc)}`;
      link.target = '_blank';
      link.rel = 'noopener';
      row.append(link);
      body.append(row);
    }
    section.append(label, body);
    host.append(section);
  }
}

/** The one fact per kind that is worth a column. */
function extraOf(member) {
  if (member.kind === 'operation') {
    return [member.method, member.path, member.permission].filter(Boolean).join(' · ');
  }
  if (member.kind === 'state') {
    if (!member.derived) return '';
    return `${plural(member.states ?? 0, 'state')} · ${plural(member.transitions ?? 0, 'transition')}`;
  }
  if (member.kind === 'event') {
    if (!member.derived) return '';
    return `published by ${member.publisher ?? '—'} · ${plural(member.consumers ?? 0, 'consumer')}`;
  }
  if (member.kind === 'table') {
    return `${storeOf(member.id)} · ${member.reads ?? 0} read, ${member.writes ?? 0} written`;
  }
  if (member.kind === 'screen') {
    const screen = state.ctx.screens.get(member.id);
    return screen ? `${screen.name} · ${screen.platformName ?? ''}`.trim() : '';
  }
  if (member.kind === 'flow') {
    return state.ctx.flows.get(member.id)?.name ?? '';
  }
  if (member.kind === 'decision') return member.status ?? '';
  return '';
}

// ── gaps pane ────────────────────────────────────────────────────────

/**
 * A view whose every row is a problem is a view nobody reads, and 53 rows all
 * called "gap" is exactly that. They are not one thing. Three are somebody's
 * intent that the graph cannot corroborate, which is a question that needs an
 * answer. The other fifty are the graph reaching something nobody bothered to
 * tag, which is mostly correct and mostly not worth doing anything about —
 * tagging a table the closure already found would only say it twice.
 *
 * So they are split, the small pile is opened, and the large one is offered
 * rather than presented.
 */
function renderGaps(lens) {
  const host = $('gaps');
  host.innerHTML = '';

  const declaredOnly = lens.gaps.filter((g) => g.gap === 'declared-not-derived');
  const derivedOnly = lens.gaps.filter((g) => g.gap === 'derived-not-declared');

  $('gaps-note').textContent =
    `${lens.gaps.length} in total · ${declaredOnly.length} worth an answer`;
  $('gaps-lead').textContent =
    'The lens reports the disagreement rather than picking a side. The two halves are ' +
    'not the same size and not the same problem, so they are not in the same list.';

  // ── the interesting ones
  const first = el('div', 'gap-block gap-block-warn');
  first.append(el('h3', 'gap-title',
    declaredOnly.length
      ? `${Spell(declaredOnly.length)} ${declaredOnly.length === 1 ? 'artefact was' : 'artefacts were'} ` +
        'tagged by hand, and nothing in the graph reaches them'
      : 'Every tag in this lens is corroborated by the graph'));
  first.append(el('p', 'gap-lead',
    declaredOnly.length
      ? 'Somebody decided these belong here and wrote it down. The closure disagrees. ' +
        'Either the artefact has drifted out of the graph and the tag is the only thing ' +
        'holding it, or the join is real and no rule can see it — which is the case the ' +
        'declaration exists for. Each one is a question with a person attached to it.'
      : 'Nothing was claimed for this lens that the closure could not also reach.'));

  if (declaredOnly.length) {
    for (const gap of declaredOnly) {
      const row = el('div', 'gap-row');
      row.append(el('span', 'gap-kind', KIND_LABEL[gap.kind] ?? gap.kind));
      row.append(el('span', 'gap-id', gap.id));
      row.append(el('span', 'gap-note', gap.note));
      first.append(row);
    }
  }
  host.append(first);

  // ── the bulk
  const byKind = new Map();
  for (const gap of derivedOnly) {
    if (!byKind.has(gap.kind)) byKind.set(gap.kind, []);
    byKind.get(gap.kind).push(gap);
  }
  const ordered = KIND_ORDER.filter((k) => byKind.has(k));

  const second = el('div', 'gap-block');
  second.append(el('h3', 'gap-title',
    `${derivedOnly.length} the graph reached and nobody tagged`));

  const shape = ordered
    .map((k) => plural(byKind.get(k).length, KIND_ONE[k] ?? k, (KIND_LABEL[k] ?? k).toLowerCase()))
    .join(', ');
  second.append(el('p', 'gap-lead',
    `These are ${shape}. Almost all of them are correct: the closure found the table ` +
    'because an operation writes it and found the screen because a screen calls the ' +
    'operation, and a tag would only repeat what the join already proves. Read this ' +
    'list looking for the one entry that surprises you, not for something to clear.'));

  for (const kind of ordered) {
    const list = byKind.get(kind);
    const [label, body] = foldable(`${KIND_LABEL[kind]} · ${list.length}`);
    // Closed to start. The framing above says these are mostly fine, and
    // opening fifty rows that say so would contradict it.
    label.click();

    for (const gap of list) {
      const row = el('div', 'gap-row gap-row-quiet');
      row.append(el('span', 'gap-id', gap.id));
      row.append(el('span', 'gap-note', gap.note));
      body.append(row);
    }
    second.append(label, body);
  }
  host.append(second);
}

// ── shell ────────────────────────────────────────────────────────────

function renderLensHead(lens) {
  $('lens-title').textContent = `${lens.label} across the package`;
  $('lens-blurb').textContent = lens.blurb;

  const meta = $('lens-meta');
  meta.innerHTML = '';
  meta.append(el('span', 'lens-meta-label', 'reached from'));
  for (const seed of lens.seed) meta.append(el('span', 'lens-seed', `${seed}.yaml`));
  meta.append(el('span', 'lens-meta-label', 'plus prose that names no operation'));
  meta.append(el('span', 'lens-seed lens-seed-doc', plural(lens.docs?.length ?? 0, 'page')));
}

function renderPaneTabs() {
  const tabs = $('pane-tabs');
  tabs.innerHTML = '';
  for (const [key, label] of PANES) {
    const button = el('button', null, label);
    button.type = 'button';
    if (state.pane === key) button.classList.add('active');
    button.onclick = () => { state.pane = key; location.hash = key; draw(); };
    tabs.append(button);
  }
}

/**
 * Only drawn when there is a choice. One lens behind a one-button segmented
 * control is a control that does nothing, and the page already names the lens
 * in its heading.
 */
function renderLensTabs() {
  const tabs = $('lens-tabs');
  tabs.hidden = state.lenses.length < 2;
  if (tabs.hidden) return;
  tabs.innerHTML = '';
  for (const lens of state.lenses) {
    const button = el('button', null, lens.label);
    button.type = 'button';
    if (lens.key === state.lens.key) button.classList.add('active');
    button.onclick = async () => {
      state.lens = lens;
      await loadProse(lens, state.ctx);
      draw();
    };
    tabs.append(button);
  }
}

function draw() {
  const lens = state.lens;
  const rows = reachRows(lens, state.ctx);

  renderLensHead(lens);
  renderLensTabs();
  renderPaneTabs();
  renderHeadline(lens, rows);
  renderFinding(rows);

  renderReach(lens, rows);
  renderMembers(lens);
  renderGaps(lens);

  for (const [key] of PANES) $(`pane-${key}`).hidden = state.pane !== key;
}

function fail(message) {
  const box = $('error');
  box.textContent = message;
  box.hidden = false;
  $('lens-title').textContent = 'The lens could not be read';
}

(async () => {
  const fromHash = location.hash.slice(1);
  if (PANES.some(([key]) => key === fromHash)) state.pane = fromHash;

  try {
    const [domains, index, journeys, lineage, domain] = await Promise.all([
      json('/api/domains'),
      json('/api/index'),
      json('/api/journeys'),
      json('/api/lineage'),
      json('/api/domain'),
    ]);

    state.lenses = (domains.lenses ?? []).filter((l) => l.stats.total > 0);
    if (!domains.present || !state.lenses.length) {
      return fail('No domain lens has anything in it yet. Nothing has been seeded.');
    }
    state.lens = state.lenses[0];
    state.ctx = buildContext({ index, journeys, lineage, domain });
    await loadProse(state.lens, state.ctx);
  } catch (error) {
    hideLoader();
    return fail(`Could not read the package: ${error.message}`);
  }

  draw();
  hideLoader();

  window.addEventListener('hashchange', () => {
    const key = location.hash.slice(1);
    if (PANES.some(([k]) => k === key) && key !== state.pane) {
      state.pane = key;
      draw();
    }
  });
})();

// Narrowing what is already here, which is a different need from the palette's:
// the palette leaves the page to find something, this stays on it. Attached
// after the first render so the sections exist; it re-applies itself as the
// lens redraws, because switching lens replaces every row underneath it.
attachSubSearch(
  document.getElementById('subsearch'),
  // Three containers, not two. `#finding` holds the stuck-state finding and is
  // easy to miss because it is usually two rows out of 237 — which is exactly
  // the size of thing a filter has to catch, since two rows left standing under
  // a filter that matched nothing read as two rows that *did* match.
  [
    { box: document.getElementById('members'), rows: '.member-row, .stuck-row' },
    { box: document.getElementById('finding'), rows: '.stuck-row' },
    { box: document.getElementById('gaps'), rows: '.gap-row' },
  ],
  { count: document.getElementById('subsearch-count'), noun: 'rows' },
);
