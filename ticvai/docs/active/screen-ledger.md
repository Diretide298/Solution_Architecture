# Screen ledger — what is missing from every screen

**Derived by `tools/screen-ledger.py`. Regenerate rather than editing.**

A screen is **done** when it calls an operation, something navigates to it, it goes somewhere, its wireframe anchor resolves to a frame that exists, it names an app/route/component, and no other screen declares an identical operation set.

| | |
|---|---:|
| Screens | 1091 |
| **Done** | **1082** |
| Outstanding | 9 |

| Missing | Screens | From the pack | Authored |
|---|---:|---:|---:|
| `ops` | 9 | 0 | 9 |
| `nav-in` | 0 | 0 | 0 |
| `nav-out` | 0 | 0 | 0 |
| `wire` | 0 | 0 | 0 |
| `impl` | 0 | 0 | 0 |
| `unique` | 0 | 0 | 0 |

## By platform

| Platform | Total | Done | Left |
|---|---:|---:|---:|
| P01 Guest Web | 46 | 46 | 0 |
| P02 Guest App | 71 | 70 | 1 |
| P04 Venue POS | 24 | 24 | 0 |
| P05 Guest Kiosk | 17 | 15 | 2 |
| P06 Venue Staff App | 66 | 64 | 2 |
| P07 Venue Scanner | 11 | 11 | 0 |
| P08 Venue Management | 363 | 363 | 0 |
| P09 TICVAI Web | 318 | 318 | 0 |
| P10 Partner Web | 51 | 51 | 0 |
| P11 Accreditation Web | 8 | 4 | 4 |
| P12 Venue Support | 28 | 28 | 0 |
| P13 Venue CMS | 60 | 60 | 0 |
| P14 Developer | 8 | 8 | 0 |
| P15 Kitchen Display | 10 | 10 | 0 |
| P16 Venue Analytics | 10 | 10 | 0 |

## Every outstanding screen

| Screen | Platform | Origin | Missing |
|---|---|---|---|
| GST-043 Arabic / RTL Experience | P02 | authored | `ops` |
| KSK-001 Attract Loop | P05 | authored | `ops` |
| KSK-014 Out of service | P05 | authored | `ops` |
| EMP-044 Accessibility | P06 | authored | `ops` |
| EMP-045 Arabic / RTL | P06 | authored | `ops` |
| ACC-001 Landing / Programme Overview | P11 | authored | `ops` |
| ACC-003 Application Review & Submit | P11 | authored | `ops` |
| ACC-004 Application Status Tracking | P11 | authored | `ops` |
| ACC-008 Credential Register | P11 | authored | `ops` |