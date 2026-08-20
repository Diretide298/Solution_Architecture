# Screen definitions

**364 screens across twelve platforms.** Everything inventoried is defined.

Each carries an id, a purpose, a module and wave, the operations it calls, its layout as
regions and component kinds, its states, its navigation and its implementation path.

| | Platform | Purpose | Screens | With ops | States written |
|---|---|---|---|---|---|
| P01 | **Guest Web** | Storefront | 29 | 26 | 10 |
| P02 | **Guest App** | Mobile | 62 | 21 | 2 |
| P04 | **Staff POS** | Terminal and Tablet | 10 | 10 | 10 |
| P05 | **Guest Kiosk** | Self-Service | 14 | 11 | 0 |
| P06 | **Staff App** | Operations | 50 | 7 | 0 |
| P07 | **Staff Scanner** | Access Control | 16 | 15 | 0 |
| P08 | **Staff Web** | Venue Back Office | 73 | 5 | 5 |
| P09 | **Admin Web** | Platform Console | 36 | 24 | 0 |
| P10 | **Partner Web** | Reseller Portal | 21 | 18 | 0 |
| P11 | **Public Web** | Accreditation | 8 | 0 | 0 |
| P12 | **Staff Web** | Support Console | 8 | 7 | 0 |
| P13 | **Staff Web** | White-Label CMS | 20 | 0 | 0 |
| | | | **347** | **144** | **27** |

## Two levels of done

**Defined** means the screen exists with a purpose, a route and navigation. All 347 are.

**Specified** means it also names its operations, its components and its states. **Twenty-seven
are.** The difference is not cosmetic: the states are where the behaviour lives, and on an
offline surface the offline state is the most important line on the page.

167 of these arrived on 14 August, extracted from the wireframe boards in `wireframes/`. The
boards carry real purposes and real navigation, so those are real. They carry no states,
because a picture does not say what happens when the network dies.

## Reading a definition

```yaml
id: SCN-004
name: Admitted
purpose: ...            # why the screen exists
apis:                   # validated against 689 operations
  - operationId: validateAccess
layout:
  template: fullscreen
  regions: [...]        # vocabulary from _components.yaml, 34 kinds
states:
  offline: ...          # required on offline-capable platforms
navigation:
  exitTo: [SCN-003]     # checked against the flows
implementation:
  app: venue-scanner
  route: /access/admitted
```

`check-screens.py` validates the component vocabulary, every operation id, required states,
navigation resolution, and that a `posTerminal` or `handheld` platform declares
`offlineCapable` — a gate that cannot validate without a network is a queue.

## What to do next

**Write the states before writing more screens.** Sixteen venue-scanner screens have `TODO` offline
states and the venue-scanner is the surface where offline matters most. P07 and P04 together are
twenty-six screens and would take the specified count from 27 to 43.
