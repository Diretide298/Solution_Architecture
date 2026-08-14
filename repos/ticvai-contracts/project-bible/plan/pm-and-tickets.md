# PM & Tickets

> **Purpose:** Ticket shape and traceability  
> **Owner:** Chinmay  
> **Status:** **Week 2**


## Ticket shape

Every ticket carries:

| Field | Rule |
|---|---|
| Capability | One or more C-IDs |
| Requirements | Requirement ID range, or the MoM decision |
| Context | Which bounded context |
| Provenance | `MATRIX` / `MOM` / `REF` / `DESIGN` |
| Gate | Which gate it must pass |

A ticket without a capability is not scope. A ticket tagged `REF` or `DESIGN` is not estimable.

## Definition of ready

- Capability and requirement IDs attached
- Contract operation exists (or the ticket **is** the contract work)
- Dependencies on other contexts identified
- Acceptance stated as behaviour, not as implementation

## Definition of done

- Behaviour tests pass, named for the rule
- Contract tests pass both directions
- Architecture tests green
- Naming conforms to [naming-and-style](../setup/naming-and-style.md)
- Deviations recorded if any requirement is knowingly unmet
- Runs against the **reference fixture**, not a single-venue simplification

## Estimating

**Estimate capabilities, not stories.** A capability has a requirement count, a contract surface and a known dependency profile. A story sliced from it does not.

## Escalation

| Situation | Route |
|---|---|
| Two sources of equal authority disagree | [conflicts register](../registers/conflicts.md) as a new CF item |
| A requirement is knowingly not being implemented | [deviations register](../registers/deviations.md), architecture lead signs |
| A satellite needs a spine change | Formal change request, contract review |
| A decision was taken but not recorded | Raise for the MoM; an unrecorded decision is not a decision |
