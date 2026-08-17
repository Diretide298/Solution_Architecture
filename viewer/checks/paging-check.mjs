// The boot payload is split and the long list is built a page at a time. Both
// are the kind of change that looks fine and quietly loses rows, so the checks
// are about what is still reachable, not about what is fast.
import puppeteer from 'puppeteer-core';
const VIEWER = 'http://localhost:4173';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

// ── the payload, before any browser is involved ──────────────────────
{
  const slim = await (await fetch(`${VIEWER}/api/index`)).json();
  const full = await (await fetch(`${VIEWER}/api/index?full=1`)).json();
  check('the index still carries every node', slim.nodes.length === full.nodes.length,
    `${slim.nodes.length} nodes`);
  check('and every edge', slim.edges.length === full.edges.length, `${slim.edges.length} edges`);
  check('the held-back fields are gone from it',
    !slim.nodes.some((n) => 'properties' in n || 'description' in n));
  check('and ?full=1 still has them',
    full.nodes.some((n) => 'properties' in n) && full.nodes.some((n) => 'description' in n));

  const smaller = JSON.stringify(slim).length / JSON.stringify(full).length;
  check('the boot payload is meaningfully smaller', smaller < 0.75,
    `${Math.round(smaller * 100)}% of the full index`);

  // every field held back is reachable again, contract by contract
  const files = [...new Set(full.nodes.map((n) => n.file))];
  let missing = 0, checked = 0;
  for (const file of files) {
    const detail = await (await fetch(`${VIEWER}/api/detail?file=${encodeURIComponent(file)}`)).json();
    for (const node of full.nodes.filter((n) => n.file === file)) {
      const heavy = ['description', 'properties'].filter((k) => k in node);
      if (!heavy.length) continue;
      checked++;
      if (heavy.some((k) => JSON.stringify(detail[node.id]?.[k]) !== JSON.stringify(node[k]))) missing++;
    }
  }
  check('every held-back field comes back from /api/detail', missing === 0,
    `${checked} nodes checked across ${files.length} contracts, ${missing} wrong`);

  const gz = await fetch(`${VIEWER}/api/index`, { headers: { 'accept-encoding': 'gzip' } });
  check('the index is served compressed', gz.headers.get('content-encoding') === 'gzip');
}

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
await page.setViewport({ width: 1600, height: 1000 });
await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate(async () => { await fetch('http://localhost:8787/api/auth/login', { method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }) }); });
await page.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 25000 });
await wait(3000);

// ── the reader still has its prose ───────────────────────────────────
{
  const full = await (await fetch(`${VIEWER}/api/index?full=1`)).json();
  const node = full.nodes.find((n) => n.type === 'operation' && (n.description ?? '').length > 60);
  await page.goto(`${VIEWER}/#${encodeURIComponent(node.id)}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(3000);
  const shown = await page.evaluate(() => document.querySelector('.reader-desc')?.textContent ?? '');
  check('the reader shows prose the index no longer carries',
    shown.trim().slice(0, 40) === node.description.trim().slice(0, 40), node.name);
}

// ── the ER diagram still has its fields ──────────────────────────────
{
  await page.evaluate(() => document.querySelector('#modes .mode[data-mode="er"]').click());
  await wait(4000);
  const er = await page.evaluate(() => ({
    boxes: window.__er?.nodes?.length ?? 0,
    rows: (window.__er?.nodes ?? []).reduce((n, b) => n + (b.rows?.length ?? 0), 0),
    hint: document.getElementById('er-hint').textContent,
  }));
  check('the ER diagram draws its entities', er.boxes > 0, `${er.boxes} boxes`);
  check('and their fields, which arrive after the index', er.rows > 0, `${er.rows} rows`);
  check('and the hint is no longer the waiting message', !/reading the fields/.test(er.hint), er.hint);
}

// ── the long list is built a group at a time ─────────────────────────
{
  await page.evaluate(() => document.querySelector('#layers button[data-layer="contracts"]').click());
  await wait(1200);
  await page.evaluate(() => document.querySelector('#modes .mode[data-mode="lineage"]').click());
  await wait(3000);

  const before = await page.evaluate(() => ({
    elements: document.querySelector('#lineage-body').querySelectorAll('*').length,
    groups: document.querySelectorAll('#lineage-body .lineage-group').length,
    rows: document.querySelectorAll('#lineage-body .lineage-row').length,
  }));
  check('a closed group builds no rows', before.rows === 0, `${before.groups} groups, ${before.rows} rows`);
  check('and the whole pane is a fraction of what it was', before.elements < 800,
    `${before.elements} elements`);

  // Open the largest group — the page cap only shows itself above 60 rows, and
  // most contracts are smaller than that. The groups are sorted largest first,
  // so this is also the one a reader meets at the top.
  const opened = await page.evaluate(() => {
    const group = document.querySelector('#lineage-body .lineage-group');
    group.open = true;
    group.id = 'probe-group';
    return group.querySelector('.lineage-group-count').textContent;
  });
  await wait(600);
  const total = Number(/of (\d+)/.exec(opened)[1]);
  const after = await page.evaluate(() => ({
    rows: document.querySelectorAll('#probe-group .lineage-row').length,
    more: document.querySelector('#probe-group .lineage-more')?.textContent ?? null,
  }));
  check('opening a group fills it', after.rows > 0, `${after.rows} rows · ${opened}`);

  // The page size is the app's business, not the harness's — so infer whether
  // the cap fired from what was drawn, and check the right thing either way.
  const capped = after.rows < total;
  if (capped) {
    check('a group longer than a page stops at one page and offers the rest',
      after.more !== null, `${after.rows} of ${total} rows · ${after.more ?? 'no button'}`);
    const left = Number(/(\d+)/.exec(after.more)[1]);
    check('the count on the button is exactly what is left', left === total - after.rows,
      `${left}, expected ${total - after.rows}`);
    await page.evaluate(() => document.querySelector('#probe-group .lineage-more').click());
    await wait(600);
    const grown = await page.evaluate(() => ({
      rows: document.querySelectorAll('#probe-group .lineage-row').length,
      more: document.querySelector('#probe-group .lineage-more')?.textContent ?? null,
    }));
    check('the button brings the next page', grown.rows > after.rows, `${after.rows} → ${grown.rows}`);
    check('and only one button is ever showing',
      await page.evaluate(() => document.querySelectorAll('#probe-group .lineage-more').length) <= 1);
    // walk it to the end — a paging bug that drops the tail only shows here
    let guard = 0;
    while (await page.evaluate(() => Boolean(document.querySelector('#probe-group .lineage-more')))) {
      if (++guard > 50) break;
      await page.evaluate(() => document.querySelector('#probe-group .lineage-more').click());
      await wait(200);
    }
    const ended = await page.evaluate(() =>
      document.querySelectorAll('#probe-group .lineage-row').length);
    check('paging to the end reaches every row and no more', ended === total,
      `${ended} of ${total} after ${guard} pages`);
  } else {
    check('a group that fits in one page gets no button', after.more === null,
      `${total} operations, all shown at once`);
    check('and shows all of them', after.rows === total, `${after.rows} of ${total}`);
  }

  // closing and reopening does not double them
  const wasShowing = await page.evaluate(() =>
    document.querySelectorAll('#probe-group .lineage-row').length);
  await page.evaluate(() => {
    const g = document.getElementById('probe-group');
    g.open = false; g.open = true;
  });
  await wait(500);
  const again = await page.evaluate(() =>
    document.querySelectorAll('#probe-group .lineage-row').length);
  check('reopening a group does not build it twice', again === wasShowing, `${wasShowing} → ${again}`);
}

// ── a filter still reaches rows in unopened groups ───────────────────
{
  const term = 'acceptFnbOrder';
  await page.evaluate((t) => {
    const input = document.getElementById('lineage-filter');
    input.value = t;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }, term);
  await wait(1500);
  const found = await page.evaluate((t) =>
    [...document.querySelectorAll('#lineage-body .lineage-op')].some((n) => n.textContent === t), term);
  check('filtering finds an operation whose group was never opened', found, term);
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
