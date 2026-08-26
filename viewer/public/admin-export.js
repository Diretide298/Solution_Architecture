/**
 * Taking a date range of a register away as a CSV, from the admin panel.
 *
 * The file is built by the service, not here — which is the opposite of the
 * reviews page, and deliberately. That export is a screenful of rows the reader
 * has already filtered, so building it in the page is what makes "exactly what
 * you see" true. This one is a range that nobody has looked at, usually longer
 * than the page ever held, and fetching the whole register into the browser to
 * throw most of it away would be a slower way of getting a worse answer.
 *
 * What the two must agree on is the file itself, and they do: the same columns,
 * the same labels, every field quoted with an inner quote doubled, CRLF between
 * rows and a byte order mark in front, so a comma inside a note lands in the
 * same place whichever button produced it.
 */

import { apiBase } from '/validation.js';

/** What may be taken, in the order the control offers it.
 *
 *  Review activity leads because it is the register the product is for — one
 *  row per thing somebody said at a time, growing with the work. The other two
 *  grow with the payroll, and are here because an admin panel is where somebody
 *  asks who was invited in July. `label` is what the option says; the value is
 *  the dataset name the service knows. */
const SETS = [
  ['verdicts', 'Review activity — every verdict recorded'],
  ['invites', 'Invites — every link made'],
  ['accounts', 'Accounts — everyone who has one'],
];

/** The filename the service decided on. It comes back in Content-Disposition,
 *  which a cross-origin fetch can only read because the service names that
 *  header in expose_headers. The fallback is for the one case where it cannot:
 *  a browser that hid it anyway leaves a file called `download` otherwise, and
 *  a file whose name does not say what range it holds is a file that reads as
 *  the whole register a week later. */
function filenameFrom(disposition, fallback) {
  const match = /filename="([^"]+)"/.exec(disposition ?? '');
  return match ? match[1] : fallback;
}

/**
 * Wires the export panel. Called once, by the admin branch of admin.html,
 * after the page has established the reader is an admin.
 *
 * Nothing here is the access rule — the service refuses this to anyone else
 * whatever the page draws, and it has to, because a hidden control is still a
 * GET away for anybody who opens devtools. Drawing it only for an admin is so
 * that nobody is shown a button that will only tell them no.
 */
export function mountExport() {
  const $ = (id) => document.getElementById(id);
  const what = $('export-what');
  const from = $('export-from');
  const to = $('export-to');
  const go = $('export-go');
  const error = $('export-error');
  const ok = $('export-ok');
  if (!what || !go) return;

  for (const [value, label] of SETS) {
    const option = new Option(label, value);
    what.append(option);
  }

  // Neither end may be in the future, because neither end could hold anything.
  // A `max` on the field is a hint rather than a rule — the service is what
  // actually decides — but it is the cheapest place to stop somebody picking a
  // range that was always going to come back empty.
  const today = new Date().toISOString().slice(0, 10);
  from.max = today;
  to.max = today;

  const say = (node, text) => {
    node.textContent = text;
    node.hidden = false;
  };
  const quiet = () => { error.hidden = true; ok.hidden = true; };

  go.onclick = async () => {
    quiet();

    // Checked here as well as at the service. The service is the one that
    // decides, and it says so in the same words; this is only so that an
    // obviously backwards range is answered before a round trip rather than
    // after one.
    if (from.value && to.value && to.value < from.value) {
      say(error, `The range runs backwards: ${from.value} is after ${to.value}. Swap them.`);
      return;
    }

    const query = new URLSearchParams();
    if (from.value) query.set('from', from.value);
    if (to.value) query.set('to', to.value);
    // Both ends are optional, and an empty one is left out of the query
    // entirely rather than sent blank: `?from=` and no `from` at all mean the
    // same thing to the service, and only one of them reads as a mistake.
    const asked = query.toString();
    const url = `${apiBase()}/api/export/${what.value}${asked ? `?${asked}` : ''}`;

    go.disabled = true;
    try {
      // A fetch, not a link. The service is on another origin, so a plain
      // anchor would be a cross-origin navigation carrying whatever cookie the
      // browser felt like sending — and worse, it has nowhere to put an
      // answer: a refusal would replace this page with a line of JSON, and an
      // empty range would save a file with no word about why it is empty. A
      // credentialed fetch sends the session cookie the same way every other
      // call on this page does, and hands back a body this code can read
      // before deciding what to say.
      const res = await fetch(url, { credentials: 'include' });
      if (!res.ok) {
        let detail = `${res.status}`;
        try { detail = (await res.json()).detail ?? detail; } catch { /* not JSON */ }
        say(error, detail);
        return;
      }

      const rows = Number(res.headers.get('X-Ticvai-Rows') ?? NaN);
      const name = filenameFrom(
        res.headers.get('Content-Disposition'),
        `ticvai-${what.value}-${from.value || 'beginning'}-to-${to.value || today}.csv`,
      );

      const href = URL.createObjectURL(await res.blob());
      const a = document.createElement('a');
      a.href = href;
      a.download = name;
      a.click();
      setTimeout(() => URL.revokeObjectURL(href), 1000);

      // An empty range still downloads, and still says so. The file has its
      // headings and nothing under them, which is the honest answer; saying
      // nothing would leave the reader unable to tell "nobody reviewed anything
      // that week" from "the export is broken", and those are the two things
      // they are actually choosing between.
      say(ok, rows === 0
        ? `${name} — that range is empty. The file has its column headings and nothing under them.`
        : `${name} — ${rows} row${rows === 1 ? '' : 's'}.`);
    } catch {
      say(error, 'Could not reach the accounts service. Nothing was downloaded.');
    } finally {
      go.disabled = false;
    }
  };
}
