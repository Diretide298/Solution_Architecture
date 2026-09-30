#!/usr/bin/env node
// Export every release tag of every registered package, for a deployed viewer.
//
//   node deploy/export-releases.mjs --source <checkout>/viewer --viewer /srv/ticvai/viewer
//
// The deployed viewer is a copy with no `.git`, so it cannot read a tag itself.
// This runs from the checkout during a deploy (deploy.sh), where the repository
// is, and writes each r<N> tag's tree into the deployed viewer's release folder
// (`.releases/<project>/<tag>/` unless projects.json says otherwise), with the
// index.json the server and the accounts service read. Tags already exported are
// left alone — a tag does not change — so running it on every deploy costs
// nothing once the first export is done.
//
// Only packages whose `root` is relative and present beside the source checkout
// are exported: the same rule deploy.sh uses for copying them.

import path from 'node:path';
import { existsSync, readFileSync } from 'node:fs';
import { exportRelease, scanReleases, writeJson } from '../lib/releases.mjs';

const args = { source: null, viewer: null };
for (let i = 2; i < process.argv.length; i += 1) {
  if (process.argv[i] === '--source') args.source = process.argv[++i];
  else if (process.argv[i] === '--viewer') args.viewer = process.argv[++i];
}
if (!args.source || !args.viewer) {
  console.error('usage: export-releases.mjs --source <checkout viewer dir> --viewer <deployed viewer dir>');
  process.exit(2);
}

const registry = JSON.parse(readFileSync(path.join(args.viewer, 'projects.json'), 'utf8'));
let failed = 0;
for (const entry of registry.projects ?? []) {
  if (entry.active === false || !entry.id || !entry.root || path.isAbsolute(entry.root)) continue;
  const root = path.resolve(args.source, entry.root);
  if (!existsSync(root)) {
    console.log(`    ${entry.id}: ${root} is not beside the checkout — no releases exported`);
    continue;
  }
  const releasesDir = path.resolve(args.viewer, entry.releases ?? `.releases/${entry.id}`);
  try {
    const scan = await scanReleases({ root, releasesDir });
    if (!scan.repo) {
      console.log(`    ${entry.id}: ${root} is not in a git repository — no releases exported`);
      continue;
    }
    const missing = scan.releases.filter((r) => !r.exported);
    for (const r of missing) {
      await exportRelease({ root, releasesDir, tag: r.tag, log: (line) => console.log(`    ${entry.id} ${line}`) });
      r.exported = true;
    }
    await writeJson(path.join(releasesDir, 'index.json'), {
      generatedAt: new Date().toISOString(), source: 'git', releases: scan.releases,
    });
    const latest = scan.releases.at(-1);
    console.log(`    ${entry.id}: ${scan.releases.length} release tag(s)`
      + (latest ? `, newest ${latest.tag}` : ' — the working tree will be served')
      + (missing.length ? `; exported ${missing.map((r) => r.tag).join(', ')}` : '; nothing new to export'));
  } catch (error) {
    failed += 1;
    console.error(`    ${entry.id}: ${error.message}`);
  }
}
process.exit(failed ? 1 : 0);
