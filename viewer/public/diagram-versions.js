/**
 * Keeping a diagram the way somebody arranged it.
 *
 * **The package is never written to.** The nodes and the edges are read from it
 * on every draw, exactly as before; what is saved is where each box was
 * dropped. So a published diagram cannot disagree with the contracts about what
 * *exists* — only about where it sits on the page, which is the only part a
 * person was ever rearranging.
 *
 * Every renderer here already pins a dragged node (`fx`/`fy`) and keeps the pin
 * across a reload, because the arrangement is the reader's and not ours. This
 * makes that arrangement publishable: an admin or a team lead saves theirs as a
 * version, and from then on everybody opening that diagram sees it.
 *
 * **The danger of a hand-arranged diagram is that it keeps looking current.** A
 * picture laid out in March against a package that changed in June still
 * renders, still looks authoritative, and is quietly a picture of something
 * else. So a hash of what was drawn goes with the arrangement, the service
 * compares it on the next read, and the bar says the arrangement is older than
 * the package rather than letting somebody present it as today's. That is the
 * mitigation agreed when free-form editing was chosen over a constrained
 * editor, and it is the reason this file exists rather than just a save button.
 */

import * as auth from '/validation.js';

const $ = (id) => document.getElementById(id);

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

/**
 * A short, stable fingerprint of what a renderer just drew.
 *
 * The node ids, sorted, hashed. Sorted because the order a layout algorithm
 * emits them in is not a fact about the package — an arrangement would go stale
 * on every reload if it were. Positions are deliberately not in it: moving a
 * box is what this feature is *for*, so it must not count as the package having
 * changed.
 *
 * FNV-1a rather than a crypto hash: this is a change detector, not a signature,
 * and `crypto.subtle` is async and unavailable over plain http on some setups —
 * which is exactly where somebody runs a workstation.
 */
export function shapeOf(nodes) {
  const ids = (nodes ?? []).map((n) => String(n.id)).sort().join('\u0000');
  let hash = 0x811c9dc5;
  for (let i = 0; i < ids.length; i += 1) {
    hash ^= ids.charCodeAt(i);
    hash = Math.imul(hash, 0x01000193) >>> 0;
  }
  return `${ids.length ? (nodes ?? []).length : 0}-${hash.toString(16)}`;
}

/** Where every pinned node was dropped. Only the pinned ones: a node the
 *  layout placed and nobody touched has no arrangement worth keeping, and
 *  saving it would freeze a position the algorithm should be free to improve. */
function arrangementOf(view) {
  const nodes = {};
  for (const node of view.nodes ?? []) {
    if (node.fx == null && node.fy == null) continue;
    nodes[String(node.id)] = {
      x: Math.round(node.fx ?? node.x),
      y: Math.round(node.fy ?? node.y),
    };
  }
  return { nodes };
}

/** Put a saved arrangement onto the nodes a renderer is holding.
 *
 *  A node the arrangement does not name is left where the layout put it, and a
 *  name the package no longer has is ignored — both silently, because a package
 *  gaining a table is not an error and the bar already says when the two have
 *  drifted apart. */
function applyArrangement(view, layout) {
  const saved = layout?.nodes ?? {};
  let placed = 0;
  for (const node of view.nodes ?? []) {
    const at = saved[String(node.id)];
    if (!at) continue;
    node.x = at.x;
    node.y = at.y;
    node.fx = at.x;
    node.fy = at.y;
    placed += 1;
  }
  return placed;
}

const fmt = (iso) => (iso ? new Date(iso).toLocaleString(undefined,
  { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '');

/**
 * How far an arrangement has come adrift from what is on screen.
 *
 * **Two numbers, because they are two different situations.** `missing` is
 * boxes the arrangement places that are not there any more — the package lost
 * something, and the picture is older than what it is drawing. `unplaced` is
 * boxes on screen the arrangement says nothing about, which the layout has put
 * somewhere by itself; that is the ordinary state of a diagram somebody
 * arranged part of, and not a warning.
 *
 * **This replaced comparing a fingerprint of the drawn node ids**, which was
 * wrong in a way only a browser could show. The schemas view has a *Shared
 * $refs* toggle, so the same package draws 193 boxes or 195 depending on a
 * switch the reader controls — a fingerprint of what was drawn therefore
 * measured the view's settings as much as the package's shape, and flipping
 * that switch marked every arrangement as older than the package it was made
 * from. A warning that is always on is one nobody reads.
 *
 * The fingerprint is still sent and still stored: it is honest provenance for
 * what was on screen when somebody pressed save. It is just not what the
 * reader is told.
 */
function driftOf(view, layout) {
  const saved = layout?.nodes ?? {};
  const here = new Set((view?.nodes ?? []).map((n) => String(n.id)));
  let missing = 0;
  for (const id of Object.keys(saved)) if (!here.has(id)) missing += 1;
  let unplaced = 0;
  for (const id of here) if (!saved[id]) unplaced += 1;
  return { missing, unplaced };
}

/**
 * Mount the version bar on one diagram view.
 *
 * `name()` returns the diagram's key — `graph:spine`, `data:orders` — which is
 * the view *and* its scope, because the same view at two scopes is two
 * pictures. `view()` returns whichever renderer is on screen, the same question
 * the PNG export asks and for the same reason.
 */
export function mountDiagramVersions({ toolbar, name, view, onApplied }) {
  if (!toolbar || !name || !view) return null;

  const bar = el('span', 'dv-bar');
  const state = el('button', 'ghost-btn dv-state', 'Arrangement');
  state.type = 'button';
  const says = el('span', 'dv-says');
  bar.append(state, says);

  const panel = el('div', 'dv-panel');
  panel.hidden = true;

  let loaded = null;     // what the service last told us
  let applied = false;   // whether we have put it on the nodes this draw
  // Which read is the newest. A diagram fills in stages — the payload arrives,
  // then the scope resolves — so two reads can be in flight at once, and the
  // first to be *sent* is not always the first to come back. Without this the
  // answer for a half-drawn diagram could land last and win, and the bar would
  // report an arrangement as older than the package on the strength of a
  // fingerprint taken while the package was still loading.
  let newest = 0;
  // How far the current arrangement has come adrift from what is drawn. Kept
  // beside `loaded` rather than derived at draw time, because `draw` is called
  // from three places and recomputing it in each is three chances to compute
  // it against a different node set.
  let drift = { missing: 0, unplaced: 0 };

  const key = () => name();

  async function refresh({ apply = false } = {}) {
    const here = view();
    if (!here) return;
    const mine = ++newest;
    let answer;
    try {
      answer = await auth.diagramVersion(key(), shapeOf(here.nodes));
    } catch (error) {
      if (mine !== newest) return;
      says.textContent = '';
      state.title = error.message;
      return;
    }
    if (mine !== newest) return;
    loaded = answer;
    drift = driftOf(here, answer.current?.layout);

    if (apply && answer.current?.layout) {
      const placed = applyArrangement(here, answer.current.layout);
      applied = placed > 0;
      here.resize?.();
      onApplied?.(placed, answer);
    }
    draw();
  }

  function draw() {
    // On the element, so what this bar is about is visible in devtools and to
    // a check. A diagram key that has to be reconstructed from the URL is one
    // that gets reconstructed slightly differently.
    state.dataset.diagram = key();
    const current = loaded?.current;
    state.classList.toggle('is-saved', Boolean(current));
    // Drift, not the fingerprint. The service still stores and compares one —
    // it is honest provenance for what was on screen — but what the reader is
    // told comes from `driftOf`, for the reason written above it.
    state.classList.toggle('is-stale', Boolean(current) && drift.missing > 0);
    if (!current) {
      state.textContent = 'Arrangement';
      says.textContent = '';
      state.title = 'Drawn from the package. Drag boxes to arrange it; an admin '
        + 'or a team lead can publish that arrangement for everybody.';
      return;
    }
    state.textContent = `v${current.version}`;
    says.textContent = drift.missing ? `${drift.missing} gone` : '';
    state.title = [
      `Version ${current.version}, saved by ${current.savedBy} on ${fmt(current.savedAt)}`,
      current.note ? `“${current.note}”` : '',
      drift.missing
        ? `${drift.missing} of the boxes this arrangement places are no longer in `
          + 'the package. It is older than what it is drawing.'
        : 'Every box it places is still here.',
      drift.unplaced
        ? `${drift.unplaced} on screen have no saved position and were placed `
          + 'automatically.'
        : '',
    ].filter(Boolean).join('\n');
  }

  async function open() {
    // Nothing has been read yet on the first click — the mount below defers
    // its read until the renderer has drawn, and somebody can be quicker than
    // that. Without this the panel decided what to offer from `loaded === null`
    // and showed everybody the read-only version, including the people who may
    // publish.
    if (!loaded) await refresh();
    panel.innerHTML = '';
    panel.hidden = false;
    const head = el('div', 'dv-head');
    head.append(el('strong', null, 'Arrangement'));
    const close = el('button', 'chip chip-quiet', 'Close');
    close.type = 'button';
    close.onclick = () => { panel.hidden = true; };
    head.append(close);
    panel.append(head);

    if (drift.missing) {
      panel.append(el('p', 'dv-warn',
        `${drift.missing} of the boxes this arrangement places are no longer in the `
        + 'package — it is older than what it is drawing. Rearrange and save '
        + 'again, or retire it.'));
    } else if (drift.unplaced && loaded?.current) {
      // Not a warning. Boxes with no saved position are the ordinary state of
      // a diagram somebody arranged part of, and of one where a toggle has
      // added a few — neither is the package having moved on.
      panel.append(el('p', 'auth-note auth-fine',
        `${drift.unplaced} boxes on screen have no saved position and were placed `
        + 'automatically. Arrange and save again to keep them where you want them.'));
    }

    if (!loaded?.mayPublish) {
      panel.append(el('p', 'auth-note auth-fine',
        'You can drag boxes around and it stays on your screen. Publishing an '
        + 'arrangement for everybody is an admin\'s or a team lead\'s.'));
      mountHistory();
      return;
    }

    const note = el('input', 'auth-input');
    note.placeholder = 'Why this arrangement (optional)';
    const save = el('button', 'chip cr-accept', 'Save as the next version');
    save.type = 'button';
    const said = el('span', 'dv-said');
    save.onclick = async () => {
      const here = view();
      if (!here) return;
      save.disabled = true;
      try {
        const made = await auth.saveDiagram(key(), arrangementOf(here),
          shapeOf(here.nodes), note.value);
        note.value = '';
        await refresh();
        // Re-render rather than patch: what the panel offers depends on
        // whether there is a current version, and there is one now. Leaving it
        // as it was meant somebody who had just published had no way to undo
        // it without closing the panel first.
        await open();
        panel.querySelector('.dv-said').textContent = `Saved as v${made.version}.`;
      } catch (error) {
        said.textContent = error.message;
      } finally {
        save.disabled = false;
      }
    };
    const bar2 = el('div', 'dv-actions');
    bar2.append(note, save, said);
    panel.append(bar2);

    if (loaded?.current) {
      const stop = el('button', 'chip', 'Back to the generated diagram');
      stop.type = 'button';
      stop.title = 'Stops showing any saved arrangement. Nothing is deleted — '
        + 'every version stays and any of them can be restored.';
      stop.onclick = async () => {
        stop.disabled = true;
        try { await auth.retireDiagram(key()); await refresh(); await open(); }
        catch (error) { said.textContent = error.message; }
        finally { stop.disabled = false; }
      };
      panel.append(stop);
    }
    mountHistory();
  }

  async function mountHistory() {
    const old = panel.querySelector('.dv-history');
    if (old) old.remove();
    const box = el('div', 'dv-history');
    panel.append(box);
    let seen;
    try { seen = await auth.diagramVersions(key()); }
    catch (error) { box.append(el('p', 'auth-error', error.message)); return; }
    if (!seen.versions.length) {
      box.append(el('p', 'auth-note auth-fine',
        'No arrangement has been saved for this diagram.'));
      return;
    }
    box.append(el('div', 'dv-label',
      `${seen.versions.length} version${seen.versions.length === 1 ? '' : 's'} — nothing is ever deleted`));
    for (const v of seen.versions) {
      const row = el('div', `dv-row${v.status === 'current' ? ' is-current' : ''}`);
      row.append(el('span', 'dv-v', `v${v.version}`));
      row.append(el('span', 'dv-who', `${v.savedBy} · ${fmt(v.savedAt)}`));
      row.append(el('span', 'dv-note', v.note || ''));
      row.append(el('span', 'dv-count', `${v.nodes} boxes`));
      if (v.status === 'current') {
        row.append(el('span', 'dv-badge', 'showing'));
      } else if (seen.mayPublish) {
        const back = el('button', 'chip chip-quiet', 'Show this one');
        back.type = 'button';
        back.onclick = async () => {
          back.disabled = true;
          try { await auth.restoreDiagram(key(), v.version); await refresh({ apply: true }); await open(); }
          catch (error) { row.append(el('span', 'dv-said', error.message)); back.disabled = false; }
        };
        row.append(back);
      }
      box.append(row);
    }
  }

  state.onclick = () => { if (panel.hidden) open(); else panel.hidden = true; };

  const hint = toolbar.querySelector('.graph-hint');
  if (hint) toolbar.insertBefore(bar, hint);
  else toolbar.append(bar);
  toolbar.parentElement?.insertBefore(panel, toolbar.nextSibling);

  // Read it, and put it on the diagram — the whole point of publishing one is
  // that the next person to open the view sees it without doing anything.
  //
  // **Not once on mount.** What this bar is about changes twice after it
  // mounts and neither moment is announced: the payload arrives and fills the
  // renderer, and the scope resolves and changes the key. Reading on the
  // second frame read `er:all` against an empty diagram and then sat there,
  // so a published arrangement never appeared for anybody but the person who
  // had just saved it.
  //
  // So: watch, and act only when something actually changed. A frame loop
  // rather than a timer because it stops while the tab is hidden, and the
  // guard means one request per real change rather than one per frame.
  let watching = '';
  const watch = () => {
    const here = view();
    const now = `${key()}|${here?.nodes?.length ?? 0}`;
    if (here?.nodes?.length && now !== watching) {
      watching = now;
      refresh({ apply: true }).catch(() => { /* a diagram still draws without one */ });
    }
    requestAnimationFrame(watch);
  };
  requestAnimationFrame(watch);

  return {
    /** Called when the view has drawn something new: re-read, and put the
     *  saved arrangement on it. Debounced by the caller, not here — a renderer
     *  that repaints on every frame is not this module's problem to solve. */
    refresh: (opts) => refresh(opts),
    applied: () => applied,
  };
}
