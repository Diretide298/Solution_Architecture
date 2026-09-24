// The "what's new" marker, end to end.
//
// The thing worth proving is not that a chip can be drawn. It is the cycle: it
// appears on a page somebody actually lands on, it survives a reload (otherwise
// it is a decoration that happens to be there once), it goes away when the notes
// are read, it stays away — and it comes back when the notes change, because a
// marker that only ever fires once is a marker nobody trusts the second time.
import puppeteer from 'puppeteer-core';
import { readFile, writeFile } from 'node:fs/promises';

//   node server.mjs                     # the viewer, on 4173
//   node checks/updates-check.mjs

const V = 'http://localhost:4173';
const NOTES = new URL('../public/updates.md', import.meta.url);
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const noise = [];
const page = await browser.newPage();
await page.setViewport({ width: 1500, height: 1000 });
page.on('console', (m) => { if (m.type() === 'error') noise.push(m.text()); });
page.on('pageerror', (e) => noise.push(String(e)));
await page.evaluateOnNewDocument((api) => {
  try { localStorage.setItem('ticvai-api', api); } catch { /* nothing to do */ }
}, V);

await page.goto(`${V}/login.html`, { waitUntil: 'domcontentloaded' });
check('signed in', await page.evaluate(async () => (await fetch('/api/auth/login', {
  method: 'POST', credentials: 'include',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: 'harness.boss@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
})).ok));

// The session cookie is set by a fetch, and the browser's cookie jar is not
// necessarily ready for the next *navigation* the instant that fetch resolves.
// Without this the first page opened here is served as a stranger and redirected
// to the landing page, which then looks exactly like a marker that did not fire.
for (let tries = 0; tries < 40; tries += 1) {
  const jar = await page.cookies();
  if (jar.some((c) => c.name === 'ticvai_session')) break;
  await new Promise((r) => setTimeout(r, 100));
}
check('the session cookie is in the jar',
  (await page.cookies()).some((c) => c.name === 'ticvai_session'));

// One throwaway navigation before anything is asserted.
//
// Signing in here is a fetch, and the gate serves the first *document* request
// after it as a stranger -- /index.html comes back as the public landing page
// even though the session cookie is in the jar and a fetch carrying it has just
// been answered. Every later navigation is fine. That is the gate's behaviour in
// lib/session.mjs and it reproduces without any of this marker's code, so it is
// warmed past here rather than asserted on: this file tests the marker.
await page.goto(`${V}/index.html`, { waitUntil: 'domcontentloaded' });
await new Promise((r) => setTimeout(r, 1500));

const stampNow = () => page.evaluate(async () =>
  (await (await fetch('/updates/stamp')).json()).stamp);
const chip = async (where) => {
  await page.goto(`${V}${where}`, { waitUntil: 'domcontentloaded' });
  // Wait for the chrome to exist, then give the marker a bounded chance to
  // appear. A flat sleep is what made this flap: the viewer's first load builds
  // a great deal before it mounts the drawer, and every later visit is warm.
  await page.waitForSelector('#account-toggle', { timeout: 20000 }).catch(() => {});
  await page.waitForFunction(() => !!document.getElementById('updates-new'), { timeout: 6000 })
    .catch(() => { /* genuinely absent is an answer this test needs */ });
  const landed = new URL(page.url()).pathname;
  if (landed !== where) console.log(`      (asked for ${where}, landed on ${landed})`);
  return page.evaluate(() => {
    const c = document.getElementById('updates-new');
    if (!c) return null;
    const box = c.getBoundingClientRect();
    return {
      text: c.textContent.trim(),
      href: new URL(c.href).pathname,
      label: c.getAttribute('aria-label') ?? '',
      // In the DOM is not the same as on screen.
      visible: box.width > 0 && box.height > 0 && getComputedStyle(c).visibility !== 'hidden',
      beforeToggle: c.nextElementSibling?.id === 'account-toggle',
    };
  });
};

const first = await stampNow();
check('the viewer stamps the notes', /^[0-9a-f]{12}$/.test(first ?? ''), first);

// ── it shows up where people land ────────────────────────────────────

// `/index.html` rather than `/`: a cold visit to `/` is redirected to the public
// landing page even for a signed-in reader, which is the gate's own behaviour and
// nothing to do with this marker. Asserting on `/` would make this test fail for
// a reason it is not testing.
const onRoot = await chip('/index.html');
check('the chip is on the viewer', !!onRoot, JSON.stringify(onRoot));
check('and is actually visible, not just in the DOM', onRoot?.visible === true);
check('it sits in the bar beside the account button', onRoot?.beforeToggle === true);
check('it goes to the notes', onRoot?.href === '/updates.html', onRoot?.href);
check('and says so to a screen reader too', /unread release notes/.test(onRoot?.label ?? ''),
  onRoot?.label);

const onSettings = await chip('/settings.html');
check('and on a standalone page with the shared chrome', !!onSettings);

check('it survives a reload while unread', !!(await chip('/index.html')));

// ── reading them puts it away ────────────────────────────────────────

await page.goto(`${V}/updates.html`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#up-body .md', { timeout: 20000 });
await new Promise((r) => setTimeout(r, 1200));
const seen = await page.evaluate(() => { try { return localStorage.getItem('adam-updates-seen'); } catch { return null; } });
check('reading the notes records the stamp', seen === first, `${seen} vs ${first}`);

check('and the chip is gone from the viewer', (await chip('/index.html')) === null);
check('still gone after another visit', (await chip('/settings.html')) === null);

// ── and it comes back when the notes change ──────────────────────────

const original = await readFile(NOTES, 'utf8');
try {
  await writeFile(NOTES, `${original}\n<!-- harness: a change to the notes -->\n`, 'utf8');
  const second = await stampNow();
  check('editing the notes moves the stamp', second !== first && /^[0-9a-f]{12}$/.test(second),
    `${first} -> ${second}`);
  const again = await chip('/index.html');
  check('and the chip comes back', !!again, JSON.stringify(again));
} finally {
  await writeFile(NOTES, original, 'utf8');
}
const restored = await stampNow();
check('putting the notes back restores the original stamp', restored === first,
  `${restored} vs ${first}`);

// ── the mascot ───────────────────────────────────────────────────────

await page.goto(`${V}/updates.html`, { waitUntil: 'domcontentloaded' });
// The panel starts hidden and updates.js reveals it, so waiting for the image to
// exist measures it while it is still in a hidden container -- which is how a
// perfectly good 96px image reports a width of zero.
await page.waitForSelector('#up-body .md', { timeout: 20000 });
await page.waitForFunction(
  () => document.querySelector('.up-mascot')?.getBoundingClientRect().width > 0,
  { timeout: 10000 },
).catch(() => {});
const mascot = await page.evaluate(() => {
  const img = document.querySelector('.up-mascot');
  return { w: img.naturalWidth, h: img.naturalHeight, drawn: img.getBoundingClientRect().width };
});
check('the mascot frame loads', mascot.w === 256 && mascot.h === 204, `${mascot.w}x${mascot.h}`);
check('and is drawn on the page', mascot.drawn > 0, `${mascot.drawn}px wide`);

check('nothing shouted on the way', noise.length === 0, noise.slice(0, 2).join(' | '));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
