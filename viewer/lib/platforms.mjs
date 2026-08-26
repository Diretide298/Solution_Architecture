/**
 * The platforms, and what is missing from each.
 *
 * A platform is an application somebody signs into — Guest Web, Venue POS, the
 * back office. It is the unit a delivery lead owns, which is why this is the
 * page they ask for: not "how many screens are there" but **is there a page for
 * this yet**.
 *
 * The package derives the answer itself. `tools/derive-platform.py` emits one
 * `handoff/platform-<code>.json` per platform, and the section worth reading is
 * `gaps` — four kinds of missing thing, none of them typed by anybody:
 *
 *   operationsWithNoScreen     in a contract this platform uses, callable by its
 *                              audience, reaching no screen anywhere
 *   modulesSplitAcrossWaves    sells in wave 1, cannot refund until wave 3
 *   screensNotDrawn            exists on paper, nobody has seen it
 *   flowsNamingAMissingScreen  the journey needs a screen that does not exist
 *
 * So this file derives nothing. It reads what the dump computed, rolls it up,
 * and — the one thing the dump cannot do — checks its own completeness against
 * `screens/`. A platform whose screen file exists and whose derived page does
 * not is the failure that matters here, because the page would simply be absent
 * and absence reads as "no gaps" rather than "not looked at".
 *
 * Superseding a wrong turn: this replaces a lens over `x-ticvai-module`, the
 * 25 numbered contract modules. Those are a different vocabulary that shares no
 * name with anything on screen, and they were not what was being asked for.
 */

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const CODE = /^P\d+$/;

/** Every gap in one platform, as a flat count. */
function gapTotal(gaps) {
  return Object.values(gaps ?? {}).reduce((n, list) => n + (list?.length ?? 0), 0);
}

export async function buildPlatforms(root) {
  const handoff = path.join(root, 'handoff');
  const problems = [];

  const index = await readFile(path.join(handoff, 'platform-index.json'), 'utf8')
    .then(JSON.parse)
    .catch(() => null);

  // Which platforms the package *has*, independent of what was derived. This is
  // the completeness check: a derived file missing is invisible without it.
  const declared = await readdir(path.join(root, 'screens'))
    .then((names) => names
      .map((n) => n.match(/^(P\d+)-/)?.[1])
      .filter(Boolean)
      .sort())
    .catch(() => []);

  const platforms = [];
  for (const code of new Set([...declared, ...Object.keys(index ?? {})].sort())) {
    if (!CODE.test(code)) continue;
    const one = await readFile(path.join(handoff, `platform-${code}.json`), 'utf8')
      .then(JSON.parse)
      .catch(() => null);

    if (!one) {
      problems.push({
        severity: 'warning',
        kind: 'platform-page-not-derived',
        file: `handoff/platform-${code}.json`,
        message: `${code} has a screen file and no derived platform page, so its gaps are unknown `
          + `rather than none — run tools/derive-platform.py ${code}`,
      });
      continue;
    }
    if (!declared.includes(code)) {
      problems.push({
        severity: 'warning',
        kind: 'platform-not-in-screens',
        file: `handoff/platform-${code}.json`,
        message: `${code} has a derived page and no screens/${code}-*.yaml behind it`,
      });
    }
    platforms.push({ ...one, gapTotal: gapTotal(one.gaps) });
  }

  if (!platforms.length) {
    return { present: false, platforms: [], problems, stats: null };
  }

  const sum = (pick) => platforms.reduce((n, p) => n + (pick(p) ?? 0), 0);
  const stats = {
    platforms: platforms.length,
    screens: sum((p) => p.counts?.screens),
    operations: sum((p) => p.counts?.operations),
    undrawn: sum((p) => p.counts?.undrawn),
    operationsWithNoScreen: sum((p) => p.counts?.operationsWithNoScreen),
    gaps: sum((p) => p.gapTotal),
    withGaps: platforms.filter((p) => p.gapTotal > 0).length,
    clean: platforms.filter((p) => p.gapTotal === 0).length,
    generated: platforms[0]?.generated ?? null,
  };

  // Worst first. A worklist is ordered by how much work is on it; a directory is
  // ordered by name, and this is not a directory.
  platforms.sort((a, b) => b.gapTotal - a.gapTotal || a.code.localeCompare(b.code));

  return { present: true, platforms, stats, problems };
}
