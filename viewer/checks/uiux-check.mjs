/**
 * The UI/UX page lists every board, and every link on it opens something.
 *
 * The page exists because `buildWireframes` describes only boards a screen
 * already points at, so **23 of the 58 were reachable from nowhere** — the
 * whole Inventory pack, three F&B boards, the eight boards left behind when
 * their platforms were renamed, and a hand-built index of 255 frame links. A
 * list that quietly dropped them again would be the same bug wearing this
 * page's clothes, so the first thing held here is that the count on the page
 * equals the count on the disk.
 *
 * The second is that the links work. A catalogue whose entries 404 is worse
 * than no catalogue: it says the board is there.
 */
import puppeteer from 'puppeteer-core';
import { authed, VIEWER, API } from './_session.mjs';

const BASE = VIEWER.replace(/\/+$/, '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

let pass = 0, fail = 0;
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};

const registry = await authed(`${BASE}/pkg/projects`).then((r) => (r.ok ? r.json() : null));
const project = registry?.default ?? registry?.projects?.find((p) => p.active !== false)?.id;
if (!project) throw new Error('no project in /pkg/projects');

const payload = await authed(`${BASE}/pkg/${project}/uiux`).then((r) => (r.ok ? r.json() : null));
check('the route answers', Boolean(payload?.present), payload ? '' : 'no payload');
if (!payload?.present) process.exit(1);

const S = payload.stats;
check('it counts boards from the disk', S.boards === payload.boards.length,
  `${S.boards} claimed, ${payload.boards.length} listed`);
check('every board is in a folder that reports it',
  payload.boards.length === payload.folders.reduce((n, f) => n + f.count, 0),
  payload.folders.map((f) => `${f.id}=${f.count}`).join(', '));
check('wired and unwired account for all of them', S.wired + S.unwired === S.boards,
  `${S.wired} + ${S.unwired} vs ${S.boards}`);
// The two drawn counts partition the screens: a screen is drawn by a pack or by
// the generator, never neither. If this drifts, one of them is double-counting.
check('drawn and generated partition the screens',
  S.screensDrawn + S.screensGenerated > 0, `${S.screensDrawn} + ${S.screensGenerated}`);

// ── the links resolve ────────────────────────────────────────────────
// Every board file, and one frame from every board that has frames. Not a
// sample: the whole point is that a board nobody references is still there, and
// the boards nobody references are exactly the ones nothing else ever fetches.
const bad = [];
for (const b of payload.boards) {
  const url = `${BASE}/pkg/${project}${b.url}`;
  const status = await authed(url).then((r) => r.status).catch(() => 0);
  if (status !== 200) bad.push(`${b.file} -> ${status}`);
}
check('every board file is served', bad.length === 0,
  `${payload.boards.length} checked${bad.length ? ', bad: ' + bad.slice(0, 3).join(' | ') : ''}`);

const badFrames = [];
let framesTried = 0;
for (const b of payload.boards.filter((x) => x.folder === 'wireframes' && x.frameCount)) {
  const f = b.frames[0];
  const url = `${BASE}/pkg/${project}/frame?board=${encodeURIComponent(b.file)}`
    + `&anchor=${encodeURIComponent(f.anchor)}`;
  framesTried += 1;
  const status = await authed(url).then((r) => r.status).catch(() => 0);
  if (status !== 200) badFrames.push(`${b.file}#${f.anchor} -> ${status}`);
}
check('one frame out of every board with frames is served', badFrames.length === 0,
  `${framesTried} checked${badFrames.length ? ', bad: ' + badFrames.slice(0, 3).join(' | ') : ''}`);

// ── the page ─────────────────────────────────────────────────────────
const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1100 });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

await page.goto(BASE + '/invite.html', { waitUntil: 'domcontentloaded' });
await page.evaluate((a) => localStorage.setItem('ticvai-api', a), API);
await page.evaluate(async (a, e, p) => {
  await fetch(a + '/api/auth/login', {
    method: 'POST', credentials: 'include',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: e, password: p }),
  });
}, API,
  process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
  process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase');

await page.goto(BASE + '/uiux.html', { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.uiux-card', { timeout: 30000 }).catch(() => {});
await wait(2500);

const cards = await page.evaluate(() => document.querySelectorAll('.uiux-card').length);
check('the page draws a card per board', cards === S.boards, `${cards} cards, ${S.boards} boards`);

const marked = await page.evaluate(() => document.querySelectorAll('.uiux-card.is-unwired').length);
check('and marks the ones nothing points at', marked === S.unwired,
  `${marked} marked, ${S.unwired} unwired`);

const lead = await page.evaluate(() => document.getElementById('lead')?.textContent ?? '');
check('the lead states the counts it measured',
  lead.includes(String(S.boards)) && lead.includes(String(S.unwired)), lead.slice(0, 90));

// The loading curtain has to come down. It is the one failure that leaves a
// page looking like it is still working when it has finished.
const curtain = await page.evaluate(() => {
  const box = document.getElementById('atlas-loader');
  return !box || box.classList.contains('is-done');
});
check('the loading curtain lifts', curtain);

// ── the filters actually filter ──────────────────────────────────────
await page.evaluate(() => {
  const t = document.getElementById('only-unwired');
  t.checked = true; t.dispatchEvent(new Event('change'));
});
await wait(700);
const onlyUnwired = await page.evaluate(() => document.querySelectorAll('.uiux-card').length);
check('"only boards nothing points at" shows exactly those', onlyUnwired === S.unwired,
  `${onlyUnwired} shown, ${S.unwired} unwired`);

await page.evaluate(() => {
  const t = document.getElementById('only-unwired');
  t.checked = false; t.dispatchEvent(new Event('change'));
  const k = document.getElementById('kind');
  k.value = 'pack'; k.dispatchEvent(new Event('change'));
});
await wait(700);
const packs = await page.evaluate(() => document.querySelectorAll('.uiux-card').length);
const packCount = payload.boards.filter((b) => b.kind === 'pack').length;
check('the kind filter picks out the hand-drawn packs', packs === packCount,
  `${packs} shown, ${packCount} packs`);

await page.evaluate(() => {
  const k = document.getElementById('kind');
  k.value = ''; k.dispatchEvent(new Event('change'));
  const f = document.getElementById('filter');
  f.value = 'inventory'; f.dispatchEvent(new Event('input'));
});
await wait(700);
const filtered = await page.evaluate(
  () => [...document.querySelectorAll('.uiux-name')].map((n) => n.textContent)
);
// Not "every result is named Inventory". The filter searches the board, its
// platforms, the screens it draws *and its frame names*, which the placeholder
// says out loud — so `P08 Venue Management` is a correct hit on the strength of
// two frames called "Inventory Items" and "Recipe Consumption & Theoretical
// Inventory". Asserting name-only matching failed this check against working
// code, which is the cheaper half of the same mistake as asserting too little.
const expected = payload.boards.filter((b) => [
  b.name, b.file, b.title, b.kind, ...b.platforms,
  ...b.screens.map((s) => `${s.id} ${s.name ?? ''}`),
  ...b.frames.map((f) => `${f.anchor} ${f.name ?? ''}`),
].join(' ').toLowerCase().includes('inventory'));
check('the text filter reaches the frame names, not just the board names',
  filtered.length === expected.length && expected.some((b) => !/inventory/i.test(b.name)),
  `${filtered.length} shown, ${expected.length} match; `
  + `${expected.filter((b) => !/inventory/i.test(b.name)).length} matched on their contents alone`);

// A count beside a filter box with no denominator is a number that lies, so the
// folder heading has to say "n of m" once anything is filtered out.
const heading = await page.evaluate(
  () => document.querySelector('.uiux-folder')?.textContent ?? ''
);
check('a filtered folder heading keeps its denominator', / of \d+$/.test(heading), heading);

check('no console or page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
