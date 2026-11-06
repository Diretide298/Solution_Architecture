// The decide page's own behaviour that no API check can see (public/decide.js), on the in-page demo with the
// fake app (`?demo=1&app=1`), so it needs no account and no watcher:
//
//   - a notification opens /decide#CR-650: the hash opens that request, as the page's own ?cr= view, on load and
//     on hashchange, and a hash that is not a waiting request opens nothing;
//   - turning notifications on mints a device token and hands it to the app; when the app refuses it
//     (setWatch fails) the token is revoked at once rather than left live with nobody holding it.
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
  check('no script error on the page', errors.length === 0, errors.join(' | ').slice(0, 300));
} catch (e) {
  check('the check ran to the end', false, e.stack);
} finally {
  await browser?.close();
  stop();
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
