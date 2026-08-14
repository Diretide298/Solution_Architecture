# Deviation Register

> **Purpose:** Knowingly-unimplemented requirements  
> **Owner:** Chinmay  
> **Status:** Living


Requirements deliberately not implemented, with the decision that supersedes them.

**Must be surfaced at acceptance testing.** A deviation the client was never told about is a defect.

| Requirement | Text | Deviation | Superseded by |
|---|---|---|---|
| **2.7.x** | Sales permissions restricted by site, operating area, **workstation**, or role | Workstation is not a permission source | [ADR-0002](../adr/0002-user-driven-authorisation.md) — authorisation is user/role-driven; workstation determines presentation, hardware, till identity and reporting dimension only |
| **7.1.10** | Configurable number of concurrent logins to multiple terminals with the same user | Not implemented | [ADR-0004](../adr/0004-single-session.md) — single session per user; a second login is rejected, not displaced |

## Adding a deviation

Requires: the requirement ID and its text, what we are doing instead, the decision that supersedes it, and the architecture lead's sign-off. Then it goes on the UAT agenda — not into a footnote.
