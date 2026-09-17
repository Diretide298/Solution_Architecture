# Dependencies

> **Purpose:** Adding a package is a decision  
> **Owner:** Chinmay  
> **Status:** Stub


## Before adding

1. Does an approved package already do this?
2. What licence? Permissive only — MIT, Apache-2.0, BSD. **GPL and AGPL are blocked** in a commercial client deliverable
3. Maintenance signal — last release, open issue count, single-maintainer risk
4. Transitive weight — what does it pull in?
5. Does it need to exist, or is it fifty lines?

## Rules

- **Contract packages are pinned, never floating.** `@ticvai/api-client`, `Ticvai.Contracts`, `ticvai-contracts` — exact versions, bumped deliberately
- Renovate raises bump PRs; humans review them
- Security scanning in CI, blocking on high severity
- A generated dependency — one an AI tool suggested — gets the same licence review as any other. See [llm-conventions](llm-conventions.md)
- Adding a dependency to `Shared.Kernel` or `offline-core` needs architecture sign-off. Those propagate everywhere

## Approved by runtime

To be filled as the stack settles. Current baseline is in each repo's project files.
