# Venue map and seating — what to send, and in what format

**For a venue's drawing office and operations team.** Written 18 August 2026 against the sample
files TICVAI supplied, so every rule below is one the existing drawings either already meet or
missed in a way that broke the import.

**The point of this document is that a file sent to spec imports in one pass.** Every rule exists
because its absence produced a specific failure, and each is named.

---

## 1. What to send

| | Format | Why this one |
|---|---|---|
| **The plan** | **DWG or DXF** preferred · PDF accepted · SVG accepted | **Send native CAD if you have it.** Exporting to PDF flattens layer names, and the layer names are what the import reads |
| **The seating manifest** | **XLSX**, one sheet per section | The definitive list of seats. The plan says where; this says what |
| **The illustrated map** | PNG or JPG, plus the source if you have it | What guests see. Separate from the plan — see §6 |
| **Georeference points** | Two rows in a spreadsheet, or a note | Without these the map is a picture. See §5 |

**Raster-only is accepted and degrades gracefully.** A scan or a photograph of a plan cannot be
layer-extracted; the manifest still gives you seats and the map still works as an image. **You lose
automatic geometry, not the map.**

---

## 2. Layers — the rule that matters most

**Name layers by what a thing *is*, not by how it was drawn.**

The sample drawing carries `VC-Seats`, `VC-wheelchairseating` and `VC-Steps` — **and those are
right.** They say what the geometry means. Keep doing that.

### Required layers

| Role | Accepted names | |
|---|---|---|
| **Walkways and paths** | `Paths`, `Walkways`, `Circulation`, `Footpath` | Best if you have it — **and see below, we can work without it** |
| **Keep-out** | `Water`, `Planting`, `BackOfHouse`, `Plant` | **Send this if you send no walkway layer.** It is what stops a derived path crossing a lake |
| Steps and stairs | `Steps`, `VC-Steps`, `Stairs` | Marks which paths are not step-free |
| Buildings | `Buildings`, `Structures`, `Footprints` | |
| Seats | `Seats`, `VC-Seats`, `Seating` | Seated venues only |
| Accessible seating | `Accessible`, `VC-wheelchairseating`, `Wheelchair` | Seated venues only |
| Section boundaries | `Sections`, `VC-Sections`, `Blocks` | Seated venues only |
| Stage or focal point | `Stage`, `Screen`, `Pitch` | |
| Exits | `Exits`, `Egress` | |
| Emergency exits | `EmergencyExits`, `FireExits` | **Send separately — see §7** |

### You do not have to draw the walkways

**Most drawings prepared for ticketing have no walkway layer**, and that is fine.

**Walkable space is the negative space.** The site boundary, minus buildings, minus seating, minus
water and planting and back-of-house. **That is subtraction — exact, repeatable, and better than
any model would be at it.** The platform thins the result to a centreline and splits it at every
fork.

**So send the keep-out layer if you send nothing else about circulation.** It is the difference
between a usable path network and one that routes a guest across a lake.

**An explicit walkway layer still beats a derived one**, because it knows about a path across a
lawn that subtraction merges into open ground. Send it where you have it; do not draw it where you
do not.

**If your plan is a scan or a photograph with no geometry at all**, there is nothing to subtract
and the paths have to be seen rather than computed. The assistant will propose a network with a
confidence on each segment and **you accept it segment by segment** — the acceptance is stricter
than for labels, because a mislabelled toilet is a cosmetic error and **a wrongly accepted walkway
routes a guest into a service yard.**

**A path that crosses the steps layer is marked as not step-free**, automatically. This is the
single most valuable thing the steps layer buys, and it is why sending it matters even for a venue
with no seating.

**Case and hyphens do not matter.** A `VC-` prefix is fine and is ignored.

### Three rules, each from a real failure

**Do not reuse a layer name.** The sample drawing has **two distinct layers both named `Layer 1`**.
The importer now accepts a list per role, so this no longer loses geometry — but it cannot tell you
which of the two you meant, and somebody has to.

**Do not leave geometry on layer `0`.** It is AutoCAD's default, it means *"nobody set a layer"*,
and it is the single most common reason an import finds nothing.

**One kind of thing per layer.** Steps on both `steps` and `VC-Steps` is workable and confusing.
Steps mixed in with seats is neither.

**Every layer you send is reported back**, mapped or not. A layer nobody claimed is shown rather
than ignored, because it usually means something was missed.

---

## 3. The seating manifest

**Exactly the shape TICVAI already sends.** The sample is correct and this is it written down.

One sheet per section. Header on row 3. Four columns:

| Description | Section | Row | Seat |
|---|---|---|---|
| Seating | A1 | 1 | 1 |
| Seating | A1 | 1 | 2 |

**`Description`** — `Seating`, or `Wheelchair`, `Companion`, `Restricted view`, `House seat`.
Anything not recognised is imported as a plain seat and reported.

**`Section`** — must match the section label in the drawing **character for character.** This is
the join, and §4 is about the one way it silently fails.

**`Row` and `Seat`** — numbers or letters. Both are fine; be consistent within a section.

### What breaks a manifest

**Merged cells.** A merged section header spanning rows produces blank sections underneath.

**A total row at the bottom.** It imports as a seat in a section called `Total`.

**Blank rows between sections.** Harmless, and they make the count ambiguous when you check the
import against your own figure.

---

## 4. Digits — the failure nobody sees

**`A١` and `A1` are the same section to a person and two different sections to a computer.**

The importer normalises Arabic-Indic digits before joining, so a mixed file works. **But if the
drawing uses `A١` and the manifest uses `A1`, nothing visibly fails** — the seats simply do not
join, and you get a map with geometry and no seats, or seats and no geometry.

**Use Western digits in section codes, row numbers and seat numbers**, in both files. Arabic in
*names* and *labels* is expected and fine — `المسرح الرئيسي` as a section name is correct. It is
only the codes that must be plain.

---

## 5. Georeference — two points

**Without this the map is a picture. With it, a guest sees where they are on it.**

Send two points that appear in the drawing and whose real-world position you know — a main entrance
and a far corner work well:

| Point | Drawing X | Drawing Y | Latitude | Longitude |
|---|---|---|---|---|
| Main entrance | 412.5 | 1203.0 | 25.2048 | 55.2708 |
| North-east corner | 2260.0 | 180.0 | 25.2061 | 55.2731 |

**Pick two points far apart.** Two points close together give an accurate scale and a rotation that
drifts across the site.

**If you cannot supply these, say so and send the map anyway.** Everything works except showing a
guest their own position.

---

## 6. The illustrated map

**This is a different artefact from the plan and both are wanted.**

The plan is an architect's drawing — accurate, and not something a guest wants to look at. The
illustrated map is the painted, styled map with your branding on it. **Guests see the second and
the platform routes on the first.**

**Send:** PNG or JPG at the largest size you have. **12,000 pixels wide is fine** — the platform
generates zoom tiles, because a phone should not download a twenty-megabyte image at the gate.

**And send four alignment points**: pick four features visible in *both* the plan and the
illustration — a corner, an entrance, a landmark — and give their pixel position in the
illustration and their coordinates in the plan. **The two are drawn at different scales by
different people**, and without these a toilet placed on the plan appears in a lake on the
illustration.

---

## 7. Points of interest

**You do not need to mark these in the drawing.** Placing rides, toilets, exits and restaurants is
done on screen after import, and the assistant proposes most of them from the layers.

**If your drawing already has them on named layers, send them** — `Toilets`, `FirstAid`, `Exits`,
`Rides`, `FoodBeverage`, `Retail`, `Parking`, `PrayerRoom`, `BabyCare`, `ATM`, `Lockers`.

**One distinction the platform needs and drawings usually blur:** an **exit** is where a guest
leaves, an **emergency exit** is where they are sent. If your drawing has them on one layer, split
them or tell us — **a map that cannot tell them apart routes a normal departure through a fire
door.**

---

## 8. Paths — what is derived and what is not

**From your drawing, automatically:**

| | From |
|---|---|
| Where paths run | The walkway polygon, thinned to a centreline |
| Where they meet | Forks in that centreline, which become **junctions** |
| How long each is | The centreline, with the georeference for real units |
| Which are not step-free | **Any path crossing the steps layer** |
| Which are indoors | Paths inside a building footprint |

**Junctions are generated, not drawn.** A fork in a walkway with nothing at it still needs a node,
and you do not name them — they are invisible to guests and present in the graph. **Otherwise every
bend would have to be a named destination**, and a guest browsing the map would see forty entries
called *Path junction 12*.

**One-way paths are not a thing.** A pedestrian walkway has no direction, and the three cases that
look one-way are all something standing on the path rather than the path itself — **a turnstile, a
queue line, an exit-only gate.** The turnstile already carries its direction as an access point and
the queue already owns its own flow, so the router reads them from there.

**Marking the path as well would have duplicated both and drifted from them**: a gate reconfigured
to bidirectional would leave a path still marked one-way, and nothing would have noticed.

**Set on screen afterwards:** closures, for maintenance and incidents — live, rather than by
redrawing.

### Why step-free matters more than the rest

**A wheelchair user routed up a staircase has been failed by the map, not by the venue** — and that
failure is invisible in a drawing. The platform refuses to publish a map where something is
reachable only by stairs without telling you first, by name.

**No drawing you send will make this visible to you**, which is why it is checked before
publication rather than discovered afterwards.

---

## 9. What happens after you send it

    you send ──► we extract ──► we propose ──► you place ──► you publish
                 (deterministic)   (assistant)   (on screen)   (goes live)

**Extraction is deterministic and reports exactly what it read** — every layer name, every shape
count, and whether anything matched. **A file that yields nothing says so rather than reporting
success.**

**The assistant then proposes labels** — *this polygon by the entrance is probably a restroom* —
with a confidence on each. **You accept, edit or reject one at a time.** It never applies anything
itself.

**Nothing is live until you publish.** You can work on a draft for weeks while the current map
keeps serving guests, and publishing creates a version so a guest halfway through a route finishes
on the version they started with.

---

## 10. If you can only send some of this

**Send what you have.** In order of how much they buy:

**The manifest alone** gives you seats, sections and rows — sellable inventory, with no map.

**A building footprint and a keep-out layer** — with no walkways drawn at all — give you a
navigable venue, because walkable space is what is left when those are subtracted. **For a park
this is the important one**, and it asks a drawing office for two layers it almost certainly
already has.

**Plus a raster plan** gives guests a map to look at.

**Plus layered CAD or PDF** gives automatic geometry and the assistant's proposals.

**Plus georeference** gives a guest their own position on it.

**Plus the illustrated map** gives them your branding rather than ours.

**Each step is independently useful and none blocks the next.**

---

## Appendix — every field, and where it comes from

**Checked 18 August: no field in the venue map has an unstated source.** If something below is not
in a file you send or a screen you fill in, it does not exist.

| Field | Comes from |
|---|---|
| `VenuePath.geometry` | Walkway layer, **or the negative space** — site minus buildings, seating and keep-out (§2) |
| `VenuePath.distanceMetres` | The centreline, with the georeference (§5) for real units |
| `VenuePath.isStepFree` | **Steps layer** (§2) — a path crossing it is not step-free |
| `VenuePath.isIndoor` | Buildings layer (§2) |
| `VenuePath.fromPointId` · `toPointId` | A point of interest, or a **generated junction** (§8) |
| `VenuePath.restrictedByPointId` | **The access point on the path** — a turnstile's direction lives there, not here |
| `VenuePath.closedReason` | Live, operational |
| `VenuePoint.position` | Plan coordinates |
| `VenuePoint.kind` | POI layers (§7), or the assistant's proposal |
| `VenuePoint.isAccessible` | Accessible layer (§2) |
| `VenuePoint.outletId` · `productId` | **On screen** (§7) — linked to the outlet or product it is |
| `VenueMap.isGeoreferenced` | **Two georeference points** (§5) |
| `VenueMap.baseAssetId` | The illustrated map (§6) |
| `VenueMap.baseImageAlignment` | **Four alignment points** (§6) |
| `VenueMap.tileSetRef` | Generated from the base asset |
| `VenueMap.graphStatus` | Computed at publish |

### The two that are not in any drawing

**Outlet and product links**, and **closures**. Both are operational rather than architectural, both
are set on screen, and **a venue that expects its drawing office to supply them will be waiting a
long time.**

**One-way used to be a third and is not.** A pedestrian path has no direction — what is one-way is
a turnstile or a queue, and both already say so.

### The two to send if you send nothing else

**Buildings and keep-out.** Between them they define the walkable space by subtraction, which is
where every path comes from. Steps make those paths accessible-aware, the georeference makes them
locatable.

**A drawing office almost always has both already**, which is the point — this asks for what
exists rather than for work.
