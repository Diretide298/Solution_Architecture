// The sidebar groups fold on the same handler the pane sections use. Twelve
// platforms of up to 29 screens each meant reaching the kiosk was a scroll past
// the whole of Guest Web. The checks are about the state surviving the things
// that rebuild the tree — a re-render, a layer switch, a regrouping.
import puppeteer from 'puppeteer-core';
const VIEWER = 'http://localhost:4173';
const API = 'http://localhost:8787';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const errors = [];
const page = await browser.newPage();
page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
await page.setViewport({ width: 1500, height: 950 });
await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate(async (api) => {
  await fetch(`${api}/api/auth/login`, {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
  });
}, API);
await page.goto(VIEWER, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 25000 });
await wait(3000);

const toLayer = async (layer) => {
  await page.evaluate((l) => document.querySelector(`#layers button[data-layer="${l}"]`).click(), layer);
  await wait(2200);
};

/** Rows visible under the first group, and whether its head reads as shut. */
const firstGroup = () => page.evaluate(() => {
  const group = document.querySelector('#tree .tree-group');
  if (!group) return null;
  const head = group.querySelector('.tree-group-head');
  const rows = [...group.querySelectorAll('.tree-file')];
  return {
    name: head.textContent.trim(),
    collapsed: head.classList.contains('collapsed'),
    expanded: head.getAttribute('aria-expanded'),
    total: rows.length,
    showing: rows.filter((r) => !r.hidden && r.offsetParent !== null).length,
  };
});

await toLayer('frontend');

// ── it folds ─────────────────────────────────────────────────────────
{
  const open = await firstGroup();
  check('a sidebar group starts open', open && !open.collapsed && open.showing > 0,
    `${open?.name} · ${open?.showing} of ${open?.total} rows`);
  check('and says so to a screen reader', open.expanded === 'true', `aria-expanded=${open.expanded}`);

  await page.evaluate(() => document.querySelector('#tree .tree-group-head').click());
  await wait(400);
  const shut = await firstGroup();
  check('clicking the head hides every row under it', shut.collapsed && shut.showing === 0,
    `${shut.showing} of ${shut.total} still showing`);
  check('and the group itself stays, so it can be opened again',
    await page.evaluate(() => Boolean(document.querySelector('#tree .tree-group-head'))));

  await page.evaluate(() => document.querySelector('#tree .tree-group-head').click());
  await wait(400);
  const again = await firstGroup();
  check('clicking again brings them back', !again.collapsed && again.showing === again.total,
    `${again.showing} of ${again.total}`);
}

// ── the keyboard reaches it ──────────────────────────────────────────
{
  await page.evaluate(() => document.querySelector('#tree .tree-group-head').focus());
  await page.keyboard.press('Enter');
  await wait(400);
  const shut = await firstGroup();
  check('Enter folds it too', shut.collapsed && shut.showing === 0);
}

// ── the state survives what rebuilds the tree ────────────────────────
{
  const name = (await firstGroup()).name;

  // a re-render caused by regrouping and coming back
  await page.evaluate(() => {
    const buttons = [...document.querySelectorAll('#group-by button')];
    if (buttons[1]) buttons[1].click();
  });
  await wait(1500);
  const other = await firstGroup();
  check('a different grouping is not folded by the first one\'s choice',
    other && !other.collapsed, `${other?.name} · ${other?.showing} of ${other?.total}`);

  await page.evaluate(() => {
    const buttons = [...document.querySelectorAll('#group-by button')];
    if (buttons[0]) buttons[0].click();
  });
  await wait(1500);
  const back = await firstGroup();
  check('and coming back finds it still folded', back.name === name && back.collapsed,
    `${back.name} · collapsed=${back.collapsed}`);

  // a layer switch and back rebuilds the tree entirely
  await toLayer('backend');
  await toLayer('frontend');
  const returned = await firstGroup();
  check('a layer switch and back does not lose the fold',
    returned.name === name && returned.collapsed, `${returned.name} · collapsed=${returned.collapsed}`);

  // and it is genuinely the same group, not a coincidence of position
  check('the rows are still hidden after all that', returned.showing === 0,
    `${returned.showing} of ${returned.total}`);

  await page.evaluate(() => document.querySelector('#tree .tree-group-head').click());
  await wait(400);
}

// ── every layer's tree folds, not just the one it was built for ──────
for (const layer of ['contracts', 'backend', 'domain', 'decisions']) {
  await toLayer(layer);
  const before = await firstGroup();
  if (!before || before.total === 0) {
    check(`${layer} — no foldable group to check`, true, before?.name ?? 'no groups');
    continue;
  }
  await page.evaluate(() => document.querySelector('#tree .tree-group-head').click());
  await wait(400);
  const after = await firstGroup();
  check(`${layer} — its groups fold as well`, after.collapsed && after.showing === 0,
    `${before.name}: ${before.showing} → ${after.showing}`);
  await page.evaluate(() => document.querySelector('#tree .tree-group-head').click());
  await wait(300);
}

// ── the pane sections still fold, which is the handler this shares ───
{
  await toLayer('frontend');
  await page.evaluate(() => document.querySelector('#modes .mode[data-mode="screen"]').click());
  await wait(3000);
  const label = await page.evaluate(() => {
    const l = [...document.querySelectorAll('#screen-body .journey-section-label')]
      .find((n) => !n.classList.contains('empty-section'));
    if (!l) return null;
    l.click();
    return l.textContent.trim();
  });
  await wait(400);
  const folded = await page.evaluate((t) => {
    const l = [...document.querySelectorAll('#screen-body .journey-section-label')]
      .find((n) => n.textContent.trim() === t);
    return l?.classList.contains('collapsed');
  }, label);
  check('a pane section still folds — the shared handler did not break it', folded === true, label);
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
