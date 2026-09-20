#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decision 14 — the loyalty tier table — and decision 15 — inspection answers.

Both were carried as open items rather than done, and both are decisions before they are
schema changes, which is why they waited.

================================================================================
## 14 · The tier table decision 8 promised — `marketing.programme_tier`
================================================================================

Decision 8 said *"retire `loyalty_tier`, and add a real tier table"*. **The retire happened and
the add did not.** `marketing.loyalty_position` still carries `tier_code` and `tier_name` as
denormalised strings and there is no definition of what tiers exist.

### The name, which is the part that needed deciding

`marketing.loyalty_tier` is the natural name and **it is spent**: `schema-history.json` declares
it renamed to `marketing.points_earning_rule` on 20 September. Re-using it would not break
`check-doc-tables` — that checker skips a token which is a current table — but it would leave the
history saying a name was renamed while a table of that name exists meaning something else.
**A rename record that contradicts the schema is worse than an awkward name.**

`marketing.tier` was considered and rejected: `subscription.tier_allowance` and
`subscription.tier_module` are about a SaaS plan's tier, and one bare `tier` in a package with
two tier concepts is the `subscription.plan` mistake waiting to happen again.

**`marketing.programme_tier`** sits beside `marketing.loyalty_programme`, which is its parent,
and says what it is a tier *of*. `tier_id` resolves to it as a unique suffix, and the
same-schema preference added today keeps a `marketing` column pointing at it.

### Scored, and the answer is "both"

| | |
|---|---|
| **Maintainability** | **the table.** A tier is currently a string somebody writes; thresholds live in code, so adding a tier is a code change |
| **Readability** | **the table.** `tier_code: 'GOLD'` on a balance row cannot tell you what tiers exist or what Gold requires |
| **Optimised access** | **the denormalised copy.** A till showing *Gold* beside a balance should not join |
| **DB strain** | tiny, read-mostly, cacheable. Neutral |
| **Cross-cell** | **the denormalised copy, decisively.** Tier definitions are programme config replicated per cell; the guest's tier is on their position row in their home cell. A till reading the definition to render a badge would be a cross-cell call to print a word |

**So both, and that is not a compromise.** The definition table is the source of truth and the two
strings on the position are a cache of it — which is what they already were, except that nothing
they cached existed.

**`points_to_next_tier` is the proof.** It is on `loyalty_position` today and computed from a
threshold that lives nowhere — exactly the shape of `renewalTermDays`, where
`orders.membership_renewal` computed `newExpiryAt` from a number no table held.

================================================================================
## 15 · Inspection answers — `maintenance.inspection_item`
================================================================================

**The answers are already submitted.** `SubmitInspectionRequest.responses[]` takes a key, a
value, a pass flag, a note and attachments, and is tagged `"none — request only"`. The only
persistence ever claimed for them was `maintenance.inspection_response`, a table that does not
exist and that this script's predecessor removed from the `Inspection` tag on 20 September.

    maintenance.inspection_template_item   the questions — 11 columns, including
                                           `is_safety_critical` and `requires_photo_on_fail`
    maintenance.inspection                 `failed_item_count`, `failed_safety_critical_count`
    (nothing)                              which item failed

**A safety-critical failure takes an asset out of service** — `InspectionResult.consequences`
says so — and the record of *which check failed* was accepted over the wire and dropped.

### Scored

| | |
|---|---|
| **Maintainability** | **the table.** A report on recurring failures has no source today |
| **Readability** | **the table.** `failedItemCount: 3` is three of what |
| **Optimised access** | **keep the counts too.** `listInspections` returns `Inspection` in a list, and twenty item rows per inspection on a list screen is the wrong trade |
| **DB strain** | **the real cost, and it is why the counts stay.** One row per item per inspection is the highest-volume table in `maintenance`; `retainUntil` on the inspection is what bounds it |
| **Cross-cell** | none. An inspection is venue-local |

So the items go on `InspectionResult`, which is the detail response, and **not** on `Inspection`,
which is the list row. `SubmitInspectionRequest` is retagged to say what it actually writes.

`attachmentAssetIds` is an array and is the same deliberate exception as
`workforce.sync_conflict.affectedAssignmentIds`: **evidence attached to an answer at the moment
it was recorded.** It is never queried from the other end — nobody asks which inspection items
reference a photograph — and it must not change when an asset library is reorganised.

    python3 tools/applied/two-decisions-tier-and-inspection-items-20-september.py --apply
"""
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CRM = os.path.join(ROOT, "contracts", "satellite", "marketing-crm.yaml")
MNT = os.path.join(ROOT, "contracts", "satellite", "maintenance.yaml")

TIER = """    MarketingProgrammeTier:
      type: object
      x-ticvai-persistence: marketing.programme_tier
      description: >
        **The tier definition decision 8 promised and nobody built.**
        `marketing.loyalty_position` carried `tierCode`, `tierName` and `pointsToNextTier` as
        denormalised strings and a number, with no table saying what tiers exist or what each
        one requires — so `pointsToNextTier` was computed from a threshold that lived nowhere.

        **Not named `marketing.loyalty_tier`**: that name is recorded in `schema-history.json`
        as renamed to `marketing.points_earning_rule` on 20 September, and a rename record that
        contradicts the schema is worse than a longer name. Not named `marketing.tier` either,
        because `subscription.tier_allowance` is a SaaS plan's tier and one bare `tier` in a
        package with two tier concepts is how `plan_id` came to point at `subscription.plan`.

        **The denormalised copy on the position stays.** A till rendering *Gold* beside a
        balance must not join, and must certainly not cross a cell boundary to print a word.
        This table is the source of truth and those columns are its cache.
      required:
      - loyaltyProgrammeId
      - code
      - name
      - rank
      properties:
        id:
          type: string
          format: uuid
        loyaltyProgrammeId:
          type: string
          format: uuid
        code:
          type: string
          maxLength: 40
        name:
          type: string
          maxLength: 120
        rank:
          type: integer
          description: >
            **Order, not threshold.** Two tiers can share a qualifying rule and still have an
            order, and sorting by points breaks the moment a tier is granted rather than earned.
        minLifetimePoints:
          type: integer
          nullable: true
          description: >
            What reaching this tier requires. **`pointsToNextTier` on the position is this minus
            the guest's lifetime points**, and until now it was this minus nothing.
        retainLifetimePoints:
          type: integer
          nullable: true
          description: >
            What keeping it requires, per review period. **Usually lower than reaching it**, and
            a scheme that cannot express the difference either never demotes or demotes on the
            day a guest stops earning.
        validityMonths:
          type: integer
          nullable: true
          description: Null means the tier does not lapse on its own.
        isActive:
          type: boolean
          default: true
"""

POSITION_ADD = """        tierId:
          type: string
          format: uuid
          nullable: true
          description: >
            **The tier this row's `tierCode` and `tierName` are a copy of.** Added 20 September
            with `marketing.programme_tier`: the two strings were a cache of something that did
            not exist, and a cache with no source cannot be rebuilt or audited.
"""

RULESET_ADD = """        tiers:
          type: array
          description: >
            The programme's tiers, in `rank` order. **Read with the rules because a redemption
            rule that is tier-gated is meaningless without them** — 500 points off for Gold
            members is two facts, and reviewing one without the other is how a tier nobody can
            reach acquires a benefit.
          items:
            $ref: '#/components/schemas/MarketingProgrammeTier'
"""

INSPECTION_ITEM = """    InspectionItem:
      x-ticvai-persistence: maintenance.inspection_item
      type: object
      description: >
        **One answer to one question, which the API has always accepted and never stored.**
        `SubmitInspectionRequest.responses[]` takes a key, a value, a pass flag, a note and
        attachments; the only persistence ever claimed for them was
        `maintenance.inspection_response`, a table that does not exist.

        So `maintenance.inspection_template_item` held the questions, `maintenance.inspection`
        held `failedItemCount` and `failedSafetyCriticalCount`, and **which check failed was
        accepted over the wire and dropped** — on a record that takes an asset out of service.

        Returned on `InspectionResult`, not on `Inspection`: `listInspections` returns the
        latter in a list, and twenty item rows per inspection on a list screen is the wrong
        trade. The counts stay for exactly that reason.
      required: [id, inspectionId, itemKey]
      properties:
        id: { type: string, format: uuid }
        inspectionId: { type: string }
        templateItemId:
          type: string
          format: uuid
          nullable: true
          description: >
            **Nullable because a template changes and an inspection does not.** An answer
            recorded against an item that was later removed still has to be readable, so the key
            below is the durable record and this is the live link.
        itemKey:
          type: string
          maxLength: 120
          description: The template item's `key`, copied at submission and never updated.
        label:
          type: string
          nullable: true
          description: >
            The question as it was asked, copied at submission. **A template reworded next
            season must not silently reword last season's inspection.**
        value:
          nullable: true
          description: Whatever the item's `kind` calls for — a boolean, a number, a string.
        passed:
          type: boolean
          nullable: true
          description: Null where the item is informational rather than pass or fail.
        isSafetyCritical:
          type: boolean
          default: false
          description: >
            Copied from the template item at submission, for the same reason as `label`: it is
            what makes `failedSafetyCriticalCount` reproducible, and the template can change.
        note: { type: string, maxLength: 1000, nullable: true }
        attachmentAssetIds:
          type: array
          items: { type: string, format: uuid }
          description: >
            **A deliberate array, and the same exception as
            `workforce.sync_conflict.affectedAssignmentIds`**: evidence attached to this answer
            at the moment it was recorded. It is never queried from the other end — nobody asks
            which inspection items reference a photograph — and it must not change when an asset
            library is reorganised.
        recordedAt: { type: string, format: date-time }
"""

RESULT_ADD = """        items:
          type: array
          description: >
            **The answers, which had nowhere to live until 20 September.** A failed
            safety-critical item takes an asset out of service and `consequences` below says it
            happened; this says which check caused it.
          items: { $ref: '#/components/schemas/InspectionItem' }
"""


def main():
    apply = "--apply" in sys.argv[1:]
    out = {}

    # ---- 14 ------------------------------------------------------------------
    c = io.open(CRM, encoding="utf-8").read()
    if "MarketingProgrammeTier" in c:
        print("    marketing-crm.yaml already has the tier")
    else:
        j = c.find("\n  schemas:\n")
        k = j + len("\n  schemas:\n")
        c = c[:k] + TIER + c[k:]

        i = c.find("x-ticvai-persistence: marketing.loyalty_position\n")
        if i < 0:
            print("    !! LoyaltyPosition schema not found")
            return 1
        anchor = c.find("        tierCode:\n", i)
        if anchor < 0:
            print("    !! tierCode anchor not found on LoyaltyPosition")
            return 1
        c = c[:anchor] + POSITION_ADD + c[anchor:]

        a2 = c.find("        redemptionRules:\n")
        if a2 < 0:
            print("    !! LoyaltyRuleSet.redemptionRules anchor not found")
            return 1
        c = c[:a2] + RULESET_ADD + c[a2:]
        print("    marketing.programme_tier  created, +LoyaltyPosition.tierId, "
              "+LoyaltyRuleSet.tiers")
    out[CRM] = c

    # ---- 15 ------------------------------------------------------------------
    m = io.open(MNT, encoding="utf-8").read()
    if "InspectionItem:" in m:
        print("    maintenance.yaml already has the inspection items")
    else:
        j = m.find("\n  schemas:\n")
        k = j + len("\n  schemas:\n")
        m = m[:k] + INSPECTION_ITEM + m[k:]

        a = m.find("        consequences:\n")
        if a < 0:
            print("    !! InspectionResult.consequences anchor not found")
            return 1
        m = m[:a] + RESULT_ADD + m[a:]

        old_tag = '      x-ticvai-persistence: "none — request only"\n'
        i = m.find("    SubmitInspectionRequest:\n")
        if i < 0 or m.find(old_tag, i) != i + len("    SubmitInspectionRequest:\n"):
            print("    !! SubmitInspectionRequest tag not where expected")
            return 1
        new_tag = ('      x-ticvai-persistence: maintenance.inspection + '
                   'maintenance.inspection_item\n'
                   '      # **It was tagged "none — request only" and it writes two tables.**\n'
                   '      # `responses[]` has always carried the per-item answers; nothing\n'
                   '      # persisted them, so the write derived from this schema named the\n'
                   '      # inspection and not the items it is made of.\n')
        m = m[:i + len("    SubmitInspectionRequest:\n")] + new_tag + \
            m[i + len("    SubmitInspectionRequest:\n") + len(old_tag):]
        print("    maintenance.inspection_item  created, +InspectionResult.items, "
              "SubmitInspectionRequest retagged")
    out[MNT] = m

    for path, s in out.items():
        try:
            doc = yaml.safe_load(s)
        except Exception as e:
            print("    !! %s would not parse: %s" % (os.path.basename(path), str(e)[:180]))
            return 1
        import re
        have = set((doc.get("components") or {}).get("schemas") or {})
        for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                                  yaml.safe_dump(doc))):
            if ref not in have:
                print("    !! %s refs %s locally and does not define it"
                      % (os.path.basename(path), ref))
                return 1
        text_n = len(re.findall(r"^      operationId:", s, re.M))
        parsed_n = sum(1 for p in (doc.get("paths") or {}).values()
                       for o in (p or {}).values()
                       if isinstance(o, dict) and o.get("operationId"))
        if text_n != parsed_n:
            print("    !! %s: %d operationId lines, %d after parsing"
                  % (os.path.basename(path), text_n, parsed_n))
            return 1
    print("    2 contract(s) parse, refs resolve, no operation discarded")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    for path, s in out.items():
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> marketing-crm.yaml, maintenance.yaml")
    print("\n  Both new tables are reached by operations that already exist — "
          "getLoyaltyRules/setLoyaltyRules and submitInspection.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
