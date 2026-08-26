# ADR-0002: Authorisation is user-driven, not workstation-driven

**Status:** Accepted  
**Date:** 12 August 2026

## Context

07 Aug 2026 recorded permissions configurable at five levels — site, operating area, workstation, role, user — with no stated resolution order. The 12 Aug decision block contained two contradictory bullets: one asserting front-end selection is role-driven and not device-driven, another asserting it auto-loads from the workstation. Resolves CF-03.

## Decision

**Authorisation is user/role-driven. A user logs in from any device and carries their access.**

Workstation determines presentation (Sale Board), hardware binding, till identity, Access Point inheritance and reporting dimension. **Never authorisation.**

Where multiple grants apply, resolution is **deny-overrides-allow**, evaluated once at login.

## Consequences

- Matrix 2.7.x (workstation-scoped sales permission) is a recorded [deviation](../registers/deviations.md)
- Qossai's 12 Aug example — a cashier seeing only F&B at a restaurant POS — is a **Sale Board** effect, not a permission effect. That cashier could switch boards if their role permits
- Permission resolution must be specified with a decision table and test vectors before implementation
- Enforcement is at the data layer via RLS, not only in services
- **Work built before 12 Aug may have assumed device-driven access and needs auditing**

## Alternatives

| Rejected | Why |
|---|---|
| Workstation ∩ role intersection | Contradicts the client decision; also harder to reason about |
| Workstation-driven | Breaks the stated requirement that access follows the individual |
