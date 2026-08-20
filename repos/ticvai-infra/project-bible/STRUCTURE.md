**New session? Read `docs/RESUME.md` first.**

# Documentation Structure

## Placement rule

The one rule that keeps docs from rotting:

> **Anything mechanically enforced lives with the code that enforces it.
> Anything narrative lives here, and links to the enforcement.**

`BannedSymbols.txt` lives in `ticvai-backend`. `.eslintrc.json` lives in
`ticvai-frontend`. `setup/naming-and-style.md` explains *why* those rules exist and links
to them. A rule documented in two places diverges; a rule documented here and enforced
there does not.

## Tree

    Home                        landing + navigation
    overview                    Project Direction — source-of-truth hierarchy, settled positions
    glossary                    canonical terms. Non-optional
    gotchas                     things that will bite you

    sources/                    CLIENT DOCUMENTS — read-only, authoritative
      mom/                      7 MoMs. Rank 1 — scope + binding
      requirements/             the 3,184-requirement matrix. Rank 2 — scope
      designs/                  design vision, guest-app app, venue-staff-app app. Rank 3
      diagrams/                 multi-tenant hierarchy. Rank 3

                                Reference-system manuals are rank 4 and are
                                deliberately NOT held here — see sources/README

    setup/                      how to work here
      quickstart                running locally in under an hour
      naming-and-style          one concept, one name, every layer
      api-conventions           contract rules and TICVAI extensions
      backend-patterns          C# / .NET 8
      frontend-patterns         TypeScript / React / React Native
      data-and-storage          SQL, migrations, partitioning, RLS
      config-and-secrets        key vault per cell, build-time vs runtime
      dependencies              approved packages, licence policy
      git-and-mrs               commits, branches, review checklist
      llm-conventions           using AI to WRITE code — provenance, accountability
      quality-gates             CI gates, testing layers, principles
      adding-things             recipes for anything structural

    architecture/               how it is built
      cells-and-tenancy         cell = tenant x jurisdiction
      hierarchy-and-authz       seven levels, deny-overrides-allow
      offline-and-sync          outbox, ordering, conflict policy
      data-model                spine aggregates, partitioning, data mask
      ai-platform               building AI FEATURES (distinct from llm-conventions)
      observability             tracing, metrics, per-venue attribution

    product/                    what it does
      modules/                  one page per domain, created as its context starts

    handoff/                    THE THREE BUILD ARTEFACTS
      api-list                  every endpoint, status, consumers
      page-inventory            every screen, capability, APIs it calls
      schema                    tables, keys, indexes, RLS

    registers/                  living reference data
      capabilities              164 capabilities, 100% requirement coverage
      actors                    33 human actors + system actors
      ai-applications           67 AI applications across 19 domains
      external-dependencies     hardware, third-party software, on-location
      conflicts                 open + closed decisions
      deviations                knowingly-unimplemented requirements

    plan/                       how work becomes code
      user-story-to-spec        the per-context loop
      pm-and-tickets            ticket shape, traceability
      ai-in-requirements        using AI on the 3,184-requirement matrix
      ai-phasing                Phase 1 AI scope and why the rest waits

    delivery/                   sequencing
      waves · context-loop · gates · environments

    integrations/               external surface
      hardware-lab · payment · identity-providers · venue-systems · distribution

    compliance/                 regulatory position
      data-residency · privacy-and-dsar · pci · audit-and-retention

    runbooks/                   operational procedures
      restore-drill · cell-provisioning · migration-rollout · venue-offline · incident

    history/                    where it has been
      milestones · timeline

    adr/                        why decisions were made
      NNNN-short-title.md

    active/                     what is in flight now

## Two splits worth noting

**`setup/llm-conventions` vs `architecture/ai-platform`.** The reference structure had one
`llm-conventions` page; that conflates two unrelated things. Using AI to *write* code is a
development practice — provenance, accountability, elevated-review areas. Building AI
*features* is product architecture — tenant isolation, evals, governance, cost attribution.
Different audiences, different review cycles.

**`registers/` separate from `product/`.** Registers are reference data that changes when
decisions land. Product pages are narrative that changes when scope changes. Mixing them
means the narrative goes stale every time a register updates.

## Additions to the reference structure

`registers/` · `integrations/` · `compliance/` · `runbooks/` · a top-level `glossary`.

The glossary is top-level rather than buried in `setup/` because it is rank-1 in the
source-of-truth hierarchy, and because a glossary nobody finds is a glossary nobody uses.

## Why `sources/` is in the repo rather than a shared drive

Three reasons:

1. **Versioned.** When a MoM is revised, the diff is visible. On a shared drive it is
   silently overwritten.
2. **Adjacent to the analysis.** A register that cites requirement 2.12.3 sits two
   directories from the file containing it.
3. **Authority is explicit.** The sources README states the rank of
   each folder. On a drive, everything looks equally authoritative — which is exactly how
   reference-system material leaks into scope.

The folder is read-only by convention. Corrections produce a new document; the original
stays, because a superseded decision is still evidence of what was decided when.
