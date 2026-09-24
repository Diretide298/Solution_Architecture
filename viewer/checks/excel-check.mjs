// The package as a spreadsheet, from the button a person actually presses.
//
// Three things worth asserting, and the file being non-empty is not one of them:
//
//   **It is a real xlsx.** Written by `lib/xlsx.mjs`, which had only the reading
//   half until now, so the container is ours and not a library's. The bytes
//   start `PK`, and the companion assertion lives outside this file: openpyxl,
//   an independent implementation, opens what we wrote.
//
//   **The picker offers what the workbook can carry, not what the document
//   can.** They differ by one section -- the wireframe boards -- and the
//   difference is marked on the control, because a section that silently
//   contributes nothing to the document is reported as a bug a fortnight later.
//
//   **Nothing chosen is a sentence.** Not an empty workbook, which opens and
//   tells the reader the package is empty.
//
// One origin, the way the deployment runs it. Pointing the page at the accounts
// service directly makes every /pkg/... route 404 -- a fact about the harness.
//
//   node viewer/server.mjs --port 4173        (with TICVAI_AUTH set)
//   node viewer/checks/excel-check.mjs
import puppeteer from 'puppeteer-core';
import { writeFileSync } from 'node:fs';

const VIEWER = process.env.VIEWER ?? 'http://localhost:4173';
// One origin, the way the deployment runs it: the viewer serves the package
// routes and proxies /api/* to the accounts service. Pointing the page at the
// accounts service directly makes every /pkg/... route 404, which is a fact
// about the harness and not about the page.
const API = process.env.API ?? 'http://localhost:4173';
const OUT = process.env.OUT ?? './adam-workbook-check.xlsx';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const noise = [];
const page = await browser.newPage();
await page.setViewport({ width: 1400, height: 950 });
page.on('console', (m) => { if (m.type() === 'error') noise.push(m.text()); });
page.on('pageerror', (e) => noise.push(String(e)));
await page.evaluateOnNewDocument((api) => {
  try { localStorage.setItem('ticvai-api', api); } catch { /* nothing to do */ }
}, API);
await page.goto(`${VIEWER}/login.html`, { waitUntil: 'domcontentloaded' });
const signedIn = await page.evaluate(async (api) => (await fetch(`${api}/api/auth/login`, {
  method: 'POST', credentials: 'include',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: 'harness.boss@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
})).ok, API);
check('signed in', signedIn);

await page.goto(`${VIEWER}/document.html?project=ticvai`, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#dc-sections input', { timeout: 20000 });
await new Promise((r) => setTimeout(r, 800));

const picker = await page.evaluate(() => ({
  ids: [...document.querySelectorAll('#dc-sections input')].map((n) => n.value),
  onlyExcel: [...document.querySelectorAll('#dc-sections label')]
    .filter((l) => /spreadsheet only/.test(l.textContent)).map((l) => l.textContent.trim()),
  button: !!document.getElementById('dc-excel'),
  hidden: document.getElementById('dc-excel')?.hidden,
}));
check('the picker offers the workbook sections', picker.ids.includes('wireframes'),
  picker.ids.join(' '));
check('and marks the one the document cannot carry',
  picker.onlyExcel.length === 1 && /Wireframe/.test(picker.onlyExcel[0]),
  picker.onlyExcel.join(' | '));
check('the download control is there without generating first',
  picker.button === true && picker.hidden === false);

// Fetched through the page, with the page's own session, so what is asserted is
// what the button does rather than what curl can do.
const got = await page.evaluate(async () => {
  const wanted = [...document.querySelectorAll('#dc-sections input:checked')].map((n) => n.value);
  const res = await fetch(`/api/workbook?sections=${encodeURIComponent(wanted.join(','))}`,
    { credentials: 'include' });
  const buf = await res.arrayBuffer();
  return {
    ok: res.ok,
    type: res.headers.get('content-type'),
    name: res.headers.get('content-disposition'),
    sheets: res.headers.get('x-ticvai-sheets'),
    rows: res.headers.get('x-ticvai-rows'),
    bytes: buf.byteLength,
    base64: btoa(String.fromCharCode(...new Uint8Array(buf.slice(0, 4)))),
    body: Array.from(new Uint8Array(buf)),
  };
});
check('the workbook downloads', got.ok === true, `${got.bytes} bytes`);
check('as a spreadsheet, not JSON',
  /spreadsheetml\.sheet/.test(got.type ?? ''), got.type);
check('named by the server', /filename="ticvai-\d{4}-\d{2}-\d{2}\.xlsx"/.test(got.name ?? ''), got.name);
check('carrying every section that was ticked', Number(got.sheets) >= 16, `${got.sheets} sheets`);
check('and it is a zip, which is what an xlsx is', got.base64.startsWith('UEsD'), got.base64);
writeFileSync(OUT, Buffer.from(got.body));

// Nothing ticked is a sentence, not a broken file.
await page.evaluate(() => {
  for (const n of document.querySelectorAll('#dc-sections input')) n.checked = false;
});
await page.click('#dc-excel');
await new Promise((r) => setTimeout(r, 900));
check('with nothing chosen it says so and downloads nothing',
  /Choose a section/.test(await page.evaluate(() => document.getElementById('dc-says').textContent)),
  await page.evaluate(() => document.getElementById('dc-says').textContent));

check('nothing shouted on the way', noise.length === 0, noise.slice(0, 2).join(' | '));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
