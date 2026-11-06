/**
 * Phone screenshots of ADAM's pages, before and after a change.
 *
 * README
 * ------
 * What it does, from nothing:
 *   1. copies a database to a temporary file (the source is only ever read),
 *   2. makes or resets one owner account in the COPY, with a random password
 *      that lives only in this process,
 *   3. starts the accounts service (uvicorn) and the viewer (server.mjs) on
 *      free ports, pointed at the copy,
 *   4. signs in through a real browser and screenshots each page at phone
 *      sizes, in night and day, as a touch device (coarse pointer),
 *   5. prints, per shot, whether the page scrolls sideways and how many visible
 *      controls are smaller than 44 px (the touch floor in DESIGN-SYSTEM.md).
 *
 *     npm i --no-save playwright-core          # once; uses the installed Chrome
 *     node checks/phone-shots.mjs --label before
 *     node checks/phone-shots.mjs --label after --pages settings,admin --desktop
 *
 * Options:
 *   --label <name>      subfolder per page: .shots/phone/<page>/<label>/ (default "now")
 *   --pages a,b,c       page names (the file name without .html) or "chrome";
 *                       default: the chrome and every batch B page
 *   --sizes WxH,WxH     default 390x844,360x780
 *   --themes dark,light default both
 *   --desktop           also one 1440x900 shot per page and theme
 *   --walk <dir>        instead of shooting, run checks/phone-walk.mjs against
 *                       the servers this started (it swipes each page a screen
 *                       at a time at 420x933 and reports STUCK and WIDE); the
 *                       account is handed to it through its environment
 *   --full              also a full-length shot per size and theme
 *   --sections          also every section of a page with a section rail
 *                       (.set-nav), full length, into <page>/<label>/sections/
 *
 * Environment:
 *   PHONE_DB_SOURCE     the database to copy (default: api/ticvai.db beside
 *                       this viewer). Never opened for writing.
 *   PHONE_VIEWER        reuse a running viewer instead of starting one; then
 *                       PHONE_EMAIL and PHONE_PASSWORD must name an account on
 *                       it. Nothing is created in that case.
 *   CHROME              the Chrome executable (default: the usual Windows path)
 *
 * "chrome" is not a page: it opens /board.html and shoots the shared frame's
 * states (the menu sheet, the account drawer, the bell) so batch A can be
 * judged on its own.
 *
 * The output folder is .shots/, which is gitignored. No password is written
 * anywhere and none is printed.
 */
import { spawn, spawnSync } from 'node:child_process';
import { randomBytes } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, rmSync } from 'node:fs';
import { createServer } from 'node:net';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const here = path.dirname(fileURLToPath(import.meta.url));
const VIEWER_DIR = path.resolve(here, '..');
const OUT = path.join(VIEWER_DIR, '.shots', 'phone');

const BATCH_B = ['settings', 'admin', 'audit', 'agents', 'domains', 'costing', 'reviews', 'changes', 'board'];

const argv = process.argv.slice(2);
const opt = (name, fallback) => {
  const at = argv.indexOf(`--${name}`);
  return at >= 0 && argv[at + 1] && !argv[at + 1].startsWith('--') ? argv[at + 1] : fallback;
};
const flag = (name) => argv.includes(`--${name}`);

const label = opt('label', 'now');
const pages = opt('pages', ['chrome', ...BATCH_B].join(',')).split(',').map((s) => s.trim()).filter(Boolean);
const sizes = opt('sizes', '390x844,360x780').split(',').map((s) => s.split('x').map(Number));
const themes = opt('themes', 'dark,light').split(',');
const CHROME = process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const freePort = () => new Promise((resolve, reject) => {
  const s = createServer();
  s.unref();
  s.on('error', reject);
  s.listen(0, '127.0.0.1', () => { const { port } = s.address(); s.close(() => resolve(port)); });
});

const waitFor = async (url, ms = 90_000) => {
  const until = Date.now() + ms;
  while (Date.now() < until) {
    try { const r = await fetch(url); if (r.status < 500) return; } catch { /* not yet */ }
    await new Promise((r) => setTimeout(r, 400));
  }
  throw new Error(`${url} did not answer within ${ms / 1000}s`);
};

const children = [];
const cleanup = [];
const stopAll = () => {
  for (const c of children) { try { c.kill(); } catch { /* gone */ } }
  for (const f of cleanup) { try { rmSync(f, { force: true }); } catch { /* held */ } }
};
process.on('exit', stopAll);
process.on('SIGINT', () => { stopAll(); process.exit(130); });

async function startServers() {
  const source = process.env.PHONE_DB_SOURCE ?? path.join(VIEWER_DIR, 'api', 'ticvai.db');
  if (!existsSync(source)) throw new Error(`No database at ${source}; set PHONE_DB_SOURCE.`);
  const copy = path.join(tmpdir(), `adam-phone-${process.pid}.db`);
  copyFileSync(source, copy);
  cleanup.push(copy, `${copy}-wal`, `${copy}-shm`);

  const email = 'phone.shots@softlabsgroup.com';
  const password = randomBytes(18).toString('base64url');
  const env = { ...process.env, TICVAI_DB: copy, PHONE_EMAIL: email, PHONE_PW: password };
  // The owner sees every page, so one account reaches all of them. Made in the
  // copy only; the password is passed through the environment, never argv.
  const py = `
import os
from api import db, security
db.init()
email = os.environ['PHONE_EMAIL']; folded = db.fold(email)
h = security.hash_password(os.environ['PHONE_PW'])
row = db.one("SELECT id FROM account WHERE email_folded = ?", (folded,))
if row:
    db.write("UPDATE account SET password_hash = ?, role = 'owner', active = 1 WHERE id = ?", (h, row['id']))
    aid = row['id']
else:
    db.write("INSERT INTO account (email, email_folded, name, password_hash, role, created_at) VALUES (?, ?, ?, ?, 'owner', ?)",
             (email, folded, 'Phone Shots', h, security.stamp()))
    aid = db.one("SELECT id FROM account WHERE email_folded = ?", (folded,))['id']
for p in db.all_rows("SELECT id FROM project"):
    db.write("INSERT OR IGNORE INTO account_project (account_id, project_id, role, created_at) VALUES (?, ?, 'owner', ?)", (aid, p['id'], security.stamp()))
`;
  const made = spawnSync('python', ['-c', py], { cwd: VIEWER_DIR, env, encoding: 'utf8' });
  if (made.status !== 0) throw new Error(`Could not make the account in the copy:\n${made.stderr}`);

  const apiPort = await freePort();
  const viewerPort = await freePort();
  const api = spawn('python', ['-m', 'uvicorn', 'api.main:app', '--port', String(apiPort), '--log-level', 'warning'],
    { cwd: VIEWER_DIR, env: { ...env, PHONE_PW: '' }, stdio: ['ignore', 'ignore', 'pipe'] });
  children.push(api);
  const viewer = spawn(process.execPath, ['server.mjs', '--port', String(viewerPort)],
    { cwd: VIEWER_DIR, env: { ...process.env, TICVAI_AUTH: `http://127.0.0.1:${apiPort}` }, stdio: ['ignore', 'ignore', 'pipe'] });
  children.push(viewer);
  const base = `http://localhost:${viewerPort}`;
  await waitFor(`http://127.0.0.1:${apiPort}/api/health`);
  await waitFor(`${base}/login.html`);
  return { base, email, password };
}

/** What a reviewer of a phone layout wants counted: sideways scroll, and controls under the touch floor. */
const audit = () => {
  // The visual viewport is the screen. A layout viewport wider than it (an
  // overflowing element on a mobile browser) draws every fixed bar and sheet
  // at that width, so it counts as sideways scroll even when nothing scrolls.
  const vw = Math.round(visualViewport?.width ?? innerWidth);
  const sideways = Math.max(document.scrollingElement.scrollWidth, innerWidth) - vw;
  const small = [];
  for (const el of document.querySelectorAll('a[href], button, select, input:not([type=hidden]), textarea, summary, [role=button], [role=tab]')) {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) continue;
    if (el.closest('[hidden], [inert]')) continue;
    // Inline links inside running text are exempt from the target size rule (WCAG 2.5.8).
    if (el.tagName === 'A' && cs.display === 'inline' && el.closest('p, li, td, dd')) continue;
    if (r.height < 44 || r.width < 44) {
      small.push(`${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${el.className && typeof el.className === 'string' ? `.${el.className.trim().split(/\s+/)[0]}` : ''} ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
  }
  // Wider than the screen but clipped by the page (`overflow-x: hidden` on the
  // body): no sideways scroll is reported, and the content is simply cut off.
  // Counted unless an ancestor scrolls sideways on purpose.
  const cut = [];
  for (const el of document.body.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (!r.width || r.right <= vw + 1) continue;
    let p = el.parentElement; let scrolls = false;
    while (p && p !== document.body) {
      const o = getComputedStyle(p).overflowX;
      if ((o === 'auto' || o === 'scroll') && p.scrollWidth > p.clientWidth) { scrolls = true; break; }
      if (o === 'hidden' || o === 'clip') { const pr = p.getBoundingClientRect(); if (pr.right <= vw + 1) { scrolls = true; break; } }
      p = p.parentElement;
    }
    if (scrolls || el.closest('[hidden], .sh-sr, .phone-menu-backdrop')) continue;
    if (getComputedStyle(el).position === 'fixed') continue;
    cut.push(`${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${typeof el.className === 'string' && el.className.trim() ? `.${el.className.trim().split(/\s+/)[0]}` : ''} ${Math.round(r.right)}`);
  }
  return { sideways, small: small.length, examples: [...new Set(small)].slice(0, 6), cut: cut.slice(0, 4), cutCount: cut.length };
};

async function main() {
  let base; let email; let password;
  if (process.env.PHONE_VIEWER) {
    base = process.env.PHONE_VIEWER.replace(/\/+$/, '');
    email = process.env.PHONE_EMAIL; password = process.env.PHONE_PASSWORD;
    if (!email || !password) throw new Error('PHONE_VIEWER needs PHONE_EMAIL and PHONE_PASSWORD.');
  } else {
    ({ base, email, password } = await startServers());
  }

  if (opt('walk')) {
    const walk = spawnSync(process.execPath, [path.join(here, 'phone-walk.mjs'), opt('walk'), ...(argv.includes('--pages') ? [pages.join(',')] : [])], {
      cwd: VIEWER_DIR, stdio: 'inherit',
      env: { ...process.env, PHONE_VIEWER: base, PHONE_EMAIL: email, PHONE_PASSWORD: password },
    });
    return walk.status;
  }

  const browser = await chromium.launch({ executablePath: CHROME, headless: true });
  const report = [];
  try {
    const shots = [];
    for (const theme of themes) {
      for (const [w, h] of sizes) shots.push({ theme, w, h, phone: true });
      if (flag('desktop')) shots.push({ theme, w: 1440, h: 900, phone: false });
    }

    for (const shot of shots) {
      const context = await browser.newContext({
        viewport: { width: shot.w, height: shot.h },
        deviceScaleFactor: shot.phone ? 2 : 1,
        isMobile: shot.phone,
        hasTouch: shot.phone,
        reducedMotion: 'reduce',
      });
      await context.addInitScript(({ theme }) => {
        localStorage.setItem('ticvai-api', '');            // this origin; server.mjs forwards to the accounts service
        localStorage.setItem('ticvai-theme', theme);
      }, { theme: shot.theme });
      const page = await context.newPage();
      // A layout change that throws leaves a page with a header and nothing
      // under it, which a screenshot can mistake for an empty state: say so.
      let errors = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push(m.text()); });
      await page.goto(`${base}/login.html`, { waitUntil: 'domcontentloaded' });
      const signed = await page.evaluate(async ({ email, password }) => {
        const r = await fetch('/api/auth/login', {
          method: 'POST', credentials: 'include',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });
        return r.status;
      }, { email, password });
      if (signed !== 200) throw new Error(`Sign-in answered ${signed}`);
      // A stable bar: the release notes count as read, so no "What's new" chip in the shots.
      await page.evaluate(async () => {
        const r = await fetch('/updates/stamp').then((a) => (a.ok ? a.json() : {})).catch(() => ({}));
        if (r.stamp) localStorage.setItem('adam-updates-seen', r.stamp);
      });

      for (const name of pages) {
        // "admin#people" shoots one section of a page; its folder is admin-people.
        const [bare, hash] = name.split('#');
        const file = bare === 'chrome' ? 'board' : bare;
        const dir = path.join(OUT, hash ? `${bare}-${hash}` : bare, label);
        mkdirSync(dir, { recursive: true });
        const tag = `${shot.w}x${shot.h}-${shot.theme}`;
        await page.goto(`${base}/${file}.html${hash ? `#${hash}` : ''}`, { waitUntil: 'domcontentloaded' });
        await page.waitForLoadState('networkidle', { timeout: 20_000 }).catch(() => {});
        await page.waitForTimeout(900);
        await page.screenshot({ path: path.join(dir, `${tag}.png`) });
        report.push({ page: name, shot: tag, ...(await page.evaluate(audit)), errors });
        errors = [];
        if (flag('full') && name !== 'chrome') {
          // The standalone pages scroll their body, not the document, so a
          // full-page shot would stop at the first screen; let the document
          // carry the length for this one shot.
          const unlock = await page.addStyleTag({ content: 'html, body { height: auto !important; overflow: visible !important; }' });
          await page.screenshot({ path: path.join(dir, `${tag}-full.png`), fullPage: true });
          await unlock.evaluate((n) => n.remove());
        }

        // The page's filter, opened, where it folds behind a button (a phone).
        const filter = page.locator('.sh-scope-toggle:visible').first();
        if (shot.phone && name !== 'chrome' && await filter.count()) {
          await filter.click().catch(() => {});
          await page.waitForTimeout(450);
          await page.screenshot({ path: path.join(dir, `${tag}-filter.png`) });
          report.push({ page: `${name}:filter`, shot: tag, ...(await page.evaluate(audit)) });
          await page.keyboard.press('Escape').catch(() => {});
        }

        if (flag('sections') && name !== 'chrome') {
          const ids = await page.evaluate(() => [...document.querySelectorAll('.set-nav a[href^="#"]')]
            .filter((a) => !a.hidden && a.getClientRects().length).map((a) => a.getAttribute('href').slice(1)));
          mkdirSync(path.join(dir, 'sections'), { recursive: true });
          for (const id of ids) {
            await page.evaluate((want) => { location.hash = want; }, id);
            await page.waitForLoadState('networkidle', { timeout: 15_000 }).catch(() => {});
            await page.waitForTimeout(600);
            const unlock = await page.addStyleTag({ content: 'html, body { height: auto !important; overflow: visible !important; }' });
            await page.screenshot({ path: path.join(dir, 'sections', `${tag}-${id}.png`), fullPage: true });
            await unlock.evaluate((n) => n.remove());
            report.push({ page: `${name}#${id}`, shot: tag, ...(await page.evaluate(audit)) });
          }
        }

        if (name === 'chrome') {
          // The frame's own states, each from a fresh load so one does not sit under another.
          const states = [
            ['menu', '#phone-more'],
            ['account', '#account-toggle'],
            ['bell', '#bell-toggle'],
          ];
          for (const [state, selector] of states) {
            await page.goto(`${base}/board.html`, { waitUntil: 'domcontentloaded' });
            await page.waitForLoadState('networkidle', { timeout: 20_000 }).catch(() => {});
            await page.waitForTimeout(500);
            const target = page.locator(`${selector}:visible`).first();
            if (!(await target.count())) continue;
            await target.click().catch(() => {});
            await page.waitForTimeout(500);
            await page.screenshot({ path: path.join(dir, `${tag}-${state}.png`) });
            report.push({ page: `chrome:${state}`, shot: tag, ...(await page.evaluate(audit)) });
          }
        }
      }
      await context.close();
    }
  } finally {
    await browser.close();
  }

  for (const r of report) {
    const side = r.sideways > 0 ? `scrolls sideways by ${r.sideways}px` : 'no sideways scroll';
    console.log(`${r.page.padEnd(16)} ${r.shot.padEnd(18)} ${side}; ${r.small} controls under 44px${r.small ? `  e.g. ${r.examples.join(', ')}` : ''}`);
    if (r.errors?.length) console.log(`${''.padEnd(16)} ${''.padEnd(18)} console errors: ${r.errors.slice(0, 3).join(' | ')}`);
    if (r.cutCount) console.log(`${''.padEnd(16)} ${''.padEnd(18)} ${r.cutCount} elements cut off at the right edge, e.g. ${r.cut.join(', ')}`);
  }
  console.log(`\nShots in ${OUT}\\<page>\\${label}`);
}

main().then(() => { stopAll(); process.exit(0); }, (error) => { console.error(error.message); stopAll(); process.exit(1); });
