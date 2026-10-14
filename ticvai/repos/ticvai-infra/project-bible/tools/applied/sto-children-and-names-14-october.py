#!/usr/bin/env python3
"""One-off, batch STO (Block A storage audit, 14 October 2026): child keys, key names, double keys and stub tables.
Already applied; kept as the record of what was changed and why. Idempotent.

* CHG-STO-001 (SP-KEY-UNDECLARED, a member that appeared after the base derive): `KioskAssistSession.deviceId` ->
  `platform.device` (a kiosk session runs on one registered device).
* CHG-STO-005 (check-ddl-conventions D-FK-TARGET-NAME): a key column is named for the table it references (an
  `x-ticvai-column`, so the wire keeps its name; derive-schema-history.py COLUMN_RENAMES makes each a rename for the
  migration owner): an access change, a scan and a cross-region right point at `access.entitlement`, an admission rule
  point at `access.admission_rules`, a proposed action and a conversation message at `ai.activity` (renamed from
  `ai.interaction`), a performance's media at the `catalogue.event_registration` it names, a tax exemption's evidence
  at an `assets.media_asset`, a waiver signature at its `marketing.form_definition`, a selection policy at the
  `catalogue.product` that is the ticket type, a shop-and-drop at its `fnb.delivery_location`, a plan tier's allowance
  and module at `subscription.plan` (`/plans/{planId}/tiers`), and a channel allocation at its
  `catalogue.channel_capacity` (`channelCapacityId`, the path's id, now a field). A visit plan's guest is
  `pii.subject`, not `marketing.guest_profile`; the Fast Pass block is columns of `queue.queue` itself, not a key to it.
* CHG-STO-006 (D-DOUBLE-KEY): `org_unit_id` (named for the table renamed to `platform.scope`) is retired from
  `platform.venue_settings` and `platform.workstation`, which carry `venue_id` (and `region_id`, `department_id`).
* CHG-STO-004 (check-ddl-conventions D-CHILD-PARENT): a menu item sits in one section and the section in its menu
  (`MenuSection.items`: "an item's membership is `MenuItem.menuSectionId`"; createMenu and setMenuSections write both),
  so `menuSectionId` is required, never null, and a declared key to `fnb.menu_section`; derive-ddl ROW_OWNER makes
  the item follow its section (it followed its catalogue variant, a tenant row a venue grant cannot see).
  `rental.agreement_item` and `rental.inspection_item` already had their parent keys declared by CHG-STO-001
  (`rental_agreement_id`, `rental_inspection_id`); the check now reads a key named with its module in front.

    python3 tools/applied/sto-children-and-names-14-october.py [--apply]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sto_markers import Contracts  # noqa: E402

MARKERS = [
    # (contract stem, schema, property path, key, value)
    ("marketing-crm", "KioskAssistSession", "deviceId", "x-ticvai-references", "platform.device"),   # CHG-STO-001
    ("fnb", "MenuItem", "menuSectionId", "x-ticvai-references", "fnb.menu_section"),                  # CHG-STO-004
    # CHG-STO-005 (D-FK-TARGET-NAME): a key column is named for the table it references; the wire keeps its name
    ("access", "AccessAccessChange", "oldAccessId", "x-ticvai-column", "old_entitlement_id"),
    ("access", "AccessAccessChange", "newAccessId", "x-ticvai-column", "new_entitlement_id"),
    ("access", "AccessEntryRulePoint", "admissionProfileId", "x-ticvai-column", "admission_rules_id"),
    ("access", "ScanEvent", "ticketId", "x-ticvai-column", "entitlement_id"),
    ("ai", "ProposedAction", "interactionId", "x-ticvai-column", "activity_id"),
    ("catalogue", "PerformanceMediaAssignment", "participantId", "x-ticvai-column", "event_registration_id"),
    ("finance", "TaxExemption", "evidenceDocumentId", "x-ticvai-column", "evidence_asset_id"),
    ("marketing-crm", "ConversationMessage", "aiInteractionId", "x-ticvai-column", "ai_activity_id"),
    ("marketing-crm", "MarketingWaiverSignature", "templateId", "x-ticvai-column", "form_definition_id"),
    ("resources", "ResourceSelectionPolicy", "ticketTypeId", "x-ticvai-column", "ticket_product_id"),
    ("retail", "ShopAndDrop", "collectionPointId", "x-ticvai-column", "collection_location_id"),
    ("subscription", "SubscriptionTierAllowance", "tierId", "x-ticvai-column", "plan_id"),
    ("subscription", "SubscriptionTierModule", "tierId", "x-ticvai-column", "plan_id"),
    ("cross-region", "CrossRegionEntitlement", "ticketId", "x-ticvai-column", "entitlement_id"),
    # a guest's visit plan is the guest's: pii.subject, not the marketing profile (venuemap.visit_plan.subject_id)
    ("venue-map", "VisitPlan", "subjectId", "x-ticvai-references", "pii.subject"),
    # the Fast Pass block is columns of queue.queue itself (QueueFastPass persists to queue.queue): no key to itself
    ("queue", "QueueDetail", "fastPass", "x-ticvai-persisted", False),
]
# A renamed key keeps its target on the field, and its old column is retired, or last run's relationship graph puts the
# old column back beside the new one (derive-schema re-creates a graph edge's column unless the schema retires it).
RENAMED_KEYS = [
    # (contract stem, persisted schema, property, target, old column)
    ("access", "AccessAccessChange", "oldAccessId", "access.entitlement", "old_access_id"),
    ("access", "AccessAccessChange", "newAccessId", "access.entitlement", "new_access_id"),
    ("access", "AccessEntryRulePoint", "admissionProfileId", "access.admission_rules", "admission_profile_id"),
    ("access", "ScanEvent", "ticketId", "access.entitlement", "ticket_id"),
    ("ai", "ProposedAction", "interactionId", "ai.activity", "interaction_id"),
    ("catalogue", "PerformanceMediaAssignment", "participantId", "catalogue.event_registration", "participant_id"),
    ("finance", "TaxExemption", "evidenceDocumentId", "assets.media_asset", "evidence_document_id"),
    ("marketing-crm", "ConversationMessage", "aiInteractionId", "ai.activity", "ai_interaction_id"),
    ("marketing-crm", "MarketingWaiverSignature", "templateId", "marketing.form_definition", "template_id"),
    ("resources", "ResourceSelectionPolicy", "ticketTypeId", "catalogue.product", "ticket_type_id"),
    ("retail", "ShopAndDrop", "collectionPointId", "fnb.delivery_location", "collection_point_id"),
    ("subscription", "SubscriptionTierAllowance", "tierId", "subscription.plan", "tier_id"),
    ("subscription", "SubscriptionTierModule", "tierId", "subscription.plan", "tier_id"),
    ("cross-region", "CrossRegionEntitlement", "ticketId", "access.entitlement", "ticket_id"),
]
RETIRED = [
    # (contract stem, persisted schema, column)
    # CHG-STO-006 (D-DOUBLE-KEY): org_unit_id, named for the table renamed to platform.scope, beside venue_id
    ("tenancy", "VenueSettings", "org_unit_id"),
    ("tenancy", "Workstation", "org_unit_id"),
    # CHG-STO-005: the envelope's key to its capacity is channel_capacity_id (the contract's channelCapacityId)
    ("catalogue", "ChannelAllocation", "envelope_id"),
]
REQUIRED = [
    ("fnb", "MenuItem", "menuSectionId"),                                                              # CHG-STO-004
]
SCHEMA_EDITS = [
    # (contract stem, schema, old text, new text)
    ("catalogue", "ChannelAllocation",
     "        salesChannelId:\n",
     "        channelCapacityId:\n          type: string\n          format: uuid\n          readOnly: true\n"
     "          x-ticvai-references: catalogue.channel_capacity\n"
     "          description: The capacity envelope this allocation draws from (`catalogue.channel_capacity`), from the "
     "path of\n            `setChannelAllocations`.\n"
     "        salesChannelId:\n"),                                                                   # CHG-STO-005
    ("fnb", "MenuItem",
     "        menuSectionId:\n          x-ticvai-references: fnb.menu_section\n          type: string\n"
     "          format: uuid\n          nullable: true\n          readOnly: true\n",
     "        menuSectionId:\n          x-ticvai-references: fnb.menu_section\n          type: string\n"
     "          format: uuid\n          readOnly: true\n"),                                         # CHG-STO-004
]
OP_EDITS = []
TEXT_EDITS = [
    # CHG-STO-007 (D-RENAME-RESIDUE): prose names a table by the name it had before a declared rename
    ("ai", "record or an `ai.interaction`; a reader", "record or an `ai.activity`; a reader"),
    ("ai", "never in an `ai.interaction`.**", "never in an `ai.activity`.**"),
    ("subscription", "`ai.interaction` recorded tokens and cost per call", "`ai.activity` recorded tokens and cost per call"),
    ("subscription", "`ai.interaction` sits on the analytical store", "`ai.activity` sits on the analytical store"),
    ("reporting", "`queue.waiting_guest.estimated_call_at` against", "`queue.entry.estimated_call_at` against"),
    ("reporting", "`queue.waiting_guest` completions per hour", "`queue.entry` completions per hour"),
    ("white-label", "from `control.footer_config` and its two child tables.",
     "from `control.footer_config` (renamed `whitelabel.footer_config`) and its two child tables."),
    ("workforce", "`orders.shift` is a cash-handling session", "`orders.pos_shift` is a cash-handling session"),
]


def main() -> int:
    apply = "--apply" in sys.argv
    c = Contracts(Path(__file__).resolve().parents[2])
    bad = 0
    for stem, schema, path, key, value in MARKERS:
        try:
            how, where = c.set_marker(stem, schema, path, key, value)
            print(f"  {how} {where}.{path} {key}: {value}")
        except (LookupError, ValueError) as e:
            print("  !", e)
            bad += 1
    for stem, schema, prop, target, was in RENAMED_KEYS:
        how, where = c.set_marker(stem, schema, prop, "x-ticvai-references", target)
        print(f"  {how} {where}.{prop} x-ticvai-references: {target}")
        print(f"  {c.add_retired(stem, schema, was)} {stem}.{schema} retires {was}")
    for stem, schema, col in RETIRED:
        print(f"  {c.add_retired(stem, schema, col)} {stem}.{schema} retires {col}")
    for stem, schema, prop in REQUIRED:
        print(f"  {c.add_required(stem, schema, prop)} {stem}.{schema} required {prop}")
    for stem, schema, old, new in SCHEMA_EDITS:
        try:
            print(f"  {c.replace_in_schema(stem, schema, old, new)} {stem}.{schema}: {new.strip().splitlines()[0][:60]}")
        except LookupError as e:
            print("  !", e)
            bad += 1
    for stem, op, old, new in OP_EDITS:
        try:
            print(f"  {c.replace_in_op(stem, op, old, new)} {stem}.{op}: {new.strip()[:60]}")
        except LookupError as e:
            print("  !", e)
            bad += 1
    for stem, old, new in TEXT_EDITS:
        try:
            print(f"  {c.replace_text(stem, old, new)} {stem}: {new.strip()[:60]}")
        except LookupError as e:
            print("  !", e)
            bad += 1
    if apply and not bad:
        print("  wrote", ", ".join(c.save()) or "nothing")
    elif not apply:
        print("dry run; pass --apply")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
