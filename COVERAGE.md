# What is in this package, and what is not

**17 August 2026.** An honest account of the delivery against the whole build.

The short version: **the design layer is substantially complete and nothing has been executed.**
Every number below is counted from the files in this package, not from memory.

---

## What exists

| | | Against |
|---|---|---|
| **API operations** | **753** | Every unblocked module. 267 spine, 470 satellite |
| API schemas | 607 | Across 25 files |
| Permissions | 128 | Every operation declares one or an `x-ticvai-auth` model |
| **Tables designed** | **278** | 2,025 columns |
| **Tables written as DDL** | **0** | Deliberate — see below |
| Relationships | 499 | 272 of 358 tables carry one; the six that do not are correct |
| Screens defined | **364** | Across 13 platforms, all linked to a board |
| **Screens specified — states written** | **364** | Of 364 |
| Screens with operations declared | 318 | Of 364 |
| Operations reaching a screen | 568 | Of 737 |
| State models | **76** | Of 77 lifecycles — **all modelled** |
| Domain events | 26 | Publisher, consumers, idempotency keys |
| User flows | **23** | 137 branches. Every contract and platform touched |
| ADRs | 24 | |
| **Requirements covered by a contract** | **2,778 of 2,990 (93%)** | The remaining 212 are workshop-blocked |
| **Requirements with an artefact** | **1,848 of 2,072 (89%)** | 12 of 15 classes closed |
| Configuration levels decided | 321 of 321 | |
| Validators | **7** | Plus two generators |

## What does not exist

| | Why |
|---|---|
| **Any SQL** | Removed deliberately. The design is still moving, and a migration written against a moving schema is a migration rewritten. `handoff/storage-design.md` holds the reasoning |
| **Any code** | Nothing has been built since 30 July. Dinesh's CI run is the blocker |
| **Sprint 0** | Not started |
| Three domains | Developer & API (94), Device Management (60), Accreditation (58) — **workshops not held** |
| Three artefact classes | Device/hardware (workshop), retention (CF-64), performance targets (none stated) |
| 194 AI requirements | Forecasting, fraud, dynamic pricing, recommendation — **parked until there is a season of history** |

## The honest gap

**Design is substantially complete. Build is zero.**

That has been the shape since 30 July, and no amount of further design changes it. The 212
blocked requirements are the only thing outside our control; everything else on this list is
ours and none of it needs a decision from anyone.

`handoff/build-order.md` names what can start. `venue-scanner` and `venue-pos` are the two apps
that clear the bar today.
