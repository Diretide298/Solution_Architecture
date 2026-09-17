/**
 * The landing page: the copy that is data, the chain picker, and the three
 * animations started.
 *
 * Ported from the handoff's prototype component. The arrays are its own,
 * verbatim — their sources are listed in the handoff README — and the three
 * animation modules are the handoff's files, loaded as globals by the page.
 */

const ACCENT = '#04d8f2';

const HUMAN = [
  { n: '01', t: 'Requirement gathering', d: 'The client’s own documents, read once into one record per screen. Seventeen module documents, 1,058 pages, 59 boards, 590 screens — the largest single addition the package has absorbed.', a: 'sources/workshop/pack.json' },
  { n: '02', t: 'Workshops with the client', d: 'Every decision, action and confirmation pulled out of the minutes, with the ones not yet written into the package named. A decision taken in a room and not recorded costs the work twice.', a: 'Moms/ → decisions register' },
  { n: '03', t: 'Choosing the strategy', d: 'The principle is argued once and recorded as an ADR: the options that were on the table, what was chosen, and what that rules out. Forty-four of them so far.', a: 'docs/decisions/*.md' },
  { n: '04', t: 'Finalising it', d: 'What is still open is carried as a numbered conflict until it is answered. “Does this deserve a table?” is asked once per drafted write, with the field evidence beside it rather than a name match.', a: 'docs/registers/conflicts.md' },
  { n: '05', t: 'Updating it inside Adam', d: 'The answer is written into the contracts, screens, states and flows — not into a document beside them. Nine validators refuse the change if it disagrees with anything already there.', a: 'contracts/ screens/ states/ flows/' },
  { n: '06', t: 'Sign-off', d: 'A reviewer’s verdict is signed and kept against the artefact it is about, so the record of who accepted what lives with the thing accepted.', a: 'review verdicts' },
  { n: '07', t: 'Handoff to engineering', d: 'What is left to draw becomes a work list a design session reads instead of asking, and the whole graph becomes something a developer’s assistant can query.', a: 'handoff/ + the MCP bridge' },
];

const CHAIN = [
  { t: 'Lineage', tool: 'derive-lineage.py --apply', writes: 'handoff/api-data-lineage.json', why: 'Every operation gets what it reads, what it writes, its service and its stores. Twenty-plus tools treat this file as authoritative, so it runs first — an operation added to a contract is invisible to all of them until it does.' },
  { t: 'Schema', tool: 'derive-schema.py', writes: 'handoff/schema-reference.json', why: 'A schema declaring where it persists says which table it lands in, and its properties become that table’s columns. Nothing here is typed by hand.' },
  { t: 'Relationships', tool: 'derive-relationships.py', writes: 'handoff/relationship-graph.json', why: 'Every edge between tables, from three sources in order of authority: a reference declared on a column, a column name that resolves to a real table, and two tables written by one operation.' },
  { t: 'DDL', tool: 'derive-ddl.py --apply', writes: 'backend/**/*.sql', why: 'Postgres DDL generated from the schema reference — the control schema and the tenant template as separate artefacts, per the deployment decisions behind them.' },
  { t: 'Burst scope', tool: 'derive-burst-scope.py --apply', writes: 'handoff/burst-scope.json', why: 'What a flash-sale environment actually runs, taken from the flows already walked. Presence on the path is not the same as carrying the load, so services are weighted by calls per buyer.' },
  { t: 'Sizing', tool: 'derive-sizing.py --apply', writes: 'handoff/sizing.json', why: 'How many instances of what, under normal load and under a sale — two mixes, because a cell provisioned from the sale mix is backwards for 363 days of the year.' },
  { t: 'Table notes', tool: 'derive-table-notes.py --apply', writes: 'handoff/table-notes.json', why: 'Every table gets a note saying what it holds, what it hangs off and what reaches it. Notes used to go where somebody happened to be working rather than where a reader needs them.' },
  { t: 'Schema roots', tool: 'derive-schema-roots.py', writes: 'handoff/schema-roots.md', why: 'The primary table of each schema and how the rest hang off it. Not simply the most-referenced table — a gate is equipment, and the thing being admitted is the point.' },
  { t: 'Frontend', tool: 'derive-frontend.py', writes: 'frontend/<app>.yaml', why: 'The app manifests, from the screens: which platforms an app serves, which contracts it reaches through their operations, and the deployment posture its platform declares.' },
  { t: 'Board-panel map', tool: 'derive-board-panel-map.py', writes: 'handoff/board-panel-map.json', why: 'Every read panel on a board against the operation that serves it. A board panel is not an endpoint — three panels on one screen are usually one operation with a filter.' },
  { t: 'Diagrams', tool: 'derive-diagrams.py', writes: 'diagrams/hld.yaml, diagrams/lld/', why: 'A diagram is a view of the other layers, not a sixth kind of thing. Derived, never authored — a hand-maintained diagram is the one artefact that goes stale in silence.' },
  { t: 'Both workbooks', tool: 'build-schema-workbook.py, build-services-workbook.py', writes: 'handoff/*.xlsx', why: 'The schema reference as a workbook, and the one that carries the reasoning: how the tables were divided into schemas, and how those schemas became sixteen deployable services.' },
  { t: 'Wireframes', tool: 'derive-wireframes.py', writes: 'wireframes/<platform>.dc.html', why: 'A board per platform, generated from the screen definitions — which is the specification. A board is generated, not maintained, so redrawing one is just deleting it.' },
  { t: 'Workshop boards', tool: 'index-boards.py', writes: 'wireframes/board-index.json', why: 'One record per board, each with a hash, so a board is read once. A number that is expensive to derive gets derived carelessly; this derives them once and records them.' },
  { t: 'Id register', tool: 'derive-id-register.py --apply', writes: 'docs/registers/screen-ids.md', why: 'Every screen id that has been issued, so two workstreams cannot issue the same one. It happened: both sides computed max+1 over the screens they could see, and both were right.' },
];

const FIGURES = [
  { n: '1,628', t: 'operations' }, { n: '28', t: 'contracts' }, { n: '388', t: 'tables' },
  { n: '1,629', t: 'screens' }, { n: '125', t: 'state models' }, { n: '96', t: 'flows' },
  { n: '44', t: 'ADRs' },
];

const LAYERS = [
  { t: 'Frontend', d: 'Screens, journeys and the apps that implement them' },
  { t: 'Contracts', d: 'Spine, graph, structure, ER and the reader' },
  { t: 'Domain', d: 'State machines and the event catalogue that check each other' },
  { t: 'Backend', d: 'The migrations as they stand, and the data model as it is meant to become' },
];

const TOOLS = ['adam_search', 'adam_screen', 'adam_journey', 'adam_contract', 'adam_table', 'adam_service',
  'adam_module', 'adam_decisions', 'adam_file', 'adam_board', 'adam_work', 'adam_links', 'adam_link',
  'adam_pull', 'adam_propose', 'adam_apply'];

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
};

/* ── the copy that is data ─────────────────────────────────────────── */

function renderFigures() {
  const host = $('lp-figures');
  for (const f of FIGURES) {
    const cell = el('div', 'lp-figure');
    cell.append(el('b', null, f.n), el('span', null, f.t));
    host.append(cell);
  }
}

function renderJourney() {
  HUMAN.forEach((s, i) => {
    const li = el('li', 'lp-jcard');
    li.dataset.card = String(i + 1);
    const band = el('div', 'lp-jband');
    band.dataset.stage = String(i + 1);
    band.setAttribute('aria-hidden', 'true');
    li.append(el('span', 'lp-jnum', s.n), el('h3', null, s.t), band, el('p', null, s.d), el('span', 'lp-jpath', s.a));
    $(i < 4 ? 'lp-jrow-top' : 'lp-jrow-bottom').append(li);
  });
}

function renderReadBack() {
  for (const l of LAYERS) {
    const li = el('li');
    li.append(el('span', null, l.t), el('span', null, l.d));
    $('lp-layers').append(li);
  }
  for (const t of TOOLS) $('lp-tools').append(el('code', null, t));
}

/* ── the chain picker ──────────────────────────────────────────────── */

let chain = null;
let step = 1;

function renderChain() {
  const list = $('lp-chain-list');
  CHAIN.forEach((c, i) => {
    const n = i + 1;
    const li = el('li');
    const button = el('button', 'lp-step');
    button.type = 'button';
    button.dataset.step = String(n);
    button.append(
      el('span', 'lp-step-n', String(n).padStart(2, '0')),
      el('span', 'lp-step-t', c.t),
      el('span', 'lp-step-tool', c.tool),
    );
    // Hover picks, as in the design; click picks too, so touch and keyboard do.
    button.addEventListener('mouseenter', () => select(n));
    button.addEventListener('click', () => select(n));
    li.append(button);
    list.append(li);
  });
  select(1);
}

function select(n) {
  step = n;
  for (const b of document.querySelectorAll('.lp-step')) {
    b.classList.toggle('is-on', Number(b.dataset.step) === n);
  }
  const c = CHAIN[n - 1];
  $('lp-step-n').textContent = `Step ${String(n).padStart(2, '0')} of ${CHAIN.length}`;
  $('lp-step-t').textContent = c.t;
  $('lp-step-why').textContent = c.why;
  $('lp-step-tool').textContent = c.tool;
  $('lp-step-writes').textContent = c.writes;
  if (chain) chain.setStep(n);
}

/* ── the hero plate ────────────────────────────────────────────────── */

let scene = null;

// Full-bleed, measured rather than declared: 100vw counts the scrollbar
// gutter and puts the page into horizontal scroll.
function fit() {
  const plate = $('lp-plate');
  if (plate?.parentElement) {
    plate.style.marginLeft = '0px';
    plate.style.marginRight = '0px';
    const host = plate.parentElement.getBoundingClientRect();
    const cw = document.documentElement.clientWidth;
    plate.style.marginLeft = `-${Math.max(0, Math.round(host.left))}px`;
    plate.style.marginRight = `-${Math.max(0, Math.round(cw - host.right))}px`;
  }
  if (scene?.remeasureFlow) scene.remeasureFlow();
}

/* ── start ─────────────────────────────────────────────────────────── */

function whenGlobal(name, then, tries = 60) {
  if (window[name]) return then(window[name]);
  if (tries <= 0) return undefined;
  return setTimeout(() => whenGlobal(name, then, tries - 1), 100);
}

renderFigures();
renderJourney();
renderReadBack();
renderChain();
fit();
window.addEventListener('resize', fit);

whenGlobal('AdamFlow', (Flow) => {
  scene = Flow.start({ root: $('lp-stage'), assets: '/landing-assets/', accent: ACCENT, theme: 'Light', fps: 6 });
  fit();
});
whenGlobal('AdamChain', (Chain) => {
  chain = Chain.mount($('lp-chain-canvas'), { accent: ACCENT, theme: 'Light', fps: 6 });
  chain.setStep(step);
});
// The React diagrams draw inside the cards and the engine keeps the signal,
// the card light and the record lines. If the bundle is missing, the engine
// draws its own SVG diagrams instead, so the section never comes up empty.
whenGlobal('AdamJourney', (Journey) => {
  const host = $('lp-journey');
  const canvas = host.querySelector('canvas');
  import('/landing-journey/journey.js')
    .then((diagrams) => {
      diagrams.mount(host);
      Journey.mount(host, { canvas, accent: ACCENT, art: false });
    })
    .catch(() => Journey.mount(host, { canvas, accent: ACCENT }));
});
