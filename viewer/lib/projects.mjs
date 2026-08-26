// projects.json — which packages this viewer reads, and where they are.
//
// The viewer used to be a folder inside the one package it read, and the
// package was wherever `..` happened to point. That is why `ROOT` was a
// constant: there was only ever one, and it could not be named because it had
// no name to be given.
//
// A package is now a thing with an id, and the id is the first segment of every
// read: `/pkg/ticvai/index`. The registry is the only place a path appears, so a
// package can live anywhere — beside the viewer, above it, on another disk —
// and nothing but this file knows.
//
// It is a file rather than an environment variable because it is a list, and a
// list of paths in an environment variable is a delimiter waiting to be wrong.
// It is read once at startup: adding a project is a restart, which is the same
// cost as adding one to a config file the process already read.

import { readFile } from 'node:fs/promises';
import { stat } from 'node:fs/promises';
import path from 'node:path';

/**
 * A project id is a path segment, a cache key and half a URL, so it is checked
 * rather than trusted.
 *
 * Lowercase, starting with a letter or digit, no dots and no slashes. That last
 * pair is not stylistic: an id reaches `path.join` when a package root is
 * resolved, and `..` is a valid folder name to a filesystem and a directory
 * traversal to everything else.
 */
const ID = /^[a-z0-9][a-z0-9-]{0,38}$/;

/**
 * Ids that would be ambiguous in the URL they end up in.
 *
 * `/pkg/<id>/<route>` has no overlap with the accounts service, which is the
 * whole reason the package reads moved out of `/api/` — but `/pkg/projects` is
 * this server's own listing, and a project called `projects` would sit exactly
 * on top of it.
 */
const RESERVED = new Set(['projects', 'api', 'pkg', 'health']);

/**
 * @typedef {object} Project
 * @property {string} id        first segment of every read — `ticvai`
 * @property {string} name      what a person calls it — `TICVAI`
 * @property {string} root      absolute path to the package
 * @property {string} contracts the contracts folder inside it, relative
 * @property {boolean} active   false hides it without deleting the entry
 * @property {string|null} note why it is here, for the listing
 */

/**
 * Read the registry, resolve every root, and say what is wrong with it.
 *
 * Nothing here throws on a bad entry. A registry with four projects and one
 * broken path should serve the other three and report the fourth — a viewer
 * that refuses to start because a disk was not mounted is a viewer that cannot
 * tell you the disk was not mounted.
 *
 * @param {string} viewerDir  the directory holding server.mjs; roots resolve
 *                            against it, so a relative root in the file means
 *                            "beside the viewer" rather than "beside whatever
 *                            directory somebody happened to run node from"
 * @returns {Promise<{projects: Project[], defaultId: string|null, problems: string[]}>}
 */
export async function loadProjects(viewerDir) {
  const file = path.join(viewerDir, 'projects.json');
  const problems = [];

  let doc = null;
  try {
    doc = JSON.parse(await readFile(file, 'utf8'));
  } catch (error) {
    // Missing is not the same as malformed, and the difference decides whether
    // somebody goes looking for a typo or for the file.
    problems.push(error.code === 'ENOENT'
      ? `${file} is missing — no packages are registered`
      : `${file} could not be read: ${error.message}`);
    return { projects: [], defaultId: null, problems };
  }

  const seen = new Set();
  const projects = [];
  for (const entry of Array.isArray(doc?.projects) ? doc.projects : []) {
    const id = String(entry?.id ?? '');
    if (!ID.test(id)) {
      problems.push(`"${id}" is not a usable project id — lowercase letters, digits and hyphens`);
      continue;
    }
    if (RESERVED.has(id)) {
      problems.push(`"${id}" is reserved — it would collide with /pkg/${id}`);
      continue;
    }
    if (seen.has(id)) {
      problems.push(`"${id}" is registered twice; the second entry is ignored`);
      continue;
    }
    seen.add(id);

    const root = path.resolve(viewerDir, String(entry?.root ?? ''));
    const there = await stat(root).catch(() => null);
    if (!there?.isDirectory()) {
      problems.push(`${id}: ${root} is not a directory — the package will not be served`);
      continue;
    }

    projects.push({
      id,
      name: String(entry?.name ?? id),
      root,
      contracts: String(entry?.contracts ?? 'contracts'),
      active: entry?.active !== false,
      note: entry?.note ?? null,
    });
  }

  // The default answers `/api/*`, which is the pre-project spelling every
  // client still uses. Named explicitly rather than "the first one", so
  // reordering the file cannot silently repoint the old routes.
  let defaultId = doc?.default ? String(doc.default) : null;
  if (defaultId && !projects.some((p) => p.id === defaultId)) {
    problems.push(`default "${defaultId}" is not a registered project`);
    defaultId = null;
  }
  if (!defaultId) defaultId = projects.find((p) => p.active)?.id ?? null;

  return { projects, defaultId, problems };
}
