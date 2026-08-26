# Storyboards against our screens — merges and gaps

**18 August 2026.** 90 storyboard panels mapped against 376 screens: 8 guest boards and employee
board 1. Employee boards 2–6 unread.

**The guest app maps almost panel for panel.** `GST-001` through `GST-060` follow boards 3–8 in
order, which is unsurprising — they were named from the same source. **The value was in the three
places they do not line up.**

---

## Merged — two screens that were one

### `GST-064` folded into `GST-036` — Loyalty & Rewards

**I created `GST-064` in the parity sweep on 17 August without noticing `GST-036` already
existed.** Same two operations, same capability, both named *Loyalty & Rewards*.

Board 6 panel 6 shows one loyalty screen. **The duplicate survived a full audit that same day**
and was found by matching against the storyboard, not by any checker — because two screens with
different ids and identical purpose is not a defect any rule was looking for.

`GST-036` kept, with `GST-064`'s better purpose and states and its Wave 2.

### `GST-060` folded into `GST-047` — Maintenance / Upgrade Page

The storyboard draws it twice, on board 7 panel 7 and board 8 panel 10. **That is a board
convention for a screen every journey can land on, not two screens** — and we had made two of
them, with the same single operation and the same purpose.

**P02 is now 63 screens; the package is 374.**

---

## Checked and deliberately kept separate

### `GST-050` and `GST-058` — cabana

Board 7 panel 10 is one cabana with a price and a Book Now. Board 8 panel 8 is availability
across areas with counts remaining.

**A detail and a list, not a duplicate.** Merging them would put a booking action on a browsing
screen, and the storyboard separates them for that reason.

---

## 🔴 Ten screens carry an entire contract

The median screen has **four** operations. These have all of one:

| | | |
|---|---|---|
| `ADM-016` `ADM-017` `ADM-018` | P09 | **all 41 white-label operations** |
| `SUP-006` Knowledge Base Search | P12 | all 41 white-label operations |
| `CMS-003` Typography · `CMS-006` Component Preview | P13 | all 41 white-label operations |
| `POS-010` · `EMP-036` · `BO-027` · `CMS-010` | four platforms | all 10 assets operations |

**A Typography screen does not create banners, delete content pages or manage domains.** A
knowledge-base search on the support console does not configure a tenant's branding at all.

This is CF-87 recurring in a different shape. That one attached sibling *operations* to guest
screens; this attaches a whole *contract* to any screen whose module resembles it. **It passed
every validator, because each operation exists, resolves to a real table and carries a permission
the screen's platform is entitled to.**

**Not fixed here.** Six of the ten are white-label and the right split follows the storyboard —
boards 1 and 2 name ten builder screens each, and those names are the natural boundaries. That is
a session of work, not a patch. Raised as **CF-114**.

---

## 🔴 The white-label builder is drawn as tenant-facing and specified as platform-facing

Boards 1 and 2 are unambiguous: *"Tenant: Dubai Museum (Demo)"*, a **Publish Changes** button, a
version history with *Restore Previous Version*, and a live mobile preview. **A tenant using it,
unaccompanied.**

Our white-label operations sit on `ADM-016`–`ADM-018` on **P09 TICVAI Web** — the platform admin
console — as well as on P13.

**Whether a tenant self-serves their own branding or TICVAI does it for them is a commercial
question, not a layout one.** It changes who is trained, who is blamed for a broken theme, and
whether a venue can rebrand on a Friday without raising a ticket. **The client has been shown
self-service.** CF-114.

---

## Gaps the mapping found, and the ones that were my matcher

**Most apparent gaps were fuzzy-match failures** — CMS *Brand Kit* is the storyboard's *Brand
Identity*, *Typography* is *Font Management*, employee *Sign in* is *Login / SSO / Biometric*.

Three are real:

| | |
|---|---|
| **Employee — Universal Search** (E1.7) | `searchCatalogue` exists and reaches only guest surfaces. **A steward looking up an asset, a work order or a colleague has no search**, and board E1 panel 7 draws one over all of them |
| **Employee — More / Role-Based Modules** (E1.4) | A module grid gated by role. `resolvePermissions` reaches no screen at all |
| **Employee — Create Request Hub** (E1.8) | Nine request types behind one entry — maintenance, IT, cleaning, security, stock, equipment, purchase, leave, other. We have the individual operations and no front door |

---

## What this exercise was worth

**One duplicate I created, one duplicate we inherited, ten screens with a contract bolted on, and
a commercial question about who owns white-label.** None of the four was findable by any rule in
the package, and all four came from reading pictures the tooling could not.
