#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every read of another module's data takes a route ADR-0055 allows (amended 14 October 2026, CHG-GEN-009).

**ADR-0055 rule 2** says a module reads another module's schemas only through views the owner publishes or the
owner's in-process query interface, and rule 4 says that across deployables modules talk by event or by the published
contract, never by shared SQL. Nothing checked either: on 14 October `handoff/api-data-lineage.json` held 941
cross-module table reads in 517 of 2,796 operations, and the refusals the developers raised that day (ADAM CR-081,
CR-083, CR-084) were rule questions answered by reading another module's tables raw, some across deployables, some
not in the lineage at all. The amendment of 14 October makes the pattern one: **a rule question is asked of the owner
by a declared query**.

  * The owner declares the question in a top-level `x-ticvai-queries:` map in its contract:
    `<queryName>: {module, inputs, returns, rule, served: [in-process, service, projection]}`.
  * The asking operation names it: `x-ticvai-read-via: [{query: <contract>#<queryName>, route, for}]`, copied into
    the lineage as `readVia` by `tools/derive-lineage.py`. `in-process` is the owner's C# query interface, called in
    the caller's transaction, within one deployable; `service` is the owner's serviceAuth operation, across
    deployables; `projection` is a local copy the asker keeps, fed by the owner's events.
  * A generated view `<table>_for_<reader>` (DB-READ-VIEWS) is for bulk data reads within one deployable only.

Rules:

    XR-UNCOVERED    a lineage read of a table another module owns that is not a view named for the reader and is
                    not covered by a readVia to a query of the owning module
    XR-VIEW-ACROSS  a `<table>_for_<reader>` view read from another deployable (across deployables: service or
                    projection, never a view)
    XR-QUERY        a readVia that names no declared query, a query declared without module, inputs, returns, rule
                    or served, or a query whose module does not own the contract that declares it
    XR-ROUTE        a route that is not in-process, service or projection, not one the query serves, or in-process
                    across deployables, unless the lead granted that read (docs/active/cross-deployable-writes.yaml
                    `reads`: the reader's deployable, the query; ADAM CR-196, CHG-R9CR-005)
    XR-FOUNDATION   Identity (the foundation module every request resolves through, ADR-0028 tiers) reads a module
                    above it other than through a projection
    XR-LINEAGE      the lineage's readVia differs from the contract's x-ticvai-read-via (derive-lineage --apply)
    XR-FACT         an operation's own text (description, parameters, request and response descriptions, the
                    fields of its contract's schemas it uses) names a table another module owns, a field of a
                    schema another module's contract persists, or a phrase of FACTS, and the operation asks no
                    query over that table (ADAM CR-096 and CR-135, 15-17 October 2026; CHG-RTE-001). The
                    lineage holds only the tables behind response schemas (derive-lineage.py), so a rule stated in
                    words read data no rule above could see. A read (GET) counts a fact its own words name, or one
                    its response schema says is worked out on read (computed on read, resolved from, a projection
                    over); a fact only in its response schema is the writer's rule (CHG-RTE-001's fix round 1, the
                    check's rule since CHG-R10GEN-001). The sentences the r10 dry run read as not reads (a contrast,
                    a cited shape, who writes it) are NOT_READ, or NOT_READ_FOR the operations they are not reads for.

**The class release, 25 October 2026** (r10 lane E, CHG-R10GEN-001; PROCESS-LOG P-30). The 720 XR-FACT findings of r9
were baselined on 18 October and acknowledged on started tickets until a class release that never ran, and about 13
of the 48 CRs of 21-24 October were among them (listDepositBoxes' drawer limits, CR-218). With the read rule above
and the dry run's NOT_READ, 198 remain, and tools/applied/read-routes-r10.py routes all but the two an Identity
operation would ask above the foundation tier (getMembership's guest link, guestUaePassLogin's custom domain), which
are the lead's.

A read counts as covered only by a query over that table (its `table`, its projection's `source`, its `reads`),
or by a rule query of the owner that names no table: until 18 October any query of the owner covered every one of
its tables, and allocateDepositBox's workstation query would have covered Tenancy's denominations (CR-135).
`--list-facts` prints the XR-FACT class query: operation, reader, table, owner, how, phrase.

Kernel tables every deployable reads directly (`platform.scope`, `platform.idempotency_record`; ADAM CR-002) are not
cross-module reads. The reads already in the lineage on 14 October are baselined in handoff/audit-baseline.json; a
read by an operation the r6 batches fix (MUST_FIX) can never be baselined.

    python tools/check-cross-module-reads.py [--all] [--update-baseline] [--list-facts]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "XR-UNCOVERED": "a read of another module's table that is neither a view named for the reader nor covered by a "
                    "readVia to the owner's declared query (ADR-0055 rule 2, amended 14 Oct; CHG-GEN-009)",
    "XR-VIEW-ACROSS": "a view named for the reader read from another deployable (rule 4: service or projection)",
    "XR-QUERY": "a readVia naming no declared query, or a query declared incompletely or by a module that does not "
                "own its contract",
    "XR-ROUTE": "a route not in-process / service / projection, not served by the query, or in-process across "
                "deployables",
    "XR-FOUNDATION": "Identity reads a module above it other than through a projection (ADR-0028 tiers)",
    "XR-LINEAGE": "the lineage's readVia differs from the contract's x-ticvai-read-via",
    "XR-FACT": "an operation's text names another module's table, field or fact (FACTS) and asks no query over that "
               "table (ADAM CR-096, CR-135; CHG-RTE-001)",
}
ROUTES = ("in-process", "service", "projection")
QUERY_FIELDS = ("module", "inputs", "returns", "rule", "served")
# Kernel tables every deployable's role reads directly (ADAM CR-002, docs/active/cross-deployable-writes.yaml).
KERNEL_READ = {"platform.scope", "platform.idempotency_record"}
# The module that reads nothing above it but through a projection (ADR-0028 "Foundation ... reads nothing above").
# Tenancy shares the foundation tier but asks commerce modules in-process inside `commerce` (CR-083: configureWorkstation
# asks Orders whether a shift is open), as the amendment of 14 October records.
FOUNDATION_STRICT = {"IdentityService"}
# **Reads the r6 batches fix, which may never be baselined** (audit of 14 October): the operation and the owning
# modules whose data its refusal or step-up asks about.
MUST_FIX = {
    "createSaleBoard": {"CatalogueService"},          # CR-081, batch TEN
    "updateSaleBoard": {"CatalogueService"},          # CR-081, batch TEN
    "configureWorkstation": {"OrderService"},         # CR-083, batch TEN
    "deleteGuestAccount": {"AccessService", "OrderService"},   # CR-084, batch GDL
    "exportSubjectData": {"AccessService", "OrderService"},    # CR-084, batch GDL
    # CR-078: the PIN step-up operations verify a PIN through Identity's published query (batch CRD)
    "reopenShift": {"IdentityService"},
    "closeShift": {"IdentityService"},
    "acceptShiftVariance": {"IdentityService"},
    "rejectShiftVariance": {"IdentityService"},
    "withdrawFromDepositBox": {"IdentityService"},
    "cancelPerformance": {"IdentityService"},
    "recountStockCount": {"IdentityService"},
    "closeTransferShort": {"IdentityService"},
    "listActiveSessions": {"IdentityService"},
}


def slug(service: str) -> str:
    return re.sub(r"Service$", "", service).lower()


def contract_ops() -> dict:
    """operationId -> the operation, from every contract."""
    return {o: f["op"] for o, f in g.operations().items()}


def granted_reads() -> set:
    """(reader deployable, `<contract>#<query>`) the lead granted in process across deployables (ADAM CR-196,
    CHG-R9CR-005): the `reads` of docs/active/cross-deployable-writes.yaml."""
    import yaml
    p = g.ROOT / "docs" / "active" / "cross-deployable-writes.yaml"
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else {}
    return {(str(r.get("reader")), str(q)) for r in (doc or {}).get("reads") or [] for q in r.get("queries") or []}


def declared_queries() -> dict:
    """`<contract>#<queryName>` -> (contract stem, the declaration)."""
    out = {}
    for stem, rel, doc in g.contracts():
        for name, q in ((doc or {}).get("x-ticvai-queries") or {}).items():
            out[f"{stem}#{name}"] = (stem, q if isinstance(q, dict) else {})
    return out


# **A fact named in an operation's text is a read too** (ADAM CR-096 and CR-135; CHG-RTE-001). The words that name
# another module's fact, phrase -> the table that holds it. A phrase joins or leaves with the change that shows the
# need, as check-error-sources' ENTITIES do. Each is one a CR of 15-17 October found unrouted.
FACTS = {
    r"\bregion'?s (?:time ?zone|clock|calendar)": "platform.region_settings",      # createPerformances (CR-096)
    r"\bregion settings?\b": "platform.region_settings",
    r"\bvenue settings?\b": "platform.venue_settings",                              # publishPromotion (CR-096)
    r"\bvenue'?s `?cashDrawerLimit\b": "platform.venue_settings",                   # allocateDepositBox (CR-135)
    r"\bvenue'?s (?:frozen )?trading currency\b": "platform.venue_settings",        # CR-135
    r"\bactive venues\b|\bscope node is active\b": "platform.scope",                # setAnalyticsProvider (CR-096)
    r"\banother tenant\b": "control.tenant_domain",                                 # claimCustomDomain (CR-096)
    r"\blicen[cs]e allows\b|\badd-on keyed\b": "control.licence_add_on",            # setBrandIdentity (CR-096)
    r"\blive promotions?\b": "promotions.promotion",                                # lookupMerchandise (CR-096)
    r"\bticket and pass templates\b": "orders.ticket_template",                     # createPreview (CR-096)
    r"\bdenominations?\b": "platform.denomination",                                 # allocateDepositBox (CR-135)
    r"\bcell serving\b|\bits cell\b": "control.cell",                               # getPlatformSubdomain (CR-096)
    r"\bcollection point\b": "fnb.delivery_location",                               # createShopAndDrop (CR-096)
    r"\btax codes?\b": "ledger.tax_code",                                           # publishBundle (CR-110)
    r"\bno rate for\b|\bexchange rates?\b": "ledger.fx_rate",                       # setVenueSettings (CR-096)
    # getOrderCalendarEvent (ADAM CR-199, CHG-R9CR-006): "the session start and end" of a ticket line are the
    # performance's, Catalogue's data, and the operation declared no read of them.
    r"\bsession start and end\b|\bperformance'?s `?(?:startsAt|endsAt|starts_at|ends_at)\b": "catalogue.performance",
}
FACT_RES = [(re.compile(p, re.I), t) for p, t in FACTS.items()]
# Phrases where a fact's words are not a read of it, removed before matching (check-error-sources NOT_ENTITY works
# the same way). Each one names the operations whose text showed the need (the CHG-RTE-001 dry run, 18 October).
NOT_READ: tuple = tuple(re.compile(p, re.I | re.S) for p in (
    # fix round 1 (18 October 2026, the task review):
    r"cell serving this region",                # getRegionSettings, updateRegionSettings: the region's own cell_name
    r"under its cell's stem",                   # resolveTenantHost: how the hostname is built; its row has cellId
    # the stored-currency sentence repeated in five schemas (Shift, RegionSettings, ...): it names four tables to
    # say they keep their own currency, not to read them; its wrapping breaks inside words (`ledger.ac\ncount`)
    r"Four\s+tables\s+genuinely\s+differ\s+from\s+their\s+region\s+and\s+keep\s+a\s+stored\s+currency"
    r".*?`control\.partner_agreement`",
    r"never from another tenant's data",        # getAiVenueSettings, setAiVenueSettings: no other tenant is read
    r"phone number or collection point",        # deliverCredential: a credential's collection desk, not F&B's
    r"moves with the exchange rate",            # listChannelListings, setChannelListing, listPartnerAgreements
    r"not the denomination of an amount",       # setCurrencyRoundingRule: the word, not a till denomination
    r"Denominations, (?:validity, activation|whether an open amount)",   # setGiftCardProduct: gift card values
    r"rather than a venue setting",             # listDiningOutlets: says what is not a venue setting
    r"introduced later as a venue setting",     # createJournalEntry: a setting that does not exist yet
    r"appears on tax codes, FX rates",          # listProducts, cloneProduct and the product family: a comparison
    # r8 integration (20 October 2026, CHG-R8INT-017): two sentences that name a table to say Identity does not read it
    r"never reads\s+`orders\.pos_shift`",      # Session.hasOpenShift (forceLogout, listSessions): fed by events
    r"`marketing\.device_consent\.scope_path`;\s+Identity\s+may\s+not\s+read\s+that\s+table",  # recordConsentIdentifier
    # r10 lane E (25 October 2026, CHG-R10GEN-001): the read-routes-r10 dry run, read group by group. Each sentence
    # names another module's table, field or schema to contrast, to explain where something lives, to cite a shape it
    # follows, or to say who writes it; none is a read by the operation that carries it.
    r"`accessPoint`\s+is\s+a\s+gate\s+\(access\s+`AccessPoint`\),\s+`operatingArea`\s+a\s+zone\s+of\s+the\s+venue\s+"
    r"\(tenancy\),\s+`outlet`\s+an\s+outlet\s+\(tenancy\s+`Outlet`\)",          # the kiosk-config family: kinds of place
    r"`access`\s+keeps\s+every\s+issued\s+credential.{0,200}?in\s+`access\.accreditation_credential`",   # verify...Credential
    r"`AdmissionRules`\s+may\s+carry\s+a\s+`biometricPolicy`",                  # get/setVenueSettings(Defaults)
    r"is\s+now\s+`access\.device_placement`\s+and\s+holds\s+only",              # approveDevice, enrolDevice, registerDevice
    r"Access\s+keeps\s+only\s+where\s+an\s+access-control\s+device\s+is\s+placed\s+\(`access\.device_placement`",  # listDevices
    r"the\s+access\s+contract's\s+(?:validation\s+against\s+)?`AccessDynamicPolicy`(?:\s+\(`access\.dynamic_policy`\))?",
    r"beside\s+access's\s+`AccessDynamicPolicy`",                                # the Identity policy family: the other engine
    r"Software-permission\s+policies\s+are\s+identity's\s+`AuthorisationPolicy`",  # listDynamicPolicyEffectiveness
    r"Not\s+identity\.authorisation_policy,\s+which\s+is\s+staff\s+permission",  # setVisualDynamicPolicy, validateAccess
    r"The\s+mechanism\s+already\s+existed\W+`access\.entitlement`\s+carries",   # the product family: open-dated passes
    r"the\s+entitlement\s+is\s+written\s+by\s+OrderService\s+\(`access\.entitlement`",   # respondToInvitation
    r"Live\s+counters\s+stay\s+on\s+access\.entitlement",                        # setMembershipUsagePolicy
    r"The\s+limit\s+is\s+the\s+venue's\s+offline\s+policy\s+\(access\s+`AccessOfflinePolicy`\),\s+carried\s+in\s+the\s+"
    r"reader's\s+edge\s+package",                                                # reportReaderQueue: the reader decides
    r"A\s+product's\s+own\s+override\s+\(access\s+`AccessVerificationMethodPolicy\.credentialFormatOverride`\)\s+wins\s+"
    r"over\s+this",                                                              # setChannelFeePayment
    r"Null:\s+the\s+product\s+takes\s+its\s+sales\s+channel's\s+`ticketCredentialFormat`\s+\(catalogue\s+"
    r"`SalesChannelProfile`\)",                                                  # setVerificationMethodPolicy
    r"`suggestionRef`\s+is\s+the\s+id\s+of\s+its\s+`AiGuidedChoiceSuggestion`",  # proposeGuidedChoice
    r"records\s+the\s+question\s+as\s+an\s+`ai\.knowledge_gap`",                 # askReportingQuestion: ai writes it
    r"turns\s+into\s+\"not\s+available\s+yet\"\s+and\s+an\s+`ai\.knowledge_gap`",   # runSemanticQuery
    r"The\s+`AiProvider\.residency`\s+values\s+a\s+tenant\s+in\s+this\s+region\s+may\s+use",  # updateRegionSettings
    r"goes\s+through\s+approvals\.request",                                      # updatePartnerAgreement: a write
    r"\*\*Not\s+`approvals\.sla_policy`,\s+which\s+times\s+an\s+approval\s+request\.\*\*",   # listSlaPolicies
    r"Setting\s+the\s+list\s+records\s+each\s+reference\s+as\s+asset\s+usage\s+\(`MediaUsage`",  # the product family
    r"`EntitlementTemplate\.crossesCells`\s+already\s+propagates\s+a\s+redemption\s+right\s+on\s+issue",  # getMembership
    r"\*\*Creating\s+a\s+route\s+creates\s+its\s+catalogue\s+side\*\*\W+a\s+catalogue\s+`Event`",   # createTransportRoute
    r"`performanceId`\s+is\s+a\s+`catalogue\.performance`\s+id",                 # getPerformanceManifest: a key
    r"The\s+catalogue\s+Performance\s+the\s+manifest\s+belongs\s+to\s+\(`catalogue\.performance`\)",  # reorder...Manifest
    r"the\s+same\s+defect\s+`Product\.onSaleFrom`\s+fixed",                      # the content-block family
    r"Catalogue\s+`Product\.segmentTags`,\s+e\.g\.\s+a\s+level\s+tag",           # the guided-choice family: filter names
    r"checked\s+against\s+each\s+product's\s+age\s+rule\s+\(catalogue\s+`ProductEligibilityRule`\)",
    r"`catalogue\.product`\s+(?:is\s+reindexed\s+when|names)\s+`catalogue\.productPublished`",   # list/setIndexSource
    r"for\s+the\s+same\s+reason\s+`ProductCategory`\s+does",                     # listModules
    r"the\s+field\s+definitions\s+travel\s+in\s+the\s+catalogue\s+bundle\s+\(`catalogue\.CatalogueBundle\.payload`\)",
    r"`control\.integration_listing`\s+is\s+the\s+marketplace\s+entry\s+an\s+adapter\s+comes\s+from",
    r"The\s+subscription\s+contract's\s+billing\s+entity\s+and\s+`PartnerDocument`\s+read\s+this\s+list",
    r"`seating\.seat_reservation_item`\s+and\s+`control\.rollout`\s+both\s+point\s+at\s+it",   # listWalletHolds
    r"which\s+writes\s+`control\.tenant_domain`",                                # verifyCustomDomain: a call
    r"`fnb\.FnbReservationPolicy\.reservedLeadMinutes`\s+is\s+canonical",        # the venue-settings family
    r"deprecated\s+in\s+favour\s+of\s+`fnb\.FnbReservationPolicy\.reservedLeadMinutes`",
    r"tenancy\s+`VenueSettings\.fnb\.tableReservedLeadMinutes`\s+is\s+deprecated\s+in\s+its\s+favour",
    r"`identity\.customer_membership\.auto_renew`\s+carries\s+the\s+flag\s+per\s+holder",   # entitlement templates
    r"`orders\.membership_renewal`\s+records\s+`previousExpiryAt`\s+and\s+`newExpiryAt`",
    r"never\s+become\s+`identity\.principal`\s+or\s+`identity\.delegated_access`\s+rows",   # setDeveloperMembers
    r"put\s+it\s+on\s+the\s+tenant's\s+`PasswordPolicy`,\s+which\s+no\s+longer\s+carries\s+it",
    r"Identity's\s+projection\s+of\s+what\s+each\s+guest\s+holds\s+\(`SubjectHolding`\)\s+learns",  # an event
    r"\*\*Not\s+the\s+same\s+as\s+a\s+procurement\s+quotation\*\*\s+-\s+`inventory\.quotation`",
    r"The\s+supplier\s+is\s+an\s+`inventory\.supplier`",                         # updateVendorServiceRequest: a key
    r"\*\*not\*\*\s+`ledger\.deposit`,\s+which\s+is\s+the\s+liability\s+posting",   # listDepositActivity
    r"`ledger\.deposit`\s+holds\s+the\s+liability\s+posting\s+and\s+its\s+`refundableUntil`",   # listDeposits
    r"the\s+precision\s+`finance\.FxRate\.rate`\s+asks\s+for",                   # every rate field: a precision
    r"`ledger\.journal_entry`\s+is\s+append-only\s+and\s+a\s+failed\s+posting\s+is\s+an\s+incident",  # dead letters
    r"`sync\.dsar_request`\s+carries\s+a\s+legal\s+clock",
    r"for\s+the\s+same\s+reason\s+`maintenance\.asset\.retired_on`\s+is\s+one",  # the device family
    r"\*\*Not\s+`marketing\.campaign`\*\*",                                      # commercial campaigns
    r"Partner\s+cases\s+stay\s+apart\s+from\s+`marketing\.case`",
    r"\*\*Same\s+shape\s+as\s+`marketing\.case\.resolution_note`\*\*",           # the dunning family
    r"Marketing\s+turns\s+it\s+into\s+the\s+reminder\s+\(a\s+`MessageTrigger`\s+on\s+the\s+event",
    r"the\s+same\s+gap\s+as\s+`MessageTrigger`,\s+seen\s+from\s+the\s+operational\s+side",
    r"a\s+guest\s+meets\s+them\s+through\s+`orders\.Cart\.consentQuestions`,\s+never\s+by\s+listing",
    r"A\s+waitlist\s+entry\s+never\s+holds\s+a\s+deposit,\s+even\s+where\s+the\s+venue's\s+`DepositPolicy\.dining`\s+is\s+on",
    r"snapshotted\s+from\s+`orders\.DepositPolicy\.dining`\s+when\s+it\s+was\s+made",   # TableReservation.deposit
    r"parties\s+take\s+a\s+deposit\s+\(see\s+`DepositPolicy`\)",
    r"so\s+the\s+orders\s+`FraudRule`\s+refund\s+rules",                         # createRetailReturn: Orders evaluates
    r"Distinct\s+from\s+a\s+provider's\s+processing\s+cost\s+\(`payments\.fee_rule`\)\s+and\s+from\s+a\s+fee\s+as\s+"
    r"charged\s+on\s+an\s+order\s+\(`orders\.order_fee`\)",
    r"the\s+(?:same\s+)?rule-and-record\s+split\s+(?:as\s+)?`(?:fnb\.service_charge_policy|payments\.fee_rule)`\s+and\s+"
    r"`orders\.order_fee`",
    r"never\s+`orders\.order_line`",                                             # transferOrderItems: F&B lines
    r"Same\s+rule\s+as\s+`orders\.payment\.fxRate`\s+under\s+CF-37",             # the wallet authorisation family
    r"without\s+reading\s+Orders'\s+`orders\.pos_shift`",                        # endOwnSession, the session family
    r"A\s+refund\s+it\s+produces\s+is\s+an\s+`orders\.refund`",
    r"The\s+shape\s+is\s+`orders\.RefundPolicy\.requiresApprovalAbove`",         # setRentalFeePolicy
    r"locked\s+on\s+the\s+order\s+\(`orders\.Order\.chargeFxRate`\)",            # listFxRates
    r"Distinct\s+from\s+`payments\.currency_rule`",                              # setCurrencyRoundingRule
    r"the\s+IP\s+address\s+and\s+user\s+agent\s+stay\s+in\s+`pii\.consent_identifier`\s+and\s+are\s+not\s+joined\s+here",
    r"`recordDeviceConsent`\s+writes\s+the\s+IP\s+address\s+and\s+user\s+agent\s+to\s+`pii\.consent_identifier`",
    r"never\s+`pii\.subject\.display_name`",                                     # the loyalty family
    r"written\s+to\s+the\s+erasable\s+store\s+\(`pii\.subject`\)",               # addIncidentPerson: a write
    r"go\s+to\s+the\s+erasable\s+store\s+\(`pii\.subject`",                      # reportIncident
    r"erasure\s+is\s+the\s+ADR-0047\s+tombstone\s+\(`pii\.subject\.is_erased`\)",
    r"Nothing\s+here\s+reads\s+`pii\.subject`",                                  # setLeaderboardNickname
    r"as\s+the\s+DDL\s+names\s+it\W+`pii\.subject_contact\.email`",              # the AI policy family: an example
    r"e\.g\.\s+`pii\.subject_contact`",                                          # setDataDiscoveryAccess: an example
    r"`platform\.device`\s+is\s+staff\s+hardware\s+bound\s+to\s+a\s+workstation",   # listGuestDevices
    r"which\s+records\s+its\s+kind,\s+hardware\s+type.{0,80}?in\s+`platform\.device`",   # placeAccessDevice
    r"a\s+model\s+that\s+devices\s+name\s+\(`platform\.device\.hardwareModelId`",
    r"is\s+changed\s+in\s+the\s+register,\s+tenancy\s+`platform\.device`,\s+not\s+here",
    r"published\s+through\s+`platform\.outbox`",                                 # createWebhookSubscription
    r"which\s+the\s+tenant's\s+region\s+may\s+restrict\s+\(`tenancy\.RegionSettings\.allowedAiResidencies`\)",
    r"a\s+region\s+restricts\s+the\s+choice\s+through\s+`tenancy\.RegionSettings\.allowedAiResidencies`\s+and\s+nothing\s+else",
    r"read\s+from\s+`platform\.sale_board`\s+when\s+the\s+bundle\s+is\s+snapshotted",   # getLatestBundle
    # set once by the writer (openShift, holdOrder, buildProductionPlan, which declare their own read), returned by
    # every operation that answers the row:
    r"\*\*The\s+business\s+day\s+the\s+shift\s+belongs\s+to\*\*.{0,120}?`businessDayCutoff`\s+\(tenancy\s+`VenueSettings`",
    r"or\s+the\s+venue's\s+next\s+business-day\s+cut-off\s+\(`VenueSettings\.businessDayCutoff`\)\s+when\s+the\s+cashier\s+"
    r"sent\s+none",
    r"The\s+trading\s+day\s+this\s+prep\s+list\s+is\s+for,\s+in\s+the\s+Region's\s+time\s+zone;\s+a\s+business\s+date,\s+"
    r"closing\s+at\s+the\s+venue's\s+`businessDayCutoff`\s+\(tenancy\s+`VenueSettings`",
    r"Where\s+`VenueSettings\.alerting\.escalateAfterMinutes`\s+passed\s+with\s+no\s+acknowledgement",   # the alert family
    r"The\s+trading\s+day\s+closes\s+at\s+the\s+venue's\s+`businessDayCutoff`\s+\(tenancy\s+`VenueSettings`",
    r"The\s+variance\s+threshold\s+and\s+the\s+drawer\s+limit\s+stay\s+where\s+they\s+are\s+\(`tenancy\.VenueSettings\."
    r"shiftVarianceThreshold`",                                                  # setTillShiftPolicy
    r"`endOfBusinessDay`\s+runs\s+when\s+the\s+venue's\s+business\s+day\s+closes",   # setWalletReconciliationSources
    r"\*\*Not\s+`queue\.joinQueue`\.\*\*\s+That\s+is\s+the\s+ride\s+queue\s+\(Q1\)\s+and\s+writes\s+`queue\.entry`",
    r"`rentalAgreement`\s+is\s+the\s+existing\s+use\s+from\s+`rental\.agreement_item`",   # the stock-reservation family
    r"`rental\.agreement_item`\s+points\s+here",
    r"`rental\.fee_policy`\s+is\s+the\s+shape\s+being\s+followed\s+here",        # getFnbServiceChargePolicy
    r"an\s+`AlertRule`\s+on\s+metric\s+`staffingShortfall`",                     # getStaffingCoverage: reporting raises it
    r"\(reporting\s+`AlertRule\.deliverTo:\s+push`\)",                           # registerDevice
    r"the\s+hold\s+is\s+converted\s+to\s+a\s+`ResourceBooking`",                 # checkoutCart: a call to resources
    r"calls\s+`resources`\s+to\s+write\s+a\s+`ResourceBooking`",                 # createOrder
    r"which\s+raises\s+the\s+cross-cell\s+sync\.dsar_request",                   # deleteGuestAccount, exportSubjectData
    r"The\s+case\s+layer\s+over\s+the\s+cross-region\s+`sync\.dsar_request`\s+fan-out",   # setPrivacyRequest
    r"`sync\.rejection`\s+exists\s+because",                                     # the burst-environment family
    r"the\s+encoding\s+that\s+`venue-map`\s+uses\s+for\s+`VenuePath\.geometry`",  # proposeWalkways
    r"guarded\s+update\s+on\s+`wallet\.balance`\s+under\s+its\s+row\s+lock",     # authoriseWalletSpend: wallet's call
    r"Schema-qualified,\s+e\.g\.\s+`whitelabel\.content_page`",                  # setIndexSource: an example
    r"while\s+white-label's\s+`CustomDomain`\s+is\s+`pendingRevalidation`",      # resolveTenantHost: pushed by white-label
    r"`whitelabel\.custom_domain`\s+stays\s+the\s+tenant's\s+own\s+record",      # setTenantDomainMapping
    r"They\s+are\s+\*\*not\*\*\s+the\s+white-label\s+app\s+features\s+of\s+`white-label\.ModuleEnablement\.moduleKey`",
    r"the\s+vocabulary\s+of\s+`white-label\.ModuleEnablement\.moduleKey`",       # setModuleListing
    r"it\s+resolved\s+to\s+`whitelabel\.policy`",                                # getPaymentRules: a dropped column
    r"`RotaAssignment`\s+carried\s+`requiredRoleId`\s+alone",                    # setResourceQualifications
    # second mentions in the same operations, found by the dry run's second pass
    r"\*\*An\s+exchange\s+rate:\s+a\s+decimal\s+string,\s+never\s+a\s+float\*\*",   # every rate field
    r"was\s+on\s+the\s+access-control\s+device\s+row,\s+now\s+`access\.device_placement`",   # the device family
    r"\*\*`AccessDynamicPolicy`\s+governs\s+who\s+may\s+pass\s+which\s+gate\*\*",       # the Identity policy family
    r"Identity's\s+staff-permission\s+engine\s+was\s+renamed\s+`AuthorisationPolicy`",   # the access policy family
    r"is\s+`platform\.device`,\s+the\s+only\s+device\s+register",                  # placeAccessDevice, update...
    r"Distinct\s+from\s+`payments\.fee_rule`\s+\(a\s+provider's\s+processing\s+cost\)\s+and\s+`orders\.order_fee`",
    r"hostname\s+taken\s+by\s+another\s+tenant",                                # verifyCustomDomain
    r"raises\s+an\s+`Alert`\s+to\s+the\s+dashboard\s+panel",                     # getStaffingCoverage
    r"a\s+cross-cell\s+sync\.dsar_request\s+raised\s+by\s+`createDsarRequest`",    # exportSubjectData
    r"The\s+model\s+choice\s+per\s+class\s+is\s+the\s+AI\s+engine's\s+\(ai\s+`AiProvider`",   # updateRegionSettings
    r"as\s+the\s+subscription\s+contract's\s+`PartnerDocument`\s+names\s+it",
    r"(?:A\s+hostname\s+already|The\s+hostname\s+is\s+already)\s+routed\s+to\s+another\s+tenant",   # verifyCustomDomain
))
# **The same words, a read for one operation and not for another** (CHG-R10GEN-001): removed only from the text of the
# operations named. A metric-source table describes where each metric comes from; the operation that computes the
# metrics reads those tables (getKpiValues, askReportingQuestion, runSemanticQuery), and one that defines, lists,
# targets or acknowledges them does not.
NOT_READ_FOR: tuple = tuple((re.compile(p, re.I | re.S), frozenset(o)) for p, o in (
    (r"\|\s*Metric\s*\|\s*Source\s*\|.*",
     {"acknowledgeAlert", "listAlerts", "setAlertRule", "setKpiTargets"}),
    (r"\|\s*Code\s*\|\s*Unit\s*\|\s*Source\s*\|.*", {"createKpi", "listSeededReports", "listKpis"}),
    # the two policy engines (ADR-0068) name each other to say which governs what; neither reads the other's rows
    (r"`AccessDynamicPolicy`|`access\.dynamic_policy`",
     {"createAuthorisationPolicy", "updateAuthorisationPolicy", "restoreAuthorisationPolicyVersion",
      "setAuthorisationPolicyState", "simulateAuthorisationPolicy", "evaluateAccess", "listAuthorisationPolicies",
      "getAuthorisationPolicy", "getAuthorisationPolicyBundle", "listAuthorisationPolicyHistory",
      "listAuthorisationPolicyTemplates", "listAuthorisationPolicyEffectiveness", "listPermissionFindings"}),
    (r"`AuthorisationPolicy`|`identity\.authorisation_policy`",
     {"listDynamicPolicyEffectiveness", "setContextTimeEvent", "setVisualDynamicPolicy", "validateAccess"}),
    (r"\*\*Three\s+accreditation\s+sources\s+added\s+29\s+September\*\*.*",
     {"createReport", "updateReport", "listReportFields", "saveNaturalLanguageQuery", "listSeededReports"}),
    # a campaign names its segment's portfolio rule; the segment's evaluation (previewSegmentDraft) reads delegations
    (r"`portfolioScope`\s+aggregates\s+across\s+a\s+`DelegatedAccess`\s+delegation",
     {"createCampaign", "pauseCampaign", "stopCampaign", "unscheduleCampaign", "updateCampaign", "createSegment"}),
    # the venue settings say which other modules' rows each setting governs; Tenancy reads none of them
    (r"each\s+one\s+its\s+region\s+holds\s+an\s+`FxRate`\s+for", {"getVenueSettings", "getVenueSettingsDefaults"}),
    (r"A\s+code\s+the\s+region\s+has\s+no\s+rate\s+for\s+is\s+refused", {"getVenueSettings", "getVenueSettingsDefaults"}),
    (r"each\s+code\s+must\s+also\s+be\s+one\s+the\s+venue's\s+payment\s+provider\s+can\s+charge\s+"
     r"\(`orders\.PaymentProvider\.presentmentCurrencies`\)", {"getVenueSettings", "getVenueSettingsDefaults"}),
    (r"the\s+same-business-day\s+void\s+\(orders\s+`AfterSalePolicy\.voidSameBusinessDayOnly`\)",
     {"getVenueSettings", "getVenueSettingsDefaults", "setVenueSettings", "setVenueSettingsDefaults"}),
    (r"\(`Cart\.maxExtensions`\)",
     {"getVenueSettings", "getVenueSettingsDefaults", "setVenueSettings", "setVenueSettingsDefaults"}),
    (r"BO-042\s+flags\s+the\s+box\s+\(`shift\.DepositBox\.overDrawerLimit`\)",
     {"getVenueSettings", "getVenueSettingsDefaults", "setVenueSettings", "setVenueSettingsDefaults"}),
    (r"a\s+shift's\s+business\s+date\s+and\s+its\s+close\s+\(shift\s+`Shift\.businessDate`",
     {"getVenueSettings", "getVenueSettingsDefaults", "setVenueSettings", "setVenueSettingsDefaults"}),
    # FxRate.chargeable answers for the venue a listFxRates caller names; a rate written has no venue
    (r"With\s+`venueId`,\s+true\s+where\s+a\s+guest\s+may\s+select\s+this\s+currency", {"ingestFxRates", "setFxRate"}),
    # a dispatch's attribution window belongs to the campaign's performance figures, not to sending one message
    (r"The\s+window\s+these\s+figures\s+were\s+attributed\s+over,\s+from\s+`VenueSettings\.marketing\."
     r"attributionWindowDays`", {"retryMessageDispatch", "sendTransactionalMessage", "testSendCampaign"}),
))


def strip_not_read(op: str, text: str) -> str:
    """The text without the NOT_READ_FOR sentences scoped to `op` (a chunk at a time: a table runs to its chunk's end)."""
    for rx, ops in NOT_READ_FOR:
        if op in ops:
            text = rx.sub(" ", text)
    return text
TABLE_IN_TEXT = re.compile(r"(?<![\w.])([a-z][a-z0-9_]*)\.([a-z][a-z0-9_]+)\b")
FIELD_IN_TEXT = re.compile(r"(?<![\w.])(?:([a-z][a-z-]+)\.)?([A-Z][A-Za-z0-9]+)\.([a-z][A-Za-z0-9]+)\b")
SCHEMA_IN_TEXT = re.compile(r"`([A-Z][A-Za-z0-9]+)`")
ID_LIKE = re.compile(r"(?:^id$|Ids?$|Ref$)")
# **The facts the CRs named, which may never be baselined** (XR-FACT): (operation, table).
MUST_FIX_FACTS = {
    ("createPerformances", "platform.region_settings"),
    ("setVenueSettings", "ledger.fx_rate"),
    ("setVenueSettings", "payments.provider"),
    ("createShopAndDrop", "fnb.delivery_location"),
    ("lookupMerchandise", "promotions.promotion"),
    ("setBrandIdentity", "control.licence_add_on"),
    ("setBrandIdentity", "assets.media_asset"),
    ("setAnalyticsProvider", "platform.scope"),
    ("setMaintenanceMode", "platform.scope"),
    ("createPreview", "orders.ticket_template"),
    ("claimCustomDomain", "control.tenant_domain"),
    ("getPlatformSubdomain", "control.cell"),
    ("allocateDepositBox", "platform.denomination"),
    ("allocateDepositBox", "platform.venue_settings"),
}


def query_tables(q: dict) -> set:
    """The tables a declared query answers over: its `table`, its projection's `source` (`a.b + c.d`), its `reads`."""
    out = set()
    if q.get("table"):
        out.add(str(q["table"]).strip())
    pr = q.get("projection") if isinstance(q.get("projection"), dict) else {}
    if pr.get("source"):
        out |= {s.strip() for s in str(pr["source"]).split("+") if s.strip()}
    out |= {str(t).strip() for t in q.get("reads") or []}
    return out


def covered_by(via: list, queries: dict) -> tuple:
    """(tables asked over, owners asked a rule query that names no table) for an operation's readVia. `queries` maps
    `<contract>#<name>` to (owning service, the query's tables)."""
    tables, owners = set(), set()
    for r in via or []:
        owner, tabs = queries.get(str((r or {}).get("query") or ""), (None, set()))
        if tabs:
            tables |= tabs
        elif owner:
            owners.add(owner)
    return tables, owners


def is_covered(table: str, owner, tables: set, owners: set) -> bool:
    """Covered by a query over that table, or by a rule query of its owner that names no table."""
    return table in tables or owner in owners


def persisted(by: dict, tables: set) -> dict:
    """(contract, schema) -> the first table its x-ticvai-persistence names, where the schema reference has it."""
    out = {}
    for key, s in by.items():
        m = re.match(r'\s*"?([a-z][a-z0-9_]*\.[a-z][a-z0-9_]+)', str((s or {}).get("x-ticvai-persistence") or ""))
        if m and m.group(1) in tables:
            out[key] = m.group(1)
    return out


def op_text(stem: str, op: dict, item: dict, by: dict) -> str:
    """Everything an operation says in words: summary, description, parameters, request and response descriptions,
    the descriptions and x-ticvai-persistence of its own contract's schemas they use (`$ref` followed, every level),
    and of an own schema named in backticks (`ConflictAnalysis`), one hop. A field that only holds a key (`id`,
    `...Id`, `...Ids`, `...Ref`, a uuid) is skipped: naming the record it points at is not reading it."""
    return "\n".join(op_chunks(stem, op, item, by))


# **A read answers from its rows; the rules in its response schema are kept by the writer** (fix round 1 of
# CHG-RTE-001, 18 October 2026, made the check's rule by CHG-R10GEN-001, 25 October). A GET names a fact by its own
# words (summary, description, parameters) or by its response schema. A phrase that sits only in the response
# schema is a rule the writing operation keeps (`businessDate` is set from the venue's cut-off when the shift opens;
# getShift returns it), unless the schema says the value is worked out when it is read: a field computed on read
# (listDepositBoxes' overDrawerLimit against the drawer limits, ADAM CR-218, whose finding round 1 left unswept), a
# value resolved from another table when the record is read (a case's guest name from `pii.subject`), or a response
# that is a projection or an aggregate over the tables it lists (`none — projection over ...`).
READ_ON_READ = re.compile(
    r"\b(?:computed|worked out|resolved|derived|calculated|evaluated) (?:on|at) read\b"
    r"|\bon read\b|\bat read time\b|\bwhen (?:the [\w ]{1,30} )?is read\b|\bwhen it is read\b"
    r"|\bresolved from\b|\bread from `?[a-z][a-z-]*\.[A-Z]"
    r"|^none\s*\W+\s*(?:projection|aggregated?|computed|derived|joined|read)\b"
    r"|\bprojection over\b|\baggregated from\b"
    r"|\bas `[a-z][a-z-]*\.[A-Z]\w*\.\w+`|\bthe server turns\b",
    re.I | re.M)


def get_counts(method: str, table: str, own: dict, response_chunks: list, named) -> bool:
    """Whether a fact `table` an operation's text names is a read of it (fix round 1 as the check's rule): every
    fact of a write; a read's (GET's) fact when its own words name it (`own`: facts_named of the text without its
    responses), or when a response chunk that names it says it is worked out on read (READ_ON_READ). `named(chunk)`
    gives the tables a chunk names."""
    if str(method).lower() != "get" or table in own:
        return True
    return any(READ_ON_READ.search(c) and table in named(c) for c in response_chunks)


def op_chunks(stem: str, op: dict, item: dict, by: dict) -> list:
    """op_text's pieces, one per description, summary or persistence string, in the order op_text reads them."""
    out, seen = [], set()

    def walk(node, depth=0, name=""):
        if depth > 8 or (name and ID_LIKE.search(name)):
            return
        if isinstance(node, dict):
            if node.get("format") == "uuid":
                return
            for k, v in node.items():
                k = str(k)
                if k in ("description", "summary") and isinstance(v, str):
                    out.append(v)
                elif k == "x-ticvai-persistence" and isinstance(v, str):
                    out.append(v)
                elif k == "$ref" and isinstance(v, str):
                    n = v.rsplit("/", 1)[-1]
                    if v.startswith("#") and (stem, n) in by and (stem, n) not in seen:
                        seen.add((stem, n))
                        walk(by[(stem, n)], depth + 1)
                elif k == "properties" and isinstance(v, dict):
                    for pn, pv in v.items():
                        walk(pv, depth + 1, str(pn))
                elif k.startswith("x-ticvai-") or k == "429":
                    continue
                else:
                    walk(v, depth)
        elif isinstance(node, list):
            for x in node:
                walk(x, depth)

    walk({"op": op, "parameters": (item or {}).get("parameters")})
    for n in sorted({m.group(1) for t in list(out) for m in SCHEMA_IN_TEXT.finditer(t)}):
        if (stem, n) in by and (stem, n) not in seen:
            seen.add((stem, n))
            walk(by[(stem, n)], 1)
    return out


def facts_named(text: str, reader: str, owner_of_schema: dict, tables: set, persist: dict = None,
                names: dict = None, svc_of_contract: dict = None) -> dict:
    """table -> [(how, phrase)]: every table of a module other than `reader` the text names, by its name (`table`),
    by a field or a backticked name of a schema another module's contract persists to it (`field`, `schema`), or by
    a phrase of FACTS (`fact`). The kernel tables every role reads are not facts by name."""
    for rx in NOT_READ:
        text = rx.sub(" ", text)
    out: dict = {}

    def note(t, how, phrase):
        own = owner_of_schema.get(t.split(".", 1)[0])
        if own and own != reader and t in tables:
            out.setdefault(t, []).append((how, phrase))

    for m in TABLE_IN_TEXT.finditer(text):
        t = f"{m.group(1)}.{m.group(2)}"
        if t not in KERNEL_READ:
            note(t, "table", m.group(0))
    if persist is not None and names is not None and svc_of_contract is not None:
        def schema_table(contract, schema):
            for stem in names.get(schema) or []:
                if contract and stem != contract:
                    continue
                if svc_of_contract.get(stem) == reader:
                    return None
                return persist.get((stem, schema))
            return None

        for m in FIELD_IN_TEXT.finditer(text):
            c, sch, fld = m.groups()
            if not ID_LIKE.search(fld):
                t = schema_table(c, sch)
                if t:
                    note(t, "field", m.group(0))
        for m in SCHEMA_IN_TEXT.finditer(text):
            t = schema_table(None, m.group(1))
            if t:
                note(t, "schema", m.group(0))
    for rx, t in FACT_RES:
        m = rx.search(text)
        if m:
            note(t, "fact", m.group(0))
    return out


def fact_findings(ignore=None) -> list:
    """[(operation, reader, table, owner, how, phrase)] for every fact an operation's text names that no query it
    asks covers, the operation's own lineage reads and writes left to the rules that judge them. Shared by main(),
    `--list-facts` and tools/applied/read-routes-18-october.py. `ignore(route) -> bool` leaves routes out of the
    coverage (the sweep ignores the routes it wrote itself, so a second run sees what justifies each)."""
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    services = (g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    tables = set((g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
    by, names = g.schemas()
    persist = persisted(by, tables)
    qtables = {k: (svc_of_contract.get(stem), query_tables(q)) for k, (stem, q) in declared_queries().items()}
    out = []
    for o, f in sorted(g.operations().items()):
        e = lin.get(o) or {}
        reader = e.get("service") or svc_of_contract.get(f["contract"])
        if reader not in services:
            continue
        # The contract's own routes as well as the lineage's, so the class query sees a route as soon as it is
        # written, before derive-lineage copies it (XR-LINEAGE keeps the two equal).
        via = [r for r in (f["op"].get("x-ticvai-read-via") or []) if isinstance(r, dict)] + (e.get("readVia") or [])
        if ignore:
            via = [r for r in via if not ignore(r)]
        cov_t, cov_o = covered_by(via, qtables)
        skip = set(e.get("reads") or []) | set(e.get("writes") or [])
        skip |= {str(w.get("table")) for w in e.get("writeVia") or [] if isinstance(w, dict)}
        skip |= {t.rsplit("_for_", 1)[0] for t in e.get("reads") or [] if "_for_" in t}
        def chunks(op, item, _o=o, _c=f["contract"]):
            return [strip_not_read(_o, c) for c in op_chunks(_c, op, item, by)]

        def named(chunk, _reader=reader):
            return facts_named(chunk, _reader, owner_of_schema, tables, persist, names, svc_of_contract)

        text = "\n".join(chunks(f["op"], f["item"]))
        own = resp = None
        for t, hits in sorted(named(text).items()):
            owner = owner_of_schema.get(t.split(".", 1)[0])
            if t in skip or is_covered(t, owner, cov_t, cov_o):
                continue
            if str(f["method"]).lower() == "get":
                if own is None:
                    own = named("\n".join(chunks({k: v for k, v in f["op"].items() if k != "responses"}, f["item"])))
                    resp = chunks({"responses": f["op"].get("responses")}, None)
                if not get_counts(f["method"], t, own, resp, named):
                    continue
            how, phrase = hits[0]
            out.append((o, reader, t, owner, how, phrase))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-cross-module-reads", RULES)
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    dec = g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}
    services = dec.get("services") or {}
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    tier_of = {s: v.get("tier") for s, v in services.items()}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    names_of = {s: {slug(s), *(v.get("contracts") or []), *(v.get("schemas") or [])} for s, v in services.items()}

    def module(name: str) -> str | None:
        """A query's `module`: a service name (`OrderService`), or one of its contracts or schemas."""
        n = str(name or "")
        if n in services:
            return n
        for s, ns in names_of.items():
            if n.lower() in {x.lower() for x in ns} or n.lower() == slug(s):
                return s
        return None

    queries = declared_queries()
    granted = granted_reads()
    ops = contract_ops()
    if "--list-facts" in sys.argv[1:]:
        for row in fact_findings():
            print("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in row))
        return 0
    qtables = {k: (svc_of_contract.get(stem), query_tables(q)) for k, (stem, q) in queries.items()}
    # XR-QUERY on the declarations themselves
    for key, (stem, q) in sorted(queries.items()):
        miss = [f for f in QUERY_FIELDS if not q.get(f)]
        if miss:
            guard.add("XR-QUERY", key, f"{key} declares no {', '.join(miss)}")
        mod = module(q.get("module"))
        if mod is None or mod != svc_of_contract.get(stem):
            guard.add("XR-QUERY", f"{key}:module", f"{key}: module {q.get('module')!r} is not "
                      f"{svc_of_contract.get(stem)}, which owns contracts/{stem}")
        bad = [r for r in (q.get("served") or []) if r not in ROUTES]
        if bad:
            guard.add("XR-QUERY", f"{key}:served", f"{key}: served {bad} is not one of {', '.join(ROUTES)}")

    n_cross = 0
    for o, e in sorted(lin.items()):
        reader = e.get("service")
        if reader not in services:
            continue
        rdep = dep_of.get(reader)
        via = e.get("readVia") or []
        for r in via:
            key = str(r.get("query") or "")
            route = str(r.get("route") or "")
            if key not in queries:
                guard.add("XR-QUERY", f"{o}:{key}", f"{o} reads via {key!r}, which no contract declares in "
                          "x-ticvai-queries")
                continue
            stem, q = queries[key]
            owner = svc_of_contract.get(stem)
            if route not in ROUTES:
                guard.add("XR-ROUTE", f"{o}:{key}", f"{o} asks {key} by {route!r}; a route is one of {', '.join(ROUTES)}")
            elif route not in (q.get("served") or []):
                guard.add("XR-ROUTE", f"{o}:{key}", f"{o} asks {key} by {route}, which the query does not serve "
                          f"({', '.join(q.get('served') or []) or 'none'})")
            if route == "in-process" and owner and dep_of.get(owner) != rdep and (rdep, key) not in granted:
                guard.add("XR-ROUTE", f"{o}:{key}", f"{o} ({rdep}) asks {key} in-process, and {owner} is in "
                          f"{dep_of.get(owner)}: across deployables a query is a service call or a projection")
            if reader in FOUNDATION_STRICT and owner and tier_of.get(owner) != "foundation" and route != "projection":
                guard.add("XR-FOUNDATION", f"{o}:{key}", f"{o} ({reader}, foundation) asks {key} of {owner} "
                          f"({tier_of.get(owner)}) by {route}: Identity reads nothing above it but a projection")
        cov_t, cov_o = covered_by(via, qtables)
        for t in e.get("reads") or []:
            if ":" in t or "." not in t or t in KERNEL_READ:
                continue
            schema, short = t.split(".", 1)
            owner = owner_of_schema.get(schema)
            if not owner or owner == reader:
                continue
            n_cross += 1
            strict = owner in MUST_FIX.get(o, set())
            m = re.match(r"^(.+)_for_([a-z0-9_]+)$", short)
            if m and m.group(2) in {x.replace("-", "_") for x in names_of.get(reader, set())}:
                if dep_of.get(owner) != rdep:
                    guard.add("XR-VIEW-ACROSS", f"{o}:{t}", f"{o} ({rdep}) reads the view {t} of {owner} "
                              f"({dep_of.get(owner)}): across deployables use the owner's service or a projection",
                              strict=strict)
                # **A view named for Identity is still a read above it** (20 October 2026, r8 cause FOUNDATION-AI-C48,
                # CHG-R8GEN-005). This branch skipped the tier rule, so an `orders.sales_order_for_identity` view
                # would have passed although ADR-0028 lets Identity read nothing above it but a projection.
                if reader in FOUNDATION_STRICT and tier_of.get(owner) != "foundation":
                    guard.add("XR-FOUNDATION", f"{o}:{t}", f"{o} ({reader}, foundation) reads the view {t} of {owner} "
                              f"({tier_of.get(owner)}): Identity reads nothing above it but a projection, and a view "
                              "is not one", strict=strict)
                continue
            if is_covered(t, owner, cov_t, cov_o):
                continue
            guard.add("XR-UNCOVERED", f"{o}:{t}", f"{o} ({reader}, {rdep}) reads {t}, which {owner} "
                      f"({dep_of.get(owner)}) owns, raw: ask a declared query (x-ticvai-read-via) or, within one "
                      f"deployable and for bulk data, read {schema}.{short}_for_{slug(reader)}", strict=strict)
            if reader in FOUNDATION_STRICT and tier_of.get(owner) != "foundation":
                guard.add("XR-FOUNDATION", f"{o}:{t}", f"{o} ({reader}, foundation) reads {t} of {owner} "
                          f"({tier_of.get(owner)}): Identity reads nothing above it but a projection", strict=strict)
    # XR-FACT (CHG-RTE-001): what the text names, beyond the lineage
    facts = fact_findings()
    for o, reader, t, owner, how, phrase in facts:
        guard.add("XR-FACT", f"{o}:{t}",
                  f"{o} ({reader}) names {t} ({how}: {phrase!r}), which {owner} owns, and asks no query over it: add "
                  f"an x-ticvai-read-via to {owner}'s query for {t} (ADR-0055 rule 2; CR-096)",
                  strict=(o, t) in MUST_FIX_FACTS)
    # XR-LINEAGE
    for o in sorted(set(ops) | {o for o, e in lin.items() if e.get("readVia")}):
        want = sorted(({k: str(r[k]) for k in ("query", "route", "for") if r.get(k)}
                       for r in (ops.get(o) or {}).get("x-ticvai-read-via") or [] if isinstance(r, dict)
                       and r.get("query")), key=lambda r: (r["query"], r.get("for", "")))
        if o in lin and (lin[o].get("readVia") or []) != want:
            guard.add("XR-LINEAGE", o, f"{o}: the lineage's readVia differs from the contract's x-ticvai-read-via "
                      "(python tools/derive-lineage.py --apply)")
    guard.note(f"{n_cross} cross-module table read(s) in the lineage; {len(facts)} fact(s) named in text and not "
               f"asked; {len(queries)} declared quer(ies)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
