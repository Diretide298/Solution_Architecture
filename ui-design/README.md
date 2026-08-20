# Handoff: Atlas — viewer UI redesign

## Overview
A redesign of the TICVAI viewer — the local browser for the delivery package (contracts, screens,
flows, state models, migrations). Two files, one design: a **day** theme and a **night** theme of
the same layout, content and component set. The nav moved from a vertical rail to a **two-row top
bar**, and the body dropped to three columns.

Brand: the product is **Atlas — the context layer for AI-assisted development**. The header carries
the Atlas lockup (mark + wordmark) as a single image; the foot of the left column carries a
**Powered by AinfiniteCore** lockup with the **Softlabs Group** logo beside it.

## About the design files
`designs/` holds two self-contained HTML pages — **design references, not production code**.
Open either in a browser to see the target. Recreate them inside the viewer's existing
environment: `viewer/public/index.html` + `styles.css` / `layers.css` with vanilla ES modules
(`app.js`). Keep that architecture. Translate the two themes into one set of CSS custom
properties on `:root` with a `[data-theme="night"]` override — the existing `theme.js` already
owns the toggle — and reuse the current class names (`.app`, `.topbar`, `.sidebar-left`,
`.sidebar-right`, `.main`, `.view`, `.graph-toolbar`, `.tree`, `.links-pane`, `.palette`) rather
than introducing a framework.

- `Viewer Redesign - Topbar.dc.html` — day theme
- `Viewer Redesign - Topbar Night.dc.html` — night theme

## Fidelity
**High fidelity.** Final colors, type, spacing, radii, shadows and hover/active treatments.
Content is real content from the delivery package (screen WEB-002, contract satellite/fnb,
Order state model, flow F01), so copy can be lifted verbatim. Recreate pixel-close.

## Layout — the shell

Full viewport height, `min-width:1180px`, `overflow-x:auto`. Desktop-only by intent: below
1180px the page scrolls horizontally rather than crushing the main column.

**Row 1 — dark chrome bar, 64px.** `padding:0 22px`, `display:flex; align-items:center; gap:20px`.
- Brand: the Atlas lockup as one image, `height:46px; width:auto`. Two files, one per theme —
  `brand/atlas-lockup-day.png` on the day chrome, `brand/atlas-lockup-night.png` on the night
  chrome. Both are background-keyed to transparent, so they sit on any dark surface. No typeset
  wordmark and no tagline in the bar: the lockup carries the name, and the tagline lives in the
  image `alt`.
- 1px × 26px divider at 13% white.
- **Layer switch** — a segmented pill tray (`radius:11px`, 4px padding, tray one step darker than
  the bar). Each item `padding:8px 14px; radius:8px; 13px/600` with a mono count at 70% opacity.
  Active = teal gradient pill, white text, `0 4px 12px` teal glow.
- Spacer, then the search field: `flex:0 1 210px; radius:11px`, mid-dark fill + 1px border,
  13px text, circle glyph, `⌘K` kbd chip.
- Status dot (7px teal, 4px halo) + user block (name 12.5px/700, role 9.5px/600 uppercase,
  right-aligned) + 32px avatar with the teal gradient.

**Row 2 — dark tab bar, 52px.** Same dark family, one step lighter than row 1, 1px bottom border.
- **View tabs** — full-height items, `padding:0 14px; 13.5px/600`, each with a small mono kbd
  hint chip. Active = white text + a 2.5px bright-teal bottom border; idle = muted grey → white
  on hover. The tab set changes with the layer (see *Views by layer*).
- Right side: the layer's summary line (11.5px/600 muted), a 1px × 22px divider, then per-view
  **toggle buttons** (`padding:7px 12px; radius:9px; 12px/600`) — dark fill when off, deep-teal
  fill with light-teal text when on.

**Body — three columns:** `grid-template-columns: 272px minmax(440px,1fr) 296px`.

**Column A — list panel.** Head block (`padding:15px 15px 12px`, 1px bottom divider): a 3-way
grouping segmented control in a `radius:10px` tray (active segment = card-surface pill with a
`0 1px 3px` shadow), then a filter input (`radius:10px`, card fill + 1px border, circle glyph).
Below it a **warm advisory note** (`radius:11px`, warm fill + warm border, 11.5px/1.55) whose text
changes per layer. Then the scrollable list, grouped: each group has a 7px square tone chip, a
9.5px/700 letter-spacing-.13em uppercase title, and a mono count; rows are `padding:8px 11px;
radius:9px` with a fixed 54px mono id column, a 13px ellipsized name, and a mono meta value on the
right. Active row = teal tint fill, teal text, weight 700. Pinned at the foot: the **Powered by
AinfiniteCore** strip on a dark band — two overlapping 14px rings (light teal over deep teal) as
the mark, an 8.5px/700 letter-spacing-.16em "POWERED BY" label, and the wordmark 12.5px/700 with
"Core" in teal.

**Column B — main.** Sticky title bar on the panel surface (`padding:14px 24px`, wraps): title
`flex:1 1 250px` — h1 20px/800/-0.02em over a 12.5px/500 muted subline — then the meta chip row
(`padding:6px 11px; radius:9px`, card fill + 1px border; a 9.5px uppercase key + 11.5px/600 value).
Body scrolls: `padding:18px 24px 36px; display:flex; flex-direction:column; gap:16px`.

**Column C — links pane.** Head `padding:18px 19px 14px`, `LINKS` 12px/700 letter-spacing .12em
uppercase + an 11px/600 muted caption. Body groups (gap 21px): a 10px/700 uppercase title, a
hairline rule filling the remaining width, and a plain mono count; empty groups render a 12.5px
muted sentence; item rows `padding:9px 11px; radius:10px` on the card surface with a 1px border,
mono id + 12.5px/600 name + 10px/700 tag, hover = teal border and teal-tinted fill.

## Views

Switching a layer swaps the view tabs, the grouping control, the list content, the advisory note,
the summary line and the toggle set together.

### Views by layer
| Layer | Views | Grouping | Toggles (per view) |
|---|---|---|---|
| Frontend | Screen, Journey, Apps, Waves, Audit | Platforms / Modules / Waves | Screen: Notes, Wireframe · Journey: Branches, Operations |
| Contracts | Graph, Structure, ER, Lineage, Reader, Audit | Contracts / Modules / Platforms | Graph: Labels, Shared $refs · ER: Fields, Enums |
| Domain | States, Events, Audit | Entities / Contexts / Events | States: Guards, Reversals |
| Backend | Services, Data, Migrations, Routing, Audit | Services / Tables / Waves | — |
| Decisions | Register, Audit | Register / Themes / Waves | — |

Five views are built out: **Screen**, **Journey**, **Graph**, **ER**, **States**. The rest swap
their sidebar and header but have no body yet.

### Frontend → Screen
Three cards in an auto-fit grid (`minmax(350px,1fr)`), all `radius:15px`, 1px border,
`0 1px 2px` shadow, with a filled header strip and a wrapping header row (wrapping is required —
badges clip otherwise).
- **Layout** — header `Layout` 15px/700 + `contentBody · 4 components` + a `REGION` badge (teal
  tint, 11px/700 letter-spacing .1em, radius 7px). Rows separated by 1px dashed dividers: component
  kind in mono 12.5px teal, label 13.5px/600, a mono binding chip on teal tint, and a 12.5px/1.5
  muted note capped at 52ch. Components: searchField / multiSelect Category / datePicker Date /
  cardList Results.
- **States** — 4 rows, `padding:12px 14px; radius:11px`, subtle fill + 1px border,
  `grid-template-columns: 7px minmax(0,1fr)` where the 7px pill carries the state's tone:
  loading (teal), empty (amber), error (red), offline (neutral, "not required here").
- **Reaches** — a `FINDING` badge (warm tint) and the finding text at 12.5px/1.6.
- **Deployment** — `repeat(auto-fit,minmax(148px,1fr))` tiles, `padding:13px 14px; radius:11px`;
  9.5px uppercase key over a 13px/600 value. Eight keys: runs on, ships by, hosted, updates,
  cadence, network, device, store review.

### Frontend → Journey
A brief card with two blocks — **Trigger** and **Offline — cannot start** (the second labelled in
the warm tone) — each a 9.5px/700 uppercase label over 13px/1.6 body text at 88ch. Then a
horizontally scrolling step rail: 258px cards (`radius:13px`) each with a 21px teal-tint step
number, mono screen id, platform tag, a 14px/700 name over a 12.5px muted action line, its
operations as mono chips with a 5px teal dot, and a 12px outcome line prefixed "→"; a 32px "→"
sits between cards. Below it a **Branches** card: `repeat(auto-fit,minmax(300px,1fr))` items with a
4px teal spine, a 13px/700 title, 12.5px body, a `RECOVERABLE` badge and a mono "resolved by" note.

### Contracts → Graph
Toolbar: a 5-way segmented tray (Spine / Files / Schemas / Permissions / Local), the count line,
and a **Fit** button. Canvas 520px tall, `radius:15px`, dotted background
(`radial-gradient(<dot> 1px, transparent 1px)`, `background-size:22px 22px`).
- **Nodes** are percent-positioned, `translate(-50%,-50%)`, a circle sized 11–26px by operation
  count over an 11px/600 label. Tier colors: **spine** deep teal, **satellite** bright teal,
  **shared** amber with a soft amber halo. 24 contracts.
- **Edges** are ONE SVG overlay, not rotated divs:
  `<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0">` with
  `<line>` elements in the same 0–100 space the nodes use, `vector-effect="non-scaling-stroke"`.
  This is the load-bearing detail — a px-based edge layer drifts out of the panel at other widths.
  Amber lines (opacity .75) are events with a critical consumer; neutral lines (opacity .5) are
  ordinary event links. 22 edges.
- Floating legend, bottom-left: translucent card, 9px dots + 11.5px labels, and a closing
  "dot size is the operation count · hover a contract to isolate its events".

### Contracts → ER
Toolbar: contract picker, count line, **Fit**. Canvas is the same dotted surface, padded 20px, with
entity boxes in `repeat(auto-fill,minmax(212px,1fr))`. Each box `radius:11px`, 1px border, a
9px/12px header (6px dot + 12.5px/700 name + mono field count) and field rows `padding:4px 12px`:
mono 11px field name, a dotted leader filling the gap, and a mono 10.5px type on the right. Key
fields are teal and 700. Three box kinds, each with its own border / header fill / dot:
**own entity** (teal), **enum** (violet), **entity from another contract** (amber).
A legend bar sits under the canvas with "click a field to follow its $ref · drag a box to pin it".

### Domain → States
Toolbar: model picker, count line, **Fit**. Canvas 480px, dotted.
- **State nodes**: percent-positioned cards, `padding:9px 16px; radius:10px`, 1.6px border,
  `0 2px 6px` shadow — border teal for the initial state, violet for terminal states, neutral
  otherwise; an optional 9px uppercase `OFFLINE` sub-label.
- **Transitions**: the same SVG overlay technique. Neutral solid = an operation moves it;
  teal dashed (`5 4`) = a timer or job; amber solid = a reversal.
- **Labels** are computed at each line's midpoint (never hand-placed), 11px/600 on a translucent
  chip so they stay legible over the dots.
- Legend bottom-left, plus a **Note** card below the canvas carrying the `DEFECT` badge and the
  `held → refunded is not a transition` finding.

## Interactions & behavior
- Layer / view / grouping / list-row / toggle selections are live state. In the real app these map
  to the existing `app.js` layer + view routing and the URL hash node id.
- Hover: chrome nav items go to white; list rows take a tinted fill; link pills and links-pane rows
  take a teal border; buttons brighten their border.
- The list column and the links pane scroll independently; the powered-by strip stays pinned.
- Loading / empty / error in the Screen view are content states **of the screen being inspected**,
  not of the viewer.
- Responsive: none below 1180px by intent. Optional improvement: collapse the links pane first,
  then the list column.

## State management
`{ layer, view, grouping, screen, graphTab, toggles:{…} }`. All of it already exists in `app.js`
(layer/view routing, sidebar grouping, selection, per-view toggles) — the redesign adds no new
state. Note that switching a layer must also reset `view` to that layer's first view, and
`grouping` to its first grouping, or the UI lands on a view the layer does not have.

## Design tokens

Same structure in both themes; only the values change. Roles: chrome-1 · chrome-2 · chrome-fill ·
chrome-border · chrome-text · chrome-muted · canvas · panel · card · border · divider · subtle-fill ·
text · muted · faint · accent · accent-bright · accent-tint · accent-text.

| Role | Day | Night |
|---|---|---|
| chrome row 1 | #333333 | #111111 |
| chrome row 2 | #3A3A3A | #333333 |
| chrome fill (inputs, off toggles) | #4A4A4A | #2E2E2E |
| chrome border | #565656 | #3A3A3A |
| chrome text / muted | #F7F7F7 / #ADADAD | #EDEDED / #9A9A9A |
| canvas | #F5F5F5 | #1A1A1A |
| panel (columns, title bars) | #FFFFFF | #1F1F1F |
| card | #FFFFFF | #242424 |
| card header strip | #F0F0F0 | #2C2C2C |
| subtle fill (tiles, state rows) | #FAFAFA | #202020 |
| border | #E4E4E4 | #3A3A3A |
| divider | #F0F0F0 | #333333 |
| text | #2E2E2E | #EDEDED |
| muted / faint | #6E6E6E / #8A8A8A | #9A9A9A / #787878 |
| accent | #229799 | #2BB3B0 |
| accent bright | #48CFCB | #48CFCB |
| accent tint | #E5F7F6 | #123A3A |
| accent text | #1C7E80 | #48CFCB |
| accent tint border | #A6E6E4 | #2C7C7D |
| warm note fill / border / text | #FBF6EC / #EADFC8 / #7A6534 | #2B2418 / #463A24 / #D9BC7C |
| finding badge | #F1EDE3 / #9A5A2A | #2B2418 / #D99A5E |
| amber signal | #C08A2E | #D9A143 |
| red signal | #C0564F | #D96C63 |
| dot grid | #E2E2E2 | #333333 |
| card shadow | `0 1px 2px rgba(66,66,66,.06)` | `0 1px 2px rgba(0,0,0,.06)` |

Diagram tiers (both themes): spine = accent, satellite = accent-bright, shared = amber,
enum = #7C5FC0, external entity = amber, ordinary edge = neutral muted.
The night theme brightens the teal deliberately — the day #229799 loses too much contrast on black.

Typography: **Plus Jakarta Sans** 400/500/600/700/800 for UI, **JetBrains Mono** 400/500 for ids,
kinds, types, counts and kbd chips. Scale: 21 / 20 / 15 / 14.5 / 14 / 13.5 / 13 / 12.5 / 11.5 /
11 / 10.5 / 10 / 9.5 / 9 / 8.5px. Small-caps meta labels: 8.5–10px, 700, letter-spacing .10–.16em,
uppercase.

Radii: 15 (cards) · 13 (journey step) · 12 (tiles) · 11 (rows, notes, tray) · 10 (buttons, link
rows) · 9 (chips, toggles) · 8 (tray segments) · 7 (badges, step number) · 5 (kbd).
Spacing: 4 / 6 / 8 / 9 / 10 / 11 / 13 / 14 / 15 / 16 / 18 / 19 / 20 / 22 / 24 px.
Scrollbars: 10px, palette-neutral thumb, 3px transparent border, `background-clip:content-box`.

## Assets
`assets/brand/` — the Atlas identity.
- `atlas-lockup-day.png` / `atlas-lockup-night.png` — the header lockups, transparent background.
  These are the two files the viewer actually loads.
- `atlas-mark.png` — mark only, transparent, for favicons, avatars and tight spaces.
- `atlas-logo-light.svg` / `atlas-logo-night.svg` — a redrawn vector lockup (mark as geometry,
  wordmark as text in Montserrat Light, tagline in Montserrat Medium). Useful when the logo has to
  scale past raster limits — print, large display. The text is live text referencing Montserrat by
  name, so outline it before sending anywhere the font is not installed.
- `atlas-mark-light.svg` / `atlas-mark-night.svg` — the vector mark alone.
- `assets/softlabs-logo.webp` — partner logo, rendered white via `filter:brightness(0) invert(1)`
  in the powered-by strip. A true white SVG/PNG would be crisper; swap when available.
- The AinfiniteCore mark is **CSS, not an asset**: two 14px overlapping bordered circles
  (light teal over deep teal, `margin-left:-5px` on the second).
- Fonts from Google Fonts. No other imagery; all icon glyphs are CSS shapes, as in the current viewer.

## Not covered yet
Structure, Lineage, Reader, Events, Apps, Waves, Audit, Data, Migrations, Routing, the Decision
register, the command palette, and the account / bell dialogs still carry the old styling. The
tokens above are enough to restyle them. The canvas renderers (`graph.js`, `boxdiagram.js`,
`statemachine.js`) should read their palette from the CSS custom properties rather than literals,
so the day/night toggle reaches them too.
