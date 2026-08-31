/**
 * The dump audit — what the last delivery brought, and what it broke.
 *
 * **Half of this page is live and half of it is a dated record, and the two are
 * marked apart on the page rather than only here.** The figures the viewer can
 * read for itself — boards on disk, frames, tables with real DDL, rows on the
 * workbook's Scaling sheet — are fetched every time it opens, so they cannot go
 * quietly stale. The findings that came from running the package's own
 * validators by hand cannot be: nothing in the viewer runs Python, and a page
 * that presented a remembered checker run as a current one would be exactly the
 * kind of confident-and-wrong artefact this audit is about.
 *
 * So the checker results carry the date they were taken and say plainly that
 * they are a record. When the next dump lands they are history, and the live
 * block beside them will disagree with them, which is the correct behaviour.
 *
 * **On the gate.** This is an admin page in the same sense `/admin.html` is: the
 * viewer only offers it to an admin, and it refuses to draw for anyone else.
 * That is a UI affordance, not a secret — every number the live block shows
 * comes from `/api/uiux`, `/api/backend` and `/api/journeys`, which any signed-in
 * reader may already call. Nothing here is hidden that is not hidden there. It
 * is admin-only because it is about the delivery process rather than about the
 * product, and a client opening it would learn nothing they wanted to know.
 */

import '/theme.js';
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const json = (path) => auth.apiFetch(path).then((r) => {
  if (!r.ok) throw new Error(`${path} answered ${r.status}`);
  return r.json();
});

/** When the by-hand half of this page was taken. */
const AUDITED = '31 August 2026';

/**
 * A live figure: the number, what it counts, and — where it is a symptom — what
 * it should be.
 */
function figure({ label, value, note, bad = false }) {
  const box = el('div', `au-figure${bad ? ' is-bad' : ''}`);
  box.append(el('p', 'au-figure-label', label));
  box.append(el('p', 'au-figure-value', String(value)));
  if (note) box.append(el('p', 'au-figure-note', note));
  return box;
}

function table(head, rows, className = '') {
  const t = el('table', `au-table ${className}`.trim());
  const thead = el('thead');
  const hr = el('tr');
  for (const h of head) hr.append(el('th', null, h));
  thead.append(hr);
  t.append(thead);
  const tb = el('tbody');
  for (const row of rows) {
    const tr = el('tr');
    for (const cell of row) {
      const td = el('td');
      if (cell instanceof Node) td.append(cell);
      else td.textContent = cell ?? '';
      tr.append(td);
    }
    tb.append(tr);
  }
  t.append(tb);
  return t;
}

const code = (text) => el('code', 'au-code', text);

(async function start() {
  await auth.requireSignIn();
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';

  if (me?.role !== 'admin') {
    // Said, not blanked. A page that renders an empty shell to a reviewer looks
    // broken; this one tells them what it is and that it is not for them.
    $('audit-body').replaceChildren(
      el('p', 'auth-note',
        'This page is for admins. It is a record of how the last delivery package was '
        + 'built and what its own validators say about it — the delivery process rather '
        + 'than the product.'));
    hideLoader();
    return;
  }

  const body = $('audit-body');

  try {
    const [uiux, backend, journeys] = await Promise.all([
      json('/api/uiux'), json('/api/backend'), json('/api/journeys'),
    ]);

    const stats = uiux.stats ?? {};
    const tables = backend.tables ?? [];
    const withDdl = tables.filter((t) => t.ddl).length;
    const scalingRows = Array.isArray(backend.scaling) ? backend.scaling.length : 0;
    const foreign = tables.filter((t) => (t.foreignWriters ?? []).length).length;

    // ── live ──
    body.append(el('h2', 'au-h2', 'Read from the package, now'));
    body.append(el('p', 'au-lead',
      'Every figure in this block is fetched when the page opens. If one of them '
      + 'disagrees with the record below, the record is out of date and this is right.'));

    const figures = el('div', 'au-figures');
    figures.append(figure({
      label: 'Design boards on disk',
      value: stats.boards ?? 0,
      note: `${stats.frames ?? 0} frames · ${stats.unwired ?? 0} boards no screen points at`,
    }));
    figures.append(figure({
      label: 'Screens the package declares',
      value: (journeys.screens ?? []).length,
      note: `${stats.screensDrawn ?? 0} drawn by a hand-made pack, the rest generated`,
    }));
    figures.append(figure({
      label: 'Rows on the workbook’s Scaling sheet',
      value: scalingRows,
      bad: scalingRows === 0,
      note: scalingRows === 0
        ? 'header and a TOTAL of zeros, no contract rows — the DB → Routing view has nothing to draw'
        : 'the read/write routing behind ADR-0016',
    }));
    figures.append(figure({
      label: 'Tables with DDL in backend/',
      value: `${withDdl} of ${tables.length}`,
      note: 'read from the migrations, not from the workbook — this figure is sound',
    }));
    figures.append(figure({
      label: 'Tables marked “Foreign writers”',
      value: `${foreign} of ${tables.length}`,
      bad: foreign > tables.length / 2,
      note: foreign > tables.length / 2
        ? 'with no service map every writer looks foreign — see the workbook finding'
        : 'tables another service may append to',
    }));
    body.append(figures);

    // ── the record ──
    body.append(el('h2', 'au-h2', `Run by hand, ${AUDITED}`));
    const note = el('p', 'au-lead');
    note.append('Nothing in the viewer runs Python, so the package’s own validators cannot be '
      + 'run from this page. These are the results of running them at a shell on the dump that '
      + 'landed that day, against the previous dump in git for comparison. ');
    note.append(el('strong', null, 'This half is a record and does not update.'));
    body.append(note);

    body.append(el('h3', 'au-h3', 'The gate is shut, and this dump shut it harder'));
    const gate = el('div', 'au-callout');
    gate.append(el('p', null,
      'tools/refresh.sh is set -euo pipefail. Line 59 is build-status.py, and it exits 1:'));
    gate.append(el('pre', 'au-pre',
      "metric 'State models' reports 124 of 122 — the numerator and denominator are\n"
      + 'counting different sets, and every figure derived from it is wrong'));
    gate.append(el('p', null,
      'So the script stops there. Everything after line 59 never runs — derive-overview.py, '
      + 'derive-mirrors.py, sync-counts.py, and the loop at the bottom that runs all ten '
      + 'validators. The previous dump read 123 of 122; this one added a state model and the '
      + 'denominator stayed, so the delivery deepened the failure that hides its own errors.'));
    const claim = el('p');
    claim.append('docs/active/renames-26-august.md states, in bold, ');
    claim.append(el('strong', null, '“All nine validators pass.”'));
    claim.append(' They do not, and they did not run — the line that would have printed their '
      + 'output is below the line that stopped.');
    gate.append(claim);
    body.append(gate);

    body.append(el('h3', 'au-h3', 'What the validators say when you run them yourself'));
    body.append(table(
      ['Validator', 'Previous dump', 'This dump', ''],
      [
        ['check-states', '1 error', '4 errors', '+3, all redemption-right.yaml'],
        ['check-package', '0 errors', '2 errors', '+2, both rename leftovers'],
        ['check-wireframes', '15 warnings', '42 warnings', '+27 boards nothing points at'],
        ['the other seven', 'unchanged', 'unchanged', ''],
      ]));
    body.append(el('p', 'au-fine',
      'The six “mirror is out of sync” errors check-package also reports are not in that table: '
      + 'the comparison copy excluded repos/, so they are not comparable. They are a symptom of '
      + 'derive-mirrors.py never running — it is line 63 — rather than a separate fault, and not '
      + 'the parked repos/ policy question.'));

    body.append(el('h3', 'au-h3', 'Every new error is one cause: the rename deleted nothing'));
    body.append(table(
      ['Still on disk', 'The replacement that was added'],
      [
        [code('states/redemption-right.yaml'), code('states/cross-region-entitlement.yaml')],
        [code('diagrams/lld/lifecycles/redemption-right.yaml'), code('…/cross-region-entitlement.yaml')],
        [code('diagrams/lld/services/CrossCellService.yaml'), code('…/CrossRegionService.yaml')],
        [code('diagrams/lld/services/ControlService.yaml'), code('…/PlatformService.yaml')],
      ]));
    body.append(el('p', 'au-fine',
      'The old state model still names cross-cell.RedemptionRight.status, consumeRedemptionRight '
      + 'and revokeRedemptionRight — none of which are in contracts/ any more, because the rename '
      + 'moved them. The new twin passes cleanly. Deleting the four files should clear all six '
      + 'errors, and takes the metric’s numerator to 123.'));

    body.append(el('h3', 'au-h3', 'The workbook builder still reads from /home/claude'));
    body.append(el('p', 'au-lead',
      'Three globs in tools/build-schema-workbook.py point at a machine the workbook is not '
      + 'built on. They match nothing, and nothing fails — the tool carries on with empty sets '
      + 'and writes a workbook that looks complete.'));
    body.append(table(
      ['Line', 'Path', 'What it silently produces'],
      [
        ['50', code('/home/claude/…/Ticvai.Migrations/Scripts/V*.sql'), '0 of 379 tables marked Written'],
        ['53', code('/home/claude/ticvai/ticvai-contracts/openapi'), 'Scaling sheet with no contract rows'],
        ['171', code('/home/claude/ticvai-pkg/handoff/service-decomposition.json'), '321 of 379 tables given “Foreign writers”'],
      ]));
    body.append(el('p', 'au-fine',
      'That 321 is the same 321 the previous dump’s audit reported. The file already defines '
      + '_ROOT and _pkg() at the top and uses them on line 33 — these three lines just do not. '
      + 'The same absolute paths are in build-review-responses.py and build-services-workbook.py; '
      + 'build-status.py and derive-domain.py have a fallback chain and are fine.'));

    body.append(el('h3', 'au-h3', 'What the dump got right'));
    body.append(el('p', 'au-lead',
      '35 new boards, five new source documents, three new tools, and a rename that is '
      + 'well-reasoned and well-documented — it is the cleanup that is missing, not the thinking. '
      + 'The written-versus-planned distinction in the DB layer reads the real SQL in backend/ '
      + 'rather than the workbook column, so it is unaffected by any of the above.'));

    const diffs = el('p', 'au-lead');
    diffs.append('The two changes this asks for are written up as diffs in ');
    diffs.append(code('viewer/handoff/package-diffs-31aug.md'));
    diffs.append(' — the viewer does not write to the package.');
    body.append(diffs);
  } catch (e) {
    body.replaceChildren(el('p', 'auth-note', `Could not read the package: ${e.message}`));
  } finally {
    hideLoader();
  }
})();
