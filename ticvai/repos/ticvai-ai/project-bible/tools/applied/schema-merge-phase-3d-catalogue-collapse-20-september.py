#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ten tables that are `catalogue.*` under a domain prefix, and the six columns worth keeping.

**The split was a stated principle and it was never carried out.** The decision log's rubric
leans on it twice — *"the same argument that gave F&B and Retail their own product and price
tables: a flash sale on retail stock must not contend with ticket inventory"* — and decision 1
uses it again against `catalogue.rental_rate`.

What the package actually holds:

    catalogue.product        21 columns   **40 operations**, read by twelve contracts
    fnb.product              12 columns    0 operations
    retail.product           11 columns    0 operations

and the same for `product_category`, `variant`, `price` and `price_list`. **Zero operations on
any of the ten.** No retail operation reads `catalogue.product` either, and `fnb` reads it once,
through `createCombo`. So the contention the split relieves is not in the contracts, while the
cost — three product models, three places to add a field, three names that all read *product* —
is being paid in full.

**A split that relieves contention requires moving the reads, not adding the tables.** Phase 3
added the tables and moved nothing, which is the worst of the two positions: all of the
maintenance cost, none of the isolation. The package already has `x-ticvai-read-routing:
analytical` for contention that turns out to be real.

Scored the same way as every other decision in the log:

    Maintainability   **catalogue** — one product model. A tax rule, an allergen flag or a
                      lifecycle state is one change, not three
    Readability       **catalogue** — three tables named `product` in one package is the
                      failure the naming rules exist to prevent
    Optimised access  **catalogue** — a guest order spanning an F&B item and a retail item is
                      one join today and a union across three product tables afterwards
    DB strain         **the split, in principle** — and nothing exercises it. This is the one
                      criterion the split wins and it wins it hypothetically

This is the `fnb.order` bug at ten times the size, from the same root: phase 3 tested *"already
a table of ours"* by NAME. `fnb.product` was not a name we had; `catalogue.product` is the thing
it is. `audit-duplicate-tables.py` now finds this class without waiting for an accident.

## What their tables found, which we keep

    catalogue.product.categoryId      **`catalogue.product_category` has two operations and
                                      nothing could be filed under it.** A merchandise hierarchy
                                      with no way to attach a product is a table with a tree and
                                      no leaves — their column is the one that makes it work
    catalogue.product.isStockTracked  distinct from `isSellable`: whether a sale decrements
                                      stock. A ticket does not, a bottle of water does
    catalogue.variant.name            `axisValues` gives `{size: L}` and no display string
    catalogue.variant.barcode         `catalogue.alternative_code` is a partner's code for a
                                      variant and **requires `partnerId`**, so an EAN has
                                      nowhere to go. Different cardinality, different home —
                                      and a POS scan is an indexed lookup, not a join
    catalogue.variant.isDefault       which variant a product page opens on
    catalogue.product_category.code   a stable key for import and integration; the table had
                                      only a uuid and a localised name

## What is declined, and why it is not an oversight

    brand              **`ProductCategory.kind` already has `brand`** and `parentId` builds the
                       tree: *"one tree, not four"*. A flat `brand` string on the product is that
                       argument reintroduced as a column
    channels_json      `PriceList.channels` is already an array of the `Channel` enum. A json
                       blob is the worse of the two
    scope_path on      `venueId` is **required** on `PriceList` — a price list belongs to a
    price_list         venue. Adding a second scoping mechanism next to a required one is the
                       maintainability fault this merge has been scoring against
    tax_code           tax lives on `catalogue.price.tax_code_id`, where a rate that changes by
                       price list can differ
    valid_from/to      `catalogue.price_list` carries validity, and `promotions` carries the
    on price           overrides. Per-price validity is a third mechanism for one idea
    type               `catalogue.product.kind` is this column
    attributes_json    `catalogue.variant.axis_values` is this, declared rather than free-form

    python3 tools/applied/schema-merge-phase-3d-catalogue-collapse-20-september.py --apply
"""
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, "handoff")
CAT = os.path.join(ROOT, "contracts", "spine", "catalogue.yaml")
FNB = os.path.join(ROOT, "contracts", "satellite", "fnb.yaml")
RET = os.path.join(ROOT, "contracts", "satellite", "retail.yaml")

DROP = {
    FNB: ["FnbProduct", "FnbProductCategory", "FnbVariant", "FnbPrice", "FnbPriceList"],
    RET: ["RetailProduct", "RetailProductCategory", "RetailVariant", "RetailPrice",
          "RetailPriceList"],
}
DROP_TABLES = ["fnb.product", "fnb.product_category", "fnb.variant", "fnb.price",
               "fnb.price_list", "retail.product", "retail.product_category", "retail.variant",
               "retail.price", "retail.price_list"]

# (anchor property line, block to insert before it) within catalogue.yaml.
ADDITIONS = [
    ("        lifecycleState:\n", """        categoryId:
          type: string
          format: uuid
          nullable: true
          description: >
            **Taken from their `fnb.product` and `retail.product`, 20 September.**
            `catalogue.product_category` has existed since 20 August with two operations and
            nothing could be filed under it — a merchandise hierarchy with a tree and no leaves.
            Their per-domain product tables both carried this column and ours did not.
"""),
    ("        hasVariants:\n", """        isStockTracked:
          type: boolean
          default: false
          description: >
            **Taken from their `fnb.product`, 20 September.** Whether a sale decrements stock,
            which is not what `isSellable` asks. A ticket is sellable and tracks no stock; a
            bottle of water is both. Without it, an F&B sale cannot tell inventory whether to
            move.
"""),
]

VARIANT_ADD = ("        isActive:\n", """        name:
          type: string
          maxLength: 150
          nullable: true
          description: >
            **Taken from their variant tables, 20 September.** `axisValues` gives `{size: L}`
            and no string a guest can read. A menu showing *Large* needs somewhere for the word
            to live.
        barcode:
          type: string
          maxLength: 64
          nullable: true
          description: >
            **Taken from their variant tables, 20 September.** `catalogue.alternative_code` is a
            partner's own code for a variant and **requires `partnerId`**, so a manufacturer's
            EAN had nowhere to go. One per variant against many per variant is a different
            cardinality and belongs in a different place — and a POS scan should be an indexed
            column lookup, not a join.
        isDefault:
          type: boolean
          default: false
          description: >
            Taken from their variant tables. Which variant a product page opens on. Ours had no
            way to say, so a three-size drink opened on whichever row sorted first.
""")

CATEGORY_ADD = ("        nameLocalised:\n", """        code:
          type: string
          maxLength: 64
          nullable: true
          description: >
            **Taken from their category tables, 20 September.** Ours had a uuid and a localised
            name, so an importer matching *Beverages* had to match on a display string that a
            venue is free to translate.
""")


def cut_schema(text, name):
    m = re.search(r"^    %s:\n" % re.escape(name), text, re.M)
    if not m:
        return text, False
    nxt = re.search(r"^    [A-Za-z]", text[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(text) - m.end())
    return text[:m.start()] + text[end:], True


def insert_before(text, anchor, block, label):
    if text.count(anchor) < 1:
        print("    !! anchor not found for %s" % label)
        return text, False
    i = text.find(anchor)
    return text[:i] + block + text[i:], True


def main():
    apply = "--apply" in sys.argv[1:]

    # 1. The six columns, into catalogue.yaml.
    c = io.open(CAT, encoding="utf-8").read()
    if "isStockTracked" in c:
        print("  catalogue.yaml already amended")
    else:
        # Product: anchor inside the Product schema, which begins at its persistence tag.
        pi = c.find("x-ticvai-persistence: catalogue.product\n")
        for anchor, block in ADDITIONS:
            j = c.find(anchor, pi)
            if j < 0:
                print("    !! Product anchor %r not found" % anchor.strip())
                return 1
            c = c[:j] + block + c[j:]
        print("    catalogue.product          +categoryId, +isStockTracked")

        vi = c.find("x-ticvai-persistence: catalogue.variant\n")
        j = c.find(VARIANT_ADD[0], vi)
        if j < 0:
            print("    !! ProductVariant anchor not found")
            return 1
        c = c[:j] + VARIANT_ADD[1] + c[j:]
        print("    catalogue.variant          +name, +barcode, +isDefault")

        ci = c.find("x-ticvai-persistence: catalogue.product_category\n")
        j = c.find(CATEGORY_ADD[0], ci)
        if j < 0:
            print("    !! ProductCategory anchor not found")
            return 1
        c = c[:j] + CATEGORY_ADD[1] + c[j:]
        print("    catalogue.product_category +code")

    try:
        yaml.safe_load(c)
    except Exception as e:
        print("    !! catalogue.yaml would not parse: %s" % str(e)[:160])
        return 1
    print("    catalogue.yaml parses")

    # 2. The ten schemas out of fnb.yaml and retail.yaml.
    texts = {}
    for path, schemas in DROP.items():
        s = io.open(path, encoding="utf-8").read()
        hits = 0
        for name in schemas:
            s, hit = cut_schema(s, name)
            hits += 1 if hit else 0
            if not hit:
                print("    %-24s not found" % name)
        try:
            yaml.safe_load(s)
        except Exception as e:
            print("    !! %s would not parse: %s" % (os.path.basename(path), str(e)[:140]))
            return 1
        print("    %-18s %d schema(s) removed, parses" % (os.path.basename(path), hits))
        texts[path] = s

    # 3. The derived files cannot drop a table by themselves.
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
    io.open(CAT, "w", encoding="utf-8", newline="\n").write(c)
    for path, s in texts.items():
        io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    io.open(sp, "w", encoding="utf-8", newline="\n").write(json.dumps(S, ensure_ascii=False))
    io.open(gp, "w", encoding="utf-8", newline="\n").write(
        json.dumps(G, indent=1, ensure_ascii=False))
    print("  -> catalogue.yaml, fnb.yaml, retail.yaml and two handoff files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
