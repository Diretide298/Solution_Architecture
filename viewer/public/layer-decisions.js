/**
 * The Decisions layer.
 *
 * `docs/` is the one layer that is prose rather than machine-readable, and the
 * reason it is here at all: everything else can be checked mechanically, and
 * this is where the reasons live. One thing in it is executable — the
 * permission vectors — so the viewer runs them rather than listing them.
 */
import {
  $, el, state, escapeHtml, inlineMarkdown, renderBoxLegend, deliveryTip,
  hue, markdownBlock,
} from './core.js';
import { tip, tipFor } from './tips.js';
// The router. A layer may reach the router; the router may not reach into a
// layer's internals — it only calls the render function below.
import { setMode } from './app.js';

export function renderDecisions() {
  const body = $('decisions-body');
  const decisions = state.decisions;
  body.innerHTML = '';

  if (!decisions?.present) {
    body.append(el('p', 'pane-empty', 'No docs/ in this package.'));
    $('decisions-hint').textContent = '';
    return;
  }

  const s = decisions.stats;
  $('decisions-hint').textContent =
    `${s.adrs} ADRs · ${s.documents} documents · ${s.vectorsPassed}/${s.vectors} vectors pass · ` +
    `${s.artefactGaps} open artefact gaps`;

  const needle = state.decisionsFilter.trim().toLowerCase();
  const hit = (text) => !needle || String(text ?? '').toLowerCase().includes(needle);

  if (state.decisionsScope === 'permissions') return renderPermissionVectors(body, hit);
  if (state.decisionsScope === 'gaps') return renderArtefactGaps(body, hit);
  if (state.decisionsScope === 'registers') return renderRegisters(body, hit);
  return renderAdrs(body, hit);
}

function renderAdrs(body, hit) {
  const adrs = state.decisions.adrs.filter(
    (a) => hit(a.title) || hit(a.id) || hit(a.decision) || hit(a.closes)
  );
  body.append(el('div', 'journey-section-label', `${adrs.length} decisions`));

  for (const adr of adrs) {
    const card = el('div', 'adr-card');
    const head = el('div', 'adr-card-head');
    const number = el('span', 'adr-number', `ADR-${adr.id}`);
    deliveryTip(number, 'adrs', adr.id);
    head.append(number);
    const title = el('button', 'adr-title', adr.title);
    title.onclick = () => openDoc(adr.file);
    head.append(title);

    const verdict = el('span', `adr-status ${String(adr.verdict ?? '').toLowerCase()}`, adr.verdict ?? '—');
    if (adr.partlySuperseded) {
      verdict.classList.add('partial');
      tip(verdict, 'Accepted, and partly superseded',
        `**${adr.qualifier}** — which is the case that misleads: it reads as current in a list, and ` +
        `the part that was superseded is not current.`);
    } else {
      tip(verdict, adr.status ?? 'No status',
        adr.status
          ? 'The decision’s standing. Only Accepted is binding.'
          : '**This ADR states no status**, so whether it is binding cannot be told from the file.');
    }
    head.append(verdict);
    if (adr.date) head.append(el('span', 'adr-date', adr.date));
    card.append(head);

    if (adr.decision) {
      const text = el('div', 'adr-decision');
      text.innerHTML = inlineMarkdown(adr.decision);
      card.append(text);
    }

    const meta = el('div', 'adr-meta');
    for (const [label, value] of [
      ['closes', adr.closes], ['withdraws', adr.withdraws], ['supersedes', adr.supersedes],
    ]) {
      if (!value) continue;
      const chip = el('span', 'jchip');
      chip.append(el('span', null, label), el('b', null, value));
      meta.append(chip);
    }
    for (const target of adr.constrains) {
      const chip = el('span', 'adr-constrains', target);
      tip(chip, 'Constrains', `**${target}** is bound by this decision. Changing it needs this ADR revisited first.`);
      meta.append(chip);
    }
    if (adr.amended) {
      const chip = el('span', 'adr-amended', 'amended');
      tip(chip, 'Amended after acceptance',
        'The accepted date is not the date of what this ADR now says. Read the amendment before acting on the decision.');
      meta.append(chip);
    }
    if (meta.children.length) card.append(meta);
    body.append(card);
  }
}

function renderPermissionVectors(body, hit) {
  const spec = state.decisions.permissions;
  if (!spec) {
    body.append(el('p', 'pane-empty', 'No permission-vectors.json in this package.'));
    return;
  }

  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', 'Authorisation, executed'));
  const chips = el('div', 'journey-chips');
  const pass = el('span', `jchip ${spec.stats.failed ? 'warn' : 'ok'}`);
  pass.append(el('span', null, 'vectors'), el('b', null, `${spec.stats.passed} of ${spec.stats.total} pass`));
  chips.append(pass);
  if (spec.fixture) {
    const chip = el('span', 'jchip');
    chip.append(el('span', null, 'fixture'), el('b', null, spec.fixture));
    chips.append(chip);
  }
  head.append(chips);
  head.append(el('div', 'journey-trigger',
    spec.note ??
    'Each vector is a set of grants, a query and the verdict the platform must reach.'));
  head.append(el('div', 'journey-trigger',
    'The viewer resolves each one against the rule rather than listing it: a grant applies when its ' +
    'permission matches and its scope is an ancestor of the query; any applicable DENY wins, however ' +
    'specific the ALLOW; nothing bubbles upward.'));
  body.append(head);

  const rows = spec.vectors.filter((v) => hit(v.id) || hit(v.proves) || hit(v.query.permission));
  body.append(el('div', 'journey-section-label', `${rows.length} vectors`));

  for (const vector of rows) {
    const card = el('div', `vector-card${vector.pass ? '' : ' failed'}`);
    const head2 = el('div', 'vector-head');
    head2.append(el('span', 'vector-id', vector.id));
    head2.append(el('span', 'vector-proves', vector.proves));
    const mark = el('span', `vector-verdict ${vector.pass ? 'pass' : 'fail'}`,
      vector.pass ? vector.actual : `${vector.actual} ≠ ${vector.expect}`);
    tip(mark, vector.pass ? 'Resolves as specified' : 'Does not resolve as specified',
      vector.pass
        ? `The rule produces **${vector.actual}**, which is what the spec requires.`
        : `The spec requires **${vector.expect}** and the rule produces **${vector.actual}**. ` +
          `The file says a failing vector is a build failure.`);
    head2.append(mark);
    card.append(head2);

    const grants = el('div', 'vector-grants');
    if (!vector.grants.length) {
      const chip = el('span', 'vector-grant none', 'no grants');
      tip(chip, 'Nothing granted', 'The default-deny case. Absence of a grant is a denial, not an error.');
      grants.append(chip);
    }
    for (const grant of vector.grants) {
      const chip = el('span', `vector-grant ${grant.effect.toLowerCase()}`);
      chip.append(el('b', null, grant.effect));
      chip.append(el('span', null, grant.permission));
      chip.append(el('span', 'vector-scope', grant.scope));
      grants.append(chip);
    }
    card.append(grants);

    const query = el('div', 'vector-query');
    query.append(el('span', 'vector-label', 'asks'));
    query.append(el('b', null, vector.query.permission));
    query.append(el('span', 'vector-scope', vector.query.scope));
    card.append(query);
    body.append(card);
  }
}

function renderArtefactGaps(body, hit) {
  const gaps = state.decisions.gaps.filter((g) => hit(g.class) || hit(g.verdict));
  const s = state.decisions.stats;

  const head = el('div', 'journey-head');
  head.append(el('h2', 'journey-title', 'What the requirements demand and the package does not have'));
  const chips = el('div', 'journey-chips');
  for (const [label, value, cls] of [
    ['classes', s.artefactClasses, ''],
    ['open', s.artefactGaps, 'warn'],
    ['requirements behind them', s.requirementsUnserved, 'warn'],
  ]) {
    const chip = el('span', `jchip ${cls}`);
    chip.append(el('span', null, label), el('b', null, String(value)));
    chips.append(chip);
  }
  head.append(chips);
  head.append(el('div', 'journey-trigger',
    'The delivery’s own audit, not the viewer’s. Every other view here measures what is present; ' +
    'this is the only one that counts what is absent — and it is derived from the requirement text ' +
    'rather than from a checklist.'));
  body.append(head);

  body.append(el('div', 'journey-section-label', `${gaps.length} artefact classes`));
  const max = Math.max(1, ...gaps.map((g) => g.requirements));
  const table = el('div', 'routing-table');
  for (const gap of gaps) {
    const line = el('div', 'routing-row');
    const name = el('span', `gap-name ${gap.state}`, gap.class);
    const said = gap.verdict.replace(/^[✅🟡🔴]\s*/, '');
    tip(name, gap.class,
      gap.state === 'blocked'
        // Not a gap in the package. Somebody outside it owes an answer, and
        // saying which is the only thing that moves it.
        ? `**Blocked — waiting on ${said}**

Not ours to close.`
        : gap.state === 'covered' ? `Covered — ${said}` : `**${said}**`,
      gap.holding ? `holding: ${gap.holding}` : null);
    line.append(name);

    const bar = el('div', 'routing-bar');
    bar.style.width = `${(gap.requirements / max) * 100}%`;
    const seg = el('div', 'routing-seg', String(gap.requirements));
    seg.style.flexGrow = '1';
    seg.style.background = {
      missing: hue('error'),
      partial: hue('warning'),
      // blocked is not the same as absent: the work cannot start until a
      // workshop happens or the client answers, so colouring it red would put
      // somebody else's decision on our side of the ledger.
      blocked: hue('info'),
      covered: hue('ok'),
    }[gap.state] ?? hue('ok');
    bar.append(seg);
    line.append(bar);
    line.append(el('span', 'routing-total', gap.state));
    table.append(line);
  }
  body.append(table);

  const legend = el('div', 'inline-legend');
  body.append(legend);
  renderBoxLegend(legend,
    [[hue('error'), 'nothing behind it'], [hue('warning'), 'partial'],
     [hue('info'), 'blocked — waiting on someone else'], [hue('ok'), 'covered']],
    'bar length is the number of requirements that need an artefact of this class');
}

function renderRegisters(body, hit) {
  const docs = state.decisions.documents.filter(
    (d) => hit(d.title) || hit(d.lead) || hit(d.id)
  );
  const GROUPS = [
    ['register', 'Registers — living reference data'],
    ['handoff', 'Handoff — the build artefacts and the narratives beside them'],
    ['architecture', 'Architecture — how it is built'],
    ['active', 'Active — what is in flight'],
    ['guide', 'Guides'],
  ];

  for (const [group, label] of GROUPS) {
    const list = docs.filter((d) => d.group === group);
    if (!list.length) continue;
    body.append(el('div', 'journey-section-label', `${label} · ${list.length}`));
    const grid = el('div', 'doc-grid');
    for (const doc of list) {
      const card = el('button', 'doc-card');
      card.append(el('span', 'doc-title', doc.title));
      if (doc.lead) card.append(el('span', 'doc-lead', doc.lead));
      const meta = el('span', 'doc-meta');
      meta.append(el('span', null, doc.file));
      if (doc.rows) meta.append(el('b', null, `${doc.rows} rows`));
      card.append(meta);
      tip(card, doc.title, doc.lead || 'No lead paragraph.',
        `${doc.lines} lines · ${doc.tables.length} table${doc.tables.length === 1 ? '' : 's'}`);
      card.onclick = () => openDoc(doc.file);
      grid.append(card);
    }
    body.append(grid);
  }
}

/** Prose has no node in the graph, so it opens in the reader as source. */
export async function openDoc(file) {
  const view = $('view-reader');
  setMode('reader');
  $('reader-empty').hidden = true;
  $('reader-body').hidden = false;
  $('reader-head').innerHTML = '';
  $('reader-meta').innerHTML = '';
  $('reader-head').append(el('h1', 'reader-title', file.split('/').pop()));
  $('reader-meta').append(el('span', 'reader-file', file));
  const source = $('reader-source');
  source.textContent = 'Loading…';
  try {
    const text = await fetch(`/api/file?path=${encodeURIComponent(file)}`).then((r) => {
      if (!r.ok) throw new Error(String(r.status));
      return r.text();
    });
    source.innerHTML = '';
    const pre = el('pre', 'doc-source');
    pre.textContent = text;
    source.append(pre);
    if (view) view.scrollTop = 0;
  } catch {
    source.textContent = `Could not read ${file}`;
  }
}


// ══ shared ═══════════════════════════════════════════════════════════

/** Register cells arrive as markdown — `**CF-17**` is a cell, not a heading. */
const plain = (cell) => String(cell ?? '').replace(/\*\*/g, '').replace(/`/g, '').trim();

const slug = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
  'august', 'september', 'october', 'november', 'december'];

/** "12 August 2026" and "14 Aug" both land on something sortable. */
function whenOf(text) {
  if (!text) return null;
  const m = /(\d{1,2})\s+([A-Za-z]{3,})\s*(\d{4})?/.exec(String(text));
  if (!m) return null;
  const month = MONTHS.findIndex((n) => n.startsWith(m[2].toLowerCase().slice(0, 3)));
  if (month < 0) return null;
  // No year on a register row means this one — every conflict here is from this
  // delivery, and defaulting to 1970 would sort them all to the top as though
  // they were the oldest decisions in the package.
  return new Date(Number(m[3] ?? new Date().getFullYear()), month, Number(m[1]));
}

const dayLabel = (d) => d.toLocaleDateString(undefined, { day: 'numeric', month: 'long', year: 'numeric' });

/**
 * The state each conflict is in, derived rather than read.
 *
 * `conflict-status.md` puts a summary table first — State against Count — then
 * one table per state in that order, and no heading survives into the payload.
 * So the states come from matching the summary's counts to the tables that
 * follow. That is a derivation, and it is only sound while the counts agree:
 * if they ever stop agreeing the mapping would be wrong in a way nobody would
 * see, so this returns nothing and the rows go unlabelled instead of wrong.
 */
function statesOf(doc) {
  const [summary, ...rest] = doc.tables ?? [];
  const head = (summary?.headers ?? []).map((h) => h.trim().toLowerCase());
  if (head[0] !== 'state' || head[1] !== 'count') return null;

  const wanted = (summary.rows ?? [])
    .map((r) => [plain(r[0]), Number(plain(r[1]))])
    .filter(([name, n]) => name.toLowerCase() !== 'total' && Number.isFinite(n));

  if (wanted.length !== rest.length) return null;
  const map = new Map();
  for (let i = 0; i < wanted.length; i++) {
    const [name, n] = wanted[i];
    if ((rest[i].rows ?? []).length !== n) return null;
    map.set(rest[i], name);
  }
  return map;
}

/**
 * Every conflict the registers carry, de-duplicated by id.
 *
 * The registers are not one shape. `conflicts.md` alone holds five different
 * tables — ID/Issue/Owner/Since, ID/Issue/Closed by/ADR, ID/Was/Now — and its
 * largest table declares three headers over rows that carry four cells, so a
 * strict header lookup silently drops the owner and the date from 106 of them.
 *
 * So: headers are used where they describe the row, and where they do not, the
 * only field guessed is the date — because a date identifies itself. It either
 * parses or it does not. The owner is left blank rather than inferred from a
 * position the header does not vouch for, since a wrong name against a conflict
 * is worse than no name.
 */
function conflictRows() {
  const out = new Map();
  let mismatched = 0;
  for (const doc of state.decisions?.documents ?? []) {
    if (doc.group !== 'register') continue;
    const states = statesOf(doc);
    for (const table of doc.tables ?? []) {
      const head = (table.headers ?? []).map((h) => h.trim().toLowerCase());
      const at = (name) => head.indexOf(name);
      if (at('id') < 0 || at('issue') < 0) continue;

      for (const row of table.rows ?? []) {
        const id = plain(row[at('id')]);
        if (!/^CF-\d+$/.test(id)) continue;
        const wide = row.length > head.length;
        if (wide) mismatched++;

        const was = out.get(id) ?? { id, issue: '', owner: '', since: '', state: '' };
        const issue = plain(row[at('issue')]);
        const owner = !wide && at('owner') >= 0 ? plain(row[at('owner')]) : '';
        // A date says what it is. Take the last cell that reads as one, which
        // works whether or not the header admits the column exists.
        let since = !wide && at('since') >= 0 ? plain(row[at('since')]) : '';
        if (!since) {
          for (let i = row.length - 1; i > 1; i--) {
            const cell = plain(row[i]);
            if (cell.length <= 14 && whenOf(cell)) { since = cell; break; }
          }
        }
        out.set(id, {
          ...was,
          issue: issue || was.issue,
          owner: owner || was.owner,
          since: since || was.since,
          state: states?.get(table) ?? was.state,
        });
      }
    }
  }
  const rows = [...out.values()];
  rows.mismatched = mismatched;
  return rows;
}

const adrById = (id) => (state.decisions?.adrs ?? []).find((a) => a.id === id) ?? null;

/** ADR-0014 in prose, and `[ADR-0014](0014-….md)` in a status line, both resolve. */
function adrRefs(text) {
  const out = new Set();
  for (const m of String(text ?? '').matchAll(/ADR-(\d{3,4})/g)) out.add(m[1].padStart(4, '0'));
  return [...out];
}

// ══ Timeline ═════════════════════════════════════════════════════════
//
// The sequence is the argument. ADR-0018 makes sense only after ADR-0011, and
// CF-138 only after the 14 August minute — a register sorted by number hides
// the one thing a reviewer needs. Decisions and conflicts share one axis
// because they happened to one team in one order, and separating them is what
// made that order unreadable.


/**
 * A headline and a body from one paragraph.
 *
 * Splits on the first sentence end, but only where that leaves a headline
 * short enough to be one — a sentence that runs to 300 characters is not a
 * title, so it is cut on a word instead.
 */
function splitFirstSentence(text) {
  const whole = String(text ?? '').trim();
  const stop = whole.search(/[.!?](\s|$)/);
  if (stop > 0 && stop <= 150) return [whole.slice(0, stop + 1), whole.slice(stop + 1).trim()];
  if (whole.length <= 150) return [whole, ''];
  const cut = whole.lastIndexOf(' ', 150);
  return [`${whole.slice(0, cut > 60 ? cut : 150)}…`, whole.slice(cut > 60 ? cut : 150).trim()];
}

export function renderTimeline() {
  const body = $('timeline-body');
  body.innerHTML = '';
  if (!state.decisions?.present) {
    body.append(el('p', 'pane-empty', 'No docs/ in this package.'));
    $('timeline-hint').textContent = '';
    return;
  }

  const needle = state.timelineFilter.trim().toLowerCase();
  const hit = (...parts) => !needle || parts.some((p) => String(p ?? '').toLowerCase().includes(needle));

  const events = [];
  if (state.timelineScope !== 'conflicts') {
    for (const adr of state.decisions.adrs ?? []) {
      if (!hit(adr.id, adr.title, adr.decision)) continue;
      events.push({ kind: 'adr', at: whenOf(adr.date), id: `ADR-${adr.id}`,
        title: adr.title, note: adr.decision, verdict: adr.verdict, adr });
    }
  }
  if (state.timelineScope !== 'adrs') {
    for (const c of conflictRows()) {
      if (!hit(c.id, c.issue, c.owner)) continue;
      // A conflict's "issue" is a paragraph, not a title — CF-157 runs to
      // 1,200 characters. The first sentence is the headline and the rest is
      // the body, which is how it reads in the register anyway.
      const [head, rest] = splitFirstSentence(c.issue);
      events.push({ kind: 'conflict', at: whenOf(c.since), id: c.id,
        title: head,
        note: [rest, c.owner ? `owner — ${c.owner}` : ''].filter(Boolean).join(' · '),
        verdict: c.state });
    }
  }

  // Undated last, and counted out loud. A timeline that quietly drops what it
  // cannot place is a timeline that misreports how much it is showing.
  const dated = events.filter((e) => e.at).sort((a, b) => b.at - a.at);
  const undated = events.filter((e) => !e.at);

  const adrs = events.filter((e) => e.kind === 'adr').length;
  const cfs = events.length - adrs;
  $('timeline-hint').textContent = `${adrs} decisions · ${cfs} conflicts · newest first`
    + (undated.length ? ` · ${undated.length} carry no date` : '');
  $('timeline-hint').title = undated.length
    ? 'A conflict with no date is one whose register table records none — it is '
      + 'listed at the end rather than placed on a date it does not have.'
    : '';

  if (!events.length) {
    body.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
    return;
  }

  const line = el('div', 'timeline');
  let lastDay = null;
  for (const e of dated) {
    const day = dayLabel(e.at);
    if (day !== lastDay) { lastDay = day; line.append(el('div', 'timeline-day', day)); }
    line.append(timelineRow(e));
  }
  if (undated.length) {
    line.append(el('div', 'timeline-day undated',
      `No date recorded — ${undated.length} item${undated.length === 1 ? '' : 's'}`));
    for (const e of undated) line.append(timelineRow(e));
  }
  body.append(line);
}

function timelineRow(e) {
  const row = el('div', `timeline-row ${e.kind}`);
  row.append(el('span', 'timeline-dot'));
  const main = el('div', 'timeline-main');
  const head = el('div', 'timeline-head');
  head.append(el('code', 'timeline-id', e.id));
  head.append(el('span', 'timeline-title', e.title));
  if (e.verdict) head.append(el('span', `timeline-verdict ${slug(e.verdict)}`, e.verdict));
  main.append(head);
  if (e.note) main.append(el('p', 'timeline-note', String(e.note).slice(0, 240)));
  row.append(main);
  if (e.kind === 'adr') {
    row.classList.add('clickable');
    row.onclick = () => openDecision(e.adr.id);
  }
  return row;
}

// ══ Supersession ═════════════════════════════════════════════════════
//
// `check-package` already enforces that a citation may not cross a
// supersession, and the viewer showed none of it. Six of the 26 decisions are
// amended or superseded, and a reader had no way to see the shape of that —
// an ADR that is Accepted and partly superseded reads as current in a list and
// is not.

export function renderSupersession() {
  const body = $('supersession-body');
  body.innerHTML = '';
  const adrs = state.decisions?.adrs ?? [];
  if (!adrs.length) {
    body.append(el('p', 'pane-empty', 'No decisions in this package.'));
    $('supersession-hint').textContent = '';
    return;
  }

  // Edges come from `supersededBy`, which is a list of ids. `supersedes` is
  // prose — "the working assumption that UAE law mandates…" — and is shown as
  // written rather than parsed into an arrow it does not support.
  const replaces = new Map();   // successor id -> [predecessor ids]
  for (const a of adrs) {
    for (const by of a.supersededBy ?? []) {
      if (!replaces.has(by)) replaces.set(by, []);
      replaces.get(by).push(a.id);
    }
  }

  const involved = new Set();
  for (const [successor, predecessors] of replaces) {
    involved.add(successor);
    for (const p of predecessors) involved.add(p);
  }
  for (const a of adrs) if (a.amended || a.partlySuperseded) involved.add(a.id);

  const shown = state.supersessionAll ? adrs : adrs.filter((a) => involved.has(a.id));
  $('supersession-hint').textContent =
    `${involved.size} of ${adrs.length} decisions are superseded, amended or replace something`
    + (state.supersessionAll ? ' · showing all' : '');

  if (!shown.length) {
    body.append(el('p', 'pane-empty', 'No decision supersedes or amends another.'));
    return;
  }

  const chart = el('div', 'supersede');
  for (const a of [...shown].sort((x, y) => Number(y.number) - Number(x.number))) {
    const card = el('div', `supersede-card ${slug(a.verdict)}`);

    const head = el('div', 'supersede-head');
    head.append(el('code', 'supersede-id', `ADR-${a.id}`));
    head.append(el('span', 'supersede-title', a.title));
    head.append(el('span', `supersede-verdict ${slug(a.verdict)}`, a.verdict));
    card.append(head);

    // The two states that read as current and are not, said plainly rather
    // than left to a badge a reader has to know how to interpret.
    if (a.partlySuperseded) {
      card.append(el('p', 'supersede-warn',
        'Accepted and partly superseded — parts of this still stand and parts do not.'));
    }
    if (a.amended && a.verdict !== 'Superseded') {
      card.append(el('p', 'supersede-note', `Amended — ${a.status}`));
    }

    for (const by of a.supersededBy ?? []) {
      card.append(arrow('replaced by', by));
    }
    for (const p of replaces.get(a.id) ?? []) {
      card.append(arrow('replaces', p));
    }
    if (a.supersedes) {
      // Prose, not an id — shown as the sentence it is.
      card.append(el('p', 'supersede-prose', `Supersedes ${a.supersedes}`));
    }

    card.onclick = () => openDecision(a.id);
    chart.append(card);
  }
  body.append(chart);
}

function arrow(label, id) {
  const other = adrById(id);
  const row = el('div', `supersede-edge ${slug(label)}`);
  row.append(el('span', 'supersede-edge-label', label));
  const link = el('button', 'supersede-link', other ? `ADR-${id} ${other.title}` : `ADR-${id}`);
  link.type = 'button';
  link.onclick = (e) => { e.stopPropagation(); openDecision(id); };
  row.append(link);
  return row;
}

// ══ Register ═════════════════════════════════════════════════════════
//
// 124 conflicts is a dataset, and a file tree is the wrong control for a
// dataset. Owner and state are columns because they are what a delivery
// meeting sorts by.

export function renderRegister() {
  const body = $('register-body');
  body.innerHTML = '';
  const docs = (state.decisions?.documents ?? []).filter((d) => d.group === 'register');
  if (!docs.length) {
    body.append(el('p', 'pane-empty', 'No registers in this package.'));
    $('register-hint').textContent = '';
    return;
  }

  const pick = $('register-pick');
  if (pick.options.length !== docs.length) {
    pick.innerHTML = '';
    for (const d of docs) {
      const option = el('option', null, `${d.title ?? d.id} · ${d.rows} rows`);
      option.value = d.id;
      pick.append(option);
    }
  }
  if (!docs.some((d) => d.id === state.registerId)) state.registerId = docs[0].id;
  pick.value = state.registerId;

  const doc = docs.find((d) => d.id === state.registerId);
  const isConflicts = /conflict/.test(doc.id);

  if (isConflicts) return renderConflictRegister(body, doc);
  return renderPlainRegister(body, doc);
}

function renderConflictRegister(body, doc) {
  const rows = conflictRows();
  const states = [...new Set(rows.map((r) => r.state).filter(Boolean))];

  const seg = $('register-state');
  seg.innerHTML = '';
  for (const [value, label] of [['', 'Every state'], ...states.map((s) => [s, s])]) {
    const button = el('button', null, label);
    button.dataset.scope = value;
    button.classList.toggle('active', state.registerState === value);
    button.onclick = () => { state.registerState = value; renderRegister(); };
    seg.append(button);
  }

  const needle = state.registerFilter.trim().toLowerCase();
  const shown = rows.filter((r) =>
    (!state.registerState || r.state === state.registerState)
    && (!needle || [r.id, r.issue, r.owner].some((f) => f.toLowerCase().includes(needle))));

  const open = rows.filter((r) => /open/i.test(r.state)).length;
  const stateless = rows.filter((r) => !r.state).length;
  // Two numbers, both true and measuring different things: every conflict the
  // registers mention, and the subset the status register tracks a state for.
  // The briefs quote 145 and 157 and the status register totals 124 — showing
  // one of those alone is how a reader ends up confident and wrong.
  $('register-hint').textContent =
    `${shown.length} of ${rows.length} conflicts${open ? ` · ${open} open` : ''}`
    + (stateless ? ` · ${stateless} carry no state in the status register` : '');

  if (!shown.length) {
    body.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
    return;
  }

  const table = el('table', 'register-table');
  const thead = el('thead');
  const hrow = el('tr');
  for (const h of ['ID', 'Issue', 'Owner', 'State', 'Since']) hrow.append(el('th', null, h));
  thead.append(hrow);
  table.append(thead);

  const tbody = el('tbody');
  // Open first — the list exists to find what still needs doing, and a closed
  // conflict is a record rather than a task.
  const order = [...shown].sort((a, b) => {
    const openness = Number(/open/i.test(b.state)) - Number(/open/i.test(a.state));
    if (openness) return openness;
    return Number(a.id.slice(3)) - Number(b.id.slice(3));
  });
  for (const r of order) {
    const tr = el('tr', `register-row ${slug(r.state)}`);
    tr.append(el('td', 'register-id', el('code', null, r.id)));
    tr.append(el('td', 'register-issue', r.issue));
    tr.append(el('td', 'register-owner', r.owner || '—'));
    const st = el('td', 'register-state');
    if (r.state) st.append(el('span', `register-chip ${slug(r.state)}`, r.state));
    else st.append(el('span', 'register-none', '—'));
    tr.append(st);
    tr.append(el('td', 'register-since', r.since || '—'));
    tbody.append(tr);
  }
  table.append(tbody);
  body.append(table);
}

/** Any other register: its own tables, as tables. */
function renderPlainRegister(body, doc) {
  $('register-state').innerHTML = '';
  const needle = state.registerFilter.trim().toLowerCase();
  let shown = 0;
  let total = 0;

  for (const t of doc.tables ?? []) {
    const rows = (t.rows ?? []).filter((r) =>
      !needle || r.some((c) => plain(c).toLowerCase().includes(needle)));
    total += (t.rows ?? []).length;
    shown += rows.length;
    if (!rows.length) continue;

    const table = el('table', 'register-table');
    const thead = el('thead');
    const hrow = el('tr');
    for (const h of t.headers ?? []) hrow.append(el('th', null, h || '—'));
    thead.append(hrow);
    table.append(thead);
    const tbody = el('tbody');
    for (const r of rows) {
      const tr = el('tr', 'register-row');
      for (const c of r) {
        const td = el('td');
        td.innerHTML = inlineMarkdown(plain(c));
        tr.append(td);
      }
      tbody.append(tr);
    }
    table.append(tbody);
    body.append(table);
  }

  $('register-hint').textContent = `${shown} of ${total} rows · ${doc.file}`;
  if (!shown) body.append(el('p', 'pane-empty', 'Nothing matches that filter.'));
}

// ══ Decision ═════════════════════════════════════════════════════════
//
// One decision as prose, with what cites it resolved as links. The body used
// to be a tooltip — the layer whose own tip says prose is where the reasons
// live was showing the reasons on hover.

export function openDecision(id) {
  state.adrId = id;
  setMode('decision');
  renderDecision();
}

export async function renderDecision() {
  const body = $('decision-body');
  const adrs = state.decisions?.adrs ?? [];
  if (!adrs.length) {
    body.innerHTML = '';
    body.append(el('p', 'pane-empty', 'No decisions in this package.'));
    return;
  }

  const pick = $('decision-pick');
  if (pick.options.length !== adrs.length) {
    pick.innerHTML = '';
    for (const a of [...adrs].sort((x, y) => Number(x.number) - Number(y.number))) {
      const option = el('option', null, `ADR-${a.id} · ${a.title}`);
      option.value = a.id;
      pick.append(option);
    }
  }
  if (!adrs.some((a) => a.id === state.adrId)) state.adrId = adrs[0].id;
  pick.value = state.adrId;

  const adr = adrById(state.adrId);
  $('decision-hint').textContent = `${adr.date ?? 'no date'} · ${adr.verdict} · ${adr.file}`;

  body.innerHTML = '';
  const head = el('div', 'decision-head');
  head.append(el('h1', 'decision-title', `ADR-${adr.id} — ${adr.title}`));
  const meta = el('div', 'decision-meta');
  meta.append(el('span', `decision-verdict ${slug(adr.verdict)}`, adr.verdict));
  if (adr.date) meta.append(el('span', 'decision-date', adr.date));
  head.append(meta);
  if (adr.partlySuperseded) {
    head.append(el('p', 'supersede-warn',
      'Accepted and partly superseded — parts of this still stand and parts do not.'));
  }
  body.append(head);

  // What links to it, resolved rather than described. This is the half that
  // was missing entirely: an ADR knew what it closed and constrained and the
  // viewer showed none of it.
  const links = el('div', 'decision-links');
  addDecisionLinks(links, 'Replaced by', (adr.supersededBy ?? []).map((x) => ({ id: x })));
  addDecisionLinks(links, 'Replaces',
    adrs.filter((a) => (a.supersededBy ?? []).includes(adr.id)).map((a) => ({ id: a.id })));
  addDecisionLinks(links, 'Cited by',
    adrs.filter((a) => a.id !== adr.id && adrRefs(a.status).includes(adr.id)).map((a) => ({ id: a.id })));

  const cites = conflictRows().filter((c) => adrRefs(c.issue).includes(adr.id));
  if (cites.length) {
    const section = el('div', 'decision-link-group');
    section.append(el('div', 'decision-link-head', `Conflicts citing it · ${cites.length}`));
    for (const c of cites) {
      const row = el('div', 'decision-link');
      row.append(el('code', null, c.id));
      row.append(el('span', null, c.issue.slice(0, 120)));
      section.append(row);
    }
    links.append(section);
  }
  if (adr.closes) links.append(factLine('Closes', adr.closes));
  if (adr.withdraws) links.append(factLine('Withdraws', adr.withdraws));
  if ((adr.constrains ?? []).length) links.append(factLine('Constrains', adr.constrains.join(', ')));
  if ((adr.domains ?? []).length) links.append(factLine('Domains', adr.domains.join(', ')));
  if (links.children.length) body.append(links);

  // The prose itself, which is the point of the layer.
  const prose = el('div', 'decision-prose');
  prose.textContent = 'Loading…';
  body.append(prose);
  try {
    const text = await fetch(`/api/file?path=${encodeURIComponent(adr.file)}`).then((r) => {
      if (!r.ok) throw new Error(String(r.status));
      return r.text();
    });
    prose.innerHTML = '';
    prose.append(markdownBlock(text));
    for (const link of prose.querySelectorAll('.md-adr')) {
      link.onclick = (e) => { e.preventDefault(); openDecision(link.dataset.adr); };
    }
  } catch {
    prose.textContent = `Could not read ${adr.file}`;
  }
}

function factLine(label, value) {
  const row = el('div', 'decision-fact');
  row.append(el('span', 'decision-fact-label', label));
  row.append(el('span', 'decision-fact-value', value));
  return row;
}

function addDecisionLinks(host, label, items) {
  if (!items.length) return;
  const section = el('div', 'decision-link-group');
  section.append(el('div', 'decision-link-head', `${label} · ${items.length}`));
  for (const item of items) {
    const other = adrById(item.id);
    const row = el('button', 'decision-link clickable');
    row.type = 'button';
    row.append(el('code', null, `ADR-${item.id}`));
    row.append(el('span', null, other ? other.title : 'not in this package'));
    if (other) row.onclick = () => openDecision(item.id);
    else row.disabled = true;
    section.append(row);
  }
  host.append(section);
}


