/**
 * The delivery audit draws for an admin and refuses everyone else.
 *
 * **What this is and is not.** `/audit.html` is admin-only in the same sense
 * `/admin.html` is: the viewer only offers it to an admin and the page refuses
 * to draw for anyone else. It is not a security boundary — every figure in its
 * live block comes from `/api/uiux`, `/api/backend` and `/api/journeys`, which
 * any signed-in reader may already call. The gate is there because the page is
 * about how the delivery was *built* rather than about what is in it.
 *
 * So this checks an affordance, and says so. What would go wrong without it is
 * not a leak, it is a reviewer opening a page of internal process notes that
 * reads like a list of things wrong with the work they are reviewing.
 *
 * **Both halves, or neither is worth having.** A gate that refuses everybody
 * passes "a reviewer sees no figures" perfectly, so the admin half is asserted
 * first and the run stops if it fails — otherwise the interesting assertion
 * below it would be measuring a broken page.
 *
 * Makes a reviewer account and removes it again. `TICVAI_DB` must point at a
 * scratch database: the default is `api/ticvai.db`, which is the real one and
 * must never be written to by a harness.
 *
 *   TICVAI_VIEWER=http://127.0.0.1:4620 TICVAI_API=http://127.0.0.1:4620 \
 *     TICVAI_DB=…/scratchpad/harness.db node checks/audit-gate-check.mjs
 */
import puppeteer from 'puppeteer-core';
import { DatabaseSync } from 'node:sqlite';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { authed, VIEWER, API } from './_session.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REAL_DB = path.join(HERE, '..', 'api', 'ticvai.db');
const DB = process.env.TICVAI_DB ?? REAL_DB;

// A harness that writes to the live database is a harness that deletes somebody's
// account one day. It refuses rather than asking to be run carefully.
if (path.resolve(DB) === path.resolve(REAL_DB)) {
  console.error('audit-gate-check writes an account, so it refuses to run against api/ticvai.db.');
  console.error('Point TICVAI_DB at a scratch copy.');
  process.exit(2);
}

const BASE = VIEWER.replace(/\/+$/, '');
const APIB = (API ?? VIEWER).replace(/\/+$/, '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

// On-domain: an off-domain address may only be invited as a client, and this
// needs the role between admin and client to be sure the page keys on `admin`
// rather than on "not a client".
const EMAIL = 'audit.gate.harness@softlabsgroup.com';
const PASSWORD = 'a-long-enough-passphrase';

let pass = 0, fail = 0;
// The detail is a diagnosis, so it prints on the line that needs one. A PASS
// carrying "no account_project row" reads as a failure that counted as a pass,
// which is the one thing a harness must never look like.
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (!ok && d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};
/** A measurement worth reading whichever way the assertion went. */
const note = (t) => console.log('      ' + t);

/**
 * Let the new reviewer read the package.
 *
 * A fresh account has no row in `account_project`, and without one the server
 * refuses every package route — including the *document* — with
 * `this account may not read "ticvai"`. So the first version of this check
 * measured a 403 from the project gate and called it the admin gate working: it
 * passed "a reviewer sees no figures" without the page ever having run.
 *
 * The grant goes in directly rather than through an endpoint because there is no
 * endpoint for it yet, and because the row is the thing the server actually
 * reads.
 */
function grant(project = 'ticvai') {
  const db = new DatabaseSync(DB);
  try {
    const row = db.prepare('SELECT id FROM account WHERE email_folded = ?')
      .get(EMAIL.trim().toLowerCase());
    if (!row) return false;
    db.prepare('INSERT OR REPLACE INTO account_project (account_id, project_id, role, created_at) '
      + "VALUES (?, ?, 'reviewer', datetime('now'))").run(row.id, project);
    return true;
  } finally {
    db.close();
  }
}

function forget(why) {
  try {
    const db = new DatabaseSync(DB);
    const folded = EMAIL.trim().toLowerCase();
    const row = db.prepare('SELECT id FROM account WHERE email_folded = ?').get(folded);
    if (row) {
      db.prepare('DELETE FROM account_project WHERE account_id = ?').run(row.id);
      db.prepare('DELETE FROM verdict WHERE account_id = ?').run(row.id);
      db.prepare('DELETE FROM session WHERE account_id = ?').run(row.id);
      db.prepare('DELETE FROM account WHERE id = ?').run(row.id);
    }
    db.prepare('DELETE FROM invite WHERE email_folded = ?').run(folded);
    db.close();
    console.log(`  ${why}: ${EMAIL} removed`);
  } catch (e) {
    console.log(`  ${why}: could not tidy up — ${e.message}`);
  }
}

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});

/** Sign in as somebody and report what `/audit.html` gives them. */
async function seenBy(email, password) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 1000 });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

  await page.goto(BASE + '/invite.html', { waitUntil: 'domcontentloaded' });
  await page.evaluate((a) => localStorage.setItem('ticvai-api', a), APIB);
  await page.evaluate(async (a, e, p) => {
    await fetch(a + '/api/auth/login', {
      method: 'POST', credentials: 'include',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: e, password: p }),
    });
  }, APIB, email, password);

  await page.goto(BASE + '/audit.html', { waitUntil: 'domcontentloaded' });
  await wait(7000);
  const seen = await page.evaluate(() => ({
    role: document.getElementById('whoami')?.textContent ?? '',
    figures: document.querySelectorAll('.au-figure').length,
    tables: document.querySelectorAll('.au-table').length,
    text: document.getElementById('audit-body')?.textContent?.trim() ?? '',
  }));
  await page.close();
  return { ...seen, errors };
}

try {
  forget('before');

  // ── the admin half, first ──
  const admin = await seenBy(
    process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
    process.env.TICVAI_HARNESS_PASSWORD ?? PASSWORD);
  check('an admin gets the audit', admin.figures >= 4 && admin.tables >= 2,
    `${admin.figures} figures, ${admin.tables} tables — "${admin.role}"`);
  note(`admin sees ${admin.figures} figures and ${admin.tables} tables as "${admin.role}"`);
  check('and it comes up clean', admin.errors.length === 0, admin.errors.slice(0, 3).join(' | '));

  if (admin.figures < 4) {
    console.log('\nThe admin view is broken, so the refusal below would prove nothing. Stopping.');
    forget('after');
    await browser.close();
    process.exit(1);
  }

  // ── make a reviewer ──
  const invited = await authed(`${APIB}/api/invites`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: EMAIL, role: 'reviewer' }),
  });
  check('the harness can invite a reviewer', invited.ok, `POST /api/invites → ${invited.status}`);
  if (!invited.ok) throw new Error(`invite failed: ${invited.status}`);
  const invite = await invited.json();

  const redeemed = await fetch(`${APIB}/api/auth/redeem`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ token: invite.token, name: 'Audit Gate', password: PASSWORD }),
  });
  check('and the reviewer can redeem it', redeemed.ok, `POST /api/auth/redeem → ${redeemed.status}`);
  if (!redeemed.ok) throw new Error(`redeem failed: ${redeemed.status}`);

  // Without this the server refuses the document itself and the page never runs
  // — see the note on `grant`. The assertion below would then be measuring the
  // project gate and reporting it as the admin gate.
  check('the reviewer is granted the package', grant(),
    'no account_project row — the refusal below would be the project gate, not this page');

  // ── the half this check exists for ──
  const reviewer = await seenBy(EMAIL, PASSWORD);
  check('a reviewer is not shown the audit', reviewer.figures === 0 && reviewer.tables === 0,
    `${reviewer.figures} figures, ${reviewer.tables} tables leaked to "${reviewer.role}"`);
  note(`reviewer signed in as "${reviewer.role}" and got ${reviewer.figures} figures`);
  // Refused, not blank. A page that renders an empty shell reads as broken, and
  // a reviewer who thinks the tool is broken files a bug about the wrong thing.
  check('and is told what the page is instead',
    /admins/i.test(reviewer.text) && reviewer.text.length > 60,
    `body was ${reviewer.text.length} chars: "${reviewer.text.slice(0, 80)}"`);
  check('with no errors on the way', reviewer.errors.length === 0,
    reviewer.errors.slice(0, 3).join(' | '));
} catch (e) {
  check('the harness ran to the end', false, e.message);
} finally {
  forget('after');
  await browser.close();
}

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
