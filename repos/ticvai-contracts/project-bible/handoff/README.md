# Build Handoff

> **Purpose:** The three artefacts a development team starts from
> **Owner:** Chinmay
> **Status:** Wave 1 complete for closed contexts

Architecture decisions live in [adr](../adr/README.md). Requirements live in
[registers](../registers/README.md). **This directory is what the team actually consumes.**

| Artefact | What it answers | Consumed by |
|---|---|---|
| [api-list](api-list.md) | What endpoints exist, what they need | Backend, frontend |
| [page-inventory](page-inventory.md) | **305 screens** across 9 platforms, with capability and API mapping |
| [schema](schema.md) | What tables exist, keys, indexes, RLS | Backend, DBA |

## Traceability

    Requirement ID  →  Capability  →  API operation  →  Table
                                   ↘  Page

Every row in every artefact carries its capability ID. A page with no API is a
**local-first read** ([ADR-0013](../adr/0013-local-first-point-of-sale.md)). An API with no
page is a partner endpoint or a gap.

## Status meaning

| | |
|---|---|
| ✅ Published | OpenAPI written, schemas defined, errors enumerated. **Buildable** |
| 🟡 Specified | Path, method, permission and offline policy known. **Estimable, not buildable** |
| ⬜ Not specified | Context has not been through the contract loop |

The gap between 🟡 and ✅ is request and response schemas plus error enumeration. That is
the contract-authoring work, and it is the current bottleneck.

## What a team can start on today

| Team | Work | Depends on |
|---|---|---|
| **Backend** | Tenant resolution · RLS · session registry · permission resolver · migration orchestrator · `ltree` tree · outbox · bundle signing and delta | **Nothing** — internal |
| **Frontend** | `offline-core` sync, bundle apply, lease hold, staleness bound · `design-tokens` · `ui` primitives · POS and scanner shells | **Nothing** — generated types + Prism mock |
| **Both** | Everything in ✅ contexts — identity, tenancy, shift, access | Published contracts |

That is roughly **6 weeks of work for 8 people with no contract dependency**, which is the
runway available while the remaining contracts are authored.
