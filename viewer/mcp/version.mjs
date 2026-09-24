/**
 * Which build of the connector this is, computed rather than stamped.
 *
 * **A hash of the files, not a version number and not a git commit.** A number
 * has to be remembered and bumped, and the one time it matters is the time
 * somebody forgot. A commit is wrong for a different reason: the installed
 * connector is a copy of four files, so `git rev-parse` on the repository
 * answers a question about the repository — including changes to the viewer,
 * the package and this file's own history — rather than about the code a
 * developer is actually running. Two people on the same connector would be
 * told they disagree because one of them pulled a CSS fix.
 *
 * Hashing the shipped files says exactly one thing: the code you are running
 * is, or is not, the code the server is offering. Nothing to bump, and it stays
 * correct for somebody who edited a file locally — they are, genuinely, on a
 * different build.
 *
 * **Line endings are normalised first, and that is not cosmetic.** The zip is
 * built on Windows, git rewrites endings on checkout, and the repository's own
 * `.gitattributes` exists because of it. A byte-for-byte hash would report two
 * identical connectors as different for the whole of their lives.
 */

import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

/**
 * The files that make up a connector, in the order they are hashed.
 *
 * **This list is the contract**, and three things read it: the hash below, the
 * viewer's `/connector/bundle`, and the updater deciding which paths it is
 * willing to write. A file not named here is not shipped, not hashed, and not
 * accepted from a bundle — so adding one to the connector means adding it here,
 * and `build-zip.ps1` copies the same list.
 *
 * Sorted, so the hash does not depend on how anybody happened to type it.
 */
export const FILES = [
  'client.mjs',
  'mcp-check.mjs',
  'server.mjs',
  'tools.mjs',
  'update.mjs',
  'version.mjs',
];

/** Where this file is, which is the connector directory on both sides. */
export const HERE = path.dirname(fileURLToPath(import.meta.url));

/**
 * The build id of the connector in `dir`: twelve hex characters.
 *
 * A missing file is hashed as a distinct value rather than skipped, so a
 * connector with `update.mjs` deleted does not hash the same as one where it
 * was never expected — "you are missing a file" and "you are current" have to
 * be different answers.
 */
export async function buildOf(dir = HERE) {
  const digest = createHash('sha256');
  for (const name of FILES) {
    const text = await readFile(path.join(dir, name), 'utf8').catch(() => null);
    digest.update(name);
    digest.update('\u0000');
    digest.update(text === null ? '\u0000absent' : text.replace(/\r\n/g, '\n'));
    digest.update('\u0000');
  }
  return digest.digest('hex').slice(0, 12);
}

/**
 * Every shipped file, read for sending. Used by the viewer to answer
 * `/connector/bundle`; a file that cannot be read is left out rather than sent
 * as an empty string, which the updater would happily write over working code.
 */
export async function filesOf(dir = HERE) {
  const out = [];
  for (const name of FILES) {
    const text = await readFile(path.join(dir, name), 'utf8').catch(() => null);
    if (text !== null) out.push({ path: name, text });
  }
  return out;
}
