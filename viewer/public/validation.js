/**
 * Who is signed in, and what they have decided about an artefact.
 *
 * The viewer itself stays open: anyone on the machine can read the delivery
 * package without an account, because it is a reference tool and gating it
 * would only make it less used. An account is needed to *write* a verdict,
 * because the whole value of a verdict is knowing who gave it.
 *
 * Everything here talks to the FastAPI service, which is a separate process on
 * a separate port. If it is not running the viewer carries on reading, and the
 * verdict blocks say so rather than breaking the page.
 */

// The service is on its own port, so calls are cross-origin and the session
// cookie only rides along with credentials: 'include'.
const API = localStorage.getItem('ticvai-api') ?? 'http://localhost:8787';

export const VERDICTS = [
  ['approved', 'Approved'],
  ['needs-work', 'Needs work'],
  ['rejected', 'Rejected'],
];

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

export const createInvite = (email, role, days) =>
  call('/api/invites', { method: 'POST', body: { email, role, days } });
export const listInvites = () => call('/api/invites');
export const revokeInvite = (id) => call(`/api/invites/${id}`, { method: 'DELETE' });

export const checkInvite = (token) => call(`/api/invites/check/${encodeURIComponent(token)}`);
export const redeemInvite = (token, name, password) =>
  call('/api/auth/redeem', { method: 'POST', body: { token, name, password } });

export const verdictHistory = (kind, id) =>
  call(`/api/validation/${kind}/${encodeURIComponent(id)}`);
export const recordVerdict = (kind, id, verdict, note) =>
  call('/api/validation', {
    method: 'POST',
    body: { target_kind: kind, target_id: id, verdict, note },
  });
export const validationSummary = (kind) =>
  call(`/api/validation${kind ? `?target_kind=${encodeURIComponent(kind)}` : ''}`);

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
 * A verdict control for one artefact. Renders immediately with what it knows
 * and fills in the history when it arrives, so a slow or absent service never
 * holds up the view it sits in.
 *
 * @param {'operation'|'table'|'screen'|'board'} kind
 * @param {string} id       the artefact, e.g. "orders.sales_order"
 * @param {string} label    what to call it in the heading
 */
export function verdictBlock(kind, id, label = id) {
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

    // what it stands at now
    const current = state?.current ?? null;
    const status = el('div', 'verdict-current');
    if (current) {
      status.append(el('span', `verdict-chip ${current.verdict}`, verdictLabel(current.verdict)));
      status.append(el('span', 'verdict-by',
        `${current.by || current.by_email} · ${WHEN(current.at)}`));
      if (current.note) status.append(el('p', 'verdict-note', current.note));
    } else {
      status.append(el('span', 'verdict-chip none', 'Not reviewed'));
      status.append(el('span', 'verdict-by', 'Nobody has recorded a verdict on this yet.'));
    }
    statusBox.append(status);

    // how it got there — only worth showing once there is a "there"
    const past = (state?.history ?? []).slice(1);
    if (past.length) {
      const list = el('div', 'verdict-history');
      list.append(el('div', 'verdict-history-head', `${past.length} earlier`));
      for (const item of past) {
        const row = el('div', 'verdict-history-row');
        row.append(el('span', `verdict-dot ${item.verdict}`));
        row.append(el('span', 'verdict-history-what', verdictLabel(item.verdict)));
        row.append(el('span', 'verdict-history-who', `${item.by || item.by_email}`));
        row.append(el('span', 'verdict-history-when', WHEN(item.at)));
        if (item.note) row.append(el('span', 'verdict-history-note', item.note));
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

    const form = el('div', 'verdict-form');
    const note = document.createElement('textarea');
    note.className = 'verdict-note-input';
    note.rows = 2;
    note.placeholder = 'Why? A verdict with no reason gets rediscovered the hard way.';
    form.append(note);

    const buttons = el('div', 'verdict-buttons');
    const message = el('span', 'verdict-message');
    for (const [value, text] of VERDICTS) {
      const button = el('button', `chip verdict-set ${value}`, text);
      button.type = 'button';
      button.onclick = async () => {
        for (const b of buttons.querySelectorAll('button')) b.disabled = true;
        message.textContent = 'Recording…';
        try {
          await recordVerdict(kind, id, value, note.value);
          note.value = '';
          message.textContent = '';
          load();
        } catch (error) {
          message.textContent = error.message;
        } finally {
          for (const b of buttons.querySelectorAll('button')) b.disabled = false;
        }
      };
      buttons.append(button);
    }
    form.append(buttons, message);
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
  // a sign-in or sign-out changes what this block offers
  const stop = onAuthChange(() => load());
  box.addEventListener('DOMNodeRemovedFromDocument', stop);

  return box;
}

export function verdictLabel(value) {
  return VERDICTS.find(([v]) => v === value)?.[1] ?? value;
}
