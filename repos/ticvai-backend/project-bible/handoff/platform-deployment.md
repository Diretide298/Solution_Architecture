# Platforms and deployment

**Twelve platforms. Six frontend apps. Four apps do not exist.**

Where each platform runs, how it ships, and what it may assume about the network.

| | Platform | App | Scaffolded | Runs on | Ships by |
|---|---|---|---|---|---|
| P01 | Guest Web Storefront | `web-b2c` | yes | browser | CDN + edge |
| P02 | Guest Mobile App | `guest` | yes | iOS / Android native | App Store + Play, tenant developer account |
| P03 | Self-Service Kiosk | `guest` | yes | kiosk hardware, kiosk-mode shell | device management push |
| P04 | Point of Sale | `pos` | yes | POS terminal — Windows or Android | device management push |
| P06 | Staff Operations App | `employee` | yes | iOS / Android native | MDM, not a public store |
| P07 | Access Control Handheld | `scanner` | yes | rugged handheld — Android | MDM |
| P08 | Venue Back Office | `backoffice` | yes | browser, desktop | served from the cell |
| P09 | Platform Admin Console | `platform-admin` | **no** | browser, desktop | served from the Control Plane |
| P10 | Partner & Reseller Portal | `partner-portal` | **no** | browser | served from the cell |
| P11 | Accreditation Portal | `accreditation` | **no** | browser | public, served from the cell |
| P12 | Support Agent Console | `support-console` | **no** | browser, desktop | served from the cell |
| P13 | White-Label CMS | `backoffice` | yes | browser, desktop | served from the cell |

## Network, offline and cadence

| | Platform | Network assumption | Offline | Store review | Release cadence |
|---|---|---|---|---|---|
| P01 | Guest Web Storefront | public internet, unmanaged | no | no | continuous |
| P02 | Guest Mobile App | mobile data, intermittent | no | **yes** | fortnightly, gated by review |
| P03 | Self-Service Kiosk | venue LAN, generally reliable | no | no | monthly, out of hours |
| P04 | Point of Sale | venue LAN with expected outages | **mandatory** | no | monthly, never during trading |
| P06 | Staff Operations App | venue wifi, dead zones expected | yes | no | fortnightly |
| P07 | Access Control Handheld | must function with none | **mandatory** | no | monthly, never on an event day |
| P08 | Venue Back Office | venue LAN | no | no | weekly |
| P09 | Platform Admin Console | corporate network, IP-restricted | no | no | weekly |
| P10 | Partner & Reseller Portal | public internet | no | no | monthly — partners integrate against it |
| P11 | Accreditation Portal | public internet | no | no | monthly |
| P12 | Support Agent Console | corporate network | no | no | weekly |
| P13 | White-Label CMS | public internet | no | no | weekly |

## Screen coverage

| | Platform | Inventoried | Defined | With navigation |
|---|---|---|---|---|
| P01 | Guest Web Storefront | 29 | 29 | 29 |
| P02 | Guest Mobile App | 60 | — | — |
| P03 | Self-Service Kiosk | — | — | — |
| P04 | Point of Sale | — | — | — |
| P06 | Staff Operations App | 50 | — | — |
| P07 | Access Control Handheld | — | — | — |
| P08 | Venue Back Office | — | — | — |
| P09 | Platform Admin Console | 36 | 36 | 36 |
| P10 | Partner & Reseller Portal | 21 | 21 | 21 |
| P11 | Accreditation Portal | 8 | 8 | 8 |
| P12 | Support Agent Console | 8 | 8 | 8 |
| P13 | White-Label CMS | 20 | — | — |

**Inventoried 232 · defined 102 · with navigation 102**

## What the deployment target changes

**Store review — P02 only.** A native guest app ships through Apple and Google under the
tenant's own developer account (ADR-0006), so a fix is a release rather than a deploy. Every
`buildTime` field in the White Label Builder exists because of this one row.

**Offline is mandatory on P04 and P07, not optional.** A gate must validate with no network
and a POS must sell. That is ADR-0013, and it is why those two carry `offline-core` and the
others do not. P06 is offline-capable but not offline-mandatory — a technician losing signal
in a plant room is an inconvenience; a gate losing signal is a queue.

**Unmanaged devices — P01, P10, P11, P13.** No device management, no guaranteed browser, no
assumption about screen size. P10 additionally has partners integrating against it, which is
why its cadence is monthly: a partner portal that changes weekly breaks weekly.

**P09 is the odd one.** Served from the Control Plane, outside every cell, because it
provisions cells. A console living inside a cell could not create the first one.

**Release windows differ by an order of magnitude.** P01 deploys continuously; P07 must not
deploy on an event day. Anything shared between them — `ui`, `design-tokens`, `api-client` —
has to survive both cadences, which is an argument for versioning those packages rather than
letting apps track head.

## The gap

**73 screens assigned to four apps that do not exist** — platform-admin (36), partner-portal
(21), support-console (8), accreditation (8).

Two were always in the proposal. They were missed because they have no UI/UX board, and the
frontend plan was built from the boards. Same root cause as CF-47.

**203 inventoried screens have no definitions** — P02, P03, P04, P07, P08, P13. Those six
apps are scaffolded; the definitions are what is missing, and they are the harder half.

