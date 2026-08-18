# Viewer — UX, views, and accounts

Written 17 August 2026, after walking every layer × view and photographing each
one. Findings below are from the screenshots, not from memory: where a view is
called broken, the break is visible.

Ordered by how much it costs to leave alone, not by how hard it is to fix.

**How the view findings were verified.** Every screenshot observation was then
root-caused in the source by one agent and attacked by a second whose only job
was to refute it — check the anchor exists, look for a comment showing the
behaviour is deliberate, find a simpler cause, and ask whether the proposed fix
would actually change what the screenshot showed. Seven findings, fourteen
agents. **Five survived, one was corrected, and one was refuted outright.**
Anchors below are the surviving ones; `file:line` references have been checked.

---

## 0. Done

- **The verdict submit button reads `Submit`.** It used to grow and shrink as
  you picked (`Record "Needs work"`), which is movement that says nothing — the
  chosen chip is already lit and named. `verdict-submit-check.mjs` updated to
  match.

---

## 1. A reviewer cannot see their own progress

The single biggest gap. 364 screens, 278 tables, 737 operations, and **every row
in the tree looks identical**. Nothing says which are approved, which need work,
which nobody has opened. Finding the next unreviewed artefact means clicking
until one has an empty VALIDATION block.

Everything needed already exists — `GET /api/verdicts` returns every row for
every artefact in one call.

- **A verdict dot on each tree row** — green / amber / red / hollow for
  untouched. Screen rows are built at `public/app.js:1316-1320` as code + name +
  api-count; this is a fourth span and a lookup.
- **A progress line on each group head** — `29 screens · 11 approved · 3 need
  work · 15 untouched`. A group should say whether it is worth opening.
- **A filter row above the tree** — `All / Untouched / Needs work / Mine`.
  "Untouched" alone turns the review from a hunt into a queue.

## 2. The review loop has no rhythm

Read → judge → next. Today "next" means aiming at a 24px row. Single letters are
all spent on modes (`app.js:7109-7136` — `j` is journey, `w` is screen, `e` is
ER); `[`, `]`, `n` and the arrows are free.

- `]` / `[` — next / previous item in the current tree
- `n` — **next unreviewed**, the one that matters
- `1` `2` `3` inside a verdict form — pick approve / needs-work / reject
- `Ctrl+Enter` — submit

## 3. The verdict form is buried

On WEB-001 you scroll past a preview, an implementation table and three history
rows before you can act, and by then the thing you are judging is off-screen.
Make it a **pinned action bar** at the foot of the reader pane, note field
expanding on focus. History stays where it is.

## 4. The LINKS rail is 300px wide and mostly empty

Two items, then ~800px of nothing, on nearly every view.

- **Move the verdict form into it.** The rail becomes "what this connects to,
  and what you think of it", and the reader column gets its width back.
- Failing that, collapse it to a strip when it holds fewer than ~4 items.

---

# The views

Twenty layer × view combinations, all photographed. Each finding below was then
root-caused in the source by one agent and attacked by a second whose job was to
refute it. Anchors are the surviving ones.

**Four of my screenshot readings were wrong.** They are marked ✗ and kept, not
deleted — a refuted finding is worth as much as a confirmed one, and deleting it
invites someone to rediscover it.

## Works, leave alone

| View | Why it works |
|---|---|
| **Contracts › Lineage** | Headline number, honest prose about what `0 unresolved` does and does not mean, provenance of both sources, grouped by contract with counts. The best page in the app. |
| **Domain › States** | Initial/terminal colour, guard ticks, dashed for timer-driven, orange for reversals, and a NOTE naming the defect the file exists to catch. The best diagram. |
| **Backend › Migrations** | Stat tiles then migration cards in apply order, each naming its tables. Reads in one pass. |
| **Frontend › Waves** | "What ships when", unbuildable screens in red. Answers its question directly. |
| **Contracts › Audit** | Severity chips, rule tag per row, file:line. Nothing to add but grouping. |

## Broken — where the view and the data disagree

### Contracts › Graph — the arrowheads are painted the background colour

✗ **The ring half of my reading was wrong.** The rings *are* drawn.
`renderSpine()` (`app.js:1672`, placement `1700-1761`) switches the force layout
off and places every contract by tier — shared at r=62, spine at `SPINE_RING`
=215, satellite at `SATELLITE_RING`=395 — then passes `{ placed: true }`, which
`setData` honours (`graph.js:113` seeds from the caller's coordinates,
`graph.js:162` sets `alpha=0` so the simulation never runs). Measuring node
centres in the committed capture `manual/shots/10-graph-spine.png`: **all 8 spine
dots at r=236-238, all 14 satellites at r=433-435**, about a common centre. Two
exact circles. They are simply large, undrawn as guides, and easy to misread.

✅ **The arrowheads are a real bug, and a subtle one.** They are drawn and then
painted invisible. `draw()` wraps the edge stroke in `ctx.save()`/`ctx.restore()`
(`graph.js:473-493`), and the arrowhead block that follows does
`ctx.fillStyle = ctx.strokeStyle` at **`graph.js:502` — after the restore**. The
restored `strokeStyle` is whatever the last frame left behind, which is the label
halo set outside any save at `graph.js:551`: the background colour.

Verified numerically rather than by eye. In `10-graph-spine.png` the background
is exactly `(20,20,26)`, an edge body is `(187,144,33)`, and the notch at the
target rim is `(45,39,27)` — precisely `rgba(20,20,26,.85)` composited over the
edge. The arrowheads are there, in background paint.

The same idiom in `boxdiagram.js:572` works, because nothing restores the context
between its stroke and its fill.

**Fix:** hoist the edge colour into a local before `ctx.save()` and use it for
both stroke and fill. Do *not* instead move the fill above `restore()` — it would
inherit the `shadowBlur` set for active links at `graph.js:475-476`. Separately,
wrap the label block at `graph.js:551` in its own save/restore; that removes the
whole class of bug rather than this one instance.

**Risk:** only the spine view passes `directed: true`, so nothing else changes.
But shared-`$ref` edges are also directed and carry `rgba(255,255,255,.07)` —
their arrowheads will become faintly visible for the first time. And
`manual/shots/10-graph-spine*.png` bake the current look into the PDF manual, so
those captures go stale.

*Still open and unexamined: 46 edges over 27 nodes with no bundling, labels
colliding with their dots, and the legend box floating over the diagram.*

### Backend › Data — the green never appears because the column is gone

✅ Confirmed, and the cause is upstream of the viewer. `buildSchemaMap` colours
each box `module.written ? '#34d399' : '#fbbf24'` (**`app.js:4157`**), and
`module.written` is derived only from the Modules sheet's `Status` text
(`lib/backend.mjs:529`). **The current workbook has no Status column on the
Modules sheet**, and the header reader treats an absent optional column as blank
by design (`backend.mjs:44-47`). So all 21 modules get `written: false` and every
box renders amber — silently, with no warning anywhere.

The fact the view exists to show is already on the objects the function loops
over: `table.ddl`, set from the parsed `.sql`. The single-schema view
(`app.js:4245`) and the sidebar note (`app.js:2099`) both use it correctly.

**Fix:** stop reading `module.written`; count DDL per module in the pass the
function already makes over `backend.tables` (`app.js:4145-4149`). And binary
green/amber would still be wrong — only `pii` is 4/4; `platform` is 13/19,
`identity` 10/14, five modules 2-4, and **13 modules are 0**. It needs three
states: written, partial, none.

*Still open: 70 relationships drawn as near-invisible dashed grey with no
direction, and the per-line column counts at ~5px.*

### Frontend › Apps — two apps look duplicated

✅ Confirmed as a **data** problem, and traced to a specific commit.

On 17 August the app manifests in `frontend/` were regenerated under
operator-based names — `guest` → `guest-app`, `employee` → `venue-staff-app`,
`backoffice` → `venue-management-web`, `web-b2c` → `guest-web`, and six more.
**The ten pre-rename files were never deleted.** `frontend/` now holds 20
committed manifests where `frontend/README.md` declares ten.

`readApps()` (`lib/journeys.mjs:433-503`) reads every YAML in `frontend/` and
pushes one entry per file with an `app:` key (`:442`), with no check that any
`screens/*.yaml` actually claims that name — so each renamed app is emitted
twice, and the sort by descending screen count puts the identical twins side by
side. `guest.yaml` and `guest-app.yaml` have **byte-identical** screen-id and
route lists (76 each, byWave 20/39/17); they differ only in the new
`operator`/`directions` keys, one extra contract, and the component path prefix.

This inflates the header: **"20 apps · 12 scaffolded · 711 screens assigned"**
should read 10 apps / 364 screens.

The commit is **`d664719`** — the one where `git add -A` swept in the dump. It
added ten manifests and deleted none.

**Fix, data first.** Delete the ten stale manifests (`accreditation`,
`backoffice`, `employee`, `guest`, `partner-portal`, `platform-admin`, `pos`,
`scanner`, `support-console`, `web-b2c`). **Check before deleting:** the old
names are *not* confined to frozen snapshots — `repos/ticvai-frontend/apps/`
still holds directories under six of them, and `KNOWN_APPS`
(`lib/consumers.mjs:28-29`) hardcodes those names as "the canonical platform
roster". Renaming the manifests without reconciling that list will break the
consumers view.

**Then close the gap that let it happen silently.** `readApps()`'s own comment
(`:429-432`) says "the check worth making here is whether the two still agree",
but only the manifest→screens direction is implemented (`app-unknown-screen`,
`:460`). Add the reverse: a warning for any manifest whose `app:` no
`screens/*.yaml` claims. Identical screen ids mean `app-unknown-screen` never
fires, which is exactly why this was invisible.

**UI issue regardless:** each card's wave bar is normalised to its own width, so
app A's W1 cannot be compared to app B's W1. A bar that cannot be compared across
cards is not a bar. Share the scale.

## Wrong at the edges

### Contracts › ER — three of four confirmed, one refuted

Three sub-claims trace to one function: `BoxDiagram.fit()`
(**`boxdiagram.js:372-392`**), the only thing that sets the ER opening transform
(`app.js:1009`).

- ✅ **Unreadable fields.** `fit()` picks `k` purely to make the extent fit, so a
  42-entity contract lands at k≈0.45-0.55. At that k, `textSize(10, k, 6)` is
  pinned at its **6px floor** (`boxdiagram.js:31`) while the row-draw gate only
  suppresses rows below k<0.42 (`:668`). Text is drawn at a size it cannot be
  read at. Give `fit()` a legibility floor, not just an extent ceiling — a
  42-box contract cannot be both complete and readable on one screen, so pick.
- ✅ **Top row clipped.** `fit()` reserves `LEGEND_H = 96` for the bottom legend
  and then shifts content up by *another* `LEGEND_H/2` (`:390`). **Nothing
  reserves anything at the top**, where `.graph-toolbar` sits `position:absolute;
  top:0` over a canvas at `inset:0`. When height binds, the content's top edge
  lands ~30·k px (≈13px) down, under a ~40px toolbar. Measure the toolbar and
  subtract it; centre in the *visible* band.
- ✅ **Uniform grey edges** — but the renderer is not the gap. `drawEdge` already
  supports per-edge `kind` weighting and `dashed`; **`buildER`
  (`app.js:2184-2189`) emits only `{source, target, label}`** and sets neither.
  Only the Data view populates them. Cardinality should be carried explicitly
  and drawn as a glyph, which stays legible small — the full label is gated at
  k>0.8 and so never draws at fit zoom.
- ✗ **"+7 more" not expandable — wrong.** `foldAt()` hit-tests exactly that line
  and `toggleFold()` (`boxdiagram.js:446-477`) opens the box in place, growing
  downward, holding the header still, keeping the open set by id so it survives
  relayout. Wired for mouse *and* tap. **The real defect is discoverability:**
  the ER hint (`app.js:2222`) advertises "click a field to follow its $ref · drag
  a box to pin it" and never mentions the fold. Add it to the hint string.

Two framing gaps found alongside: the `er-scope` change handler
(`app.js:6897-6901`) re-renders but never re-fits, so switching contracts keeps
the previous scope's transform; and when `renderER` returns early to await
`ensureERDetail`, the `fit()` at `app.js:1009` runs against an empty diagram.

### Frontend › Journey — real, but there is no fit to fix

✅ The clipping reproduces exactly, including "Date & Session Selecti" and "The
session sells out bet", in the committed `manual/shots/21-journey.png`.

✗ But my diagnosis was wrong. **Journey has no Fit control at all**
(`index.html:195-210` has only the Branches and Operations checkboxes). The
sideways track is designed: fixed 268px columns, `min-width: min-content` inside
an `overflow:auto` body (`styles.css:596-604`), panned by `enableDragScroll` and
advertised in its own hint as "drag to pan".

So there is nothing to repair — only to choose. Options, cheapest last:
a fade or chevron on the right edge of `.journey-body` so the first impression
reads *"there is more"* rather than *"the page is broken"*; a fit-to-width that
CSS-scales `.journey-track` (the pattern already exists in `frameStage`,
`app.js:2644-2656`, negative-margin correction included); or a vertical track.

### Backend › Routing
- The **legend is cut off below the fold**. A chart's key must not require a
  scroll.
- **Red = "primary (write)"** on a traffic-light palette. Red reads as *error*.
  Recolour to a sequential or categorical ramp with no danger connotation.
- The ADR quote is truncated: *"…named the cost plainly:"* — colon, then nothing.

### Decisions › Decisions — one confirmed, one right for the wrong reason

- ✅ **Doubled IDs.** `lib/decisions.mjs:173` extracts the title with
  `/^#\s*ADR-\d+:\s*(.+)$/im` and falls back to `/^#\s*(.+)$/m`. ADR-0001..0015
  write the heading with a **colon** so the id is stripped; ADR-0016..0019
  switched to an **em dash**, the colon regex misses, and the fallback captures
  the whole heading including the id. `app.js:5148` then prints an `ADR-${id}`
  badge next to it. Same doubling in the tree at `app.js:1162`.
  **Fix at the parse site, not in `app.js`** — both render sites concatenate:
  `/^#\s*(?:ADR-\d+\s*[:—–-]\s*)?(.+)$/im`, through the existing `strip()`.
- ✗ **"Truncated at a colon" — symptom right, mechanism wrong.** Nothing cuts on
  a colon. `lead()` (`decisions.mjs:69-73`) splits on blank lines and returns the
  first block that isn't a heading, quote or list; `backend.mjs:401-406` does the
  same. Both stop at the end of the **first prose paragraph**. ADR-0012's
  Decision opens with the lead-in "TICVAI builds:" whose payload is the numbered
  list in the *next* block; ADR-0016's Context opens with a sentence whose
  payload is the `>` blockquote in the next block. The 400-char cap is nowhere
  near hit — both strings are under 80 characters.
  **Fix:** when the chosen paragraph ends in `:`, append the next block with its
  markers flattened — drop `>` from a blockquote, join list items with `; ` —
  then apply the cap. Both extractors need it.
- Status vocabulary is mixed: `part`, `Accepted`, `Decided`.

### Contracts › Structure
- Empty state on load — a 1340×950 canvas saying "Select a contract to diagram
  its structure", **with the legend still drawn** for a diagram that isn't
  there, and a fully populated toolbar (Tree/Nested, filter, Fields, $ref links,
  Expand all, Collapse, Fit) driving nothing.
- Fix: hide the legend and disable the toolbar until something is selected, and
  make the empty state a list of contracts you can click.

## Cross-cutting

1. ✅ **The LINKS rail goes stale — and it is worse than I said.**
   `fillSidePane()` (**`app.js:5409-5419`**) dispatches per layer — frontend
   `:5410`, backend `:5411`, domain `:5414-5416` — and each of those renderers
   clears the pane first. The tail is
   `const node = …; if (node) renderLinksPane(node);` **with no `else`**, and
   `renderLinksPane` clears only at its own top. `setLayer()` (`:625`) calls
   `renderSidePane()` but never touches `state.selectedId`, which is only ever
   assigned at `:195` and inside `select()` at `:1042`. So a reader who has never
   selected a contract keeps `selectedId === null` and the fallback is a **pure
   no-op, forever**. One shared `#links-pane` exists, so whatever Frontend left
   is what stays.

   ✗ **Correction to my reading:** "Decisions resets correctly" is false.
   Decisions has no dispatch either — the `Select a table.` seen there is the
   *leaked Backend empty state* from `renderTableLinks:5522`. So this is not a
   Contracts-branch bug; it is **every layer without a dispatch line**, and
   cross-cutting bugs 1 and 2 here are one bug, not two.

   The nearby comment (`:5412-5413`) is the author special-casing Domain *to
   avoid exactly this staleness* — evidence the fall-through is an oversight.
   **Fix:** clear before the dispatch, not before the `if (node)`, so
   `renderStateLinks`'s own early return at `:3518` (which returns *before* its
   clear at `:3519`) is covered too. Keep the `pane-empty` class — `syncLinksToggle`
   counts a child as "filled" only if it lacks it, so the phone toggle stays right.
2. **Legend boxes float bottom-left over live content** on Graph, Structure, ER,
   States and Data. Dock them, or make them dismissible.
3. ✗ **"Canvas views don't fit on load" — wrong, and instructive.** States
   *already* fits on first draw: `machine.resize(); machine.fit();` runs at
   `app.js:1019-1024` when the view is shown and `:3490-3491` on every data
   change, and the Fit button at `:6886` is **literally the same pair** — it
   cannot produce a different frame. Nor is the machine in the lower-right:
   `toScreen()` re-derives from `width/2, height/2` every draw, so it cannot
   drift without a user drag.

   What I photographed is the **deliberate zoom cap** at `statemachine.js:205`
   (`Math.min(…, 1.1)`), whose comment explains it: blowing a small machine up to
   fill the screen collides its guard labels. The 9-state order machine is
   529×274 world units, so at k=1.1 it uses ~582×302 of a ~1040×950 canvas.

   So the change, if wanted, is a **judgement about the cap**, not a missing
   call: derive the ceiling from what it protects (comfortable box height) rather
   than a flat 1.1. Worth noting `LEGEND_H` is hard-coded 96 while the real
   legend is ~190px tall, and the same `LEGEND_H`/cap pattern is duplicated in
   `boxdiagram.js:382-387` (cap 1.4) and `structure.js:354-376` (floor 0.3) —
   change them together or write down why they differ.
5. **Unexplained counts in the tree.** `3` / `0` / `22` on screens is
   `screen.apis.length`; `9/14` on state models is states/transitions; `7` on
   ACCESS is table count. Nothing says so, and `0` reads as broken.
6. **`status: notStarted`** renders as plain monospace in a key/value table.
   It is the field a PM scans for. Make it a chip in the verdict palette.
7. **Nested scroll regions.** The screen preview scrolls inside a page that also
   scrolls; the wheel does different things a few pixels apart.
8. **No breadcrumb.** Nothing states `Frontend › Guest Web — Storefront ›
   WEB-001`. The dropdown and the sidebar each say part of it.
9. **Orphaned history notes.** A one-word note renders as a bare line under its
   row with no tie to it. Indent or rule it.
10. **The sidebar note box is permanent** — 100px of explanation you have
    already read, on every layer, forever. One line, or dismissible.

---

# 5. A guest account type

> **Superseded in two ways, 18 August — built as written below, then changed.**
>
> **The role is `client`, not `guest`.** The package already uses `guest` for a
> venue visitor, on 96 operations in `x-ticvai-audience`. Two meanings for one
> word in one repository is a bug waiting for somebody to read the wrong one.
>
> **A client sees everything except the Decisions layer**, not the Frontend and
> Contracts subset decided on 17 August. Requested directly, and the narrower
> version withheld the data model and the state machines — which are a
> description of what is being built, and the thing a client is entitled to.
> What is still withheld is the deliberation: rejected options, what they would
> have cost, which vendor lost, what has since been superseded.
>
> Everything else below holds as written: invite-only, off-domain only for this
> role, three-day links, read-only enforced by `require_writer`, and the payload
> refused rather than hollowed out. The one addition experience forced is the
> `/api/file` gate — an ADR is a `.md` file, so refusing `/api/decisions` and
> leaving that endpoint open would have let a client read every decision one
> path at a time.

Requested: an account **outside `softlabsgroup.com`** that can **view but not
write**.

## What exists

- `security.py:32` — `ALLOWED_DOMAIN`, default `softlabsgroup.com`.
- `security.py:64-75` — `check_email` refuses any other domain outright.
- Roles are exactly `admin` and `reviewer`, validated in two places:
  `main.py:305` (`set_role`) and `main.py:360` (`create_invite`).
- Verdicts are written by `main.py:492` behind `require_account` — **any**
  signed-in account, of any role.

## The shape

Add a third role, `guest`, and let it — and only it — come from outside the
domain.

1. **Role list** becomes `admin | reviewer | guest`, at `main.py:305` and
   `main.py:360`.
2. **`check_email` takes the role.** The domain rule stays exactly as it is for
   `admin` and `reviewer`; it is skipped only for `guest`. The check must live
   in `security.py` so there is one place that decides, not two.
3. **Guests are invite-only.** The domain rule is what currently stops a
   stranger self-registering. Removing it for guests means an admin issuing the
   invite is the *only* thing establishing who they are. So:
   - `/api/auth/bootstrap` never mints a guest — the first account is an admin.
   - No self-signup path accepts an outside address.
   - Guest invites should expire faster than the current 7 days. Suggest 3.
4. **Read-only is enforced on the server**, not by hiding buttons. A new
   `require_writer` dependency — role in `{admin, reviewer}` — guards
   `POST /api/validation` (`main.py:492`) and every other write. Hiding the
   form is presentation; the guard is the rule.
5. **The UI says why.** Where a reviewer sees the verdict form, a guest sees
   one line: *"Signed in as a guest — you can read everything and record
   nothing."* Silence would read as a bug.
6. **Guests are visible as guests.** The admin roster and
   `/api/verdicts` roster should mark them, and the account chip should carry
   the role, so nobody wonders why an address on another domain is in the list.
7. **Reads a guest should still not get**: the admin roster
   (`require_admin` already covers it) and the invite list. Worth confirming
   nothing else in the payload is sensitive before handing an outside address a
   login.

## Decided: a guest is a client, and sees less

Confirmed 17 August. A guest is an **outside client**, not a contractor, so the
view is restricted rather than complete.

### What a client sees

- **Frontend** — Screen, Journey, Apps, Waves. Their product, and what ships when.
- **Contracts** — Reader and Structure. The interface they will build against.

### What a client does not see

| Hidden | Why |
|---|---|
| **Decisions** (all ADRs) | Rejected options, cost arguments, vendor choices, supersession history. Deliberation, not deliverable. |
| **Every Audit view** | A live defect count is our own quality control. Handing a client "5 errors, 7 warnings, 4 broken refs" starts the wrong conversation. |
| **Backend** (Data, Migrations, Routing) | Database internals, row-security policies, read/write routing. Nothing a client needs; everything an attacker would want. |
| **Verdict history and the reviews dashboard** | Internal reviewers disagreeing with each other, and per-person performance stats. |
| **Contracts › Lineage** | It is a candour page — it names what is stale and which source won. Correct for us, wrong as a client's first impression. |

## The blocker: hiding it in the UI does not hide it

**`server.mjs` has no authentication at all.** Not a cookie, not a session, not
a token — grep the file. Every payload is served open on port 4173:

```
/api/index   /api/detail    /api/journeys   /api/backend
/api/domain  /api/lineage   /api/decisions  /api/tooltips
/api/events  /api/file      /api/tree
```

`/api/file` (`server.mjs:319-331`) will hand back **any** `.yaml`, `.md`,
`.json` or `.csv` in the tree. Authentication lives entirely in the separate
FastAPI service on 8787; the data server knows nothing about it.

So a client given a login could open devtools and `fetch('/api/decisions')` —
every ADR we just decided to hide. **Hiding a layer in `app.js` is decoration,
not access control.** This must be fixed before a single outside address gets
an account.

### What that means for the work

1. **`server.mjs` has to check the session.** Either it validates the same
   cookie against the auth service, or the auth service proxies the data
   routes. The first is less disruptive: one `verify` call, cached briefly.
2. **The payload is filtered on the server, per role.** A guest's `/api/index`
   must not contain the Decisions or Backend branch at all — not "contains it,
   and the UI declines to draw it".
3. **`/api/file` needs a role gate too**, or an allowlist of paths a guest may
   read. It is the widest hole here.
4. **Only then** does the UI work matter: hide the layer tabs a guest cannot
   use, and say why rather than showing empty pages.

Order matters. Steps 1–3 are the feature; step 4 is the finish.

---

# Order of work

1. **Put `server.mjs` behind the session** *(§5 blocker)* — this is the one item
   that is a security fix rather than an improvement, and the guest role cannot
   ship without it.
2. Role-filtered payloads + `/api/file` gate, then the `guest` role itself *(§5)*
3. Verdict dots + group progress + untouched filter *(§1)*
4. `]` `[` `n` and verdict keys *(§2)*
5. The three self-contradicting diagrams: Graph legend, Data colours, Apps
   duplication *(§ broken)*
6. Stale LINKS rail on Contracts, ADR title doubling, colon-truncated prose —
   all small, all visible
7. Fit-on-load and docked legends across the canvas views
8. Pinned verdict bar and the rail rethink *(§3, §4)*
