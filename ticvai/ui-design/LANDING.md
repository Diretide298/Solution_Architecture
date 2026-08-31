# Handoff: Aster landing page

The entry page for Aster. Five nodes in 3D space — one per layer of the delivery package — that you
scroll through, click into, and back out of. It is the same visual language as the Contracts → Graph
sphere (`GRAPH.md`); read that first, because the renderer here is the same engine at a different
scale, and this document only records what differs.

Design file: `designs/Aster Landing.dc.html`. **Design reference, not production code** — recreate it
in the viewer's own environment (vanilla ES modules, no framework).

## What it is

One full-viewport scene, `min-height:640px`, no page scroll. The wheel does not scroll the document;
it moves through the layers.

- **Overview** — all five clusters visible, the whole graph turning slowly. This is the initial state.
- **Focused** — one cluster, centred and enlarged, its siblings dimmed to 30%. A detail panel appears
  bottom-left with the layer's count, its source folders, a sentence on what it holds, its view tabs,
  and a primary action into the viewer.

Nothing else is on the page. The value of the surface is that it answers "what is in here" in one
picture before anyone has clicked anything.

## The five nodes

Each layer is a cluster: a bright core, a shell of unlabelled motes, and nearest-neighbour filaments.
Mote count is `min(340, 70 + count^0.62 · 8) · density`, cluster radius `0.3 + ln(count) · 0.058` — so
Frontend (364 screens) is visibly the largest body and Decisions (18 ADRs) the smallest, without the
difference being 20:1.

| Layer | Count | Position (x, y, z) | Label | Tint |
|---|---|---|---|---|
| Frontend | 364 screens | −1.45, 0.78, −0.50 | above | teal |
| Contracts | 24 contracts | 0, −0.05, 0.55 | below | **amber** |
| Domain | 38 status enums | 1.50, 0.72, −0.25 | above | teal |
| Backend | 224 tables | 1.15, −0.88, 0.20 | below | pale teal |
| Decisions | 18 ADRs | −1.35, −0.92, −0.55 | below | teal |

Two things in that table are arguments, not decoration:

- **Contracts sits at the origin, nearest the viewer, and is the only amber body.** The package's own
  claim is that the API is the join between the outer layers; the layout says it rather than captioning
  it.
- **Labels alternate above and below** by the `up` flag. The scene rotates, so any two labels that
  share a horizontal band will eventually collide; alternating removes the whole class of collision
  instead of nudging positions until one frame looks right.

Links between clusters (`[0,1] [1,2] [1,3] [2,3] [3,4] [1,4]`) are dashed, flowing, and carry a
travelling packet — the same treatment as an event link in the graph view. When a layer is focused,
links that do not touch it drop to 22%.

## Camera

There is no orbit control. The scene rotates on its own (`yaw = t · 0.075` in overview, slowed to
`t · 0.03` when focused, so a focused cluster does not wander off) with a slow pitch nod of
`−0.2 + sin(t · 0.06) · 0.05`.

Selection moves a **screen-space camera**, not a world camera:

```
UNIT = min(W · 0.175, H · 0.26)      // world unit → px
zoom = 1 (overview) → 2.5 (focused)
anchor = origin (overview) | the focused cluster's position
target = (W · 0.605 | 0.66, H · 0.50 | 0.46) − anchor_projected · UNIT · zoom
```

`x`, `y` and `zoom` each ease toward target at 6–7% per frame. That is the whole transition: no
tween library, no keyframes, and it is interruptible — clicking a second node mid-flight just
retargets. The horizontal bias (60% of width, not 50%) is what keeps the constellation clear of the
hero copy on the left.

## Interaction

| Input | Result |
|---|---|
| Wheel down / up | next / previous layer; past the first, back to overview |
| Click a node | focus it |
| Click the focused node again, or `Enter` | **go in** — `Viewer…#layer=<Name>` |
| Click empty space | back to overview |
| Hover a node | that cluster brightens 25%, cursor becomes a pointer |
| Rail item (right edge) | focus that layer. **Overview** | back out |
| `↓` `→` / `↑` `←` | step through layers |
| `Esc` | back to overview |

Wheel handling is deliberately **discrete**: deltas accumulate, a step fires past ±70, then a 420ms
lock swallows the rest of the gesture. Without the lock a trackpad flick crosses all five layers.
The listener is non-passive and calls `preventDefault()` — the page must not scroll.

Hit testing is on the canvas: the five projected cluster centres are stored each frame and the click
picks the nearest within `max(46px, radius · 1.25)`. The 46px floor exists so the small bodies
(Decisions, Contracts) stay clickable when zoomed out.

## The chrome

- **Hero, top-left, 430px column.** Aster night lockup at 42px, then `Five layers, one reference
  graph.` at 34px/800/−0.028em, a 14.5px/1.62 support line, and two figures — 668 artefacts
  indexed · 1043 operations — as 19px/800 numerals with 11px/600 labels.
- **Rail, right edge, vertically centred.** An `OVERVIEW` button in 9.5px/700 uppercase
  letter-spacing .16em, then one row per layer: name 12.5px/600, mono count, and a 2px bar that grows
  from 12px to 26px and turns bright teal on the active row. It is the affordance that tells a first
  visitor the wheel does something.
- **Detail panel, bottom-left, 428px.** `radius:17px`, `rgba(12,18,21,.82)` + 1px `#1D2C30` border +
  `blur(9px)`, entering on a 0.34s rise. Tinted dot, layer name at 22px/800, `count unit · source`
  line, the blurb at 13.5px/1.62, view chips (`#132227` on `#1E3238`, 11.5px/600), then a teal
  gradient primary into the viewer and a quiet `Back out`.
- **Hint line, bottom-centre**, breathing between 45% and 90% opacity on a 3.4s cycle. Its text
  changes with state — it tells you what to do next, not what the page is.
- A 210px top scrim keeps the hero legible when a bright cluster rotates behind it.

## Tokens

Field: `radial-gradient(130% 100% at 50% 46%, #16262C, #111A1F 34%, #0C1013 68%, #080A0B 100%)`.
Text: `#EDF4F3` primary, `#9CAFAE` body, `#93A6A5` support, `#78908E` / `#6D8482` meta.
Lines and borders: `#1D2C30`, `#223338`, `#1E2C30`. Accent `#48CFCB`, deep `#2BB3B0`, amber
`#E0AE52`. Type: Plus Jakarta Sans 400–800, JetBrains Mono 400/500 for counts. Everything else —
mote and filament colours, the additive blending, the depth maths — is `GRAPH.md`.

## Notes for the build

- **Bind the renderer on the canvas ref**, cancel the previous frame loop, and remove the wheel /
  mousemove / click listeners on teardown. The scene is a permanent `requestAnimationFrame` loop; if
  the page can be navigated away from and back, that loop must die with it.
- **The model is built once.** Only mote density rebuilds it.
- **`prefers-reduced-motion: reduce`** should stop the rotation and the packets and keep the camera
  easing — the easing is the feedback for a click, so it is the one motion worth keeping.
- **Deep links.** Each node's action goes to the viewer's own layer route; carry the layer in the
  URL (`#layer=contracts`) and open the landing page focused on it when it is present, so the page
  is linkable in the state a reader was sent to.
- **The `3D / 2D` tray, top-right**, mirrors the graph view's (`GRAPH.md`). 2D lays the five
  layers out on a plane — Contracts centred, the other four on the corners — with each layer's count
  drawn as a dashed hoop instead of a mote cloud, no rotation, and a gentler focus zoom (1.7 rather
  than 2.5). The 3D scene is the one that sells the scale; the flat one is the one that reads at a
  glance and prints.
- **Going in is two steps, deliberately.** The first click focuses and shows what the layer holds;
  the second opens it. A single click straight into the viewer makes the node a menu item and throws
  away the reason the page exists.
- **Not built:** touch (the wheel has no touch equivalent yet — a horizontal swipe should step, a
  tap should focus), drag-to-spin, and any real data behind the counts. All five counts and the
  668 / 1043 figures are hard-coded from the 21 August index and should come from `/api/index`.
