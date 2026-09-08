/**
 * The settings page: what one developer configures about themselves.
 *
 * Three panels, and each is a different kind of thing. The OpenProject token is
 * a live credential to another system — it is checked before it is kept, shown
 * back only as its last four characters, and removing it here is said plainly
 * *not* to revoke it there. The git identity is not a secret and is stored as
 * typed. The bridge line is not stored at all; it is assembled from the account
 * so nobody has to hand-write it.
 *
 * Nothing on this page ever holds a token after the request that saves it. The
 * field is cleared on success, because a password box left full is a password
 * box somebody walks away from.
 */

import {
  requireSignIn, mySettings, saveGitIdentity,
  saveOpenProjectToken, forgetOpenProjectToken,
} from '/validation.js';

const $ = (id) => document.getElementById(id);

/** A one-line answer under a control. Tone is colour only — the sentence has to
 *  work without it, for the same reason an error is never just a red border. */
function say(node, text, tone = '') {
  node.textContent = text;
  if (tone) node.dataset.tone = tone;
  else delete node.dataset.tone;
}

/** Whatever the server refused with, or something honest when it did not say. */
const because = (error) => error?.message || 'That did not work. Try again.';

function drawOpenProject(state) {
  const badge = $('op-state');
  const forget = $('op-forget');
  const { configured, hint, endpoint } = state.openproject;

  badge.textContent = configured ? `connected ${hint}` : 'not connected';
  badge.dataset.on = configured ? 'yes' : 'no';
  forget.hidden = !configured;
  $('op-endpoint').value = endpoint ?? '';
  $('op-save').textContent = configured ? 'Replace' : 'Check and save';

  // A deployment with no encryption key cannot store a credential. Say so
  // before the field rather than after somebody types a live token into it.
  if (!state.canStoreCredentials) {
    const note = $('op-nokey');
    note.hidden = false;
    note.innerHTML = '<strong>This deployment cannot store credentials yet.</strong> ';
    note.append(state.whyNot ?? 'No encryption key is configured.');
    $('op-token').disabled = true;
    $('op-save').disabled = true;
  }
}

/**
 * The line a developer runs to wire up the bridge, with their own address in
 * it. The password is deliberately left as a placeholder: this page has never
 * seen it and must not pretend otherwise.
 */
function drawBridge(state) {
  $('mcp-line').textContent = [
    'claude mcp add adam -- node <path-to>/adam/viewer/mcp/server.mjs \\',
    `  -e ADAM_VIEWER_URL=${location.origin} \\`,
    `  -e ADAM_EMAIL=${state.email} \\`,
    '  -e ADAM_PASSWORD=<your password>',
  ].join('\n');
}

async function load() {
  const state = await mySettings();
  $('whoami').textContent = state.email;
  $('git-email').value = state.gitEmail ?? '';
  drawOpenProject(state);
  drawBridge(state);
  return state;
}

function wire() {
  $('git-save').addEventListener('click', async () => {
    const says = $('git-says');
    say(says, 'Saving…');
    try {
      const answer = await saveGitIdentity($('git-email').value.trim());
      say(says, answer.gitEmail ? `Saved — ${answer.gitEmail}` : 'Cleared.', 'good');
    } catch (error) {
      say(says, because(error), 'bad');
    }
  });

  $('op-save').addEventListener('click', async () => {
    const says = $('op-says');
    const token = $('op-token').value.trim();
    if (!token) return say(says, 'Paste a token first.', 'bad');

    say(says, 'Checking it against OpenProject…');
    try {
      const answer = await saveOpenProjectToken(token, $('op-endpoint').value.trim());
      // Cleared the moment it is stored. A token sitting in a field is a token
      // on somebody's screen.
      $('op-token').value = '';
      // Who it turned out to be — so a wrong token is caught now, not when work
      // starts being attributed to somebody else.
      say(says, `Connected as ${answer.connectedAs}. Stored as ${answer.hint}.`, 'good');
      await load();
    } catch (error) {
      say(says, because(error), 'bad');
    }
  });

  $('op-forget').addEventListener('click', async () => {
    const says = $('op-says');
    say(says, 'Removing…');
    try {
      const answer = await forgetOpenProjectToken();
      // The server's own sentence, which says removing it here does not revoke
      // it there. Substituting a cheerier one would be the lie.
      say(says, answer.note, 'good');
      await load();
    } catch (error) {
      say(says, because(error), 'bad');
    }
  });

  $('mcp-copy').addEventListener('click', async () => {
    const says = $('mcp-says');
    try {
      await navigator.clipboard.writeText($('mcp-line').textContent);
      say(says, 'Copied — put your own password in before running it.', 'good');
    } catch {
      // Clipboard access is refused in plenty of ordinary situations, and the
      // text is on the screen either way.
      say(says, 'Could not copy — select it and copy by hand.', 'bad');
    }
  });
}

if (await requireSignIn()) {
  try {
    await load();
    $('settings').hidden = false;
    wire();
  } catch (error) {
    // Signed in, and the settings would not load — a different fault from being
    // signed out, and it must not present as one.
    $('signed-out').hidden = false;
    $('signed-out').querySelector('.auth-title').textContent = 'That did not load';
    $('signed-out').querySelector('.auth-note').textContent = because(error);
  }
}
