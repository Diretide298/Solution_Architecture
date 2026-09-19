#!/usr/bin/env python3
"""Give every table a note saying what it holds, what it hangs off, and what reaches it.

**165 of 368 tables carried a note and the distribution was backwards.** `ai.index_entry` — an
obscure mapping table — had a good one; **`platform.scope`, the single most-referenced table in
the package, had none.** Notes went where somebody happened to be working rather than where a
reader needs them.

**Three parts, and only the first is written by hand:**

- **what it holds** — from the contract description, or the schema's own summary
- **what it hangs off** — its parent and its anchors, from `handoff/schema-reference.json`
- **what reaches it** — the operations and foreign writers, from `relationship-graph.json`

**The last two are derived and cannot drift.** A note that says *reached by 17 operations* and then
stops being true is worse than no note, which is why they are computed here rather than typed once.

Run: `python3 tools/derive-table-notes.py [--apply]`
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "handoff"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# **Written by hand, because a name cannot be derived into a meaning.** These are the tables whose
# name does not say what they hold — the rest get a note assembled from their shape alone.
WHAT = {
    "approvals.accreditation_badge": (
        "**The badge an approved accreditation actually issues**, held apart from the request "
        "that granted it. `zones` is the access it carries and `state` walks issued, expired "
        "and revoked — **a badge outlives the decision behind it**, which is why revoking one "
        "is a row here and not an edit to `approvals.request`. `revoked_reason` is required in "
        "practice for the same reason an empty state is: a badge that stops working without "
        "saying why sends someone to a gate to find out."),
    "control.archival_job": (
        "**One archival run against one table in one cell**, with what it moved and what it "
        "destroyed counted separately. `rows_archived` and `rows_purged` are two numbers because "
        "they are two different consequences — copying rows out is reversible and deleting them "
        "is not, and a single `rows_processed` would hide which of the two happened. `error` "
        "holds the failure text, because **an archival job that fails silently is a table that "
        "grows until something else breaks.**"),
    "control.backup_run": (
        "**One backup, and whether anyone has proved it restores.** `restore_tested_at` is the "
        "column that matters: a backup nobody has restored from is a belief, not a backup, and "
        "it is null far more often than `state` being `completed` suggests. `scope` names what "
        "was taken — a cell, a tenant database — because ADR-0038 makes those different sizes "
        "of loss."),
    "control.scaling_policy": (
        "**The bounds a service scales within inside one cell**, not the scaling itself. "
        "`replica_floor` and `replica_ceiling` are the decision; `target_utilisation_pct` and "
        "`scale_step_pct` are how fast it moves between them. **A ceiling is a cost limit and a "
        "floor is an availability one**, and a cell that hits its ceiling under load is a "
        "capacity decision someone has to take rather than a fault to page on."),
    "control.cell_tenant": (
        "**Which tenants live in which cell, and under what database name** (ADR-0038). The "
        "relation that replaced `control.cell.tenant_id`: a cell is a region and holds many "
        "tenants, so a tenant with venues in two regions has two rows, two cells and two "
        "databases. **`database_name` does not encode the region** — the instance already is the "
        "region, and a name that repeats it is a name that can contradict it. `status` walks "
        "provisioning, live, suspended, draining, dropped, and **a service resolves every "
        "request through this table** before it opens a connection."),
    "control.migration_run_tenant": (
        "**What one migration did to one tenant database** (ADR-0039). `migration_run_cell` "
        "exists so a partial failure is *named rather than counted*, and once a cell held two "
        "hundred tenants it counted: a run that succeeded for 180 and failed for 20 had one row "
        "saying `failed`. This is that row, one level down. **`database_name` is denormalised "
        "deliberately** — after a drop, the run record still has to say what it touched."),
    "control.rollout_tenant": (
        "**How far a release has reached into one tenant database** (ADR-0039). The per-tenant "
        "sibling of `control.rollout_cell`, which stays as the regional rollup. **The canary is "
        "a tenant, not a cell** — the point of a canary is that its failure is cheap, and a "
        "first cell holding two hundred databases is not a cheap failure. `wave` is therefore a "
        "set of tenants, and it may be a subset of one cell."),
    "control.burst_environment": (
        "**One flash sale's own environment, from provisioning to teardown** (ADR-0035). A cell "
        "stood up for a single performance, holding a catalogue snapshot taken at "
        "`snapshot_taken_at`, and **it cannot be decommissioned until `orders_taken` equals "
        "`orders_reconciled` plus `orders_rejected`** — which is what `reconciled_at` records and "
        "why `auto_decommission` has a `grace_minutes` rather than a timer. The five timestamps "
        "are the states in order: provisioned, live, drained, reconciled, decommissioned. "
        "**`sequence_high` is what the merge back reads**, because the sale issued order numbers "
        "the origin cell never saw."),
    "platform.scope": (
        "**One unit of the venue structure** — a tenant, a brand, a region, a venue, a department, "
        "a sub-department, a workstation or an outlet. Every row has a level, a parent and a "
        "materialised `path`, and **configuration resolves by walking that path upward until "
        "something answers.** Renamed from `org_unit` on 26 August: *node* said it was a tree and "
        "hid what the tree is of. **A row is an org unit; a `scope_path` is a pointer into it** — "
        "same structure, two roles."),
    "catalogue.channel_capacity": (
        "**How much of a performance each sales channel may sell.** Two hundred seats with eighty "
        "to the web, eighty to the box office and forty held back. Renamed from `envelope`, which "
        "was unguessable."),
    "catalogue.inventory_hold": (
        "**A short-lived claim on contended stock** while somebody decides. A seat in a basket is "
        "held, not sold — CF-115 settled that contended inventory is leased rather than reserved, "
        "and the hold expires on its own. Renamed from `lease`, which read as a rental agreement."),
    "catalogue.variant_dimension": (
        "**The axis a product varies along** — size, colour, session length. A t-shirt has one; a "
        "timed ticket has none. Renamed from `variant_dimension`."),
    "identity.delegated_access": (
        "**One person acting for another, or for a scope they do not own.** A parent managing a "
        "child's membership, a manager covering another venue for a week. Renamed from `grant`, "
        "which is a verb, a subsidy and a permission depending on who reads it."),
    "ledger.posting": (
        "**One side of a double-entry movement.** Renamed from `entry`, which sat beside "
        "`journal_entry` and `journal_line` — **three things called entry in one schema is a "
        "schema nobody reads twice.**"),
    "queue.entry": (
        "**A person in a virtual queue**, with their position and their window. Renamed from "
        "`entry`: it is somebody waiting, not a row in a log."),
    "access.admission_rules": (
        "**What a gate checks before it opens** — how early, how late, how many times, and which "
        "credentials count. Renamed from `admission_rules`, because *profile* reads as a person."),
    "platform.cross_region_entitlement": (
        "**Something bought in one jurisdiction and honoured in another.** ADR-0010: the guest does "
        "not move, a pseudonymous link does. Renamed from `cross_region_entitlement` — a right to redeem "
        "what, and where?"),
    "subscription.plan": (
        "**What a tenant pays for** — the modules, the limits, the price. Renamed from `plan`, "
        "which sat beside `migration_plan` and `production_plan`."),
    # **Written 31 August, ranked by reach.** 200 of 369 tables carried a note saying no
    # description had been written — honest, and useless to a reader. These forty are the ones most
    # referenced and most operated on, so a wrong sentence here misleads more people than anywhere
    # else in the package.
    #
    # **What it is, not what it holds.** A column list is already in the workbook; the sentence
    # earns its place only by saying something the columns cannot.
    "identity.principal": (
        "**A person who can be authorised** — staff, partner, platform operator. The most "
        "referenced table in the package at 122 incoming columns, because almost everything "
        "records who did it. **Not a guest**: a guest is a `pii.subject`, and ADR-0023 keeps them "
        "apart so a data-subject request has one place to answer from."),
    "pii.subject": (
        "**A guest, and the only table holding who they are.** Name, and through its children the "
        "contacts, documents and biometrics. **Isolated deliberately** — erasure is a delete here "
        "and a pseudonym everywhere else, which is what makes a DSAR answerable at all."),
    "orders.sales_order": (
        "**The sale.** What was bought, by whom, through which channel, at what scope. Every "
        "payment, refund, entitlement and ledger posting reaches back to a row here."),
    "catalogue.product": (
        "**What a venue sells** — admission, a session, a bundle, a membership, a locker. Not the "
        "instance: a product is the offer and `catalogue.performance` is the occasion."),
    "platform.outlet": (
        "**A commercial branch — a restaurant, a shop, a bar.** A sibling of department rather "
        "than a child (CF-138, ADR-0018): a department has requisitions and rotas, an outlet has "
        "a menu and stock, and modelling a restaurant as a department puts it in the staffing "
        "tree."),
    "ledger.account": (
        "**A line in the chart of accounts**, denominated in its own currency. One of four tables "
        "that genuinely differ from their region — a group consolidating across jurisdictions "
        "holds accounts in several."),
    "inventory.item": (
        "**Something a venue stocks**, distinct from something it sells. A bottle of syrup is an "
        "item and never a product; a t-shirt is both, joined through `retail.merchandise`."),
    "maintenance.asset": (
        "**A physical thing with a service history** — a lift, a chiller, a ride. Distinct from a "
        "resource, which is bookable: an asset is maintained and a resource is reserved."),
    "catalogue.entitlement_template": (
        "**The rules a ticket carries before anybody buys one** — validity, entries allowed, "
        "transferability, what a gate does with it. `access.entitlement` is the issued instance."),
    "fnb.table_visit": (
        "**One party at one table, from seating to settling.** Distinct from `fnb.table_session`, "
        "which is the device claim: a QR scanned at the table opens a session, and the visit is "
        "the hospitality event around it."),
    "orders.payment": (
        "**A tender against an order**, with the rate it converted at fixed on the row (CF-37). A "
        "payment reconciled next month is reconciled at the rate of the day it was taken."),
    "control.cell": (
        "**A deployment and a legal boundary at once** (ADR-0001). One per jurisdiction, carrying "
        "its cloud provider, region and endpoint. **Only `CrossRegionService` reaches another "
        "one**, and it moves a pseudonymous link rather than a guest."),
    "catalogue.performance": (
        "**When a product happens** — a session, a showing, a timed entry slot. Capacity lives "
        "here and in `catalogue.channel_capacity`, never on the product."),
    "catalogue.variant": (
        "**One sellable configuration of a product** — a size, a colour, a tier. Varies along the "
        "dimensions in `catalogue.variant_dimension`."),
    "reporting.report_definition": (
        "**A saved question, not its answer.** Columns, filters and parameters are children; a run "
        "is an `execution`, and the result set is cached in object storage rather than here."),
    "access.access_point": (
        "**A place a credential is presented** — a gate, a turnstile, a door, a scanner position. "
        "Carries the rules it applies through `access.admission_rules`."),
    "platform.workstation": (
        "**A till, a scanner, a kiosk — a place work happens.** The lowest organisational level. "
        "**Authority is the person\u2019s, not the workstation\u2019s** (ADR-0002), which is what makes a "
        "shared handheld safe."),
    "whitelabel.tenant_config": (
        "**Everything a tenant has branded or switched on.** Versioned, published, and the reason "
        "a guest storefront looks like the venue rather than like TICVAI."),
    "seating.seat_map": (
        "**The plan of a room** — sections, rows, seats, and what may combine with what. Versioned, "
        "so `diffSeatMapVersions` can answer what changed between two layouts."),
    "fnb.delivery_location": (
        "**Where food goes that is not a table** — a lounger, a cabana, a suite, a stand. Served "
        "by outlets through a join, because one kitchen serves several."),
    "identity.role": (
        "**A named set of permissions**, inheritable. A principal holds roles at scopes; the "
        "resolution walks the org tree upward until something answers."),
    "ledger.journal_entry": (
        "**A balanced set of postings.** Append-only: a correction is another entry, never an "
        "edit, which is what makes a period closeable."),
    "maintenance.work_order": (
        "**Something that needs doing to an asset**, raised by a person, an inspection or a "
        "schedule. The evidence attaches here."),
    "orders.order_line": (
        "**One thing bought on one order**, priced at the moment of sale. A price list changing "
        "afterwards does not change what somebody paid."),
    "orders.pos_shift": (
        "**A cash session at a workstation** — opened with a float, closed with a count and a "
        "variance. Moved to OrderService on 24 August because all its data is in `orders`."),
    "assets.media_asset": (
        "**An image, video or document with a licence and a lifecycle.** Referenced everywhere and "
        "owned by one service, so a takedown is one delete."),
    "control.tenant": (
        "**A customer of the platform** — the root of the org tree. `platform.tenant` is a "
        "one-column projection of this, so a cell can resolve its own tenant without reaching "
        "across a residency boundary."),
    "fnb.service_order": (
        "**Food and drink ordered**, wherever from — a counter, a table, a lounger, the app. The "
        "kitchen ticket is what the pass sees; this is what the guest bought."),
    "fnb.menu_item": (
        "**A product seen through a menu.** Catalogue owns whether it can be sold; F&B owns what a "
        "kitchen needs to make it \u2014 station, prep time, allergens, and the 86 flag."),
    "marketing.campaign": (
        "**A send with an audience and a schedule.** Every dispatch it produces is a "
        "`message_dispatch` row, which is where consent was checked."),
    "catalogue.event": (
        "**A named thing on at a venue**, grouping performances. A concert is an event; each "
        "showing is a performance."),
    "fnb.dining_table": (
        "**A physical table with a capacity and a position.** What may combine with what is "
        "declared rather than inferred \u2014 a pillar or a service run means two adjacent tables "
        "sometimes cannot."),
    "marketing.guest_profile": (
        "**What a venue knows about a guest that is not their identity** — preferences, lifetime "
        "value, segments, consent. Twenty operations touch it and it references `pii.subject` "
        "rather than duplicating it."),
    "fnb.kitchen_ticket": (
        "**What the pass sees.** One order can produce several, routed by station, and the clock "
        "on it is the kitchen\u2019s rather than the counter\u2019s."),
    "marketing.case": (
        "**A guest problem with a lifecycle** — raised, assigned, answered, closed. The messages "
        "are children; the SLA is not yet modelled."),
    "promotions.promotion": (
        "**A rule that changes a price**, with eligibility and a budget. Evaluated at the basket "
        "rather than stored on a product."),
    "queue.queue": (
        "**A line, physical or virtual.** The platform holds what a venue\u2019s own queue system "
        "reports (ADR-0012) rather than trying to be one."),
    "ledger.cost_center": (
        "**Where a cost lands.** Referenced by seven tables and operated on by two, because it is "
        "written once and read constantly."),
    "platform.device": (
        "**A physical thing that authenticates and does not authorise** — a scanner, a printer, a "
        "kitchen display. It proves which device; the person proves what they may do."),
    "inventory.requisition": (
        "**A department asking for stock**, which becomes a movement when fulfilled. The line "
        "items are children."),

    # **Second tranche.** Child tables and the rest of the spine — where a name is nearly enough
    # and the sentence exists to say the one thing it does not.
    "orders.refund": "**Money going back**, always against a payment and never editing it. The ledger posts both.",
    "orders.refund_policy": "**When a refund is allowed and what it costs.** Scoped, so a venue may be stricter than its tenant.",
    "orders.reservation": "**A held place that is not yet a sale** — a table, a cabana, a slot.",
    "orders.ticket_transfer": "**A ticket moving between people.** Claimed by whoever holds the link, which is why it expires.",
    "orders.b2b_credit": "**A partner\u2019s credit line**, drawn against and settled periodically.",
    "orders.cash_movement": "**Cash in or out of a drawer** — a float, a pickup, a drop, a payout. Denominated, and the audit trail behind a shift variance.",
    "catalogue.price": "**What something costs on one price list.** A change here never rewrites what somebody already paid.",
    "catalogue.price_list": "**A named set of prices for a region and channel.** Region-scoped, because currency is (ADR-0018).",
    "catalogue.channel_allocation": "**How much of a capacity each channel may sell.** Web cannot consume the counter\u2019s share.",
    "catalogue.published_bundle": "**A catalogue snapshot a till can trade from offline** (ADR-0013). Published, versioned, and the reason a counter works with no network.",
    "catalogue.alternative_code": "**Another way to name the same product** — a barcode, a supplier code, a legacy id.",
    "access.scan_event": "**Every presentation of a credential, admitted or not.** The highest-volume table in the platform.",
    "access.blacklist": "**Who may not be admitted**, and by whose authority.",
    "identity.mfa_method": "**A second factor a principal has enrolled.** Guests may enrol too, from 26 August.",
    "identity.sso_provider": "**A tenant\u2019s own identity provider.** A guest arriving through UAE Pass is verified in a way an email never is.",
    "identity.sso_group_mapping": "**Which provider group becomes which role.** The join that stops SSO meaning manual role assignment.",
    "ledger.journal_line": "**One side of a posting.** Entries balance; lines do not.",
    "ledger.fiscal_period": "**A window that closes.** Once closed, corrections post to the next one.",
    "ledger.settlement": "**Money actually arriving from a provider**, matched against what was taken.",
    "ledger.settlement_exception": "**A settlement that did not match.** The queue somebody works, not an error log.",
    "ledger.tax_code": "**A rate and its rules**, scoped to a region.",
    "ledger.legal_entity": "**Who the money belongs to.** A tenant may trade through several, which is why inter-entity rates exist.",
    "ledger.recognition_schedule": "**When deferred revenue becomes revenue** — a membership sold in March and earned across a year.",
    "ledger.price_variance": "**What was expected against what was invoiced.** Where a three-way match would post if it existed.",
    "marketing.message_dispatch": "**One message to one person.** Consent was checked here, which is why it is a row and not a log line.",
    "marketing.consent_record": "**What a guest agreed to and when.** A merge takes the narrower of two (CF-160).",
    "marketing.consent_purpose": "**What a tenant may ask consent for.** The question is the tenant\u2019s; the answer is the guest\u2019s.",
    "marketing.suppression": "**Who must not be contacted**, whatever a campaign says.",
    "marketing.loyalty_position": "**Where a guest stands** — points, tier, progress. A balance, not a history.",
    "marketing.segment": "**A rule that selects an audience**, evaluated rather than stored as a list.",
    "marketing.wishlist_item": "**Something a guest saved.** Per guest, synced across their devices.",
    "marketing.guest_device": "**A phone or browser a guest has registered.** How they revoke an old one that still holds tickets.",
    "retail.wallet": "**A guest balance**, holding money they paid in and bonus the venue gave them separately \u2014 the two refund differently.",
    "retail.wallet_transaction": "**Every movement on a wallet**, with the balance after. Append-only.",
    "retail.gift_card": "**Stored value somebody bought for somebody else.** Has a code, a face value, and can be blocked.",
    "retail.merchandise": "**A product a venue sells as goods**, joined to the catalogue rather than duplicating it.",
    "retail.shop_and_drop": "**Bought now, collected later.** The reason a guest is not carrying it round the park.",
    "retail.return_policy": "**When goods may come back and in what state.** Outlet-scoped.",
    "inventory.location": "**Where stock physically is** — a stockroom, a bar, a cellar.",
    "inventory.supplier": "**Who a venue buys from**, invoicing in their own currency.",
    "inventory.transfer": "**Stock moving between locations.** In transit is a state, not a gap.",
    "inventory.count": "**A stock take.** Its lines carry both the counted number and the recount, because two counts that agree is a different fact from one nobody checked.",
    "control.environment": "**Dev, staging, production — and which cells are in each.** Promotion may require approval and a soak period.",
    "control.rollout": "**One release reaching cells**, in waves, with a canary first.",
    "control.migration": "**A schema change with a version.** Plans group them; runs record what happened per cell.",
    "subscription.contract": "**What a tenant is paying for**, and which modules that licenses.",
    "control.invoice": "**A bill to a tenant.** Lines are children.",
    "control.usage_record": "**What a tenant consumed**, which is what an invoice is computed from.",
    "whitelabel.feature_toggle": "**A switch a tenant may throw**, distinct from a module they have licensed.",
    "whitelabel.module_enablement": "**Which modules a tenant has on.** The gate every `requiresModule` screen resolves against.",
    "whitelabel.policy": "**A tenant\u2019s own terms, privacy and cookie text**, versioned because agreeing to one version is not agreeing to the next.",
    "whitelabel.content_page": "**A page a tenant writes** — about, directions, accessibility.",
    "promotions.voucher": "**A named value a guest can spend**, with its own balance and expiry.",
    "promotions.coupon_campaign": "**A batch of codes with shared rules.** The codes are children.",
    "promotions.bundle": "**Several products sold as one**, with the components priced by allocation.",
    "promotions.upsell_rule": "**What to offer alongside what**, and where it may appear.",
    "seating.seat": "**One seat, addressable and holdable.** 396 rows in the sample manifest is one amphitheatre.",
    "seating.seat_hold": "**A temporary claim on a seat.** Expires, which is what stops two channels selling it.",
    "seating.seat_block": "**Seats withheld from sale** \u2014 house seats, accessibility, production hold.",
    "seating.section_row": "**A row within a section**, carrying its own numbering scheme.",
    "games.card": "**An arcade card holding credits.** The credit ledger is its history.",
    "games.play": "**One game played**, what it cost and what it won.",
    "games.prize": "**What credits can be redeemed for**, with its own stock.",
    "queue.reading": "**What a queue system reported at a moment.** The platform stores readings, not estimates.",
    "queue.feed": "**Where readings come from** — an adaptor to a venue\u2019s own system (ADR-0012).",
    "platform.dsar_request": "**A data-subject request and its progress.** The reason `pii` is a schema of its own.",
    "platform.guest_link": "**A pseudonymous link between cells** (ADR-0010). Carries no personal data, which is the point.",
    "platform.sale_board": "**What a till shows and in what order.** Configured by the venue, not by code.",
    "platform.region_settings": "**Currency, scale, timezone, fiscal year.** Region-scoped and not overridable below.",
    "maintenance.incident": "**Something that happened and needs recording** \u2014 distinct from a work order, which is something to do.",
    "maintenance.inspection": "**A completed check against a template.** The responses are children.",
    "maintenance.preventive_plan": "**What should be inspected, how often.** Generates work orders rather than being one.",
    "reporting.execution": "**One run of a report definition.** The result set is cached in object storage, not here.",
    "reporting.schedule": "**When a report runs and who receives it.**",
    "reporting.export": "**A file somebody asked for**, with an expiry.",

    # **Third tranche — the remainder.** Mostly child tables, where the parent already says what
    # the thing is and the sentence exists to say why the child is separate.
    "assets.media_collection": "**A named group of assets**, so a gallery is one reference rather than forty.",
    "assets.media_upload": "**An upload in progress**, with the ticket a client uses to send bytes directly.",
    "assets.media_usage": "**Where an asset is used.** What a takedown has to check before deleting.",
    "control.cell_job": "**Work running against a cell** — provisioning, migration, decommission.",
    "control.invoice_line": "**One charge on a tenant invoice**, traced to the usage that produced it.",
    "control.licence_add_on": "**Something bought beyond the plan.**",
    "control.migration_plan": "**A set of migrations to apply together**, with the cells they target.",
    "control.migration_plan_cell": "**One cell in a plan**, and its own readiness.",
    "control.migration_run": "**One execution of a plan.** Runs are append-only; a retry is a new run.",
    "control.migration_run_cell": "**What happened in one cell during one run.** Where a partial failure is named rather than counted.",
    "control.release_component": "**One service and version inside a release.** A release is not a single artefact.",
    "control.rollout_cell": "**One cell in a rollout** — its wave, whether it is the canary, and what version it moved between.",
    "control.support_notice": "**Something the platform is telling tenants**, scheduled or in progress.",
    "control.upgrade_schedule": "**When a tenant has agreed to be upgraded.** Not every tenant takes a release the day it ships.",
    "fnb.bill_split": "**How one table\u2019s bill was divided.** A party of six paying separately is the ordinary case.",
    "fnb.service_order_line": "**One item on a food order**, with its modifiers resolved at the moment of sale.",
    "fnb.kitchen_station": "**Where a ticket is routed** — grill, cold, bar, pass.",
    "fnb.kitchen_ticket_line": "**One item the kitchen is making**, bumped independently.",
    "fnb.location_session": "**A guest claim on a delivery location** — a lounger, a cabana. The equivalent of a table session away from a table.",
    "fnb.menu": "**What an outlet is offering**, versioned and published. Outlet-scoped (CF-138).",
    "fnb.menu_section": "**A run of items on a menu**, in the order the outlet set. Not alphabetical, or Desserts sits above Mains forever.",
    "fnb.modifier_group": "**A choice attached to an item** — how it is cooked, what is on it. Attached to the item, not chosen per sale (CF-160).",
    "fnb.modifier_option": "**One choice within a group**, with its own price delta.",
    "fnb.recipe": "**What an item is made of**, which is how a sale becomes a stock movement.",
    "fnb.recipe_ingredient": "**One component of a recipe**, in its own unit.",
    "fnb.table_session": "**A device claim on a table** — a QR scanned, an order opened. The hospitality event around it is a `table_visit`.",
    "games.game": "**A machine or attraction**, with its cost in credits.",
    "games.redemption": "**Credits exchanged for prizes.** Lines are children.",
    "games.redemption_line": "**One prize taken**, drawn against its stock.",
    "inventory.goods_receipt": "**Stock arriving against a purchase order.** Where a three-way match would begin.",
    "inventory.goods_receipt_line": "**One line received**, which may differ from what was ordered.",
    "inventory.movement": "**Every change in stock**, and the only truth about a level \u2014 `stock_level` is computed from these and never stored.",
    "inventory.purchase_order": "**A commitment to buy**, priced in the supplier\u2019s currency.",
    "inventory.purchase_order_line": "**One item ordered**, at a unit price.",
    "inventory.quotation": "**A supplier\u2019s price**, comparable against others.",
    "inventory.quotation_line": "**One item quoted.**",
    "inventory.requisition_line": "**One item asked for.**",
    "inventory.transfer_line": "**One item moving**, which is in neither location until it arrives.",
    "ledger.account_mapping": "**Which account a kind of transaction posts to.** Configuration, not a posting.",
    "ledger.tax_exemption": "**Who does not pay, and on what evidence.**",
    "maintenance.inspection_template": "**The questions an inspection asks.** Versioned, because changing them changes what past answers meant.",
    "maintenance.inspection_template_item": "**One question**, with its expected range.",
    "marketing.case_message": "**One exchange in a case**, from either side.",
    "marketing.loyalty_programme": "**The rules of earning and burning.** Tiers are children.",
    "marketing.loyalty_tier": "**One level**, with its threshold and benefits.",
    "marketing.message_template": "**Reusable content for a channel**, with the variables a dispatch fills.",
    "marketing.review": "**What a guest said afterwards**, with the venue\u2019s response and whether it is public.",
    "marketing.segment_criterion": "**One condition in a segment rule.**",
    "pii.subject_biometric": "**A face template, and nothing else.** Separate from contact and document so consent and erasure differ per kind.",
    "pii.subject_contact": "**An email, a phone.** The thing a marketing suppression matches on.",
    "pii.subject_document": "**A passport or ID, and its verification state.**",
    "platform.sale_board_page": "**One page of a till board**, holding tiles in position.",
    "platform.wallet_authorisation": "**A hold on a balance held in another jurisdiction**, with the rate it converted at fixed on authorisation rather than capture.",
    "promotions.allocation_split": "**How a bundle price divides across its components.** What the ledger posts against.",
    "promotions.allocation_component": "**One component\u2019s share**, fixed or proportional.",
    "promotions.bundle_component": "**One product inside a bundle**, with its quantity.",
    "promotions.coupon_code": "**One issued code**, with its own redemption state.",
    "promotions.voucher_batch": "**Vouchers issued together**, sharing rules and an expiry.",
    "reporting.dashboard": "**An arrangement of tiles**, each resolving its own source.",
    "reporting.dashboard_tile": "**One panel**, and the query behind it.",
    "reporting.report_column": "**One column of a definition**, with its aggregation.",
    "reporting.report_filter": "**A condition applied before aggregation.**",
    "reporting.report_parameter": "**Something the reader supplies at run time.**",
    "reporting.schedule_recipient": "**Who receives a scheduled report**, which is a consent question as well as a distribution one.",
    "retail.exchange": "**Goods swapped rather than returned**, which settles differently.",
    "retail.reservation": "**Merchandise held for collection.**",
    "retail.reservation_line": "**One item reserved.**",
    "retail.return": "**Goods coming back**, against the sale that produced them.",
    "retail.return_line": "**One item returned**, with its condition.",
    "retail.sale": "**A retail transaction**, distinct from an admission sale because it moves stock.",
    "retail.sale_line": "**One item sold**, which produces a stock movement.",
    "retail.shop_and_drop_line": "**One item bought for later collection.**",
    "seating.import_job": "**A seat map read from a plan or a manifest.** It proposes a draft; a person accepts it (ADR-0020).",
    "seating.seat_category": "**A price band or a physical class** — restricted view, accessible, premium.",
    "seating.seat_map_template": "**A known venue shape**, which raises the confidence of an import sharply.",
    "seating.seating_rules": "**How seats may be chosen** — best available, adjacency, party splitting.",
    "seating.section": "**A named part of a room**, holding rows.",
    "sync.rejection": "**An offline record the server refused**, with the reason. Kept, because a till that loses a rejected sale silently is worse than one that reports it.",
    "whitelabel.banner": "**A notice on a tenant storefront**, scheduled.",
    "whitelabel.config_version": "**One published version of a tenant\u2019s configuration.** Rolling back is selecting an earlier one.",
    "whitelabel.faq_category": "**A grouping of FAQ entries.**",
    "whitelabel.faq_entry": "**One question and answer**, localised.",
    "whitelabel.homepage_section": "**A block on a tenant homepage**, ordered. A section naming a disabled module must not render at all.",
    "whitelabel.navigation_item": "**One entry in a tenant\u2019s own navigation.**",
    "whitelabel.promo_block": "**A merchandising slot**, targeted and scheduled.",

    "platform.dead_letter": (
        "**An outbox row whose delivery failed after its retry budget** (ADR-0033). Carries the "
        "payload rather than a reference, because a dead letter you cannot replay is a log entry "
        "with a table's overhead. **A financial posting and a DSAR are never dead-lettered** \u2014 "
        "both halt and alert."),
    "ai.index_failure": (
        "**A document that would not chunk, embed or parse.** `ai.index_job` counts `records_failed` "
        "and holds a `failure_sample`; this is where the other 4,999 go. **`stage` decides who "
        "fixes it** \u2014 a parse failure is a document problem, an embed failure is a provider one."),

}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    S = json.loads((H / "schema-reference.json").read_text(encoding="utf-8"))
    lin = json.loads((H / "api-data-lineage.json").read_text(encoding="utf-8"))
    graph = json.loads((H / "relationship-graph.json").read_text(encoding="utf-8"))

    real = [t for t in sorted(S["cols"]) if "." in t and ":" not in t]
    storage = S.setdefault("storage", {})
    lineage = S.get("lineage") or {}

    # what reaches each table
    reads = defaultdict(set)
    writes = defaultdict(set)
    for o, v in lin.items():
        for t in v.get("reads", []):
            reads[t].add(o)
        for t in v.get("writes", []):
            writes[t].add(o)
    writers = defaultdict(set)
    for o, v in lin.items():
        for t in v.get("writes", []):
            writers[t].add(v.get("contract"))

    # incoming references
    incoming = Counter()
    for r in graph.get("rels", []):
        if r.get("to") and r.get("how") in ("declared", "convention"):
            incoming[r["to"]] += 1

    written = 0
    for t in real:
        existing = str(storage.get(t) or "").strip()
        parts = []

        # **The note is rebuilt, never extended.** An existing note ends with the two sentences this
        # loop writes, and reusing it whole appended them again on every refresh — found 17
        # September with 168 notes carrying the same *Hangs off* line up to a hundred times.
        kept = re.split(r"\s*\*\*(?:Hangs off|Reached by)\*\*:", existing, maxsplit=1)[0].strip()

        what = WHAT.get(t)
        if what:
            parts.append(what)
        elif kept:
            parts.append(kept)
        else:
            # **No hand-written meaning and no existing note.** Say what the shape says and no
            # more — an invented sentence is worse than an honest structural one.
            cols = len(S["cols"].get(t) or [])
            parts.append(f"Holds {cols} columns. **No description has been written for this "
                         "table** — the name is the only thing saying what it is.")

        # **What it hangs off, from its own row and not from the global anchor list.**
        # `lineage[t]["anchors"]` is the set of anchor tables in the package, the same for every
        # row — reading it per table produced *`fnb.menu_item` anchored on `pii.subject`*, which is
        # false and reads like a data-protection claim. **A list that is identical on every row is
        # not a property of the row.**
        #
        # `schemaRoot` is the real answer: the table this one reaches through its foreign keys.
        L = lineage.get(t) or {}
        hangs = []
        if L.get("parent"):
            hangs.append(f"a child of `{L['parent']}`")
        root = L.get("schemaRoot")
        if root and root != t and str(L.get("isSchemaRoot")) != "True":
            hangs.append(f"reaches `{root}` through its keys")
        elif str(L.get("isSchemaRoot")) == "True":
            hangs.append("**a root** — nothing above it in its schema")
        fk = [c["references"] for c in (S["cols"].get(t) or []) if c.get("references")]
        if fk:
            uniq = sorted(set(fk))[:3]
            hangs.append("references " + ", ".join(f"`{x}`" for x in uniq))
        if hangs:
            parts.append("**Hangs off**: " + "; ".join(hangs) + ".")

        # what reaches it
        nr, nw = len(reads.get(t, ())), len(writes.get(t, ()))
        foreign = sorted(writers.get(t, set()) - {None})
        reach = []
        if nr or nw:
            reach.append(f"{nr} operations read it and {nw} write it")
        if incoming.get(t):
            reach.append(f"{incoming[t]} tables reference it")
        if len(foreign) > 1:
            reach.append(f"**written by {len(foreign)} contracts** — "
                         + ", ".join(f"`{c}`" for c in foreign[:4]))
        if reach:
            parts.append("**Reached by**: " + "; ".join(reach) + ".")

        note = " ".join(parts)
        if note != existing:
            storage[t] = note
            written += 1

    if a.apply:
        (H / "schema-reference.json").write_text(
            json.dumps(S, indent=1, ensure_ascii=False), encoding="utf-8")

    have = len([t for t in real if str(storage.get(t) or "").strip()])
    print(f"  {written} notes {'written' if a.apply else 'would be written'}")
    print(f"  {have} of {len(real)} tables have one ({round(100 * have / len(real))}%)")
    if not a.apply:
        print("  nothing written — pass --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
