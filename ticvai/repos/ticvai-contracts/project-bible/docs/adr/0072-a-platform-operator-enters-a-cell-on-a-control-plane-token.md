# ADR-0072: A platform operator enters a tenant's cell on a signed Control Plane token

**Status:** Accepted · 25 October 2026 · Chinmay Parab (ADAM CR-175, option A, accepted 21 October 2026: "1,2,3 all")
**Date:** 2026-10-25 · **Deciders:** Chinmay Parab
**Source:** ADAM CR-175 (Sanket Keluskar, ticket 30742 `openPlatformStaffGrant`; 30739 `listOwnPlatformStaffGrants`); change entry CHG-R10ID-007; R8 blocker IDENTITY-C20 (CHG-R8MIG-006), which settled that the cell validates the Control Plane token and reads the step-up from it, and left the token itself undefined
**Related:** ADR-0004 (IdentityService issues a tenant's JWT; one session per user) · ADR-0038 (as amended by ADR-0040) and ADR-0039 (the Control Plane is a database of its own) · ADR-0063 (keys; Key Vault) · ADR-0071 (credentials) · audit R098 (a tenant never grants a support role; platform-staff grants), R135 (MFA by permission), R203 (`PLATFORM_*` never rides in a grant)

---

## Context

The Platform Console (P09) runs outside every cell. Its tenant screens call operations in a tenant's cell
through a time-boxed platform-staff grant (`openPlatformStaffGrant`, R098). Since IDENTITY-C20 the contract
says the cell validates the Control Plane token, takes its subject as `operatorPrincipalId` and reads the MFA
step-up from the token, never from a tenant session. **Nothing said what that token is**: its issuer and
signing keys, the claim that carries the operator and the `PLATFORM_*` set, where the operator's second
factor is recorded, or how the cell represents such a caller. A tenant's own session context believes only a
session issued in the same tenant ("a token carried to another tenant's host opens nothing"), and the
step-up the contract names (`x-ticvai-step-up: mfa`, carrier `session`) is recorded on `identity.mfa_challenge`,
a tenant table keyed to a tenant principal. An operator is neither.

## Decision

1. **The Control Plane issues the platform token**: a signed JWT. Issuer `https://<control-plane-host>/`,
   signed with a Control Plane key held in Key Vault (ADR-0063); its public keys are published as a JWKS that
   every cell host trusts (configured per environment, never fetched from a URL the token names). **Audience**
   is the cell the call goes to (`control.cell.id`): a token for one cell opens nothing in another.
   Lifetime at most 15 minutes (confirmed by the lead, 25 October 2026); the Console refreshes it from its platform
   session.
2. **Claims.** `sub` is the operator (`control.platform_operator.id`, a Control Plane principal, never a
   tenant `identity.principal`); `ticvai_platform_permissions` is the operator's `PLATFORM_*` set, nothing
   else; `sid` is the platform session (`control.platform_session.id`); `amr` includes `mfa` once the
   operator has passed the second factor in that session; **`ticvai_step_up`** is `{action, at}`, the last
   MFA step-up: what it was for and when, as a short-lived claim the cell checks without a tenant row.
3. **Operators are Control Plane principals with Control Plane storage**: `control.platform_operator` (the
   operator and its `PLATFORM_*` set), `control.platform_session` (one sign-in to the Console, with its
   step-up), `control.platform_operator_mfa` (its second factors; a `totp` secret and an `emailOtp`
   destination stored encrypted under the Control Plane's field key, since the control database has no
   tenant key). An operator never has a credential, a principal or a session in a tenant database (R098).
4. **The step-up is recorded in the Control Plane**, against the operator's platform session
   (`control.platform_session.step_up_action`, `step_up_at`), and carried in the token (`ticvai_step_up`). A
   cell operation that declares `x-ticvai-step-up: mfa` for a platform caller (`openPlatformStaffGrant`) accepts
   it when `ticvai_step_up.action` names the operation, `ticvai_step_up.at` is within the step-up window (5
   minutes, confirmed by the lead, 25 October 2026) and `amr` includes `mfa`; it never looks for an
   `identity.mfa_challenge` row. A tenant step-up is single-use (`consumedAt`); a platform one is bounded by
   its window and its action instead, since the cell keeps no row for it.
5. **The cell builds a platform caller** from a verified token: an operator id, the `PLATFORM_*` set and the
   step-up, with **no tenant scope** until a platform-staff grant is open. It honours a `PLATFORM_*` permission
   only on the operations that name it (R203); while a grant is open the operator's tenant permissions are
   the grant's, at the tenant root, and every action is audited with the grant's id.
6. **What builds it**: one platform-auth ticket, scheduled before 30739 and 30742, builds the Control Plane
   sign-in that writes these tables and issues the token, the JWKS, and the verification and the platform
   caller in every cell host. Until it lands both tickets wait (the decision); scheduling it is a plan
   change and goes through the plan rules.

## Consequences

**Easier:** operators stay out of tenant databases (R098); `PLATFORM_*` stays in the token, as the contract
said; a cell checks the operator and the step-up statelessly, with no call back to the Control Plane on each
request.

**Harder:** the cells must hold the Control Plane's JWKS and follow its key rotation (publish the new key
before signing with it; keep the old one until the longest token has expired); a revoked operator keeps
working until the token's expiry, which is why it is short-lived.

**What it asks of the package:** the three Control Plane schemas in `contracts/satellite/subscription.yaml`
(`PlatformOperator`, `PlatformSession`, `PlatformOperatorMfaMethod`) derived into the control DDL;
`openPlatformStaffGrant` and `listOwnPlatformStaffGrants` cite this ADR; the platform-auth ticket.
