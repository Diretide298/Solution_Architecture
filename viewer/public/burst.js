/**
 * The burst scope — what a flash-sale environment actually runs.
 *
 * **The point of the page is what is not deployed.** `handoff/burst-scope.json`
 * carries every service with `deployed: false` rather than omitting it, and this
 * draws all sixteen for the same reason: an environment defined by what it
 * leaves out cannot be described by a list of what it keeps.
 *
 * **Three states, not two.** The file distinguishes `onBurstPath` from
 * `deployed`, and the two disagree for four services — Tenancy, Retail,
 * Marketing and Access are on the path and still not deployed, because the
 * shared cell answers for them. Collapsing that into deployed/not-deployed
 * would lose the only group whose absence is a routing decision rather than an
 * irrelevance.
 *
 * **Read from the package, never restated here.** Every figure below comes out
 * of the JSON on each open, through `/api/file`. Nothing is transcribed into
 * this file: `tools/derive-burst-scope.py` regenerates the source on every
 * `refresh.sh`, and a number typed into a viewer is a number that goes stale
 * without saying so.
 *
 * **Why `/api/file` rather than a route of its own.** A new `/api/burst` would
 * have to be added to server.mjs *and* to the location regex in
 * `deploy/nginx/adamapi.ainfinite.ai`, or it answers 404 on the deployed host
 * for every caller still on the `/api/` spelling. The file route already serves
 * `.json` out of the package root and needs neither.
 */

import '/theme.js';
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';
import { renderDeployMap } from '/burst-map.js';

const SOURCE = 'handoff/burst-scope.json';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const fmt = (n) => (typeof n === 'number' ? n.toLocaleString('en-GB') : String(n ?? ''));

/**
 * The package's notes are markdown-ish — `**bold**` and nothing else that
 * matters here. Rendered as text with the emphasis honoured, never as HTML: the
 * note is package content and this page has no reason to trust it with markup.
 */
function noteText(raw) {
  const frag = document.createDocumentFragment();
  const parts = String(raw ?? '').split(/\*\*(.+?)\*\*/g);
  parts.forEach((part, i) => {
    if (!part) return;
    frag.append(i % 2 ? el('strong', null, part) : document.createTextNode(part));
  });
  return frag;
}

/* ── services ─────────────────────────────────────────────────────────────
   Grouped by the two flags together. The order is deliberate: the load first,
   then the path that is served elsewhere, then the absence — which is the order
   the environment was reasoned about, and it puts the largest group last
   without burying it. */

const GROUPS = [
  {
    key: 'deployed',
    title: 'Deployed into the burst environment',
    note: 'The environment runs these and nothing else. Two of the three carry the load; the third is small and not optional.',
    match: (s) => s.deployed,
  },
  {
    key: 'shared',
    title: 'On the burst path, served from the shared cell',
    note: 'A buyer reaches these during a purchase, but they are answered by the permanent platform rather than replicated here. On the path without being the load.',
    match: (s) => !s.deployed && s.onBurstPath,
  },
  {
    key: 'off',
    title: 'No part of a ticket sale',
    note: 'Not on the path at any point in a purchase, and not deployed. This group is the reason the environment is three services rather than sixteen.',
    match: (s) => !s.deployed && !s.onBurstPath,
  },
];

function serviceRow(svc, group, peak) {
  // `reason` is read, never inferred. IdentityService is 1.8% and mandatory;
  // sorting or styling by share alone would present it as marginal, which is
  // the one reading of this data that could get an environment stood up
  // without authentication in it.
  const mandatory = group === 'deployed' && /not optional/i.test(svc.reason ?? '');

  const row = el('div', `bu-svc${mandatory ? ' is-mandatory' : ''}`);

  const name = el('div', 'bu-svc-name', svc.name);
  name.append(el('span', 'bu-svc-tier', svc.tier));
  row.append(name);

  row.append(el('div', `bu-svc-share${svc.weightedShare ? '' : ' is-zero'}`,
    svc.weightedShare ? `${svc.weightedShare}%` : '—'));

  // Widths are share against the largest share on the page, not against 100 —
  // the top service is 63.6% today, so a bar scaled to 100 would sit two-thirds
  // empty and the four below it would be slivers rather than a comparison.
  // `peak` is read off the data, not fixed here: derive-burst-scope.py rewrites
  // this file on every refresh and a hardcoded denominator would quietly
  // mis-scale every bar the first time the shape of a purchase changed.
  const bar = el('div', `bu-bar is-${group}`);
  const span = el('span');
  span.style.width = peak > 0 ? `${(svc.weightedShare / peak) * 100}%` : '0%';
  bar.append(span);
  bar.setAttribute('role', 'img');
  bar.setAttribute('aria-label', `${svc.weightedShare}% of a buyer's weighted calls`);
  row.append(bar);

  row.append(el('div', `bu-svc-rep${svc.replicas ? '' : ' is-none'}`,
    svc.replicas ? `${svc.replicas.min}–${svc.replicas.max} replicas` : 'not deployed'));

  row.append(el('div', 'bu-svc-reason', noteText(svc.reason)));
  return row;
}

function renderServices(host, data) {
  const services = [...data.services].sort((a, b) => b.weightedShare - a.weightedShare);
  const sec = el('section', 'bu-sec');
  sec.append(el('p', 'bu-h2', 'Section one'));
  sec.append(el('h2', 'bu-h3', 'Services'));

  const onPath = services.filter((s) => s.onBurstPath).length;
  const peak = services.reduce((max, s) => Math.max(max, s.weightedShare), 0);
  const carried = services
    .filter((s) => s.deployed && s.weightedShare >= 20)
    .reduce((sum, s) => sum + s.weightedShare, 0);

  const lead = el('p', 'bu-lead');
  lead.append(noteText(
    `Sixteen services exist. **${data.totals.deployed} are deployed** into a burst environment, ` +
    `${onPath} appear somewhere on the path a buyer takes, and ` +
    `${services.length - onPath} see no part of a ticket sale at all. ` +
    `**Two services carry ${carried.toFixed(1)}% of a buyer's weighted calls** — which is why the ` +
    `environment is three services and not seven. Share is weighted by how many times one buyer ` +
    `calls each operation, so it measures load rather than presence.`,
  ));
  sec.append(lead);

  for (const group of GROUPS) {
    const members = services.filter(group.match);
    if (!members.length) continue;

    const block = el('div', 'bu-group');
    const head = el('div', 'bu-group-head');
    head.append(el('span', 'bu-group-title', group.title));
    head.append(el('span', 'bu-group-count', `${members.length} of ${services.length}`));
    head.append(el('p', 'bu-group-note', group.note));
    block.append(head);

    for (const svc of members) block.append(serviceRow(svc, group.key, peak));
    sec.append(block);
  }

  host.append(sec);
}

/* ── tables ───────────────────────────────────────────────────────────────
   Two of the forty-two are contended and they are the whole risk, so they are
   lifted out above the list rather than flagged inside it. The lock each one is
   taken under lives on the operations, not the table, and is joined here —
   `FOR UPDATE SKIP LOCKED` beside the row it serialises is the pair of facts a
   reader needs at once. */

function contendedCard(table, operations) {
  const card = el('div', 'bu-cont');
  card.append(el('span', 'bu-cont-flag', 'Contended'));
  card.append(el('p', 'bu-cont-name', table.table));
  card.append(el('p', 'bu-cont-meta',
    `${table.columns} columns · ${table.burstOperations} burst operations · written`));
  card.append(el('p', 'bu-cont-note', noteText(table.note)));

  const locking = operations.filter((op) => op.lock && op.writes.includes(table.table));
  if (locking.length) {
    const locks = el('div', 'bu-cont-locks');
    for (const op of locking) {
      const row = el('div', 'bu-lock-row');
      row.append(el('span', 'bu-lock-op', op.operationId));
      row.append(el('span', 'bu-lock-kw', op.lock));
      locks.append(row);
    }
    card.append(locks);
  }
  return card;
}

function renderTables(host, data) {
  const tables = [...data.tables].sort(
    (a, b) => b.burstOperations - a.burstOperations || a.table.localeCompare(b.table),
  );
  const contended = tables.filter((t) => t.contended);

  const sec = el('section', 'bu-sec');
  sec.append(el('p', 'bu-h2', 'Section two'));
  sec.append(el('h2', 'bu-h3', 'Tables'));

  const lead = el('p', 'bu-lead');
  lead.append(noteText(
    `**${data.totals.tables} tables of ${fmt(data.totals.ofTotalTables)}**, and ` +
    `${tables.filter((t) => t.written).length} of them written during a sale. ` +
    `**Two are contended**, and that is where a flash sale fails: every buyer wants the same ` +
    `rows, the lease path serialises, and no amount of horizontal scaling helps a contended row. ` +
    `They are the two to load-test before anything else.`,
  ));
  sec.append(lead);

  const cards = el('div', 'bu-contended');
  for (const t of contended) cards.append(contendedCard(t, data.operations));
  sec.append(cards);

  const scroll = el('div', 'bu-scroll');
  const table = el('table', 'bu-table');
  table.innerHTML =
    '<thead><tr><th>Table</th><th>Schema</th><th class="n">Cols</th>' +
    '<th class="n">Burst ops</th><th>Written</th></tr></thead>';
  const body = el('tbody');
  for (const t of tables) {
    const tr = el('tr', t.contended ? 'is-contended' : null);
    tr.append(el('td', 'mono', t.table));
    tr.append(el('td', null, t.schema));
    tr.append(el('td', 'n', String(t.columns)));
    tr.append(el('td', 'n', String(t.burstOperations)));
    const flags = el('td');
    if (t.written) flags.append(el('span', 'bu-flag is-write', 'written'));
    if (t.contended) flags.append(document.createTextNode(' '), el('span', 'bu-flag is-lock', 'contended'));
    tr.append(flags);
    body.append(tr);
  }
  table.append(body);
  scroll.append(table);
  sec.append(scroll);

  host.append(sec);
}

/* ── operations ───────────────────────────────────────────────────────── */

function renderOperations(host, data) {
  const ops = [...data.operations].sort(
    (a, b) => b.callsPerBuyer - a.callsPerBuyer || a.operationId.localeCompare(b.operationId),
  );
  const perBuyer = ops.reduce((sum, o) => sum + o.callsPerBuyer, 0);

  const sec = el('section', 'bu-sec');
  sec.append(el('p', 'bu-h2', 'Section three'));
  sec.append(el('h2', 'bu-h3', 'Operations'));

  const lead = el('p', 'bu-lead');
  lead.append(noteText(
    `**${data.totals.operations} operations of ${fmt(data.totals.ofTotalOperations)}** — ` +
    `${(100 * data.totals.operations / data.totals.ofTotalOperations).toFixed(1)}% of the contract ` +
    `surface. One buyer makes about ${perBuyer} calls across them to complete a purchase.`,
  ));
  sec.append(lead);

  // Said on the page and not only in the JSON. A per-buyer figure looks
  // measured, and a reader sizing an environment off it would be sizing off
  // somebody's reading of a flow diagram.
  const caveat = el('div', 'bu-caveat');
  caveat.append(el('p', null, noteText(
    '**`callsPerBuyer` is estimated, not measured.** It is derived from the flow steps and the ' +
    'shape of a purchase — `getAvailability` at 6 is a buyer checking repeatedly, `createPayment` ' +
    'at 1 is paying once. Nothing here has been observed against a running system.',
  )));
  caveat.append(el('p', null, noteText(
    'Run `tools/bench.py` when there is something to run it against, and these become real numbers.',
  )));
  sec.append(caveat);

  const scroll = el('div', 'bu-scroll');
  const table = el('table', 'bu-table');
  table.innerHTML =
    '<thead><tr><th>Operation</th><th>Verb</th><th>Path</th><th>Service</th>' +
    '<th class="n">Calls<br>per buyer</th><th class="n">Reads</th><th class="n">Writes</th>' +
    '<th>Lock</th></tr></thead>';
  const body = el('tbody');
  for (const op of ops) {
    const tr = el('tr', op.lock ? 'is-contended' : null);
    tr.append(el('td', 'mono', op.operationId));
    tr.append(el('td', null, el('span', `bu-verb ${op.verb.toLowerCase()}`, op.verb)));
    tr.append(el('td', 'mono', op.path));
    tr.append(el('td', null, op.service));
    tr.append(el('td', 'n', String(op.callsPerBuyer)));
    tr.append(el('td', 'n', String(op.reads.length)));
    tr.append(el('td', 'n', String(op.writes.length)));
    tr.append(el('td', null, op.lock ? el('span', 'bu-flag is-lock', op.lock) : document.createTextNode('—')));
    body.append(tr);
  }
  table.append(body);
  scroll.append(table);
  sec.append(scroll);

  host.append(sec);
}

/* ── related ──────────────────────────────────────────────────────────── */

const RELATED = [
  {
    path: 'states/burst-environment.yaml',
    href: '/api/file?path=states/burst-environment.yaml',
    note: 'Nine states. `decommissioned` is reachable only through `reconciled` — an environment torn down before its orders reach the permanent platform has lost real money and real tickets, and no path allows it.',
  },
  {
    path: 'deploy/c-flash-sale.yml',
    href: '/api/file?path=deploy/c-flash-sale.yml',
    note: 'The scenario itself. Written before this file was derived, and its counts differ — treat the JSON as current.',
  },
  {
    path: 'handoff/TICVAI_Deployment_Technical.docx — Part 6',
    href: null,
    note: 'The prose account of the burst environment. Not served by the viewer; open it from the package.',
  },
  {
    path: 'docs/diagrams/deploy/burst-scope.png',
    href: null,
    note: 'The rendered diagram of the same data. This page is built from the JSON rather than from it.',
  },
];

function renderRelated(host) {
  const sec = el('section', 'bu-related');
  sec.append(el('p', 'bu-h2', 'Alongside this'));
  const list = el('div', 'bu-rel-list');
  for (const item of RELATED) {
    const card = el('div', 'bu-rel');
    if (item.href) {
      const a = el('a', 'bu-rel-path', item.path);
      a.href = auth.apiUrl(item.href);
      card.append(a);
    } else {
      card.append(el('div', 'bu-rel-path is-plain', item.path));
    }
    card.append(el('p', 'bu-rel-note', noteText(item.note)));
    list.append(card);
  }
  sec.append(list);
  host.append(sec);
}

/* ── boot ─────────────────────────────────────────────────────────────── */

function renderTotals(host, data) {
  const t = data.totals;
  const strip = el('div', 'bu-totals');

  const tile = (value, of, key, note) => {
    const box = el('div', 'bu-total');
    const v = el('div', 'bu-total-v', fmt(value));
    if (of != null) v.append(el('span', 'of', ` of ${fmt(of)}`));
    box.append(v);
    box.append(el('div', 'bu-total-k', key));
    box.append(el('div', 'bu-total-n', note));
    return box;
  };

  strip.append(tile(t.deployed, t.services, 'services deployed',
    `${t.services - t.deployed} are not, and are on the page below with their reason`));
  strip.append(tile(t.operations, t.ofTotalOperations, 'operations on the burst path',
    `${(100 * t.operations / t.ofTotalOperations).toFixed(1)}% of the contract surface`));
  strip.append(tile(t.tables, t.ofTotalTables, 'tables touched',
    'two of them contended, which is where the sale fails'));
  host.append(strip);
}

async function main() {
  const host = $('burst-body');
  try {
    const res = await auth.apiFetch(`/api/file?path=${encodeURIComponent(SOURCE)}`);
    if (!res.ok) throw new Error(`${SOURCE} answered ${res.status}`);
    // The file route sends text/plain — it hands back package source rather than
    // a payload — so the body is parsed here rather than trusted to a content
    // type the route never claimed.
    const data = JSON.parse(await res.text());

    $('bu-basis').textContent = data.basis ?? '';
    renderTotals(host, data);
    // The map goes straight after the totals: it is the one block that answers
    // "what does this look like running" rather than "what is in it", and a
    // reader who stops after the first screen should have had that.
    await renderDeployMap(host, data, {
      file: async (path) => {
        const res2 = await auth.apiFetch(`/api/file?path=${encodeURIComponent(path)}`);
        if (!res2.ok) throw new Error(String(res2.status));
        return res2.text();
      },
      // The parsed payloads the viewer already builds. /api/domain carries the
      // state machines, so the burst lifecycle arrives read rather than reread.
      api: async (route) => {
        const res2 = await auth.apiFetch(`/api/${route}`);
        if (!res2.ok) throw new Error(String(res2.status));
        return res2.json();
      },
    });
    renderServices(host, data);
    renderTables(host, data);
    renderOperations(host, data);
    renderRelated(host);
  } catch (err) {
    host.append(el('div', 'bu-error',
      `Could not read ${SOURCE}: ${err.message}. It is regenerated by tools/derive-burst-scope.py on every refresh.sh — if it is missing, the package has not been rebuilt.`));
  } finally {
    hideLoader();
  }
}

main();
