// The whole path a person actually walks: an admin signs in, invites someone,
// that person opens the link and sets a password, then records a verdict on an
// artefact and sees it stick. Driven through the browser, not the API, because
// that is where the wiring can be wrong.
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

// a fresh reviewer each run, so the harness can be run twice
const stamp = Math.floor(Number(process.env.RUN_STAMP ?? '1000'));
const REVIEWER = `ui.reviewer${stamp}@softlabsgroup.com`;
const ADMIN = { email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' };

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
const errors = [];
const EXPECTED = /Failed to load resource.*(400|401|403|404|409)/;
const note = (text) => { if (!EXPECTED.test(text)) errors.push(text); };
page.on('console', (m) => m.type() === 'error' && note(m.text()));
page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
await page.setViewport({ width: 1600, height: 1000 });

const boot = async (url = VIEWER) => {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  if (url === VIEWER) await page.waitForSelector('#layers button', { timeout: 25000 });
  await wait(2600);
};

// The viewer is behind the door now, so this starts at the door. What happens
// to a stranger who arrives is gate-check's subject, not this one's; this
// follows a person who has been let in.
await page.goto(`${VIEWER}/login.html`, { waitUntil: 'domcontentloaded' });
await wait(1600);

check('the door is the landing page',
  await page.evaluate(() => !document.querySelector('#signin').hidden ||
                            !document.querySelector('#bootstrap').hidden),
  'sign-in offered');

await page.type('#email', ADMIN.email);
await page.type('#password', 'wrong-but-long-enough');
await page.evaluate(() => document.querySelector('#submit').click());
await wait(1400);
check('a wrong password is refused at the door',
  await page.evaluate(() => !document.querySelector('#error').hidden),
  await page.evaluate(() => document.querySelector('#error').textContent));

await page.evaluate(() => { document.querySelector('#password').value = ''; });
await page.type('#password', ADMIN.password);
await page.evaluate(() => document.querySelector('#submit').click());
await wait(3000);

check('signing in lands in the viewer', !page.url().includes('/login.html'),
  page.url().replace(VIEWER, '') || '/');
await page.waitForSelector('#layers button', { timeout: 25000 });
await wait(2600);
check('which now draws',
  await page.evaluate(() => document.querySelectorAll('#tree .tree-file').length > 0));

await page.evaluate(() => document.querySelector('#tree .tree-file').click());
await wait(900);
await page.evaluate(() => {
  document.querySelector('#tree .tree-children .tree-child, #tree .tree-children .tree-file')?.click();
});
await wait(1600);
const anon = await page.evaluate(() => {
  const box = document.querySelector('#reader-validation .verdict-box');
  return { present: Boolean(box), chip: box?.querySelector('.verdict-chip')?.textContent };
});
check('an operation shows its validation state', anon.present, anon.chip);

// ── the account panel ───────────────────────────────────
const initials = await page.evaluate(() => document.querySelector('#account-initials').textContent.trim());
check('the topbar shows who is signed in', initials !== '·' && initials.length >= 1, initials);

await page.evaluate(() => document.querySelector('#account-toggle').click());
await wait(700);
check('the account panel opens',
  await page.evaluate(() => !document.querySelector('#account-panel').hidden));
check('an admin is pointed at the accounts page',
  await page.evaluate(() => !document.querySelector('#account-admin').hidden));

// ── inviting, from the accounts page ─────────────────────────
await page.goto(`${VIEWER}/admin.html`, { waitUntil: 'networkidle2' });
await wait(2200);
check('the accounts page opens for an admin',
  await page.evaluate(() => !document.querySelector('#admin').hidden));

await page.type('#invite-email', 'someone@gmail.com');
await page.evaluate(() => document.querySelector('#invite-create').click());
await wait(1400);
const outside = await page.evaluate(() => ({
  shown: !document.querySelector('#invite-error').hidden,
  text: document.querySelector('#invite-error').textContent,
}));
check('an address outside the domain is refused in the UI', outside.shown, outside.text);

await page.evaluate(() => { document.querySelector('#invite-email').value = ''; });
await page.type('#invite-email', REVIEWER);
await page.evaluate(() => document.querySelector('#invite-create').click());
await wait(1600);

const made = await page.evaluate(() => ({
  shown: !document.querySelector('#invite-result').hidden,
  link: document.querySelector('#invite-link').value,
  listed: document.querySelectorAll('#invites .invite-row-item').length,
}));
check('an invite is made and its link shown once', made.shown && made.link.includes('/invite.html#'),
  made.link.replace(/#.*/, '#…'));
check('and it appears in the list of invites', made.listed > 0, `${made.listed} listed`);
await page.screenshot({ path: `${OUT}/auth-invite.png` });

// ── the invited person opens the link ────────────────────────────────
const invitePage = await browser.newPage();
await invitePage.setViewport({ width: 1000, height: 900 });
invitePage.on('pageerror', (e) => errors.push(`invite pageerror: ${e.message}`));
await invitePage.goto(made.link, { waitUntil: 'domcontentloaded' });
await wait(1800);

const greeting = await invitePage.evaluate(() => ({
  formShown: !document.querySelector('#form').hidden,
  email: document.querySelector('#invite-email')?.textContent,
  role: document.querySelector('#invite-role')?.textContent,
}));
check('the invite page names who it is for, before any password is set',
  greeting.formShown && greeting.email === REVIEWER, `${greeting.email} as ${greeting.role}`);

// mismatched passwords are caught before anything is sent
await invitePage.type('#name', 'Ui Reviewer');
await invitePage.type('#password', 'a-perfectly-good-passphrase');
await invitePage.type('#confirm', 'a-different-passphrase');
await invitePage.evaluate(() => document.querySelector('#submit').click());
await wait(800);
check('two different passwords are refused',
  await invitePage.evaluate(() => !document.querySelector('#error').hidden),
  await invitePage.evaluate(() => document.querySelector('#error').textContent));

await invitePage.evaluate(() => { document.querySelector('#confirm').value = ''; });
await invitePage.type('#confirm', 'a-perfectly-good-passphrase');
await invitePage.evaluate(() => document.querySelector('#submit').click());
await wait(2200);

check('the account is created and signed in',
  await invitePage.evaluate(() => !document.querySelector('#done').hidden),
  await invitePage.evaluate(() => document.querySelector('#done-email')?.textContent));
await invitePage.screenshot({ path: `${OUT}/auth-invited.png` });

// the same link a second time is refused. goto() to a URL that differs only
// by fragment does not navigate, so this has to be a real reload.
await invitePage.reload({ waitUntil: 'domcontentloaded' });
await wait(1900);
check('opening the same link again is refused',
  await invitePage.evaluate(() => !document.querySelector('#refused').hidden),
  await invitePage.evaluate(() => document.querySelector('#refused-why')?.textContent));

// ── that person records a verdict ────────────────────────────────────
const reviewerPage = await browser.newPage();
await reviewerPage.setViewport({ width: 1600, height: 1000 });
reviewerPage.on('pageerror', (e) => errors.push(`reviewer pageerror: ${e.message}`));
await reviewerPage.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await reviewerPage.waitForSelector('#layers button', { timeout: 25000 });
await wait(2800);

check('the invited person arrives already signed in',
  await reviewerPage.evaluate(() => document.querySelector('#account-initials').textContent.trim() !== '·'),
  await reviewerPage.evaluate(() => document.querySelector('#account-toggle').title));

// open an operation
await reviewerPage.evaluate(() => document.querySelector('#tree .tree-file').click());
await wait(900);
await reviewerPage.evaluate(() => {
  document.querySelector('#tree .tree-children .tree-child, #tree .tree-children .tree-file')?.click();
});
await wait(1600);

const canRecord = await reviewerPage.evaluate(() =>
  document.querySelectorAll('#reader-validation .verdict-set').length);
check('a signed-in reviewer is offered the verdicts', canRecord === 3, `${canRecord} buttons`);

await reviewerPage.evaluate(() => {
  document.querySelector('#reader-validation .verdict-note-input').value = '';
});
await reviewerPage.type('#reader-validation .verdict-note-input', 'checked against the workbook');
await reviewerPage.evaluate(() => {
  document.querySelector('#reader-validation .verdict-set.approved').click();
});
await wait(2000);

const recorded = await reviewerPage.evaluate(() => {
  const box = document.querySelector('#reader-validation .verdict-box');
  return {
    chip: box?.querySelector('.verdict-chip')?.textContent,
    by: box?.querySelector('.verdict-by')?.textContent,
    note: box?.querySelector('.verdict-note')?.textContent,
    target: box?.dataset.target,
  };
});
check('the verdict is recorded and shown', recorded.chip === 'Approved', recorded.chip);
check('it says who gave it', /softlabsgroup\.com|Ui Reviewer/.test(recorded.by ?? ''), recorded.by);
check('and why', /workbook/.test(recorded.note ?? ''), recorded.note);
await reviewerPage.screenshot({ path: `${OUT}/auth-verdict.png` });

// it survives a reload, because it is in the store rather than the page
await reviewerPage.reload({ waitUntil: 'domcontentloaded' });
await reviewerPage.waitForSelector('#layers button', { timeout: 25000 });
await wait(2600);
const persisted = await fetch(`${API}/api/validation/operation/${encodeURIComponent(recorded.target)}`)
  .then((r) => r.json());
check('and it is in the store, not just on the page',
  persisted.current?.verdict === 'approved', `${persisted.current?.verdict} by ${persisted.current?.by_email}`);

// ── a reviewer is not an admin ───────────────────────────────────────
await reviewerPage.evaluate(() => document.querySelector('#account-toggle').click());
await wait(700);
check('a reviewer is not pointed at the accounts page',
  await reviewerPage.evaluate(() => document.querySelector('#account-admin').hidden));

await reviewerPage.goto(`${VIEWER}/admin.html`, { waitUntil: 'networkidle2' });
await wait(2000);
check('and the accounts page refuses them',
  await reviewerPage.evaluate(() => !document.querySelector('#denied').hidden));

// ── signing out ──────────────────────────────────────────────────────
// Back to the viewer first: the accounts page has no account panel on it, and
// the reviewer was left there by the check above.
await reviewerPage.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await reviewerPage.waitForSelector('#layers button', { timeout: 25000 });
await wait(2600);
await reviewerPage.evaluate(() => document.querySelector('#account-toggle').click());
await wait(600);
await reviewerPage.evaluate(() => document.querySelector('#signout').click());
await wait(1800);
check('signing out returns the topbar to nobody',
  await reviewerPage.evaluate(() => document.querySelector('#account-initials').textContent.trim() === '·'));

// and the viewer will not draw for them any more
await reviewerPage.goto(VIEWER, { waitUntil: 'networkidle2' });
await wait(1800);
check('and the viewer sends them back to the door',
  reviewerPage.url().includes('/login.html'), reviewerPage.url().replace(VIEWER, ''));

check('no console errors', errors.length === 0, errors.slice(0, 3).join(' | '));
await browser.close();
console.log(`\nRESULT: ${pass}/${pass + fail} passed — ${fail ? 'FAIL' : 'PASS'}`);
process.exitCode = fail ? 1 : 0;
