# Frontend delivery

**Written 17 August.** Four things the screen definitions already imply and nothing has stated.
None needs new data — all of it derives from `handoff/screen-index.json` and the app manifests.

---

## Bundles split by wave

Every screen carries a wave and every manifest carries `byWave`. **A Wave 1 build does not need
Wave 2 and Wave 3 routes**, and the split is already described in data.

| App | Total | W1 | W2 | W3 |
|---|---|---|---|---|
| `venue-management-web` | 111 | **45** | 62 | 4 |
| `guest-app` | 80 | **21** | 42 | 17 |
| `venue-staff-app` | 50 | **29** | 20 | 1 |
| `ticvai-web` | 37 | 11 | 16 | 10 |
| `guest-web` | 35 | **20** | 11 | 4 |
| `partner-web` | 21 | 0 | 11 | 10 |
| `venue-scanner` | 16 | **16** | — | — |
| `venue-pos` | 10 | 7 | 3 | — |
| `accreditation-web` · `venue-support-web` | 16 | 0 | 2 | 14 |

**`guest-app` is the case that matters.** Eighty screens, twenty-one of them Wave 1, and it is the
app a guest downloads on hotel wifi before their visit. **Shipping 80 routes to deliver 21** is a
download a guest abandons, and the abandonment is invisible to us.

**`venue-scanner` is the opposite and the reason it is the build candidate**: sixteen screens, all
Wave 1, nothing to split.

**Route-level splitting, not component-level.** A screen is the natural boundary because it is
already the unit everything else is defined against.

---

## Two apps serve two platforms each, and the shells differ

| App | Platforms | |
|---|---|---|
| `guest-app` | P02 Guest App **65** · P05 Guest Kiosk **15** | |
| `venue-management-web` | P08 Venue Management **91** · P13 Venue CMS **20** | |

**A kiosk build does not need the guest app's account screens, and nothing says so.**

A kiosk is a shell configuration over the same codebase (ADR-0006) — but *the same codebase* is
not *the same bundle*. **The kiosk needs 15 of 80 routes**, runs unattended on known hardware, and
has no login, no wallet, no order history and no push notifications.

**Loading the other 65 onto a wall-mounted machine is not a performance problem** — it is 65 routes
of attack surface on a device the public can touch.

Same for the CMS: 20 of 111 routes, and a content editor does not need the finance screens.

---

## The offline bundle has no declared size

`venue-scanner` is offline-mandatory and its bundle is the whole gate operation — the entitlement
set, the blacklist, the access points, the admission profiles. **F06 depends on it and does not say
how big it is.**

Three numbers nobody has stated:

**Size at a large venue.** A 30,000-attendee event is a different bundle from a museum, and the
difference decides whether it downloads over venue wifi in a minute or in twenty.

**Build time.** `getOfflinePackage` builds per device today — **a bundle identical for every
scanner at a venue, rebuilt once per scanner.** Twelve scanners at shift start is twelve identical
builds against the primary at the busiest moment of the day.

**Staleness limit.** How old a bundle may be before a scanner refuses to work from it. **A scanner
running on Tuesday's entitlements will admit somebody refunded on Wednesday**, and nothing
currently says when it should stop trusting itself.

**The first fix is the cheap one**: build once per venue per version, cache it (`cache:resolution`),
and serve every scanner the same artefact.

---

## No screen has a performance budget

This is a known blocked artefact class — *performance/SLA (no targets)* — rather than an oversight.
**But 376 screens with no budget will produce some slow ones**, and the ones that matter are
predictable without a client conversation:

| | Why it is different |
|---|---|
| `SCN-*` scan screens | **A gate queues behind them.** The budget is a scan-to-answer figure, not a page-load one |
| `POS-*` sale screens | A cashier with a queue in front of them |
| `KSK-*` kiosk screens | **A guest walks away rather than waiting**, and we never learn they did |
| `BO-*` back office | Nobody is waiting in a physical line |
| `*` reports | Minutes are acceptable and already routed `analytical` |

**Three of these five are guest-facing and time-critical, and they are the smallest apps.** The
targets can be proposed rather than waiting on the workshop.

---

## The venue map in the offline bundle

**A guest standing in the middle of a park with no signal is the guest who most needs directions**,
so the map ships in the offline package rather than being fetched when it is wanted.

Three parts, three sizes, three lifetimes:

| | | |
|---|---|---|
| **The graph** | Small — a few hundred nodes and edges | **Versioned, and it changes on every closure.** A route computed offline across a path that closed this morning is the failure this versioning exists to catch |
| **The points** | A few hundred rows | Changes when the venue edits the map, which is monthly |
| **The base image or tiles** | **Megabytes** | Changes rarely, and is the reason this is a bundle rather than a request |

**A 12,000-pixel park map is not something a phone downloads on arrival.** Tiles exist so the
device takes the zoom levels it needs, and a guest opening the map on venue wifi at the gate is the
worst possible moment to send twenty megabytes.

**The graph is cached separately from the map** because they change at different rates — the map is
monthly and a path closure is immediate. Caching them together means either re-sending the image
for a closure or serving a stale graph, and both are worse than two entries.
