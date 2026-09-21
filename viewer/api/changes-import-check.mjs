// The change request round trip: a range goes out as a CSV, somebody says how
// each was settled, and the file comes back. What this spends its time on is
// the half that does not write — the rows a bulk upload must refuse to touch —
// because those are the ones nobody would notice going wrong. A settlement that
// did not happen is visible on the page; a settlement that overwrote who
// settled something in March is not.
//
// Wants a service with an empty store:
//   TICVAI_DB=/tmp/check.db python -m uvicorn api.main:app --port 8799
//   API=http://localhost:8799 node api/changes-import-check.mjs
// The page's half of the same file. Imported rather than described, because
// the whole point of that module is that there is one column list and both
// ends use it — and a check that restated the list here would be a third
// copy to keep in step.
import { CHANGE_CSV_HEADER, changeCsvRow } from '../public/change-csv.js';

const API = process.env.API ?? 'http://localhost:8787';
let pass = 0, fail = 0;
const check = (n, ok, d = '') => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}${d ? ` — ${d}` : ''}`); ok ? pass++ : fail++; };

let cookie = '';
async function call(method, path, body) {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: { 'content-type': 'application/json', ...(cookie ? { cookie } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const set = res.headers.get('set-cookie');
  if (set) cookie = set.split(';')[0];
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data };
}

// The file, as a form the two routes read. Named so the service has a filename
// to quote back, which is half of what the preview is for.
async function send(path, csv, confirm) {
  const form = new FormData();
  form.append('file', new Blob([csv], { type: 'text/csv' }), 'change-requests.csv');
  if (confirm !== undefined) form.append('confirm', confirm);
  const res = await fetch(`${API}${path}`, { method: 'POST', headers: { cookie }, body: form });
  let data = null;
  try { data = await res.json(); } catch {}
  return { status: res.status, data };
}

// ── the CSV the service writes, read back ────────────────────────────
//
// Every field is quoted and an inner quote is doubled, so this is a small
// state machine rather than a split on commas: a `because` column is exactly
// where somebody puts a comma, and a parser that got that wrong would shift
// every column after it and pass anyway.
function parseCsv(text) {
  const rows = [];
  let row = [], field = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\r') { /* CRLF: the \n does the work */ }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows;
}

const quote = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
const toCsv = (header, body) =>
  '﻿' + [header.join(','), ...body.map((r) => r.map(quote).join(','))].join('\r\n');

// ── set the store up ─────────────────────────────────────────────────

const boot = await call('POST', '/api/auth/bootstrap', {
  email: 'harness.admin@softlabsgroup.com',
  name: 'Harness Admin',
  password: 'a-long-enough-passphrase',
});
check('an admin exists', boot.status === 200, `${boot.status} ${JSON.stringify(boot.data?.detail ?? '')}`);

const raised = [];
for (const [n, kind, target, title] of [
  [1, 'table', 'orders.sales_order', 'Order total has no currency'],
  [2, 'operation', 'POST /orders', 'Idempotency key is not on the request'],
  [3, 'screen', 'POS-002', 'No offline state for a held order'],
  [4, 'table', 'access.entitlement', 'Entitlement has no expiry'],
  [5, 'operation', 'GET /guests', 'Guest list is unpaginated'],
  [6, 'screen', 'BO-102', 'Two screens claim the same route'],
]) {
  const r = await call('POST', '/api/changes', {
    target_kind: kind,
    target_id: target,
    title,
    problem: `Raised by the harness so there is something to settle: ${title}.`,
    options: ['Leave it', 'Change the contract'],
  });
  if (r.status !== 200) { check(`CR ${n} filed`, false, `${r.status} ${JSON.stringify(r.data?.detail ?? '')}`); break; }
  raised.push(r.data.change);
}
check('six change requests are open', raised.length === 6, `${raised.length}`);

const byRef = Object.fromEntries(raised.map((c) => [c.id, c]));
const numberOf = (ref) => byRef[ref].number;

// Two of them are settled on the page first, so the file meets rows that are
// not open: one accepted (which `Done` may advance) and one rejected (which
// nothing in a file may move).
const accept = await call('POST', `/api/changes/CR-${String(numberOf('CR-002')).padStart(3, '0')}/resolve`,
  { status: 'accepted', resolution: 'Agreed at the 12 March review.', ref: 'ADR-014' });
check('CR-002 is accepted on the page', accept.status === 200, `${accept.status}`);

const reject = await call('POST', `/api/changes/CR-${String(numberOf('CR-004')).padStart(3, '0')}/resolve`,
  { status: 'rejected', resolution: 'Entitlements expire with the tenant, not on their own.' });
check('CR-004 is rejected on the page', reject.status === 200, `${reject.status}`);

// ── the export ───────────────────────────────────────────────────────

const dl = await fetch(`${API}/api/export/changes`, { headers: { cookie } });
check('the range downloads', dl.status === 200, `${dl.status}`);
check('it is named for what it holds',
  /filename="ticvai-change-requests-.*\.csv"/.test(dl.headers.get('content-disposition') ?? ''),
  dl.headers.get('content-disposition') ?? '');
check('it says how many rows are under the header', dl.headers.get('x-ticvai-rows') === '6',
  dl.headers.get('x-ticvai-rows') ?? 'absent');

// The bytes, not the text: Response.text() strips a byte order mark on the way
// through, so reading it back that way would pass whether the service wrote one
// or not — and the mark is the whole reason an em dash survives Excel.
const bytes = new Uint8Array(await dl.arrayBuffer());
check('it opens in Excel as UTF-8', bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf,
  [...bytes.slice(0, 3)].map((b) => b.toString(16)).join(' '));
const rows = parseCsv(new TextDecoder().decode(bytes).replace(/^﻿/, ''));
const header = rows[0];
const body = rows.slice(1);
const at = (name) => header.indexOf(name);

check('id is the first column', header[0] === 'id', header[0]);
check('the human reference is beside it', header[1] === 'ref', header[1]);
check('the three editable columns are there and are ahead of problem',
  at('our decision') > 0 && at('because') > at('our decision')
  && at('reference') > at('because') && at('problem') > at('reference'),
  header.join('|'));

const rowFor = (ref) => body.find((r) => r[1] === ref);
check('an open request has a blank "our decision"', rowFor('CR-001')[at('our decision')] === '',
  JSON.stringify(rowFor('CR-001')[at('our decision')]));
check('a settled one carries its decision', rowFor('CR-002')[at('our decision')] === 'Accepted',
  rowFor('CR-002')[at('our decision')]);
check('the status column shows Open for the open ones', rowFor('CR-001')[at('status')] === 'Open',
  rowFor('CR-001')[at('status')]);
check('options come back pipe-separated', rowFor('CR-001')[at('options')] === 'Leave it | Change the contract',
  rowFor('CR-001')[at('options')]);

// ── the two exports are one file ─────────────────────────────────────
//
// There are two buttons that write this CSV — the one on the changes page and
// Download a date range here — and either file can be filled in and uploaded
// back. That only holds while they are the same file, so it is asserted rather
// than described: the service builds its rows from the store, the page builds
// them from what /api/changes hands over, and they have to land on the same
// text.
check('the service writes the columns change-csv.js declares',
  JSON.stringify(header) === JSON.stringify(CHANGE_CSV_HEADER),
  `service: ${header.join('|')}`);

const live = await call('GET', '/api/changes');
const asPage = Object.fromEntries((live.data?.items ?? []).map((c) => [c.id, changeCsvRow(c)]));
const mismatched = body
  .map((row) => {
    const mine = asPage[row[1]];
    if (!mine) return `${row[1]}: the page has no such row`;
    const col = row.findIndex((cell, i) => cell !== String(mine[i] ?? ''));
    return col === -1 ? null
      : `${row[1]} · ${header[col]}: service ${JSON.stringify(row[col])} `
        + `vs page ${JSON.stringify(String(mine[col] ?? ''))}`;
  })
  .filter(Boolean);
check('and the page builds the same row for every request the service does',
  mismatched.length === 0, mismatched.join(' | '));

// ── the file somebody edited ─────────────────────────────────────────
//
// One row per bucket, so the preview's counts are a statement about the
// reasoning rather than about this particular sheet.
const idOf = (ref) => rowFor(ref)[0];
const edited = toCsv(
  ['id', 'ref', 'our decision', 'because', 'reference'],
  [
    [idOf('CR-001'), 'CR-001', 'Accepted', 'Currency goes on the line, not the order.', 'ADR-021'],
    [idOf('CR-002'), 'CR-002', 'Done', '', ''],                       // accepted → done: advance
    [idOf('CR-003'), 'CR-003', '', '', ''],                            // blank: left alone
    [idOf('CR-004'), 'CR-004', 'Rejected', '', ''],                    // already, with a stored reason
    [idOf('CR-005'), 'CR-005', 'Rejected', '', ''],                    // open, rejected with no reason
    [idOf('CR-006'), 'CR-006', 'Sorted', '', ''],                      // not one of the four
    ['99999', 'CR-999', 'Accepted', '', ''],                           // no such request
    ['', 'CR-000', 'Accepted', '', ''],                                // a decision with no id
    ['not-a-number', 'CR-000', 'Accepted', '', ''],                    // an id that is not one
  ],
);

const plan = await send('/api/changes/import/preview', edited);
check('the preview answers', plan.status === 200, `${plan.status} ${JSON.stringify(plan.data?.detail ?? '')}`);
const c = plan.data?.counts ?? {};
check('one open request would be settled', c.settle === 1, JSON.stringify(c));
check('the accepted one would advance to done', c.advance === 1, JSON.stringify(c));
check('the one that agrees is left alone', c.already === 1, JSON.stringify(c));
check('a blank cell is counted, not acted on', c.blank === 1, JSON.stringify(c));
check('five rows are reported as problems', c.problems === 5, JSON.stringify(c));
check('the preview wrote nothing', plan.data?.applied === false);
check('problems are in the order the sheet has them',
  (plan.data?.problems ?? []).every((p, i, all) => i === 0 || all[i - 1].row <= p.row),
  JSON.stringify((plan.data?.problems ?? []).map((p) => p.row)));
check('a rejection with nothing saying why is refused by name',
  (plan.data?.problems ?? []).some((p) => /is rejected with nothing/.test(p.message)),
  JSON.stringify((plan.data?.problems ?? []).map((p) => p.message)));
check('a word outside the four is refused with the four named',
  (plan.data?.problems ?? []).some((p) => /'Sorted' is not one of Open, Accepted, Rejected, Done/.test(p.message)),
  JSON.stringify((plan.data?.problems ?? []).map((p) => p.message)));

// ── reopening, which a file may never do ─────────────────────────────

const reopen = toCsv(['id', 'our decision', 'because'],
  [[idOf('CR-004'), 'Open', 'Actually let us look again.']]);
const reopenPlan = await send('/api/changes/import/preview', reopen);
check('reopening a settled request lands in differs, not settle',
  reopenPlan.data?.counts?.differs === 1 && reopenPlan.data?.counts?.settle === 0,
  JSON.stringify(reopenPlan.data?.counts));

// ── the wrong file, and the right one ────────────────────────────────

const noId = toCsv(['ref', 'our decision'], [['CR-001', 'Accepted']]);
const noIdPlan = await send('/api/changes/import/preview', noId);
check('a file with no id column is refused', noIdPlan.status === 400, `${noIdPlan.status}`);
check('and says why there is no guessing it', /no way to tell which/.test(noIdPlan.data?.detail ?? ''),
  noIdPlan.data?.detail ?? '');

const verdictish = toCsv(['id', 'our verdict'], [['1', 'Built']]);
const verdictPlan = await send('/api/changes/import/preview', verdictish);
check('the review activity file is recognised and sent to the right panel',
  verdictPlan.status === 400 && /Close items from a spreadsheet/.test(verdictPlan.data?.detail ?? ''),
  verdictPlan.data?.detail ?? '');

const noConfirm = await send('/api/changes/import/apply', edited);
check('an apply with no checksum is refused', noConfirm.status === 400, `${noConfirm.status}`);
const wrongConfirm = await send('/api/changes/import/apply', edited, 'f'.repeat(64));
check('an apply carrying another file’s checksum is refused', wrongConfirm.status === 400, `${wrongConfirm.status}`);
const staleConfirm = await send('/api/changes/import/apply', reopen, plan.data.digest);
check('the checksum is about the bytes, not the press', staleConfirm.status === 400, `${staleConfirm.status}`);

const applied = await send('/api/changes/import/apply', edited, plan.data.digest);
check('the file applies', applied.status === 200, `${applied.status} ${JSON.stringify(applied.data?.detail ?? '')}`);
check('it says it wrote', applied.data?.applied === true);
check('it says who settled them', applied.data?.settled_by === 'Harness Admin', applied.data?.settled_by ?? '');

// ── what the store says afterwards ───────────────────────────────────

const after = await call('GET', '/api/changes');
const now = Object.fromEntries((after.data?.items ?? []).map((x) => [x.id, x]));
check('the open one was settled', now['CR-001']?.status === 'accepted', now['CR-001']?.status);
check('with the reason from the file', now['CR-001']?.resolution === 'Currency goes on the line, not the order.',
  now['CR-001']?.resolution ?? '');
check('and the reference from the file', now['CR-001']?.resolvedRef === 'ADR-021', now['CR-001']?.resolvedRef ?? '');
check('the accepted one advanced to done', now['CR-002']?.status === 'done', now['CR-002']?.status);
check('a blank "because" left the stored reason alone',
  now['CR-002']?.resolution === 'Agreed at the 12 March review.', now['CR-002']?.resolution ?? '');
check('a blank "reference" left the stored one alone',
  now['CR-002']?.resolvedRef === 'ADR-014', now['CR-002']?.resolvedRef ?? '');
check('the blank row is untouched', now['CR-003']?.status === 'open', now['CR-003']?.status);
check('the one that agreed is untouched', now['CR-004']?.status === 'rejected', now['CR-004']?.status);
check('a rejection with no reason wrote nothing', now['CR-005']?.status === 'open', now['CR-005']?.status);
check('a word outside the four wrote nothing', now['CR-006']?.status === 'open', now['CR-006']?.status);

// The same file twice. Everything it settled now agrees with the store, so the
// second pass is all `already` and writes nothing — which is what stops a file
// applied twice moving who settled something to whoever pressed the button.
const again = await send('/api/changes/import/preview', edited);
check('applying the same file again would write nothing',
  again.data?.counts?.settle === 0 && again.data?.counts?.advance === 0,
  JSON.stringify(again.data?.counts));
check('and the rows it settled read as already settled', again.data?.counts?.already === 3,
  JSON.stringify(again.data?.counts));

const settledBefore = now['CR-001']?.resolvedAt;
await send('/api/changes/import/apply', edited, again.data.digest);
const after2 = await call('GET', '/api/changes');
const now2 = Object.fromEntries((after2.data?.items ?? []).map((x) => [x.id, x]));
check('re-applying does not move when it was settled', now2['CR-001']?.resolvedAt === settledBefore,
  `${settledBefore} → ${now2['CR-001']?.resolvedAt}`);

// ── and none of it is open to a stranger ─────────────────────────────

const held = cookie;
cookie = '';
const anonPreview = await send('/api/changes/import/preview', edited);
check('a stranger cannot preview', anonPreview.status === 401, `${anonPreview.status}`);
const anonExport = await fetch(`${API}/api/export/changes`);
check('a stranger cannot download the range', anonExport.status === 401, `${anonExport.status}`);
cookie = held;

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
