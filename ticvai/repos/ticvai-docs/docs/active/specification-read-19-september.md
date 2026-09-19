# Reading the specifications — the RFP, the hardware sheet, the seat manifest

> **Owner:** Chinmay · **Written:** 19 September 2026 · **Status:** open — four conflicts to settle
>
> Third of the three categories in a client drop. The design books were parsed, the MoMs were
> mined, and **these had never been opened.** `sources/specifications/` after the re-section holds
> twelve files; this is what is in them.

---

## The RFP is the document everything else answers

`TAIS Platform RFP From Miracle Star Trading.pdf` — 13 pages, **rank 2, scope** — sets out twelve
functional domains and names roughly 120 capabilities inside them.

**It has the same twelve domains, in the same order, as `Ch03_Functional_Domain_Coverage`.** That is
not a coincidence: Ch03 was written to answer it. Which means the coverage check built this morning
was checking our screens against *our own reply* rather than against the request. That check now
exists in both directions:

| tool | reads | rank | what it tells you |
|---|---|---|---|
| `tools/check-rfp-coverage.py` | the RFP | **2 — scope** | whether we are building what was asked for |
| `tools/check-spec-coverage.py` | Ch03 | 3 — ours | whether our proposal is self-consistent |

**RFP result: 154 capability lines, 104 carried by a screen, 50 not.** The count over-reads — the
mobile-application bullets on page 9 get filed under domain 11, and domains 9–11 are bare bullet
lists the client never defined — so treat it as a review queue, like every other lexical match here.

### Four capabilities that two independent documents both say are missing

These appear in the RFP **and** in Ch03, and match nothing in any of the 1,629 screens:

| capability | RFP domain | what it is |
|---|---|---|
| **Seatmap Management** | 4 Ticketing | *"create and manage interactive seat maps for reserved seating events"* |
| **Gamification** | 8 Marketing | *"loyalty points, achievements, and reward mechanisms"* |
| **System Telemetry** | 9 Intelligence | bulleted, undefined |
| **Procurement Management** | 10 Operations | bulleted, undefined |

Agreement between a rank-2 source and a rank-3 one does not make a thing scope twice over, but it
does remove the usual explanation — that we named it differently.

---

## Four things the RFP says that the package contradicts or does not model

### 1. Access control vendors — three lists, and the rank-1 one is not in the rank-2 one

| source | rank | names |
|---|---|---|
| **RFP**, domain 4 | **2** | *"Axess, Skidata, CAME, KABA, Boon Edam, and other industry-standard systems"* |
| **MoM 24 August** | **1** | narrowed to **HID or Suprema** (CF-35) |
| Hardware sheet | — | turnstile reader: **HID, Axess, Suprema** |

**`HID` and `Suprema` do not appear in the RFP list at all.** `Axess` is the only name common to
more than one source. `Skidata`, `CAME`, `KABA` and `Boon Edam` appear nowhere else in the package.

A later MoM outranks the RFP, so the 24 August narrowing stands — but it narrowed to two vendors the
RFP never mentioned, and nothing records that as a change. **That is a conflict to raise, not a
reading error.**

### 2. On-premise deployment is required and is not modelled

> *"Deployment model supporting Cloud, On-Premise, and Hybrid environments"* — RFP §Vendor Proposal
> Requirements

The architecture is cells: one Postgres per cell, in-region, in-cell hosting, per the ADRs. **There
is no on-premise story at all.** Whether that is a real requirement or boilerplate is a question for
the client, but it is a rank-2 sentence and the package is silent on it.

### 3. The client owns the source, and the handover artefacts were just retired

> *"The TIAS platform will be fully owned by the client, including source code, architecture,
> documentation, and intellectual property… The vendor must provide full access to the source code
> repository and ensure the platform can be independently maintained and extended by the client or
> third-party developers."*

`Dev01_Engineering_Handbook`, `Dev02_Repository_Structure_and_Contract_Pipeline` and
`Dev03_Local_Development_Environment` were moved to `sources/legacy/` today. **That is right for
scope and wrong to forget**: those three are the shape of what this clause obliges us to hand over.
Retired as a source of requirements; still owed as a deliverable.

### 4. The evaluation is weighted toward cost and architecture, not features

| criterion | weight |
|---|---:|
| **Total Cost of Ownership** | **30%** |
| Technical Architecture & Platform Design | 20% |
| AI Capabilities & Innovation | 15% |
| Functional Coverage of RFP Requirements | 15% |
| Implementation Approach & Project Plan | 10% |
| Vendor Experience · Integration & Scalability | 5% each |

**Functional coverage is 15%** — the same as AI, half of TCO. Worth knowing before the next round of
screen-count arguments.

---

## `TICVAI_Hardware_Integration v1.0.xlsx` — fifteen integrations, each with a vendor chosen

Not background. This is a decision sheet, and **not one of these names appears in any screen**:

| # | integration | chosen |
|---:|---|---|
| 1 | Emirates ID Reader | HID |
| 2 | Chainway Handheld Device | Chainway C66 |
| 3 | RFID Reader | Kaptur |
| 4 | NFC / Gaming reader | *China* — undecided |
| 5 | Biometric finger print scanners | HID / Suprema |
| 6 | Receipt Printer | Epson TM‑T88VII |
| 7 | Cash Drawer | HP |
| 8 | Customer Display | HP, Toshiba |
| 9 | Turnstile Reader | HID, Axess, Suprema |
| 10 | Kitchen Display | *Decide later* |
| 11 | Facial Readers | HID, Suprema |
| 12 | Barcode Scanner | HP, Datalogic |
| 13 | Kiosk | BlueRhine Kiosk |
| 14 | Boca Printer | Boca Wristband and Ticket Printer |
| 15 | Zebra Bluetooth Printer | Zebra |

Two are open — **NFC/gaming reader** and **kitchen display** — and both are open in a sheet nobody
had read, so neither is on any list of things awaiting a decision.

`Device Management` is a named RFP capability in domain 10. A device management screen that does not
know these fifteen device classes exist is a screen drawn from a board rather than from the estate.

## `Seating Manifest.xlsx` — the seat import format, and it is trivially small

```
Description | Section | Row | Seat
Seating     | A1      | 1   | 1
```

435 rows, **one sheet per section** (`Section A`), sections named `A1`. `venue-map.yaml` already
describes this shape — the one place in the package that had read any of this folder.

**And `Seatmap Management` still matches nothing.** The import format is understood; the editor the
RFP asks for is not drawn.

---

## What is owed

- [ ] **Raise the access-control vendor conflict** — CF item. Rank 1 narrowed to two vendors the
      rank-2 document does not name
- [ ] **Ask about on-premise.** Rank 2 requires it; the cell architecture does not model it
- [ ] **Decide Seatmap Management and Gamification** — named by both documents, drawn by neither
- [ ] **Put the fifteen hardware integrations in front of device management**, and surface the two
      open choices as open
- [ ] **Keep Dev01–03 as a handover obligation** even though they are retired as a source
- [ ] Read `TAIS_Product_Planning_and_Delivery_Plan` and `TICVAI_Task_Track_From_Workshops` — the
      two remaining unread files in `specifications/planning/`
