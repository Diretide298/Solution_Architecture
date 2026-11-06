/**
 * Walk ADAM's pages as the lead's phone sees them (420 x 933, touch, 3x), a screen at a time.
 * Each page: open it, screenshot, scroll by a finger's swipe from the middle of the screen, screenshot again,
 * up to four screens. A page that is taller than the screen but does not move is reported STUCK; a page wider
 * than the screen is reported WIDE. Unlike phone-shots.mjs --full it never unlocks the page's own scrolling.
 *
 *   PHONE_VIEWER=http://localhost:8702 PHONE_EMAIL=... PHONE_PASSWORD=... node checks/phone-walk.mjs <out dir> [pages]
 */
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const [out, list] = process.argv.slice(2);
const base = process.env.PHONE_VIEWER;
const pages = (list ?? 'home,decide,board,changes,reviews,tasks,plan,settings,admin,audit,agents,domains,costing,ips,chat,document,updates,viewer').split(',');
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const context = await browser.newContext({ viewport: { width: 420, height: 933 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'dark' });
await context.addInitScript(() => { localStorage.setItem('ticvai-api', ''); localStorage.setItem('ticvai-theme', 'dark'); });
const page = await context.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message.slice(0, 160)));
await page.goto(`${base}/login.html`, { waitUntil: 'domcontentloaded' });
const status = await page.evaluate(async ({ email, password }) => (await fetch('/api/auth/login', {
  method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password }),
})).status, { email: process.env.PHONE_EMAIL, password: process.env.PHONE_PASSWORD });
if (status !== 200) throw new Error(`sign-in answered ${status}`);
const where = () => page.evaluate(() => {
  let y = Math.max(scrollY, document.body.scrollTop);
  for (const el of document.querySelectorAll('body *')) if (el.scrollTop > 0 && el.clientHeight > innerHeight * 0.4) y = Math.max(y, el.scrollTop);
  const d = document.documentElement;
  return { y, tall: Math.max(d.scrollHeight, document.body.scrollHeight), wide: Math.max(d.scrollWidth, document.body.scrollWidth) };
});
for (const name of pages) {
  errors.length = 0;
  const url = name === 'viewer' ? '/' : name === 'decide' ? '/decide' : `/${name}.html`;
  await page.goto(base + url, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1200);
  const first = await where();
  let shots = 1, stuck = false, prev = first.y;
  await page.screenshot({ path: path.join(out, `${name}-1.png`) });
  for (let i = 2; i <= 4; i++) {
    await page.mouse.move(210, 520);
    await page.mouse.wheel(0, 760);
    await page.waitForTimeout(700);
    const now = await where();
    if (now.y <= prev + 5) { if (i === 2 && first.tall > 933 + 40) stuck = true; break; }
    prev = now.y; shots = i;
    await page.screenshot({ path: path.join(out, `${name}-${i}.png`) });
  }
  console.log(`${stuck ? 'STUCK ' : ''}${first.wide > 422 ? 'WIDE ' : ''}${name}: ${shots} screen(s), page ${first.tall}px tall${first.wide > 422 ? `, ${first.wide}px wide` : ''}${page.url().includes(url) ? '' : `, landed on ${new URL(page.url()).pathname}`}${errors.length ? ` | errors: ${errors.join(' ; ')}` : ''}`);
}
await browser.close();
