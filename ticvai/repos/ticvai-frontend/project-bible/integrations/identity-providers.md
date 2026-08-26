# Identity Providers

> **Purpose:** External authentication  
> **Owner:** Backend  
> **Status:** **Wave 1**


| Provider | Use | Lead time |
|---|---|---|
| **UAE Pass** | Guest and staff identity in UAE | **Government onboarding — start early** |
| Azure AD / Entra | Tenant staff SSO | Standard |
| Okta-class SAML/OIDC | Tenant staff SSO | Standard |
| Apple ID | Guest social login | Standard |
| Google ID | Guest social login | Standard |
| Al Hosn | UAE health/identity | Confirm scope |
| MFA provider | Step-up authentication | Standard |
| Emirates ID reader | In-person identity capture at counters | **Hardware — see [hardware-lab](hardware-lab.md)** |

## Rules

- **Identity ≠ Entitlement** (05 Aug 2026). An authenticated guest is not an entitled one; the two models stay separate
- External identity maps to a `Principal`, never replaces it
- Guest checkout without an account must remain possible — it is a conversion requirement, not an edge case
- Account linking across providers is a first-class flow, not an afterthought
- Staff SSO is per tenant; a tenant's Azure AD is not TICVAI's

## Outstanding

UAE Pass integration approval has government onboarding lead time. **Start the process before it is on the critical path**, not after.
