/**
 * Every page can be narrowed, and narrowing it says what it did.
 *
 * `platforms`, `uiux` and `validation` each filter their own data before
 * rendering. `domains` had a segmented control and no text box; `reviews` and
 * `admin` had nothing at all — so finding one reviewer among ninety, or one
 * account, meant Ctrl+F, which highlights the word and leaves the rest of the
 * page around it.
 *
 * The three claims, in the order they matter:
 *
 *   it narrows       typing hides the rows that do not match
 *   it counts        "12 of 90", with the denominator, because a bare 12 beside
 *                    a filter box cannot be read
 *   it survives      the rows arrive after the payload and some pages redraw on
 *                    a tab change, so a filter typed first has to still be
 *                    applied afterwards — the MutationObserver is the whole
 *                    reason this is not three lines of oninput
 */
import puppeteer from 'puppeteer-core';
import { VIEWER, API } from './_session.mjs';

const BASE = VIEWER.replace(/\/+$/, '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

let pass = 0, fail = 0;
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};

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

// Every page that reads the package, and what a row is on it. `platforms`,
// `uiux` and `validation` use their own field; the other three use the shared
// one. Both are checked, because "every page can be narrowed" is the claim and
// it does not care which implementation answers it.
const PAGES = [
  { url: '/platforms.html', input: '#filter', rows: '.plat-card' },
  { url: '/uiux.html', input: '#filter', rows: '.uiux-card' },
  { url: '/domains.html', input: '#subsearch', rows: '.member-row, .stuck-row, .gap-row' },
  { url: '/reviews.html', input: '#subsearch', rows: '.people-row, .contested-row, .mention-row' },
  { url: '/admin.html', input: '#subsearch', rows: '.account-row' },
];

const missing = [];
const notNarrowed = [];

for (const p of PAGES) {
  await page.goto(BASE + p.url, { waitUntil: 'domcontentloaded' });
  await wait(5000);

  const has = await page.evaluate((sel) => Boolean(document.querySelector(sel)), p.input);
  if (!has) { missing.push(p.url); continue; }

  const before = await page.evaluate((sel) => document.querySelectorAll(sel).length, p.rows);
  if (!before) continue;   // nothing drawn on this instance; nothing to narrow

  // A string nothing can contain. Everything should end up hidden, which is the
  // strongest form of "it is actually filtering" — a filter that matches
  // everything is indistinguishable from one that does nothing.
  await page.evaluate((sel) => {
    const i = document.querySelector(sel);
    i.value = 'zzqqxx-no-such-thing';
    i.dispatchEvent(new Event('input'));
  }, p.input);
  await wait(900);
  const after = await page.evaluate((sel) => {
    const all = [...document.querySelectorAll(sel)];
    return all.filter((r) => !r.hidden && r.offsetParent !== null).length;
  }, p.rows);

  if (after !== 0) notNarrowed.push(`${p.url}: ${before} -> ${after}`);
}

check('every page that lists things has a filter', missing.length === 0,
  `${PAGES.length} pages${missing.length ? ' | without: ' + missing.join(', ') : ''}`);
check('and a filter that matches nothing leaves nothing showing',
  notNarrowed.length === 0, notNarrowed.join(' | ') || 'all narrowed to zero');

// ── the count keeps its denominator ──────────────────────────────────
await page.goto(BASE + '/admin.html', { waitUntil: 'domcontentloaded' });
await wait(5000);
const total = await page.evaluate(() => document.querySelectorAll('.account-row').length);
await page.evaluate(() => {
  const i = document.querySelector('#subsearch');
  i.value = 'harness';
  i.dispatchEvent(new Event('input'));
});
await wait(800);
const counted = await page.evaluate(() => document.getElementById('subsearch-count')?.textContent ?? '');
check('the count says how many of how many', / of \d+/.test(counted), `"${counted}" of ${total} rows`);

const shown = await page.evaluate(
  () => [...document.querySelectorAll('.account-row')].filter((r) => !r.hidden).length
);
check('and matches what is actually left showing',
  counted.startsWith(String(shown)), `${counted} vs ${shown} visible`);

// ── it survives a redraw ─────────────────────────────────────────────
// The rows are rebuilt from scratch here. A plain oninput filter would be
// silently undone, and the page would show every row under a filter that still
// says it is filtering — which is worse than not filtering at all.
const survived = await page.evaluate(async () => {
  const box = document.getElementById('accounts');
  const one = box.querySelector('.account-row');
  if (!one) return null;
  const clone = one.cloneNode(true);
  clone.hidden = false;
  box.append(clone);           // a row arriving after the filter was typed
  await new Promise((r) => setTimeout(r, 500));
  return clone.hidden;
});
check('a row drawn after the filter is filtered too',
  survived === true, survived === null ? 'no rows to test with' : `hidden=${survived}`);

check('no console or page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
