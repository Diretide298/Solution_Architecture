# Viewer upgrade — the brief to hand Claude Code

Paste the block below. Everything it needs is in the package it will be pointed at; the two briefs
named in it carry the detail.

---

## The command

> You are working on the TICVAI viewer, a local Node server that reads the design package sitting
> in its parent directory and renders it as five layers. Run `npm start` from `viewer/` and open
> `http://localhost:4173`. It boots clean today — 0 errors, 932 operations, 383 screens — so
> **anything you break, you broke.**
>
> Read `docs/active/viewer-redesign-brief.md` and `docs/active/viewer-update-brief-20aug.md`
> first. They are written for you and they contain the reasoning, not just the instructions.
>
> Work in this order. **Do not start at step 3** — it is the most visible problem and the least
> well-understood, and rebuilding it before the layer underneath means doing it twice.
>
> **1 — Split `public/app.js`.** It is 7,395 lines and 302 KB, and it holds routing, state, every
> render function, the lens logic, tip wiring and search. The `LAYERS` constant at the top already
> describes the seams: five layers, each with its own modes and render functions. Split along
> them, leaving `app.js` as the router and the shared state. **Change no behaviour in this step.**
> Take a screenshot before and after and confirm they match.
>
> **2 — Rebuild the Decisions layer.** It has one mode where Contracts has six, and it is the
> layer a client reviewer opens first. It currently renders 26 ADRs and 157 conflicts as a file
> tree with a badge, while the layer's own tip says prose is where the reasons live. Four modes:
>
>   - **Timeline** — ADRs and conflicts in the order they were decided. **The sequence is the
>     argument**: ADR-0018 makes sense only after ADR-0011, and CF-138 only after the 14 August
>     minute. A list sorted by number hides the one thing a reviewer needs.
>   - **Supersession graph** — which ADR replaced which, and where a citation crosses a
>     supersession. `check-package` already enforces this and it is invisible in the viewer. Six
>     ADRs are amended or superseded and a reader cannot see the shape of it.
>   - **Register** — the conflicts as a filterable table with owner, rows blocked and status.
>     **157 conflicts is a dataset, and a file tree is the wrong control for a dataset.**
>   - **Decision detail** — one ADR rendered as prose, with every conflict citing it and every
>     contract implementing it resolved as links. Currently the body is a tooltip.
>
> **3 — Then the boards, and treat it as a design conversation.** A `.dc.html` per platform is a
> document; a design system is a component library, and **the same button drawn 383 times is 383
> buttons.** Do not refactor your way into this one.
>
> Alongside those, six things the package gained on 20 August that the viewer currently ignores.
> Each is described in the 20 August brief with the reason it exists:
>
>   - `schema-reference.json` now has a **`lineage`** block per table — `parent`, `schemaRoot`,
>     `anchors`. `platform.scope_node` is reached by 289 of 353 tables. **Make `anchors` a filter
>     on the ER view**: *everything anchored only on `scope_node`* is *everything purely
>     tenancy-scoped*, and the diagram cannot answer that today.
>   - **`entryState`** on 280 screens — what each arrives holding and where it came from. **A
>     journey drawn as `A → B` where B needs an id A does not supply is a journey that cannot
>     run**, and the Frontend layer draws it happily. Flag those.
>   - **`density`** on every screen — `compact`, `comfortable`, `touchLarge`. Worth a lens: *every
>     touchLarge screen* is *everything a gloved hand uses with a queue behind it*.
>   - **`wireframe.stateBoards`** — nine scanner drawings now belong to states rather than
>     screens. The viewer will show those anchors as orphans until it knows.
>   - **`metricDefinitions`** in `status.json` — population and exclusions per metric. If the
>     viewer computes its own version of any of these, read the definition rather than reinvent
>     it. A dump and the package disagreed about one metric by 948 against 287.
>   - **`handoff/relationships.csv` is derived now**, not hand-maintained. Nothing to change —
>     but it was the cause of a real bug, so do not go back to editing it.
>
> Two rules throughout:
>
> **Preserve the lens.** `passesLens` and `markLens` thread a filter through every layer, so
> selecting a platform in Frontend narrows Contracts and Backend. **It is the best idea in the
> viewer and the thing a rewrite would most easily lose.**
>
> **Preserve the resolution model.** A screen names an operation, the operation resolves against
> the contracts, the contract resolves against the schema. **No layer holds a copy of another
> layer's truth**, which is why the viewer has never disagreed with the package. Do not cache your
> way out of a slow render.
>
> Run `checks/*.mjs` after each step — they are the viewer's own tests. And run
> `bash tools/refresh.sh` in the package before you start, so you are reading current artefacts.

---

## What not to ask it to do

**Do not ask it to fix the numbers it will see.** 320 of 392 screens reachable, 27 of 60 flows,
159 of 932 operations named by a flow — **those are the package's gaps, not the viewer's**, and a
viewer that hides them is worse than one that shows them plainly.

**Do not ask it to populate `backend/`.** The layer reads `0 tables` because build is 0% and the
folder holds `.sql` migrations. That is correct and it will fill when Sprint 0 runs.

**Do not let it hand-edit anything under `repos/`.** Those are mirrors, `tools/derive-mirrors.py`
writes them, and `check-package` fails on drift. A file edited there is a file overwritten on the
next refresh — which is exactly how a state model spent two days anchored on an object that had no
values.
