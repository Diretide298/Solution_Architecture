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
 *
 * **A section has one name.** `lib/document.mjs` owns the list and the
 * workbook imports it, so the word on the tick box is the heading in the
 * document. The page never shows an id: a skipped section is reported by name.
 *
 * **A preview can go stale.** The ticks are live and the preview is not, so the
 * moment they disagree the preview says so, and anything that takes the
 * document away (download, copy, print) builds it again first. Taking away
 * last time's choice under this time's ticks is the failure this prevents.
 */

// The viewer's top bar on a page that is not the viewer, and the saved theme.
import '/page-chrome.js';
import * as auth from '/validation.js';
import { markdownBlock } from '/core.js';
import { el, plural } from '/sheet.js';

const $ = (id) => document.getElementById(id);

const state = {
  available: [],      // [{ id, title, excelOnly }]
  built: null,        // the last document the server built
  builtFor: '',       // the ticks it was built for, as a sorted key
  view: 'read',
};

const titleOf = (id) => state.available.find((s) => s.id === id)?.title ?? 'a section';

// ── the one place for an error ───────────────────────────────────────

function fail(message) {
  $('dc-error').textContent = message ?? '';
  $('dc-error').hidden = !message;
}

/**
 * An error whose message is already the sentence to show: what the server
 * said, or what happened and what to do. Marked so the catch that shows it
 * does not wrap it a second time.
 */
async function refused(res, doing) {
  let said = '';
  try { said = (await res.json()).error ?? ''; } catch { /* not JSON */ }
  const error = new Error(said || `${doing} failed: the server answered ${res.status}. `
    + 'Try again in a moment; if it keeps failing, the package may still be loading on the server.');
  error.said = true;
  return error;
}

/** A thrown error as a sentence: as it is when it already is one. */
const plainly = (error, doing, next) => (error.said ? error.message
  : `${doing} failed: ${error.message}. ${next}`);

// ── the ticks ────────────────────────────────────────────────────────

function chosen() {
  return [...document.querySelectorAll('#dc-sections input:checked')].map((n) => n.value);
}
const keyOf = (ids) => [...ids].sort().join(',');

function drawSections() {
  const host = $('dc-sections');
  host.replaceChildren();
  for (const section of state.available) {
    const label = el('label', 'doc-section');
    const box = el('input');
    box.type = 'checkbox';
    box.value = section.id;
    box.checked = true;
    box.onchange = ticked;
    label.append(box, el('span', null, section.title));
    // Said on the control rather than in a note underneath it: a section that
    // silently contributes nothing to the document is the kind of thing
    // somebody reports as a bug a fortnight later.
    if (section.excelOnly) label.append(el('span', 'sh-quiet', 'spreadsheet only'));
    host.append(label);
  }
  ticked();
}

function ticked() {
  const n = chosen().length;
  $('dc-count').textContent = `${n} of ${plural(state.available.length, 'section')} chosen`;
  if (n) fail('');
  // Stale only once something has been built; before that there is nothing to
  // be stale about.
  const stale = !!state.built && keyOf(chosen()) !== state.builtFor;
  $('dc-stale').hidden = !stale;
  $('dc-preview-panel').classList.toggle('is-stale', stale);
}

// ── building ─────────────────────────────────────────────────────────

/** Build the document for the current ticks. True when it worked. */
async function build() {
  fail('');
  const wanted = chosen();
  // Checked before anything is said about reading: the old order left
  // "Reading the package…" beside the error for as long as the page was open.
  if (!wanted.length) { fail('Choose at least one section, then generate.'); return false; }
  $('dc-says').textContent = 'Reading the package…';
  $('dc-build').disabled = true;
  try {
    const res = await auth.apiFetch(`/document?sections=${encodeURIComponent(wanted.join(','))}`);
    if (!res.ok) throw await refused(res, 'Generating the document');
    state.built = await res.json();
    state.builtFor = keyOf(wanted);
  } catch (error) {
    fail(plainly(error, 'Generating the document', 'Check your connection and try again.'));
    return false;
  } finally {
    $('dc-says').textContent = '';
    $('dc-build').disabled = false;
  }
  drawPreview();
  return true;
}

function drawPreview() {
  const built = state.built;
  $('dc-preview').textContent = built.markdown;
  // Rendered by the viewer's own Markdown reader, which escapes first and
  // understands the tables the document is mostly made of. `adrLinks: false`:
  // the links would point into a viewer the document's reader may not have.
  $('dc-rendered').replaceChildren(markdownBlock(built.markdown, { adrLinks: false }));
  $('dc-preview-panel').hidden = false;
  $('dc-words').textContent = `${built.words.toLocaleString()} words, ${plural(built.sections.length, 'section')}`;
  for (const id of ['dc-download', 'dc-copy', 'dc-print']) $(id).hidden = false;
  showView(state.view);
  ticked();

  // Named rather than silently absent. A section that was asked for and is not
  // in the document is either a layer the package has not built or one this
  // reader may not have, and both are worth knowing before the file is sent on.
  // The server reports ids, with the reason in brackets when one failed; the
  // reader gets the section's name.
  const skipped = (built.skipped ?? []).map((s) => {
    const at = s.indexOf(' (');
    return at < 0 ? titleOf(s) : `${titleOf(s.slice(0, at))}${s.slice(at)}`;
  });
  $('dc-skipped').hidden = !skipped.length;
  $('dc-skipped').textContent = skipped.length
    ? `Left out, because the package has nothing for ${skipped.length === 1 ? 'it' : 'them'} `
      + `or your account may not read ${skipped.length === 1 ? 'it' : 'them'}: ${skipped.join(', ')}.`
    : '';
}

function showView(view) {
  state.view = view;
  for (const b of document.querySelectorAll('[data-view]')) {
    b.setAttribute('aria-pressed', String(b.dataset.view === view));
  }
  $('dc-rendered').hidden = view !== 'read';
  $('dc-preview').hidden = view !== 'markdown';
}

/** The document for the current ticks, built again only when the ticks moved. */
async function current() {
  if (state.built && keyOf(chosen()) === state.builtFor) return true;
  return build();
}

// ── taking it away ───────────────────────────────────────────────────

function downloadMarkdown() {
  // A BOM, so Word on Windows reads the dashes and the quotes as written —
  // the same reason the CSV exports carry one.
  const blob = new Blob(['﻿' + state.built.markdown], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${auth.project() ?? 'adam'}-documentation-${new Date().toISOString().slice(0, 10)}.md`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 10_000);
}

async function copyMarkdown() {
  try {
    await navigator.clipboard.writeText(state.built.markdown);
    $('dc-says').textContent = 'Copied the Markdown.';
  } catch {
    // Clipboard access is refused outright in some browsers, over plain http,
    // and after a regenerate has used up the click. Selecting it is something
    // the person can finish themselves.
    showView('markdown');
    const range = document.createRange();
    range.selectNodeContents($('dc-preview'));
    getSelection().removeAllRanges();
    getSelection().addRange(range);
    $('dc-says').textContent = 'Selected: copy it with Ctrl+C.';
  }
}

async function downloadWorkbook() {
  fail('');
  const wanted = chosen();
  if (!wanted.length) { fail('Choose a section first, then download the spreadsheet.'); return; }
  $('dc-excel').disabled = true;
  $('dc-says').textContent = 'Building the workbook…';
  try {
    const res = await auth.apiFetch(`/workbook?sections=${encodeURIComponent(wanted.join(','))}`);
    // The server says what is wrong in a sentence; a bare status code would
    // send somebody to the network tab to find it out again.
    if (!res.ok) throw await refused(res, 'Building the workbook');
    const blob = await res.blob();
    // The name the server chose, off Content-Disposition, so the file is
    // called the same thing however it was fetched.
    const named = /filename="([^"]+)"/.exec(res.headers.get('content-disposition') ?? '')?.[1];
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = named || `${auth.project() ?? 'adam'}-${new Date().toISOString().slice(0, 10)}.xlsx`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
    const sheets = res.headers.get('x-ticvai-sheets');
    const rows = res.headers.get('x-ticvai-rows');
    $('dc-says').textContent = sheets
      ? `Downloaded: ${sheets} sheets, ${Number(rows).toLocaleString()} rows.` : 'Downloaded.';
  } catch (error) {
    $('dc-says').textContent = '';
    fail(plainly(error, 'Building the workbook', 'Check your connection and try again.'));
  } finally {
    $('dc-excel').disabled = false;
  }
}

// ── loading ──────────────────────────────────────────────────────────

(async () => {
  if (!(await auth.requireSignIn())) return;
  const me = auth.account();
  $('whoami').textContent = me ? `${me.name || me.email} · ${auth.roleLabel(me.role)}` : '';

  // The project by its name, so the form says whose document this is. The id
  // is the fallback rather than nothing: it is still the right project.
  auth.ensureProject().then(async (id) => {
    let name = id ?? '';
    try {
      const doc = await auth.listProjects();
      name = (doc?.projects ?? []).find((p) => p.id === id)?.name ?? name;
    } catch { /* the id will do */ }
    if (name) $('dc-project').textContent = name;
  });

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
    if (!docRes.ok) throw await refused(docRes, 'Reading which sections you may have');
    const inDocument = (await docRes.json()).available ?? [];
    const ids = new Set(inDocument.map((s) => s.id));
    const sheets = wbRes.ok ? ((await wbRes.json()).available ?? []) : [];
    state.available = sheets.length
      ? sheets.map((s) => ({ ...s, excelOnly: !ids.has(s.id) }))
      : inDocument;
  } catch (error) {
    $('dc-sections').replaceChildren();
    fail(plainly(error, 'Reading which sections you may have', 'Reload the page to try again.'));
    return;
  }
  drawSections();

  $('dc-form').onsubmit = (event) => { event.preventDefault(); build(); };
  $('dc-all').onclick = () => {
    for (const box of document.querySelectorAll('#dc-sections input')) box.checked = true;
    ticked();
  };
  $('dc-none').onclick = () => {
    for (const box of document.querySelectorAll('#dc-sections input')) box.checked = false;
    ticked();
  };
  for (const b of document.querySelectorAll('[data-view]')) b.onclick = () => showView(b.dataset.view);

  $('dc-excel').onclick = downloadWorkbook;
  $('dc-download').onclick = async () => { if (await current()) downloadMarkdown(); };
  $('dc-copy').onclick = async () => { if (await current()) copyMarkdown(); };
  // The rendered document, never the Markdown source: print.css hides the
  // page around it and shows the "as it reads" view whichever one is on.
  $('dc-print').onclick = async () => { if (await current()) window.print(); };
})();
