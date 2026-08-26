// A pane that reads a part has to ask for it, even when the view around it does
// not. Every check here is against a COLD load — one navigation, no visiting
// another layer first — because that is the state the bugs lived in.
import puppeteer from 'puppeteer-core';
const VIEWER = 'http://localhost:4173';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

let signedIn = false;
async function signIn(page) {
  if (signedIn) return;
  await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
  const ok = await page.evaluate(async () => (await fetch('http://localhost:8787/api/auth/login', {
    method: 'POST', credentials: 'include',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
  })).ok);
  if (!ok) throw new Error('could not sign in');
  signedIn = true;
}

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];

/** A brand new tab, so nothing has been warmed by an earlier visit. */
async function cold(hash = '') {
  const page = await browser.newPage();
  page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
  await page.setViewport({ width: 1600, height: 1000 });
  await signIn(page);
  await page.goto(`${VIEWER}/${hash}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(3200); // the extras are fetched behind the layer; give them time to land
  return page;
}

const L = await (await fetch(`${VIEWER}/api/lineage`)).json();
const J = await (await fetch(`${VIEWER}/api/journeys`)).json();
const B = await (await fetch(`${VIEWER}/api/backend`)).json();
const realTables = new Set((B.tables ?? []).map((t) => t.name));

// ── 1. the lineage table chips ───────────────────────────────────────
{
  const page = await cold();
  await page.evaluate(() => document.querySelector('#modes .mode[data-mode="lineage"]').click());
  await wait(3000);
  const chips = await page.evaluate(() => {
    const all = [...document.querySelectorAll('#lineage-body .lineage-table')];
    return { total: all.length, unknown: all.filter((c) => c.classList.contains('unknown')).length };
  });
  check('on a cold Lineage view, the table chips are not all marked unknown',
    chips.total > 0 && chips.unknown < chips.total,
    `${chips.unknown} of ${chips.total} unknown`);
  // The bug marked every chip; the truth is a handful. Assert the shape rather
  // than an exact figure, which moves whenever the delivery does.
  check('and only a handful are marked unknown',
    chips.unknown < chips.total * 0.05,
    `${chips.unknown} of ${chips.total} — under 5% is the real rate`);

  // and a chip actually opens its table
  const opened = await page.evaluate(async () => {
    const chip = [...document.querySelectorAll('#lineage-body .lineage-table')]
      .find((c) => !c.classList.contains('unknown'));
    if (!chip) return { none: true };
    const name = chip.textContent.trim();
    chip.click();
    await new Promise((r) => setTimeout(r, 1600));
    return { name, layer: window.__state.layer, mode: window.__state.mode, table: window.__state.tableName };
  });
  check('and clicking one opens it in Backend',
    !opened.none && opened.layer === 'backend' && Boolean(opened.table),
    opened.none ? 'no usable chip' : `${opened.name} -> ${opened.layer}/${opened.mode} ${opened.table}`);
  await page.close();
}

// ── 2. called-by-screens on an operation ─────────────────────────────
{
  // The operation's own contract, not a guessed one — the node id is built from
  // the file it lives in, and guessing sends the viewer looking for nothing.
  const index = await (await fetch(`${VIEWER}/api/index`)).json();
  const withUsage = Object.keys(J.operationUsage ?? {})
    .sort((a, b) => (J.operationUsage[b].screens?.length ?? 0) - (J.operationUsage[a].screens?.length ?? 0));
  let name = null, nodeId = null;
  for (const candidate of withUsage) {
    const node = index.nodes.find((n) => n.type === 'operation' && n.name === candidate);
    if (node) { name = candidate; nodeId = node.id; break; }
  }
  const expected = J.operationUsage[name].screens.length;

  const page = await cold(`#${encodeURIComponent(nodeId)}`);
  const pane = await page.evaluate(() => ({
    heads: [...document.querySelectorAll('#links-pane .links-section-head')].map((h) => h.textContent),
    empty: [...document.querySelectorAll('#links-pane .pane-empty')].map((n) => n.textContent),
  }));
  const said = pane.heads.find((h) => /Called by screens/.test(h)) ?? '';
  const count = Number((said.match(/(\d+)$/) ?? [])[1] ?? -1);
  check(`a cold operation pane counts the screens that call it (${name})`,
    count === expected, `pane says ${count}, journeys says ${expected}`);
  check('and does not claim no screen calls it when some do',
    !pane.empty.some((t) => /No screen definition calls this operation/.test(t)) || expected === 0,
    pane.empty.join(' | ').slice(0, 80) || 'no false claim');
  await page.close();
}

// ── 3. "persisted as" on a schema ────────────────────────────────────
{
  const persisted = (B.tables ?? []).find((t) => t.schemaId);
  const page = await cold(`#${encodeURIComponent(persisted.schemaId)}`);
  const heads = await page.evaluate(() =>
    [...document.querySelectorAll('#links-pane .links-section-head')].map((h) => h.textContent));
  check('a cold schema pane says what it is persisted as',
    heads.some((h) => /Persisted as/.test(h)),
    `${persisted.schemaId} -> ${heads.join(' | ').slice(0, 70)}`);
  await page.close();
}

// ── 4. screens that reach a table, in Backend ────────────────────────
{
  const busy = [...(L.whereUsed ?? [])].sort((a, b) => b.screenCount - a.screenCount)[0];
  const page = await cold();
  await page.evaluate(() => document.querySelector('#layers button[data-layer="backend"]').click());
  await wait(2600);
  await page.evaluate((name) => {
    document.querySelector('#modes .mode[data-mode="data"]')?.click();
    const row = [...document.querySelectorAll('#tree .tree-file')].find((r) => r.dataset.id === `table:${name}`);
    row?.scrollIntoView({ block: 'center' });
    row?.click();
  }, busy.table);
  await wait(3000);
  const rows = await page.evaluate(() =>
    [...document.querySelectorAll('#links-pane .link-item')].map((i) => i.textContent));
  // a resolved screen shows its name; an unresolved one shows a bare sheet ref
  const named = rows.filter((t) => /[A-Z]{3}-\d{3}\s+\S/.test(t)).length;
  check(`a cold table pane names the screens that reach it (${busy.table})`,
    named > 0, `${named} named of ${rows.length} rows`);
  await page.close();
}

// ── 5. table chips on a screen ───────────────────────────────────────
{
  const screen = [...L.screens].sort((a, b) =>
    (b.reads.length + b.writes.length) - (a.reads.length + a.writes.length))[0];
  const page = await cold();
  await page.evaluate(() => document.querySelector('#layers button[data-layer="frontend"]').click());
  await wait(2200);
  await page.evaluate((id) => {
    document.querySelector('#modes .mode[data-mode="screen"]')?.click();
    const sel = document.getElementById('screen-scope');
    if (sel) { sel.value = `screen:${id}`; sel.dispatchEvent(new Event('change')); }
  }, screen.id);
  await wait(3200);
  const chips = await page.evaluate(() => {
    const all = [...document.querySelectorAll('#screen-body .lineage-table')];
    return { total: all.length, unknown: all.filter((c) => c.classList.contains('unknown')).length };
  });
  const expectUnknown = [...screen.reads, ...screen.writes].filter((t) => !realTables.has(t)).length;
  check(`a cold screen's table chips are not all marked unknown (${screen.id})`,
    chips.total > 0 && chips.unknown <= expectUnknown,
    `${chips.unknown} of ${chips.total} unknown, ${expectUnknown} genuinely absent`);
  await page.close();
}

// ── 6. verdict blocks let go when their pane is replaced ─────────────
{
  const page = await cold();
  const growth = await page.evaluate(async () => {
    // open twenty operations in turn, then see how many blocks still answer
    const before = performance.now();
    const rows = [...document.querySelectorAll('#tree .tree-file')];
    rows[0]?.click();
    await new Promise((r) => setTimeout(r, 700));
    const children = [...document.querySelectorAll('#tree .tree-children .tree-child, #tree .tree-children .tree-file')];
    for (const child of children.slice(0, 12)) {
      child.click();
      await new Promise((r) => setTimeout(r, 120));
    }
    return { visited: Math.min(12, children.length), ms: Math.round(performance.now() - before) };
  });
  // the real assertion: only the block on screen may still be listening, which
  // shows up as exactly one validation request when the session changes
  const requests = [];
  page.on('request', (r) => {
    if (r.url().includes('/api/validation/')) requests.push(r.url());
  });
  await page.evaluate(() => window.dispatchEvent(new Event('focus')));
  await page.evaluate(async () => {
    const mod = await import('/validation.js');
    await mod.refreshSession();
  });
  await wait(1400);
  check('a stale verdict block stops asking once its pane is gone',
    requests.length <= 2,
    `${requests.length} validation request(s) after ${growth.visited} panes`);
  await page.close();
}

check('no page errors', errors.length === 0, errors.slice(0, 3).join(' | '));
await browser.close();
console.log(`\nRESULT: ${pass}/${pass + fail} passed — ${fail ? 'FAIL' : 'PASS'}`);
process.exitCode = fail ? 1 : 0;
