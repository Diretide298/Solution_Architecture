# ADR-0043: The control plane splits on personal data

**Status:** Accepted
**Date:** 8 September 2026
**Decides:** **CF-167**, raised by [ADR-0039](0039-control-plane-and-tenant-database-lifecycle.md)
**Amends:** [ADR-0039](0039-control-plane-and-tenant-database-lifecycle.md) — it gave the control plane a database and did not say how many of them there are
**Depends on:** [ADR-0038](0038-cell-is-a-region-database-per-tenant.md), [ADR-0010](0010-cross-jurisdiction-entitlements.md), [ADR-0023](0023-pii-separation.md)

---

## Context

**Two requirements want the control plane in two places, and both are right.**

**It must be above every region.** ADR-0010 §1 puts the Guest Link Registry *"in the Control Plane,
pseudonymous only"* and orchestrates cross-region redemption *"from the Control Plane by
`guestLinkId`, fanning out to each linked cell."* A registry that fans out across regions cannot
live inside one of them.

**It must be inside one.** `control.onboarding_application` carries `company_name`, `contact_email`,
`contact_phone` and `country_code` — **a prospect's contact details, recorded before there is a
tenant to own them.** ADR-0038 — amended by ADR-0040, which lets a region hold more than one
instance — made residency structural by giving each region its own hardware, and a prospect's phone
number sitting in the wrong country is exactly the thing that was made structural.

**ADR-0039 gave `control` a database and did not say how many.** That is what blocks the
provisioning script, which has to connect to a control database *by name*, and `control.cell`, which
either lists every region's cells or only its own.

---

## Decision

**The control plane splits on personal data, which is the line ADR-0023 and ADR-0010 already draw.**

### 1 · One global control database, holding no natural person

`control` sits above every region and holds the platform's own record of itself: the cell registry,
`cell_instance` and placement (ADR-0042), releases and rollouts, licences and plans, migrations and
their fan-out, and **the Guest Link Registry, pseudonymous only.**

**It is 47 of the 50 `control` tables.** Measured, not assumed — the split is far cheaper than the
register expected, because the schema was already careful: `control.partner_user` carries a
`principal_id` and not a name, which is the pattern the rest of this decision generalises.

### 2 · One regional control database per region, for the three that do

`control_regional` sits on that region's own instance and holds what names a person:

| | what moves | why |
|---|---|---|
| `onboarding_application` | **the whole table** | its subject *is* a prospect; there is no non-personal remainder worth keeping |
| `developer_account` | `contact_email` only | its subject is an organisation, which is not a person |
| `tenant` | `billing_email` only | its subject is a tenant |

### 3 · The rule, so the next table does not need this ADR again

**A table goes regional when its subject is a natural person. A table whose subject is something
else stays global and the column that names a person is extracted.**

**This is the part worth keeping.** A list of three tables is an artefact that goes stale the next
time somebody adds a column; the rule is what decides that column. And it is deliberately *not*
"move any table containing personal data" — that would take `tenant` and `developer_account` with
it, and **a tenant record in one region is a platform that cannot see its own customers.**

---

## Consequences

**🔴 The global control plane needs an instance that is not in any region.** This is the real cost of
the decision and it is a new one: ADR-0038's instances are all regional, and hosting the global
control plane inside one of them would make every other region depend on that region being up. **A
control plane that fails when one region fails is not above the regions**, whatever the diagram says.

**Provisioning connects to two databases and the order matters.** The application is read from the
regional control database in the prospect's own jurisdiction; the tenant, cell and instance records
are written globally. **Verification still gates it** — ADR-0039's *nothing is provisioned until
verification passes* is unchanged.

**`control.cell` lists every region's cells.** It is global, which is what makes cross-region
redemption and placement possible at all, and it was the second thing CF-167 blocked.

**Reading a person costs a second connection.** An operator screen showing a prospect's contact
details reads globally for the application's status and regionally for its contact fields. **Three
tables' worth of joins is the price of the residency property**, and it is paid on admin screens
rather than on any guest path.

**Two databases called control is a naming hazard and it is named here.** They are `control` and
`control_regional`, never both called *the control plane* in the same sentence without saying which.

**The Guest Link Registry stays pseudonymous, and this is now load-bearing.** ADR-0010 already
required it; with the registry global, **pseudonymity is what keeps a global table from being a
global personal-data store.** A `guestLinkId` that became resolvable to a person in the global
database would undo this decision without amending it.

---

## When this is reopened

**A fourth table wants to go regional.** Apply the rule rather than this list. If the rule stops
answering cleanly — a table whose subject is genuinely both — that is the reopening.

**A jurisdiction requires the platform record itself to be local**, not only the person. The split
here assumes residency binds to natural persons, which is what PDPL and the DESC position address.
A rule that binds to *commercial* records would move `tenant` and `invoice`, and that is a different
topology, not an extension of this one.

**The global instance's own residency is questioned.** It holds no natural person by construction,
which is the argument for it being able to sit anywhere. **If that construction stops holding, so
does the argument.**

---

## Alternatives considered

**One global control plane only.** Rejected. It is simpler in every way except the one that matters:
a prospect's phone number ends up outside their jurisdiction, recorded before anyone has agreed to
anything, which is the weakest possible position to be in about consent.

**One control plane per region only.** Rejected. Cross-region redemption stops working —
ADR-0010's registry has to see across regions to fan out — and the cell registry becomes N partial
lists with no authority, so placement (ADR-0042) has nothing to read.

**Host the global control plane inside a designated home region.** Rejected, and it is the tempting
one because it costs no new instance. It makes every region's provisioning, licensing and
cross-region redemption depend on one region's availability, and **it converts a regional outage
into a platform outage** — which is precisely the coupling ADR-0038 spent a topology to avoid.

**Keep the whole `tenant` and `developer_account` rows regional.** Rejected. It satisfies the same
residency property and leaves the platform unable to list its own customers without querying every
region — and the extraction is three columns.
