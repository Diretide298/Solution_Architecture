# Contracts → Graph: the rotating sphere

Spec for the Spine scope of the contract graph. It replaces the flat placed-ring layout in
`public/graph.js` (`renderSpine()` and its `SPINE_RING` / `SATELLITE_RING` placement) for that
scope only; Files, Schemas, Permissions and Local keep the existing force renderer.

The executable reference is `buildGalaxy()` and `drawGalaxy()` in
`designs/Viewer Redesign - Topbar Night.dc.html`. Every constant below is lifted from there, and the
day file is byte-identical in this area. Read that source alongside this document — it is shorter
than the prose.

## Why canvas, and why a sphere

The old Spine view was two placed rings on a 2D plane. It was correct and it read as a diagram of
nothing in particular: 24 dots and 22 lines, all the same weight, no sense of a system with a
centre. The sphere carries three things the rings could not:

- **Volume.** 24 contracts is the visible layer; the ~1000 operations, schemas and permissions
  underneath it are the mass. Drawing that mass as unlabelled motes says "this is bigger than the
  labels" without adding 1000 things to read.
- **Motion as evidence.** The event links pulse a packet from publisher to consumer, so the
  direction that mattered most in the old view — and was invisible there, because the arrowheads
  were painted the background colour — is now the thing the eye follows first.
- **Rotation instead of a legend about depth.** A static 3D projection is a puzzle; a slow turn
  resolves it for free.

It is DOM-free by necessity. 900 motes, ~1300 filaments and 22 animated links is ~2200 painted
primitives per frame; as elements that is a dead tab.

## Geometry

One unit sphere in model space, projected per frame. No physics, no layout pass, nothing cached
per frame — the model is built once and only the projection runs at 60fps.

**Hubs — the 24 contracts.** Placed by Fibonacci spiral so they are evenly spread with no clumping
and no seams:

```
GOLD = π(3 − √5)
y    = 1 − (i / (n − 1)) · 2        // i = index + 0.5, n = 24
rad  = √(1 − y²)
θ    = GOLD · i
p    = (cos θ · rad, y, sin θ · rad) · shell
```

`shell` is `1` for spine and satellite contracts and **`0.34` for the two shared ones** — that is
the whole visual argument of the view: `shared/common` and `shared/permissions` sit inside
everything else, and nothing else does.

Hub radius is the operation count, compressed: `r = 1.5 + ops^0.55 · 0.3`. The exponent matters —
linear sizing makes `catalogue` (73 ops) eleven times the area of `queue` (25), which reads as
importance nobody claimed.

**Motes — the mass.** 900 points from a seeded PRNG (`seed = 20260821`, LCG
`1103515245 / 12345 / 2^31`) so the field is identical on every load and between the two themes.
Uniform on the sphere via `u = 2·rnd − 1`, `θ = 2π·rnd`:

- 78% are **shell** motes at `0.9 ± 0.075` — this is what gives the silhouette a defined edge
- 22% are **interior** at `0.3 … 0.82`, which is what stops the middle reading as an empty balloon
- radius `0.35 … 1.3`, a per-mote twinkle phase, and 10% flagged `hot` (drawn brighter)

**Filaments.** Each mote is joined to its **three nearest neighbours within `d² < 0.011`**,
deduplicated by index (`j > i`). Computed once, O(n²) over 900 points — about 40ms at build time
and never again. This is the only structure in the picture that is not data: it is texture, and it
is honest about that by carrying no colour coding at all.

**Event links.** The 22 pairs from the delivery's own event catalogue, hub centre to hub centre,
each flagged critical or not.

## Projection

```
yaw   = t · 0.11                        // radians/sec — one turn in ~57s
pitch = −0.34 + sin(t · 0.07) · 0.06    // a slow nod, so the poles never sit still
R     = min(W · 0.30, H · 0.37)
c     = (W / 2, H · 0.43)               // lifted above centre: the legend strip owns the foot
FOV   = 3.1
```

Rotate about Y by `yaw`, then about X by `pitch`, then

```
k  = FOV / (FOV + z · 1.35)             // perspective factor, also the per-point scale
sx = cx + x · R · k
sy = cy + y · R · k
```

`k` is reused as the size multiplier for every primitive at that point, which is what makes the
front of the sphere read as nearer rather than merely brighter. Negative `z` is towards the viewer
throughout; every depth expression below reads `−z` as "near".

No z-sorting. Everything is drawn with `globalCompositeOperation = 'lighter'` and depth-scaled
alpha, so overlap accumulates light instead of needing an order — additive blending is why this
looks like a nebula rather than a scatter plot. Labels are the exception and are drawn last, in
`source-over`.

## Draw order, per frame

1. **Filaments** — `rgba(120,214,210, 0.15 − depth·0.08)`, `lineWidth 0.5`.
2. **Motes** — a 3-stop radial gradient out to `r·k·2.4`: white-teal core
   (`224,250,248` hot / `150,232,228` ordinary), `rgba(96,214,210, α·0.45)` at the halfway stop,
   transparent teal at the rim. Alpha `(0.5 − z·0.3) · twinkle`, where
   `twinkle = 0.55 + sin(t·1.4 + phase)·0.3`, doubled for `hot`. Minimum on-screen radius 0.4px so
   the back of the sphere stays a field rather than dropping out.
3. **Event links** — dashed `[2.4, 7]` with `lineDashOffset` marching at `26` (critical) or `17`
   px/sec, so the lane itself flows. Amber `224,174,82` critical, teal `120,214,210` otherwise,
   alpha `max(0.04, 0.34 − depth·0.22)`.
4. **Packets** — one per link, a radial-gradient dot travelling A → B on
   `(t · 0.34 | 0.22 + i · 0.13) mod 1`, radius `(2.6 | 1.9) · k̄ · 3`. A → B is
   publisher → consumer; the direction is the payload, so do not symmetrise it.
5. **Hubs** — gradient out to `r·k·2.8` (core colour at 0, tier colour at 0.3, transparent at the
   rim) plus a hard core disc at `r·k·0.8`. `front = max(0.24, 0.9 − z·0.55)` scales both. A
   breathing pulse of ±9% (spine, core) or ±4% (satellite) at `sin(t·1.6 + i)`.
6. **Labels** — `600 10.5px Plus Jakarta Sans`, centred, `sy + r·k·2.2 + 12`. Drawn **only where
   `z ≤ 0.1`**: near face and the terminator, nothing behind. Alpha
   `max(0.22, 0.92 − (z+1)·0.36)`.

## Palette

| Element | Colour |
|---|---|
| spine hub | core `214,248,246` · body `72,207,203` |
| satellite hub | core `175,235,232` · body `43,179,176` |
| shared hub (inner shell) | core `252,230,184` · body `224,174,82` |
| mote | `150,232,228`, hot `224,250,248`, mid-stop `96,214,210` |
| filament | `120,214,210` |
| critical event link + packet | `224,174,82` · packet `255,224,166` |
| ordinary event link + packet | `120,214,210` · packet `207,247,245` |
| label | `226,242,241` |
| field | `#16262C → #111A1F → #0D1113 → #0A0C0E` |

## Implementation notes

- **Bind on the ref, not on mount.** The canvas element arrives and departs as the view switches;
  the design binds in a ref callback, guards on element identity, cancels the previous
  `requestAnimationFrame` and only then starts a new one. Cancel in `componentWillUnmount` /
  the view teardown, or every visit to the Graph view leaves another loop running.
- **Size from `getBoundingClientRect()` every frame**, and set `canvas.width/height` only when it
  actually changed. That covers the sidebar collapsing, the links pane toggling and a window
  resize without a ResizeObserver.
- **`devicePixelRatio` capped at 2.** At 3 the mote count starts costing real milliseconds for no
  visible gain.
- **`setTransform(dpr,0,0,dpr,0,0)`** each frame, then draw in CSS pixels — every constant above is
  a CSS pixel.
- **The model is built once** and survives re-renders; only rebuild it if the contract set changes.
- **Reduced motion.** `prefers-reduced-motion: reduce` should hold `t` at a fixed 4.2s and draw a
  single frame: same picture, no rotation, no packets. Not in the design files — add it in the app.
- **Interaction is not built.** Hover-to-isolate, click-to-select and drag-to-spin are all
  reasonable next steps, and all of them need a hit test the design does not have: project the 24
  hubs into screen space each frame, keep the array, and pick the nearest within ~14px. Do that
  before wiring the toolbar's Labels / Shared $refs toggles to it.
- **The `Fit` button has no job here** — a sphere is always framed. Either drop it in this scope or
  repurpose it as a zoom reset once drag-spin exists.

## 2D mode

The toolbar carries a `3D / 2D` tray (mono 11.5px, same tray treatment as the scope tabs) and the
state is one field, `graphMode`. **2D is not a different diagram — it is the same model with the
projection switched off**, which is why it costs about fifteen lines rather than a second renderer:

- every hub carries a plane coordinate alongside its sphere coordinate, assigned once in
  `buildGalaxy()`: spine on a ring at `0.56`, satellites at `1`, the two shared contracts at
  `0.17`, evenly spaced by index, satellites offset `+0.22rad` so they do not sit on the spokes
- in 2D, `hp` reads those coordinates through `flatPos()` at `FR = min(W·0.34, H·0.36)` with
  `k = 1, z = 0`, so every depth expression downstream evaluates flat and unchanged
- the motes and their filaments are skipped entirely, the two rings are drawn as dashed guides, and
  hub radii scale ×1.5 to hold the picture together without the dust behind them
- event links, dash flow and packets are identical in both modes

Keep both. 3D is the view that says how big the system is; 2D is the one you screenshot into a
document, and the one that stays legible at 500px tall.

## Entry from the landing page

The graph is reachable directly: the landing page links to `#layer=Contracts`, and the shell reads
`/layer=([A-Za-z]+)/` off the hash on mount and on `hashchange`, setting the layer and that
layer's first view. Case-insensitive, ignored if it names no layer. In the real app this folds into
the existing hash routing rather than adding a second scheme — `app.js` already owns node ids in
the hash, so treat `layer=` as one more key it parses.
