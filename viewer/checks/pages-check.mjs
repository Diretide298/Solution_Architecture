/**
 * Every page loads, and every layer and mode renders, without a console error.
 *
 * This is the check that would have caught all three of the failures that
 * prompted it — `KINDS is not defined` after an edit to reviews.js, and two
 * missing imports while app.js was being split. Each one left a clean
 * `node --check`, a page that rendered its static HTML, and nothing at all in
 * the part a reader came for.
 *
 * A static version of this was tried first and pulled: it could not tell a
 * regex literal from a reference and reported eighteen things that were fine.
 * The browser has no such trouble — it either throws or it does not.
 *
 * Needs an admin account. See checks/README.md.
 */
import puppeteer from 'puppeteer-core';
import { authed, VIEWER, API } from './_session.mjs';

const MODES = {
  frontend: ['screen', 'journey', 'apps', 'waves', 'audit'],
  contracts: ['graph', 'structure', 'er', 'lineage', 'reader', 'audit'],
  domain: ['states', 'events', 'audit'],
  backend: ['data', 'migrations', 'routing', 'audit'],
  decisions: ['timeline', 'supersession', 'register', 'decision', 'decisions', 'audit'],
};
// The real pages, read off public/ rather than remembered — an invented name
// here fails as a 404 and reads like a broken page.
//
// `/platforms.html` was excluded here as an orphan — the 20 August revert took
// `public/platforms.js` and `changes.html` with it and left the HTML behind, so
// the page loaded and then 404d on its own script. **That has not been true for
// some time**: `public/platforms.js` is back, `server.mjs` imports
// `lib/platforms.mjs`, and all three of the page, its script and its payload
// answer 200. An exclusion outlives its reason silently, which is how a page
// stays untested after it starts working.
//
// It was still reachable from nothing but the header chips on its siblings,
// which is why nobody noticed either way. Linked from the viewer's own menu now,
// alongside `/uiux.html`.
const PAGES = [
  '/validation.html', '/reviews.html', '/admin.html', '/domains.html',
  '/platforms.html', '/uiux.html',
];

let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (d ? ' — ' + d : '')); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

await authed(VIEWER + '/api/index');   // fail early and clearly if there is no account

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});

const errors = [];
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000 });
page.on('pageerror', (e) => errors.push(CURRENT + ': ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(CURRENT + ': ' + m.text()); });

let CURRENT = 'boot';

await page.goto(VIEWER + '/invite.html', { waitUntil: 'domcontentloaded' });
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

CURRENT = 'the viewer';

// **A bare `/` is the door now, not the viewer.** Since the package split there is no single
// project to open, so `/` renders `home.html` and waits for the reader to pick one. This
// harness kept asking for `#layers button` on the picker and timing out after thirty seconds
// naming nothing, which is how it went from a check to a thing nobody ran.
//
// Ask the registry rather than hard-coding `ticvai`: `default` is the same field the server
// resolves the pre-project routes against, so the harness opens whatever this deployment says
// it opens. A harness that named one project would pass here and fail anywhere else.
//
// Not by clicking through the door — its links stay *on* the door with a project selected,
// which is a picker affordance rather than a way in. Two hops through markup that exists to
// be redesigned is a harness that breaks on a layout change; the registry is the contract.
const registry = await authed(`${VIEWER.replace(/\/+$/, '')}/pkg/projects`)
  .then((r) => (r.ok ? r.json() : null)).catch(() => null);
const openProject = registry?.default
  ?? registry?.projects?.find((p) => p.active !== false)?.id;
if (!openProject) throw new Error('no project in /pkg/projects — is projects.json empty?');
await page.goto(`${VIEWER.replace(/\/+$/, '')}/?project=${encodeURIComponent(openProject)}`,
                { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 30000 });
await wait(6000);

for (const [layer, modes] of Object.entries(MODES)) {
  await page.evaluate((l) => document.querySelector('#layers button[data-layer="' + l + '"]').click(), layer);
  await wait(2200);
  for (const mode of modes) {
    CURRENT = layer + '/' + mode;
    const found = await page.evaluate((m) => {
      const b = [...document.querySelectorAll('#modes button')].find((x) => x.dataset.mode === m);
      if (!b) return false;
      b.click(); return true;
    }, mode);
    check('the ' + layer + ' layer offers its ' + mode + ' mode', found);
    if (!found) continue;
    await wait(2400);
    // Rendered something, rather than merely not throwing — a view that dies at
    // module scope leaves an empty container and a silent page.
    const filled = await page.evaluate((m) => {
      const view = document.getElementById('view-' + m);
      return !!view && !view.hidden && view.querySelectorAll('*').length > 5;
    }, mode);
    check(CURRENT + ' renders content', filled);
  }
}

for (const path of PAGES) {
  CURRENT = path;
  await page.goto(VIEWER + path, { waitUntil: 'domcontentloaded' });
  await wait(3500);
  const filled = await page.evaluate(() => document.querySelectorAll('main *').length > 20);
  check(path + ' renders content', filled);
}

check('no console or page errors anywhere', errors.length === 0,
  errors.slice(0, 6).join(' | '));

await browser.close();
console.log('\n' +  + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
