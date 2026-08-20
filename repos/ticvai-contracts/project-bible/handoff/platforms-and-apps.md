# Platforms and apps

**Twelve platforms, ten apps, 364 screens.**

Named by **who operates them**, agreed 17 August. A platform is a surface a person uses; an
app is the codebase that serves it. **Ten platforms map to one app each. Two apps serve two
platforms**, and both cases are deliberate.

| | Platform | Purpose | App | Operator | Form factor | Screens |
|---|---|---|---|---|---|---|
| P01 | **Guest Web** | Storefront | `guest-web` | guest | web | 29 |
| P02 | **Guest App** | Mobile | `guest-app` | guest | mobileApp | 62 |
| P04 | **Venue POS** | Terminal and Tablet | `venue-pos` | venue | posTerminal | 10 |
| P05 | **Guest Kiosk** | Self-Service | `guest-app` | guest | kiosk | 14 |
| P06 | **Venue Staff App** | Operations | `venue-staff-app` | venue | mobileApp | 50 |
| P07 | **Venue Scanner** | Access Control | `venue-scanner` | venue | handheld | 16 |
| P08 | **Venue Management** | Back Office | `venue-management-web` | venue | web | 73 |
| P09 | **TICVAI Web** | Platform Console | `ticvai-web` | ticvai | web | 36 |
| P10 | **Partner Web** | Reseller Portal | `partner-web` | partner | web | 21 |
| P11 | **Accreditation Web** | Applications | `accreditation-web` | public | web | 8 |
| P12 | **Venue Support** | Agent Console | `venue-support-web` | venue | web | 8 |
| P13 | **Venue CMS** | White Label | `venue-management-web` | venue | web | 20 |
| | | | | | | **347** |

## The two apps that serve two platforms

| App | Platforms | Why one codebase |
|---|---|---|
| `guest-app` | P02 Guest App · P05 Guest Kiosk | Same guest, same white-label branding, same purchase flow. **The kiosk is a layout, not a product** — it is unattended and touch-first, and that changes the frame rather than the code beneath it |
| `venue-management-web` | P08 Venue Management · P13 Venue CMS | Same venue manager, same session, same permissions. The CMS is the branding section of the back office, and splitting it would mean two logins for one person |

**Everything else is one platform, one app.** If a third platform ever wants to join one of
these apps, that is the moment to ask whether it is really the same product.

## Operators

| | Apps | Screens | Who runs it |
|---|---|---|---|
| **guest** | `guest-web`, `guest-app` | 105 | A visitor, on their own device or a kiosk |
| **venue** | `venue-pos`, `venue-scanner`, `venue-staff-app`, `venue-management-web`, `venue-support-web` | 177 | Venue staff |
| **ticvai** | `ticvai-web` | 36 | **Us.** The only app we operate |
| **partner** | `partner-web` | 21 | A reseller or tour operator |
| **public** | `accreditation-web` | 8 | An applicant who is not yet anyone |

**That column is the one that matters at 9pm on a Saturday**, because it answers who is
supposed to fix it.

## A naming rule, enforced

Until 17 August three platforms were called **Staff Web** — the back office, the support
console and the CMS. Each file was individually correct and the set was unusable.

`check-screens.py` now fails a `shortName` used by two platforms. **A name that identifies
three things identifies none.**
