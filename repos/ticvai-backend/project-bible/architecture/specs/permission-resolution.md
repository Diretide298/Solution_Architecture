# Permission Resolution — Specification

> **Purpose:** Normative definition of authorisation resolution. The implementation is checked against this, not the reverse.
> **Owner:** Chinmay + Dinesh
> **Status:** **Stage 0.7 — draft for review**
> **Implements:** [ADR-0002](../../adr/0002-authorisation-is-user-driven-not-workstation-driven.md)

This is the largest security surface in the platform. The hierarchy diagram asserts
*"no cross-venue data access unless explicitly permitted"*, and a permissive default
silently violates it.

---

## 1. Model

```
Grant = (principal_id, permission, scope_node, effect)
effect ∈ { ALLOW, DENY }
```

A **query** is `(principal, permission, target_scope)` → `PERMIT | DENY`.

### 1.1 Scope tree

Seven levels, materialised as `ltree`:

```
Tenant → Brand → Region → Venue → Department → Sub-Department → Workstation
```

Path form: `t_ref.b_beta.r_south.v_beta1.d_ticketing.sd_mainentrance.ws_pos01`

### 1.2 Containment

`A contains B` when `B = A` or `B` starts with `A + "."`.

Containment is **downward only**. A grant at Venue does not confer anything at Region.

---

## 2. Resolution Algorithm

```
resolve(principal, permission, target):

  1. denies  = grants where principal matches
                 and (grant.permission = permission or grant.permission = "*")
                 and effect = DENY
                 and grant.scope contains target          # ancestor or self

  2. if denies is non-empty:  return DENY                 # deny wins, always

  3. allows  = grants where principal matches
                 and grant.permission = permission
                 and effect = ALLOW
                 and grant.scope contains target          # ancestor or self

  4. if allows is non-empty:  return PERMIT

  5. return DENY                                          # default deny
```

### 2.1 Normative rules

| # | Rule | Consequence |
|---|---|---|
| **R1** | **Default deny.** No grant means no access | Absence is never permission |
| **R2** | **Deny overrides allow, at any depth** | A deny at Brand is not overridden by an allow at Venue |
| **R3** | **Grants inherit downward only** | A Venue grant confers nothing at Region or Tenant |
| **R4** | **Wildcard applies to DENY only** (`permission = "*"`) | A wildcard allow would be an accident waiting to happen |
| **R5** | **Workstation is never a permission source** | It may be a *scope target*; it is not a grant input |
| **R6** | **Only the selected role's grants apply** | A multi-role user holding role A and B, logged in as A, has A's grants only |
| **R7** | **Resolved once at login**, cached in the session registry | A 7-level tree × 70+ venues cannot be walked per request at 1,000 req/s |
| **R8** | **Grants outside the cell are unresolvable** | A different jurisdiction is a different deployment. A Tenant-level grant does not reach the Oman cell |
| **R9** | Inactive scope nodes resolve to DENY | `is_active = false` on any ancestor |
| **R10** | Expired grants are excluded before resolution | `valid_to < now()` |

### 2.2 Why deny-overrides-allow rather than most-specific-wins

Most-specific-wins is more flexible and more dangerous. Under it, a tenant administrator
who denies `LEDGER_POST` across the tenant can be silently overridden by a venue-level
allow that someone added months earlier. Under deny-overrides, a deny is a guarantee.

The cost is that revoking access at one venue requires a deny at that venue rather than
narrowing an allow. That is the correct trade for a platform where a mistake is a
cross-venue data breach.

---

## 3. Decision Table

`G` = grant scope relative to the query target.

| # | ALLOW at | DENY at | Query target | Result | Rule |
|---|---|---|---|---|---|
| 1 | — | — | any | **DENY** | R1 |
| 2 | target | — | target | **PERMIT** | — |
| 3 | ancestor | — | target | **PERMIT** | R3 |
| 4 | descendant | — | target | **DENY** | R3 |
| 5 | sibling | — | target | **DENY** | — |
| 6 | target | target | target | **DENY** | R2 |
| 7 | target | ancestor | target | **DENY** | R2 |
| 8 | ancestor | descendant | target=ancestor | **PERMIT** | R3 — deny does not bubble up |
| 9 | ancestor | descendant | target=descendant | **DENY** | R2 |
| 10 | ancestor | sibling | target | **PERMIT** | Deny does not contain target |
| 11 | — | any containing | target | **DENY** | R1 + R2 |
| 12 | ancestor | `*` at ancestor | target | **DENY** | R4 |
| 13 | ancestor (different cell) | — | target | **UNRESOLVABLE → DENY** | R8 |
| 14 | ancestor (inactive node in path) | — | target | **DENY** | R9 |
| 15 | ancestor (expired) | — | target | **DENY** | R10 |

---

## 4. Reference Fixture

Synthetic. **Named for its shape, not after any client.** It exists to exercise every
structural property the platform must handle; it is not a model of any specific tenant.

```
t_ref                                            Tenant
├── b_alpha                                      Brand A
│   └── r_north          CUR-A, 2dp              Region      ── cell: ref-north
│       └── v_alpha1                             Venue
│           ├── d_ticketing                      Department
│           │   ├── sd_mainentrance              Sub-department
│           │   │   └── ws_pos01                 Workstation
│           │   └── sd_membership
│           └── d_fnb
│               └── sd_outlet1
│                   └── ws_pos02
└── b_beta                                       Brand B
    ├── r_south          CUR-A, 2dp              Region      ── cell: ref-north
    │   └── v_beta1
    │       └── d_ticketing
    │           └── sd_mainentrance
    │               └── ws_pos03
    └── r_offshore       CUR-B, 3dp              Region      ── cell: ref-offshore
        └── v_beta2
```

### 4.0 Properties it must exercise

Any replacement fixture must preserve all seven. These are the reasons the fixture exists.

| # | Property | Why it must be present |
|---|---|---|
| 1 | **More than one brand** | Brand isolation (V06) |
| 2 | **More than one region per brand** | Region is the currency and jurisdiction owner |
| 3 | **A brand spanning two jurisdictions** | Proves brand is not a cell boundary (V14) |
| 4 | **Two currencies with different decimal scales** | 2dp vs 3dp. A fixed `decimal(18,2)` truncates one of them silently |
| 5 | **More than one venue per region** | Sibling venue isolation (V05) |
| 6 | **Full depth to workstation on at least one path** | Six-level inheritance (V03) |
| 7 | **More than one department per venue** | Department isolation (V15) |

**Note `b_beta` spans two cells.** `r_south` is in `ref-north`; `r_offshore` is in
`ref-offshore`. Brand is a reporting and organisational grouping, not a resolution
boundary.

### 4.1 Permission vocabulary (extract)

Generated from one enum in `ticvai-contracts`. Never hand-typed.

| Permission | Scope levels where meaningful |
|---|---|
| `ORDER_CREATE` | venue, department, sub-department, workstation |
| `ORDER_REFUND` | venue, department |
| `ORDER_REFUND_APPROVE` | venue, region |
| `SHIFT_OPEN` / `SHIFT_CLOSE` | workstation |
| `SHIFT_CLOSE_OTHER` | venue |
| `CASH_LIFT` | venue |
| `ACCESS_VALIDATE` | venue, department, workstation |
| `ACCESS_OVERRIDE` | venue |
| `PRODUCT_CONFIGURE` / `PRICE_CONFIGURE` | venue, region, tenant |
| `USER_MANAGE` / `ROLE_MANAGE` | venue, region, brand, tenant |
| `LEDGER_POST` | venue, region |
| `LEDGER_APPROVE` | region, tenant |
| `REPORT_VIEW_OWN` | *self-scoped — see §6.3* |
| `REPORT_VIEW_VENUE` | venue |
| `REPORT_VIEW_TENANT` | tenant |
| `SESSION_FORCE_LOGOUT` | venue |
| `KIOSK_ATTEND` | workstation |

---

## 5. Test Vectors

**These are normative.** The implementation passes all of them or it is wrong.

| # | Grants | Query | Expect | Proves |
|---|---|---|---|---|
| **V01** | *(none)* | `ORDER_CREATE` @ `v_alpha1` | **DENY** | R1 default deny |
| **V02** | ALLOW `ORDER_CREATE` @ `v_alpha1` | `ORDER_CREATE` @ `v_alpha1` | **PERMIT** | Exact match |
| **V03** | ALLOW `ORDER_CREATE` @ `t_ref` | `ORDER_CREATE` @ `ws_pos01` | **PERMIT** | R3 inherits 6 levels down |
| **V04** | ALLOW `ORDER_CREATE` @ `ws_pos01` | `ORDER_CREATE` @ `v_alpha1` | **DENY** | R3 does not bubble up |
| **V05** | ALLOW `ORDER_CREATE` @ `v_alpha1` | `ORDER_CREATE` @ `v_beta1` | **DENY** | **Sibling venue isolation** |
| **V06** | ALLOW `ORDER_CREATE` @ `b_alpha` | `ORDER_CREATE` @ `v_beta1` | **DENY** | Cross-brand isolation |
| **V07** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `ORDER_CREATE` @ `v_alpha1` | `ORDER_CREATE` @ `v_alpha1` | **DENY** | **R2 — deny wins over broader allow** |
| **V08** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `ORDER_CREATE` @ `v_alpha1` | `ORDER_CREATE` @ `ws_pos01` | **DENY** | R2 inherits downward |
| **V09** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `ORDER_CREATE` @ `v_alpha1` | `ORDER_CREATE` @ `v_beta1` | **PERMIT** | Deny is scoped, not global |
| **V10** | ALLOW `ORDER_CREATE` @ `v_alpha1`<br>DENY `ORDER_CREATE` @ `b_alpha` | `ORDER_CREATE` @ `v_alpha1` | **DENY** | **R2 — specific allow does NOT override broader deny** |
| **V11** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `ORDER_CREATE` @ `ws_pos01` | `ORDER_CREATE` @ `v_alpha1` | **PERMIT** | Deny does not bubble up |
| **V12** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `*` @ `r_north` | `ORDER_CREATE` @ `v_alpha1` | **DENY** | R4 wildcard deny |
| **V13** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `*` @ `r_north` | `ORDER_CREATE` @ `v_beta1` | **PERMIT** | Wildcard deny is scoped |
| **V14** | ALLOW `ORDER_CREATE` @ `t_ref` | `ORDER_CREATE` @ `v_beta2` | **DENY** | **R8 — different cell, unresolvable** |
| **V15** | ALLOW `ORDER_CREATE` @ `d_ticketing` (Yas) | `ORDER_CREATE` @ `sd_outlet1` (Yas F&B) | **DENY** | Department isolation within a venue |
| **V16** | ALLOW `ORDER_CREATE` @ `d_ticketing` (Yas) | `ORDER_CREATE` @ `ws_pos01` | **PERMIT** | Department inherits to workstation |
| **V17** | ALLOW `ORDER_REFUND` @ `v_alpha1`<br>*(no `ORDER_REFUND_APPROVE`)* | `ORDER_REFUND_APPROVE` @ `v_alpha1` | **DENY** | Permissions are not hierarchical among themselves |
| **V18** | ALLOW `ORDER_CREATE` @ `v_alpha1`, logged in as **role A**<br>ALLOW `LEDGER_POST` @ `v_alpha1` via **role B** | `LEDGER_POST` @ `v_alpha1` | **DENY** | **R6 — only the selected role's grants apply** |
| **V19** | ALLOW `ORDER_CREATE` @ `v_alpha1`<br>Session workstation = `ws_pos03` (Venue Beta-1) | `ORDER_CREATE` @ `v_alpha1` | **PERMIT** | **R5 — workstation is not a permission source** |
| **V20** | ALLOW `ORDER_CREATE` @ `v_beta1`<br>Session workstation = `ws_pos01` (Yas) | `ORDER_CREATE` @ `v_alpha1` | **DENY** | R5 — a device does not confer access either |
| **V21** | ALLOW `PRODUCT_CONFIGURE` @ `r_north` | `PRODUCT_CONFIGURE` @ `v_alpha1` | **PERMIT** | Region-scoped configuration |
| **V22** | ALLOW `PRODUCT_CONFIGURE` @ `r_north` | `PRODUCT_CONFIGURE` @ `r_north` | **PERMIT** | Self-scope |
| **V23** | ALLOW `USER_MANAGE` @ `v_alpha1`, `is_active = false` on `v_alpha1` | `USER_MANAGE` @ `v_alpha1` | **DENY** | R9 inactive node |
| **V24** | ALLOW `USER_MANAGE` @ `t_ref`, `valid_to` in the past | `USER_MANAGE` @ `v_alpha1` | **DENY** | R10 expired grant |
| **V25** | ALLOW `REPORT_VIEW_VENUE` @ `v_alpha1` | `REPORT_VIEW_TENANT` @ `t_ref` | **DENY** | Reporting scope is explicit, not implied |
| **V26** | ALLOW `SESSION_FORCE_LOGOUT` @ `v_alpha1` | `SESSION_FORCE_LOGOUT` @ `v_beta1` | **DENY** | A supervisor cannot terminate another venue's sessions |
| **V27** | ALLOW `KIOSK_ATTEND` @ `ws_pos02` | `KIOSK_ATTEND` @ `ws_pos02` | **PERMIT** | Workstation as a valid **target** |
| **V28** | ALLOW `ORDER_CREATE` @ `t_ref`<br>DENY `ORDER_CREATE` @ `t_ref` | `ORDER_CREATE` @ `ws_pos01` | **DENY** | R2 at equal depth |

### 5.1 Machine-runnable form

```json
{
  "fixture": "reference",
  "vectors": [
    { "id": "V07",
      "grants": [
        { "permission": "ORDER_CREATE", "scope": "t_ref",          "effect": "ALLOW" },
        { "permission": "ORDER_CREATE", "scope": "t_ref.b_alpha.r_north.v_alpha1", "effect": "DENY" }
      ],
      "query":  { "permission": "ORDER_CREATE", "scope": "t_ref.b_alpha.r_north.v_alpha1" },
      "expect": "DENY",
      "proves": "R2 deny overrides broader allow"
    }
  ]
}
```

Committed to `ticvai-backend/tests/Ticvai.UnitTests/PermissionVectors.json` and run as a
theory. A failing vector is a build failure.

---

## 6. Edge Cases

### 6.1 Grant on a path that no longer exists

A venue is deleted or moved. Grants referencing a dead path resolve to DENY and are
reported by a nightly integrity job. **Never silently pruned** — a disappearing grant is
indistinguishable from a revocation in an audit.

### 6.2 Role changes mid-session

Grants are resolved at login (R7). A role change does **not** take effect until the next
login, except for revocations: a revocation publishes an event that invalidates the
session in the registry, forcing re-authentication.

Additive changes waiting for re-login is acceptable. Revocations taking effect eventually
is not.

### 6.3 Self-scoped permissions

`REPORT_VIEW_OWN` is not scope-resolved. It grants access to rows where
`principal_id = session.principal_id`, at whatever scope the session already holds.
Cashiers see their own sales summary (07 Aug §21) without a venue-level reporting grant.

### 6.4 Approval chains

`ORDER_REFUND_APPROVE` is a permission, not a chain position. The chain — Ops Manager →
Finance → CEO — is workflow configuration in the approval module. Authorisation only
answers *may this principal act on this request at this scope*.

### 6.5 Dual-authorisation

Requirement 2.12.3: a cashier may refund up to a threshold with a **second user** naming
themselves as audit control. Both principals are resolved independently against
`ORDER_REFUND` at the same scope. This is **not** an escalation to a higher permission.

---

## 7. Enforcement

### 7.1 Data layer — authoritative

```sql
CREATE OR REPLACE FUNCTION platform.in_scope(target ltree)
RETURNS boolean LANGUAGE sql STABLE AS $$
    SELECT EXISTS (
        SELECT 1 FROM unnest(platform.current_scope_paths()) AS granted
        WHERE target <@ granted
    );
$$;
```

The session sets `ticvai.scope_paths` to the **resolved allow set** — paths where the
permission relevant to the operation is permitted after deny processing. Denies are
resolved in the application layer at login; RLS enforces the result.

Every tenant-scoped table carries `ENABLE` **and** `FORCE ROW LEVEL SECURITY`. Without
FORCE the table owner bypasses every policy, and it reviews clean.

### 7.2 Service layer — defence in depth

Every operation declares `x-ticvai-permission` and `x-ticvai-scope-level` in the contract.
The gateway checks the session's effective set before the handler runs.

### 7.3 Client — presentation only

Clients consume `effectivePermissions` from the session and filter navigation on it.
**Clients never compute permissions.** Client-side authorisation is both a security hole
and a source of divergence from server truth.

---

## 8. Performance

| Concern | Approach |
|---|---|
| Resolution cost | Once at login. Cached in the Redis session registry, which single-session already requires |
| Grant volume per principal | Expected < 50. Resolution is O(allows × denies), trivial at that size |
| Tree queries | `ltree` GiST index. Never recursive CTEs per request |
| Cache invalidation | Revocation event → session invalidated → re-login |
| Payload size | `effectivePermissions` is a flat string set plus a scope list. Kilobytes, not megabytes |

---

## 9. Open Questions

| # | Question | Owner |
|---|---|---|
| 1 | Should `ORDER_REFUND_APPROVE` carry a **threshold value** on the grant, or is the threshold a separate configuration? 2.12.3 implies a value; the grant model has no amount field | Chinmay |
| 2 | Is `REPORT_VIEW_OWN` the only self-scoped permission, or is self-scoping a general modifier? | Chinmay |
| 3 | Do accreditation credential holders resolve through this model, or a separate one? They are non-user humans holding scannable access | Chinmay |
| 4 | Does a Tenant-level grant span cells once **CF-31** is answered? Currently R8 says no | **Qossai — depends on CF-31** |

Question 4 is the only one that could change a normative rule. Everything else is
additive.

---

## 10. Implementation Gap Analysis

`Ticvai.Shared.Kernel.Security.PermissionResolver` was written **before** this spec —
inverted, and recorded as such. Checked against the table:

| Rule | Implemented | Note |
|---|---|---|
| R1 default deny | Yes | Allows drive the output set |
| R2 deny-overrides-allow | Yes | `IsDenied` checks ancestors |
| R3 downward inheritance only | Yes | `ScopeNode.Contains` |
| R4 wildcard deny | Yes | `"*"` handled |
| R5 workstation not a source | Yes | No workstation input exists |
| R6 selected role only | Yes | Caller supplies the role's grants |
| R7 resolve once at login | Yes | Pure function; caching is the caller's job |
| R8 cross-cell unresolvable | By construction | Another cell is another database |
| **R9 inactive scope node** | **No** | No `is_active` input. **Gap** |
| **R10 expired grant** | **No** | No `valid_to` input. **Gap** |

Two gaps, both additive: filter grants by `is_active` on every node in the path and by
`valid_to` before resolution. Neither changes the algorithm.

---

## 11. Review Checklist

Before this spec is accepted:

- [ ] Dinesh confirms the model fits the service boundaries in the HLD/LLD
- [ ] All 28 vectors agreed as correct expectations
- [ ] `PermissionResolver` reconciled against this spec — **the code was written first and must be checked against the table, not the reverse**
- [ ] `PermissionVectors.json` committed and running in CI
- [ ] RLS policy template asserts V05 (sibling isolation) in the restore drill
- [ ] Question 1 resolved before the refund flow is contracted
