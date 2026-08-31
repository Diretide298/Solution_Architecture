/**
 * A box you drop stays where you dropped it — and a box you merely *look at*
 * does not move at all.
 *
 * The ER views — Contracts/ER, DB/Data and the force graph behind Contracts/Graph
 * — re-heat their simulation on *every pointer move* of a drag. So at mouseup the
 * box was handed back to a field still carrying ~0.2 of alpha, and gravity toward
 * the origin, the springs and the collision passes carried it out from under the
 * cursor over the following second and a half. The reader's words for it were
 * "when I move they lose structure due to gravity and floating".
 *
 * **The timing is the whole check.** Reading the position straight after mouseup
 * passes on the broken code — nothing has drifted yet, because the drift is the
 * simulation cooling. So every assertion here reads the position again after a
 * long wait, and the tolerance is two pixels rather than "roughly there".
 *
 * It also holds the way back. An arrangement nothing can undo is a worse diagram
 * than one that drifts, so double-click puts a box back — and what "back" means
 * differs by view, which is why `simulated` is a parameter. On the force graph
 * the node is handed to the field and the proof is that it *moves*. On the box
 * diagrams there is no field any more: the proof is that it lands on the
 * position the layout gave it and then stays there.
 *
 * **The last leg is the one the reader actually reported.** Pinning the dropped
 * box fixed the box you dragged and left every other box free — and `mousedown`
 * re-heated by 0.25, so clicking a table to read it set the whole schema
 * drifting. "It holds structure but as soon as I click a table it gets
 * disturbed." So every view here is also asked to survive a plain click with
 * nothing moving.
 *
 * Needs an admin account and a viewer that is already up. See checks/README.md.
 *
 *   TICVAI_VIEWER=http://127.0.0.1:4620 TICVAI_API=http://127.0.0.1:4620 \
 *     node checks/er-drag-check.mjs
 */
import puppeteer from 'puppeteer-core';
import { authed, VIEWER, API } from './_session.mjs';

/** How far a dropped node may have moved after the simulation has finished. */
const TOLERANCE = 2;
/** Long enough for alpha to decay from a drag's 0.2 to nothing, several times over. */
const SETTLE_MS = 6000;

let pass = 0, fail = 0;
// The detail is the diagnosis, so it is printed on the line that needs one. A
// PASS carrying "fx/fy were not written" reads as a failure that counted as a
// pass, which is the one thing a harness must never look like.
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (!ok && d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};
/** A measurement worth reading whichever way the assertion went. */
const note = (text) => console.log('      ' + text);
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
const round = (v) => Math.round(v * 100) / 100;

await authed(VIEWER + '/api/index'); // fail early and clearly if there is no account

const browser = await puppeteer.launch({
  executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: 'new', args: ['--no-sandbox'],
});

const errors = [];
let CURRENT = 'boot';
const page = await browser.newPage();
await page.setViewport({ width: 1600, height: 1000 });
// The whole point of this harness is to compare a fixed module against a broken
// one on the same URL, so a cached graph.js would report yesterday's answer.
await page.setCacheEnabled(false);
page.on('pageerror', (e) => errors.push(CURRENT + ': ' + e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(CURRENT + ': ' + m.text()); });

// ── sign in and open the package ─────────────────────────────────────
await page.goto(VIEWER + '/invite.html', { waitUntil: 'domcontentloaded' });
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

// Ask the registry which project this deployment opens rather than naming one —
// same reason pages-check does.
const registry = await authed(`${VIEWER.replace(/\/+$/, '')}/pkg/projects`)
  .then((r) => (r.ok ? r.json() : null)).catch(() => null);
const openProject = registry?.default
  ?? registry?.projects?.find((p) => p.active !== false)?.id;
if (!openProject) throw new Error('no project in /pkg/projects — is projects.json empty?');

CURRENT = 'the viewer';
await page.goto(`${VIEWER.replace(/\/+$/, '')}/?project=${encodeURIComponent(openProject)}`,
                { waitUntil: 'domcontentloaded' });
await page.waitForSelector('#layers button', { timeout: 30000 });
await wait(6000);

// ── driving the app ──────────────────────────────────────────────────
const clickLayer = (l) =>
  page.evaluate((x) => document.querySelector('#layers button[data-layer="' + x + '"]')?.click(), l);
const clickMode = (m) =>
  page.evaluate((x) => [...document.querySelectorAll('#modes button')]
    .find((b) => b.dataset.mode === x)?.click(), m);
const clickIn = (sel) => page.evaluate((s) => document.querySelector(s)?.click(), sel);

/** Wait until the named diagram has boxes to drag, or give up. */
async function waitForNodes(key, min = 3, ms = 20000) {
  const until = Date.now() + ms;
  while (Date.now() < until) {
    const n = await page.evaluate((k) => window[k]?.nodes?.length ?? 0, key);
    if (n >= min) return n;
    await wait(400);
  }
  return page.evaluate((k) => window[k]?.nodes?.length ?? 0, key);
}

/**
 * The whole gesture, on one diagram.
 *
 * `key` is the debug handle app.js hangs the renderer off (`__er`, `__data`,
 * `__graph`); `pickKind` names the rule for choosing a node it is safe to click —
 * one whose selection will not rescope the view and rebuild the layout under us,
 * which would make every assertion below meaningless in a way that looks like a
 * pass.
 */
/**
 * @param {boolean} simulated  whether this view still has a force field behind
 *   it. The box diagrams do not — the arrangement is deterministic and nothing
 *   moves it but a hand — so "released" cannot be proved by the node moving.
 */
async function dragHolds({ label, key, canvasId, pickKind, header, simulated = false }) {
  CURRENT = label;

  const plan = await page.evaluate((k, cid, kind) => {
    const d = window[k];
    const rect = document.getElementById(cid).getBoundingClientRect();
    // Named rather than passed as a function: the page has a content policy and
    // `new Function` is not worth finding out about at run time.
    const safe = (n) =>
      kind === 'not-external' ? !n.external
      : kind === 'table' ? String(n.id).startsWith('table:')
      : kind === 'not-selected' ? n.id !== window.__state?.selectedId
      : true;
    const inside = ({ p }) =>
      p.x > rect.width * 0.18 && p.x < rect.width * 0.82 &&
      p.y > rect.height * 0.18 && p.y < rect.height * 0.82;
    const candidates = d.nodes
      .filter(safe)
      .map((n) => ({ n, p: d.toScreen(n.x, n.y) }))
      .filter(inside);
    if (!candidates.length) return null;
    const chosen = candidates[Math.floor(candidates.length / 2)];

    // Aim at the corner furthest from the world origin. Gravity pulls toward the
    // origin, so a drop out there is the drop the broken code cannot hold — and
    // it is also what makes "it moved after the un-pin" a real observation
    // rather than a node already sitting at equilibrium.
    const o = d.toScreen(0, 0);
    const tx = rect.width * (o.x > rect.width / 2 ? 0.14 : 0.86);
    const ty = rect.height * (o.y > rect.height / 2 ? 0.16 : 0.84);
    return {
      from: { x: rect.left + chosen.p.x, y: rect.top + chosen.p.y },
      to: { x: rect.left + tx, y: rect.top + ty },
      candidates: candidates.length,
    };
  }, key, canvasId, pickKind);

  if (!plan) { check(label + ': a node to drag', false, 'no candidate node on screen'); return; }
  if (dist(plan.from, plan.to) < 120) {
    check(label + ': the drag is long enough to mean anything', false,
      `only ${round(dist(plan.from, plan.to))}px`);
    return;
  }

  // ── the drag: press, several moves, release ──
  await page.mouse.move(plan.from.x, plan.from.y);
  await page.mouse.down();
  const id = await page.evaluate((k) => window[k]._drag?.node?.id ?? null, key);
  check(label + ': the press picks up a node', Boolean(id), id ?? 'nothing under the pointer');
  if (!id) { await page.mouse.up(); return; }

  const STEPS = 14;
  for (let i = 1; i <= STEPS; i++) {
    await page.mouse.move(
      plan.from.x + ((plan.to.x - plan.from.x) * i) / STEPS,
      plan.from.y + ((plan.to.y - plan.from.y) * i) / STEPS,
    );
    await wait(18);
  }
  await page.mouse.up();

  const read = () => page.evaluate((k, i) => {
    const n = window[k].byId.get(i);
    return n
      ? { x: n.x, y: n.y, pinned: n.fx != null, alpha: window[k].alpha, gone: false }
      : { gone: true };
  }, key, id);

  const dropped = await read();
  if (dropped.gone) { check(label + ': the dragged node survives the drop', false, id); return; }

  // The mechanism, stated directly: the drop pinned it.
  check(label + ': the drop pins the node', dropped.pinned === true,
    'fx/fy were not written on mouseup');

  // The claim, stated as the reader would see it. **Everything above this line
  // passes on the broken code.**
  await wait(SETTLE_MS);
  const settled = await read();
  const drift = settled.gone ? Infinity : dist(dropped, settled);
  check(label + `: the node is still where it was dropped ${SETTLE_MS / 1000}s later`,
    drift <= TOLERANCE, settled.gone ? 'the node vanished' : '');
  if (!settled.gone) {
    note(`dropped at (${round(dropped.x)}, ${round(dropped.y)}), `
      + `found at (${round(settled.x)}, ${round(settled.y)}) — drift ${round(drift)}px`);
  }

  // A release is only a release if there was a pin. Without this the two
  // assertions below pass on the broken code for the emptiest of reasons —
  // nothing was pinned, so nothing is pinned afterwards either.
  if (!dropped.pinned) {
    check(label + ': double-click releases the pin', false, 'nothing was pinned to release');
    check(label + ': the released node is simulated again', false, 'nothing was pinned to release');
    return;
  }

  // ── the way back: double-click releases it ──
  // Where the node is on screen, asked again between the two clicks. The first
  // click of a double-click selects, and selecting a box in the ER view centres
  // the camera on it — so the second click aimed at the first one's coordinates
  // lands on empty canvas and the gesture never reaches the box.
  const screenAt = () => page.evaluate((k, i, cid, hdr) => {
    const d = window[k];
    const n = d.byId.get(i);
    if (!n) return null;
    const r = document.getElementById(cid).getBoundingClientRect();
    // On a box diagram, aim at the header band: the rows underneath are links,
    // and clicking one navigates instead of selecting.
    const p = d.toScreen(n.x, hdr ? n.y - n.h / 2 + 8 : n.y);
    return { x: r.left + p.x, y: r.top + p.y };
  }, key, id, canvasId, Boolean(header));

  const first = await screenAt();
  await page.mouse.move(first.x, first.y);
  await page.mouse.down({ clickCount: 1 });
  await page.mouse.up({ clickCount: 1 });
  await wait(120);
  const second = await screenAt();
  await page.mouse.move(second.x, second.y);
  await page.mouse.down({ clickCount: 2 });
  await page.mouse.up({ clickCount: 2 });
  await wait(200);

  const released = await read();
  check(label + ': double-click gives the node back',
    !released.gone && released.pinned === false,
    released.gone ? 'the node vanished' : 'fx/fy are still set');

  await wait(3000);
  const after = await read();
  const moved = after.gone ? 0 : dist(released, after);

  if (simulated) {
    // Released is a claim about the simulation, not about a flag, so it is
    // checked against the simulation: a node handed back to a field that is
    // pulling on it moves.
    check(label + ': the released node is simulated again',
      !after.gone && moved > TOLERANCE,
      after.gone ? 'the node vanished' : `it moved only ${round(moved)}px`);
    if (!after.gone) note(`it moved ${round(moved)}px once released`);
  } else {
    // No field to hand it to. "Release" means the layout's own position, and
    // the second half of that sentence is the important one: **and then it
    // stops**. A release that dropped the node somewhere and let it wander
    // would satisfy the first half.
    const home = await page.evaluate((k, i) => {
      const n = window[k].byId.get(i);
      return n && n.lx != null ? { x: n.lx, y: n.ly } : null;
    }, key, id);
    check(label + ': and puts it back where the layout had it',
      Boolean(home) && !released.gone && dist(released, home) <= TOLERANCE,
      home ? `released at (${round(released.x)}, ${round(released.y)}), `
        + `layout says (${round(home.x)}, ${round(home.y)})` : 'the layout kept no position for it');
    check(label + ': and it stays there', !after.gone && moved <= TOLERANCE,
      after.gone ? 'the node vanished' : `it wandered ${round(moved)}px afterwards`);
  }
}

/**
 * Clicking a box reads it. It does not rearrange the diagram.
 *
 * Every node's position before and after, not just the one clicked — the report
 * was about the *others* moving, and an assertion that watched only the box
 * under the cursor would have passed on the broken code, since that one was
 * pinned and the rest were not.
 */
async function clickIsInert({ label, key, canvasId, header = false }) {
  CURRENT = label + ' (click)';
  const before = await page.evaluate((k) => window[k].nodes.map((n) => ({ id: n.id, x: n.x, y: n.y })), key);
  if (before.length < 3) { check(label + ': enough boxes to notice a drift', false, `${before.length}`); return; }

  const target = await page.evaluate((k, cid, hdr) => {
    const d = window[k];
    const rect = document.getElementById(cid).getBoundingClientRect();
    const inside = ({ p }) =>
      p.x > rect.width * 0.15 && p.x < rect.width * 0.85 &&
      p.y > rect.height * 0.15 && p.y < rect.height * 0.85;
    const seen = d.nodes
      .map((n) => ({ n, p: d.toScreen(n.x, hdr ? n.y - n.h / 2 + 8 : n.y) }))
      .filter(inside);
    if (!seen.length) return null;
    const chosen = seen[Math.floor(seen.length / 2)];
    return { x: rect.left + chosen.p.x, y: rect.top + chosen.p.y, id: chosen.n.id };
  }, key, canvasId, header);

  if (!target) { check(label + ': a box to click', false, 'nothing on screen'); return; }

  await page.mouse.click(target.x, target.y);
  // Long enough that a re-heated field would have visibly cooled by now. A read
  // taken straight after the click passes on the broken code for the same reason
  // the drop assertions do.
  await wait(SETTLE_MS);

  const after = await page.evaluate((k) => {
    const at = new Map(window[k].nodes.map((n) => [n.id, n]));
    return [...at].map(([id, n]) => ({ id, x: n.x, y: n.y }));
  }, key);
  const at = new Map(after.map((n) => [n.id, n]));
  let worst = 0;
  let worstId = '';
  for (const b of before) {
    const a = at.get(b.id);
    if (!a) continue;
    const d = dist(b, a);
    if (d > worst) { worst = d; worstId = b.id; }
  }
  check(label + `: clicking a box moves nothing, ${SETTLE_MS / 1000}s later`,
    worst <= TOLERANCE, `${worstId} drifted ${round(worst)}px after a click on ${target.id}`);
  note(`worst drift across ${before.length} boxes: ${round(worst)}px`);
}

// ── Contracts / ER — entities and their fields ───────────────────────
await clickLayer('contracts');
await wait(1800);
await clickMode('er');
await wait(1200);
const erNodes = await waitForNodes('__er');
check('the ER view has entities to drag', erNodes >= 3, `${erNodes} boxes`);
if (erNodes >= 3) {
  await wait(2500); // let the opening layout settle before touching it
  await dragHolds({
    label: 'contracts/er',
    key: '__er',
    canvasId: 'er-canvas',
    header: true,
    // An external box belongs to another contract, and selecting one rescopes
    // the whole diagram — a fresh layout, and nothing left to measure.
    pickKind: 'not-external',
  });
  await clickIsInert({ label: 'contracts/er', key: '__er', canvasId: 'er-canvas', header: true });
}

// ── Contracts / Graph — the force layout, dots rather than boxes ─────
// Only the Local scope is simulated; the other four are drawn or fielded. Local
// is the neighbourhood of the selection, and the ER pass above left one.
CURRENT = 'contracts/graph setup';
// The selection is made here rather than inherited from the leg above. A
// harness whose second claim depends on its first having succeeded reports the
// wrong failure — with the fix stashed this said "the local graph has 0 nodes",
// which is true and tells you nothing about the bug. The deep link is the app's
// own way in, so this drives it rather than reaching past it.
await page.evaluate(() => {
  const nodes = window.__state?.index?.nodes ?? [];
  const node = nodes.find((n) => n.type === 'schema') ?? nodes[0];
  if (node) location.hash = encodeURIComponent(node.id);
});
await wait(1500);
await clickMode('graph');
await wait(1200);
await clickIn('#graph-scope button[data-scope="local"]');
await wait(3000);
const graphNodes = await waitForNodes('__graph', 4, 8000);
check('the local graph has nodes to drag', graphNodes >= 4, `${graphNodes} nodes`);
if (graphNodes >= 4) {
  await wait(2500);
  // The node picked is deliberately not the anchor of the local scope: clicking
  // the anchor re-renders the neighbourhood around itself, and a node set rebuilt
  // under the assertions would make them measure nothing.
  await dragHolds({
    label: 'contracts/graph (local)',
    key: '__graph',
    canvasId: 'graph-canvas',
    pickKind: 'not-selected',
    simulated: true,
  });
}

// ── DB / Data — the same box renderer over database tables ───────────
CURRENT = 'backend/data setup';
await clickLayer('backend');
await wait(1800);
await clickMode('data');
await wait(1200);
await clickIn('#data-layout button[data-layout="boxes"]'); // it opens as a galaxy
await wait(2500);
// Scope it to one schema. The default is every schema at once, whose boxes are
// `schema:` rather than `table:` — and clicking one of those opens that schema,
// which rescopes and relays out the diagram being measured.
await page.evaluate(() => {
  const picker = document.getElementById('data-scope');
  const real = [...picker.options].find((o) => o.value && o.value !== '*');
  if (!real || picker.value === real.value) return;
  picker.value = real.value;
  picker.dispatchEvent(new Event('change'));
});
await wait(3000);
const dataNodes = await waitForNodes('__data');
check('the Data view has tables to drag', dataNodes >= 3, `${dataNodes} boxes`);
if (dataNodes >= 3) {
  await wait(2500);
  await dragHolds({
    label: 'backend/data',
    key: '__data',
    canvasId: 'data-canvas',
    header: true,
    // A `schema:` box opens that schema, which rescopes and relays out.
    pickKind: 'table',
  });
  await clickIsInert({ label: 'backend/data', key: '__data', canvasId: 'data-canvas', header: true });
}

CURRENT = 'teardown';
check('no console or page errors anywhere', errors.length === 0,
  errors.slice(0, 6).join(' | '));

await browser.close();
console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
