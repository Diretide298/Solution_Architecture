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

## Amendment, 20 October 2026: GitLab, six frontend repositories, one published client

**Decided by the lead (r8 cause FOUNDATION-AI-C37, option A), following CHG-R6-058 and CHG-R6-059 (13 October).**

- **The code lives in GitLab** (`gitlab.softlabsgroup.in`), and **CI is GitLab CI** (`.gitlab-ci.yml`, the shared
  runners) in every repository: contracts, backend, ai, infra, docs and the six frontend repositories. The GitHub
  Actions workflows the starters shipped are replaced (audit R057's CI half is superseded; its Azure half stands).
- **The frontend is six repositories in the group `ticvai-frontend`, one app each**, not the one Nx workspace this
  ADR decided (`docs/active/frontend-repos.yaml` maps each platform to its repository). The shared packages are no
  longer a workspace: `@ticvai/api-client` is **one package published to the group's GitLab npm registry** on each
  contracts tag (`v*`), and each frontend repository pins it by **exact version**. `offline-core`, `design-tokens`
  and `ui` follow the same route when a second repository needs them.
- Each frontend repository's owner records its profile (workspace, package manager, lint, typecheck, test and build
  scripts) in `frontend-repos.yaml`; the CI template in `ticvai-frontend/.gitlab-ci.yml` runs those scripts. Until a
  profile exists, SETUP-CI builds the backend pipeline and that frontend template.
- The consequences above about coupling by versioned artefact, the `oasdiff` gate and pinned contract versions are
  unchanged; "a cross-cutting change is 2-3 PRs" is now 2-3 merge requests.
