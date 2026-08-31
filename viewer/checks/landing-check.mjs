/**
 * The door sends people where it says it does.
 *
 * `home.html` is the first thing a reader sees and the only page with no
 * harness. It shipped a lockup labelled **"Aster — open the viewer"** that did
 * not open the viewer: `href="/"` is `index.html`, which bounces a reader back
 * to the door on the **first** load of a session — it gates that on a
 * `ticvai-session` flag it sets itself, and the door never sets it. So the first
 * click went `/home.html?project=ticvai` → `/` → `/home.html`, landing back on
 * the door **with the project dropped from the address**, and every click after
 * it opened the viewer normally.
 *
 * **One link, two behaviours, and the wrong one is the one a new reader gets** —
 * which is why this needs a fresh session rather than a second look. Anyone
 * testing it twice sees it work.
 *
 * Also holds the 42 panel links, which are the actual way in: each must land on
 * the layer *and* the mode it names, with content under it.
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
let collecting = true;
page.on('pageerror', (e) => { if (collecting) errors.push(e.message); });
page.on('console', (m) => { if (collecting && m.type() === 'error') errors.push(m.text()); });

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

const door = async () => {
  await page.goto(BASE + '/home.html', { waitUntil: 'domcontentloaded' });
  await wait(7000);
};

// ── the lockup, on a session that has never seen index.html ──────────
await page.evaluate(() => sessionStorage.clear());
await door();
check('the door names a project in its address', page.url().includes('project='), page.url().replace(BASE, ''));

await page.evaluate(() => document.querySelector('.home-lockup')?.click());
await wait(6000);
const afterLockup = page.url();
const layerAfter = await page.evaluate(() => document.body.dataset.layer ?? '');
// **The logo is not a way into a package.** Choosing one is what the rail and
// the project row are for, and they say which; the lockup says nothing, so it
// must not pick. It shipped pointing at `/`, which fell through into whichever
// package was last opened — and it must not go the other way either, into a
// named package, which is what the first fix here wrongly did.
check('the lockup stays on the door', afterLockup.includes('/home.html') && layerAfter === '',
  afterLockup.replace(BASE, ''));
check('and it keeps the project in the address', afterLockup.includes(`project=${project}`),
  afterLockup.replace(BASE, ''));
check('the lockup does not claim to open the viewer',
  (await page.evaluate(() => document.querySelector('.home-lockup')?.getAttribute('aria-label') ?? '')) === 'Aster');

// ── every panel link lands where it says ─────────────────────────────
await door();
const rails = await page.evaluate(
  () => [...document.querySelectorAll('.rail-row')].map((b) => b.innerText.replace(/\s+/g, ' ').trim().split(' ')[0])
);
check('the rail offers a row per layer', rails.length >= 5, rails.join(', '));

let total = 0;
const wrong = [];
for (const name of rails) {
  await door();
  await page.evaluate((n) => {
    [...document.querySelectorAll('.rail-row')].find((x) => x.innerText.trim().startsWith(n))?.click();
  }, name);
  await wait(2200);
  const links = await page.evaluate(
    () => [...(document.getElementById('home-panel')?.querySelectorAll('a[href]') ?? [])].map((a) => a.getAttribute('href'))
  );
  for (const href of links) {
    await page.goto(BASE + href, { waitUntil: 'domcontentloaded' });
    await wait(4200);
    const st = await page.evaluate(() => ({
      layer: document.body.dataset.layer ?? '',
      mode: document.querySelector('#modes button.active')?.dataset.mode ?? '',
      n: document.querySelectorAll('main *').length,
    }));
    const want = new URLSearchParams(href.split('?')[1] ?? '');
    total += 1;
    const ok = (!want.get('layer') || st.layer === want.get('layer'))
      && (!want.get('mode') || st.mode === want.get('mode'))
      && st.n > 20;
    if (!ok) wrong.push(`${href} -> layer=${st.layer} mode=${st.mode} nodes=${st.n}`);
  }
}
check('every panel link lands on the layer and mode it names',
  wrong.length === 0, `${total} links${wrong.length ? ', wrong: ' + wrong.slice(0, 3).join(' | ') : ''}`);

// ── Overview deselects rather than navigating ────────────────────────
// `.rail-overview` is a class, not an id. A probe using getElementById finds
// nothing, clicks nothing, and reads the *previous* state as this one's result.
await door();
await page.evaluate((names) => {
  [...document.querySelectorAll('.rail-row')].find((x) => x.innerText.trim().startsWith(names[0]))?.click();
}, rails);
await wait(1800);
const filled = await page.evaluate(() => document.getElementById('home-panel')?.querySelectorAll('*').length ?? 0);
await page.evaluate(() => document.querySelector('.rail-overview')?.click());
await wait(1800);
const cleared = await page.evaluate(() => document.getElementById('home-panel')?.querySelectorAll('*').length ?? -1);
check('Overview clears the panel rather than navigating', filled > 0 && cleared === 0,
  `filled ${filled} -> ${cleared}`);

// ── sign out really ends the session ─────────────────────────────────
if (gated) {
  // Stop collecting from here. Signing out is *meant* to make the next package
  // read fail, and since the gate started answering a signed-out `/pkg/` fetch
  // with 401 instead of a 302 to the sign-in page, the browser logs that refusal
  // as a console error. It is the behaviour the two assertions below are for.
  //
  // Left in, this passed or failed depending on whether the page got its fetch
  // away before the browser closed — green in one run and red in the next, off
  // the same code. A flaky check is worse than no check: it teaches you to rerun
  // rather than to look.
  collecting = false;
  await door();
  await page.evaluate(() => {
    [...document.querySelectorAll('button')].find((x) => /sign out/i.test(x.innerText))?.click();
  });
  await wait(4500);
  check('sign out lands on the sign-in page', page.url().includes('/login.html'), page.url().replace(BASE, ''));
  const after = await page.evaluate(
    async () => (await fetch('/pkg/projects', { credentials: 'include', redirect: 'manual' })).status
  );
  check('and the session is actually over', after !== 200, `/pkg/projects answered ${after}`);
}

check('no console or page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
