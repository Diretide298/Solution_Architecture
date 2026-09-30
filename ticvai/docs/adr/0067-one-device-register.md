# ADR-0067: One device register; Access keeps only where a device is placed

**Status:** Accepted · 1 October 2026 · Chinmay Parab
**Date:** 2026-10-01 (drafted 30 September from the system-design review) · **Deciders:** Chinmay Parab
**Finding:** SD-004 (medium)
**Amends:** ADR-0015 (standards-first device drivers, amended by this ADR) — one register for every device class
**Related:** ADR-0055 (modules and deployables) · ADR-0013 (local-first POS)

---

## Context

**Two tables register devices, and both hold the same facts.**

| | `platform.device` (`010-platform.sql:130`) | `access.access_device` (`010-access.sql:67`) |
|---|---|---|
| Owner | Tenancy: `registerDevice`, `recordDeviceHeartbeat`, `enrolDevice`, `configureWorkstation` (`tenancy.yaml`) | Access: `registerAccessDevice`, `updateAccessDevice` (`access.yaml`) |
| Identity | `kind`, `model`, `identifier` | `hardware_type`, `hardware_model_id`, `serial_number` |
| Versions | `firmware_version` | `configuration_version`, `local_rule_version`, `credential_security_package_version` |
| Health | `status`, `health`, `battery_percent`, `last_heartbeat_at` | `status`, `scanner_health`, `controller_health`, `camera_health`, `last_heartbeat_at` |
| Lifecycle | `state`, `enrolment_state` (registered → retired) | `provisioning_stage`, `lifecycle_status` (registered → production) |

- `audit/ticvai/steps/B/RD.json` has this as an open item.
- `device.enrolmentChanged` exists to keep them in step. That is a patch, not a design.
- Firmware, health and lifecycle can diverge. A turnstile could be "retired" in one and "production" in the other.

**The name the review proposed is taken.** `access.device_binding` already exists
(`010-access.sql:681`): it binds a **guest's phone** to an entitlement (app installation, security
status). The placement of a gate device therefore gets its own name below.

---

## Decision

**`platform.device` is the only register. Access keeps a placement table and nothing else.**

- **`platform.device`** holds identity (kind, hardware type, model, serial), every version (firmware, configuration, rule package, credential package), health, heartbeat and one lifecycle: registered → enrolled → provisioned → active → deactivated → retired.
- **The device kind vocabulary merges.** Access's hardware types (speed gate, tripod turnstile, podium and so on) become a `hardware_type` under `kind`.
- **`access.device_placement`**: `device_id` (→ `platform.device`), `access_point_id`, `gate_lane_id`, `access_area_id`, role, proximity threshold, controller reference. Access's provisioning stages (hardware profile assigned … connectivity tested) become a checklist on the placement, not a second lifecycle. `access.device_binding` keeps its current meaning (a guest's phone).
- **Operations:** `registerAccessDevice` becomes "register in the platform, then place in Access" (rename to `placeAccessDevice`). Heartbeats have one path: `recordDeviceHeartbeat`.
- `device.enrolmentChanged` is no longer needed to sync two registers.
- **Ownership follows ADR-0055's rule:** Tenancy owns and migrates `platform.device`; Access owns `access.device_placement`, reads device facts only through what Tenancy publishes, and never writes the register with its own SQL.

---

## Options Considered

### Option A: Keep both and sync by event (status quo)

| Dimension | Assessment |
|---|---|
| Complexity | Medium, forever |
| Cost | Two sets of screens and operations |
| Scalability | Fine |
| Team familiarity | High |
| Time to Block A | None |

**Pros:** No change. **Cons:** Two truths about one device.

### Option B: Platform register plus Access placement (decided)

| Dimension | Assessment |
|---|---|
| Complexity | Low |
| Cost | One contract move, one table merge |
| Scalability | One heartbeat path for every device |
| Team familiarity | High |
| Time to Block A | No Block A cost; lands before B1 scanner work |

**Pros:** One lifecycle, one health view for POS printers and turnstiles alike. **Cons:** Access screens read device facts from the platform module.

### Option C: Access owns every device

| Dimension | Assessment |
|---|---|
| Complexity | Medium |
| Cost | Moves POS peripherals into Access |
| Scalability | Fine |
| Team familiarity | Medium |
| Time to Block A | Touches Block A POS work |

**Pros:** One register. **Cons:** Receipt printers and kitchen displays would belong to the gate module.

---

## Trade-off Analysis

B puts the register where every device class already lives and leaves Access with the one fact that
is truly its own: where a device is placed. C would make the gate module own the kitchen's printers.

---

## Consequences

**Easier:** one device health view; one firmware report.
**Harder:** Access operations and screens change before the scanner work starts.
**Revisit:** none expected.

---

## Action Items

**Before B1 scanner tickets are cut (by 13 November)**

1. [x] Chinmay: accepted 1 October 2026. ADR-0015 marked amended.
2. [ ] Package: merge the columns into `platform.device`; create `access.device_placement`; rename and rewire the Access operations (`placeAccessDevice`); drop `device.enrolmentChanged`. New operations need a vocabulary permission. Re-derive, mirrors, check. (3 pts, the finding's estimate) — **Authored 1 October**: `platform.device` carries hardware type (shared `DeviceHardwareType`), model, serial, every version and component health; `access.access_device` became `access.device_placement` (declared rename); `registerAccessDevice` and `updateAccessDevice` became `placeAccessDevice` and `updateAccessDevicePlacement` (`DEVICE_CONFIGURE`); BO-194 and BO-196 rewired. **`device.enrolmentChanged` lost its access consumer but not its webhook subscribers (16.9.56)**, so it was not dropped: a person decides. Re-derive, mirrors and check at the next refresh.

**B1**

3. [ ] Build the placement operations with the scanner work. (about 3 pts)

## Amendment, 1 October 2026: `device.enrolmentChanged` stays for now (Chinmay)

The public-API webhook (16.9.56) still offers `device.enrolmentChanged` to outside subscribers, so it is not dropped yet: it is **deprecated in the webhook first** (marked in `public-api.yaml`), announced in a release note, and removed at the next major version of the public API. Internally nothing consumes it any more.
