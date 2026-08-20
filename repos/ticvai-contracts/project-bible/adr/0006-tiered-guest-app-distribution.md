# ADR-0006: Tiered guest-app app distribution

**Status:** Accepted  
**Date:** 12 August 2026

## Context

CF-13. Whether to publish one universal TICVAI app or per-tenant branded apps, and whether TICVAI operates the build pipeline or tenants self-publish.

## Decision

**Tiered (Option C).** Dedicated and isolated tenants get branded native apps published under **their own** Apple and Google accounts, with TICVAI granted App Manager access. Shared-tier tenants get a branded PWA. A universal TICVAI app exists as a discovery surface only.

**Managed build pipeline.** TICVAI builds, signs and submits. Tenants do not self-publish.

## Consequences

- Apple Review Guideline 4.2.6 is satisfied — template apps must be submitted by the content provider
- **Tenant ID is baked at build time**, so a branded app resolves one cell and never crosses a jurisdiction
- Onboarding gains a step: tenant developer account provisioning, including D-U-N-S registration, which has lead time
- Build-time set is minimised; theming, imagery, copy and module visibility are runtime config
- Contracts must support N-3 minor versions — store review plus tenant update adoption means live apps lag
- PWA tier removes the store cost floor for small tenants without forcing TICVAI branding on them

## Alternatives

| Rejected | Why |
|---|---|
| Universal app only | Cannot bind to one cell; a guest-app selecting venues in two jurisdictions holds cross-border session state |
| Branded apps, self-published | Version fragmentation, signing key custody, toolchain burden |
| TICVAI publishes all branded apps under its own account | Guideline 4.2.6 rejection |
