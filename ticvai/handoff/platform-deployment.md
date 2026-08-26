# Platform deployment

**Derived from `screens/` by `tools/derive-platform-deployment.py`. Do not hand-edit.**

This table was maintained by hand until 26 August and held **twelve rows against fifteen platforms** — P14, P15 and P16 were never added. The viewer's `lib/boards.mjs` had written a comment around that number, so the gap travelled into a second repo before anybody counted.

**A figure typed once is correct once.** `platform-P01.md` claimed 35 screens against a live 46; the viewer carried *654 operations* in 25 places against a live 1,023. This file is now derived for the same reason both of those were fixed.

**15 platforms · 492 screens · 64 drawn.**

| | Short | Purpose | Audience | Form factor | App | Offline | Screens | Drawn |
|---|---|---|---|---|---|---|---:|---:|
| P01 | **Guest Web** | Guest Web — Storefront | guest | web | `guest-web` | no | 46 | 0 |
| P02 | **Guest App** | Guest App — Mobile | guest | mobileApp | `guest-app` | yes | 63 | 0 |
| P04 | **Venue POS** | Venue POS — Terminal and Tablet | staff | posTerminal | `venue-pos` | yes | 24 | 12 |
| P05 | **Guest Kiosk** | Guest Kiosk — Self-Service | guest | kiosk | `guest-app` | no | 17 | 0 |
| P06 | **Venue Staff App** | Venue Staff App — Operations | staff | mobileApp | `venue-staff-app` | yes | 66 | 9 |
| P07 | **Venue Scanner** | Venue Scanner — Access Control | staff | handheld | `venue-scanner` | yes | 11 | 0 |
| P08 | **Venue Management** | Venue Management — Back Office | staff | web | `venue-management-web` | no | 143 | 43 |
| P09 | **TICVAI Web** | TICVAI Web — Platform Console | platformAdmin | web | `ticvai-web` | no | 37 | 0 |
| P10 | **Partner Web** | Partner Web — Reseller Portal | partner | web | `partner-web` | no | 21 | 0 |
| P11 | **Accreditation Web** | Accreditation Web — Applications | public | web | `accreditation-web` | no | 8 | 0 |
| P12 | **Venue Support** | Venue Support — Agent Console | staff | web | `venue-support-web` | no | 8 | 0 |
| P13 | **Venue CMS** | Venue CMS — White Label | staff | web | `venue-management-web` | no | 20 | 0 |
| P14 | **Developer** | Developer Portal | partner | web | `developer-portal-web` | no | 8 | 0 |
| P15 | **Kitchen Display** | Kitchen Display — Pass and Stations | staff | kiosk | `kitchen-display` | yes | 10 | 0 |
| P16 | **Venue Analytics** | Venue Analytics — Cross-Domain Reporti | staff | web | `venue-management-web` | no | 10 | 0 |

## What the columns mean

**Offline** is the platform's own flag. It is not the same claim as an operation's `x-ticvai-offline-capable` — **the two disagreed on 37 screens until 25 August**, and `check-screens` now compares a screen's offline prose against the operations it loads.

**Drawn** counts screens whose `wireframe.status` is `designed` — a board a person drew, not one this package generated. **It sits on three platforms only**: P04, P06 and P08, the three with client packs. Twelve platforms are wholly generated.

**App** is the installable, and it is deliberately not one per platform. `guest-app` serves P02 and P05; a kiosk is the guest app with no person holding it.
