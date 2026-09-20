#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Membership: the half of a TAKE BODY verdict that was never executed, plus eleven operations.

The verdict on `catalogue.membership_plan` was **TAKE BODY**:

    "our catalogue.entitlement_template is the plan — validity kind, entries, transferability,
     eligibility, stored value. It has no renewal rules; take those"

**Phase 3 took the three satellite tables and did neither half of that.** It created
`membership_programme`, `membership_benefit` and `plan_benefit`, declined the plan table
correctly, and then left every key that pointed at the plan pointing at nothing real — while the
renewal rules it was supposed to take were never taken.

## Where the plan keys went

There is no `membership_plan`, so the convention matcher resolved `plan_id` to the only plan
there is:

    identity.customer_membership.plan_id       -> subscription.plan
    catalogue.plan_benefit.membership_plan_id  -> subscription.plan
    orders.membership_renewal.plan_id          -> subscription.plan

**`subscription.plan` is what a venue pays TICVAI** — `cell_tier`, `base_price`,
`includes_branded_app`, `included_ai_tokens`, `subscriber_count`. A guest's annual pass pointed at
whether the venue's SaaS tier includes a branded app.

This is the `user_id` finding again and the cause is identical: **a name resolved to the nearest
table rather than the right one, because the right one deliberately does not exist.** Renamed to
`entitlement_template_id`, which is what the verdict said the plan is, and which
`catalogue.membership_benefit.entitlement_template_id` already spelled correctly.

## The renewal rules, taken now

`catalogue.entitlement_template` has 35 columns and not one of them is about renewing. Meanwhile
`identity.customer_membership.auto_renew` has no default to read, and
`orders.membership_renewal` records `previous_expiry_at`, `new_expiry_at` and `failure_reason`
against a term, a grace period and a price that were nowhere.

    autoRenewDefault      what a membership starts with, since the holder row carries the flag
                          and nothing said what it should be
    renewalTermDays       what a renewal extends by. `new_expiry_at` was being computed from
                          a number that did not exist
    renewalGraceDays      how long a lapsed membership can still be renewed. `failure_reason`
                          implies a window and there was none
    renewalVariantId      **what a renewal sells, which is usually not what joining sold.**
                          A first-year price and a renewal price are different products and
                          pointing both at one variant makes the discount unrepresentable

## Cross-cell: composed reads, following ADR-0010

`EntitlementTemplate.crossesCells` says *"True propagates a redemption right to other cells on
issue"* — **the package's answer to cross-cell is to propagate on issue, not to fetch on read**,
and this follows it rather than inventing a second mechanism.

Where a read is unavoidable, it is composed. `getMembership` returns the membership, its status
history and its benefit usage **in one call**. A guest's membership lives in their home cell
(`platform.guest_link.home_cell_name`), so a venue in another cell reading those three tables
separately is **three cross-cell round trips at a counter**. One composed read is one.

**Renewals are deliberately left out of it**, and that is the same criterion applied honestly.
They belong to OrderService and the rest belongs to IdentityService, and the package has **no
cross-contract `$ref` anywhere** — each contract is one service's API. Composing them would make
every membership read an in-cell service hop in order to save a second cross-cell call on the
rare read where somebody disputes a renewal. `history` already records the lapse transition, so
the common question is answered without leaving the service.

    listMembershipProgrammes / set      catalogue.membership_programme
    listMembershipBenefits / set        catalogue.membership_benefit
    getPlanBenefits / set               catalogue.plan_benefit, keyed by entitlement template
    listCustomerMemberships             identity.customer_membership
    getMembership                       + membership_history + benefit_usage
    recordBenefitUsage                  identity.benefit_usage
    listMembershipRenewals              orders.membership_renewal, kept separate - see above
    renewMembership

    python3 tools/applied/wire-membership-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")
CAT = os.path.join(ROOT, "contracts", "spine", "catalogue.yaml")
IDN = os.path.join(ROOT, "contracts", "spine", "identity.yaml")
ORD = os.path.join(ROOT, "contracts", "spine", "orders.yaml")

RENAMES = [
    (IDN, "identity.customer_membership", "planId", "entitlementTemplateId",
     "plan_id", "entitlement_template_id"),
    (CAT, "catalogue.plan_benefit", "membershipPlanId", "entitlementTemplateId",
     "membership_plan_id", "entitlement_template_id"),
    (ORD, "orders.membership_renewal", "planId", "entitlementTemplateId",
     "plan_id", "entitlement_template_id"),
]

RENEWAL = """        autoRenewDefault:
          type: boolean
          default: false
          description: >
            **Taken from their `membership_plan`, 20 September — the "take those" half of the
            TAKE BODY verdict.** `identity.customer_membership.auto_renew` carries the flag per
            holder and nothing said what it should start as.
        renewalTermDays:
          type: integer
          nullable: true
          description: >
            What a renewal extends the membership by. `orders.membership_renewal` records
            `previousExpiryAt` and `newExpiryAt` and **the number between them lived nowhere**.
        renewalGraceDays:
          type: integer
          default: 0
          description: >
            How long after expiry a membership can still be renewed rather than rejoined.
            `membership_renewal.failureReason` implies a window and there was none, so a failed
            card on the expiry date had no defined consequence.
        renewalVariantId:
          type: string
          format: uuid
          nullable: true
          description: >
            **What a renewal sells, which is usually not what joining sold.** A first-year price
            and a renewal price are different products, and pointing both at one variant makes a
            loyalty discount unrepresentable. Null means renewal sells the same thing.
"""

PATHS_CAT = '''  /membership-programmes:
    get:
      operationId: listMembershipProgrammes
      summary: Membership schemes, the level above a plan
      description: 'Decision 9 of the schema merge. **A programme groups plans**; the plan itself is
        `catalogue.entitlement_template`, which the TAKE BODY verdict settled — validity kind,
        entries, transferability, eligibility and stored value were already there.

        '
      tags:
      - catalogue
      x-ticvai-permission: CATALOGUE_VIEW
      x-ticvai-audience:
      - staff
      - guest
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Programmes
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CatalogueMembershipProgramme'
    put:
      operationId: setMembershipProgramme
      summary: Define a membership programme
      tags:
      - catalogue
      x-ticvai-permission: CATALOGUE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CatalogueMembershipProgramme'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CatalogueMembershipProgramme'
  /membership-benefits:
    get:
      operationId: listMembershipBenefits
      summary: Benefits a plan can grant
      description: 'Decision 9. **Benefits were columns on `entitlement_template`**, so adding one
        was a schema change — `can_share_media`, `can_claim_shop_and_drop`, `included_value`. Its 15
        operations and 34 screens read 34 columns to get three.

        '
      tags:
      - catalogue
      x-ticvai-permission: CATALOGUE_VIEW
      x-ticvai-audience:
      - staff
      - guest
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Benefits
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CatalogueMembershipBenefit'
    put:
      operationId: setMembershipBenefit
      summary: Define a benefit
      tags:
      - catalogue
      x-ticvai-permission: CATALOGUE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CatalogueMembershipBenefit'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CatalogueMembershipBenefit'
  /entitlement-templates/{templateId}/benefits:
    get:
      operationId: getPlanBenefits
      summary: Which benefits a plan grants, and how much of each
      description: '**Keyed by the entitlement template because that is the plan.** `plan_benefit`
        carries the usage limit and the period, which is the part a benefit definition cannot hold —
        four free coffees a month is the same benefit as one a year.

        '
      tags:
      - catalogue
      x-ticvai-permission: CATALOGUE_VIEW
      x-ticvai-audience:
      - staff
      - guest
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: templateId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Benefits granted
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CataloguePlanBenefit'
    put:
      operationId: setPlanBenefits
      summary: Replace the benefits a plan grants
      description: '**Set whole.** A plan losing one benefit and gaining another is one change to a
        guest, and applying it in two steps sells a plan that briefly has neither or both.

        '
      tags:
      - catalogue
      x-ticvai-permission: CATALOGUE_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - name: templateId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/CataloguePlanBenefit'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CataloguePlanBenefit'
'''

PATHS_IDN = '''  /customers/{customerId}/memberships:
    get:
      operationId: listCustomerMemberships
      summary: Memberships a customer holds
      description: '**We had `entitlement_template` and no holder record** — the plan existed and
        nothing said who was on it. Decision 9 took `identity.customer_membership` for exactly that.

        '
      tags:
      - identity
      x-ticvai-permission: GUEST_VIEW
      x-ticvai-audience:
      - staff
      - guest
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: customerId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - name: status
        in: query
        schema:
          type: string
      responses:
        '200':
          description: Memberships
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/IdentityCustomerMembership'
  /memberships/{membershipId}:
    get:
      operationId: getMembership
      summary: A membership with its history, usage and renewals
      description: '**Composed because of where the data lives.** A guest''s membership sits in their
        home cell (`platform.guest_link.homeCellName`), so a venue in another cell reading the
        membership, its status history, its benefit usage and its renewal attempts as four calls
        makes **four cross-cell round trips at a counter**. One composed read is one.

        This follows ADR-0010 rather than adding to it: `EntitlementTemplate.crossesCells` already
        propagates a redemption right on issue, so the hot path — is this pass valid — stays local.
        This endpoint is the cold path, where somebody is asking why.

        '
      tags:
      - identity
      x-ticvai-permission: GUEST_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: membershipId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Membership
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MembershipDetail'
        '404':
          description: No such membership
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /memberships/{membershipId}/benefit-usage:
    post:
      operationId: recordBenefitUsage
      summary: Consume a benefit
      description: '**`remaining_quantity` is written on the row, not computed on read.** A counter
        asking whether a guest has a free coffee left must not sum a usage history across a cell
        boundary, and a benefit with a monthly limit has a period the sum would have to know about
        anyway.

        '
      tags:
      - identity
      x-ticvai-permission: GUEST_MANAGE
      x-ticvai-audience:
      - staff
      - service
      x-ticvai-scope-level: venue
      x-ticvai-offline-capable: true
      x-ticvai-conflict-policy: serverWins
      parameters:
      - name: membershipId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/IdentityBenefitUsage'
      responses:
        '201':
          description: Recorded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IdentityBenefitUsage'
        '409':
          description: The benefit is exhausted for this period, or the membership is not active
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
'''

PATHS_ORD = '''  /memberships/{membershipId}/renewals:
    get:
      operationId: listMembershipRenewals
      summary: Renewal attempts and why they failed
      description: '**A failed renewal is the thing a guest phones about**, and until 20 September
        there was nowhere to read one. `failureReason` is on the row precisely so the answer does not
        require reading a payment provider''s logs.

        '
      tags:
      - orders
      x-ticvai-permission: ORDER_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: membershipId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Renewals
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/OrdersMembershipRenewal'
    post:
      operationId: renewMembership
      summary: Renew a membership
      description: '**The term, the grace period and what a renewal sells come from the entitlement
        template**, which is the plan. Until those four columns were added on 20 September this
        operation could not have computed `newExpiryAt` — the number to add did not exist anywhere.

        A renewal inside the grace period extends from the old expiry, not from today; outside it,
        the membership is rejoined rather than renewed, and the two produce different dates.

        '
      tags:
      - orders
      x-ticvai-permission: ORDER_MANAGE
      x-ticvai-audience:
      - staff
      - service
      x-ticvai-scope-level: venue
      parameters:
      - name: membershipId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrdersMembershipRenewal'
      responses:
        '201':
          description: Renewed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrdersMembershipRenewal'
        '409':
          description: Outside the grace period, or already renewed for this term
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
'''

DETAIL = """    MembershipDetail:
      type: object
      x-ticvai-persistence: none — composed from the membership and three related tables
      description: >
        **One cross-cell round trip instead of three.** A membership lives in the guest's home
        cell and its status history and benefit usage live beside it, in the same service. A venue
        in another cell asking why a pass was refused needs all three, and asking three times is
        three round trips at a counter with somebody waiting.

        The hot path is not this: `EntitlementTemplate.crossesCells` propagates the redemption
        right on issue (ADR-0010), so *is this valid* stays local. This is the cold path, where
        somebody is asking why.
      required:
      - membership
      properties:
        membership:
          $ref: '#/components/schemas/IdentityCustomerMembership'
        history:
          type: array
          description: Status changes, most recent first.
          items:
            $ref: '#/components/schemas/IdentityMembershipHistory'
        benefitUsage:
          type: array
          items:
            $ref: '#/components/schemas/IdentityBenefitUsage'

      # **Renewals are deliberately not here, and the reason is the cross-cell criterion itself.**
      # `orders.membership_renewal` belongs to OrderService; this schema belongs to
      # IdentityService. **The package has no cross-contract `$ref` anywhere** — every contract is
      # self-contained, one per service — so including them would make IdentityService call
      # OrderService to build every membership read.
      #
      # That trades one in-cell service hop on EVERY read for one cross-cell call on the rare
      # read where somebody is disputing a renewal. `history` already records the lapse
      # transition, so the common question is answered without leaving the service. When the
      # renewal attempts themselves are wanted, `listMembershipRenewals` is one more call and
      # only then.
"""


def schema_span(text, tag):
    i = text.find("x-ticvai-persistence: %s\n" % tag)
    if i < 0:
        return None, None
    start = text.rfind("\n    ", 0, i) + 1
    nxt = re.search(r"^    [A-Za-z]", text[i:], re.M)
    return start, i + (nxt.start() if nxt else len(text) - i)


def insert_paths(s, block):
    i = s.find("\ncomponents:\n")
    return s[:i + 1] + block + s[i + 1:] if i > 0 else None


def main():
    apply = "--apply" in sys.argv[1:]
    texts = {p: io.open(p, encoding="utf-8").read() for p in (CAT, IDN, ORD)}

    # 1. The three plan keys.
    for path, tag, old, new, _so, _sn in RENAMES:
        s = texts[path]
        a, b = schema_span(s, tag)
        if a is None:
            print("    !! %s not found" % tag)
            return 1
        block = s[a:b]
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(old) + r"(?![A-Za-z])")
        n = len(pat.findall(block))
        if not n:
            print("    %-46s already %s" % (tag + "." + old, new))
            continue
        texts[path] = s[:a] + pat.sub(new, block) + s[b:]
        print("    %-46s -> %-24s (%d)" % (tag + "." + old, new, n))

    # 2. The renewal rules onto EntitlementTemplate.
    c = texts[CAT]
    if "renewalTermDays" in c:
        print("    EntitlementTemplate  already has the renewal rules")
    else:
        i = c.find("x-ticvai-persistence: catalogue.entitlement_template\n")
        j = c.find("        crossesCells:\n", i)
        if j < 0:
            print("    !! crossesCells anchor not found")
            return 1
        c = c[:j] + RENEWAL + c[j:]
        texts[CAT] = c
        print("    EntitlementTemplate  +autoRenewDefault, +renewalTermDays, +renewalGraceDays, "
              "+renewalVariantId")

    # 3. Operations.
    for path, block, marker in ((CAT, PATHS_CAT, "listMembershipProgrammes"),
                                (IDN, PATHS_IDN, "listCustomerMemberships"),
                                (ORD, PATHS_ORD, "renewMembership")):
        if ("operationId: %s\n" % marker) in texts[path]:
            print("    %-18s already wired" % os.path.basename(path))
            continue
        out = insert_paths(texts[path], block)
        if out is None:
            print("    !! no components block in %s" % os.path.basename(path))
            return 1
        texts[path] = out

    # MembershipDetail lives in identity, beside the membership it is about.
    s = texts[IDN]
    if "MembershipDetail:" not in s:
        j = s.find("\n  schemas:\n")
        k = j + len("\n  schemas:\n")
        texts[IDN] = s[:k] + DETAIL + s[k:]

    docs = {}
    for path, s in texts.items():
        try:
            docs[path] = yaml.safe_load(s)
        except Exception as e:
            print("    !! %s would not parse: %s" % (os.path.basename(path), str(e)[:160]))
            return 1
    print("    3 contract(s) parse")

    # `MembershipDetail` refs a schema defined in orders.yaml. A local $ref that resolves to
    # nothing is exactly how a composed response silently derives no lineage.
    # **A local `$ref` that resolves to nothing derives no lineage and fails nothing.** This is
    # how the first cut of this script tried to put `OrdersMembershipRenewal` into an `identity`
    # schema, which is why the check is here rather than in a review.
    for path, doc in docs.items():
        have = set((doc.get("components") or {}).get("schemas") or {})
        body = yaml.safe_dump(doc)
        # **Only a LOCAL ref.** `../shared/common.yaml#/components/schemas/Page` ends in the same
        # text, and matching it reported `Page` as undefined in every contract in the package.
        for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)", body)):
            if ref not in have:
                print("    !! %s refs %s locally and does not define it"
                      % (os.path.basename(path), ref))
                return 1
    print("    every local $ref resolves")

    new_ops = sorted({o.get("operationId")
                      for d in docs.values() for p in (d.get("paths") or {}).values()
                      for o in p.values() if isinstance(o, dict) and o.get("operationId")
                      and ("operationId: %s\n" % o.get("operationId"))
                      in (PATHS_CAT + PATHS_IDN + PATHS_ORD)})
    print("    %d new operation(s):" % len(new_ops))
    for o in new_ops:
        print("        %s" % o)

    # The derived files carry the old column names.
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    fixed = 0
    for _p, tag, _o, _n, s_old, s_new in RENAMES:
        for col in (S.get("cols") or {}).get(tag, []):
            if col.get("column") == s_old:
                col["column"] = s_new
                col["references"] = "catalogue.entitlement_template"
                col["referenceHow"] = "convention"
                fixed += 1
    print("    schema-reference: %d column(s) renamed and repointed" % fixed)

    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    edges = 0
    for r in (G.get("rels") or []):
        for _p, tag, _o, _n, s_old, s_new in RENAMES:
            if r.get("frm") == tag and r.get("col") == s_old:
                r["col"] = s_new
                r["to"] = "catalogue.entitlement_template"
                r["cross"] = "yes" if tag.split(".")[0] != "catalogue" else ""
                edges += 1
    print("    relationship-graph: %d edge(s) repointed" % edges)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    for path, s in texts.items():
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    io.open(gp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(G, indent=1, ensure_ascii=False))
    print("  -> 3 contracts and two handoff files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
