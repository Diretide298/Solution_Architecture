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
    // Said on the control rather than in a note underneath it: a section that
    // silently contributes nothing to the document is the kind of thing
    // somebody reports as a bug a fortnight later.
    if (section.excelOnly) label.append(el('span', 'auth-fine', ' spreadsheet only'));
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
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';

  try {
    // An empty build, to learn which sections this reader may have without
    // generating anything. The server narrows the list; the page does not.
    // Both lists, because the two outputs do not carry the same sections: the
    // workbook has one for the wireframe boards and the document has none,
    // a board being a picture. One picker drawn from the wider list, with the
    // difference marked, rather than two pickers that mostly agree.
    const [docRes, wbRes] = await Promise.all([
      auth.apiFetch('/document?sections='),
      auth.apiFetch('/workbook'),
    ]);
    if (!docRes.ok) throw new Error(`the server answered ${docRes.status}`);
    const inDocument = new Set(((await docRes.json()).available ?? []).map((s) => s.id));
    const sheets = wbRes.ok ? ((await wbRes.json()).available ?? []) : [];
    state.available = sheets.length
      ? sheets.map((s) => ({ ...s, excelOnly: !inDocument.has(s.id) }))
      : [...inDocument].map((id) => ({ id, title: id }));
  } catch (error) {
    say(error.message);
    return;
  }
  drawSections();

  $('dc-build').onclick = build;

  // The same sections, as a spreadsheet. The file is built and named by the
  // server, so this asks for it and hands the browser the bytes rather than
  // assembling a workbook out of JSON the page would have to fetch twice.
  $('dc-excel').onclick = async () => {
    const wanted = chosen();
    if (!wanted.length) { $('dc-says').textContent = 'Choose a section first.'; return; }
    $('dc-excel').disabled = true;
    $('dc-says').textContent = 'Building the workbook…';
    try {
      const res = await auth.apiFetch(`/workbook?sections=${encodeURIComponent(wanted.join(','))}`);
      if (!res.ok) {
        // The server says what is wrong in a sentence; a bare status code
        // would send somebody to the network tab to find it out again.
        let why = `the server answered ${res.status}`;
        try { why = (await res.json()).error ?? why; } catch { /* not JSON */ }
        throw new Error(why);
      }
      const blob = await res.blob();
      // The name the server chose, off Content-Disposition, so the file is
      // called the same thing however it was fetched.
      const said = res.headers.get('content-disposition') ?? '';
      const named = /filename="([^"]+)"/.exec(said)?.[1];
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = named
        || `${auth.project() ?? 'adam'}-${new Date().toISOString().slice(0, 10)}.xlsx`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 10_000);
      const sheets = res.headers.get('x-ticvai-sheets');
      const rows = res.headers.get('x-ticvai-rows');
      $('dc-says').textContent = sheets
        ? `${sheets} sheets, ${Number(rows).toLocaleString()} rows.` : 'Downloaded.';
    } catch (error) {
      $('dc-says').textContent = error.message;
    }
    $('dc-excel').disabled = false;
  };

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
