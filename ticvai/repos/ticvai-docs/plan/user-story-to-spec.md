# User Story to Spec

> **Purpose:** Requirement to running code  
> **Owner:** Chinmay  
> **Status:** Settled


## The chain

```
Requirement ID  →  Capability (C-ID)  →  Contract operation  →  Schema + Page  →  Test name
```

Every link is traceable in both directions. A ticket that traces to neither a Requirement ID nor a MoM decision **is not scope**.

## Provenance

| Tag | Source | Build? |
|---|---|---|
| `MATRIX` | Requirement ID | Yes |
| `MOM` | Dated MoM decision | Yes |
| `REF` | Reference-system material | **No — a question for the client** |
| `DESIGN` | Our recommendation, unratified | **No — until accepted** |

`REF` and `DESIGN` items are excluded from estimates, contracts and sprint scope until promoted.

## Per context

See [delivery/context-loop](../delivery/context-loop.md) for the eight stages. In short: capabilities → contract → *(schema ∥ pages ∥ mock)* → build → harden.

## Freezing

After **Gate 2** a contract is frozen for the context. A satellite context needing a spine change raises a **formal change request with review** — never an inline edit. This is the rule that bounds rework to one context.

## Naming a test

Tests assert behaviour and are named for what they prove:

```
Refund_below_threshold_requires_second_user_authorisation   // 2.12.3
Scan_offline_then_sync_deduplicates_on_replay               // 3.2.x, 31 Jul
Grant_denied_at_region_suppresses_allow_at_venue            // ADR-0002
Money_allocation_across_weights_preserves_total             // 12 Aug §16
```

A test name that does not describe a rule is a test nobody will trust when it fails.
