# The TICVAI motion and interaction vocabulary

Read off `sources/designs/TICVAI_Mobile.dc.html` — 657 KB, **54 screens in one navigable file**,
202 `sc-if`, 181 `sc-for`, 133 `animation:` declarations and 128 `backdrop-filter` uses.

**This is the standard a TICVAI build is measured against.** A frame with a grey box where a
seat map belongs, a table with no empty state, or a payment screen that jumps straight from
"Pay" to "Confirmed" is not a draft of this — it is a different, worse product.

## The 24 named animations

Two house curves carry almost everything: `cubic-bezier(0.2,0.7,0.2,1)` for entrances and
`cubic-bezier(0.2,0.8,0.2,1)` for anything that overshoots. Durations sit between 180 ms and
620 ms; only ambient loops run longer.

| animation | what it does | where it belongs |
|---|---|---|
| `tvScreenIn` | opacity 0 → 1, 300 ms | every screen change |
| `tvRise` | up 18 px + scale 0.99, 560–620 ms | a screen's first content block |
| `tvUp` | up 10 px, 500 ms | confirmation headings |
| `tvFade` | opacity only, 180–220 ms | overlays, sticky bars appearing |
| `tvStagger` | up 12 px | list items, one after another |
| `tvSlideIn` | in from −16 px, 460 ms + 50 ms per item | horizontal tile rows |
| `tvDetailIn` | scale 1.08 → 1, 460 ms, origin 50% 30% | opening a detail screen |
| `tvDetailBody` | up 18 px, 560 ms, 140 ms delay | the body under a detail hero |
| `tvSlowZoom` | scale 1 → 1.12 over 14–20 s, alternating | hero photography, always moving |
| `tvSheet` | translateY 100% → 0, 240 ms | every bottom sheet |
| `tvPop` | scale 0.84 → 1.05 → 1, 380 ms | tab bar icon on selection |
| `tvToast` | up 16 px + scale 0.96, 260 ms | the toast |
| `tvSpin` | 360°, 800–900 ms linear | every spinner |
| `tvBar` | translateX −100% → 320%, 1200 ms | indeterminate progress |
| `tvGlow` | box-shadow ring 0 → 9 px → 0, 2.8 s | the primary CTA, resting |
| `tvFloat` | ±4 px, 3.4 s | a badge that should feel alive |
| `tvCheckPop` | scale 0.4 rot −20° → 1.18 rot 6° → 1, 620 ms | the success tick |
| `tvConfetti` | translate to `--tvx`/`--tvy`, rotate 220°, scale 0.3, fade | six pieces behind every success |
| `tvLovePop` | scale 0.4 → 1.12 → 1 → 0.9, rises and fades, 900 ms | saving to a wishlist |
| `tvMascotBob` | ±8 px, 1.1 s | mascot while waiting |
| `tvSadIn` / `tvSadDroop` / `tvTear` | enter, rock ±2°, tear falls | the abandon-booking sequence |
| `tvHero` | scale 1.025 → 1 | hero settle |

**`@media (prefers-reduced-motion: reduce) { * { animation: none !important } }`** closes the
block. It is not optional and it is one line.

## The 24 interaction mechanisms

Every one of these exists in the build. None is a placeholder.

**Motion and feedback**
- **Swipeable card deck** — three cards, the front one draggable via `onPointerDown/Move/Up`;
  drag rotates by `dx/18`, past 60 px it advances. Auto-advances every 4.2 s, and a touch
  pauses that for 6 s.
- **Scroll-reactive header** — a translucent bar fades in past 24 px; on detail screens the
  title crossfades in past 560 px while the back pill swaps from dark glass to surface.
- **Toast** — one line, bottom, 2.2 s.
- **Lightbox** — tap a gallery image, it fills the frame, `cursor: zoom-out`.

**Waiting, honestly**
- **Loading overlay** — glass card, pulsing ring plus spinner plus indeterminate bar, and a
  label that says what is happening: *"Checking live availability"*, *"Holding your place in
  the queue"*. Never a bare spinner.
- **Payment as five states** — `device → auth → 3ds → verify → done`. The auth step names its
  three sub-steps one at a time (*contacting your bank, securing the connection, requesting
  authorisation*). 3-D Secure renders six OTP boxes with a resend countdown. Only then the
  tick and confetti.

**Structure**
- **Bottom sheets** for filters, the cart, the AI chat, the calendar, the pass buyer.
- **Stepper chips** across a booking: done steps show a tick and are tappable, the current one
  is filled, later ones are inert.
- **Seat map** — real rows, taken seats derived from a stable hash, a legend, zone pricing, and
  a collapsible summary listing each seat as a Sec/Row/Seat card with a remove button.
- **Calendar** — month grid with a demand dot per day: green quiet, amber moderate, red peak.
- **Empty states** — illustration, one sentence, a CTA, and a "You might like" list underneath.
  Never a bare "No results".
- **Tab bar** — glass pill, icon fills on selection, label appears only when active, count badge.

**Content**
- **AI chat** — mascot avatar, message bubbles, input with send-on-enter.
- **Mascot states** — idle, curious, success, love, sad, walk 1–3, crying. It carries the tone.
- **Exit-intent modal** — leaving a half-finished booking asks once, warmly, then plays the sad
  walk-off if you go.
- **Virtual queue** — live position, progress bar, return window, refresh that actually moves.

**System**
- **Theme** — auto / dark / light, all colour through `--tv-*` tokens, never a hard-coded hex
  outside the brand blue `#083E8F`.
- **RTL** — Arabic flips the whole app; numerals and codes stay LTR with `unicode-bidi: isolate`.
- **Four languages** — English, Arabic, Chinese, Russian.
- **Glass** — `backdrop-filter: blur(18–22px) saturate(180%)` with an inset top highlight, used
  128 times. It is the surface treatment, not an accent.

## What "not a skeleton" means, concretely

A screen is finished when it has all five:

1. **Real seeded content** — AED prices, real names, real dates, plausible counts.
2. **Every declared state drawn** — loading, empty, error, offline, denied. The empty state is
   a designed screen, not a missing one.
3. **Motion on entry and on change** — at minimum `tvScreenIn`, plus `tvRise` on first content.
4. **Feedback for every action** — a control that can be refused says so before it is pressed;
   one that takes time shows what it is doing.
5. **Density that matches the operator** — a gate scanner in sunlight is not an analyst's report.

## Two things this file does NOT carry

**It does not render standalone.** It expects eight siblings that did not ship with it:
`ticvai-theme.css`, `ticvai-data.js`, `ticvai-i18n.js`, `image-slot.js`, `support.js`,
`_ds/nocturne-…/styles.css`, `_ds/nocturne-…/_ds_bundle.js` and an `images/` folder. Opened
alone it is unstyled and empty. **Ask for those files before treating it as a running
reference** — as a source of patterns it is complete without them.

**Its data is its own.** Falcon Bay, Sahli, the fictional cities and the seeded catalogue are
demo content, not the platform's. Take the mechanisms; leave the fixtures.
