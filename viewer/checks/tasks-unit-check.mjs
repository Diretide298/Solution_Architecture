// The Count switch, in a browser: Tasks and Tickets each leave no number on
// the page counted in the other unit, the switch asks the service for nothing,
// and it lands in the address and in the reader's storage.
//
//   TICVAI_VIEWER=http://localhost:4822 node checks/tasks-unit-check.mjs ["Person Name"]
//
// Against a viewer whose accounts service has harness.admin@softlabsgroup.com
// and an OpenProject connection (the stand-in with FAKE_TEAM=1 FAKE_BULK=8000).
//
// Every section is read, shown or not (the rail shows one at a time), minus
// the parts marked data-unit-fixed: the testing gate, which is ten *tickets*
// closed through ADAM in either view, and the plan's sizing line ("6 tasks a
// day is about 19.8 points"), which is the plan's rule rather than a count.
import puppeteer from 'puppeteer-core';
const V = process.env.TICVAI_VIEWER ?? 'http://localhost:4173';
const person = process.argv[2] ?? '';
let ok = 0, bad = 0;
const check = (n, c, d = '') => { console.log(`${c ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); c ? ok++ : bad++; };

const b = await puppeteer.launch({ executablePath: process.env.CHROME ?? 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--no-sandbox'] });
const p = await b.newPage();
await p.setViewport({ width: 1440, height: 1000 });
const errors = [];
p.on('pageerror', (e) => errors.push(String(e)));
await p.goto(`${V}/invite.html`, { waitUntil: 'domcontentloaded' });
await p.evaluate((a) => { localStorage.setItem('ticvai-api', a); localStorage.removeItem('adam-tasks-count'); }, V);
await p.evaluate(async (a) => fetch(`${a}/api/auth/login`, { method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }) }), V);
await p.goto(`${V}/tasks.html${person ? `?person=${encodeURIComponent(person)}` : ''}`, { waitUntil: 'domcontentloaded' });
await p.waitForFunction(() => /\d/.test(document.getElementById('tk-lede')?.textContent ?? ''), { timeout: 120000 });
await new Promise((r) => setTimeout(r, 800));

/** Every text on the page body, one text node per word gap, minus the fixed parts. */
const read = () => p.evaluate(() => {
  const root = document.getElementById('tasks').cloneNode(true);
  for (const fixed of root.querySelectorAll('[data-unit-fixed]')) fixed.remove();
  const parts = [];
  const walk = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  while (walk.nextNode()) parts.push(walk.currentNode.nodeValue);
  return parts.join(' ').replace(/\s+/g, ' ');
});
// A number followed (perhaps after "open"/"more") by the unit, lower case:
// type names are capitalised ("Task"), units in sentences are not.
const countsIn = (text, word) => [...text.matchAll(new RegExp(`\\d[\\d,.]*\\s+(?:open\\s+|more\\s+)?${word}s?\\b`, 'g'))].map((m) => m[0]);
const headline = () => p.$eval('#tk-sprint-title', (e) => e.textContent);

const asked = [];
p.on('request', (r) => { if (/\/api\//.test(r.url())) asked.push(r.url()); });

let text = await read();
const tasksHead = await headline();
check(`${person || 'team'}: the page opens counting tasks`, (await p.$eval('[data-unit="tasks"]', (e) => e.getAttribute('aria-pressed'))) === 'true');
check('in Tasks, no number is a ticket count', countsIn(text, 'ticket').length === 0, countsIn(text, 'ticket').slice(0, 5).join(' | '));
check('and numbers are labelled in tasks', countsIn(text, 'task').length > 10, `${countsIn(text, 'task').length} labelled`);
check('the daily table says tasks a day', /Tasks per working day/.test(text));

asked.length = 0;
const t0 = Date.now();
await p.click('[data-unit="tickets"]');
await p.waitForFunction(() => document.querySelector('[data-unit="tickets"]').getAttribute('aria-pressed') === 'true');
const took = Date.now() - t0;
text = await read();
const ticketsHead = await headline();
check('in Tickets, no number is a task count', countsIn(text, 'task').length === 0, countsIn(text, 'task').slice(0, 5).join(' | '));
check('and numbers are labelled in tickets', countsIn(text, 'ticket').length > 10, `${countsIn(text, 'ticket').length} labelled`);
check('the daily table says tickets a day', /Tickets per working day/.test(text));
check('the sprint verdict changed', tasksHead !== ticketsHead, `${tasksHead} → ${ticketsHead}`);
check('switching asked the service for nothing', asked.length === 0, asked.join(' '));
check('and was quick', took < 3000, `${took} ms`);
const where = await p.evaluate(() => ({ q: location.search, saved: localStorage.getItem('adam-tasks-count') }));
check('the address and the reader\'s storage say tickets', /count=tickets/.test(where.q) && where.saved === 'tickets', JSON.stringify(where));

await p.reload({ waitUntil: 'domcontentloaded' });
await p.waitForFunction(() => /\d/.test(document.getElementById('tk-lede')?.textContent ?? ''), { timeout: 120000 });
check('a reload keeps tickets', (await p.$eval('[data-unit="tickets"]', (e) => e.getAttribute('aria-pressed'))) === 'true');

await p.click('[data-unit="tasks"]');
await new Promise((r) => setTimeout(r, 400));
text = await read();
check('back in Tasks, no number is a ticket count', countsIn(text, 'ticket').length === 0, countsIn(text, 'ticket').slice(0, 5).join(' | '));
check('and the verdict is the tasks one again', (await headline()) === tasksHead);
check('no page errors', errors.length === 0, errors.join(' | '));
console.log(`${ok} passed, ${bad} failed`);
await b.close();
process.exit(bad ? 1 : 0);
