# Environments

> **Purpose:** Local through production  
> **Owner:** Dinesh  
> **Status:** **Week 2**


| Environment | Purpose | Data |
|---|---|---|
| **Local** | Development | reference fixture, synthetic |
| **CI** | Every commit | reference fixture, ephemeral Postgres + Redis |
| **Mock** | Frontend and AI before backend exists | Prism, contract-driven |
| **Canary cell** | Migration and release proving | Synthetic tenant, production-shaped |
| **Pilot venue** | On-location proving | Real network, real devices |
| **Production cells** | Live | Per tenant per jurisdiction |

## The reference fixture

**Every environment seeds it.** Two brands, three regions across two countries, 3+ venues, full department and workstation tree, AED and OMR.

The failure mode this prevents is specific: a team develops against a single-venue single-currency fixture, everything passes, and multi-region breaks at UAT. Since the matrix is written system-centric with 9.2% actor coverage, the fixture is also the cheapest way to surface assumptions the requirements never state.

## A pilot venue is a Phase 1 requirement

The vertical slice — *configure a timed product → sell at POS → validate at gate offline → sync* — is **not provable without one**. The failure mode being tested is a real network dropping mid-transaction at a real gate, with real turnstile hardware.

**Currently unidentified.** Raised with TICVAI 12 Aug.

## Release rollout

Never all cells at once. **Canary cell → 10% → remainder**, gated on health.

Version skew between cells is expected and acceptable. The Control Plane tracks per-cell version; contracts tolerate N-3 minor versions.
