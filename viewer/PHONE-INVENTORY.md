# ADAM pages on a phone: inventory

4 November 2026, read from the code (not a browser): every "breaks below 420px" is an inference to check with
screenshots. Companion to PHONE-SPEC.md section 5.

## Summary

- 26 files in viewer/public. Five (burst, canvas, platforms, uiux, uiux-boards) are redirect stubs with no viewport
  meta (e.g. uiux.html:13-25): they `location.replace('/?layer=...&mode=...')`, so they are views of index.html.
  validation.html forwards to reviews.html#coverage. That leaves 20 real pages.
- index.html (the viewer) already has a phone layout: 760px one column with off-canvas drawers (styles.css:2026),
  32px touch targets (styles.css:2336), a 380px bar fix (styles.css:2381), and touch.js pan and pinch on four canvases
  (graph, boxdiagram, statemachine, structure).
- The 16 standalone pages share the `.admin-bar` chrome: the right strip scrolls at 640px (layers.css:1723), the nine
  layer tabs hide at 720px (layers.css:3105). Sheet tables scroll sideways (sheet.css:218). The settings-style left nav
  becomes pills at 820px (layers.css:3050-3061).
- Worst gaps: home.html (hero, colophon and a panel fixed at 340px with no phone rule, home.css:458-463; wheel
  preventDefault at home.js:482); galaxy.js has no touch support and `.galaxy-field` is `touch-action: none`
  (layers.css:66); plan.html is a drag Gantt.

## Pages: route, who, layout, narrow behaviour

- **index.html `/`**: everyone signed in; Build owner-only, Decisions hidden from clients (lib/audience.mjs:132);
  audit route owner/admin (audience.mjs:64). Three chrome rows (layer rail, mode rail at index.html:254), tree left
  (:266), links right (:1053), about 30 views in main (:296-1040), canvases, galaxy views, UI/UX rail and detail
  (:830, :898, :923), iframes (app.js:3580, cicd.js:78), palette (:1076), account drawer, bell, mascot. Hover tooltips
  and Ctrl+K. Risks: galaxy views untouchable, iframes, body overflow-x hidden.
- **settings.html**: signed in; Administration tab hidden unless allowed (panels.js:16). set-nav pills, `.set-matrix`
  table (layers.css:3626, scroll unchecked), 820px rules (settings.html:53).
- **admin.html**: administrators (require_admin main.py:465; scopes and IP owner-only main.py:1004). Wide people table
  (about 9 columns) with inline role picker, invites, platform scopes, decisions; 820px forms full width
  (admin.css:119), 640px decisions (admin-decisions.css:96).
- **ips.html**: owner only (main.py:1091-1250). Row lists, not tables; 820px two-column rows (ips.css:101). Low risk.
- **plan.html**: owner only (main.py:7489). Names column plus time axis, ROW_H 38, zoom 28/8/3 px a day (plan.js:36),
  pointer drag with grips (plan.js:268-313), keyboard alternative (:315), confirm dialog (plan.html:126). Only the names
  column shrinks to 150px at 820px (plan.css:185); no touch-action; about 200px left for the axis at 360px.
- **tasks.html**: the delivery team, clients refused (tasks.js:3). Grouped rail, sprint hero, burn-up, Gantt strip,
  tables tk-daily, tk-fd, tk-people, person panel, hover tooltip (tasks.js:2820). Best covered: eight media blocks at
  1100/900/820/760 (tasks.css:301-855). Own CSS, no sheet.css.
- **board.html**: everyone signed in, own tickets (/api/board/mine). Gate meter cells 16-18px wide (board.css:119-131).
- **changes.html**: all signed in; settle link admin (changes.js:1468); overdue needs require_reader. Table of about 7
  columns, columns hide at 1100 and 820 (changes.css:184-194), four-textarea form.
- **reviews.html**: all signed in including clients (require_voice main.py:530). Coverage bars, filter bar, tables,
  respond form; 820px (reviews.css:93).
- **audit.html**: owner/admin only (audit.js:534). 13px check marks (audit.css:99), far below touch size; 860/600px rules.
- **costing.html**: read owner/admin/pm (require_reader main.py:4478, 4740); edit admin (costing.js:977 mayEdit).
  Chart, people and sprint tables, money forms; 820px (costing.css:88).
- **agents.html**: a developer sees their own, admin/pm the whole project (agents.js:15). Three groupings, bar chart,
  sessions table; 820px (agents.css:80).
- **domains.html**: signed in. Wide Reach table (about 24 column definitions), six parallel fetches;
  `(max-width:768px),(pointer:coarse)` and 860px (domains.css:59, :225).
- **document.html**: signed in; sections narrowed server-side. Checkboxes, markdown preview, print CSS; one 640px rule
  (document.css:63).
- **chat.html**: signed in, the caller's own model key (main.py:4097). Textarea, Enter sends (chat.js:357); 640px
  (chat.css:108). Separate from the mascot chat panel (chat-panel.js and mascot.js load only in index.html; the mascot
  dock hides under 900px, layers.css:3303).
- **updates.html**: signed in; release notes list with the mascot image; simple.
- **home.html**: signed in (home.js:526). Full-screen galaxy canvas, absolutely placed hero, colophon, rail and panel;
  needs a phone layout of its own.
- **landing.html** public: canvases, seven media rules (landing.css:257-338); responsive already.
- **login.html** public: collapses at 940px (login.css:348). **invite.html** public: 520px (invite.css:64). Both fine.
- Common to the 16 standalone pages: page-chrome.js:96 upgrades `header.admin-bar` with layer links, bell, the
  deployment-map link, home link, account button and theme toggle; `auth.requireSignIn()`. Sheet pages use
  sheet.css/js (`.sh-scope` filter bar, `confirmStep` inline confirm, not a modal).

## 1. Shared components, by how many pages use them

1. styles.css and layers.css: all 20 real pages.
2. theme.js: every real page.
3. admin-bar, page-chrome.js, the account drawer and the bell: about 15 standalone pages (the viewer has its own copy).
4. sheet.css and sheet.js: 12 pages link sheet.css, 8 import sheet.js, plus the viewer's sheet views.
5. panels.js and the set-nav rail: about 10 pages (admin, agents, audit, board, changes, costing, domains, reviews,
   settings, tasks).
6. validation.js as auth: all signed-in pages.
7. touch.js: the viewer only.
8. galaxy.js: home plus viewer views, no touch.
9. mascot and chat-panel: the viewer only.
10. auth.css: login, invite.

## 2. Phone batches

- **A. The chrome, once:** page-chrome, account drawer, bell, admin-bar (test at 360px).
- **B. Rail-and-sheet pages:** settings, admin, audit, agents, domains, costing, reviews, changes, board; fix the sheet
  table (cards below 600px, or a sticky first column), the filter bar and forms once.
- **C. Tasks** (own CSS, Gantt, roster), after B.
- **D. Simple lists and forms:** ips, chat, document, updates.
- **E. Public:** login, invite, landing (test only).
- **F. The viewer's canvas views** (touch for galaxy.js, the iframes).
- **G. Home:** its own phone layout.
- **H. Plan:** view only (below).

## 3. View-and-zoom only on a phone

plan.html (drag editing; keep keyboard and desktop editing); the viewer's canvas views (graph, structure, ER, states,
data, services graph, galaxy; node drag stays on desktop); the UI/UX wireframe iframes and boards, the flash-sale
simulator; the Tasks Gantt and burn-up; home.html as a tap list of the five layers instead of the 3D scene.

Column counts are rough, from a grep of `{ key, label }` definitions.
