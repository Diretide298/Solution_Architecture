// The Contracts layer never said where a contract lands in the database. The
// Backend layer has said the reverse since the start, so the trail ran one way
// only. These checks are all on a COLD tab, because the two parts the block
// reads are extras on this layer and arrive after the reader is already drawn —
// which is exactly where a block like this fails quietly.
import puppeteer from 'puppeteer-core';
import { authed } from './_session.mjs';
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

/** A fresh tab opened straight at one node, nothing warmed by an earlier visit. */
async function coldAt(id) {
  const page = await browser.newPage();
  page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
  await page.setViewport({ width: 1600, height: 1000 });
  await signIn(page);
  // the node id contains a '#' of its own, so it has to be encoded or the
  // fragment stops at the contract file
  await page.goto(`${VIEWER}/#${encodeURIComponent(id)}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(3500); // let the extras land — the block is redrawn when they do
  return page;
}

const readTrace = (page) => page.evaluate(() => {
  const box = document.getElementById('reader-trace');
  return {
    text: box.textContent.trim(),
    heads: [...box.querySelectorAll('.journey-section-label, .section-head')].map((n) => n.textContent.trim()),
    rows: [...box.querySelectorAll('.link-item .link-name')].map((n) => n.textContent.trim()),
    chips: [...box.querySelectorAll('.lineage-table')].map((n) => n.textContent.trim()),
    writes: [...box.querySelectorAll('.lineage-table.write')].map((n) => n.textContent.trim()),
    services: [...box.querySelectorAll('.lineage-service')].map((n) => n.textContent.trim()),
  };
});

const B = await (await authed(`${VIEWER}/api/backend`)).json();
const L = await (await authed(`${VIEWER}/api/lineage`)).json();

// ── 1. a schema stored across two tables ─────────────────────────────
{
  const id = 'schema:contracts/satellite/subscription.yaml#SubscriptionInvoice';
  const expected = (B.tables ?? []).filter((t) => t.schemaId === id).map((t) => t.name);
  const page = await coldAt(id);
  const t = await readTrace(page);
  check('a schema names the tables it is stored as', t.rows.length === expected.length,
    `${t.rows.length} rows, expected ${expected.length}: ${expected.join(', ')}`);
  check('and names them correctly', expected.every((n) => t.rows.includes(n)), t.rows.join(', '));
  check('and says so when it is more than one', /stored across 2 tables/.test(t.text));
  await page.close();
}

// ── 2. a schema that becomes no table says why ───────────────────────
{
  const schemas = await (await authed(`${VIEWER}/api/index`)).json()
    .then((idx) => idx.nodes.filter((n) => n.type === 'schema'));
  const stored = new Set((B.tables ?? []).map((t) => t.schemaId).filter(Boolean));
  const orphan = schemas.find((s) => !stored.has(s.id));
  const page = await coldAt(orphan.id);
  const t = await readTrace(page);
  check('a schema stored as nothing says so rather than drawing nothing',
    /No table in the schema reference is derived from this schema/.test(t.text), orphan.name);
  check('and it is not an empty block', t.text.length > 40);
  await page.close();
}

// ── 3. an operation that resolves to tables ──────────────────────────
{
  const op = (L.operations ?? []).find((o) => (o.writes?.length ?? 0) > 1 && o.service);
  const node = await (await authed(`${VIEWER}/api/index`)).json()
    .then((idx) => idx.nodes.find((n) => n.type === 'operation' && n.name === op.name));
  const page = await coldAt(node.id);
  const t = await readTrace(page);
  check('an operation names the tables it reaches', t.chips.length > 0,
    `${op.name}: ${t.chips.join(', ')}`);
  check('and marks which of them it writes', t.writes.length === op.writes.length,
    `${t.writes.length} of ${op.writes.length}`);
  check('and names the service behind it', t.services.includes(op.service), t.services.join(', '));
  check('and none of the chips is marked unknown — the backend part is in hand',
    await page.evaluate(() => ![...document.querySelectorAll('#reader-trace .lineage-table')]
      .some((c) => c.classList.contains('unknown'))));
  await page.close();
}

// ── 4. an unresolved operation is drawn, not dropped ─────────────────
{
  const op = (L.operations ?? []).find((o) => o.source === 'unresolved');
  // The package resolved its last unresolved operation — 932 of 932 — so the
  // fixture this asserts on no longer exists. Skipped and said out loud rather
  // than crashed on `op.name`, and rather than passed quietly: if an
  // unresolved operation ever comes back, this starts running again by itself.
  if (!op) {
    console.log('SKIP  an unresolved operation is drawn, not dropped '
      + '— every operation resolves, so there is nothing in this state');
  } else {
  const node = await (await authed(`${VIEWER}/api/index`)).json()
    .then((idx) => idx.nodes.find((n) => n.type === 'operation' && n.name === op.name));
  const page = await coldAt(node.id);
  const t = await readTrace(page);
  check('an unresolved operation says the lineage carries no tables for it',
    /carries no tables for this operation/.test(t.text), op.name);
  check('and does not claim it touches nothing',
    /not a claim that/.test(t.text));
  await page.close();
  }
}

// ── 5. the chip opens the table in the Backend layer ─────────────────
{
  const op = (L.operations ?? []).find((o) => (o.writes?.length ?? 0) > 0);
  const node = await (await authed(`${VIEWER}/api/index`)).json()
    .then((idx) => idx.nodes.find((n) => n.type === 'operation' && n.name === op.name));
  const page = await coldAt(node.id);
  await page.evaluate(() => document.querySelector('#reader-trace .lineage-table').click());
  await wait(1500);
  const landed = await page.evaluate(() => ({
    layer: window.__state.layer, mode: window.__state.mode, table: window.__state.tableName,
  }));
  check('a table chip lands on that table in the Backend layer',
    landed.layer === 'backend' && landed.table === op.writes[0],
    `${landed.layer}/${landed.mode} · ${landed.table}`);
  await page.close();
}

// ── 6. a file node draws no trace block at all ───────────────────────
{
  const node = await (await authed(`${VIEWER}/api/index`)).json()
    .then((idx) => idx.nodes.find((n) => n.type === 'file'));
  const page = await coldAt(node.id);
  const t = await readTrace(page);
  check('a contract file draws no trace block — it is not a thing with a table',
    t.text === '', t.text.slice(0, 60));
  await page.close();
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
