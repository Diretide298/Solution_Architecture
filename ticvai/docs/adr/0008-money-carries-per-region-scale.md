# ADR-0008: Money carries per-region scale

**Status:** Accepted  
**Date:** 12 August 2026

## Context

The client's own hierarchy example spans Abu Dhabi and Dubai (AED, 2 decimal places) and Oman (OMR, **3 decimal places**). Region owns currency and decimal configuration.

## Decision

Money is `{ amount, currency, scale }` at every layer. SQL columns are `numeric(18,4)` with the currency and scale carried alongside. Wire format is a decimal **string**, never a float.

## Consequences

- A fixed `decimal(18,2)` would silently truncate every Omani transaction
- The ledger is append-only, so corrections are new entries — this must be right **before** data lands
- Allocation across weights (12 Aug §16 revenue split) must distribute the remainder, or the ledger will not balance
- `decimal` for money is banned at compile time via `BannedSymbols.txt`
- Consolidated brand P&L across AED and OMR needs a stated FX conversion rule
