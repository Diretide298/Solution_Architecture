# Invite page — Aster

Two files, one design: a **night** invite and a **day** invite. Same layout, same copy, same
animated background; only the palette changes.

- `designs/Aster Invite.dc.html` — night
- `designs/Aster Invite Day.dc.html` — day

Replaces `viewer/public/invite.html`. The three states the current page already has
(`#checking`, `#refused`, `#form`) still apply — the design shows the **form** state. Keep the
existing rule: never a form over an invalid link.

## Layout
A full-viewport stage, `display:flex; align-items:center; justify-content:center`, `padding:48px 24px`,
`overflow:hidden`. Three stacked layers:

1. `<canvas>` pinned `position:absolute; inset:0` at 100% × 100% — the node field.
2. A radial scrim over it, `pointer-events:none`, transparent at the centre and opaque at the
   edges. It sinks the lattice behind the card without hiding it:
   night `radial-gradient(ellipse at 50% 45%, rgba(8,11,12,0) 0%, rgba(8,11,12,.45) 62%, rgba(8,11,12,.85) 100%)`;
   day the same stops in `rgba(238,242,243, …)`.
3. The card, `position:relative` so it sits above both.

**Card** — `max-width:452px`, `radius:18px`, `padding:34px 34px 28px`, `display:flex;
flex-direction:column; gap:22px`, `backdrop-filter:blur(14px)`, translucent fill so the lattice
shows faintly through it. Contents in order: lockup · title + invite note · three fields · submit ·
fine print · powered-by strip.

- Title 23px/800/-0.02em; note 13.5px/1.6 with the invited address at 600 in the stronger text tone.
- Fields: a 10.5px/700 letter-spacing-.13em uppercase label over an input at 14px,
  `radius:11px; padding:12px 14px`, 1px border, teal border on focus. Labels are `<label>`-wrapped.
- Submit: full width, `radius:11px; padding:13px 18px`, 14.5px/700, teal gradient, dark ink,
  teal glow that strengthens on hover.
- Powered-by strip: 1px top rule, the two-ring AinfiniteCore mark (CSS, not an asset), the
  wordmark, then the Softlabs logo pushed right.

## The node field
One `<canvas>`, seeded randomly on every load and on every resize, so no two visits draw the same
lattice. Written in `componentDidMount`, torn down in `componentWillUnmount`
(`cancelAnimationFrame` + `ResizeObserver.disconnect`).

**Seeding.** `count = min(240, (W × H) / 6800) × density`. Each node gets a random position, a
velocity in ±0.16 px/frame on each axis, a radius of 1.3–3.4px, a twinkle phase and speed, and an
8% chance of being a **hub** — brighter, with a radial glow.

**Per frame.**
1. Beams (behind everything): at most 3 alive, spawned at ~0.6% chance per frame from the top or
   left edge at a 0.5–1.15 rad angle. Each is a long round-capped stroke, 22–74px wide, drawn with
   a three-stop gradient that is transparent at both ends, and fades in and out over its life via
   `sin(life/max × π)`. Night composites them `lighter`; day composites `multiply`, or they wash out.
2. Nodes advance by their velocity and wrap 40px outside each edge.
3. **Edges are recomputed every frame** — every pair closer than `linkDistance` (default 168px) is
   stroked, with alpha scaled by `1 − d/linkDistance` so links fade in as nodes approach and fade
   out as they part. That is what makes the lattice continuously form and dissolve; there is no
   fixed edge list. A cheap `abs(dx) > dist || abs(dy) > dist` test skips most pairs before the
   square root. Hub-touching edges are brighter and 1.2px; ordinary edges 0.85px.
4. Nodes draw last: hubs get a radial glow at 9× their radius, then every node draws with alpha
   modulated by its own twinkle.

Canvas is sized at `min(devicePixelRatio, 2)` and the context scaled to match, so it stays sharp
on retina without paying for 3x.

**Tunable props** (already exposed): `density` 0.4–1.8, `linkDistance` 90–260, `beams` on/off.

**Cost.** The edge pass is O(n²) — ~240 nodes is ~29k distance tests per frame, which is fine on a
desktop invite page. If it needs to run on low-end mobile, drop `density` to ~0.6 or bucket the
nodes into a grid and only test neighbouring cells. Respect `prefers-reduced-motion`: skip the
`requestAnimationFrame` loop and paint one static frame.

## Palette
| Role | Night | Day |
|---|---|---|
| stage | #080B0C | #EEF2F3 |
| card | rgba(18,23,25,.82) | rgba(255,255,255,.88) |
| card border | rgba(72,207,203,.16) | rgba(31,143,145,.18) |
| card shadow | `0 24px 70px rgba(0,0,0,.6)` | `0 22px 60px rgba(21,43,49,.14)` |
| title | #EDF2F2 | #16323A |
| body | #96A3A4 | #5F7274 |
| strong body | #CFDADA | #2A4A50 |
| label | #7E8C8D | #6C7D7F |
| input fill / border | #0E1314 / #24302F | #F7FAFA / #DBE3E4 |
| focus border | #2BB3B0 | #1F8F91 |
| button | `linear-gradient(135deg,#2BB3B0,#48CFCB)` on #04211F | `linear-gradient(135deg,#1F8F91,#3FC9C5)` on #04211F |
| hub node | rgba(160,245,242,·) | rgba(14,105,107,·) |
| node | rgba(88,216,212,·) | rgba(36,150,152,·) |
| hub edge | rgba(110,232,228,·) | rgba(20,120,122,·) |
| edge | rgba(72,178,180,·) | rgba(60,140,142,·) |
| beam | rgba(150,235,232,·) | rgba(70,195,192,·) |

## Brand
Night uses `brand/aster-lockup-night.png` at 44px tall. Day cannot — that lockup's wordmark is
white — so it composes the mark and the wordmark: `brand/aster-mark-day.png` at 44px, a 1px
rule, then `Aster` in **Montserrat Light**, 22px, letter-spacing .3em, #16323A. If a dark-wordmark
lockup gets produced later, swap it in and drop the composed version.
