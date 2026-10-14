/**
 * Audit the package: does the package pass its own checks, and what did the
 * last drop break.
 *
 * **Opened after a release, by an administrator or the delivery lead.** So it
 * opens on that answer for the release being served, in one sentence, with the
 * figures under it and the first thing to fix. Everything else is further down
 * the rail.
 *
 * **The checks come from the pipeline, not from this page.** Until 14 October
 * the lower half of this page was a checker run typed into its source by hand
 * on 31 August, and five releases later it still said so: a record that cannot
 * update is wrong from the next drop on, however carefully it was written. Now
 * `tools/run-checks.py --json` writes `handoff/checks.json` on every refresh,
 * the release carries it, and `/api/audit` hands it over with which release
 * the run was for (lib/audit.mjs). The 31 August record is kept under History,
 * dated, as what it is.
 *
 * **A run for an older release is said loudly, not quietly.** If nobody has
 * refreshed through refresh-safe since r3, r5's export still holds r3's run; a
 * page that showed it as r5's would be the confident-and-wrong artefact this
 * audit exists to catch. So the banner above the verdict names both releases
 * and says what to do.
 *
 * **On the gate.** The page draws for owners and admins. The server refuses
 * `/api/audit` to everybody else as well (lib/audience.mjs), so the panel a
 * reviewer sees is an explanation and the refusal is at the door.
 */

// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer.
import '/page-chrome.js';
import '/theme.js';
import { hideLoader } from '/loader.js';
import * as auth from '/validation.js';
import { mountPanels } from '/panels.js';
import { el, fmt, plural, daysSince, verdict, next, mountScope, legend, badge, table } from '/sheet.js';

const $ = (id) => document.getElementById(id);

// ── words ───────────────────────────────────────────────────────────
// One state colour per verdict, from the sheet's set: a pass is the finished
// teal, a failure the late red, a report-only warning the held amber. Each is
// always written beside its colour.
const STATUS = {
  pass: { kind: 'done', word: 'Pass', glyph: '' },
  fail: { kind: 'late', word: 'Fail', glyph: '×' },
  warn: { kind: 'stalled', word: 'Warning', glyph: '!' },
};

/** "check-authored-inputs" → "authored inputs": the name a sentence can carry. */
const short = (name) => name.replace(/^(check|audit)-/, '').replace(/-/g, ' ');

const day = (iso) => {
  const t = Date.parse(iso ?? '');
  return Number.isFinite(t) ? new Date(t).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) : '';
};

/** "today", "yesterday", "16 days ago": the sheet's `ago` turns into a date past
 *  a fortnight, which beside the date it came from would say it twice. */
const since = (iso) => {
  const d = daysSince(iso);
  if (d === null) return '';
  return d === 0 ? 'today' : d === 1 ? 'yesterday' : `${d} days ago`;
};

const took = (secs) => {
  if (!Number.isFinite(secs)) return '';
  if (secs < 60) return `${secs.toFixed(1)} s`;
  const min = Math.round(secs / 60);
  return min < 90 ? `${min} min` : `${(secs / 3600).toFixed(1)} h`;
};

const code = (text) => el('code', 'au-code', text);

/** "states, package and authored inputs", or the first three and how many more. */
function names(list) {
  const words = list.map((c) => short(c.name));
  if (words.length > 4) return `${words.slice(0, 3).join(', ')} and ${words.length - 3} more`;
  return words.length > 1 ? `${words.slice(0, -1).join(', ')} and ${words.at(-1)}` : (words[0] ?? '');
}

/** The release a run was for, as a sentence's subject. */
function runLabel(place) {
  if (place.ranFor) return place.ranFor;
  return place.servedTag ? `After ${place.servedTag}` : 'The working tree';
}

// ── reading ─────────────────────────────────────────────────────────
async function load() {
  const r = await auth.apiFetch('/api/audit');
  if (r.status === 403) return { denied: true };
  if (!r.ok) {
    let why = '';
    try { why = (await r.json()).error ?? ''; } catch { /* not JSON: the status says enough */ }
    throw new Error(`/api/audit answered ${r.status}${why ? `: ${why}` : ''}`);
  }
  return r.json();
}

// ── the opening ─────────────────────────────────────────────────────
function drawVerdict(data, scope) {
  const { checks, place, release } = data;
  const served = release.mode === 'tag' ? release.tag : 'the working tree';
  const stale = $('au-stale');
  stale.hidden = true;
  $('au-figure').hidden = true;

  if (!checks || checks.problem) {
    verdict($('au-verdict'), {
      when: `${release.mode === 'tag' ? `Release ${release.tag}` : 'The working tree'} is served`,
      headline: checks?.problem
        ? `The checks run kept with ${served} cannot be read.`
        : `No checks run is kept with ${served}.`,
      pill: { tone: 'warn', text: 'No record' },
      pace: checks?.problem
        ? `${checks.problem}. Nothing on this page can say whether the package passes until it is written again.`
        : `Nothing has written ${data.file} into this release yet, so this page cannot say whether it passes its checks.`,
    });
    next($('au-next'), [
      'Run the refresh with ', code('bash tools/refresh-safe.sh'),
      `. It writes ${data.file} from the run it judges, and the next release carries it.`,
    ]);
    return;
  }

  const all = checks.checks;
  const failing = all.filter((c) => c.status === 'fail');
  const warning = all.filter((c) => c.status === 'warn');
  const passing = all.filter((c) => c.status === 'pass');
  const ran = day(checks.ranAt);

  // Loud when the run is for an older release than the one served: the
  // verdict below is then about something nobody is building against.
  if (place.stale) {
    stale.hidden = false;
    stale.replaceChildren(
      el('strong', '', place.how === 'git'
        ? `These checks ran on ${place.ranFor}; ${served} is served.`
        : `These checks ran on ${ran}, before ${place.ranFor} was tagged; ${served} is served.`),
      ' Run the refresh (',
      code('bash tools/refresh-safe.sh'),
      ') and release it, so this page describes what people are building against.',
    );
  }

  const label = runLabel(place);
  const headline = failing.length
    ? `${label}: ${failing.length} of ${plural(all.length, 'check')} fail (${names(failing)}).`
    : `${label}: all ${plural(all.length, 'check')} pass.`;

  const pace = [`Last run ${ran} (${since(checks.ranAt)}), ${plural(all.length, 'check')} in ${took(checks.seconds)}.`];
  if (warning.length) {
    pace.push(` ${plural(warning.length, 'report-only check')} answered with something for a person to judge (${names(warning)}); ${warning.length === 1 ? 'it does' : 'they do'} not stop a release.`);
  }
  if (place.newer) pace.push(` The run is newer than ${served}: it is of work not released yet.`);
  if (checks.dirty) pace.push(' The run was taken with uncommitted changes in the package.');

  const accepted = failing.filter((c) => c.baseline);
  const sayings = [];
  if (accepted.length) {
    sayings.push(`${names(accepted)} ${accepted.length === 1 ? 'fails' : 'fail'} only with findings the refresh baseline already accepts, so the refresh merged anyway.`);
  }
  if (checks.source === 'log') {
    sayings.push(`This run was read back from a printed table (${checks.log ?? 'a log'}), which keeps each check's last line only, so first findings and fix files are not known.`);
  }

  verdict($('au-verdict'), {
    when: [
      el('strong', '', release.mode === 'tag' ? `Release ${release.tag} is served` : 'The working tree is served'),
      el('span', '', `· checks from ${data.file}`),
    ],
    headline,
    headlineId: 'au-headline',
    pill: failing.length
      ? { tone: 'bad', text: `${fmt(failing.length)} failing` }
      : { tone: 'ok', text: 'Passing' },
    pace: pace.join(''),
    ledger: [
      { label: 'Pass', value: passing.length, swatch: 'done' },
      { label: 'Fail', value: failing.length, swatch: 'late', bad: failing.length > 0 },
      { label: 'Warnings', value: warning.length, swatch: 'stalled', title: 'Report-only checks that answered with something to judge; they never stop a release' },
      { label: 'Run', value: ran || '—', unit: checks.source === 'log' ? 'from a log' : '' },
      {
        label: 'Release',
        value: place.ranFor ?? (place.servedTag ? 'unreleased' : 'working tree'),
        unit: place.current ? 'served' : (place.servedTag ? `${place.servedTag} served` : ''),
        bad: place.stale,
        title: place.how === 'date'
          ? 'Worked out from the run date: the first release tagged after the run'
          : 'Worked out from the commit the run sat on',
      },
    ],
    saying: sayings.join(' '),
  });

  drawStrip(all, scope);

  const first = failing[0];
  if (first) {
    const parts = [el('strong', '', first.name), ` fails with ${findingWords(first)}.`];
    if (first.first?.length) parts.push(' The first: ', code(first.first[0].replace(/\s+/g, ' ')), '.');
    if (first.fix) parts.push(' Fix it in ', code(first.fix), '.');
    else parts.push(' Run ', code(`python3 tools/${first.name}.py`), ' to see its findings.');
    next($('au-next'), parts);
  } else {
    next($('au-next'), place.stale
      ? ['Nothing failed in that run, but it is not ', served, '’s. Run the refresh to check what is served.']
      : 'Nothing to fix. The next run is the refresh before the next release.');
  }
}

/** check-authored-inputs counts inputs gone stale, not errors, and says so. */
const errorWord = (c) => (/\bstale\b/i.test(c.summary ?? '') ? 'stale input' : 'error');

function findingWords(c) {
  const bits = [];
  if (c.errors) bits.push(plural(c.errors, errorWord(c)));
  if (c.warnings && c.status !== 'pass') bits.push(plural(c.warnings, 'warning'));
  return bits.join(' and ') || `exit code ${c.rc}`;
}

// ── the check strip: the page's one bold thing ─────────────────────
/**
 * One mark per check, in the order the run takes them, coloured and marked by
 * its verdict. What the page filter leaves out is dimmed rather than removed,
 * so the strip keeps its shape and still reads as the whole run.
 */
function drawStrip(all, scope) {
  const strip = $('au-strip');
  strip.replaceChildren();
  strip.setAttribute('role', 'img');
  const counts = { pass: 0, fail: 0, warn: 0 };
  for (const c of all) {
    counts[c.status] = (counts[c.status] ?? 0) + 1;
    const s = STATUS[c.status] ?? STATUS.fail;
    const mark = el('span', `au-mark sh-fill-${s.kind} is-${c.status}`, s.glyph);
    mark.title = `${c.name}: ${s.word.toLowerCase()}${c.status !== 'pass' ? `, ${findingWords(c)}` : ''}`;
    mark.dataset.name = c.name;
    strip.append(mark);
  }
  strip.setAttribute('aria-label',
    `${all.length} checks: ${counts.pass} pass, ${counts.fail} fail, ${counts.warn} warn`);

  const key = $('au-strip-key');
  key.replaceChildren(legend([
    { kind: 'done', label: 'Pass', value: counts.pass },
    { kind: 'late', label: 'Fail', value: counts.fail },
    { kind: 'stalled', label: 'Warning (report only)', value: counts.warn },
  ]));

  // The marks that are not passing, by name: what a reader looks for in the
  // strip, said in words, and a way into the table filtered to that check.
  const named = all.filter((c) => c.status !== 'pass');
  if (named.length) {
    const list = el('ul', 'au-strip-names');
    for (const c of named) {
      const li = el('li');
      const b = el('button', 'au-name', '');
      b.type = 'button';
      b.append(badge(STATUS[c.status].kind, STATUS[c.status].word), ` ${c.name}`);
      b.title = `Show ${c.name} in the table of checks`;
      b.onclick = () => { scope.set({ q: c.name, show: '' }); showSection('checks'); };
      li.append(b);
      list.append(li);
    }
    key.append(list);
  }

  $('au-strip-twin').replaceChildren(table({
    caption: 'Every check and its verdict, the strip as a table',
    srOnly: true,
    columns: [
      { key: 'name', label: 'Check' },
      { key: 'status', label: 'Verdict', render: (c) => STATUS[c.status]?.word ?? c.status },
    ],
    rows: all,
  }));
  $('au-figure').hidden = false;
  dimStrip(scope.state);
}

function dimStrip(state) {
  const keep = new Set(filtered(state).map((c) => c.name));
  for (const mark of $('au-strip').children) mark.classList.toggle('is-dim', !keep.has(mark.dataset.name));
}

// ── the page's filter ───────────────────────────────────────────────
let DATA = null;
let showSection = () => {};
let checksTable = null;

function filtered(state) {
  const all = DATA?.checks?.checks ?? [];
  const q = (state.q ?? '').toLowerCase();
  return all.filter((c) => (!state.show || c.status === state.show) && (!q || c.name.toLowerCase().includes(q)));
}

function says(state) {
  const all = DATA?.checks?.checks ?? [];
  if (!all.length) return '';
  const shown = filtered(state);
  const what = { fail: 'failing ', warn: 'report-only ', pass: 'passing ' }[state.show] ?? '';
  const named = state.q ? ` whose name has “${state.q}”` : '';
  if (!state.show && !state.q) return `Showing all ${plural(all.length, 'check')} in the run.`;
  if (!shown.length) return `No ${what}checks${named}, of ${fmt(all.length)}. Show everything to see the whole run.`;
  return `Showing ${shown.length === 1 ? 'the one' : `the ${fmt(shown.length)}`} ${what}${shown.length === 1 ? 'check' : 'checks'}${named}, of ${fmt(all.length)}.`;
}

// ── every check ─────────────────────────────────────────────────────
function drawChecks(data) {
  const note = $('au-checks-note');
  const host = $('au-checks-table');
  const checks = data.checks;
  if (!checks || checks.problem) {
    note.textContent = '';
    host.replaceChildren(el('p', 'sh-empty',
      `There is no checks run to list. Run the refresh (bash tools/refresh-safe.sh); it writes ${data.file}, and the next release carries it.`));
    checksTable = null;
    return;
  }
  note.textContent = `In the order the run takes them. A failing check stops a release unless the refresh baseline already names its findings; a warning comes from a report-only check, which asks a person to judge and never stops one. ${checks.source === 'log' ? 'This run came from a printed table, so the first finding is its last line.' : ''}`.trim();

  checksTable = table({
    caption: `${plural(checks.checks.length, 'check')}, run ${day(checks.ranAt)}`,
    empty: 'No check matches the filter. Show everything to see the whole run.',
    columns: [
      {
        key: 'name', label: 'Check', sort: (c) => c.name,
        render: (c) => {
          const box = el('span', 'au-check');
          box.append(el('span', 'au-check-name', c.name));
          // The reason is a sentence or four; the column says what it is and
          // the reason is a hover away, so the table stays a table.
          if (c.reportOnly) {
            const why = el('span', 'sh-quiet au-check-why', 'Report only');
            why.title = `Report only: ${c.reportOnly}.`;
            box.append(why);
          }
          return box;
        },
      },
      {
        key: 'status', label: 'Status', nowrap: true,
        sort: (c) => ({ fail: 0, warn: 1, pass: 2 }[c.status] ?? 3),
        render: (c) => {
          const box = el('span', 'au-status');
          box.append(badge(STATUS[c.status]?.kind ?? 'late', STATUS[c.status]?.word ?? c.status));
          if (c.baseline) {
            const b = el('span', 'sh-quiet', 'accepted by the baseline');
            b.title = c.baseline;
            box.append(b);
          }
          return box;
        },
      },
      {
        key: 'findings', label: 'Findings', num: true,
        sort: (c) => (c.status === 'pass' ? (c.warnings ?? 0) : (c.errors ?? 0) * 1e6 + (c.warnings ?? 0)),
        render: (c) => {
          const box = el('span', 'au-findings');
          if (c.status !== 'pass' && c.errors != null) box.append(el('span', '', plural(c.errors, errorWord(c))));
          if (c.warnings) box.append(el('span', 'sh-quiet', plural(c.warnings, 'warning')));
          if (!box.childElementCount) box.append(el('span', 'sh-quiet', c.status === 'pass' ? 'none' : `exit ${c.rc}`));
          return box;
        },
      },
      {
        key: 'first', label: 'First finding',
        render: (c) => {
          if (c.first?.length) {
            const box = el('span', 'au-first');
            for (const line of c.first) box.append(el('code', 'au-code au-line', line.replace(/\s+/g, ' ')));
            return box;
          }
          return el('span', c.status === 'pass' ? 'sh-quiet' : 'au-summary', c.summary || '');
        },
      },
      {
        key: 'fix', label: 'Fix file',
        render: (c) => (c.fix ? code(c.fix) : el('span', 'sh-quiet', c.status === 'pass' ? '' : 'not named')),
      },
      { key: 'seconds', label: 'Took', num: true, sort: (c) => c.seconds ?? 0, render: (c) => took(c.seconds) },
    ],
    rows: [],
    rowClass: (c) => `is-${c.status}`,
  });
  host.replaceChildren(checksTable);
}

function redrawFiltered(state) {
  if (checksTable) checksTable.redraw(filtered(state));
  if (DATA?.checks?.checks) dimStrip(state);
}

// ── the package as it stands ────────────────────────────────────────
function drawLive(live) {
  const half = live.tables / 2;
  const rows = [
    {
      what: 'Design boards on disk', now: fmt(live.boards),
      means: `${plural(live.frames, 'frame')}; ${plural(live.unwired, 'board')} no screen points at.`,
    },
    {
      what: 'Screens the package declares', now: fmt(live.screens),
      means: live.screensDrawn
        ? `${fmt(live.screensDrawn)} drawn by a hand-made pack, the rest generated.`
        : 'All generated; none is drawn by a hand-made pack.',
    },
    {
      what: 'Rows on the workbook’s Scaling sheet', now: fmt(live.scalingRows), bad: live.scalingRows === 0,
      means: live.scalingRows === 0
        ? 'None, and there should be one per contract. The DB routing view has nothing to draw, so the read and write routing behind ADR-0016 goes unchecked.'
        : 'The read and write routing behind ADR-0016.',
    },
    {
      what: 'Tables with DDL in backend/', now: `${fmt(live.withDdl)} of ${fmt(live.tables)}`,
      means: 'Read from the migrations, not from the workbook, so this figure is sound.',
    },
    {
      what: 'Tables marked “Foreign writers”', now: `${fmt(live.foreignWriters)} of ${fmt(live.tables)}`,
      bad: live.tables > 0 && live.foreignWriters > half,
      means: live.foreignWriters > half
        ? 'More than half, which is a symptom, not a fact: with no service map every writer looks foreign. It should be the few tables another service really appends to.'
        : 'Tables another service may append to.',
    },
  ];
  $('au-live-table').replaceChildren(table({
    caption: 'Counted from the served release when the page opened',
    columns: [
      { key: 'what', label: 'Figure' },
      { key: 'now', label: 'Now', num: true, cellClass: (r) => (r.bad ? 'is-late' : '') },
      { key: 'means', label: 'What it means' },
    ],
    rows,
  }));
}

// ── what came before ────────────────────────────────────────────────
/**
 * The 31 August record, kept whole and closed. It was the page's lower half
 * for six weeks; it is history now, and dated as such, so nobody mistakes its
 * findings for the current run.
 */
function drawHistory() {
  const entry = el('details', 'au-entry');
  const summary = el('summary');
  summary.append(el('strong', '', '31 August 2026'), ' · validators run by hand, before the checks were kept');
  entry.append(summary);
  const body = el('div', 'au-entry-body');
  const p = (text, cls = 'au-p') => { const n = el('p', cls); n.append(...[].concat(text)); return n; };
  const h = (text) => el('h3', 'au-h3', text);
  const t = (head, rows) => table({
    columns: head.map((label, i) => ({ key: String(i), label, render: (r) => r[i] })),
    rows,
  });

  body.append(
    p('Run at a shell on the dump that landed that day, against the previous dump in git. Nothing in the viewer ran Python then, which is why this was written into the page by hand.', 'sh-note'),
    h('The gate was shut, and that dump shut it harder'),
    p(['tools/refresh.sh is set -euo pipefail. Line 59 was build-status.py, and it exited 1:']),
    el('pre', 'au-pre', "metric 'State models' reports 124 of 122: the numerator and denominator are\ncounting different sets, and every figure derived from it is wrong"),
    p('So the script stopped there, and everything after line 59 never ran: derive-overview.py, derive-mirrors.py, sync-counts.py and the loop that ran all ten validators. The previous dump read 123 of 122; this one added a state model and the denominator stayed.'),
    p(['docs/active/renames-26-august.md said, in bold, ', el('strong', '', '“All nine validators pass.”'), ' They did not, and they did not run.']),
    h('What the validators said when run by hand'),
    t(['Validator', 'Previous dump', 'That dump', 'Change'], [
      ['check-states', '1 error', '4 errors', '3 more, all redemption-right.yaml'],
      ['check-package', '0 errors', '2 errors', '2 more, both rename leftovers'],
      ['check-wireframes', '15 warnings', '42 warnings', '27 boards nothing points at'],
      ['The other seven', 'unchanged', 'unchanged', ''],
    ]),
    p('Six “mirror is out of sync” errors from check-package are left out: the comparison copy excluded repos/, so they were not comparable. They were a symptom of derive-mirrors.py never running.', 'au-fine'),
    h('Every new error was one cause: the rename deleted nothing'),
    t(['Still on disk', 'The replacement that was added'], [
      [code('states/redemption-right.yaml'), code('states/cross-region-entitlement.yaml')],
      [code('diagrams/lld/lifecycles/redemption-right.yaml'), code('…/cross-region-entitlement.yaml')],
      [code('diagrams/lld/services/CrossCellService.yaml'), code('…/CrossRegionService.yaml')],
      [code('diagrams/lld/services/ControlService.yaml'), code('…/PlatformService.yaml')],
    ]),
    h('The workbook builder still read from /home/claude'),
    p('Three globs in tools/build-schema-workbook.py pointed at a machine the workbook is not built on. They matched nothing and nothing failed: the tool carried on with empty sets and wrote a workbook that looked complete.'),
    t(['Line', 'Path', 'What it silently produced'], [
      ['50', code('/home/claude/…/Ticvai.Migrations/Scripts/V*.sql'), '0 of 379 tables marked Written'],
      ['53', code('/home/claude/ticvai/ticvai-contracts/openapi'), 'A Scaling sheet with no contract rows'],
      ['171', code('/home/claude/ticvai-pkg/handoff/service-decomposition.json'), '321 of 379 tables given “Foreign writers”'],
    ]),
    h('What that dump got right'),
    p('35 new boards, five new source documents, three new tools, and a rename that was well reasoned and well documented: it was the cleanup that was missing, not the thinking. The two changes it asked for were written up as diffs in viewer/handoff/package-diffs-31aug.md.'),
  );
  entry.append(body);
  $('au-history').replaceChildren(entry);
}

// ── the page ────────────────────────────────────────────────────────
let scope = null;

async function read() {
  const error = $('au-error');
  error.hidden = true;
  $('au-asof').textContent = 'Reading…';
  try {
    const data = await load();
    if (data.denied) return deny();
    DATA = data;
    const served = data.release.mode === 'tag' ? `${data.release.tag}, the release being served` : 'the working tree, which is being served';
    $('au-lede').textContent = `Reads ${data.file} from ${served}. The refresh writes it after every checks run, and each release carries its own.`;
    scope.redraw();
    drawVerdict(data, scope);
    drawChecks(data);
    redrawFiltered(scope.state);
    drawLive(data.live);
    $('au-asof').textContent = `Read at ${new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}`;
    $('au-asof').classList.remove('is-failed');
  } catch (e) {
    error.textContent = `Could not read the audit: ${e.message}. Read again in a moment; if it keeps failing, the viewer’s log says why.`;
    error.hidden = false;
    $('au-asof').textContent = 'Not read';
    $('au-asof').classList.add('is-failed');
  }
}

function deny() {
  $('audit').hidden = true;
  $('denied').hidden = false;
}

(async function start() {
  // A session first: without one requireSignIn has already sent the reader
  // to the sign-in page, and drawing anything here would flash under it.
  if (!(await auth.requireSignIn())) return hideLoader();
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';

  if (!auth.isAdmin(me)) {
    deny();
    return hideLoader();
  }

  $('audit').hidden = false;
  showSection = mountPanels({ nav: document.querySelector('#audit .set-nav'), fallback: 'verdict' });
  scope = mountScope({
    root: $('au-scope'),
    fields: [
      {
        key: 'show', label: 'Show', kind: 'switch',
        options: [['', 'All'], ['fail', 'Failing'], ['warn', 'Warnings'], ['pass', 'Passing']],
      },
      { key: 'q', label: 'Check name', kind: 'search', placeholder: 'states, package…' },
    ],
    says,
    onChange: redrawFiltered,
  });
  $('au-reload').onclick = read;
  drawHistory();
  await read();
  hideLoader();
})();
