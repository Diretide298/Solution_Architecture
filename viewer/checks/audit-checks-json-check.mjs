/**
 * The checks run as JSON, from the run to the Audit page's sentence.
 *
 * **Why this exists.** The Audit page's verdict is only as true as the file it
 * reads, and that file is written by three hands: `run-checks.py --json` for a
 * plain run, `run-checks.py --from-log` for the logs taken before the JSON
 * existed, and refresh-safe.sh's judge, which runs the baseline checkers itself
 * and has to put them back beside the rest. Then lib/audit.mjs decides which
 * release the run was for. A slip in any of the four shows up as a page that
 * says "all pass" about a run that failed, or calls an r3 run r5's, and nothing
 * else would notice: the human log beside it keeps printing correctly.
 *
 * So each is run for real, against a package made up for the purpose in a
 * temporary folder: three checkers (one passes, one fails naming a file, one
 * is report-only and warns), a copy of run-checks.py with its list pointed at
 * them, and refresh-safe.sh's own helper, cut out of the script the way the
 * script writes it. Nothing here needs the viewer running, and nothing touches
 * the real package.
 *
 *   node checks/audit-checks-json-check.mjs       (PYTHON=python3 where that is its name)
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync, utimesSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { placeChecks, readChecks } from '../lib/audit.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TOOLS = path.join(HERE, '..', '..', 'ticvai', 'tools');
const PY = process.env.PYTHON ?? (process.platform === 'win32' ? 'python' : 'python3');

let pass = 0, fail = 0;
const check = (n, ok, d = '') => {
  console.log((ok ? 'PASS  ' : 'FAIL  ') + n + (!ok && d ? ' — ' + d : ''));
  ok ? pass++ : fail++;
};
const py = (args, cwd) => execFileSync(PY, args, {
  cwd, encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf8' }, stdio: ['ignore', 'pipe', 'pipe'],
});

const root = mkdtempSync(path.join(tmpdir(), 'audit-checks-json-'));
try {
  // ── a package of three checkers ──────────────────────────────────
  const pkg = path.join(root, 'pkg');
  mkdirSync(path.join(pkg, 'tools'), { recursive: true });
  mkdirSync(path.join(pkg, 'handoff'), { recursive: true });
  const tool = (name, body) => writeFileSync(path.join(pkg, 'tools', `${name}.py`), body);
  tool('check-good', 'print("  WARN  a thing to look at")\nprint("PASS — 1 warning(s)")\n');
  tool('check-bad', [
    'import sys',
    'print("  WARN  noise")',
    'print("  FAIL  states/redemption-right.yaml: names unknown operation consumeRedemptionRight")',
    'print("  FAIL  second finding")',
    'print()',
    'print("2 error(s), 1 warning(s)")',
    'sys.exit(1)', '',
  ].join('\n'));
  tool('audit-judged', 'import sys\nprint("  WARN  whether this is a table is a judgement")\nprint("1 untriaged")\nsys.exit(1)\n');
  // run-checks.py as it is, with its list pointed at these three.
  const real = readFileSync(path.join(TOOLS, 'run-checks.py'), 'utf8');
  const pointed = real.replace('\nif __name__ == "__main__":',
    '\nCHECKS[:] = ["check-good", "check-bad", "audit-judged"]\n'
    + 'REPORT_ONLY.clear()\nREPORT_ONLY["audit-judged"] = "a judgement"\n\nif __name__ == "__main__":');
  check('the copy of run-checks.py could be pointed at the made-up checkers', pointed !== real);
  writeFileSync(path.join(pkg, 'tools', 'run-checks.py'), pointed);

  // ── 1. a plain run, --json ───────────────────────────────────────
  const out = path.join(root, 'run.json');
  const table = py([path.join(pkg, 'tools', 'run-checks.py'), '--no-gate', '--json', out], pkg);
  check('the table still prints', /check-bad\s+FAIL rc=1/.test(table) && /1 gate failure/.test(table), table);
  const run = JSON.parse(readFileSync(out, 'utf8'));
  const by = Object.fromEntries(run.checks.map((c) => [c.name, c]));
  check('every checker is in the JSON, in the run\'s order',
    run.checks.map((c) => c.name).join() === 'check-good,check-bad,audit-judged', run.checks.map((c) => c.name).join());
  check('the totals count pass, fail and warn',
    run.totals.run === 3 && run.totals.pass === 1 && run.totals.fail === 1 && run.totals.warn === 1, JSON.stringify(run.totals));
  check('a failing checker is a fail with its error and warning counts',
    by['check-bad'].status === 'fail' && by['check-bad'].errors === 2 && by['check-bad'].warnings === 1 && by['check-bad'].gates,
    JSON.stringify(by['check-bad']));
  check('its first findings are its FAIL lines, not its warnings',
    by['check-bad'].first.length === 2 && by['check-bad'].first[0].startsWith('FAIL  states/'), JSON.stringify(by['check-bad'].first));
  check('and the fix file is the path the first finding names',
    by['check-bad'].fix === 'states/redemption-right.yaml', by['check-bad'].fix);
  check('a report-only checker answering non-zero is a warning that does not gate',
    by['audit-judged'].status === 'warn' && !by['audit-judged'].gates && by['audit-judged'].reportOnly === 'a judgement',
    JSON.stringify(by['audit-judged']));
  check('a passing checker is a pass with no first findings',
    by['check-good'].status === 'pass' && by['check-good'].first.length === 0 && by['check-good'].warnings === 1,
    JSON.stringify(by['check-good']));
  check('the run says when it ran and that it was a run',
    run.source === 'run' && Number.isFinite(Date.parse(run.ranAt)) && run.schema === 1, `${run.source} ${run.ranAt}`);

  // ── 2. an old table log, --from-log ──────────────────────────────
  const log = path.join(root, 'checks-latest.log');
  writeFileSync(log, [
    '  check-screens              ok   rc=0   552.0s  PASS — 1428 warning(s)',
    '  check-states               FAIL rc=1    15.7s  4 error(s), 146 warning(s)',
    '  check-bindings             rpt  rc=1    39.7s  (baseline run — `--strict` fails on unbound components and boilerplate)',
    '  check-authored-inputs      FAIL rc=1    12.4s  FAIL - 7 stale, 0 issue(s), 7 authored input(s) checked',
    '  audit-screenless-operations ok   rc=0    12.5s  orders           /memberships                  2   listMembershipRenewals',
    '',
    '  5 checker(s) run · 2 gate failure(s) · 1 report-only non-zero',
    '    rpt  check-bindings             rc=1 — runs as a baseline',
    '    FAIL check-states               rc=1',
    'CHECKS DONE ', '',
  ].join('\n'));
  const when = new Date('2026-09-27T22:58:37Z');
  utimesSync(log, when, when);
  const fromLog = path.join(root, 'from-log.json');
  py([path.join(TOOLS, 'run-checks.py'), '--from-log', log, '--json', fromLog], root);
  const old = JSON.parse(readFileSync(fromLog, 'utf8'));
  const ob = Object.fromEntries(old.checks.map((c) => [c.name, c]));
  check('a log gives one record per table row, and not the summary lines under it',
    old.checks.length === 5, old.checks.map((c) => c.name).join());
  check('a row whose name runs into its mark is still read (audit-screenless-operations)',
    ob['audit-screenless-operations']?.status === 'pass');
  check('its verdicts are the table\'s: 2 fail, 1 warn, 2 pass',
    old.totals.fail === 2 && old.totals.warn === 1 && old.totals.pass === 2, JSON.stringify(old.totals));
  check('stale inputs count as the failure\'s findings',
    ob['check-authored-inputs'].errors === 7 && ob['check-states'].errors === 4, `${ob['check-authored-inputs'].errors} ${ob['check-states'].errors}`);
  check('a log has no first findings, and says it was a log rather than guessing',
    old.source === 'log' && old.checks.every((c) => c.first.length === 0 && c.fix === null) && old.commit === null);
  check('the run finished when the log was written', old.finishedAt === '2026-09-27T22:58:37Z', old.finishedAt);

  // ── 3. refresh-safe.sh's judge puts the baseline checkers back ────
  const script = readFileSync(path.join(TOOLS, 'refresh-safe.sh'), 'utf8');
  // \r?\n: a Windows checkout can carry the script with CRLF endings.
  const helper = /cat > "\$HELPER" <<'PYHELPER'\r?\n([\s\S]*?)\r?\nPYHELPER\r?\n/.exec(script)?.[1];
  check('the helper can be cut out of refresh-safe.sh', !!helper);
  writeFileSync(path.join(root, 'helper.py'), helper ?? '');
  const baseline = path.join(root, 'baseline.json');
  writeFileSync(baseline, JSON.stringify({
    checkers: { 'check-bad': { why: 'known for the test', known: ['^states/redemption-right\\.yaml: ', '^second finding$'] } },
  }));
  rmSync(path.join(pkg, 'handoff', 'checks.json'), { force: true });
  let judged = '';
  try {
    judged = py([path.join(root, 'helper.py'), 'judge', pkg, baseline, path.join(root, 'judge.log'), '', '2'], pkg);
  } catch (e) {
    judged = `${e.stdout ?? ''}${e.stderr ?? ''}`;
  }
  check('the judge passes a failure the baseline names', /JUDGEMENT: PASS/.test(judged), judged.slice(-400));
  const merged = await readChecks(pkg);
  const mb = Object.fromEntries((merged?.checks ?? []).map((c) => [c.name, c]));
  check('and writes handoff/checks.json with all three, the baseline checker included',
    merged?.checks?.length === 3 && !!mb['check-bad'], JSON.stringify(merged)?.slice(0, 300));
  check('the baseline checker keeps its findings and says the baseline accepted it',
    mb['check-bad']?.status === 'fail' && mb['check-bad']?.baseline === 'known for the test' && mb['check-bad']?.fix === 'states/redemption-right.yaml',
    JSON.stringify(mb['check-bad']));
  check('and the file records the judgement', merged?.judgement === 'pass' && merged?.by === 'refresh-safe.sh');

  // ── 4. which release a run was for ───────────────────────────────
  const releases = [
    { tag: 'r1', taggedAt: '2026-10-04T17:27:37+05:30' },
    { tag: 'r3', taggedAt: '2026-10-08T01:00:45+05:30' },
    { tag: 'r5', taggedAt: '2026-10-13T20:38:34+05:30' },
  ];
  const served = { mode: 'tag', tag: 'r5', releases };
  const p1 = placeChecks(old, served);
  check('a log from 28 September, served at r5, was for r1 and is stale',
    p1.ranFor === 'r1' && p1.stale && !p1.current && p1.how === 'date', JSON.stringify(p1));
  const p2 = placeChecks({ checks: [], base: 'r3', ahead: 4, ranAt: '2026-10-12T00:00:00Z' }, served);
  check('a run four commits past r3 was for the next tag, r5, and is current',
    p2.ranFor === 'r5' && p2.current && !p2.stale && p2.how === 'git', JSON.stringify(p2));
  const p3 = placeChecks({ checks: [], base: 'r3', ahead: 0 }, served);
  check('a run on the r3 tag itself, served at r5, is stale', p3.ranFor === 'r3' && p3.stale, JSON.stringify(p3));
  const p4 = placeChecks({ checks: [], base: 'r5', ahead: 2 }, { mode: 'working', tag: null, releases });
  check('a run past the last tag, with the working tree served, is current',
    p4.ranFor === null && p4.current && !p4.stale, JSON.stringify(p4));
  const p5 = placeChecks({ checks: [], base: 'r5', ahead: 2 }, served);
  check('the same run with r5 served is newer than what is served, not stale',
    p5.newer && !p5.stale && !p5.current, JSON.stringify(p5));
  check('no file is neither current nor stale', (() => { const p = placeChecks(null, served); return !p.current && !p.stale && p.servedTag === 'r5'; })());
  rmSync(path.join(pkg, 'handoff', 'checks.json'), { force: true });
  check('a missing file reads as none, not as an error', (await readChecks(pkg)) === null);
  writeFileSync(path.join(pkg, 'handoff', 'checks.json'), '{ not json');
  check('a broken file reads as a problem the page can say', /not JSON/.test((await readChecks(pkg))?.problem ?? ''));
} catch (e) {
  check('the harness ran to the end', false, `${e.message}\n${e.stdout ?? ''}${e.stderr ?? ''}`);
} finally {
  rmSync(root, { recursive: true, force: true });
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
