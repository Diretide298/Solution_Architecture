// Release tags: which state of a package ADAM serves.
//
// **ADAM used to serve the working tree**, so the spec moved under a developer
// every time somebody saved a file in the package. The rule since 1 October
// (council C2): the package is released on a cadence as git tags `r1`, `r2`, …
// and ADAM serves the newest tag. A ticket records the tag it was pulled at
// (api/releases.py, `ticket_pin`), and `/ticket` shows what changed between that
// tag and the one being served (lib/release-diff.mjs).
//
// **A tag is served from an export, not from git.** Every reader in lib/ reads
// files under a root — about sixty readFile and readdir calls across twenty
// modules — so the honest way to serve a tag is to give them a root that *is*
// the tag. `exportRelease` writes the tagged tree once into
// `<releases>/<tag>/`, and a served tag is just a different `pkg.root`. A tag
// never changes, so an export is never rewritten and is not watched.
//
// Two places export, one implementation:
//   - on a workstation the viewer is inside the git repository, so the server
//     exports a tag itself the first time it needs one;
//   - on the server the deployed viewer is a copy with no `.git`, so
//     deploy/export-releases.mjs runs from the checkout during a deploy and the
//     server finds the exports already there.
//
// **The mirrors under `repos/` are left out of an export**, all but the parts
// the viewer reads (.github, terraform, apps, openapi, and the top-level names).
// They are generated copies of the package itself — 4 GB of the 4.8 GB — and
// carry the same tag in their own repositories. The folders left out are still
// created, empty, so a reader listing `repos/<repo>/` sees the same names.
//
// Files already exported under an earlier tag with the same content are hard
// links to it, not copies, so the second release costs what changed.
//
// Files this module writes, beside the exports:
//   <releases>/index.json    every r<N> tag: name, commit, date, exported or not
//   <releases>/served.json   what the viewer is serving right now (the accounts
//                            service reads this to know the tag in force)
//   <releases>/<tag>.json    one export's manifest: path -> blob, so the next
//                            export can link rather than copy

import { execFile, spawn } from 'node:child_process';
import { copyFile, link, mkdir, readFile, readdir, rename, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { promisify } from 'node:util';

const run = promisify(execFile);

/** A release tag. `r1` and up; nothing else is a release, however it is named. */
export const TAG = /^r([1-9]\d{0,5})$/;
export const tagNumber = (tag) => Number(TAG.exec(String(tag ?? ''))?.[1] ?? NaN);

/** Mirror folders an export keeps; every other folder under repos/<repo>/ is left empty. */
const KEEP_REPO_DIRS = new Set(['.github', 'terraform', 'apps', 'openapi']);

/**
 * `-c safe.directory=*` only when running as root. A deploy runs under sudo
 * against a checkout owned by somebody else, and git (2.35.2 on) refuses that
 * repository outright; everywhere else the owner is running it and the check
 * stays on.
 */
const SAFE = typeof process.getuid === 'function' && process.getuid() === 0
  ? ['-c', 'safe.directory=*'] : [];

async function git(cwd, args, opts = {}) {
  const { stdout } = await run('git', [...SAFE, ...args],
    { cwd, maxBuffer: 1024 * 1024 * 1024, timeout: 300000, windowsHide: true, ...opts });
  return stdout;
}

const exists = (p) => stat(p).then(() => true, () => false);

async function readJson(file) {
  try { return JSON.parse(await readFile(file, 'utf8')); } catch { return null; }
}

/** Written beside and renamed over, so a reader never sees half a file. */
export async function writeJson(file, value) {
  await mkdir(path.dirname(file), { recursive: true });
  const temp = `${file}.${process.pid}.tmp`;
  await writeFile(temp, `${JSON.stringify(value, null, 2)}\n`);
  await rename(temp, file);
}

/**
 * The repository a package root is in, and where in it: `{ top, prefix }` with
 * prefix `ticvai/` for adam/ticvai. Null when it is not in one, or git is not
 * installed — the deployed copy, which is not a failure.
 */
export async function repoOf(root) {
  try {
    const top = (await git(root, ['rev-parse', '--show-toplevel'])).trim();
    const prefix = (await git(root, ['rev-parse', '--show-prefix'])).trim();
    return top ? { top, prefix } : null;
  } catch {
    return null;
  }
}

/** Every r<N> tag in the repository, oldest first, with its commit and date. */
export async function listTags(top) {
  const out = await git(top, ['for-each-ref', '--format=%(refname:short)%09%(objectname)%09%(*objectname)%09%(creatordate:iso-strict)', 'refs/tags']);
  const tags = [];
  for (const line of out.split(/\r?\n/)) {
    const [tag, object, peeled, date] = line.split('\t');
    if (!TAG.test(tag ?? '')) continue;
    // An annotated tag points at a tag object; `*objectname` is the commit under it.
    tags.push({ tag, commit: peeled || object, taggedAt: date || null });
  }
  return tags.sort((a, b) => tagNumber(a.tag) - tagNumber(b.tag));
}

/** Whether an export of this tag is complete: the tree and its manifest, which is written last. */
export async function isExported(releasesDir, tag) {
  return (await exists(path.join(releasesDir, tag))) && (await exists(path.join(releasesDir, `${tag}.json`)));
}

/**
 * The releases there are for one package.
 *
 * From git when the package is in a repository (a workstation, or the checkout a
 * deploy runs from), and then written to index.json; from index.json otherwise
 * (the deployed copy, which has no .git). `exported` says which have a tree.
 */
export async function scanReleases({ root, releasesDir }) {
  const repo = await repoOf(root);
  let releases = [];
  let source = 'none';
  if (repo) {
    releases = await listTags(repo.top).catch(() => []);
    source = 'git';
  } else {
    const index = await readJson(path.join(releasesDir, 'index.json'));
    releases = Array.isArray(index?.releases)
      ? index.releases.filter((r) => TAG.test(r?.tag ?? '')).sort((a, b) => tagNumber(a.tag) - tagNumber(b.tag))
      : [];
    source = index ? 'index' : 'none';
  }
  releases = await Promise.all(releases.map(async (r) => ({
    tag: r.tag, commit: r.commit ?? null, taggedAt: r.taggedAt ?? null,
    exported: await isExported(releasesDir, r.tag),
  })));
  if (source === 'git') {
    await writeJson(path.join(releasesDir, 'index.json'), {
      generatedAt: new Date().toISOString(), source, releases,
    }).catch(() => {});
  }
  return { repo, releases, source };
}

/**
 * Whether a path in the package goes into an export. Paths are relative to the
 * package root, with forward slashes.
 *
 * `repos/<repo>/<file>` stays, `repos/<repo>/<dir>/…` stays only for the folders
 * the viewer reads. Returns `{ keep, hollow }` where `hollow` is the folder to
 * create empty when the file is left out.
 */
export function exportRule(rel) {
  const parts = rel.split('/');
  if (parts[0] !== 'repos' || parts.length < 4) return { keep: true, hollow: null };
  if (KEEP_REPO_DIRS.has(parts[2])) return { keep: true, hollow: null };
  return { keep: false, hollow: parts.slice(0, 3).join('/') };
}

/**
 * Stream blobs out of one `git cat-file --batch`, writing each to its file.
 * One process for thousands of files, read with backpressure, so neither
 * memory nor open files grow with the size of the release.
 */
async function writeBlobs(top, jobs) {
  if (!jobs.length) return;
  const child = spawn('git', [...SAFE, 'cat-file', '--batch'], { cwd: top, windowsHide: true });
  let stderr = '';
  child.stderr.on('data', (c) => { stderr += c; });
  const closed = new Promise((resolve) => child.on('close', resolve));
  for (const job of jobs) child.stdin.write(`${job.sha}\n`);
  child.stdin.end();

  let chunks = [];
  let have = 0;
  let need = null;
  let done = 0;
  const take = (n) => {
    const all = chunks.length === 1 ? chunks[0] : Buffer.concat(chunks, have);
    const head = all.subarray(0, n);
    const rest = all.subarray(n);
    chunks = rest.length ? [rest] : [];
    have = rest.length;
    return head;
  };
  for await (const chunk of child.stdout) {
    chunks.push(chunk);
    have += chunk.length;
    for (;;) {
      if (need === null) {
        const all = chunks.length === 1 ? chunks[0] : Buffer.concat(chunks, have);
        chunks = [all];
        const nl = all.indexOf(10);
        if (nl < 0) break;
        const header = take(nl + 1).toString('utf8').trim();
        const m = /^[0-9a-f]+ (\w+) (\d+)$/.exec(header);
        if (!m) throw new Error(`git cat-file answered "${header}" for ${jobs[done]?.sha}`);
        need = Number(m[2]);
      }
      if (have < need + 1) break;
      const body = take(need + 1).subarray(0, need);
      const job = jobs[done];
      await writeFile(job.dest, body);
      for (const twin of job.twins) await linkOrCopy(job.dest, twin);
      done += 1;
      need = null;
    }
  }
  const code = await closed;
  if (code !== 0 || done !== jobs.length) {
    throw new Error(`git cat-file stopped after ${done} of ${jobs.length} files (exit ${code}) ${stderr.trim()}`);
  }
}

async function linkOrCopy(from, to) {
  try {
    await link(from, to);
  } catch {
    await copyFile(from, to);
  }
}

/**
 * Export one tag's package tree into `<releasesDir>/<tag>/`.
 *
 * Built in a hidden staging folder and renamed into place, and the manifest is
 * written last, so a half-finished export (a deploy interrupted, a disk full)
 * is never mistaken for a release: `isExported` needs both.
 */
export async function exportRelease({ root, releasesDir, tag, log = () => {} }) {
  if (!TAG.test(tag)) throw new Error(`"${tag}" is not a release tag (r1, r2, …)`);
  if (await isExported(releasesDir, tag)) return readJson(path.join(releasesDir, `${tag}.json`));
  const repo = await repoOf(root);
  if (!repo) throw new Error(`${root} is not in a git repository, so ${tag} cannot be exported from it`);
  const commit = (await git(repo.top, ['rev-parse', `${tag}^{commit}`])).trim();
  const taggedAt = (await listTags(repo.top)).find((t) => t.tag === tag)?.taggedAt ?? null;

  const listing = await git(repo.top, ['ls-tree', '-r', '-z', '--full-tree', commit,
    ...(repo.prefix ? ['--', repo.prefix] : [])]);

  // What earlier exports already hold, by blob, so an unchanged file is a link.
  const held = new Map();
  for (const name of await readdir(releasesDir).catch(() => [])) {
    const m = /^(r\d+)\.json$/.exec(name);
    if (!m || m[1] === tag) continue;
    const manifest = await readJson(path.join(releasesDir, name));
    for (const [rel, sha] of Object.entries(manifest?.files ?? {})) {
      if (!held.has(sha)) held.set(sha, path.join(releasesDir, m[1], rel));
    }
  }

  await mkdir(releasesDir, { recursive: true });
  const staging = path.join(releasesDir, `.${tag}.partial-${process.pid}`);
  await rm(staging, { recursive: true, force: true });
  await mkdir(staging, { recursive: true });

  const files = {};
  const hollow = new Set();
  const made = new Set();
  const ensureDir = async (dir) => {
    if (made.has(dir)) return;
    await mkdir(dir, { recursive: true });
    made.add(dir);
  };
  const fetch = new Map(); // sha -> job
  let linked = 0;
  let skipped = 0;
  for (const entry of listing.split('\0')) {
    if (!entry) continue;
    const tab = entry.indexOf('\t');
    const [mode, type, sha] = entry.slice(0, tab).split(' ');
    const full = entry.slice(tab + 1);
    // Blobs only: a submodule (commit) has no content here, and a symlink
    // (120000) would point somewhere outside the export.
    if (type !== 'blob' || mode === '120000') { skipped += 1; continue; }
    const rel = repo.prefix ? full.slice(repo.prefix.length) : full;
    const rule = exportRule(rel);
    if (!rule.keep) { hollow.add(rule.hollow); skipped += 1; continue; }
    const dest = path.join(staging, ...rel.split('/'));
    await ensureDir(path.dirname(dest));
    files[rel] = sha;
    const earlier = held.get(sha);
    if (earlier && await exists(earlier)) {
      await linkOrCopy(earlier, dest);
      linked += 1;
      continue;
    }
    const job = fetch.get(sha);
    if (job) job.twins.push(dest);
    else fetch.set(sha, { sha, dest, twins: [] });
  }
  for (const dir of hollow) await ensureDir(path.join(staging, ...dir.split('/')));
  log(`${tag}: ${Object.keys(files).length} files (${linked} linked from earlier releases, `
    + `${fetch.size} written), ${hollow.size} mirror folders left empty`);
  await writeBlobs(repo.top, [...fetch.values()]);

  const target = path.join(releasesDir, tag);
  if (await exists(target)) await rm(target, { recursive: true, force: true });
  await rename(staging, target);
  const manifest = {
    tag, commit, taggedAt, prefix: repo.prefix, exportedAt: new Date().toISOString(),
    counts: { files: Object.keys(files).length, linked, written: fetch.size, hollow: hollow.size, skipped },
    hollow: [...hollow].sort(),
    files,
  };
  await writeJson(path.join(releasesDir, `${tag}.json`), manifest);
  return manifest;
}

/**
 * Which tree to serve, from `packageRef`.
 *
 *   latest   the newest r<N> tag; the working tree while there is none
 *   working  the working tree, whatever tags exist (a workstation editing the package)
 *   r<N>     that tag
 *
 * ADAM_PACKAGE_REF overrides the registry for every project. A ref that names a
 * tag that does not exist, or a tag that is not exported and cannot be, is
 * reported as a problem and the newest usable state is served instead — a
 * viewer that refuses to start cannot say what is wrong.
 */
export async function resolveRelease(project, { env = process.env, log = () => {} } = {}) {
  const releasesDir = project.releases;
  const ref = String(env.ADAM_PACKAGE_REF || project.packageRef || 'latest').trim();
  const scan = await scanReleases({ root: project.root, releasesDir });
  const releases = scan.releases;
  const latest = releases.at(-1) ?? null;
  const working = {
    mode: 'working', tag: null, commit: null, taggedAt: null, root: project.root,
  };
  const base = { ref, releasesDir, releases, source: scan.source, repo: scan.repo };
  if (ref === 'working') return { ...base, ...working, problem: null };

  let problem = null;
  let target = latest;
  if (ref !== 'latest') {
    if (!TAG.test(ref)) problem = `packageRef "${ref}" is not latest, working or r<N>`;
    else {
      target = releases.find((r) => r.tag === ref) ?? null;
      if (!target) {
        problem = `packageRef ${ref} is not a release tag of ${project.id}`;
        target = latest;
      }
    }
    if (problem) problem += `; serving ${target ? target.tag : 'the working tree'} instead`;
  }
  if (!target) return { ...base, ...working, problem, note: 'no release tag yet' };

  if (!target.exported) {
    if (!scan.repo) {
      return {
        ...base, ...working,
        problem: `${target.tag} is not exported under ${releasesDir} and there is no git `
          + 'repository here to export it from (deploy/export-releases.mjs does that on a '
          + 'server); serving the working tree',
      };
    }
    log(`exporting ${target.tag} for ${project.id} into ${releasesDir}`);
    await exportRelease({ root: project.root, releasesDir, tag: target.tag, log });
    target.exported = true;
  }
  return {
    ...base, mode: 'tag', tag: target.tag, commit: target.commit, taggedAt: target.taggedAt,
    root: path.join(releasesDir, target.tag), problem,
  };
}

/**
 * The tree for one tag, exporting it if it is missing and can be. Null when it
 * is missing and cannot be — the deployed copy, for a tag the deploy did not
 * export — which the diff reports rather than guesses around.
 */
export async function releaseRoot(release, sourceRoot, tag) {
  if (!TAG.test(String(tag ?? ''))) return null;
  if (await isExported(release.releasesDir, tag)) return path.join(release.releasesDir, tag);
  if (!release.repo) return null;
  const known = release.releases.some((r) => r.tag === tag)
    || (await listTags(release.repo.top).catch(() => [])).some((r) => r.tag === tag);
  if (!known) return null;
  await exportRelease({ root: sourceRoot, releasesDir: release.releasesDir, tag });
  return path.join(release.releasesDir, tag);
}

/** What the accounts service reads to learn the tag in force. */
export async function writeServed(project, release) {
  await writeJson(path.join(project.releases, 'served.json'), {
    project: project.id,
    mode: release.mode,
    tag: release.tag,
    commit: release.commit,
    taggedAt: release.taggedAt,
    packageRef: release.ref,
    problem: release.problem ?? null,
    at: new Date().toISOString(),
  });
}

/** For the `release` route: the release in force and the others, without paths. */
export function describeRelease(release) {
  return {
    mode: release.mode,
    tag: release.tag,
    commit: release.commit,
    taggedAt: release.taggedAt,
    packageRef: release.ref,
    ...(release.problem ? { problem: release.problem } : {}),
    ...(release.note ? { note: release.note } : {}),
    releases: release.releases.map(({ tag, commit, taggedAt, exported }) => ({ tag, commit, taggedAt, exported })),
  };
}
