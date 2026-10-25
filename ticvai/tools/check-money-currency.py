#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every operation that answers or accepts Money has a source for its currency (r10 lane E, CHG-R10GEN-002).

**Money is three fields on the wire and one column in the database.** naming-and-style 5.1 and ADR-0018 (amended
20 September): a column holds the amount only, and the currency and scale "resolve from what denominates the
amount": a posting from `ledger.account.currency`, a payment from its `tender_currency`, a wallet from
`wallet.wallet.currency`, and everything else from the venue's frozen trading currency
(`platform.venue_settings.currency_code` and `currency_scale`, defaulted from `platform.region_settings`). The
venue's settings are Tenancy's, so every other module asks them of Tenancy (ADR-0055 rule 2 as amended 14 October:
`tenancy#venueSettingsRecords` or `tenancy#regionSettingsRecords`, declared in `x-ticvai-read-via`).

**No check could see the read that 5.1 implies.** From 21 to 23 October five change requests found an operation that
had to put a currency on Money and had no allowed way to: mergeTableVisits (ADAM CR-234: a TableVisit's
runningTotal from `fnb.table_visit`, which stores amounts only), getGuestBundle (CR-197: GuestBundle.price and
savingsAmount), createEntitlementTemplate (CR-217: includedValue accepted with no venue currency to check it
against), setEntitlementTemplateBlackoutDates (CR-235: the same answered from a row that keeps only its scope_path)
and generateInvoice (CR-202: a platform invoice whose `control.invoice` amounts have no currency at all). XR-FACT
reads the words of an operation; none of these words named the venue's settings, so none was a finding (PROCESS-LOG
P-30, "Money with no currency source").

Rules:

    MC-NO-CURRENCY  an operation answers (2xx) or accepts (request body) common Money, `$ref` followed through
                    every schema, and for at least one Money field:
                      * the schema that holds it persists (x-ticvai-persistence) to a table with no currency column
                        of its own (`currency`, `currency_code`, `<x>_currency`, `<x>_currency_code`) and none on a
                        parent row of the same module it references (one hop by any key, two by required keys:
                        `ledger.posting` -> `ledger.account`, `orders.order_line` -> `orders.sales_order`), or
                      * no schema around it persists (a computed answer) and the operation reads no table, and asks no
                        query over a table, that holds a currency column;
                    and the operation asks no query over `platform.venue_settings` or `platform.region_settings` (its
                    own x-ticvai-read-via or the lineage's readVia) and reads neither table, nor a view of them, and
                    is not Tenancy's own (Tenancy owns the settings)

The key is the operationId. The message names the Money fields, the tables that store the amount only, and the
route the read would take (in-process within one deployable, service across, as tools/applied/read-routes-18-
october.py writes them). `tools/applied/money-currency-reads-r10.py` writes that read where the row holds the venue
(`venue_id`, `outlet_id`) or the region (`region_id`), and lists for the lead the rows that hold neither.

**Precision first.** An operation is a finding only where nothing it touches can denominate the Money: a computed
answer next to a read of `orders.payment` or `wallet.wallet` passes, though the read may serve another field.
Nothing is baselined: the lead's rule is that a new check blocks in the release it arrives (25 October 2026).

On r9 (25 October): 451 operations, the five CRs' among them. The fixer routes 301 (the row, a parent row of its
schema, or the operation holds the venue or region); 150 are for the lead: 112 rows that keep only a scope_path
(routed by a second run once Tenancy declares tenancy#scopeRecords, CR-217 option A, leaving 38), 18 platform
billing rows (`control.*`, CR-202), 11 rows with no venue and 9 computed answers that read no table.

    python tools/check-money-currency.py [--all] [--list]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "MC-NO-CURRENCY": "an operation answers or accepts Money from a row that stores the amount only (or computes it "
                      "from rows that hold no currency) and asks no read of the venue's or region's currency "
                      "(naming-and-style 5.1, ADR-0018; ADAM CR-197, CR-202, CR-217, CR-234, CR-235)",
}
SETTINGS = ("platform.venue_settings", "platform.region_settings")
SETTINGS_OWNER = "TenancyService"
# A column that says what currency the row's amounts are in. Not a list a row may charge in (`charge_currencies`,
# `supported_currencies`), not a flag (`allow_multiple_currencies`).
DENOMINATES = re.compile(r"^(?:[a-z]+_)?currency(?:_code)?$")
MONEY = ("common", "Money")


def resolve(stem: str, ref: str) -> tuple:
    """(contract stem, schema name) a `$ref` points at, from the contract `stem` it is written in."""
    path, _, frag = ref.partition("#")
    st = stem if not path else path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return st, frag.rsplit("/", 1)[-1]


def persisted_table(schema: dict, tables) -> str | None:
    """The first table a schema's x-ticvai-persistence names, where the schema reference has it."""
    m = re.match(r'\s*"?([a-z][a-z0-9_]*\.[a-z][a-z0-9_]+)', str((schema or {}).get("x-ticvai-persistence") or ""))
    return m.group(1) if m and m.group(1) in tables else None


def money_hits(stem: str, node, by: dict, tables, ctx=None, field: str = "", seen=frozenset(), depth: int = 0,
               out=None, holder: str = "body") -> list:
    """[(schema stem, schema name, table or None, field)] for every common Money under `node`. The schema named is
    the nearest one around the field that persists to a table, else the nearest one at all (a computed answer);
    `field` is `Schema.property` of the property that holds the Money."""
    out = [] if out is None else out
    if depth > 14:
        return out
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            st, n = resolve(stem, ref)
            if (st, n) == MONEY:
                out.append((ctx[0], ctx[1], ctx[2], field) if ctx else (None, None, None, field))
                return out
            if (st, n) in seen or (st, n) not in by:
                return out
            s = by[(st, n)]
            t = persisted_table(s, tables)
            nctx = (st, n, t) if t or not ctx or not ctx[2] else ctx
            return money_hits(st, s, by, tables, nctx, field, seen | {(st, n)}, depth + 1, out, n)
        for k, v in node.items():
            k = str(k)
            if k.startswith("x-") or k in ("example", "examples", "description"):
                continue
            if k == "properties" and isinstance(v, dict):
                for pn, pv in v.items():
                    money_hits(stem, pv, by, tables, ctx, f"{holder}.{pn}", seen, depth + 1, out, holder)
            else:
                money_hits(stem, v, by, tables, ctx, field, seen, depth + 1, out, holder)
    elif isinstance(node, list):
        for x in node:
            money_hits(stem, x, by, tables, ctx, field, seen, depth + 1, out, holder)
    return out


def op_money(stem: str, op: dict, by: dict, tables) -> list:
    """Every Money an operation accepts (its request body) or answers (its 2xx responses)."""
    out = []
    if op.get("requestBody"):
        money_hits(stem, op["requestBody"], by, tables, out=out)
    for code, r in (op.get("responses") or {}).items():
        if str(code).startswith("2"):
            money_hits(stem, r, by, tables, out=out)
    return out


def currency_columns(cols: list) -> list:
    return [c.get("column") for c in cols or [] if DENOMINATES.match(str(c.get("column") or ""))]


def currency_source(table: str, cols_of: dict, module_of, depth: int = 0) -> str | None:
    """The table of the same module that denominates `table`'s amounts: itself when it has a currency column, else a
    parent it references (one hop by any key, the second by a required key). `module_of(table)` names its owner."""
    if currency_columns(cols_of.get(table)):
        return table
    if depth >= 2:
        return None
    for c in cols_of.get(table) or []:
        ref = c.get("references")
        if not ref or ref not in cols_of or ref == table or module_of(ref) != module_of(table):
            continue
        if depth == 1 and c.get("required") != "yes":
            continue
        got = currency_source(ref, cols_of, module_of, depth + 1)
        if got:
            return got
    return None


def asks_settings(via: list, qtables: dict, reads) -> bool:
    """The operation asks a query over the venue's or region's settings, or reads them (or a view of them)."""
    for r in via or []:
        if set(qtables.get(str((r or {}).get("query") or ""), ())) & set(SETTINGS):
            return True
    return any(str(t).split("_for_", 1)[0] in SETTINGS for t in reads or [])


def judge(hits: list, cols_of: dict, module_of, touched_currency: bool) -> tuple:
    """(tables storing the amount only, computed schemas) behind an operation's Money; both empty when every Money
    has a source. `touched_currency`: the operation reads, or asks a query over, a table with a currency column."""
    bare, computed = set(), set()
    for st, n, t, _f in hits:
        if t:
            if not currency_source(t, cols_of, module_of):
                bare.add(t)
        elif not touched_currency:
            computed.add(f"{st}.{n}" if n else "an inline body")
    return sorted(bare), sorted(computed)


def load():
    """Everything the check and the fixer read, from the package as it is now."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("xr", Path(__file__).resolve().parent / "check-cross-module-reads.py")
    xr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(xr)
    by, _names = g.schemas()
    by = dict(by)
    common = g.load_yaml(g.CONTRACTS / "shared" / "common.yaml") or {}
    for n, s in ((common.get("components") or {}).get("schemas") or {}).items():
        if isinstance(s, dict):
            by.setdefault(("common", n), s)
    services = (g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}).get("services") or {}
    cols_of = (g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {}
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    owner_of_schema = {sc: s for s, v in services.items() for sc in v.get("schemas") or []}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    qtables = {k: xr.query_tables(q) for k, (_stem, q) in xr.declared_queries().items()}
    return {"by": by, "services": services, "cols_of": cols_of, "lin": lin, "owner_of_schema": owner_of_schema,
            "svc_of_contract": svc_of_contract, "qtables": qtables, "ops": g.operations()}


def findings(ctx=None, ignore=None) -> list:
    """[(operation, service, Money fields, bare tables, computed schemas)] for MC-NO-CURRENCY. Shared with the fixer,
    which passes `ignore(route) -> bool` to leave out the routes it wrote, so a second run sees what justifies each."""
    c = ctx or load()
    cols_of, lin, qtables = c["cols_of"], c["lin"], c["qtables"]
    tables = set(cols_of)

    def module_of(t):
        return c["owner_of_schema"].get(str(t).split(".", 1)[0])

    out = []
    for o, f in sorted(c["ops"].items()):
        svc = c["svc_of_contract"].get(f["contract"])
        if not svc or svc == SETTINGS_OWNER:
            continue
        hits = op_money(f["contract"], f["op"], c["by"], tables)
        if not hits:
            continue
        e = lin.get(o) or {}
        via = [r for r in (f["op"].get("x-ticvai-read-via") or []) if isinstance(r, dict)] + (e.get("readVia") or [])
        if ignore:
            via = [r for r in via if not ignore(r)]
        reads = list(e.get("reads") or [])
        if asks_settings(via, qtables, reads):
            continue
        asked = {t for r in via for t in qtables.get(str(r.get("query") or ""), ())}
        touched = any(currency_source(t, cols_of, module_of) for t in set(reads) | asked if t in cols_of)
        bare, computed = judge(hits, cols_of, module_of, touched)
        if bare or computed:
            fields = sorted({h[3] for h in hits if (h[2] in bare) or (not h[2] and computed)})
            out.append((o, svc, fields, bare, computed))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-money-currency", RULES)
    ctx = load()
    dep_of = {s: v.get("deployable") for s, v in ctx["services"].items()}
    rows = findings(ctx)
    if "--list" in sys.argv[1:]:
        for o, svc, fields, bare, computed in rows:
            print("\t".join([o, svc, ", ".join(fields), ", ".join(bare), ", ".join(computed)]))
        return 0
    for o, svc, fields, bare, computed in rows:
        route = "in-process" if dep_of.get(svc) == dep_of.get(SETTINGS_OWNER) else "service"
        where = ([f"{', '.join(bare)} store{'s' if len(bare) == 1 else ''} the amount only"] if bare else []) + (
            [f"{', '.join(computed)} computed from rows with no currency"] if computed else [])
        shown = ", ".join(fields[:4]) + (f" and {len(fields) - 4} more" if len(fields) > 4 else "")
        guard.add("MC-NO-CURRENCY", o,
                  f"{o} ({svc}) answers or accepts Money ({shown}); {'; '.join(where)}; and it asks no read of the "
                  f"venue's or region's currency: add x-ticvai-read-via tenancy#venueSettingsRecords ({route}), or "
                  "store the currency on the row (naming-and-style 5.1, ADR-0018; CR-234)")
    guard.note(f"{len(rows)} operation(s) answer or accept Money with no currency source")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
