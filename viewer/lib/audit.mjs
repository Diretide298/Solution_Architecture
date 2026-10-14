/**
 * What the Audit page reads: the last checks run, placed against the release
 * being served, and the few figures from the package that the page used to
 * fetch whole payloads to count.
 *
 * **The checks are a file the pipeline writes, not something this server
 * runs.** `tools/run-checks.py --json` writes `handoff/checks.json`, and
 * `refresh-safe.sh` writes it from the run it judges, so it is merged and
 * tagged with the rest of the refresh. That puts it under the served root like
 * every other derived file: a tag's export carries the checks that release was
 * made with, and nothing here has to know where releases are kept.
 *
 * **Which release a run belongs to is worked out, not trusted.** The file can
 * sit in r5's export and still be the run from before r3, when nobody refreshed
 * through refresh-safe in between; presenting that as r5's run is the exact
 * confident-and-wrong the old page was (a hand-typed record from 31 August,
 * five releases on). So `placeChecks` says which release the run was for and
 * whether that is the one being served:
 *
 *   - a run that knows its git position (`base` r4, `ahead` 3) was for r4 when
 *     it sat on the tag, and for the next tag after r4 when it sat past it;
 *   - a run converted from an old log knows only its date, and was for the
 *     first release tagged after it ran.
 */

import { readFile } from 'node:fs/promises';
import path from 'node:path';

export const CHECKS_FILE = 'handoff/checks.json';

const tagNo = (tag) => Number(/^r(\d+)$/.exec(String(tag ?? ''))?.[1] ?? NaN);

/** The parsed file, `null` when there is none, `{ problem }` when it cannot be read. */
export async function readChecks(root) {
  let text;
  try {
    text = await readFile(path.join(root, CHECKS_FILE), 'utf8');
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    return { problem: `could not read ${CHECKS_FILE}: ${error.message}` };
  }
  try {
    const doc = JSON.parse(text);
    if (!Array.isArray(doc?.checks)) return { problem: `${CHECKS_FILE} has no list of checks in it` };
    return doc;
  } catch (error) {
    return { problem: `${CHECKS_FILE} is not JSON: ${error.message}` };
  }
}

/**
 * Which release a run was for, against the one served.
 *
 * @param {object|null} checks   the file, as readChecks returned it
 * @param {object} release       describeRelease(pkg.release)
 * @returns {{ servedTag, mode, ranFor, how, current, stale, newer }}
 *   `ranFor` is a tag, or `null` for a run after every tag (work not yet
 *   released). `how` is 'git' or 'date'. `stale` is a run for an older release
 *   than the one served; `newer` a run past the served one.
 */
export function placeChecks(checks, release) {
  const releases = [...(release?.releases ?? [])].sort((a, b) => tagNo(a.tag) - tagNo(b.tag));
  const servedTag = release?.mode === 'tag' ? release.tag : null;
  const latest = releases.at(-1)?.tag ?? null;
  const out = { servedTag, mode: release?.mode ?? null, latest, ranFor: null, how: null, current: false, stale: false, newer: false };
  if (!checks || checks.problem) return out;

  if (checks.base && Number.isFinite(checks.ahead)) {
    out.how = 'git';
    if (checks.ahead === 0) out.ranFor = checks.base;
    else out.ranFor = releases.find((r) => tagNo(r.tag) > tagNo(checks.base))?.tag ?? null;
  } else {
    out.how = 'date';
    const ran = Date.parse(checks.ranAt ?? '');
    const after = Number.isFinite(ran)
      ? releases.find((r) => Number.isFinite(Date.parse(r.taggedAt ?? '')) && Date.parse(r.taggedAt) >= ran)
      : null;
    out.ranFor = after?.tag ?? null;
  }

  // The working tree is served: a run for no tag yet is a run of what is
  // there, and one for any tag is behind it.
  const servedNo = servedTag ? tagNo(servedTag) : Infinity;
  const ranNo = out.ranFor ? tagNo(out.ranFor) : Infinity;
  out.current = ranNo === servedNo;
  out.stale = ranNo < servedNo;
  out.newer = ranNo > servedNo;
  return out;
}

/**
 * The figures the page shows under "Live package counts", from payloads this
 * server already holds. Counted here so the page asks for a few numbers rather
 * than for /api/backend, /api/uiux and /api/journeys whole.
 */
export function liveCounts(pkg) {
  const tables = pkg.backend?.tables ?? [];
  const stats = pkg.uiux?.stats ?? {};
  return {
    boards: stats.boards ?? 0,
    frames: stats.frames ?? 0,
    unwired: stats.unwired ?? 0,
    screens: pkg.journeys?.screens?.length ?? 0,
    screensDrawn: stats.screensDrawn ?? 0,
    scalingRows: Array.isArray(pkg.backend?.scaling) ? pkg.backend.scaling.length : 0,
    tables: tables.length,
    withDdl: tables.filter((t) => t.ddl).length,
    foreignWriters: tables.filter((t) => (t.foreignWriters ?? []).length).length,
  };
}
