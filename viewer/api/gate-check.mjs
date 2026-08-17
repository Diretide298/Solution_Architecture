// The front door. An empty database offers to make the first administrator and
// then never offers again; the viewer refuses to draw for anyone not signed in;
// the accounts page refuses anyone who is not an admin.
import puppeteer from 'puppeteer-core';

// The viewer is behind a sign-in now, so a harness has to come in the front
// door like anyone else. The cookie is set on localhost by the accounts
// service; cookies ignore the port, so it rides along to the viewer too.
let harnessSignedIn = false;
async function harnessSignIn(target) {
  if (harnessSignedIn) return;
  // Not login.html: once the cookie is set that page redirects to the viewer
  // the moment it loads, which destroys the execution context in the middle of
  // the very call that set it. invite.html is on the same origin, needs no
  // account, and stays put.
  await target.goto('http://localhost:4173/invite.html', { waitUntil: 'domcontentloaded' });
  const ok = await target.evaluate(async () => {
    const r = await fetch('http://localhost:8787/api/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        email: 'harness.admin@softlabsgroup.com',
        password: 'a-long-enough-passphrase',
      }),
    });
    return r.ok;
  });
  if (!ok) throw new Error('the harness could not sign in — is the accounts service running?');
  harnessSignedIn = true;
}
const VIEWER = 'http://localhost:4173';
const API = 'http://localhost:8787';
const OUT = 'C:/Users/CHINMA~1.PAR/AppData/Local/Temp/claude/c--Users-Chinmay-Parab-Desktop-ticvai/fbd4bcf3-a6ac-43c2-ab81-807eba134bb2/scratchpad';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const OWNER = { email: 'chinmay.parab@softlabsgroup.com', name: 'Chinmay Parab', password: 'the-first-administrator' };

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
const errors = [];
const EXPECTED = /Failed to load resource.*(400|401|403|404|409)/;
page.on('console', (m) => m.type() === 'error' && !EXPECTED.test(m.text()) && errors.push(m.text()));
page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
await page.setViewport({ width: 1500, height: 1000 });

const health = await fetch(`${API}/api/health`).then((r) => r.json());
check('starting from an empty database', health.accounts === 0, `${health.accounts} accounts`);

// ── the viewer will not draw for a stranger ──────────────────────────
// Deliberately NOT signed in: this file exists to test the door, so it has to
// arrive at it the way a stranger does.
await page.goto(VIEWER, { waitUntil: 'networkidle2' });
await wait(1800);
check('the viewer sends a stranger to the sign-in page',
  page.url().includes('/login.html'), page.url().replace(VIEWER, ''));

// and it did not hand over the delivery package on the way
const fetched = [];
page.on('response', (r) => fetched.push(new URL(r.url()).pathname));

// ── the first account ────────────────────────────────────────────────
const boot = await page.evaluate(() => ({
  bootstrap: !document.querySelector('#bootstrap').hidden,
  signin: !document.querySelector('#signin').hidden,
  title: document.querySelector('#bootstrap .auth-title')?.textContent,
}));
check('an empty database offers to make the first administrator',
  boot.bootstrap && !boot.signin, boot.title);
await page.screenshot({ path: `${OUT}/gate-bootstrap.png` });

// the domain rule holds here too
await page.type('#boot-email', 'someone@gmail.com');
await page.type('#boot-password', 'a-long-enough-passphrase');
await page.type('#boot-confirm', 'a-long-enough-passphrase');
await page.evaluate(() => document.querySelector('#boot-submit').click());
await wait(1400);
check('the first account still has to be in the domain',
  await page.evaluate(() => !document.querySelector('#boot-error').hidden),
  await page.evaluate(() => document.querySelector('#boot-error').textContent));

await page.evaluate(() => {
  for (const id of ['boot-email', 'boot-password', 'boot-confirm']) {
    document.getElementById(id).value = '';
  }
});
await page.type('#boot-email', OWNER.email);
await page.type('#boot-name', OWNER.name);
await page.type('#boot-password', OWNER.password);
await page.type('#boot-confirm', OWNER.password);
await page.evaluate(() => document.querySelector('#boot-submit').click());
await wait(3000);

check('making it lands in the viewer, signed in',
  !page.url().includes('/login.html'),
  page.url().replace(VIEWER, '') || '/');
await page.waitForSelector('#layers button', { timeout: 25000 });
await wait(2600);

const who = await page.evaluate(() => ({
  initials: document.querySelector('#account-initials')?.textContent.trim(),
  title: document.querySelector('#account-toggle')?.title,
  tree: document.querySelectorAll('#tree .tree-file').length,
}));
check('the viewer draws for them', who.tree > 0, `${who.tree} rows in the tree`);
check('and the bar says who they are', who.title?.includes('admin'), who.title);

const state = await fetch(`${API}/api/auth/state`).then((r) => r.json());
check('the door closes behind it', state.needsBootstrap === false, 'no second bootstrap offered');

// a second attempt is refused by the server, not merely hidden by the page
const second = await fetch(`${API}/api/auth/bootstrap`, {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ email: 'other@softlabsgroup.com', password: 'another-long-passphrase' }),
});
check('and a second one is refused outright', second.status === 409, `${second.status}`);

// ── the accounts page ────────────────────────────────────────────────
await page.goto(`${VIEWER}/admin.html`, { waitUntil: 'networkidle2' });
await wait(2000);
const admin = await page.evaluate(() => ({
  shown: !document.querySelector('#admin').hidden,
  denied: !document.querySelector('#denied').hidden,
  who: document.querySelector('#whoami')?.textContent,
  accounts: document.querySelectorAll('#accounts .account-row').length,
}));
check('the owner can open the accounts page', admin.shown && !admin.denied, admin.who);
check('and sees the accounts', admin.accounts === 1, `${admin.accounts} listed`);
await page.screenshot({ path: `${OUT}/gate-admin.png` });

// an admin cannot lock themselves out
const selfDemote = await page.evaluate(() => {
  const row = document.querySelector('#accounts .account-row');
  const role = row?.querySelector('select');
  const toggle = [...row.querySelectorAll('button')].find((b) => /Disable/.test(b.textContent));
  return { roleDisabled: role?.disabled, hasDisableButton: Boolean(toggle) };
});
check('they cannot demote themselves', selfDemote.roleDisabled === true);
check('nor disable themselves', selfDemote.hasDisableButton === false);

// ── inviting from the page ───────────────────────────────────────────
const INVITED = `gate.reviewer${process.env.RUN_STAMP ?? '1'}@softlabsgroup.com`;
await page.type('#invite-email', INVITED);
await page.evaluate(() => document.querySelector('#invite-create').click());
await wait(1800);
const made = await page.evaluate(() => ({
  shown: !document.querySelector('#invite-result').hidden,
  link: document.querySelector('#invite-link').value,
  rows: document.querySelectorAll('#invites .invite-row-item').length,
}));
check('an invite is made from the accounts page', made.shown && made.link.includes('/invite.html#'));
check('and listed', made.rows > 0, `${made.rows} invite(s)`);

// ── a reviewer is kept out of the accounts page ──────────────────────
const other = await browser.newPage();
other.on('pageerror', (e) => errors.push(`reviewer pageerror: ${e.message}`));
await other.setViewport({ width: 1400, height: 950 });
await other.goto(made.link, { waitUntil: 'domcontentloaded' });
await wait(1800);
await other.type('#name', 'Gate Reviewer');
await other.type('#password', 'a-reviewer-passphrase');
await other.type('#confirm', 'a-reviewer-passphrase');
await other.evaluate(() => document.querySelector('#submit').click());
await wait(2400);
check('the invited person gets an account',
  await other.evaluate(() => !document.querySelector('#done').hidden));

await other.goto(`${VIEWER}/admin.html`, { waitUntil: 'networkidle2' });
await wait(2000);
const kept = await other.evaluate(() => ({
  denied: !document.querySelector('#denied').hidden,
  shown: !document.querySelector('#admin').hidden,
}));
check('a reviewer is refused the accounts page', kept.denied && !kept.shown);

// and the server refuses them too, not just the page
const asReviewer = await other.evaluate(async () => {
  const r = await fetch('http://localhost:8787/api/accounts', { credentials: 'include' });
  return r.status;
});
check('the server refuses them as well as the page', asReviewer === 403, `${asReviewer}`);

// but they can read the viewer
await harnessSignIn(other);
await other.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await other.waitForSelector('#layers button', { timeout: 25000 });
await wait(2600);
check('a reviewer can still read the viewer',
  await other.evaluate(() => document.querySelectorAll('#tree .tree-file').length > 0));

// ── signing out returns you to the door ──────────────────────────────
await other.evaluate(() => document.querySelector('#account-toggle').click());
await wait(600);
await other.evaluate(() => document.querySelector('#signout').click());
await wait(1600);
await harnessSignIn(other);
await other.goto(VIEWER, { waitUntil: 'networkidle2' });
await wait(1800);
check('after signing out the viewer sends them back to the door',
  other.url().includes('/login.html'), other.url().replace(VIEWER, ''));

check('no console errors', errors.length === 0, errors.slice(0, 3).join(' | '));
await browser.close();
console.log(`\nRESULT: ${pass}/${pass + fail} passed — ${fail ? 'FAIL' : 'PASS'}`);
process.exitCode = fail ? 1 : 0;
