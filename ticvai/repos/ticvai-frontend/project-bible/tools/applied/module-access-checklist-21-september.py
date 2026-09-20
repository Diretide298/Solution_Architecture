#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grant access to a module by ticking what a person may do in it.

**Decided 21 September, Chinmay.** *"The roles of the modules are not really defined... How about,
while creating a user or granting them access to a module, we have a checklist of things they can
do in that module?"*

**A role taxonomy is the part nobody can agree, and this removes the need for one.** Supervisor,
Manager, Lead — each venue means something different by them, and the argument is never about the
name, it is about whether that person may void a transaction. **The checklist asks that question
directly.** `handoff/module-capabilities.json` already derives the answer set: 232 capability pairs
across 32 modules, from the 167-key vocabulary crossed with every contract's
`x-ticvai-permission`.

## Three things this contract does that a role model could not

**1 · A role becomes a saved checklist rather than a prerequisite.** `CapabilityTemplate` is a
named tick-set a venue can reuse. **Applying one copies the ticks; it does not bind to it** — so
editing a template never silently widens access somebody already holds, which is the failure mode
that makes role hierarchies frightening to change.

**2 · "Not everyone can change this" is a property of the capability, not a rank.** `elevated` is
derived: a capability is elevated because an operation behind it already declares
`x-ticvai-step-up`, not because its name sounds dangerous. Ticking one raises an `approvals`
request instead of taking effect — which is where 11.1.24 already lives, so *a requester may never
approve their own request* applies without being restated.

**3 · Segregation is checked at the tick, not discovered later.** `SegregationRule` says which
permissions one person may not hold at once; `setPrincipalModuleAccess` answers 409 naming the
rule and the conflicting capability. **The person granting access finds out while they are
deciding**, rather than in a violation report a month later.

## And it settles the 167-against-44 conflict

`roles.yaml` holds 44 lowercase POS keys sharing zero with the 167, so `check-screens` could only
validate POS guards. The conflict was framed as *reconcile two vocabularies*. **There is one
vocabulary — the 167 — and `roles.yaml` is a saved checklist for one surface that was mistaken for
the alphabet.** It becomes the first `CapabilityTemplate`.

    python3 tools/applied/module-access-checklist-21-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDN = os.path.join(ROOT, "contracts", "spine", "identity.yaml")

PATH_ANCHOR = "  /segregation-rules:\n"

PATHS = """  /module-capabilities:
    get:
      operationId: listModuleCapabilities
      x-ticvai-consumed-by:
        - "P08 BO-1066 Roles, Permissions & Masking"
      summary: What a person can be allowed to do, per module
      description: '3.3.5, BL-110. **The checklist a grant screen renders**, and the reason the
        package does not need a role taxonomy first.

        **Derived, not authored** (`handoff/module-capabilities.json`): the 167-key vocabulary in
        `contracts/shared/permissions.yaml` crossed with every contract''s
        `x-ticvai-permission`. 232 capability pairs across 32 modules, and adding an operation
        with a permission adds it to the right checklist by existing.

        **`label` may be null and the client must render the key when it is.** 72 permissions
        carry no description yet; a generated sentence would read like a label and mean nothing,
        and **a checklist item nobody understands gets ticked anyway.**

        '
      tags:
      - administration
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      parameters:
      - name: module
        in: query
        description: A contract name. Omitted returns every module.
        schema:
          type: string
      responses:
        '200':
          description: Modules and their capabilities
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ModuleCapabilitySet'
  /principals/{principalId}/module-access:
    parameters:
    - name: principalId
      in: path
      required: true
      schema:
        type: string
        format: uuid
    get:
      operationId: getPrincipalModuleAccess
      x-ticvai-consumed-by:
        - "P08 BO-1066 Roles, Permissions & Masking"
      summary: What this person may do, as ticks
      description: 'BL-110. **The same shape the grant screen writes**, so what an administrator
        sees when they open it is what they saved. A read that returns a different structure from
        the write is how an interface grows a translation layer nobody maintains.

        '
      tags:
      - administration
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: venue
      x-ticvai-read-routing: primary
      responses:
        '200':
          description: Access
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ModuleAccess'
    put:
      operationId: setPrincipalModuleAccess
      x-ticvai-consumed-by:
        - "P08 BO-1066 Roles, Permissions & Masking"
      summary: Tick what they may do
      description: 'BL-110, 3.3.5. **The whole grant, replaced.** A partial update would make
        "everything else stays as it was" a claim the caller cannot verify, and access is the one
        setting where a silent survivor is a breach.

        **Segregation is checked here, while the person is deciding.** `SegregationRule` says
        which permissions one principal may not hold at once; a tick that would create a conflict
        is refused with 409 naming the rule and the other capability — rather than appearing in a
        violation report a month later, which is the same finding arriving too late to act on.

        **An `elevated` capability raises an approval rather than taking effect.** The response is
        202 with the request id when any tick is elevated, 200 when none is. Routed through
        `approvals` so that 11.1.24 — *a requester may never approve their own request* — applies
        without being restated here.

        '
      tags:
      - administration
      x-ticvai-permission: PERMISSION_GRANT
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
              type: array
              items:
                $ref: '#/components/schemas/ModuleAccess'
      responses:
        '200':
          description: Granted
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ModuleAccess'
        '202':
          description: '**Raised for approval**, because at least one capability is elevated.'
          content:
            application/json:
              schema:
                type: object
                properties:
                  approvalRequestId:
                    type: string
                    format: uuid
                  elevatedCapabilities:
                    type: array
                    items:
                      type: string
        '409':
          description: '**A tick would breach a segregation rule.** Names the rule and the
            capability already held, so the person deciding can narrow one rather than guess.'
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
  /capability-templates:
    get:
      operationId: listCapabilityTemplates
      x-ticvai-consumed-by:
        - "P08 BO-1066 Roles, Permissions & Masking"
      summary: Saved tick-sets
      description: '3.3.23, BL-110. **A role, without the taxonomy.** *Duty Manager* is a named
        set of ticks somebody saved because they grant it often — useful, and **not a thing access
        depends on.**

        **Applying a template copies its ticks and does not bind to them.** Editing one never
        widens access somebody already holds, which is what makes a role hierarchy frightening to
        change and is why most of them are never changed.

        '
      tags:
      - administration
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      responses:
        '200':
          description: Templates
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CapabilityTemplate'
    put:
      operationId: setCapabilityTemplate
      x-ticvai-consumed-by:
        - "P08 BO-1066 Roles, Permissions & Masking"
      summary: Save a tick-set under a name
      tags:
      - administration
      x-ticvai-permission: ROLE_MANAGE
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
              $ref: '#/components/schemas/CapabilityTemplate'
      responses:
        '200':
          description: Saved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CapabilityTemplate'
"""

SCHEMA_ANCHOR = "    SegregationRule:\n      type: object\n"

SCHEMAS = """    ModuleCapability:
      type: object
      x-ticvai-persistence: none — derived from contracts/shared/permissions.yaml and every contract
      description: >
        BL-110. **One tickable thing a person can be allowed to do in a module.** Derived rather
        than authored, so an operation added with a permission appears on the right checklist by
        existing rather than by somebody remembering.
      required:
      - key
      properties:
        key:
          type: string
          description: >
            **The permission string, and the only vocabulary there is.** `roles.yaml` holds 44
            lowercase keys sharing none of these; that file is a saved tick-set for the POS
            surface which was mistaken for the alphabet, and it becomes a `CapabilityTemplate`.
        label:
          type: string
          nullable: true
          description: >
            **Null where the permission has no description yet, and the client renders the key.**
            72 of them are in that state. **A generated sentence would read like a label and mean
            nothing** — and a checklist item nobody understands is ticked anyway, which is worse
            than one that visibly needs explaining.
        group:
          type: string
          nullable: true
          description: The heading it sits under in the vocabulary — Selling, Access control, Shift
            and cash. **How a checklist of forty items stays readable.**
        operationCount:
          type: integer
          description: >
            **How much this tick actually grants.** A capability behind ninety operations and one
            behind two are different decisions, and the number is the only honest way to say so on
            a screen.
        elevated:
          type: boolean
          default: false
          description: >
            **Derived: at least one operation behind it declares `x-ticvai-step-up`.** Not a rank
            and not a judgement about the name — the operation already said it needs a second
            factor. Ticking one raises an approval rather than taking effect.
        segregationConstrained:
          type: boolean
          default: false
          description: >
            **Named in a `SegregationRule`.** Ticking it may conflict with something the principal
            already holds, and `setPrincipalModuleAccess` answers 409 rather than letting it
            through.

    ModuleCapabilitySet:
      type: object
      description: BL-110. One module and everything a person could be allowed to do in it.
      properties:
        module:
          type: string
        title:
          type: string
        unguardedOperations:
          type: integer
          description: >
            **Operations in this module that carry no permission, and so appear on no checklist.**
            94 across the package — guest-facing, service-to-service or self-scoped. Stated
            because a checklist that silently omits a third of a module reads as complete.
        capabilities:
          type: array
          items:
            $ref: '#/components/schemas/ModuleCapability'

    ModuleAccess:
      x-ticvai-persistence: identity.module_access
      type: object
      description: >
        BL-110. **What one principal may do in one module, at one scope.** The unit the grant
        screen writes and reads back unchanged.
      required:
      - module
      - scopePath
      - capabilities
      properties:
        principalId:
          type: string
          format: uuid
          readOnly: true
        module:
          type: string
        scopePath:
          type: string
          description: >
            **Where, and it is half the grant** (ADR-0018). A capability means nothing until it is
            held at a scope containing the thing it acts on — holding `ORDER_REFUND` at one venue
            is not holding it at another, and the checklist is per scope for that reason.
        capabilities:
          type: array
          items:
            type: string
          description: >
            **Permission keys, ticked.** The complete set for this module and scope: what is
            absent is not granted, which is what makes the write replaceable and the read
            verifiable.
        appliedTemplate:
          type: string
          nullable: true
          description: >
            **Which saved tick-set this was copied from, for the record only.** It is not a
            binding: the ticks are the grant, and editing the template afterwards changes nothing
            here. A grant that silently follows a template is a grant nobody can audit at a point
            in time.
        grantedByPrincipalId:
          type: string
          format: uuid
          readOnly: true
        grantedAt:
          type: string
          format: date-time
          readOnly: true

    CapabilityTemplate:
      x-ticvai-persistence: identity.capability_template
      type: object
      description: >
        3.3.23, BL-110. **A named tick-set — a role, with nothing depending on the name.**
      required:
      - code
      - name
      - capabilities
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        code:
          type: string
          maxLength: 64
        name:
          type: string
          maxLength: 200
        description:
          type: string
          nullable: true
        capabilities:
          type: array
          items:
            type: string
        scopePath:
          type: string
          description: '**The partition key** (ADR-0005). Written at `tenant` scope.'

"""


def check(s, label):
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


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(IDN, encoding="utf-8").read()

    if "listModuleCapabilities" in s:
        print("  already applied")
        return 0

    for label, old, new in (("+listModuleCapabilities, +get/setPrincipalModuleAccess, "
                             "+list/setCapabilityTemplate", PATH_ANCHOR, PATHS + PATH_ANCHOR),
                            ("+ModuleCapability, +ModuleCapabilitySet, +ModuleAccess, "
                             "+CapabilityTemplate", SCHEMA_ANCHOR, SCHEMAS + SCHEMA_ANCHOR)):
        if s.count(old) != 1:
            print("  !! anchor matched %d times for %s" % (s.count(old), label))
            return 1
        s = s.replace(old, new, 1)
        print("    %s" % label)

    doc = check(s, "identity.yaml")
    if doc is None:
        return 1

    S = doc["components"]["schemas"]
    if S["ModuleAccess"]["properties"]["appliedTemplate"].get("nullable") is not True:
        print("  !! appliedTemplate is not optional — a grant would depend on a template")
        return 1
    if "capabilities" not in (S["ModuleAccess"].get("required") or []):
        print("  !! ModuleAccess does not require its tick set")
        return 1
    if str(S["ModuleCapability"].get("x-ticvai-persistence", "")).split("—")[0].strip() != "none":
        print("  !! ModuleCapability is persisted — the checklist would stop being derived")
        return 1
    print("    checklist derived · ticks are the grant · template is a record, not a binding")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(IDN, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/spine/identity.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
