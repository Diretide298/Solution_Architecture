# ADR-0015: Standards-First Device Drivers

**Status:** Accepted
**Date:** 13 August 2026
**Unblocks:** hardware-dependent work currently waiting on the model list and turnstile SDK
**Related:** ADR-0012 adaptor-first integration

---

## Context

316 requirements are device-blocked and 194 depend on third-party software. Both sets are
waiting on client deliverables — the hardware model list (outstanding since 12 August) and
the turnstile SDK (since 5 August).

The proposal was to build adaptors against general information now and rework when the real
hardware arrives.

**Research shows that is the wrong frame for roughly half the device classes**, because real
open standards exist. Building to those is not provisional work to be redone — it is the
correct implementation, and the vendor's own device already speaks it.

## Findings

### Point-of-sale peripherals — a genuine vendor-neutral standard exists

<cite index="32-1">UnifiedPOS (UPOS) is a vendor- and retailer-driven open standard under the National Retail Federation's Association for Retail Technology Standards, providing vendor-neutral APIs for thirty-six point-of-sale peripherals — printer, cash drawer, magnetic stripe reader, barcode venue-scanner, line displays. The goal is to give retailers freedom of choice in peripheral selection through standardised connectivity, with appendices covering .NET and Java implementation.</cite>

Beneath it, the command layer is equally settled:

<cite index="34-1">ESC/POS is the most widely recognised POS printer command model, offering direct control over formatting, paper feed, cutting and status functions. OPOS is a middleware driver model for Windows POS environments.</cite>

<cite index="35-1">OPOS, UnifiedPOS, POS for .NET and JavaPOS are retail peripheral API standards providing device abstraction above raw command sets like ESC/POS. Cross-platform applications frequently bypass operating-system print formatting entirely and write ESC/POS over USB, serial, Bluetooth or TCP sockets.</cite>

<cite index="38-1">ESC/POS is a binary protocol — a type of raw text — which means no drivers are required to use it. Mature cross-platform libraries exist covering thermal receipt printers, line displays and cash drawers over serial, USB, Ethernet and WiFi.</cite>

Notably, **the cash drawer is not a separate driver.** It is triggered by an ESC/POS kick
pulse through the printer.

### Access control — a standard exists at the reader layer, not the controller layer

<cite index="21-1">OSDP is an open communications standard between access-control panels and peripheral devices such as card readers, designed to improve interoperability, cybersecurity and device management as a more capable alternative to legacy Wiegand. Ownership transferred to the Security Industry Association in 2012. It was approved as an international standard by the IEC in May 2020 and published as IEC 60839-11-5:2020, defining communications between an access-control unit and its connected peripheral devices. SIA released version 2.2.2 in October 2024.</cite>

<cite index="26-1">OSDP uses AES-128 encryption, continuously monitors wiring, and supports advanced user interfaces including welcome messages and text prompts, smart-card applications and biometrics.</cite>

<cite index="23-1">It provides bi-directional communication, so devices can exchange information and receive commands.</cite>

**The critical limit:** OSDP standardises *reader ↔ controller*. It does **not** standardise
*controller ↔ application*. Axess, SkiData, Gantner and the rest each expose their own API
above the controller.

That still helps, and in a specific way — see §Decision 3.

---

## Decision

**Classify every device class by whether a standard exists, and treat the three tiers
differently.**

### Tier A — Build to the standard. Not rework.

The vendor's device already speaks it. When the model list arrives, the driver works.

| Class | Standard | Notes |
|---|---|---|
| Receipt printer | **ESC/POS** | De facto universal; mature libraries for .NET and TypeScript |
| Cash drawer | **ESC/POS kick pulse** | Not a separate driver |
| Customer / line display | **ESC/POS + UnifiedPOS** | |
| Barcode venue-scanner | **HID keyboard-wedge / serial** | Trivially abstracted |
| Magnetic stripe reader | **UnifiedPOS MSR** | |
| POS peripheral abstraction | **UnifiedPOS / UPOS** | Thirty-six device classes, ARTS-managed |
| Ticket printer | **Boca FGL** | Vendor command language, publicly documented and stable |
| Mobile printer | **Zebra ZPL / CPCL** | Publicly documented |
| Access reader ↔ controller | **OSDP / IEC 60839-11-5** | AES-128 secure channel, bidirectional |

**Approximately 9 of 14 device classes. Build now, at full quality, with no rework
expected.**

### Tier B — Build to the published vendor SDK. Low rework risk.

Public documentation, versioned, sandbox available.

| Class | Source |
|---|---|
| Payment terminal — Stripe | Stripe Terminal SDK |
| Payment terminal — Network International | N-Genius API |
| Wallet passes | Apple Wallet, Google Wallet |
| ID reader | Emirates ID SDK *(vendor-supplied)* |

**Blocked only on sandbox credentials**, which is a smaller ask than the hardware list and
should be requested this week.

### Tier C — Build to our own interface plus a mock. Rework is bounded.

No standard exists. The vendor API is unknown until the client names one.

| Class | Why no standard |
|---|---|
| Turnstile controller *(above OSDP)* | Each vendor proprietary |
| KDS | Vendor-specific |
| Lockers | Proprietary |
| ANPR | Usually HTTP or webhook, but no schema standard |
| Queue / people-counting sensors | Proprietary — already adaptor-first per ADR-0012 |
| Ticket-eater / game reader | Proprietary |
| Digital signage | Varies |

**For these, define our interface, ship a mock adaptor, and treat the vendor adaptor as
bespoke work** — which is already the settled pattern (10 Aug §83, ADR-0012).

### 3. Use standards to shape the interface even where we cannot use them to talk to the device

This is the part worth stating explicitly.

OSDP cannot drive a turnstile controller, but it **defines what an access-control device
does**: credential presented, LED and beep feedback, tamper notification, status
supervision, secure channel, biometric support.

That command set is a **well-designed template for our access-control driver interface**.
Building the interface to OSDP's shape means:

- The vendor adaptor is a translation, not a redesign
- Any genuinely OSDP-compliant reader works directly
- The interface was designed by an industry working group over fifteen years rather than by
  us in an afternoon

The same applies to UnifiedPOS for POS peripherals — thirty-six device classes already
specified, and our interface should not diverge from them without a reason.

---

## Consequences

| | |
|---|---|
| **Tier A work starts now** at full quality. Not provisional | ~9 device classes |
| **Tier B needs sandbox credentials**, not hardware | Request this week |
| **Tier C rework is bounded** to per-vendor adaptors — small, isolated, expected | ~7 classes |
| **The hardware model list stops being a hard blocker** | It becomes a *verification* input: confirm the named model speaks the standard we built to |
| **Turnstile SDK stops blocking the interface** | It blocks one adaptor, not the design |
| Lab still required for acceptance | Building to a standard is not the same as proving it against the device |

### What the hardware list is still needed for

- Confirming each model implements its standard rather than an emulation with gaps
- Procurement
- Acceptance testing

Those are real. But they no longer sit on the critical path for **design and
implementation**, which is what was blocked.

---

## Alternatives

| Rejected | Why |
|---|---|
| Wait for the hardware list before writing any driver | Two weeks lost already; 316 requirements idle behind a list that gates procurement, not design |
| Build a generic guess for every class and rework all of it | Ignores that real standards exist for most classes. Manufactures rework |
| Build only Tier C mocks and defer Tier A | Backwards — Tier A is the low-risk, high-certainty work |

---

## Actions

| # | Action | Owner |
|---|---|---|
| 1 | Define the access-control driver interface **modelled on OSDP's command set** | Chinmay |
| 2 | Define the POS peripheral interface **modelled on UnifiedPOS** | Chinmay |
| 3 | Implement Tier A drivers — ESC/POS printing, drawer kick, display, venue-scanner, MSR | Backend |
| 4 | **Request payment gateway sandbox credentials** — Stripe and N-Genius | Allam |
| 5 | Mock adaptors for every Tier C class, conforming to our interface | Backend |
| 6 | Device simulator suite in CI, per class | Backend |
| 7 | Re-scope the hardware list request: **verification and procurement**, not design input | Chinmay |

Action 7 changes the conversation with the client. The list is still needed — but the
message becomes *"we are building; confirm these models speak the standards"* rather than
*"we are blocked."*

---

## Caveat

Standards compliance is frequently partial. Vendors document ESC/POS *emulation* with gaps;
OSDP support varies by version and by whether secure channel is enabled. Building to the
standard removes most of the risk, not all of it.

**The lab still decides.** This ADR moves work off the critical path; it does not remove the
need to prove each driver against real hardware before acceptance.
