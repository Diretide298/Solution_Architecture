# Viewer — what changed in the package on 20 August

**For whoever picks up the viewer next.** The package grew six things the viewer has no knowledge
of, and one thing it reads is now derived rather than hand-maintained. None of it breaks the
viewer — it boots clean, 0 errors — but each is data it is currently ignoring.

Ordered by what a reviewer would notice first.

---

## 1. `handoff/relationships.csv` is derived now — and the ER diagram was wrong because of it

**Read this one even if you read nothing else.** The ER diagram takes its edges from this file, and
until 20 August it was hand-maintained: **515 rows against the relationship graph's 854**, and it
marked `identity.grant.principal_id` as `ambient`.

The viewer hides ambient edges by default. **A declared foreign key was being drawn as nothing** —
which a reviewer spotted by looking at the picture and asking why `grant` had no connector to
`principal`.

`tools/derive-relationships.py` now writes it, and the edge kinds map deliberately:

| CSV `edge_kind` | Comes from | Drawn as |
|---|---|---|
| `reference` | a declared or conventional foreign key | the ordinary case |
| `child` | a `<parent>_<thing>` table naming its parent | strongly |
| `ambient` | two tables written by one operation | hidden unless asked for |

**48 child edges, not 335.** A first cut marked every required foreign key as parentage and
produced `entitlement.product_id` as a child — **a product does not own the entitlements issued
against it**, and deleting one must not take them.

**Nothing to change in the viewer.** The file it already reads is now correct, and it will stay
correct because `refresh.sh` rebuilds it.

---

## 2. `schema-reference.json` gained a `lineage` block — the ER diagram could show where a table hangs

New top-level key, one entry per table:

```json
"orders.order_line": {
  "schemaRoot": "orders.sales_order",
  "isSchemaRoot": false,
  "anchors": ["access.admission_profile", "identity.role", "pii.subject", "platform.scope_node"],
  "isAnchor": false,
  "parent": "orders.sales_order",
  "depth": 1,
  "reachesRootVia": "sales_order_id -> orders.sales_order"
}
```

**`anchors` is where a table's own outbound keys stop**, following them across schemas. The
distribution is the honest shape of the package: **`platform.scope_node` is reached by 289 of 353
tables** — the tenancy spine — and `identity.role` by 207.

**Worth surfacing as a filter**: *show me everything anchored only on `scope_node`* is *show me
everything that is purely tenancy-scoped*, and that is a question the ER diagram cannot currently
answer.

`handoff/schema-roots.md` is the prose version, per schema, with the four places the arithmetic and
the meaning disagree stated outright — `access` is about entitlements even though `access_point`
has more inbound edges.

---

## 3. Screens gained `entryState` — 280 of them

**The largest gap the review found, and the viewer shows nothing of it.**

280 screens call an operation with a path parameter and **not one route declared it**. `GST-013
Ticket Details` calls `getEntitlement(entitlementId)` on `/general/ticket-details` — **the screen
could not know which ticket it was showing.**

```yaml
entryState:
  params:
    - name: entitlementId
      from: deepLink        # or a screen id, or `session`
  coldEntry: >
    A ticket link opened after the event. Shows the entitlement with its status — expired, used,
    transferred — because *not found* to somebody holding a ticket is the wrong answer.
```

**`from` is the interesting field.** It names the screen that supplies the id, `session` where it
comes from the signed-in principal, or `deepLink` where a guest can arrive cold.

**This makes the journey view honest.** A journey drawn as `A → B` where B needs an id A does not
supply is a journey that cannot run, and the viewer currently draws it happily. **152 screens still
have a `deepLink` parameter with no cold-entry answer** — those are a product decision, not a
derivation, and showing them as a list would be useful.

---

## 4. Screens gained `density` — and it is not cosmetic

`compact` · `comfortable` · `touchLarge`, derived from `platform.formFactor`.

**A gate device held in one hand while the other takes a ticket is not a desktop.** P07 was
`compact` until 20 August because the first pass assigned density by platform number.

**Worth a lens.** *Show me every touchLarge screen* is *show me everything a gloved hand uses with a
queue behind it*, and those screens fail differently.

---

## 5. `wireframe.stateBoards` — boards that draw a state rather than a screen

Nine scanner screens became states of two screens on 18 August. **`SCN-004 Admitted` had a route of
`/access/admitted` and a purpose that said *readable at arm's length, gone in 1.5 seconds*** — a
route you navigate to is not a thing that disappears in 1.5 seconds, and a gate doing forty guests a
minute cannot afford a page load per scan.

**The drawings stayed correct** — an admitted flash and a denial with a reason are different
visuals — so the board anchors are recorded against the state they draw:

```yaml
wireframe:
  stateBoards:
    - state: outcomeAdmitted
      board: "<the P07 board file>#scn-004"   # the filename predates the rename to Venue Scanner
```

`check-wireframes` already understands these. **The viewer will show those anchors as orphans** until
it does too.

---

## 6. `status.json` gained `metricDefinitions`

A dump and the package disagreed about *operations reaching a screen* — **948 against 287** — and
neither said what it was counting. **948 out of 927 total implies −21 reached**, which is not a
count of anything.

Every metric now publishes its population and what it excludes:

> **Not counted:** screen-operation pairs — one operation on six screens is one, not six ·
> per-platform tallies summed · flow steps.

**An invariant refuses `done > total`** at build time. If the viewer computes its own version of any
of these, **it should read the definition rather than reinvent it** — that is what the block is for.

---

## 7. Two checks the viewer was doing that the package was not

The viewer reported these where nobody was reading, and the package now fails on them:

**Six contracts declared no `x-ticvai-platforms`** — `ai`, `public-api`, `resources`, `venue-map`,
`workforce`, `approvals`. Now derived from the screens.

**`P04` meant two things** — *POS* in ten contracts and *Venue POS* in one. The viewer groups by
code and labels by name, so a collision renders one platform twice under two headings.

**This is the wrong way round and worth saying plainly: a reader should not be the thing that
catches a gap in what it reads.** Both are `check-package` errors now.

---

## What has not changed

`backend/` still does not exist, so the backend layer still reads `0 tables`. **That is correct** —
it holds `.sql` migrations and build is 0%. It will populate when Sprint 0 runs.

`lenses ai 166 (69 undeclared)` is unchanged and still worth a look.

---

## The one thing I would fix first

**Not any of the above.** `app.js` is 7,395 lines, and the Decisions layer has one mode where
Contracts has six — **it is the layer a client reviewer opens first and it renders 26 ADRs and 157
conflicts as a file tree with a badge.** The layer's own tip says prose is where the reasons live,
and then shows the prose as a directory listing.

`docs/active/viewer-redesign-brief.md` has the detail. **Do the Decisions layer before the boards** —
the boards are the more visible problem and the less well-understood one, and rebuilding them first
means doing them twice.
