/**
 * The saved theme, applied before anything paints.
 *
 * Day is the default and carries no attribute, so this only ever has to stamp
 * the night one on.
 *
 * It is its own module rather than a corner of core.js because the standalone
 * pages — reviews, domains, platforms, validation — do not import core.js and
 * have no business pulling in the layer vocabulary and the tip wiring just to
 * read one localStorage key. They used to ignore the toggle completely and
 * render whichever theme :root happened to carry, which is how you could set
 * night on the main view and still be handed a cream page by the review table.
 */
export const THEME_KEY = 'ticvai-theme';

/** 'dark' or 'light'. Day is the default, so anything unset reads as light. */
export const currentTheme = () =>
  document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';

/** Stamps `theme`, remembers it, and hands it back. */
export function setTheme(theme) {
  if (theme === 'dark') document.documentElement.dataset.theme = 'dark';
  else delete document.documentElement.dataset.theme;
  localStorage.setItem(THEME_KEY, theme);
  return theme;
}

if (localStorage.getItem(THEME_KEY) === 'dark') {
  document.documentElement.dataset.theme = 'dark';
}
