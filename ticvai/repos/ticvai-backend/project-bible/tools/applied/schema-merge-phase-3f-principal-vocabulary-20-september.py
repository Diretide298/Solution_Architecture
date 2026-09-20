#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eleven columns that say `user` where this package says `principal`, and all eleven point nowhere real.

**There is no `identity.user` table.** The user is `identity.principal`, and 133 columns across
the package spell it that way — `created_by_principal_id`, `closed_by_principal_id`,
`set_by_principal_id`, `rota_assignment.principal_id`. The merge brought in eleven that do not,
and the convention matcher resolved every one of them to the wrong table:

    *_user_id            -> identity.user_access   because `user` is a unique PREFIX of
                                                   `user_access` once no `identity.user` exists
    *_user_account_id    -> ledger.account         because `account` is a unique SUFFIX

**`identity.user_access.user_id` resolves to `identity.user_access`** — a grant whose subject is
another grant. **`identity.user_access.granted_by_user_account_id` resolves to `ledger.account`**
— the person who granted a permission, pointing at a general-ledger account.

`derive-relationships` documents this hazard in its own comment: *"a stem may be a prefix of the
table name as well as the whole of it"*, added because `developer_id` needs to reach
`control.developer_account`. The rule is right and the input was wrong. **A prefix rule cannot
tell a missing table from a differently-named one** — it can only find the nearest thing, and the
nearest thing to `user` was a table about users rather than a table of them.

## Why rename rather than declare the reference

Declaring `references: identity.principal` on each column would fix the graph and leave the
package with two words for one thing. The vocabulary is the point: a developer reading
`granted_by_user_account_id` beside `closed_by_principal_id` has to ask whether they are the same
kind of identity, and the answer is yes. **This is the same finding as the permission bootstrap** —
the two sides had two vocabularies for identity and they share no keys.

Renaming also makes the convention matcher *right* rather than overridden, so the next table
somebody adds gets the correct edge for free.

    access.access_change.changed_by_user_id              -> changed_by_principal_id
    identity.membership_history.changed_by_user_account_id -> changed_by_principal_id
    identity.refresh_token.user_id                       -> principal_id
    identity.user_access.user_id                         -> principal_id
    identity.user_access.granted_by_user_account_id      -> granted_by_principal_id
    identity.user_access.revoked_by_user_account_id      -> revoked_by_principal_id
    inventory.supplier_contract.created_by_user_id       -> created_by_principal_id
    marketing.review_response.responded_by_user_id       -> responded_by_principal_id
    orders.upgrade.requested_by_user_id                  -> requested_by_principal_id
    payments.deposit_activity.created_by_user_id         -> created_by_principal_id
    workforce.employee.user_id                           -> principal_id

**`workforce.employee.principal_id` is the one that mattered most.** The rota keys on
`principal_id` and the HR projection keyed on `user_id`, so the only join between a person's
roster and their employment record ran through a table that is neither.

    python3 tools/applied/schema-merge-phase-3f-principal-vocabulary-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")

# (contract file, persistence tag, camelCase old, camelCase new, snake old, snake new)
RENAMES = [
    ("spine/access.yaml", "access.access_change",
     "changedByUserId", "changedByPrincipalId", "changed_by_user_id", "changed_by_principal_id"),
    ("spine/identity.yaml", "identity.membership_history",
     "changedByUserAccountId", "changedByPrincipalId",
     "changed_by_user_account_id", "changed_by_principal_id"),
    ("spine/identity.yaml", "identity.refresh_token",
     "userId", "principalId", "user_id", "principal_id"),
    ("spine/identity.yaml", "identity.user_access",
     "userId", "principalId", "user_id", "principal_id"),
    ("spine/identity.yaml", "identity.user_access",
     "grantedByUserAccountId", "grantedByPrincipalId",
     "granted_by_user_account_id", "granted_by_principal_id"),
    ("spine/identity.yaml", "identity.user_access",
     "revokedByUserAccountId", "revokedByPrincipalId",
     "revoked_by_user_account_id", "revoked_by_principal_id"),
    ("satellite/inventory.yaml", "inventory.supplier_contract",
     "createdByUserId", "createdByPrincipalId",
     "created_by_user_id", "created_by_principal_id"),
    ("satellite/marketing-crm.yaml", "marketing.review_response",
     "respondedByUserId", "respondedByPrincipalId",
     "responded_by_user_id", "responded_by_principal_id"),
    ("spine/orders.yaml", "orders.upgrade",
     "requestedByUserId", "requestedByPrincipalId",
     "requested_by_user_id", "requested_by_principal_id"),
    ("satellite/payments.yaml", "payments.deposit_activity",
     "createdByUserId", "createdByPrincipalId",
     "created_by_user_id", "created_by_principal_id"),
    ("satellite/workforce.yaml", "workforce.employee",
     "userId", "principalId", "user_id", "principal_id"),
]


def schema_span(text, tag):
    """The slice of the file holding the schema that declares this persistence tag."""
    i = text.find("x-ticvai-persistence: %s\n" % tag)
    if i < 0:
        return None, None
    start = text.rfind("\n    ", 0, i) + 1
    nxt = re.search(r"^    [A-Za-z]", text[i:], re.M)
    end = i + (nxt.start() if nxt else len(text) - i)
    return start, end


def main():
    apply = "--apply" in sys.argv[1:]
    texts, done = {}, 0

    for rel, tag, old, new, _s_old, _s_new in RENAMES:
        path = os.path.join(ROOT, "contracts", rel)
        if path not in texts:
            texts[path] = io.open(path, encoding="utf-8").read()
        s = texts[path]
        a, b = schema_span(s, tag)
        if a is None:
            print("    !! %s not found in %s" % (tag, rel))
            return 1
        block = s[a:b]
        # **Only inside this schema.** `userId` is a common property name and a file-wide
        # replace would rewrite unrelated schemas that legitimately carry one.
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(old) + r"(?![A-Za-z])")
        n = len(pat.findall(block))
        if not n:
            if new in block:
                print("    %-40s already %s" % (tag + "." + old, new))
                continue
            print("    !! %s.%s not found in its schema" % (tag, old))
            return 1
        texts[path] = s[:a] + pat.sub(new, block) + s[b:]
        print("    %-46s -> %-26s (%d occurrence(s))" % (tag + "." + old, new, n))
        done += 1

    for path, s in texts.items():
        try:
            yaml.safe_load(s)
        except Exception as e:
            print("    !! %s would not parse: %s" % (os.path.basename(path), str(e)[:140]))
            return 1
    print("    %d file(s) parse" % len(texts))

    # The derived files carry the old column name and the wrong edge with it.
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    cols_fixed = 0
    for _rel, tag, _o, _n, s_old, s_new in RENAMES:
        for c in (S.get("cols") or {}).get(tag, []):
            if c.get("column") == s_old:
                c["column"] = s_new
                # The reference was wrong precisely because the name was.
                c["references"] = "identity.principal"
                c["referenceHow"] = "convention"
                cols_fixed += 1
    print("    schema-reference: %d column(s) renamed and repointed at identity.principal"
          % cols_fixed)

    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    edges = 0
    for r in (G.get("rels") or []):
        for _rel, tag, _o, _n, s_old, s_new in RENAMES:
            if r.get("frm") == tag and r.get("col") == s_old:
                r["col"] = s_new
                r["to"] = "identity.principal"
                r["cross"] = "yes" if tag.split(".")[0] != "identity" else ""
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
    print("  -> %d contract(s) and two handoff files" % len(texts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
