# Accessibility

**26 requirements, no criteria and no audit plan.** This is the standard we propose and what
it means for each surface.

## The standard

**WCAG 2.2 Level AA.** It is what UAE public-facing digital services are measured against, it
is what a procurement team will ask for, and AAA is not achievable for a seat map or a live
queue board.

## Where it bites, per surface

| Surface | The hard part |
|---|---|
| **Guest Kiosk** | **Physical, not just software.** Reach height, screen angle and a tactile or audio path for a guest who cannot see the screen. A kiosk that is only reachable standing excludes a wheelchair user regardless of contrast |
| **Guest Web / App** | The purchase path must be completable by keyboard and screen reader end to end. **A seat map is the hard case** — it needs a list-based equivalent, not a described image |
| **Venue Scanner** | Sunlight and night in one device. High contrast, and audible confirmation so a steward does not have to read a screen in glare |
| **Venue POS** | Speed and accessibility pull against each other. Keyboard-first helps both |
| **Venue Staff App** | Dark theme must still meet contrast. **Inverting a light theme does not** |
| **Back office** | Data tables, which are where screen-reader support is usually worst |

## Non-negotiables

**Every interactive element reachable by keyboard**, in a visible order. This is the one that
cannot be retrofitted cheaply.

**Colour is never the only signal.** A red row and a green row are the same row to a colour-blind
user, and the status pill vocabulary from the client's reference already carries text.

**Contrast 4.5:1 for text.** Checked in the token set rather than per screen, so it cannot
regress.

**Every form field has a label**, not a placeholder. A placeholder disappears when typing begins
and is not read reliably.

**Errors are announced, not just shown.** A refusal a screen reader does not announce is a form
that silently failed.

## The audit plan

| When | What |
|---|---|
| Per component, in CI | Automated checks in the `ui` package. **Catches roughly a third** and catches it early |
| Per flow, before release | Keyboard and screen-reader walkthrough of the twelve flows. Automated tools cannot tell whether a journey is completable |
| Before go-live | Independent audit of the guest surfaces and the kiosk |
| **Kiosk** | **A physical assessment**, which is not a software test and needs the hardware in place |

## Open

**Whether an independent audit is contracted**, and by whom. It is the one item here with a
cost and a lead time, and it belongs in the plan rather than discovered near go-live.
