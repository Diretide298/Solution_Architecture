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
| **The resource manifest** | **XLSX**, one sheet | Only where guests book cabanas, loungers or tables from the map. See §3a |
| **The illustrated map** | PNG or JPG, plus the source if you have it | What guests see. Separate from the plan — see §6 |
| **Georeference points** | Two rows in a spreadsheet, or a note | Without these the map is a picture. See §5 |
| **A 3D model** (optional) | **GLB** (binary glTF 2.0), at most 40 MB, **with its navigation file** (JSON) | For the in-park 3D view (ADR-0069). Without it guests get the 2D map. See §11 |
| **A scanned plan or a plan with paths marked by hand** | PDF, PNG or JPG | Accepted since 3 October 2026: the text is read for hints and the marked paths are proposed for you to accept. See §12 |

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
| Bookable resources | `VC-Resources`, `Cabanas`, `Loungers`, `Tables` | Only where guests book them from the map. One closed shape per cabana, lounger or table, labelled — see §3a |

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

## 3a. Bookable resources — cabanas, loungers, tables

**Added 29 September** (decided 29 September, rev 3 REV3-15 and GAP-C2): guests now pick a specific
cabana, lounger or table on the map, hold it and buy it, the way they pick a seat. That needs the
same two files as seating: **the drawing says where each one is; a manifest says what it is.**

**In the drawing:** one closed shape per resource on a resource layer (`VC-Resources`, or one layer
each: `Cabanas`, `Loungers`, `Tables`), **each labelled with its code in Western digits** — `B09`,
`R01`, `T08` — as text inside or on the shape. The label is what the guest sees and taps.

**The resource manifest:** one sheet, header on row 3, five columns:

| Label | Kind | Zone | Capacity | Price band |
|---|---|---|---|---|
| B09 | cabana | Beach | 15 | Large |
| R01 | cabana | River | 6 | Family |

**`Label`** — must match the label in the drawing **character for character** (after digit
normalisation, §4). **`Kind`** — `cabana`, `lounger`, `table`, `pitch` or `other`. A `table` here
is a beach or event table sold like a cabana; restaurant tables are not placed as resources, they
are booked as table reservations. **`Zone`** — the area a guest reads it by. **`Capacity`** — the
most people it takes. **`Price band`** — a band name, the same across the sheet (`Family`,
`Medium`, `Large`, `XL` at Coastal Aqua); **each band is mapped to a product variant at import**,
which is where its price comes from. The map holds no prices.

### What the import reports

| Finding | Meaning |
|---|---|
| `resourceLabelMissing` | A shape on the resource layer has no label |
| `resourceLabelDuplicate` | Two shapes carry the same label |
| `resourceManifestMissingFromPlan` | A manifest row has no shape in the drawing |
| `resourcePlanMissingFromManifest` | A shape in the drawing has no manifest row |
| `resourceCodeUnmatched` | A label names no resource set up at the venue (unless the import is told to create missing ones) |
| `resourcePriceBandUnknown` | A price band not mapped to a product variant |

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

## 11. A 3D model and its navigation file (added 3 October 2026)

**Optional, and it never blocks the map.** ADR-0069: the guest app shows a 3D view of the venue where a
model exists and the 2D map otherwise, with the same route either way. Send two files per venue map,
uploaded together on the Map Import screen (BO-093, source "3D model + navigation file"):

| File | Format | Limits |
|---|---|---|
| **The model** | **GLB** (binary glTF 2.0), metres, +Y up, origin on a surveyed point on the ground (ideally the main entrance) | **At most 40 MB: a larger file is refused at upload.** About 25 MB is the target (a zone 6 MB or less). **At most 300,000 triangles at LOD0 in any zone**, 1.5 million across all levels. Draco or meshopt geometry; **KTX2 textures** (uncompressed textures are refused for 3D), 2048 px at most, 128 MB after transcoding; 150 draw calls. Zones as named nodes with `<zone>__LOD0`, `__LOD1`, `__LOD2` meshes; a node a guest taps is named by its location's `ref` |
| **The navigation file** | **JSON**, format `urn:ticvai:venue-navigation-file:1.0` (the contract's `VenueNavigationFile`) | `anchor` (origin latitude and longitude, heading, scale, two to eight control points far apart), `nodes` (two or more), `edges` (one or more; step-free and indoor flags, an access point where one makes a passage one-way), `locations` (ref, kind, name, the node a guest is routed to, and catalogue **codes**, never ids) |

**What the import does.** The navigation file's nodes, edges and locations become the map's paths and points,
exactly as a walkway layer would; its anchor becomes the map's georeference. The model is measured and every
line of the budget comes back as a number. **What keeps the 3D view off** (the 2D map still publishes): more
than 300,000 triangles at LOD0, uncompressed textures, a control point more than 10 metres from where the
anchor puts it, or a navigation file that does not validate. **Warnings, with the number:** the 25 MB target,
1.5 million triangles, 150 draw calls, texture size and memory, a control point more than 3 metres out,
control points close together, and a catalogue code that matches nothing (that location imports unlinked).

**Start from the graph we already hold.** Where the venue already has a 2D map, the editor exports it in the
navigation-file format (Map Editor, "Export navigation file"), so the 3D studio builds around the paths and
points the venue has already checked rather than describing them again.

**The navigation file alone** (no model) is accepted too: it imports the graph and the points, with no 3D view.

---

## 12. A scanned plan, or a plan with the paths marked by hand (added 3 October 2026)

**A scanned PDF** (a page that is an image, with no vector lines) is read through an **OCR step**: the text on
it, English and Arabic, is found and placed on the plan, and the assistant uses the text near a shape
("WC", "First Aid", a ride's name) as a hint when it proposes what the shape is. **The text never names a point
by itself**: every proposal is accepted, edited or rejected by a person, as with any plan. Its geometry is a
picture's (`rasterOnly`), so its paths are proposed as below.

**A PNG or JPG with the walkways marked by hand** is the quickest way to give a park without CAD a working
route network. Print the plan, draw a single clear line along every walkway in one colour that the plan does
not use (a red or blue marker), keep lines joined where paths meet, and leave a gap where there is no way
through. Photograph or scan it flat, as large as you can, and say on upload that the paths are marked (and in
what colour, if you know). The assistant traces **one segment per marked stretch** and shows each with its
confidence; **you accept or reject each segment on its own**, and the map checks what is reachable after every
decision. A gap in a mark stays a gap: it is never bridged for you.

**Still better:** a walkway or keep-out layer in CAD (§8), which needs no assistant at all.

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
