/**
 * A key sequence that opens a standalone page.
 *
 * Type the word on any viewer page and a drop opens in a new tab. The drop is
 * served from a path that is a digest of the word, on the public allowlist in
 * `viewer/lib/session.mjs`, so it answers whether or not anybody is signed in —
 * one word, both states.
 *
 * **The word is not in this file, and neither is a hash of it.** `OPEN_WORD`
 * below is a placeholder. The server replaces it, as it serves `/shortcuts.js`, with
 * a SHA-256 of the word it read from `TICVAI_DROP_WORD` — which on the box comes
 * from `/etc/ticvai/drop.word`, a file that is not in git. So the running page
 * carries the hash, this repository carries a placeholder, and the word itself
 * lives in one file on one server. Written plainly here it would be published:
 * this file is committed to a public repository, and the page it opens is not
 * behind the gate, so the word is the only thing in front of it.
 *
 * **What that is worth, honestly.** A hash is not a lock. If the word is short
 * and ordinary, somebody who decides to go after it can hash a word list and
 * have it in seconds; what this stops is the far likelier case of somebody
 * reading the repository and finding the word sitting there in plain sight. It
 * also guards a page already published on the open web under its own domain, so
 * what is being protected is tidiness, not a secret. Do not put anything behind
 * this that would actually matter if it were found.
 *
 * **Unset is off.** When no word is deployed the server substitutes an empty
 * string, no typed word can hash to that, and the sequence does nothing. That is
 * the right default for anybody else who clones this — no word file, no drop.
 *
 * **Its own module, because it used to live in `theme.js` on the claim that
 * theme.js is loaded by every page in the viewer.** It is not: eight of the
 * twenty-six loaded no theme module at all, and two of those are `landing.html`
 * and `login.html` — the door, and the page in front of it, which are exactly
 * where somebody idly types a magic word.
 *
 * Splitting it means a page can take the sequence without also taking the
 * theming. That matters for `landing.html`, which carries no theme attribute at
 * all and would have been flipped to night by importing theme.js. It does not
 * matter for `login.html`, which stamps the theme itself in an inline script
 * before it paints — worth knowing before anyone "tidies" that duplication
 * away, because an imported module cannot run before first paint and the
 * inline stamp is there to stop the page flashing day on the way to night.
 *
 * **Where it is loaded, exactly.** Every page that imports `theme.js` gets it
 * from there, and `landing.html`, `login.html` and `invite.html` carry their
 * own tag. The five remaining pages — `burst`, `canvas`, `platforms`, `uiux`
 * and `uiux-boards` — are shells with an empty `<body></body>` whose content is
 * drawn by script, and several are embedded in a frame on a page that already
 * has the listener. They are left out deliberately rather than missed.
 *
 * `/shortcuts.js` is itself on the public allowlist, because it has to load on the
 * two signed-out pages. Leaving it off is how it silently did nothing on exactly
 * the pages it was added for: a module that 302s to the sign-in page is a module
 * the browser refuses to parse, and nothing in the console says so.
 *
 * The HEAD request is what makes it quiet: when the drop is not on the server —
 * it is deliberately not in git, see .gitignore — the sequence does nothing at
 * all rather than opening a tab onto a 404.
 *
 * `window.open` returns null here because of `noopener`, which is the spec and
 * not a failure; the tab opens regardless. Do not "fix" that null.
 */

/**
 * Replaced at serve time by `server.mjs` with a SHA-256 of the deployed word,
 * or with an empty string when none is deployed. The literal below is neither —
 * it is a token no SHA-256 will ever equal, so an un-substituted copy (served
 * raw, or opened from disk) matches nothing and stays silent.
 */
const OPEN_WORD = '__ADAM_DROP_HASH__';

// The prefix the path is salted with. Not the word, and not secret: the server
// derives the same `/drop/<digest>` in session.mjs from the same prefix, and
// this is only how the two ends agree on a URL without either holding it.
const OPEN_SALT = 'adam-drop:';

// The longest word the rolling buffer will hold. Comfortably above the deployed
// word's length; a word longer than this could never complete.
const LONGEST = 32;

const hex = async (text) => {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
};

const open = (path) => {
  fetch(path, { method: 'HEAD', redirect: 'manual' })
    .then((res) => { if (res.ok) window.open(path, '_blank', 'noopener'); })
    .catch(() => { /* not deployed here; say nothing */ });
};

let typed = '';
let mark = 0;

addEventListener('keydown', (event) => {
  // A hex hash means a deployed word; anything else — the placeholder, or the
  // empty string the server writes when none is set — means there is nothing to
  // match, so there is no reason to hash a keystroke.
  if (!/^[0-9a-f]{64}$/.test(OPEN_WORD)) return;
  if (!globalThis.crypto?.subtle) return; // secure context only: https or localhost

  // Not while somebody is typing. Without this the sequence fires out of any
  // search box that happens to contain those letters in that order.
  const on = document.activeElement;
  if (on && (on.isContentEditable || /^(?:INPUT|TEXTAREA|SELECT)$/.test(on.tagName))) return;
  if (event.ctrlKey || event.metaKey || event.altKey) return;

  // A run has to be typed, not accumulated over an afternoon.
  const now = Date.now();
  if (now - mark > 1500) typed = '';
  mark = now;
  if (event.key.length !== 1) return;

  // The word's length is not known here, so every tail of the buffer is tried.
  // All of it is local: nothing is asked of the server until a word matches,
  // which is what keeps a probe per keystroke out of the network panel and out
  // of the access log, where it would advertise the whole mechanism.
  typed = (typed + event.key.toLowerCase()).slice(-LONGEST);
  const buffer = typed;
  for (let length = 3; length <= buffer.length; length += 1) {
    const candidate = buffer.slice(-length);
    hex(candidate).then(async (digest) => {
      if (digest !== OPEN_WORD) return;
      typed = '';
      open(`/drop/${(await hex(OPEN_SALT + candidate)).slice(0, 16)}.html`);
    }).catch(() => { /* no digest available; say nothing */ });
  }
});
