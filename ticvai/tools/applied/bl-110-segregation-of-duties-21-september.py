#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BL-110: both things the walk left are already built. Three smaller holes are not.

**The 20 September walk left BL-110 as "one schema change and one small new rule". Both are
done.**

    the schema change    AccessPolicy + AccessCondition, 26 attributes covering 3.3.2
                         through 3.3.21, deny-wins, versions, templates, simulation and
                         a signed offline bundle -- landed in "Phase 2: the forty-two
                         identity rows were one gap, and it was ABAC"
    the new rule         SegregationRule + setSegregationRules, built by BL-147,
                         checked at grant time, with allowWithCompensatingControl

**That is the fifth stale measurement in two days**, and this one was mine: I searched for
`segregat` across `contracts/`, piped it through `head -10`, saw `approvals`, `access`, `workforce`
and `permissions` and concluded identity had none. **The identity rows were on lines 11 through
14 of a list I had truncated to 10.** It is the same failure as concluding no operation retires a
device because no operationId contains *retire*.

## What is genuinely missing, which is smaller and real

**1 · `setSegregationRules` is a PUT with no GET.** `P09 ADM-340 Segregation of Duties Policy
Manager` is a screen that manages rules **and has nothing to load them with**. A tenant cannot read
back its own controls, which also means nobody can audit them without database access.

**2 · Nothing lists who currently violates a rule.** The check runs at grant time, which BL-147
argued well — *"discovering the conflict when somebody exercises it means the conflict already
existed"*. But **a rule added today has said nothing about the grants made yesterday.** Turning one
on polices the future and leaves the actual exposure invisible: the venue has the control and not
the finding.

**3 · Scope is not part of the conflict, and `scopePath` is not it.** `scopePath` on the rule is
the partition key — where the rule row lives (ADR-0005). It does not say where the *conflict*
applies. So `ACCREDITATION_ISSUE` at Yas Island beside `ACCREDITATION_MANAGE` at Warner Bros reads
as a toxic pair when it is two jobs at two sites, and the first thing a venue does with a control
that cries wolf is switch it off.

**`allowWithCompensatingControl` already covers the exception case** and covers it better than a
separate exception object would — *"a named compensating control is better than no rule"*. Not
rebuilt.

    python3 tools/applied/bl-110-segregation-of-duties-21-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDN = os.path.join(ROOT, "contracts", "spine", "identity.yaml")
APR = os.path.join(ROOT, "contracts", "spine", "approvals.yaml")

# --- 1 · the GET the screen has no way to call ------------------------------------------------

GET_ANCHOR = """  /segregation-rules:
    put:
      operationId: setSegregationRules
"""

GET_OP = """  /segregation-rules:
    get:
      operationId: listSegregationRules
      x-ticvai-consumed-by:
        - "P09 ADM-340 Segregation of Duties Policy Manager"
      summary: Read the conflicting-permission rules back
      description: 'BL-110, 3.3.31. **`setSegregationRules` was a PUT with no GET**, so the screen
        named above manages rules it cannot load — and nobody could audit a tenant''s controls
        without reaching the database.

        **Rules are evidence as much as configuration.** An auditor asking *"what does this venue
        forbid"* is asking a question the platform should answer without a query.

        '
      tags:
      - identity
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Rules
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SegregationRule'
    put:
      operationId: setSegregationRules
"""

# --- 2 · what the rule finds when it is turned on ---------------------------------------------

VIOL_ANCHOR = "  /guests/{subjectId}/data-export:\n"

VIOL_OP = """  /segregation-violations:
    get:
      operationId: listSegregationViolations
      x-ticvai-consumed-by:
        - "P09 ADM-340 Segregation of Duties Policy Manager"
        - "P09 ADM-339 Governance & Compliance Command Center"
      summary: Who already holds a conflicting pair
      description: 'BL-110, 3.3.31, 3.3.38. **The check runs at grant time, and a rule added today
        has said nothing about the grants made yesterday.** BL-147 was right that catching a
        conflict at use time catches it too late — but a rule that only polices future grants
        leaves the venue holding the control and not the finding.

        **This is deliberately a report and not an action.** The two automatic answers are both
        wrong: revoking on rule creation strands a venue mid-shift, and doing nothing leaves real
        exposure unreported. **A person decides, and this is what they read.**

        **Violations covered by `allowWithCompensatingControl` are flagged rather than filtered.**
        A queue that hides what has been excused stops measuring the thing it exists to measure.

        '
      tags:
      - identity
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: ruleId
        in: query
        schema:
          type: string
          format: uuid
      - name: severity
        in: query
        schema:
          type: string
          enum: [block, requireApproval, warn]
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Violations
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SegregationViolation'
"""

# --- 3 · scope, which scopePath is not ---------------------------------------------------------

SCOPE_OLD = """        allowWithCompensatingControl:
          type: boolean
          default: false
"""

SCOPE_NEW = """        scopeSensitive:
          type: boolean
          default: true
          description: '**Whether the two permissions must overlap in scope to conflict**, and this
            is not `scopePath` below — that one is the partition key and says where the rule *row*
            lives (ADR-0005), not where the *conflict* applies.

            **True, and it should rarely be false.** `ACCREDITATION_ISSUE` at Yas Island beside
            `ACCREDITATION_MANAGE` at Warner Bros is two jobs at two sites; flagging it is a
            control crying wolf, and the first thing a venue does with one of those is switch it
            off. The comparison walks `scopePath` prefixes the same way `resolvePermissions`
            already does — `uae.dubai` contains `uae.dubai.marina`, so one is an overlap and two
            siblings are not.

            **False is for conflicts that are genuinely estate-wide**, such as holding both sides
            of a financial reconciliation anywhere at all.

            '
        allowWithCompensatingControl:
          type: boolean
          default: false
"""

VIOL_SCHEMA_ANCHOR = "    SegregationRule:\n      type: object\n"

VIOL_SCHEMA = """    SegregationViolation:
      type: object
      x-ticvai-persistence: none — computed from identity.grant against identity.segregation_rule
      description: 'BL-110, 3.3.31, 3.3.38. **One principal currently holding both halves of a
        rule.**

        **Computed rather than stored.** A violation row that survived the grant behind it would be
        a queue item nobody could close, and a compliance queue that cannot reach zero is one
        people stop opening.

        '
      required:
      - ruleId
      - principalId
      - permissionA
      - permissionB
      properties:
        ruleId:
          type: string
          format: uuid
        ruleName:
          type: string
        severity:
          type: string
          enum:
          - block
          - requireApproval
          - warn
          description: '**From the rule.** A `warn` violation and a `block` violation are the same
            finding with very different urgency, and a queue that does not carry it sorts by
            nothing useful.

            '
        principalId:
          type: string
          format: uuid
        principalName:
          type: string
        permissionA:
          type: string
        permissionB:
          type: string
        atScopePath:
          type: string
          description: '**Where the two overlap**, and the field that makes a finding actionable:
            the answer is usually to narrow one grant rather than to remove it.

            **Null where the rule is not `scopeSensitive`**, which is the estate-wide case.

            '
        compensatingControlNoted:
          type: boolean
          default: false
          description: '**True where `allowWithCompensatingControl` covers this one.** Flagged
            rather than filtered out — a small venue that cannot separate duties is a fact somebody
            accepted, and it should stay visible rather than disappearing from the count.

            '
        detectedAt:
          type: string
          format: date-time

"""

APR_OLD = """      description: 'Approvals boards 4.8, 6.2 and 6.3. **`identity.setSegregationRules` says which roles
        one person may not hold at once. This says which *decisions* one person may not take alone**, and
        they are different controls that get conflated."""

APR_NEW = """      description: 'Approvals boards 4.8, 6.2 and 6.3. **`identity.setSegregationRules` says which
        permissions one person may not hold at once. This says which *decisions* one person may not take
        alone**, and they are different controls that get conflated.

        **Corrected 21 September, from "roles" to "permissions".** The operation exists and has always
        been over permission pairs; the description here described a model that was never built. A rule
        over roles would be defeated by editing a role — add `ORDER_REFUND_APPROVE` to a third role and
        the conflict reappears while the rule still reports compliant."""


def check(path, s, label):
    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! %s would not parse: %s" % (label, str(e)[:220]))
        return None
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("  !! %s refs %s and does not define it" % (label, ref))
            return None
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %s: %d operationId lines, %d parsed" % (label, text_n, parsed_n))
        return None
    print("    %-15s parses, refs resolve, %d operations" % (label, parsed_n))
    return doc


def sub(s, old, new, label):
    if s.count(old) != 1:
        print("  !! %s matched %d times" % (label, s.count(old)))
        return None
    print("    %s" % label)
    return s.replace(old, new, 1)


def main():
    apply = "--apply" in sys.argv[1:]
    i = io.open(IDN, encoding="utf-8").read()
    p = io.open(APR, encoding="utf-8").read()

    if "listSegregationViolations" in i:
        print("  already applied")
        return 0

    # What BL-147 already built, asserted rather than assumed a second time.
    for need in ("operationId: setSegregationRules", "    SegregationRule:"):
        if need not in i:
            print("  !! expected BL-147's %r and it is not there" % need)
            return 1
    print("    BL-147's rule confirmed present — this adds the read, the report and the scope")

    i = sub(i, GET_ANCHOR, GET_OP, "+listSegregationRules (the PUT had no GET)")
    if i is None:
        return 1
    i = sub(i, VIOL_ANCHOR, VIOL_OP + VIOL_ANCHOR, "+listSegregationViolations")
    if i is None:
        return 1
    i = sub(i, SCOPE_OLD, SCOPE_NEW, "SegregationRule  +scopeSensitive")
    if i is None:
        return 1
    i = sub(i, VIOL_SCHEMA_ANCHOR, VIOL_SCHEMA + VIOL_SCHEMA_ANCHOR, "+SegregationViolation")
    if i is None:
        return 1

    p = sub(p, APR_OLD, APR_NEW, "approvals.yaml  roles -> permissions, which is what was built")
    if p is None:
        return 1

    di = check(IDN, i, "identity.yaml")
    dp = check(APR, p, "approvals.yaml")
    if di is None or dp is None:
        return 1

    ops = {o["operationId"] for pp in (di.get("paths") or {}).values()
           for o in (pp or {}).values() if isinstance(o, dict) and o.get("operationId")}
    for need in ("listSegregationRules", "setSegregationRules", "listSegregationViolations"):
        if need not in ops:
            print("  !! %s missing" % need)
            return 1
    print("    /segregation-rules now reads and writes · violations are reportable")

    r = di["components"]["schemas"]["SegregationRule"]["properties"]
    if r["scopeSensitive"].get("default") is not True:
        print("  !! scopeSensitive does not default to true — two sites would read as a conflict")
        return 1
    if "allowWithCompensatingControl" not in r:
        print("  !! BL-147's compensating control was lost")
        return 1
    v = di["components"]["schemas"]["SegregationViolation"]
    if not str(v.get("x-ticvai-persistence", "")).startswith("none"):
        print("  !! violations are stored — one would outlive the grant behind it")
        return 1
    print("    scope-sensitive by default · compensating control intact · violations computed")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(IDN, "w", encoding="utf-8", newline="\n").write(i)
    io.open(APR, "w", encoding="utf-8", newline="\n").write(p)
    print("  -> contracts/spine/identity.yaml, contracts/spine/approvals.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
