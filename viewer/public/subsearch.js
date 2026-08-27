/**
 * A text filter over what is already on a page.
 *
 * The palette searches the package. This is the other half of the same need and
 * a different thing: **once you are on a page, you want to narrow it**, not
 * leave it. `platforms.html`, `uiux.html` and `validation.html` each grew their
 * own; `domains.html` had a segmented control and no text box, and
 * `reviews.html` and `admin.html` had nothing at all — so the way to find one
 * reviewer among ninety, or one account, was Ctrl+F, which finds the word and
 * leaves the other eighty-nine on the screen around it.
 *
 * Shared rather than a fourth copy, because the three that exist already
 * disagree about small things — whether the count keeps its denominator,
 * whether an empty result says so — and a fourth would disagree differently.
 *
 * **It filters rendered rows, not data.** The pages that filter their data
 * before rendering do it better and keep doing it; this is for the ones whose
 * rendering it would mean rewriting to reach. The cost is honest and small: a
 * row that has not been drawn yet cannot be filtered, which is what `observe`
 * below is for.
 */

/**
 * @param input     the text field
 * @param sections  [{ box, rows, label }] — where to look, what a row is, and
 *                  what to call them in the count
 * @param options   count: an element to write "12 of 90" into
 *                  onEmpty: text for when nothing matches
 */
export function attachSubSearch(input, sections, options = {}) {
  if (!input) return { apply() {}, stop() {} };
  const live = sections.filter((s) => s.box);
  const count = options.count ?? null;
  const emptyText = options.onEmpty ?? 'Nothing on this page matches that.';

  // One per section, made on demand, so a page with nothing to say says nothing.
  const emptyNodes = new Map();

  let observer = null;

  function apply() {
    // Deaf while it works. The guards below avoid pointless DOM writes, but
    // they are one careless edit away from being incomplete, and the failure
    // mode is not a wasted render — it is a tab that stops answering. This
    // makes the whole class impossible rather than the instances unlikely.
    observer?.disconnect();
    try {
      filter();
    } finally {
      observe();
    }
  }

  function filter() {
    const needle = input.value.trim().toLowerCase();
    let shown = 0;
    let total = 0;

    for (const section of live) {
      const rows = [...section.box.querySelectorAll(section.rows)];
      let visible = 0;
      for (const row of rows) {
        // `textContent` and not a field list: these rows are already the
        // rendered answer, and every word in one is a word somebody might be
        // looking for. A field list here would silently exclude whatever the
        // page adds next.
        const hit = !needle || row.textContent.toLowerCase().includes(needle);
        row.hidden = !hit;
        if (hit) visible += 1;
      }
      total += rows.length;
      shown += visible;

      // A section that has been emptied by the filter says so where it was,
      // rather than vanishing — a heading with nothing under it reads as a page
      // that failed to load.
      // Every branch here is guarded on the DOM already being wrong, and that
      // is not tidiness — this runs *inside* the observed subtree.
      //
      // `note.textContent = emptyText` looks idempotent and is not: assigning
      // textContent replaces the child text node whether or not the text
      // changed, which is a childList mutation, which wakes the observer, which
      // calls this, which assigns it again. It span until the tab stopped
      // answering. An unconditional `append` of a node already appended is the
      // same trap one line down.
      let note = emptyNodes.get(section.box);
      if (rows.length && !visible) {
        if (!note) {
          note = document.createElement('p');
          note.className = 'subsearch-empty';
          note.textContent = emptyText;
          emptyNodes.set(section.box, note);
        }
        if (note.textContent !== emptyText) note.textContent = emptyText;
        if (note.parentNode !== section.box) section.box.append(note);
      } else if (note?.parentNode) {
        note.remove();
      }
    }

    if (count) {
      // With the denominator. A bare "12" beside a filter box is a number that
      // cannot be read: twelve of what?
      count.textContent = needle
        ? `${shown} of ${total}${options.noun ? ' ' + options.noun : ''}`
        : (total ? `${total}${options.noun ? ' ' + options.noun : ''}` : '');
    }
  }

  input.addEventListener('input', apply);

  /**
   * Re-apply when the page draws more.
   *
   * These pages render after their payload lands, and some of them re-render on
   * a tab change — so a filter typed first would be silently undone by rows
   * arriving after it, leaving every row on screen under a box that still says
   * it is filtering. `childList` only: hiding a row is an attribute change, and
   * observing attributes would wake this on every row it touches.
   */
  function observe() {
    observer ??= new MutationObserver(apply);
    for (const section of live) {
      observer.observe(section.box, { childList: true, subtree: true });
    }
  }

  apply();
  return { apply, stop: () => observer?.disconnect() };
}
