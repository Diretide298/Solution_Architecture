/**
 * People and projects (admin.html): it opens on what needs an administrator,
 * and nothing on it that cannot be taken back happens on one press.
 *
 * The bugs this holds shut were all one-press: Disable signed somebody out of
 * every browser with no question asked, the role picker applied on change (so
 * arrowing through it moved somebody through every role), the platform "×"
 * took a grant back with no name on the button, and withdrawing an invite
 * killed the link at once. Each now opens a confirm under the row that names
 * the person, and Cancel leaves everything as it was. So most of what is below
 * is pressing the first button, reading the sentence, pressing Cancel, and
 * asking the service whether anything changed.
 *
 * Also: the old addresses the reviews and changes pages link at still land on
 * the right register, every field has a label, and an existing account can be
 * given another project from the page.
 *
 * **Writes accounts and invites**, so it refuses to run unless `TICVAI_DB`
 * points at a scratch copy (it does not open it; the guard is the point).
 *
 *   TICVAI_VIEWER=http://localhost:4205 TICVAI_API=http://localhost:8805 \
 *     TICVAI_DB=…/scratch.db node checks/admin-page-check.mjs
 */
import puppeteer from 'puppeteer-core';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { VIEWER, API } from './_session.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REAL_DB = path.join(HERE, '..', 'api', 'ticvai.db');
const DB = process.env.TICVAI_DB ?? REAL_DB;
if (path.resolve(DB) === path.resolve(REAL_DB)) {
  console.error('admin-page-check writes accounts, so it refuses to run against api/ticvai.db.');
  console.error('Point TICVAI_DB at the scratch copy the accounts service is using.');
  process.exit(2);
}

const BASE = VIEWER.replace(/\/+$/, '');
const APIB = API.replace(/\/+$/, '');
const PASSWORD = 'a-long-enough-passphrase';
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push(e.message));
await page.setViewport({ width: 1500, height: 1000 });
await page.goto(`${BASE}/invite.html`, { waitUntil: 'domcontentloaded' });
// The pages find the accounts service through this key when it is not on the
// default port, as it is not for a scratch run.
await page.evaluate((a) => localStorage.setItem('ticvai-api', a), APIB);
const signed = await page.evaluate(async (a, password) => (await fetch(`${a}/api/auth/login`, {
  method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password }),
})).status, APIB, PASSWORD);
check('the harness administrator signs in', signed === 200, String(signed));

/** The service's own answer, from the page's session. */
const api = (method, p, body) => page.evaluate(async (a, m, q, b) => {
  const r = await fetch(`${a}${q}`, {
    method: m, credentials: 'include',
    headers: b === undefined ? {} : { 'content-type': 'application/json' },
    body: b === undefined ? undefined : JSON.stringify(b),
  });
  let data = null; try { data = await r.json(); } catch {}
  return { status: r.status, data };
}, APIB, method, p, body);

// A person to act on, made fresh so a rerun does not trip over the last one.
const stamp = Date.now() % 1_000_000;
const handle = `admin.page${stamp}`;
const made = await api('POST', '/api/invites', { email: `${handle}@softlabsgroup.com`, role: 'dev', project_id: 'ticvai' });
const redeemed = await fetch(`${APIB}/api/auth/redeem`, {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ token: made.data?.link?.split('#')[1], password: PASSWORD, name: `Admin Page ${stamp}` }),
});
check('a developer to act on is invited and signs up', redeemed.status === 200, String(redeemed.status));
const findThem = async () => (await api('GET', '/api/accounts')).data?.accounts?.find((a) => a.email === `${handle}@softlabsgroup.com`);
const them = await findThem();

const open = async (hash) => {
  await page.goto(`${BASE}/admin.html${hash}`, { waitUntil: 'networkidle2' });
  await wait(1500);
};
/** The row of the person made above, in the accounts table. */
const theirRow = `#accounts tr.account-row:has(a[href*="${encodeURIComponent(`Admin Page ${stamp}`)}"])`;

// ── it opens on what needs you ───────────────────────────────────────
await open('');
const opening = await page.evaluate(() => ({
  title: document.title,
  h1: document.querySelector('h1.set-nav-title')?.textContent,
  shown: [...document.querySelectorAll('.set-section')].filter((s) => !s.hidden).map((s) => s.id),
  headline: document.querySelector('#ad-headline')?.textContent,
  current: document.querySelector('.set-nav a[aria-current="true"]')?.getAttribute('href'),
}));
check('the page is called People and projects', opening.title === 'ADAM — People and projects'
  && opening.h1 === 'People and projects', `${opening.title} / ${opening.h1}`);
check('it opens on Needs you, one section at a time',
  JSON.stringify(opening.shown) === '["attention"]' && opening.current === '#attention', JSON.stringify(opening));
check('which answers in a sentence', /need(s)? you\.$/.test(opening.headline ?? ''), opening.headline);

// ── old addresses ────────────────────────────────────────────────────
await open('#settle-from-sheet');
const settle = await page.evaluate(() => ({
  hash: location.hash, search: location.search,
  pressed: document.querySelector('#upload button[aria-pressed="true"]')?.dataset.register,
  showing: !document.querySelector('#settle-from-sheet').hidden && document.querySelector('#close-from-sheet').hidden,
}));
check('the changes page\'s old link lands on the upload with change requests picked',
  settle.hash === '#upload' && settle.pressed === 'changes' && settle.showing, JSON.stringify(settle));
await open('#close-from-sheet');
check('and the reviews page\'s on review items',
  await page.evaluate(() => location.hash === '#upload'
    && document.querySelector('#upload button[aria-pressed="true"]')?.dataset.register === 'verdicts'));

// ── every field has a label ──────────────────────────────────────────
await open('#people');
const unlabelled = await page.evaluate(() => [...document.querySelectorAll('#admin input, #admin select')]
  .filter((n) => n.type !== 'hidden' && !n.labels?.length && !n.getAttribute('aria-label') && !n.getAttribute('aria-labelledby'))
  .map((n) => n.id || n.className));
check('every input and select on the page has a label', unlabelled.length === 0, unlabelled.join(', '));

// ── the role asks, names both roles, and Cancel puts it back ─────────
await page.evaluate((sel) => {
  const s = document.querySelector(`${sel} select.ad-role`);
  s.value = 'lead';
  s.dispatchEvent(new Event('change'));
}, theirRow);
await wait(300);
const asked = await page.evaluate(() => document.querySelector('#accounts .sh-confirm')?.textContent ?? '');
check('changing a role asks first, naming the person and both roles',
  asked.includes(`Admin Page`) && asked.includes('Developer') && asked.includes('Team Lead'), asked);
await page.evaluate(() => [...document.querySelectorAll('#accounts .sh-confirm button')].find((b) => b.textContent === 'Cancel').click());
await wait(400);
check('and Cancel leaves the role where it was, on the page and in the service',
  (await page.evaluate((sel) => document.querySelector(`${sel} select.ad-role`).value, theirRow)) === 'dev'
  && (await findThem()).role === 'dev');

await page.evaluate((sel) => {
  const s = document.querySelector(`${sel} select.ad-role`);
  s.value = 'lead';
  s.dispatchEvent(new Event('change'));
}, theirRow);
await wait(300);
await page.evaluate(() => [...document.querySelectorAll('#accounts .sh-confirm button')].find((b) => b.textContent.startsWith('Make them')).click());
await wait(1200);
check('the second press changes it', (await findThem()).role === 'lead', (await findThem()).role);

// ── Disable asks, because it signs them out everywhere ───────────────
const disableButton = async () => page.evaluate((sel) =>
  [...document.querySelectorAll(`${sel} button`)].find((b) => b.textContent === 'Disable')?.click() ?? 'missing', theirRow);
await disableButton();
await wait(300);
const disableAsk = await page.evaluate(() => document.querySelector('#accounts .sh-confirm')?.textContent ?? '');
check('Disable asks first and says they are signed out of every browser',
  /signed out of every browser/.test(disableAsk) && disableAsk.includes('Admin Page'), disableAsk);
check('and nothing has happened yet', (await findThem()).active === 1);
await page.evaluate(() => [...document.querySelectorAll('#accounts .sh-confirm button')].find((b) => b.textContent === 'Cancel').click());
await wait(300);
check('Cancel keeps the account', (await findThem()).active === 1);

// ── another project, from the page ───────────────────────────────────
const projects = (await api('GET', '/api/pms/projects')).data?.projects ?? [];
const other = projects.find((p) => p.active && !them.projects?.some((h) => h.id === p.id));
if (other) {
  await page.evaluate((sel) => document.querySelector(`${sel} .ad-add`).click(), theirRow);
  await wait(300);
  await page.evaluate((id) => {
    const s = document.querySelector('#accounts tr.ad-detail select');
    s.value = id;
    [...document.querySelectorAll('#accounts tr.ad-detail button')].find((b) => b.textContent === 'Give it').click();
  }, other.id);
  await wait(1200);
  check('an existing account is given another project from the page',
    (await findThem()).projects?.some((p) => p.id === other.id), JSON.stringify((await findThem()).projects));
  const dropLabel = await page.evaluate((sel, name) => [...document.querySelectorAll(`${sel} .ad-chip-drop`)]
    .map((b) => b.getAttribute('aria-label')).find((l) => l.includes(name)), theirRow, other.name);
  check('and its remove button says what it takes from whom', /^Take .+ away from Admin Page/.test(dropLabel ?? ''), dropLabel);
  await page.evaluate((sel, name) => [...document.querySelectorAll(`${sel} .ad-chip-drop`)]
    .find((b) => b.getAttribute('aria-label').includes(name)).click(), theirRow, other.name);
  await wait(300);
  check('taking it away asks first', (await findThem()).projects?.some((p) => p.id === other.id)
    && /stop being able to open it/.test(await page.evaluate(() => document.querySelector('#accounts .sh-confirm')?.textContent ?? '')));
  await page.evaluate(() => [...document.querySelectorAll('#accounts .sh-confirm button')].find((b) => b.textContent.startsWith('Take')).click());
  await wait(1200);
  check('and the second press takes it', !(await findThem()).projects?.some((p) => p.id === other.id));
} else {
  check('there is a second project to give (register one in projects.json)', false);
}

// ── invites: every role the service takes, and Withdraw asks ─────────
await open('#invites');
const roles = await page.evaluate(() => [...document.querySelectorAll('#invite-role option')].map((o) => o.value));
check('the invite offers every role the service accepts from here',
  JSON.stringify(roles) === JSON.stringify(['reviewer', 'dev', 'lead', 'pm', 'admin', 'client']), roles.join(' '));
await page.type('#invite-email', `withdraw.me${stamp}@softlabsgroup.com`);
await page.evaluate(() => { document.querySelector('#invite-role').value = 'pm'; document.querySelector('#invite-role').dispatchEvent(new Event('change')); });
await page.evaluate(() => document.querySelector('#invite-create').click());
await wait(1500);
const link = await page.evaluate(() => !document.querySelector('#invite-result').hidden && document.querySelector('#invite-link').value);
check('a project manager is invited from the page', /\/invite\.html#/.test(link || ''), String(link).replace(/#.*/, '#…'));
const states = await page.evaluate(() => [...document.querySelectorAll('#invites-list .sh-badge')].map((b) => b.textContent));
check('invite states are words in sentence case', states.length > 0 && states.every((s) => /^[A-Z][a-z]+$/.test(s)), [...new Set(states)].join(' '));
await page.evaluate((addr) => [...document.querySelectorAll('#invites-list tr')]
  .find((tr) => tr.textContent.includes(addr))?.querySelector('button')?.click(), `withdraw.me${stamp}@`);
await wait(300);
const stillOpen = async () => (await api('GET', '/api/invites')).data?.invites
  ?.find((i) => i.email === `withdraw.me${stamp}@softlabsgroup.com`)?.state;
check('Withdraw asks first', (await stillOpen()) === 'open'
  && /link stops working/.test(await page.evaluate(() => document.querySelector('#invites-list .sh-confirm')?.textContent ?? '')));
await page.evaluate(() => [...document.querySelectorAll('#invites-list .sh-confirm button')].find((b) => b.textContent === 'Withdraw it').click());
await wait(1200);
check('and the second press withdraws it', (await stillOpen()) === 'revoked', await stillOpen());

// ── tidy up: the person made above is disabled, through the page ─────
await open('#people');
await disableButton();
await wait(300);
await page.evaluate(() => [...document.querySelectorAll('#accounts .sh-confirm button')].find((b) => b.textContent.startsWith('Disable')).click());
await wait(1200);
check('Disable, confirmed, disables', (await findThem()).active === 0);

check('no page errors', errors.length === 0, errors.slice(0, 3).join(' | '));
await browser.close();
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
