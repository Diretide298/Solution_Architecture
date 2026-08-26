// Drives the running viewer and photographs it, so the manual's figures are the
// real application rather than mock-ups that drift from it.
//
//   node manual/capture.mjs            (viewer must be running on :4173)
//
// Every figure is one entry in SHOTS below. Add a view, add an entry.

import puppeteer from 'puppeteer-core';
import { mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(here, 'shots');
const URL = process.env.VIEWER_URL ?? 'http://localhost:4173';

// puppeteer-core brings no browser of its own, so find one already installed
const CANDIDATES = [
  process.env.CHROME,
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].filter(Boolean);
const EXE = CANDIDATES.find((p) => existsSync(p));
if (!EXE) {
  console.error('No Chrome found. Set CHROME=/path/to/chrome and re-run.');
  process.exit(1);
}

await mkdir(OUT, { recursive: true });

const browser = await puppeteer.launch({
  executablePath: EXE,
  headless: 'new',
  args: ['--no-sandbox', '--window-size=1600,1000', '--force-device-scale-factor=1'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000, deviceScaleFactor: 2 });

const problems = [];
page.on('console', (m) => m.type() === 'error' && problems.push(m.text()));
page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`));

// ── driving helpers ──────────────────────────────────────────────────
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const layer = async (key) => {
  await page.click(`#layers button[data-layer="${key}"]`);
  await wait(700);
};

const mode = async (key) => {
  await page.click(`#modes .mode[data-mode="${key}"]`);
  await wait(900);
};

/** Deep-link by node id — ids live in the hash, so this is how the app links. */
const open = async (id) => {
  await page.evaluate((nodeId) => {
    location.hash = encodeURIComponent(nodeId);
  }, id);
  await wait(700);
};

const press = async (sel) => {
  if (await page.$(sel)) {
    await page.click(sel);
    await wait(1100);
  }
};

/** Selects the first <option> whose label or value contains `match`. */
const pick = async (selectId, match) => {
  const label = await page.evaluate(
    ([id, m]) => {
      const sel = document.getElementById(id);
      if (!sel) return null;
      const opt = [...sel.options].find(
        (o) => o.textContent.toLowerCase().includes(m) || o.value.toLowerCase().includes(m)
      );
      if (!opt) return null;
      sel.value = opt.value;
      sel.dispatchEvent(new Event('change'));
      return opt.textContent.trim();
    },
    [selectId, match.toLowerCase()]
  );
  await wait(1000);
  if (!label) console.warn(`  ! #${selectId} has no option matching "${match}"`);
  return label;
};

/** Hovers a target and waits for the tip panel, so a figure can show one. */
const hover = async (selector, { nth = 0 } = {}) => {
  const found = await page.evaluate(
    ([sel, index]) => {
      const node = document.querySelectorAll(sel)[index];
      if (!node) return null;
      node.scrollIntoView({ block: 'center' });
      node.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
      return node.textContent.trim().slice(0, 40);
    },
    [selector, nth]
  );
  await wait(700);
  if (!found) console.warn(`  ! nothing matching "${selector}" to hover`);
  return found;
};

const taken = [];
const shot = async (name, clip) => {
  const file = path.join(OUT, `${name}.png`);
  await page.screenshot({ path: file, clip });
  taken.push(name);
  console.log(`  ✓ ${name}.png`);
};

/** Photographs one element rather than the window — used for the panes. */
const shotOf = async (name, selector, pad = 0) => {
  const box = await page.$eval(selector, (n) => {
    const r = n.getBoundingClientRect();
    return { x: r.x, y: r.y, width: r.width, height: r.height };
  });
  await shot(name, {
    x: Math.max(0, box.x - pad),
    y: Math.max(0, box.y - pad),
    width: box.width + pad * 2,
    height: box.height + pad * 2,
  });
};

// ── go ───────────────────────────────────────────────────────────────
console.log(`\nCapturing ${URL} with ${path.basename(EXE)}\n`);

// The viewer asks who you are before it draws anything, so the capture has to
// come in the way a person does. The credentials are read from the environment
// so that nobody's real password has to live in this file; the fallback is the
// account api/ui-auth-check.mjs makes on this machine, which is what makes
// `node manual/capture.mjs` work with nothing set.
const WHO = {
  email: process.env.VIEWER_EMAIL ?? 'harness.admin@softlabsgroup.com',
  password: process.env.VIEWER_PASSWORD ?? 'a-long-enough-passphrase',
};

console.log('signing in');
await page.goto(`${URL}/login.html`, { waitUntil: 'domcontentloaded' });
// If a session is already live this page forwards to the viewer instead of
// drawing a form, so its absence is a state rather than a failure.
const form = await page
  .waitForSelector('#signin:not([hidden]) #email', { timeout: 15000 })
  .catch(() => null);
if (form) {
  await wait(600);
  await shotOf('ac-login', '.auth-card', 14);
  await page.type('#email', WHO.email, { delay: 20 });
  await page.type('#password', WHO.password, { delay: 20 });
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'domcontentloaded' }).catch(() => {}),
    page.click('#submit'),
  ]);
  await wait(1400);
  console.log(`  signed in as ${WHO.email}`);
} else {
  console.log('  already signed in');
}

await page.goto(URL, { waitUntil: 'domcontentloaded' });
try {
  await page.waitForSelector('#layers button', { timeout: 20000 });
} catch {
  console.error(
    `\nThe viewer never drew. If it bounced to the sign-in page, ${WHO.email} is not\n` +
    'an account here — set VIEWER_EMAIL and VIEWER_PASSWORD and run this again.'
  );
  await browser.close();
  process.exit(1);
}
await wait(1800);

// -- 1. the window itself ---------------------------------------------------
console.log('anatomy');
await layer('contracts');
await mode('graph');
await press('#graph-recenter');
await shot('01-overview');
await shot('02-topbar', { x: 0, y: 0, width: 1600, height: 50 });
await shotOf('03-sidebar-left', '#sidebar-left');

// the measured geometry, so the manual's callout numbers sit on the real regions
const layout = await page.evaluate(() => {
  const rect = (sel) => {
    const n = document.querySelector(sel);
    if (!n) return null;
    const r = n.getBoundingClientRect();
    return { x: r.x, y: r.y, w: r.width, h: r.height };
  };
  return {
    page: { w: window.innerWidth, h: window.innerHeight },
    brand: rect('.brand'),
    layers: rect('#layers'),
    search: rect('#search-trigger'),
    modes: rect('#modes'),
    live: rect('#live-dot'),
    theme: rect('#theme-toggle'),
    groupBy: rect('#group-by'),
    filter: rect('#side-filter'),
    tree: rect('#tree'),
    main: rect('#main'),
    right: rect('#sidebar-right'),
  };
});
await writeFile(path.join(OUT, 'layout.json'), JSON.stringify(layout, null, 2));

// -- 2. contracts -----------------------------------------------------------
console.log('contracts');
for (const scope of ['spine', 'files', 'schemas', 'permissions']) {
  await page.click(`#graph-scope button[data-scope="${scope}"]`);
  await wait(2200);
  await press('#graph-recenter');
  await shot(`10-graph-${scope}`);
}

// the spine with one contract's events isolated — the reason the view exists
await page.click('#graph-scope button[data-scope="spine"]');
await wait(2000);
await press('#graph-recenter');
await page.evaluate(() => {
  const orders = window.__graph.nodes.find((n) => n.name === 'orders');
  if (!orders) return;
  window.__graph.hoverNode = orders;
  window.__graph._updateHighlight();
  window.__graph.draw();
});
await wait(600);
await shot('10-graph-spine-focused');

await open('op:contracts/spine/orders.yaml#listOrders');
await page.click('#graph-scope button[data-scope="local"]');
await wait(1800);
await press('#graph-recenter');
await shot('11-graph-local');

await mode('structure');
await wait(1500);
await press('#struct-fit');
await shot('12-structure-tree');
await page.click('#struct-layout button[data-layout="nested"]');
await wait(1800);
await press('#struct-fit');
await shot('13-structure-nested');
await page.click('#struct-layout button[data-layout="tree"]');
await wait(800);

await mode('er');
console.log(`  er scope: ${await pick('er-scope', 'fnb')}`);
await press('#er-fit');
await shot('14-er');

await mode('reader');
await open('op:contracts/spine/orders.yaml#createOrder');
await wait(900);
await shot('15-reader');
await shotOf('16-links-pane', '#sidebar-right');

await mode('audit');
await wait(900);
await shot('17-audit-contracts');

// search palette
await page.keyboard.down('Control');
await page.keyboard.press('KeyK');
await page.keyboard.up('Control');
await wait(400);
await page.keyboard.type('reserv', { delay: 60 });
await wait(700);
await shot('18-palette');
await page.keyboard.press('Escape');
await wait(400);

// -- 3. frontend ------------------------------------------------------------
console.log('frontend');
await layer('frontend');
await mode('screen');
await pick('screen-scope', 'WEB-001');
await shot('20-screen');

await mode('journey');
console.log(`  journey: ${await pick('journey-scope', 'F01')}`);
await shot('21-journey');

// drag the track to show that it pans
await page.mouse.move(900, 600);
await page.mouse.down();
for (const x of [800, 650, 500, 380, 300]) {
  await page.mouse.move(x, 600);
  await wait(60);
}
await page.mouse.up();
await wait(500);
await shot('22-journey-panned');

await mode('apps');
await shot('23-apps');
await page.evaluate(() => {
  document.querySelector('#apps-body iframe.wireframe-frame')
    ?.closest('.board-card')?.scrollIntoView({ block: 'center' });
});
await wait(1400);
await shot('23b-apps-wireframes');

// the wireframe on a screen — every screen has one, matched by id
await mode('screen');
await wait(900);
await page.evaluate(() => {
  const sel = document.getElementById('screen-scope');
  const opt = [...sel.options].find((o) => o.value === 'screen:POS-002')
    ?? [...sel.options].find((o) => /^screen:POS/.test(o.value));
  if (opt) { sel.value = opt.value; sel.dispatchEvent(new Event('change')); }
});
await wait(2600);
await page.evaluate(() => {
  document.querySelector('#screen-body iframe.wireframe-frame')
    ?.closest('.board-card')?.scrollIntoView({ block: 'center' });
});
await wait(900);
await shot('28-screen-wireframe');

// a component explaining itself, from the shared library
await page.evaluate(() => document.querySelector('#screen-body').scrollTo(0, 0));
await wait(600);
console.log(`  hovered: ${await hover('#screen-body .component-kind', { nth: 1 })}`);
await shot('29-hover-tip');

await mode('journey');
await wait(1600);
await page.evaluate(() => {
  document.querySelector('#journey-body iframe.wireframe-frame')
    ?.closest('.board-card')?.scrollIntoView({ block: 'center' });
});
await wait(1200);
await shot('28b-journey-wireframe');

await mode('audit');
await wait(900);
await shot('24-audit-frontend');

await shotOf('25-sidebar-frontend', '#sidebar-left');

// -- 3b. design boards ------------------------------------------------------
console.log('design boards');
await mode('screen');
await wait(800);

// a board on its own page, reached from the sidebar
const boardOpened = await page.evaluate(() => {
  const row = document.querySelector('#tree .board-row');
  if (!row) return null;
  row.scrollIntoView({ block: 'center' });
  row.click();
  return row.textContent.trim();
});
await wait(3000);
console.log(`  board: ${boardOpened ?? '(no board row in the sidebar)'}`);
await shot('26-board-page');

// a screen drawn from a board, scrolled to the board section
const withBoard = await page.evaluate(() => {
  const picker = document.getElementById('screen-scope');
  const option = [...picker.options].find((o) => o.value.startsWith('screen:POS-'));
  if (!option) return null;
  picker.value = option.value;
  picker.dispatchEvent(new Event('change'));
  return option.textContent.trim();
});
await wait(3000);
console.log(`  screen with a board: ${withBoard ?? '(none)'}`);
await page.evaluate(() => {
  const label = [...document.querySelectorAll('#screen-body .journey-section-label')]
    .find((n) => /design board/i.test(n.textContent));
  label?.scrollIntoView({ block: 'start' });
});
await wait(1200);
await shot('27-screen-board');

// -- 3b. domain -------------------------------------------------------------
console.log('domain');
await layer('domain');
await mode('states');
await wait(1800);
await press('#states-fit');
await shot('50-states-order');

// a state selected, so the right pane shows how it is left and reached
await page.evaluate(() => {
  const paid = window.__machine.nodes.find((n) => n.name === 'paid');
  if (!paid) return;
  window.__machine.selected = 'paid';
  window.__machine.onSelect(paid);
  window.__machine.draw();
});
await wait(900);
await shot('51-states-selected');
await shotOf('52-states-links', '#sidebar-right');

// a guard, shown on the transition the pointer is over
await page.evaluate(() => {
  const machine = window.__machine;
  const edge = machine.edges.find((e) => e.guard && e.operation);
  if (!edge) return;
  machine.hoverEdge = edge;
  machine.draw();
});
await wait(500);
await shot('53-states-guard');

console.log(`  states scope: ${await pick('states-scope', 'seat')}`);
await press('#states-fit');
await shot('54-states-seat');

await mode('events');
await wait(1600);
await shot('55-events-catalogue');
await page.evaluate(() => {
  const sel = document.getElementById('events-scope');
  const opt = [...sel.options].find((o) => o.value === 'order.paid');
  if (opt) { sel.value = opt.value; sel.dispatchEvent(new Event('change')); }
});
await wait(1400);
await shot('56-events-detail');

await mode('states');
await wait(900);
await shotOf('57-sidebar-domain', '#sidebar-left');
await mode('audit');
await wait(900);
await shot('58-audit-domain');

// -- 4. backend -------------------------------------------------------------
console.log('backend');
await layer('backend');
await mode('data');
await wait(1600);
await press('#data-fit');
await shot('30-data-all');

console.log(`  data scope: ${await pick('data-scope', 'orders')}`);
await wait(1600);
await press('#data-fit');
await shot('31-data-schema');

await mode('migrations');
await wait(900);
await shot('32-migrations');

await mode('routing');
await wait(900);
await shot('33-routing');

// a table selected, so the right pane shows what the DDL says about it
await mode('data');
await wait(1200);
await page.evaluate(() => {
  const sel = document.getElementById('data-scope');
  const opt = [...sel.options].find((o) => o.value === 'orders' || /orders/i.test(o.textContent));
  if (opt) {
    sel.value = opt.value;
    sel.dispatchEvent(new Event('change'));
  }
});
await wait(1400);
// rows carry the table id, which is steadier than matching their label text
const table = await page.evaluate(() => {
  const row = document.querySelector('#tree .tree-file[data-id="table:orders.sales_order"]');
  if (!row) return null;
  row.scrollIntoView({ block: 'center' });
  row.click();
  return row.dataset.id;
});
await wait(1400);
console.log(`  table: ${table ?? '(sales_order row not found in sidebar)'}`);
await shotOf('34-table-links', '#sidebar-right');
await shot('35-data-selected');

await mode('audit');
await wait(900);
await shot('36-audit-backend');

// -- 4b. the views added in the second drop --------------------------------
// These were photographed by hand once and then went three days without being
// regenerated, because this script did not know about them. A figure the
// rebuild skips is a figure that quietly stops being true.

const scope = async (paneId, key, settle = 1500) => {
  const sel = `#${paneId} button[data-scope="${key}"]`;
  if (!(await page.$(sel))) { console.warn(`  ! no ${key} scope in #${paneId}`); return false; }
  await page.click(sel);
  await wait(settle);
  return true;
};

await layer('contracts');
await mode('lineage');
await wait(1300);
await shot('hc-lineage');
if (await scope('lineage-scope', 'services', 1800)) await shot('hc-lineage-services');
if (await scope('lineage-scope', 'tables', 1600)) await shot('hc-lineage-tables');
await scope('lineage-scope', 'operations', 1000);

await layer('frontend');
await mode('waves');
await wait(1700);
await shot('hc-waves');

await layer('decisions');
await wait(1400);
await shot('hc-decisions');
if (await scope('decisions-scope', 'permissions', 1600)) await shot('hc-vectors');
if (await scope('decisions-scope', 'gaps', 1400)) await shot('hc-gaps');
if (await scope('decisions-scope', 'registers', 1400)) await shot('hc-registers');

// a table explaining itself in the delivery's own words
await layer('backend');
await wait(1200);
console.log(`  hovered: ${await hover('#tree .tree-file', { nth: 0 })}`);
await shot('hc-table-tip');

// the permissions graph, the densest one the declutter had to carry
await layer('contracts');
await mode('graph');
if (await scope('graph-scope', 'permissions', 4500)) await shot('hc-graph-permissions');

// the schema picker with the workbook's footnote rows no longer read as modules
await layer('backend');
await mode('data');
await wait(1600);
await shot('hc-data-clean');

// -- 5. accounts and sign-off ----------------------------------------------
// The one part of the viewer that writes rather than reads. It answers to the
// FastAPI service on 8787; with that stopped the blocks say so instead, which
// is a true picture of a half-started machine and no use as a figure. So the
// state each one was photographed in is printed rather than assumed.
console.log('accounts');
await layer('contracts');
await mode('reader');
await open('op:contracts/spine/catalogue.yaml#listProducts');
await wait(1400);
const verdict = await page.evaluate(() => {
  const box = document.querySelector('#reader-validation .verdict-box');
  if (!box) return null;
  return box.querySelector('.verdict-chip')?.textContent.trim() ?? '(no chip)';
});
console.log(`  verdict block: ${verdict ?? '(no block — is the operation selected?)'}`);
if (verdict === 'Not reviewed' || verdict === null) {
  console.warn('  ! nothing recorded on listProducts — is the service on 8787 running?');
}
await shotOf('ac-verdict', '#reader-validation', 8);

// The invites and the people, which live on their own page rather than in the
// panel. Only an admin is shown this, so the shot is only right when the
// account this signed in as is one.
await page.goto(`${URL}/admin.html`, { waitUntil: 'domcontentloaded' });
const isAdmin = await page
  .waitForSelector('#admin:not([hidden])', { timeout: 12000 })
  .catch(() => null);
if (isAdmin) {
  await wait(1200);
  await shot('ac-admin');
} else {
  console.warn(`  ! ${WHO.email} is not an admin, so there is no invite page to photograph`);
}
await page.goto(URL, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 20000 });
await wait(1600);

// -- 6. light theme, for the teams that print ------------------------------
await layer('contracts');
await mode('graph');
await page.click('#theme-toggle');
await wait(900);
await press('#graph-recenter');
await shot('40-light-theme');
await page.click('#theme-toggle');
await wait(600);

// -- 7. the phone ----------------------------------------------------------
// The responsive layout only exists below 760px, so none of it can be
// photographed at the 1600px width every shot above uses. One viewport swap,
// the shots that need it, and the desktop viewport back at the end — anything
// added after this section would otherwise be photographed on a phone.
console.log('phone');
const DESKTOP = { width: 1600, height: 1000, deviceScaleFactor: 2 };
const PHONE = { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true };

await page.setViewport(PHONE);
// The breakpoints are CSS and would apply to a bare resize, but the topbar
// rails scroll their active button into view on load and the drawer toggles
// are wired once — so reload rather than trusting the resize.
await page.reload({ waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 20000 });
await wait(2200);

await layer('contracts');
await mode('graph');
await press('#graph-recenter');
await shot('ph-graph');
// --topbar-h is 124px here: small controls, then the layer rail, then the modes
await shot('ph-topbar', { x: 0, y: 0, width: 390, height: 124 });

// the tree off-canvas, over the view it was opened from
await page.click('#drawer-left-toggle');
await wait(800);
await shot('ph-drawer');
// closed from the toggle, which is never under the backdrop — the backdrop's
// own centre is behind the open drawer, so clicking it here would miss
await page.click('#drawer-left-toggle');
await wait(600);

// The links pane is the other drawer, and its toggle stays hidden until the
// pane holds something — so there has to be a selection before this works.
await mode('reader');
await open('op:contracts/spine/orders.yaml#createOrder');
await wait(1400);
if (await page.$('#drawer-right-toggle:not([hidden])')) {
  await page.click('#drawer-right-toggle');
  await wait(800);
  await shot('ph-links');
} else {
  console.warn('  ! the links drawer toggle is hidden — nothing selected?');
}

await page.setViewport(DESKTOP);
await wait(600);

// ── report ───────────────────────────────────────────────────────────
await browser.close();

console.log(`\n${taken.length} figures written to manual/shots`);
if (problems.length) {
  console.log(`\n${problems.length} console error(s) while capturing:`);
  for (const p of problems.slice(0, 10)) console.log(`  ${p}`);
  process.exitCode = 1;
} else {
  console.log('no console errors');
}
