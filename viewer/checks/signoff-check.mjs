// Where the review stands: the Reviews page's coverage, its list of every
// artefact, and the address that used to be the sign-off page.
//
// The coverage joins two servers: the population from the reader, the verdicts
// from the accounts service. An artefact nobody has looked at exists in one and
// not the other, so the checks are mostly about the join — that "not reviewed"
// is a row rather than an absence, that a row leads somewhere, and (since the
// merge into reviews.html on 14 Oct) that an ask somebody answered reads as
// fixed rather than as the ask, and that a kind the reader could not serve is
// said rather than counted as empty.
//
// Writes verdicts, so it runs against a scratch store. Ports come from the
// environment like every other check:
//   TICVAI_VIEWER=http://localhost:4173 TICVAI_API=http://localhost:8787 node checks/signoff-check.mjs
// With TICVAI_API set to the viewer's own origin, the viewer forwards the
// accounts routes and the page reads both from one address.
import puppeteer from 'puppeteer-core';
import { authed, VIEWER as V, API as A } from './_session.mjs';
const VIEWER = V.replace(/\/+$/, '');
const API = A.replace(/\/+$/, '');
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
// `ticvai-api` moves the accounts service *and* the package together, so it is
// only set when both live at the viewer's address; otherwise the page's own
// defaults (accounts on :8787, the package on this origin) are what is tested.
await page.evaluate((v, a) => { if (a === v) localStorage.setItem('ticvai-api', ''); }, VIEWER, API);
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
  state: (domain.machines ?? []).length,
  schema: (backend.modules ?? []).length,
};

const post = (path, body) => page.evaluate(async (api, p, b) => {
  const r = await fetch(`${api}${p}`, {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
    body: JSON.stringify(b),
  });
  return { ok: r.ok, body: await r.json().catch(() => null) };
}, API, path, body);

// One verdict of each kind, so every kind has something in it. Recorded through
// the API rather than the UI — this harness is about the overview, not the
// verdict block, which verdict-submit-check holds still.
//
// Each target is one nobody has judged yet, so a store that already holds a
// review (an open ask on the first table, say) cannot decide what the page
// shows for it.
const judgedAlready = await page.evaluate(async (api) => {
  const r = await fetch(`${api}/api/verdicts`, { credentials: 'include' });
  return (await r.json()).verdicts.map((v) => `${v.target_kind} ${v.target_id}`);
}, API);
const seen = new Set(judgedAlready);
const fresh = (kind, ids) => ids.find((id) => !seen.has(`${kind} ${id}`)) ?? ids[0];
const targets = {
  operation: fresh('operation', index.nodes.filter((n) => n.type === 'operation').map((n) => n.name)),
  table: fresh('table', backend.tables.map((t) => t.name)),
  screen: fresh('screen', journeys.screens.map((x) => x.id)),
  board: fresh('board', journeys.boards.map((x) => x.id)),
  state: fresh('state', domain.machines.map((m) => m.id)),
  schema: fresh('schema', backend.modules.map((m) => m.name)),
};
for (const [kind, id] of Object.entries(targets)) {
  const r = await post('/api/validation', { target_kind: kind, target_id: id, verdict: 'approved', note: 'harness' });
  if (!r.ok) throw new Error(`could not record a ${kind} verdict`);
}

const KIND_ORDER = ['operation', 'table', 'screen', 'board', 'state', 'schema'];
const LABEL = { operation: 'APIs', table: 'Tables', screen: 'Wireframes', board: 'Design boards', state: 'State models', schema: 'Schemas' };

const open = async (path, ready = '.rv-cov-row') => {
  await page.goto(`${VIEWER}${path}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector(ready, { timeout: 40000 });
  await wait(1200);
};
const typeSearch = async (text) => {
  await page.evaluate((t) => {
    const input = document.querySelector('#rv-scope input[type="search"]');
    input.value = t;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }, text);
  await wait(900);
};

// ── coverage, against the whole population ───────────────────────────
await open('/reviews.html#coverage');
const numbers = await page.evaluate(() => [...document.querySelectorAll('#rv-numbers tbody tr')].map((tr) => ({
  label: tr.querySelector('th').textContent,
  cells: [...tr.querySelectorAll('td')].map((td) => td.textContent),
})));
const byLabel = Object.fromEntries(numbers.map((r) => [r.label, r.cells]));
const num = (s) => Number(String(s).replace(/[^\d]/g, ''));
check(`coverage has a row for each of the ${KIND_ORDER.length} kinds`,
  KIND_ORDER.every((k) => byLabel[LABEL[k]]), numbers.map((r) => r.label).join(', '));
const denominators = KIND_ORDER.map((k) => num(byLabel[LABEL[k]]?.[0]));
check('each kind counts against the whole population, not just what was judged',
  denominators.join(',') === KIND_ORDER.map((k) => population[k]).join(','),
  `${denominators.join(', ')} vs ${KIND_ORDER.map((k) => population[k]).join(', ')} from the reader`);
// cells: artefacts, approved, open, fixed, never reviewed, have a verdict
const judged = KIND_ORDER.map((k) => num(byLabel[LABEL[k]]?.[0]) - num(byLabel[LABEL[k]]?.[4]));
check('and every kind now shows at least the one just recorded', judged.every((n) => n >= 1), judged.join(', '));
check('the opening says how many have never been looked at',
  /never been looked at/.test(await page.evaluate(() => document.getElementById('rv-verdict').textContent)));
const bars = await page.evaluate(() => [...document.querySelectorAll('#rv-cov .rv-cov-row')].map((r) => r.querySelector('.rv-cov-label').textContent));
check('the bold chart has one bar per kind, with a legend', bars.length === KIND_ORDER.length
  && await page.evaluate(() => document.querySelectorAll('#rv-cov-legend .sh-legend-item').length === 4), bars.join(', '));
const sides = await page.evaluate(() => [...document.querySelectorAll('#rv-scope .sh-switch button')].map((b) => `${b.textContent}:${b.getAttribute('aria-pressed')}`));
check('whose review is a switch, with the pressed one said', sides.join(',') === 'Both:true,The team:false,The client:false', sides.join(', '));

// ── every artefact ─────────────────────────────────────────────────────
await open('/reviews.html#artefacts', '.rv-art-row');
const first = await page.evaluate(() => document.querySelector('#rv-art .rv-art-row .sh-badge').textContent);
check('unreviewed artefacts are listed first — the list exists to find them', first === 'Not reviewed', first);

await typeSearch(targets.operation);
const found = await page.evaluate((name) => {
  const row = [...document.querySelectorAll('#rv-art .rv-art-row')]
    .find((r) => r.querySelector('.rv-art-link').textContent === name);
  return row ? { badge: row.querySelector('.sh-badge').textContent, who: row.lastElementChild.textContent } : null;
}, targets.operation);
check('a judged artefact shows its verdict and who gave it',
  found?.badge === 'Approved' && /harness/i.test(found.who), found ? `${found.badge} · ${found.who}` : 'not found');
check('and the search is in the address, so the view is a link to send',
  new URL(page.url()).searchParams.get('q') === targets.operation, page.url());

await typeSearch('');
await page.evaluate(() => {
  const box = document.getElementById('rv-only-open');
  box.checked = true;
  box.dispatchEvent(new Event('change', { bubbles: true }));
});
await wait(800);
const onlyOpen = await page.evaluate(() => ({
  any: [...document.querySelectorAll('#rv-art .rv-art-row .sh-badge')].some((c) => c.textContent !== 'Not reviewed'),
  rows: document.querySelectorAll('#rv-art .rv-art-row').length,
  note: document.getElementById('rv-art-note').textContent,
}));
check('"only those with no verdict" shows nothing already judged', !onlyOpen.any && onlyOpen.rows > 0, onlyOpen.note);

// ── an answered ask reads as fixed, not as the ask ───────────────────
{
  const target = backend.tables.map((t) => t.name).find((n) => !seen.has(`table ${n}`) && n !== targets.table);
  const asked = await post('/api/validation', { target_kind: 'table', target_id: target, verdict: 'needs-work', note: 'harness: fix me' });
  await open(`/reviews.html?kind=table&q=${encodeURIComponent(target)}#artefacts`, '.rv-art-row');
  const before = await page.evaluate((t) => [...document.querySelectorAll('#rv-art .rv-art-row')]
    .find((r) => r.querySelector('.rv-art-link').textContent === t)?.querySelector('.sh-badge').textContent, target);
  await post(`/api/verdicts/${asked.body.id}/done`, { done: true, response: 'built' });
  // The same address with a hash is a same-document navigation, which would
  // leave the page as it was; leaving first makes the second visit a load.
  await page.goto('about:blank');
  await open(`/reviews.html?kind=table&q=${encodeURIComponent(target)}#artefacts`, '.rv-art-row');
  const after = await page.evaluate((t) => [...document.querySelectorAll('#rv-art .rv-art-row')]
    .find((r) => r.querySelector('.rv-art-link').textContent === t)?.querySelector('.sh-badge').textContent, target);
  check('a needs-work somebody marked built says "Fixed", not "Needs work"',
    before === 'Needs work' && after === 'Fixed', `${before} → ${after}`);
}

// ── the deep links ───────────────────────────────────────────────────
// A row that leads nowhere is worse than no row.
for (const [kind, expectMode] of [['table', 'data'], ['screen', 'screen'], ['board', 'screen']]) {
  await open(`/reviews.html?kind=${kind}#artefacts`, '.rv-art-row');
  const href = await page.evaluate(() => document.querySelector('#rv-art .rv-art-link').getAttribute('href'));
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

// an operation routes by node id, as it always did
{
  const node = index.nodes.find((n) => n.type === 'operation' && n.name === targets.operation);
  await open(`/reviews.html?kind=operation&q=${encodeURIComponent(targets.operation)}#artefacts`, '.rv-art-row');
  const href = await page.evaluate((name) => [...document.querySelectorAll('#rv-art .rv-art-link')]
    .find((a) => a.textContent === name)?.getAttribute('href'), targets.operation);
  check('an operation row links by node id', href === `/#${encodeURIComponent(node.id)}`, href);
  await page.goto(`${VIEWER}/#${encodeURIComponent(node.id)}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(3000);
  check('and the viewer opens that operation from it',
    await page.evaluate((id) => window.__state.selectedId === id, node.id), node.id);
}

// ── the old address ──────────────────────────────────────────────────
await page.goto(`${VIEWER}/validation.html?kind=table`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.rv-cov-row', { timeout: 40000 });
{
  const u = new URL(page.url());
  check('validation.html lands on Reviews, where it stands, keeping its query',
    u.pathname === '/reviews.html' && u.hash === '#coverage' && u.searchParams.get('kind') === 'table', page.url());
}

// ── a kind the reader cannot serve is said, not counted as empty ─────
{
  await page.setRequestInterception(true);
  const refuse = (req) => (/\/domain(\?|$)/.test(new URL(req.url()).pathname + new URL(req.url()).search)
    ? req.respond({ status: 503, contentType: 'application/json', body: '{}' })
    : req.continue());
  page.on('request', refuse);
  await open('/reviews.html#coverage');
  const said = await page.evaluate(() => ({
    row: [...document.querySelectorAll('#rv-cov .rv-cov-row')]
      .find((r) => r.querySelector('.rv-cov-label').textContent === 'State models')?.textContent ?? '',
    verdict: document.getElementById('rv-verdict').textContent,
  }));
  check('a kind that could not be read says so in the chart and the opening',
    /could not be read/.test(said.row) && /state models could not be read/i.test(said.verdict),
    said.row);
  page.off('request', refuse);
  await page.setRequestInterception(false);
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
