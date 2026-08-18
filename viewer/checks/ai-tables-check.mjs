// Clicking an AI table in the backend tree opened nothing: the scope picker was
// built from the workbook's Modules sheet, which has no `ai` row, so the
// renderer rejected the scope and fell back to the first schema alphabetically.
// This asks the running viewer whether the click now lands.
import puppeteer from 'puppeteer-core';
const V = 'http://localhost:4173';
const b = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new',
  args: ['--no-sandbox'],
});
const p = await b.newPage();
const errs = [];
p.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
await p.setViewport({ width: 1600, height: 1100 });
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const API = process.env.TICVAI_API ?? 'http://localhost:8787';
await p.goto(`${V}/invite.html`, { waitUntil: 'domcontentloaded' });
await p.evaluate((a) => localStorage.setItem('ticvai-api', a), API);
const ok = await p.evaluate(
  async (a, e, pw) =>
    (await fetch(`${a}/api/auth/login`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: e, password: pw }),
    })).ok,
  API,
  process.env.TICVAI_USER ?? 'chinmay.parab@softlabsgroup.com',
  process.env.TICVAI_PASS ?? 'the-first-administrator'
);
if (!ok) console.log('note: not signed in — the tree may not render');

await p.goto(V, { waitUntil: 'domcontentloaded' });
await p.waitForSelector('#layers button', { timeout: 30000 });
await wait(4500);
await p.evaluate(() => document.querySelector('#layers button[data-layer="backend"]').click());
await wait(3000);

const options = await p.evaluate(() =>
  [...document.querySelectorAll('#data-scope option')].map((o) => o.value)
);
console.log(`scope picker: ${options.length} options · ai present = ${options.includes('ai')}`);
for (const want of ['ai', 'approvals', 'workforce']) {
  if (!options.includes(want)) console.log(`  MISSING ${want}`);
}

// click the AI table the screenshot had selected
const clicked = await p.evaluate(() => {
  const row = [...document.querySelectorAll('.tree-file')].find(
    (r) => r.dataset.id === 'table:ai.conversation'
  );
  if (!row) return false;
  row.click();
  return true;
});
console.log(`clicked ai.conversation: ${clicked}`);
await wait(3500);

// The entity view draws to a canvas, so there is nothing in the DOM to read
// back — the scope the renderer settled on and the hint it wrote are the two
// honest witnesses that the click landed where it was sent.
const after = await p.evaluate(() => ({
  scope: document.getElementById('data-scope')?.value,
  hint: document.getElementById('data-hint')?.textContent ?? '',
  canvas: Boolean(document.getElementById('data-canvas')),
}));
console.log(`scope after click: ${after.scope}${after.scope === 'ai' ? '' : '   ← FELL BACK'}`);
console.log(`hint: ${after.hint}`);
if (after.scope !== 'ai') console.log('FAIL: the click did not open the ai schema');
else if (!/^13 tables/.test(after.hint)) console.log('FAIL: ai opened but drew no tables');

console.log('\nerrors:', errs.length ? errs.slice(0, 5) : 'none');
await b.close();
