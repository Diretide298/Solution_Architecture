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

const VERDICTS = ['approved', 'needs-work', 'rejected'];
const LABEL = { approved: 'Approved', 'needs-work': 'Needs work', rejected: 'Rejected' };
const COLOUR = { approved: '#4ade80', 'needs-work': '#fbbf24', rejected: '#f87171' };
const KINDS = { operation: 'APIs', table: 'Tables', screen: 'Wireframes', board: 'Boards' };

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
  filter: { kind: '', verdict: '', person: '', window: '', text: '' },
};

// ── filtering ────────────────────────────────────────────────────────

function filtered() {
  const f = state.filter;
  const needle = f.text.trim().toLowerCase();
  const cutoff = f.window ? Date.now() - Number(f.window) * DAY : null;
  return state.all.filter((v) => {
    if (f.kind && v.target_kind !== f.kind) return false;
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
        fill: COLOUR[k], rx: Math.min(2, bw * 0.2),
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
    dot.style.background = COLOUR[k];
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
      seg.style.background = COLOUR[k];
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

// ── the list ─────────────────────────────────────────────────────────

function renderRows(rows) {
  const host = $('rows');
  host.innerHTML = '';
  $('rows-note').textContent = `${rows.length} of ${state.all.length}`;

  if (!rows.length) {
    host.append(el('p', 'pane-empty', 'Nothing matches that.'));
    return;
  }

  let shown = 0;
  const PAGE = 60;
  const more = el('button', 'lineage-more');
  more.type = 'button';

  const draw = () => {
    for (const v of rows.slice(shown, shown + PAGE)) host.insertBefore(line(v), more);
    shown += Math.min(PAGE, rows.length - shown);
    const left = rows.length - shown;
    if (left > 0) more.textContent = `${left} more`;
    else more.remove();
  };
  more.onclick = draw;
  host.append(more);
  draw();
}

function line(v) {
  const row = el('div', 'response-row');
  row.append(el('span', `verdict-chip ${v.verdict}`, LABEL[v.verdict]));

  const main = el('span', 'signoff-row-main');
  const target = el('a', 'signoff-row-name', v.target_id);
  target.href = `/#${encodeURIComponent(
    v.target_kind === 'operation' ? v.target_id : `${v.target_kind}:${v.target_id}`)}`;
  main.append(target);
  if (v.note) main.append(el('span', 'response-note', v.note));
  else main.append(el('span', 'response-note response-note-empty', 'no reason given'));
  row.append(main);

  row.append(el('span', 'signoff-row-group', KINDS[v.target_kind] ?? v.target_kind));

  const who = el('span', 'signoff-row-who');
  who.append(el('span', null, v.by || v.by_email));
  who.append(el('span', 'signoff-row-when', fmt(when(v.at))));
  row.append(who);
  return row;
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
  segment($('f-kind'), [['', 'All kinds'], ...Object.entries(KINDS)], 'kind');
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
    state.filter = { kind: '', verdict: '', person: '', window: '', text: '' };
    text.value = '';
    win.value = '';
    renderControls();
    redraw();
  };

  $('f-export').onclick = () => exportCsv(filtered());
}

/** The filtered selection, as a file. Built in the page rather than served,
 *  so what you get is exactly what is on screen. */
function exportCsv(rows) {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const body = [
    ['when', 'kind', 'artefact', 'verdict', 'reviewer', 'email', 'note'].join(','),
    ...rows.map((v) => [v.at, v.target_kind, v.target_id, v.verdict, v.by, v.by_email, v.note]
      .map(esc).join(',')),
  ].join('\n');
  const url = URL.createObjectURL(new Blob([body], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  a.download = 'ticvai-review-activity.csv';
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
  for (const host of [$('f-kind'), $('f-verdict')]) {
    const key = host.id === 'f-kind' ? 'kind' : 'verdict';
    for (const b of host.querySelectorAll('button')) {
      const label = b.textContent;
      const value = label.startsWith('All') ? '' :
        (key === 'kind' ? Object.entries(KINDS).find(([, l]) => l === label)?.[0]
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
})();
