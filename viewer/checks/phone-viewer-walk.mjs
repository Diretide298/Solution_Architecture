/**
 * Walk every view of the viewer (index.html, `/?layer=...&mode=...`) as the lead's phone sees it:
 * 420 x 933 CSS px, touch, Android edge to edge (a 54 px status bar and a 48 px button bar, reported
 * through env(safe-area-inset-*) by a CDP override). The layers and their modes are read from the
 * page's own core.js, so a new tab is walked without editing this file.
 *
 * For each view it prints one line:
 *   STUCK   a pane that holds more than it shows and does not move under a finger's swipe
 *   CLIP    a box that cuts its content off with no way to scroll to it
 *   WIDE    the document, or something visible, past the right edge with no scroller to reach it
 *   SMALL   tappable things under 44 px (count, then a few of them)
 *   TINY    visible text under 14 px (count)
 *   BARS    top chrome under the status bar, or fixed things under the button bar
 *   ERR     console errors and uncaught exceptions
 * and screenshots the viewport (never a forced-open full page) into <out>/<layer>--<mode>.png.
 *
 *   PHONE_VIEWER=http://localhost:8702 PHONE_EMAIL=... PHONE_PASSWORD=... \
 *     node checks/phone-viewer-walk.mjs <out dir> [--only layer:mode,...] [--desktop] [--drawers]
 *
 * --desktop  also a 1440 x 900 screenshot of each view into <out>/desktop/ (for before/after diffs)
 * --drawers  also open the tree and the links drawer on each layer's first view and check they scroll
 */
import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright-core';

const argv = process.argv.slice(2);
const out = argv[0];
const opt = (n) => { const i = argv.indexOf(`--${n}`); return i >= 0 ? argv[i + 1] : null; };
const only = opt('only')?.split(',');
const base = process.env.PHONE_VIEWER ?? 'http://localhost:8702';
const W = 420, H = 933, TOP = 54, BOTTOM = 48;
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe' });

async function signedIn(ctx) {
  const p = await ctx.newPage();
  await p.goto(`${base}/login.html`, { waitUntil: 'domcontentloaded' });
  const status = await p.evaluate(async ({ email, password }) => (await fetch('/api/auth/login', {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, password }),
  })).status, { email: process.env.PHONE_EMAIL, password: process.env.PHONE_PASSWORD });
  if (status !== 200) throw new Error(`sign-in answered ${status}`);
  await p.close();
}

const phone = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'dark' });
const THEME = process.env.PHONE_THEME === 'light' ? 'light' : 'dark';
await phone.addInitScript((t) => { localStorage.setItem('ticvai-api', ''); localStorage.setItem('ticvai-theme', t); sessionStorage.setItem('ticvai-session', '1'); }, THEME);
await signedIn(phone);
const page = await phone.newPage();
const cdp = await phone.newCDPSession(page);
let insets = true;
try { await cdp.send('Emulation.setSafeAreaInsetsOverride', { insets: { top: TOP, bottom: BOTTOM, left: 0, right: 0 } }); }
catch (e) { insets = false; console.log(`(no safe-area override in this Chrome: ${e.message.slice(0, 80)})`); }

const errors = [];
page.on('pageerror', (e) => errors.push(e.message.slice(0, 140)));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 140)); });

// The layers and modes, from the viewer's own vocabulary.
await page.goto(`${base}/?layer=contracts&mode=graph`, { waitUntil: 'domcontentloaded' });
const layers = await page.evaluate(async () => (await import('/core.js')).LAYERS.map((l) => ({ key: l.key, modes: l.modes.map(([m, label]) => [m, label]) })));
let views = layers.flatMap((l) => l.modes.map(([m, label]) => ({ layer: l.key, mode: m, label })));
if (only) views = views.filter((v) => only.includes(`${v.layer}:${v.mode}`) || only.includes(v.layer));

const settle = async () => {
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1400);
};

/** Everything measured in the page; no scrolling happens here. */
const measure = () => page.evaluate(({ TOP, BOTTOM }) => {
  const vw = innerWidth, vh = innerHeight;
  const shown = (el) => {
    if (!el.isConnected) return false;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) return false;
    if (el.closest('[inert], [aria-hidden="true"]')) return false;
    // Behind something else? Only the centre point is asked.
    const x = Math.min(vw - 1, Math.max(0, r.left + r.width / 2)), y = Math.min(vh - 1, Math.max(0, r.top + r.height / 2));
    if (r.bottom < 0 || r.top > vh || r.right < 0 || r.left > vw) return 'off';
    const hit = document.elementFromPoint(x, y);
    return !!hit && (hit === el || el.contains(hit) || hit.contains(el)) ? true : 'covered';
  };
  const name = (el) => {
    const t = (el.getAttribute('aria-label') || el.textContent || el.title || '').trim().replace(/\s+/g, ' ').slice(0, 24);
    return `${el.tagName.toLowerCase()}${el.id ? `#${el.id}` : ''}${el.classList.length ? `.${[...el.classList].slice(0, 2).join('.')}` : ''}${t ? `"${t}"` : ''}`;
  };
  const scroller = (el, axis) => {
    const cs = getComputedStyle(el);
    const o = axis === 'x' ? cs.overflowX : cs.overflowY;
    return o === 'auto' || o === 'scroll';
  };
  const view = document.querySelector('#main > .view:not([hidden])');
  const res = { view: view?.id ?? '(none)', small: [], tiny: 0, tinySample: [], wide: [], clip: [], panes: [], bars: [] };
  const d = document.documentElement;
  res.docWide = Math.max(d.scrollWidth, document.body.scrollWidth);

  // Tappable things in the chrome and the view.
  const roots = [document.querySelector('.chrome'), view, document.querySelector('.phone-tabbar')].filter(Boolean);
  const seen = new Set();
  for (const root of roots) {
    for (const el of root.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=tab], [role=option], [tabindex]:not([tabindex="-1"])')) {
      if (seen.has(el)) continue; seen.add(el);
      if (el.closest('svg') && el.tagName !== 'svg') continue;
      const s = shown(el);
      if (s !== true) continue;
      let r = el.getBoundingClientRect();
      // A checkbox is hit through its label.
      if (el.type === 'checkbox' || el.type === 'radio') { const l = el.closest('label'); if (l) r = l.getBoundingClientRect(); }
      // A link inside running text is exempt (WCAG 2.5.8's inline exception).
      if (el.tagName === 'A' && el.closest('p, li, td, .reader-body, .md') && (el.parentElement.textContent.trim().length > el.textContent.trim().length + 20)) continue;
      if (r.width < 43.5 || r.height < 43.5) res.small.push(`${name(el)} ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
  }

  // Text under 14 px, on screen.
  const walker = document.createTreeWalker(view ?? document.body, NodeFilter.SHOW_TEXT);
  const tinyEls = new Set();
  while (walker.nextNode()) {
    const n = walker.currentNode; if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el || tinyEls.has(el)) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize) * (el.currentCSSZoom ?? 1);
    if (fs < 13.95 && shown(el) === true) { tinyEls.add(el); if (res.tinySample.length < 4) res.tinySample.push(`${name(el)} ${fs}px`); }
  }
  for (const el of document.querySelectorAll('.chrome *')) {
    if (el.children.length || !el.textContent.trim()) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize) * (el.currentCSSZoom ?? 1);
    if (fs < 13.95 && shown(el) === true) { tinyEls.add(el); if (res.tinySample.length < 6) res.tinySample.push(`${name(el)} ${fs}px`); }
  }
  res.tiny = tinyEls.size;

  // The whole view, below the fold too: each class of text under 14 px and of
  // tappable thing under 44 px, once, for writing the rules that fix them.
  res.classes = { text: {}, tap: {} };
  const key = (el) => `${el.tagName.toLowerCase()}${el.classList.length ? `.${[...el.classList].join('.')}` : ''}${el.closest('svg') ? ' (svg)' : ''} < ${el.parentElement?.className?.baseVal ?? el.parentElement?.className ?? ''}`;
  if (view) {
    for (const el of view.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      const own = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
      if (own) {
        const fs = parseFloat(getComputedStyle(el).fontSize) * (el.currentCSSZoom ?? 1);
        if (fs < 13.95) { const k = `${key(el)} @${fs}`; res.classes.text[k] = (res.classes.text[k] ?? 0) + 1; }
      }
      if (el.matches('a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=tab], [tabindex]:not([tabindex="-1"])') && !el.closest('svg')) {
        if (r.width < 43.5 || r.height < 43.5) { const k = `${key(el)} ${Math.round(r.width)}x${Math.round(r.height)}`.replace(/ \d+x/, (m) => m); const kk = key(el); res.classes.tap[kk] = res.classes.tap[kk] ?? `${Math.round(r.width)}x${Math.round(r.height)}`; }
      }
    }
  }

  // Past the right edge with nothing to scroll it back: walk up to the first box that clips it.
  if (view) for (const el of [...view.querySelectorAll('*'), ...document.querySelectorAll('.chrome *')]) {
    if (el.children.length > 3) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4 || r.right <= vw + 2) continue;
    if (shown(el) === false) continue;
    let p = el.parentElement, reachable = false, clipped = false;
    while (p && p !== document.body) {
      if (scroller(p, 'x') && p.scrollWidth > p.clientWidth + 1) { reachable = true; break; }
      const cs = getComputedStyle(p);
      if ((cs.overflowX === 'hidden' || cs.overflowX === 'clip') && p.getBoundingClientRect().right <= vw + 2) { clipped = true; break; }
      p = p.parentElement;
    }
    if (el.closest('canvas, svg.diagram, .galaxy-field')) continue;
    if (!reachable && res.wide.length < 6) res.wide.push(`${name(el)} right=${Math.round(r.right)}${clipped ? ' (clipped)' : ''}`);
  }

  // Panes: every visible box that is meant to scroll vertically and has more than it shows.
  const all = [view, document.querySelector('#sidebar-left'), document.querySelector('#sidebar-right')].filter(Boolean);
  for (const root of all) {
    for (const el of [root, ...root.querySelectorAll('*')]) {
      if (el.clientHeight < 80) continue;
      const over = el.scrollHeight - el.clientHeight;
      if (over < 24) continue;
      if (shown(el) === false) continue;
      const cs = getComputedStyle(el);
      if (scroller(el, 'y')) {
        const r = el.getBoundingClientRect();
        // the part of it on screen, under the status bar and above the button bar
        const top = Math.max(r.top, TOP), bottom = Math.min(r.bottom, vh - BOTTOM);
        if (bottom - top < 40) continue;
        if (!el.dataset.walkId) el.dataset.walkId = String(Math.random()).slice(2, 9);
        res.panes.push({ id: el.dataset.walkId, name: name(el), x: Math.round(Math.min(Math.max(r.left + r.width / 2, 20), vw - 20)), y: Math.round((top + bottom) / 2), top: el.scrollTop, over });
      } else if ((cs.overflowY === 'hidden' || cs.overflowY === 'clip') && !el.querySelector(':scope > canvas, :scope > svg') && el.tagName !== 'CANVAS' && cs.position !== 'fixed') {
        // Clipped boxes whose overflow is real content (not a canvas or an empty absolute layer).
        const kids = [...el.children].filter((k) => shown(k) && k.getBoundingClientRect().bottom > el.getBoundingClientRect().bottom + 8 && !['CANVAS'].includes(k.tagName));
        if (!kids.length) continue;
        const inner = kids.find((k) => scroller(k, 'y'));
        if (inner) continue;
        if (res.clip.length < 5) res.clip.push(`${name(el)} shows ${el.clientHeight} of ${el.scrollHeight}`);
      }
    }
  }

  // The bars: the chrome below the status bar, fixed things above the button bar.
  const chrome = document.querySelector('.chrome');
  if (chrome) {
    const firstRow = [...chrome.querySelectorAll('button, a')].filter((e) => shown(e) === true);
    const highest = Math.min(...firstRow.map((e) => e.getBoundingClientRect().top));
    if (highest < TOP) res.bars.push(`chrome control at y=${Math.round(highest)} under the status bar`);
  }
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    if (r.height < 8 || r.width < 8 || shown(el) === false) continue;
    if (cs.pointerEvents === 'none' && !el.querySelector('button, a')) continue;
    const kids = el.matches('button, a') ? [el] : [...el.querySelectorAll('button, a, input')];
    for (const k of kids) {
      const kr = k.getBoundingClientRect();
      if (kr.height < 4 || shown(k) !== true) continue;
      if (kr.bottom > vh - BOTTOM + 1 && kr.top < vh) { res.bars.push(`${name(k)} bottom=${Math.round(kr.bottom)} under the button bar`); break; }
    }
    if (res.bars.length > 4) break;
  }
  return res;
}, { TOP, BOTTOM });

/** A finger's swipe up in a pane, then whether it moved. */
// Raw touch events: Input.synthesizeScrollGesture reports success here and moves nothing.
async function swipe(p) {
  const from = Math.min(p.y + 60, H - BOTTOM - 4);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: p.x, y: from }] });
  for (let i = 1; i <= 8; i++) {
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: p.x, y: from - i * 15 }] });
    await page.waitForTimeout(16);
  }
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await page.waitForTimeout(450);
  return page.evaluate((id) => document.querySelector(`[data-walk-id="${id}"]`)?.scrollTop ?? -1, p.id);
}

const lines = [];
const details = {};
const report = (s) => { console.log(s); lines.push(s); };
report(`viewer walk at ${W}x${H}, safe areas ${insets ? `${TOP}/${BOTTOM}` : 'not emulated'}, ${views.length} views`);

for (const v of views) {
  errors.length = 0;
  const file = `${v.layer}--${v.mode}`;
  await page.goto(`${base}/?layer=${v.layer}&mode=${v.mode}`, { waitUntil: 'domcontentloaded' });
  await settle();
  const landed = await page.evaluate(() => `${new URLSearchParams(location.search).get('layer')}:${new URLSearchParams(location.search).get('mode')}`);
  await page.screenshot({ path: path.join(out, `${file}.png`) });
  const m = await measure();
  const stuck = [];
  for (const p of m.panes.slice(0, 6)) {
    const after = await swipe(p);
    if (after <= p.top + 2) stuck.push(`${p.name} (${p.over}px more)`);
  }
  const flags = [];
  if (stuck.length) flags.push(`STUCK ${stuck.join('; ')}`);
  if (m.clip.length) flags.push(`CLIP ${m.clip.join('; ')}`);
  if (m.docWide > W + 1 || m.wide.length) flags.push(`WIDE${m.docWide > W + 1 ? ` doc ${m.docWide}px` : ''} ${m.wide.join('; ')}`);
  if (m.small.length) flags.push(`SMALL ${m.small.length}: ${m.small.slice(0, 5).join(', ')}`);
  if (m.tiny) flags.push(`TINY ${m.tiny}: ${m.tinySample.join(', ')}`);
  if (m.bars.length) flags.push(`BARS ${m.bars.join('; ')}`);
  if (errors.length) flags.push(`ERR ${[...new Set(errors)].slice(0, 3).join(' ; ')}`);
  details[`${v.layer}:${v.mode}`] = m.classes;
  report(`${v.layer}:${v.mode} [${v.label}] ${m.view}${landed !== `${v.layer}:${v.mode}` ? ` landed ${landed}` : ''} panes=${m.panes.length}${flags.length ? `\n    ${flags.join('\n    ')}` : ' ok'}`);
}

if (argv.includes('--drawers')) {
  for (const l of layers) {
    if (only && !views.some((v) => v.layer === l.key)) continue;
    await page.goto(`${base}/?layer=${l.key}&mode=${l.modes[0][0]}`, { waitUntil: 'domcontentloaded' });
    await settle();
    for (const side of ['left', 'right']) {
      const btn = page.locator(`#drawer-${side}-toggle`);
      if (!(await btn.isVisible().catch(() => false))) { report(`drawer ${side} on ${l.key}: no toggle shown`); continue; }
      await btn.tap();
      await page.waitForTimeout(500);
      await page.screenshot({ path: path.join(out, `drawer-${side}--${l.key}.png`) });
      const pane = await page.evaluate((side) => {
        const root = document.getElementById(`sidebar-${side}`);
        const el = [root, ...root.querySelectorAll('*')].find((e) => ['auto', 'scroll'].includes(getComputedStyle(e).overflowY) && e.scrollHeight > e.clientHeight + 24 && e.clientHeight > 80);
        if (!el) return null;
        el.dataset.walkId = 'drawer';
        const r = el.getBoundingClientRect();
        return { id: 'drawer', name: el.className, x: Math.round(r.left + r.width / 2), y: Math.round(Math.min(r.bottom - 40, (r.top + r.bottom) / 2)), top: el.scrollTop, over: el.scrollHeight - el.clientHeight };
      }, side);
      const after = pane ? await swipe(pane) : null;
      report(`drawer ${side} on ${l.key}: ${pane ? (after > pane.top + 2 ? 'scrolls' : `STUCK ${pane.name}`) : 'nothing to scroll'}`);
      await page.locator(`#drawer-${side}-toggle`).tap().catch(() => {});
      await page.waitForTimeout(400);
    }
  }
}

if (argv.includes('--desktop')) {
  const desk = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, colorScheme: 'dark', reducedMotion: 'reduce' });
  await desk.addInitScript(() => { localStorage.setItem('ticvai-api', ''); localStorage.setItem('ticvai-theme', 'dark'); sessionStorage.setItem('ticvai-session', '1'); });
  await signedIn(desk);
  const dp = await desk.newPage();
  mkdirSync(path.join(out, 'desktop'), { recursive: true });
  for (const v of views) {
    await dp.goto(`${base}/?layer=${v.layer}&mode=${v.mode}`, { waitUntil: 'domcontentloaded' });
    await dp.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await dp.waitForTimeout(1800);
    await dp.screenshot({ path: path.join(out, 'desktop', `${v.layer}--${v.mode}.png`) });
  }
  report(`desktop: ${views.length} shots in ${path.join(out, 'desktop')}`);
}

writeFileSync(path.join(out, 'walk.txt'), `${lines.join('\n')}\n`);
writeFileSync(path.join(out, 'classes.json'), JSON.stringify(details, null, 1));
await browser.close();
