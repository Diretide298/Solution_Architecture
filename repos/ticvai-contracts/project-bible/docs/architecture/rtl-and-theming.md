# RTL and theming

**Arabic is a mirror, not a translation.** Every one of the twelve platforms declares
`directions: [ltr, rtl]`, and that declaration is currently a claim with nothing behind it.
This is what it has to mean.

---

## Why this is Sprint 1 and not a localisation pass

A translation pass swaps strings. **A direction pass swaps the layout**, and the difference is
that strings can be added to a finished screen while direction cannot.

Retrofitting RTL means revisiting every layout decision made in between — every margin, every
icon, every animation — and the work is roughly linear in the number of screens by then.
Doing it first costs about four days on `design-tokens` and `ui`; doing it after 364 screens
exist costs weeks and produces a worse result, because the retrofit is a search for mistakes
rather than a decision made once.

The client's own hierarchy is emphatic that Arabic is core rather than optional.

---

## What mirrors, and what does not

**This is the part teams get wrong**, so it is written as rules rather than a principle.

| Mirrors | Does not mirror |
|---|---|
| Layout, columns, sidebars, drawers | **Numbers.** `AED 213.75` reads left-to-right in both |
| Text alignment and reading order | **Times and dates.** `09:41` is not `14:90` |
| Icons with a direction — back, forward, next | **Icons with a real-world orientation** — a clock, a padlock, a logo |
| Progress bars, steppers, breadcrumbs | **Media controls.** Play still points the way playback moves |
| Chart axes and category order | **Chart data direction where time is the axis** — time runs the same way |
| Slide-in animation and drawer edges | **Phone numbers, IBANs, codes, QR payloads** |

**The two that cause the most trouble:** a total of `AED 213.75` inside a right-aligned Arabic
line, and a time range `09:00 – 17:00` where the dash must not reverse the operands. Both are
solved by treating numerals and times as embedded LTR runs rather than by mirroring the whole
line.

---

## Rules that belong in `design-tokens`

**No physical direction properties.** `margin-left` becomes `margin-inline-start`, `left`
becomes `inset-inline-start`, `text-align: left` becomes `text-align: start`. A lint rule fails
the build on a physical property, which is the only thing that keeps it true after week two.

**No mirrored icon assets.** The icon set is authored once and mirrored by transform, with an
explicit `no-mirror` list for clocks, padlocks, logos and media controls. Two icon sets diverge.

**Direction is a document attribute, not a class.** `dir="rtl"` on the root, so every logical
property resolves without the component knowing which direction it is in.

**One font stack with Arabic and Latin in it.** The client's reference uses Tajawal for Arabic
alongside a Latin face; the pairing must be chosen once because Arabic and Latin at the same
point size do not look the same size, and matching them is a type decision rather than a CSS
one.

---

## Theming

Three themes, agreed 17 August, and they are **audience-driven rather than a preference
toggle**:

| | Theme | Why |
|---|---|---|
| Guest surfaces — web, app, kiosk | **Light**, white-labelled | The tenant's brand, not ours |
| Staff surfaces — POS, back office, admin | **Light**, TICVAI-branded | Confirmed 14 August: staff UIs carry TICVAI branding |
| Venue Staff App | **Dark** | The client's own employee reference is dark, and staff use it in low light |

**Dark is not an inverted light theme.** The employee reference uses a navy ground with a cyan
accent and its own elevation model; inverting the light tokens produces grey mush and unreadable
disabled states.

**The tenant chooses brand colour; the tenant does not choose the theme.** A guest surface is
light because it is white-labelled and a scanner is dark because of where it is used, and
letting a tenant flip either produces surfaces nobody designed.

---

## What this means per platform

All twelve declare `[ltr, rtl]`. **Three carry a further constraint worth stating.**

**P07 Venue Scanner** renders outdoors in sunlight and at night. Contrast has to survive both,
which is a harder problem than either theme alone and argues for a high-contrast variant rather
than a dark one.

**P05 Guest Kiosk** is white-labelled, so its RTL is the tenant's content mirrored, and the
tenant may supply Arabic content for an English-default venue or the reverse. **The direction
follows the content, not the venue.**

**P13 Venue CMS** authors content in both directions and must preview both. The live-preview
device frame in the client's reference boards needs a direction toggle beside the platform and
theme toggles it already has.

---

## Effort, and what it buys

**Roughly four days** across `design-tokens` and `ui`: logical properties throughout, the icon
mirroring transform and its exception list, the font pairing, the three themes, and a lint rule
that fails a physical property.

**Done in Sprint 1, every screen built after it is bidirectional for free.** Done later, 347
screens need revisiting and the result is a search for mistakes.

## Open

**Which locales ship at go-live.** English and Arabic are certain. The white-label reference
board shows a Francais tab on the policy editor, which implies French, and nobody has confirmed
whether that is a real requirement or a placeholder in a mockup. It changes the font pairing and
the translation-key inventory, not the direction work.
