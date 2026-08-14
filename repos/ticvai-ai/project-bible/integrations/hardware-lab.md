# Hardware Lab

> **Purpose:** Device lab and drivers  
> **Owner:** Dinesh  
> **Status:** Design unblocked ([ADR-0015](../adr/0015-standards-first-device-drivers.md)) · procurement outstanding

A third of the requirement base cannot reach *done* without devices on a bench.

**No longer blocked on the model list for design.** Per
[ADR-0015](../adr/0015-standards-first-device-drivers.md), roughly nine of fourteen device
classes have real open standards — ESC/POS, UnifiedPOS, OSDP. Building to those is the
correct implementation, not provisional work.

The model list and turnstile SDK are still needed, for **verification, procurement and
acceptance** — not for design.

## Tier A — standards exist, build now

| Class | Standard |
|---|---|
| Receipt printer · cash drawer · customer display | **ESC/POS** (drawer via kick pulse — not a separate driver) |
| Barcode scanner · magnetic stripe reader | **UnifiedPOS / HID** |
| POS peripheral abstraction | **UnifiedPOS**, 36 device classes, ARTS-managed |
| Ticket printer | **Boca FGL** |
| Mobile printer | **Zebra ZPL / CPCL** |
| Access reader ↔ controller | **OSDP / IEC 60839-11-5:2020**, v2.2.2 |

## Tier B — published vendor SDK, needs sandbox not hardware

Stripe Terminal · N-Genius · Apple and Google Wallet · Emirates ID reader.

**Request sandbox credentials this week.**

## Tier C — no standard, mock to our own interface

Turnstile controller *(above OSDP)* · KDS · lockers · ANPR · queue sensors · ticket-eater ·
signage. Vendor adaptor is bespoke work per ADR-0012.

**Design the interface to OSDP's command shape anyway** — credential presented, LED and beep
feedback, tamper, status supervision. A working group spent fifteen years on it.

Must cover: Priority 1 bench · driver abstraction interface · simulators for CI ·
nightly hardware runs · the five device classes absent from the Integrations sheet
*(parking, sensors, game readers, lockers, signage)*.
