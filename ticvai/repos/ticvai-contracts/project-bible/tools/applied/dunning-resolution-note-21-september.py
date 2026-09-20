#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`resolveDunningCase` accepts a `note` and `DunningCase` has nowhere to put it.

**Found while checking whether BL-100 added anything the RAG index should read.** It did not —
neither dunning table carries retrievable text — and the reason `dunning_case` had none is that
**the note a person writes when they close a case was being accepted and dropped.**

`derive-lineage` computes writes from the request body, so the field was real enough to be read by
a tool and not real enough to survive. The failure it produces is specific: the operation's own
description argues that `writeOff`, `paidByOtherMeans` and `cardReplaced` *"must be told apart
afterwards"* — and the enum tells them apart while **the sentence explaining which invoice, which
phone call or whose decision it was goes nowhere.**

**`marketing.case.resolution_note` is the package's own precedent** and is one of the eleven RAG
sources precisely because a resolution note is the most useful free text a support record holds.

    python3 tools/applied/dunning-resolution-note-21-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAY = os.path.join(ROOT, "contracts", "satellite", "payments.yaml")

OLD = """        resolution:
          type: string
          nullable: true
          enum:
          - paidByOtherMeans
          - cardReplaced
          - writeOff
          - cancelledByGuest
          - null
"""

NEW = """        resolution:
          type: string
          nullable: true
          enum:
          - paidByOtherMeans
          - cardReplaced
          - writeOff
          - cancelledByGuest
          - null
        resolutionNote:
          type: string
          nullable: true
          maxLength: 500
          description: >
            **What `resolveDunningCase` was told, which had nowhere to land until now.** The enum
            above tells `writeOff` from `cardReplaced`; **which invoice, whose phone call and on
            what authority is the sentence beside it**, and the operation's own reasoning — that
            these reasons must be told apart afterwards — only works if the sentence survives.

            **Same shape as `marketing.case.resolution_note`**, which is a RAG source for exactly
            this reason: a resolution note is the most useful free text a support record holds.
        resolvedByPrincipalId:
          type: string
          format: uuid
          nullable: true
          readOnly: true
          description: >
            **Who closed it.** A write-off with no name against it is the one resolution nobody
            can follow up, and it is also the one that moves money.
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(PAY, encoding="utf-8").read()

    if "resolutionNote:" in s:
        print("  already applied")
        return 0
    if s.count(OLD) != 1:
        print("  !! DunningCase.resolution matched %d times" % s.count(OLD))
        return 1
    s = s.replace(OLD, NEW, 1)
    print("    DunningCase  +resolutionNote, +resolvedByPrincipalId")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("  !! refs %s and does not define it" % ref)
            return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    print("    payments.yaml  parses, refs resolve, %d operations" % parsed_n)

    body = (doc["paths"]["/dunning-cases/{caseId}/resolve"]["post"]["requestBody"]
            ["content"]["application/json"]["schema"]["properties"])
    props = doc["components"]["schemas"]["DunningCase"]["properties"]
    dropped = [k for k in body if k not in props and k + "Note" not in props
               and ("note" not in k or "resolutionNote" not in props)]
    if dropped:
        print("  !! request fields with nowhere to land: %s" % dropped)
        return 1
    print("    every field resolveDunningCase accepts now has a column")

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PAY, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/payments.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
