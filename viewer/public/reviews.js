/**
 * What everyone has actually been doing.
 *
 * The sign-off page answers "where does each artefact stand", which is what a
 * report needs. It cannot answer this, because one row per artefact has already
 * thrown away the three things that say whether a review is going well: the
 * disagreement, the revisions, and the pace. Those come off the full verdict
 * history, so this page reads /api/verdicts and keeps them.
 *
 * Charts are hand-drawn SVG. Everything else in this viewer is — the graph, the
 * ER boxes, the state machines — and a charting library would be the first
 * dependency in the frontend, for four charts.
 */
import * as auth from '/validation.js';
import { hue } from '/core.js';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const svgEl = (tag, attrs = {}) => {
  const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  return node;
};

// Every value, in the order the form offers them, so the pace chart and the
// filters both cover the whole vocabulary rather than the three it started with.
const VERDICTS = auth.VERDICTS.map(([k]) => k);
// Labels come from one place so the page and the form can never disagree about
// what a value is called.
const LABEL = Object.fromEntries(auth.VERDICTS);
const VERDICT_TOKENS = { approved: 'ok', 'needs-work': 'warning', rejected: 'error' };
const colour = (k) => hue(VERDICT_TOKENS[k] ?? 'text-faint');

// How the team answered — the tracker's "Our verdict" column, in the tracker's
// own colours: green for the two that mean the thing exists now, slate for a
// question answered, khaki for a point taken, grey for nothing to do.
const RESPONSE_LABEL = Object.fromEntries(auth.RESPONSES);

const KINDS = {
  operation: 'APIs', table: 'Tables', screen: 'Wireframes',
  board: 'Boards', module: 'Modules',
  state: 'State models', schema: 'Schemas',
};

// Where the reviewer was standing. Recorded on the verdict rather than derived
// from its kind, so "how much of the frontend is signed off" can be asked
// separately from "how much of the backend is" — which is the question a
// delivery meeting asks and the kind alone was answering only by coincidence.
const LAYERS = {
  frontend: 'Frontend', contracts: 'Contracts', domain: 'Domain',
  backend: 'Backend', modules: 'Modules', decisions: 'Decisions',
};

// Which side has to act on it, as the reviewer said rather than as the kind
// implies. Two values, because the question is whose queue it is in.
const TAGS = { frontend: 'Frontend', backend: 'Backend' };

// Whose review a row belongs to. The team's and the client's are two reviews of
// the same package, and mixing them would make "12 approved" a number nobody
// could act on — it would not say approved by whom.
const AUDIENCES = { internal: 'The team', client: 'Client' };

const DAY = 86400000;
const when = (iso) => new Date(iso);
const fmt = (d) => d.toLocaleString(undefined,
  { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
const fmtDay = (d) => d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });

/** "3 minutes", "2 days" — a duration a person can hold in their head. */
function human(ms) {
  if (!Number.isFinite(ms)) return '—';
  const s = Math.round(ms / 1000);
  if (s < 90) return `${s}s`;
  const m = Math.round(s / 60);
  if (m < 90) return `${m}m`;
  const h = Math.round(m / 60);
  if (h < 48) return `${h}h`;
  return `${Math.round(h / 24)}d`;
}

const median = (xs) => {
  if (!xs.length) return NaN;
  const s = [...xs].sort((a, b) => a - b);
  const mid = s.length >> 1;
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
};

const state = {
  all: [],
  accounts: [],
  filter: {
    kind: '', layer: '', tag: '', done: '', verdict: '',
    audience: '', person: '', window: '', text: '',
  },
  // Newest first, which is what a log is. Every column is sortable because the
  // question changes: "what happened today" wants time, "what is still open"
  // wants status, and "what did Asha say about the POS" wants the artefact.
  sort: { key: 'at', dir: -1 },
};

// ── filtering ────────────────────────────────────────────────────────

function filtered() {
  const f = state.filter;
  const needle = f.text.trim().toLowerCase();
  const cutoff = f.window ? Date.now() - Number(f.window) * DAY : null;
  return state.all.filter((v) => {
    if (f.kind && v.target_kind !== f.kind) return false;
    if (f.layer && (v.layer || '') !== f.layer) return false;
    if (f.tag && (v.tag || '') !== f.tag) return false;
    if (f.audience && (v.audience || 'internal') !== f.audience) return false;
    // Settled rather than "has a date": work that was marked done and sent
    // back is open again, and a filter that disagreed with the badge beside it
    // would be the kind of wrong nobody reports because they assume they
    // misread it.
    if (f.done === 'done' && !auth.isSettled(v)) return false;
    if (f.done === 'open' && auth.isSettled(v)) return false;
    if (f.verdict && v.verdict !== f.verdict) return false;
    if (f.person && String(v.account_id) !== f.person) return false;
    if (cutoff && when(v.at).getTime() < cutoff) return false;
    if (needle) {
      const hay = `${v.target_id} ${v.note ?? ''} ${v.by ?? ''} ${v.by_email ?? ''} ${v.verdict}`;
      if (!hay.toLowerCase().includes(needle)) return false;
    }
    return true;
  });
}

// ── headline ─────────────────────────────────────────────────────────

function renderHeadline(rows) {
  const box = $('headline');
  box.innerHTML = '';

  const artefacts = new Set(rows.map((v) => `${v.target_kind} ${v.target_id}`));
  const people = new Set(rows.map((v) => v.account_id));
  // A revision is a second verdict on something already judged. It is the
  // clearest sign a review is doing work rather than rubber-stamping.
  const revisions = rows.length - artefacts.size;
  const withNote = rows.filter((v) => (v.note ?? '').trim().length).length;

  const stat = (value, label, hint) => {
    const card = el('div', 'stat-card');
    card.append(el('div', 'stat-value', String(value)));
    card.append(el('div', 'stat-label', label));
    if (hint) card.append(el('div', 'stat-hint', hint));
    return card;
  };

  box.append(stat(rows.length, 'responses', `${people.size} reviewer${people.size === 1 ? '' : 's'}`));
  box.append(stat(artefacts.size, 'artefacts judged',
    `${(rows.length / Math.max(artefacts.size, 1)).toFixed(1)} responses each`));
  box.append(stat(revisions, 'revisions',
    revisions ? 'someone changed their mind' : 'nothing has been revisited'));

  // The only number on this strip that goes down. Counted over everything that
  // asked for work — a rejection or a needs-work — because an approval is not
  // a thing anybody has to come back and close.
  const asked = rows.filter((v) => auth.asksForWork(v.verdict));
  const openWork = asked.filter((v) => !auth.isSettled(v)).length;
  box.append(stat(openWork, 'still open',
    !asked.length ? 'nothing has been sent back'
      : openWork ? `of ${asked.length} that asked for work`
      : 'all of it has been marked done'));
  box.append(stat(
    `${Math.round((withNote / Math.max(rows.length, 1)) * 100)}%`,
    'gave a reason',
    withNote === rows.length ? 'every one' : `${rows.length - withNote} without a note`));
}

// ── pace: verdicts per day, stacked ──────────────────────────────────

function renderPace(rows) {
  const host = $('pace');
  host.innerHTML = '';
  if (!rows.length) {
    host.append(el('p', 'pane-empty', 'Nothing recorded yet.'));
    $('pace-note').textContent = '';
    return;
  }

  const times = rows.map((v) => when(v.at).getTime()).filter(Number.isFinite);
  const first = Math.min(...times);
  const last = Math.max(...times);
  const spanDays = Math.max(1, Math.ceil((last - first) / DAY) + 1);

  // One bucket per day, unless it all happened inside a day — in which case
  // days would be one bar and say nothing, so bucket by hour instead.
  const byHour = spanDays <= 1;
  const size = byHour ? 3600000 : DAY;
  const start = new Date(first);
  if (byHour) start.setMinutes(0, 0, 0);
  else start.setHours(0, 0, 0, 0);
  const buckets = Math.max(1, Math.ceil((last - start.getTime()) / size) + 1);

  const grid = Array.from({ length: buckets }, () => ({ approved: 0, 'needs-work': 0, rejected: 0 }));
  for (const v of rows) {
    const i = Math.floor((when(v.at).getTime() - start.getTime()) / size);
    if (grid[i] && grid[i][v.verdict] != null) grid[i][v.verdict]++;
  }

  const peak = Math.max(1, ...grid.map((g) => VERDICTS.reduce((n, k) => n + g[k], 0)));
  const W = 940, H = 168, PAD = 26;
  const bw = (W - PAD * 2) / buckets;

  const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, class: 'chart', preserveAspectRatio: 'none' });
  // baseline
  svg.append(svgEl('line', {
    x1: PAD, x2: W - PAD, y1: H - 22, y2: H - 22,
    stroke: 'currentColor', 'stroke-opacity': 0.18,
  }));

  grid.forEach((g, i) => {
    let y = H - 22;
    for (const k of VERDICTS) {
      if (!g[k]) continue;
      const h = (g[k] / peak) * (H - 46);
      y -= h;
      const bar = svgEl('rect', {
        x: PAD + i * bw + bw * 0.14, y,
        width: Math.max(1.5, bw * 0.72), height: h,
        fill: colour(k), rx: Math.min(2, bw * 0.2),
      });
      // append() returns undefined, so the title has to be built before it is
      // attached — chaining off it throws, and the throw takes every panel
      // below this one with it.
      const at = new Date(start.getTime() + i * size);
      const title = svgEl('title');
      title.textContent = `${g[k]} ${LABEL[k].toLowerCase()} · ${byHour ? fmt(at) : fmtDay(at)}`;
      bar.append(title);
      svg.append(bar);
    }
  });

  // only the ends get a label — a tick under every bar is unreadable at 30 days
  const tick = (i, text, anchor) => {
    const t = svgEl('text', {
      x: PAD + i * bw + bw / 2, y: H - 6, 'text-anchor': anchor,
      class: 'chart-tick',
    });
    t.textContent = text;
    return t;
  };
  const startAt = new Date(start);
  const endAt = new Date(start.getTime() + (buckets - 1) * size);
  svg.append(tick(0, byHour ? fmt(startAt) : fmtDay(startAt), 'start'));
  if (buckets > 1) svg.append(tick(buckets - 1, byHour ? fmt(endAt) : fmtDay(endAt), 'end'));

  host.append(svg);
  host.append(legend());

  const perDay = rows.length / spanDays;
  $('pace-note').textContent =
    `${rows.length} over ${byHour ? 'one day' : `${spanDays} days`} · ` +
    `${perDay.toFixed(1)}/day · busiest ${peak} in one ${byHour ? 'hour' : 'day'}`;
}

function legend() {
  const box = el('div', 'chart-legend');
  for (const k of VERDICTS) {
    const item = el('span', 'signoff-legend-item');
    const dot = el('span', 'verdict-dot');
    dot.style.background = colour(k);
    item.append(dot, el('span', null, LABEL[k]));
    box.append(item);
  }
  return box;
}

// ── disagreement ─────────────────────────────────────────────────────

function renderContested(rows) {
  const host = $('contested');
  host.innerHTML = '';

  const byTarget = new Map();
  for (const v of rows) {
    const key = `${v.target_kind} ${v.target_id}`;
    if (!byTarget.has(key)) byTarget.set(key, []);
    byTarget.get(key).push(v);
  }

  // Disagreement means two *different people* reaching different verdicts. One
  // person changing their own mind is a revision, which is healthy and belongs
  // in a different count.
  const contested = [];
  for (const [key, list] of byTarget) {
    const latestPerPerson = new Map();
    for (const v of [...list].sort((a, b) => a.id - b.id)) latestPerPerson.set(v.account_id, v);
    const distinct = new Set([...latestPerPerson.values()].map((v) => v.verdict));
    if (latestPerPerson.size > 1 && distinct.size > 1) {
      contested.push({ key, list: [...latestPerPerson.values()] });
    }
  }

  $('contested-panel').hidden = contested.length === 0;
  $('contested-note').textContent =
    `${contested.length} artefact${contested.length === 1 ? '' : 's'} where reviewers do not agree`;
  if (!contested.length) return;

  for (const { key, list } of contested) {
    const row = el('div', 'contested-row');
    const [kind, ...rest] = key.split(' ');
    row.append(el('span', 'signoff-row-name', rest.join(' ')));
    row.append(el('span', 'signoff-row-group', KINDS[kind] ?? kind));
    const opinions = el('span', 'contested-opinions');
    for (const v of list.sort((a, b) => a.by?.localeCompare?.(b.by) ?? 0)) {
      const chip = el('span', `verdict-chip ${v.verdict}`, `${LABEL[v.verdict]} · ${v.by || v.by_email}`);
      if (v.note) chip.title = v.note;
      opinions.append(chip);
    }
    row.append(opinions);
    host.append(row);
  }
}

// ── per reviewer ─────────────────────────────────────────────────────

function renderPeople(rows) {
  const host = $('people');
  host.innerHTML = '';

  const byPerson = new Map();
  for (const v of rows) {
    if (!byPerson.has(v.account_id)) byPerson.set(v.account_id, []);
    byPerson.get(v.account_id).push(v);
  }

  const stats = [...byPerson.entries()].map(([id, list]) => {
    const counts = Object.fromEntries(VERDICTS.map((k) => [k, list.filter((v) => v.verdict === k).length]));
    const times = list.map((v) => when(v.at).getTime()).sort((a, b) => a - b);
    // Gaps between consecutive responses, as a rough sense of working rhythm.
    // Gaps over a day are dropped: they are "went home", not "took a while".
    const gaps = times.slice(1).map((t, i) => t - times[i]).filter((g) => g < DAY);
    const notes = list.map((v) => (v.note ?? '').trim()).filter(Boolean);
    return {
      id,
      who: list[0].by || list[0].by_email,
      email: list[0].by_email,
      role: list[0].by_role,
      total: list.length,
      counts,
      artefacts: new Set(list.map((v) => `${v.target_kind} ${v.target_id}`)).size,
      noteRate: notes.length / list.length,
      medianNote: median(notes.map((n) => n.length)),
      cadence: gaps.length ? median(gaps) : NaN,
      first: times[0],
      last: times[times.length - 1],
    };
  }).sort((a, b) => b.total - a.total);

  $('people-note').textContent = `${stats.length} active of ${state.accounts.length} account${state.accounts.length === 1 ? '' : 's'}`;

  if (!stats.length) {
    host.append(el('p', 'pane-empty', 'Nobody has recorded a verdict in this selection.'));
    return;
  }

  const head = el('div', 'people-row people-head');
  for (const h of ['Reviewer', 'Responses', 'Mix', 'Artefacts', 'Gave a reason', 'Typical gap', 'Last seen']) {
    head.append(el('span', null, h));
  }
  host.append(head);

  const busiest = Math.max(...stats.map((s) => s.total));
  for (const s of stats) {
    const row = el('div', 'people-row');

    const who = el('span', 'people-who');
    who.append(el('span', 'people-name', s.who));
    who.append(el('span', 'people-role', `${s.role ?? ''} · ${s.email}`));
    row.append(who);

    const count = el('span', 'people-count');
    count.append(el('b', null, String(s.total)));
    const bar = el('span', 'people-bar');
    const fill = el('span', 'people-bar-fill');
    fill.style.width = `${(s.total / busiest) * 100}%`;
    bar.append(fill);
    count.append(bar);
    row.append(count);

    // The mix is the interesting column: someone who only ever approves is not
    // reviewing, and the shape shows it faster than three numbers would.
    const mix = el('span', 'people-mix');
    for (const k of VERDICTS) {
      if (!s.counts[k]) continue;
      const seg = el('span', 'people-mix-seg');
      seg.style.width = `${(s.counts[k] / s.total) * 100}%`;
      seg.style.background = colour(k);
      seg.title = `${s.counts[k]} ${LABEL[k].toLowerCase()}`;
      mix.append(seg);
    }
    row.append(mix);

    row.append(el('span', 'people-num', String(s.artefacts)));
    row.append(el('span', 'people-num',
      `${Math.round(s.noteRate * 100)}%${Number.isFinite(s.medianNote) ? ` · ~${Math.round(s.medianNote)} chars` : ''}`));
    row.append(el('span', 'people-num', human(s.cadence)));
    row.append(el('span', 'people-num', fmt(new Date(s.last))));

    host.append(row);
  }

  const rubber = stats.filter((s) => s.total >= 5 && s.counts.approved === s.total);
  const quiet = stats.filter((s) => s.noteRate < 0.34 && s.total >= 5);
  const notes = [];
  if (rubber.length) {
    notes.push(`${rubber.map((s) => s.who).join(', ')} ${rubber.length === 1 ? 'has' : 'have'} ` +
      `approved everything they touched. Worth a look — a reviewer who never dissents may not be reviewing.`);
  }
  if (quiet.length) {
    notes.push(`${quiet.map((s) => s.who).join(', ')} gave a reason on under a third. ` +
      `A verdict with no reason gets rediscovered the hard way.`);
  }
  for (const n of notes) host.append(el('p', 'pane-note warn-note', n));
}

// ── where you were named ───────────────────────────────

/**
 * The notes that named you, unread first.
 *
 * Shown above everything else on the page because it is the only part of it
 * addressed to one person. Read rows stay for a while rather than vanishing on
 * sight — the thing people do with a notification is read it, get interrupted,
 * and come back for it, and a list that empties itself on the first glance is
 * one they stop trusting.
 */
async function renderMentions() {
  let payload = null;
  try {
    payload = await auth.myMentions();
  } catch {
    return;                       // the page is still worth having without it
  }
  const items = payload?.mentions ?? [];
  if (!items.length) return;

  const panel = $('mentions-panel');
  const box = $('mentions');
  panel.hidden = false;
  box.innerHTML = '';
  $('mentions-note').textContent = payload.unseen
    ? `${payload.unseen} unread of ${items.length}`
    : `${items.length}, all read`;
  $('mentions-seen').hidden = !payload.unseen;

  for (const m of items.slice(0, 12)) {
    const row = el('div', `mention-row${m.seen_at ? '' : ' unread'}`);
    if (!m.seen_at) row.append(el('span', 'mention-dot'));

    const who = el('span', 'mention-by', m.by || m.by_email);
    const what = el('span', 'mention-what');
    what.append(el('span', `verdict-chip ${m.verdict}`, LABEL[m.verdict] ?? m.verdict));
    const target = el('a', 'rt-artefact-link', m.target_id);
    target.href = `/#${encodeURIComponent(
      m.target_kind === 'operation' ? m.target_id : `${m.target_kind}:${m.target_id}`)}`;
    what.append(target);

    const line = el('div', 'mention-line');
    line.append(who, what, el('span', 'rt-when-text', fmt(when(m.at))));
    row.append(line);
    // The note itself, with the handles picked out — without it the row says
    // somebody wanted you and not what for, which is a notification that costs
    // a click to become information.
    row.append(auth.renderNote(m.note));
    box.append(row);
  }

  $('mentions-seen').onclick = async () => {
    $('mentions-seen').disabled = true;
    try {
      await auth.markMentionsSeen();
      for (const row of box.querySelectorAll('.mention-row.unread')) {
        row.classList.remove('unread');
        row.querySelector('.mention-dot')?.remove();
      }
      $('mentions-note').textContent = `${items.length}, all read`;
      $('mentions-seen').hidden = true;
    } finally {
      $('mentions-seen').disabled = false;
    }
  };
}

// ── the list ─────────────────────────────────────────────────────────

// The columns, in the order they get read: when it happened, what was said,
// whose queue it lands in, what it was about, and whether anybody has been back
// to it. `get` is both what is drawn and what is sorted on, so a column can
// never sort by something other than what it shows.
const COLUMNS = [
  { key: 'at', label: 'When', cls: 'rt-when', get: (v) => when(v.at).getTime(),
    draw: (v) => el('span', 'rt-when-text', fmt(when(v.at))) },
  { key: 'verdict', label: 'Verdict', cls: 'rt-verdict', get: (v) => v.verdict,
    draw: (v) => el('span', `verdict-chip ${v.verdict}`, LABEL[v.verdict] ?? v.verdict) },
  { key: 'audience', label: 'Review', cls: 'rt-audience',
    get: (v) => v.audience ?? 'internal',
    draw: (v) => ((v.audience ?? 'internal') === 'client'
      ? el('span', 'rt-audience-chip client', 'Client')
      : el('span', 'rt-none', 'team')) },
  { key: 'tag', label: 'Lands on', cls: 'rt-tag', get: (v) => v.tag ?? '',
    draw: (v) => (v.tag
      ? el('span', `verdict-tag-chip ${v.tag}`, TAGS[v.tag] ?? v.tag)
      : el('span', 'rt-none', '—')) },
  { key: 'target_kind', label: 'Kind', cls: 'rt-kind', get: (v) => v.target_kind,
    draw: (v) => el('span', 'rt-kind-text', KINDS[v.target_kind] ?? v.target_kind) },
  { key: 'target_id', label: 'Artefact', cls: 'rt-artefact', get: (v) => v.target_id,
    draw: (v) => {
      const link = el('a', 'rt-artefact-link', v.target_id);
      link.href = `/#${encodeURIComponent(
        v.target_kind === 'operation' ? v.target_id : `${v.target_kind}:${v.target_id}`)}`;
      return link;
    } },
  { key: 'note', label: 'Why', cls: 'rt-note', get: (v) => v.note ?? '',
    draw: (v) => (v.note
      ? auth.renderNote(v.note)
      : el('span', 'rt-none', 'no reason given')) },
  { key: 'by', label: 'Reviewer', cls: 'rt-who', get: (v) => v.by || v.by_email,
    draw: (v) => el('span', 'rt-who-text', v.by || v.by_email) },
];

function sorted(rows) {
  const col = COLUMNS.find((c) => c.key === state.sort.key)
    ?? COLUMNS.find((c) => c.key === 'at');
  const dir = state.sort.dir;
  // A copy: `rows` is the filtered view and sorting it in place would reorder
  // state.all through the shared references on the next pass.
  return [...rows].sort((a, b) => {
    const x = col.get(a);
    const y = col.get(b);
    if (x === y) return b.id - a.id;               // newest first inside a tie
    if (typeof x === 'number' && typeof y === 'number') return (x - y) * dir;
    return String(x).localeCompare(String(y)) * dir;
  });
}

function renderRows(rows) {
  const host = $('rows');
  host.innerHTML = '';
  $('rows-note').textContent = `${rows.length} of ${state.all.length}`;

  if (!rows.length) {
    host.append(el('p', 'pane-empty', 'Nothing matches that.'));
    return;
  }

  const table = el('table', 'review-table');
  const thead = el('thead');
  const hrow = el('tr');
  for (const col of COLUMNS) {
    const th = el('th', `${col.cls}${state.sort.key === col.key ? ' sorted' : ''}`);
    const button = el('button', 'rt-sort', col.label);
    button.type = 'button';
    if (state.sort.key === col.key) {
      // A CSS triangle rather than U+25BE — a border trick needs no font at all.
      button.append(el('span', `rt-arrow ${state.sort.dir < 0 ? 'down' : 'up'}`));
    }
    button.onclick = () => {
      // Clicking the sorted column reverses it; clicking another starts that
      // one descending, because the first thing anybody wants from a new
      // column is its largest or latest end.
      if (state.sort.key === col.key) state.sort.dir *= -1;
      else state.sort = { key: col.key, dir: -1 };
      redraw();
    };
    th.append(button);
    hrow.append(th);
  }
  // Not sortable: it is an action, and a column of buttons that reorders itself
  // when pressed moves the next one out from under the cursor.
  hrow.append(el('th', 'rt-done', 'Status'));
  thead.append(hrow);
  table.append(thead);

  const body = el('tbody');
  table.append(body);
  host.append(table);

  const ordered = sorted(rows);
  let shown = 0;
  const PAGE = 60;
  const more = el('button', 'lineage-more');
  more.type = 'button';

  const draw = () => {
    for (const v of ordered.slice(shown, shown + PAGE)) body.append(tableRow(v));
    shown += Math.min(PAGE, ordered.length - shown);
    const left = ordered.length - shown;
    if (left > 0) more.textContent = `${left} more`;
    else more.remove();
  };
  more.onclick = draw;
  host.append(more);
  draw();
}

function tableRow(v) {
  const row = el('tr', `review-row${auth.isSettled(v) ? ' done' : ''}`);
  for (const col of COLUMNS) {
    const cell = el('td', col.cls);
    cell.append(col.draw(v));
    row.append(cell);
  }
  row.append(doneCell(v));
  return row;
}

/**
 * Mark complete, or put it back.
 *
 * The row is not removed when it is marked done — it is dimmed and stamped with
 * who and when. A worklist that deletes what has been finished cannot answer
 * "was this ever dealt with", which is the question asked three weeks later,
 * and the filter above already gives anybody who wants only the open ones a way
 * to say so.
 */
function doneCell(v) {
  const cell = el('td', 'rt-done');
  const me = auth.account();
  const mayWrite = me && me.role !== 'client';

  const stamp = el('span', 'rt-done-stamp');
  const paint = () => {
    stamp.innerHTML = '';
    if (auth.isSettled(v)) {
      // The response rather than the word "Done": five different answers all
      // showing as one word is what the tracker had already outgrown.
      const how = v.done_response;
      stamp.append(how
        ? el('span', `response-chip ${how}`, RESPONSE_LABEL[how] ?? how)
        : el('span', 'rt-done-chip', 'Done'));
      stamp.append(el('span', 'rt-done-by',
        `${v.done_by_name ? `${v.done_by_name} · ` : ''}${fmt(when(v.done_at))}`));
    } else if (v.sent_back_at) {
      // Open again, but not the same as never having been finished — somebody
      // did the work and it was not accepted, and the reason is the only part
      // of this row that says what to do next, so it is shown rather than
      // hidden behind a hover.
      stamp.append(el('span', 'rt-sentback-chip', 'Sent back'));
      stamp.append(el('span', 'rt-done-by',
        `${v.sent_back_by_name ? `${v.sent_back_by_name} · ` : ''}${fmt(when(v.sent_back_at))}`));
      if (v.sent_back_note) {
        stamp.append(el('span', 'rt-sentback-note', v.sent_back_note));
      }
    } else if (!auth.asksForWork(v.verdict)) {
      stamp.append(el('span', 'rt-none', '—'));
    } else {
      stamp.append(el('span', 'rt-open-chip', 'Open'));
    }
  };
  paint();
  cell.append(stamp);

  // Two separate rules, and only the first is about closing. Discarding is
  // always offered on your own row — a client's mis-click is as much a mis-click
  // as anybody's, and an approval typed into the wrong artefact is the most
  // likely row to want gone.
  //
  // An approval is not a thing anybody has to go and *do*, so there is nothing
  // to close: a tick on one would mean nothing and would make the open count
  // answer a different question than it says it does.
  if (!mayWrite || !auth.asksForWork(v.verdict)) {
    cell.append(discardButton(v));
    return cell;
  }

  const settled = auth.isSettled(v);

  const apply = async (want, response) => {
    try {
      const result = await auth.markVerdictDone(v.id, want, response);
      v.done_at = result.done_at;
      v.done_by_name = result.done_by_name;
      v.done_response = result.done_response ?? '';
      cell.replaceWith(doneCell(v));
      // The headline counts open work, so it has to hear about this.
      renderHeadline(filtered());
    } catch (error) {
      $('error').textContent = error.message;
      $('error').hidden = false;
    }
  };

  if (settled) {
    const reopen = el('button', 'chip rt-done-button', 'Reopen');
    reopen.type = 'button';
    reopen.onclick = () => { reopen.disabled = true; apply(false, ''); };
    cell.append(reopen);
  } else {
    // Closing is answering, so the control is the five answers rather than one
    // button called Done. Folded behind a press because five chips on every row
    // of a sixty-row table is a wall, and only one row is being answered at a
    // time.
    const open = el('button', 'chip rt-done-button', 'Respond');
    open.type = 'button';
    open.onclick = () => {
      open.remove();
      const picker = el('div', 'response-picker');
      for (const [value, label] of auth.RESPONSES) {
        const pick = el('button', `chip response-set ${value}`, label);
        pick.type = 'button';
        pick.onclick = () => {
          for (const b of picker.querySelectorAll('button')) b.disabled = true;
          apply(true, value);
        };
        picker.append(pick);
      }
      const cancel = el('button', 'chip response-cancel', 'Cancel');
      cancel.type = 'button';
      cancel.onclick = () => { picker.replaceWith(open); };
      picker.append(cancel);
      cell.append(picker);
    };
    cell.append(open);
  }
  cell.append(sendBackControl(v, paint));
  cell.append(discardButton(v));
  return cell;
}

/**
 * Reject a completion, with a reason. Admin only.
 *
 * The other half of Mark done. Without it the only answer to work that was not
 * really finished is to reopen it silently, which tells whoever did it nothing
 * and so tends to produce the same thing again.
 *
 * The note is not optional and the control is built around that: pressing
 * "Send back" opens a field rather than doing anything, and the confirm stays
 * disabled until something has been typed. There is no path through this that
 * sends work back without saying why.
 */
function sendBackControl(v, repaint) {
  const me = auth.account();
  // Only on a row that is actually claiming to be finished — there is nothing
  // to reject on one nobody has marked done.
  if (me?.role !== 'admin' || !auth.isSettled(v)) return el('span');

  const wrap = el('span', 'rt-sendback');
  const open = el('button', 'chip rt-sendback-open', 'Send back');
  open.type = 'button';
  open.title = 'Reject this as not finished, and say why.';
  wrap.append(open);

  open.onclick = () => {
    open.remove();
    const form = el('span', 'rt-sendback-form');
    const note = document.createElement('textarea');
    note.className = 'rt-sendback-note';
    note.rows = 2;
    note.placeholder = 'What is still wrong? This is what they will read.';

    const send = el('button', 'chip rt-sendback-send', 'Send back');
    send.type = 'button';
    send.disabled = true;
    const cancel = el('button', 'chip rt-sendback-cancel', 'Cancel');
    cancel.type = 'button';

    note.oninput = () => { send.disabled = !note.value.trim(); };
    cancel.onclick = () => { form.replaceWith(open); };

    send.onclick = async () => {
      send.disabled = true;
      try {
        const result = await auth.sendBackVerdict(v.id, note.value.trim());
        v.sent_back_at = result.sent_back_at;
        v.sent_back_by_name = result.sent_back_by_name;
        v.sent_back_note = result.sent_back_note;
        form.remove();
        repaint();
        // It is open work again, so the count above has to hear about it, and
        // the row loses the dimming that said it was finished.
        renderHeadline(filtered());
        redraw();
      } catch (error) {
        $('error').textContent = error.message;
        $('error').hidden = false;
        send.disabled = false;
      }
    };

    form.append(note, send, cancel);
    wrap.append(form);
    note.focus();
  };
  return wrap;
}

/**
 * Discard one of your own rows.
 *
 * Two presses, not one. Everything else on this page is reversible — a verdict
 * is answered by a later verdict, a closed item can be reopened — and this is
 * the only control that destroys something. It asks once, and gives up asking
 * after four seconds so a half-pressed button cannot sit there waiting to be
 * completed by a stray click much later.
 *
 * Shown only on your own rows, because the server refuses anybody else's and a
 * button that exists to be told no is worse than no button.
 */
function discardButton(v) {
  const me = auth.account();
  if (!me || v.account_id !== me.id) return el('span');

  let armed = null;
  const button = el('button', 'chip rt-discard', 'Discard');
  button.type = 'button';
  button.title = 'Remove this row. Only you can, and only this one.';

  const disarm = () => {
    clearTimeout(armed);
    armed = null;
    button.textContent = 'Discard';
    button.classList.remove('armed');
  };

  button.onclick = async () => {
    if (!armed) {
      button.textContent = 'Discard?';
      button.classList.add('armed');
      armed = setTimeout(disarm, 4000);
      return;
    }
    clearTimeout(armed);
    button.disabled = true;
    button.textContent = 'Discarding…';
    try {
      await auth.discardVerdict(v.id);
      // Gone from the store, so gone from the page — including the counts and
      // the pace chart above, which would otherwise still be describing it.
      state.all = state.all.filter((row) => row.id !== v.id);
      redraw();
    } catch (error) {
      $('error').textContent = error.message;
      $('error').hidden = false;
      button.disabled = false;
      disarm();
    }
  };
  return button;
}

// ── controls ─────────────────────────────────────────────────────────

function segment(host, options, key) {
  host.innerHTML = '';
  for (const [value, label] of options) {
    const b = el('button', null, label);
    b.type = 'button';
    if (state.filter[key] === value) b.classList.add('active');
    b.onclick = () => { state.filter[key] = value; redraw(); };
    host.append(b);
  }
}

function renderControls() {
  // Only the kinds anything has actually been reviewed in — the same rule as
  // the layers below. A button for a kind with nothing behind it says the
  // review covers ground it has not been near.
  const kinds = new Set(state.all.map((v) => v.target_kind));
  segment($('f-kind'),
    [['', 'All kinds'], ...Object.entries(KINDS).filter(([k]) => kinds.has(k))], 'kind');
  // Only the layers anything has actually been reviewed in — six empty buttons
  // would say the review is broader than it is.
  const used = new Set(state.all.map((v) => v.layer).filter(Boolean));
  if (used.size > 1) {
    segment($('f-layer'),
      [['', 'All layers'], ...Object.entries(LAYERS).filter(([k]) => used.has(k))], 'layer');
  }
  // Only offered once a client has actually reviewed something — until then it
  // is a filter with one populated side, which says a distinction is being made
  // that is not yet being made.
  if (state.all.some((v) => v.audience === 'client')) {
    segment($('f-audience'),
      [['', 'Both reviews'], ...Object.entries(AUDIENCES)], 'audience');
  }
  segment($('f-tag'), [['', 'Both sides'], ...Object.entries(TAGS)], 'tag');
  segment($('f-done'), [['', 'Open and done'], ['open', 'Open'], ['done', 'Done']], 'done');
  segment($('f-verdict'), [['', 'All verdicts'], ...VERDICTS.map((k) => [k, LABEL[k]])], 'verdict');

  const person = $('f-person');
  person.innerHTML = '';
  const seen = new Map();
  for (const v of state.all) seen.set(String(v.account_id), v.by || v.by_email);
  person.append(new Option('Everyone', ''));
  for (const [id, name] of seen) person.append(new Option(name, id));
  person.value = state.filter.person;
  person.onchange = () => { state.filter.person = person.value; redraw(); };

  const win = $('f-window');
  if (!win.options.length) {
    for (const [v, l] of [['', 'All time'], ['1', 'Last 24 hours'], ['7', 'Last 7 days'], ['30', 'Last 30 days']]) {
      win.append(new Option(l, v));
    }
    win.onchange = () => { state.filter.window = win.value; redraw(); };
  }

  const text = $('f-text');
  text.oninput = () => { state.filter.text = text.value; redraw(); };

  $('f-clear').onclick = () => {
    state.filter = { kind: '', layer: '', verdict: '', person: '', window: '', text: '' };
    text.value = '';
    win.value = '';
    renderControls();
    redraw();
  };

  $('f-export').onclick = () => exportCsv(filtered());
}

/** The filtered selection, as a file. Built in the page rather than served,
 *  so what you get is exactly what is on screen.
 *
 *  Every row is a verdict at a moment, not a current state — which is what
 *  makes the file worth having. A summary has already thrown away the
 *  revisions, the disagreement and the pace, and those are most of what says
 *  whether a review is going well. Oldest first, because a history read top to
 *  bottom should run forwards.
 *
 *  `layer` and `date` are here for the pivot a reader builds the moment they
 *  open it — how much of the frontend was signed off in a week against how much
 *  of the backend. Excel derives neither from a timestamp and a kind on its own.
 */
function exportCsv(rows) {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const day = (iso) => {
    const d = new Date(iso);
    return Number.isNaN(+d) ? '' : d.toISOString().slice(0, 10);
  };
  const ordered = [...rows].sort((a, b) => when(a.at) - when(b.at));
  const body = [
    ['when', 'date', 'review', 'layer', 'lands on', 'kind', 'artefact', 'verdict',
     'reviewer', 'email', 'status', 'our verdict', 'done on', 'done by',
     'sent back because', 'note'].join(','),
    ...ordered.map((v) => [
      v.at, day(v.at), AUDIENCES[v.audience ?? 'internal'] ?? v.audience,
      LAYERS[v.layer] ?? v.layer ?? '', TAGS[v.tag] ?? v.tag ?? '',
      KINDS[v.target_kind] ?? v.target_kind, v.target_id,
      LABEL[v.verdict] ?? v.verdict, v.by, v.by_email,
      auth.isSettled(v) ? 'Done' : v.sent_back_at ? 'Sent back' : 'Open',
      RESPONSE_LABEL[v.done_response] ?? v.done_response ?? '',
      v.done_at ? day(v.done_at) : '', v.done_by_name ?? '',
      v.sent_back_note ?? '',
      v.note,
    ].map(esc).join(',')),
  ].join('\r\n');

  // A BOM, because Excel on Windows reads a UTF-8 CSV as the system codepage
  // without one — and these notes are full of the em dashes and curly quotes
  // this package is written in, which would arrive as mojibake.
  const url = URL.createObjectURL(
    new Blob(['\uFEFF' + body], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  // The export is what is on screen — every filter above applies to it. Which
  // is right, and is exactly why the name has to say so: a filtered file called
  // ticvai-review-activity-2026-08-20.csv reads as the whole review a week
  // later, and nothing inside it says otherwise.
  // `day` is already the function that formats a row's date, so this one is
  // named for what it is rather than shadowing it.
  const narrowed = Object.values(state.filter).some(Boolean);
  const today = new Date().toISOString().slice(0, 10);
  a.download = `ticvai-review-activity-${today}${narrowed ? '-filtered' : ''}.csv`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function redraw() {
  const rows = filtered();
  renderHeadline(rows);
  renderPace(rows);
  renderContested(rows);
  renderPeople(rows);
  renderRows(rows);
  const LOOKUP = {
    kind: KINDS, layer: LAYERS, tag: TAGS, audience: AUDIENCES,
    done: { open: 'Open', done: 'Done' },
  };
  for (const host of [$('f-kind'), $('f-layer'), $('f-audience'), $('f-tag'),
    $('f-done'), $('f-verdict')]) {
    if (!host) continue;
    const key = {
      'f-kind': 'kind', 'f-layer': 'layer', 'f-audience': 'audience', 'f-tag': 'tag',
      'f-done': 'done', 'f-verdict': 'verdict',
    }[host.id];
    for (const b of host.querySelectorAll('button')) {
      const label = b.textContent;
      const value = /^(All|Both|Open and)/.test(label) ? '' :
        (LOOKUP[key] ? Object.entries(LOOKUP[key]).find(([, l]) => l === label)?.[0]
                     : VERDICTS.find((k) => LABEL[k] === label));
      b.classList.toggle('active', (value ?? '') === state.filter[key]);
    }
  }
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';
  try {
    const data = await auth.allVerdicts();
    state.all = data.verdicts ?? [];
    state.accounts = data.accounts ?? [];
  } catch (error) {
    $('error').textContent = `Could not read the verdicts: ${error.message}`;
    $('error').hidden = false;
  }
  renderControls();
  redraw();
  renderMentions();
})();
