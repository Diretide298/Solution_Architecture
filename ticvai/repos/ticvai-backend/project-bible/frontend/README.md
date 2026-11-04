# Frontend manifests

One manifest per app, `frontend/<app>.yaml`, **derived by `tools/derive-frontend.py` from `screens/*.yaml`; do not
hand-edit the manifests**. Each says who operates the app, its audience, form factor and runtime, whether it is
offline-capable, the platforms it serves and their repositories (`docs/active/frontend-repos.yaml`), the packages and
contracts it uses, and its screens by wave (`byWave`). **This page carries no count**: how many apps and screens there
are is in the manifests and in [OVERVIEW.md](../OVERVIEW.md), derived on every refresh (r13 system review F-13).

Named by **who operates them**, agreed 17 August. `guest-*` is what a visitor touches,
`venue-*` is what venue staff run, `ticvai-*` is ours. That is the boundary that matters when
someone asks who supports a screen at 9pm on a Saturday.

## What the naming settles

**An app is not a platform.** `guest-app` serves both the mobile app and the kiosk, because
they share a codebase and differ by layout. `venue-management-web` serves the back office and
the White-Label CMS for the same reason.

**`venue-support-web` is separate from `venue-management-web` deliberately.** A contact-centre
agent and a venue manager are different people with different shifts, and folding the support
screens into the back office would bury them.

**`ticvai-web` is the only app we operate.** Everything else is run by a venue, a partner or a
guest, and that is what the prefix is for.

## History (17 August 2026)

> **Historical.** What follows is this page as written on 17 August 2026, kept as the record of that day. Its
> figures were true then and are not now (r13 system review F-13, CHG-R14J-041); today's are in
> [OVERVIEW.md](../OVERVIEW.md) and in the files themselves.

**Ten apps, 364 screens.** Generated from `screens/*.yaml` — do not hand-edit.

| App | Operator | Audience | Form factor | Screens | Offline | Platforms |
|---|---|---|---|---|---|---|
| `accreditation-web` | **public** | public | web | 8 | no | P11 |
| `guest-app` | **guest** | guest | kiosk | 76 | no | P02, P05 |
| `guest-web` | **guest** | guest | web | 29 | no | P01 |
| `partner-web` | **partner** | partner | web | 21 | no | P10 |
| `ticvai-web` | **ticvai** | platformAdmin | web | 36 | no | P09 |
| `venue-management-web` | **venue** | staff | web | 93 | no | P08, P13 |
| `venue-pos` | **venue** | staff | posTerminal | 10 | **yes** | P04 |
| `venue-scanner` | **venue** | staff | handheld | 16 | **yes** | P07 |
| `venue-staff-app` | **venue** | staff | mobileApp | 50 | **yes** | P06 |
| `venue-support-web` | **venue** | staff | web | 8 | no | P12 |
| | | | | **347** | | |

## Build order

Classified in `handoff/build-order.md`, and on each manifest as `buildReadiness`.

| | Apps | Screens |
|---|---|---|
| **Ready to build** | `venue-scanner`, `venue-pos` | **26** |
| Wave 1 critical, specify first | `venue-staff-app`, `guest-web` | 79 |
| Wave 1 partial | `venue-management-web`, `guest-app`, `ticvai-web` | 205 |
| Wave 2 or later | `partner-web`, `accreditation-web`, `venue-support-web` | 37 |

**The gate is specified, not defined.** Every screen is defined — purpose, route, navigation,
enough to draw. Specified means it also names its operations and its states, and **the states
are what a developer builds from**.

Only two apps clear it, and both are offline-mandatory. That is not a coincidence: they were
specified first because a gate that cannot validate without a network is a queue.

## Status

**All ten scaffolded, none implemented.** `status: notStarted` on every route. Four were
created on 17 August and had never existed — `ticvai-web`, `partner-web`, `venue-support-web`
and `accreditation-web` carried 73 screens between them with no folder to put them in.
