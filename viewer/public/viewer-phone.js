/**
 * The viewer on a phone.
 *
 * Every standalone page gets its phone frame from page-chrome.js: an app bar, a
 * bottom bar and the More sheet. The viewer has its own chrome, so it takes
 * only the bottom bar and More, from the same builder (`mountPhoneBar`), and
 * layers.css styles both (under 720 px only; on a desk nothing here shows).
 * The lead moves between the viewer and the other pages without the
 * navigation changing under the thumb.
 *
 * Also here, because they only matter on a phone:
 *   - the chrome's real height, measured, so the off-canvas drawers start under
 *     it whatever the rows wrap to (`--viewer-chrome-h`);
 *   - a short note where a view's editing is desktop-only (decided with the
 *     lead: big diagrams and canvases are view and zoom only on a phone).
 */
import { mountPhoneBar } from './page-chrome.js';

const PHONE = window.matchMedia('(max-width: 719px)');

/** The chrome's height, for the drawers and the backdrop that start under it. */
function measureChrome() {
  const chrome = document.querySelector('.app > .chrome');
  if (!chrome || !('ResizeObserver' in window)) return;
  const root = document.documentElement;
  const set = () => root.style.setProperty('--viewer-chrome-h', `${Math.round(chrome.getBoundingClientRect().height)}px`);
  new ResizeObserver(set).observe(chrome);
  set();
}

/**
 * Each view's toolbar height, on the view, for the sheet under it. The sheets
 * start 46 px down on a desk, which is the desk toolbar; on a phone the toolbar
 * holds 44 px controls and is taller.
 */
function measureToolbars() {
  if (!('ResizeObserver' in window)) return;
  const seen = new WeakSet();
  const watch = new ResizeObserver((entries) => {
    for (const { target } of entries) {
      // 0 too: a toolbar with nothing to show on a phone is hidden, and the
      // sheet under it then starts at the top. A hidden view reports 0 as
      // well, and is measured again the moment it is shown.
      const h = Math.round(target.getBoundingClientRect().height);
      target.parentElement?.style.setProperty('--toolbar-h', `${h}px`);
    }
  });
  const scan = () => {
    for (const bar of document.querySelectorAll('#main > .view > .graph-toolbar')) {
      if (seen.has(bar)) continue;
      seen.add(bar);
      watch.observe(bar);
    }
  };
  scan();
  // Some views draw their toolbar on first open.
  new MutationObserver(scan).observe(document.getElementById('main'), { childList: true, subtree: true });
}

/** A rail with more past an edge says so with a fade at that edge. */
function railFades() {
  for (const rail of [document.getElementById('layers'), document.getElementById('modes')]) {
    if (!rail) continue;
    const mark = () => {
      const more = [];
      if (rail.scrollLeft > 2) more.push('start');
      if (rail.scrollLeft + rail.clientWidth < rail.scrollWidth - 2) more.push('end');
      if (more.length) rail.dataset.more = more.join(' ');
      else delete rail.dataset.more;
    };
    rail.addEventListener('scroll', mark, { passive: true });
    new MutationObserver(mark).observe(rail, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
    if ('ResizeObserver' in window) new ResizeObserver(mark).observe(rail);
    mark();
  }
}

/**
 * The bottom bar and More, from page-chrome.js like every other page's. Home
 * is lit (the viewer is entered from it) without being marked as this page;
 * More lists only the Deployment map under the package, since the viewer has
 * the layers as tabs; the theme goes through the viewer's own toggle, which
 * also repaints what was drawn with the old palette.
 */
function buildTabbar() {
  mountPhoneBar({
    current: 'home',
    className: 'viewer-tabbar',
    layers: false,
    setTheme: () => document.getElementById('theme-toggle')?.click(),
    watch: document.querySelector('.chrome'),
  });
}

/**
 * View and zoom only: a phone reads these and the desk edits them. One line
 * at the top of the view says so, where the edit control would have been.
 */
const DESK_ONLY = {
  'view-er': 'Moving tables is for a desk. Drag, pinch, tap a table.',
  'view-er-services': 'Moving boxes is for a desk. Drag, pinch, tap a box.',
  'view-structure': 'Rearranging is for a desk. Drag, pinch, tap a node.',
  'view-states': 'Rearranging is for a desk. Drag, pinch, tap a state.',
  'view-data': 'Moving tables is for a desk. Drag, pinch, tap a table.',
  // In the canvas's own column, over the sheet rather than over the bar.
  'view-uiux-screens': ['#viewport', 'Arranging screens is for a desk. Drag, pinch, tap a screen.'],
};

function deskNotes() {
  for (const [id, spec] of Object.entries(DESK_ONLY)) {
    const view = document.getElementById(id);
    if (!view || view.querySelector('.phone-desk-note')) continue;
    const [before, says] = Array.isArray(spec) ? spec : [null, spec];
    const note = document.createElement('p');
    note.className = 'phone-desk-note';
    note.textContent = says;
    const at = before && view.querySelector(before);
    if (at) { note.classList.add('is-inline'); at.before(note); } else view.prepend(note);

    // Tap for details. A tap on these drawings says what it picked in the
    // toolbar's hint line (a transition's guard, a table's columns), and that
    // line is hidden on a phone for want of room. So after a tap in the view
    // the note line says it instead.
    const hint = view.querySelector('.graph-hint');
    if (!hint) continue;
    let touched = -Infinity;
    view.addEventListener('pointerdown', (e) => { if (e.pointerType === 'touch') touched = performance.now(); }, true);
    new MutationObserver(() => {
      const text = hint.textContent.trim();
      if (!text || performance.now() - touched > 1500) return;
      note.textContent = text;
      note.classList.add('is-hint');
    }).observe(hint, { childList: true, characterData: true, subtree: true });
  }
}

/**
 * The UI/UX layer's three-pane views, one pane at a time.
 *
 * Each is a rail (what to look at), a middle (what is drawn) and, on two of
 * them, a detail pane (the one you picked), side by side on a desk. A phone has
 * room for one, so a strip of tabs over the view picks which, and the panes
 * move on by themselves the way a reader expects: picking from the rail shows
 * the middle, and opening a screen or a board shows its detail.
 */
const PANES = {
  'view-uiux-screens': {
    shell: '.canvas-main',
    panes: [['#rail', 'Lists'], ['.canvas-stage', 'Canvas'], ['#detail', 'Screen']],
    start: 1,
  },
  'view-uiux-boards': {
    shell: '.ux-shell',
    panes: [['.ux-rail', 'Browse'], ['.ux-main', 'Boards'], ['#bd-detail', 'Picked']],
    start: 1,
  },
  'view-uiux-platforms': {
    shell: '.ux-shell',
    panes: [['.ux-rail', 'Browse'], ['.ux-main', 'Platforms']],
    start: 1,
  },
};

function phonePanes() {
  for (const [id, spec] of Object.entries(PANES)) {
    const view = document.getElementById(id);
    const shell = view?.querySelector(spec.shell);
    if (!shell || view.querySelector('.phone-panes')) continue;
    const panes = spec.panes.map(([sel]) => shell.querySelector(sel));
    if (panes.some((p) => !p)) continue;

    const strip = document.createElement('div');
    strip.className = 'phone-panes';
    strip.setAttribute('role', 'tablist');
    strip.setAttribute('aria-label', 'Show');
    const tabs = spec.panes.map(([, label], i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'phone-pane-tab';
      b.setAttribute('role', 'tab');
      b.textContent = label;
      b.onclick = () => show(i);
      strip.append(b);
      panes[i].classList.add('phone-pane');
      return b;
    });
    shell.before(strip);
    view.classList.add('has-phone-panes');

    let on = -1;
    function show(i) {
      on = i;
      panes.forEach((p, n) => p.classList.toggle('is-phone-on', n === i));
      tabs.forEach((t, n) => {
        t.setAttribute('aria-selected', String(n === i));
        // A detail pane with nothing in it yet is not a place to go.
        const empty = n === 2 && (panes[n].hidden || !panes[n].textContent.trim());
        t.disabled = empty;
      });
    }
    show(spec.start);

    // Picking in the rail is asking to see it: go to the middle.
    panes[0].addEventListener('click', (e) => {
      if (!PHONE.matches) return;
      if (e.target.closest('.ux-row, .cv-row, .ux-tree button, .ux-tree a')) setTimeout(() => show(1), 0);
    });
    // A detail that fills in or opens after a tap in the middle: go to it.
    if (panes[2]) {
      let armed = false;
      panes[1].addEventListener('click', () => { armed = true; setTimeout(() => { armed = false; }, 1200); }, true);
      new MutationObserver(() => {
        const has = !panes[2].hidden && panes[2].textContent.trim();
        tabs[2].disabled = !has;
        if (has && armed && PHONE.matches) { armed = false; show(2); }
        else if (!has && on === 2) show(1);
      }).observe(panes[2], { childList: true, subtree: true, attributes: true, attributeFilter: ['hidden'] });
    }
  }
}

/**
 * The design diagrams (HLD, LLD, scopes) are SVGs in a frame that scrolls
 * sideways, so one finger already pans them. Two fingers zoom them, from the
 * frame's width (the whole drawing) to three times the drawing's own size, and
 * the point between the fingers stays put. The page's own zoom is off in the
 * app, so without this the only size a diagram had was the one it opened at.
 */
function pinchDiagrams() {
  const main = document.getElementById('main');
  if (!main) return;
  let g = null;
  const mid = (t) => ({ x: (t[0].clientX + t[1].clientX) / 2, d: Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY) });
  main.addEventListener('touchstart', (e) => {
    if (e.touches.length !== 2) { if (e.touches.length > 2) g = null; return; }
    const frame = e.target.closest?.('.dia-frame');
    const svg = frame?.querySelector(':scope > svg');
    if (!svg) return;
    const z = frame.currentCSSZoom || 1;            // the reading scale round it
    const box = frame.getBoundingClientRect();
    const m = mid(e.touches);
    const w0 = svg.getBoundingClientRect().width;   // on screen, scale included
    if (!svg.dataset.naturalW) svg.dataset.naturalW = String(w0 / z);
    g = {
      frame, svg, z, d0: Math.max(1, m.d), w0,
      at: m.x - box.left,
      f: (frame.scrollLeft * z + (m.x - box.left)) / w0,
      min: frame.clientWidth - 8,                   // local px: the whole drawing in view
      max: Number(svg.dataset.naturalW) * 3,
    };
  }, { passive: true });
  main.addEventListener('touchmove', (e) => {
    if (!g || e.touches.length !== 2) return;
    const m = mid(e.touches);
    const local = Math.max(g.min, Math.min(g.max, (g.w0 * (m.d / g.d0)) / g.z));
    g.svg.style.minWidth = '0';
    g.svg.style.width = `${local}px`;
    g.svg.style.height = 'auto';
    g.frame.scrollLeft = (g.f * local * g.z - g.at) / g.z;
  }, { passive: true });
  const end = (e) => { if (e.touches.length < 2) g = null; };
  main.addEventListener('touchend', end, { passive: true });
  main.addEventListener('touchcancel', end, { passive: true });
}

/**
 * The legends under the drawings say how to drive them with a mouse: double-
 * click to open, scroll to zoom, drag a box to pin it. On a touch screen those
 * are instructions for gestures that do nothing, so the words follow the hand:
 * a tap picks, the card it raises opens (galaxyFocus in app.js), two fingers
 * zoom, and boxes are not pinned on a phone at all.
 */
const FINGER = window.matchMedia('(hover: none) and (pointer: coarse)');
const SAYINGS = [
  [/click a context, double-click to open it/g, 'tap a context, then Open'],
  [/double-click (an? |one )?([\w-]+) to open (?:it|one)(?: in the ER view)?/g, 'tap $1$2, then Open'],
  [/double-click to open (?:it|one|its contract)(?: in the ER view)?/g, 'tap, then Open'],
  [/click to fold one level · double-click to fold the branch/g, 'tap to fold one level'],
  [/scroll to zoom/g, 'pinch to zoom'],
  [/drag an? (?:state|box|table|node|card|screen) to (?:move|pin) it\s*·\s*/g, ''],
  [/\s*·\s*drag an? (?:state|box|table|node|card|screen) to (?:move|pin) it/g, ''],
  [/drag an? (?:state|box|table|node|card|screen) to (?:move|pin) it/g, ''],
  [/\bclick\b/g, 'tap'],
  [/\bhover\b/g, 'tap'],
];
function fingerWords() {
  const main = document.getElementById('main');
  if (!main) return;
  const fix = (root) => {
    if (!FINGER.matches) return;
    const scopes = root.matches?.('.graph-legend, .legend-row') ? [root] : root.querySelectorAll?.('.graph-legend, .legend-row') ?? [];
    for (const scope of scopes) {
      const walk = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
      while (walk.nextNode()) {
        const n = walk.currentNode;
        let t = n.textContent;
        for (const [re, to] of SAYINGS) t = t.replace(re, to);
        if (t !== n.textContent) n.textContent = t;
      }
    }
  };
  fix(main);
  new MutationObserver((records) => {
    for (const r of records) {
      const at = r.target.nodeType === 3 ? r.target.parentElement : r.target;
      const scope = at?.closest?.('.graph-legend, .legend-row') ?? at;
      if (scope) fix(scope);
    }
  }).observe(main, { childList: true, subtree: true, characterData: true });
}

/**
 * The key under a drawing, folded behind one button on a phone. Open, a key
 * at reading size covers a third of a phone's drawing; folded, it is a 44 px
 * pill in the corner that opens it. app.js redraws the keys, so the button is
 * put back whenever a key is redrawn. Hidden on a desk by viewer-phone.css.
 */
function legendKeys() {
  const main = document.getElementById('main');
  if (!main) return;
  const ensure = () => {
    for (const key of main.querySelectorAll('.graph-legend')) {
      if (key.querySelector(':scope > .legend-key')) continue;
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'legend-key';
      const paint = () => {
        const open = key.classList.contains('is-open');
        b.setAttribute('aria-expanded', String(open));
        b.textContent = open ? 'Hide the key' : 'Key';
      };
      b.onclick = () => { key.classList.toggle('is-open'); paint(); };
      paint();
      key.prepend(b);
    }
  };
  ensure();
  new MutationObserver(ensure).observe(main, { childList: true, subtree: true });
}

function boot() {
  measureChrome();
  measureToolbars();
  railFades();
  buildTabbar();
  deskNotes();
  phonePanes();
  pinchDiagrams();
  fingerWords();
  legendKeys();
  document.documentElement.classList.add('viewer-phone-ready');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot, { once: true });
} else {
  boot();
}
