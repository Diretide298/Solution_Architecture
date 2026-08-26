/**
 * Every count a tip states is the count the payload holds.
 *
 * The tips used to write their numbers into the sentence, and the numbers
 * rotted: **654 operations against a live 1,023, 22 services against 16, 18
 * ADRs against 30**, and "318 of the 654 resolve to no table" against a lineage
 * in which nothing is unresolved. Nothing failed. Every page rendered, every
 * check passed, and the viewer quietly told its readers the wrong size of the
 * thing they were reviewing — which is the failure mode the whole tool exists
 * to catch in the delivery, reproduced in the tool itself.
 *
 * `lib/lineage.mjs` had already written the rule after the first time — *"a
 * number in a comment is a claim nothing checks"* — and then rotted a second
 * time nine lines below it, which is the argument for a check rather than a
 * habit.
 *
 * So tips now write `{operations}` and `public/tips.js` substitutes at hover.
 * This is the check that the substitution happens and lands on the truth:
 *
 *   1. no tip renders a raw `{token}` — an unknown one survives on purpose, so
 *      a typo shows up here rather than vanishing
 *   2. the numbers rendered are the numbers the API serves
 *
 * Runs against a gated viewer with an admin account, or against a throwaway
 * `TICVAI_NO_GATE=1` instance with none. See checks/README.md.
 */
import puppeteer from 'puppeteer-core';
import { authed, VIEWER } from './_session.mjs';

const BASE = VIEWER.replace(/\/+$/, '');

let pass = 0, fail = 0;
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

// Is the gate up? A throwaway instance answers the registry without a cookie,
// and signing in against an API that has no harness account would fail the run
// before it measured anything.
// `redirect: 'manual'` matters more than it looks: the gate answers 302 to
// login.html, and a followed redirect returns 200 with a page of HTML on it. A
// probe that only reads the status would call a gated viewer open, skip the
// sign-in, and then fail three steps later parsing the login page as JSON.
const gated = await fetch(`${BASE}/pkg/projects`, { redirect: 'manual' })
  .then((r) => r.status !== 200).catch(() => true);

// The registry is behind the gate too, so it needs the session when there is
// one. A bare fetch here answers 302 and the run dies claiming projects.json is
// empty, which is the wrong thing to go and look at.
const registry = await (gated ? authed(`${BASE}/pkg/projects`) : fetch(`${BASE}/pkg/projects`))
  .then((r) => (r.ok ? r.json() : null)).catch(() => null);

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000 });

const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

// `ticvai-api` has to be *set to empty*, never removed. An absent key falls
// through to the hardcoded `http://localhost:8787` in validation.js, which a
// throwaway instance on another port answers with a CORS failure — so the page
// concludes it is signed out and renders the login screen, and the check then
// measures a page with no layers on it and times out naming a selector.
await page.goto(BASE + '/invite.html', { waitUntil: 'domcontentloaded' });
// Empty, so the page talks to its own origin and the viewer proxies `/api/*`
// on to whatever `TICVAI_AUTH` names. That also settles the cookie: the session
// is `SameSite=lax`, so a login posted cross-origin — page on one port, API on
// another — is accepted by the API and then dropped by the browser, leaving the
// sign-in screen up with nothing in the console to say why.
await page.evaluate(() => localStorage.setItem('ticvai-api', ''));

if (gated) {
  await page.evaluate(async (e, p) => {
    await fetch('/api/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: e, password: p }),
    });
  },
    process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
    process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase');
}

const project = registry?.default
  ?? registry?.projects?.find((p) => p.active !== false)?.id;
if (!project) throw new Error('no project in /pkg/projects — is projects.json empty?');

await page.goto(`${BASE}/?project=${encodeURIComponent(project)}`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 30000 });
await wait(6000);

// The facts come off three payloads, and each is fetched when its layer is
// first opened. A tip hovered before then renders `{operations}` correctly —
// the number genuinely is not known yet — so the layers are walked first.
for (const layer of ['contracts', 'backend', 'frontend', 'decisions']) {
  await page.evaluate((l) => document.querySelector(`#layers button[data-layer="${l}"]`)?.click(), layer);
  await wait(2500);
}

// What the server says, which is what the tips must agree with.
const truth = await page.evaluate(async (p) => {
  const get = (r) => fetch(`/pkg/${p}/${r}`, { credentials: 'include' }).then((x) => (x.ok ? x.json() : null));
  const [lineage, journeys, decisions] = await Promise.all([get('lineage'), get('journeys'), get('decisions')]);
  return {
    operations: lineage?.stats?.operations,
    services: lineage?.stats?.services,
    unresolved: lineage?.stats?.unresolved,
    screens: lineage?.stats?.screens,
    platforms: journeys?.stats?.platforms,
    adrs: decisions?.adrs?.length,
  };
}, project);

check('the payloads carry the counts the tips ask for',
  Object.values(truth).every((v) => typeof v === 'number'), JSON.stringify(truth));

// Open each tokened tip and read what the panel actually shows.
//
// Dispatched rather than hovered. Most of these live in a toolbar belonging to
// a view that is not the open one, so `el.hover()` cannot reach them and fails
// silently — leaving the *previous* tip's text in the panel, which then reads
// as a pass for every element after the first. The listener is a delegated
// `mouseover` on the capture phase, so a bubbling event finds it wherever the
// element is, and each measurement is of the tip it names.
const measure = async () => page.evaluate(async (delay) => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const panel = () => document.querySelector('.tip-panel');
  const out = [];
  for (const node of document.querySelectorAll('[data-tip]')) {
    const raw = node.dataset.tip ?? '';
    if (!/\{[A-Za-z][A-Za-z0-9]*\}/.test(raw)) continue;
    if (panel()) { panel().hidden = true; panel().innerHTML = ''; }
    node.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
    await sleep(delay);
    out.push({ raw, shown: panel()?.innerText ?? '', hidden: panel()?.hidden ?? true });
  }
  return out;
}, 420);

// A mode button exists only while its own layer is open, and the view tips are
// on the mode buttons — so a single sweep sees whichever layer happened to be
// last and none of the others. Measuring per layer is the difference between
// covering three tips and covering all of them.
const results = [];
const byRaw = new Set();
for (const layer of ['contracts', 'backend', 'frontend', 'domain', 'decisions']) {
  await page.evaluate((l) => document.querySelector(`#layers button[data-layer="${l}"]`)?.click(), layer);
  await wait(2200);
  for (const row of await measure()) {
    if (byRaw.has(row.raw)) continue;   // the same tip on two layers is one tip
    byRaw.add(row.raw);
    results.push(row);
  }
}

check('the page has tips carrying a count token', results.length > 0, `${results.length} found`);
check('every one of them opened a panel',
  results.every((r) => !r.hidden && r.shown.trim().length > 0),
  results.filter((r) => r.hidden || !r.shown.trim()).map((r) => r.raw.slice(0, 50)).join(' | '));

const rawLeft = results.filter((r) => /\{[A-Za-z][A-Za-z0-9]*\}/.test(r.shown));
check('no tip renders a raw {token}', rawLeft.length === 0,
  rawLeft.map((r) => r.shown.replace(/\s+/g, ' ').slice(0, 70)).join(' | '));

// The token a tip asks for, resolved against the payload, must be the number
// the panel shows — not merely *a* number, and not a stale one that happens to
// still parse.
let checked = 0;
for (const r of results) {
  for (const [, key] of r.raw.matchAll(/\{([A-Za-z][A-Za-z0-9]*)\}/g)) {
    const value = truth[key];
    if (typeof value !== 'number') continue;
    checked += 1;
    check(`{${key}} renders as ${value}`, r.shown.includes(String(value)),
      r.shown.replace(/\s+/g, ' ').slice(0, 90));
  }
}
check('at least one token was checked against the payload', checked > 0, `${checked} checked`);

const body = results.map((r) => r.shown).join('\n');
check('no tip still quotes a retired figure',
  !/\b654\b|\b22 services\b|\b18 ADRs\b|\b318 of\b|\b347 screens\b/.test(body));

check('no console or page errors', errors.length === 0, errors.slice(0, 4).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
