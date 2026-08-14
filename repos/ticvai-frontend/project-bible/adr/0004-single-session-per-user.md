# ADR-0004: Single session per user

**Status:** Accepted  
**Date:** 12 August 2026

## Context

Matrix 5.8.2 requires one session per user. Matrix 7.1.10 allows configurable concurrent logins across terminals. 12 Aug 2026 §1 confirmed one user per workstation at a time. Resolves CF-02.

## Decision

**Single session per user.** A second login is **rejected**, not auto-terminating the first. A supervisor holding `SESSION_FORCE_LOGOUT` may terminate an abandoned session.

## Consequences

- Cannot be enforced with stateless JWT alone. A **server-side session registry** (Redis) is required, with the JWT carrying a `sid` claim validated per request
- The registry is reused to cache resolved permissions — two problems, one mechanism
- Matrix 7.1.10 is a recorded [deviation](../registers/deviations.md)
- Force-logout exists precisely because rejection does not displace

## Rationale for rejection over displacement

Auto-terminating an existing session can orphan an open cart or an unclosed cash drawer. A refused login is recoverable in seconds; an orphaned till is an audit exception.
