# Viewer — redesign brief

**Parked 18 August 2026.** The viewer as uploaded (`viewer.zip`, 2,666 files, 86 MB) read and
noted, no code changed. This is the brief for the pass that reworks it.

---

## What is there

Five layers, each with modes and grouping axes, defined once in `LAYERS` at the top of `app.js`.
**The layer model itself is good** — it is the one thing in the viewer that would survive a
rewrite, and the comment on it is right that adding a layer is one entry plus a render function.

| Layer | Modes |
|---|---|
| Frontend | Screen · Journey · Apps · Waves · Audit |
| Contracts | Graph · Structure · ER · Lineage · Reader · Audit |
| Domain | States · Events · Audit |
| Backend | Data · Migrations · Routing · Audit |
| **Decisions** | **Decisions · Audit** |

**14 files, 17,774 lines.** `app.js` alone is **7,395 lines and 302 KB**.

---

## The three problems worth fixing

### 1. `app.js` is 7,395 lines

Everything that is not a graph, a tree, a box diagram or a state machine lives in one file:
routing, state, every render function, the tip wiring, the lens logic, the search.

**The layer model already describes the seams.** Five layers with their own render functions is
five modules, and `app.js` becomes the router and the shared state.

### 2. Decisions is one mode where the other layers have five

**Contracts has six views of one artefact set. Decisions has one view of the thing that explains
all of them.**

The ADRs, the conflict register, the backlog, the clusters and the traceability are the layer a
reviewer actually reads, and they are rendered as a tree of files with a badge. **The layer's own
tip says prose is where the reasons live — and then shows the prose as a directory listing.**

What it needs, and each is a mode:

**Timeline.** ADRs and conflicts in the order they were decided, because **the sequence is the
argument** — ADR-0018 makes sense only after ADR-0011, and CF-138 only after the 14 August
minute. A list sorted by number hides the one thing a reviewer needs.

**Supersession graph.** Which ADR replaced which, and where a citation crosses a supersession.
`check-package` already enforces this and it is invisible in the viewer. **Six ADRs are amended or
superseded; a reader has no way to see the shape of that.**

**Register.** The conflicts as a filterable table with owner, rows blocked and status — not a
tree. **145 conflicts is a dataset, and a file tree is the wrong control for a dataset.**

**Decision detail.** One ADR with its context, decision, consequences and alternatives rendered as
prose, with every conflict that cites it and every contract that implements it resolved as links.
**Currently the body is a tooltip.**

### 3. The boards

**Chinmay, 18 August: the boards are not built how a frontend or UX person would build them.**

That is the honest read. The screens layer models screens as records with an operations list and a
wireframe reference, which is what a *contract* needs and not what a *designer* needs. A screen in
the viewer is a row; a screen to a designer is a composition — layout, hierarchy, states, the
thing next to it.

**This needs its own pass and its own thinking**, not a CSS change.

---

## What to preserve

**The lens.** `passesLens` and `markLens` thread a filter through every layer, so selecting a
platform in Frontend narrows Contracts and Backend. **That is the best idea in the viewer** and
the thing a rewrite would most easily lose.

**The tips.** `tips.js` and `GLOSSARY` carry real explanation rather than field names, and
`deliveryTip` resolves an artefact's own note. Keep the mechanism, keep the content.

**Everything is resolved, not duplicated.** A screen names an operation, the operation resolves
against the contracts, the contract resolves against the schema. **No layer holds a copy of
another layer's truth**, which is why the viewer has never disagreed with the package.

---

## Order for the next pass

1. **Split `app.js`** along the layer seams. Mechanical, and everything else is easier after it.
2. **Rebuild Decisions** as four modes. Highest value per hour — it is the layer a client reviewer
   opens first and the one that shows least.
3. **Then the boards**, as a design conversation rather than a refactor.

**Do not start with 3.** The boards are the most visible problem and the least well-understood,
and rebuilding them before the decisions layer means doing them twice.
