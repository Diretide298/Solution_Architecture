# Platforms and deployment

> Naming and ownership are in [`platforms-and-apps.md`](platforms-and-apps.md). This page is
> where each runs and how it ships.

**Twelve platforms. Six frontend apps. Four apps do not exist.**

Named so the thing says what it *is* before what it is *for* — audience and form factor
lead, purpose follows. `Guest App — Mobile`, not `Guest Mobile App`. The short name is what
you say in a standup; the full name is what you put in a document.

| | Short | Purpose | Audience | Form factor | App | Scaffolded |
|---|---|---|---|---|---|---|
| P01 | **Guest Web** | Storefront | guest-app | web | `guest-web` | yes |
| P02 | **Guest App** | Mobile | guest-app | mobileApp | `guest-app` | yes |
| P03 | **Guest Kiosk** | Self-Service | guest-app | kiosk | `guest-app` | yes |
| P04 | **Staff POS** | Terminal and Tablet | staff | posTerminal | `venue-pos` | yes |
| P06 | **Staff App** | Operations | staff | mobileApp | `venue-staff-app` | yes |
| P07 | **Staff Scanner** | Access Control | staff | handheld | `venue-scanner` | yes |
| P08 | **Staff Web** | Venue Back Office | staff | web | `venue-management-web` | yes |
| P09 | **Admin Web** | Platform Console | platformAdmin | web | `ticvai-web` | **no** |
| P10 | **Partner Web** | Reseller Portal | partner | web | `partner-web` | **no** |
| P11 | **Public Web** | Accreditation | public | web | `accreditation-web` | **no** |
| P12 | **Staff Web** | Support Console | staff | web | `venue-support-web` | **no** |
| P13 | **Staff Web** | White-Label CMS | staff | web | `venue-management-web` | yes |

## Where it runs and how it ships

| | Platform | Runs on | Ships by | Release cadence |
|---|---|---|---|---|
| P01 | Guest Web — Storefront | browser | CDN + edge | continuous |
| P02 | Guest App — Mobile | iOS / Android native | App Store + Play, tenant developer account | fortnightly, gated by review |
| P03 | Guest Kiosk — Self-Service | kiosk hardware, kiosk-mode shell | device management push | monthly, out of hours |
| P04 | Staff POS — Terminal and Tablet | POS terminal — Windows or Android | device management push | monthly, never during trading |
| P06 | Staff App — Operations | iOS / Android native | MDM, not a public store | fortnightly |
| P07 | Staff Scanner — Access Control | rugged handheld — Android | MDM | monthly, never on an event day |
| P08 | Staff Web — Venue Back Office | browser, desktop | served from the cell | weekly |
| P09 | Admin Web — Platform Console | browser, desktop | served from the Control Plane | weekly |
| P10 | Partner Web — Reseller Portal | browser | served from the cell | monthly — partners integrate against it |
| P11 | Public Web — Accreditation | browser | public, served from the cell | monthly |
| P12 | Staff Web — Support Console | browser, desktop | served from the cell | weekly |
| P13 | Staff Web — White-Label CMS | browser, desktop | served from the cell | weekly |

## Network, offline and store review

| | Platform | Network assumption | Offline | Store review |
|---|---|---|---|---|
| P01 | Guest Web — Storefront | public internet, unmanaged | no | no |
| P02 | Guest App — Mobile | mobile data, intermittent | no | **yes** |
| P03 | Guest Kiosk — Self-Service | venue LAN, generally reliable | no | no |
| P04 | Staff POS — Terminal and Tablet | venue LAN with expected outages | **mandatory** | no |
| P06 | Staff App — Operations | venue wifi, dead zones expected | yes | no |
| P07 | Staff Scanner — Access Control | must function with none | **mandatory** | no |
| P08 | Staff Web — Venue Back Office | venue LAN | no | no |
| P09 | Admin Web — Platform Console | corporate network, IP-restricted | no | no |
| P10 | Partner Web — Reseller Portal | public internet | no | no |
| P11 | Public Web — Accreditation | public internet | no | no |
| P12 | Staff Web — Support Console | corporate network | no | no |
| P13 | Staff Web — White-Label CMS | public internet | no | no |

## Screen coverage

| | Platform | Inventoried | Defined | With navigation |
|---|---|---|---|---|
| P01 | Guest Web — Storefront | 29 | 29 | 29 |
| P02 | Guest App — Mobile | 60 | 62 | 62 |
| P03 | Guest Kiosk — Self-Service | — | — | — |
| P04 | Staff POS — Terminal and Tablet | — | 10 | 10 |
| P06 | Staff App — Operations | 50 | — | — |
| P07 | Staff Scanner — Access Control | — | — | — |
| P08 | Staff Web — Venue Back Office | 73 | 6 | 6 |
| P09 | Admin Web — Platform Console | 36 | 36 | 36 |
| P10 | Partner Web — Reseller Portal | 21 | 21 | 21 |
| P11 | Public Web — Accreditation | 8 | 8 | 8 |
| P12 | Staff Web — Support Console | 8 | 8 | 8 |
| P13 | Staff Web — White-Label CMS | 20 | — | — |

**Inventoried 305 · defined 180 · with navigation 180**

## What the form factor changes

**`mobileApp` on a guest-app surface means store review.** P02 ships under the tenant's own
developer account (ADR-0006), so a fix is a release rather than a deploy. Every `buildTime`
field in the White Label Builder exists because of that one row.

**`posTerminal` and `handheld` are offline-mandatory, not offline-capable.** A gate must
validate with no network and a POS must sell. `check-screens` fails any platform declaring
either form factor without `offlineCapable`, so the two cannot drift apart. P06 is a staff
`mobileApp` and offline-capable but not mandatory — a technician losing signal in a plant
room is an inconvenience; a gate losing signal is a queue.

**`web` on an unmanaged device** — Guest Web, Partner Web, Public Web, and the CMS. No device
management, no guaranteed browser, no assumption about screen size. Partner Web additionally
has partners integrating against it, which is why its cadence is monthly: a portal that
changes weekly breaks weekly.

**Admin Web is the odd one.** Served from the Control Plane, outside every cell, because it
provisions cells. A console living inside a cell could not create the first one.

**Branding follows audience, not platform.** Confirmed 14 August: staff surfaces carry TICVAI
branding; guest-app surfaces are white-label. **Guest Kiosk is the case that makes the rule
clear** — it is venue hardware but a guest-app uses it, so it is white-labelled like the website
rather than branded like the POS beside it.

## The gap

**73 screens assigned to four apps that do not exist** — ticvai-web (36), partner-web
(21), venue-support-web (8), accreditation-web (8).

**Guest Kiosk and Staff Scanner are not even inventoried.** No count, no screens. The venue-scanner
is a Wave 1 surface.

