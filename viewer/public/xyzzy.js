/**
 * Two key sequences that open a standalone page.
 *
 * `xyzzy` is the traditional one, from Colossal Cave, and it opens the drop at
 * `/offline.html` — which is **behind the gate**, so it answers a signed-in
 * reader and nobody else. Its word is spelled as character codes rather than a
 * string, which is obscurity and not secrecy: the codes decode in a second, and
 * anybody reading this comment has already found it. That is fine here — the
 * page behind it is refused to a stranger by the server, so the word being
 * readable costs nothing.
 *
 * The second sequence is the public one, and it is a different bargain: the
 * page it opens is **not** gated, so the word is the only thing in front of it.
 * That is why the word is not in this file. What is stored is a SHA-256 of it,
 * and the URL is derived from the word as well, so neither the word nor the
 * path can be read off the source — this file is committed to a public
 * repository, and anything written here plainly is published.
 *
 * **What that is worth, honestly.** A hash is not a lock. The word is short and
 * ordinary, so anybody who decides to go after it can hash a name list and have
 * it in seconds; what this stops is the far likelier case of somebody reading
 * the repository and finding the word sitting there in plain sight. It also
 * guards a page already published on the open web under its own domain, so what
 * is being protected is tidiness rather than a secret. Do not put anything
 * behind this that would actually matter if it were found.
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
 * `/xyzzy.js` is itself on the public allowlist in `viewer/lib/session.mjs`,
 * because it has to load on the two signed-out pages. Leaving it off is how it
 * silently did nothing on exactly the pages it was added for: a module that
 * 302s to the sign-in page is a module the browser refuses to parse, and
 * nothing in the console says so.
 *
 * The HEAD request is what makes both of them quiet. When the page is not on
 * the server — neither drop is in git, see .gitignore — the sequence does
 * nothing at all rather than opening a tab onto a 404.
 *
 * `redirect: 'manual'` is the other half of quiet, and it is not optional. The
 * gated drop sends a signed-out reader to `/login.html`, which is public and
 * answers 200, so a following fetch reports the payload as present and the
 * sequence opens a tab onto the sign-in door: not silence, and not the page.
 * Left manual, the 302 arrives as an opaque redirect whose `ok` is false.
 *
 * `window.open` returns null here because of `noopener`, which is the spec and
 * not a failure; the tab opens regardless. Do not "fix" that null.
 */

/** The gated drop. Its word may be read; the server refuses the page anyway. */
const GATED_WORD = [120, 121, 122, 122, 121];
const GATED_PATH = '/offline.html';

/**
 * The public drop, by hash.
 *
 * `OPEN_WORD` is SHA-256 of the word. The path is a digest of that same word
 * under a different prefix, so holding this constant does not hand over the URL
 * — the two are separate digests of a thing neither of them contains. The
 * server derives the same path from `TICVAI_DROP_WORD`; when that is unset
 * there is no public drop at all, which is the right default for anybody else
 * who clones this.
 */
const OPEN_WORD = '424b805d7cc050a2d67b39adba9f0eb5e7a4f7c9825b522d17d9bfce518a5f4c';
const OPEN_SALT = 'adam-drop:';
const LONGEST = 16;

const hex = async (text) => {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
};

const open = (path) => {
  fetch(path, { method: 'HEAD', redirect: 'manual' })
    .then((res) => { if (res.ok) window.open(path, '_blank', 'noopener'); })
    .catch(() => { /* not deployed here; say nothing */ });
};

let step = 0;
let typed = '';
let mark = 0;

addEventListener('keydown', (event) => {
  // Not while somebody is typing. Without this the sequence fires out of any
  // search box that happens to contain those letters in that order.
  const on = document.activeElement;
  if (on && (on.isContentEditable || /^(?:INPUT|TEXTAREA|SELECT)$/.test(on.tagName))) return;
  if (event.ctrlKey || event.metaKey || event.altKey) return;

  // A run has to be typed, not accumulated over an afternoon.
  const now = Date.now();
  if (now - mark > 1500) { step = 0; typed = ''; }
  mark = now;
  if (event.key.length !== 1) return;
  const key = event.key.toLowerCase();

  // --- the gated one, matched on the spot --------------------------------
  const code = key.charCodeAt(0);
  // A miss still starts a new run when it is itself the opening character, or
  // a doubled first key would drop the attempt on the floor.
  if (code === GATED_WORD[step]) step += 1;
  else step = code === GATED_WORD[0] ? 1 : 0;
  if (step === GATED_WORD.length) { step = 0; open(GATED_PATH); }

  // --- the public one, matched by hash -----------------------------------
  // The length of the word is not stored either, so every tail of the buffer is
  // tried. All of it is local: nothing is asked of the server until a word
  // matches, which is what keeps a probe per keystroke out of the network panel
  // and out of the access log, where it would advertise the whole mechanism.
  //
  // crypto.subtle exists only in a secure context — https and localhost, which
  // is every way this viewer is meant to be reached. Over plain http to a bare
  // address it is undefined and the public sequence does not work. Guarded
  // rather than shimmed: hand-rolling a digest to prop up a deployment that
  // should not exist is the worse trade.
  if (!globalThis.crypto?.subtle) return;
  typed = (typed + key).slice(-LONGEST);
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
