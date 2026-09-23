/**
 * The saved theme, applied before anything paints.
 *
 * Night is the default, and it is the one that carries the attribute — day is
 * the bare `:root`. So an unset key still has to be stamped, which is why the
 * check below is `?? 'dark'` rather than a plain equality: only the *unset*
 * case moved, and a reader who has chosen day still gets day.
 *
 * It is its own module rather than a corner of core.js because the standalone
 * pages — reviews, domains, platforms, validation — do not import core.js and
 * have no business pulling in the layer vocabulary and the tip wiring just to
 * read one localStorage key. They used to ignore the toggle completely and
 * render whichever theme :root happened to carry, which is how you could set
 * night on the main view and still be handed a cream page by the review table.
 */
export const THEME_KEY = 'ticvai-theme';

/**
 * 'dark' or 'light', read off the element rather than off storage — by the time
 * anything asks, the attribute is the truth and storage is only where it came
 * from. Absence of the attribute is day, which is what the CSS says too.
 */
export const currentTheme = () =>
  document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';

/** Stamps `theme`, remembers it, and hands it back. */
export function setTheme(theme) {
  if (theme === 'dark') document.documentElement.dataset.theme = 'dark';
  else delete document.documentElement.dataset.theme;
  localStorage.setItem(THEME_KEY, theme);
  return theme;
}

if ((localStorage.getItem(THEME_KEY) ?? 'dark') === 'dark') {
  document.documentElement.dataset.theme = 'dark';
}

/**
 * An easter egg: a key sequence that opens a standalone page.
 *
 * `xyzzy` is the traditional one, from Colossal Cave, and it is spelled as
 * character codes rather than a string so the word does not sit in the source
 * for anyone idly scrolling past. That is obscurity and not secrecy — the codes
 * decode in a second, and anybody reading this comment has already found it.
 * The real reason nobody stumbles on it is that nothing links to the page.
 *
 * It lives here because theme.js is loaded by every page in the viewer, so one
 * listener covers all of them without a new file or a new script tag.
 *
 * The HEAD request is what makes it quiet: when the page is not on the server —
 * it is deliberately not in git, see .gitignore — the sequence does nothing at
 * all rather than opening a tab onto a 404.
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
  fetch(SHELL, { method: 'HEAD' })
    .then((res) => { if (res.ok) window.open(SHELL, '_blank', 'noopener'); })
    .catch(() => { /* not deployed here; say nothing */ });
});
