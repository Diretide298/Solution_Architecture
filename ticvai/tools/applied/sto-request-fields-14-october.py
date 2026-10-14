#!/usr/bin/env python3
"""One-off, batch STO (Block A storage audit, 14 October 2026): every field a write takes is stored, or says it is not.
Already applied; kept as the record of what was changed and why. Idempotent.

* CHG-STO-016 (check-stored-request-fields SR-STORED-NO-COLUMN, SR-STUB-WRITE): a field the contract says is stored
  names the column that keeps it (`x-ticvai-stored-as`, and the lineage writes that table): an alert's
  acknowledgement note, a resource booking's check-out and return times, a case's opening attachments (on its
  first `CaseMessage`), an exchange line's recommendation (on its `orders.order_line`), a media asset's collections
  (`MediaCollectionMember` rows), a guest's dietary and accessibility preferences (`marketing.guest_preference`), a
  delivery location's serving outlets (one
  `fnb.delivery_location_outlet` row each). A field that is not kept says so: a deprecated, ignored `Theme.darkMode`,
  the saved card a dunning retry charges. `evaluateAccess` records its decision in `identity.access_decision` (the
  decision, the policy version and the attribute values it saw), which nothing wrote; the append-only
  `identity.authz_audit` trail (CHG-R6-014) is the authorisation layer's on every call, not this operation's write.
* CHG-STO-017 (check-request-fields-stored RF-REQUEST-NOT-STORED): each configuration write's field is one of: stored
  as an existing column (`x-ticvai-stored-as`: a game card's action is its status and its reason the blocked reason, a
  menu item's daily count, a table visit's service stage, a path's closure reason, a leaderboard nickname, a firmware's
  status reason, a wallet risk rule's status reason and end, an incident's escalation and the reason on its history
  row, a section's view photo); a new readOnly field on the resource that keeps it (a status's reason where the
  record had none, a closed path's expected reopening and note, a resource's lifecycle effective date, reason,
  replacement and disposal record, a journal entry's posting date, an access point's pending direction and reason, an
  accreditation's status dates, a channel incident's resolution note, a security alert's note, a booking change's
  reason, a table visit's note, a supplier's contacts, a menu item's unavailability note); or not stored
  (`x-ticvai-persisted: false`): an input the operation acts on and does not keep (a quote converted or accepted,
  a template's source map, a payment's return URL, device, wallet hold and cross-cell authorisation, an instalment
  count that is the number of instalment rows, a validate-only or force flag, the device time that orders a replay).

    python3 tools/applied/sto-request-fields-14-october.py [--apply]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sto_markers import Contracts  # noqa: E402

# (operationId, request field path, marker, value): the marker is placed where the field is declared
FIELD = [
    # CHG-STO-016
    ("acknowledgeAlert", "note", "x-ticvai-stored-as", "reporting.alert.acknowledgement_note"),
    ("checkInResource", "recordedAt", "x-ticvai-stored-as", "resources.booking.returned_at"),
    ("checkOutResource", "recordedAt", "x-ticvai-stored-as", "resources.booking.checked_out_at"),
    ("createCase", "attachmentRefs", "x-ticvai-stored-as", "marketing.case_message.attachment_refs"),
    ("retryMyDunningPayment", "paymentTokenId", "x-ticvai-persisted", False),
    ("setTheme", "darkMode", "x-ticvai-persisted", False),
    ("updateMediaAsset", "collectionIds", "x-ticvai-stored-as", "assets.media_collection_member.collection_id"),
    ("updateMyProfile", "accessibility", "x-ticvai-stored-as", "marketing.guest_preference.accessibility"),
    ("updateMyProfile", "dietary", "x-ticvai-stored-as", "marketing.guest_preference.dietary"),
    ("setDeliveryLocationOutletMapping", "mappings[].servingOutletIds", "x-ticvai-stored-as",
     "fnb.delivery_location_outlet.outlet_id"),
    # CHG-STO-017: stored as an existing column
    ("createGuestLink", "consentedAt", "x-ticvai-stored-as", "sync.guest_link.linked_at"),
    ("createGuestLink", "targetCellName", "x-ticvai-stored-as", "sync.guest_link.linked_cells"),
    ("createInstalmentPlan", "customDueDates", "x-ticvai-stored-as", "payments.instalment.due_date"),
    ("createInstalmentPlan", "firstDueDate", "x-ticvai-stored-as", "payments.instalment.due_date"),
    ("createShopAndDrop", "recordedAt", "x-ticvai-stored-as", "retail.shop_and_drop.dropped_at"),
    ("setAuthorisationPolicyState", "state", "x-ticvai-stored-as", "identity.authorisation_policy.status"),
    ("setDeviceFirmwareStatus", "reason", "x-ticvai-stored-as", "tenancy.device_firmware.status_reason"),
    ("setEntitlementTemplateBlackoutDates", "reason", "x-ticvai-stored-as", "catalogue.audit_entry.reason"),
    ("setGameCardLifecycle", "action", "x-ticvai-stored-as", "games.card.status"),
    ("setGameCardLifecycle", "reason", "x-ticvai-stored-as", "games.card.blocked_reason"),
    ("setItemAvailability", "reason", "x-ticvai-stored-as", "fnb.menu_item.unavailable_reason"),
    ("setLeaderboardNickname", "nickname", "x-ticvai-stored-as", "marketing.loyalty_position.leaderboard_nickname"),
    ("setMenuItemDailyCount", "count", "x-ticvai-stored-as", "fnb.menu_item.daily_count"),
    ("setPathClosure", "reason", "x-ticvai-stored-as", "venuemap.path.closed_reason"),
    ("setServiceStage", "stage", "x-ticvai-stored-as", "fnb.table_visit.service_stage"),
    ("setWalletAllocationPolicy", "fixedAmount", "x-ticvai-stored-as", "sync.wallet_authorisation.allocated_amount"),
    ("setWalletRiskRuleStatus", "reason", "x-ticvai-stored-as", "wallet.risk_rule.status_reason"),
    ("setWalletRiskRuleStatus", "until", "x-ticvai-stored-as", "wallet.risk_rule.status_until"),
    ("updateIncident", "escalate", "x-ticvai-stored-as", "maintenance.incident.escalation"),
    ("updateIncident", "reason", "x-ticvai-stored-as", "maintenance.incident_history.note"),
    ("updatePriceList", "isActive", "x-ticvai-stored-as", "catalogue.price_list.status"),
    ("updateSeatMap", "sectionViews", "x-ticvai-stored-as", "seating.section.view_asset_id"),
    # CHG-STO-017: stored in a new readOnly field of the resource (NEW_PROPS)
    ("setAccessAreaCapacity", "reason", "x-ticvai-stored-as", "access.configuration_change.reason"),
    ("setAccessPointDirection", "effectiveAt", "x-ticvai-stored-as", "access.access_point.direction_effective_at"),
    ("setAccessPointDirection", "reason", "x-ticvai-stored-as", "access.access_point.direction_change_reason"),
    ("setAccreditationStatus", "effectiveFrom", "x-ticvai-stored-as", "accreditation.holder.status_effective_from"),
    ("setAccreditationStatus", "reviewAt", "x-ticvai-stored-as", "accreditation.holder.status_review_at"),
    ("setApiClientStatus", "reason", "x-ticvai-stored-as", "control.api_client.status_reason"),
    ("setAuthorisationPolicyState", "reason", "x-ticvai-stored-as", "identity.authorisation_policy.status_reason"),
    ("setItemAvailability", "note", "x-ticvai-stored-as", "fnb.menu_item.unavailable_note"),
    ("setPathClosure", "expectedReopenAt", "x-ticvai-stored-as", "venuemap.path.expected_reopen_at"),
    ("setPathClosure", "isClosed", "x-ticvai-stored-as", "venuemap.path.is_closed"),
    ("setPathClosure", "note", "x-ticvai-stored-as", "venuemap.path.closed_note"),
    ("setResourceLifecycleState", "state", "x-ticvai-stored-as", "resources.resource.lifecycle_state"),
    ("setResourceLifecycleState", "effectiveFrom", "x-ticvai-stored-as",
     "resources.resource.lifecycle_effective_from"),
    ("setResourceLifecycleState", "reason", "x-ticvai-stored-as", "resources.resource.lifecycle_reason"),
    ("setResourceLifecycleState", "replacementResourceId", "x-ticvai-stored-as",
     "resources.resource.replacement_resource_id"),
    ("setResourceLifecycleState", "disposal", "x-ticvai-stored-as", "resources.resource.disposal"),
    ("setTransportRouteStatus", "reason", "x-ticvai-stored-as", "transport.route.status_reason"),
    ("setWalletAllocationPolicy", "percentage", "x-ticvai-stored-as", "sync.wallet_authorisation.share_percentage"),
    ("updateChannelIncident", "resolutionNote", "x-ticvai-stored-as", "catalogue.channel_incident.resolution_note"),
    ("updateRentalBooking", "reason", "x-ticvai-stored-as", "rental.booking.change_reason"),
    ("updateResourceBooking", "reason", "x-ticvai-stored-as", "resources.booking.change_reason"),
    ("updateSecurityAlert", "note", "x-ticvai-stored-as", "access.security_alert.note"),
    ("updateSupplier", "contacts", "x-ticvai-stored-as", "inventory.supplier.contacts"),
    ("updateTableVisit", "note", "x-ticvai-stored-as", "fnb.table_visit.note"),
    ("createJournalEntry", "postingDate", "x-ticvai-stored-as", "ledger.journal_entry.posting_date"),
    # the AI provider's key is a Key Vault secret; the row keeps its name (ADR-0063 as amended 14 October 2026)
    ("setAiCredential", "secret", "x-ticvai-secret", "vault-reference"),
    ("setAiCredential", "secret", "x-ticvai-stored-as", "ai.provider.credential_ref"),
    # CHG-STO-017: not stored
    ("createGroupBooking", "groupQuoteId", "x-ticvai-persisted", False),
    ("createGuestLink", "homeSubjectId", "x-ticvai-stored-as", "sync.guest_link.local_subject_id"),
    ("createGuestLink", "targetSubjectId", "x-ticvai-persisted", False),
    ("createInstalmentPlan", "instalmentCount", "x-ticvai-persisted", False),
    ("createOrder", "catalogueBundleVersion", "x-ticvai-persisted", False),
    ("createOrder", "guestLinkId", "x-ticvai-persisted", False),
    ("createPayment", "deviceId", "x-ticvai-persisted", False),
    ("createPayment", "returnUrl", "x-ticvai-persisted", False),
    ("createPayment", "walletAuthorisationId", "x-ticvai-persisted", False),
    ("createPayment", "walletHoldId", "x-ticvai-persisted", False),
    ("createRentalBooking", "acceptedQuoteId", "x-ticvai-persisted", False),
    ("createSeatMapTemplate", "sourceSeatMapId", "x-ticvai-persisted", False),
    ("setAiCredential", "graceMinutes", "x-ticvai-persisted", False),
    ("setGameCardLifecycle", "replacementCardId", "x-ticvai-persisted", False),
    ("setItemAvailability", "recordedAt", "x-ticvai-persisted", False),
    ("setKitchenTicketStatus", "recordedAt", "x-ticvai-persisted", False),
    ("setPathClosure", "force", "x-ticvai-persisted", False),
]
# (contract stem, resource schema, property, YAML body): the readOnly field that keeps a request field
NEW_PROPS = [
    ("access", "AccessConfigurationChange", "reason",
     "type: string\nmaxLength: 200\nnullable: true\nreadOnly: true\n"
     "description: Why the change was made, where the operation asks for one (`setAccessAreaCapacity`)."),
    ("access", "AccessPoint", "directionEffectiveAt",
     "type: string\nformat: date-time\nnullable: true\nreadOnly: true\n"
     "description: When a direction change set by `setAccessPointDirection` takes effect; held `pending` until then."),
    ("access", "AccessPoint", "directionChangeReason",
     "type: string\nmaxLength: 200\nnullable: true\nreadOnly: true\n"
     "description: Why the gate was last turned round (`setAccessPointDirection`)."),
    ("accreditation", "AccreditationHolder", "statusEffectiveFrom",
     "type: string\nformat: date-time\nnullable: true\nreadOnly: true\n"
     "description: When the status `setAccreditationStatus` set takes effect."),
    ("accreditation", "AccreditationHolder", "statusReviewAt",
     "type: string\nformat: date\nnullable: true\nreadOnly: true\n"
     "description: When the status is due for review (`setAccreditationStatus`)."),
    ("public-api", "ApiClient", "statusReason",
     "type: string\nmaxLength: 500\nnullable: true\nreadOnly: true\n"
     "description: Why the client was suspended (`setApiClientStatus`)."),
    ("identity", "AuthorisationPolicy", "statusReason",
     "type: string\nnullable: true\nreadOnly: true\n"
     "description: Why the policy's state last changed (`setAuthorisationPolicyState`)."),
    ("fnb", "MenuItem", "unavailableNote",
     "type: string\nmaxLength: 500\nnullable: true\nreadOnly: true\n"
     "description: The free text with an `other` unavailable reason (`setItemAvailability`); reviewed quarterly so the "
     "common ones become reasons (audit R222)."),
    ("venue-map", "VenuePath", "isClosed",
     "type: boolean\nreadOnly: true\ndefault: false\n"
     "description: Closed by `setPathClosure`; routing does not use a closed path."),
    ("venue-map", "VenuePath", "expectedReopenAt",
     "type: string\nformat: date-time\nnullable: true\nreadOnly: true\n"
     "description: When a closed path is expected to reopen (`setPathClosure`)."),
    ("venue-map", "VenuePath", "closedNote",
     "type: string\nmaxLength: 500\nnullable: true\nreadOnly: true\n"
     "description: The free text with an `other` closure reason (`setPathClosure`; audit R222)."),
    ("resources", "Resource", "lifecycleState",
     "allOf:\n- $ref: '#/components/schemas/ResourceLifecycleState'\nnullable: true\nreadOnly: true\n"
     "description: The lifecycle state `setResourceLifecycleState` set."),
    ("resources", "Resource", "lifecycleEffectiveFrom",
     "type: string\nformat: date-time\nnullable: true\nreadOnly: true\n"
     "description: When the lifecycle state takes effect (`setResourceLifecycleState`)."),
    ("resources", "Resource", "lifecycleReason",
     "type: string\nnullable: true\nreadOnly: true\n"
     "description: Why the lifecycle state changed (`setResourceLifecycleState`)."),
    ("resources", "Resource", "replacementResourceId",
     "type: string\nformat: uuid\nnullable: true\nreadOnly: true\nx-ticvai-references: resources.resource\n"
     "description: The resource that replaces this one, where it was retired for a replacement."),
    ("resources", "Resource", "disposal",
     "type: object\nadditionalProperties: true\nnullable: true\nreadOnly: true\n"
     "description: How a disposed resource left (`setResourceLifecycleState`), as given."),
    ("transport", "TransportRoute", "statusReason",
     "type: string\nmaxLength: 500\nnullable: true\nreadOnly: true\n"
     "description: Why the route's status last changed (`setTransportRouteStatus`)."),
    ("cross-region", "WalletAllocation", "sharePercentage",
     "type: number\nminimum: 0\nmaximum: 100\nnullable: true\nreadOnly: true\n"
     "description: The share of the wallet allocated, where the policy is a percentage (`setWalletAllocationPolicy`)."),
    ("catalogue", "ChannelIncident", "resolutionNote",
     "type: string\nmaxLength: 1000\nnullable: true\nreadOnly: true\n"
     "description: How the incident was resolved (`updateChannelIncident`)."),
    ("rental", "RentalBooking", "changeReason",
     "type: string\nnullable: true\nreadOnly: true\n"
     "description: Why the booking was last changed (`updateRentalBooking`)."),
    ("resources", "ResourceBooking", "changeReason",
     "type: string\nnullable: true\nreadOnly: true\n"
     "description: Why the booking was last changed (`updateResourceBooking`)."),
    ("access", "AccessSecurityAlert", "note",
     "type: string\nmaxLength: 1000\nnullable: true\nreadOnly: true\n"
     "description: The latest note on the alert (`updateSecurityAlert`)."),
    ("inventory", "Supplier", "contacts",
     "type: array\nreadOnly: true\nx-ticvai-persistence-kind: valueObject\nx-ticvai-persistence-column: jsonb\n"
     "description: Every contact `updateSupplier` was given; the first is also the primary contact's three fields.\n"
     "items:\n  type: object\n  additionalProperties: true"),
    ("fnb", "TableVisit", "note",
     "type: string\nmaxLength: 500\nnullable: true\nreadOnly: true\n"
     "description: The server's note on the visit (`updateTableVisit`)."),
    ("finance", "JournalEntry", "postingDate",
     "type: string\nformat: date\nnullable: true\nreadOnly: true\n"
     "description: The accounting day the entry posts on, in the region's time zone (`createJournalEntry`)."),
]
# operationId -> {"reads+": [...], "reads-": [...], "writes+": [...], "writes-": [...]}
LINEAGE = {
    "createCase": {"writes+": ["marketing.case_message"]},
    "exchangeOrderLines": {"writes+": ["orders.order_line"]},
    "updateMyProfile": {"writes+": ["marketing.guest_preference"]},
    # not this operation's write: the incident person's contact reaches pii through Identity, whose route is not
    # declared yet (a keep of CHG-STO-016)
    "addIncidentPerson": {"writes-": ["pii.subject_contact"]},
    "setEntitlementTemplateBlackoutDates": {"writes+": ["catalogue.audit_entry"]},
    "setWalletRiskRuleStatus": {"writes+": ["wallet.risk_rule"]},
    "updateIncident": {"writes+": ["maintenance.incident_history"]},
    # the authorisation layer appends to identity.authz_audit on every call (its storage note; CHG-R6-014), not this
    # operation; what evaluateAccess writes is its decision
    "evaluateAccess": {"writes+": ["identity.access_decision"], "writes-": ["identity.authz_audit"]},
}


def place(c, ops, oid, path, key, value):
    """Put the marker where the field is declared: the request body's component schema, or the inline body."""
    o = ops[oid]
    body = ((((o["op"].get("requestBody") or {}).get("content") or {}).get("application/json") or {})
            .get("schema") or {})
    ref = str(body.get("$ref") or "")
    if ref:
        stem = o["contract"]
        name = ref.rsplit("/", 1)[-1]
        if ".yaml#" in ref:
            stem = ref.split(".yaml#", 1)[0].rsplit("/", 1)[-1]
        return c.set_marker(stem, name, path, key, value)
    # an inline body's nested field: the first line naming it below requestBody (each is unique in its body)
    return c.set_body_marker(o["contract"], oid, path.rsplit("[].", 1)[-1], key, value), oid


def main() -> int:
    apply = "--apply" in sys.argv
    tic = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(tic / "tools"))
    import audit_guard as g
    ops = g.operations()
    c = Contracts(tic)
    n, bad = 0, 0
    for stem, schema, prop, block in NEW_PROPS:
        try:
            n += c.add_property(stem, schema, prop, block) != "="
        except LookupError as e:
            print("  !", e)
            bad += 1
    for oid, path, key, value in FIELD:
        try:
            how, where = place(c, ops, oid, path, key, value)
            n += how != "="
            if how != "=" and "--debug" in sys.argv:
                print("   ", how, oid, path, where)
        except (LookupError, ValueError, KeyError) as e:
            print("  !", oid, path, e)
            bad += 1
    print(f"  {n} contract edit(s), {bad} not found")
    lp = tic / "handoff" / "api-data-lineage.json"
    raw = lp.read_text(encoding="utf-8")
    lin = json.loads(raw)
    m = 0
    for oid, ch in LINEAGE.items():
        e = lin.get(oid)
        if e is None:
            print("  ! lineage has no", oid)
            bad += 1
            continue
        for k in ("reads", "writes"):
            cur = list(e.get(k) or [])
            new = [t for t in cur if t not in set(ch.get(k + "-", []))]
            if ch.get(k + "+"):
                new = sorted(set(new) | set(ch[k + "+"]))
            if new != cur:
                e[k] = new
                m += 1
    print(f"  {m} lineage entr(ies) changed")
    if apply and not bad:
        print("  wrote", ", ".join(c.save()) or "nothing")
        if m:
            indent = 1 if raw.startswith("{\n ") else None
            lp.write_text(json.dumps(lin, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""),
                          encoding="utf-8")
    elif not apply:
        print("dry run; pass --apply")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
