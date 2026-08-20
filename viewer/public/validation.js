/**
 * Who is signed in, and what they have decided about an artefact.
 *
 * The viewer is behind a sign-in: requireSignIn() runs before anything is
 * fetched, so a stranger is sent to the door rather than handed two megabytes
 * of somebody's architecture. Signing in is also what makes a verdict worth
 * having, since the whole value of one is knowing who gave it.
 *
 * Everything here talks to the FastAPI service, which is a separate process on
 * a separate port. If it is not running nobody can get in at all, which is the
 * price of the gate; the sign-in page is the one place that says so plainly.
 */

// Where the accounts service is, in the three arrangements there are.
//
// Most specific first:
//
//   1. `ticvai-api` in localStorage — what the check harnesses set, and the
//      only one that survives a page the server did not render.
//   2. `<meta name="ticvai-api">`, written into the page by server.mjs from
//      TICVAI_API_PUBLIC. This is the split deployment: the reading server on
//      one name and this service on another, so the browser calls the second
//      one directly and the node proxy is not in the path.
//   3. Neither, and then the host decides. Anything other than localhost is
//      the one-origin deployment, where the right base is the empty string —
//      same origin, no CORS, one cookie both halves see. Localhost is a
//      workstation, the only place the two ports are apart.
//
// Cross-origin either way: calls carry credentials: 'include' so the session
// cookie rides along, which is also why the service can never allow "*".
const declared = document.querySelector('meta[name="ticvai-api"]')?.content?.trim();
const sameOrigin = !/^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
const API = localStorage.getItem('ticvai-api')
  ?? (declared || (sameOrigin ? '' : 'http://localhost:8787'));

/** What a *review* can say. Three values, unchanged: this is somebody judging
 *  an artefact, and the vocabulary for answering one lives below. */
export const VERDICTS = [
  ['approved', 'Approved'],
  ['needs-work', 'Needs work'],
  ['rejected', 'Rejected'],
];

/**
 * How the team answered a review — the tracker's "Our verdict" column.
 *
 * Deliberately not more verdicts. A verdict is what the reviewer thinks; this
 * is what was done about it, and they are different columns in the spreadsheet
 * for the same reason they are different fields here. "Needs work" answered by
 * "Built" is a complete exchange; two verdicts in a row is an argument.
 *
 * Recorded when an item is closed, so closing now says *how* rather than only
 * that it happened.
 */
export const RESPONSES = [
  ['built', 'Built'],
  ['wired', 'Wired'],
  ['answered', 'Answered'],
  ['accepted', 'Accepted'],
  ['approved-no-action', 'Approved — no action'],
];

/** The two verdicts that put work in a queue. Everything else is a resolution. */
export const ASKS_FOR_WORK = new Set(['needs-work', 'rejected']);
export const asksForWork = (verdict) => ASKS_FOR_WORK.has(verdict);

/** Cached so every verdict block on a page does not ask again. */
let session = { signedIn: false, account: null, reachable: true };
const listeners = new Set();

export const account = () => (session.signedIn ? session.account : null);
export const reachable = () => session.reachable;
export const onAuthChange = (fn) => { listeners.add(fn); return () => listeners.delete(fn); };
const announce = () => { for (const fn of listeners) fn(session); };

async function call(path, { method = 'GET', body } = {}) {
  const res = await fetch(`${API}${path}`, {
    method,
    credentials: 'include',
    headers: body === undefined ? {} : { 'content-type': 'application/json' },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  let data = null;
  try { data = await res.json(); } catch { /* an empty or non-JSON body is fine */ }
  if (!res.ok) {
    const error = new Error(data?.detail ?? `${res.status}`);
    error.status = res.status;
    throw error;
  }
  return data;
}

export const apiBase = () => API;

/**
 * Makes sure somebody is signed in before the viewer draws anything, and sends
 * them to the sign-in page if not.
 *
 * Returns false when it has started a navigation, so the caller stops rather
 * than carrying on against a page that is about to be replaced.
 *
 * If the service is unreachable this still sends them to the sign-in page,
 * which is the one page that can explain the situation. Failing open — showing
 * the whole delivery package because the thing that checks permission is down
 * — would be the wrong way round.
 */
export async function requireSignIn() {
  let state = null;
  try {
    state = await authState();
  } catch {
    location.replace(`/login.html?next=${encodeURIComponent(location.pathname + location.hash)}`);
    return false;
  }
  if (state.signedIn) {
    session = { signedIn: true, account: state.account, reachable: true };
    announce();
    return true;
  }
  location.replace(`/login.html?next=${encodeURIComponent(location.pathname + location.hash)}`);
  return false;
}

/** What the sign-in page needs before it can draw: is anyone signed in, and
 *  does an account exist at all. Throws if the service is not answering, which
 *  is a different thing from nobody being signed in. */
export const authState = () => call('/api/auth/state');

export const bootstrapAccount = (email, name, password) =>
  call('/api/auth/bootstrap', { method: 'POST', body: { email, name, password } });

export const listAccounts = () => call('/api/accounts');
export const setAccountActive = (id, active) =>
  call(`/api/accounts/${id}/active?active=${active ? 'true' : 'false'}`, { method: 'POST' });
export const setAccountRole = (id, role) =>
  call(`/api/accounts/${id}/role?role=${encodeURIComponent(role)}`, { method: 'POST' });
export const changePassword = (current, replacement) =>
  call('/api/auth/password', { method: 'POST', body: { current, replacement } });

export async function refreshSession() {
  try {
    const data = await call('/api/auth/me');
    session = { ...data, reachable: true };
  } catch {
    // The service being down is not an error the reader caused, and not a
    // reason to stop them reading.
    session = { signedIn: false, account: null, reachable: false };
  }
  announce();
  return session;
}

export async function signIn(email, password) {
  await call('/api/auth/login', { method: 'POST', body: { email, password } });
  return refreshSession();
}

export async function signOut() {
  try { await call('/api/auth/logout', { method: 'POST' }); } catch { /* going anyway */ }
  return refreshSession();
}

/**
 * End every session on this account, on every device, this browser included.
 *
 * Not a stronger sign-out but a different one. `signOut` clears the session in
 * front of you, which is what leaving a desk needs. This is for the sessions
 * you cannot reach — the laptop that was left somewhere, the browser on a
 * machine you borrowed — and it costs whoever presses it nothing but signing
 * in again. Nothing else moves: the account stays enabled and every verdict
 * keeps its author, which is what makes it the thing to reach for rather than
 * disabling the account.
 *
 * Unlike `signOut` this does not go anyway when the call fails. Signing out
 * locally regardless would leave somebody believing their other devices were
 * cleared when nothing had been revoked at all, and that is the one thing this
 * control must never say wrongly. The caller shows the error instead.
 */
export async function logoutAll() {
  const result = await call('/api/auth/logout-all', { method: 'POST' });
  await refreshSession();
  return result;
}

/** The same done to somebody else. Admin only, and deliberately not the same
 *  as `setAccountActive(id, false)`: the account stays enabled, so they can
 *  sign back in, and their verdicts are untouched. Answers with how many
 *  sessions it dropped, which is the only way to tell "they had none open"
 *  from "it did nothing". */
export const logoutAccount = (id) =>
  call(`/api/accounts/${id}/logout-all`, { method: 'POST' });

export const createInvite = (email, role, days) =>
  call('/api/invites', { method: 'POST', body: { email, role, days } });
export const listInvites = () => call('/api/invites');
export const revokeInvite = (id) => call(`/api/invites/${id}`, { method: 'DELETE' });

export const checkInvite = (token) => call(`/api/invites/check/${encodeURIComponent(token)}`);
export const redeemInvite = (token, name, password) =>
  call('/api/auth/redeem', { method: 'POST', body: { token, name, password } });

export const verdictHistory = (kind, id) =>
  call(`/api/validation/${kind}/${encodeURIComponent(id)}`);
// The layer the reviewer is standing in. Sent with every verdict so the review
// can be read per layer — how much of the frontend is signed off against how
// much of the backend — rather than inferred from the kind afterwards.
export const recordVerdict = (kind, id, verdict, note, layer, tag) =>
  call('/api/validation', {
    method: 'POST',
    body: {
      target_kind: kind, target_id: id, verdict, note,
      layer: layer ?? '', tag: tag ?? '',
    },
  });

/** Mark a verdict complete, or put it back. Anybody who can record one can
 *  close one — the person who fixes a thing is rarely the one who found it. */
export const markVerdictDone = (id, done = true, response = '') =>
  call(`/api/verdicts/${id}/done`, { method: 'POST', body: { done, response } });

/** Reject a completion, with a reason. Admin only, and the note is required —
 *  it is the only thing that tells whoever did the work what to do next. */
export const sendBackVerdict = (id, note) =>
  call(`/api/verdicts/${id}/send-back`, { method: 'POST', body: { note } });

/** Whether a row counts as finished right now.
 *
 *  Both stamps are kept, so this is a comparison rather than a flag: marked
 *  done, sent back, marked done again. Exported because the reviews page and
 *  the verdict block have to agree — two readings of the same two dates would
 *  differ exactly once and nobody would know which was right. */
export function isSettled(v) {
  if (!v?.done_at) return false;
  if (!v.sent_back_at) return true;
  return new Date(v.done_at) > new Date(v.sent_back_at);
}

// ── naming somebody in a note ────────────────────────────

export const mentionable = () => call('/api/mentionable');
export const myMentions = () => call('/api/mentions');
export const markMentionsSeen = () => call('/api/mentions/seen', { method: 'POST' });

/** The roster, fetched once per page rather than per verdict block. There are
 *  a few dozen accounts and 374 screens, and a block per screen each asking
 *  for the same list is the sort of thing that only shows up in production. */
let roster = null;
async function people() {
  if (!roster) roster = mentionable().then((r) => r.people ?? []).catch(() => []);
  return roster;
}

/**
 * Turn a textarea into one that can name somebody.
 *
 * Typing `@` opens a list; the arrows move through it, Enter or Tab picks, Esc
 * closes. What gets inserted is the handle — the local part of the address —
 * because that is what the server matches on, and it is unique by construction
 * where a display name is not. Two people called Chris is normal, and a
 * notification that reaches the wrong Chris is worse than one that does not go.
 */
export function attachMentions(textarea, host) {
  const menu = el('div', 'mention-menu');
  menu.hidden = true;
  host.append(menu);

  let matches = [];
  let active = 0;
  let at = -1;                       // where the @ that opened this sits

  const close = () => {
    menu.hidden = true;
    matches = [];
    at = -1;
  };

  const draw = () => {
    menu.innerHTML = '';
    if (!matches.length) return close();
    matches.forEach((person, i) => {
      const row = el('button', `mention-option${i === active ? ' active' : ''}`);
      row.type = 'button';
      row.append(el('span', 'mention-handle', `@${person.handle}`));
      row.append(el('span', 'mention-name', person.name || person.email));
      if (person.role === 'client') row.append(el('span', 'mention-role', 'client'));
      // mousedown, not click: click lands after the textarea has already lost
      // focus, and the caret position we are about to write into is gone by then.
      row.onmousedown = (e) => { e.preventDefault(); pick(i); };
      menu.append(row);
    });
    menu.hidden = false;
  };

  const pick = (i) => {
    const person = matches[i];
    if (!person) return;
    const before = textarea.value.slice(0, at);
    const after = textarea.value.slice(textarea.selectionStart);
    const inserted = `@${person.handle} `;
    textarea.value = before + inserted + after;
    const caret = before.length + inserted.length;
    textarea.setSelectionRange(caret, caret);
    close();
    textarea.focus();
  };

  textarea.addEventListener('input', async () => {
    const upto = textarea.value.slice(0, textarea.selectionStart);
    // The @ must start a word, or every address typed into a note opens a menu.
    const open = /(?:^|\s)@([A-Za-z0-9._-]*)$/.exec(upto);
    if (!open) return close();
    at = textarea.selectionStart - open[1].length - 1;
    const needle = open[1].toLowerCase();
    const all = await people();
    matches = all
      .filter((p) => p.handle.includes(needle)
        || (p.name ?? '').toLowerCase().includes(needle))
      .slice(0, 6);
    active = 0;
    draw();
  });

  textarea.addEventListener('keydown', (e) => {
    if (menu.hidden) return;
    if (e.key === 'ArrowDown') { active = (active + 1) % matches.length; draw(); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { active = (active - 1 + matches.length) % matches.length; draw(); e.preventDefault(); }
    else if (e.key === 'Enter' || e.key === 'Tab') { pick(active); e.preventDefault(); }
    else if (e.key === 'Escape') { close(); e.preventDefault(); }
  });

  textarea.addEventListener('blur', () => setTimeout(close, 120));
}

/** A note with the handles in it turned into something that reads as a name.
 *  Text nodes throughout — a note is somebody's prose and never markup. */
export function renderNote(text) {
  const box = el('span', 'note-text');
  const parts = String(text ?? '').split(/(@[A-Za-z0-9._%+-]+)/g);
  for (const part of parts) {
    if (/^@/.test(part)) box.append(el('span', 'note-mention', part));
    else box.append(document.createTextNode(part));
  }
  return box;
}

/** Discard a verdict you recorded yourself. The server refuses anybody else's,
 *  admin included — see the endpoint for why. */
export const discardVerdict = (id) =>
  call(`/api/verdicts/${id}`, { method: 'DELETE' });

/** Which side of the house a kind lands on before anybody says otherwise.
 *  Mirrors TAG_OF in db.py; the server defaults the same way if this is wrong,
 *  so the two disagreeing costs a wrong pre-selection and never a wrong row. */
export const TAGS = [['frontend', 'Frontend'], ['backend', 'Backend']];
const TAG_OF = {
  screen: 'frontend', board: 'frontend',
  operation: 'backend', table: 'backend', platform: 'frontend',
};
// audience: 'internal' (the team, and the default every existing caller means),
// 'client', or 'all'.
export const validationSummary = (kind, audience = 'internal') => {
  const q = new URLSearchParams();
  if (kind) q.set('target_kind', kind);
  if (audience) q.set('audience', audience);
  return call(`/api/validation${q.toString() ? `?${q}` : ''}`);
};

/** Every verdict ever recorded, plus the roster. The summary throws away the
 *  disagreement, the revisions and the pace; this keeps them. */
export const allVerdicts = () => call('/api/verdicts');

// ── the block that goes in a view ────────────────────────────────────

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text instanceof Node) node.append(text);
  else if (text != null) node.textContent = text;
  return node;
};

const WHEN = (iso) => {
  const then = new Date(iso);
  if (Number.isNaN(+then)) return iso;
  return then.toLocaleString(undefined,
    { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
};

/**
 * Discard your own verdict, from wherever it is being shown.
 *
 * Matched on the address rather than an id because that is what the payload
 * carries, and one account is one address by construction — `email_folded` is
 * unique, so Asha@ and asha@ cannot be two people.
 *
 * Two presses. Everything else here is reversible: a verdict is answered by a
 * later verdict, a closed item reopens. This is the only control that removes
 * something, so it asks, and stops asking after four seconds rather than
 * sitting armed for a stray click later.
 */
function discardControl(item, after) {
  const mine = session.signedIn
    && session.account?.email?.toLowerCase() === (item.by_email ?? '').toLowerCase();
  if (!mine) return el('span');

  let armed = null;
  const button = el('button', 'verdict-discard', 'Discard this');
  button.type = 'button';
  const disarm = () => {
    clearTimeout(armed);
    armed = null;
    button.textContent = 'Discard this';
    button.classList.remove('armed');
  };
  button.onclick = async () => {
    if (!armed) {
      button.textContent = 'Discard — sure?';
      button.classList.add('armed');
      armed = setTimeout(disarm, 4000);
      return;
    }
    clearTimeout(armed);
    button.disabled = true;
    try {
      await discardVerdict(item.id);
      after();
    } catch (error) {
      button.disabled = false;
      disarm();
      button.textContent = error.message;
    }
  };
  return button;
}

/**
 * A verdict control for one artefact. Renders immediately with what it knows
 * and fills in the history when it arrives, so a slow or absent service never
 * holds up the view it sits in.
 *
 * @param {'operation'|'table'|'screen'|'board'} kind
 * @param {string} id       the artefact, e.g. "orders.sales_order"
 * @param {string} label    what to call it in the heading
 */
export function verdictBlock(kind, id, label = id, { layer = '' } = {}) {
  const box = el('div', 'verdict-box');
  box.dataset.kind = kind;
  box.dataset.target = id;

  const head = el('div', 'journey-section-label', `validation · ${label}`);
  const body = el('div', 'verdict-body');

  // Two regions, refreshed by different things, because they answer to
  // different events. The status is rebuilt whenever the history is re-read —
  // which happens about a second after the block first appears, exactly when
  // somebody has started typing. Rebuilding the form on that schedule would
  // pull the textarea out from under them mid-sentence and drop every
  // keystroke after it. The form is built once, and only when who is signed in
  // actually changes.
  const statusBox = el('div', 'verdict-status');
  const formBox = el('div', 'verdict-actions');
  body.append(statusBox, formBox);
  box.append(head, body);

  const drawStatus = (state) => {
    statusBox.innerHTML = '';

    if (!session.reachable) {
      statusBox.append(el('p', 'pane-note',
        'The validation service is not running, so nothing can be recorded or read. ' +
        'Start it with: python -m uvicorn api.main:app --port 8787'));
      return;
    }

    // what it stands at now — the team's, and the client's beside it
    const current = state?.current ?? null;
    const fromClient = state?.client_current ?? null;
    const status = el('div', 'verdict-current');
    if (current) {
      status.append(el('span', `verdict-chip ${current.verdict}`, verdictLabel(current.verdict)));
      if (current.tag) status.append(el('span', `verdict-tag-chip ${current.tag}`, current.tag));
      status.append(el('span', 'verdict-by',
        `${current.by || current.by_email} · ${WHEN(current.at)}`));
      // Shown next to the verdict rather than instead of it: "needs work, and
      // it has been dealt with" is two facts, and dropping either one loses
      // whether anybody ever went back to look.
      if (current.done_at) {
        status.append(el('span', 'verdict-done-chip',
          `Done${current.done_by_name ? ` · ${current.done_by_name}` : ''} · ${WHEN(current.done_at)}`));
      }
      if (current.note) status.append(el('p', 'verdict-note', renderNote(current.note)));
      status.append(discardControl(current, load));
    } else {
      status.append(el('span', 'verdict-chip none', 'Not reviewed'));
      status.append(el('span', 'verdict-by',
        fromClient ? 'Nobody on the team has recorded a verdict on this yet.'
          : 'Nobody has recorded a verdict on this yet.'));
    }
    statusBox.append(status);

    // Drawn only once a client has actually said something. An empty "client:
    // not reviewed" on every artefact in the package would be a second row of
    // nothing on 374 screens, and would read as an outstanding step rather
    // than an absent one.
    if (fromClient) {
      const theirs = el('div', 'verdict-current verdict-client-track');
      theirs.append(el('span', 'verdict-track-label', 'Client'));
      theirs.append(el('span', `verdict-chip ${fromClient.verdict}`,
        verdictLabel(fromClient.verdict)));
      theirs.append(el('span', 'verdict-by',
        `${fromClient.by || fromClient.by_email} · ${WHEN(fromClient.at)}`));
      if (fromClient.note) theirs.append(el('p', 'verdict-note', renderNote(fromClient.note)));
      theirs.append(discardControl(fromClient, load));
      statusBox.append(theirs);
    }

    // How it got there — only worth showing once there is a "there".
    //
    // By id rather than by position. Slicing the first row off assumed the
    // newest row was the one drawn above it, which stopped being true the
    // moment a second audience could write: a client verdict recorded last
    // would be sliced away as "already shown" while the team's current one
    // appeared twice.
    const standing = new Set([current?.id, fromClient?.id].filter((x) => x != null));
    const past = (state?.history ?? []).filter((item) => !standing.has(item.id));
    if (past.length) {
      const list = el('div', 'verdict-history');
      list.append(el('div', 'verdict-history-head', `${past.length} earlier`));
      for (const item of past) {
        const row = el('div', 'verdict-history-row');
        row.append(el('span', `verdict-dot ${item.verdict}`));
        row.append(el('span', 'verdict-history-what', verdictLabel(item.verdict)));
        row.append(el('span', 'verdict-history-who',
          `${item.by || item.by_email}${item.audience === 'client' ? ' · client' : ''}`));
        row.append(el('span', 'verdict-history-when', WHEN(item.at)));
        if (item.note) row.append(el('span', 'verdict-history-note', renderNote(item.note)));
        list.append(row);
      }
      statusBox.append(list);
    }
  };

  /** Built only when who is signed in changes — never by a history refresh. */
  let builtFor = Symbol('nothing yet');
  const drawForm = () => {
    const who = session.reachable ? (session.account?.email ?? null) : false;
    if (who === builtFor) return;
    builtFor = who;
    formBox.innerHTML = '';
    if (who === false) return;

    if (!session.signedIn) {
      const prompt = el('div', 'verdict-signin');
      prompt.append(el('span', null, 'Sign in to record a verdict.'));
      const button = el('button', 'chip', 'Sign in');
      button.type = 'button';
      button.onclick = () => document.dispatchEvent(new CustomEvent('ticvai:signin'));
      prompt.append(button);
      formBox.append(prompt);
      return;
    }

    // A client records a verdict like anybody else. What differs is where it
    // lands: the server files it under its own audience from the role on the
    // session, so it stands beside the team's review rather than on top of it.
    // Saying so here is worth a line — somebody signing off on their own
    // project should know their approval is being kept as theirs.
    const asClient = session.account?.role === 'client';

    const form = el('div', 'verdict-form');
    if (asClient) {
      form.append(el('p', 'pane-note verdict-as-client',
        'Recorded as the client review, kept separately from the team’s.'));
    }

    // Which side has to act on it. Pre-selected from the kind and changeable,
    // because the default is right most of the time and wrong exactly when it
    // matters: a screen that draws the wrong total is found in the frontend
    // and fixed in the backend, and only the person looking at it knows which.
    let tag = TAG_OF[kind] ?? 'backend';
    const tagRow = el('div', 'verdict-tag-row');
    // Which side has to act is the team's triage, not the client's — they are
    // not the ones holding either queue. The server defaults it from the kind.
    if (asClient) tagRow.hidden = true;
    tagRow.append(el('span', 'verdict-tag-label', 'Lands on'));
    const tagButtons = el('div', 'verdict-tag-buttons');
    const paintTags = () => {
      for (const b of tagButtons.querySelectorAll('button')) {
        b.classList.toggle('chosen', b.dataset.tag === tag);
        b.setAttribute('aria-pressed', String(b.dataset.tag === tag));
      }
    };
    for (const [value, text] of TAGS) {
      const button = el('button', `chip verdict-tag ${value}`, text);
      button.type = 'button';
      button.dataset.tag = value;
      // No clearing this one. Every verdict lands on somebody, and an untagged
      // row is one that drops out of both filters and gets worked on by nobody.
      button.onclick = () => { tag = value; paintTags(); };
      tagButtons.append(button);
    }
    tagRow.append(tagButtons);
    paintTags();
    form.append(tagRow);

    const note = document.createElement('textarea');
    note.className = 'verdict-note-input';
    note.rows = 2;
    note.placeholder =
      'Why? A verdict with no reason gets rediscovered the hard way. Type @ to name somebody.';
    const noteWrap = el('div', 'verdict-note-wrap');
    noteWrap.append(note);
    attachMentions(note, noteWrap);
    form.append(noteWrap);

    // Pick, then submit — rather than one click recording a verdict outright.
    //
    // A single click used to write the row, which put "Rejected" one stray tap
    // away on a page a reviewer is scrolling through, and gave no moment in
    // which to write the reason. The verdicts are append-only, so a mistaken
    // one cannot be taken back — only argued with by a later row. A deliberate
    // second action is cheap next to that.
    let chosen = null;
    const buttons = el('div', 'verdict-buttons');
    const message = el('span', 'verdict-message');

    const submit = el('button', 'chip verdict-submit', 'Submit');
    submit.type = 'button';
    submit.disabled = true;

    const setChosen = (value) => {
      chosen = value;
      for (const b of buttons.querySelectorAll('button')) {
        b.classList.toggle('chosen', b.dataset.verdict === value);
        b.setAttribute('aria-pressed', String(b.dataset.verdict === value));
      }
      submit.disabled = value === null;
      // The label stays "Submit". The chosen chip is already lit and named, so
      // repeating it on the button only made the button change width as you
      // picked, which is movement that says nothing.
      submit.classList.toggle('rejected', value === 'rejected');
      message.textContent = '';
    };

    for (const [value, text] of VERDICTS) {
      const button = el('button', `chip verdict-set ${value}`, text);
      button.type = 'button';
      button.dataset.verdict = value;
      button.setAttribute('aria-pressed', 'false');
      // clicking the chosen one again clears it, so a misclick costs nothing
      button.onclick = () => setChosen(chosen === value ? null : value);
      buttons.append(button);
    }

    submit.onclick = async () => {
      if (!chosen) return;
      const all = [...buttons.querySelectorAll('button'), submit];
      for (const b of all) b.disabled = true;
      message.textContent = 'Recording…';
      try {
        await recordVerdict(kind, id, chosen, note.value, layer, tag);
        note.value = '';
        setChosen(null);
        load();
      } catch (error) {
        message.textContent = error.message;
        for (const b of all) b.disabled = false;
        submit.disabled = !chosen;
      }
    };

    const actions = el('div', 'verdict-actions-row');
    actions.append(buttons, submit);
    form.append(actions, message);
    formBox.append(form);
  };

  const load = async () => {
    drawForm();
    if (!session.reachable) return drawStatus(null);
    try {
      drawStatus(await verdictHistory(kind, id));
    } catch {
      drawStatus(null);
    }
  };

  drawStatus(null);
  drawForm();
  load();

  // A sign-in or sign-out changes what this block offers. Panes are rebuilt
  // constantly, so a block that never unsubscribes would pile up: every one
  // ever rendered would hold its detached DOM alive and fire another request
  // on each sign-in. Mutation events would be the obvious hook and are gone
  // from the browser, so the check happens where it is certain to run — on the
  // notification itself, which is the only thing that would do any work.
  const stop = onAuthChange(() => {
    if (!box.isConnected) return stop();
    load();
  });

  return box;
}

export function verdictLabel(value) {
  return VERDICTS.find(([v]) => v === value)?.[1] ?? value;
}
