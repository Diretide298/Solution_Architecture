// The decide page's own behaviour that no API check can see (public/decide.js), on the in-page demo with the
// fake app (`?demo=1&app=1`), so it needs no account and no watcher:
//
//   - a notification opens /decide#CR-650: the hash opens that request, as the page's own ?cr= view, on load and
//     on hashchange, and a hash that is not a waiting request opens nothing;
//   - turning notifications on mints a device token and hands it to the app; when the app refuses it
//     (setWatch fails) the token is revoked at once rather than left live with nobody holding it;
//   - a request with no draft (6 November 2026: every turn failed on an invalid API key) is never decided: no
//     swipe, no approve, not in "Approve all that need nobody", not counted in the headline; it opens to why, with
//     Draft again;
//   - the inbox's filters, search and developer; History; Health; the all-failed headline (`&scenario=failed`).
//
// Starts its own viewer (server.mjs, the gate off, port 8895) and a headless Chrome (CHROME, default the
// workstation's).
//
//   node checks/decide-check.mjs            # from viewer/

import { spawn, spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const VIEWER = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORT = 8895;
const BASE = `http://127.0.0.1:${PORT}`;
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const server = spawn(process.execPath, ['server.mjs', '--port', String(PORT), '--host', '127.0.0.1'],
  { cwd: VIEWER, env: { ...process.env, TICVAI_NO_GATE: '1' }, windowsHide: true });
let log = '';
server.stdout.on('data', (c) => { log += c; });
server.stderr.on('data', (c) => { log += c; });
const stop = () => {
  if (server.exitCode !== null) return;
  if (process.platform === 'win32') spawnSync('taskkill', ['/pid', String(server.pid), '/T', '/F'], { windowsHide: true });
  else server.kill();
};

let browser;
try {
  let up = false;
  for (let i = 0; i < 480 && !up; i++) {
    try { up = (await fetch(`${BASE}/decide.html`)).status === 200; } catch { /* not yet */ }
    if (!up) await new Promise((r) => setTimeout(r, 250));
  }
  if (!up) throw new Error(`the viewer did not start:\n${log.slice(-2000)}`);
  browser = await chromium.launch({ executablePath: process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await (await browser.newContext({ viewport: { width: 420, height: 900 } })).newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  const state = () => page.evaluate(() => ({
    cr: new URL(location.href).searchParams.get('cr') ?? '', hash: location.hash,
    open: !document.getElementById('dc-request').hidden,
    title: document.getElementById('dc-request').textContent.slice(0, 4000),
  }));
  const settle = async (want) => {
    for (let i = 0; i < 60; i++) {
      const s = await state();
      if (want(s)) return s;
      await page.waitForTimeout(100);
    }
    return state();
  };

  // ── #CR-n from a notification ──────────────────────────────────
  await page.goto(`${BASE}/decide?demo=1&app=1#CR-602`, { waitUntil: 'domcontentloaded' });
  let s = await settle((x) => x.open && x.cr === 'CR-602');
  check('a #CR-n link opens that request on load', s.open && s.cr === 'CR-602' && s.title.includes('CR-602'), JSON.stringify({ ...s, title: '' }));
  check('as the page\'s own ?cr= view, the hash gone', s.hash === '', s.hash);
  await page.evaluate(() => { location.hash = '#cr-598'; });
  s = await settle((x) => x.cr === 'CR-598');
  check('a hashchange opens the request it names (any case)', s.open && s.cr === 'CR-598' && s.title.includes('CR-598'), JSON.stringify({ ...s, title: '' }));
  await page.goto(`${BASE}/decide?demo=1&app=1#CR-999999`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2500);
  s = await state();
  check('a #CR-n that is not a waiting request opens nothing', !s.open && s.cr === '', JSON.stringify({ ...s, title: '' }));
  await page.evaluate(() => { location.hash = '#not-a-request'; });
  await page.waitForTimeout(500);
  s = await state();
  check('nor does a hash that is not a request number', !s.open && s.cr === '', JSON.stringify({ ...s, title: '' }));

  // ── a token the app does not take is revoked ───────────────────
  await page.goto(`${BASE}/decide?demo=1&app=1`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.AdamApp && window.__decideDemoCalls);
  await page.evaluate(() => {
    window.__setWatchSaw = [];
    window.AdamApp.setWatch = async (w) => { window.__setWatchSaw.push(w); if (w.token) throw new Error('The app could not keep the token.'); };
  });
  await page.click('[data-go="health"]');
  await page.waitForSelector('.dc-switch');
  await page.click('.dc-switch');
  await page.waitForFunction(() => window.__decideDemoCalls.some(([k]) => k === 'drop'), null, { timeout: 5000 }).catch(() => {});
  const calls = await page.evaluate(() => window.__decideDemoCalls);
  const saw = await page.evaluate(() => window.__setWatchSaw.map((w) => ({ base: w.base, token: Boolean(w.token) })));
  check('when the app refuses the token, the token is revoked (DELETE device-token/{id})',
    JSON.stringify(calls) === JSON.stringify([['token', 1], ['drop', '1']]), JSON.stringify(calls));
  check('the app was handed ADAM\'s API origin as the base', saw.length === 1 && typeof saw[0].base === 'string', JSON.stringify(saw));
  const toast = await page.evaluate(() => document.body.textContent.includes('Notifications did not change.'));
  check('and the lead is told notifications did not change', toast);
  await page.evaluate(() => { window.AdamApp.setWatch = async () => {}; window.__decideDemoCalls.length = 0; });
  await page.click('.dc-switch');
  await page.waitForTimeout(800);
  check('when the app takes it, it is kept', JSON.stringify(await page.evaluate(() => window.__decideDemoCalls)) === JSON.stringify([['token', 1]]),
    JSON.stringify(await page.evaluate(() => window.__decideDemoCalls)));

  // ── a request with no draft is never decided here (6 November 2026) ─
  await page.goto(`${BASE}/decide?demo=1`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('.dc-group-undrafted .dc-row');
  const shape = await page.evaluate(() => {
    const und = [...document.querySelectorAll('.dc-group-undrafted .dc-row')];
    return {
      crs: und.map((li) => li.dataset.cr),
      approveInside: und.some((li) => li.querySelector('[data-approve], .dc-row-under')),
      noswipe: und.every((li) => li.hasAttribute('data-noswipe')),
      inOtherGroups: [...document.querySelectorAll('.dc-group:not(.dc-group-undrafted) .dc-row')].some((li) => und.some((u) => u.dataset.cr === li.dataset.cr)),
      head: document.getElementById('dc-headline').textContent,
      decided: document.getElementById('dc-count-tray').textContent,
    };
  });
  check('requests with no draft sit under "Not drafted yet", with no approve and no swipe',
    shape.crs.join(',') === 'CR-652,CR-651,CR-653,CR-654' && !shape.approveInside && shape.noswipe && !shape.inOtherGroups, JSON.stringify(shape));
  check('and the headline counts only the drafted ones', shape.head === '9 blocking of 17', shape.head);
  const row = await page.$('.dc-group-undrafted .dc-row[data-cr="CR-651"] .dc-row-face');
  const box = await row.boundingBox();
  await page.mouse.move(box.x + 40, box.y + 30);
  await page.mouse.down();
  for (let x = 40; x <= 360; x += 40) await page.mouse.move(box.x + x, box.y + 32);
  await page.mouse.up();
  await page.waitForTimeout(700);
  const afterSwipe = await page.evaluate(() => ({
    still: Boolean(document.querySelector('.dc-group-undrafted .dc-row[data-cr="CR-651"]')),
    decided: document.getElementById('dc-count-tray').textContent,
  }));
  check('a swipe right on one decides nothing', afterSwipe.still && afterSwipe.decided === shape.decided, JSON.stringify(afterSwipe));
  // With no swipe, the press may land as a tap and open the request: back to the list either way.
  if (await page.evaluate(() => !document.getElementById('dc-request').hidden)) {
    await page.click('#dc-req-back');
    await page.waitForFunction(() => document.getElementById('dc-request').hidden);
  }
  const nobody = await page.evaluate(() => document.querySelector('.dc-inline-action .dc-btn')?.textContent ?? '');
  await page.click('.dc-inline-action .dc-btn');
  await page.waitForSelector('.dc-pick');
  const picked = await page.evaluate(() => [...document.querySelectorAll('.dc-pick-sub')].map((x) => x.textContent.split(',')[0]));
  check('"Approve all that need nobody" never lists one', picked.length > 1 && !picked.some((c) => ['CR-651', 'CR-652', 'CR-653', 'CR-654'].includes(c)),
    `${nobody}: ${picked.join(',')}`);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(400);
  await page.evaluate(() => { window.__decideDemoCalls.length = 0; });
  await page.click('.dc-group-undrafted .dc-row[data-cr="CR-651"] [data-redraft]');
  await page.waitForFunction(() => window.__decideDemoCalls.some(([k]) => k === 'redraft'), null, { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(500);
  const redrafted = await page.evaluate(() => ({
    calls: window.__decideDemoCalls,
    why: document.querySelector('.dc-row[data-cr="CR-651"] .dc-row-why')?.textContent ?? '',
    button: Boolean(document.querySelector('.dc-row[data-cr="CR-651"] [data-redraft]')),
  }));
  check('Draft again asks the API to draft it again, and the row then waits for the next run',
    JSON.stringify(redrafted.calls) === JSON.stringify([['redraft', 'CR-651']]) && /next hourly run/.test(redrafted.why) && !redrafted.button,
    JSON.stringify(redrafted));
  await page.click('.dc-row[data-cr="CR-652"] .dc-row-open');
  await page.waitForFunction(() => document.querySelector('.dc-nodraft'));
  const opened = await page.evaluate(() => ({
    acts: [...document.querySelectorAll('#dc-actions button')].map((b) => b.textContent.trim()),
    asked: document.getElementById('dc-req-body').textContent.includes('What Pranay asked'),
    link: document.querySelector('.dc-ticket')?.href ?? '',
  }));
  check('one opens to why it has no draft, the developer\'s words, the ticket link, and only Draft again',
    JSON.stringify(opened.acts) === JSON.stringify(['Draft again']) && opened.asked
    && opened.link === 'https://pms.softlabsgroup.in/work_packages/30851', JSON.stringify(opened));
  await page.keyboard.press('a');
  await page.waitForTimeout(400);
  check('and a on the keyboard approves nothing', await page.evaluate(() => document.getElementById('dc-count-tray').textContent) === shape.decided);

  // ── filters, search, developer ─────────────────────────────────
  await page.goto(`${BASE}/decide?demo=1`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-filter="undrafted"]');
  const counts = await page.evaluate(() => Object.fromEntries([...document.querySelectorAll('.dc-filter')].map((b) => [b.dataset.filter, b.querySelector('.dc-filter-n').textContent])));
  check('each filter shows its count', JSON.stringify(counts) === JSON.stringify({ all: '21', blocking: '11', lead: '6', client: '2', undrafted: '4' }), JSON.stringify(counts));
  await page.click('[data-filter="undrafted"]');
  const onlyU = await page.evaluate(() => ({ groups: [...document.querySelectorAll('#dc-groups .dc-group-title')].map((x) => x.textContent), n: document.querySelectorAll('#dc-groups .dc-row').length }));
  check('"Not drafted" shows only those', JSON.stringify(onlyU) === JSON.stringify({ groups: ['Not drafted yet'], n: 4 }), JSON.stringify(onlyU));
  await page.click('[data-filter="all"]');
  await page.fill('#dc-search', '30874');
  const byTicket = await page.evaluate(() => [...document.querySelectorAll('#dc-groups .dc-row')].map((li) => li.dataset.cr));
  await page.fill('#dc-search', '610');
  const byNumber = await page.evaluate(() => [...document.querySelectorAll('#dc-groups .dc-row')].map((li) => li.dataset.cr));
  await page.fill('#dc-search', 'wishlist');
  const byTitle = await page.evaluate(() => [...document.querySelectorAll('#dc-groups .dc-row')].map((li) => li.dataset.cr));
  check('search finds by ticket, number and title', byTicket.join() === 'CR-602' && byNumber.join() === 'CR-610' && byTitle.join() === 'CR-634',
    JSON.stringify({ byTicket, byNumber, byTitle }));
  await page.fill('#dc-search', '');
  await page.selectOption('#dc-dev', 'Narayan Gaonkar');
  const byDev = await page.evaluate(() => [...document.querySelectorAll('#dc-groups .dc-row')].map((li) => li.dataset.cr).sort());
  check('the developer filter shows only theirs', byDev.join() === 'CR-598,CR-599,CR-600,CR-612,CR-651', byDev.join());

  // ── History and Health ─────────────────────────────────────────
  await page.goto(`${BASE}/decide?demo=1`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-go="history"]');
  await page.click('[data-go="history"]');
  await page.waitForSelector('.dc-hist');
  const hist = await page.evaluate(() => ({
    first: document.querySelector('.dc-hist .dc-row-cr')?.textContent,
    labels: [...document.querySelectorAll('.dc-hist .dc-mark-label')].map((x) => x.textContent),
    told: document.querySelector('.dc-hist .dc-ticket')?.href ?? '',
  }));
  check('History lists what was settled, newest first, with its decision and the ticket it told', hist.first === 'CR-597'
    && hist.labels.join() === 'Approved,Changed,Approved,Approved,Approved,Settle failed'
    && hist.told === 'https://pms.softlabsgroup.in/work_packages/31533', JSON.stringify(hist));
  await page.click('[data-go="health"]');
  await page.waitForSelector('.dc-runs li');
  const health = await page.evaluate(() => ({
    runs: document.querySelectorAll('.dc-runs li').length, text: document.getElementById('dc-health').textContent,
  }));
  check('Health shows the last runs, the next run, why drafting is held and today\'s spend', health.runs === 4
    && /Next run/.test(health.text) && /Why drafting is held/.test(health.text) && /\$12\.40 of \$50\.00/.test(health.text),
  JSON.stringify({ runs: health.runs }));
  await page.goto(`${BASE}/decide?demo=1&scenario=failed`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('.dc-group-undrafted');
  const failedHead = await page.evaluate(() => ({ head: document.getElementById('dc-headline').textContent,
    line: document.getElementById('dc-lede-line').textContent, approveAll: Boolean(document.querySelector('[data-approve]')) }));
  check('with no draft at all, the headline says none is drafted and why, and nothing offers approve',
    failedHead.head === '21 new, none drafted yet' && /^Drafting failed: Invalid API key\./.test(failedHead.line) && !failedHead.approveAll,
    JSON.stringify(failedHead));

  // ── no watcher on this server (6 November 2026: the lead stopped it) ─
  const plainState = async () => page.evaluate(() => ({
    banner: document.getElementById('dc-banner').hidden ? '' : document.getElementById('dc-banner').textContent,
    inbox: document.getElementById('dc-groups').textContent,
    errorBlock: Boolean(document.querySelector('.dc-empty.is-error')),
  }));
  await page.goto(`${BASE}/decide?demo=1&scenario=unset`, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => document.getElementById('dc-groups').textContent.includes('not running'));
  const unsetInbox = await plainState();
  await page.click('[data-go="health"]');
  await page.waitForTimeout(400);
  const unsetHealth = await page.evaluate(() => document.getElementById('dc-health').textContent);
  await page.click('[data-go="history"]');
  await page.waitForSelector('.dc-hist');
  check('with no watcher at all (503), the inbox and Health say plainly it is not running, with no error, and History still reads',
    /The watcher is not running on this server/.test(unsetInbox.inbox) && !unsetInbox.errorBlock && !/Drafting|failed|held/i.test(unsetInbox.banner)
    && /Not running here/.test(unsetHealth) && !/Next run|Why drafting|The last error/.test(unsetHealth),
    JSON.stringify({ ...unsetInbox, inbox: unsetInbox.inbox.slice(0, 80), health: unsetHealth.slice(0, 120) }));
  await page.goto(`${BASE}/decide?demo=1&scenario=stopped`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('.dc-group-undrafted .dc-row');
  await page.waitForTimeout(400);
  const stopped = await page.evaluate(() => ({
    banner: document.getElementById('dc-banner').hidden ? '' : document.getElementById('dc-banner').textContent,
    buttons: [...document.querySelectorAll('[data-redraft], [data-redraft-all]')].map((b) => b.disabled),
    off: document.querySelector('.dc-row-off')?.textContent ?? '',
    line: document.getElementById('dc-lede-line').textContent,
  }));
  check('with its folder kept and its job gone, no pause banner, and Draft again is off with the reason', !/Drafting|held|failed/i.test(stopped.banner)
    && stopped.buttons.length > 0 && stopped.buttons.every(Boolean) && stopped.off === 'The watcher is not running on this server.'
    && /not running on this server/.test(stopped.line), JSON.stringify(stopped));

  // ── only the System Architect is shown Decide (security.py DECIDERS) ─
  const asRole = async (role, size, at = '/home.html') => {
    const ctx = await browser.newContext({ viewport: size, isMobile: size.width < 600, hasTouch: size.width < 600 });
    // The pages ask ADAM's API (another origin) who is signed in: answered here, as that origin would, with CORS.
    await ctx.route('**/api/**', (route) => {
      const url = route.request().url();
      const headers = { 'access-control-allow-origin': BASE, 'access-control-allow-credentials': 'true',
        'access-control-allow-headers': 'content-type', 'access-control-allow-methods': 'GET, POST, PUT, DELETE' };
      if (route.request().method() === 'OPTIONS') return route.fulfill({ status: 204, headers });
      if (['/api/auth/me', '/api/auth/state'].includes(new URL(url).pathname)) {
        return route.fulfill({ headers, json: { signedIn: true, account: { id: 1, email: `${role}@softlabsgroup.com`, name: `Harness ${role}`, role }, projects: [] } });
      }
      return route.fulfill({ status: 404, headers, json: { detail: 'Not in this check.' } });
    });
    const p = await ctx.newPage();
    await p.goto(`${BASE}${at}`, { waitUntil: 'domcontentloaded' });
    await p.waitForFunction(() => document.querySelector('#decide-link') && document.querySelector('#whoami, .account-btn, body'), null, { timeout: 15000 }).catch(() => {});
    await p.waitForTimeout(1800);
    // The menu's links are drawn when the account menu opens.
    await p.evaluate(async () => { (await import('/account-drawer.js')).openAccountPanel(); }).catch(() => {});
    await p.waitForTimeout(300);
    const seen = await p.evaluate(() => {
      const where = location.pathname;
      const shown = (el) => Boolean(el) && !el.hidden && !el.closest('[hidden]') && el.getClientRects().length > 0;
      return {
        chip: shown(document.getElementById('decide-chip')),
        link: Boolean(document.getElementById('decide-link')) && !document.getElementById('decide-link').hidden,
        tab: shown(document.querySelector('.phone-tabbar [data-tab="decide"]')),
        changesTab: shown(document.querySelector('.phone-tabbar [data-tab="changes"]')),
        home: Boolean(document.querySelector('#home-pages-list a[href="/decide"]')),
        where,
      };
    });
    await ctx.close();
    return seen;
  };
  // The chip and the menu link are the shared top bar's (a page like Reviews); the Go-to entry and the tab, home's on a phone.
  const leadDesk = await asRole('lead', { width: 1440, height: 900 }, '/reviews.html');
  const leadPhone = await asRole('lead', { width: 420, height: 933 });
  const adminDesk = await asRole('admin', { width: 1440, height: 900 }, '/reviews.html');
  const ownerDesk = await asRole('owner', { width: 1440, height: 900 }, '/reviews.html');
  const ownerPhone = await asRole('owner', { width: 420, height: 933 });
  check('a Team Lead sees no Decide chip, menu link, Go-to entry or phone tab; Changes is in their bar',
    !leadDesk.chip && !leadDesk.link && !leadPhone.tab && leadPhone.changesTab && !leadPhone.home,
    JSON.stringify({ leadDesk, leadPhone }));
  check('nor does an admin', !adminDesk.chip && !adminDesk.link, JSON.stringify(adminDesk));
  check('the System Architect sees the chip, the link, the Go-to entry and the Decide tab',
    ownerDesk.chip && ownerDesk.link && ownerPhone.tab && !ownerPhone.changesTab && ownerPhone.home,
    JSON.stringify({ ownerDesk, ownerPhone }));
  check('no script error on the page', errors.length === 0, errors.join(' | ').slice(0, 300));
} catch (e) {
  check('the check ran to the end', false, e.stack);
} finally {
  await browser?.close();
  stop();
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
