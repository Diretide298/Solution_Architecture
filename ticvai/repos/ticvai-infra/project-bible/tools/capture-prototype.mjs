#!/usr/bin/env node
/*
 * capture-prototype.mjs: capture screens of a client prototype as board frames.
 *
 * A client prototype (a self-contained .dc.html app) is served on 127.0.0.1, opened in a headless
 * browser, and walked to each screen's view by the steps in a capture plan. The tool then checks
 * that the view shows the texts that prove it is the right view, and writes, per screen:
 *
 *   <out>/<id>.html       the frame fragment (<section id="<id>">, an <img>, a caption), ready for
 *                         tools/import-design-frames.py
 *   <out>/img/<id>.png    the capture (a .jpg when the PNG is over the plan's maxBytes)
 *   <out>/manifest.json   what was captured from which view, with the proof texts, and what was not
 *
 * A screen whose proof text is missing is not captured, and the tool exits 1 once every other
 * screen is done: a frame of the wrong view counted as client-verified is worse than no frame.
 *
 *   node tools/capture-prototype.mjs <plan.json> <out-dir> [--only GST-001,GST-002] [--headed]
 *
 * Plan paths (prototype, assetRoots) are relative to the package root (the folder above tools/).
 * Plan format: see tools/capture-plans/guest-mobile-v4.json. Each step is one of
 *   {"click": "Text"}            exact visible text inside the device frame ("nth" picks a match)
 *   {"clickContains": "Text"}    visible text containing this, inside the frame
 *   {"clickPage": "Text"}        exact visible text anywhere on the page (the prototype's config panel)
 *   {"clickSelector": "css"}     a visible element inside the frame
 *   {"fill": "placeholder", "text": "..."}  type into the frame's input with that placeholder
 *   {"type": "..."}  {"press": "Enter"}  {"wait": ms}  {"scroll": px}  {"hash": "#view"}
 * "scroll" sets every scrollable element in the frame to that offset.
 *
 * Playwright: set PLAYWRIGHT_MODULE to its index.mjs (or package folder), or install it where
 * Node can find it:  npm install playwright && npx playwright install chromium
 * The browser is Playwright's Chromium, falling back to the installed Edge or Chrome; set
 * PLAYWRIGHT_CHANNEL (msedge, chrome) to choose one.
 */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const TOOLS = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(TOOLS, '..');

function die(msg) { console.error(msg); process.exit(2); }

async function loadPlaywright() {
  const env = process.env.PLAYWRIGHT_MODULE;
  const tries = [];
  if (env) {
    let p = env;
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.mjs');
    tries.push(pathToFileURL(path.resolve(p)).href);
  }
  for (const base of [process.cwd(), ROOT, TOOLS]) {
    try { tries.push(pathToFileURL(createRequire(path.join(base, 'noop.js')).resolve('playwright')).href); } catch { /* not here */ }
  }
  for (const t of tries) {
    try { return await import(t); } catch { /* next */ }
  }
  die('Playwright not found. Either set PLAYWRIGHT_MODULE to its index.mjs, e.g.\n' +
      '  PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.mjs\n' +
      'or install it next to the package:\n' +
      '  npm install playwright && npx playwright install chromium' +
      (env ? `\n(PLAYWRIGHT_MODULE=${env} could not be loaded)` : ''));
}

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.gif': 'image/gif', '.svg': 'image/svg+xml', '.json': 'application/json', '.mp4': 'video/mp4',
  '.webm': 'video/webm', '.glb': 'model/gltf-binary', '.woff2': 'font/woff2', '.woff': 'font/woff' };

/** Serve the prototype's folder, then each asset root in turn for files the first does not have. */
function serve(roots) {
  return new Promise(resolve => {
    const srv = http.createServer((q, res) => {
      const rel = decodeURIComponent(q.url.split('?')[0].split('#')[0]);
      for (const r of roots) {
        const p = path.join(r, rel);
        if (!p.startsWith(r)) break;
        if (fs.existsSync(p) && fs.statSync(p).isFile()) {
          res.writeHead(200, { 'content-type': TYPES[path.extname(p).toLowerCase()] || 'application/octet-stream' });
          res.end(fs.readFileSync(p));
          return;
        }
      }
      res.writeHead(404); res.end();
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const q = s => JSON.stringify(String(s));

async function main() {
  const args = process.argv.slice(2);
  const pos = args.filter((a, i) => !a.startsWith('--') && args[i - 1] !== '--only');
  if (pos.length < 2) die('usage: node tools/capture-prototype.mjs <plan.json> <out-dir> [--only ID,ID] [--headed]');
  const oi = args.indexOf('--only');
  const only = oi > -1 ? new Set(args[oi + 1].split(',').map(s => s.trim().toUpperCase())) : null;
  const planFile = path.resolve(pos[0]);
  const out = path.resolve(pos[1]);
  const plan = JSON.parse(fs.readFileSync(planFile, 'utf-8'));
  const abs = p => path.isAbsolute(p) ? p : path.join(ROOT, p);

  const proto = abs(plan.prototype);
  if (!fs.existsSync(proto)) die(`prototype not found: ${proto}`);
  const roots = [path.dirname(proto), ...(plan.assetRoots || []).map(abs)];
  const fr = plan.frame || {};
  const vp = plan.viewport || { width: 1600, height: 1000 };
  const maxBytes = plan.maxBytes || 250000;
  const settle = plan.stepWait ?? 1200;

  const { chromium } = await loadPlaywright();
  let browser, lastErr;
  const channels = process.env.PLAYWRIGHT_CHANNEL ? [process.env.PLAYWRIGHT_CHANNEL] : [undefined, 'msedge', 'chrome'];
  for (const channel of channels) {
    try { browser = await chromium.launch({ channel, headless: !args.includes('--headed') }); break; } catch (e) { lastErr = e; }
  }
  if (!browser) die('could not start a browser: ' + String(lastErr && lastErr.message).split('\n')[0] +
                    '\ninstall one with: npx playwright install chromium');

  const srv = await serve(roots);
  const url = `http://127.0.0.1:${srv.address().port}/${encodeURIComponent(path.basename(proto))}`;
  fs.mkdirSync(path.join(out, 'img'), { recursive: true });
  const page = await browser.newPage({ viewport: vp, deviceScaleFactor: 1 });
  const captured = [], missing = [];

  const frameSel = '[data-capture-frame]';
  async function markFrame() {
    if (fr.selector) {
      await page.locator(fr.selector).first().evaluate(e => e.setAttribute('data-capture-frame', '1'));
      return;
    }
    // The device frame is the element the size of the device plus its border.
    const ok = await page.evaluate(({ w, h, inset }) => {
      const tw = w + 2 * inset, th = h + 2 * inset;
      const el = [...document.querySelectorAll('body *')].find(d => {
        const r = d.getBoundingClientRect(); return Math.abs(r.width - tw) < 3 && Math.abs(r.height - th) < 3;
      });
      if (el) el.setAttribute('data-capture-frame', '1');
      return !!el;
    }, { w: fr.width || 390, h: fr.height || 844, inset: fr.inset ?? 1 });
    if (!ok) throw new Error(`no ${fr.width || 390}x${fr.height || 844} device frame on the page`);
  }

  async function run(step) {
    const F = page.locator(frameSel);
    const nth = step.nth || 0;
    let target;
    if ('click' in step) target = F.locator(`text=${q(step.click)} >> visible=true`);
    else if ('clickContains' in step) target = F.locator(`text=${step.clickContains} >> visible=true`);
    else if ('clickPage' in step) target = page.locator(`text=${q(step.clickPage)} >> visible=true`);
    else if ('clickSelector' in step) target = F.locator(`${step.clickSelector} >> visible=true`);
    if (target) {
      const n = await target.count();
      if (n <= nth) throw new Error(`step ${JSON.stringify(step)}: ${n} visible match(es)`);
      await target.nth(nth).click({ timeout: 10000 });
    } else if ('fill' in step) {
      const i = F.locator(`input[placeholder=${q(step.fill)}] >> visible=true`).first();
      await i.click({ timeout: 10000 });
      await page.keyboard.type(step.text || '');
    } else if ('type' in step) await page.keyboard.type(step.type);
    else if ('press' in step) await page.keyboard.press(step.press);
    else if ('wait' in step) { await page.waitForTimeout(step.wait); return; }
    else if ('scroll' in step) {
      await F.evaluate((e, y) => e.querySelectorAll('*').forEach(x => {
        const o = getComputedStyle(x).overflowY;
        if ((o === 'auto' || o === 'scroll') && x.scrollHeight > x.clientHeight + 20) x.scrollTop = y;
      }), step.scroll);
    } else if ('hash' in step) await page.evaluate(h => { location.hash = h; }, step.hash);
    else throw new Error(`unknown step ${JSON.stringify(step)}`);
    await page.waitForTimeout(step.after ?? settle);
  }

  for (const s of plan.screens) {
    const id = s.id.toUpperCase(), low = id.toLowerCase();
    if (only && !only.has(id)) continue;
    try {
      await page.goto(url + (s.hash || ''), { waitUntil: 'load' });
      await page.waitForTimeout(plan.loadWait ?? 3000);
      await markFrame();
      for (const st of [...(s.noSetup ? [] : plan.setup || []), ...(s.steps || [])]) await run(st);
      await page.waitForTimeout(s.settle ?? 800);
      const text = (await page.locator(frameSel).innerText()).toLowerCase();
      const gone = (s.expect || []).filter(t => !text.includes(t.toLowerCase()));
      if (gone.length) throw new Error(`proof text not visible: ${gone.map(q).join(', ')}; the view shows: ` +
                                       text.slice(0, 160).replace(/\s+/g, ' '));
      const extra = (s.absent || []).filter(t => text.includes(t.toLowerCase()));
      if (extra.length) throw new Error(`text that should not be there is: ${extra.map(q).join(', ')}`);
      if (!(s.expect || []).length) throw new Error('the plan gives no proof text for this screen');

      const bb = await page.locator(frameSel).boundingBox();
      const inset = fr.selector ? 0 : (fr.inset ?? 1);
      const clip = { x: bb.x + inset, y: bb.y + inset, width: bb.width - 2 * inset, height: bb.height - 2 * inset };
      let buf = await page.screenshot({ clip, type: 'png' }), ext = 'png';
      for (let qq = 85; buf.length > maxBytes && qq >= 55; qq -= 10) {
        buf = await page.screenshot({ clip, type: 'jpeg', quality: qq }); ext = 'jpg';
      }
      for (const e of ['png', 'jpg']) fs.rmSync(path.join(out, 'img', `${low}.${e}`), { force: true });
      const file = `${low}.${ext}`;
      fs.writeFileSync(path.join(out, 'img', file), buf);
      const cap = plan.caption || 'Client prototype';
      const frag = `<section id="${low}" class="proto-frame"><img src="${plan.imgBase || 'frames/img/'}${file}" ` +
        `alt="${esc(`${id} ${s.name || ''}, ${cap}`.replace(/ ,/, ','))}" style="display:block;width:100%;height:auto">` +
        `<p style="font:12px sans-serif;color:#667">${esc(cap)} · ${esc(s.view)}</p></section>\n`;
      fs.writeFileSync(path.join(out, `${low}.html`), frag, 'utf-8');
      captured.push({ id, name: s.name || '', view: s.view, proof: s.expect, file: 'img/' + file, bytes: buf.length });
      console.log(`  captured  ${id}  ${s.view}`);
    } catch (e) {
      missing.push({ id, view: s.view, reason: String(e.message).split('\n')[0] });
      console.log(`  MISSING   ${id}  ${String(e.message).split('\n')[0]}`);
    }
  }
  await browser.close();
  srv.close();
  const manifest = { prototype: plan.prototype, plan: path.relative(ROOT, planFile).split(path.sep).join('/'),
                     captured, missing };
  fs.writeFileSync(path.join(out, 'manifest.json'), JSON.stringify(manifest, null, 1) + '\n', 'utf-8');
  console.log(`\n${captured.length} captured · ${missing.length} missing → ${out}`);
  process.exit(missing.length ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });
