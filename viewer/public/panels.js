/**
 * One section on screen at a time, driven by the nav beside it.
 *
 * **Why this exists rather than a third copy.** Settings grew a tab strip that
 * shows one section and hides the rest; the tasks page needed the same
 * behaviour and would have got its own. Two implementations of "which panel is
 * showing" is how one of them quietly stops syncing the hash, or stops
 * restoring the right section on a deep link, and nobody notices because the
 * other one still works.
 *
 * **It does not care what the nav looks like.** Settings uses a row of
 * `<button data-tab>`; tasks uses a rail of `<a href="#id">` under group
 * headings, because the rail's grouping is worth keeping and a flat strip would
 * throw it away. Either is a list of things naming a section id.
 *
 * **A hidden control is not a destination.** Settings hides its Administration
 * tab for accounts that may not see it, and a link to `#admin` from somewhere
 * else must land on the fallback rather than on a section the reader is not
 * allowed. That check is here so it cannot be forgotten by the next caller.
 */

/**
 * @param {object} options
 * @param {Element} options.nav      the element holding the controls
 * @param {string}  options.fallback section id to show when the hash names none
 * @param {(name: string) => void} [options.onShow] called after each switch
 * @returns {(name: string) => void} show, for a caller that needs to switch
 */
export function mountPanels({ nav, fallback, onShow }) {
  const controls = [...nav.querySelectorAll('[data-tab], a[href^="#"]')];
  const nameOf = (el) => el.dataset.tab ?? el.getAttribute('href').slice(1);
  const names = controls.map(nameOf);

  const show = (want, push) => {
    const at = names.indexOf(want);
    const pick = at >= 0 && !controls[at].hidden ? want : fallback;

    for (const control of controls) {
      control.setAttribute('aria-current', nameOf(control) === pick ? 'true' : 'false');
    }
    for (const name of names) {
      const section = document.getElementById(name);
      if (section) section.hidden = name !== pick;
    }
    // `replaceState`, not `pushState`: switching section is not somewhere to go
    // back to, and a back button that walks the tabs is a back button that never
    // leaves the page.
    if (push) history.replaceState(null, '', `#${pick}`);
    // Back to the top of the section, not to wherever the last one was scrolled.
    window.scrollTo({ top: 0 });
    onShow?.(pick);
  };

  for (const control of controls) {
    control.addEventListener('click', (event) => {
      // An anchor would otherwise jump and put the id in the address itself.
      event.preventDefault();
      show(nameOf(control), true);
    });
  }
  addEventListener('hashchange', () => show(location.hash.slice(1), false));
  show(location.hash.slice(1) || fallback, false);

  return (name) => show(name, true);
}
