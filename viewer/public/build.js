/**
 * Build — the package, in the order it is made.
 *
 * One view. The steps of `tools/refresh.sh` trickle down the left, one at a
 * time, and the contracts stay pinned on the right because every step resolves
 * back to them. The step in focus draws a line to each earlier step it reads,
 * and to the contracts when it reads those directly — which is the argument of
 * the whole package made visible: nothing here was typed twice.
 *
 * Nothing on a card is transcribed. The payload is built in `lib/build.mjs`
 * from the script, the tools' own docstrings and the files on disk.
 */

import * as auth from '/validation.js';
import { LAYERS } from '/core.js';

const MODE = 'build-chronology';
const PLAY_MS = 4200;

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
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  return node;
};

const fmt = (n) => (typeof n === 'number' ? n.toLocaleString('en-GB') : String(n ?? ''));

const bytes = (n) => {
  if (!n) return null;
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(n < 10240 ? 1 : 0)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
};

const when = (ms) => (ms
  ? new Date(ms).toLocaleString('en-GB', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
  : null);

/** `**bold**` and `` `code` `` as elements, everything else as text — never as
 *  HTML, because every string here came out of a file in the package. */
function rich(raw) {
  const frag = document.createDocumentFragment();
  for (const part of String(raw ?? '').split(/(\*\*[^*]+\*\*|`[^`]+`)/g)) {
    if (!part) continue;
    if (part.startsWith('**')) frag.append(el('strong', null, part.slice(2, -2)));
    else if (part.startsWith('`')) frag.append(el('code', null, part.slice(1, -1)));
    else frag.append(document.createTextNode(part));
  }
  return frag;
}

const reduceMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function viewLabel(open) {
  const layer = LAYERS.find((l) => l.key === open.layer);
  const mode = layer?.modes.find(([m]) => m === open.mode);
  return layer && mode ? `${layer.label} · ${mode[1]}` : `${open.layer} · ${open.mode}`;
}

/** Into the real view, in place. The href is there for a middle click. */
function openLink(open, className, text) {
  const a = el('a', className, text ?? `Open ${viewLabel(open)}`);
  a.href = `${location.pathname}?layer=${encodeURIComponent(open.layer)}&mode=${encodeURIComponent(open.mode)}`;
  a.addEventListener('click', (event) => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
    event.preventDefault();
    import('/app.js').then((m) => m.setMode(open.mode)).catch(() => { location.href = a.href; });
  });
  return a;
}

/* ── the view ─────────────────────────────────────────────────────────── */

const ui = {
  host: null,
  data: null,
  flow: null,
  wires: null,
  aside: null,
  items: [],      // one per step, plus the finale
  step: 0,
  showAll: false,
  timer: null,
  counter: null,
  actLabel: null,
  playButton: null,
  allButton: null,
  frame: 0,
};

function renderHero(col) {
  const hero = el('section', 'bld-hero');
  hero.append(el('p', 'bld-eyebrow', 'Build · contracts to a running package'));
  hero.append(el('h1', 'bld-title', 'How the package is made, in order'));
  const sub = el('p', 'bld-sub');
  sub.append(rich(
    'Every step below is a tool in `tools/refresh.sh`, shown in the order the script runs it. '
    + 'Each one reads what the steps before it wrote, and the contracts on the right are where '
    + 'all of it starts. **Nothing downstream is typed by hand**, so a change to a contract '
    + 'reaches every screen, table and document by running the script again.',
  ));
  hero.append(sub);
  const src = el('p', 'bld-source');
  src.append(rich('Read live from **tools/refresh.sh** · each tool’s own docstring · the files each step writes'));
  hero.append(src);
  col.append(hero);
}

function renderTotals(col, data) {
  const row = el('div', 'bld-totals');
  const add = (value, label) => {
    const box = el('div', 'bld-total');
    box.append(el('b', null, fmt(value)), el('span', null, label));
    row.append(box);
  };
  add(data.stats.contracts, 'contracts');
  add(data.stats.operations, 'operations');
  add(data.stats.stages, 'steps');
  add(data.stats.tools, 'tools in the run');
  add(data.stats.outputs, 'files written');
  add(data.stats.checks, 'checks after');
  col.append(row);
}

function renderStage(stage, index, data) {
  const li = el('li', 'bld-stage is-pending');
  li.dataset.index = String(index);
  li.dataset.key = stage.key;
  li.style.setProperty('--i', String(index));

  li.append(el('span', 'bld-node'));

  const head = el('header', 'bld-head');
  head.append(el('span', 'bld-num', String(index + 1).padStart(2, '0')));
  head.append(el('h3', 'bld-name', stage.label));
  if (stage.line) head.append(el('span', 'bld-line', `refresh.sh:${stage.line}`));
  else head.append(el('span', 'bld-line is-gone', 'not in the script'));
  head.addEventListener('click', () => setStep(index));
  li.append(head);

  const body = el('div', 'bld-body');

  if (stage.figure) {
    const fig = el('div', 'bld-figure');
    fig.append(el('b', null, fmt(stage.figure.value)), el('span', null, stage.figure.unit));
    body.append(fig);
  }

  // The step's namesake speaks for it when there is one — Wireframes is six
  // helpers and `derive-wireframes`, and the helpers are not what it is.
  const lead = stage.tools.find((t) => t.summary && t.name === `derive-${stage.key}`)
    ?? stage.tools.find((t) => t.summary) ?? null;
  if (lead) body.append(el('p', 'bld-summary', rich(lead.summary)));

  const reads = el('div', 'bld-reads');
  reads.append(el('span', 'bld-label', 'Reads'));
  if (stage.readsContracts) {
    const chip = el('span', 'bld-chip is-contracts', 'contracts/');
    reads.append(chip);
  }
  for (const key of stage.upstream) {
    const at = data.stages.findIndex((s) => s.key === key);
    if (at < 0) continue;
    const chip = el('button', 'bld-chip', data.stages[at].label);
    chip.type = 'button';
    chip.title = `Step ${at + 1}`;
    chip.addEventListener('click', () => setStep(at));
    reads.append(chip);
  }
  if (reads.childElementCount === 1) reads.append(el('span', 'bld-muted', 'the package’s own sources'));
  body.append(reads);

  const tools = el('ul', 'bld-tools');
  for (const tool of stage.tools) {
    const item = el('li', tool.inScript ? 'bld-tool' : 'bld-tool is-gone');
    item.append(el('code', null, tool.file));
    if (tool.lines) item.append(el('span', 'bld-muted', `${fmt(tool.lines)} lines`));
    if (tool.summary && tool !== lead) item.title = tool.summary.replace(/\*\*|`/g, '');
    tools.append(item);
  }
  body.append(tools);

  if (stage.note || stage.trailing) {
    const why = el('details', 'bld-why');
    why.append(el('summary', null, 'Why it runs here'));
    if (stage.note) {
      for (const para of stage.note.split(/\n(?=\*\*)|\n\s*\n/)) {
        why.append(el('p', null, rich(para.replace(/\n/g, ' '))));
      }
    }
    if (stage.trailing) why.append(el('p', 'bld-muted', rich(stage.trailing)));
    why.addEventListener('toggle', scheduleWires);
    body.append(why);
  }

  const writes = el('ul', 'bld-writes');
  for (const w of stage.writes) {
    const item = el('li', w.files ? null : 'is-missing');
    item.append(el('code', null, w.pattern));
    const facts = [];
    if (w.pattern.includes('*')) facts.push(`${fmt(w.files)} ${w.files === 1 ? 'file' : 'files'}`);
    if (!w.files) facts.push('not on disk');
    if (bytes(w.bytes)) facts.push(bytes(w.bytes));
    if (when(w.modified)) facts.push(when(w.modified));
    item.append(el('span', 'bld-muted', facts.join(' · ')));
    writes.append(item);
  }
  const writesWrap = el('div', 'bld-writes-wrap');
  writesWrap.append(el('span', 'bld-label', 'Writes'), writes);
  body.append(writesWrap);

  if (stage.open) body.append(openLink(stage.open, 'bld-open'));

  li.append(body);
  return li;
}

function renderFinale(data, index) {
  const li = el('li', 'bld-stage bld-finale is-pending');
  li.dataset.index = String(index);
  li.style.setProperty('--i', String(index));
  li.append(el('span', 'bld-node'));

  const head = el('header', 'bld-head');
  head.append(el('span', 'bld-num', '✓'));
  head.append(el('h3', 'bld-name', 'Checked, then shipped'));
  head.addEventListener('click', () => setStep(index));
  li.append(head);

  const body = el('div', 'bld-body');
  body.append(el('p', 'bld-summary', rich(
    `The run ends with **${fmt(data.checks.length)} checks**, each reporting on its own so one failure `
    + 'cannot hide the rest. What passes is what a commit carries into the pipeline.',
  )));
  const checks = el('div', 'bld-checks');
  for (const name of data.checks) checks.append(el('code', 'bld-chip is-check', name));
  body.append(checks);

  if (data.also.length) {
    const also = el('details', 'bld-why');
    also.append(el('summary', null, `Also in the run · ${data.also.length} more tools`));
    const list = el('div', 'bld-checks');
    for (const t of data.also) {
      const chip = el('code', 'bld-chip', t.tool === '@inline' ? 'screen index' : t.tool);
      chip.title = `refresh.sh:${t.line}`;
      list.append(chip);
    }
    also.append(list);
    also.addEventListener('toggle', scheduleWires);
    body.append(also);
  }

  body.append(openLink({ layer: 'cicd', mode: 'cicd-pipeline' }, 'bld-open bld-ship', 'Ship it → CI/CD pipeline'));
  li.append(body);
  return li;
}

function renderContracts(aside, data) {
  const head = el('div', 'bld-aside-head');
  head.append(el('span', 'bld-label', 'Contracts'));
  head.append(el('span', 'bld-muted', `${fmt(data.stats.contracts)} files · ${fmt(data.stats.operations)} operations`));
  aside.append(head);
  aside.append(el('p', 'bld-aside-note', 'Hand-authored OpenAPI. The only input every step resolves back to.'));

  const max = Math.max(1, ...data.contracts.map((c) => c.operations));
  let tier = null;
  let list = null;
  data.contracts.forEach((c, i) => {
    if (c.tier !== tier) {
      tier = c.tier;
      aside.append(el('p', 'bld-tier', tier ?? 'other'));
      list = el('ul', 'bld-contract-list');
      aside.append(list);
    }
    const row = el('li', 'bld-contract');
    row.style.setProperty('--i', String(i));
    row.style.setProperty('--w', `${Math.max(3, Math.round((c.operations / max) * 100))}%`);
    row.title = c.title ? `${c.title} — ${c.file}` : c.file;
    row.append(el('span', 'bld-contract-name', c.name));
    row.append(el('span', 'bld-contract-ops', c.operations ? fmt(c.operations) : '—'));
    row.append(el('span', 'bld-contract-bar'));
    list.append(row);
  });
  aside.append(openLink({ layer: 'contracts', mode: 'graph' }, 'bld-open', 'Open the contracts'));
}

function renderControls(col) {
  const bar = el('div', 'bld-controls');
  const btn = (label, title, onClick, className = 'bld-btn') => {
    const b = el('button', className, label);
    b.type = 'button';
    b.title = title;
    b.addEventListener('click', onClick);
    bar.append(b);
    return b;
  };
  btn('←', 'Previous step (←)', () => setStep(ui.step - 1));
  ui.playButton = btn('Play', 'Play through (space)', togglePlay, 'bld-btn is-primary');
  btn('→', 'Next step (→)', () => setStep(ui.step + 1));
  ui.counter = el('span', 'bld-counter');
  ui.actLabel = el('span', 'bld-act-now');
  const where = el('span', 'bld-where');
  where.append(ui.counter, ui.actLabel);
  bar.append(where);
  btn('Restart', 'Back to the first step (Home)', () => { ui.showAll = false; setStep(0); }, 'bld-btn is-quiet');
  ui.allButton = btn('Show all', 'Reveal every step at once', () => {
    ui.showAll = !ui.showAll;
    applyStep();
  }, 'bld-btn is-quiet');
  btn('Present', 'Full screen', () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else ui.host.requestFullscreen?.().catch(() => {});
  }, 'bld-btn is-quiet');
  col.append(bar);
}

/* ── moving through it ────────────────────────────────────────────────── */

function setStep(index, { scroll = true } = {}) {
  const last = ui.items.length - 1;
  ui.step = Math.max(0, Math.min(last, index));
  applyStep();
  if (scroll) {
    ui.items[ui.step]?.scrollIntoView({ block: 'center', behavior: reduceMotion() ? 'auto' : 'smooth' });
  }
  if (ui.step === last) stopPlay();
}

function applyStep() {
  const { data, step } = ui;
  const active = data.stages[step] ?? null;
  const upstream = new Set(active?.upstream ?? []);
  ui.items.forEach((li, i) => {
    li.classList.toggle('is-active', i === step);
    li.classList.toggle('is-done', i < step);
    li.classList.toggle('is-pending', i > step && !ui.showAll);
    li.classList.toggle('is-upstream', upstream.has(li.dataset.key));
  });
  for (const act of ui.flow.querySelectorAll('.bld-act')) {
    act.classList.toggle('is-pending', Number(act.dataset.first) > step && !ui.showAll);
  }
  ui.aside.classList.toggle('is-lit', Boolean(active?.readsContracts) || step === 0);
  ui.counter.textContent = step < data.stages.length
    ? `Step ${step + 1} of ${data.stages.length}`
    : 'Checks';
  const act = active ? data.acts.find((a) => a.key === active.act) : null;
  ui.actLabel.textContent = act ? act.label : 'Ship';
  ui.allButton.textContent = ui.showAll ? 'Step through' : 'Show all';
  scheduleWires();
}

function togglePlay() {
  if (ui.timer) { stopPlay(); return; }
  if (ui.step >= ui.items.length - 1) setStep(0);
  ui.timer = setInterval(() => setStep(ui.step + 1), PLAY_MS);
  ui.playButton.textContent = 'Pause';
  ui.playButton.classList.add('is-on');
}

function stopPlay() {
  if (ui.timer) clearInterval(ui.timer);
  ui.timer = null;
  if (ui.playButton) {
    ui.playButton.textContent = 'Play';
    ui.playButton.classList.remove('is-on');
  }
}

function onKey(event) {
  if (document.body.dataset.mode !== MODE || !ui.data) return;
  if (event.metaKey || event.ctrlKey || event.altKey) return;
  const target = event.target;
  if (target instanceof HTMLElement && target.closest('input, textarea, select, [contenteditable="true"]')) return;
  const moves = {
    ArrowRight: () => setStep(ui.step + 1),
    ArrowLeft: () => setStep(ui.step - 1),
    Home: () => setStep(0),
    End: () => setStep(ui.items.length - 1),
    ' ': togglePlay,
  };
  const move = moves[event.key];
  if (!move) return;
  event.preventDefault();
  event.stopPropagation();
  move();
}

/* ── the lines ────────────────────────────────────────────────────────── */

function scheduleWires() {
  if (ui.frame) return;
  ui.frame = requestAnimationFrame(() => {
    ui.frame = 0;
    drawWires();
  });
}

/**
 * From the step in focus to what it reads. Earlier steps are joined by an arc
 * in the left gutter, so the lines run up the rail the steps came down; the
 * contracts by a curve across to the pinned column, aimed at the part of it
 * that is level with the card.
 */
function drawWires() {
  const svg = ui.wires;
  if (!svg || !ui.data) return;
  svg.replaceChildren();
  if (getComputedStyle(svg).display === 'none') return;

  const box = ui.flow.getBoundingClientRect();
  svg.setAttribute('viewBox', `0 0 ${box.width} ${box.height}`);
  svg.setAttribute('width', box.width);
  svg.setAttribute('height', box.height);

  const li = ui.items[ui.step];
  const stage = ui.data.stages[ui.step];
  if (!li || !stage) return;
  const card = li.getBoundingClientRect();
  const y1 = card.top - box.top + Math.min(34, card.height / 2);
  const x1 = card.left - box.left;

  stage.upstream.forEach((key, n) => {
    const from = ui.items.find((item) => item.dataset.key === key);
    if (!from || from.classList.contains('is-pending')) return;
    const r = from.getBoundingClientRect();
    const y2 = r.top - box.top + Math.min(34, r.height / 2);
    const x2 = r.left - box.left;
    const bend = 22 + Math.min(40, Math.abs(y1 - y2) / 18) + n * 5;
    svg.append(svgEl('path', {
      class: 'bld-wire',
      d: `M ${x1} ${y1} C ${x1 - bend} ${y1}, ${x2 - bend} ${y2}, ${x2} ${y2}`,
      style: `--n:${n}`,
    }));
    svg.append(svgEl('circle', { class: 'bld-wire-end', cx: x2, cy: y2, r: 3.5 }));
  });

  if (stage.readsContracts) {
    const aside = ui.aside.getBoundingClientRect();
    const x2 = aside.left - box.left;
    const top = aside.top - box.top + 24;
    const bottom = aside.bottom - box.top - 24;
    const y2 = Math.max(top, Math.min(bottom, y1));
    const x0 = card.right - box.left;
    const mid = (x0 + x2) / 2;
    svg.append(svgEl('path', {
      class: 'bld-wire is-contracts',
      d: `M ${x0} ${y1} C ${mid} ${y1}, ${mid} ${y2}, ${x2} ${y2}`,
    }));
    svg.append(svgEl('circle', { class: 'bld-wire-end is-contracts', cx: x2, cy: y2, r: 4 }));
  }
}

/* ── drawing it once ──────────────────────────────────────────────────── */

async function render(host) {
  ui.host = host;
  const col = el('div', 'bld-col');
  host.append(col);
  renderHero(col);

  let data = null;
  try {
    const res = await auth.apiFetch('/api/build');
    if (!res.ok) throw new Error(`/api/build answered ${res.status}`);
    data = await res.json();
  } catch (err) {
    col.append(el('div', 'bld-error', `Could not read the build payload: ${err.message}`));
    return;
  }
  if (!data?.present) {
    col.append(el('div', 'bld-error',
      'This package has no tools/refresh.sh, so there is no order to show. The chronology is read '
      + 'from that script and nothing else states it.'));
    return;
  }
  ui.data = data;

  renderTotals(col, data);

  const flow = el('div', 'bld-flow');
  ui.flow = flow;
  const list = el('ol', 'bld-stages');
  let act = null;
  data.stages.forEach((stage, i) => {
    if (stage.act !== act) {
      act = stage.act;
      const about = data.acts.find((a) => a.key === act);
      const head = el('li', 'bld-act');
      head.dataset.first = String(i);
      head.append(el('span', 'bld-act-name', about?.label ?? act));
      if (about?.blurb) head.append(el('span', 'bld-act-blurb', about.blurb));
      list.append(head);
    }
    const li = renderStage(stage, i, data);
    ui.items.push(li);
    list.append(li);
  });
  const finale = renderFinale(data, data.stages.length);
  ui.items.push(finale);
  list.append(finale);

  const aside = el('aside', 'bld-contracts');
  ui.aside = aside;
  renderContracts(aside, data);

  const wires = svgEl('svg', { class: 'bld-wires', 'aria-hidden': 'true' });
  ui.wires = wires;

  flow.append(list, aside, wires);
  col.append(flow);
  renderControls(col);

  host.addEventListener('scroll', scheduleWires, { passive: true });
  window.addEventListener('resize', scheduleWires);
  window.addEventListener('keydown', onKey, true);
  document.addEventListener('fullscreenchange', () => {
    host.classList.toggle('is-presenting', document.fullscreenElement === host);
    scheduleWires();
  });
  if ('ResizeObserver' in window) new ResizeObserver(scheduleWires).observe(flow);

  setStep(0, { scroll: false });
}

let drawn = null;

/** Draw once; `app.js` calls this every time the tab is shown. Coming back to
 *  the tab has to re-aim the lines, since nothing was measurable while hidden. */
export function show(mode) {
  if (mode !== MODE) return Promise.resolve();
  if (drawn) {
    scheduleWires();
    return drawn;
  }
  const host = $(`view-${mode}`);
  if (!host) return Promise.resolve();
  drawn = render(host).catch((err) => {
    host.append(el('div', 'bld-error', `Could not draw this view: ${err.message}`));
  });
  return drawn;
}

/** Called when the tab is left, so a presentation does not keep advancing
 *  behind a view nobody is looking at. */
export function hide() {
  stopPlay();
}
