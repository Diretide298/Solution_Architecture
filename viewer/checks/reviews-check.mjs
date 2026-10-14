// What the Reviews page lets somebody do, and that each of those does what it
// says: answer an ask (it leaves the worklist and the count drops), take the
// answer back, send it back with a reason, and discard your own verdict only
// after a second press. Then the page's own promises: one filter in the
// address that "Show everything" clears whole (the old Clear left three keys
// behind), every control labelled, the pace chart drawn at its own size with a
// table twin, and the notes that name you not stopping at twelve.
//
// signoff-check.mjs holds the coverage and the list of every artefact; this
// holds the rest. Writes verdicts, so it runs against a scratch store:
//   TICVAI_VIEWER=http://localhost:4173 TICVAI_API=http://localhost:4173 node checks/reviews-check.mjs
import puppeteer from 'puppeteer-core';
import { authed, VIEWER as V, API as A } from './_session.mjs';
const VIEWER = V.replace(/\/+$/, '');
const API = A.replace(/\/+$/, '');
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
await page.setViewport({ width: 1400, height: 1000 });
await page.goto(`${VIEWER}/invite.html`, { waitUntil: 'domcontentloaded' });
await page.evaluate((v, a) => { if (a === v) localStorage.setItem('ticvai-api', ''); }, VIEWER, API);
await page.evaluate(async (api) => {
  await fetch(`${api}/api/auth/login`, {
    method: 'POST', credentials: 'include', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'harness.admin@softlabsgroup.com', password: 'a-long-enough-passphrase' }),
  });
}, API);

const call = (method, path, body) => page.evaluate(async (api, m, p, b) => {
  const r = await fetch(`${api}${p}`, {
    method: m, credentials: 'include', headers: { 'content-type': 'application/json' },
    body: b ? JSON.stringify(b) : undefined,
  });
  return { ok: r.ok, status: r.status, body: await r.json().catch(() => null) };
}, API, method, path, body);
const history = async (kind, id) => (await call('GET', `/api/validation/${kind}/${encodeURIComponent(id)}`)).body.history;

// Three tables nobody has judged, so a store that already holds a review
// cannot decide what these rows show.
const backend = await (await authed(`${VIEWER}/api/backend`)).json();
const judged = new Set((await call('GET', '/api/verdicts')).body.verdicts.map((v) => `${v.target_kind} ${v.target_id}`));
const [answerMe, discardMe, sendMe] = backend.tables.map((t) => t.name).filter((n) => !judged.has(`table ${n}`));

const open = async (path, ready) => {
  await page.goto('about:blank');
  await page.goto(`${VIEWER}${path}`, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector(ready, { timeout: 40000 });
  await wait(1000);
};
const listed = (host, name) => page.evaluate((h, n) => [...document.querySelectorAll(`${h} .rv-art-link`)]
  .some((a) => a.textContent === n), host, name);
const pressIn = async (host, name, label) => page.evaluate((h, n, l) => {
  const row = [...document.querySelectorAll(`${h} tr.rv-row`)]
    .find((r) => [...r.querySelectorAll('.rv-art-link')].some((a) => a.textContent === n));
  const b = row && [...row.querySelectorAll('button')].find((x) => x.textContent === l);
  if (!b) return false;
  b.click();
  return true;
}, host, name, label);

// ── answering an ask ─────────────────────────────────────────────────
{
  const asked = await call('POST', '/api/validation', { target_kind: 'table', target_id: answerMe, verdict: 'needs-work', note: 'harness: answer me' });
  await open(`/reviews.html?q=${encodeURIComponent(answerMe)}#asked`, '#rv-asked tr.rv-row');
  const before = await page.evaluate(() => document.getElementById('rv-nav-asked').textContent);
  check('the ask is in the worklist, and the rail counts it', await listed('#rv-asked', answerMe) && before === '1', `rail count ${before}`);
  await pressIn('#rv-asked', answerMe, 'Respond');
  await wait(300);
  const choices = await page.evaluate(() => [...document.querySelectorAll('#rv-asked .rv-picker button')].map((b) => b.textContent));
  check('Respond offers the five answers and a way out', choices.length === 6 && choices.at(-1) === 'Cancel', choices.join(', '));
  await pressIn('#rv-asked', answerMe, 'Built');
  await wait(1500);
  const after = {
    still: await listed('#rv-asked', answerMe),
    count: await page.evaluate(() => document.getElementById('rv-nav-asked').textContent),
    hidden: await page.evaluate(() => document.getElementById('rv-nav-asked').hidden),
  };
  const row = (await history('table', answerMe)).find((v) => v.id === asked.body.id);
  check('answering it records how, and it leaves the worklist and the count',
    row.done_response === 'built' && !after.still && after.hidden, `${row.done_response} · count "${after.count}"`);

  await open(`/reviews.html?q=${encodeURIComponent(answerMe)}#responses`, '#rv-log tr.rv-row');
  const status = await page.evaluate((n) => [...document.querySelectorAll('#rv-log tr.rv-row')]
    .find((r) => r.querySelector('.rv-art-link')?.textContent === n)?.querySelector('.rv-status').textContent, answerMe);
  check('the log says it was answered "Built", and by whom', /Built/.test(status) && /harness/i.test(status), status);
  await pressIn('#rv-log', answerMe, 'Reopen');
  await wait(1500);
  const reopened = (await history('table', answerMe)).find((v) => v.id === asked.body.id);
  check('Reopen takes the answer back', !reopened.done_at, String(reopened.done_at));
}

// ── sending an answer back ───────────────────────────────────────────
{
  const asked = await call('POST', '/api/validation', { target_kind: 'table', target_id: sendMe, verdict: 'needs-work', note: 'harness: send me back' });
  await call('POST', `/api/verdicts/${asked.body.id}/done`, { done: true, response: 'built' });
  await open(`/reviews.html?q=${encodeURIComponent(sendMe)}#responses`, '#rv-log tr.rv-row');
  await pressIn('#rv-log', sendMe, 'Send back');
  await wait(300);
  const form = await page.evaluate(() => {
    const note = document.querySelector('#rv-log .rv-sendback-note');
    const send = [...document.querySelectorAll('#rv-log .rv-sendback-form button')].find((b) => b.textContent === 'Send back');
    return { labelled: Boolean(note?.closest('label')), disabled: send?.disabled };
  });
  check('Send back asks why first, and will not send without a reason', form.labelled && form.disabled === true, JSON.stringify(form));
  await page.type('#rv-log .rv-sendback-note', 'harness: the 422 still has no field name');
  await page.evaluate(() => [...document.querySelectorAll('#rv-log .rv-sendback-form button')].find((b) => b.textContent === 'Send back').click());
  await wait(1500);
  const sent = (await history('table', sendMe)).find((v) => v.id === asked.body.id);
  const inWorklist = await listed('#rv-asked', sendMe);
  check('sent back, with the reason, and open again in the worklist',
    /field name/.test(sent.sent_back_note ?? '') && inWorklist, sent.sent_back_note);
}

// ── discarding your own verdict asks twice ───────────────────────────
{
  await call('POST', '/api/validation', { target_kind: 'table', target_id: discardMe, verdict: 'approved', note: 'harness: discard me' });
  await open(`/reviews.html?q=${encodeURIComponent(discardMe)}#responses`, '#rv-log tr.rv-row');
  await pressIn('#rv-log', discardMe, 'Discard');
  await wait(300);
  const strip = await page.evaluate(() => {
    const box = document.querySelector('#rv-log .sh-confirm');
    return box ? { role: box.getAttribute('role'), text: box.textContent } : null;
  });
  check('Discard asks a second time, saying it cannot be undone',
    strip?.role === 'alertdialog' && /cannot be brought back/.test(strip.text), strip?.text);
  check('and the first press removed nothing', (await history('table', discardMe)).length === 1);
  await page.evaluate(() => [...document.querySelectorAll('#rv-log .sh-confirm button')].find((b) => b.textContent === 'Cancel').click());
  await wait(300);
  check('Cancel leaves it', (await history('table', discardMe)).length === 1
    && await page.evaluate(() => !document.querySelector('#rv-log .sh-confirm')));
  await pressIn('#rv-log', discardMe, 'Discard');
  await wait(300);
  await page.evaluate(() => [...document.querySelectorAll('#rv-log .sh-confirm button')].find((b) => b.textContent === 'Discard it').click());
  await wait(1500);
  check('the second press discards it', (await history('table', discardMe)).length === 0);
}

// ── one filter, in the address, cleared whole ────────────────────────
{
  await open('/reviews.html?kind=table&side=client&window=7&q=zz-none#coverage', '#rv-scope .sh-clear');
  const says = await page.evaluate(() => document.querySelector('#rv-scope .sh-says').textContent);
  check('the filter says what it shows', /the client's verdicts on tables from the last 7 days, about anything matching "zz-none"/.test(says), says);
  await page.evaluate(() => document.querySelector('#rv-scope .sh-clear').click());
  await wait(800);
  const after = await page.evaluate(() => ({
    search: location.search,
    pressed: [...document.querySelectorAll('#rv-scope .sh-switch button')].map((b) => `${b.textContent}:${b.getAttribute('aria-pressed')}`).join(','),
    kind: document.querySelector('#rv-scope select').value,
  }));
  check('Show everything clears every key, and the switch shows Both pressed',
    after.search === '' && after.pressed.startsWith('Both:true') && after.kind === '', JSON.stringify(after));

  const unlabelled = await page.evaluate(() => [...document.querySelectorAll('#reviews input, #reviews select, #reviews textarea')]
    .filter((i) => !i.closest('label') && !i.getAttribute('aria-label') && !i.getAttribute('aria-labelledby'))
    .map((i) => i.id || i.type));
  check('every control on the page has a label', unlabelled.length === 0, unlabelled.join(', ') || 'all labelled');
}

// ── reviewers: the pace chart and the person filter ──────────────────
{
  await open('/reviews.html#reviewers', '#rv-people tr.rv-row');
  const chart = await page.evaluate(() => {
    const svg = document.querySelector('#rv-pace svg');
    return svg && {
      stretch: svg.getAttribute('preserveAspectRatio'),
      sized: svg.getAttribute('viewBox') === `0 0 ${svg.getAttribute('width')} ${svg.getAttribute('height')}`,
      twin: document.querySelectorAll('#rv-pace-table tbody tr').length,
      legend: document.querySelectorAll('#rv-pace-legend .sh-legend-item').length,
    };
  });
  check('the pace chart is drawn at its own size, with a legend and a table twin',
    chart && !chart.stretch && chart.sized && chart.twin > 0 && chart.legend === 2, JSON.stringify(chart));

  await page.evaluate(() => {
    const row = [...document.querySelectorAll('#rv-people tr.rv-row')].find((r) => /harness/i.test(r.textContent));
    row.querySelector('button.rv-only').click();
  });
  await wait(800);
  const person = await page.evaluate(() => ({
    url: new URLSearchParams(location.search).get('person'),
    pressed: [...document.querySelectorAll('#rv-people button.rv-only')].filter((b) => b.getAttribute('aria-pressed') === 'true').length,
    rows: document.querySelectorAll('#rv-people tr.rv-row').length,
  }));
  check('"Only theirs" filters the page to one reviewer, in the address, and says it is pressed',
    person.url === 'harness.admin@softlabsgroup.com' && person.pressed === 1 && person.rows === 1, JSON.stringify(person));
}

// ── named you: every note, a page at a time ──────────────────────────
{
  const mine = (await call('GET', '/api/mentions')).body.mentions.length;
  await open('/reviews.html#named', '#rv-named table');
  const shown = await page.evaluate(() => ({
    rows: document.querySelectorAll('#rv-named tr.rv-row').length,
    more: Boolean(document.querySelector('#rv-named .sh-more')),
  }));
  check('the notes that name you are paged, not capped',
    shown.rows === Math.min(mine, 20) && shown.more === (mine > 20), `${mine} notes, ${shown.rows} drawn, more: ${shown.more}`);
}

console.log(`\n${pass} passed, ${fail} failed`);
if (errors.length) { console.log('page errors:'); for (const e of errors) console.log('  ', e); }
await browser.close();
process.exit(fail || errors.length ? 1 : 0);
