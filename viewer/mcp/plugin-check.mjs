#!/usr/bin/env node
/**
 * The plugin packaging, checked against the files it actually points at.
 *
 *   node viewer/mcp/plugin-check.mjs
 *
 * `claude plugin validate` reads the manifests and says whether the JSON is
 * legal. It cannot say whether `${CLAUDE_PLUGIN_ROOT}/server.mjs` is a file that
 * exists, whether every `${user_config.*}` the server asks for was declared, or
 * whether the marketplace's relative source lands on the plugin — and those are
 * the three ways this breaks silently. A manifest that validates and points at
 * nothing installs cleanly and then does nothing, with no error anybody sees
 * until a developer says the tools are missing.
 *
 * It also guards the two behaviours that have to differ between the plugin
 * install and the zip install: the updater must refuse to write into a plugin,
 * and the connector must tell a plugin user to run `/plugin update` rather than
 * the updater. Getting either wrong leaves somebody's files overwritten by the
 * next marketplace update, with ADAM reporting a build they are not on.
 */

import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..');

const results = [];
const pass = (what) => { results.push([true, what]); console.log(`  ok    ${what}`); };
const fail = (what, why) => { results.push([false, what]); console.log(`  FAIL  ${what}\n        ${why}`); };
const ok = (cond, what, why) => (cond ? pass(what) : fail(what, why));

const exists = (p) => stat(p).then(() => true, () => false);
const readJson = async (p) => JSON.parse(await readFile(p, 'utf8'));

const manifest = await readJson(path.join(HERE, '.claude-plugin', 'plugin.json'));
const market = await readJson(path.join(ROOT, '.claude-plugin', 'marketplace.json'));

console.log('\nthe manifests point at real files');

// ---- the marketplace resolves to this plugin --------------------------------

const entry = (market.plugins ?? []).find((p) => p.name === 'adam');
ok(entry, 'the marketplace lists the adam plugin', `plugins: ${JSON.stringify(market.plugins)}`);
if (entry) {
  ok(typeof entry.source === 'string' && entry.source.startsWith('./'),
    'the entry uses a relative source', `source: ${JSON.stringify(entry.source)}`);
  const target = path.resolve(ROOT, entry.source);
  ok(target === HERE, 'the entry resolves to the connector directory',
    `${target}\n        expected ${HERE}`);
  ok(await exists(path.join(target, '.claude-plugin', 'plugin.json')),
    'the resolved directory holds plugin.json', target);
  // An entry that also sets version would be overridden by plugin.json and
  // `claude plugin validate` only warns, so the two are kept from disagreeing.
  ok(!entry.version, 'the entry leaves the version to plugin.json',
    `entry version: ${entry.version}`);
}

// ---- every path in the manifest is a file -----------------------------------

const servers = manifest.mcpServers ?? {};
ok(Object.keys(servers).length === 1 && servers.adam,
  'the manifest declares exactly one server, named adam', Object.keys(servers).join(', '));

const args = servers.adam?.args ?? [];
const entryArg = args.find((a) => a.includes('${CLAUDE_PLUGIN_ROOT}'));
ok(entryArg, 'the server is launched from the plugin root', JSON.stringify(args));
if (entryArg) {
  const file = path.join(HERE, entryArg.replace('${CLAUDE_PLUGIN_ROOT}/', ''));
  ok(await exists(file), 'the server file the manifest names exists', file);
}

const hooksPath = path.join(HERE, String(manifest.hooks ?? '').replace(/^\.\//, ''));
ok(typeof manifest.hooks === 'string' && await exists(hooksPath),
  'the hooks file the manifest names exists', hooksPath);

// ---- user config is complete, both ways -------------------------------------

const declared = new Set(Object.keys(manifest.userConfig ?? {}));
const referenced = new Set();
for (const value of Object.values(servers.adam?.env ?? {})) {
  const m = /^\$\{user_config\.([A-Za-z0-9_]+)\}$/.exec(String(value));
  if (m) referenced.add(m[1]);
}
const undeclared = [...referenced].filter((k) => !declared.has(k));
ok(!undeclared.length, 'every ${user_config.*} the server uses is declared',
  `undeclared: ${undeclared.join(', ')}`);
const unused = [...declared].filter((k) => !referenced.has(k));
ok(!unused.length, 'every declared option is actually used', `unused: ${unused.join(', ')}`);

// The password is the one value that must not land in settings.json.
ok(manifest.userConfig?.password?.sensitive === true,
  'the password is marked sensitive, so it goes to the credential store',
  JSON.stringify(manifest.userConfig?.password));
ok(manifest.userConfig?.email?.required === true
  && manifest.userConfig?.viewer_url?.required === true,
  'the address and e-mail are required', 'an empty one installs a connector that cannot sign in');

// ---- the hooks file is exec form and points at the hook ----------------------

const hooks = await readJson(hooksPath);
const commands = Object.values(hooks.hooks ?? {}).flat()
  .flatMap((g) => g.hooks ?? []);
ok(commands.length >= 5, 'every hook event is wired', `${commands.length} commands`);
ok(commands.every((c) => Array.isArray(c.args) && c.args.length),
  'the hooks use exec form',
  'shell form re-parses the substituted path, and ${CLAUDE_PLUGIN_ROOT} can hold a space');
const hookFiles = new Set(commands.map((c) => c.args[0]));
ok(hookFiles.size === 1, 'every hook runs the same script', [...hookFiles].join(', '));
const hookFile = path.join(HERE, [...hookFiles][0].replace('${CLAUDE_PLUGIN_ROOT}/', ''));
ok(await exists(hookFile), 'the hook script exists', hookFile);

const modes = new Set(commands.map((c) => c.args[1]));
ok(modes.has('record') && modes.has('flush'),
  'the hooks use both modes', [...modes].join(', '));

// ---- the plugin and the zip behave differently where they must --------------

console.log('\nthe plugin install and the zip install diverge where they have to');

const hookSrc = await readFile(path.join(HERE, 'hooks', 'adam-hook.mjs'), 'utf8');
ok(hookSrc.includes('CLAUDE_PLUGIN_OPTION_'),
  'the hook reads the plugin\'s options as well as ADAM_*',
  'a plugin exports CLAUDE_PLUGIN_OPTION_<KEY> to hooks and sets no ADAM_* at all');

const updateSrc = await readFile(path.join(HERE, 'update.mjs'), 'utf8');
ok(updateSrc.includes('installedAsPlugin'),
  'the updater refuses to write into a plugin install',
  'the marketplace replaces the plugin directory, so an update written here is reverted later');
ok(/\.claude-plugin/.test(updateSrc),
  'the updater detects the plugin from disk, not the environment',
  'CLAUDE_PLUGIN_ROOT does not reach a script run from a shell');

const serverSrc = await readFile(path.join(HERE, 'server.mjs'), 'utf8');
ok(serverSrc.includes('CLAUDE_PLUGIN_ROOT'),
  'the connector knows which install it is', 'it has to, to give the right update command');
ok(serverSrc.includes('/plugin update'),
  'a plugin install is told to update through the marketplace',
  'sending it to update.mjs would have it write files the marketplace owns');
ok(serverSrc.includes('claude-code-plugin'),
  'the fleet list can tell the two installs apart',
  'without it there is no way to see how far the migration off the zip has got');

// The connector's build hash covers a fixed list of files; a plugin-only file
// added to the plugin but not to that list would ship unhashed.
const { FILES } = await import('./version.mjs');
for (const name of FILES) {
  // eslint-disable-next-line no-await-in-loop
  if (!await exists(path.join(HERE, name))) fail('every hashed file is present', name);
}
pass(`every hashed file is present (${FILES.length})`);

const failed = results.filter(([good]) => !good);
console.log(`\n${results.length - failed.length} of ${results.length} checks passed`);
process.exit(failed.length ? 1 : 0);
