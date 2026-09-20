#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The permission catalogue, scoped grants, and one table that should never have an API.

Four identity tables were unreachable and they are not one problem.

## `identity.module` and `identity.permission` — the catalogue the package has been missing

Every refresh prints this and nothing acts on it:

    154 permission key(s) on operations · 35 in roles.yaml · 0 shared

**Zero.** The keys the contracts enforce and the keys the roles grant are two vocabularies with
no overlap, so a role cannot be checked against the thing it is supposed to authorise. There has
never been a catalogue of permissions to check against — `identity.role_permission` maps a role
to a key and nothing says which keys exist or what they mean.

`identity.permission` is that catalogue, grouped by `identity.module`. **Read-only over HTTP and
that is deliberate**: a permission key exists because an operation declares
`x-ticvai-permission`, so the catalogue is derived from the contracts, and an API that let
somebody invent a permission would create a key no operation checks.

## `identity.user_access` — the scoped grant with nowhere else to live

`identity.principal.primary_role_id` is a **single** role. `identity.role_permission` is role to
permission. Between them there was no way to say *this person is a Duty Manager at Venue 3 until
March, and is explicitly denied refunds anywhere*.

    principal_id + (role_id | permission_id) + scope_path + effect + valid_from/to

`effect` carries allow and deny, which is why this cannot be folded into a list of roles: a deny
has to outrank an allow it overlaps, and a set of role names cannot express that.

**It was also the most-referenced unreachable table in the package** — eight columns pointed at
it, though that turned out to be the `user_id` mis-resolution rather than eight real users.

## `identity.refresh_token` — storage only, and this is the security control

`schema-storage-only.md` already says why `identity.principal_credential` has no API: *"a
credential hash has no response it belongs in."* **A refresh token hash is the same object.** It
is a bearer credential; returning one over any endpoint, to anyone, defeats rotation.

Revocation already exists and does not need this table exposed — `forceLogout` and `guestLogout`
end sessions, and revoking the tokens behind them is an implementation of that, not a resource.
So it is documented in `schema-storage-only.md` rather than wired, which is what that file is for.

## Three tables no contract has ever declared

`fnb.location_code`, `orders.donation_line` and `orders.order_media_link` hold an `id` and
foreign keys and nothing else. No contract declares them and **`git log -S` finds no commit in
which one ever did.**

They exist because `derive-schema` materialises a table from a relationship edge, and the edge
exists because a column carries `references` — **which `derive-schema` wrote from the graph.**
The two derivers feed each other, which `derive-relationships` calls *"the worst kind of drift:
it looks like progress."* Removed; with no `cols` entry, neither deriver has an input.

    python3 tools/applied/wire-identity-authz-20-september.py --apply
"""
import io
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")
IDN = os.path.join(ROOT, "contracts", "spine", "identity.yaml")
SO = os.path.join(H, "schema-storage-only.md")

PHANTOMS = ["fnb.location_code", "orders.donation_line", "orders.order_media_link"]

PATHS = '''  /modules:
    get:
      operationId: listModules
      summary: The module tree permissions are grouped under
      description: '**Read-only, and that is the point.** A module exists because the product has
        one; inventing modules over an API would create groups no permission belongs to.

        `parentModuleId` builds one tree rather than a fixed two levels, for the same reason
        `ProductCategory` does — a venue that nests its modules differently should not need a schema
        change.

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
          description: Modules
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/IdentityModule'
  /permissions:
    get:
      operationId: listPermissions
      summary: Every permission key the contracts enforce
      description: '**The catalogue that makes a role reviewable.** Every refresh reports *154
        permission keys on operations, 35 in roles.yaml, 0 shared* — the keys the contracts enforce
        and the keys the roles grant have been two vocabularies with no overlap, and nothing could
        reconcile them because there was no list of what exists.

        **Read-only.** A permission key exists because an operation declares
        `x-ticvai-permission`; this catalogue is derived from the contracts. An endpoint that let
        somebody create one would produce a key no operation checks, which is worse than a missing
        key because it looks granted.

        '
      tags:
      - identity
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      parameters:
      - name: moduleId
        in: query
        schema:
          type: string
          format: uuid
      - name: action
        in: query
        schema:
          type: string
      responses:
        '200':
          description: Permissions
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/IdentityPermission'
  /principals/{principalId}/access:
    get:
      operationId: listPrincipalAccess
      summary: What a principal is granted, and where
      description: '**`identity.principal.primaryRoleId` is one role.** Between that and
        `role_permission` there was no way to say *Duty Manager at Venue 3 until March, and denied
        refunds anywhere*.

        Grants are returned including expired ones by default filter, because **the question asked
        of this endpoint is usually why somebody could do something last Tuesday**, and a view that
        silently drops lapsed grants cannot answer it.

        '
      tags:
      - identity
      x-ticvai-permission: PERMISSION_VIEW
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      x-ticvai-read-routing: replica
      parameters:
      - name: principalId
        in: path
        required: true
        schema:
          type: string
          format: uuid
      - name: activeOn
        in: query
        description: Grants in force at this instant. Omit for all, including lapsed and revoked.
        schema:
          type: string
          format: date-time
      responses:
        '200':
          description: Grants
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/IdentityUserAccess'
    put:
      operationId: setPrincipalAccess
      summary: Replace a principal's grants
      description: '**Set whole, because a deny only means something against the allows it sits
        beside.** Applying grants one at a time opens a window in which a revoked allow is gone and
        its replacing deny is not yet there, or the reverse — and for an access table that window is
        the whole problem.

        Revoking is expressed by omitting a grant, which records `revokedAt` and
        `revokedByPrincipalId` rather than deleting the row. **A grant that is deleted cannot answer
        why somebody had it.**

        '
      tags:
      - identity
      x-ticvai-permission: PERMISSION_GRANT
      x-ticvai-audience:
      - staff
      x-ticvai-scope-level: tenant
      parameters:
      - name: principalId
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
              type: array
              items:
                $ref: '#/components/schemas/IdentityUserAccess'
      responses:
        '200':
          description: Granted
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/IdentityUserAccess'
        '409':
          description: A grant breaches a segregation-of-duties rule
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
'''

STORAGE_ROW = ("| `identity.refresh_token` | **A bearer credential, like "
               "`principal_credential`.** Returning a refresh token hash over any endpoint "
               "defeats rotation. Revocation is `forceLogout` and `guestLogout`, which end a "
               "session; the tokens behind them are an implementation of that, not a resource |\n")


def main():
    apply = "--apply" in sys.argv[1:]

    s = io.open(IDN, encoding="utf-8").read()
    if "operationId: listPermissions" in s:
        print("    identity.yaml already wired")
    else:
        i = s.find("\ncomponents:\n")
        if i < 0:
            print("    !! no components block")
            return 1
        s = s[:i + 1] + PATHS + s[i + 1:]
        try:
            doc = yaml.safe_load(s)
        except Exception as e:
            print("    !! identity.yaml would not parse: %s" % str(e)[:160])
            return 1
        have = set((doc.get("components") or {}).get("schemas") or {})
        missing = [w for w in ("IdentityModule", "IdentityPermission", "IdentityUserAccess")
                   if w not in have]
        if missing:
            print("    !! schema(s) not defined: %s" % ", ".join(missing))
            return 1
        print("    identity.yaml  +listModules, +listPermissions, +listPrincipalAccess, "
              "+setPrincipalAccess")

    # `identity.refresh_token` joins the tables that must have no API.
    so = io.open(SO, encoding="utf-8").read()
    if "identity.refresh_token" in so:
        print("    schema-storage-only.md already records refresh_token")
    else:
        anchor = "| `identity.authz_audit` |"
        j = so.find(anchor)
        if j < 0:
            print("    !! could not find the authz_audit row to insert beside")
            return 1
        so = so[:j] + STORAGE_ROW + so[j:]
        so = so.replace("**Twelve tables are in the migrations and not in the schema reference.**",
                        "**Thirteen tables are in the migrations and not in the schema "
                        "reference.**")
        print("    schema-storage-only.md  +identity.refresh_token")

    # The three tables no contract has ever declared.
    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    dropped = 0
    for section in ("cols", "origin", "storage", "store", "lineage"):
        d = S.get(section)
        if isinstance(d, dict):
            for t in PHANTOMS:
                if d.pop(t, None) is not None:
                    dropped += 1
    print("    schema-reference: %d section entr(y/ies) dropped for %d undeclared table(s)"
          % (dropped, len(PHANTOMS)))

    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    before = len(G.get("rels") or [])
    G["rels"] = [r for r in (G.get("rels") or [])
                 if r.get("frm") not in PHANTOMS and r.get("to") not in PHANTOMS]
    for key in ("tab_ops", "tab_screens"):
        for t in PHANTOMS:
            (G.get(key) or {}).pop(t, None)
    print("    relationship-graph: %d edge(s) dropped" % (before - len(G["rels"])))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(IDN, "w", encoding="utf-8", newline="\n").write(s)
    io.open(SO, "w", encoding="utf-8", newline="\n").write(so)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    io.open(gp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(G, indent=1, ensure_ascii=False))
    print("  -> identity.yaml, schema-storage-only.md and two handoff files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
