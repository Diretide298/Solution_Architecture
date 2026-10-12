# -*- coding: utf-8 -*-
"""ADAM CR-011, CR-012, CR-013 and CR-014, decided 12 October 2026 (CHG-R6-010..018). Re-runnable.

The decisions are declared where the generators read them: the table and column renames in
`tools/derive-schema-history.py` (`RENAMES`, `COLUMN_RENAMES`). This script does the part that is
mechanical and would otherwise be half-done, as `adr-1-october.py` did for the renames of 1 October:

1. **A renamed table is renamed where the package names it**: the `x-ticvai-persistence` tags and
   `x-ticvai-references` in the contracts, the prose that names the table (check-ddl-conventions
   D-RENAME-RESIDUE fails on an old name left there), the screens, flows, states and events, and
   `handoff/api-data-lineage.json`, which derive-lineage adds to and never prunes. `schema-reference.json`
   is not edited: derive-schema retires a declared rename's old name itself.
2. **A renamed column keeps its wire name**: `x-ticvai-column: <new>` goes on every contract field that
   lands in it (every schema persisting to the table that has the field), the mechanism of the 27 money
   columns of 24 September. A child table's parent key follows its parent's name and needs nothing.
3. **CR-013**: `x-ticvai-references` on the fields that point at a same-schema parent (and the two whose
   name rule picked the wrong table), `x-ticvai-references: none` on the two that are not keys at all, and
   `x-ticvai-unique: tenant` on the human codes.

Wire names and types are not touched: only `x-ticvai-*` keys are added and table names in prose replaced.

    python tools/applied/ddl-names-12-october.py            # report
    python tools/applied/ddl-names-12-october.py --apply    # write
"""
import ast
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv
ON = "2026-10-12"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def declared(name):
    tree = ast.parse((ROOT / "tools" / "derive-schema-history.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    return []


TABLES = [(r["from"], r["to"]) for r in declared("RENAMES") if r.get("on") == ON]
COLUMNS = [r for r in declared("COLUMN_RENAMES") if r.get("on") == ON]
OLD_OF = {n: o for o, n in TABLES}

# CR-013: (contract file stem, schema, property path) -> extension key and value.
EXTRA = [
    # in-schema NOT NULL keys that point at their parent, so 920 scopes the child through it
    ("orders", "ParticipantGuestListView", "groupBookingId", "x-ticvai-references", "orders.group_booking"),
    ("orders", "OrderEvent", "orderId", "x-ticvai-references", "orders.sales_order"),
    ("promotions", "PromotionRule", "promotionId", "x-ticvai-references", "promotions.promotion"),
    ("promotions", "PromotionVariant", "promotionId", "x-ticvai-references", "promotions.promotion"),
    ("promotions", "PromotionAuditEvent", "promotionId", "x-ticvai-references", "promotions.promotion"),
    ("promotions", "PromotionChannelPublication", "promotionId", "x-ticvai-references", "promotions.promotion"),
    ("inventory", "InventoryStockReservation", "locationId", "x-ticvai-references", "inventory.location"),
    ("inventory", "InventoryStockReservation", "itemId", "x-ticvai-references", "inventory.inventory_item"),
    ("inventory", "GoodsReceipt", "locationId", "x-ticvai-references", "inventory.location"),
    ("inventory", "StockMovement", "locationId", "x-ticvai-references", "inventory.location"),
    ("inventory", "SerialisedItem", "locationId", "x-ticvai-references", "inventory.location"),
    ("inventory", "SerialisedItem", "itemId", "x-ticvai-references", "inventory.inventory_item"),
    ("inventory", "InventoryKitComponent", "kitItemId", "x-ticvai-references", "inventory.inventory_item"),
    ("inventory", "InventoryKitComponent", "componentItemId", "x-ticvai-references", "inventory.inventory_item"),
    ("inventory", "PurchaseOrder", "deliverToLocationId", "x-ticvai-references", "inventory.location"),
    ("inventory", "Requisition", "costCenterId", "x-ticvai-references", "ledger.cost_center"),
    # keys whose name rule stops resolving once inventory.item is inventory.inventory_item
    ("inventory", "CountLine", "itemId", "x-ticvai-references", "inventory.inventory_item"),
    ("reporting", "Alert", "itemId", "x-ticvai-references", "inventory.inventory_item"),
    # a renamed key keeps the declaration its old name carried as a legacy label
    ("orders", "CartLine", "inventoryHoldId", "x-ticvai-references", "catalogue.inventory_reservation"),
    ("orders", "OrderLine", "inventoryHoldId", "x-ticvai-references", "catalogue.inventory_reservation"),
    # CR-011: wallet.hold.wallet_hold_id was a second identity beside the surrogate `id` (the wire's
    # walletHoldId is the row's id, /wallet-holds/{walletHoldId}); it is stored as `id`, not renamed
    ("wallet", "WalletHold", "walletHoldId", "x-ticvai-column", "id"),
    # wrong 910 targets
    ("promotions", "CouponCode", "campaignId", "x-ticvai-references", "promotions.coupon_campaign"),
    ("promotions", "CouponCodeAssignment", "batchId", "x-ticvai-references", "promotions.coupon_code_batch"),
    ("finance", "FinEInvoiceTransmission", "providerMessageId", "x-ticvai-references", "none"),
    ("finance", "FinEInvoicingProvider", "participantId", "x-ticvai-references", "none"),
    # human codes, unique per tenant
    ("orders", "Order", "orderNumber", "x-ticvai-unique", "tenant"),
    ("inventory", "InventoryItem", "sku", "x-ticvai-unique", "tenant"),
    ("finance", "Account", "code", "x-ticvai-unique", "tenant"),
    ("finance", "TaxCode", "code", "x-ticvai-unique", "tenant"),
    ("finance", "JournalEntry", "entryNumber", "x-ticvai-unique", "tenant"),
    ("finance", "FinTaxInvoice", "invoiceNumber", "x-ticvai-unique", "tenant"),
    ("finance", "FinCreditMemo", "creditMemoNumber", "x-ticvai-unique", "tenant"),
]

CONTRACT_FILES = sorted((ROOT / "contracts").glob("*/*.yaml"))
TEXT_SOURCES = (CONTRACT_FILES + sorted((ROOT / "screens").glob("*.yaml"))
                + sorted((ROOT / "states").glob("*.yaml")) + sorted((ROOT / "events").glob("*.yaml"))
                + sorted((ROOT / "flows").glob("*.yaml")))
LINEAGE = ROOT / "handoff" / "api-data-lineage.json"


def table_re(name):
    return re.compile(r"(?<![\w.])" + re.escape(name) + r"(?![\w])")


# --- property surgery on the YAML text --------------------------------------------------------

def indent(line):
    return len(line) - len(line.lstrip(" "))


def schema_block(lines, schema):
    """(start, end) line range of components.schemas.<schema>, or None."""
    pat = re.compile(r"^    " + re.escape(schema) + r":\s*(#.*)?$")
    for i, ln in enumerate(lines):
        if pat.match(ln):
            j = i + 1
            while j < len(lines) and (not lines[j].strip() or indent(lines[j]) > 4 or lines[j].lstrip().startswith("#")):
                j += 1
            return i, j
    return None


def find_prop(lines, lo, hi, prop):
    """The shallowest line in [lo, hi) declaring `prop:` directly under a `properties:` key."""
    pat = re.compile(r"^(\s+)" + re.escape(prop) + r":(\s|$)")
    best = None
    for i in range(lo, hi):
        m = pat.match(lines[i])
        if not m:
            continue
        ind = len(m.group(1))
        k = i - 1
        while k >= lo and (not lines[k].strip() or indent(lines[k]) >= ind or lines[k].lstrip().startswith("#")):
            k -= 1
        if k >= lo and lines[k].strip() == "properties:" and (best is None or ind < indent(lines[best])):
            best = i
    return best


def prop_end(lines, i, hi):
    ind = indent(lines[i])
    j = i + 1
    while j < hi and (not lines[j].strip() or indent(lines[j]) > ind):
        j += 1
    return j


def set_ext(lines, i, hi, key, value):
    """Give the property on line i `key: value`. Returns 'added', 'same' or 'changed:<old>'."""
    ln = lines[i]
    flow = re.match(r"^(\s*[\w$-]+:\s*)\{(.*)\}\s*(#.*)?$", ln)
    if flow:
        body = flow.group(2)
        m = re.search(r"(?:^|,)\s*" + re.escape(key) + r":\s*([^,}]+)", body)
        if m:
            if m.group(1).strip() == value:
                return "same"
            lines[i] = ln.replace(m.group(0), m.group(0).replace(m.group(1), " " + value + " " if m.group(1).endswith(" ") else value))
            return "changed:" + m.group(1).strip()
        lines[i] = flow.group(1) + "{" + body.rstrip() + ", " + key + ": " + value + " }" + (
            " " + flow.group(3) if flow.group(3) else "")
        return "added"
    end = prop_end(lines, i, hi)
    child = indent(ln) + 2
    for k in range(i + 1, end):
        m = re.match(r"^\s{%d}%s:\s*(.*)$" % (child, re.escape(key)), lines[k])
        if m:
            if m.group(1).strip() == value:
                return "same"
            old = m.group(1).strip()
            lines[k] = " " * child + key + ": " + value
            return "changed:" + old
    if ln.rstrip().endswith(":"):
        lines.insert(i + 1, " " * child + key + ": " + value)
        return "added"
    return "unplaceable"


def persisted_props():
    """(table, property path) -> [(file, schema, path)] for every contract schema persisting to a table."""
    sys.path.insert(0, str(ROOT / "tools"))
    import importlib.util
    spec = importlib.util.spec_from_file_location("_ds", ROOT / "tools" / "derive-schema.py")
    ds = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ds)
    out = {}
    registry = {}
    docs = {}
    for f in CONTRACT_FILES:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        docs[f] = d
        for sname, body in ((d.get("components") or {}).get("schemas") or {}).items():
            registry.setdefault(sname, body)
    for f, d in docs.items():
        for sname, body in ((d.get("components") or {}).get("schemas") or {}).items():
            if not isinstance(body, dict):
                continue
            tag = ds.persistence_of(body)
            if not isinstance(tag, str) or "." not in tag or "—" in tag:
                continue
            parts = [p.strip() for p in tag.split("+")]
            for prop, pspec in ds.properties_of(body, registry).items():
                out.setdefault((parts[0], prop), []).append((f, sname, prop))
                if isinstance(pspec, dict) and pspec.get("type") == "array":
                    items = pspec.get("items") or {}
                    if isinstance(items, dict) and items.get("$ref"):
                        items = registry.get(items["$ref"].rsplit("/", 1)[-1]) or {}
                    for cprop in ds.properties_of(items, registry):
                        for child in parts[1:]:
                            out.setdefault((child, f"{prop}[].{cprop}"), []).append((f, sname, f"{prop}[].{cprop}"))
    return out


def head_sources():
    raw = subprocess.run(["git", "show", "HEAD:ticvai/handoff/schema-reference.json"], cwd=ROOT,
                         capture_output=True).stdout
    cols = json.loads(raw)["cols"]
    return {(t, c["column"]): str(c.get("source") or "") for t, cs in cols.items() for c in cs}


def defining(registry, home, schema, path):
    """(file, schema, path) where the property is written: a persisted schema often takes its fields from an
    `allOf` request schema (`OrderLine` from `CreateOrderLine`), and a line array from a `$ref` item schema
    (`FinTaxInvoice.lines[]` from `FinTaxInvoiceLine`). The extension goes where the field is written; every
    schema built from it gets the same column name."""
    body = registry.get(schema) or {}
    if "[]." in path:
        arr, prop = path.split("[].", 1)
        f, s, p = defining(registry, home, schema, arr)
        if not f:
            f, s, p = home.get(schema), schema, arr
        aspec = ((registry.get(s) or {}).get("properties") or {}).get(p) or {}
        for branch in (registry.get(s) or {}).get("allOf") or []:
            if isinstance(branch, dict):
                aspec = aspec or (branch.get("properties") or {}).get(p) or {}
        items = aspec.get("items") or {}
        if isinstance(items, dict) and items.get("$ref"):
            return defining(registry, home, items["$ref"].rsplit("/", 1)[-1], prop)
        return f, s, f"{p}[].{prop}"
    if path in (body.get("properties") or {}):
        return home.get(schema), schema, path
    for branch in body.get("allOf") or []:
        if not isinstance(branch, dict):
            continue
        if branch.get("$ref"):
            got = defining(registry, home, branch["$ref"].rsplit("/", 1)[-1], path)
            if got[0]:
                return got
        elif path in (branch.get("properties") or {}):
            return home.get(schema), schema, path
    return None, schema, path


def annotate(edits):
    """edits: [(file, schema, path, key, value)]. Applies them to the text, reports each."""
    registry, home = {}, {}
    for f in CONTRACT_FILES:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for sname, body in ((d.get("components") or {}).get("schemas") or {}).items():
            if sname not in registry or not registry[sname]:
                registry[sname], home[sname] = body, f
    moved = []
    for f, schema, path, key, value in edits:
        f2, s2, p2 = defining(registry, {**home, schema: f}, schema, path)
        if not f2:
            f2, s2, p2 = f, schema, path
        moved.append((f2, s2, p2, key, value))
    edits = sorted(set(moved), key=lambda e: (str(e[0]), e[1], e[2], e[3]))
    by_file = {}
    for e in edits:
        by_file.setdefault(e[0], []).append(e)
    report = []
    for f, es in sorted(by_file.items()):
        text = f.read_text(encoding="utf-8")
        lines = text.split("\n")
        for _f, schema, path, key, value in es:
            blk = schema_block(lines, schema)
            if not blk:
                report.append(f"  ! {f.name} {schema}: schema not found")
                continue
            lo, hi = blk
            if "[]." in path:
                arr, prop = path.split("[].", 1)
                a = find_prop(lines, lo, hi, arr)
                if a is None:
                    report.append(f"  ! {f.name} {schema}.{arr}: array not found")
                    continue
                lo, hi = a + 1, prop_end(lines, a, hi)
            else:
                prop = path
            i = find_prop(lines, lo, hi, prop)
            if i is None:
                report.append(f"  ! {f.name} {schema}.{path}: property not found")
                continue
            r = set_ext(lines, i, hi, key, value)
            report.append(f"  {r:9} {f.relative_to(ROOT).as_posix()} {schema}.{path}  {key}: {value}")
        new = "\n".join(lines)
        if new != text and APPLY:
            io.open(f, "w", encoding="utf-8", newline="\n").write(new)
    return report


def main():
    # 1. tables, by name, wherever the package names them
    pats = [(table_re(o), n, o) for o, n in TABLES]
    for f in TEXT_SOURCES + [LINEAGE]:
        text = f.read_text(encoding="utf-8")
        new = text
        hits = []
        for pat, n, o in pats:
            new, k = pat.subn(n, new)
            if k:
                hits.append(f"{o} x{k}")
        if hits:
            print(f"  {f.relative_to(ROOT).as_posix()}: " + ", ".join(hits))
            if APPLY:
                io.open(f, "w", encoding="utf-8", newline="\n").write(new)

    # 2. columns: x-ticvai-column on every field that lands in a renamed column
    where = persisted_props()
    src = head_sources()
    edits = []
    for r in COLUMNS:
        t_now, old, new = r["table"], r["from"], r["to"]
        t_was = OLD_OF.get(t_now, t_now)
        s = src.get((t_was, old), "")
        parts = s.split(".", 2)
        if len(parts) < 3:
            print(f"  ! {t_was}.{old}: no contract source at HEAD ({s!r})")
            continue
        path = parts[2]
        leaf = path.rsplit(".", 1)[-1]
        snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", leaf)).lower()
        if "[]" not in path and snake != old and old.endswith("_id"):
            print(f"  = {t_now}.{new}: a child table's parent key ({s}); follows its parent's name")
            continue
        # the tags name the table as it was before step 1 wrote them, and as it is now after
        hits = where.get((t_was, path), []) + where.get((t_now, path), []) if t_was != t_now else \
            where.get((t_now, path), [])
        if not hits:
            print(f"  ! {t_was}.{old}: no persisted schema has {path}")
            continue
        for f, schema, p in hits:
            edits.append((f, schema, p, "x-ticvai-column", new))

    # 3. CR-013
    files = {f.stem: f for f in CONTRACT_FILES}
    for stem, schema, path, key, value in EXTRA:
        edits.append((files[stem], schema, path, key, value))

    for line in annotate(edits):
        print(line)
    if not APPLY:
        print("\n  nothing written - pass --apply")


if __name__ == "__main__":
    main()
