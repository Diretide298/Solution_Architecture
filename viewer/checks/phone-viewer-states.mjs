/**
 * The viewer's phone states that a walk of the views does not reach: a galaxy's
 * focus card after a tap, the drawers, More, the palette, the bell, the account
 * drawer, the UI/UX canvas under a pinch and a design diagram under a pinch.
 * 420 x 933, touch, safe areas 54/48. Viewport screenshots into <out>/.
 *
 *   PHONE_VIEWER=http://localhost:8702 PHONE_EMAIL=... PHONE_PASSWORD=... node checks/phone-viewer-states.mjs <out>
 */
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const out = process.argv[2];
const base = process.env.PHONE_VIEWER ?? 'http://localhost:8702';
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const ctx = await browser.newContext({ viewport: { width: 420, height: 933 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'dark' });
await ctx.addInitScript(() => { localStorage.setItem('ticvai-theme', 'dark'); sessionStorage.setItem('ticvai-session', '1'); });
const page = await ctx.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message.slice(0, 160)));
await page.goto(`${base}/login.html`);
const status = await page.evaluate(async ({ email, password }) => (await fetch('/api/auth/login', { method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password }) })).status, { email: process.env.PHONE_EMAIL, password: process.env.PHONE_PASSWORD });
if (status !== 200) throw new Error(`sign-in answered ${status}`);
const cdp = await ctx.newCDPSession(page);
await cdp.send('Emulation.setSafeAreaInsetsOverride', { insets: { top: 54, bottom: 48, left: 0, right: 0 } }).catch(() => {});
const shot = (name) => page.screenshot({ path: path.join(out, `${name}.png`) });
const open = async (q) => {
  await page.goto(`${base}/${q}`, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2200);
};
const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', { type, touchPoints: pts });
const tap = async (x, y) => { await touch('touchStart', [{ x, y }]); await page.waitForTimeout(40); await touch('touchEnd', []); await page.waitForTimeout(500); };
const pinch = async (cx, cy, from, to) => {
  const steps = 10;
  await touch('touchStart', [{ x: cx - from, y: cy, id: 1 }, { x: cx + from, y: cy, id: 2 }]);
  for (let i = 1; i <= steps; i++) {
    const d = from + ((to - from) * i) / steps;
    await touch('touchMove', [{ x: cx - d, y: cy, id: 1 }, { x: cx + d, y: cy, id: 2 }]);
    await page.waitForTimeout(16);
  }
  await touch('touchEnd', []);
  await page.waitForTimeout(500);
};
const say = (s) => console.log(s);

// 1. A galaxy: tap until a body is picked, then the card and its button.
for (const q of ['?layer=services&mode=services-graph', '?layer=domain&mode=events', '?layer=frontend&mode=apps']) {
  await open(q);
  const box = await page.evaluate(() => { const r = document.querySelector('#main > .view:not([hidden])').getBoundingClientRect(); return { top: r.top, bottom: r.bottom }; });
  let found = null;
  outer: for (let y = box.top + 140; y < box.bottom - 120; y += 34) {
    for (let x = 60; x < 380; x += 34) {
      await tap(x, y);
      if (await page.locator('.galaxy-focus').count()) { found = { x, y }; break outer; }
    }
  }
  const name = q.split('mode=')[1];
  if (!found) { say(`${name}: no body picked by a tap`); await shot(`galaxy-${name}-none`); continue; }
  const card = await page.evaluate(() => {
    const c = document.querySelector('.galaxy-focus');
    const b = c.querySelector('.galaxy-focus-open');
    const r = c.getBoundingClientRect();
    return { name: c.querySelector('.galaxy-focus-name')?.textContent, open: b?.textContent ?? null, bottom: Math.round(r.bottom), openH: b ? Math.round(b.getBoundingClientRect().height) : 0 };
  });
  say(`${name}: tap at ${found.x},${found.y} picked "${card.name}", button "${card.open}" ${card.openH}px, card bottom ${card.bottom}`);
  await shot(`galaxy-${name}-focus`);
  // A drag turns the scene (pixels change).
  const before = await page.screenshot({ clip: { x: 0, y: box.top + 60, width: 420, height: 300 } });
  await touch('touchStart', [{ x: 120, y: box.top + 200 }]);
  for (let i = 1; i <= 8; i++) { await touch('touchMove', [{ x: 120 + i * 20, y: box.top + 200 }]); await page.waitForTimeout(16); }
  await touch('touchEnd', []);
  await page.waitForTimeout(400);
  const after = await page.screenshot({ clip: { x: 0, y: box.top + 60, width: 420, height: 300 } });
  say(`${name}: a one-finger drag ${before.equals(after) ? 'changed nothing' : 'turned the scene'}`);
  if (card.open) {
    const was = page.url();
    await page.locator('.galaxy-focus-open').tap();
    await page.waitForTimeout(2500);
    say(`${name}: Open went from ${new URL(was).search} to ${new URL(page.url()).search}${await page.locator('#sidebar-right').isVisible() ? ' (links drawer open)' : ''}`);
    await shot(`galaxy-${name}-opened`);
  }
}

// 2. The drawers, More, the palette, the bell and the account drawer.
await open('?layer=contracts&mode=graph');
await page.locator('#drawer-left-toggle').tap(); await page.waitForTimeout(500); await shot('drawer-left');
await page.locator('#drawer-left-toggle').tap(); await page.waitForTimeout(400);
await page.locator('#phone-more').tap(); await page.waitForTimeout(600); await shot('more');
say(`more: ${await page.locator('#phone-menu-body a.drawer-link').count()} links, ${await page.locator('#phone-menu .phone-seg button').count()} theme buttons`);
await page.locator('#phone-menu-close').tap(); await page.waitForTimeout(400);
await page.locator('#search-trigger').tap(); await page.waitForTimeout(500);
await page.keyboard.type('order');
await page.waitForTimeout(900); await shot('palette');
await page.keyboard.press('Escape'); await page.waitForTimeout(300);
await page.locator('#account-toggle').tap(); await page.waitForTimeout(600); await shot('account');
await page.keyboard.press('Escape'); await page.waitForTimeout(300);
if (await page.locator('#bell-toggle').isVisible()) { await page.locator('#bell-toggle').tap(); await page.waitForTimeout(600); await shot('bell'); await page.keyboard.press('Escape'); }

// 3. The UI/UX canvas: pinch in.
await open('?layer=uiux&mode=uiux-screens');
const z0 = await page.locator('#zoom-level').textContent();
await pinch(210, 600, 40, 160);
const z1 = await page.locator('#zoom-level').textContent();
say(`uiux canvas: pinch took the zoom from ${z0} to ${z1}`);
await shot('uiux-pinched');
await tap(210, 640);
await shot('uiux-tapped');
say(`uiux canvas: after a tap the pane is "${await page.evaluate(() => document.querySelector('#view-uiux-screens .phone-pane.is-phone-on')?.id || document.querySelector('#view-uiux-screens .phone-pane.is-phone-on')?.className)}"`);

// 4. A design diagram: pinch in.
await open('?layer=services&mode=hld');
const w0 = await page.evaluate(() => Math.round(document.querySelector('#hld-body .dia-frame svg').getBoundingClientRect().width));
const fy = await page.evaluate(() => { const r = document.querySelector('#hld-body .dia-frame').getBoundingClientRect(); return Math.round(Math.min(r.top + 160, 700)); });
await pinch(210, fy, 120, 40);
const w1 = await page.evaluate(() => Math.round(document.querySelector('#hld-body .dia-frame svg').getBoundingClientRect().width));
say(`diagram: pinch out took the drawing from ${w0}px to ${w1}px wide`);
await shot('diagram-pinched');

say(errors.length ? `errors: ${[...new Set(errors)].join(' ; ')}` : 'no page errors');
await browser.close();
