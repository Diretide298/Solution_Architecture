/**
 * Closing review items from the spreadsheet they were decided on.
 *
 * The other end of the export panel above it. A range of the register goes out
 * as a CSV, somebody works down the "Our verdict" column in Excel saying how
 * each thing was answered, and this sends the file back to be applied.
 *
 * Two presses, never one, and the first press writes nothing. A bulk close is
 * the one action on this page that cannot be undone by doing it again with the
 * right file: closing an item overwrites who closed it and when, so a file
 * applied by accident does not leave the previous answer behind to be restored.
 * So the first press asks the service what the file *would* do and shows it —
 * including the rows it disagrees with and the rows it cannot use — and only
 * the second one applies it.
 *
 * What links the two is the checksum the preview answered with, sent back with
 * the apply. Not a flag: a flag would confirm the press, and the press is not
 * the thing in doubt. What has to be established is that the file about to be
 * applied is the file whose consequences were read, and picking a different one
 * between the two presses is exactly the mistake worth catching.
 */

import { apiBase } from '/validation.js';

/** Long enough to read, short enough that a four-thousand-row file does not
 *  become four thousand DOM nodes nobody scrolls to. The count above each list
 *  is always the true one; this only caps what is drawn. */
const SHOWN = 150;

/** Wires the panel. Called once, by the admin branch of admin.html, after the
 *  page has established the reader is an admin.
 *
 *  Nothing here is the access rule — the service refuses both routes to anyone
 *  else whatever the page draws, and it has to, because a hidden control is
 *  still a POST away for anybody who opens devtools. */
export function mountDecisions() {
  const $ = (id) => document.getElementById(id);
  const picker = $('decide-file');
  const check = $('decide-check');
  const apply = $('decide-apply');
  const error = $('decide-error');
  const ok = $('decide-ok');
  const plan = $('decide-plan');
  if (!picker || !check) return;

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };
  const say = (node, text) => { node.textContent = text; node.hidden = false; };
  const quiet = () => { error.hidden = true; ok.hidden = true; };

  // The checksum of the file the plan on screen was built from. Held here and
  // nowhere else, and dropped the moment anything could have changed — which is
  // what makes the apply below unable to act on a file nobody previewed.
  let confirm = '';

  const forget = () => {
    confirm = '';
    plan.innerHTML = '';
    plan.hidden = true;
    apply.hidden = true;
  };

  // A new file means the plan on screen is about the old one. Clearing it here
  // rather than letting the service refuse the mismatch is only manners: the
  // service still refuses it, because this line is presentation and the rule
  // has to hold for a caller that never ran it.
  picker.onchange = () => { quiet(); forget(); };

  /** One row of the plan, as a sentence. `#812` is there because it is what
   *  every message from the service names, and a reader who has the file open
   *  beside this wants to find the same row in it. */
  const line = (item, tail) => {
    const row = el('div', 'decide-line');
    row.append(el('span', 'decide-row', `Row ${item.row}`));
    row.append(el('span', 'decide-id', `#${item.id}`));
    row.append(el('span', 'decide-what', `${item.kind} · ${item.artefact}`));
    row.append(el('span', 'decide-tail', tail));
    return row;
  };

  /** A named group of them, with its own count and its own reason for being
   *  shown separately. Empty groups are not drawn: a panel listing four
   *  headings with nothing under three of them buries the one that matters. */
  const group = (title, why, items, tail, tone) => {
    if (!items.length) return;
    const box = el('section', `decide-group ${tone}`);
    box.append(el('h3', 'decide-group-title', `${title} — ${items.length}`));
    box.append(el('p', 'auth-note auth-fine decide-why', why));
    const list = el('div', 'decide-list');
    for (const item of items.slice(0, SHOWN)) list.append(tail(item));
    if (items.length > SHOWN) {
      list.append(el('p', 'auth-note auth-fine',
        `and ${items.length - SHOWN} more, not listed.`));
    }
    box.append(list);
    plan.append(box);
  };

  function draw(result) {
    plan.innerHTML = '';
    plan.hidden = false;

    const head = el('p', 'auth-note decide-summary');
    const format = result.format === 'xlsx'
      ? `Excel workbook${result.tab ? ` · sheet "${result.tab}"` : ''}` : 'CSV';
    head.textContent =
      `${result.file} — ${format}, ${result.rows} row${result.rows === 1 ? '' : 's'}. `
      + `${result.blank} of them have no decision in the "our verdict" column and `
      + 'are left exactly as they are.';
    plan.append(head);

    // The heading is in a different tense before and after, because the same
    // list means two different things either side of the press and a panel
    // still headed "would be closed" over rows that have been is the one place
    // a reader could reasonably think nothing happened.
    group(result.applied ? 'Closed' : 'Would be closed', result.applied
      ? 'Closed, with you recorded as who closed them and when.'
      : 'Not closed yet — nothing has been written. The button below is what '
        + 'writes them.',
      result.close,
      (item) => line(item, `${item.verdict} → ${item.response_label}`
        + (item.was === 'sent back' ? ' · was sent back, this closes it again' : '')),
      'good');

    group('Already closed the same way', 'Left alone. Closing them again would '
      + 'move the date and the name to you and today, and lose who actually did '
      + 'it, in exchange for no change of meaning.',
      result.already,
      (item) => line(item, `already ${item.current_label} on ${item.done_on}`
        + (item.done_by ? ` by ${item.done_by}` : '')),
      'quiet');

    group('Closed, but differently', 'Not touched, and worth a look: the file '
      + 'and the register disagree about how these were answered. Changing one '
      + 'of them is a decision about that item, so it is made on the item — on '
      + 'the reviews page — rather than by a file that happens to name it.',
      result.differs,
      (item) => line(item,
        `file says ${item.response_label}, closed as `
        + `${item.current_label || 'nothing recorded'} on ${item.done_on}`),
      'warn');

    group('Could not be used', 'These rows named something this cannot act on. '
      + 'Everything else in the file still applies.',
      result.problems,
      (item) => {
        const row = el('div', 'decide-line');
        row.append(el('span', 'decide-tail', item.message));
        return row;
      },
      'bad');

    if (!result.applied && result.close.length) {
      apply.hidden = false;
      apply.textContent = `Close ${result.close.length} item`
        + `${result.close.length === 1 ? '' : 's'}`;
    } else {
      apply.hidden = true;
    }
  }

  /** Both presses go the same way: a credentialed cross-origin POST of a
   *  multipart form, exactly as the export beside it does a credentialed GET.
   *  The session cookie is only sent because of `credentials: 'include'`, and
   *  the service names this origin in its CORS list because a browser refuses a
   *  credentialed response that answers "*". */
  async function post(path, extra) {
    const body = new FormData();
    body.append('file', picker.files[0]);
    for (const [key, value] of Object.entries(extra ?? {})) body.append(key, value);
    // No Content-Type header set by hand. fetch writes it, with the multipart
    // boundary it generated — setting it here would send a boundary that
    // nothing in the body matches, and the service would see an empty form.
    const res = await fetch(`${apiBase()}${path}`, {
      method: 'POST', credentials: 'include', body,
    });
    if (!res.ok) {
      let detail = `${res.status}`;
      try {
        const said = (await res.json()).detail;
        // A string is one of this service's own refusals and is written to be
        // read. Anything else is FastAPI's own validation shape, which is a list
        // of objects and lands on screen as [object Object]; the status code is
        // a worse message and a true one.
        if (typeof said === 'string') detail = said;
      } catch { /* not JSON */ }
      throw new Error(detail);
    }
    return res.json();
  }

  check.onclick = async () => {
    quiet();
    forget();
    if (!picker.files.length) {
      say(error, 'Choose the file first.');
      return;
    }
    check.disabled = true;
    try {
      const result = await post('/api/decisions/preview');
      confirm = result.digest;
      draw(result);
      if (!result.close.length) {
        say(ok, 'Nothing in that file would close anything. Everything it names '
          + 'is already closed, disagrees with the register, or could not be used.');
      }
    } catch (failure) {
      say(error, failure.message);
    } finally {
      check.disabled = false;
    }
  };

  apply.onclick = async () => {
    quiet();
    if (!confirm) {
      say(error, 'Check the file again — the plan on screen is not this file.');
      return;
    }
    apply.disabled = true;
    check.disabled = true;
    try {
      const result = await post('/api/decisions/apply', { confirm });
      draw(result);
      say(ok, `Closed ${result.close.length} item`
        + `${result.close.length === 1 ? '' : 's'}, recorded against you at `
        + `${result.closed_at}.`);
      // Applying it once is the whole of it. The plan on screen is now a record
      // of what happened rather than an offer, and pressing again would ask the
      // service to close rows it has just closed — which it would answer by
      // moving every one of them into "already closed the same way", correctly
      // and confusingly.
      confirm = '';
      picker.value = '';
    } catch (failure) {
      say(error, failure.message);
    } finally {
      apply.disabled = false;
      check.disabled = false;
      apply.hidden = true;
    }
  };
}
