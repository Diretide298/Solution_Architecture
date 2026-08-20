// The overview joins two servers: the population from the reader, the verdicts
// from the accounts service. An artefact nobody has looked at exists in one and
// not the other, so the checks are mostly about the join — that "not reviewed"
// is a row rather than an absence, and that a row leads somewhere.
import puppeteer from 'puppeteer-core';
import { authed } from './_session.mjs';
const VIEWER = 'http://localhost:4173';
const API = 'http://localhost:8787';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
await page.setViewport({ width: 1400, height: 1000 });
await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate(async (api) => {
  await fetch(`${api}/api/auth/login`, {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
  });
}, API);

// The populations, straight from the reader, so the page's own numbers can be
// checked against something that did not come from the page.
const index = await (await authed(`${VIEWER}/api/index`)).json();
const backend = await (await authed(`${VIEWER}/api/backend`)).json();
const journeys = await (await authed(`${VIEWER}/api/journeys`)).json();
const domain = await (await authed(`${VIEWER}/api/domain`)).json();
const population = {
  operation: index.nodes.filter((n) => n.type === 'operation').length,
  table: (backend.tables ?? []).length,
  screen: (journeys.screens ?? []).length,
  board: (journeys.boards ?? []).length,
  // Added when the Domain and Backend layers gained a review of their own: a
  // state model and a schema are each judged once, not per state or per table.
  state: (domain.machines ?? []).length,
  schema: (backend.modules ?? []).length,
};

// One verdict of each kind, so every card has something in it. Recorded through
// the API rather than the UI — this harness is about the overview, not the
// verdict block, which extras-check already holds still.
const targets = {
  operation: index.nodes.find((n) => n.type === 'operation').name,
  table: backend.tables[0].name,
  screen: journeys.screens[0].id,
  board: journeys.boards[0].id,
  state: domain.machines[0].id,
  schema: backend.modules[0].name,
};
for (const [kind, id] of Object.entries(targets)) {
  const ok = await page.evaluate(async (api, k, i) => (await fetch(`${api}/api/validation`, {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ target_kind: k, target_id: i, verdict: 'approved', note: 'harness' }),
  })).ok, API, kind, id);
  if (!ok) throw new Error(`could not record a ${kind} verdict`);
}

await page.goto(`${VIEWER}/validation.html`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.signoff-card', { timeout: 25000 });
await wait(2500);

// ── the cards ────────────────────────────────────────────────────────
const cards = await page.evaluate(() => [...document.querySelectorAll('.signoff-card')].map((c) => ({
  label: c.querySelector('.signoff-card-label').textContent,
  count: c.querySelector('.signoff-card-count').textContent,
})));
// Driven by `population` rather than a hard-coded four. This read `=== 4` and
// broke the day the Domain and Backend layers gained a review of their own —
// a harness that has to be edited to admit a new kind is a harness that fails
// for the wrong reason, and it fails loudest exactly when something was added.
const KIND_ORDER = ['operation', 'table', 'screen', 'board', 'state', 'schema'];
check(`there is a card for each of the ${KIND_ORDER.length} kinds`,
  cards.length === KIND_ORDER.length, cards.map((c) => c.label).join(', '));

const denominators = cards.map((c) => Number(/of (\d+)/.exec(c.count)[1]));
const expected = KIND_ORDER.map((k) => population[k]);
check('each card counts against the whole population, not just what was judged',
  denominators.join(',') === expected.join(','),
  `${denominators.join(', ')} vs ${expected.join(', ')} from the reader`);

const numerators = cards.map((c) => Number(/^(\d+)/.exec(c.count)[1]));
check('and every kind now shows at least the one just recorded',
  numerators.every((n) => n >= 1), numerators.join(', '));

check('the summary says how many have never been looked at',
  /never been looked at/.test(await page.evaluate(() => document.getElementById('overall').textContent)));

// ── the list ─────────────────────────────────────────────────────────
const first = await page.evaluate(() => {
  const row = document.querySelector('.signoff-row');
  return { chip: row.querySelector('.verdict-chip').textContent, href: row.getAttribute('href') };
});
check('unreviewed artefacts are listed first — the list exists to find them',
  first.chip === 'Not reviewed', first.chip);

// filtering to the one that was judged
await page.evaluate((t) => {
  const input = document.getElementById('filter');
  input.value = t;
  input.dispatchEvent(new Event('input', { bubbles: true }));
}, targets.operation);
await wait(800);
const judged = await page.evaluate(() => {
  const row = [...document.querySelectorAll('.signoff-row')]
    .find((r) => r.querySelector('.verdict-chip').textContent === 'Approved');
  return row ? { name: row.querySelector('.signoff-row-name').textContent, who: row.querySelector('.signoff-row-who').textContent } : null;
});
check('a judged artefact shows its verdict and who gave it',
  judged !== null && /harness/i.test(judged.who), judged ? `${judged.name} · ${judged.who}` : 'not found');

// "only what still needs a verdict" must exclude it
await page.evaluate(() => {
  document.getElementById('filter').value = '';
  document.getElementById('filter').dispatchEvent(new Event('input', { bubbles: true }));
  const box = document.getElementById('only-open');
  box.checked = true;
  box.dispatchEvent(new Event('change', { bubbles: true }));
});
await wait(800);
const open = await page.evaluate(() => ({
  any: [...document.querySelectorAll('.signoff-row .verdict-chip')].some((c) => c.textContent !== 'Not reviewed'),
  note: document.getElementById('listing-note').textContent,
}));
check('"only what still needs a verdict" shows nothing already judged', !open.any, open.note);

// ── the deep links ───────────────────────────────────────────────────
// A row that leads nowhere is worse than no row, and three of the four kinds
// had no hash of their own until this page needed one.
for (const [kind, expectMode] of [['table', 'data'], ['screen', 'screen'], ['board', 'screen']]) {
  await page.goto(`${VIEWER}/validation.html`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('.signoff-card', { timeout: 25000 });
  await wait(2000);
  const label = { table: 'Tables', screen: 'Wireframes', board: 'Design boards' }[kind];
  await page.evaluate((l) => {
    [...document.querySelectorAll('.signoff-card')]
      .find((c) => c.querySelector('.signoff-card-label').textContent === l).click();
  }, label);
  await wait(700);
  const href = await page.evaluate(() => document.querySelector('.signoff-row').getAttribute('href'));
  await page.goto(`${VIEWER}${href}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(4000);
  const landed = await page.evaluate(() => ({
    layer: window.__state.layer, mode: window.__state.mode,
    table: window.__state.tableName, screen: window.__state.screenId, board: window.__state.boardId,
  }));
  const target = decodeURIComponent(href.slice(2)).slice(kind.length + 1);
  const arrived = kind === 'table' ? landed.table === target
    : kind === 'screen' ? landed.screen === target
    : landed.board === target;
  check(`a ${kind} row opens that ${kind} in the viewer`,
    arrived && landed.mode === expectMode,
    `${href} → ${landed.layer}/${landed.mode} · ${landed.table ?? landed.screen ?? landed.board}`);
}

// an operation still routes the way it always did
{
  const node = index.nodes.find((n) => n.type === 'operation' && n.name === targets.operation);
  await page.goto(`${VIEWER}/#${encodeURIComponent(node.id)}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(3000);
  check('and an operation row still routes by node id, as it always did',
    await page.evaluate((id) => window.__state.selectedId === id, node.id), node.id);
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
