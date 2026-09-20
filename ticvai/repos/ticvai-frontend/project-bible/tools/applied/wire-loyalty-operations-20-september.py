#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fourteen operations for the eight loyalty tables decision 8 accepted and nothing could reach.

**Decision 8 took their split and the tables arrived without a way in.** `marketing.loyalty_programme`
has 7 operations and `marketing.loyalty_position` has 8 — the header and the balance were wired.
The rules that earn the points, the ledger behind the balance, the rewards the points buy and the
badges a guest collects were not.

    marketing.loyalty_rule              0 ops    campaign rules: bonus, multiplier, conditions
    marketing.points_redemption_rule    0 ops    what points can be turned into
    marketing.loyalty_campaign          0 ops    a programme's time-boxed campaigns
    marketing.loyalty_points            0 ops    **the ledger** — decision 8's whole point
    marketing.reward                    0 ops
    marketing.reward_assignment         0 ops
    marketing.badge                     0 ops
    marketing.customer_badge            0 ops

`marketing.points_earning_rule` is not in this list: it is `LoyaltyProgramme.earnRules[]` and is
already reached through the programme.

## The ledger is the one that mattered

The merge response says it plainly: *"`marketing.loyalty_position` is a balance with no ledger
behind it. It cannot be audited or corrected."* We took `marketing.loyalty_points` and then gave
it no operation, so the package held the ledger and still could not read it. **A balance nobody
can explain is the same defect whether the ledger is missing or merely unreachable.**

`listLoyaltyPointEntries` reads it and `adjustLoyaltyPoints` is the correction path —
`reversed_loyalty_points_id` on the table exists precisely so a correction is a new row pointing
at the one it reverses, never an edit. **A loyalty balance that can be edited is a currency that
can be printed.**

## Rules are set as a set

`getLoyaltyRules` and `setLoyaltyRules` work on the whole rule set for a programme rather than
row by row. Earning, redemption and campaign rules are read together and only make sense
together — a redemption rule worth 500 points beside an earning rule that grants 5 per visit is
a hundred visits, and an administrator is reasoning about that ratio, not about one row. Applying
them one at a time also leaves the programme inconsistent in the middle, which for a live
loyalty scheme means guests earning under one rule and redeeming under another.

## Still outstanding from decision 8, and deliberately not done here

Decision 8 said *"retire `loyalty_tier`, and add a real tier table"*. **The retire happened and
the tier table does not exist** — `marketing.loyalty_position` still carries `tier_code` and
`tier_name` as denormalised strings.

It is not added here because `schema-history.json` declares `marketing.loyalty_tier` renamed to
`marketing.points_earning_rule` on 20 September. **Re-introducing that name for a different thing
would make every document mentioning it ambiguous** and `check-doc-tables` would report the
rename as stale. It needs a name chosen on purpose, which is a decision and not a wiring.

    python3 tools/applied/wire-loyalty-operations-20-september.py --apply
"""
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET = os.path.join(ROOT, "contracts", "satellite", "marketing-crm.yaml")

PATHS = '''  /loyalty/programmes/{programmeId}/rules:
    get:
      operationId: getLoyaltyRules
      summary: Every rule a loyalty programme runs on
      description: 'Decision 8 of the schema merge. **`marketing.loyalty_programme` holds no rules** —
        it is a header with a code, a name and an expiry. The rules were taken from the backend
        workbook and had no operation, so a programme could be created and never configured.

        Returned as a set because they are read as a set: a redemption worth 500 points beside an
        earning rule granting 5 per visit is a hundred visits, and **the ratio is what an
        administrator is reasoning about**, not any one row.

        '
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: programmeId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Rules
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoyaltyRuleSet'
        '404':
          description: No such programme
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
    put:
      operationId: setLoyaltyRules
      summary: Replace a programme's rules as one set
      description: '**Applied whole or not at all.** Setting rules one at a time leaves a live
        programme inconsistent in the middle, which means guests earning under one rule and
        redeeming under another.

        '
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_MANAGE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-config-scope: venue
      parameters:
      - name: programmeId
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
              $ref: '#/components/schemas/LoyaltyRuleSet'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoyaltyRuleSet'
        '409':
          description: A rule references a reward or product that does not exist
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /loyalty/campaigns:
    get:
      operationId: listLoyaltyCampaigns
      summary: Time-boxed campaigns inside a programme
      description: '**A campaign is how a rule gets a start and an end.** Double points in August is
        the programme''s earning rule plus a window, and without this table it is a rule somebody has
        to remember to switch off.

        '
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: programmeId
        in: query
        schema:
          type: string
          format: uuid
      - name: activeOn
        in: query
        schema:
          type: string
          format: date-time
      responses:
        '200':
          description: Campaigns
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MarketingLoyaltyCampaign'
    put:
      operationId: setLoyaltyCampaign
      summary: Define a loyalty campaign and its window
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_MANAGE
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
              $ref: '#/components/schemas/MarketingLoyaltyCampaign'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketingLoyaltyCampaign'
  /loyalty/points:
    get:
      operationId: listLoyaltyPointEntries
      summary: The ledger behind a points balance
      description: '**This is the point of decision 8.** The merge response says it plainly:
        *"`marketing.loyalty_position` is a balance with no ledger behind it. It cannot be audited or
        corrected."* We took `marketing.loyalty_points` and gave it no operation, so the package held
        the ledger and still could not read it.

        Every row carries `balance_after`, so a disputed balance can be walked rather than argued
        about.

        '
      tags:
      - loyalty
      x-ticvai-permission: LOYALTY_ACCRUE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: analytical
      parameters:
      - name: customerId
        in: query
        schema:
          type: string
          format: uuid
      - name: programmeId
        in: query
        schema:
          type: string
          format: uuid
      - name: transactionType
        in: query
        schema:
          type: string
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Entries
          content:
            application/json:
              schema:
                allOf:
                - $ref: ../shared/common.yaml#/components/schemas/Page
                - type: object
                  properties:
                    items:
                      type: array
                      items:
                        $ref: '#/components/schemas/MarketingLoyaltyPoints'
  /loyalty/points/adjustments:
    post:
      operationId: adjustLoyaltyPoints
      summary: Correct a balance by posting a reversing entry
      description: '**A loyalty balance that can be edited is a currency that can be printed.**
        `reversed_loyalty_points_id` exists on the table precisely so a correction is a new row
        pointing at the one it reverses — the original entry is never touched and the history stays
        walkable.

        Goodwill and service-recovery grants use the same path, so every movement has a reason and an
        author.

        '
      tags:
      - loyalty
      x-ticvai-permission: LOYALTY_ACCRUE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdjustLoyaltyPointsRequest'
      responses:
        '201':
          description: Posted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketingLoyaltyPoints'
        '409':
          description: The entry being reversed is already reversed, or the balance would go negative
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /loyalty/rewards:
    get:
      operationId: listRewards
      summary: What points can be turned into
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_VIEW
      x-ticvai-audience:
      - staff
      - guest
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: programmeId
        in: query
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Rewards
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MarketingReward'
    put:
      operationId: setReward
      summary: Define a reward and its points cost
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_MANAGE
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
              $ref: '#/components/schemas/MarketingReward'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketingReward'
  /loyalty/reward-assignments:
    get:
      operationId: listRewardAssignments
      summary: Rewards issued to guests, and whether they were used
      description: '**A reward is a definition and an assignment is an instance**, which is why the
        code, the expiry and the order it was redeemed against live here rather than on the reward.

        '
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: customerId
        in: query
        schema:
          type: string
          format: uuid
      - name: status
        in: query
        schema:
          type: string
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Assignments
          content:
            application/json:
              schema:
                allOf:
                - $ref: ../shared/common.yaml#/components/schemas/Page
                - type: object
                  properties:
                    items:
                      type: array
                      items:
                        $ref: '#/components/schemas/MarketingRewardAssignment'
    post:
      operationId: issueReward
      summary: Issue a reward to a guest
      description: '**Issuing spends points and the spend is a ledger entry**, not a decrement — the
        assignment and the `redemption` row are written together or neither is.

        '
      tags:
      - loyalty
      x-ticvai-permission: LOYALTY_REDEEM
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/MarketingRewardAssignment'
      responses:
        '201':
          description: Issued
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketingRewardAssignment'
        '409':
          description: Not enough points, or the reward is not available at this venue
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /badges:
    get:
      operationId: listBadges
      summary: Badges a guest can be awarded
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_VIEW
      x-ticvai-audience:
      - staff
      - guest
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Badges
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MarketingBadge'
    put:
      operationId: setBadge
      summary: Define a badge
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_MANAGE
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
              $ref: '#/components/schemas/MarketingBadge'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketingBadge'
  /customers/{customerId}/badges:
    get:
      operationId: listCustomerBadges
      summary: Badges a guest holds
      description: '**A badge can expire and can be revoked**, so this returns the status rather than
        a list of names — a guest page showing a lapsed badge as current is a promise the venue did
        not make.

        '
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_VIEW
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
      responses:
        '200':
          description: Badges held
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/MarketingCustomerBadge'
    post:
      operationId: awardBadge
      summary: Award a badge
      description: '**`sourceType` and `sourceReferenceId` say why.** A badge awarded by a challenge,
        by a purchase or by a manager are three different things to a guest asking how they got it,
        and a badge with no provenance cannot be explained or withdrawn.

        '
      tags:
      - loyalty
      x-ticvai-permission: MARKETING_MANAGE
      x-ticvai-audience:
      - staff
      - service
      x-ticvai-scope-level: venue
      parameters:
      - name: customerId
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
              $ref: '#/components/schemas/MarketingCustomerBadge'
      responses:
        '201':
          description: Awarded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MarketingCustomerBadge'
        '409':
          description: Already held and not expired
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
'''

SCHEMAS = '''    LoyaltyRuleSet:
      type: object
      x-ticvai-persistence: none — composed from the rule tables of one programme
      description: >
        **Every rule a programme runs on, read and written as one thing.** Earning, redemption and
        campaign rules only make sense against each other: a 500-point redemption beside a 5-point
        earning rule is a hundred visits, and that ratio is the artefact being configured.

        Earning rules are not repeated here — they are `LoyaltyProgramme.earnRules[]` and reached
        through the programme, which is where they were already declared.
      required:
      - programmeId
      properties:
        programmeId:
          type: string
          format: uuid
        campaignRules:
          type: array
          description: Bonus, multiplier and condition rules, each scoped to a campaign window.
          items:
            $ref: '#/components/schemas/MarketingLoyaltyRule'
        redemptionRules:
          type: array
          items:
            $ref: '#/components/schemas/MarketingPointsRedemptionRule'
    AdjustLoyaltyPointsRequest:
      type: object
      x-ticvai-persistence: none — writes marketing.loyalty_points
      description: >
        **A correction is a new entry, never an edit.** Reversing an entry writes a row pointing at
        it through `reversedLoyaltyPointsId`; granting goodwill writes a row with no reversal
        target. Either way the movement has a reason and an author, and the history stays walkable.
      required:
      - customerId
      - programmeId
      - points
      - reason
      properties:
        customerId:
          type: string
          format: uuid
        programmeId:
          type: string
          format: uuid
        points:
          type: integer
          description: Signed. Negative removes points, and the balance may not go below zero.
        reason:
          type: string
          enum:
          - correction
          - goodwill
          - serviceRecovery
          - fraudReversal
          - expiryAdjustment
          - migration
        reversedLoyaltyPointsId:
          type: string
          format: uuid
          nullable: true
          description: >
            The entry this reverses, when it is a reversal. **Set it and the sign is checked
            against the original** — a reversal that does not cancel what it names is a second
            grant wearing a correction's label.
        notes:
          type: string
          maxLength: 1000
          nullable: true
'''


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(TARGET, encoding="utf-8").read()
    if "operationId: listLoyaltyPointEntries" in s:
        print("  already wired — nothing to do")
        return 0

    i = s.find("\ncomponents:\n")
    if i < 0:
        print("  !! no components block")
        return 1
    s = s[:i + 1] + PATHS + s[i + 1:]

    j = s.find("\n  schemas:\n")
    if j < 0:
        print("  !! no components.schemas block")
        return 1
    k = j + len("\n  schemas:\n")
    s = s[:k] + SCHEMAS + s[k:]

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1

    want = ["MarketingBadge", "MarketingCustomerBadge", "MarketingLoyaltyCampaign",
            "MarketingLoyaltyPoints", "MarketingLoyaltyRule", "MarketingPointsRedemptionRule",
            "MarketingReward", "MarketingRewardAssignment", "LoyaltyRuleSet",
            "AdjustLoyaltyPointsRequest"]
    have = set((doc.get("components") or {}).get("schemas") or {})
    missing = [w for w in want if w not in have]
    if missing:
        print("  !! schema(s) referenced and not defined: %s" % ", ".join(missing))
        return 1

    new = sorted({o.get("operationId") for p in (doc.get("paths") or {}).values()
                  for o in p.values()
                  if isinstance(o, dict) and ("operationId: %s\n" % o.get("operationId")) in PATHS})
    print("  %d new operation(s), all %d referenced schema(s) exist:" % (len(new), len(want)))
    for o in new:
        print("      %s" % o)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(TARGET, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/marketing-crm.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
