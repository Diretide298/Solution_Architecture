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
import {
  mountAccountDrawer, openAccountPanel, closeAccountPanel, closeBellPanel,
  showLinksFor, isDecider, initialsOf, holdSheet, releaseSheet, followFromSheet,
} from '/account-drawer.js';
import * as auth from '/validation.js';

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

// ── the phone frame ───────────────────────────────────────────────────────
//
// On a phone (under 720 px, DESIGN-SYSTEM.md's breakpoint) the bar above
// becomes a compact app bar (the mark, this page's name, the bell and you), and
// the places people go most sit in a bottom bar under the thumb. Everything
// else is one tap away in a full-screen sheet, More. All of it is drawn here and
// shown or hidden by CSS (layers.css, "the phone frame"), so a desk never sees
// it and a window narrowed past the breakpoint gets it without a reload.
//
// The bottom bar and More are built by `mountPhoneBar`, exported, and used by
// every page that has the bar: the frame pages (below), Home (home.js) and the
// viewer (viewer-phone.js). One builder, so the three cannot drift.

/** 24 px line icons at a 1.8 stroke, the design system's icon rule. */
const icon24 = (body) =>
  `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;

/**
 * The bottom bar, in order, and who sees each tab. The one list to change.
 *
 * At most five buttons with More, so a 360 px phone still gives each a 72 px
 * target. `bar(who)` says whether the tab is in the bar for this account; when
 * it is not and `orMore` is set, it heads More's list instead, with its icon.
 *
 *   Owner and lead:  Home, Tasks, My work, Decide, More (Changes heads More).
 *   Everyone else:   Home, Tasks, My work, Changes, More.
 *   A client:        Home, My work, Changes, More (Tasks refuses a client).
 *
 * The lead, 6 November 2026: Changes moves into More for the two roles that
 * have Decide, so the bar stays at five.
 */
export const PHONE_TABS = [
  { key: 'home', href: '/home.html', label: 'Home', bar: () => true,
    icon: icon24('<path d="M4 10.5 12 4l8 6.5V19a1 1 0 0 1-1 1h-4.5v-5.5h-5V20H5a1 1 0 0 1-1-1Z" />') },
  { key: 'tasks', href: '/tasks.html', label: 'Tasks', bar: (who) => !auth.isClient(who),
    icon: icon24('<path d="M10 6h10M10 12h10M10 18h10" /><path d="m3.5 6 1.3 1.3L7.5 4.6M3.5 12l1.3 1.3 2.7-2.7M3.5 18l1.3 1.3 2.7-2.7" />') },
  { key: 'board', href: '/board.html', label: 'My work', bar: () => true,
    icon: icon24('<rect x="3.5" y="4" width="7" height="16" rx="1.5" /><rect x="13.5" y="4" width="7" height="10" rx="1.5" />') },
  { key: 'changes', href: '/changes.html', label: 'Changes', bar: (who) => !isDecider(who), orMore: true,
    icon: icon24('<path d="M7 7v13M17 4v13" /><path d="m4 10 3-3 3 3M14 14l3 3 3-3" />') },
  { key: 'decide', href: '/decide', label: 'Decide', bar: (who) => isDecider(who),
    icon: icon24('<path d="M4 13l2.5-7.5h11L20 13M4 13v5.5h16V13M4 13h4.5l1 2.5h5l1-2.5H20" />') },
];
const ICON_MORE = icon24('<path d="M4 7h16M4 12h16M4 17h16" />');
const ICON_CLOSE = icon24('<path d="M6 6l12 12M18 6 6 18" />');
const ICON_CHEVRON = icon24('<path d="m9 6 6 6-6 6" />');

/** The page's name for the app bar: the bar's own subtitle, in sentence case. */
function pageTitle(bar) {
  const sub = bar.querySelector('.brand-sub')?.textContent.trim()
    || document.title.replace(/^Adam\W*/i, '').trim();
  return sub ? sub[0].toUpperCase() + sub.slice(1) : 'ADAM';
}

/** env(safe-area-inset-*) is zero unless the page asks to be laid out under the
 *  notch and the gesture bar; asked here once so every page with this frame
 *  gets it, including the ones added after this was written. */
function coverSafeAreas() {
  const meta = document.querySelector('meta[name="viewport"]');
  if (meta && !/viewport-fit/.test(meta.content)) meta.content += ', viewport-fit=cover';
  // The phone app's status bar and Android's own bar take the frame's colour.
  if (!document.querySelector('meta[name="theme-color"]')) {
    const tint = document.createElement('meta');
    tint.name = 'theme-color';
    tint.content = '#0b161c';
    document.head.append(tint);
  }
}

/** Which tab this address is, if any. */
function tabForHere() {
  const here = location.pathname.replace(/\/$/, '') || '/';
  return PHONE_TABS.find((t) => here === t.href || here === t.href.replace(/\.html$/, ''))?.key ?? null;
}

/** A text field: while one has focus, the keyboard is up. */
const TYPING = 'textarea, [contenteditable="true"], input:not([type="checkbox"], [type="radio"], [type="button"], '
  + '[type="submit"], [type="reset"], [type="range"], [type="color"], [type="file"], [type="hidden"])';

/**
 * The bottom bar and the More sheet, on any page. Drawn always and shown by
 * CSS under 720 px only (layers.css), so a desk never sees it.
 *
 * @param o.current    the tab this page is, a PHONE_TABS key; defaults to the
 *                     tab whose address this is. Marked `aria-current="page"`
 *                     on that tab's own page and only lit elsewhere (the viewer
 *                     is entered from Home, so Home is lit there). A page that
 *                     is no tab, or whose tab is in More for this account,
 *                     lights More.
 * @param o.className  extra classes for the bar
 * @param o.layers     true: More lists the package's layers (a page without
 *                     layer tabs of its own); false: only the Deployment map
 * @param o.setTheme   how this page changes theme (the viewer repaints through
 *                     its own toggle); theme.js's by default
 * @param o.watch      where the "What's new" chip turns up, for More's dot
 * @param o.drawer     true on a page that mounts no account drawer of its own
 *                     (Home): it is mounted the first time More opens, since
 *                     More copies its groups and "you" at its top opens it
 * @returns { tabbar, openMenu, closeMenu }
 */
export function mountPhoneBar({
  current = tabForHere(), className = '', layers = true,
  setTheme: changeTheme = setTheme, watch = document.body, drawer = false,
} = {}) {
  const ownPage = current != null && current === tabForHere();

  // Real links, so a long press offers "open in new tab" and the current page
  // is marked the way a screen reader expects.
  const tabbar = document.createElement('nav');
  tabbar.className = `phone-tabbar ${className}`.trim();
  tabbar.setAttribute('aria-label', 'Main');
  for (const tab of PHONE_TABS) {
    const a = document.createElement('a');
    a.className = 'phone-tab';
    a.href = tab.href;
    a.dataset.tab = tab.key;
    a.innerHTML = `${tab.icon}<span class="phone-tab-label">${tab.label}</span>`;
    tabbar.append(a);
  }
  const more = document.createElement('button');
  more.type = 'button';
  more.id = 'phone-more';
  more.className = 'phone-tab';
  more.setAttribute('aria-haspopup', 'dialog');
  more.setAttribute('aria-expanded', 'false');
  more.setAttribute('aria-controls', 'phone-menu');
  more.innerHTML = `${ICON_MORE}<span class="phone-tab-label">More</span><span class="phone-tab-dot" hidden></span>`;
  tabbar.append(more);
  document.body.append(tabbar);

  // The More sheet: everything the bottom bar has no room for.
  document.body.insertAdjacentHTML('beforeend', `
    <div class="phone-menu-backdrop" id="phone-menu" hidden>
      <section class="phone-menu" role="dialog" aria-modal="true" aria-labelledby="phone-menu-title">
        <header class="phone-menu-head">
          <h2 class="phone-menu-title" id="phone-menu-title">More</h2>
          <button class="phone-menu-close" id="phone-menu-close" type="button" aria-label="Close">${ICON_CLOSE}</button>
        </header>
        <div class="phone-menu-body" id="phone-menu-body"></div>
      </section>
    </div>`);

  const menu = document.getElementById('phone-menu');
  const body = document.getElementById('phone-menu-body');
  let opener = null;

  const fillMenu = () => {
    const who = auth.account();
    body.replaceChildren();

    // You, at the top: who is signed in, and the way to the account itself.
    if (who) {
      const me = document.createElement('button');
      me.type = 'button';
      me.className = 'phone-menu-me';
      me.innerHTML = `<span class="account-avatar" aria-hidden="true"></span>
        <span class="phone-menu-me-text"><b></b><small></small></span>${ICON_CHEVRON}`;
      me.querySelector('.account-avatar').textContent = initialsOf(who);
      me.querySelector('b').textContent = who.name || who.email;
      me.querySelector('small').textContent = auth.roleLabel(who.role);
      me.setAttribute('aria-label', `${who.name || who.email}, ${auth.roleLabel(who.role)}: your account`);
      // The account panel takes over More's history entry, so Back from it
      // is back to the page, as from More.
      me.onclick = () => { closeMenu(false, { handOver: true }); openAccountPanel(); };
      body.append(me);
    }

    // The tabs this account's bar has no room for, first, with their icons.
    const moved = PHONE_TABS.filter((t) => t.orMore && !t.bar(who));
    if (moved.length) {
      const group = document.createElement('nav');
      group.className = 'drawer-group phone-menu-tabs';
      group.setAttribute('aria-label', 'From the bar');
      for (const tab of moved) {
        const a = document.createElement('a');
        a.className = 'drawer-link phone-menu-tab';
        a.href = tab.href;
        a.innerHTML = `${tab.icon}<span>${tab.label}</span>`;
        group.append(a);
      }
      body.append(group);
    }

    // The drawer's own groups, copied as they stand (badges included), so the
    // list of pages is written once, in account-drawer.js.
    for (const group of document.querySelectorAll('#account-panel .drawer-group')) {
      const copy = group.cloneNode(true);
      for (const node of [copy, ...copy.querySelectorAll('[id]')]) node.removeAttribute('id');
      copy.removeAttribute('aria-labelledby');
      const title = copy.querySelector('.drawer-group-title');
      if (title) copy.setAttribute('aria-label', title.textContent.trim());
      body.append(copy);
    }
    showLinksFor(body, who);
    // Not twice: a page the bar already has, or that heads this list (Changes,
    // for the owner and the lead), is dropped from the copy. A count it carried
    // goes with it to the head of the list.
    const tabbed = new Set(PHONE_TABS.filter((t) => t.bar(who) || t.orMore).map((t) => t.href));
    for (const a of body.querySelectorAll('.drawer-group:not(.phone-menu-tabs) a.drawer-link')) {
      const path = new URL(a.href, location.href).pathname;
      if (!tabbed.has(path)) continue;
      const head = body.querySelector(`.phone-menu-tabs a[href="${path}"]`);
      const badge = a.querySelector('.drawer-badge');
      if (head && badge) {
        head.append(badge);
        if (a.title) head.title = a.title;
        if (a.hasAttribute('aria-description')) head.setAttribute('aria-description', a.getAttribute('aria-description'));
      }
      a.hidden = true;
    }
    for (const group of body.querySelectorAll('.drawer-group:not(.phone-menu-tabs)')) {
      if (!group.querySelector('a.drawer-link:not([hidden])')) group.hidden = true;
    }

    // The package: its layers where the page has no layer tabs of its own,
    // and the flash-sale map, which has a button of its own in the desk chrome.
    const pkg = document.createElement('nav');
    pkg.className = 'drawer-group';
    const pkgTitle = layers ? 'The package, layer by layer' : 'In the package';
    pkg.setAttribute('aria-label', pkgTitle);
    pkg.innerHTML = `<h3 class="drawer-group-title">${pkgTitle}</h3>`;
    for (const [key, label] of layers ? LAYER_LINKS : []) {
      const a = document.createElement('a');
      a.className = 'drawer-link';
      a.href = `/?layer=${key}`;
      a.textContent = label;
      pkg.append(a);
    }
    const map = document.createElement('a');
    map.className = 'drawer-link';
    map.href = '/?layer=cicd&mode=cicd-burst';
    map.textContent = 'Deployment map';
    pkg.append(map);
    body.append(pkg);

    // Day or night, said as a choice between two rather than a toggle whose
    // state has to be guessed from the icon.
    const look = document.createElement('div');
    look.className = 'drawer-group phone-menu-look';
    look.innerHTML = `<h3 class="drawer-group-title" id="phone-look-title">Appearance</h3>
      <div class="phone-seg" role="group" aria-labelledby="phone-look-title">
        <button type="button" data-theme="dark">Night</button>
        <button type="button" data-theme="light">Day</button>
      </div>`;
    const paint = () => {
      for (const b of look.querySelectorAll('button')) {
        b.setAttribute('aria-pressed', String(b.dataset.theme === currentTheme()));
      }
    };
    for (const b of look.querySelectorAll('button')) {
      b.onclick = () => {
        if (b.dataset.theme !== currentTheme()) changeTheme(b.dataset.theme);
        paint();
      };
    }
    paint();
    body.append(look);

    // The page you are on, marked in the copy as in the drawer.
    for (const a of body.querySelectorAll('a.drawer-link')) {
      const url = new URL(a.href, location.href);
      if (url.pathname === location.pathname && !url.search) a.setAttribute('aria-current', 'page');
    }
  };

  function openMenu() {
    opener = document.activeElement;
    if (drawer && !document.getElementById('account-panel')) mountAccountDrawer();
    closeAccountPanel({ handOver: true });
    closeBellPanel();
    fillMenu();
    menu.hidden = false;
    // Back closes More (account-drawer.js holdSheet).
    holdSheet(() => closeMenu(true, { fromHistory: true }));
    more.setAttribute('aria-expanded', 'true');
    document.body.classList.add('phone-sheet-open');
    document.getElementById('phone-menu-close').focus();
  }
  function closeMenu(restore = true, { fromHistory = false, handOver = false } = {}) {
    if (menu.hidden) return;
    menu.hidden = true;
    releaseSheet({ fromHistory, handOver });
    more.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('phone-sheet-open');
    if (restore && opener && document.contains(opener)) opener.focus();
    opener = null;
  }
  more.onclick = () => (menu.hidden ? openMenu() : closeMenu());
  document.getElementById('phone-menu-close').onclick = () => closeMenu();
  menu.addEventListener('click', (e) => { if (e.target === menu) closeMenu(); });
  followFromSheet(menu);
  menu.addEventListener('keydown', (e) => {
    // The page's own keys (the viewer's Escape leaves for Home, Home's backs
    // out of the scene) must not see these.
    e.stopPropagation();
    if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
    // Focus stays inside the sheet while it is open.
    if (e.key !== 'Tab') return;
    const stops = [...menu.querySelectorAll('a[href], button:not([disabled])')].filter((n) => n.offsetParent);
    if (!stops.length) return;
    const first = stops[0];
    const last = stops[stops.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  // Turning the phone, or widening a window, past the breakpoint closes it.
  matchMedia('(min-width: 720px)').addEventListener('change', (q) => { if (q.matches) closeMenu(false); });

  // The tabs this account has, and where "you are here" points.
  const byRole = () => {
    const who = auth.account();
    let lit = false;
    for (const tab of PHONE_TABS) {
      const a = tabbar.querySelector(`[data-tab="${tab.key}"]`);
      a.hidden = !tab.bar(who);
      const here = tab.key === current && !a.hidden;
      a.classList.toggle('is-here', here && !ownPage);
      if (here && ownPage) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
      lit ||= here;
    }
    more.classList.toggle('is-here', !lit);
    if (!menu.hidden) fillMenu();
  };
  auth.onAuthChange(byRole);
  byRole();

  // While a text field has focus the keyboard is up, and the bar steps aside
  // so the field sits on the keyboard rather than behind the bar.
  const typing = () => {
    const at = document.activeElement;
    const on = Boolean(at?.matches?.(TYPING)) && !menu.contains(at);
    tabbar.style.display = on ? 'none' : '';
  };
  document.addEventListener('focusin', typing);
  document.addEventListener('focusout', () => setTimeout(typing, 0));

  // Unread release notes put a dot on More, since the bar's chip has no room on
  // a phone. Watched rather than asked: the chip arrives when its fetch does.
  const dot = more.querySelector('.phone-tab-dot');
  const notes = () => { dot.hidden = !document.getElementById('updates-new'); };
  if (watch) new MutationObserver(notes).observe(watch, { childList: true, subtree: true });
  notes();

  // The waiting count the drawer puts on Changes shows on the bar's Changes tab
  // too, for the accounts whose bar has it (for the owner and the lead it moves
  // with the link to the head of More instead). Mirrored, not fetched again: the
  // drawer owns the number, and it arrives when the drawer's fetch does.
  const changesTab = tabbar.querySelector('[data-tab="changes"]');
  const counts = () => {
    const link = document.getElementById('changes-link');
    const from = link?.querySelector('.drawer-badge');
    let mark = changesTab.querySelector('.phone-tab-count');
    if (!from) { mark?.remove(); changesTab.removeAttribute('aria-description'); return; }
    if (!mark) {
      mark = document.createElement('span');
      mark.className = 'phone-tab-count';
      mark.setAttribute('aria-hidden', 'true');
      changesTab.append(mark);
    }
    mark.textContent = from.textContent;
    if (link.hasAttribute('aria-description')) changesTab.setAttribute('aria-description', link.getAttribute('aria-description'));
  };
  const panelWatch = new MutationObserver(counts);
  const watchPanel = () => {
    const panel = document.getElementById('account-panel');
    if (!panel) return false;
    panelWatch.observe(panel, { childList: true, subtree: true, characterData: true });
    counts();
    return true;
  };
  // A page that mounts its drawer later (home, on the first More) is watched from then.
  if (!watchPanel()) {
    const late = new MutationObserver(() => { if (watchPanel()) late.disconnect(); });
    late.observe(document.body, { childList: true });
  }

  return { tabbar, openMenu, closeMenu };
}

function buildPhoneFrame(bar) {
  document.body.classList.add('has-phone-frame');

  // The app bar's start: the mark (a way home) and this page's name.
  const start = document.createElement('div');
  start.className = 'phone-bar-start';
  start.innerHTML = `
    <a class="phone-mark" href="/home.html" aria-label="ADAM home">
      <img src="/brand/adam-mark-night.svg" alt="" width="28" height="28" />
    </a>
    <span class="phone-title"></span>`;
  start.querySelector('.phone-title').textContent = pageTitle(bar);
  bar.prepend(start);

  mountPhoneBar({ watch: bar });
}

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
    <a id="decide-chip" class="chip" href="/decide" hidden
       title="Decide the change requests the watcher has drafted">Decide</a>
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

  // Decide, beside Tasks and Reviews, for the two roles that decide: on a desk
  // it was only in the account menu, one click deeper than the lead looked.
  // The server answers 403 to anyone else; this only keeps the chip from
  // offering a page that would refuse them.
  const decideChip = document.getElementById('decide-chip');
  const showDecide = () => { decideChip.hidden = !isDecider(auth.account()); };
  auth.onAuthChange(showDecide);
  showDecide();

  coverSafeAreas();
  buildPhoneFrame(bar);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', buildChrome, { once: true });
} else {
  buildChrome();
}
