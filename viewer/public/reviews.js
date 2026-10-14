/**
 * Reviews: where the review of the package stands, and what is waiting on us.
 *
 * **Two pages became this one** (14 October). "What has been signed off"
 * (validation.html) read the newest verdict per artefact; "Review activity"
 * read every verdict ever given. They were the same store read two ways, under
 * three names, and each could answer only half of what somebody opens either
 * for: *is the review keeping up, and what has it asked us to do?* The first
 * half needs the population (what there is to review); the second needs the
 * history (who asked for what, and whether anybody answered). This page reads
 * both once and draws every section from the same filtered set, so a count in
 * the headline and a row in a list can never disagree.
 *
 * **The order is the Tasks page's.** It opens on a verdict: one sentence of
 * coverage, a pace line naming the open asks and the disagreement, the
 * figures as a line of type, coverage by kind as the one bold picture, and a
 * "Next" naming the oldest unanswered ask. Then the worklist, second on the
 * rail rather than last, because it is the only part anybody acts on.
 *
 * **One filter for the whole page**, in the address: kind, whose review (the
 * team's, the client's or both: client verdicts were returned by the service
 * and shown nowhere), reviewer, window and a search. The search is the only
 * text box on the page. There used to be two, filtering different things.
 *
 * **State colours, one meaning each** (sheet.css): approved is done, an open
 * ask for work is stalled (waiting on somebody), fixed is qa (finished, for
 * the reviewer to look at again), never reviewed is fresh. Rejected and needs
 * work are both "asked for work" in every picture, and said in words beside.
 */
import '/page-chrome.js';
import * as auth from '/validation.js';
import { hideLoader } from '/loader.js';
import { mountPanels } from '/panels.js';
import {
  el, fmt, plural, ago, daysSince, param, setParams, personLink,
  verdict, next, mountScope, legend, badge, stack, table,
} from '/sheet.js';
import {
  KINDS, MODULE_KIND, kindOf, kindLabel, artefactKey, viewerHref,
  loadPopulations, standingOf, isOpenAsk, STANDINGS,
} from '/reviews-coverage.js';
import {
  statusCell, statusOf, exportCsv,
  VERDICT_LABEL, TAG_LABEL, LAYER_LABEL, RESPONSE_LABEL,
} from '/reviews-respond.js';

const $ = (id) => document.getElementById(id);
const DAY = 86_400_000;
const SVG = 'http://www.w3.org/2000/svg';
const svg = (tag, attrs = {}, text) => {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  if (text != null) node.textContent = text;
  return node;
};
const firstName = (name) => String(name ?? '').split(/[\s@]/)[0] || name;
const who = (v) => v.by || v.by_email;
const isClientRow = (v) => (v.audience || 'internal') === 'client';

const state = {
  me: null,
  populations: new Map(),   // kind -> {rows, error}
  index: new Map(),         // "kind id" -> artefact from the population
  verdicts: [],
  accounts: [],
  mentions: [],
  mentionsError: '',
  scope: null,              // mountScope's handle
  // Filters that belong to one section, on top of the page's. In the address
  // too, so "the open asks on the backend" is a link somebody can send.
  local: {
    only: param('only') === '1',
    said: param('said'), status: param('status'), lands: param('lands'), layer: param('layer'),
  },
  pages: {},                // table id -> rows shown
  sorts: {},                // table id -> {key, dir}
  view: null,               // the last derived view, see derive()
  section: '',
};

// ── the filter ───────────────────────────────────────────────────────

const SIDES = [['', 'Both'], ['internal', 'The team'], ['client', 'The client']];
const WINDOWS = [['7', 'Last 7 days'], ['14', 'Last 14 days'], ['30', 'Last 30 days'], ['90', 'Last 90 days']];

/** The reviewers in the store, by email (unique) with their name as the label. */
function reviewerOptions() {
  const seen = new Map();
  for (const v of state.verdicts) if (!seen.has(v.by_email)) seen.set(v.by_email, who(v));
  return [...seen].sort((a, b) => a[1].localeCompare(b[1]));
}
const nameOf = (email) => reviewerOptions().find(([e]) => e === email)?.[1] ?? email;

/**
 * A link from elsewhere may name a reviewer the way people do, by name
 * (`?person=Asha Menon`), where the filter keys on the address because two
 * accounts can share a name. Resolved once, before the filter reads the URL.
 */
function resolvePersonParam() {
  const want = param('person');
  if (!want) return;
  const options = reviewerOptions();
  if (options.some(([email]) => email === want)) return;
  const byName = options.find(([, name]) => name.toLowerCase() === want.toLowerCase());
  setParams({ person: byName ? byName[0] : '' });
}

function says(s) {
  const whose = s.side === 'client' ? "the client's verdicts"
    : s.side === 'internal' ? "the team's verdicts"
    : "the team's and the client's verdicts";
  let line = `Showing ${whose}`;
  if (s.kind) line += ` on ${kindOf(s.kind)?.many ?? s.kind}`;
  if (s.person) line += ` by ${nameOf(s.person)}`;
  if (s.window) line += ` from the last ${s.window} days`;
  if (s.q) line += `, about anything matching "${s.q}"`;
  return `${line}.`;
}

function mountFilter() {
  const kinds = () => {
    const list = KINDS.map((k) => [k.key, k.label]);
    if (state.verdicts.some((v) => v.target_kind === 'module')) list.push([MODULE_KIND.key, MODULE_KIND.label]);
    return list;
  };
  state.scope = mountScope({
    root: $('rv-scope'),
    fields: [
      { key: 'kind', label: 'Kind', options: kinds, all: 'Every kind' },
      { key: 'side', label: 'Whose review', options: SIDES, kind: 'switch' },
      { key: 'person', label: 'Reviewer', options: reviewerOptions, all: 'Everyone' },
      { key: 'window', label: 'Given in', options: WINDOWS, all: 'All time' },
      { key: 'q', label: 'Find', kind: 'search', placeholder: 'artefact, note or reviewer' },
    ],
    says,
    onChange: () => {
      // A new filter is a new list: start every table at its first page.
      state.pages = {};
      redraw();
    },
  });
}

// ── deriving one view from the filter ───────────────────────────────

/**
 * Everything every section draws, computed once per change. Sections read
 * this and never filter on their own, which is what keeps the headline's
 * numbers and the lists' rows the same rows.
 */
function derive() {
  const s = state.scope.state;
  const needle = (s.q ?? '').trim().toLowerCase();
  const cutoff = s.window ? Date.now() - Number(s.window) * DAY : null;
  const artText = (a) => `${a.id} ${a.name} ${a.detail ?? ''} ${a.group ?? ''}`.toLowerCase();

  const passes = (v) => {
    if (s.kind && v.target_kind !== s.kind) return false;
    if (s.side && (v.audience || 'internal') !== s.side) return false;
    if (s.person && v.by_email !== s.person) return false;
    if (cutoff && Date.parse(v.at) < cutoff) return false;
    if (needle) {
      const a = state.index.get(artefactKey(v.target_kind, v.target_id));
      const hay = `${v.target_id} ${v.note ?? ''} ${v.by ?? ''} ${v.by_email ?? ''} ${a ? artText(a) : ''}`;
      if (!hay.toLowerCase().includes(needle)) return false;
    }
    return true;
  };
  const rows = state.verdicts.filter(passes);

  const byKey = new Map();
  for (const v of rows) {
    const key = artefactKey(v.target_kind, v.target_id);
    if (!byKey.has(key)) byKey.set(key, []);
    byKey.get(key).push(v);
  }

  // Judged against the artefact's rows in the whole store, not the filtered
  // set: an ask its author has since replaced with an approval is closed
  // whether or not the approval falls inside the window being looked at.
  const everything = new Map();
  for (const v of state.verdicts) {
    const key = artefactKey(v.target_kind, v.target_id);
    if (!everything.has(key)) everything.set(key, []);
    everything.get(key).push(v);
  }

  // Coverage, against the whole population of each kind in scope.
  const kinds = s.kind ? KINDS.filter((k) => k.key === s.kind) : KINDS;
  const artefacts = [];
  const failed = [];
  for (const kind of kinds) {
    const pop = state.populations.get(kind.key);
    if (!pop || pop.error) { failed.push({ kind, error: pop?.error ?? 'not read' }); continue; }
    for (const a of pop.rows) {
      const key = artefactKey(kind.key, a.id);
      if (needle && !artText(a).includes(needle) && !byKey.has(key)) continue;
      artefacts.push({ ...a, key, ...standingOf(byKey.get(key), everything.get(key)) });
    }
  }
  const tally = (list) => {
    const t = { approved: 0, open: 0, fixed: 0, none: 0, total: list.length };
    for (const a of list) t[a.standing]++;
    return t;
  };

  // Verdicts about things the package no longer has: in the lists, never in
  // a count against a population they are not part of.
  const gone = new Set();
  for (const key of byKey.keys()) {
    const [kind] = key.split(' ');
    const pop = state.populations.get(kind);
    if (pop && !pop.error && !state.index.has(key)) gone.add(key);
  }

  // The worklist: every ask for work nobody has answered, oldest first.
  const withdrawn = new Set(rows
    .filter((v) => auth.asksForWork(v.verdict) && !auth.isSettled(v)
      && !isOpenAsk(v, everything.get(artefactKey(v.target_kind, v.target_id))))
    .map((v) => v.id));
  const open = rows.filter((v) => auth.asksForWork(v.verdict) && !auth.isSettled(v) && !withdrawn.has(v.id))
    .sort((a, b) => Date.parse(a.at) - Date.parse(b.at) || a.id - b.id);

  // Disagreement means two *different people* reaching different verdicts.
  // One person changing their own mind is a revision, which is healthy.
  const contested = [];
  const pairs = new Map();
  for (const [key, list] of byKey) {
    const latest = new Map();
    for (const v of [...list].sort((a, b) => a.id - b.id)) latest.set(v.account_id, v);
    const views = [...latest.values()];
    if (views.length < 2 || new Set(views.map((v) => v.verdict)).size < 2) continue;
    contested.push({ key, views, at: Math.max(...views.map((v) => Date.parse(v.at))) });
    for (let i = 0; i < views.length; i++) {
      for (let j = i + 1; j < views.length; j++) {
        if (views[i].verdict === views[j].verdict) continue;
        const pair = [who(views[i]), who(views[j])].sort().join('\u0000');
        pairs.set(pair, (pairs.get(pair) ?? 0) + 1);
      }
    }
  }
  contested.sort((a, b) => b.at - a.at);
  const topPair = [...pairs].sort((a, b) => b[1] - a[1])[0] ?? null;

  const mentions = state.mentions.filter(passes);

  state.view = {
    s, rows, byKey, kinds, artefacts, failed, gone, open, withdrawn, contested, topPair, mentions,
    totals: tally(artefacts), tally,
  };
  return state.view;
}

// ── where it stands ─────────────────────────────────────────────────

function drawCoverage(view) {
  const { s, totals, open, contested, topPair, rows, failed } = view;
  const kind = s.kind ? kindOf(s.kind) : null;
  const noun = kind ? kind.many : 'artefacts';
  const reviewed = totals.total - totals.none;
  const subject = s.person ? nameOf(s.person)
    : s.side === 'client' ? 'The client' : s.side === 'internal' ? 'The team' : '';

  let headline;
  if (s.kind === 'module') {
    headline = plural(new Set(rows.map((v) => v.target_id)).size, 'module has a verdict', 'modules have a verdict');
  } else if (!totals.total) {
    headline = failed.length
      ? 'The package could not be read, so there is nothing to count the verdicts against.'
      : `Nothing in the package matches "${s.q}"`;
  } else if (subject) {
    headline = `${subject} has given a verdict on ${fmt(reviewed)} of ${fmt(totals.total)} ${noun}`;
  } else {
    headline = `${fmt(reviewed)} of ${fmt(totals.total)} ${noun} have a verdict`;
  }

  // The pace line: the open asks, then the disagreement, in words.
  const openArtefacts = new Set(open.map((v) => artefactKey(v.target_kind, v.target_id))).size;
  const oldest = open[0];
  const oldestDays = oldest ? daysSince(oldest.at) : 0;
  const pace = [];
  if (open.length) {
    pace.push(`${plural(open.length, 'ask for work is', 'asks for work are')} open` +
      `${openArtefacts !== open.length ? ` on ${plural(openArtefacts, 'artefact')}` : ''}, ` +
      `the oldest ${oldestDays === 0 ? 'from today' : `${plural(oldestDays, 'day')} old`}.`);
  } else if (rows.some((v) => auth.asksForWork(v.verdict))) {
    pace.push('Every ask for work has been answered.');
  } else if (rows.length) {
    pace.push('Nobody has asked for work.');
  }
  if (contested.length) {
    if (topPair && topPair[1] === contested.length) {
      const [a, b] = topPair[0].split('\u0000');
      pace.push(`${firstName(a)} and ${firstName(b)} disagree on ${fmt(contested.length)}.`);
    } else {
      pace.push(`Reviewers disagree on ${plural(contested.length, 'artefact')}` +
        (topPair ? `, ${firstName(topPair[0].split('\u0000')[0])} and ${firstName(topPair[0].split('\u0000')[1])} most often (${fmt(topPair[1])}).` : '.'));
    }
  }

  const reviewers = new Set(rows.map((v) => v.by_email)).size;
  const whenLine = [el('strong', '', s.window ? `The last ${s.window} days` : 'The whole review so far'),
    ` · ${plural(rows.length, 'verdict')} from ${plural(reviewers, 'reviewer')}`];

  const sayingBits = [];
  if (totals.none && totals.total) {
    sayingBits.push(`${fmt(totals.none)} have never been looked at, which is a different thing from having been looked at and passed.`);
  }
  if (failed.length) {
    // One sentence however many failed: six copies of the same advice is
    // what the first draft of this said when the reader was down.
    const names = failed.map((f) => f.kind.many);
    const list = names.length > 1 ? `${names.slice(0, -1).join(', ')} and ${names.at(-1)}` : names[0];
    sayingBits.push(`The ${list} could not be read (${failed[0].error}), so they are left out of every count. Reload the page; if it stays, the package reader is down.`);
  }

  verdict($('rv-verdict'), {
    when: whenLine,
    headline,
    headlineId: 'rv-headline',
    pill: !rows.length ? null
      : !open.length ? { tone: 'ok', text: 'Nothing waiting on work' }
      : oldestDays > 7 ? { tone: 'bad', text: `Oldest ask ${plural(oldestDays, 'day')}` }
      : { tone: 'warn', text: `${fmt(open.length)} open` },
    pace: pace.join(' '),
    ledger: s.kind === 'module' || !totals.total ? [] : STANDINGS.map((st) => ({
      label: st.label, value: totals[st.key], swatch: st.fill,
      title: `${fmt(totals[st.key])} of ${fmt(totals.total)} ${noun}`,
    })),
    saying: sayingBits.join(' '),
  });

  // Next: the oldest unanswered ask, named, or where the unreviewed start.
  if (oldest) {
    const a = state.index.get(artefactKey(oldest.target_kind, oldest.target_id));
    const link = el('a', 'sh-link', a?.name ?? oldest.target_id);
    link.href = viewerHref(oldest.target_kind, oldest.target_id, a?.nodeId);
    const go = el('a', 'sh-link', 'Respond in Asked for work');
    go.href = '#asked';
    next($('rv-next'), [
      `Answer ${firstName(who(oldest))}'s "${VERDICT_LABEL[oldest.verdict] ?? oldest.verdict}" on `, link,
      `, open ${oldestDays === 0 ? 'since today' : plural(oldestDays, 'day')}. `, go, '.',
    ]);
  } else if (!totals.total && !failed.length) {
    next($('rv-next'), 'Nothing matches the filter. Show everything, above, to see the whole review.');
  } else if (totals.none) {
    const go = el('a', 'sh-link', 'Every artefact');
    go.href = '#artefacts';
    next($('rv-next'), [`Nothing is waiting on work. ${fmt(totals.none)} ${noun} have no verdict yet; `, go, ' lists them first.']);
  } else {
    next($('rv-next'), null);
  }

  drawCoverageFigure(view);
  drawCoverageNumbers(view);
}

/**
 * The bold thing: one bar per kind, each the standing of every artefact of
 * that kind. Filtered to one kind, it breaks that kind down by its group
 * (tables by module, wireframes by platform), because one bar alone answers
 * nothing a sentence did not.
 */
function coverageRows(view) {
  const { s, artefacts, tally } = view;
  if (!s.kind) {
    return KINDS.map((k) => {
      const pop = state.populations.get(k.key);
      return {
        label: k.label, kind: k.key, error: pop?.error ?? '',
        ...tally(artefacts.filter((a) => a.kind === k.key)),
      };
    });
  }
  const groups = new Map();
  for (const a of artefacts) {
    const g = a.group || 'no group';
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g).push(a);
  }
  const sorted = [...groups].sort((a, b) => b[1].length - a[1].length);
  const TOP = 10;
  const out = sorted.slice(0, TOP).map(([g, list]) => ({ label: g, ...tally(list) }));
  const rest = sorted.slice(TOP);
  if (rest.length) {
    out.push({ label: `${plural(rest.length, 'other')}`, ...tally(rest.flatMap(([, list]) => list)) });
  }
  return out;
}

function drawCoverageFigure(view) {
  const { s } = view;
  const kind = s.kind ? kindOf(s.kind) : null;
  const host = $('rv-cov');
  host.replaceChildren();
  // Nothing to draw is said by the headline; six empty bars would only say
  // it again, in grey.
  $('rv-figure').hidden = s.kind === 'module' || (!view.totals.total && !view.failed.length);
  if ($('rv-figure').hidden) return;
  $('rv-figure-caption').textContent = kind
    ? `${kind.label} by ${kind.group}, largest first`
    : 'Coverage by kind: every artefact, in the standing its verdicts give it';

  for (const r of coverageRows(view)) {
    const row = el('div', 'rv-cov-row');
    let label;
    if (r.kind) {
      // The label is the way in: pressing it filters the page to that kind.
      label = el('button', 'rv-cov-label', r.label);
      label.type = 'button';
      label.title = `Show only ${kindOf(r.kind).many}`;
      label.onclick = () => state.scope.set({ kind: r.kind });
    } else {
      label = el('span', 'rv-cov-label', r.label);
      label.title = r.label;
    }
    row.append(label);
    if (r.error) {
      row.append(el('span', 'rv-cov-failed', 'could not be read'), el('span', 'rv-cov-count', ''));
    } else {
      row.append(stack(STANDINGS.map((st) => ({ kind: st.fill, value: r[st.key], label: st.label })), true));
      const count = el('span', 'rv-cov-count', `${fmt(r.total - r.none)} of ${fmt(r.total)}`);
      count.title = `${fmt(r.total - r.none)} of ${fmt(r.total)} have a verdict`;
      row.append(count);
    }
    host.append(row);
  }
  $('rv-cov-legend').replaceChildren(legend(STANDINGS.map((st) => ({ kind: st.fill, label: st.label }))));
}

/** The chart's twin, in the open: every figure the bars draw. */
function drawCoverageNumbers(view) {
  const { s, gone } = view;
  const kind = s.kind ? kindOf(s.kind) : null;
  const host = $('rv-numbers');
  host.replaceChildren();
  if (s.kind === 'module') {
    $('rv-numbers-note').textContent = 'Modules have no list in the package to count against. Their verdicts are under Every response.';
    return;
  }
  if (!view.totals.total && !view.failed.length) {
    $('rv-numbers-note').textContent = 'Nothing in the package matches this filter, so there is nothing to count. Show everything, above, to see the whole package.';
    return;
  }
  const pct = (r) => (r.total ? Math.round(((r.total - r.none) / r.total) * 100) : 0);
  const rows = coverageRows(view);
  const total = view.totals;
  host.append(table({
    columns: [
      { key: 'label', label: kind ? kind.group[0].toUpperCase() + kind.group.slice(1) : 'Kind', sort: (r) => r.label },
      { key: 'total', label: 'Artefacts', num: true, sort: (r) => r.total },
      ...STANDINGS.map((st) => ({ key: st.key, label: st.label, num: true, sort: (r) => r[st.key] })),
      { key: 'pct', label: 'Have a verdict', num: true, sort: pct, render: (r) => (r.error ? 'could not be read' : `${pct(r)}%`) },
    ],
    rows: [...rows, { label: 'All of them', ...total }],
    empty: 'Nothing in the package matches this filter. Show everything to see the whole package.',
  }));
  const notes = [
    'An artefact is open while any ask for work on it is unanswered, fixed once every ask has been answered (built, wired, answered or accepted), and approved when its current verdicts all approve.',
  ];
  if (gone.size) {
    notes.push(`${plural(gone.size, 'artefact')} with verdicts ${gone.size === 1 ? 'is' : 'are'} no longer in the package; ${gone.size === 1 ? 'it is' : 'they are'} in the lists, not in these counts.`);
  }
  $('rv-numbers-note').textContent = notes.join(' ');
}

// ── a paged, sortable table over the whole list ─────────────────────

/**
 * Page-local, beside sheet.js's `table()`, because these lists run to
 * thousands of rows. `table()` sorts the rows it is given; here only a page of
 * them is drawn, and a sort that reordered page one alone would put the
 * largest of fifty at the top and call it the largest. This sorts the whole
 * list, then draws a page of it, and "Show more" draws the next.
 */
function paged(host, o) {
  const { id, columns, rows, empty, page = 50, rowClass, caption } = o;
  host.replaceChildren();
  const sort = state.sorts[id];
  let list = rows;
  const col = sort && columns.find((c) => c.key === sort.key);
  if (col?.sort) {
    list = [...rows].sort((a, b) => {
      const x = col.sort(a), y = col.sort(b);
      return (x > y ? 1 : x < y ? -1 : 0) * sort.dir;
    });
  }
  const shown = Math.min(list.length, state.pages[id] ?? page);

  const wrap = el('div', 'sh-table-wrap');
  const t = el('table', `sh-table ${o.className ?? ''}`.trim());
  if (caption) t.append(el('caption', 'sh-sr', caption));
  const hr = el('tr');
  for (const c of columns) {
    const th = el('th', c.num ? 'is-num' : '');
    th.scope = 'col';
    if (c.sort) {
      const b = el('button', 'sh-sort', c.label);
      b.type = 'button';
      b.onclick = () => {
        state.sorts[id] = sort?.key === c.key ? { key: c.key, dir: -sort.dir } : { key: c.key, dir: c.num ? -1 : 1 };
        paged(host, o);
        host.querySelector(`th[aria-sort] .sh-sort`)?.focus();
      };
      th.append(b);
      if (sort?.key === c.key) th.setAttribute('aria-sort', sort.dir > 0 ? 'ascending' : 'descending');
    } else th.textContent = c.label;
    hr.append(th);
  }
  const thead = el('thead');
  thead.append(hr);
  const tbody = el('tbody');
  t.append(thead, tbody);
  wrap.append(t);
  host.append(wrap);

  if (!list.length) {
    const tr = el('tr');
    const td = el('td', 'sh-empty', empty);
    td.colSpan = columns.length;
    tr.append(td);
    tbody.append(tr);
    return;
  }
  for (const row of list.slice(0, shown)) {
    const tr = el('tr', rowClass ? rowClass(row) : '');
    columns.forEach((c, i) => {
      const cell = el(i === 0 ? 'th' : 'td', [c.num ? 'is-num' : '', c.nowrap ? 'is-nowrap' : '', c.cls ?? ''].filter(Boolean).join(' '));
      if (i === 0) cell.scope = 'row';
      const v = c.render ? c.render(row) : row[c.key];
      if (v instanceof Node) cell.append(v);
      else cell.textContent = typeof v === 'number' ? fmt(v) : (v ?? '');
      tr.append(cell);
    });
    tbody.append(tr);
  }
  const left = list.length - shown;
  if (left > 0) {
    const more = el('button', 'chip sh-more', `Show ${fmt(Math.min(page, left))} more (${fmt(left)} not shown)`);
    more.type = 'button';
    more.onclick = () => {
      state.pages[id] = shown + page;
      paged(host, o);
      // Keep the reader where they were: on the first of the new rows.
      host.querySelectorAll('tbody tr')[shown]?.querySelector('a, button')?.focus();
    };
    host.append(more);
  }
}

// ── shared cells ────────────────────────────────────────────────────

/** The second half of an empty state, when the filter is why it is empty. */
const widen = (view) => (['kind', 'side', 'person', 'window', 'q'].some((k) => view.s[k])
  ? ' Show everything, above, to widen it.' : '');

function artefactCell(kind, id, { detail = true, withKind = false } = {}) {
  const a = state.index.get(artefactKey(kind, id));
  const box = el('span', 'rv-art');
  const link = el('a', 'sh-link rv-art-link', a?.name ?? id);
  link.href = viewerHref(kind, id, a?.nodeId);
  link.title = 'Open it in the viewer, where verdicts are recorded';
  box.append(link);
  if (withKind) box.append(el('span', 'rv-detail', kindOf(kind)?.one ?? kind));
  if (detail && a?.detail) box.append(el('span', 'rv-detail', a.detail));
  if (!a && state.populations.get(kind) && !state.populations.get(kind).error) {
    box.append(el('span', 'rv-detail', 'no longer in the package'));
  }
  return box;
}

function reviewerCell(v) {
  const box = el('span', 'rv-who');
  box.append(personLink(who(v)));
  if (isClientRow(v)) box.append(el('span', 'sh-side', 'client'));
  return box;
}

/** A verdict's word, coloured by where it stands now rather than what it was. */
function verdictBadge(v) {
  const label = VERDICT_LABEL[v.verdict] ?? v.verdict;
  if (!auth.asksForWork(v.verdict)) return badge('done', label);
  // Withdrawn by its own author's later verdict: still what was said, but no
  // longer anybody's work, so it does not wear the colour of open work.
  if (state.view?.withdrawn.has(v.id)) return badge('fresh', label);
  if (auth.isSettled(v)) {
    const b = badge('qa', `${label}, fixed`);
    b.title = `Answered: ${RESPONSE_LABEL[v.done_response] ?? 'done'}`;
    return b;
  }
  return badge('stalled', label);
}

function noteCell(v) {
  return v.note ? auth.renderNote(v.note) : el('span', 'sh-quiet', 'no reason given');
}

const whenCell = (iso) => {
  const s = el('span', 'is-nowrap', ago(iso));
  s.title = new Date(iso).toLocaleString('en-GB');
  return s;
};

const failLine = (text) => { $('rv-error').textContent = text; $('rv-error').hidden = !text; };
const say = (text) => { $('rv-asof').textContent = text; };

/** After any action on a row: the store changed, so every count re-derives. */
function changed(what) {
  state.verdicts = state.verdicts.filter((v) => !v.discarded);
  failLine('');
  say(`${what}: done.`);
  redraw();
}
const actionOptions = (extra = {}) => ({ me: state.me, done: changed, fail: failLine, ...extra });

// ── asked for work ──────────────────────────────────────────────────

function drawAsked(view) {
  const { open } = view;
  const navCount = $('rv-nav-asked');
  navCount.textContent = open.length ? fmt(open.length) : '';
  navCount.hidden = !open.length;
  navCount.setAttribute('aria-label', `${plural(open.length, 'open ask')}`);

  const mayWrite = state.me && !auth.isClient(state.me);
  $('rv-asked-note').textContent = open.length
    ? `Every ask for work nobody has answered, oldest first. ${mayWrite
      ? 'Respond says how it was answered; it then counts as fixed until somebody sends it back.'
      : 'The team answers these; a client account can read them.'}`
    : '';
  paged($('rv-asked'), {
    id: 'asked',
    caption: 'Open asks for work, oldest first',
    columns: [
      { key: 'age', label: 'Waiting', num: true, sort: (v) => -Date.parse(v.at),
        render: (v) => { const d = daysSince(v.at); return d === 0 ? 'today' : plural(d, 'day'); } },
      { key: 'verdict', label: 'Asked', render: (v) => {
        const box = el('span', 'rv-asked-what');
        box.append(verdictBadge(v));
        if (v.sent_back_at) box.append(el('span', 'rv-detail', `sent back: ${v.sent_back_note || 'no reason'}`));
        return box;
      } },
      { key: 'artefact', label: 'Artefact', sort: (v) => v.target_id, render: (v) => artefactCell(v.target_kind, v.target_id) },
      { key: 'kind', label: 'Kind', sort: (v) => kindLabel(v.target_kind), render: (v) => kindLabel(v.target_kind) },
      { key: 'tag', label: 'Lands on', sort: (v) => v.tag ?? '', render: (v) => el('span', 'sh-side', TAG_LABEL[v.tag] ?? 'not said') },
      { key: 'note', label: 'Why', cls: 'rv-note', render: noteCell },
      { key: 'by', label: 'Reviewer', sort: who, render: reviewerCell },
      ...(mayWrite ? [{ key: 'act', label: 'Answer', render: (v) => statusCell(v, actionOptions({ compact: true })) }] : []),
    ],
    rows: open,
    rowClass: () => 'rv-row',
    empty: view.rows.some((v) => auth.asksForWork(v.verdict))
      ? `Every ask for work in this selection has been answered; Every response has the answered ones.${widen(view)}`
      : `Nobody has asked for work in this selection.${widen(view)}`,
  });
}

// ── disagreement ────────────────────────────────────────────────────

function drawDisagreement(view) {
  const { contested } = view;
  $('rv-dis-note').textContent = contested.length
    ? `${plural(contested.length, 'artefact')} where two or more reviewers' latest verdicts differ, newest first. One person changing their own mind is not counted here.`
    : '';
  paged($('rv-dis'), {
    id: 'dis',
    caption: 'Artefacts where reviewers disagree',
    columns: [
      { key: 'artefact', label: 'Artefact', sort: (c) => c.key, render: (c) => {
        const [kind, ...rest] = c.key.split(' ');
        return artefactCell(kind, rest.join(' '));
      } },
      { key: 'kind', label: 'Kind', render: (c) => kindLabel(c.key.split(' ')[0]) },
      { key: 'views', label: 'Who said what', render: (c) => {
        const list = el('ul', 'rv-views');
        for (const v of [...c.views].sort((a, b) => who(a).localeCompare(who(b)))) {
          const li = el('li');
          li.append(verdictBadge(v), ' ', personLink(who(v)));
          if (isClientRow(v)) li.append(' ', el('span', 'sh-side', 'client'));
          if (v.note) li.title = v.note;
          list.append(li);
        }
        return list;
      } },
      { key: 'at', label: 'Last said', num: true, sort: (c) => c.at, render: (c) => whenCell(new Date(c.at).toISOString()) },
    ],
    rows: contested,
    rowClass: () => 'rv-row',
    empty: `Nobody disagrees in this selection: wherever two people looked at the same thing, they said the same.${widen(view)}`,
  });
}

// ── reviewers ───────────────────────────────────────────────────────

const median = (xs) => {
  if (!xs.length) return NaN;
  const s = [...xs].sort((a, b) => a - b);
  const mid = s.length >> 1;
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
};

/** "3 minutes", "2 days": a duration a person can hold in their head. */
function human(ms) {
  if (!Number.isFinite(ms)) return '—';
  const m = Math.round(ms / 60000);
  if (m < 2) return 'under 2 minutes';
  if (m < 90) return `${m} minutes`;
  const h = Math.round(m / 60);
  return h < 48 ? `${h} hours` : `${Math.round(h / 24)} days`;
}

function drawReviewers(view) {
  const { rows, s } = view;
  const by = new Map();
  for (const v of rows) {
    if (!by.has(v.by_email)) by.set(v.by_email, []);
    by.get(v.by_email).push(v);
  }
  const stats = [...by].map(([email, list]) => {
    const times = list.map((v) => Date.parse(v.at)).sort((a, b) => a - b);
    // Gaps between consecutive verdicts, as a rough sense of rhythm. Gaps over
    // a day are dropped: they are "went home", not "took a while".
    const gaps = times.slice(1).map((t, i) => t - times[i]).filter((g) => g < DAY);
    const notes = list.map((v) => (v.note ?? '').trim()).filter(Boolean);
    const asked = list.filter((v) => auth.asksForWork(v.verdict)).length;
    return {
      email, name: who(list[0]), role: list[0].by_role,
      total: list.length, approved: list.length - asked, asked,
      rejected: list.filter((v) => v.verdict === 'rejected').length,
      artefacts: new Set(list.map((v) => artefactKey(v.target_kind, v.target_id))).size,
      noteRate: notes.length / list.length,
      cadence: gaps.length ? median(gaps) : NaN,
      last: times[times.length - 1],
    };
  }).sort((a, b) => b.total - a.total);

  const accounts = state.accounts.length;
  $('rv-people-note').textContent = stats.length
    ? `${plural(stats.length, 'person has', 'people have')} given a verdict in this selection, of ${plural(accounts, 'account')}. A name opens that person on Tasks; "Only theirs" filters this page to them.`
    : '';

  paged($('rv-people'), {
    id: 'people',
    caption: 'Reviewers, busiest first',
    page: 30,
    columns: [
      { key: 'name', label: 'Reviewer', sort: (r) => r.name, render: (r) => {
        const box = el('span', 'rv-who rv-who-stack');
        box.append(personLink(r.name));
        box.append(el('span', 'rv-detail', auth.roleLabel(r.role)));
        return box;
      } },
      { key: 'total', label: 'Verdicts', num: true, sort: (r) => r.total },
      { key: 'mix', label: 'Approved or asked for work', render: (r) => {
        const box = el('span', 'rv-mix');
        box.append(stack([
          { kind: 'done', value: r.approved, label: 'Approved' },
          { kind: 'stalled', value: r.asked, label: 'Asked for work' },
        ]));
        box.append(el('span', 'rv-detail', `${fmt(r.approved)} approved, ${fmt(r.asked)} asked${r.rejected ? ` (${fmt(r.rejected)} rejected)` : ''}`));
        return box;
      } },
      { key: 'artefacts', label: 'Artefacts', num: true, sort: (r) => r.artefacts },
      { key: 'notes', label: 'Gave a reason', num: true, sort: (r) => r.noteRate, render: (r) => `${Math.round(r.noteRate * 100)}%` },
      { key: 'gap', label: 'Typical gap', num: true, sort: (r) => (Number.isFinite(r.cadence) ? r.cadence : Infinity), render: (r) => human(r.cadence) },
      { key: 'last', label: 'Last verdict', num: true, sort: (r) => r.last, render: (r) => whenCell(new Date(r.last).toISOString()) },
      { key: 'only', label: 'Filter', render: (r) => {
        const on = s.person === r.email;
        const b = el('button', 'chip rv-only', on ? 'Everyone' : 'Only theirs');
        b.type = 'button';
        b.setAttribute('aria-pressed', String(on));
        b.title = on ? 'Show every reviewer again' : `Filter the whole page to ${r.name}`;
        b.onclick = () => state.scope.set({ person: on ? '' : r.email });
        return b;
      } },
    ],
    rows: stats,
    rowClass: () => 'rv-row',
    empty: 'Nobody has given a verdict in this selection. Widen the window, or Show everything.',
  });

  // The two warnings this page has always given, now as sentences under the
  // table rather than coloured cells: a reviewer who never dissents may not be
  // reviewing, and a verdict with no reason gets rediscovered the hard way.
  const warn = $('rv-people-warn');
  warn.replaceChildren();
  const rubber = stats.filter((r) => r.total >= 5 && r.asked === 0);
  const quiet = stats.filter((r) => r.total >= 5 && r.noteRate < 0.34);
  const names = (list) => list.map((r) => r.name).join(', ');
  if (rubber.length) {
    warn.append(el('p', 'rv-warn', `${names(rubber)} ${rubber.length === 1 ? 'has' : 'have'} approved everything they touched. Worth a look: a reviewer who never asks for anything may not be reviewing.`));
  }
  if (quiet.length) {
    warn.append(el('p', 'rv-warn', `${names(quiet)} gave a reason on under a third of their verdicts. A verdict with no reason gets rediscovered the hard way.`));
  }

  drawPace(view);
}

/**
 * Verdicts per day, stacked approved and asked for work.
 *
 * Drawn at the width it is shown at, with a viewBox the same size, so the
 * text is the size it says. The old chart stretched a 940-wide drawing with
 * preserveAspectRatio="none", which squashed or smeared its labels at every
 * width but one.
 */
function drawPace(view) {
  const host = $('rv-pace');
  const { rows, s } = view;
  host.replaceChildren();
  $('rv-pace-legend').replaceChildren();
  $('rv-pace-table').replaceChildren();
  if (!rows.length) {
    $('rv-pace-note').textContent = 'No verdicts in this selection, so there is no pace to draw.';
    return;
  }
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const firstAt = Math.min(...rows.map((v) => Date.parse(v.at)));
  const start = new Date(s.window ? today.getTime() - (Number(s.window) - 1) * DAY : firstAt);
  start.setHours(0, 0, 0, 0);
  const days = Math.round((today - start) / DAY) + 1;
  // A day per bar up to four months; past that, weeks, or the bars are
  // hairlines nobody can point at.
  const size = days > 120 ? 7 : 1;
  const n = Math.ceil(days / size);
  const buckets = Array.from({ length: n }, (_, i) => ({
    from: new Date(start.getTime() + i * size * DAY), approved: 0, asked: 0,
  }));
  for (const v of rows) {
    const i = Math.floor((Date.parse(v.at) - start.getTime()) / (size * DAY));
    if (!buckets[i]) continue;
    if (auth.asksForWork(v.verdict)) buckets[i].asked++;
    else buckets[i].approved++;
  }
  const peak = Math.max(1, ...buckets.map((b) => b.approved + b.asked));
  const step = peak <= 5 ? 1 : 10 ** Math.floor(Math.log10(peak / 2));
  const top = Math.ceil(peak / step / 2) * step * 2 || 2;

  const W = Math.max(280, host.clientWidth || 720);
  const H = 190;
  const L = 34, R = 8, T = 10, B = 26;
  const plotW = W - L - R, plotH = H - T - B;
  const bw = plotW / n;
  const y = (value) => T + plotH - (value / top) * plotH;
  const day = (d) => d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
  const unit = size === 1 ? 'day' : 'week';

  const chart = svg('svg', {
    width: W, height: H, viewBox: `0 0 ${W} ${H}`, role: 'img',
    'aria-label': `Verdicts per ${unit}, ${day(start)} to ${day(today)}; the busiest ${unit} had ${peak}. The numbers are in the table below.`,
  });
  for (const value of [0, top / 2, top]) {
    chart.append(svg('line', { class: 'sh-grid-line', x1: L, x2: W - R, y1: y(value), y2: y(value) }));
    chart.append(svg('text', { class: 'sh-tick', x: L - 6, y: y(value) + 4, 'text-anchor': 'end' }, fmt(value)));
  }
  buckets.forEach((b, i) => {
    const x = L + i * bw + Math.min(2, bw * 0.12);
    const w = Math.max(1, bw - Math.min(4, bw * 0.24));
    const g = svg('g');
    g.append(svg('title', {}, `${size === 1 ? day(b.from) : `Week of ${day(b.from)}`}: ${b.approved} approved, ${b.asked} asked for work`));
    if (b.approved) g.append(svg('rect', { class: 'rv-bar-done', x, width: w, y: y(b.approved), height: plotH + T - y(b.approved) }));
    if (b.asked) g.append(svg('rect', { class: 'rv-bar-asked', x, width: w, y: y(b.approved + b.asked), height: y(b.approved) - y(b.approved + b.asked) }));
    chart.append(g);
  });
  const ticks = n > 6 ? [0, Math.floor((n - 1) / 2), n - 1] : n > 1 ? [0, n - 1] : [0];
  for (const i of ticks) {
    const anchor = i === 0 ? 'start' : i === n - 1 ? 'end' : 'middle';
    const x = anchor === 'start' ? L : anchor === 'end' ? W - R : L + i * bw + bw / 2;
    chart.append(svg('text', { class: 'sh-tick', x, y: H - 8, 'text-anchor': anchor }, day(buckets[i].from)));
  }
  host.append(chart);
  $('rv-pace-legend').append(legend([
    { kind: 'done', label: 'Approved' },
    { kind: 'stalled', label: 'Asked for work (needs work or rejected)' },
  ]));

  const busiest = buckets.reduce((a, b) => (a.approved + a.asked >= b.approved + b.asked ? a : b));
  $('rv-pace-note').textContent =
    `${plural(rows.length, 'verdict')} over ${plural(days, 'day')}, about ${(rows.length / days).toFixed(1)} a day. ` +
    `The busiest ${unit} was ${size === 1 ? day(busiest.from) : `the week of ${day(busiest.from)}`}, with ${fmt(busiest.approved + busiest.asked)}.`;

  $('rv-pace-table').append(table({
    caption: `Verdicts per ${unit}`,
    columns: [
      { key: 'from', label: size === 1 ? 'Day' : 'Week of', render: (b) => day(b.from) },
      { key: 'approved', label: 'Approved', num: true },
      { key: 'asked', label: 'Asked for work', num: true },
      { key: 'total', label: 'All', num: true, render: (b) => fmt(b.approved + b.asked) },
    ],
    rows: [...buckets].reverse(),
  }));
}

// ── named you ───────────────────────────────────────────────────────

function drawNamed(view) {
  const all = state.mentions;
  const items = view.mentions;
  const unseen = all.filter((m) => !m.seen_at).length;
  const navCount = $('rv-nav-named');
  navCount.textContent = unseen ? fmt(unseen) : '';
  navCount.hidden = !unseen;
  navCount.setAttribute('aria-label', `${fmt(unseen)} unread`);
  $('rv-named-seen').hidden = !unseen;

  if (state.mentionsError) {
    $('rv-named-note').textContent = `The notes that name you could not be read (${state.mentionsError}). Reload the page to try again.`;
  } else if (!all.length) {
    $('rv-named-note').textContent = '';
  } else {
    $('rv-named-note').textContent = `${plural(all.length, 'note')} named you, ${unseen ? `${fmt(unseen)} unread` : 'all read'}` +
      `${items.length !== all.length ? `; ${fmt(items.length)} in this selection` : ''}. Newest first.`;
  }

  // Every one, a page at a time. The old panel stopped at twelve with no way
  // to the thirteenth.
  paged($('rv-named'), {
    id: 'named',
    caption: 'Notes that named you, newest first',
    page: 20,
    columns: [
      { key: 'at', label: 'When', num: true, sort: (m) => Date.parse(m.at), render: (m) => {
        const box = el('span', 'rv-when');
        if (!m.seen_at) box.append(el('span', 'rv-unread', 'unread'));
        box.append(whenCell(m.at));
        return box;
      } },
      { key: 'by', label: 'Who', sort: who, render: reviewerCell },
      { key: 'verdict', label: 'Said', render: (m) => badge(auth.asksForWork(m.verdict) ? 'stalled' : 'done', VERDICT_LABEL[m.verdict] ?? m.verdict) },
      { key: 'artefact', label: 'About', sort: (m) => m.target_id, render: (m) => artefactCell(m.target_kind, m.target_id, { detail: false }) },
      { key: 'note', label: 'Note', cls: 'rv-note', render: (m) => auth.renderNote(m.note) },
    ],
    rows: items,
    rowClass: (m) => `rv-row${m.seen_at ? '' : ' is-unread'}`,
    empty: all.length
      ? 'None of the notes that name you are in this selection. Show everything to see them all.'
      : 'Nobody has named you in a note yet. When somebody writes @ and your name in a verdict, it lands here and on the bell.',
  });
}

async function markAllRead() {
  const button = $('rv-named-seen');
  button.disabled = true;
  try {
    await auth.markMentionsSeen();
    const now = new Date().toISOString();
    for (const m of state.mentions) m.seen_at ??= now;
    say('Every note that named you is marked read.');
    redraw();
  } catch (error) {
    failLine(`Marking them read did not go through: ${error.message}. Try again.`);
  } finally {
    button.disabled = false;
  }
}

// ── every artefact ──────────────────────────────────────────────────

const STANDING_BADGE = {
  none: () => badge('fresh', 'Not reviewed'),
  approved: () => badge('done', 'Approved'),
  open: (a) => badge('stalled', VERDICT_LABEL[a.open[0]?.verdict] ?? 'Asked for work'),
  fixed: (a) => {
    const ask = a.current.find((v) => auth.asksForWork(v.verdict));
    const b = badge('qa', 'Fixed');
    b.title = `${VERDICT_LABEL[ask?.verdict] ?? 'Asked for work'}, answered: ${RESPONSE_LABEL[ask?.done_response] ?? 'done'}`;
    return b;
  },
};
const STANDING_ORDER = { none: 0, open: 1, fixed: 2, approved: 3 };
const KIND_ORDER = Object.fromEntries(KINDS.map((k, i) => [k.key, i]));

function drawArtefacts(view) {
  const { s, artefacts } = view;
  const kind = s.kind ? kindOf(s.kind) : null;
  const only = state.local.only;
  const list = (only ? artefacts.filter((a) => a.standing === 'none') : artefacts)
    // Unreviewed first, because the list exists to find them. Within that,
    // the order the viewer shows them in, so two people reading the same list
    // are looking at the same thing.
    .sort((a, b) => STANDING_ORDER[a.standing] - STANDING_ORDER[b.standing]
      || KIND_ORDER[a.kind] - KIND_ORDER[b.kind] || a.name.localeCompare(b.name));
  const noun = kind ? kind.many : 'artefacts';
  $('rv-art-note').textContent = s.kind === 'module'
    ? 'Modules have no list in the package. Their verdicts are under Every response.'
    : `${fmt(list.length)} of ${fmt(artefacts.length)} ${noun}${only ? ', only those with no verdict' : ''}; never reviewed first. A name opens it in the viewer, where the verdict is recorded.`;

  paged($('rv-art'), {
    id: 'art',
    caption: `Every ${kind ? kind.one : 'artefact'} and where it stands`,
    columns: [
      { key: 'standing', label: 'Standing', render: (a) => STANDING_BADGE[a.standing](a) },
      { key: 'name', label: kind ? kind.label : 'Artefact', render: (a) => artefactCell(a.kind, a.id) },
      ...(kind ? [] : [{ key: 'kind', label: 'Kind', render: (a) => kindOf(a.kind).label }]),
      { key: 'group', label: kind ? kind.group[0].toUpperCase() + kind.group.slice(1) : 'Group', render: (a) => a.group ?? '' },
      { key: 'last', label: 'Latest verdict', render: (a) => {
        if (!a.latest) return el('span', 'sh-quiet', 'none');
        const box = el('span', 'rv-who rv-who-stack');
        box.append(reviewerCell(a.latest), el('span', 'rv-detail', ago(a.latest.at)));
        if (a.latest.note) box.title = a.latest.note;
        return box;
      } },
    ],
    rows: list,
    rowClass: (a) => `rv-row rv-art-row is-${a.standing}`,
    empty: only && artefacts.length
      ? `Every one of these ${noun} has a verdict. That is the whole population under this filter, not a page of it.`
      : 'Nothing in the package matches this filter. Show everything to see the whole package.',
  });
}

// ── every response ──────────────────────────────────────────────────

const STATUS_OPTIONS = [
  ['open', 'Open'], ['sent-back', 'Sent back'], ['answered', 'Answered'],
  ['withdrawn', 'Replaced by a later verdict'], ['none', 'Nothing to answer'],
];

function drawLogFilter(view) {
  const host = $('rv-log-filter');
  host.replaceChildren();
  const layers = new Set(state.verdicts.map((v) => v.layer).filter(Boolean));
  const fields = [
    ['said', 'Verdict', 'Any verdict', auth.VERDICTS],
    ['status', 'Status', 'Any status', STATUS_OPTIONS],
    ['lands', 'Lands on', 'Either side', auth.TAGS],
    ['layer', 'Reviewed from', 'Any layer', Object.entries(LAYER_LABEL).filter(([k]) => layers.has(k))],
  ];
  for (const [key, label, all, options] of fields) {
    const wrap = el('label', 'sh-field');
    const select = el('select', 'scope-select');
    select.append(new Option(all, ''));
    for (const [value, text] of options) select.append(new Option(text, value));
    select.value = state.local[key];
    if (select.value !== state.local[key]) state.local[key] = '';
    select.onchange = () => {
      state.local[key] = select.value;
      setParams({ [key]: select.value });
      delete state.pages.log;
      drawLog(view);
    };
    wrap.append(el('span', '', label), select);
    host.append(wrap);
  }
  if (['said', 'status', 'lands', 'layer'].some((k) => state.local[k])) {
    const clear = el('button', 'chip sh-clear', 'Clear these four');
    clear.type = 'button';
    clear.onclick = () => {
      for (const k of ['said', 'status', 'lands', 'layer']) state.local[k] = '';
      setParams({ said: '', status: '', lands: '', layer: '' });
      drawLog(view);
    };
    host.append(clear);
  }
}

function logRows(view) {
  const l = state.local;
  return view.rows.filter((v) => {
    if (l.said && v.verdict !== l.said) return false;
    if (l.status && statusOf(v, view.withdrawn) !== l.status) return false;
    if (l.lands && (v.tag || '') !== l.lands) return false;
    if (l.layer && (v.layer || '') !== l.layer) return false;
    return true;
  });
}

function drawLog(view) {
  drawLogFilter(view);
  const rows = logRows(view);
  $('rv-log-note').textContent =
    `${fmt(rows.length)} of ${plural(state.verdicts.length, 'verdict')} ever given, newest first. Every verdict at the moment it was given: a revision is a new row, not an edit. Export CSV takes exactly these rows.`;
  $('rv-export').onclick = () => exportCsv(rows, {
    narrowed: rows.length !== state.verdicts.length,
  });
  $('rv-close-link').hidden = !auth.isAdmin(state.me);
  if (!state.sorts.log) state.sorts.log = { key: 'at', dir: -1 };

  paged($('rv-log'), {
    id: 'log',
    caption: 'Every verdict, newest first',
    page: 60,
    columns: [
      { key: 'at', label: 'When', num: true, sort: (v) => Date.parse(v.at) * 1e3 + (v.id % 1e3), render: (v) => whenCell(v.at) },
      { key: 'verdict', label: 'Verdict', sort: (v) => v.verdict, render: verdictBadge },
      // Whose review it was is said under the reviewer ("client"), and the
      // kind under the artefact: two columns fewer, so the status and its
      // actions stay on screen at a laptop's width.
      { key: 'artefact', label: 'Artefact', sort: (v) => v.target_id, render: (v) => artefactCell(v.target_kind, v.target_id, { detail: false, withKind: true }) },
      { key: 'tag', label: 'Lands on', sort: (v) => v.tag ?? '', render: (v) => el('span', 'sh-side', TAG_LABEL[v.tag] ?? 'not said') },
      { key: 'note', label: 'Why', cls: 'rv-note', sort: (v) => v.note ?? '', render: noteCell },
      { key: 'by', label: 'Reviewer', sort: who, render: reviewerCell },
      { key: 'status', label: 'Status', sort: (v) => statusOf(v, view.withdrawn), render: (v) => statusCell(v, actionOptions({ withdrawn: view.withdrawn })) },
    ],
    rows,
    rowClass: (v) => `rv-row${auth.isSettled(v) ? ' is-settled' : ''}`,
    empty: state.verdicts.length
      ? 'No verdict matches these filters. Clear these four, or Show everything above.'
      : 'Nobody has given a verdict yet. Open an artefact in the viewer and record one; it lands here.',
  });
}

// ── drawing ─────────────────────────────────────────────────────────

function redraw() {
  const view = derive();
  drawCoverage(view);
  drawAsked(view);
  drawDisagreement(view);
  drawReviewers(view);
  drawNamed(view);
  drawArtefacts(view);
  drawLog(view);
}

function drawLede() {
  const total = KINDS.reduce((n, k) => n + (state.populations.get(k.key)?.rows.length ?? 0), 0);
  const first = state.verdicts.length ? state.verdicts.reduce((a, b) => (a.at < b.at ? a : b)).at : null;
  $('rv-lede').textContent = `${fmt(total)} artefacts in the package, ${plural(state.verdicts.length, 'verdict')} given on them` +
    `${first ? ` since ${new Date(first).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })}` : ''}.`;
  say(`Read at ${new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}`);
}

(async () => {
  if (!(await auth.requireSignIn())) return hideLoader();
  state.me = auth.account();
  $('whoami').textContent = state.me ? `${state.me.name || state.me.email} · ${auth.roleLabel(state.me.role)}` : '';

  // All three at once: the package is the slow one (the journeys payload is
  // tens of megabytes), and the verdicts should not queue behind it.
  const [populations, verdicts, mentions] = await Promise.allSettled([
    loadPopulations(), auth.allVerdicts(), auth.myMentions(),
  ]);
  try {
    state.populations = populations.status === 'fulfilled' ? populations.value : new Map();
    for (const [kind, { rows }] of state.populations) {
      for (const a of rows) state.index.set(artefactKey(kind, a.id), a);
    }
    if (verdicts.status === 'fulfilled') {
      state.verdicts = verdicts.value.verdicts ?? [];
      state.accounts = verdicts.value.accounts ?? [];
    } else {
      failLine(`The verdicts could not be read: ${verdicts.reason?.message ?? verdicts.reason}. The counts below are the package only, as if nothing had been reviewed. Reload the page to try again.`);
    }
    if (mentions.status === 'fulfilled') state.mentions = mentions.value?.mentions ?? [];
    else state.mentionsError = mentions.reason?.message ?? 'no answer';

    resolvePersonParam();
    mountFilter();
    $('rv-only-open').checked = state.local.only;
    $('rv-only-open').onchange = (e) => {
      state.local.only = e.target.checked;
      setParams({ only: e.target.checked ? '1' : '' });
      delete state.pages.art;
      drawArtefacts(state.view);
    };
    $('rv-named-seen').onclick = markAllRead;
    drawLede();
    redraw();
  } finally {
    hideLoader();
  }

  mountPanels({
    nav: document.querySelector('#reviews .set-nav'),
    fallback: 'coverage',
    onShow: (name) => {
      state.section = name;
      // The pace chart is drawn at the width it is shown at, and a hidden
      // section has none.
      if (name === 'reviewers' && state.view) drawPace(state.view);
    },
  });
  let resizing;
  addEventListener('resize', () => {
    clearTimeout(resizing);
    resizing = setTimeout(() => { if (state.section === 'reviewers' && state.view) drawPace(state.view); }, 150);
  });
})();
