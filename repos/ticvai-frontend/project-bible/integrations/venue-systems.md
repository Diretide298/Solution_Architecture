# Venue Systems

> **Purpose:** Turnstiles, queue feeds, KDS, lockers, signage  
> **Owner:** Chinmay  
> **Status:** **Wave 1–3**


## Standard pattern

**TICVAI exposes an inbound API; the client's chosen third-party system feeds into it.** Direct integration with a named vendor is bespoke work, quoted separately (10 Aug §83).

This converts an unbounded vendor matrix into one interface plus optional paid adapters — which matters when every new venue arrives with equipment nobody has seen.

## Systems

| System | Pattern | Status |
|---|---|---|
| **Turnstile controllers** | Driver abstraction. Vendor SDK per controller | **Blocked — SDK outstanding since 05 Aug** |
| **Queue / people-counting sensors** | Inbound API (C99). TICVAI does not build or buy sensors | CF-33 — ownership unresolved |
| **KDS** | Integration point only, not a full KDS build (31 Jul §11) | Wave 2 |
| **Lockers** | Driver abstraction | Wave 2 — device class absent from Integrations sheet |
| **ANPR / parking** | Inbound API | Wave 3 — device class absent from Integrations sheet |
| **Ticket-eater / game readers** | Driver abstraction | Wave 3 — device class absent from Integrations sheet |
| **Digital signage** | Outbound feed (C100) | Wave 3 — device class absent from Integrations sheet |

## Four classes absent from the Integrations sheet

Parking, sensors, game readers, lockers and signage appear in requirements but not on the sheet. Either the sheet is incomplete or these are out of scope. **Both answers are acceptable; the ambiguity is not.**

## Queue data — the correction

Wait-time accuracy depends on a **third-party camera or sensor system at the venue** (10 Aug §4.4, §4.11). TICVAI builds the queue engine and exposes the inbound API; the venue supplies the feed.

**Consequence for the lab:** no sensor hardware needed. A conforming mock against the inbound API is sufficient. Queue *entry validation* does need scanning devices, and queue calls need a signage display.
