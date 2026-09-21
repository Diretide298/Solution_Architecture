/**
 * The viewer's top bar, on the pages that are not the viewer.
 *
 * **Eight pages were outside the application they belong to.** Settings, admin,
 * tasks, validation, reviews, changes, domains and audit each drew a minimal
 * `.admin-bar` — a lockup, the page's name, and a "Back to the viewer" chip —
 * so a reader on any of them had no layer tabs, no search, no bell and no
 * account drawer. The way to your own settings was through the viewer, and the
 * way out of settings was back to the viewer. A section of a product that has
 * to be left before it can be navigated is a second application.
 *
 * This upgrades the bar that is already there rather than replacing it: the
 * `.admin-bar` is already the same dark strip in both themes, on the same
 * tokens as the viewer's `.chrome`, so what was missing was its middle and its
 * right-hand side — not its existence.
 *
 *     import '/page-chrome.js';   // once, at the top of the page's module
 *
 * **The tabs carry no counts, and that is the app's own rule rather than a
 * shortcut.** Each layer fetches its payload the first time it is opened, so a
 * settings page could not answer for any of them without fetching all nine.
 * `refreshLayerCounts` already says why the pill starts bare: *a zero is a
 * claim, where "not yet" is not.* The same holds one page across.
 *
 * The page's own left navigation is left exactly as it was. Settings keeps its
 * section list, admin keeps its own — what belongs to the page stays with the
 * page, and only the chrome around it is shared.
 */
// The saved day/night choice, stamped before anything paints. `setTheme` is
// the same one the viewer's toggle calls, so the two cannot drift on which key
// they write or on which value is the bare `:root`.
import { currentTheme, setTheme } from '/theme.js';
import { mountAccountDrawer } from '/account-drawer.js';

/**
 * Mirrors `LAYERS` in core.js — key, label and the one-line hint that becomes
 * the title attribute.
 *
 * **Named here rather than imported, deliberately.** `core.js` is the viewer's
 * shared vocabulary: it pulls in the tooltip engine, the glossary and the fact
 * provider, and a settings page has no use for any of it. What this needs is
 * nine labels and nine hrefs, and paying for the rest to get them would make
 * every standalone page carry the viewer's boot cost.
 *
 * The cost of the copy is that a tenth layer has to be added twice. That is
 * checked rather than hoped: `checks/chrome-check.mjs` reads `LAYERS` out of
 * core.js and fails if this list and that one disagree.
 */
const LAYER_LINKS = [
  ['frontend', 'Frontend', 'screens, journeys and the apps that implement them'],
  ['uiux', 'UI/UX', 'screens, flows and the design boards they are drawn on'],
  ['contracts', 'Contracts', 'the API — the join between the other two layers'],
  ['domain', 'Lifecycles', 'states/ and events/ — the legal moves, and what crosses the outbox'],
  ['backend', 'DB', 'the SQL in backend/, against the schema reference in handoff/'],
  // **`services`, not `architecture`.** The label and the key disagree here and
  // only here — the layer was renamed and the key stayed, because it is in deep
  // links, API paths and every mode id under it. Guessing the key from the label
  // gives a tab that lands on the default layer and looks like a dead button.
  ['services', 'Architecture', 'diagrams/ — the HLD, the sixteen LLDs, and what ships in what order'],
  ['build', 'Build', 'tools/refresh.sh — the package, derived step by step from the contracts'],
  ['cicd', 'CI/CD', 'repos/ · services/ · deploy/ — how it is built, shipped and run'],
  ['decisions', 'Decisions', 'docs/ — the ADRs, the registers, and the authorisation spec'],
];

const svg = (cls, body, extra = '') =>
  `<svg class="${cls}" viewBox="0 0 16 16" aria-hidden="true" ${extra}>${body}</svg>`;

const ICON_BELL = svg('icon-bell',
  '<path d="M4 6.5a4 4 0 0 1 8 0c0 2.4.6 3.6 1.2 4.2a.5.5 0 0 1-.35.85H3.15a.5.5 0 0 1-.35-.85C3.4 10.1 4 8.9 4 6.5Z" />'
  + '<path d="M6.6 13.4a1.6 1.6 0 0 0 2.8 0" />',
  'fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"');

const ICON_BURST = svg('icon-burst',
  '<rect x="1.6" y="2.2" width="4.4" height="2.9" rx="0.8" />'
  + '<rect x="1.6" y="6.6" width="4.4" height="2.9" rx="0.8" />'
  + '<rect x="1.6" y="11" width="4.4" height="2.9" rx="0.8" />'
  + '<path d="M6 3.65h2.2L11 8M6 8.05h5M6 12.45h2.2L11 8" opacity=".65" />'
  + '<path d="M11 5.6 14.2 8 11 10.4Z" fill="currentColor" stroke="none" />',
  'fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"');

const ICON_HOME = svg('icon-home',
  '<circle cx="8" cy="8" r="2.1" fill="currentColor" />'
  + '<circle cx="3" cy="3.6" r="1.5" fill="currentColor" opacity=".72" />'
  + '<circle cx="13" cy="3.6" r="1.5" fill="currentColor" opacity=".72" />'
  + '<circle cx="3" cy="12.4" r="1.5" fill="currentColor" opacity=".72" />'
  + '<circle cx="13" cy="12.4" r="1.5" fill="currentColor" opacity=".72" />'
  + '<path d="M8 8 3 3.6M8 8l5-4.4M8 8l-5 4.4M8 8l5 4.4" fill="none" stroke="currentColor" stroke-width="1" opacity=".5" />');

// Drawn, not typed. The viewer's was U+25D0 once, which is an icon only where a
// font ships it — and on a box with a minimal font set it is a tofu box sitting
// next to the bell, which made the bell look broken too.
const ICON_THEME = svg('icon-theme',
  '<circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.4" />'
  + '<path d="M8 2a6 6 0 0 0 0 12Z" fill="currentColor" />');

function buildChrome() {
  const bar = document.querySelector('header.admin-bar');
  if (!bar || bar.dataset.chrome) return;
  bar.dataset.chrome = 'full';

  // ── the layer tabs, between the brand and whatever the page already had ──
  //
  // Real anchors rather than buttons that navigate. These go to another
  // document, and a control that goes to another document should open in a new
  // tab when somebody middle-clicks it — which a <button> with an onclick
  // silently will not.
  const tray = document.createElement('nav');
  tray.className = 'layer-tray chrome-layers';
  tray.setAttribute('aria-label', 'Layer');
  for (const [key, label, hint] of LAYER_LINKS) {
    const a = document.createElement('a');
    a.href = `/?layer=${key}`;
    a.textContent = label;
    a.title = hint;
    a.dataset.layer = key;
    tray.append(a);
  }

  const divider = document.createElement('span');
  divider.className = 'chrome-divider';
  divider.setAttribute('aria-hidden', 'true');

  const brand = bar.querySelector('.brand');
  (brand ?? bar.firstElementChild).after(divider, tray);

  // ── the right-hand controls ─────────────────────────────────────────────
  const right = bar.querySelector('.admin-bar-right') ?? bar;

  // The "Back to the viewer" chip goes: the nine tabs beside it are nine ways
  // back, each of them saying where to. A general link next to specific ones is
  // the vaguer of two answers to a question already answered.
  right.querySelector('.chip[href="/"]')?.remove();

  right.insertAdjacentHTML('beforeend', `
    <button id="bell-toggle" class="icon-btn bell-toggle" type="button"
            title="Where you were named" aria-haspopup="dialog"
            aria-expanded="false" aria-controls="bell-panel" hidden>
      ${ICON_BELL}<span id="bell-count" class="bell-count" hidden></span>
    </button>
    <a id="burst-link" class="icon-btn" href="/?layer=cicd&amp;mode=cicd-burst"
       title="Deployment map — what a flash sale runs"
       aria-label="Deployment map — what a flash sale runs">${ICON_BURST}</a>
    <a id="home-link" class="icon-btn" href="/home.html"
       title="Every layer" aria-label="Every layer">${ICON_HOME}</a>
    <button id="account-toggle" class="icon-btn account-toggle" type="button"
            title="Your account" aria-haspopup="dialog">
      <span id="account-initials" class="account-initials">·</span>
    </button>
    <button id="theme-toggle" class="icon-btn" title="Toggle theme" type="button">
      ${ICON_THEME}
    </button>`);

  // `theme.js` stamps the theme on import and exports the setter; it binds no
  // control, because the control lives in whichever chrome is on the page. The
  // viewer binds its own; this binds this one, and both call `setTheme`.
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.onclick = () => setTheme(currentTheme() === 'dark' ? 'light' : 'dark');
  }

  // **`#whoami` stays.** Several of these pages write into it, and the account
  // button beside it answers a different question: the badge is who you are,
  // the line is what this page decided to say about you.
  mountAccountDrawer();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', buildChrome, { once: true });
} else {
  buildChrome();
}
