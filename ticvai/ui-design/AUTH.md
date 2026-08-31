# Auth pages — Aster

Covers the **invite** page and the **sign-in** page, each in a night and a day variant. They share
one background (the animated node field, specified under *The node field*), one card language and
one palette; the sign-in page adds a second column.

## Invite page

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


# Sign-in page

- `designs/Aster Sign In.dc.html` — night
- `designs/Aster Sign In Day.dc.html` — day

Replaces `viewer/public/login.html`. The existing states (`#checking`, `#bootstrap`, `#signin`)
still apply; the design shows **signin**. The bootstrap state reuses the same card with its four
fields and the "Create the administrator" button.

## Layout
`display:grid; grid-template-columns: minmax(420px,7fr) 9fr`, full viewport height. The node-field
canvas and its scrim span the whole grid, behind both columns; the scrim's radial centre is offset
to **22% 45%** so the lattice stays visible on the right while the form side stays quiet.

**Left column** — the form, centred, `max-width:396px`, `gap:24px`. Lockup at 58px, then the title
(26px/800), a one-paragraph explanation, the two fields, the button, the invitation note, and the
powered-by strip. The password label carries a right-aligned **Forgot?** link in the same row as
the label text (`flex` with a spacer, so the link stays on the baseline).

**Right column** — the demonstration, `padding:48px 56px 48px 20px`:
1. An eyebrow (`THE CONTEXT LAYER`, 10.5px/700, letter-spacing .16em, teal) over a 19px/600 line
   of positioning copy at `max-width:520px`.
2. The **editor window** — `max-width:640px`, `radius:16px`, translucent, blurred, with a title bar
   (three dots, the file path in mono, the language in small caps, and a live status pill), a code
   body, and a findings tray.
3. Four stats — value in mono 19px, label in 10px/700 letter-spacing-.13em uppercase. The numbers
   are properties of the product, not of any one package (12 file types read · 1 graph · 0 bytes
   uploaded · 100% local), because the sign-in page is seen before a package is loaded.

## The typing animation
A single `setInterval` at **46ms** drives a four-part state: `{ scene, step, chars, findings }`.

Each tick does exactly one thing, in this order:
1. If the current line is not fully typed, advance `chars` by **3** (so it types in bursts, not
   letter-by-letter — a character-per-tick reads as too slow at this line length).
2. Otherwise move to the next line and reset `chars`.
3. When all 9 lines are typed, reveal one more finding chip per tick.
4. When the findings are exhausted, jump to a **different** scene chosen at random —
   `while (n === s.scene) n = random()` — so it never plays the same file twice in a row. The
   first scene is also chosen at random on mount, so two people signing in do not see the same thing.

**Scenes** — six, one per language the package actually contains: `orders.yaml` (OpenAPI),
`resolve_refs.py` (Python), `OrderStateMachine.java` (Java), `0041_seat_holds.sql` (SQL),
`useAvailability.ts` (TypeScript), `WEB-002.json` (JSON). Each is 9 lines and carries its own
findings — every one a real fact from the package (the illegal `HELD → REFUNDED` pair, the 192
screens that reach nothing, the 6 tables written by two services). Nothing is lorem.

**Colouring.** Lines are authored as `[text, token]` where the token is one of
`com | key | val | acc | warn`, and `renderVals` maps tokens to hex through a single `pal` object.
That is what lets the night and day files carry identical scene data with different palettes:

| Token | Night | Day |
|---|---|---|
| com (comment, import) | #8A9899 | #8A9899 |
| key (keyword, structure) | #8FB6B7 | #3E7C7E |
| val (value, literal) | #C8D4D4 | #31474C |
| acc (the line that matters) | #48CFCB | #12878A |
| warn (the finding) | #D9A143 | #9A6B18 |

**Caret** — a 7×14px block on the active line only, blinking via
`@keyframes aster-caret` at `1s steps(1) infinite`.

**Findings** rise in with `@keyframes aster-rise` (.35s, 6px). Two tones: **ok** teal, **warn** amber.

**Layout stability** — the code body is a `grid` of `30px minmax(0,1fr)` with
`min-height:238px; align-content:start`, and the findings tray has `min-height:56px`. Both are
fixed so the window does not resize as lines and chips appear. All 9 line rows render from the
first frame; untyped ones are empty strings.

**Reduced motion** — skip the interval and render the last scene fully typed with all findings shown.
