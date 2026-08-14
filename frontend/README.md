# Frontend manifests

**Ten apps, 180 screens.** Generated from `screens/*.yaml` — do not hand-edit.

One file per app, listing every route, its component path, its wave and its build status.
An app is not a platform: `backoffice` serves two, and `guest` serves the mobile app and the
kiosk.

| App | Audience | Form factor | Screens | Offline | Platforms |
|---|---|---|---|---|---|
| `accreditation` | public | web | 8 | no | P11 |
| `backoffice` | staff | web | 6 | no | P08 |
| `guest` | guest | mobileApp | 62 | **yes** | P02 |
| `partner-portal` | partner | web | 21 | no | P10 |
| `platform-admin` | platformAdmin | web | 36 | no | P09 |
| `pos` | staff | posTerminal | 10 | **yes** | P04 |
| `support-console` | staff | web | 8 | no | P12 |
| `web-b2c` | guest | web | 29 | no | P01 |
| | | | **180** | | |

## What the checker enforces

`check-frontend.py` verifies that every app referenced by a screen exists, that routes are
unique within an app, that component paths follow the convention, and that an offline-capable
app declares the `offline-core` package. An app claiming to work offline without the package
that makes it possible is a claim nobody tested.

## Status

**All ten are scaffolded and none has an implemented screen.** `status: notStarted` on every
route. The manifests are the build order, not a record of progress.
