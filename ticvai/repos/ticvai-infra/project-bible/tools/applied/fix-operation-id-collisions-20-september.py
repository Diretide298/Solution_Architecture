#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two operationIds I duplicated, and the better fix one of them points at.

Wiring loyalty and workforce introduced the first duplicate `operationId`s the package has ever
had. **Nothing checked**, and the way each was found is different from the way it should have
been found — `derive-lineage` keys on `operationId`, so a collision silently means one operation
takes the other's reads and writes. `adjustLoyaltyPoints` came back reading
`marketing.loyalty_position`, which is the *other* operation's lineage.

    adjustLoyaltyPoints   marketing-crm  POST /guests/{subjectId}/loyalty/adjust   existed
                          marketing-crm  POST /loyalty/points/adjustments          mine
    listShifts            shift          GET  /shifts                              existed
                          workforce      GET  /shifts                              mine

## The loyalty one is not a naming clash, it is the defect

The existing `adjustLoyaltyPoints` returns `LoyaltyPosition` — **the balance** — and writes
nothing else. That is exactly what decision 8 objected to: *"`marketing.loyalty_position` is a
balance with no ledger behind it. It cannot be audited or corrected."* A manual adjustment that
moves the balance and posts no entry is the clearest possible case of it.

So the second operation is removed and the existing one is corrected instead: it takes a typed
reason and an optional `reversedLoyaltyPointsId`, and returns **both** the entry it posted and
the resulting position. **Two operations that adjust points would have been worse than the bug** —
one of them would have become the one people call and the other the one nobody remembered.

## The workforce one is a real ambiguity and both names are right

`shift.yaml` is the till: `closeShift` reads `ledger.fx_rate` and reconciles a cash drawer.
`workforce.shift` is a staffing pattern — *"Early, 06:00 to 14:00"*. **Two different things
called a shift, and a venue calls both of them that.**

Renamed on the workforce side, because the spine contract holds the plain word and a staffing
pattern is the more qualified of the two:

    /shifts       -> /shift-patterns
    listShifts    -> listShiftPatterns
    setShift      -> setShiftPattern

    python3 tools/applied/fix-operation-id-collisions-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CRM = os.path.join(ROOT, "contracts", "satellite", "marketing-crm.yaml")
WF = os.path.join(ROOT, "contracts", "satellite", "workforce.yaml")

# The whole path block I added, removed again.
MY_PATH_START = "  /loyalty/points/adjustments:\n"

OLD_BODY = """      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
              - points
              - reason
              properties:
                points:
                  type: integer
                reason:
                  type: string
                  minLength: 3
                  maxLength: 500
      responses:
        '200':
          description: Adjusted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoyaltyPosition'
"""

NEW_BODY = """      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AdjustLoyaltyPointsRequest'
      responses:
        '200':
          description: Adjusted — the entry posted and the balance it produced
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoyaltyAdjustmentResult'
        '409':
          description: The entry being reversed is already reversed, or the balance would go negative
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
"""

RESULT_SCHEMA = """    LoyaltyAdjustmentResult:
      type: object
      x-ticvai-persistence: none — composed from the entry posted and the resulting position
      description: >
        **Both halves of an adjustment, because returning only the balance is the defect decision
        8 named.** Until 20 September this operation moved `marketing.loyalty_position` and
        returned it, and posted nothing to `marketing.loyalty_points` — so a manual adjustment was
        the one movement in the system that could not be walked back to a reason.
      required:
      - entry
      - position
      properties:
        entry:
          $ref: '#/components/schemas/MarketingLoyaltyPoints'
        position:
          $ref: '#/components/schemas/LoyaltyPosition'
"""


def cut_path(text, header):
    i = text.find(header)
    if i < 0:
        return text, False
    nxt = re.search(r"^  /", text[i + len(header):], re.M)
    end = i + len(header) + (nxt.start() if nxt else len(text) - i - len(header))
    return text[:i] + text[end:], True


def main():
    apply = "--apply" in sys.argv[1:]

    c = io.open(CRM, encoding="utf-8").read()
    c, cut = cut_path(c, MY_PATH_START)
    print("    /loyalty/points/adjustments   %s" % ("removed" if cut else "not present"))

    if "LoyaltyAdjustmentResult" in c:
        print("    existing adjustLoyaltyPoints  already corrected")
    else:
        if c.count(OLD_BODY) != 1:
            print("    !! existing adjustLoyaltyPoints body matched %d times" % c.count(OLD_BODY))
            return 1
        c = c.replace(OLD_BODY, NEW_BODY)
        j = c.find("\n  schemas:\n")
        k = j + len("\n  schemas:\n")
        c = c[:k] + RESULT_SCHEMA + c[k:]
        print("    existing adjustLoyaltyPoints  now posts an entry and returns both")

    # `customerId` is redundant: the surviving operation is keyed by `subjectId` in its path.
    c = c.replace("""      required:
      - customerId
      - programmeId
      - points
      - reason
      properties:
        customerId:
          type: string
          format: uuid
        programmeId:""", """      required:
      - programmeId
      - points
      - reason
      properties:
        programmeId:""")

    try:
        yaml.safe_load(c)
    except Exception as e:
        print("    !! marketing-crm.yaml would not parse: %s" % str(e)[:160])
        return 1
    print("    marketing-crm.yaml parses")

    w = io.open(WF, encoding="utf-8").read()
    renames = [("  /shifts:\n", "  /shift-patterns:\n"),
               ("operationId: listShifts\n", "operationId: listShiftPatterns\n"),
               ("operationId: setShift\n", "operationId: setShiftPattern\n")]
    for old, new in renames:
        if new in w:
            print("    %-34s already renamed" % old.strip())
            continue
        if w.count(old) != 1:
            print("    !! %r matched %d times in workforce.yaml" % (old.strip(), w.count(old)))
            return 1
        w = w.replace(old, new)
        print("    %-34s -> %s" % (old.strip(), new.strip()))
    try:
        yaml.safe_load(w)
    except Exception as e:
        print("    !! workforce.yaml would not parse: %s" % str(e)[:160])
        return 1
    print("    workforce.yaml parses")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(CRM, "w", encoding="utf-8", newline="\n").write(c)
    io.open(WF, "w", encoding="utf-8", newline="\n").write(w)
    print("  -> marketing-crm.yaml, workforce.yaml")
    print("\n  Remove the stale lineage entries for the operationIds that no longer exist:")
    print("    python3 tools/derive-lineage.py --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
