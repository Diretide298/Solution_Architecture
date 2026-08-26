/**
 * The LINKS rail describes the layer you are on, and no other.
 *
 * This bug has now been fixed twice. The first fix moved the clear out of the
 * individual renderers and up in front of the dispatch, which stopped a layer
 * with no dispatch line from keeping the *previous* layer's pane — and gave
 * each layer its own empty sentence, because "Select a table." on Decisions was
 * the Backend empty state wearing a plausible noun.
 *
 * It left the harder half. `state.selectedId` is written only by `select()`,
 * and `select()` only resolves ids in `state.nodesById`, which holds contract
 * artefacts. The Decisions layer never calls it — it tracks `state.adrId` — so
 * the tail of the dispatch read a contract selection on a layer that has none,
 * and the rail showed the last contract's REFERENCED BY and REFERENCES under a
 * heading about decisions. **An empty state left behind looks like a bug; real
 * content left behind looks like an answer**, which is why the second half
 * survived the first fix and why it is worth a check rather than a re-read.
 *
 * So: pick something on Contracts, walk every layer, and assert each one either
 * says its own sentence or shows its own content — and that coming back to
 * Contracts still restores the selection, because the fix must not be "clear
 * the selection", which would cost the reader their place on every excursion.
 */
import puppeteer from 'puppeteer-core';
import { authed, VIEWER } from './_session.mjs';

const BASE = VIEWER.replace(/\/+$/, '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

let pass = 0, fail = 0;
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};

const gated = await fetch(`${BASE}/pkg/projects`, { redirect: 'manual' })
  .then((r) => r.status !== 200).catch(() => true);
const registry = await (gated ? authed(`${BASE}/pkg/projects`) : fetch(`${BASE}/pkg/projects`))
  .then((r) => (r.ok ? r.json() : null)).catch(() => null);
const project = registry?.default ?? registry?.projects?.find((p) => p.active !== false)?.id;
if (!project) throw new Error('no project in /pkg/projects — is projects.json empty?');

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000 });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

// Same-origin, so the viewer proxies /api/* and the SameSite=lax cookie sticks.
await page.goto(BASE + '/invite.html', { waitUntil: 'domcontentloaded' });
await page.evaluate(() => localStorage.setItem('ticvai-api', ''));
if (gated) {
  await page.evaluate(async (e, p) => {
    await fetch('/api/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: e, password: p }),
    });
  },
    process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
    process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase');
}

await page.goto(`${BASE}/?project=${encodeURIComponent(project)}`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 30000 });
await wait(7000);

const rail = () => page.evaluate(
  () => (document.getElementById('links-pane')?.innerText ?? '').replace(/\s+/g, ' ').trim()
);
const openLayer = async (l) => {
  await page.evaluate((k) => document.querySelector(`#layers button[data-layer="${k}"]`)?.click(), l);
  await wait(2600);
};

await openLayer('contracts');
const picked = await page.evaluate(() => {
  const row = document.querySelector('#tree .tree-row, #tree button, #tree [data-id]');
  if (!row) return null;
  row.click();
  return row.innerText.trim().split('\n')[0];
});
await wait(3000);
const contractsRail = await rail();
check('a contract can be selected and fills the rail',
  Boolean(picked) && /REFERENCES|REFERENCED BY/i.test(contractsRail), `${picked} — ${contractsRail.slice(0, 60)}`);

// The signature of the leak: the contract's own rail text appearing anywhere else.
const fingerprint = contractsRail.slice(0, 60);

for (const layer of ['decisions', 'domain', 'backend', 'frontend']) {
  await openLayer(layer);
  const text = await rail();
  check(`the ${layer} rail is not the contract's`, !text.startsWith(fingerprint),
    text.slice(0, 70));
  check(`the ${layer} rail says something`, text.length > 0);
}

// Decisions is the one with no rail of its own, so it must ask in its own noun
// rather than fall through to a contract or to another layer's sentence.
await openLayer('decisions');
const decisions = await rail();
check('the decisions rail asks for a decision', /decision|register/i.test(decisions), decisions.slice(0, 70));

// A theme flip repaints everything that carries an inline colour, and it used
// to repaint the rail by calling the Contracts renderer on `selectedId`
// directly — putting the contract back on Decisions, through a door the
// dispatch does not watch. Still on Decisions here.
await page.evaluate(() => document.getElementById('theme-toggle')?.click());
await wait(1500);
const flipped = await rail();
check('a theme flip does not repaint the contract onto decisions',
  !flipped.startsWith(fingerprint), flipped.slice(0, 70));
await page.evaluate(() => document.getElementById('theme-toggle')?.click());
await wait(1200);

// And the selection survives the excursion — the fix is scoping the read, not
// clearing the selection.
await openLayer('contracts');
const back = await rail();
check('returning to contracts restores the selection', back.startsWith(fingerprint), back.slice(0, 70));

check('no console or page errors', errors.length === 0, errors.slice(0, 4).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
