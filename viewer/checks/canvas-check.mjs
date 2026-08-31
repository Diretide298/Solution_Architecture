/**
 * The canvas puts every screen on one surface, and does not lie about it.
 *
 * Four claims, in the order they would hurt if they were wrong:
 *
 *   it is all there    a node per screen **of the platform on the sheet**, and
 *                      every platform offered in the rail. A canvas that quietly
 *                      drops screens is worse than the list it replaces, because
 *                      a gap on a map reads as "nothing goes here" — and now
 *                      that only one platform is drawn at a time, the way to
 *                      lose 300 screens without noticing is for the rail to stop
 *                      offering the platforms they are on.
 *   it is drawn        the frames mount when they are in view and above the
 *                      zoom where they are legible, and unmount when they are
 *                      not. 492 live documents is the stall this avoids, and
 *                      "no frames at any zoom" would look identical to a
 *                      working canvas at low zoom.
 *   inference is       345 of the 492 screens have navigation the package
 *   marked             guessed. Drawn like the rest, a guess reads as a
 *                      designed flow.
 *   it leads back      a screen opens a panel that reaches the Frontend layer,
 *                      the deep link and the frame — the canvas is a way in,
 *                      not a second copy of the viewer.
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

const journeys = await authed(`${BASE}/pkg/${project}/journeys`).then((r) => (r.ok ? r.json() : null));
const screens = journeys?.screens ?? [];
const flows = journeys?.flows ?? [];
const platforms = new Set(screens.map((s) => s.platform));
const inferred = screens.filter((s) => s.navigationInferred).length;
check('the package has screens to draw', screens.length > 0,
  `${screens.length} screens, ${platforms.size} platforms, ${flows.length} journeys`);

// ── the still frame ──────────────────────────────────────────────────
// The tiles are sandboxed without `allow-scripts`, so a document with a script
// in it logs a console error per tile. `still=1` is the server taking them out;
// if it stops doing that the canvas goes back to a page of console errors and
// nothing else changes, which is exactly the kind of regression nobody sees.
const withBoard = screens.find((s) => /^wireframes\/.+#/i.test(s.wireframe?.board ?? ''));
if (withBoard) {
  const [target, anchor] = withBoard.wireframe.board.split('#');
  const board = target.replace(/^wireframes\//i, '');
  const q = `board=${encodeURIComponent(board)}&anchor=${encodeURIComponent(anchor.toLowerCase())}`;
  const plain = await authed(`${BASE}/pkg/${project}/frame?${q}`).then((r) => r.text());
  const still = await authed(`${BASE}/pkg/${project}/frame?${q}&still=1`).then((r) => r.text());
  check('the frame is served', plain.length > 200, `${plain.length} bytes`);
  check('and `still=1` takes the scripts out', !/<script\b/i.test(still) && still.length > 200,
    `${(plain.match(/<script\b/gi) ?? []).length} script tags -> ${(still.match(/<script\b/gi) ?? []).length}`);
}

// ── the browser ──────────────────────────────────────────────────────
const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000 });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

await page.goto(BASE + '/invite.html', { waitUntil: 'domcontentloaded' });
await page.evaluate((a) => localStorage.setItem('ticvai-api', a), API);
await page.evaluate(async (a, e, p) => {
  try {
    await fetch(a + '/api/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: e, password: p }),
    });
  } catch { /* gate off */ }
}, API,
  process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
  process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase');

// The canvas is a view of the `uiux` layer, not a page. Driven by its deep link
// rather than by clicking through the tray: the tabs are markup that exists to
// be redesigned, and a harness that goes through them breaks on a layout change
// while the thing it is testing is fine.
await page.goto(`${BASE}/?project=${encodeURIComponent(project)}&layer=uiux&mode=uiux-screens`,
                { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.cv-card', { timeout: 40000 });
await wait(4000);

// The sheet is one platform. Pick the largest to test against: it is the one
// that broke the all-at-once layout, it is the only one certain to carry both
// declared and inferred links, and a check that passed on a four-screen
// platform would say nothing about the case that matters.
const byPlatform = new Map();
for (const s of screens) {
  if (!byPlatform.has(s.platform)) byPlatform.set(s.platform, []);
  byPlatform.get(s.platform).push(s);
}
const [biggest, onBiggest] = [...byPlatform.entries()].sort((a, b) => b[1].length - a[1].length)[0];
const here = new Set(onBiggest.map((s) => s.id));
const flowsHere = flows.filter((f) => (f.steps ?? []).some((st) => here.has(st.screenId)));

await page.select('#platform', biggest);
await wait(4000);

const laid = await page.evaluate(() => ({
  cards: document.querySelectorAll('.cv-card').length,
  ids: [...document.querySelectorAll('.cv-card')].map((c) => c.dataset.id),
  blocks: document.querySelectorAll('.cv-band').length,
  crossings: document.querySelectorAll('.cv-edge.is-cross').length,
  edges: document.querySelectorAll('.cv-edge').length,
  dashed: document.querySelectorAll('.cv-edge.is-inferred').length,
  platforms: document.querySelectorAll('#rail-platforms .cv-row').length,
  current: document.querySelector('#rail-platforms .cv-row.is-on')?.dataset.id ?? '',
  journeys: document.querySelectorAll('#rail-journeys .cv-row').length,
  railScreens: document.querySelectorAll('#rail-screens .cv-row').length,
  scope: document.getElementById('rail-scope')?.textContent ?? '',
}));

// One shelf per module, and the modules are the platform's own. A sheet that
// dropped a shelf would lose every screen on it without losing a card count,
// because the cards would still be laid out — just nowhere.
const modulesHere = new Set(onBiggest.map((s) => s.module || 'Unmoduled'));
check('the sheet is shelved by module',
  laid.blocks === modulesHere.size && laid.current === biggest,
  `${laid.blocks} shelves, ${modulesHere.size} modules, rail says "${laid.current}", scope reads "${laid.scope}"`);
check('a card for every screen on it', laid.cards === onBiggest.length,
  `${laid.cards} cards, ${onBiggest.length} screens on ${biggest}`);
// The way to lose screens now is to drop a whole platform from the rail rather
// than a card from the sheet — nothing else offers a way to reach them.
check('every platform is offered in the rail', laid.platforms === byPlatform.size,
  `${laid.platforms} of ${byPlatform.size}`);
check('and no card belongs to another platform',
  laid.ids.every((id) => here.has(id)),
  `${laid.ids.filter((id) => !here.has(id)).slice(0, 3).join(', ') || 'none stray'}`);

// The journeys listed are the ones that touch this platform, not all 60. A rail
// that kept listing every journey would look right and select nothing.
check('the rail lists the journeys that touch this platform', laid.journeys === flowsHere.length,
  `${laid.journeys} of ${flowsHere.length} touching, ${flows.length} in the package`);
check('and the screens on it', laid.railScreens === onBiggest.length,
  `${laid.railScreens} of ${onBiggest.length}`);

// The sheet opens on the crossings — the links that leave the module they start
// in, which are the ones the shelves cannot show. Nothing else in the layout
// says a screen in ordering leads to one in payments.
check('the links that cross a module are drawn',
  laid.crossings > 0 && laid.crossings === laid.edges,
  `${laid.crossings} crossings of ${laid.edges} links drawn on open`);

// Inference is drawn differently, and the count is not zero — a stylesheet that
// stopped marking them would leave this at 0 and everything else passing.
check('inferred navigation is drawn as inferred',
  laid.dashed > 0 && laid.dashed <= laid.edges,
  `${laid.dashed} of ${laid.edges} links dashed; ${inferred} screens in the package carry inferred navigation`);

// And "every link" has to actually be more than the crossings, or the control
// is decorative.
await page.select('#links-mode', 'all');
await page.waitForFunction((n) => document.querySelectorAll('.cv-edge').length > n, {}, laid.edges);
const allLinks = await page.evaluate(() => document.querySelectorAll('.cv-edge').length);
check('and asking for every link draws more of them', allLinks > laid.edges,
  `${laid.edges} crossings -> ${allLinks} links`);
await page.select('#links-mode', 'cross');

// ── frames mount, and only when they should ──────────────────────────
// Zoomed out first. "No frames at any zoom" and "frames only when legible"
// look identical unless both ends are asked for.
for (let i = 0; i < 4; i += 1) await page.evaluate(() => document.getElementById('zoom-out').click());
await wait(2500);
const far = await page.evaluate(() => ({
  live: document.querySelectorAll('.cv-iframe').length,
  zoom: document.getElementById('zoom-level').textContent,
  note: document.getElementById('canvas-note').textContent,
}));
check('nothing is mounted once it is too small to read', far.live === 0,
  `${far.live} live frames at ${far.zoom} — "${far.note}"`);

// Up to the zoom the frames are drawn at, rather than a fixed number of clicks:
// a fixed five took a 14% fit to 44%, under the 55% threshold, and the check
// failed the code for doing exactly what it says.
for (let i = 0; i < 14; i += 1) {
  const k = await page.evaluate(() => parseInt(document.getElementById('zoom-level').textContent, 10));
  if (k >= 60) break;
  await page.evaluate(() => document.getElementById('zoom-in').click());
}
await wait(5000);
const near = await page.evaluate(() => ({
  live: document.querySelectorAll('.cv-iframe').length,
  zoom: document.getElementById('zoom-level').textContent,
}));
check('and they mount again once it is', near.live > 0, `${near.live} live at ${near.zoom}`);

// ── a screen leads back into the viewer ──────────────────────────────
await page.evaluate(() => document.getElementById('zoom-fit').click());
await wait(1500);
const picked = await page.evaluate(() => {
  const card = document.querySelector('.cv-card:not([hidden])');
  card?.click();
  return card?.dataset.id ?? null;
});
await wait(1200);
const detail = await page.evaluate(() => ({
  open: !document.getElementById('detail').hidden,
  name: document.querySelector('.cv-detail-name')?.textContent ?? '',
  facts: [...document.querySelectorAll('.cv-facts dt')].map((d) => d.textContent),
  links: [...document.querySelectorAll('.cv-links .chip')].map((a) => a.getAttribute('href') ?? ''),
}));
check('clicking a screen opens its detail', detail.open && Boolean(detail.name),
  `${picked} — "${detail.name}"`);
check('which states whether the navigation was declared or guessed',
  detail.facts.includes('Navigation'), detail.facts.join(', '));
check('and leads back into the Frontend layer',
  detail.links.some((h) => h.includes('layer=frontend') && h.includes('mode=screen')),
  detail.links.filter(Boolean).slice(0, 3).join(' | '));

// ── the sheet actually changes ───────────────────────────────────────
// A platform control that filters nothing is the failure this rework exists to
// prevent, and it looks exactly like a working one until you count the cards.
const other = [...byPlatform.entries()].sort((a, b) => b[1].length - a[1].length)[1];
if (other) {
  const [otherId, otherScreens] = other;
  await page.select('#platform', otherId);
  await wait(4000);
  const swapped = await page.evaluate(() => ({
    ids: [...document.querySelectorAll('.cv-card')].map((c) => c.dataset.id),
    current: document.querySelector('#rail-platforms .cv-row.is-on')?.dataset.id ?? '',
    address: location.search,
  }));
  const want = new Set(otherScreens.map((s) => s.id));
  check('picking another platform redraws the sheet as that platform',
    swapped.ids.length === otherScreens.length && swapped.ids.every((id) => want.has(id)),
    `${swapped.ids.length} cards, ${otherScreens.length} screens on ${otherId}, rail says "${swapped.current}"`);
  // A sheet you cannot send to somebody is a sheet you have to describe over
  // the phone.
  check('and says so in the address', swapped.address.includes(`platform=${otherId}`),
    swapped.address);
}

check('no console or page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
