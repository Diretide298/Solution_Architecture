#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The last 33 tables nothing could reach, across nine contracts.

Written as a generator rather than 33 blocks of YAML, because the shapes repeat and a
hand-copied operation is where a wrong permission or a missing page cursor gets in. **What does
not repeat is the reasoning**, so every operation carries its own.

## The cross-cell criterion, applied

Three of these tables are the cell machinery itself and they are the only ones where the
criterion changes a design:

    sync.cross_cell_request     **the record of a call that had to leave a cell.** Listing it is
                                how anyone finds out the topology is wrong — a pair of cells
                                exchanging thousands of these is a tenant in the wrong home
    sync.cell_connection        which cells may talk to which, and when the link was valid
    platform.cell_endpoint      where a service answers inside a cell

Everything else is configuration or a per-venue record, and **configuration is read from a
replica inside the cell**. `x-ticvai-read-routing: replica` is on every list here that a hot
path touches: a dynamic price evaluated at a till, a payment eligibility rule at checkout, a
deposit policy at a rental desk. **None of them should ever cross a cell boundary**, and the
routing hint is what says so.

`wallet.balance` is the one to watch: a shared wallet spans venues, and a venue in another cell
reading a balance is a cross-cell call on a payment path. It is listed by wallet, not by guest,
so the common read stays inside the cell that owns the wallet.

## Two decisions rather than wiring

**`orders.deposit` and `ledger.deposit` are not duplicates and the convention matcher could not
tell.** `audit-duplicate-tables` paired them on the name and `derive-relationships` refused
`payments.deposit_activity.deposit_id` as ambiguous — correctly, because both exist. They are
the two sides:

    orders.deposit      the authorisation lifecycle — required, authorized, captured, released,
                        forfeited. **What the card company knows**
    ledger.deposit      the liability posting — `liability_account_id`, `refundable_until`.
                        **What the accounts know**

`deposit_activity` records movements on the first, so the reference is declared here rather than
guessed.

**`pricing.dynamic_price_condition.rule_id` and `dynamic_price_action.rule_id` are renamed** to
`dynamic_price_rule_id`. They resolved to `approvals.rule`, which is the only table in the
package short-named `rule`, and `pricing` has none — so the same-schema preference cannot save
them and the name has to say what it means.

    python3 tools/applied/wire-remaining-tables-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")


def C(rel):
    return os.path.join(ROOT, "contracts", rel)


# (contract, path, verb, operationId, tag, permission, scope, summary, description, kind, schema)
# kind: list | page | get | set | setList | post
OPS = [
    # ---- pricing, in catalogue.yaml. Decision 5 said "give the schema an owner"; declaring the
    #      operations here does exactly that — the lineage takes its service from the contract.
    ("spine/catalogue.yaml", "/pricing/dynamic-rules", "get", "listDynamicPriceRules",
     "catalogue", "PRICE_VIEW", "venue",
     "Dynamic pricing rules",
     "Decision 5 of the schema merge took all three `pricing` tables and said the schema needed "
     "an owner. **It had none because it had no operations** — a service is inferred from the "
     "contract that declares them, and nothing declared any. They live here because a price "
     "belongs to the catalogue.\n\n**Read from a replica inside the cell.** A dynamic price is "
     "evaluated at a till; a rule fetched across a cell boundary at the moment of sale is a "
     "queue.",
     "list", "PricingDynamicPriceRule"),
    ("spine/catalogue.yaml", "/pricing/dynamic-rules/{ruleId}", "get", "getDynamicPriceRule",
     "catalogue", "PRICE_VIEW", "venue",
     "One rule with its conditions and actions",
     "**A rule is unreadable without both halves.** The conditions say when it fires and the "
     "actions say what it does to the price, and a screen showing one without the other cannot "
     "tell a reviewer whether the rule is safe. `minPrice` and `maxPrice` on the action are the "
     "guard rails, and they are the first thing anyone looks for.",
     "get", "DynamicPriceRuleDetail"),
    ("spine/catalogue.yaml", "/pricing/dynamic-rules/{ruleId}", "put", "setDynamicPriceRule",
     "catalogue", "PRICE_CONFIGURE", "venue",
     "Replace a rule, its conditions and its actions",
     "**Applied whole.** A rule whose conditions have been updated and whose actions have not is "
     "a rule that fires on the new trigger with the old discount, and for a live price that is a "
     "loss taken silently.",
     "set", "DynamicPriceRuleDetail"),

    # ---- payments
    ("satellite/payments.yaml", "/payments/rules", "get", "getPaymentRules",
     "payments", "PAYMENT_VIEW", "venue",
     "Currency, eligibility and fee rules as one set",
     "**Three tables, one decision.** Whether a guest may pay with this method, in this currency, "
     "and what it costs the venue are evaluated together at checkout, and an administrator "
     "changing one without seeing the others is how a method becomes eligible in a currency it "
     "cannot settle.\n\n**`payment_policy_id` was dropped from all three**: no such table exists "
     "and it resolved to `whitelabel.policy` — a payment rule pointing at a website's terms page. "
     "They are scoped by `scopePath`, `channelId` and `businessArea`, which they already carry.",
     "get", "PaymentRuleSet"),
    ("satellite/payments.yaml", "/payments/rules", "put", "setPaymentRules",
     "payments", "PAYMENT_CONFIGURE", "venue",
     "Replace the payment rule set",
     "**Whole, for the reason the read is composed.** An eligibility rule admitting a currency "
     "the currency rule does not settle is only visible when both are in front of you.",
     "set", "PaymentRuleSet"),
    ("satellite/payments.yaml", "/deposits/{depositId}/activity", "get", "listDepositActivity",
     "payments", "PAYMENT_VIEW", "venue",
     "Movements on a deposit",
     "**Authorise, capture, release, forfeit — the history a disputed deposit is settled from.** "
     "`orders.deposit` carries the five running totals and could not say how they got there.\n\n"
     "The deposit referenced is `orders.deposit`, the authorisation lifecycle, **not** "
     "`ledger.deposit`, which is the liability posting. Both exist, both are called deposit, and "
     "the convention matcher correctly refused to guess — so the reference is declared.",
     "list", "PaymentsDepositActivity"),
    ("satellite/payments.yaml", "/deposits/{depositId}/activity", "post", "recordDepositActivity",
     "payments", "PAYMENT_CONFIGURE", "venue",
     "Record a movement on a deposit",
     "**A forfeit needs a reason and an author, which is why this is a row rather than a column "
     "update.** A deposit that went from authorised to forfeited with no record of who decided "
     "is the dispute the venue loses.",
     "post", "PaymentsDepositActivity"),

    # ---- orders
    ("spine/orders.yaml", "/deposits", "get", "listDeposits",
     "orders", "ORDER_VIEW", "venue",
     "Deposits and their authorisation state",
     "**The authorisation lifecycle, not the accounting one.** `required`, `authorized`, "
     "`captured`, `released` and `forfeited` are what the card company knows; `ledger.deposit` "
     "holds the liability posting and its `refundableUntil`. Two tables called deposit, two "
     "different questions.",
     "page", "OrdersDeposit"),
    ("spine/orders.yaml", "/order-discounts", "get", "listOrderDiscounts",
     "orders", "ORDER_VIEW", "venue",
     "Discounts applied to orders",
     "**Distinct from `promotions`, which decides whether a discount applies.** This records that "
     "one did, to this order, for this amount — the row a refund has to reverse and a report has "
     "to total.",
     "page", "OrdersDiscount"),
    ("spine/orders.yaml", "/orders/{orderId}/fees", "get", "listOrderFees",
     "orders", "ORDER_VIEW", "venue",
     "Fees charged on an order",
     "**A booking fee is not a line and not a tax**, and putting it in either makes one of the "
     "two wrong. A guest disputing a total is usually disputing a fee, and until now there was "
     "nowhere to read them.",
     "list", "OrdersOrderFee"),
    ("spine/orders.yaml", "/upgrades", "get", "listUpgrades",
     "orders", "ORDER_VIEW", "venue",
     "Upgrade requests and their outcome",
     "**`quoteUpgrade` priced an upgrade and nothing recorded that one happened.** The quote is "
     "the cheap half; the record is what a guest arriving with an upgraded entitlement is "
     "checked against.",
     "page", "OrdersUpgrade"),

    # ---- marketing
    ("satellite/marketing-crm.yaml", "/guest-extra-fields", "get", "listGuestExtraFields",
     "marketing", "GUEST_VIEW", "venue",
     "Venue-defined guest fields and their options",
     "**A venue that needs one more field about a guest should not need a schema change.** "
     "Dietary requirement, accessibility need, school year group — three venues want three "
     "different ones, and the alternative is a `notes` column nobody can report on.\n\nThe "
     "options come back with the field because a select with no options is not a field.",
     "list", "GuestExtraFieldDefinition"),
    ("satellite/marketing-crm.yaml", "/guest-extra-fields", "put", "setGuestExtraFields",
     "marketing", "MARKETING_MANAGE", "venue",
     "Define the extra guest fields",
     "**Set whole, because removing an option is only safe when the values are in view.** An "
     "option deleted while guests still hold it leaves rows pointing at nothing.",
     "setList", "GuestExtraFieldDefinition"),
    ("satellite/marketing-crm.yaml", "/guests/{guestId}/extra-values", "get",
     "getGuestExtraValues", "marketing", "GUEST_VIEW", "venue",
     "What a guest answered",
     "Separate from the field definitions because **the definitions are venue configuration and "
     "the values are personal data.** `GUEST_VIEW_PII` guards the values on the write side; the "
     "definitions are readable by anyone who can see a guest at all.",
     "list", "MarketingGuestExtraValue"),
    ("satellite/marketing-crm.yaml", "/guests/{guestId}/extra-values", "put",
     "setGuestExtraValues", "marketing", "GUEST_VIEW_PII", "venue",
     "Record a guest's answers",
     "**Whole, so a cleared answer is expressible.** Sending only what changed cannot say that a "
     "guest withdrew a dietary requirement, and a stale allergy is the worst kind of stale.",
     "setList", "MarketingGuestExtraValue"),
    ("satellite/marketing-crm.yaml", "/sla-policies", "get", "listSlaPolicies",
     "marketing", "CASE_VIEW", "venue",
     "Response and resolution targets for cases",
     "**Not `approvals.sla_policy`, which times an approval request.** This times a guest case: "
     "first response, resolution, escalation, and whether the clock runs outside business hours. "
     "Two tables with one name, and the `audit-duplicate-tables` pairing was a false positive "
     "for exactly that reason.",
     "list", "MarketingSlaPolicy"),
    ("satellite/marketing-crm.yaml", "/sla-policies", "put", "setSlaPolicy",
     "marketing", "CASE_MANAGE", "venue",
     "Define an SLA policy",
     "**`businessHoursOnly` is the field that makes the rest meaningful.** Four hours to first "
     "response means something different on a Sunday night, and a policy that cannot say which "
     "breaches every weekend.",
     "set", "MarketingSlaPolicy"),
    ("satellite/marketing-crm.yaml", "/waiver-signatures", "get", "listWaiverSignatures",
     "marketing", "GUEST_VIEW_PII", "venue",
     "Signed waivers",
     "**`getWaiverStatus` answered whether a guest had signed and nothing could produce the "
     "signature.** A waiver whose evidence cannot be retrieved is not a waiver, which is the "
     "entire reason venues collect them.",
     "page", "MarketingWaiverSignature"),

    # ---- fnb
    ("satellite/fnb.yaml", "/recipes/{recipeId}/substitutes", "get", "listIngredientSubstitutes",
     "fnb", "PRODUCT_VIEW", "venue",
     "Approved substitutions for a recipe's ingredients",
     "**A kitchen out of an ingredient substitutes it whether or not the system says so.** "
     "Recording which swaps are approved is how an allergen declaration survives a delivery that "
     "did not arrive.",
     "list", "FnbIngredientSubstitute"),
    ("satellite/fnb.yaml", "/recipes/{recipeId}/substitutes", "put", "setIngredientSubstitutes",
     "fnb", "PRODUCT_CONFIGURE", "venue",
     "Define approved substitutions",
     "Set whole per recipe: a substitution list is reviewed as a list, usually against an "
     "allergen matrix.",
     "setList", "FnbIngredientSubstitute"),
    ("satellite/fnb.yaml", "/product-recommendations", "get", "listFnbRecommendations",
     "fnb", "PRODUCT_VIEW", "venue",
     "Upsell and pairing suggestions for F&B",
     "**Seventeen columns and no way to read them.** Kept whole from the backend workbook when "
     "the ten duplicate catalogue tables were collapsed, because we have nothing like it — "
     "`promotions.getUpsellSuggestions` computes, and this is what a venue configured.",
     "list", "FnbProductRecommendation"),

    # ---- retail
    ("satellite/retail.yaml", "/product-recommendations", "get", "listRetailRecommendations",
     "retail", "PRODUCT_VIEW", "venue",
     "Upsell and pairing suggestions for retail",
     "The retail half of the same table F&B keeps. **Separate because the merchandising is "
     "separate** — a coffee pairs with a pastry and a jacket pairs with a hat, and one list "
     "serving both would be filtered on every read.",
     "list", "RetailProductRecommendation"),

    # ---- rental
    ("satellite/rental.yaml", "/agreements", "get", "listRentalAgreements",
     "rental", "RENTAL_VIEW", "venue",
     "Rental agreements",
     "**We held `agreement_rules` and `agreement_signature` and no agreement.** The signature "
     "referenced a participant and a version *string*, so it signed a version number rather than "
     "a document. Decision 1 took their `rental_agreement` for exactly this.",
     "page", "RentalAgreement"),
    ("satellite/rental.yaml", "/agreements/{agreementId}", "get", "getRentalAgreement",
     "rental", "RENTAL_VIEW", "venue",
     "One agreement with its items",
     "**The items are what was actually handed over**, merged with our `equipment_assignment` "
     "under decision 1. A signed agreement that cannot list its equipment settles no dispute "
     "about a missing helmet.",
     "get", "RentalAgreementDetail"),
    ("satellite/rental.yaml", "/agreements", "post", "createRentalAgreement",
     "rental", "RENTAL_BOOK", "venue",
     "Raise a rental agreement",
     "**Raised before signature, not after.** `rental.agreement_signature` points at an "
     "agreement, so the document has to exist for a participant to sign it — which is the gap "
     "that made the signature reference a version string.",
     "post", "RentalAgreementDetail"),

    # ---- inventory
    ("satellite/inventory.yaml", "/stock-reservations", "get", "listStockReservations",
     "inventory", "PRODUCT_VIEW", "venue",
     "Soft holds on stock",
     "**A reservation is not a batch and not a movement.** `rental.agreement_item` points here: "
     "equipment promised to a booking that has not been collected is neither available nor gone, "
     "and without this it was one or the other.\n\n`expiresAt` is what stops a hold outliving "
     "the booking that made it.",
     "page", "InventoryStockReservation"),

    # ---- access
    ("spine/access.yaml", "/access-changes", "get", "listAccessChanges",
     "access", "GUEST_VIEW", "venue",
     "Changes made to an entitlement's access",
     "**Who changed what a pass could do, and when.** An entitlement that stopped working at a "
     "gate is answered from here or from nowhere.",
     "page", "AccessAccessChange"),
    ("spine/access.yaml", "/admission-rules/{ruleId}/points", "get", "listEntryRulePoints",
     "access", "SCOPE_VIEW", "venue",
     "Which access points an admission rule covers",
     "**This is `access.admission_rules.allowedAccessPointIds` as a table**, and it is the "
     "clearest case in the merge: their normalisation was taken because an array cannot carry "
     "per-row state. A point that is temporarily closed under one rule and open under another "
     "has nowhere to live in an array.",
     "list", "AccessEntryRulePoint"),
    ("spine/access.yaml", "/admission-rules/{ruleId}/points", "put", "setEntryRulePoints",
     "access", "ACCESS_POINT_CONFIGURE", "venue",
     "Set the access points an admission rule covers",
     "Set whole: a rule's coverage is decided as a set, and applying it point by point leaves "
     "gates admitting on a rule that is half-applied.",
     "setList", "AccessEntryRulePoint"),

    # ---- subscription and control
    ("satellite/subscription.yaml", "/plans/{planId}/tiers", "get", "getPlanTiers",
     "subscription", "PLATFORM_PLAN_VIEW_OR_MANAGE", "tenant",
     "What a plan tier allows and includes",
     "**Two tables that only make sense together**: `tier_allowance` is the numbers — how many "
     "venues, how many users, unlimited or not — and `tier_module` is which modules are switched "
     "on. A plan page shows both and a decision about one is made against the other.",
     "get", "PlanTierDetail"),
    ("satellite/subscription.yaml", "/plans/{planId}/tiers", "put", "setPlanTiers",
     "subscription", "PLATFORM_PLAN_MANAGE", "tenant",
     "Set a plan tier's allowances and modules",
     "**Whole.** A tier that gained a module and not the allowance to use it sells something the "
     "enforcement policy will refuse.",
     "set", "PlanTierDetail"),
    # **`listBurstEnvironments` was in this list and has been removed.** `subscription.yaml`
    # already declares it, along with `requestBurstEnvironment`, `drainBurstEnvironment` and
    # `decommissionBurstEnvironment`, and all four already return `BurstEnvironment`.
    #
    # `control.burst_environment` looked unreachable because its hand-mapped lineage entry, dated
    # 31 August, lists `catalogue.performance` and not the table the operation actually returns.
    # **The audit trusts the lineage, so a short lineage entry looks exactly like a missing API.**
    # 82 tables are in that state; they are repaired by `derive-lineage`, not by new operations.
    #
    # Adding it produced a duplicate path key in YAML, where the last wins silently — the parse
    # check passed and four operations disappeared. `check-package` rule 35b catches the
    # duplicate `operationId`; nothing caught the duplicate path, and now something does.

    # ---- the cell machinery, where the cross-cell criterion is the subject rather than a
    #      constraint on the design
    ("spine/tenancy.yaml", "/cells/{cellId}/endpoints", "get", "listCellEndpoints",
     "tenancy", "PLATFORM_CELL_VIEW_OR_SCOPE_VIEW", "tenant",
     "Where each service answers inside a cell",
     "**A cross-cell call needs an address and the addresses were not readable.** `contract_"
     "version` is on the row because two cells can run different versions of the same contract "
     "during a rollout, and a caller that assumes otherwise fails in the least debuggable way.",
     "list", "PlatformCellEndpoint"),
    ("spine/cross-region.yaml", "/cell-connections", "get", "listCellConnections",
     "cross-region", "REGION_CONFIGURE", "tenant",
     "Which cells may talk to which",
     "**A connection has a validity window, which is what makes this a table rather than a "
     "config flag.** A link opened for a summer festival and never closed is a standing "
     "cross-cell path nobody remembers authorising.",
     "list", "SyncCellConnection"),
    ("spine/cross-region.yaml", "/cross-cell-requests", "get", "listCrossCellRequests",
     "cross-region", "ORDER_VIEW", "tenant",
     "Calls that had to leave a cell",
     "**This is how anyone finds out the topology is wrong.** A pair of cells exchanging "
     "thousands of these is usually a tenant homed in the wrong cell, and until now the evidence "
     "existed and could not be read.\n\n`correlationId` is what joins a slow guest-facing request "
     "to the hop that made it slow. Routed to the analytical replica: this is diagnosis, and it "
     "must not compete with the traffic it is diagnosing.",
     "page", "SyncCrossCellRequest"),

    # ---- wallet
    ("satellite/wallet.yaml", "/wallets/{walletId}/balance", "get", "getWalletBalance",
     "wallet", "WALLET_VIEW", "venue",
     "A wallet's balance",
     "**Keyed by wallet, not by guest, and that is the cross-cell decision.** A shared wallet "
     "spans venues and a guest spans cells; listing balances by guest would make a till in "
     "another cell fetch across the boundary on a payment path. The wallet's own cell owns the "
     "balance and answers for it.",
     "get", "WalletBalance"),
    ("satellite/wallet.yaml", "/wallets/{walletId}/holds", "get", "listWalletHolds",
     "wallet", "WALLET_VIEW", "venue",
     "Funds held against a wallet",
     "**A hold is the difference between a balance and a spendable balance**, and a guest "
     "refused at a till with money showing is this table being invisible. `seating.seat_hold_item` "
     "and `control.rollout` both point at it.",
     "list", "WalletHold"),
]

# Composed schemas the operations above need.
COMPOSED = {
    "spine/catalogue.yaml": """    DynamicPriceRuleDetail:
      type: object
      x-ticvai-persistence: none — composed from a rule, its conditions and its actions
      description: >
        **A rule is unreadable without both halves.** The conditions say when it fires, the
        actions say what it does to the price, and `minPrice`/`maxPrice` on the action are the
        guard rails a reviewer looks for first.
      required:
      - rule
      properties:
        rule:
          $ref: '#/components/schemas/PricingDynamicPriceRule'
        conditions:
          type: array
          items:
            $ref: '#/components/schemas/PricingDynamicPriceCondition'
        actions:
          type: array
          items:
            $ref: '#/components/schemas/PricingDynamicPriceAction'
""",
    "satellite/payments.yaml": """    PaymentRuleSet:
      type: object
      x-ticvai-persistence: none — composed from the three payment rule tables
      description: >
        **Three tables, one decision.** Whether a guest may pay with this method, in this
        currency, and what it costs the venue are evaluated together at checkout. An
        administrator changing one without seeing the others is how a method becomes eligible in
        a currency it cannot settle.
      properties:
        currencyRules:
          type: array
          items:
            $ref: '#/components/schemas/PaymentsCurrencyRule'
        eligibilityRules:
          type: array
          items:
            $ref: '#/components/schemas/PaymentsEligibilityRule'
        feeRules:
          type: array
          items:
            $ref: '#/components/schemas/PaymentsFeeRule'
""",
    "satellite/marketing-crm.yaml": """    GuestExtraFieldDefinition:
      type: object
      x-ticvai-persistence: none — composed from a field and its options
      description: >
        **A select with no options is not a field**, so the options come back with the
        definition rather than from a second call.
      required:
      - field
      properties:
        field:
          $ref: '#/components/schemas/MarketingGuestExtraField'
        options:
          type: array
          items:
            $ref: '#/components/schemas/MarketingGuestExtraOption'
""",
    "satellite/rental.yaml": """    RentalAgreementDetail:
      type: object
      x-ticvai-persistence: none — composed from an agreement and its items
      description: >
        **The items are what was actually handed over.** A signed agreement that cannot list its
        equipment settles no dispute about a missing helmet.
      required:
      - agreement
      properties:
        agreement:
          $ref: '#/components/schemas/RentalAgreement'
        items:
          type: array
          items:
            $ref: '#/components/schemas/RentalAgreementItem'
""",
    "satellite/subscription.yaml": """    PlanTierDetail:
      type: object
      x-ticvai-persistence: none — composed from a tier's allowances and modules
      description: >
        **Two tables that only make sense together.** `tierAllowance` is the numbers — how many
        venues, how many users, unlimited or not — and `tierModule` is which modules are switched
        on. A tier that gained a module and not the allowance to use it sells something the
        enforcement policy will refuse.
      properties:
        allowances:
          type: array
          items:
            $ref: '#/components/schemas/SubscriptionTierAllowance'
        modules:
          type: array
          items:
            $ref: '#/components/schemas/SubscriptionTierModule'
""",
}

# Where a permission had to be chosen from what the contract already uses.
PERM_FIX = {
    "PLATFORM_PLAN_VIEW_OR_MANAGE": "PLATFORM_PLAN_MANAGE",
    "PLATFORM_CELL_VIEW_OR_SCOPE_VIEW": "SCOPE_VIEW",
}

# `rule_id` resolves to `approvals.rule`, the only table short-named `rule`, and `pricing` has
# none — so the same-schema preference cannot help and the column has to say what it means.
RENAMES = [
    ("spine/catalogue.yaml", "pricing.dynamic_price_condition", "ruleId", "dynamicPriceRuleId",
     "rule_id", "dynamic_price_rule_id"),
    ("spine/catalogue.yaml", "pricing.dynamic_price_action", "ruleId", "dynamicPriceRuleId",
     "rule_id", "dynamic_price_rule_id"),
]

# Declared because both `orders.deposit` and `ledger.deposit` exist and the matcher refused.
DECLARE = [("payments.deposit_activity", "deposit_id", "orders.deposit")]

IND = "      "


def body(desc):
    """A block description, indented the way the rest of the file writes them."""
    out = ["%sdescription: >\n" % IND]
    for para in desc.split("\n\n"):
        words, line = para.split(), ""
        for w in words:
            if len(line) + len(w) + 1 > 92:
                out.append("%s  %s\n" % (IND, line))
                line = w
            else:
                line = (line + " " + w).strip()
        if line:
            out.append("%s  %s\n" % (IND, line))
        out.append("\n")
    return "".join(out).rstrip("\n") + "\n"


def params(path, kind):
    out = []
    for name in re.findall(r"\{([A-Za-z]+)\}", path):
        out += ["%s- name: %s\n" % (IND, name), "%s  in: path\n" % IND,
                "%s  required: true\n" % IND, "%s  schema:\n" % IND,
                "%s    type: string\n" % IND, "%s    format: uuid\n" % IND]
    if kind == "page":
        out += ["%s- $ref: %scommon.yaml#/components/parameters/PageSize\n" % (IND, REL),
                "%s- $ref: %scommon.yaml#/components/parameters/PageCursor\n" % (IND, REL)]
    if kind in ("set", "setList", "post"):
        out += ["%s- $ref: %scommon.yaml#/components/parameters/IdempotencyKey\n" % (IND, REL)]
    return ("%sparameters:\n" % IND) + "".join(out) if out else ""


REL = "../shared/"


def render(op):
    (_c, path, verb, oid, tag, perm, scope, summary, desc, kind, schema) = op
    perm = PERM_FIX.get(perm, perm)
    s = ["    %s:\n" % verb, "      operationId: %s\n" % oid,
         "      summary: %s\n" % summary, body(desc),
         "      tags:\n      - %s\n" % tag,
         "      x-ticvai-permission: %s\n" % perm,
         "      x-ticvai-audience:\n      - staff\n",
         "      x-ticvai-scope-level: %s\n" % scope]
    if verb == "get":
        s.append("      x-ticvai-read-routing: %s\n"
                 % ("analytical" if oid == "listCrossCellRequests" else "replica"))
    if verb == "put":
        s.append("      x-ticvai-config-scope: %s\n" % scope)
    s.append(params(path, kind))
    if kind in ("set", "setList", "post"):
        item = ("                $ref: '#/components/schemas/%s'\n" % schema)
        inner = (("              type: array\n              items:\n" + item)
                 if kind == "setList" else
                 ("              $ref: '#/components/schemas/%s'\n" % schema))
        s += ["      requestBody:\n        required: true\n        content:\n",
              "          application/json:\n            schema:\n", inner]
    code = "'201'" if kind == "post" else "'200'"
    s += ["      responses:\n        %s:\n          description: %s\n" % (code, summary),
          "          content:\n            application/json:\n              schema:\n"]
    if kind == "page":
        s += ["                allOf:\n",
              "                - $ref: %scommon.yaml#/components/schemas/Page\n" % REL,
              "                - type: object\n                  properties:\n",
              "                    items:\n                      type: array\n",
              "                      items:\n",
              "                        $ref: '#/components/schemas/%s'\n" % schema]
    elif kind in ("list", "setList"):
        s += ["                type: array\n                items:\n",
              "                  $ref: '#/components/schemas/%s'\n" % schema]
    else:
        s += ["                $ref: '#/components/schemas/%s'\n" % schema]
    return "".join(s)


def main():
    apply = "--apply" in sys.argv[1:]
    by_contract = {}
    for op in OPS:
        by_contract.setdefault(op[0], []).append(op)

    texts, added = {}, 0
    for rel, ops in sorted(by_contract.items()):
        path = C(rel)
        s = io.open(path, encoding="utf-8").read()
        if ("operationId: %s\n" % ops[0][3]) in s:
            print("    %-30s already wired" % rel)
            texts[path] = s
            continue
        blocks, seen = [], {}
        for op in ops:
            seen.setdefault(op[1], []).append(op)
        for p, group in seen.items():
            blocks.append("  %s:\n" % p)
            for op in group:
                blocks.append(render(op))
                added += 1
        block = "".join(blocks)
        if rel in COMPOSED:
            j = s.find("\n  schemas:\n")
            k = j + len("\n  schemas:\n")
            s = s[:k] + COMPOSED[rel] + s[k:]
        i = s.find("\ncomponents:\n")
        if i < 0:
            print("    !! %s has no components block" % rel)
            return 1
        s = s[:i + 1] + block + s[i + 1:]
        texts[path] = s
        print("    %-30s +%d operation(s)" % (rel, len(ops)))

    # The pricing rule keys.
    for rel, tag, old, new, _so, _sn in RENAMES:
        p = C(rel)
        s = texts.get(p) or io.open(p, encoding="utf-8").read()
        i = s.find("x-ticvai-persistence: %s\n" % tag)
        if i < 0:
            print("    !! %s not found" % tag)
            return 1
        a = s.rfind("\n    ", 0, i) + 1
        nxt = re.search(r"^    [A-Za-z]", s[i:], re.M)
        b = i + (nxt.start() if nxt else len(s) - i)
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(old) + r"(?![A-Za-z])")
        if pat.search(s[a:b]):
            texts[p] = s[:a] + pat.sub(new, s[a:b]) + s[b:]
            print("    %-46s -> %s" % (tag + "." + old, new))

    docs = {}
    for path, s in texts.items():
        try:
            docs[path] = yaml.safe_load(s)
        except Exception as e:
            print("    !! %s would not parse: %s" % (os.path.basename(path), str(e)[:200]))
            return 1
        have = set((docs[path].get("components") or {}).get("schemas") or {})
        for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                                  yaml.safe_dump(docs[path]))):
            if ref not in have:
                print("    !! %s refs %s locally and does not define it"
                      % (os.path.basename(path), ref))
                return 1
    print("    %d contract(s) parse, every local $ref resolves, %d operation(s)"
          % (len(texts), added))

    # Handoff: the renames and the one declared reference.
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    n = 0
    for _r, tag, _o, _nn, s_old, s_new in RENAMES:
        for c in (S.get("cols") or {}).get(tag, []):
            if c.get("column") == s_old:
                c["column"] = s_new
                c["references"] = "pricing.dynamic_price_rule"
                c["referenceHow"] = "declared"
                n += 1
    for tag, col, target in DECLARE:
        for c in (S.get("cols") or {}).get(tag, []):
            if c.get("column") == col:
                c["references"] = target
                c["referenceHow"] = "declared"
                n += 1
    print("    schema-reference: %d column(s) renamed or declared" % n)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    for path, s in texts.items():
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    print("  -> %d contracts and handoff/schema-reference.json" % len(texts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
