/**
 * ADAM's own release notes.
 *
 * The content is a markdown file in this folder rather than rows in a database,
 * and that is the whole design. Release notes are written by a person, reviewed
 * in a diff alongside the change they describe, and deployed with it — so the
 * note and the thing it describes cannot drift apart, and nobody has to
 * remember to go and type it in somewhere afterwards.
 *
 * It is behind the same gate as every other page: what has changed in ADAM says
 * a good deal about what is being built and for whom.
 */

import { requireSignIn, servedBuild } from '/validation.js';
import { markdownBlock } from '/core.js';

const $ = (id) => document.getElementById(id);

if (await requireSignIn()) {
  $('updates').hidden = false;

  // The build first and separately: it is the one line on this page that is a
  // fact about right now rather than a record of what happened, and somebody
  // reading an entry that mentions the connector wants it in front of them.
  //
  // Its failure is not the page's failure — the notes are worth reading on an
  // ADAM too old to answer — so it degrades to nothing rather than to an error.
  servedBuild()
    .then((build) => {
      $('up-build').textContent = build
        ? `This ADAM is serving connector build ${build}. `
          + 'Settings → Claude connector → Builds says which one you are running.'
        : '';
    })
    .catch(() => { $('up-build').textContent = ''; });

  try {
    const answer = await fetch('/updates.md', { headers: { accept: 'text/markdown' } });
    if (!answer.ok) throw new Error(`the notes did not load (${answer.status})`);
    const text = await answer.text();

    // `adrLinks: false` — the renderer otherwise turns anything shaped like a
    // decision reference into a link into the package, and prose here mentions
    // things like `1.10` that are not decisions and would 404.
    const body = markdownBlock(text, { adrLinks: false });
    $('up-body').replaceChildren(body);
  } catch (error) {
    $('up-body').replaceChildren();
    $('up-error').hidden = false;
    $('up-error').textContent = `${error.message}. The file is viewer/public/updates.md.`;
  }
} else {
  $('signed-out').hidden = false;
}
