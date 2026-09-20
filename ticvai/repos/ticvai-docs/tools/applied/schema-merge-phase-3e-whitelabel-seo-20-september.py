#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two more tables that already existed, and this pair goes the other way.

`audit-duplicate-tables.py` found `whitelabel.seo_setting` against `control.seo_metadata` (0.588
column overlap) and `whitelabel.redirect` against `control.url_redirect` (0.375). **The tool
reports a pair; which one survives is a judgement**, and here it is not the same direction as the
catalogue collapse — there, ours won because it was richer and wired; here, ours wins for a
different reason and it is worth saying which.

    control.seo_metadata     **traced to requirements 22.11.1-22.11.12 and CF-137.** `entityKind`
                             is a typed enum over contentPage, product, event, performance,
                             membership, promotion and venue — so SEO attaches to a ticket as
                             well as to a page. `keywords` is a typed array
    whitelabel.seo_setting   scoped to a `tenant_config_id`, with `hreflang_json` and
                             `open_graph_json` as blobs

**Their table adds nothing ours does not already have.** Every column matches, including the five
that looked like additions — `hreflang`, `schema_org_type`, `open_graph`, `is_auto_generated`,
`no_index` are all on `control.seo_metadata` already. The only genuine difference is
`tenant_config_id` against `scope_path`, and `scope_path` is the package's partition key (ADR-0005)
rather than a second foreign key to a config row.

**A json blob against a typed field is the argument this merge has made all along** — it is why
`selected_modifiers_json` was declined on the F&B order and why `channels_json` was declined on
the price list.

## The redirect

    control.url_redirect     **22.11.7**, and it knows about redirect chains: *"a new redirect
                             whose target is itself a redirect is collapsed rather than
                             appended"*. `reason` is an enum, `statusCode` is constrained to
                             301/302/307/308
    whitelabel.redirect      the same columns under different names, plus timestamps

**`createdAt` is taken.** Ours counts hits and cannot say when the redirect was added, so a
table that exists to record a site's history had no date on its own rows.

`updatedAt` is not taken: a redirect's target changing is a new row by the chain-collapsing rule
above, not an edit.

    python3 tools/applied/schema-merge-phase-3e-whitelabel-seo-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")
WL = os.path.join(ROOT, "contracts", "satellite", "white-label.yaml")
CRM = os.path.join(ROOT, "contracts", "satellite", "marketing-crm.yaml")

DROP_SCHEMAS = ["WhitelabelRedirect", "WhitelabelSeoSetting"]
DROP_TABLES = ["whitelabel.redirect", "whitelabel.seo_setting"]

ADD = """        createdAt:
          type: string
          format: date-time
          readOnly: true
          nullable: true
          description: >
            **Taken from their `whitelabel.redirect`, 20 September.** This table counts hits and
            could not say when a redirect was added — a record of a site's history with no date
            on its own rows. Ours had `hitCount` and no timestamp of any kind.
"""


def cut_schema(text, name):
    m = re.search(r"^    %s:\n" % re.escape(name), text, re.M)
    if not m:
        return text, False
    nxt = re.search(r"^    [A-Za-z]", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    return text[:m.start()] + text[end:], True


def main():
    apply = "--apply" in sys.argv[1:]

    w = io.open(WL, encoding="utf-8").read()
    for name in DROP_SCHEMAS:
        w, hit = cut_schema(w, name)
        print("    %-22s %s" % (name, "removed" if hit else "not found"))
    try:
        yaml.safe_load(w)
    except Exception as e:
        print("    !! white-label.yaml would not parse: %s" % str(e)[:140])
        return 1
    print("    white-label.yaml parses")

    c = io.open(CRM, encoding="utf-8").read()
    i = c.find("x-ticvai-persistence: control.url_redirect\n")
    if i < 0:
        print("    !! control.url_redirect schema not found")
        return 1
    if "createdAt" in c[i:i + 2200]:
        print("    control.url_redirect   already has createdAt")
    else:
        j = c.find("        hitCount:\n", i)
        if j < 0:
            print("    !! hitCount anchor not found")
            return 1
        c = c[:j] + ADD + c[j:]
        print("    control.url_redirect   +createdAt")
    try:
        yaml.safe_load(c)
    except Exception as e:
        print("    !! marketing-crm.yaml would not parse: %s" % str(e)[:140])
        return 1
    print("    marketing-crm.yaml parses")

    sp = os.path.join(H, "schema-reference.json")
    S = json.load(io.open(sp, encoding="utf-8"))
    dropped = 0
    for section in ("cols", "origin", "storage", "store", "lineage"):
        d = S.get(section)
        if isinstance(d, dict):
            for t in DROP_TABLES:
                if d.pop(t, None) is not None:
                    dropped += 1
    print("    schema-reference: %d section entr(y/ies) dropped" % dropped)

    gp = os.path.join(H, "relationship-graph.json")
    G = json.load(io.open(gp, encoding="utf-8"))
    before = len(G.get("rels") or [])
    G["rels"] = [r for r in (G.get("rels") or [])
                 if r.get("frm") not in DROP_TABLES and r.get("to") not in DROP_TABLES]
    for key in ("tab_ops", "tab_screens"):
        for t in DROP_TABLES:
            (G.get(key) or {}).pop(t, None)
    print("    relationship-graph: %d edge(s) dropped" % (before - len(G["rels"])))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(WL, "w", encoding="utf-8", newline="\n").write(w)
    io.open(CRM, "w", encoding="utf-8", newline="\n").write(c)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    io.open(gp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(G, indent=1, ensure_ascii=False))
    print("  -> white-label.yaml, marketing-crm.yaml and two handoff files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
