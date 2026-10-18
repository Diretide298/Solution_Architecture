/**
 * ADAM's own files in a developer's workspace, as the starters have them now (CHG-ADM-006).
 *
 * Served at `/connector/workspace?role=backend|frontend` so `/update-adam` can refresh a workspace that was made
 * before a change: setup only ever added files that were missing, so an existing folder kept its old `/ticket` for
 * good. The five command files are ADAM's and are sent whole. CLAUDE.md is the team's, so it is sent whole too and
 * the receiver takes only the parts between ADAM's markers (`<!-- ADAM:start name -->` ... `<!-- ADAM:end name -->`).
 *
 * The same text as the setup zip's starters, because it is read from them: one place to edit, never a copy.
 */

import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const STARTERS = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'mcp', 'setup', 'starters');

/** The command files ADAM owns, in the order they are listed. Bare names: the receiver accepts nothing else. */
export const COMMAND_FILES = ['ticket.md', 'board.md', 'cr.md', 'done.md', 'update-adam.md'];

export const ROLES = ['backend', 'frontend'];

/**
 * @param {string} role backend or frontend
 * @param {string} [starters] where the starters are (the viewer's own copy by default)
 * @returns {Promise<{role: string, commands: {name: string, text: string}[], claudeMd: string}|null>} null for a role
 *   that is neither, which the route answers with 400
 */
export async function workspaceFilesOf(role, starters = STARTERS) {
  if (!ROLES.includes(role)) return null;
  const commands = [];
  for (const name of COMMAND_FILES) {
    const text = await readFile(path.join(starters, role, '.claude', 'commands', name), 'utf8').catch(() => null);
    if (text !== null) commands.push({ name, text });
  }
  const claudeMd = await readFile(path.join(starters, role, 'CLAUDE.md'), 'utf8').catch(() => '');
  return { role, commands, claudeMd };
}
