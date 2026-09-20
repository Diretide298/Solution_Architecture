/**
 * Every page and every layer/mode view, shot in both themes, into `assets/`.
 *
 * Not a check — nothing here asserts. It is the deck harness: the pictures it
 * writes are for slides and presentations, which is why they are 2x and why
 * `assets/` is gitignored rather than tracked.
 *
 * It walks the same ground as `pages-check.mjs`, but it takes the layer and
 * mode table from `core.js` *in the page* rather than repeating it here. That
 * list has grown four times; a copy in this file would be wrong by the next one.
 *
 *   node checks/capture-assets.mjs
 *
 * Against a throwaway pair, which is the point — `HANDOFF.md` says not to
 * restart 4173/8787, and signing in rewrites a session either way:
 *
 *   TICVAI_DB=…/shots.db python -m uvicorn api.main:app --port 8791
 *   TICVAI_AUTH=http://127.0.0.1:8791 node server.mjs --port 4620
 *   TICVAI_VIEWER=http://localhost:4620 TICVAI_API=http://127.0.0.1:8791 \
 *     node checks/capture-assets.mjs
 */
import puppeteer from 'puppeteer-core';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const VIEWER = process.env.TICVAI_VIEWER ?? 'http://localhost:4173';
/**
 * Empty, and deliberately — `validation.js` reads `''` as "this origin".
 *
 * The obvious spelling is the accounts service's own address, and it is wrong
 * on a throwaway pair for two separate reasons. Its CORS allowlist names 4173,
 * not whatever spare port the viewer is on, so the sign-in `fetch` is refused
 * before it is sent; and a cookie is per *host*, so a session set by
 * `127.0.0.1:8791` is never sent back to `localhost:4620`.
 *
 * Going through the viewer sidesteps both: `server.mjs` proxies `/api/auth`
 * (line 721) *before* the gate runs, so sign-in on this origin reaches the
 * service and the cookie comes back on the origin the pages are served from.
 */
const API = process.env.TICVAI_API ?? '';
const EMAIL = process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com';
const PASSWORD = process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase';
const OUT = process.env.TICVAI_SHOTS ?? path.resolve(process.cwd(), '..', 'assets');
const PROJECT = process.env.TICVAI_PROJECT ?? 'ticvai';

// 2x at 1600x1000: a deck slide is projected, and a 1x shot of a dense table
// is unreadable on a wall. `fullPage` is deliberately off — these frame the
// product, and a full-page shot of the migrations view is four screens tall.
const WIDTH = 1600, HEIGHT = 1000, SCALE = 2;

// The standalone pages, in reading order rather than alphabetical.
const PAGES = [
  ['home', '/home.html'],
  ['validation', '/validation.html'],
  ['reviews', '/reviews.html'],
  ['changes', '/changes.html'],
  ['domains', '/domains.html'],
  ['settings', '/settings.html'],
  ['admin', '/admin.html'],
  ['audit-package', '/audit.html'],
];

// Public, and shot signed *out* — /login.html signed in is a redirect, and the
// landing page is the one picture a deck actually opens on.
const PUBLIC = [
  ['landing', '/landing.html'],
  ['login', '/login.html'],
  ['invite', '/invite.html'],
];

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const slug = (s) => s.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').toLowerCase();

let shot = 0, failed = [];

async function capture(page, dir, name) {
  const file = path.join(dir, `${String(++shot).padStart(3, '0')}-${slug(name)}.png`);
  await page.screenshot({ path: file });
  console.log('  ✓ ' + path.relative(OUT, file));
}

/**
 * Theme is a localStorage key read before first paint, so it has to be set on
 * an already-loaded same-origin document and then navigated into — setting it
 * and screenshotting the current page would shoot the old theme.
 */
async function setTheme(page, theme) {
  await page.evaluate((t) => localStorage.setItem('ticvai-theme', t), theme);
}

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME
    ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new',
  args: ['--no-sandbox', '--force-device-scale-factor=' + SCALE],
});

for (const [theme, folder] of [['light', 'day'], ['dark', 'night']]) {
  const dir = path.join(OUT, folder);
  await mkdir(dir, { recursive: true });
  console.log(`\n── ${folder} (${theme}) ${'─'.repeat(40)}`);

  // ── signed out: the three public pages ──────────────────────────────
  const anon = await browser.createBrowserContext();
  const a = await anon.newPage();
  await a.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: SCALE });
  await a.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
  await a.evaluate((api) => localStorage.setItem('ticvai-api', api), API);
  await setTheme(a, theme);
  for (const [name, url] of PUBLIC) {
    try {
      await a.goto(VIEWER + url, { waitUntil: 'networkidle2', timeout: 30000 });
      await wait(2200);
      await capture(a, dir, name);
    } catch (e) { failed.push(`${folder}/${name}: ${e.message}`); console.log('  ✗ ' + name); }
  }
  await anon.close();

  // ── signed in: the pages, then every view ───────────────────────────
  const ctx = await browser.createBrowserContext();
  const p = await ctx.newPage();
  await p.setViewport({ width: WIDTH, height: HEIGHT, deviceScaleFactor: SCALE });
  await p.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
  await p.evaluate((api) => localStorage.setItem('ticvai-api', api), API);
  await setTheme(p, theme);
  const signedIn = await p.evaluate(async (api, email, password) => {
    const r = await fetch(`${api}/api/auth/login`, {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return r.status;
  }, API, EMAIL, PASSWORD);
  if (signedIn !== 200) {
    throw new Error(`sign-in as ${EMAIL} answered ${signedIn} — create the account first: `
      + 'python -m api.cli admin ' + EMAIL);
  }

  for (const [name, url] of PAGES) {
    try {
      await p.goto(VIEWER + url, { waitUntil: 'networkidle2', timeout: 40000 });
      await wait(2500);
      await capture(p, dir, name);
    } catch (e) { failed.push(`${folder}/${name}: ${e.message}`); console.log('  ✗ ' + name); }
  }

  // The layer/mode table, read out of the page's own core.js.
  await p.goto(`${VIEWER}/?project=${PROJECT}`, { waitUntil: 'domcontentloaded' });
  await p.waitForSelector('#layers button', { timeout: 40000 });
  const layers = await p.evaluate(async () => {
    const m = await import('/core.js');
    return m.LAYERS.map((l) => ({ key: l.key, modes: l.modes.map(([k]) => k) }));
  });

  for (const layer of layers) {
    for (const mode of layer.modes) {
      const name = `${layer.key}-${mode}`;
      try {
        await p.goto(`${VIEWER}/?project=${PROJECT}&layer=${layer.key}&mode=${mode}`,
          { waitUntil: 'domcontentloaded', timeout: 40000 });
        await p.waitForSelector('#layers button', { timeout: 30000 });
        // The views fetch their payload on first open and most of them draw;
        // the graph and canvas ones settle noticeably later than the tables.
        await wait(/graph|canvas|er|burst|cell|sphere|services/.test(mode) ? 6000 : 3800);
        await capture(p, dir, name);
      } catch (e) { failed.push(`${folder}/${name}: ${e.message}`); console.log('  ✗ ' + name); }
    }
  }
  await ctx.close();
}

await browser.close();
console.log(`\n${shot} shots → ${OUT}`);
if (failed.length) {
  console.log(`\n${failed.length} did not render:`);
  for (const f of failed) console.log('  ' + f);
}
