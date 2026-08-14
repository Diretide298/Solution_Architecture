# ADR-0003: Conditional role selection at login

**Status:** Accepted  
**Date:** 12 August 2026

## Context

07 Aug 2026: a user may hold multiple roles and switch between them at login. 10 Aug 2026 §5.1 and §6: the role-selection screen is removed in favour of automatic routing. Directly contradictory for multi-role users. Resolves CF-01.

## Decision

**One role → direct login. Several roles → selection prompt.** Confirmed 12 Aug 2026 §4 and corroborated by the reference system's own behaviour.

## Consequences

- Every archetype needs a defined default landing screen
- The Sale Board bound to the workstation determines the landing surface, not the role
- The 10 Aug "removal" is effectively reversed for multi-role users — the record should say so

## Note

The 10 Aug decision carries a **lost subject** — *"agreed this makes more sense and will be adopted"* names nobody. Recorded as CF-23.
