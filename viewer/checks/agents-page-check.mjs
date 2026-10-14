/**
 * Agent activity (agents.html): it opens on the answer, the rail shows one
 * section at a time, the filter lives in the address, and its figures are the
 * service's whole-window counts rather than the length of a capped list.
 *
 * The rail used to do nothing: the page loaded `set-layout` and never called
 * `mountPanels`, so every section was stacked and the links only scrolled. And
 * its "sessions" card counted a list the service caps at a hundred, while the
 * per-person totals beside it summed five hundred. Both are asserted here
 * against what the service itself says.
 *
 * Reads only. Needs sessions in the window to be worth running; with none it
 * checks the empty state instead and says so.
 *
 *   TICVAI_VIEWER=http://localhost:4205 TICVAI_API=http://localhost:8805 \
 *     node checks/agents-page-check.mjs
 */
import puppeteer from 'puppeteer-core';
import { VIEWER, API } from './_session.mjs';

const BASE = VIEWER.replace(/\/+$/, '');
const APIB = API.replace(/\/+$/, '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push(e.message));
await page.setViewport({ width: 1500, height: 1000 });
await page.goto(`${BASE}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate((a) => localStorage.setItem('ticvai-api', a), APIB);
await page.evaluate(async (a) => fetch(`${a}/api/auth/login`, {
  method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
}), APIB);

const usage = (q) => page.evaluate(async (a, query) => (await fetch(`${a}/api/agent/usage?${query}`, { credentials: 'include' })).json(), APIB, q);

await page.goto(`${BASE}/agents.html`, { waitUntil: 'networkidle2' });
await wait(1200);
const truth = await usage('days=14');
const first = await page.evaluate(() => ({
  shown: [...document.querySelectorAll('.set-section')].filter((s) => !s.hidden).map((s) => s.id),
  headline: document.querySelector('#ag-headline')?.textContent ?? '',
  h1: document.querySelector('h1')?.textContent,
  ledger: Object.fromEntries([...document.querySelectorAll('.sh-ledger-item')]
    .map((i) => [i.querySelector('dt').textContent.trim(), i.querySelector('dd').textContent.replace(/[^\d]/g, '')])),
  rail: document.querySelector('#ag-nav-overview')?.textContent,
}));
check('the page is called Agent activity', first.h1 === 'Agent activity', first.h1);
check('it opens on the overview alone', JSON.stringify(first.shown) === '["overview"]', first.shown.join(' '));
check('the rail names the window', first.rail === 'This fortnight', first.rail);

if (!truth.totals?.sessions) {
  check('with nothing in the window, it says nothing arrived and how to fix it',
    /Nothing has arrived/.test(first.headline)
    && await page.evaluate(() => /plugin install adam@adam/.test(document.querySelector('#ag-nothing')?.textContent ?? '')),
    first.headline);
} else {
  check('the headline answers who used it', /used the agent|across/.test(first.headline), first.headline);
  check('the sessions figure is the window\'s true count, not the capped list',
    Number(first.ledger.Sessions) === truth.sessionCount, `${first.ledger.Sessions} on the page, ${truth.sessionCount} counted`);
  check('and the failed figure is the tools\' sum',
    Number(first.ledger.Failed) === truth.totals.failed, `${first.ledger.Failed} vs ${truth.totals.failed}`);
  const worst = truth.tools.find((t) => t.failed);
  if (worst) {
    const bars = await page.evaluate(() => [...document.querySelectorAll('#ag-bars .ag-bar-row')]
      .map((r) => [r.querySelector('.sh-bar-label').textContent, r.querySelector('.sh-bar-count').textContent]));
    check('the bold thing is failures by tool, the worst first, with its count',
      bars[0]?.[1] === String(worst.failed), JSON.stringify(bars.slice(0, 3)));
    check('with a legend and a table twin',
      await page.evaluate(() => Boolean(document.querySelector('#ag-bars-key .sh-legend')
        && document.querySelector('#ag-bars-twin table'))));
  }
}

// ── the rail is one section at a time ────────────────────────────────
await page.evaluate(() => document.querySelector('.set-nav a[href="#tools"]').click());
await wait(300);
check('a rail link shows its section and hides the rest',
  await page.evaluate(() => location.hash === '#tools'
    && [...document.querySelectorAll('.set-section')].filter((s) => !s.hidden).map((s) => s.id).join() === 'tools'
    && document.querySelector('.set-nav a[href="#tools"]').getAttribute('aria-current') === 'true'));

// ── the filter is in the address ─────────────────────────────────────
await page.evaluate(() => {
  const s = [...document.querySelectorAll('#ag-scope select')][0];
  s.value = '30';
  s.dispatchEvent(new Event('change'));
});
await wait(1500);
check('choosing a window puts it in the address and names it on the rail',
  await page.evaluate(() => location.search.includes('days=30')
    && document.querySelector('#ag-nav-overview').textContent === 'Last 30 days'));

const people = truth.people ?? [];
if (people.length && truth.whole) {
  const who = people[people.length - 1];
  await page.goto(`${BASE}/agents.html?person=${encodeURIComponent(who.name)}#sessions`, { waitUntil: 'networkidle2' });
  await wait(1500);
  const narrowed = await page.evaluate(() => ({
    says: document.querySelector('.sh-says')?.textContent,
    picked: [...document.querySelectorAll('#ag-scope select')][1]?.value,
    whos: [...new Set([...document.querySelectorAll('#ag-sessions tbody tr:not(.ag-detail) td:nth-child(2)')].map((t) => t.textContent))],
  }));
  check('a link with ?person= opens narrowed to that person, and says so',
    narrowed.picked === who.name && narrowed.says?.includes(who.name), JSON.stringify(narrowed));
  check('and every session listed is theirs', narrowed.whos.length === 1 && narrowed.whos[0] === who.name,
    narrowed.whos.join(', '));
  const linked = await page.evaluate(() => document.querySelector('#ag-sessions a.sh-link')?.getAttribute('href'));
  check('names lead to that person on Tasks', /^\/tasks\.html\?person=.+#person$/.test(linked ?? ''), linked);
  await page.evaluate(() => document.querySelector('#ag-sessions .ag-open').click());
  await wait(1200);
  check('a session opens into its events',
    await page.evaluate(() => document.querySelector('#ag-sessions .ag-open').getAttribute('aria-expanded') === 'true'
      && document.querySelectorAll('#ag-sessions .ag-event').length > 0));
}

check('no page errors', errors.length === 0, errors.slice(0, 3).join(' | '));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
