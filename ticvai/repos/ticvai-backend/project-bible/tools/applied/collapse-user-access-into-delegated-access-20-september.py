#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A second grant table, which would have been a security hole, and the audit that missed it.

**I wired `identity.user_access` this morning and it is `identity.delegated_access` with six
columns missing.**

    identity.user_access       principal_id, role_id, permission_id, scope_path, effect,
                               valid_from, valid_to, granted_by_principal_id, revoked_at,
                               revoked_by_principal_id
    identity.delegated_access  all of the above, plus subject_id, over_subject_id,
                               over_object_ref, delegation_kind, quota, is_revocable_by_subject
                               — **and 17 operations**

`CreateGrantRequest` already takes `principalId`, `roleId`, `permission`, `scopePath`, `effect`,
`validFrom`, `validTo` and persists to `delegated_access`. `listDelegatedAccess` is summarised
*"List grants for a principal or role"* and takes a `principalId` parameter. **My
`/principals/{principalId}/access` was that endpoint again.**

## Why this one mattered more than the other duplicates

**`resolvePermissions`, `login` and `getCurrentSession` all read `identity.delegated_access` and
none of them reads `identity.user_access`.**

So a grant written through `setPrincipalAccess` would have been invisible to permission
resolution — and `effect` carries DENY. **A deny that the resolver never reads is a permission
somebody believes is revoked and is not.** Every other duplicate found today wasted a table; this
one would have shipped a security hole, and it would have looked like a feature.

Two grant tables cannot both be right, whichever way the collapse goes: one resolver has to read
one table, or every reader has to remember both and the one that forgets is the vulnerability.

## What is kept from it

    permissionId   `delegated_access.permission` is free text. **`identity.permission` is the
                   catalogue wired today** — the one that answers "154 permission keys on
                   operations, 35 in roles.yaml, 0 shared". A grant that names a catalogue row
                   can be checked; a grant that names a string cannot
    revokedAt      `delegated_access` has `revoked_by` and no `revoked_at`, so it could say who
                   revoked a grant and not when

## Why `audit-duplicate-tables` missed it

Column overlap was 0.26 against a floor of 0.34 — **just under**, because the tool compared
column names literally: `permission_id` against `permission`, `granted_by_principal_id` against
`granted_by`, `revoked_by_principal_id` against `revoked_by`. Three of the strongest signals
scored zero for being spelled differently.

**Two changes, both in the tool.** Column names are compared with a trailing `_id` and a
`_principal` infix stripped, and the test is no longer symmetric: what matters is how much of the
**suspect** the original covers, not how much they share. A rich original containing a poor
duplicate whole is the exact shape being hunted, and Jaccard punishes it for being rich.

Rescored: 8 of 9 columns covered, 0.89.

    python3 tools/applied/collapse-user-access-into-delegated-access-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")
IDN = os.path.join(ROOT, "contracts", "spine", "identity.yaml")

ADD = """        permissionId:
          type: string
          format: uuid
          nullable: true
          description: >
            **Taken from `identity.user_access`, 20 September, when that table was collapsed into
            this one.** `permission` above is free text; this names a row in
            `identity.permission`, the catalogue wired the same day. A grant that names a
            catalogue row can be checked against the keys the contracts actually enforce — which
            is the whole point of a catalogue that reported *154 on operations, 35 in roles.yaml,
            0 shared*.

            Nullable because a role grant carries no permission at all.
        revokedAt:
          type: string
          format: date-time
          nullable: true
          readOnly: true
          description: >
            Taken from `identity.user_access`. This table recorded `revokedBy` and not when, so
            it could say who revoked a grant and not whether it was before or after the thing
            somebody is asking about.
"""


def cut_schema(text, name):
    m = re.search(r"^    %s:\n" % re.escape(name), text, re.M)
    if not m:
        return text, False
    nxt = re.search(r"^    [A-Za-z]", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    return text[:m.start()] + text[end:], True


def cut_path(text, header):
    """**Bounded by `components:` as well as by the next path.**

    Searching only for the next `^  /` means a path that happens to be the LAST one before
    `components:` cuts to the end of the file — every schema, every security scheme, gone. The
    file then still parses as a document with no components, and the next thing to run reports
    a hundred missing `$ref`s rather than the one deletion that caused them.
    """
    i = text.find(header)
    if i < 0:
        return text, False
    rest = text[i + len(header):]
    stops = [m.start() for m in (re.search(r"^  /", rest, re.M),
                                 re.search(r"^components:", rest, re.M)) if m]
    end = i + len(header) + (min(stops) if stops else len(rest))
    return text[:i] + text[end:], True


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(IDN, encoding="utf-8").read()

    s, cut = cut_path(s, "  /principals/{principalId}/access:\n")
    print("    /principals/{principalId}/access  %s"
          % ("removed — listDelegatedAccess is this endpoint" if cut else "not present"))

    s, cut = cut_schema(s, "IdentityUserAccess")
    print("    IdentityUserAccess                %s" % ("removed" if cut else "not present"))

    if "permissionId" in s[s.find("    DelegatedAccess:"):s.find("    DelegatedAccess:") + 3000]:
        print("    DelegatedAccess                   already has permissionId")
    else:
        i = s.find("x-ticvai-persistence: identity.delegated_access\n")
        j = s.find("        validFrom:\n", i)
        if j < 0:
            print("    !! DelegatedAccess.subjectId anchor not found")
            return 1
        s = s[:j] + ADD + s[j:]
        print("    DelegatedAccess                   +permissionId, +revokedAt")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("    !! identity.yaml would not parse: %s" % str(e)[:180])
        return 1
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("    !! identity.yaml refs %s and does not define it" % ref)
            return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("    !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    print("    identity.yaml parses, refs resolve, no operation discarded")

    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    dropped = 0
    for section in ("cols", "origin", "storage", "store", "lineage"):
        d = S.get(section)
        if isinstance(d, dict) and d.pop("identity.user_access", None) is not None:
            dropped += 1
    print("    schema-reference: %d section entr(y/ies) dropped" % dropped)

    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    before = len(G.get("rels") or [])
    G["rels"] = [r for r in (G.get("rels") or [])
                 if r.get("frm") != "identity.user_access" and r.get("to") != "identity.user_access"]
    for key in ("tab_ops", "tab_screens"):
        (G.get(key) or {}).pop("identity.user_access", None)
    print("    relationship-graph: %d edge(s) dropped" % (before - len(G["rels"])))

    lp = os.path.join(H, "api-data-lineage.json")
    L = json.load(io.open(lp, encoding="utf-8"))
    for o in ("listPrincipalAccess", "setPrincipalAccess"):
        if L.pop(o, None) is not None:
            print("    lineage: removed %s" % o)
    cleaned = 0
    for op, v in L.items():
        for k in ("reads", "writes"):
            row = v.get(k) or []
            keep = [t for t in row if t != "identity.user_access"]
            if len(keep) != len(row):
                v[k] = keep
                cleaned += 1
    print("    lineage: %d entr(y/ies) cleaned" % cleaned)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(IDN, "w", encoding="utf-8", newline="\n").write(s)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    io.open(gp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(G, indent=1, ensure_ascii=False))
    io.open(lp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(L, indent=1, ensure_ascii=False))
    print("  -> identity.yaml and three handoff files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
