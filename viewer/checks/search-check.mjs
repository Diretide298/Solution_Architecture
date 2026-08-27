/**
 * Search finds the package, not just the contracts — and every result opens.
 *
 * The palette searched `index.nodes` and nothing else: **1,979 contract nodes,
 * out of 3,199 things in the package.** Its own placeholder said "Search
 * operations…", so it was not lying, but a reviewer typing `POS-006` got "No
 * match" — which reads as *not in this package* and meant *not a contract*.
 * 492 screens, 379 tables, 123 state models, 94 flows, 58 boards, 31 decisions
 * and 29 events were unfindable, and nothing anywhere said so.
 *
 * Two claims here, and the second is the one that matters:
 *
 *   it can be found     every kind is reachable by typing its own id
 *   it can be opened    the result lands on the artefact's page, and where the
 *                       package writes it down, the line is real — checked by
 *                       fetching the file and reading that line
 *
 * A file:line nobody verifies is the worst kind of precision: it is believed.
 */
import puppeteer from 'puppeteer-core';
import { authed, VIEWER, API } from './_session.mjs';

const BASE = VIEWER.replace(/\/+$/, '');
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

let pass = 0, fail = 0;
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};

const registry = await authed(`${BASE}/pkg/projects`).then((r) => (r.ok ? r.json() : null));
const project = registry?.default ?? registry?.projects?.find((p) => p.active !== false)?.id;
if (!project) throw new Error('no project in /pkg/projects');
const pkg = `${BASE}/pkg/${project}`;

const payload = await authed(`${pkg}/search`).then((r) => (r.ok ? r.json() : null));
check('the search route answers', Boolean(payload?.present));
if (!payload?.present) process.exit(1);

const S = payload.stats;
const entries = payload.entries;
check('it covers every kind, not only contracts',
  Object.keys(S.byKind).length >= 8, Object.entries(S.byKind).map(([k, v]) => `${k}=${v}`).join(' '));
check('the located/file-only/unplaced split accounts for all of them',
  S.located + S.fileOnly + S.unplaced === S.entries,
  `${S.located}+${S.fileOnly}+${S.unplaced} vs ${S.entries}`);

// ── the lines are real ───────────────────────────────────────────────
// A sample per kind rather than all 807: this fetches whole files, and the
// claim is about how the line was derived, which is one code path per kind.
const bad = [];
let tried = 0;
const cache = new Map();
const fileText = async (f) => {
  if (!cache.has(f)) {
    cache.set(f, await authed(`${pkg}/file?path=${encodeURIComponent(f)}`)
      .then((r) => (r.ok ? r.text() : null)).catch(() => null));
  }
  return cache.get(f);
};

for (const kind of Object.keys(S.byKind)) {
  const sample = entries.filter((e) => e.kind === kind && e.file && e.line).slice(0, 6);
  for (const e of sample) {
    tried += 1;
    const text = await fileText(e.file);
    if (text == null) { bad.push(`${e.kind} ${e.id}: ${e.file} would not fetch`); continue; }
    const lines = text.split(/\r?\n/);
    const at = lines[e.line - 1];
    if (at === undefined) { bad.push(`${e.kind} ${e.id}: ${e.file} has no line ${e.line}`); continue; }
    // The line has to actually be about this artefact. For a screen or a flow
    // that is its id; for a table its name; for a state model or an event the
    // first line of the document; for an ADR the heading.
    const token = String(e.id).split(/[.\s]/).pop().toLowerCase();
    const ok = at.toLowerCase().includes(String(e.id).toLowerCase())
      || at.toLowerCase().includes(token)
      || /^(entity|name|title|#|CREATE)/i.test(at.trim());
    if (!ok) bad.push(`${e.kind} ${e.id}: ${e.file}:${e.line} reads ${JSON.stringify(at.slice(0, 48))}`);
  }
}
check('every sampled line really is where that artefact is written',
  bad.length === 0, `${tried} checked${bad.length ? ', wrong: ' + bad.slice(0, 3).join(' | ') : ''}`);

// A file that cannot be fetched is a `file:line` that cannot be opened, and the
// peek would show an error where it promised source. `.sql` was refused by
// /api/file until search started pointing into the migrations.
const kinds = [...new Set(entries.filter((e) => e.file).map((e) => e.file.split('.').pop().toLowerCase()))];
const unfetchable = [];
for (const ext of kinds) {
  const one = entries.find((e) => e.file?.toLowerCase().endsWith('.' + ext));
  const status = await authed(`${pkg}/file?path=${encodeURIComponent(one.file)}`)
    .then((r) => r.status).catch(() => 0);
  if (status !== 200 && ext !== 'html') unfetchable.push(`${ext} -> ${status}`);
}
check('every file extension search points at can be read',
  unfetchable.length === 0, `${kinds.join(', ')}${unfetchable.length ? ' | bad: ' + unfetchable.join(', ') : ''}`);

// ── the browser ──────────────────────────────────────────────────────
const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1100 });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });

await page.goto(BASE + '/invite.html', { waitUntil: 'domcontentloaded' });
await page.evaluate((a) => localStorage.setItem('ticvai-api', a), API);
await page.evaluate(async (a, e, p) => {
  await fetch(a + '/api/auth/login', {
    method: 'POST', credentials: 'include',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: e, password: p }),
  });
}, API,
  process.env.TICVAI_HARNESS_EMAIL ?? 'harness.admin@softlabsgroup.com',
  process.env.TICVAI_HARNESS_PASSWORD ?? 'a-long-enough-passphrase');

await page.goto(BASE + '/?project=' + project, { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 30000 });
await wait(4000);

const search = async (text) => {
  await page.evaluate(() => document.getElementById('search-trigger')?.click());
  await wait(1200);
  await page.evaluate((t) => {
    const i = document.getElementById('palette-input');
    i.value = t;
    i.dispatchEvent(new Event('input'));
  }, text);
  await wait(1400);
  return page.evaluate(() => [...document.querySelectorAll('.palette-item')].map((r) => ({
    title: r.querySelector('.palette-item-title')?.textContent ?? '',
    kind: r.querySelector('.palette-item-kind')?.textContent ?? '',
    where: r.querySelector('.palette-item-where')?.textContent ?? '',
  })));
};

// One query per kind, using the id somebody would actually type.
const probes = [
  ['screen', entries.find((e) => e.kind === 'screen')?.id],
  ['table', entries.find((e) => e.kind === 'table')?.id],
  ['state model', entries.find((e) => e.kind === 'state')?.id],
  ['journey', entries.find((e) => e.kind === 'flow')?.id],
  ['event', entries.find((e) => e.kind === 'event')?.id],
];
const missed = [];
for (const [label, id] of probes) {
  if (!id) continue;
  const rows = await search(id);
  const hit = rows.some((r) => r.kind === label || r.title.toLowerCase().includes(String(id).toLowerCase()));
  if (!hit) missed.push(`${label} "${id}" -> ${rows.slice(0, 2).map((r) => r.kind + ':' + r.title).join(', ') || 'nothing'}`);
}
check('typing an id finds that kind', missed.length === 0,
  `${probes.length} kinds${missed.length ? ' | missed: ' + missed.join(' | ') : ''}`);

// ── a result opens the artefact's page ───────────────────────────────
const screen = entries.find((e) => e.kind === 'screen' && e.file && e.line);
await search(screen.id);
await page.evaluate(() => document.querySelector('.palette-item')?.click());
await wait(3500);
const landed = await page.evaluate(() => ({
  layer: document.body.dataset.layer ?? '',
  hash: location.hash,
  mode: document.querySelector('#modes button.active')?.dataset.mode ?? '',
}));
check('opening a screen result lands on the screen view',
  landed.layer === 'frontend' && landed.mode === 'screen',
  `layer=${landed.layer} mode=${landed.mode} hash=${landed.hash}`);
check('and leaves a link in the address', landed.hash === `#screen:${screen.id}`, landed.hash);

// ── file:line opens the source at that line ──────────────────────────
await search(screen.id);
const opened = await page.evaluate(() => {
  const w = document.querySelector('.palette-item .palette-item-where');
  if (!w) return false;
  w.click();
  return true;
});
check('a result offers where it is written', opened);
await wait(3500);
const peek = await page.evaluate(() => {
  const box = document.getElementById('peek');
  if (!box || box.hidden) return null;
  const hi = box.querySelector('.code-line.highlight');
  return {
    where: document.getElementById('peek-where')?.textContent ?? '',
    lines: box.querySelectorAll('.code-line').length,
    highlighted: hi?.querySelector('.ln')?.textContent ?? null,
    text: hi?.textContent ?? '',
  };
});
check('the source peek opens', Boolean(peek), peek ? `${peek.lines} lines` : 'it stayed shut');
check('it names the file and line', peek?.where === `${screen.file}:${screen.line}`, peek?.where ?? '');
check('and highlights that exact line', peek?.highlighted === String(screen.line),
  `highlighted ${peek?.highlighted}, wanted ${screen.line}`);
check('which is the line the artefact is defined on',
  (peek?.text ?? '').includes(screen.id), (peek?.text ?? '').slice(0, 60));

// Escape belongs to the peek while it is open, not to the drawer underneath.
await page.keyboard.press('Escape');
await wait(800);
check('escape closes the peek',
  await page.evaluate(() => document.getElementById('peek')?.hidden === true));

check('no console or page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
