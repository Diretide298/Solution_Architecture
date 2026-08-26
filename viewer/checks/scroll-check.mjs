// styles.css puts `overflow: hidden` on html and body for the app shell, and
// every standalone page loads the same stylesheet. Anything past the fold on
// one of them was unreachable — no scrollbar, no wheel, no keyboard. This holds
// all four of them open, at a height where each really does overflow.
import puppeteer from 'puppeteer-core';
const VIEWER = 'http://localhost:4173';
const API = 'http://localhost:8787';
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

await page.setViewport({ width: 1200, height: 800 });
await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate(async (api) => {
  await fetch(`${api}/api/auth/login`, {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
  });
}, API);

// A short viewport, so a page that fits at 800px still has to scroll here and
// the check is about scrolling rather than about how much content there is.
const SIZES = [
  ['desktop', 1200, 420],
  ['phone', 390, 620],
];

const PAGES = [
  ['/admin.html', '.admin-panel'],
  ['/validation.html', '.signoff-card'],
  ['/login.html', '.auth-card'],
  ['/invite.html', '.auth-card'],
];

for (const [label, width, height] of SIZES) {
  await page.setViewport({ width, height });
  for (const [path, ready] of PAGES) {
    await page.goto(`${VIEWER}${path}`, { waitUntil: 'domcontentloaded' });
    await page.waitForSelector(ready, { timeout: 25000 }).catch(() => null);
    await wait(1800);

    // `document.scrollingElement` is <html>, and <html> is exactly the element
    // that must never scroll here — measuring it passes whatever is true.
    const before = await page.evaluate(() => {
      const scroller = document.body;
      return {
        top: scroller.scrollTop,
        scrollHeight: scroller.scrollHeight,
        clientHeight: scroller.clientHeight,
        bodyOverflow: getComputedStyle(document.body).overflowY,
      };
    });

    const overflows = before.scrollHeight > before.clientHeight + 4;
    if (!overflows) {
      check(`${label} ${path} — fits without scrolling`, true,
        `${before.scrollHeight}px in ${before.clientHeight}px`);
      continue;
    }

    // scroll it the way a person would, not by setting scrollTop
    await page.mouse.move(width / 2, height / 2);
    await page.mouse.wheel({ deltaY: 600 });
    await wait(400);
    const after = await page.evaluate(() => document.body.scrollTop);

    check(`${label} ${path} — the wheel moves it`, after > 0,
      `${before.scrollHeight}px of content in ${before.clientHeight}px, scrolled to ${after} (body overflow-y: ${before.bodyOverflow})`);

    // and the bottom is actually reachable
    await page.evaluate(() => { document.body.scrollTop = document.body.scrollHeight; });
    await wait(300);
    const bottom = await page.evaluate(() => {
      const s = document.body;
      return s.scrollTop + s.clientHeight >= s.scrollHeight - 4;
    });
    check(`${label} ${path} — the bottom is reachable`, bottom);
  }
}

// The app shell must NOT gain a document scrollbar: its panes scroll on their
// own, and a second one with nothing in it is what the hidden overflow is for.
await page.setViewport({ width: 1200, height: 500 });
await page.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 25000 });
await wait(3000);
const shell = await page.evaluate(() => ({
  overflow: getComputedStyle(document.body).overflowY,
  scrolls: document.body.scrollHeight > document.body.clientHeight + 4
        || document.scrollingElement.scrollHeight > document.scrollingElement.clientHeight + 4,
}));
check('the viewer itself still does not scroll as a document', !shell.scrolls,
  `body overflow-y: ${shell.overflow}`);

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
