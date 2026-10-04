#!/usr/bin/env python3
"""The contracts half of the Sprint 1-2 fix round (4 October 2026, CHG-FXC-003 to CHG-FXC-009).

**Found by the judge of 4 October** (`audit/ticvai/runs/fix-s12/contracts.tsv`: 141 tickets, 38 not buildable): a
developer pulling a Sprint 1 or 2 ticket met a field with nowhere to be stored, a table the behaviour needs that its
lineage did not list, or a rule the contract named and never gave. The generators were fixed where a generator made
the gap (CHG-FXC-001 resolution-cache keys, CHG-FXC-002 a 201 writes what it creates, both in derive-lineage and
check-write-lineage); this one-off gives the existing authored files their answers:

* storage (CHG-FXC-003): a column or a child table for every field the judged operations store, read off the same
  `x-ticvai-persistence` and property rules `derive-schema` uses, so the DDL and its forward migration follow at the
  refresh;
* lineage (CHG-FXC-004): the tables each judged operation's own description says it reads or writes;
* drafted composites (CHG-FXC-005): where a drafted workspace input lands, field by field;
* decisions taken with a default (CHG-FXC-006 to -009): game-card loads, an invitation's entitlement, the shift swap's
  approval kind, the fiscal close checks, deep-link patterns, the PINT AE mapping, the rotating location code.

Contracts are edited as text (tools/applied/yamltext.py), never round-tripped, and each file must still parse.

    python tools/applied/contracts-s12-4-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import yamltext as Y  # noqa: E402

C = lambda rel: os.path.join(ROOT, "contracts", rel)  # noqa: E731
FNB, WAL, WL, APR = C("satellite/fnb.yaml"), C("satellite/wallet.yaml"), C("satellite/white-label.yaml"), C("spine/approvals.yaml")
CAT, ACC, FIN, IDN = C("spine/catalogue.yaml"), C("spine/access.yaml"), C("spine/finance.yaml"), C("spine/identity.yaml")
SUB, PUB, TRN, RES = C("satellite/subscription.yaml"), C("satellite/public-api.yaml"), C("satellite/transport.yaml"), C("satellite/resources.yaml")
GAM, INV, PRO, ORD = C("satellite/games.yaml"), C("satellite/inventory.yaml"), C("satellite/promotions.yaml"), C("spine/orders.yaml")
WRK, MKT, TEN, QUE = C("satellite/workforce.yaml"), C("satellite/marketing-crm.yaml"), C("spine/tenancy.yaml"), C("satellite/queue.yaml")

EDITS = []  # (callable, args) applied in order


def E(fn, *args):
    EDITS.append((fn, args))


# ── CHG-FXC-003: storage for what the operations store ─────────────────────────────────────────────────────────
JSONB = "x-ticvai-persistence-column: jsonb"

E(Y.add_props, FNB, "Recipe", """
id:
  type: string
  format: uuid
  readOnly: true
  description: '**The recipe''s own id** (4 October 2026, CHG-FXC-003; the Sprint 1-2 judging found no operation
    returned one, so `listIngredientSubstitutes`, `setIngredientSubstitutes` and `SubstitutionRule.recipeId` had
    nothing to send). One recipe per menu item: `setRecipe` upserts on `menuItemId` and returns the id it kept.'
""")
E(Y.add_props, FNB, "FnbIngredientSubstitute", """
recipeId:
  type: string
  format: uuid
  readOnly: true
  description: '**The recipe this substitute belongs to** (4 October 2026, CHG-FXC-003): the `{recipeId}` of
    `listIngredientSubstitutes` and `setIngredientSubstitutes`, stored on every row so the list filters by it and the
    set replaces exactly that recipe''s rows. Taken from the path, never from the body.'
""")
E(Y.replace_in_schema, FNB, "AllergenVerdict", "        undeclared:\n          type: array\n",
  "        undeclared:\n          type: array\n          " + JSONB + "\n")
E(Y.replace_in_schema, FNB, "ComboSlot", "x-ticvai-persistence: fnb.combo_slot\n",
  "x-ticvai-persistence: fnb.combo_slot + fnb.combo_slot_option\n")
E(Y.replace_in_schema, IDN, "AuthorisationPolicy", "        conditions:\n          type: array\n",
  "        conditions:\n          type: array\n          " + JSONB + "\n")
for prop in ("fieldMappings", "currencyMappings", "statusMappings", "creditTypeMappings"):
    E(Y.replace_in_schema, WAL, "WalletIntegrationMapping", "        %s:\n          type: array\n" % prop,
      "        %s:\n          type: array\n          %s\n" % (prop, JSONB))
E(Y.replace_in_schema, WAL, "WalletRiskRules", "x-ticvai-persistence: wallet.risk_rules\n",
  "x-ticvai-persistence: wallet.risk_rules + wallet.risk_rule\n")
E(Y.replace_in_schema, WL, "NavigationConfig", "x-ticvai-persistence: whitelabel.navigation_item\n",
  "x-ticvai-persistence: whitelabel.navigation_config + whitelabel.navigation_item\n")
E(Y.replace_in_schema, WL, "HomepageLayout", "x-ticvai-persistence: whitelabel.homepage_section\n",
  "x-ticvai-persistence: whitelabel.homepage_layout + whitelabel.homepage_section\n")

E(Y.add_props, CAT, "Event", """
lifecycleState:
  type: string
  readOnly: true
  enum:
  - draft
  - planned
  - onSale
  - live
  - closed
  - cancelled
  - archived
  description: '**Where the event is in its lifecycle** (4 October 2026, CHG-FXC-003; catalogue.event had nowhere to
    keep it). Written only by `setEventLifecycleState`, which checks the transition; `createEvent` and `cloneEvent`
    create an event in `draft`. `isActive` stays the switch that hides an event from sale without changing its state.'
lifecycleStateChangedAt:
  type: string
  format: date-time
  readOnly: true
  nullable: true
""")
E(Y.add_props, FIN, "InterEntityObligation", """
agreedAmount:
  allOf:
  - $ref: ../shared/common.yaml#/components/schemas/Money
  nullable: true
  readOnly: true
  description: '**The figure a dispute was resolved at** (4 October 2026, CHG-FXC-003): written by
    `resolveObligationDispute`, which returns the obligation to `outstanding`. `arisingAmount` keeps the original, so
    the difference stays auditable; settlement settles `agreedAmount` where it is set and `arisingAmount` otherwise.
    Null until a dispute is resolved.'
disputeNote:
  type: string
  nullable: true
  readOnly: true
  description: The `note` of the last `disputeObligation` or `resolveObligationDispute`.
""")
E(Y.add_props, SUB, "UsageRecord", """
tenantId:
  type: string
  format: uuid
  readOnly: true
  description: '**Whose usage it is** (4 October 2026, CHG-FXC-003). The control database is read across tenants by the
    operator; `getUsageMetering` (`/tenants/{tenantId}/usage`) selects one tenant''s rows by this column.'
scopePath:
  type: string
  readOnly: true
  description: The tenant's root scope path, so the row sits under the scope row-level security of the control
    database (`platform.apply_scope_rls`) like every other tenant-owned control row.
""")
E(Y.add_props, PUB, "ApiAnomalyRule", """
tenantId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: '**The tenant a rule belongs to** (4 October 2026, CHG-FXC-003). Null for a platform default, which
    every tenant reads; `listApiAnomalyRules` returns the platform defaults and the caller tenant''s own rules.'
scopePath:
  type: string
  nullable: true
  readOnly: true
  description: The tenant's root scope path for a tenant rule (scope row-level security); null for a platform default.
""")
E(Y.add_props, TRN, "FavouriteRoute", """
subjectId:
  type: string
  format: uuid
  readOnly: true
  description: '**The guest who saved it** (4 October 2026, CHG-FXC-003; transport.favourite_route had no owner
    column). Taken from the guest session, never from the body. Unique per (subjectId, venueId, fromStationId,
    toStationId); `saveFavouriteRoute` counts this column for the 20-per-guest limit and `listMyFavouriteRoutes` and
    `deleteFavouriteRoute` match on it (`x-ticvai-self-scoped: subject`).'
""")
E(Y.add_props, RES, "Resource", """
resourceTypeId:
  type: string
  format: uuid
  nullable: true
  description: '**The configurable resource type** (`resources.resource_type`, 4 October 2026, CHG-FXC-003).
    `kind` is the fixed family a type belongs to; this is the tenant''s own type within it, and the
    `resourceTypeId` filter of `suggestResources` and `ResourceRequirement.resourceTypeId` match on it.'
""")
E(Y.add_props, RES, "ResourceRequirement", """
packageId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: '**The package this requirement is a component of** (4 October 2026, CHG-FXC-003). Written by
    `updateResourcePackage`, which replaces the package''s `components` as these rows; `listResourcePackages` reads
    them back by it. Null for an experience''s own requirement (`productId`).'
productId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: The experience product this requirement belongs to (`setExperienceResourceRequirements`). Exactly one
    of `packageId` and `productId` is set.
""")
E(Y.add_props, ACC, "Entitlement", """
invitationId:
  type: string
  format: uuid
  nullable: true
  description: '**The invitation that issued it** (4 October 2026, CHG-FXC-007): `orders.issueInvitation` issues the
    entitlement without an order, because an invitation never enters the order path. Exactly one of `orderId` and
    `invitationId` is set.'
""")
E(Y.replace_in_schema, ACC, "Entitlement",
  "        orderId:\n          type: string\n          format: uuid\n          description: The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`).\n",
  "        orderId:\n          type: string\n          format: uuid\n          nullable: true\n          description: The order's id, a UUIDv7 as in `/orders/{orderId}` (`orders.sales_order.id`). **Null for an\n            entitlement an invitation issued** (`invitationId`; 4 October 2026, CHG-FXC-007).\n")
E(Y.add_props, GAM, "GameCard", """
id:
  type: string
  format: uuid
  readOnly: true
  description: '**The card''s own id** (4 October 2026, CHG-FXC-006): the `{cardId}` of `setGameCardLifecycle`,
    which had no column to match, and the `id` of the Wallet view `wallet.loadGameCredits` and
    `wallet.adjustGameCard` return for a card with no wallet.'
walletId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: '**Where the card''s credits are held** (4 October 2026, CHG-FXC-006). Set when the card is registered
    to a guest who has a wallet: credits loaded to it are wallet credit lots. Null for an anonymous card, whose
    credits are held on the card row itself (`credits`, `bonusCredits`).'
""")

# ── new stores the judged writes had nowhere to put ──────────────────────────────────────────────────────────────
E(Y.add_schema_after, INV, "InventoryItem", """
DailyCountList:
  x-ticvai-persistence: inventory.daily_count_list
  type: object
  description: '**The items counted every day at one location** (`setDailyCount`, 4 October 2026, CHG-FXC-003: the
    write had only `inventory.item` to land in, which has no column for any of it). One row per venue and location
    (`locationId` null is the venue-wide list); `setDailyCount` replaces it.'
  required:
  - itemIds
  - postsAdjustment
  properties:
    id:
      type: string
      format: uuid
      readOnly: true
    itemIds:
      type: array
      items:
        type: string
        format: uuid
    locationId:
      type: string
      format: uuid
      nullable: true
    dueBy:
      type: string
      nullable: true
      description: Local time, e.g. 10:00
    postsAdjustment:
      type: boolean
      x-ticvai-column: does_post_adjustment
    scopePath:
      type: string
      readOnly: true
""")
E(Y.replace_in_op, INV, "setDailyCount", """              schema:
                type: object
                required:
                - itemIds
                - postsAdjustment
                properties:
                  itemIds:
                    type: array
                    items:
                      type: string
                      format: uuid
                  locationId:
                    type: string
                    format: uuid
                    nullable: true
                  dueBy:
                    type: string
                    nullable: true
                    description: Local time, e.g. 10:00
                  postsAdjustment:
                    type: boolean
""", """              schema:
                $ref: '#/components/schemas/DailyCountList'
""")
E(Y.add_schema_after, PUB, "ApiAnomalyRule", """
DeveloperMember:
  type: object
  x-ticvai-persistence: control.developer_member
  description: '**One person at a developer organisation** (`setDeveloperMembers`, 4 October 2026, CHG-FXC-005).
    Developer-portal people are not tenant staff: they are kept here in the control database beside
    `control.developer_account`, keyed by email, and never become `identity.principal` or `identity.delegated_access`
    rows (the Sprint 1-2 judging found no email column on a principal and no permission a portal role could map to).
    A new email is invited (`status` `invited`) and becomes `active` when the person signs in to the portal with it.
    What each role may do in the portal: `owner` everything and the member list, `admin` everything but removing the
    owner, `developer` its own clients and credentials, `readOnly` view.'
  required: [email, role, status]
  properties:
    id: { type: string, format: uuid, readOnly: true }
    developerAccountId: { type: string, format: uuid, readOnly: true }
    email: { type: string, format: email }
    role: { type: string, enum: [owner, admin, developer, readOnly] }
    status: { type: string, enum: [invited, active, removed], readOnly: true }
    invitedAt: { type: string, format: date-time, readOnly: true }
    activatedAt: { type: string, format: date-time, nullable: true, readOnly: true }
""")
E(Y.replace_in_op, PUB, "setDeveloperMembers", """                type: array
                items:
                  type: object
                  additionalProperties: true
""", """                type: array
                items:
                  $ref: '#/components/schemas/DeveloperMember'
""")
E(Y.append_op_description, PUB, "setDeveloperMembers", """
**What the PUT does** (4 October 2026, CHG-FXC-005). Replaces the organisation's member list in
`control.developer_member` (DeveloperMember): an email not on the list is invited, a listed email's role is
updated, a member left off is `removed`. Exactly one `owner` must remain, or 409. Nothing is written to the tenant's
identity tables; the portal signs a member in by the email.""", "CHG-FXC-005")
E(Y.add_schema_after, PRO, "CouponCode", """
CouponCodeAssignment:
  x-ticvai-persistence: promotions.code_assignment
  type: object
  description: '**Who a batch of codes was given to, and through which channel** (`setCodeDistributionManager`,
    4 October 2026, CHG-FXC-005: the drafted input had no table). One row per assignment; the codes it assigned carry
    its id (`CouponCode.assignmentId`) and their distribution state.'
  required:
  - channelsType
  - assigneeType
  - batchId
  - quantity
  properties:
    id:
      type: string
      format: uuid
      readOnly: true
    batchId:
      type: string
      format: uuid
    channelsType:
      type: string
      description: As `CodeDistributionAssignmentManagerInput.channelsType`.
    assigneeType:
      type: string
      description: As `CodeDistributionAssignmentManagerInput.assigneeType` (a customer segment, a B2B company, a
        reseller, a marketing campaign ...).
    assigneeReference:
      type: string
      nullable: true
      description: The assignee's id in its own context (a segment id, a company id, a campaign id); not a
        `pii.subject`, which is why `CouponCode.assignedSubjectId` cannot hold it.
    quantity:
      type: integer
      minimum: 1
    assignedAt:
      type: string
      format: date-time
      readOnly: true
    assignedByPrincipalId:
      type: string
      format: uuid
      readOnly: true
    scopePath:
      type: string
      readOnly: true
""")
E(Y.add_props, PRO, "CouponCode", """
assignmentId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: The `CouponCodeAssignment` that assigned this code (4 October 2026, CHG-FXC-005).
distributionStatus:
  type: string
  nullable: true
  readOnly: true
  enum:
  - pending
  - sent
  - delivered
  - viewed
  - cancelled
  description: '**How far the code got to its holder** (4 October 2026, CHG-FXC-005). `pending` when assigned,
    `sent` when the channel accepted it, `delivered` on the channel''s delivery receipt, `viewed` when the holder
    opened it, `cancelled` when the assignment was withdrawn. Null for a code never assigned. Kept apart from
    `status`, which is the code''s redemption life (issued, assigned, redeemed, expired, voided).'
""")
E(Y.append_op_description, PRO, "setCodeDistributionManager", """
**Where it is stored** (4 October 2026, CHG-FXC-005). The input becomes one `promotions.code_assignment` row
(CouponCodeAssignment: channelsType, assigneeType, assigneeReference, batchId, quantity); `quantity` codes of the batch
that are `issued` and unassigned move to `assigned` with `assignmentId` set and `distributionStatus` `pending` (409
when the batch has fewer left). The view counts the batch's codes: `generated` all of them, `assigned` those with an
assignment, `sent`, `delivered`, `viewed` and `cancelled` by `distributionStatus`, `redeemed` and `expired` by
`status`.""", "CHG-FXC-005")
E(Y.set_persistence, PRO, "CodeDistributionAssignmentManagerInput",
  "none — request only; stored as one promotions.code_assignment row (CouponCodeAssignment) and the coupon codes it "
  "assigns (CHG-FXC-005)")

# ── CHG-FXC-005: the drafted composite approvals inputs, field by field ─────────────────────────────────────────
E(Y.add_props, APR, "ApprovalRule", """
code:
  type: string
  maxLength: 64
  nullable: true
  description: '**A stable code for the rule, unique within its matrix** (4 October 2026, CHG-FXC-005). The composite
    `approveMatrixMultiLevel` upserts a rule by it; `setApprovalMatrix` may leave it null.'
minimumApprovals:
  type: integer
  minimum: 1
  nullable: true
  description: N in N-of-M (CHG-FXC-005). Null means every approver the mode asks.
requiredApproverRoleId:
  type: string
  format: uuid
  nullable: true
  description: A role that must be among the approvals whatever N is (the CFO in an N-of-M group); it is also one of
    `approverRoleIds` (CHG-FXC-005).
rejectionBehavior:
  type: string
  nullable: true
  enum:
  - rejectRequest
  - returnToPreviousLevel
  - returnToRequester
  description: What a rejection at this rule does; null is `rejectRequest` (CHG-FXC-005).
allowRequestChanges:
  type: boolean
  default: false
allowDelegate:
  type: boolean
  default: true
allowReassign:
  type: boolean
  default: false
minPercentage:
  type: number
  nullable: true
  description: A percentage threshold (a discount or a margin impact) at or above which the rule applies, beside
    `minAmount` (CHG-FXC-005).
matchAttributes:
  type: object
  x-ticvai-persistence-column: jsonb
  nullable: true
  additionalProperties:
    type: string
  description: '**The request attributes a rule matches on** (CHG-FXC-005): keys `module`, `product`, `department`,
    `customerType`, `risk`, `exceptionType`, `legalEntity`, each an exact value the request''s attributes must carry.
    Every key given must match; an absent key matches anything. Evaluated before `condition`.'
compositeMode:
  type: string
  nullable: true
  enum:
  - single
  - sequential
  - parallel
  - anyOne
  - allMustApprove
  - conditional
  - multiLevel
  description: The `approvalMode` the composite screen sent, kept so it reads back what it saved; `mode`, `levels`
    and `minimumApprovals` are what the engine runs (CHG-FXC-005).
""")
E(Y.add_props, APR, "ApprovalDelegation", """
delegationType:
  type: string
  nullable: true
  description: The composite screen's `delegationType` (planned absence, temporary cover ...), for display and
    reporting; the engine treats every delegation alike (4 October 2026, CHG-FXC-005).
maxPercentage:
  type: number
  nullable: true
  description: A percentage cap beside `maxAmount` (the composite's `authorityPercentage`, CHG-FXC-005).
requiredRoleId:
  type: string
  format: uuid
  nullable: true
  description: A role the delegate must hold for the delegation to act (the composite's `requiredRole`); checked when
    the delegate decides, refused with 409 at creation where the delegate does not hold it (CHG-FXC-005).
""")
E(Y.set_persistence, APR, "ApprovalMatrixMultiLevelApprovalConfigurationInput",
  "none — request only; written as one approvals.rule row (ApprovalRule) of the approvals.matrix for the kind and "
  "scope it names, field by field in approveMatrixMultiLevel (CHG-FXC-005)")
E(Y.set_persistence, APR, "RolesAuthorityDelegationApprovalLimitsInput",
  "none — request only; written as one approvals.delegation row (ApprovalDelegation), field by field in "
  "approveRoleAuthorityDelegation (CHG-FXC-005)")
E(Y.append_op_description, APR, "approveMatrixMultiLevel", """
**What it writes, field by field** (4 October 2026, CHG-FXC-005; the Sprint 1-2 judging found no mapping). It is
`setApprovalMatrix` for one rule, through the same tables and the same versioning (a matrix in use gets a new version;
in-flight requests keep theirs, R129):

| Input | Stored as |
|---|---|
| `module` | the matrix: `approvals.matrix.kind`, an `ApprovalKind` value (400 when it is not one) |
| `venue` | the matrix's scope (`scope_level` venue, its `scope_path`); absent, the tenant's matrix |
| `code` | `approvals.rule.code`, the upsert key within the matrix |
| `approvalMode` | `compositeMode`, and what the engine runs: `single` sequential with `levels` 1; `sequential` and `multiLevel` sequential with `levels` = `minimumApprovals`; `parallel` parallel; `anyOne` parallel with `minimumApprovals` 1; `allMustApprove` consensus; `conditional` sequential, applying only where `skipConditions` does not hold |
| `amount`, `percentage` | `minAmount`, `minPercentage` |
| `product`, `department`, `customerType`, `risk`, `exceptionType`, `legalEntity` | `matchAttributes` (with `module`) |
| `minimumApprovals`, `rejectionBehavior` | the same-named rule fields |
| `requestChanges`, `delegate`, `reassign` | `allowRequestChanges`, `allowDelegate`, `allowReassign` |
| `skipConditions` | `condition`, negated: the rule is skipped where it holds |
| `requiredApproverRole` | `requiredApproverRoleId`, and `approverRoleIds` = [it] when the rule is new |

The view reads the same row back in the input's shape. `setApprovalMatrix` stays the operation of record for whole
matrices; both write the same rows, so neither overwrites the other's rules.""", "CHG-FXC-005")
E(Y.append_op_description, APR, "approveRoleAuthorityDelegation", """
**What it writes, field by field** (4 October 2026, CHG-FXC-005). One `approvals.delegation` row, as
`createApprovalDelegation` writes it (an existing active delegation between the same two people is updated):

| Input | Stored as |
|---|---|
| `delegator`, `delegate` (principal ids; `user` is the delegator when `delegator` is absent) | `delegatorPrincipalId`, `delegatePrincipalId` |
| `start`, `end`, `reason` | `from`, `to`, `reason` |
| `requestKind` | `kinds` = [it] (an `ApprovalKind`; absent, every kind) |
| `authorityAmount`, `authorityPercentage` | `maxAmount`, `maxPercentage`: the delegation's own cap, which never exceeds what the delegator may approve under the matrix (409 `exceedsDelegatorAuthority`) |
| `scope`, `venue`, `region`, `businessUnit`, `legalEntity`, `department` | `scopePath`: the most specific scope node given |
| `delegationType` | `delegationType` |
| `requiredRole` (and `role`, `position`) | `requiredRoleId`: the delegate must hold it (409 otherwise); `role` and `position` are display only |

Authority limits of a role stay in `setApprovalMatrix`; this sets the limit of one delegation.""", "CHG-FXC-005")

# ── BO-346: the printable design lands in the media template ────────────────────────────────────────────────────
E(Y.set_persistence, ACC, "PdfPrintablePosTicketDesignerInput",
  "none — request only; the whole body is stored as the design document (access.media_template.design, jsonb) of "
  "the template named by templateId, designer pdfPrintablePos (CHG-FXC-005)")
E(Y.insert_after_in_op, ACC, "getPdfPrintablePos", "      x-ticvai-conflict-policy: serverWins", """
parameters:
- name: templateId
  in: query
  required: false
  description: '**The template to open** (4 October 2026, CHG-FXC-005): `access.media_template.id` of a template whose
    `designer` is `pdfPrintablePos`, as BO-346 opened it. Absent: the most recently updated such template at the
    caller''s venue; 404 when there is none.'
  schema:
    type: string
    format: uuid
""", 6)
for op in ("setPdfPrintablePos", "getPdfPrintablePos"):
    E(Y.append_op_description, ACC, op, """
**Where the design is stored** (4 October 2026, CHG-FXC-005; the Sprint 1-2 judging found the schemas saying nothing
is stored while the lineage wrote `access.media_template`). The body is the template's working design document:
`access.media_template.design` (jsonb) on the row `templateId` names, with `designer` `pdfPrintablePos` and
`media_type` from `outputFormat`; a save appends an `access.configuration_change` with the before and after. The GET
reads that row and returns `design` in the write's shape.""", "CHG-FXC-005")

# ── CHG-FXC-006: game-card loads ─────────────────────────────────────────────────────────────────────────────────
GAMECARD = """
**Where the credits go and what comes back** (4 October 2026, CHG-FXC-006; the Sprint 1-2 judging found a Wallet
response and a wallet lock for a card that has no wallet). The card is found by `cardCode` (`games.card.card_code`).
* **A card with a `walletId`** (registered to a guest with a wallet): the movement is a wallet movement under the
  one-balance-writer rule: `wallet.balance` locked for one guarded statement, a `wallet.wallet_transaction` (kind
  `topUp`, `reason` `gameCard:{cardCode}`), and a `wallet.credit_lot` per kind of credit (`source_kind` `topUp` for
  paid credits, `promotion` for bonus credits, `source_reference` `gameCard:{cardCode}`). Returns that Wallet.
* **An anonymous card** (`walletId` null): the card row is the balance. `games.card.credits` and `bonus_credits`
  change in one guarded update on the locked row. Returns the card as a Wallet view: `id` the card's `id`,
  `subjectId` the nil UUID `00000000-0000-0000-0000-000000000000` (no guest), `balance` the paid credits,
  `bonusBalance` the bonus credits, `currency` the venue's, `status` the card's status.
Either way the movement emits `wallet.credited` (`kind` `gameCreditLoad`, `walletId` the wallet or the card's id)
through `platform.outbox` in the same transaction, and the ledger posts `gameCreditLoaded` from it."""
E(Y.append_op_description, WAL, "loadGameCredits", GAMECARD, "CHG-FXC-006")
E(Y.append_op_description, WAL, "adjustGameCard", GAMECARD.replace("Where the credits go", "Where an adjustment goes")
  .replace("(kind\n  `topUp`", "(kind\n  `adjustment`")
  .replace("(`kind` `gameCreditLoad`", "(`kind` `adjustment`")
  .replace("the ledger posts `gameCreditLoaded` from it", "the ledger posts it as a stored-value adjustment"),
  "CHG-FXC-006")

# ── CHG-FXC-007: an invitation issues its entitlement without an order ───────────────────────────────────────────
E(Y.append_op_description, ORD, "issueInvitation", """
**The entitlement it issues has no order** (4 October 2026, CHG-FXC-007; `access.entitlement.order_id` was NOT NULL
with a key to `orders.sales_order`, so the row could not be inserted). The entitlement is written with `orderId` null
and `invitationId` set to this invitation; exactly one of the two is set on every entitlement. Nothing is written to
`orders.sales_order`.""", "CHG-FXC-007")

# ── CHG-FXC-008: the shift swap's approval request ───────────────────────────────────────────────────────────────
E(Y.append_schema_description, APR, "ApprovalKind", """
**A rota shift swap** (4 October 2026, CHG-FXC-008; Sprint 1-2 judging: `workforce.requestShiftSwap` raised a request
with no kind that fits). `configurationChange`, subject `shiftSwap`, `subjectContract` `workforce`, `subjectId` the
ShiftSwap id: an existing kind narrowed by `subjectTypes`, as the optional review steps above, so no kind is added.""",
  "shiftSwap")
E(Y.append_op_description, WRK, "requestShiftSwap", """
**The approval request it raises** (4 October 2026, CHG-FXC-008): `approvals.createApprovalRequest` with kind
`configurationChange`, `subjectType` `shiftSwap`, `subjectContract` `workforce` and `subjectId` the ShiftSwap's id,
once both parties have accepted. A venue's matrix routes it with a rule whose `subjectTypes` holds `shiftSwap`; with no
such rule the tenant default asks a supervisor at the assignment's venue.""", "CHG-FXC-008")

# ── CHG-FXC-009: rules the contract named and never gave ─────────────────────────────────────────────────────────
E(Y.append_prop_description, FIN, "PeriodCloseResult", "checks", """
**What each check is, and what fails it** (4 October 2026, CHG-FXC-009; the Sprint 1-2 judging found the values and
no definition). Each runs over the period's legal entity and dates; `blockingCount` is what fails it.
- `trialBalanceBalances`: posted `ledger.journal_line` debits equal credits for the period, per currency. Blocking:
  currencies out of balance.
- `noUnapprovedJournals`: no `ledger.journal_entry` dated in the period is `draft` or awaiting approval. Blocking: those
  entries.
- `noOpenShifts`: no POS shift with a business date in the period is still open, suspended or awaiting close approval,
  asked of `orders.listShifts`. Blocking: those shifts.
- `settlementsReconciled`: every `ledger.settlement` in the period is reconciled and no `ledger.settlement_exception`
  on it is open. Blocking: unreconciled settlements plus open exceptions.
- `recognitionRunComplete`: no `ledger.recognition_schedule` line due on or before the period end is unrecognised.
  Blocking: those lines.
- `priorPeriodClosed`: the legal entity's previous `ledger.fiscal_period` is `closed`. Blocking: 1 or 0.
- `varianceExceptionsReviewed`: no `ledger.price_variance` in the period is unreviewed. Blocking: those variances.
The close fails (409, `PeriodCloseProblem.failedChecks`) when any check or wallet check fails; a dry run reports the
same list and locks nothing. Each run, dry or not, appends one `ledger.fiscal_period_event` with the results.""",
  "CHG-FXC-009", ["items", "properties", "check"])
E(Y.append_prop_description, WL, "DeepLinkScheme", "patterns", """
**The patterns, fixed** (4 October 2026, CHG-FXC-009). One per target kind, under `baseUrl`:
`product` `/p/{productId}`, `event` `/e/{eventId}`, `contentPage` `/c/{contentPageId}`, `module` `/m/{moduleKey}`,
`appSection` `/s/{appSection}`, `bookingFlow` `/book/{productId}` (optionally `?date=YYYY-MM-DD`). `externalUrl` and
`none` have no pattern. Campaign tags are appended as `utm_*` query parameters. A released pattern never changes: a new
target kind gets a new prefix, so a link a tenant printed keeps working. Where app links are enabled the same path opens
the app (universal links and app links on the primary domain) and the storefront where the app is not installed;
`buildDeepLink` returns the URL from these patterns and `appLink` as the same URL.""", "CHG-FXC-009")
E(Y.append_op_description, FIN, "transmitEInvoices", """
**The PINT AE mapping this build uses until the regulator's list is in hand** (4 October 2026, CHG-FXC-009; a client
question, CF-133, stays open). From FinTaxInvoice: `invoiceNumber` the invoice ID, `issuedAt` the issue date,
`supplyDate` the supply date, `invoiceType` the type code (380 a tax invoice, simplified invoices flagged as
simplified), `currency` the document currency, `supplierName`, `supplierAddress` and
`supplierTaxRegistrationNumber` the seller party and its TRN, `buyerName`, `buyerAddress`, `buyerCountryCode` and
`buyerTaxRegistrationNumber` the buyer party, each line its quantity, net amount, tax category and rate, and the
totals `netAmount`, `discountAmount`, `taxAmount`, `grossAmount` (with `taxAmountInLegalCurrency` where the document
currency is not AED). From FinCreditMemo: type code 381, `creditMemoNumber`, the billing reference to
`taxInvoiceNumber`, `reason`, its lines and totals. A document missing a field the provider rejects as mandatory is
not sent: its `eInvoiceStatus` becomes `rejected` with the provider's reason, and the rest of the batch goes on. The
mapping lives in the provider adapter (ADR-0062), so the regulator's final list changes the adapter, not this
contract.""", "CHG-FXC-009")
for op in ("claimLocationSession", "claimTableSession"):
    E(Y.append_op_description, FNB, op, """
**What the rotating code is** (4 October 2026, CHG-FXC-009; the Sprint 1-2 judging found no store for it). Not a row:
a signed token, `{locationRef}.{generation}.{expiresAt}.{signature}`, where `locationRef` is the delivery location's
or table's id, `generation` the location's `codeGeneration`, `expiresAt` a Unix time (0 for a printed code that does
not expire by time), and `signature` an HMAC-SHA256 over the other three with the tenant's location-code key from the
secrets store. **Unknown** (`codeUnknown`): the signature does not verify or the location does not exist. **Expired**
(`codeExpired`): it verifies, and its `generation` is behind the location's or `expiresAt` has passed. Reprinting a
location's codes bumps its `codeGeneration`, which retires every code printed before.""", "CHG-FXC-009")
for sch in ("DeliveryLocation", "TableDefinition"):
    E(Y.add_props, FNB, sch, """
codeGeneration:
  type: integer
  minimum: 1
  default: 1
  description: '**Which printing of the location''s ordering code is current** (4 October 2026, CHG-FXC-009). A code
    carrying an older generation is refused as `codeExpired` by `claimLocationSession`; raising it retires every code
    printed before.'
""")

# ── guess-ticket storage the judged operations need ──────────────────────────────────────────────────────────────
E(Y.replace_in_schema, C("satellite/accreditation.yaml"), "AccessProfile", "        schedule:\n          type: array\n",
  "        schedule:\n          type: array\n          " + JSONB + "\n")
E(Y.replace_in_schema, C("satellite/accreditation.yaml"), "HolderAccess", "        exceptions:\n          type: array\n",
  "        exceptions:\n          type: array\n          " + JSONB + "\n")
E(Y.add_props, FNB, "TableVisit", """
serviceStage:
  type: string
  nullable: true
  readOnly: true
  description: '**Where the table is in its service** (4 October 2026, CHG-FXC-003): the last stage `setServiceStage`
    recorded (its `stage` value), null before the first. Kept with `serviceStageRecordedAt` so the last-writer-wins rule
    compares the incoming `recordedAt` with the stored one and ignores an older write.'
serviceStageRecordedAt:
  type: string
  format: date-time
  nullable: true
  readOnly: true
""")
E(Y.add_props, QUE, "WaitingGuest", """
overriddenByPrincipalId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: '**Who let the party past the queue** (`overrideWaitingGuest`, 4 October 2026, CHG-FXC-003), with
    `overrideReason` and `overriddenAt`. Null when the entry was never overridden.'
overrideReason:
  type: string
  nullable: true
  readOnly: true
overriddenAt:
  type: string
  format: date-time
  nullable: true
  readOnly: true
""")
E(Y.add_schema_after, C("satellite/maintenance.yaml"), "Incident", """
IncidentHistoryEntry:
  x-ticvai-persistence: maintenance.incident_history
  type: object
  description: '**One line of an incident''s append-only history** (4 October 2026, CHG-FXC-003). `updateIncident`
    appends one per note, status change and escalation in the same transaction as the change; rows are never updated
    or deleted.'
  required: [id, incidentId, kind, recordedAt, principalId]
  properties:
    id: { type: string, format: uuid, readOnly: true }
    incidentId: { type: string, format: uuid }
    kind: { type: string, enum: [note, statusChange, escalation] }
    fromStatus: { type: string, nullable: true }
    toStatus: { type: string, nullable: true }
    note: { type: string, nullable: true }
    principalId: { type: string, format: uuid }
    recordedAt: { type: string, format: date-time }
""")
E(Y.add_schema_after, IDN, "AuthorisationPolicy", """
GuestCredential:
  x-ticvai-persistence: identity.guest_credential
  type: object
  description: '**A guest''s password, as stored** (4 October 2026, CHG-FXC-003; `registerGuest` took a password and
    no table held it, so `guestPasswordLogin` had nothing to check). Never returned by any operation: this schema exists
    to say where the hash lives. One row per guest subject; `registerGuest` and `changeOwnCredential` write it,
    `guestPasswordLogin` reads it, counts failures against `identity.password_policy` and locks until `lockedUntil`.'
  required: [subjectId, passwordHash, failedAttempts]
  properties:
    subjectId: { type: string, format: uuid }
    passwordHash: { type: string, writeOnly: true, description: 'Argon2id, with its parameters, never the password.' }
    failedAttempts: { type: integer, minimum: 0 }
    lockedUntil: { type: string, format: date-time, nullable: true }
    passwordSetAt: { type: string, format: date-time }
""")

# ── CHG-FXC-004: the tables each judged operation's own description says it touches ─────────────────────────────
# op: (reads to add, writes to add, writes to remove, reads to remove, why)
LINEAGE = {
    "rollbackMenu": ([], ["fnb.menu_version"], [], [], "a rollback writes the new MenuVersion it creates"),
    "scheduleMenuPublish": ([], ["fnb.menu_schedule"], [], [], "creates or cancels the MenuSchedule"),
    "seatTableReservation": ([], ["fnb.reservation_table"], [], [], "a table assignment is one reservation_table row"),
    "claimTableSession": (["fnb.dining_table", "fnb.table_visit", "platform.outlet"], ["fnb.table_visit"], [], [],
                          "the table the code names, the open visit it joins or starts, the outlet's opening"),
    "claimLocationSession": (["fnb.delivery_location", "fnb.dining_table", "fnb.table_visit"], ["fnb.table_visit"], [], [],
                             "the location the code names and its codeGeneration; a table's open visit"),
    "setRecipe": (["inventory.item", "fnb.menu_item", "fnb.substitution_rule", "fnb.modifier_group"],
                  ["fnb.menu_item", "fnb.allergen_verdict"], [], [],
                  "costs from inventory items; the menu item marked stock-tracked; verifyAllergens re-run"),
    "getTableMap": (["fnb.table_visit"], [], [], [], "TableState is the table and its open visit"),
    "clearTable": (["fnb.table_visit"], ["fnb.table_visit"], [], [], "clearing closes the open visit"),
    "setTableLayout": (["fnb.table_visit"], [], [], [], "a table with an open visit cannot be removed or resized"),
    "verifyAllergens": (["fnb.recipe_ingredient", "fnb.ingredient_substitute", "fnb.modifier_option",
                         "fnb.menu_item_modifier", "inventory.item"], [], [], [],
                        "the actual allergens come from the recipe's ingredients (inventory items' allergens), "
                        "their substitutes and the modifier options"),
    "listIngredientSubstitutes": (["fnb.recipe"], [], [], [], "the recipe the path names"),
    "setIngredientSubstitutes": (["fnb.recipe"], [], [], [], "the recipe the path names"),
    "recordWriteOff": ([], ["ledger.journal_entry", "ledger.journal_line"], [], [], "the posting needs its journal entry"),
    "settleDeposit": ([], ["ledger.journal_entry", "ledger.journal_line"], [], [], "the posting needs its journal entry"),
    "closeFiscalPeriod": (["ledger.journal_entry", "ledger.journal_line", "ledger.settlement",
                           "ledger.settlement_exception", "ledger.recognition_schedule", "ledger.price_variance"],
                          ["ledger.fiscal_period_event"], [], [],
                          "the close checks (PeriodCloseResult.checks) and the run record"),
    "beginPeriodClose": ([], ["ledger.fiscal_period_event"], [], [], "every close step is a fiscal_period_event"),
    "abandonPeriodClose": ([], ["ledger.fiscal_period_event"], [], [], "every close step is a fiscal_period_event"),
    "listSegmentMembers": (["marketing.segment", "marketing.segment_criterion"], [], [], [],
                           "the definition evaluated live"),
    "previewSegmentDraft": (["marketing.guest_profile", "marketing.consent_record", "marketing.suppression",
                             "marketing.segment", "marketing.segment_criterion"], [], ["marketing.segment_criterion"], [],
                            "a preview counts and stores nothing (the contract says it writes nothing)"),
    "setDailyCount": (["inventory.daily_count_list"], ["inventory.daily_count_list"], ["inventory.item"], [],
                      "the daily list is its own row (DailyCountList)"),
    "setDeveloperMembers": (["control.developer_member"], ["control.developer_member"], ["identity.delegated_access"],
                            ["identity.principal"], "portal members are control.developer_member rows, not tenant grants"),
    "setCodeDistributionManager": (["promotions.code_assignment"], ["promotions.code_assignment"], [], [],
                                   "the assignment row and the codes it assigns"),
    "createApprovalDelegation": (["approvals.matrix", "approvals.rule"], [], [], [],
                                 "exceedsDelegatorAuthority compares with what the matrix lets the delegator approve"),
    "getPdfPrintablePos": (["access.media_template"], [], [], [], "the template's design document"),
    "loadGameCredits": (["wallet.balance"], ["wallet.wallet", "wallet.credit_lot", "wallet.balance",
                                             "wallet.wallet_transaction", "platform.outbox"], [], [],
                        "a registered card's credits are wallet movements; wallet.credited through the outbox"),
    "adjustGameCard": (["wallet.balance"], ["wallet.balance", "wallet.wallet_transaction", "wallet.credit_lot",
                                            "platform.outbox"], [], [], "as loadGameCredits"),
    "topUpWallet": (["wallet.balance"], ["wallet.balance", "wallet.wallet_transaction"], [], [],
                    "the one balance writer (SD-027)"),
    "listResourcePackages": (["resources.resource_requirement"], [], [], [], "components by package_id"),
    "suggestResources": (["resources.resource_type", "resources.booking", "resources.resource_block"], [], [], [],
                         "the type filter and what is free"),
    "createResourceHold": (["resources.resource", "resources.booking", "resources.resource_block",
                            "venuemap.map", "venuemap.placed_resource"], [], [], [],
                           "bookability, capacity, setup and teardown, existing bookings and blocks, the published map"),
    "acceptShiftVariance": (["orders.deposit_box"], ["orders.deposit_box"], [], [],
                            "the shift's deposit boxes become reconciled"),
    "applyManualDiscount": ([], ["orders.order_line_discount"], [], [],
                            "the discount it records (the ledger posts from the order events)"),
    "submitReview": (["marketing.case"], ["marketing.case"], [], [], "a low rating opens a service case"),
    "publishBundle": (["catalogue.product", "catalogue.variant", "catalogue.price", "catalogue.price_list",
                       "platform.sale_board", "platform.sale_board_tile"], [], [], [],
                      "the snapshot is built from the catalogue and the sale boards"),
    "recommendSeats": (["seating.seat", "seating.seat_hold", "seating.seat_hold_item", "seating.seat_category",
                        "seating.seat_price_band", "seating.recommendation_rules", "seating.accessible",
                        "seating.seat_block_item"], [], [], [], "seat ids, contiguity, category and price"),
    "updateMediaAsset": (["assets.media_collection"], ["assets.media_collection_member"], [], [],
                         "collectionIds replaces the asset's collection members"),
    "getExpiringRights": (["assets.media_usage"], [], [], [], "isInUse and liveUsageCount count live usage"),
    "setTransportRouteStatus": (["transport.fare_table", "transport.departure"], [], [], [],
                                "the fare-table and sold-departure refusals"),
    "updateTransportRoute": (["transport.timetable"], [], [], [], "a stops change is refused under a published timetable"),
    "publishVenueMap": (["venuemap.placed_resource"], ["venuemap.map_version"], [], [],
                        "the version snapshot with its placed resources"),
    "transitionProductLifecycle": (["access.entitlement", "catalogue.published_bundle"], [], [], [],
                                   "the archive rule and isSellable"),
    "amendFnbOrder": ([], ["fnb.service_order_line"], [], [], "lines added and removed"),
    "acceptFnbOrder": ([], ["fnb.kitchen_ticket", "fnb.kitchen_ticket_line"], [], [], "accepting creates the kitchen ticket"),
    "callNextParties": (["queue.entry"], ["queue.entry"], [], [], "entries move to called"),
    "submitQueueReading": (["queue.feed"], [], [], [], "the feed names the queue"),
    "cloneGame": (["games.pricing", "games.operational_config", "games.reader_profile"],
                  ["games.pricing", "games.operational_config", "games.reader_profile"], [], [],
                  "pricing, operational settings and reader configuration are copied"),
    "updateGame": (["games.play"], [], [], [], "no price or payout change while a play is in flight"),
    "updateIncident": ([], ["maintenance.incident_history"], [], [], "the append-only history"),
    "guestPasswordLogin": (["pii.subject_contact", "identity.guest_credential", "identity.password_policy"],
                           ["identity.guest_credential", "identity.guest_session"], [], [],
                           "the account by identifier, its hash and lockout, the per-device session"),
    "registerGuest": ([], ["identity.guest_credential"], [], [], "the optional password's hash"),
    "completeSsoAuthorization": (["identity.sso_group_mapping", "identity.role", "identity.delegated_access"],
                                 ["identity.principal", "identity.delegated_access"], [], [],
                                 "group-to-role mapping, availableRoles and requiresMfa"),
    "createRole": (["identity.role_permission", "identity.capability_template", "identity.segregation_rule"],
                   ["identity.role_permission"], [], [], "the permissions, preset template and segregation rules"),
    "listRoles": (["identity.role_permission"], [], [], [], "each role's permissions"),
    "forceLogout": (["identity.principal", "identity.principal_credential", "identity.delegated_access",
                     "platform.workstation"], [], [], [],
                    "the supervisor's PIN and SESSION_FORCE_LOGOUT at the till's venue"),
    "exportSubjectData": ([], ["platform.dsar_request"], [], [], "the 202 raises a dsar_request"),
    "getStockPositions": (["inventory.movement", "inventory.stock_reservation"], [], [], ["inventory.stock_level"],
                          "on hand is derived from movements; allocated from reservations; stock_level is not stored"),
    "getStockValuation": (["inventory.movement"], [], [], ["inventory.stock_level"], "derived from movements"),
    "createGuestFnbOrder": (["inventory.movement"], [], [], ["inventory.stock_level"], "derived from movements"),
    "planProductionRun": (["inventory.movement"], [], [], ["inventory.stock_level"], "derived from movements"),
    "reserveMerchandise": (["inventory.movement", "inventory.stock_reservation"], ["inventory.stock_reservation"], [], [],
                           "stock available to allocate, and the allocation"),
    "retryMyDunningPayment": (["payments.dunning_policy", "orders.payment"], ["orders.payment"], [], [],
                              "the retry charges the stored card as a payment"),
}
# ── cross-service steps named as calls rather than foreign writes ────────────────────────────────────────────────
E(Y.insert_after_in_op, MKT, "respondToInvitation", "      x-ticvai-conflict-policy: serverWins", """
x-ticvai-calls:
- orders.issueInvitation
""", 6)
E(Y.append_op_description, MKT, "respondToInvitation", """
**How accepting issues the entitlement** (4 October 2026, CHG-FXC-004). Accepting calls `orders.issueInvitation`
(OrderService) with the invitation campaign's product, performance and quantity and the invited guest as holder;
`entitlementIds` are the ids that call returns. This operation writes only `marketing.invitation`; the entitlement is
written by OrderService (`access.entitlement` with `invitationId`, CHG-FXC-007).""", "CHG-FXC-004")
E(Y.append_op_description, C("satellite/transport.yaml"), "updateTransportDeparture", """
**Capacity goes through Catalogue** (4 October 2026, CHG-FXC-004). A departure is a catalogue performance, and its
capacity is `catalogue.channel_capacity`, which CatalogueService owns: a capacity change calls
`catalogue.updateChannelCapacity` on the departure's performance capacity after `transport.departure` is updated, in the same
request; a refusal from it (capacity below seats sold) is returned as this operation's 409.""", "CHG-FXC-004")
E(Y.append_op_description, C("satellite/transport.yaml"), "createTransportRoute", """
**The catalogue records it creates** (4 October 2026, CHG-FXC-004). The route's catalogue Event and its
`timedAdmission` product are created by calling `catalogue.createEvent` and `catalogue.createProduct` (CatalogueService
owns those tables); their ids are stored on `transport.route`. This operation writes only transport tables.""",
  "CHG-FXC-004")
E(Y.append_op_description, CAT, "cancelPerformance", """
**Where the impact figures come from** (4 October 2026, CHG-FXC-004). `affectedOrders`, `affectedGuests` and
`refundExposure` are counted from the performance's live entitlements (`access.entitlement` by `performance_id`,
status not cancelled or used: distinct `order_id`, distinct `subject_id`, the sum of their order lines' paid amounts);
`notificationsQueued` is the number of `performance.cancelled` notifications written to the outbox. Refunds themselves
run in OrderService from the `performance.cancelled` event.""", "CHG-FXC-004")
E(Y.append_op_description, QUE, "redeemWaitingGuest", """
**A Fast Pass redemption** (4 October 2026, CHG-FXC-004). Where the entry carries an `entitlementId`, redeeming calls
`access.validateAccess` for that entitlement at the queue's access point, which decrements its uses in Product &
Entitlement; `entitlementRemaining` is the remaining uses that call returns. This operation writes only
`queue.entry`.""", "CHG-FXC-004")
E(Y.append_op_description, SUB, "terminateTenant", """
**The unsettled-balance refusal** (4 October 2026, CHG-FXC-004). The tenant's ledger lives in its own cell database,
which the control plane does not read. Before terminating, the Control Plane asks the tenant's cell (`serviceAuth`) for
`finance.getTrialBalance` at today's date for every legal entity; any non-zero receivable, payable or inter-entity
balance refuses the termination with 409 `unsettledBalances`, naming the legal entities.""", "CHG-FXC-004")
E(Y.append_op_description, FNB, "setTableLayout", """
**A table with an open visit** (4 October 2026, CHG-FXC-004): removing it, or lowering its capacity below the visit's
covers, is refused with 409 `tableHasOpenVisit` (an `FnbProblem` reason), read from `fnb.table_visit`.""", "CHG-FXC-004")

# ── the events the game-card movements publish ───────────────────────────────────────────────────────────────────
EVENTS = os.path.join(ROOT, "events", "wallet-credited.yaml")


def wallet_credited_emitters() -> bool:
    t = io.open(EVENTS, encoding="utf-8").read()
    if "wallet.loadGameCredits" in t:
        return False
    t = t.replace("- wallet.releaseWalletHold\n", "- wallet.releaseWalletHold\n- wallet.loadGameCredits\n- wallet.adjustGameCard\n", 1)
    t = t.replace("emittedWhen: topUpWallet, adjustWallet, releaseWalletHold or a refund to wallet moves the balance up",
                  "emittedWhen: topUpWallet, adjustWallet, releaseWalletHold or a refund to wallet moves the balance up; "
                  "loadGameCredits and adjustGameCard move a game card's credits (kind gameCreditLoad or adjustment; "
                  "walletId is the card's id for an anonymous card; 4 October 2026, CHG-FXC-006)", 1)
    io.open(EVENTS, "w", encoding="utf-8", newline="\n").write(t)
    return True


E(wallet_credited_emitters)

# ── [screens -> contracts] requests from the ledger (CHG-FXC-010) ────────────────────────────────────────────────
def add_operation(path, url, verb, text):
    """A new operation: under its path when the path exists, or a new path before `components:`."""
    lines = Y._read(path)
    block_has = "operationId: " + [l for l in text.split("\n") if "operationId:" in l][0].split("operationId:")[1].strip()
    if any(l.strip() == block_has for l in lines):
        return False
    key = "  %s:" % url
    if key in lines:
        at = lines.index(key) + 1
        new = Y._block(verb + ":\n" + Y.textwrap.indent(Y.textwrap.dedent(text).strip("\n"), "  "), 4)
    else:
        at = lines.index("components:")
        new = Y._block(url + ":\n  " + verb + ":\n" + Y.textwrap.indent(Y.textwrap.dedent(text).strip("\n"), "    "), 2)
    lines[at:at] = new
    Y._write(path, lines)
    return True


def copy_create_campaign_fields() -> bool:
    """updateCampaign's body gains `variants` and `abTest`, exactly as CreateCampaignRequest has them."""
    lines = Y._read(MKT)
    s, e = Y.op_span(lines, "updateCampaign")
    if any(l.strip() == "abTest:" for l in lines[s:e]):
        return False
    a, b = Y.schema_span(lines, "CreateCampaignRequest")
    v = next(i for i in range(a, b) if lines[i] == "        variants:")
    ve = Y._span(lines, v, 8)
    ab = next(i for i in range(a, b) if lines[i] == "        abTest:")
    abe = Y._span(lines, ab, 8)
    at = next(i for i in range(s, e) if lines[i] == "                content:"
              and "CampaignContent" in lines[i + 1]) + 2
    lines[at:at] = [(" " * 8 + l) if l.strip() else l for l in lines[v:ve] + lines[ab:abe]]
    Y._write(MKT, lines)
    return True


E(copy_create_campaign_fields)
E(Y.append_op_description, MKT, "updateCampaign", """
**Variants and the A/B test are editable here** (4 October 2026, CHG-FXC-010; BO-772): `variants` and `abTest` take
the shapes `createCampaign` takes. While the campaign is a draft both may change; once it is live only
`abTest.winningVariantId` may be set (409 otherwise), and only where `abTest.winnerRule` is `manual`.""", "CHG-FXC-010")

E(add_operation, MKT, "/message-templates/{templateId}", "patch", """
operationId: updateMessageTemplate
x-ticvai-consumed-by:
  - "P08 BO-785 Message Template Library"
summary: Change a message template
description: |-
  **Added 4 October 2026 (CHG-FXC-010; BO-785, design-notes correction CHG-SBO-005).** A tenant's own template is
  edited in place: `name`, `subjects`, `bodies`, `mergeFields` and `providerTemplateId`. Every change writes a new
  `marketing.message_template_version`, so a campaign already sent keeps the version it used. A template whose
  `ownership` is `platform` is TICVAI's and is refused with 409; copy it with `createMessageTemplate` instead.
tags:
- marketing
x-ticvai-permission: MARKETING_MANAGE
x-ticvai-audience:
- staff
x-ticvai-scope-level: tenant
x-ticvai-config-scope: tenant
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
parameters:
- $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
- name: templateId
  in: path
  required: true
  schema:
    type: string
    format: uuid
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        minProperties: 1
        properties:
          name:
            type: string
            maxLength: 200
          subjects:
            type: object
            additionalProperties:
              type: string
            description: Per language, as `MessageTemplate.subjects`.
          bodies:
            type: object
            additionalProperties:
              type: string
            description: Per language, as `MessageTemplate.bodies`.
          mergeFields:
            type: array
            items:
              type: string
          providerTemplateId:
            type: string
            nullable: true
responses:
  '200':
    headers:
      X-Consistency-Token:
        $ref: '../shared/common.yaml#/components/headers/ConsistencyToken'
    description: Changed
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/MessageTemplate'
  '404':
    $ref: '../shared/common.yaml#/components/responses/NotFound'
  '409':
    description: The template is platform-owned (`template-platform-owned`) and cannot be edited by a tenant.
    x-ticvai-problem-types:
    - template-platform-owned
    content:
      application/problem+json:
        schema:
          $ref: ../shared/common.yaml#/components/schemas/Problem
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
E(add_operation, MKT, "/loyalty/programmes/{programmeId}", "patch", """
operationId: updateLoyaltyProgramme
x-ticvai-consumed-by:
  - "P08 BO-827 Loyalty Programme Configuration"
summary: Change a loyalty programme
description: |-
  **Added 4 October 2026 (CHG-FXC-010; BO-827).** The earning rules are `LoyaltyProgramme.earnRules` and nothing wrote
  them after `createLoyaltyProgramme`. Changes `name`, `earnRules` (replaced whole, as `marketing.points_earning_rule`
  rows), `pointsExpireAfterMonths` and `isActive`. Points already earned keep the rule and the expiry they were earned
  under; the change applies to what is earned from now. Tiers are not changed here.
tags:
- marketing
x-ticvai-permission: MARKETING_MANAGE
x-ticvai-audience:
- staff
x-ticvai-scope-level: tenant
x-ticvai-config-scope: tenant
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
parameters:
- $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
- name: programmeId
  in: path
  required: true
  schema:
    type: string
    format: uuid
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        minProperties: 1
        properties:
          name:
            type: string
            maxLength: 200
          earnRules:
            type: array
            description: Replaces the programme's earning rules; each item as `LoyaltyProgramme.earnRules[]`.
            items:
              type: object
              required:
              - trigger
              - points
              properties:
                trigger:
                  type: string
                points:
                  type: number
                productKinds:
                  type: array
                  items:
                    $ref: '../spine/catalogue.yaml#/components/schemas/ProductKind'
                multiplier:
                  type: number
          pointsExpireAfterMonths:
            type: integer
            nullable: true
          isActive:
            type: boolean
responses:
  '200':
    headers:
      X-Consistency-Token:
        $ref: '../shared/common.yaml#/components/headers/ConsistencyToken'
    description: Changed
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/LoyaltyProgramme'
  '404':
    $ref: '../shared/common.yaml#/components/responses/NotFound'
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
E(add_operation, WAL, "/wallet-refund-policy", "get", """
operationId: getWalletRefundPolicy
x-ticvai-consumed-by:
  - "P08 BO-1146 Wallet Refund Policy"
summary: The wallet refund policy in force
description: |-
  **Added 4 October 2026 (CHG-FXC-010; BO-1146): `setWalletRefundPolicy` was a PUT nothing read.** Returns the policy
  at the venue, or the defaults it would get before the first save (`defaultDestination` the original payment method,
  `restoreToOriginalLots` true, `restoreOriginalExpiry` true, no bonus). The `ETag` header carries the version the PUT
  takes as `If-Match`.
tags:
- wallet
x-ticvai-permission: WALLET_VIEW
x-ticvai-audience:
- staff
x-ticvai-scope-level: venue
x-ticvai-read-routing: replica
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
responses:
  '200':
    description: The policy
    headers:
      ETag:
        schema:
          type: string
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/WalletRefundPolicy'
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
E(add_operation, ACC, "/visual-access-rules", "get", """
operationId: listVisualAccessRules
x-ticvai-consumed-by:
  - "P08 BO-155 Visual Access Rule Builder"
summary: The visual access rules at a venue
description: |-
  **Added 4 October 2026 (CHG-FXC-010; BO-155): `setVisualAccessRule` upserts rules by `ruleId` and nothing read
  them.** One item per rule, in the shape the PUT returns, ordered by `ruleId`.
tags:
- access
x-ticvai-permission: ACCESS_POINT_CONFIGURE
x-ticvai-audience:
- staff
x-ticvai-scope-level: venue
x-ticvai-read-routing: replica
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
parameters:
- $ref: ../shared/common.yaml#/components/parameters/PageSize
- $ref: ../shared/common.yaml#/components/parameters/PageCursor
responses:
  '200':
    description: The rules
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
                  $ref: '#/components/schemas/VisualAccessRuleBuilderView'
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
E(add_operation, SUB, "/membership-product-validation", "get", """
operationId: getMembershipProductValidation
x-ticvai-consumed-by:
  - "P09 BO-293 Membership Product Validation, Approval & Publication"
summary: A membership product's validation, as the approver sees it
description: |-
  **Added 4 October 2026 (CHG-FXC-010; VM-BO-293): `approveMembershipProductValidation` was the only operation, and the
  screen must show the checks, the impact and the stage before anyone decides.** Returns the view the PUT returns for
  one membership product version; without `version`, the latest.
tags:
- subscription
x-ticvai-permission: PLATFORM_CELL_MANAGE
x-ticvai-audience:
- staff
x-ticvai-scope-level: tenant
x-ticvai-read-routing: replica
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
parameters:
- name: membershipCode
  in: query
  required: true
  schema:
    type: string
- name: version
  in: query
  required: false
  schema:
    type: string
responses:
  '200':
    description: The validation
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/MembershipProductValidationApprovalPublicationVersioView'
  '404':
    $ref: '../shared/common.yaml#/components/responses/NotFound'
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
E(Y.add_props, C("satellite/payments.yaml"), "PaymentProviderConnection", """
credentialRef:
  type: string
  writeOnly: true
  description: '**Where the provider credential is kept** (4 October 2026, CHG-FXC-010; ADM-570): the vault reference
    the credential was stored under, as `SetPaymentProviderRequest.credentialRef`. Sent on create, never returned;
    `credentialFingerprint` is what reads show.'
""")
E(Y.add_props, ORD, "OrdersDeposit", """
ledgerDepositId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: '**The finance Deposit that holds this deposit''s liability** (4 October 2026, CHG-FXC-010; VM-BO-024):
    the `depositId` `finance.settleDeposit` takes. Null until the liability is posted.'
""")
E(Y.add_props, ACC, "ParkingFacility", """
productVariantId:
  type: string
  format: uuid
  nullable: true
  description: '**The catalogue variant sold for parking here** (4 October 2026, CHG-FXC-010; GST-027, WEB-041): what
    `addCartLine` sells when a guest buys parking at this car park. Set by staff; readable by guests. Null where the
    car park does not sell parking through the platform.'
""")
E(Y.add_props, WL, "PublishedTenantConfig", """
paymentTokenisation:
  type: object
  nullable: true
  description: '**The provider the guest app tokenises cards with** (4 October 2026, CHG-FXC-010; GST-071): the
    `providerId` `storePaymentToken` requires, its kind and the publishable key the client SDK needs. Never a secret.
    Null where no provider with tokenisation is connected.'
  required:
  - providerId
  - providerKind
  properties:
    providerId:
      type: string
      format: uuid
    providerKind:
      type: string
    publishableKey:
      type: string
      nullable: true
""")
for _p in ("moduleCode", "requiresModules", "incompatibleWithModules"):
    E(Y.append_prop_description, SUB, "ModuleListing", _p, """
**Values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424): the vocabulary of
`white-label.ModuleEnablement.moduleKey`, so a dependency is checked against what `setModuleEnablement` switches.""",
      "CHG-FXC-010")
E(Y.append_prop_description, SUB, "LicencePosition", "licensedModules", """
**`moduleKey` values are `ModuleKey`s** (4 October 2026, CHG-FXC-010; ADM-424), the vocabulary of
`white-label.ModuleEnablement.moduleKey`.""", "CHG-FXC-010")


def experience_id_is_product() -> bool:
    t = io.open(RES, encoding="utf-8").read()
    old = ("  /experiences/{experienceId}/resource-requirements:\n    parameters:\n    - name: experienceId\n"
           "      in: path\n      required: true\n")
    if old not in t or "CHG-FXC-010; BO-877" in t:
        return False
    t = t.replace(old, old + "      description: The experience's catalogue `Product.id` (4 October 2026, CHG-FXC-010; BO-877).\n", 1)
    io.open(RES, "w", encoding="utf-8", newline="\n").write(t)
    return True


E(experience_id_is_product)

E(Y.replace_in_schema, WAL, "WalletRiskRules", "              alertOnAction:\n                type: boolean\n",
  "              alertOnAction:\n                type: boolean\n                x-ticvai-column: does_alert_on_action\n")

E(Y.add_props, ACC, "LiveGateModeLaneControlView", """
pendingChangeId:
  type: string
  format: uuid
  nullable: true
  readOnly: true
  description: '**The scheduled mode change on this lane, if any** (4 October 2026, CHG-FXC-003; BO-230): the
    `access.gate_mode_change` id `cancelGateModeChange` takes as `{changeId}`, set while `targetMode` differs from
    `currentMode` and the change has not taken effect. Null otherwise.'
""")

# ADM-069: many reusable tax profiles, so a list and an id (CHG-FXC-010)
E(add_operation, CAT, "/tax-profiles", "get", """
operationId: listTaxProfiles
x-ticvai-consumed-by:
  - "P08 ADM-069 Tax Profile & Jurisdiction Configuration"
summary: The tax profiles
description: |-
  **Added 4 October 2026 (CHG-FXC-010; ADM-069): the screen manages many reusable tax profiles and the contract had one
  record per venue with no list.** Every `catalogue.tax_profile` at or above the caller's scope, in the shape
  `getTaxProfileJurisdiction` returns, ordered by `taxProfileCode`. A profile is opened with
  `getTaxProfileJurisdiction?taxProfileId=` and saved with `setTaxProfileJurisdiction`, which creates a profile when the
  body's `taxProfileId` is empty and updates that profile otherwise.
tags:
- catalogue
x-ticvai-permission: PRODUCT_VIEW
x-ticvai-audience:
- staff
x-ticvai-scope-level: venue
x-ticvai-read-routing: replica
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
parameters:
- name: legalEntityId
  in: query
  required: false
  schema:
    type: string
    format: uuid
- name: status
  in: query
  required: false
  schema:
    type: string
- $ref: ../shared/common.yaml#/components/parameters/PageSize
- $ref: ../shared/common.yaml#/components/parameters/PageCursor
responses:
  '200':
    description: The profiles
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
                  $ref: '#/components/schemas/TaxProfileJurisdictionConfigurationView'
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
E(Y.insert_after_in_op, CAT, "getTaxProfileJurisdiction", "      x-ticvai-conflict-policy: serverWins", """
parameters:
- name: taxProfileId
  in: query
  required: false
  description: '**The profile to open** (4 October 2026, CHG-FXC-010; ADM-069), from `listTaxProfiles`. Absent: the
    profile in force at the caller''s venue; 404 when there is none.'
  schema:
    type: string
    format: uuid
""", 6)
E(Y.append_op_description, CAT, "setTaxProfileJurisdiction", """
**One profile per call, many per tenant** (4 October 2026, CHG-FXC-010; ADM-069). An empty `taxProfileId` creates a
`catalogue.tax_profile` row; a `taxProfileId` updates that row (a rate change is a new future-dated version, as
above). `listTaxProfiles` lists them; the legal entity comes from `finance.listLegalEntities`.""", "CHG-FXC-010")
for _op, _w in (("getVirtualTicketIdentity", ["access.credential_policy"]),
                ("getBleBeaconGeofence", ["access.access_point", "access.device_placement"]),
                ("getBiometricVerificationProfile", ["access.biometric_profile"]),
                ("getFacePassEnrollmentConfiguration", ["access.biometric_profile"]),
                ("listBiometricLifecycleRetention", ["tenancy.data_retention_setting"]),
                ("getTaxProfileJurisdiction", ["catalogue.tax_profile"]),
                ("listTaxProfiles", ["catalogue.tax_profile"])):
    LINEAGE[_op] = (_w, [], [], [], "reads what its write stores (the r1 gate's added reads had none)")

# exportSubjectData now writes its platform.dsar_request, so its 2xx carries the consistency token (api-conventions 3)
E(Y.replace_in_op, IDN, "exportSubjectData",
  "        '202':\n          description: 'Export started, as a data-subject request",
  "        '202':\n          headers:\n            X-Consistency-Token:\n"
  "              $ref: '../shared/common.yaml#/components/headers/ConsistencyToken'\n"
  "          description: 'Export started, as a data-subject request")

# VM-BO-669 and BO-666: the accreditation validity a whole-record PUT writes and nothing read (CHG-FXC-010)
E(add_operation, C("satellite/accreditation.yaml"), "/accreditation-validity", "get", """
operationId: getAccreditationValidity
x-ticvai-consumed-by:
  - "P08 BO-669 Accreditation Validity & Renewal"
  - "P08 BO-666 Accreditation Programme Setup"
summary: The validity and renewal rules of a programme
description: |-
  **Added 4 October 2026 (CHG-FXC-010; VM-BO-669, BO-666): `setAccreditationValidity` is a whole-record PUT that
  nothing read.** Returns the programme's `accreditation.validity` row at the caller's venue, or the default before the
  first save (`validityKind` eventDuration, `renewalRequiresReverification` true, `onExpiry` revokeAccess, the schema's
  own defaults; no months, renewal window or grace period).
tags:
- accreditation
x-ticvai-permission: ACCREDITATION_VIEW
x-ticvai-audience:
- staff
x-ticvai-scope-level: venue
x-ticvai-read-routing: replica
x-ticvai-offline-capable: false
x-ticvai-conflict-policy: serverWins
parameters:
- name: programmeId
  in: query
  required: true
  schema:
    type: string
    format: uuid
responses:
  '200':
    description: The validity rules
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/AccreditationValidity'
  '404':
    $ref: '../shared/common.yaml#/components/responses/NotFound'
  '429':
    $ref: '../shared/common.yaml#/components/responses/TooManyRequests'
""")
LINEAGE["getAccreditationValidity"] = (["accreditation.validity"], [], [], [], "reads what setAccreditationValidity stores")

# [plan -> contracts] requests (CHG-FXC-010)
E(Y.insert_after_in_op, C("satellite/payments.yaml"), "receivePaymentProviderWebhook",
  "      x-ticvai-conflict-policy: append", """
parameters:
- name: connectionId
  in: query
  required: false
  description: '**The provider connection this webhook belongs to** (4 October 2026, CHG-FXC-010): the
    `payments.provider_connection` id, which `createPaymentProviderConnection` puts into the webhook URL it registers
    with the provider. The tenant is the cell the request reached (the tenant''s API host, `resolveTenantHost`); the
    connection is this id within it; its signing secret then verifies the body. Unknown, absent or of another
    provider: 404 with no detail, and nothing is read from the body.'
  schema:
    type: string
    format: uuid
""", 6)
LINEAGE["receivePaymentProviderWebhook"] = (["payments.provider_connection"], [], [], [],
                                            "the connection named by connectionId and its signing secret")
LINEAGE["listTenantCells"] = (["control.cell_tenant"], [], [], [], "Cell.tenant_id is retired (ADR-0039 section 4)")

# The item tables' old self-pointers, left behind as relationship-graph columns when the container moved to a table of
# its own (derive-schema reads a qualified name as the child table's column).
E(Y.replace_in_schema, WL, "NavigationConfig",
  "x-ticvai-persistence: whitelabel.navigation_config + whitelabel.navigation_item\n",
  "x-ticvai-persistence: whitelabel.navigation_config + whitelabel.navigation_item\n"
  "      x-ticvai-retired-columns:\n      - whitelabel.navigation_item.navigation_item_id\n")
E(Y.replace_in_schema, WL, "HomepageLayout",
  "x-ticvai-persistence: whitelabel.homepage_layout + whitelabel.homepage_section\n",
  "x-ticvai-persistence: whitelabel.homepage_layout + whitelabel.homepage_section\n"
  "      x-ticvai-retired-columns:\n      - whitelabel.homepage_section.homepage_section_id\n")

LINEAGE.update({
    "updateMessageTemplate": (["cache:idempotency"], ["cache:idempotency", "marketing.message_template_version"], [], [],
                              "every change is a new template version"),
    "updateLoyaltyProgramme": (["cache:idempotency"], ["cache:idempotency"], ["marketing.programme_tier"], [],
                               "earning rules replaced; tiers are not changed here"),
    "listVisualAccessRules": (["access.admission_rules", "access.entry_rule_point"], [], [], [],
                              "the rules setVisualAccessRule writes"),
    "getMembershipProductValidation": (["subscription.membership_product", "subscription.membership_product_history",
                                        "subscription.membership_eligibility_rule", "subscription.membership_entitlement",
                                        "subscription.membership_household_policy",
                                        "subscription.membership_renewal_policy",
                                        "subscription.membership_usage_policy", "approvals.request", "catalogue.product"],
                                       [], [], [], "what approveMembershipProductValidation checks"),
})
NEW_TABLES = {"inventory.daily_count_list", "control.developer_member", "promotions.code_assignment",
              "maintenance.incident_history", "identity.guest_credential"}


def apply_lineage(apply: bool) -> int:
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    lin = json.load(io.open(path, encoding="utf-8"))
    sref = json.load(io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8"))["cols"]
    n = 0
    for op, (r_add, w_add, w_del, r_del, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:  # a new operation: derive-lineage adds it first, then a second run fills it
            continue
        for t in r_add + w_add:
            if t not in sref and t not in NEW_TABLES:
                raise SystemExit("%s: %s is not a table" % (op, t))
        reads = (set(e.get("reads") or []) | set(r_add)) - set(r_del)
        writes = (set(e.get("writes") or []) | set(w_add)) - set(w_del)
        if sorted(reads) != sorted(e.get("reads") or []) or sorted(writes) != sorted(e.get("writes") or []):
            e["reads"], e["writes"] = sorted(reads), sorted(writes)
            e["fixNote"] = "4 October 2026 (CHG-FXC-004): " + why
            n += 1
        # An entry that now writes a table is no longer `pure`; one that now writes none says why.
        if e.get("pure") and [t for t in e["writes"] if ":" not in t]:
            del e["pure"]
            n += 1
        if not [t for t in e["writes"] if ":" not in t] and e.get("verb") != "GET" and not e.get("pure"):
            e["pure"] = why
            n += 1
    if apply:
        io.open(path, "w", encoding="utf-8").write(json.dumps(lin, indent=1, ensure_ascii=False))
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not a.apply:
        print("%d contract edits and %d lineage entries listed; pass --apply" % (len(EDITS), len(LINEAGE)))
        return 0
    changed = 0
    for fn, args in EDITS:
        if fn(*args):
            changed += 1
    print("contract edits applied: %d of %d (the rest were already in place)" % (changed, len(EDITS)))
    print("lineage entries changed: %d" % apply_lineage(True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
