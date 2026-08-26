# Workshop packs — the three blocked domains

**212 requirements sit behind three workshops that have not been scheduled** (CF-21). This is
what we would take into each one.

The point of preparing them is that **two of the three are less blocked than the label
suggests.** Device Management is a lifecycle over a table we already have; Accreditation is an
application workflow in front of access machinery we already built. Going in with a proposal
turns a discovery session into a review, and a review is shorter.

Only Developer & API genuinely needs the conversation first, because its open questions are
commercial rather than technical.

---

## 1 — Accreditation & Credential Management · 58 reqs

**Schedule this one first.** Accreditation validation appears on the Wave 1 scanner, so this is
the only one of the three where waiting has a cost we can name: a steward at a service gate
scans a contractor's badge on the same handheld as a guest ticket, and today the handheld has
nothing to validate it against.

### What we already have

**The access half exists.** An accreditation is structurally an entitlement:

| It needs | We have |
|---|---|
| Zone and time-bounded access | `access.admission_profile` — allowed access points, open and close windows, max duration |
| Validated at a gate, offline | `validateAccess`, `scan_event`, the offline bundle |
| QR, NFC, RFID, printed badge | `MediaKind` — all four |
| Immediate revocation | `access.blacklist`, in the offline bundle |
| Holder identity, photo, documents | `pii.subject`, `subject_document`, `subject_biometric` |
| Approval before issue | `approvals` — routing, escalation, segregation of duties |

**What is genuinely missing is the front half**: an application form, a review workflow, and a
holder-type vocabulary.

### What we propose

**One satellite contract of roughly 25 operations, not a parallel access system.** Building a
second gate-validation path would be the expensive mistake here — two systems deciding who gets
in, diverging quietly.

### Decisions we need

| | |
|---|---|
| **Seven holder types confirmed?** | Staff, contractor, vendor, media, VIP, guest, government. Do they differ in anything but their approval route? |
| **Who approves each type?** | A media pass and a contractor pass are not the same risk |
| **Does an accreditation grant access, or request it?** | Whether the badge carries zones, or names a profile that does |
| **Sponsor model** | Does a contractor's accreditation belong to the contractor or the company that brought them |
| **Expiry and renewal** | Does a lapsed badge fail at the gate, or warn for a grace period |
| **Background-check integration** | 12.1.x implies verification. Against what, and who runs it |

### The matrix defect to raise

**All 58 requirements are filed under sub-domain "Reporting and Dashboards."** Application
forms, badge printing and revocation are not reporting. It runs the length of the domain and
suggests it was filled in quickly — **so the 58 may be thinner than the count implies**, which
is worth knowing before estimating.

---

## 2 — Device Management · 60 reqs

### What we already have

`platform.device` with **20 device kinds**, `recordDeviceHeartbeat`, and workstation assignment.
ADR-0015 holds: all 16 named hardware types resolve to a `DeviceKind`.

**What is missing is the lifecycle** — registration, enrolment, provisioning, activation,
deactivation, retirement — which is mechanical rather than contentious.

### What we propose

**Extend `tenancy` rather than a new contract.** A device belongs to a workstation which belongs
to a venue; splitting the lifecycle from the thing it manages would put one object in two
contracts.

### Decisions we need

| | |
|---|---|
| **Who enrols a device?** | A technician on site, or an administrator remotely |
| **What proves a device is itself?** | A certificate, a shared secret, or a code typed at enrolment. **This is the security decision in the domain** |
| **MDM or ours?** | The employee app and scanner ship via MDM (ADR-0006). Does device *enrolment* also, or does the platform own it |
| **Offline enrolment** | Can a device be enrolled with no network — matters for a venue opening a new gate |
| **Retirement and wipe** | What happens to a lost handheld holding an offline bundle and a scan journal |
| **Vendor SDKs** | CF-33 is still open on turnstile and payment terminal SDKs |

**The last one is the real blocker.** Everything else is ours to design.

---

## 3 — Developer & API Management · 94 reqs

**The only one where the conversation must come first**, because the open questions are
commercial.

### What we already have

**More than the requirement realises.** 13.1.5 asks for OpenAPI support; there are **26 contract
files and 737 operations** sitting in `contracts/`, and a documentation portal over them is
generation rather than authorship.

| Requirement | Position |
|---|---|
| API documentation portal | **The contracts exist.** A portal is a build, not a design |
| Endpoint documentation, schemas, examples | Already in the contracts |
| OpenAPI/Swagger | 3.1.0 throughout |
| Developer registration, keys, sandbox | **Nothing.** And it is a commercial question before a technical one |
| Rate limits, quotas, throttling | **Nothing.** Depends on what a partner is sold |
| Webhooks | Partial — the outbox and events exist; subscription management does not |

### Decisions we need

| | |
|---|---|
| **Who gets an API key?** | Any partner, approved partners, or only integrators TICVAI onboards |
| **Is the API a product?** | Charged, bundled with a plan, or free to contracted partners |
| **Rate limits by what?** | Plan tier, endpoint cost, or a flat ceiling |
| **Sandbox** | A separate cell with seeded data, or a flag on a real one. **Cost and residency both bite here** |
| **Versioning commitment** | How long a version is supported once superseded — a promise, not a technical choice |
| **Who supports integrators?** | TICVAI or the tenant whose data they are reaching |

**Until "is the API a product" is answered, the other five cannot be.**

---

## Scheduling

**Accreditation first** — Wave 1, and the scanner is the surface we most want to build.
**Device Management second** — mostly ours, one blocker (CF-33).
**Developer & API third** — the least urgent and the most commercial.

Each should be an hour with a proposal on screen, not a discovery session. **The two later ones
could be combined** if diary time is short, since both are largely confirmation.
