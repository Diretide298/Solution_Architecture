/**
 * The curtain every page opens behind.
 *
 * The viewer reads a two-megabyte index before it can draw anything, and the
 * standalone pages each fetch their own slice before their tables mean
 * anything. Without a curtain that gap shows as an empty chrome with a
 * scrollbar — which does not read as "loading", it reads as "loaded, and there
 * is nothing here". The mark is the right thing to fill it with: it is a
 * network, and what the page is doing is assembling one.
 *
 * The markup is inline in each page rather than injected from here, because a
 * loader that arrives with the JavaScript is a loader that misses the part of
 * the wait it exists to cover — the module fetch itself. By the time this file
 * runs the curtain has already been up for a while. All this module does is
 * take it down.
 *
 * `window.load` is deliberately *not* one of the things that ends it. It fires
 * when the subresources are in, which on the viewer is well before `boot()`
 * has finished awaiting the index — using it would drop the curtain on the one
 * page whose wait is worth covering. So a page with a script of its own says
 * when it is ready, and importing this file is what claims that right. The
 * page's `<head>` snippet handles both the case where nobody claims it and the
 * case where the claim never arrives.
 */

const ID = 'adrov-loader';

// Claimed on import: the head snippet watches this to decide whether anything
// is going to lower the curtain deliberately, or whether it has to do it on
// `load` for a page that ships no script at all.
if (typeof window !== 'undefined') {
  window.__adrovLoader = window.__adrovLoader ?? {};
  window.__adrovLoader.claimed = true;
}

/** Down, and out of the accessibility tree with it. */
export function hideLoader() {
  const box = document.getElementById(ID);
  if (!box || box.classList.contains('is-done')) return;
  box.classList.add('is-done');
  box.setAttribute('aria-hidden', 'true');
  clearTimeout(window.__adrovLoader?.timer);

  // Removed rather than left transparent: it covers the viewport, and a
  // pointer-events:none overlay is still one focus trap and one stacking
  // context away from a bug nobody would think to connect to a loading screen.
  const drop = () => box.remove();
  box.addEventListener('transitionend', drop, { once: true });
  // Not every browser fires transitionend on every property, and a curtain
  // that stays up because an event did not arrive is precisely the failure
  // this file exists to prevent.
  setTimeout(drop, 700);
}

/**
 * A different line part-way through, for a wait that turns out to be long.
 * Only ever called by the page, which is the only thing that knows what it is
 * waiting for. Silent once the curtain is down.
 */
export function loaderSays(text) {
  const line = document.querySelector(`#${ID} .al-text`);
  if (line) line.textContent = text;
}
