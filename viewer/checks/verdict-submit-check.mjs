// A verdict is recorded by picking one and then submitting, not by a single
// click. Verdicts are append-only, so a mistaken one cannot be withdrawn —
// only argued with by a later row — and these checks are about the gap between
// choosing and writing, which is the whole point of the change.
//
// Runs against a scratch store, because it writes real verdicts:
//   TICVAI_DB=/tmp/scratch.db python -m uvicorn api.main:app --port 8788
//   node checks/verdict-submit-check.mjs --api http://localhost:8788
import puppeteer from 'puppeteer-core';

const VIEWER = 'http://localhost:4173';
const argApi = process.argv.indexOf('--api');
const API = argApi > -1 ? process.argv[argApi + 1] : 'http://localhost:8787';
const EMAIL = process.env.TICVAI_USER ?? 'harness.admin@softlabsgroup.com';
const PASSWORD = process.env.TICVAI_PASS ?? 'a-long-enough-passphrase';

let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
await page.setViewport({ width: 1500, height: 1000 });

await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate((a) => localStorage.setItem('ticvai-api', a), API);
const ok = await page.evaluate(async (a, e, p) => (await fetch(`${a}/api/auth/login`, {
  method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: e, password: p }),
})).ok, API, EMAIL, PASSWORD);
if (!ok) throw new Error(`could not sign in as ${EMAIL} against ${API}`);

// A screen page carries a verdict block and is cheap to reach.
await page.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 25000 });
await wait(3000);
await page.evaluate(() => document.querySelector('#layers button[data-layer="frontend"]').click());
await wait(2200);
await page.evaluate(() => document.querySelector('#modes .mode[data-mode="screen"]')?.click());
await page.waitForSelector('.verdict-set', { timeout: 25000 });
await wait(1500);

const target = await page.evaluate(() => {
  const box = document.querySelector('.verdict-box');
  return { kind: box.dataset.kind, id: box.dataset.target };
});
const countRows = () => page.evaluate(async (a, k, i) => {
  const r = await fetch(`${a}/api/validation/${k}/${encodeURIComponent(i)}`, { credentials: 'include' });
  return (await r.json()).history.length;
}, API, target.kind, target.id);

const before = await countRows();

// ── 1. the submit starts disabled ────────────────────────────────────
{
  const s = await page.evaluate(() => {
    const b = document.querySelector('.verdict-submit');
    return { exists: Boolean(b), disabled: b?.disabled, label: b?.textContent };
  });
  check('there is a submit button', s.exists, s.label);
  check('and it is disabled until a verdict is picked', s.disabled === true);
}

// ── 2. picking does NOT record ───────────────────────────────────────
{
  await page.evaluate(() => document.querySelector('.verdict-set.approved').click());
  await wait(1200);
  const after = await countRows();
  check('picking a verdict records nothing on its own', after === before,
    `${before} rows before, ${after} after clicking Approved`);
  const s = await page.evaluate(() => ({
    chosen: document.querySelectorAll('.verdict-set.chosen').length,
    pressed: document.querySelector('.verdict-set.approved')?.getAttribute('aria-pressed'),
    label: document.querySelector('.verdict-submit')?.textContent,
    disabled: document.querySelector('.verdict-submit')?.disabled,
  }));
  check('the picked one is marked chosen', s.chosen === 1 && s.pressed === 'true');
  check('and the submit keeps its steady label', s.label.trim() === 'Submit', s.label);
  check('and is now enabled', s.disabled === false);
}

// ── 3. only one can be chosen, and clicking it again clears it ───────
{
  await page.evaluate(() => document.querySelector('.verdict-set.rejected').click());
  await wait(500);
  const one = await page.evaluate(() => ({
    chosen: [...document.querySelectorAll('.verdict-set.chosen')].map((b) => b.dataset.verdict),
    submitRed: document.querySelector('.verdict-submit').classList.contains('rejected'),
  }));
  check('choosing another replaces the first', one.chosen.length === 1 && one.chosen[0] === 'rejected',
    one.chosen.join(','));
  check('and a rejection is not the same colour as an approval', one.submitRed);

  await page.evaluate(() => document.querySelector('.verdict-set.rejected').click());
  await wait(500);
  const cleared = await page.evaluate(() => ({
    chosen: document.querySelectorAll('.verdict-set.chosen').length,
    disabled: document.querySelector('.verdict-submit').disabled,
  }));
  check('clicking the chosen one again clears it, so a misclick costs nothing',
    cleared.chosen === 0 && cleared.disabled === true);
  const after = await countRows();
  check('and still nothing has been recorded', after === before, `${after} rows`);
}

// ── 4. submitting records exactly one, with the note ─────────────────
{
  const note = `harness ${Date.now()}`;
  await page.evaluate((n) => {
    document.querySelector('.verdict-note-input').value = n;
    document.querySelector('.verdict-set[data-verdict="needs-work"]').click();
  }, note);
  await wait(400);
  await page.evaluate(() => document.querySelector('.verdict-submit').click());
  await wait(2500);

  const after = await countRows();
  check('submitting records exactly one row', after === before + 1, `${before} → ${after}`);

  const top = await page.evaluate(async (a, k, i) => {
    const r = await fetch(`${a}/api/validation/${k}/${encodeURIComponent(i)}`, { credentials: 'include' });
    return (await r.json()).current;
  }, API, target.kind, target.id);
  check('with the verdict that was picked', top?.verdict === 'needs-work', top?.verdict);
  check('and the note that was typed', top?.note === note, top?.note);

  const reset = await page.evaluate(() => ({
    chosen: document.querySelectorAll('.verdict-set.chosen').length,
    note: document.querySelector('.verdict-note-input')?.value,
    disabled: document.querySelector('.verdict-submit')?.disabled,
  }));
  check('the form clears itself afterwards', reset.chosen === 0 && reset.note === '' && reset.disabled === true);
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
