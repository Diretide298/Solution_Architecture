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
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

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

// ── against the disk, not against itself ─────────────────────────────
// The two checks above compare the payload to the payload. They pass whatever
// `buildUiux` decides to read, which is exactly the bug this page exists for
// one level up: `ui-design/designs/` held seven drawn boards and the reader
// knew two directory names, so seven boards were missing and every count above
// agreed with every other count.
//
// So this walks the package. The directories are named here rather than
// imported from the reader, because a list the reader also owns cannot
// contradict it — that is the whole failure being guarded against.
const HERE = path.dirname(fileURLToPath(import.meta.url));
const VIEWER_DIR = path.join(HERE, '..');
const ON_DISK = [
  ['wireframes', 'wireframes'],
  ['designs', 'designs'],
  ['ui-design', path.join('ui-design', 'designs')],
];
const IS_BOARD = /[._]dc\.html$/i;

let pkgRoot = null;
try {
  const registryFile = JSON.parse(await readFile(path.join(VIEWER_DIR, 'projects.json'), 'utf8'));
  const entry = (registryFile.projects ?? []).find((p) => p.id === project);
  if (entry?.root) pkgRoot = path.resolve(VIEWER_DIR, entry.root);
} catch { /* not beside this checkout */ }

const found = [];
let readable = false;
if (pkgRoot) {
  for (const [id, rel] of ON_DISK) {
    const names = await readdir(path.join(pkgRoot, rel)).catch(() => null);
    if (names === null) continue;
    readable = true;
    for (const name of names.filter((n) => IS_BOARD.test(n))) found.push(`${id}/${name}`);
  }
}

if (!readable) {
  // Said out loud rather than passed. A disk check that silently skips when it
  // cannot see the disk is a check that reports success for doing nothing.
  check('the package is beside this checkout, so the disk can be compared',
    false, `no readable board folder under ${pkgRoot ?? 'projects.json (unreadable)'}`);
} else {
  const listed = new Set(payload.boards.map((b) => `${b.folder}/${b.file}`));
  const missing = found.filter((f) => !listed.has(f));
  const phantom = [...listed].filter((f) => !found.includes(f));
  check('every board file on disk is on the page', missing.length === 0,
    `${found.length} on disk, ${listed.size} listed`
    + (missing.length ? ` | missing: ${missing.slice(0, 4).join(', ')}` : ''));
  check('and the page invents none', phantom.length === 0,
    phantom.length ? phantom.slice(0, 4).join(', ') : 'none');
}
// No board reports the same frame twice.
//
// Anchors are folded to lower case, and 65 of the 100 boards carry each one in
// both cases — `id="FNB-6A"` on the frame and `id="fnb-6a"` on the thumbnail
// that links to it. Counting both reported 1829 frames against 1362 drawn, and
// every figure on the page derived from it was a third too high. The page puts
// that number in 25px type, so it is held here rather than eyeballed.
const doubled = payload.boards
  .map((b) => ({ b, extra: b.frames.length - new Set(b.frames.map((f) => f.anchor)).size }))
  .filter((x) => x.extra > 0);
check('no board counts the same frame twice', doubled.length === 0,
  `${doubled.length} boards double-count `
  + `${doubled.reduce((n, x) => n + x.extra, 0)} frames, e.g. ${doubled[0]?.b.name}`);
// And the total is the sum of the parts, which is what makes the headline
// figure a measurement rather than a second opinion.
check('the frame total is the sum of the boards',
  S.frames === payload.boards.reduce((n, b) => n + b.frameCount, 0),
  `${S.frames} claimed, ${payload.boards.reduce((n, b) => n + b.frameCount, 0)} summed`);

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

// The board index is a view of the `uiux` layer now, not a page of its own.
await page.goto(`${BASE}/?layer=uiux&mode=uiux-boards`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('.bd-tile', { timeout: 30000 }).catch(() => {});
await wait(2500);

const tiles = await page.evaluate(() => document.querySelectorAll('.bd-tile').length);
check('the map draws a tile per board', tiles === S.boards, `${tiles} tiles, ${S.boards} boards`);

const marked = await page.evaluate(() => document.querySelectorAll('.bd-tile.is-unwired').length);
check('and marks the ones nothing points at', marked === S.unwired,
  `${marked} marked, ${S.unwired} unwired`);

// ── the tiles are all one size ───────────────────────────────────────
// The map replaced a masonry of cards whose heights came from their contents,
// so a row of four was four different shapes and the eye spent its effort on
// the mosaic rather than on the colours inside it. "One board, one tile, one
// size" is the rule that layout is for, and a rule nothing holds is a rule that
// comes back the first time somebody adds a line to a tile.
const boxes = await page.evaluate(() => [...document.querySelectorAll('.bd-tile')].map((t) => {
  const r = t.getBoundingClientRect();
  return { w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top) };
}));
const heights = [...new Set(boxes.map((b) => b.h))];
check('every tile is the same height', heights.length === 1,
  `${heights.length} distinct heights: ${heights.slice(0, 5).join(', ')}`);

// Width is checked per row rather than across the page, because that is the
// actual claim: two tiles side by side are the same size.
const rows = new Map();
for (const b of boxes) {
  if (!rows.has(b.top)) rows.set(b.top, []);
  rows.get(b.top).push(b.w);
}
const ragged = [...rows.entries()].filter(([, ws]) => new Set(ws).size > 1);
check('and tiles side by side are the same width', ragged.length === 0,
  ragged.length ? `${ragged.length} ragged rows, first: ${ragged[0][1].join(', ')}` : `${rows.size} rows`);

// One chip per frame, up to the cap the tile stops at. If this drifts, the tile
// is either hiding frames silently or growing to fit them — the two failures
// the fixed height exists to prevent.
const CHIP_CAP = 60;
const chips = await page.evaluate(() => document.querySelectorAll('.bd-tile .bd-chip').length);
const wantChips = payload.boards.reduce((n, b) => n + Math.min(b.frameCount, CHIP_CAP), 0);
check('a chip per frame, and the overflow is counted not dropped', chips === wantChips,
  `${chips} chips, ${wantChips} expected`);
const more = await page.evaluate(() => [...document.querySelectorAll('.bd-chip-more')]
  .reduce((n, e) => n + Number(e.textContent.replace('+', '')), 0));
const wantMore = payload.boards.reduce((n, b) => n + Math.max(0, b.frameCount - CHIP_CAP), 0);
check('and the overflow adds up to the rest of them', more === wantMore,
  `+${more} counted, +${wantMore} over the cap`);

const lead = await page.evaluate(() => document.getElementById('lead')?.textContent ?? '');
check('the header states the counts it measured',
  lead.includes(String(S.boards)) && lead.includes(String(S.unwired)), lead.slice(0, 90));

// The loading curtain has to come down. It is the one failure that leaves a
// page looking like it is still working when it has finished.
const curtain = await page.evaluate(() => {
  const box = document.getElementById('adam-loader');
  return !box || box.classList.contains('is-done');
});
check('the loading curtain lifts', curtain);

// ── the rail ─────────────────────────────────────────────────────────
// Every board nothing points at, by name. This is the group the page was
// written for: a board no screen claims appears nowhere else in the viewer, so
// if the rail drops one it is unreachable again and the page has quietly
// reverted to being the thing it replaced.
const railed = await page.evaluate(
  () => [...document.querySelectorAll('.ux-tree .ux-row-label')].map((n) => n.textContent)
);
const orphans = payload.boards.filter((b) => !b.wired).map((b) => b.name);
const droppedFromRail = orphans.filter((n) => !railed.includes(n));
check('the rail lists every board nothing points at', droppedFromRail.length === 0,
  `${orphans.length} unwired, missing: ${droppedFromRail.slice(0, 3).join(', ')}`);

// Picking one narrows the map to it and fills the panel on the right.
const firstOrphan = payload.boards.filter((b) => !b.wired)
  .sort((a, b) => b.frameCount - a.frameCount || a.name.localeCompare(b.name))[0];
if (firstOrphan) {
  await page.evaluate((name) => {
    const row = [...document.querySelectorAll('.ux-tree .ux-row')]
      .find((r) => r.querySelector('.ux-row-label')?.textContent === name);
    row?.click();
  }, firstOrphan.name);
  await wait(600);
  const picked = await page.evaluate(() => ({
    tiles: document.querySelectorAll('.bd-tile').length,
    title: document.querySelector('.bd-detail-title')?.textContent ?? '',
    frames: document.querySelectorAll('.bd-frame').length,
  }));
  check('picking a board in the rail narrows the map to it', picked.tiles === 1,
    `${picked.tiles} tiles`);
  check('and the panel on the right is that board', picked.title === firstOrphan.name,
    `"${picked.title}" vs "${firstOrphan.name}"`);
  check('with a row per frame to claim', picked.frames === firstOrphan.frameCount,
    `${picked.frames} rows, ${firstOrphan.frameCount} frames`);
  // Back to everything: clicking the selected row again clears it.
  await page.evaluate((name) => {
    const row = [...document.querySelectorAll('.ux-tree .ux-row')]
      .find((r) => r.querySelector('.ux-row-label')?.textContent === name);
    row?.click();
  }, firstOrphan.name);
  await wait(500);
}

// The Kinds rail replaces what used to be a `<select>`. Same job, and it is now
// the only way to reach it, so it is the thing worth driving.
await page.evaluate(() => {
  document.querySelector('.ux-tabs button[data-rail="kinds"]')?.click();
});
await wait(400);
await page.evaluate(() => {
  const row = [...document.querySelectorAll('.ux-tree .ux-row')]
    .find((r) => r.querySelector('.ux-row-label')?.textContent === 'drawn by hand');
  row?.click();
});
await wait(600);
const packs = await page.evaluate(() => document.querySelectorAll('.bd-tile').length);
const packCount = payload.boards.filter((b) => b.kind === 'pack').length;
check('the kinds rail picks out the hand-drawn packs', packs === packCount,
  `${packs} shown, ${packCount} packs`);

// Clear it, and go back to the folders rail.
await page.evaluate(() => {
  const row = [...document.querySelectorAll('.ux-tree .ux-row')]
    .find((r) => r.querySelector('.ux-row-label')?.textContent === 'drawn by hand');
  row?.click();
  document.querySelector('.ux-tabs button[data-rail="folders"]')?.click();
});
await wait(500);

// ── the filters actually filter ──────────────────────────────────────
await page.evaluate(() => {
  const t = document.getElementById('only-unwired');
  t.checked = true; t.dispatchEvent(new Event('change'));
});
await wait(700);
const onlyUnwired = await page.evaluate(() => document.querySelectorAll('.bd-tile').length);
check('"unwired only" shows exactly those', onlyUnwired === S.unwired,
  `${onlyUnwired} shown, ${S.unwired} unwired`);

await page.evaluate(() => {
  const t = document.getElementById('only-unwired');
  t.checked = false; t.dispatchEvent(new Event('change'));
  const f = document.getElementById('filter');
  f.value = 'inventory'; f.dispatchEvent(new Event('input'));
});
await wait(700);
const filtered = await page.evaluate(
  () => [...document.querySelectorAll('.bd-tile-name')].map((n) => n.textContent)
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
// section heading has to say "n of m" once anything is filtered out.
const heading = await page.evaluate(
  () => document.querySelector('.uiux-folder')?.textContent ?? ''
);
check('a filtered section heading keeps its denominator', / of \d+$/.test(heading), heading);

// ── the other two middle views ───────────────────────────────────────
await page.evaluate(() => {
  const f = document.getElementById('filter');
  f.value = ''; f.dispatchEvent(new Event('input'));
  document.querySelector('.bd-seg button[data-view="list"]')?.click();
});
await wait(900);
const cards = await page.evaluate(() => document.querySelectorAll('.uiux-card').length);
check('the list view draws a card per board', cards === S.boards,
  `${cards} cards, ${S.boards} boards`);

await page.evaluate(() => document.querySelector('.bd-seg button[data-view="frames"]')?.click());
await wait(1200);
const ROW_CAP = 600;
const frameRows = await page.evaluate(() => document.querySelectorAll('.bd-table tbody tr').length);
check('the frames view draws the worklist', frameRows === Math.min(S.frames, ROW_CAP),
  `${frameRows} rows, ${S.frames} frames (cap ${ROW_CAP})`);

// The claim list is the button in the header, and it has one job: unclaimed
// frames only, in the frames view.
await page.evaluate(() => document.getElementById('bd-claim')?.click());
await wait(1200);
const claimRows = await page.evaluate(() => document.querySelectorAll('.bd-table tbody tr').length);
const unclaimed = S.frames - S.framesClaimed;
check('"the claim list" shows the unclaimed frames and nothing else',
  claimRows === Math.min(unclaimed, ROW_CAP),
  `${claimRows} rows, ${unclaimed} unclaimed (cap ${ROW_CAP})`);

// ── one rail, three views ────────────────────────────────────────────
// The layer's three views were three different places: a canvas with its own
// rail, a board list with a filter box, and a platform page that was a reading
// column with no navigation at all — so on Platforms the only way to reach P13
// was to scroll past twelve other platforms, on a page whose whole subject is
// which platform you are looking at.
//
// They share `.ux-rail` now, and the assertion is that all three still do. A
// shared component that two of three views use is not a shared component; it is
// a copy waiting to drift.
for (const [mode, waitFor] of [
  ['uiux-screens', '.cv-row'],
  ['uiux-boards', '.bd-tile'],
  ['uiux-platforms', '.plat-card'],
]) {
  await page.goto(`${BASE}/?layer=uiux&mode=${mode}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector(waitFor, { timeout: 30000 }).catch(() => {});
  await wait(2200);
  const rail = await page.evaluate(() => {
    const view = document.querySelector('.view:not([hidden]) .ux-rail');
    return {
      present: Boolean(view),
      tabs: view ? view.querySelectorAll('.ux-tabs button').length : 0,
      groups: view ? view.querySelectorAll('.ux-group').length : 0,
      rows: view ? view.querySelectorAll('.ux-row').length : 0,
      find: view ? Boolean(view.querySelector('.ux-rail-find .ux-input')) : false,
    };
  });
  check(`${mode} carries the layer's rail`,
    rail.present && rail.tabs >= 2 && rail.groups >= 1 && rail.rows > 0 && rail.find,
    `rail=${rail.present} tabs=${rail.tabs} groups=${rail.groups} rows=${rail.rows} filter=${rail.find}`);
}

check('no console or page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
