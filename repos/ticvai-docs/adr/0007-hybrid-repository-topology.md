# ADR-0007: Hybrid repository topology

**Status:** Accepted  
**Date:** 12 August 2026

## Context

Four runtimes — .NET, TypeScript/React Native, Python, Terraform — plus a shared contract. Question: monorepo or polyrepo.

## Decision

**Polyrepo between runtimes, monorepo within frontend.** Six repositories: contracts, backend, frontend, ai, infra, docs.

## Consequences

- The six frontend apps share `offline-core`, `api-client`, `design-tokens` and `ui` in one workspace. Six copies of a sync engine would be six divergent bug surfaces
- Coupling between runtimes is by **versioned artefact** — private NuGet, npm, PyPI — not directory adjacency
- Contract breaks become reviewed, versioned events gated by `oasdiff`, rather than invisible same-commit edits
- Mobile apps pin a contract version and keep working while the backend advances
- Client-hosted deployments ship the backend repo alone
- Cost: a cross-cutting change is 2–3 PRs instead of 1

## Rationale

React Native ships through store review; the backend deploys continuously. **They can never deploy atomically**, so the primary benefit of a monorepo is structurally unavailable. Exactly one boundary has real shared code — that is where the monorepo earns its cost.
