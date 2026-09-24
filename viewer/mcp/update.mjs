/**
 * Bring this connector up to what ADAM is serving.
 *
 *     node update.mjs            # from the connector folder
 *     node update.mjs --check    # say whether an update exists, write nothing
 *
 * **This downloads code and runs it afterwards, so it is written like something
 * that does.** Four rules, and each one closes a way this could go wrong:
 *
 *   **One address, and it is the one already configured.** The bundle is
 *   fetched from `ADAM_VIEWER_URL` — the same server this connector already
 *   reads the package from. There is no URL argument, so there is nothing to
 *   talk somebody into passing.
 *
 *   **Only the files that are already the connector.** A bundle entry whose
 *   path is not in `FILES` is refused. That list has no directories in it, so
 *   `../`, an absolute path, a drive letter and a backslash are all rejected by
 *   the same check rather than by three regexes that each miss something.
 *
 *   **Nothing is executed.** The bundle is text written to disk. There is no
 *   install script in it and no hook that runs one; the new code runs when the
 *   person restarts Claude Code, which is a thing they do knowingly.
 *
 *   **The old build is kept.** Replaced files are copied next door first, so a
 *   bad update is undone by copying them back, with no network involved.
 *
 * The connector cannot replace itself while it is running — the MCP server is
 * this process's own source — so the last thing this prints is the one manual
 * step: restart Claude Code.
 */

import { readFile, writeFile, mkdir, rename, copyFile } from 'node:fs/promises';
import path from 'node:path';
import { FILES, HERE, buildOf } from './version.mjs';

const BASE = (process.env.ADAM_VIEWER_URL ?? 'http://127.0.0.1:4173').replace(/\/+$/, '');
const CHECK_ONLY = process.argv.includes('--check');

// Long enough for a server on the other side of a VPN, short enough that a
// machine which cannot reach ADAM says so rather than appearing to hang.
const PATIENCE = 15000;

const say = (...parts) => console.log('[adam]', ...parts);

async function ask(route) {
  const res = await fetch(`${BASE}${route}`, {
    signal: AbortSignal.timeout(PATIENCE),
    headers: { accept: 'application/json' },
  });
  if (!res.ok) throw new Error(`${route} answered ${res.status}`);
  return res.json();
}

/** Every path a bundle is allowed to carry. Membership, not pattern matching:
 *  the list holds bare file names, so anything with a separator in it fails by
 *  not being in the list rather than by being caught. */
const ALLOWED = new Set(FILES);

async function main() {
  const mine = await buildOf(HERE);

  let theirs;
  try {
    theirs = await ask('/connector/version');
  } catch (error) {
    say(`could not reach ADAM at ${BASE} — ${error.message}`);
    say('If ADAM is on another machine, set ADAM_VIEWER_URL and try again.');
    process.exit(2);
  }

  if (!theirs?.build) {
    say(`${BASE} does not serve connector updates. It may be an older ADAM.`);
    process.exit(2);
  }

  if (theirs.build === mine) {
    say(`already current — build ${mine}`);
    return;
  }

  say(`an update is available: ${mine} -> ${theirs.build}`);
  if (CHECK_ONLY) return;

  const bundle = await ask('/connector/bundle');
  const files = bundle?.files ?? [];
  const refused = files.filter((f) => !ALLOWED.has(f?.path));
  if (refused.length) {
    // Refused whole rather than partly applied. A bundle carrying a path this
    // connector does not recognise is not a bundle to take the good half of.
    say('refused: the bundle names files that are not part of the connector —',
      refused.map((f) => String(f?.path)).join(', '));
    process.exit(3);
  }
  if (!files.length) {
    say('refused: the bundle is empty.');
    process.exit(3);
  }
  // Every file, or none. Half a connector does not start.
  const missing = FILES.filter((name) => !files.some((f) => f.path === name));
  if (missing.length) {
    say('refused: the bundle is missing', missing.join(', '));
    process.exit(3);
  }

  const backup = path.join(HERE, `backup-${mine}`);
  await mkdir(backup, { recursive: true });
  for (const name of FILES) {
    await copyFile(path.join(HERE, name), path.join(backup, name)).catch(() => {});
  }

  // Written beside the target and renamed into place: a half-written tools.mjs
  // is a connector that will not start, and a crash mid-write is exactly when
  // somebody least wants to debug one.
  for (const file of files) {
    const target = path.join(HERE, file.path);
    const temporary = `${target}.incoming`;
    await writeFile(temporary, file.text, 'utf8');
    await rename(temporary, target);
  }

  const now = await buildOf(HERE);
  if (now !== theirs.build) {
    // Said rather than swallowed. The backup is right there, and a connector
    // that hashes to something nobody expected should not be trusted silently.
    say(`warning: after writing, this reads as ${now} and ADAM offered ${theirs.build}.`);
    say(`The previous build is in ${backup} if you want it back.`);
    process.exit(4);
  }

  say(`updated to ${now}. The previous build is in ${backup}.`);
  say('Restart Claude Code to load it — the running connector is still the old one.');
}

main().catch((error) => {
  say('update failed —', error.message);
  process.exit(1);
});
