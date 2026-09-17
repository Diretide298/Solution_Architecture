/**
 * The settings page: everything one person configures about themselves.
 *
 * One page with a section list rather than a panel of links, so there is a
 * single place to go and everything on it can be deep-linked
 * (`/settings.html#password`). The account drawer in the viewer points here.
 *
 * The sections are different kinds of thing, and are treated differently. The
 * password is checked by the server and changing it signs out every other
 * session. The OpenProject token is a live credential to another system — it is
 * checked before it is kept, shown back only as its last four characters, and
 * removing it here is said plainly *not* to revoke it there. The git identity is
 * not a secret and is stored as typed. The connector line is not stored at all;
 * it is assembled from the account so nobody has to hand-write it.
 *
 * Nothing on this page holds a secret after the request that uses it. Password
 * and token fields are cleared on success, because a password box left full is
 * a password box somebody walks away from.
 */

import {
  requireSignIn, account, mySettings, saveGitIdentity,
  saveOpenProjectToken, forgetOpenProjectToken,
  changePassword, signOut, logoutAll,
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

const MIN_PASSWORD = 12;   // the server's rule, said here so the answer is instant

const ROLE_SAYS = {
  reviewer: 'Read everything, and record reviews.',
  admin: 'Everything a reviewer can, plus invite people, manage accounts and make password-reset links.',
  client: 'Read everything except Decisions. Your reviews are kept separately, as the client review.',
};

/** The same two letters the viewer's top bar shows. */
function initialsOf(name, email) {
  const source = (name || email).trim();
  const initials = source.includes(' ')
    ? source.split(/\s+/).slice(0, 2).map((w) => w[0]).join('')
    : source.slice(0, 2);
  return initials.toUpperCase();
}

function drawAccount(state, who) {
  const role = who?.role ?? '';
  $('whoami').textContent = state.email;
  $('me-avatar').textContent = initialsOf(state.name, state.email);
  $('me-name').textContent = state.name || state.email;
  $('me-email').textContent = state.name ? state.email : '';
  $('me-role').textContent = role;
  $('me-role').dataset.role = role;
  $('me-role-says').textContent = ROLE_SAYS[role] ?? '—';

  const admin = role === 'admin';
  $('admin').hidden = !admin;
  $('nav-admin').hidden = !admin;
  $('nav-admin-group').hidden = !admin;
}

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
 * The line a developer runs to wire up the connector, with their own address in
 * it. The password is deliberately left as a placeholder: this page has never
 * seen it and must not pretend otherwise.
 *
 * **Every `-e` goes before the `--`.** Everything after `--` is handed to node
 * as arguments, and server.mjs never reads its arguments — so the first version
 * of this line, with the `-e` flags at the end, registered a server with no
 * credentials at all, which then could not sign in.
 *
 * **And the `--` is quoted.** In PowerShell `claude` is npm's `claude.ps1`
 * wrapper, and PowerShell drops a bare `--` handed to a script — the `-e` list
 * then swallows `node` and the path, and claude fails with "missing required
 * argument 'commandOrUrl'". A quoted `'--'` reaches claude intact in PowerShell,
 * and bash removes the quotes, so one line works in both.
 *
 * One line rather than `\` continuations, because `\` is not a continuation in
 * PowerShell, and placeholders in plain capitals rather than `<angle brackets>`,
 * which both shells read as redirection. The password is single-quoted, which
 * both shells treat literally. `-s user` so the connector is there in every repo
 * a developer opens, not only in the directory they happened to run this from.
 */
function drawConnector(state) {
  $('mcp-line').textContent =
    `claude mcp add -s user adam -e ADAM_VIEWER_URL=${location.origin} ` +
    `-e ADAM_EMAIL=${state.email} -e 'ADAM_PASSWORD=YOUR_PASSWORD' ` +
    "'--' node PATH-TO-REPO/viewer/mcp/server.mjs";
}

async function load() {
  const state = await mySettings();
  drawAccount(state, account());
  $('git-email').value = state.gitEmail ?? '';
  drawOpenProject(state);
  drawConnector(state);
  return state;
}

/** Marks the section being read in the list on the left. */
function followScroll() {
  const links = new Map(
    [...document.querySelectorAll('.set-nav a[href^="#"]')].map((a) => [a.getAttribute('href').slice(1), a]),
  );
  const mark = (id) => {
    for (const [key, link] of links) link.setAttribute('aria-current', String(key === id));
  };
  for (const [id, link] of links) link.addEventListener('click', () => mark(id));

  const watcher = new IntersectionObserver((entries) => {
    const showing = entries.filter((e) => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (showing.length) mark(showing[0].target.id);
  }, { rootMargin: '-90px 0px -55% 0px' });
  for (const section of document.querySelectorAll('.set-section')) watcher.observe(section);

  mark(location.hash.slice(1) || 'account');
}

function wirePassword() {
  $('pw-submit').addEventListener('click', async () => {
    const says = $('pw-says');
    const current = $('pw-current').value;
    const next = $('pw-new').value;
    if (!current) return say(says, 'Type your current password first.', 'bad');
    if (next.length < MIN_PASSWORD) {
      return say(says, `A password needs at least ${MIN_PASSWORD} characters.`, 'bad');
    }
    if (next !== $('pw-confirm').value) return say(says, 'Those two passwords are not the same.', 'bad');

    $('pw-submit').disabled = true;
    say(says, 'Changing it…');
    try {
      await changePassword(current, next);
      for (const id of ['pw-current', 'pw-new', 'pw-confirm']) $(id).value = '';
      say(says, 'Changed. Every other session on your account has been signed out.', 'good');
    } catch (error) {
      say(says, because(error), 'bad');
    } finally {
      $('pw-submit').disabled = false;
    }
  });
}

function wireConnections() {
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
      say(says, 'Copied — put your own password and path in before running it.', 'good');
    } catch {
      // Clipboard access is refused in plenty of ordinary situations, and the
      // text is on the screen either way.
      say(says, 'Could not copy — select it and copy by hand.', 'bad');
    }
  });
}

function wireSessions() {
  const confirm = $('sess-all-confirm');
  const says = $('sess-says');

  $('sess-signout').addEventListener('click', async () => {
    await signOut();
    // The session behind this page is gone; the door is the honest place to land.
    location.replace('/login.html');
  });

  // Two presses, and the second is a different button under a sentence that
  // says what the first only implies — the part that surprises people is that
  // "everywhere" includes this browser.
  $('sess-all').addEventListener('click', () => {
    confirm.hidden = false;
    $('sess-all').disabled = true;
    say(says, '');
    $('sess-all-go').focus();
  });
  $('sess-all-cancel').addEventListener('click', () => {
    confirm.hidden = true;
    $('sess-all').disabled = false;
  });
  $('sess-all-go').addEventListener('click', async () => {
    $('sess-all-go').disabled = true;
    $('sess-all-go').textContent = 'Ending every session…';
    try {
      await logoutAll();
      location.replace('/login.html');
    } catch (error) {
      // Nothing was revoked, so say so and leave it armed: the usual cause is
      // the service being down for a moment, and the next press is the one
      // that works. Signing out locally anyway would claim the other devices
      // were cleared when they were not.
      say(says, because(error), 'bad');
      $('sess-all-go').disabled = false;
      $('sess-all-go').textContent = 'Yes, end every session';
    }
  });
}

if (await requireSignIn()) {
  try {
    await load();
    $('settings').hidden = false;
    wirePassword();
    wireConnections();
    wireSessions();
    followScroll();
    // The page was hidden when the browser tried to jump to the #section in the
    // address, so the jump is made again now that there is something to land on.
    if (location.hash) $(location.hash.slice(1))?.scrollIntoView();
  } catch (error) {
    // Signed in, and the settings would not load — a different fault from being
    // signed out, and it must not present as one.
    $('signed-out').hidden = false;
    $('signed-out').querySelector('.auth-title').textContent = 'That did not load';
    $('signed-out').querySelector('.auth-note').textContent = because(error);
  }
}
