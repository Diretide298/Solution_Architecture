#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BL-100: dunning, a retry schedule and a billing statement — and the boundary they settle.

**The entry named eight capabilities and five arrived without it noticing.** Auto-renewal, grace
periods, billing cycles, downgrade and mandates all exist. **Three did not appear anywhere in
`contracts/`**: dunning, a retry schedule, and a billing statement. `grep` finds no `dunning`
outside a state model — CF-49's exact shape, a capability present only in states.

## The boundary, decided

The entry's own argument was overtaken: it said *"`subscription` looks like the answer and is not
— it is the Control Plane"*, and then `setRenewalAutoMembership` and sixteen other membership
operations turned up **in `subscription.yaml`**. All seventeen are `x-ticvai-provisional`, read off
a workshop pack and never specified.

**Decided by Chinmay, 21 September: guest billing goes where the rest of the billing is.**

    payments.yaml     the policy -- dunning, retry spacing, what happens at the end
    orders.yaml       the record -- a statement of what was charged, guest-facing

**The seventeen provisional drafts are not moved by this script.** They are unreviewed workshop
text awaiting one of the seven sessions, and relocating seventeen operations nobody has agreed
would assert a home rather than record one. **The decision is written down so the session that
reads them knows where they land.**

## The three things worth arguing about

**1 · Dunning retry is not gateway retry, and conflating them charges a guest twice.**
`setPaymentFailoverPolicy` already governs retry *inside* one attempt — a timeout or a 5xx moves
to the next provider in seconds, and **a decline is final there**. Dunning is the opposite axis:
days later, a fresh authorisation, the same guest. Both are called "retry" and they must never
share a counter.

**2 · A hard decline must never be retried, and that is a merchant-account risk rather than a
courtesy.** A closed account, a stolen card or a "do not honour" retried on a schedule is how a
merchant ID gets flagged by the scheme. `DeclineClass` splits `soft` from `hard`, and the hard set
exits dunning immediately and asks the guest for a different card.

**3 · Dunning must not revoke admission on its own.** `graceDays` already exists on the renewal
model, and the failure this prevents is concrete: **a guest at a gate on a family day out, refused
because a card expired and a retry ran at 3am.** `terminalAction` tops out at `suspendBilling`, and
**revoking entry stays a staff decision with a person's name on it.**

**A statement is not a tax invoice.** `isTaxInvoice` is `false` and read-only. UAE e-invoicing is
Peppol five-corner with the FTA as the fifth, PINT AE XML and 51 mandatory fields — **CF-133, and
AED 50m+ businesses must appoint an accredited service provider by 30 October 2026.** A statement
that implied it was a tax invoice would be wrong in the one direction that has a regulator at the
end of it.

    python3 tools/applied/bl-100-dunning-retry-statements-21-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAY = os.path.join(ROOT, "contracts", "satellite", "payments.yaml")
ORD = os.path.join(ROOT, "contracts", "spine", "orders.yaml")

PAY_PATH_ANCHOR = "  /payment-methods:\n"

PAY_PATHS = """  /dunning-policy:
    get:
      operationId: getDunningPolicy
      x-ticvai-consumed-by:
        - "P09 ADM-575 Failover, Retry & Resilience Manager\\t34"
      summary: How a failed recurring charge is chased
      description: '2.14.19-2.14.23, BL-100. **Recurring guest billing had auto-renewal and no
        answer for the renewal that fails**, which is the case that actually happens.

        '
      tags:
      - payments
      x-ticvai-permission: PAYMENT_CONFIGURE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: primary
      responses:
        '200':
          description: Policy
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DunningPolicy'
    put:
      operationId: setDunningPolicy
      x-ticvai-consumed-by:
        - "P09 ADM-575 Failover, Retry & Resilience Manager\\t34"
      summary: Set the retry schedule and what happens when it runs out
      description: '2.14.19-2.14.23, BL-100. **Dunning retry and gateway retry are different axes
        and must never share a counter.** `setPaymentFailoverPolicy` governs retry *inside* one
        attempt — a timeout or a 5xx moves to the next provider within seconds, and a decline is
        final there. This governs retry *across days*: a fresh authorisation, the same guest, a
        card that may since have been replaced. **Both are called retry, and treating a dunning
        attempt as a failover attempt is how a guest is charged twice.**

        **A hard decline exits immediately and is never scheduled.** A closed account, a stolen
        card or a do-not-honour retried on a timetable is how a merchant ID gets flagged by the
        scheme — so the classification is explicit rather than "anything that was not a success".

        **Dunning cannot revoke admission.** `terminalAction` tops out at `suspendBilling`, and
        the reason is a person rather than a principle: a guest at a gate on a family day out,
        refused because a card expired and a retry ran at 3am. Ending someone''s access stays a
        staff decision with a name attached to it.

        '
      tags:
      - payments
      x-ticvai-permission: PAYMENT_CONFIGURE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-config-scope: tenant
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DunningPolicy'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DunningPolicy'
        '422':
          description: '**An attempt schedule that would breach the policy''s own guard** — more
            attempts than `maxAttempts`, two attempts inside `minimumHoursBetweenAttempts`, or a
            `terminalAction` the caller is not permitted to set.

            '
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /dunning-cases:
    get:
      operationId: listDunningCases
      x-ticvai-consumed-by:
        - "P09 ADM-575 Failover, Retry & Resilience Manager\\t34"
      summary: Recurring charges currently being chased
      description: '2.14.19-2.14.23, BL-100. **The work queue, and the number a venue actually
        manages by.** A dunning policy with no view of what it is doing is a schedule running in
        the dark.

        **Ordered by attempts remaining rather than by age**, because the ones about to exhaust
        are the ones somebody can still save by calling the guest.

        '
      tags:
      - payments
      x-ticvai-permission: PAYMENT_CONFIGURE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: replica
      parameters:
      - name: state
        in: query
        schema:
          $ref: '#/components/schemas/DunningState'
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Cases
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/DunningCase'
  /dunning-cases/{caseId}/resolve:
    post:
      operationId: resolveDunningCase
      x-ticvai-consumed-by:
        - "P09 ADM-575 Failover, Retry & Resilience Manager\\t34"
      summary: Stop chasing, with a reason
      description: 'BL-100. **The manual exit, and it is an operation rather than a status edit
        because somebody has to own it.** A guest who paid at a counter, a card replaced over the
        phone, or a venue writing the balance off — three different reasons that must be told
        apart afterwards.

        **`writeOff` does not erase the case**, which is why this is not a delete: a dunning case
        that vanishes leaves the finance side unable to say what happened to the money.

        '
      tags:
      - payments
      x-ticvai-permission: PAYMENT_CONFIGURE
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      parameters:
      - name: caseId
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
              type: object
              required:
              - resolution
              properties:
                resolution:
                  type: string
                  enum:
                  - paidByOtherMeans
                  - cardReplaced
                  - writeOff
                  - cancelledByGuest
                note:
                  type: string
                  maxLength: 500
      responses:
        '200':
          description: Resolved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DunningCase'
"""

PAY_SCHEMA_ANCHOR = "components:\n  schemas:\n"

PAY_SCHEMAS = """components:
  schemas:
    DeclineClass:
      type: string
      description: >
        BL-100. **Whether a failed charge may be tried again at all**, and the distinction is a
        merchant-account risk rather than a courtesy.

        `soft` — insufficient funds, a temporary hold, an issuer timeout. **Worth another attempt
        on another day**, and the whole reason a dunning schedule exists.

        `hard` — closed account, stolen card, do-not-honour, invalid number. **Never retried.** A
        hard decline put on a timetable is how a merchant ID gets flagged by the scheme, and the
        venue finds out when its acquirer calls.

        `unknown` — the provider gave no usable code. **Treated as `hard`**, because guessing
        `soft` optimises for one more attempt and risks the thing that cannot be undone.
      enum:
      - soft
      - hard
      - unknown

    DunningState:
      type: string
      enum:
      - scheduled
      - inProgress
      - exhausted
      - recovered
      - resolvedManually
      description: >
        BL-100. **`exhausted` and `recovered` are both endings and only one of them is a
        failure.** A schedule with a single terminal state cannot tell a venue whether dunning is
        working, which is the only question a venue asks of it.

    DunningPolicy:
      x-ticvai-persistence: payments.dunning_policy
      type: object
      description: >
        2.14.19-2.14.23, BL-100. **How a failed recurring charge is chased, as a tenant policy
        rather than a platform constant.** A season pass at AED 300 a month and a locker
        subscription at AED 15 do not deserve the same number of attempts.
      required:
      - maxAttempts
      - terminalAction
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        maxAttempts:
          type: integer
          minimum: 1
          maximum: 8
          default: 4
          description: >
            **Capped at eight and defaulted to four.** The ceiling is not arbitrary: past a
            handful of attempts the recovery rate is close to nothing and the cost is a guest
            watching their bank app light up repeatedly for a charge they already know failed.
        attemptOffsetDays:
          type: array
          items:
            type: integer
            minimum: 0
          default: [0, 3, 7, 14]
          description: >
            **Days after the first failure, and the spacing is the part that matters.** Retrying
            at the same hour each day hits the same daily limit on the same card and tells the
            venue nothing it did not already know — **attempts spaced across the month straddle a
            payday**, which is the single thing that changes the answer for a soft decline.

            **Must be non-decreasing and no longer than `maxAttempts`**, enforced with 422 rather
            than by silently truncating a list somebody meant.
        minimumHoursBetweenAttempts:
          type: integer
          default: 24
          description: >
            **A floor under the offsets, because a schedule is edited by hand.** Two offsets on
            the same day are a typo that reads as a policy.
        retryableDeclineClasses:
          type: array
          items:
            $ref: '#/components/schemas/DeclineClass'
          default: [soft]
          description: >
            **`soft` alone, and widening it is a deliberate act.** The field exists rather than
            being implied so that a venue that adds `unknown` has chosen to, and so an auditor can
            see that it did.
        notifyGuestOnEachAttempt:
          type: boolean
          default: false
          description: >
            **False by default.** A guest told four times about one failed renewal reads it as
            four failures. The first and the last are the ones that mean something — the first
            because they can fix it, the last because their pass is about to change.
        terminalAction:
          type: string
          enum:
          - suspendBilling
          - cancelRenewal
          default: suspendBilling
          description: >
            **What happens when the attempts run out, and it deliberately stops short of
            admission.** `suspendBilling` stops charging and leaves the entitlement as it is;
            `cancelRenewal` also stops the next term. **Neither revokes entry.**

            `graceDays` on the renewal model already governs how long a pass keeps working, and
            the failure this separation prevents is concrete: **a guest at a gate on a family day
            out, refused because a card expired and a retry ran at 3am.** Ending somebody's access
            stays a staff decision with a name on it.
        scopePath:
          type: string
          description: >
            **The partition key** (ADR-0005). Written at `tenant` scope.

    DunningCase:
      x-ticvai-persistence: payments.dunning_case
      type: object
      description: >
        BL-100. **One recurring charge being chased**, and the row a venue works from.
      required:
      - id
      - state
      - attemptsMade
      - firstFailedAt
      properties:
        id:
          type: string
          format: uuid
        subjectId:
          type: string
          format: uuid
        orderId:
          type: string
          description: The order whose renewal failed.
        amount:
          $ref: ../shared/common.yaml#/components/schemas/Money
        state:
          $ref: '#/components/schemas/DunningState'
        declineClass:
          allOf:
          - $ref: '#/components/schemas/DeclineClass'
          description: >
            **From the most recent attempt.** A case that begins `soft` and turns `hard` stops
            immediately rather than finishing its schedule — the card changed underneath it.
        attemptsMade:
          type: integer
        nextAttemptAt:
          type: string
          format: date-time
          nullable: true
          description: >
            **Null where the case has ended or the decline is hard.** A scheduled time on a case
            nothing will act on is the field that makes a queue untrustworthy.
        firstFailedAt:
          type: string
          format: date-time
        resolvedAt:
          type: string
          format: date-time
          nullable: true
        resolution:
          type: string
          nullable: true
          enum:
          - paidByOtherMeans
          - cardReplaced
          - writeOff
          - cancelledByGuest
          - null
        scopePath:
          type: string
          description: >
            **The partition key** (ADR-0005). Written at `venue` scope.

"""

ORD_PATH_ANCHOR = "  /orders:\n"

ORD_PATHS = """  /billing-statements:
    get:
      operationId: listBillingStatements
      x-ticvai-consumed-by:
        - "P01 WEB-018 My Tickets"
        - "P02 GST-012 My Tickets"
      x-ticvai-audience:
      - guest
      - staff
      summary: What was charged, when, and against which agreement
      description: '2.14.19-2.14.23, 5.7.96, BL-100. **A guest paying monthly could see their
        pass and not what they had been charged for it.** Auto-renewal, grace and mandates all
        existed; the record a guest reads was the piece missing.

        **A statement is not a tax invoice.** `isTaxInvoice` is false and read-only. UAE
        e-invoicing is Peppol five-corner with the FTA as the fifth corner, PINT AE XML and 51
        mandatory fields, and **CF-133 is open on it** — a statement that implied otherwise would
        be wrong in the one direction with a regulator at the end of it.

        **A guest sees their own and nothing else** (`x-ticvai-self-scoped: subject`); supplying
        another subject is 403 rather than silently honoured.

        '
      tags:
      - orders
      x-ticvai-permission: null
      x-ticvai-self-scoped: subject
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      security:
      - guestAuth: []
      - bearerAuth: []
      parameters:
      - name: from
        in: query
        schema:
          type: string
          format: date
      - name: to
        in: query
        schema:
          type: string
          format: date
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Statements
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/BillingStatement'
  /billing-statements/{statementId}:
    get:
      operationId: getBillingStatement
      x-ticvai-consumed-by:
        - "P01 WEB-018 My Tickets"
        - "P02 GST-012 My Tickets"
      x-ticvai-audience:
      - guest
      - staff
      summary: One statement, with its lines
      description: 'BL-100. **The lines are the point.** A total with no breakdown is what a guest
        rings a call centre about, and the call centre has no more than they do.

        **A failed attempt appears as a line.** A statement that shows only successful charges
        cannot explain why a pass lapsed, which is the question somebody is reading it to answer.

        '
      tags:
      - orders
      x-ticvai-permission: null
      x-ticvai-self-scoped: subject
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      security:
      - guestAuth: []
      - bearerAuth: []
      parameters:
      - name: statementId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      responses:
        '200':
          description: Statement
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BillingStatement'
"""

ORD_SCHEMA_ANCHOR = "    TenderKind:\n"

ORD_SCHEMAS = """    BillingStatementLine:
      type: object
      description: >
        BL-100. **One charge, refund or failed attempt.** Failures are lines rather than omissions
        — a statement showing only what succeeded cannot explain why a pass lapsed.
      required:
      - occurredAt
      - kind
      - amount
      properties:
        occurredAt:
          type: string
          format: date-time
        kind:
          type: string
          enum:
          - charge
          - refund
          - failedAttempt
          - adjustment
        amount:
          $ref: ../shared/common.yaml#/components/schemas/Money
        description:
          type: string
        declineClass:
          type: string
          nullable: true
          description: >
            **Present on `failedAttempt` only**, and it is what turns *"your payment failed"* into
            something a guest can act on: a soft decline means try again, a hard one means the
            card needs replacing.

    BillingStatement:
      x-ticvai-persistence: none — computed from orders.order_payment and payments.dunning_case
      type: object
      description: >
        2.14.19-2.14.23, 5.7.96, BL-100. **What a guest was charged over a period, and
        deliberately not a tax document.**

        **Computed rather than stored**, because a statement assembled at read time cannot
        disagree with the ledger it describes. A stored statement is a second source of truth
        about money, and the package already has one of those.
      required:
      - id
      - periodStart
      - periodEnd
      - total
      - isTaxInvoice
      properties:
        id:
          type: string
          format: uuid
        subjectId:
          type: string
          format: uuid
          readOnly: true
        periodStart:
          type: string
          format: date
        periodEnd:
          type: string
          format: date
        lines:
          type: array
          items:
            $ref: '#/components/schemas/BillingStatementLine'
        total:
          $ref: ../shared/common.yaml#/components/schemas/Money
        isTaxInvoice:
          type: boolean
          default: false
          readOnly: true
          description: >
            **Always false, and stated rather than assumed.** UAE e-invoicing is Peppol
            five-corner with the FTA as the fifth corner, PINT AE XML and 51 mandatory fields;
            **CF-133 is open on it and AED 50m+ businesses must appoint an accredited service
            provider by 30 October 2026.** A statement that implied it was a tax invoice would be
            wrong in the one direction that has a regulator at the end of it.

"""


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
    print("    %-14s parses, refs resolve, %d operations" % (label, parsed_n))
    return doc


def sub(s, old, new, label):
    if s.count(old) != 1:
        print("  !! %s matched %d times" % (label, s.count(old)))
        return None
    print("    %s" % label)
    return s.replace(old, new, 1)


def main():
    apply = "--apply" in sys.argv[1:]
    p = io.open(PAY, encoding="utf-8").read()
    o = io.open(ORD, encoding="utf-8").read()

    if "DunningPolicy:" in p and "BillingStatement:" in o:
        print("  already applied")
        return 0

    print("  payments.yaml — the policy")
    p = sub(p, PAY_PATH_ANCHOR, PAY_PATHS + PAY_PATH_ANCHOR,
            "+getDunningPolicy, +setDunningPolicy, +listDunningCases, +resolveDunningCase")
    if p is None:
        return 1
    p = sub(p, PAY_SCHEMA_ANCHOR, PAY_SCHEMAS,
            "+DeclineClass, +DunningState, +DunningPolicy, +DunningCase")
    if p is None:
        return 1

    print("  orders.yaml — the record")
    o = sub(o, ORD_PATH_ANCHOR, ORD_PATHS + ORD_PATH_ANCHOR,
            "+listBillingStatements, +getBillingStatement")
    if o is None:
        return 1
    o = sub(o, ORD_SCHEMA_ANCHOR, ORD_SCHEMAS + ORD_SCHEMA_ANCHOR,
            "+BillingStatementLine, +BillingStatement")
    if o is None:
        return 1

    dp = check(PAY, p, "payments.yaml")
    do = check(ORD, o, "orders.yaml")
    if dp is None or do is None:
        return 1

    pol = dp["components"]["schemas"]["DunningPolicy"]["properties"]
    if "revokeAccess" in pol or "revokeEntitlement" in pol["terminalAction"].get("enum", []):
        print("  !! dunning can revoke admission")
        return 1
    if pol["terminalAction"]["enum"] != ["suspendBilling", "cancelRenewal"]:
        print("  !! terminalAction is %s" % pol["terminalAction"]["enum"])
        return 1
    print("    terminalAction stops at billing: %s" % ", ".join(pol["terminalAction"]["enum"]))

    if dp["components"]["schemas"]["DunningPolicy"]["properties"][
            "retryableDeclineClasses"]["default"] != ["soft"]:
        print("  !! hard declines are retryable by default")
        return 1
    print("    only soft declines retry by default")

    st = do["components"]["schemas"]["BillingStatement"]
    if st["properties"]["isTaxInvoice"].get("default") is not False:
        print("  !! a statement claims to be a tax invoice")
        return 1
    if not str(st.get("x-ticvai-persistence", "")).startswith("none"):
        print("  !! BillingStatement is stored — a second source of truth about money")
        return 1
    print("    BillingStatement  computed, isTaxInvoice false (CF-133 stays open)")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PAY, "w", encoding="utf-8", newline="\n").write(p)
    io.open(ORD, "w", encoding="utf-8", newline="\n").write(o)
    print("  -> contracts/satellite/payments.yaml, contracts/spine/orders.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
