/**
 * The account drawer and the bell — the chrome that belongs to *you* rather
 * than to a layer of the package.
 *
 * **Lifted out of app.js on 21 September so it can be on every page.** It was
 * 330 lines in the middle of the viewer's main file and its markup was 130
 * lines in `index.html`, which meant the eight standalone pages — settings,
 * admin, tasks, validation, reviews, changes, domains, audit — had no way to
 * reach it. A reader on the settings page could not see who they were signed in
 * as, could not check a mention, and could not sign out without going back to
 * the viewer first.
 *
 * **The markup moved here with the behaviour, and that is the point.** Copying
 * the drawer's HTML into nine pages would have made it nine things to keep in
 * step, which is the failure this codebase keeps writing comments about. The
 * module owns the markup, injects it where it is not already, and binds it the
 * same way everywhere.
 *
 *     import { mountAccountDrawer } from '/account-drawer.js';
 *     const drawer = mountAccountDrawer();
 *
 * The one thing a caller can change is where a mention goes when it is clicked.
 * In the viewer that is a hash on the page you are already on; on a standalone
 * page there is nothing to select, so it is a trip back to the viewer.
 */
import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

/** Local rather than core.js's, so a settings page does not pull the glossary,
 *  the tooltip engine and every layer's shared vocabulary in behind it. */
const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
};

/** Two letters for the avatar: initials where there is a name, otherwise the
 *  first two characters of the address. */
export function initialsOf(who) {
  const source = (who?.name || who?.email || '?').trim();
  const initials = source.includes(' ')
    ? source.split(/\s+/).slice(0, 2).map((w) => w[0]).join('')
    : source.slice(0, 2);
  return initials.toUpperCase();
}

// ── markup ──────────────────────────────────────────────────────────────────
// Moved verbatim out of index.html. The comments came with it: they say why
// each control is where it is, and a comment that stays behind when its markup
// moves is a comment about nothing.

/** Where you were named. It carries the note itself: a panel that says
 *  "3 notifications" and makes you go somewhere else to find out what for is
 *  one people stop opening. */
const BELL_HTML = `
<div class="palette-backdrop" id="bell-panel" hidden>
  <div class="account-dialog bell-dialog" role="dialog" aria-modal="true"
       aria-labelledby="bell-title">
    <h2 class="account-title" id="bell-title">Where you were named</h2>
    <p class="auth-note auth-fine" id="bell-note"></p>
    <div id="bell-list" class="bell-list"></div>
    <button class="auth-button auth-button-quiet" id="bell-seen" type="button" hidden>
      Mark all read
    </button>
    <a class="auth-button auth-button-quiet" href="/reviews.html">
      All review activity
    </a>
  </div>
</div>`;

/**
 * A panel from the right rather than a dialog in the middle. It opens from the
 * far right of the top bar, so it arrives from where the hand already is, and
 * it leaves the view it was opened over in sight.
 *
 * It holds what belongs to *you* — who you are, your settings, your reviews,
 * and the way out — and nothing that is really a page of the package.
 * Everything configurable lives on the settings page, which is the one large
 * button here.
 */
const DRAWER_HTML = `
<div class="account-backdrop" id="account-panel" hidden>
  <aside class="account-drawer" role="dialog" aria-modal="true" aria-labelledby="account-title">
    <header class="account-drawer-head">
      <h2 class="account-title" id="account-title">Sign in</h2>
      <button id="account-close" class="icon-btn account-close" type="button" aria-label="Close">
        <svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor"
             stroke-width="1.6" stroke-linecap="round"><path d="M4 4l8 8M12 4l-8 8" /></svg>
      </button>
    </header>

    <div class="account-drawer-body">
      <div id="account-signin">
        <p class="auth-note">
          Your session has ended. Sign in again to carry on — nothing you were
          looking at has moved.
        </p>
        <label class="auth-label" for="signin-email">Email</label>
        <input id="signin-email" class="auth-input" type="email"
               autocomplete="username" placeholder="you@softlabsgroup.com" />
        <label class="auth-label" for="signin-password">Password</label>
        <input id="signin-password" class="auth-input" type="password"
               autocomplete="current-password" />
        <p class="auth-error" id="signin-error" hidden></p>
        <button id="signin-submit" class="auth-button" type="button">Sign in</button>
        <p class="auth-note auth-fine">
          No account? Ask an admin for an invite link — accounts are made from
          invites, not from a signup page.
        </p>
      </div>

      <div id="account-signed" hidden>
        <div class="account-id">
          <span class="account-avatar" id="account-avatar" aria-hidden="true">·</span>
          <div class="account-id-text">
            <div class="account-who-name" id="account-name"></div>
            <div class="account-who-email" id="account-email"></div>
          </div>
          <span class="account-role" id="account-role"></span>
        </div>

        <a class="drawer-primary" href="/settings.html">
          <span class="drawer-primary-icon" aria-hidden="true">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor">
              <circle cx="8" cy="8" r="5.2" stroke-width="2.2" stroke-dasharray="2 2.08" />
              <circle cx="8" cy="8" r="3.4" stroke-width="1.4" />
              <circle cx="8" cy="8" r="1.2" fill="currentColor" stroke="none" />
            </svg>
          </span>
          <span class="drawer-primary-text">
            <b>Settings</b>
            <small>Password, OpenProject, git identity, the Claude connector and sessions</small>
          </span>
          <svg class="drawer-chevron" viewBox="0 0 16 16" aria-hidden="true" fill="none"
               stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
               stroke-linejoin="round"><path d="M6 3.5 10.5 8 6 12.5" /></svg>
        </a>

        <nav class="drawer-group" aria-labelledby="drawer-mine">
          <h3 class="drawer-group-title" id="drawer-mine">Your work</h3>
          <a class="drawer-link" href="/board.html">My work, and the testing gate</a>
          <a class="drawer-link" href="/agents.html">Agent activity</a>
        </nav>

        <nav class="drawer-group" aria-labelledby="drawer-reviews">
          <h3 class="drawer-group-title" id="drawer-reviews">Reviews</h3>
          <a class="drawer-link" href="/validation.html">What has been signed off</a>
          <a class="drawer-link" id="mentions-link" href="/reviews.html">Review activity</a>
          <a class="drawer-link" id="changes-link" href="/changes.html">Change requests</a>
        </nav>

        <nav class="drawer-group" aria-labelledby="drawer-explore">
          <h3 class="drawer-group-title" id="drawer-explore">Explore</h3>
          <a class="drawer-link" href="/domains.html">Domain lenses</a>
          <a class="drawer-link" href="/avatar.html">The avatar, and what it can do</a>
        </nav>

        <nav class="drawer-group" id="account-admin" hidden aria-labelledby="drawer-admin">
          <h3 class="drawer-group-title" id="drawer-admin">Administration</h3>
          <a class="drawer-link" href="/admin.html">Admin: accounts, invites and projects</a>
          <a class="drawer-link" href="/tasks.html">Tasks: the delivery overview</a>
          <a class="drawer-link" href="/audit.html">Audit the delivery package</a>
        </nav>
      </div>

      <p class="auth-note auth-fine" id="account-offline" hidden>
        The validation service is not running, so there is nothing to sign in
        to. Start it with:
        <code>python -m uvicorn api.main:app --port 8787</code>
      </p>
    </div>

    <footer class="account-drawer-foot" id="account-foot" hidden>
      <button id="signout" class="drawer-foot-btn" type="button">Sign out</button>
      <button id="signout-all" class="drawer-foot-btn drawer-foot-quiet" type="button">
        Sign out everywhere
      </button>
      <div id="signout-all-confirm" hidden>
        <p class="auth-note auth-fine">
          This ends every session on your account — every browser, every
          device, <b>including this one</b>. You will be signed out here and
          sent back to the door. Nothing else changes: your account stays
          enabled, you can sign straight back in, and every verdict you have
          recorded keeps your name on it.
        </p>
        <button id="signout-all-go" class="auth-button" type="button">
          Yes, end every session
        </button>
        <button id="signout-all-cancel" class="auth-button auth-button-quiet" type="button">
          Cancel
        </button>
      </div>
      <p class="auth-error" id="signout-all-error" hidden></p>
    </footer>
  </aside>
</div>`;

// ── behaviour ───────────────────────────────────────────────────────────────

// Whatever opened the drawer, so closing it hands the focus back there — the
// initials in the top bar usually, a verdict block asking for a sign-in
// sometimes — rather than dropping it on the page.
let accountOpener = null;
let mentionCache = [];
// Conditions rather than events — see showMentionCount. Held beside the
// mentions and never merged into them, because the two behave differently at
// every point: one can be marked read and the other cannot.
let alertCache = [];
let onMentionTarget = null;

export function openAccountPanel() {
  accountOpener = document.activeElement;
  $('account-panel').hidden = false;
  renderAccountPanel();
  (auth.account() ? $('account-close') : $('signin-email'))?.focus();
}

export function closeAccountPanel() {
  const panel = $('account-panel');
  if (!panel || panel.hidden) return;
  panel.hidden = true;
  if (accountOpener && document.contains(accountOpener)) accountOpener.focus();
  accountOpener = null;
}

function renderAccountPanel() {
  const who = auth.account();
  const reachable = auth.reachable();

  $('account-offline').hidden = reachable;
  $('account-signin').hidden = Boolean(who) || !reachable;
  $('account-signed').hidden = !who;
  $('account-foot').hidden = !who;
  $('account-title').textContent = who ? 'Your account' : 'Sign in';

  if (who) {
    $('account-avatar').textContent = initialsOf(who);
    // The name when there is one, with the address under it — the address is
    // what signs in; the name is only what people call you.
    $('account-name').textContent = who.name || who.email;
    $('account-email').textContent = who.name ? who.email : '';
    $('account-role').textContent = who.role;
    $('account-role').dataset.role = who.role;
    $('account-admin').hidden = !auth.isAdmin(who);
    // Never reopen already armed. This panel is opened and closed all day, and
    // a confirm left standing from a change of mind ten minutes ago would sit
    // one click from ending every session on the account.
    disarmSignOutAll();
  }
}

/** Puts "Sign out everywhere" back to its resting state — asking nothing. */
function disarmSignOutAll() {
  $('signout-all').hidden = false;
  $('signout-all-confirm').hidden = true;
  $('signout-all-error').hidden = true;
  $('signout-all-go').disabled = false;
  $('signout-all-go').textContent = 'Yes, end every session';
}

/**
 * How many notes have named you, on the account button and on the link that
 * leads to them.
 *
 * Asked once per sign-in rather than polled. A mention arrives when somebody
 * types it, which is not often enough to be worth a timer, and the count is
 * re-read whenever the account panel is opened.
 */
async function showMentionCount() {
  const bell = $('bell-toggle');
  const link = $('mentions-link');
  if (!bell) return;

  // Shown for anyone signed in, whether or not anything is waiting — and
  // before the fetch, so a slow or unreachable accounts service does not take
  // the control with it. Empty is a state a bell can say out loud. Gone is not.
  bell.hidden = false;

  // Two fetches, two different kinds of thing. A mention is an *event* — it
  // happened, it is stored, and marking it read is meaningful because the
  // moment has passed. An alert is a *condition*: it is true of the store right
  // now, it is computed on every read, and it cannot be marked read because the
  // only way to clear it is to fix what it is about. Keeping them apart here is
  // what stops the panel offering "mark all read" over an overdue request.
  //
  // allSettled, because the bell must draw whichever half answers: a reader
  // with three unread mentions should not lose them to an alerts query that
  // failed.
  const [mentions, standing] = await Promise.allSettled([
    auth.myMentions(), auth.myAlerts(),
  ]);
  if (mentions.status === 'rejected' && standing.status === 'rejected') {
    return;                       // the viewer is not about this
  }
  const payload = mentions.status === 'fulfilled' ? mentions.value : {};
  alertCache = (standing.status === 'fulfilled' ? standing.value.alerts : null) ?? [];
  mentionCache = payload.mentions ?? [];
  const unseen = payload.unseen ?? 0;

  // Only the *unread* mark comes and goes. The bell itself stays put, and it
  // keeps the history: "what did that say again" is a question people ask an
  // hour after reading something, and a control that empties itself on the
  // last read takes the answer with it.
  // An alert counts as unread for as long as it is true. There is no seen
  // state to set and setting one would be a way of turning an escalation off,
  // which is the one thing it must not have.
  const standingCount = alertCache.length;
  const waiting = unseen + standingCount;
  const loud = alertCache.some((a) => a.severity === 'high');

  bell.classList.toggle('has-mentions', waiting > 0);
  bell.classList.toggle('has-alert', loud);
  bell.title = standingCount
    ? alertCache.map((a) => a.title).join(' · ')
    : unseen
      ? `${unseen} note${unseen === 1 ? '' : 's'} named you`
      : mentionCache.length
        ? 'Where you were named'
        : 'No notifications';

  const count = $('bell-count');
  count.textContent = waiting > 9 ? '9+' : String(waiting);
  count.hidden = waiting === 0;

  if (link) {
    link.textContent = unseen ? `Review activity - ${unseen} named you` : 'Review activity';
    link.classList.toggle('auth-button-loud', unseen > 0);
  }
  const changes = $('changes-link');
  if (changes) {
    changes.textContent = standingCount
      ? `Change requests - ${standingCount} waiting`
      : 'Change requests';
    changes.classList.toggle('auth-button-loud', loud);
  }
}

/** The other half of `showMentionCount`: the bell persists across having
 *  nothing to say, but not across having nobody to say it to. */
function hideBell() {
  const bell = $('bell-toggle');
  if (!bell) return;
  mentionCache = [];
  bell.hidden = true;
  bell.classList.remove('has-mentions');
  $('bell-count').hidden = true;
  if (!$('bell-panel').hidden) closeBellPanel();
}

/** The panel behind the bell. Drawn from what the count already fetched, so
 *  opening it costs nothing and never shows a spinner over three rows. */
function renderBellPanel() {
  const list = $('bell-list');
  list.innerHTML = '';
  const unseen = mentionCache.filter((m) => !m.seen_at).length;

  // Standing first, and above the rule. A mention is something that happened;
  // an alert is something that is still happening, and the thing still
  // happening is the one to read first.
  for (const alert of alertCache) {
    const row = el('div', `bell-alert bell-alert-${alert.severity}`);
    const head = el('div', 'bell-row-head');
    head.append(el('span', 'bell-alert-title', alert.title));
    row.append(head);
    row.append(el('p', 'bell-alert-detail', alert.detail));
    if (alert.items.length) {
      const named = el('div', 'bell-alert-items');
      for (const item of alert.items) {
        const chip = el('button', 'bell-alert-chip',
          `${item.id}${item.days ? ` · ${item.days}d` : ''}`);
        chip.type = 'button';
        chip.title = item.slice ? `${item.title} — ${item.slice}` : item.title;
        chip.onclick = () => { closeBellPanel(); location.href = alert.href; };
        named.append(chip);
      }
      if (alert.count > alert.items.length) {
        named.append(el('span', 'bell-alert-more', `and ${alert.count - alert.items.length} more`));
      }
      row.append(named);
    }
    // No "mark read". There is nothing to mark: the alert is a reading of the
    // store and it goes when the store changes, which is the only way it
    // should go.
    const go = el('button', 'chip bell-alert-go', 'Open the change requests');
    go.type = 'button';
    go.onclick = () => { closeBellPanel(); location.href = alert.href; };
    row.append(go);
    list.append(row);
  }

  $('bell-note').textContent = mentionCache.length
    ? (unseen ? `${unseen} unread of ${mentionCache.length}` : `${mentionCache.length}, all read`)
    : alertCache.length ? 'Nobody has named you' : 'No notifications';
  $('bell-seen').hidden = unseen === 0;

  // Said in the list rather than only in the line above it, because the empty
  // list is the thing the eye lands on and a blank box is ambiguous between
  // "nothing here" and "did not load".
  if (!mentionCache.length) {
    // Only when there is genuinely nothing. With an alert drawn above, "nobody
    // has named you yet" is true and "no notifications" is not, so the sentence
    // stays and the framing changes.
    if (alertCache.length) return;
    const empty = el('p', 'bell-empty');
    empty.append('Nobody has named you yet. When someone writes ');
    empty.append(el('span', 'bell-empty-handle', `@${auth.account()?.email ?? 'your address'}`));
    empty.append(' in a note on a contract, a screen or a table, it will show up here.');
    list.append(empty);
    return;
  }

  // Everything, not the newest eight. The list scrolls, so a cap here bought
  // nothing and cost the reader the difference between "that is all of them"
  // and "that is as many as this box felt like drawing".
  for (const m of mentionCache) {
    const row = el('div', `bell-row${m.seen_at ? '' : ' unread'}`);
    const head = el('div', 'bell-row-head');
    head.append(el('span', 'bell-who', m.by || m.by_email));
    const target = el('button', 'bell-target', m.target_id);
    target.type = 'button';
    // Goes to the thing rather than to a list of things, because the reason
    // somebody was named is always about one artefact.
    target.onclick = () => {
      closeBellPanel();
      onMentionTarget(m);
    };
    head.append(target);
    row.append(head);
    row.append(auth.renderNote(m.note));
    list.append(row);
  }
}

function openBellPanel() {
  renderBellPanel();
  $('bell-panel').hidden = false;
  $('bell-toggle').setAttribute('aria-expanded', 'true');
}

export function closeBellPanel() {
  const panel = $('bell-panel');
  if (!panel) return;
  panel.hidden = true;
  $('bell-toggle')?.setAttribute('aria-expanded', 'false');
}

/** The initials in the topbar, and what the button says it is for. */
export function renderAccountButton() {
  const who = auth.account();
  const badge = $('account-initials');
  const button = $('account-toggle');
  if (!badge || !button) return;

  if (!who) {
    badge.textContent = '·';
    button.classList.remove('signed-in');
    button.title = auth.reachable()
      ? 'Sign in to record verdicts'
      : 'The validation service is not running';
    return;
  }
  badge.textContent = initialsOf(who);
  button.classList.add('signed-in');
  button.title = `${who.email} — ${who.role}`;
}

/**
 * The hash the viewer selects a thing by. The same rule the bell used inline
 * before this moved: an operation is addressed bare, everything else by kind.
 */
export const mentionHash = (m) =>
  encodeURIComponent(m.target_kind === 'operation' ? m.target_id : `${m.target_kind}:${m.target_id}`);

/**
 * Put the drawer on this page and wire it.
 *
 * Injects the markup only where it is not already in the document, so the
 * viewer — which used to carry it inline and may again — cannot end up with
 * two. Safe to call once per page; calling it twice rebinds the same nodes.
 */
export function mountAccountDrawer({ onTarget } = {}) {
  // In the viewer a mention is a selection on the page you are already on. On
  // a standalone page there is nothing to select, so it is a trip back.
  onMentionTarget = onTarget ?? ((m) => { location.href = `/#${mentionHash(m)}`; });

  if (!$('bell-panel')) document.body.insertAdjacentHTML('beforeend', BELL_HTML);
  if (!$('account-panel')) document.body.insertAdjacentHTML('beforeend', DRAWER_HTML);

  const bell = $('bell-toggle');
  if (bell) {
    bell.onclick = () => ($('bell-panel').hidden ? openBellPanel() : closeBellPanel());
    $('bell-panel').onclick = (e) => { if (e.target === $('bell-panel')) closeBellPanel(); };
    $('bell-seen').onclick = async () => {
      $('bell-seen').disabled = true;
      try {
        await auth.markMentionsSeen();
        for (const m of mentionCache) m.seen_at = m.seen_at ?? new Date().toISOString();
        renderBellPanel();
        showMentionCount();
      } finally {
        $('bell-seen').disabled = false;
      }
    };
  }

  $('account-toggle').onclick = () =>
    ($('account-panel').hidden ? openAccountPanel() : closeAccountPanel());
  $('account-panel').onclick = (e) => { if (e.target === $('account-panel')) closeAccountPanel(); };
  $('account-close').onclick = closeAccountPanel;
  // a verdict block asking for a sign-in
  document.addEventListener('ticvai:signin', openAccountPanel);

  const signInError = (message) => {
    $('signin-error').textContent = message;
    $('signin-error').hidden = false;
  };

  const doSignIn = async () => {
    $('signin-error').hidden = true;
    $('signin-submit').disabled = true;
    $('signin-submit').textContent = 'Signing in…';
    try {
      await auth.signIn($('signin-email').value.trim(), $('signin-password').value);
      $('signin-password').value = '';
      closeAccountPanel();
      // A page drawn for a signed-out reader stays drawn for one. The viewer
      // redraws itself on the auth change; a standalone page has no such loop,
      // so the honest move is to draw it again from the top.
      if (document.body.classList.contains('admin-page')) location.reload();
    } catch (error) {
      signInError(error.message);
    } finally {
      $('signin-submit').disabled = false;
      $('signin-submit').textContent = 'Sign in';
    }
  };

  $('signin-submit').onclick = doSignIn;
  for (const id of ['signin-email', 'signin-password']) {
    $(id).addEventListener('keydown', (e) => { if (e.key === 'Enter') doSignIn(); });
  }

  $('signout').onclick = async () => {
    await auth.signOut();
    // The session behind this panel is gone, so closing the panel would leave a
    // fully drawn viewer — the tree, the graph, somebody's verdicts — sitting
    // there looking signed in. Every next click would 401 and bounce, which
    // reads as the app breaking rather than as the sign-out having worked.
    location.replace('/login.html');
  };

  // Two presses, and the second one is a different button under a paragraph
  // that says what the first one only implies.
  $('signout-all').onclick = () => {
    $('signout-all').hidden = true;
    $('signout-all-confirm').hidden = false;
    $('signout-all-error').hidden = true;
    $('signout-all-go').focus();
  };
  $('signout-all-cancel').onclick = disarmSignOutAll;

  $('signout-all-go').onclick = async () => {
    $('signout-all-error').hidden = true;
    $('signout-all-go').disabled = true;
    $('signout-all-go').textContent = 'Ending every session…';
    try {
      await auth.logoutAll();
      location.replace('/login.html');
    } catch (error) {
      // Nothing was revoked, so nothing about the panel changes except this
      // line. Leaving it armed is deliberate: the usual cause is the service
      // being down for a moment, and the next press is the one that works.
      $('signout-all-error').textContent = error.message;
      $('signout-all-error').hidden = false;
      $('signout-all-go').disabled = false;
      $('signout-all-go').textContent = 'Yes, end every session';
    }
  };

  // Escape closes whichever is open. The viewer binds its own key handling and
  // calls these; a standalone page has none, so the drawer brings its own.
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    if (!$('bell-panel')?.hidden) { e.preventDefault(); closeBellPanel(); return; }
    if (!$('account-panel')?.hidden) { e.preventDefault(); closeAccountPanel(); }
  });

  auth.onAuthChange(() => {
    renderAccountButton();
    // The bell has to be told on sign-in, not on the first time somebody opens
    // the account panel. It was hanging off renderAccountPanel, which meant the
    // one control whose job is to tell you something unprompted only appeared
    // once you had gone looking — exactly the failure it exists to fix.
    if (auth.account()) showMentionCount();
    else hideBell();
    if (!$('account-panel').hidden) renderAccountPanel();
  });
  auth.refreshSession();

  return { openAccountPanel, closeAccountPanel, closeBellPanel, renderAccountButton };
}
