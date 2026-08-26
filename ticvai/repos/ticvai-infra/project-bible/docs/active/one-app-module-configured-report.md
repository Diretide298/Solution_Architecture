# One app, configured by module — does the package already do this?

**Asked 24 August: F&B should not be its own app. It should be the same app, installed once and
configured — select F&B and the F&B modules appear. Same for POS across ticketing and retail.**

**Short answer: the direction is already the package's direction, the licensing machinery to
support it is built, and the screen layer does not use it.** Three of five pieces exist. Two are
missing, and one of the two is the reason platform count keeps climbing.

---

## What already works

### Apps already serve several platforms

**`venue-management-web` serves three** — P08 back office, P13 white-label CMS, P16 analytics.
**`guest-app` serves two** — P02 mobile and P05 kiosk.

**A platform in this package is a navigation and permission boundary, not a codebase**, and it has
been since P16 was written. **The pattern you are describing is the one already in use; it has
just never been stated as a rule.**

### Licensing decides what a tenant may use

`getTenantLicences` returns a `LicencePosition` — **the union of the plan's modules and any
add-ons** — and its own description says it plainly:

> *The authoritative source for module enablement. Two places deciding what a tenant may use is one
> place too many.*

`addLicenceAddOn` and `removeLicenceAddOn` change it. `LicenceAddOn` carries a `moduleKey`, a price
and a validity window. **The commercial half of "select F&B and F&B appears" is done.**

### Enablement decides what a tenant has turned on

`getModuleEnablement` and `setModuleEnablement` sit on top: **licensed and enabled are separate
states**, and a module that is not licensed cannot be enabled.

`setModuleEnablement` already refuses to disable a module that navigation or the homepage
references, **and names the references so the tenant can clear them first** — which is the exact
failure mode of a modular app, caught in the contract.

**A disabled module is hidden entirely, not greyed out.** That decision is already made and it is
the right one.

---

## What is missing

### 🔴 No screen declares which module it needs

**This is the gap that matters.** 476 screens carry a `module` field and it is **prose, not a key**
— 38 distinct values, 124 of them literally `TODO`, and the rest a mixture of section names
(`Sell`, `Orders & Money`) and domain names (`Kitchen`, `Floor Service`).

**Nothing connects `screen.module` to `LicencePosition.licensedModules`.** A tenant without an F&B
licence would still be served every F&B screen, because no screen says it belongs to F&B in a form
the licence can match.

**This is one field and a vocabulary**, and it is what turns the direction into a mechanism:
`requiresModule: fnb` on the 62 F&B screens, checked against the licence at navigation build time.

### 🔴 Roles are barely on the screens

**16 of 476 screens declare a permission.** The permission model is complete —
`identity.role_permission` was fixed on 20 August, `Role.permissions` exists, ADR-0002 makes
authorisation user-driven rather than workstation-driven — **and the screens do not use it.**

Your description has two gates: *"configured to login and modules they can use"*. **The module gate
has no hook; the role gate has a hook on 3% of screens.**

---

## What this direction would change, and what it would not

**It would not change the contracts.** 966 operations already carry `x-ticvai-permission` and
`x-ticvai-scope-level`. **The API is already gated correctly** — this is a frontend composition
question, not a contract one.

**It would not change the placement work.** 157 board screens were placed by operator and surface,
and that analysis holds: a kitchen display is still a different surface from a back office, because
**the reason it is separate is that it must survive the network going down and is bumped by
somebody wearing gloves** — not because F&B is a different product.

**It would collapse platform count and it should.** P15 kitchen and P16 analytics are both
`reactWeb`, both venue-operated, both served from the cell. **Under this direction they are two
module-gated areas of one installed app**, distinguished by their density, their offline story and
their entry point — all of which are already declared per screen.

---

## The honest risk

**A modular app is easy to describe and hard to keep honest.** The failure is not technical; it is
that a screen quietly starts depending on a module the tenant did not buy — a menu link, a report
that joins F&B revenue, a dashboard tile.

**The package already has the checker shape for this.** `check-screens` refuses a screen calling an
operation its entry state does not declare; **the same check over `requiresModule` against what a
screen's operations actually touch would catch a cross-module dependency the day it is written**,
rather than the day a tenant without F&B opens a broken page.

**That check is the thing worth building alongside the field.** Without it, the direction is a
convention, and conventions in a 476-screen estate last about a fortnight.

---

## Summary

| Piece | Status |
|---|---|
| One app serving several platforms | **Already done** — `venue-management-web` serves 3 |
| Licence decides what a tenant may use | **Already built** — `LicencePosition`, add-ons |
| Enablement decides what is turned on | **Already built** — and it refuses unsafe disables |
| Screens declare which module they need | **Missing** — `module` is prose, 124 are `TODO` |
| Screens declare which role they need | **Barely** — 16 of 476 |
| A check that catches cross-module dependency | **Missing** — and it is the one that keeps it honest |

**The direction is right and it is already half-implemented.** What is missing is the join between
the licence model and the screen model, and it is a field plus a checker rather than a rebuild.
