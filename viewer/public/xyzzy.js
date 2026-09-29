/**
 * A key sequence that opens a standalone page.
 *
 * `xyzzy` is the traditional one, from Colossal Cave, and it is spelled as
 * character codes rather than a string so the word does not sit in the source
 * for anyone idly scrolling past. That is obscurity and not secrecy — the codes
 * decode in a second, and anybody reading this comment has already found it.
 * The real reason nobody stumbles on it is that nothing links to the page.
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
 * The HEAD request is what makes it quiet: when the page is not on the server —
 * it is deliberately not in git, see .gitignore — the sequence does nothing at
 * all rather than opening a tab onto a 404.
 *
 * `redirect: 'manual'` is the other half of quiet, and it is not optional. The
 * page sits behind the gate, so a signed-out reader is sent to `/login.html`
 * — which is public and answers 200. A following fetch therefore reports the
 * payload as present, and the sequence opens a tab onto the sign-in door: not
 * silence, and not the page. Left manual, the 302 arrives as an opaque
 * redirect whose `ok` is false, and a reader who may not have it gets nothing.
 *
 * `window.open` returns null here because of `noopener`, which is the spec and
 * not a failure; the tab opens regardless. Do not "fix" that null.
 */

const SHELL = '/offline.html';
const ORDER = [120, 121, 122, 122, 121];
let step = 0;
let mark = 0;

addEventListener('keydown', (event) => {
  // Not while somebody is typing. Without this the sequence fires out of any
  // search box that happens to contain those letters in that order.
  const on = document.activeElement;
  if (on && (on.isContentEditable || /^(?:INPUT|TEXTAREA|SELECT)$/.test(on.tagName))) return;
  if (event.ctrlKey || event.metaKey || event.altKey) return;

  // A run has to be typed, not accumulated over an afternoon.
  const now = Date.now();
  if (now - mark > 1500) step = 0;
  mark = now;

  const code = event.key.length === 1 ? event.key.toLowerCase().charCodeAt(0) : -1;
  // A miss still starts a new run when it is itself the opening character, or
  // a doubled first key would drop the attempt on the floor.
  if (code === ORDER[step]) step += 1;
  else step = code === ORDER[0] ? 1 : 0;
  if (step < ORDER.length) return;

  step = 0;
  fetch(SHELL, { method: 'HEAD', redirect: 'manual' })
    .then((res) => { if (res.ok) window.open(SHELL, '_blank', 'noopener'); })
    .catch(() => { /* not deployed here; say nothing */ });
});
