# ADR-0069: In-park 3D navigation is built natively, from a venue model, a pathway file and GPS

**Status:** Accepted · 30 September 2026 · agreed with the client in the meeting of 30 September
**Date:** 2026-09-30 · **Deciders:** Chinmay Parab (Softlabs), with Qossai and Allam (TICVAI)
**Source:** client meeting of 30 September 2026, MoM section 4.8 and section 5 ("In-park 3D navigation can be built natively within the platform (React Three.js, a venue GLB model plus a pathway/location metadata file, and live GPS), without external mapping integration")
**Related:** `contracts/satellite/venue-map.yaml` (`VenueMap`, `VenuePoint`, `VenuePath`, `getVenueMapGraph`) · `handoff/venue-map-input-spec.md` · screens GST-021 Interactive Map and GST-038 At the Venue (P02) · ADR-0007 (React Native guest app) · ADR-0013 (local-first, the offline pattern) · ADR-0038, amended by ADR-0040 (data stays in the tenant's region)
**Scope:** the file formats below are our proposal inside the accepted decision; the decision itself (native, no external mapping integration) is the client's agreement

---

## Context

**The question was asked in the room.** At the 30 September walkthrough of the guest mobile app, the
live map took a guest to a selected point (the nearest food outlet) and into a walking-navigation mode.
Qossai asked what software an in-park **3D** navigation would need, and whether it needs an external
tool. The answer given, and agreed: it can be built natively in the platform with React Three.js, from
a 3D GLB model of the venue and a metadata file of pathways and locations, combined with the guest's
live GPS position, with no external mapping integration.

**Most of the machinery already exists in the specification.** The venue-map contract (19.2.55 to
19.2.60) holds maps per venue (park, floor, zone, parking), points of interest (`VenuePoint`, a closed
set of kinds linked to outlets and products), paths (`VenuePath`, with step-free, indoor and access-point
restrictions), a georeference, and **a navigation graph the platform guarantees and the client routes
over** (`getVenueMapGraph`, versioned, offline-capable). GST-021 already routes on the device. What was
missing is the 3D view, the file a venue sends for it, and how a model's coordinates meet GPS.

**The benchmark is known.** The client referenced the Kidzania app's interactive 3D-style map as the
bar for the venue map (mom-digest, venue map section).

**Three constraints decide the shape:**

1. **A guest in the middle of a park has no signal.** The route has to be computed on the phone.
2. **A mid-range phone must carry it.** A 3D park is the heaviest thing the guest app will render.
3. **No third-party map service.** Data stays in the platform and the tenant's region; there is no
   external licence, key or per-request cost, and nothing to integrate.

---

## Decision

**In-park 3D navigation is part of the guest app, rendered with react-three-fiber (three.js,
`@react-three/fiber/native` on `expo-gl` in the React Native app), from three inputs per venue map:**

| Input | What it is | Where it comes from |
|---|---|---|
| **(a) The venue model** | One GLB (binary glTF 2.0) file per venue map | The venue supplies it, or commissions it |
| **(b) The navigation file** | One JSON file: pathways (a walkable graph) and locations (POIs linked to catalogue items) | The venue supplies it with the model; the platform imports it |
| **(c) The guest's position** | Live GPS (WGS84) from the phone | The device |

**There is no external mapping SDK, tile service or routing API.** The navigation file is not a second
graph: it is **imported into the existing venue map** (`VenuePoint`, `VenuePath`) through the same
import pipeline as a CAD drawing, validated by `validateVenueMapGraph`, and published with
`publishVenueMap`. The guest app routes over `getVenueMapGraph` as GST-021 already does. **The 3D model
is a rendering of the map, never the source of its truth** — a path closed with `setPathClosure` closes
in 3D too, because the route comes from the graph, not from the mesh.

**Until a venue supplies a model, the venue gets the 2D map** (the illustrated base map or plain
geometry, GST-021 as specified). The 3D view is a per-map upgrade, not a precondition.

### 1. The venue model (GLB)

- **glTF 2.0 binary (`.glb`), one file per venue map** (a park map, or a floor per building, as
  `VenueMap.kind` already allows). Units are **metres**; axes are glTF's (**+Y up**, right-handed).
- **Model origin at a surveyed point on the ground**, ideally the main entrance. Its WGS84 position is
  the anchor in the navigation file (section 3).
- **Geometry compressed with Draco or meshopt; textures in KTX2 (Basis Universal).** Uncompressed
  textures are refused at import.
- **Three levels of detail**, as separate meshes named `<zone>__LOD0`, `__LOD1`, `__LOD2`, and the park
  split into **zones** (named nodes) so the app loads and culls a zone at a time.
- **Nodes for things a guest taps are named by the POI's `ref`** (section 2), so a tap on the 3D ride
  resolves to the same `VenuePoint` as a tap on the pin. A node without a matching `ref` is scenery.
- **No embedded cameras, lights or animations are relied on.** The app lights the scene; an animated
  element (a ride turning) is optional and must not exceed the budget.

### 2. The navigation file (pathways and locations)

JSON, one per venue map, UTF-8. **Proposed schema** (JSON Schema 2020-12; `$id` to be fixed when the
contract is updated):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TICVAI venue navigation file",
  "type": "object",
  "required": ["formatVersion", "venueCode", "mapName", "anchor", "nodes", "edges", "locations"],
  "properties": {
    "formatVersion": { "const": "1.0" },
    "venueCode": { "type": "string", "description": "The venue's code on the platform" },
    "mapName": { "type": "string", "description": "Matches VenueMap.name; a floor plan is its own file" },
    "floorLevel": { "type": ["integer", "null"] },
    "modelFile": { "type": "string", "description": "The GLB this file belongs to, e.g. park-2026-10.glb" },
    "anchor": {
      "type": "object",
      "description": "How the model's local frame sits on the earth",
      "required": ["originLat", "originLng", "headingDegrees"],
      "properties": {
        "originLat": { "type": "number", "minimum": -90, "maximum": 90, "description": "WGS84 latitude of the model origin" },
        "originLng": { "type": "number", "minimum": -180, "maximum": 180, "description": "WGS84 longitude of the model origin" },
        "originAltitudeMetres": { "type": "number", "default": 0, "description": "Ellipsoidal height; informational" },
        "headingDegrees": { "type": "number", "minimum": 0, "exclusiveMaximum": 360, "description": "True-north bearing of the model's -Z axis, clockwise" },
        "scale": { "type": "number", "default": 1, "description": "Metres per model unit; 1 for a model in metres" },
        "controlPoints": {
          "type": "array", "minItems": 2, "maxItems": 8,
          "description": "Surveyed checks, far apart. Used to verify the anchor, not to define it",
          "items": {
            "type": "object", "required": ["label", "x", "z", "lat", "lng"],
            "properties": {
              "label": { "type": "string" },
              "x": { "type": "number" }, "z": { "type": "number" },
              "lat": { "type": "number" }, "lng": { "type": "number" }
            }
          }
        }
      }
    },
    "nodes": {
      "type": "array", "minItems": 2,
      "description": "Graph vertices in model coordinates. A junction, or the door of a location",
      "items": {
        "type": "object", "required": ["id", "x", "z"],
        "properties": {
          "id": { "type": "string", "pattern": "^[A-Za-z0-9_-]{1,64}$" },
          "x": { "type": "number" }, "y": { "type": "number", "default": 0 }, "z": { "type": "number" },
          "zone": { "type": "string", "description": "The GLB zone node it sits in" }
        }
      }
    },
    "edges": {
      "type": "array", "minItems": 1,
      "description": "Walkable connections. Undirected; a one-way passage names the access point that makes it one-way",
      "items": {
        "type": "object", "required": ["from", "to"],
        "properties": {
          "from": { "type": "string" }, "to": { "type": "string" },
          "polyline": {
            "type": "array", "items": { "type": "array", "items": { "type": "number" }, "minItems": 2, "maxItems": 3 },
            "description": "Intermediate [x, z] or [x, y, z] points along the centreline; straight when absent"
          },
          "isStepFree": { "type": "boolean", "default": true },
          "isIndoor": { "type": "boolean", "default": false },
          "throughAccessPointCode": { "type": ["string", "null"], "description": "A gate or turnstile on the edge; its direction lives on the access point" }
        }
      }
    },
    "locations": {
      "type": "array",
      "description": "Points of interest. Each becomes a VenuePoint",
      "items": {
        "type": "object", "required": ["ref", "kind", "name", "nodeId"],
        "properties": {
          "ref": { "type": "string", "description": "Stable key; also the name of the GLB node drawn for it" },
          "kind": { "type": "string", "description": "One of VenuePoint.kind (ride, restaurant, shop, toilet, firstAid, ...); junction is not allowed here" },
          "name": { "type": "string" },
          "nameLocalised": { "type": "object", "additionalProperties": { "type": "string" } },
          "nodeId": { "type": "string", "description": "The graph node a guest is routed to: the entrance, not the centre" },
          "labelPosition": { "type": "array", "items": { "type": "number" }, "minItems": 3, "maxItems": 3, "description": "[x, y, z] where the pin floats" },
          "catalogue": {
            "type": "object",
            "description": "The catalogue item it is. Codes, not ids, so a file can be written before the platform assigns ids",
            "properties": {
              "productCode": { "type": "string", "description": "A ride, show or attraction product" },
              "outletCode": { "type": "string", "description": "A restaurant, cafe, shop or kiosk outlet" },
              "facilityCode": { "type": "string", "description": "A facility or placed resource" }
            }
          }
        }
      }
    }
  }
}
```

**Codes, not ids, and names resolve at import.** `productCode`, `outletCode` and `facilityCode`
resolve to `VenuePoint.productId` and `outletId` at import; an unresolved code is an import finding,
not a silent drop. `kind` uses `VenuePoint.kind` as it stands, so rides, outlets, retail and facilities
(toilets, first aid, prayer rooms, lockers) need no new vocabulary. Point names stay unique per venue
(audit R108).

### 3. Coordinates: a WGS84 anchor and a local model transform

**One transform, stored once, used both ways.** The model and the navigation file share the model's
local frame (metres, +Y up). The anchor places that frame on the earth:

- **Local to WGS84:** rotate (x, z) by `headingDegrees` into east/north metres, scale, then offset from
  (`originLat`, `originLng`) on a local tangent plane (east-north-up). Over a park (a few kilometres)
  the tangent-plane error is centimetres, below GPS noise.
- **GPS to local:** the inverse, done on the phone for every fix.
- **This is the existing georeference, not a new one.** It maps onto the import's `georeference`:
  `originLat`/`originLng` as given, `rotationDegrees` from `headingDegrees`, `scaleMetresPerUnit` from
  `scale`, `planX = x` and `planY = -z`. `VenuePoint.position` keeps drawing coordinates and latitude and
  longitude stay derived, exactly as the contract already says.
- **Control points check the anchor at import.** More than **3 metres** of residual at any control point
  is a `warning` finding; more than **10 metres** refuses the publish of the 3D layer (the 2D map still
  publishes). Two control points close together are flagged, as the input spec already does for plans.

### 4. How the route is computed

**On the phone, over the published graph** (`getVenueMapGraph`), as GST-021 already specifies:

1. **Shortest path: A\*** over the graph, with straight-line distance as the heuristic and
   `distanceMetres` (along the centreline) as the edge cost. Dijkstra is the fallback where the
   heuristic is not admissible (a multi-floor map with a lift). `stepFreeOnly` routes over the step-free
   subgraph the server returns, never a filtered copy. Closed edges and access-point directions are
   honoured as the contract states.
2. **Snap GPS to the nearest edge.** Each fix is projected into the local frame and onto the nearest
   edge's centreline within a radius of `max(15 m, 1.5 × reported accuracy)`, preferring the edge on the
   current route (hysteresis) so the dot does not jump between parallel paths. The route starts from the
   snapped point: a virtual node on that edge, joined to both its ends.
3. **Re-route** when the snapped position is more than 20 metres off the route for more than 5 seconds,
   or when a newer `graphVersion` arrives with a closure on the route (the guest is told why).
4. **Weak GPS and indoors.** When reported accuracy is worse than 30 metres, or the route runs along an
   `isIndoor` edge, the app switches to **approximate mode**: it keeps the last confident position,
   shows the turn list and the remaining distance, dims the moving dot, and offers **"I am at…"**, a
   tap on a nearby location or a scan of a location's QR sign, to re-anchor. A floor plan is its own
   map (`kind: floor`), so a building is navigated floor by floor. Beacons or other indoor positioning
   are **not** in this decision; they can be added later as another position source behind the same
   snapping step.
5. **No location permission, or outside the venue:** the route is shown from a chosen start (the
   entrance by default) and the camera follows the route, not the guest.

### 5. Offline behaviour

- **The venue pack is downloaded, not streamed on the path.** GLB, navigation graph, POIs and the 2D
  base map are cached per map version, offered for download on wifi and after a ticket is bought for
  that venue, and refreshed at the gate if signal allows. ETags and `VenueMapVersion` decide what to
  fetch again.
- **Routing, snapping and rendering work with no signal.** GPS needs no data connection.
- **What needs signal:** closures and live waits. With no signal the app routes on the cached
  `graphVersion` and says the route may not reflect closures since the time it was fetched, as the
  contract requires.
- **Storage is bounded:** the app keeps the current venue's pack and at most two others, evicting the
  least recently used.

### 6. Performance budget on a mid-range phone

**The reference device** is a mid-range Android phone of about three years old (4 GB RAM, Adreno 610 /
Mali-G57 class GPU) and an iPhone 11. **Targets:**

| | Budget |
|---|---|
| GLB download per map (compressed) | **≤ 25 MB**, a zone ≤ 6 MB; over 40 MB is refused at import |
| Triangles on screen | **≤ 300,000** at LOD0 near the camera, the park as a whole ≤ 1.5 million across LODs |
| Draw calls | ≤ 150 (merged meshes per zone and material; POI markers instanced) |
| Texture memory | ≤ 128 MB after KTX2 transcoding; textures ≤ 2048 px |
| Frame rate | 30 fps sustained while walking; 60 fps where the device allows |
| First render from cache | ≤ 3 seconds to an interactive scene |
| LOD switching | LOD0 within about 80 m of the camera, LOD1 to about 250 m, LOD2 beyond; zones outside the view frustum are not drawn |

- **The app measures itself.** Below 24 fps for 5 seconds, it drops a LOD level; below 20 fps, or on a
  device that fails the WebGL capability check at start, **it falls back to the 2D map with the same
  route**. The guest never loses navigation because the phone is weak.
- **GPS at high accuracy only in walking-navigation mode**, to protect the battery; browsing the map
  uses balanced accuracy.
- **The import checks the budget.** Triangle count, draw calls, texture format and size are measured
  when the file arrives, and a file over budget is an import finding with the number, not a slow app.

### 7. Where the assets are stored

**In the platform's asset store (`assets`, the DAM), per venue, in the tenant's region.** For a UAE
tenant that is **UAE-hosted** storage (the same region as the rest of the tenant's data), served to the
app through the platform's CDN with the delivery rules the asset module already has. The GLB and the
navigation file are `MediaAsset`s uploaded with `createUpload` and `completeUpload` like any drawing,
referenced by the venue map and versioned with it (`VenueMapVersion`), so a published 3D map is always
the model and the graph that were checked together. **No asset leaves the platform for a third-party
map service.**

### 8. Who produces the assets

- **The client or the venue supplies them**: a GLB to the specification above and the navigation file,
  per venue map. Where they do not have one, **they commission it** from a 3D modelling vendor of their
  choice (the minutes already name a 3D vendor, "3DDV", for the seating drawings), working from the
  same CAD plans the venue sends for the 2D map.
- **The platform does not model venues.** It validates what arrives (format, budget, anchor residuals,
  graph connectivity, unresolved catalogue codes) and says exactly what is wrong.
- **A navigation file can be derived** from the 2D map the platform already builds from a CAD plan
  (walkways, points): the export of that graph in the format above is the starting point a 3D vendor
  fills in, so the venue does not describe its paths twice.
- **The request goes to the client** in the Decisions Register ("3D venue model for in-park
  navigation"). **Default until it is answered: 2D park map navigation.**

---

## Options Considered

### Option A: Native, react-three-fiber over the platform's own graph (chosen)

| Dimension | Assessment |
|---|---|
| Complexity | Medium: a 3D scene, a transform and on-device routing, most of it already specified |
| Cost | No licence or per-request cost; the model is the venue's cost |
| Scalability | Per venue map; nothing on the server per guest step |
| Team familiarity | Medium: React Native is the app's stack (ADR-0007); three.js is new to the team |
| Offline | Full, from the cached pack |

**Pros:** No external dependency; data stays in the tenant's region; one graph for 2D and 3D; closures
and step-free routing already specified.
**Cons:** 3D rendering on low-end phones needs a strict budget and a fallback; the venue must produce
the model.

### Option B: An external indoor/outdoor mapping SDK (a commercial venue-mapping or map-tile service)

**Pros:** Ready-made 3D maps and routing.
**Cons:** A licence and a per-venue or per-request cost; venue data and guest positions in a third-party
service, possibly outside the region; a second graph that closures would have to be synced into.
**Rejected in the meeting**: the agreement was "without external mapping integration".

### Option C: 2D only

**Pros:** Already specified; lightest.
**Cons:** Below the benchmark the client named. **Kept as the default and the fallback**, not the goal.

### Option D: Server-side routing

**Pros:** Routing logic in one place.
**Cons:** Fails with no signal, which is where directions are needed; already rejected by the venue-map
contract ("routing is a client concern").

---

## Trade-off Analysis

B buys speed with a dependency the client said no to, and splits the graph. C is safe and below the
bar. D fails in the middle of the park. A reuses the graph, the import pipeline, the asset store and the
offline pattern that exist, and adds only the rendering layer and a file format. Its real cost is the
performance budget, which is why the budget is measured at import and the 2D fallback is automatic.

---

## Consequences

**Easier:** One graph serves 2D, 3D, the visit planner's walking times and the step-free route. A venue
upgrades to 3D by sending two files, without a new integration.
**Harder:** The guest app carries a 3D renderer and must be tested on the reference devices. The import
gains a format with its own findings. Venues without a model need to commission one to get 3D.
**Revisit:** when the first real venue model arrives (check the budget against it), and if indoor
positioning (beacons) is asked for.

---

## Action Items

1. [x] Record the decision (this ADR) and reference it from GST-021 and GST-038 (P02).
2. [x] Ask the client for the model and the navigation file per venue, or who produces them (Decisions Register).
3. [ ] Contract `venue-map.yaml`: `VenueMap.modelAssetId` and `VenueMap.modelTransform` (the anchor); `importVenueGeometry` accepts the navigation file as a source format; import findings for budget, anchor residual and unresolved codes; export of the graph in the navigation-file format.
4. [ ] Contract `assets.yaml`: a `model3d` media kind (`model/gltf-binary`) with its size limit.
5. [ ] `handoff/venue-map-input-spec.md`: a section for the GLB and the navigation file.
6. [ ] Guest app: react-three-fiber scene, LOD and zone loading, snapping, approximate mode, 2D fallback; test on the reference devices.
