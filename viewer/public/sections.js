/**
 * The list on the left of a sectioned page, following what is on screen.
 *
 * Settings, the admin page and the tasks page are the same page shape — a
 * `.set-nav` of links beside a column of `.set-section` panels — so the marking
 * lives here rather than three times over.
 *
 * An observer rather than a scroll handler: a scroll handler asks every section
 * where it is on every frame, and the answer is the same one the browser
 * already knows. The margins make "the section being read" mean the one under
 * the top of the window rather than the one nearest the middle, which is what a
 * reader following a long page expects.
 */
export function followSections(firstId = '') {
  const links = new Map(
    [...document.querySelectorAll('.set-nav a[href^="#"]')]
      .map((a) => [a.getAttribute('href').slice(1), a]),
  );
  const mark = (id) => {
    for (const [key, link] of links) link.setAttribute('aria-current', String(key === id));
  };
  // A click marks its own section at once. The observer agrees a moment later,
  // once the scroll lands; without this the link you just pressed stays dim.
  for (const [id, link] of links) link.addEventListener('click', () => mark(id));

  const watcher = new IntersectionObserver((entries) => {
    const showing = entries.filter((e) => e.isIntersecting)
      .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (showing.length) mark(showing[0].target.id);
  }, { rootMargin: '-90px 0px -55% 0px' });
  for (const section of document.querySelectorAll('.set-section')) watcher.observe(section);

  mark(location.hash.slice(1) || firstId || [...links.keys()][0] || '');
  return watcher;
}
