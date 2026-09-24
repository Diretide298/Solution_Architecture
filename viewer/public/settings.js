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

// The viewer's top bar on a page that is not the viewer: the layer tabs, the
// bell and the account drawer. Eight pages had none of it.
import '/page-chrome.js';
import {
  requireSignIn, account, mySettings, saveGitIdentity,
  saveOpenProjectToken, forgetOpenProjectToken,
  changePassword, signOut, logoutAll, project, isAdmin, isOwner,
  connectorFleet, servedBuild,
} from '/validation.js';
import { followSections } from '/sections.js';

const $ = (id) => document.getElementById(id);

/** A node with a class and its text. Local, like the one on the agents page:
 *  three lines is less to carry than importing the viewer's whole core module
 *  into a page that draws one table. */
function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

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
  owner: 'Everything an admin can, plus the Build layer, the IP allowlist and granting roles. Set on the machine, not from here.',
  admin: 'Everything a reviewer can, plus invite people, manage accounts and make password-reset links.',
  pm: 'Read everything an admin can read. Records nothing — not a review, not a change request decision.',
  lead: 'See all activity and every change request. Notified about, and settle, the platforms you own.',
  dev: 'Your own tasks and backlog, and the package behind them.',
  reviewer: 'Read everything, and record reviews.',
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

  // The owner administers too, so this is the shared predicate rather than a
  // comparison — see isAdmin in validation.js.
  const admin = isAdmin({ role });
  $('admin').hidden = !admin;
  $('nav-admin').hidden = !admin;
  $('nav-admin-group').hidden = !admin;
  // Inside the admin section and narrower than it: the allowlist and the log of
  // where people sign in from are the super admin's, and an admin opening that
  // page is told so rather than shown an empty one.
  $('link-networks').hidden = !isOwner({ role });
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
    // ADAM_PROJECT picks the package, and so the OpenProject project the
    // board reads. The one this browser last opened is the likeliest answer.
    `claude mcp add -s user adam -e ADAM_VIEWER_URL=${location.origin} ` +
    `-e ADAM_PROJECT=${project() ?? 'PROJECT-ID'} ` +
    `-e ADAM_EMAIL=${state.email} -e 'ADAM_PASSWORD=YOUR_PASSWORD' ` +
    "'--' node PATH-TO-REPO/viewer/mcp/server.mjs";
}

/** When an install last said anything, in words rather than a timestamp.
 *
 *  "3 days ago" is the form the question is asked in -- nobody reading this
 *  wants to subtract dates to find out whether an update has landed. */
function ago(stamp) {
  const then = Date.parse(stamp);
  if (!Number.isFinite(then)) return 'at some point';
  const days = Math.floor((Date.now() - then) / 86400000);
  if (days <= 0) return 'today';
  if (days === 1) return 'yesterday';
  if (days < 31) return `${days} days ago`;
  const months = Math.round(days / 30);
  return months <= 1 ? 'a month ago' : `${months} months ago`;
}

/**
 * Who is on which build.
 *
 * Two independent sources, deliberately: the accounts service says what each
 * install last reported, and the viewer says what it is serving. The comparison
 * is made here because neither side should be asked to hold the other's number.
 *
 * **Failure is a sentence, not an empty panel.** The rest of this section tells
 * somebody how to install a connector, and it has to keep working when the build
 * list does not -- so nothing here can throw into `load()`.
 */
async function drawFleet() {
  const host = $('fleet-list');
  const lede = $('fleet-serving');
  host.innerHTML = '';

  const [serving, fleet] = await Promise.all([
    servedBuild().catch(() => null),
    connectorFleet().catch(() => null),
  ]);

  if (!fleet) {
    say(lede, 'ADAM could not say which builds are installed.', 'bad');
    return;
  }

  const installs = fleet.installs ?? [];
  // The count of what is behind, not of what is installed: "four installs" is a
  // fact nobody acts on, and "two are behind" is the whole reason to look.
  const behind = serving ? installs.filter((i) => i.build !== serving).length : 0;
  lede.textContent = serving
    ? `ADAM is serving ${serving}.`
      + (installs.length
        ? ` ${behind === 0 ? 'Every install reporting in is on it.'
          : `${behind} of ${installs.length} ${behind === 1 ? 'is' : 'are'} behind.`}`
        : ' Nothing has reported a build yet.')
    : 'This ADAM does not serve a build yet, so there is nothing to compare against.';
  delete lede.dataset.tone;

  if (!installs.length) {
    host.append(el('p', 'auth-note auth-fine',
      fleet.whole
        ? 'No connector has reported in. An install reports itself when Claude Code '
          + 'starts, and one that predates this feature reports nothing until it is updated.'
        : 'Your connector has not reported in yet. It does so when Claude Code starts.'));
    return;
  }

  for (const install of installs) {
    const row = el('div', 'admin-row');
    // Whose, only when it could be somebody else's: on a developer's own page
    // every row is theirs and a column of one repeated name is noise.
    row.append(el('span', 'account-name',
      fleet.whole ? install.name : (install.host || 'this machine')));
    if (fleet.whole) row.append(el('span', 'invite-who', install.host || 'unnamed machine'));
    row.append(el('span', 'set-mono', install.build || 'unreadable'));
    const current = serving && install.build === serving;
    row.append(el('span', `ag-verdict${current || !serving ? '' : ' bad'}`,
      !serving ? '' : current ? 'current' : 'behind'));
    row.append(el('span', 'invite-who', `seen ${ago(install.at)}`));
    host.append(row);
  }
}

async function load() {
  const state = await mySettings();
  drawAccount(state, account());
  $('git-email').value = state.gitEmail ?? '';
  drawOpenProject(state);
  drawConnector(state);
  return state;
}

/** Marks the section being read in the list on the left. Shared with the admin
 *  and tasks pages, which are the same page shape. */
const followScroll = () => followSections('account');

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
    // Not awaited and not inside load(): the build list is the one thing on this
    // page that asks two services a question, and a page that will not show
    // somebody their password form because a build list timed out is worse than
    // a build list that arrives a moment late.
    drawFleet().catch(() => {});
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
