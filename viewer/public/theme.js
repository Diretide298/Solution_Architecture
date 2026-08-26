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
