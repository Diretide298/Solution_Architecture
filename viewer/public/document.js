/**
 * The package as one document.
 *
 * **The page picks sections and nothing else.** All the building happens on the
 * server, from the same payloads the viewer draws — a second reader of the
 * contracts here would be a second answer to every question the viewer already
 * answers, and the two would drift the first time a field was renamed.
 *
 * What a reader may include is decided by the server too, from the same rule
 * that decides which tabs they get: a client has no Decisions in their document
 * either, and the list that comes back is already narrowed. The page never
 * offers a section it would then be refused.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

const state = { available: [], built: null };

function say(message) {
  $('dc-error').textContent = message ?? '';
  $('dc-error').hidden = !message;
}

function chosen() {
  return [...document.querySelectorAll('#dc-sections input:checked')].map((n) => n.value);
}

function drawSections() {
  const host = $('dc-sections');
  host.replaceChildren();
  for (const section of state.available) {
    const label = el('label', 'doc-section');
    const box = el('input');
    box.type = 'checkbox';
    box.value = section.id;
    box.checked = true;
    label.append(box, el('span', null, section.title));
    host.append(label);
  }
}

async function build() {
  say('');
  $('dc-says').textContent = 'Reading the package…';
  $('dc-build').disabled = true;
  try {
    const wanted = chosen();
    if (!wanted.length) { say('Choose at least one section.'); return; }
    const res = await auth.apiFetch(`/document?sections=${encodeURIComponent(wanted.join(','))}`);
    if (!res.ok) throw new Error(`the server answered ${res.status}`);
    state.built = await res.json();
  } catch (error) {
    say(error.message);
    $('dc-says').textContent = '';
    return;
  } finally {
    $('dc-build').disabled = false;
  }

  $('dc-preview').textContent = state.built.markdown;
  $('dc-preview-panel').hidden = false;
  $('dc-words').textContent = `${state.built.words.toLocaleString()} words`;
  $('dc-download').hidden = false;
  $('dc-copy').hidden = false;
  $('dc-print').hidden = false;
  $('dc-says').textContent = `${state.built.sections.length} section`
    + `${state.built.sections.length === 1 ? '' : 's'}.`;

  // Named rather than silently absent. A section that was asked for and is not
  // in the document is either a layer the package has not built or one this
  // reader may not have, and both are worth knowing before the file is sent on.
  const skipped = state.built.skipped ?? [];
  $('dc-skipped').hidden = !skipped.length;
  $('dc-skipped').textContent = skipped.length
    ? `Left out, because the package has nothing for ${skipped.length === 1 ? 'it' : 'them'} `
      + `or this account may not read ${skipped.length === 1 ? 'it' : 'them'}: ${skipped.join(', ')}.`
    : '';
}

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${me.role}` : '';

  try {
    // An empty build, to learn which sections this reader may have without
    // generating anything. The server narrows the list; the page does not.
    const res = await auth.apiFetch('/document?sections=');
    if (!res.ok) throw new Error(`the server answered ${res.status}`);
    const first = await res.json();
    state.available = first.available ?? [];
  } catch (error) {
    say(error.message);
    return;
  }
  drawSections();

  $('dc-build').onclick = build;

  $('dc-download').onclick = () => {
    // A BOM, so Word on Windows reads the dashes and the quotes as written —
    // the same reason the CSV exports carry one.
    const blob = new Blob(['﻿' + state.built.markdown],
      { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${auth.project() ?? 'adam'}-documentation-`
      + `${new Date().toISOString().slice(0, 10)}.md`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  };

  $('dc-copy').onclick = async () => {
    try {
      await navigator.clipboard.writeText(state.built.markdown);
      $('dc-says').textContent = 'Copied.';
    } catch {
      // Clipboard access is refused outright in some browsers and over plain
      // http. Selecting it is something the person can finish themselves.
      const range = document.createRange();
      range.selectNodeContents($('dc-preview'));
      getSelection().removeAllRanges();
      getSelection().addRange(range);
      $('dc-says').textContent = 'Selected — copy it with Ctrl+C.';
    }
  };

  $('dc-print').onclick = () => window.print();
})();
