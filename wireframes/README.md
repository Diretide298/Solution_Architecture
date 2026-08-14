# TICVAI — wireframe boards

**Open `TICVAI Wireframe Boards.dc.html` first.** It links every board.

Twelve platform boards, 347 screens, one visual system. Every file is
self-contained apart from `support.js`, which sits alongside them — keep the
folder together and any board opens in a browser with no build step.

## Boards

| File | Platform | Screens | Definition status |
|---|---|---|---|
| P01 Guest Web | Storefront | 29 | 29 defined, 13 were stubs |
| P02 Guest App | Guest mobile | 62 | 62 defined, none had a purpose line |
| P04 Staff POS | Terminal and tablet | 10 | 10 defined, 6 existed as client mockups |
| P05 Guest Kiosk | Unattended | 14 | never inventoried |
| P06 Staff App | Employee mobile | 50 | inventoried, none defined |
| P07 Staff Scanner | Access handheld | 16 | never inventoried — Wave 1 |
| P08 Staff Web — Back Office | Venue operations | 73 | 6 of 73 defined |
| P09 Admin Web | Platform console | 36 | 36 defined, 16 were stubs |
| P10 Partner Web | Reseller portal | 21 | 21 defined |
| P11 Accreditation | Public web | 8 | 8 defined, contract workshop-blocked |
| P12 Support Console | Staff web | 8 | 8 defined |
| P13 White-Label CMS | Tenant CMS | 20 | inventoried, none defined |

## How to read a board

Each board opens with the finding, three callouts and a **flow map** — click any
screen in the map to jump to it. Under every frame is a monospace line naming the
contract operation the screen was drawn from, and a **GOES TO** row linking the
screens it leads to. Cross-platform links are qualified with the target file, so
they work from the folder.

Flags on a screen header mean something specific:

- `UNSPECIFIED` — the screen definition declares a template and a placeholder field, nothing more
- `SCOPED SETTINGS` — an instance of the one settings template (thirteen of them across the estate)
- `SHARED PAYMENT COMPONENT` — the same component as POS-005, WEB-012, GST-009 and PTR-012
- `WORKSHOP-BLOCKED` — drawn from the requirement register, with no contract behind it

## Where the content came from

Field names, enums, states and deny reasons are read off the package:
`contracts/spine/*.yaml`, `states/*.yaml`, `screens/P*.yaml` and `COVERAGE.md`.
Where a screen had no definition — 136 of them — it is derived from contract
operations that reach no screen, and the board header says so.

## What these boards do not settle

- **One token set, three themes** (light guest, dark staff, light POS) is proposed here and not decided anywhere in the package. It determines whether `design-tokens` is one package or three.
- **RPO, RTO and retention** are unanswered. Six Admin screens are drawn against them.
- **Four workshop-blocked domains** — accreditation, device management, developer/API, approval workflows — carry 212 requirements between them. Accreditation blocks the Wave 1 scanner.
- **AI-61→66** is a Wave 1 commitment with no engineer. The AI tab is already in the delivered employee shell (CF-41).
- **No audit register, no notification catalogue, no accessibility criteria.** Screens that depend on them are flagged.

## Six components carry a third of the work

Payment · denomination counter · scoped settings form · pipeline stepper ·
identity field group · consent block. Each appears on three or four platforms.
Getting them right once removes a large part of what is left.
