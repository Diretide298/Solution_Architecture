/**
 * What can be done to one verdict row on the Reviews page, and the file the
 * log exports as.
 *
 * Four actions, and only one of them destroys anything:
 *
 *   Respond     closes an ask for work by saying *how* it was answered (built,
 *               wired, answered, accepted, approved with no action). Closing
 *               is answering, so the control is the five answers rather than
 *               one button called Done.
 *   Reopen      takes the answer back. Reversible by answering again.
 *   Send back   an admin rejects an answer, and has to say why: the reason is
 *               the only thing that tells whoever did the work what to do next.
 *   Discard     removes a verdict you recorded yourself, for good. The one
 *               irreversible control, so it asks a second time (confirmStep).
 *
 * The row is never removed when it is answered. A worklist that deletes what
 * was finished cannot answer "was this ever dealt with", which is the question
 * asked three weeks later.
 */
import * as auth from '/validation.js';
import { el, confirmStep } from '/sheet.js';
import { kindLabel } from '/reviews-coverage.js';

export const RESPONSE_LABEL = Object.fromEntries(auth.RESPONSES);
export const VERDICT_LABEL = Object.fromEntries(auth.VERDICTS);
export const TAG_LABEL = Object.fromEntries(auth.TAGS);
export const AUDIENCE_LABEL = { internal: 'Team', client: 'Client' };
// Where the reviewer was standing. Recorded on the verdict rather than derived
// from its kind, so "how much of the frontend is signed off" can be asked
// separately from "how much of the backend is".
export const LAYER_LABEL = {
  frontend: 'Frontend', contracts: 'Contracts', domain: 'Domain',
  backend: 'Backend', modules: 'Modules', decisions: 'Decisions',
};

const when = (iso) => {
  const d = new Date(iso);
  return Number.isNaN(+d) ? '' : d.toLocaleString('en-GB',
    { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
};

/** Where a row stands, as one word: open, sent back, answered, withdrawn
 *  (its author has since given a later verdict on the same artefact) or
 *  nothing to do. `withdrawn` is the set of ids the page worked out, because
 *  only the whole store can say whether a later verdict exists. */
export function statusOf(v, withdrawn) {
  if (auth.isSettled(v)) return 'answered';
  if (!auth.asksForWork(v.verdict)) return 'none';
  if (withdrawn?.has(v.id)) return 'withdrawn';
  return v.sent_back_at ? 'sent-back' : 'open';
}

/**
 * The status cell: what has happened to this row, and what you may do next.
 *
 * @param {object} v       the verdict row (mutated in place on success)
 * @param {object} o
 * @param {object} o.me                    the signed-in account
 * @param {(what:string) => void} o.done   called after any change, to redraw
 * @param {(text:string) => void} o.fail   says what went wrong
 * @param {boolean} [o.compact]            the worklist: Respond only
 * @param {Set<number>} [o.withdrawn]      asks their author has replaced
 */
export function statusCell(v, { me, done, fail, compact = false, withdrawn }) {
  const cell = el('div', 'rv-status');
  const stamp = el('div', 'rv-stamp');
  const status = statusOf(v, withdrawn);
  if (status === 'answered') {
    // The answer rather than the word "Done": five different answers showing
    // as one word is what the tracker had already outgrown.
    stamp.append(el('span', 'rv-stamp-what', RESPONSE_LABEL[v.done_response] ?? 'Answered'));
    stamp.append(el('span', 'sh-quiet', `${v.done_by_name ? `${v.done_by_name}, ` : ''}${when(v.done_at)}`));
  } else if (status === 'sent-back') {
    // Open again, but not the same as never having been finished: somebody did
    // the work and it was not accepted, and the reason is shown rather than
    // hidden behind a hover because it is what to do next.
    stamp.append(el('span', 'rv-stamp-what', 'Sent back'));
    stamp.append(el('span', 'sh-quiet', `${v.sent_back_by_name ? `${v.sent_back_by_name}, ` : ''}${when(v.sent_back_at)}`));
    if (v.sent_back_note) stamp.append(el('span', 'rv-stamp-note', v.sent_back_note));
  } else if (status === 'withdrawn') {
    stamp.append(el('span', 'sh-quiet', 'Replaced by their later verdict'));
  } else if (status === 'open') {
    stamp.append(el('span', 'rv-stamp-what', 'Open'));
  } else {
    stamp.append(el('span', 'sh-quiet', 'Nothing to answer'));
  }
  if (!compact) cell.append(stamp);

  const actions = el('div', 'rv-actions');
  cell.append(actions);
  // A client reviews; the team answers. The server refuses a client's close,
  // and a button that exists to be told no is worse than no button.
  const mayWrite = me && !auth.isClient(me);

  const run = async (button, what, call) => {
    button.disabled = true;
    try {
      await call();
      done(what);
    } catch (error) {
      button.disabled = false;
      fail(`${what} did not go through: ${error.message}. Nothing was changed; try again, and reload the page if it keeps failing.`);
    }
  };

  if (mayWrite && (status === 'open' || status === 'sent-back')) {
    const respond = el('button', 'chip rv-respond', 'Respond');
    respond.type = 'button';
    respond.setAttribute('aria-expanded', 'false');
    respond.onclick = () => {
      // Folded behind a press because five answers on every row of a long
      // table is a wall, and only one row is answered at a time.
      respond.hidden = true;
      const picker = el('div', 'rv-picker');
      picker.setAttribute('role', 'group');
      picker.setAttribute('aria-label', `How was the ask on ${v.target_id} answered`);
      for (const [value, label] of auth.RESPONSES) {
        const pick = el('button', 'chip', label);
        pick.type = 'button';
        pick.onclick = () => {
          for (const b of picker.querySelectorAll('button')) b.disabled = true;
          run(pick, `Answering it "${label}"`, async () => {
            const result = await auth.markVerdictDone(v.id, true, value);
            v.done_at = result.done_at;
            v.done_by_name = result.done_by_name;
            v.done_response = result.done_response ?? value;
          }).finally(() => { for (const b of picker.querySelectorAll('button')) b.disabled = false; });
        };
        picker.append(pick);
      }
      const cancel = el('button', 'chip rv-cancel', 'Cancel');
      cancel.type = 'button';
      cancel.onclick = () => { picker.remove(); respond.hidden = false; respond.focus(); };
      picker.append(cancel);
      actions.append(picker);
      picker.querySelector('button')?.focus();
    };
    actions.append(respond);
  }
  if (compact) return cell;

  if (mayWrite && status === 'answered') {
    const reopen = el('button', 'chip', 'Reopen');
    reopen.type = 'button';
    reopen.title = 'Take the answer back: the ask is open again.';
    reopen.onclick = () => run(reopen, 'Reopening it', async () => {
      const result = await auth.markVerdictDone(v.id, false, '');
      v.done_at = result.done_at;
      v.done_by_name = result.done_by_name;
      v.done_response = result.done_response ?? '';
    });
    actions.append(reopen);
  }

  if (auth.isAdmin(me) && status === 'answered') actions.append(sendBack(v, { done, fail }));

  // Your own rows only: the server refuses anybody else's, admin included.
  if (me && v.account_id === me.id) {
    const discard = el('button', 'chip rv-discard', 'Discard');
    discard.type = 'button';
    discard.title = 'Remove this verdict. Only you can, and only your own.';
    discard.onclick = async () => {
      const sure = await confirmStep(discard, {
        say: `Remove your "${VERDICT_LABEL[v.verdict] ?? v.verdict}" on ${v.target_id} for good? It cannot be brought back.`,
        action: 'Discard it',
      });
      if (!sure) return;
      run(discard, 'Discarding it', async () => {
        await auth.discardVerdict(v.id);
        v.discarded = true;
      });
    };
    actions.append(discard);
  }
  return cell;
}

/**
 * Reject an answer, with a reason. Admin only.
 *
 * The note is not optional and the control is built around that: pressing
 * "Send back" opens a field, and the second "Send back" stays disabled until
 * something has been typed. There is no path that sends work back without
 * saying why.
 */
function sendBack(v, { done, fail }) {
  const wrap = el('div', 'rv-sendback');
  const open = el('button', 'chip', 'Send back');
  open.type = 'button';
  open.title = 'Reject the answer as not finished, and say why.';
  open.setAttribute('aria-expanded', 'false');
  wrap.append(open);
  open.onclick = () => {
    open.hidden = true;
    const form = el('div', 'rv-sendback-form');
    const label = el('label', 'sh-field');
    const note = document.createElement('textarea');
    note.className = 'sh-input rv-sendback-note';
    note.rows = 2;
    label.append(el('span', '', 'What is still wrong? This is what they will read.'), note);
    const send = el('button', 'chip', 'Send back');
    send.type = 'button';
    send.disabled = true;
    const cancel = el('button', 'chip', 'Cancel');
    cancel.type = 'button';
    note.oninput = () => { send.disabled = !note.value.trim(); };
    cancel.onclick = () => { form.remove(); open.hidden = false; open.focus(); };
    send.onclick = async () => {
      send.disabled = true;
      try {
        const result = await auth.sendBackVerdict(v.id, note.value.trim());
        v.sent_back_at = result.sent_back_at;
        v.sent_back_by_name = result.sent_back_by_name;
        v.sent_back_note = result.sent_back_note;
        done('Sending it back');
      } catch (error) {
        send.disabled = false;
        fail(`Sending it back did not go through: ${error.message}. Nothing was changed; try again.`);
      }
    };
    form.append(label, send, cancel);
    wrap.append(form);
    note.focus();
  };
  return wrap;
}

/**
 * The rows shown, as a file. Built in the page rather than served, so what you
 * get is exactly what is on screen.
 *
 * Every row is a verdict at a moment, not a current state, which is what makes
 * the file worth having. Oldest first, because a history read top to bottom
 * should run forwards. `id` first, matching the service's export column for
 * column: it is what the admin panel's bulk close matches a row back to.
 */
export function exportCsv(rows, { narrowed }) {
  const esc = (s) => `"${String(s ?? '').replace(/"/g, '""')}"`;
  const day = (iso) => {
    const d = new Date(iso);
    return Number.isNaN(+d) ? '' : d.toISOString().slice(0, 10);
  };
  const ordered = [...rows].sort((a, b) => new Date(a.at) - new Date(b.at));
  const body = [
    ['id',
     'when', 'date', 'review', 'layer', 'lands on', 'kind', 'artefact', 'verdict',
     'reviewer', 'email', 'status', 'our verdict', 'done on', 'done by',
     'sent back because', 'note'].join(','),
    ...ordered.map((v) => [
      v.id,
      v.at, day(v.at), v.audience === 'client' ? 'Client' : 'The team',
      LAYER_LABEL[v.layer] ?? v.layer ?? '', TAG_LABEL[v.tag] ?? v.tag ?? '',
      kindLabel(v.target_kind), v.target_id,
      VERDICT_LABEL[v.verdict] ?? v.verdict, v.by, v.by_email,
      auth.isSettled(v) ? 'Done' : v.sent_back_at ? 'Sent back' : 'Open',
      RESPONSE_LABEL[v.done_response] ?? v.done_response ?? '',
      v.done_at ? day(v.done_at) : '', v.done_by_name ?? '',
      v.sent_back_note ?? '',
      v.note,
    ].map(esc).join(',')),
  ].join('\r\n');

  // A BOM, because Excel on Windows reads a UTF-8 CSV as the system codepage
  // without one, and these notes are full of em dashes and curly quotes.
  const url = URL.createObjectURL(new Blob(['﻿' + body], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  // A filtered file called ticvai-reviews-2026-10-14.csv reads as the whole
  // review a week later, and nothing inside it says otherwise.
  const today = new Date().toISOString().slice(0, 10);
  a.download = `ticvai-reviews-${today}${narrowed ? '-filtered' : ''}.csv`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
