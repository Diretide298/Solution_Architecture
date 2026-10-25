#!/usr/bin/env python3
"""The venue's currency read for every operation that answers Money with no currency source (r10 lane E,
CHG-R10GEN-002; ADAM CR-197, CR-202, CR-217, CR-234, CR-235).

tools/check-money-currency.py (MC-NO-CURRENCY) lists the operations that answer or accept common Money from rows that
store the amount only, and ask nothing that denominates it. naming-and-style 5.1 and ADR-0018 say where the currency
comes from: the venue's frozen trading currency, Tenancy's `platform.venue_settings`, defaulted from
`platform.region_settings`. This writes that read, at each operation's own lines, the way
tools/applied/read-routes-18-october.py writes a route:

  venue    the row (or the operation) holds the venue (`venue_id`, `outlet_id`, a `venueId` parameter or body field):
           x-ticvai-read-via tenancy#venueSettingsRecords, `in-process` within commerce, `service` from another
           deployable (CR-234 option A);
  region   the row holds a region and no venue (`region_id`): tenancy#regionSettingsRecords, the same way;
  scope    the row keeps only its `scope_path`: routed through tenancy#scopeRecords (the venue of a scope path) and
           tenancy#venueSettingsRecords once Tenancy declares tenancy#scopeRecords (CR-217 and CR-235 option A);
           until then it is printed for the lead;
  and each query's `served` gains the route its new askers take.

Printed for the lead, grouped by kind, each with the default ruling this recommends:

  platform   a `control.*` row: the platform's own billing to a tenant, which no venue denominates (CR-202);
  no venue   a row that holds no venue, region or scope path;
  no row     a computed answer whose operation reads no table.

Identity never appears: Tenancy shares its foundation tier (ADR-0028), so no route here is above it.

Re-runnable on a changed tree: the findings are read fresh, with the routes this script wrote left out, so a route
it wrote that nothing justifies any more is removed and a second run writes nothing. Contracts keep their line ends.

    python tools/applied/money-currency-reads-r10.py            # what it would write
    python tools/applied/money-currency-reads-r10.py --apply
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


rr = _load("rr", TOOLS / "applied" / "read-routes-18-october.py")
mc = _load("mc", TOOLS / "check-money-currency.py")

VENUE_Q = "tenancy#venueSettingsRecords"
REGION_Q = "tenancy#regionSettingsRecords"
SCOPE_Q = "tenancy#scopeRecords"
TAG = "(naming-and-style 5.1, ADR-0018; CHG-R10GEN-002)"
OWN_FOR = re.compile(r".*\(naming-and-style 5\.1, ADR-0018; CHG-R10GEN-002\)$")
VENUE_KEYS = {"venue_id", "outlet_id"}
VENUE_PARAMS = {"venueId", "outletId"}

DECISIONS = {
    "platform": "a control.* row is the platform's own billing to a tenant, and no venue denominates it. Recommended "
                "default (CR-202 option A): a billing currency on the billing entity, copied to a currency_code "
                "column on the row when it is made",
    "scope": "the row keeps only its scope_path, and reaching its venue needs platform.scope. Recommended default "
             "(CR-217 and CR-235 option A): Tenancy declares tenancy#scopeRecords (platform.scope by id and by path, "
             "in-process and service); a second run of this script then routes these through it and "
             "tenancy#venueSettingsRecords. A row kept above a venue (a region or tenant policy) answers in the "
             "region's currency, the ADR-0018 default, and says so in its operation",
    "no venue": "the row holds no venue, region or scope path. Recommended default: the venue the operation acts at "
                "(the caller's working venue) through tenancy#venueSettingsRecords, stated in the operation; a row "
                "that is tenant-wide stores its own currency_code instead",
    "no row": "a computed answer whose operation reads no table. Recommended default: the venue the operation acts at, "
              "through tenancy#venueSettingsRecords, stated in the operation",
}


def is_own(route: dict) -> bool:
    """A read route this script wrote (its `for` ends with this change's tag)."""
    return bool(OWN_FOR.match(str((route or {}).get("for") or "")))


def route_for(reader_deployable, owner_deployable) -> str:
    return rr.route_for(reader_deployable, owner_deployable)


def venue_named(f: dict, by: dict) -> bool:
    """The operation is asked about one venue: a `venueId` or `outletId` parameter, or a top-level body field."""
    params = list((f.get("item") or {}).get("parameters") or []) + list((f.get("op") or {}).get("parameters") or [])
    if any(isinstance(p, dict) and p.get("name") in VENUE_PARAMS for p in params):
        return True
    body = (((f.get("op") or {}).get("requestBody") or {}).get("content") or {}).get("application/json") or {}
    s = body.get("schema") or {}
    if isinstance(s.get("$ref"), str):
        s = by.get(mc.resolve(f.get("contract"), s["$ref"])) or {}
    return bool(set((s.get("properties") or {})) & VENUE_PARAMS)


def lineage_up(rows: list, cols_of: dict, depth: int = 2) -> set:
    """The rows and the parents of the same schema they reference, `depth` hops up (a menu item's menu and outlet)."""
    out, edge = set(rows), set(rows)
    for _ in range(depth):
        nxt = set()
        for t in edge:
            for c in cols_of.get(t) or []:
                ref = c.get("references")
                if ref and ref in cols_of and ref.split(".", 1)[0] == t.split(".", 1)[0] and ref not in out:
                    nxt.add(ref)
        out |= nxt
        edge = nxt
    return out


def classify(f: dict, bare: list, computed: list, rows: list, cols_of: dict, by: dict, declared: set) -> str:
    """venue | region | scope (routed when tenancy#scopeRecords is declared) | platform | no venue | no row.
    `rows` are the tables behind the Money: those storing the amount only, and for a computed answer the tables the
    operation reads in its own module. A row holds what its parents of the same schema hold (lineage_up)."""
    if venue_named(f, by):
        return "venue"
    if any(t.startswith("control.") for t in bare):
        return "platform"
    cols = {c.get("column") for t in lineage_up(rows, cols_of) for c in cols_of.get(t) or []}
    if cols & VENUE_KEYS:
        return "venue"
    if "region_id" in cols:
        return "region"
    if "scope_path" in cols:
        return "scope"
    return "no venue" if rows else "no row"


def queries_for(kind: str, declared: set) -> list:
    if kind == "venue":
        return [VENUE_Q]
    if kind == "region":
        return [REGION_Q]
    if kind == "scope" and SCOPE_Q in declared:
        return [SCOPE_Q, VENUE_Q]
    return []


def why(kind: str, query: str, verb: str, fields: list) -> str:
    shown = ", ".join(fields[:4]) + (f" and {len(fields) - 4} more" if len(fields) > 4 else "")
    if query == SCOPE_Q:
        what = "the venue its row's scope_path names, whose settings give the currency"
    elif query == REGION_Q:
        what = "the region's trading currency and scale (currency_code, currency_scale)"
    else:
        what = "the venue's frozen trading currency and scale (currency_code, currency_scale)"
    return f"{what} for the Money it {verb}: {shown} {TAG}"


def add_read_via(text: str, op: str, entries: list):
    """read-routes-18-october's add_read_via, writing at the list's own indent: four of the 660 lists in r9 indent
    their items two more than the key (addCartLine's), and an item at the key's indent there breaks the YAML.
    entries: [(query, route, for)]. Returns (text, entries added)."""
    lines = text.split("\n")
    i, end, ind = rr._op_block(lines, op)
    k = next((n for n in range(i, end) if lines[n] == f"{ind}x-ticvai-read-via:"), None)
    if k is None:
        return rr.add_read_via(text, op, entries)
    m = re.match(r"^(\s*)- ", lines[k + 1]) if k + 1 < end else None
    item = m.group(1) if m else ind
    have, at = set(), k + 1
    while at < end and (lines[at].startswith(f"{item}- ") or lines[at].startswith(f"{item}  ")):
        q = re.match(r"^\s+- query:\s*(\S+)", lines[at])
        if q:
            have.add(q.group(1))
        at += 1
    new = []
    for q, route, w in entries:
        if q in have:
            continue
        have.add(q)
        new += [f"{item}- query: {q}", f"{item}  route: {route}", f"{item}  for: '" + w.replace("'", "''") + "'"]
    if not new:
        return text, 0
    lines[at:at] = new
    return "\n".join(lines), len(new) // 3


def remove_own(text: str, op: str, query: str):
    """Removes the operation's route to `query` that this script wrote; drops the list when it empties."""
    lines = text.split("\n")
    i, end, ind = rr._op_block(lines, op)
    k = next((n for n in range(i, end) if lines[n] == f"{ind}x-ticvai-read-via:"), None)
    if k is None:
        return text, 0
    m = re.match(r"^(\s*)- ", lines[k + 1]) if k + 1 < end else None
    ind = m.group(1) if m else ind
    at, items = k + 1, []
    while at < end and (lines[at].startswith(f"{ind}- ") or lines[at].startswith(f"{ind}  ")):
        if lines[at].startswith(f"{ind}- "):
            items.append([at, at + 1])
        else:
            items[-1][1] = at + 1
        at += 1
    for a, b in items:
        block = lines[a:b]
        q = re.match(r"^\s+- query:\s*(\S+)", block[0])
        w = next((re.match(r"^\s+for:\s*'(.*)'\s*$", l) for l in block if re.match(r"^\s+for:", l)), None)
        if q and q.group(1) == query and w and is_own({"for": w.group(1).replace("''", "'")}):
            del lines[a:b]
            if len(items) == 1:
                del lines[k]
            return "\n".join(lines), 1
    return text, 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    ctx = mc.load()
    services, cols_of, by, lin = ctx["services"], ctx["cols_of"], ctx["by"], ctx["lin"]
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    declared = set(ctx["qtables"])
    owner_of_schema = ctx["owner_of_schema"]
    tenancy_dep = dep_of.get(mc.SETTINGS_OWNER)
    ops = ctx["ops"]
    texts: dict = {}

    def text(rel):
        if rel not in texts:
            texts[rel] = rr._read(ROOT / rel)
        return texts[rel]

    plan, held = {}, {}
    for o, svc, fields, bare, computed in mc.findings(ctx, ignore=is_own):
        f = ops[o]
        rows = list(bare)
        if computed:
            rows += [t for t in (lin.get(o) or {}).get("reads") or []
                     if t in cols_of and owner_of_schema.get(t.split(".", 1)[0]) == svc]
        kind = classify(f, bare, computed, sorted(set(rows)), cols_of, by, declared)
        qs = queries_for(kind, declared)
        if not qs:
            held.setdefault(kind, []).append(f"{o} ({svc}): {', '.join(bare + computed)}")
            continue
        verb = "answers" if f["method"] == "get" else "accepts or answers"
        route = route_for(dep_of.get(svc), tenancy_dep)
        plan[o] = [(q, route, why(kind, q, verb, fields)) for q in qs]
    n_via = 0
    for o, entries in sorted(plan.items()):
        rel = ops[o]["file"]
        texts[rel], n = add_read_via(text(rel), o, entries)
        n_via += n
        if n:
            print(f"  {o}: {', '.join(f'{q} ({r})' for q, r, _w in entries)}")
    # a route this script wrote that no finding justifies any more goes
    wanted = {(o, q) for o, entries in plan.items() for q, _r, _w in entries}
    n_gone = 0
    for o, f in sorted(ops.items()):
        for r in f["op"].get("x-ticvai-read-via") or []:
            if isinstance(r, dict) and is_own(r) and (o, r.get("query")) not in wanted:
                texts[f["file"]], n = remove_own(text(f["file"]), o, r.get("query"))
                n_gone += n
                if n:
                    print(f"  {o}: {r.get('query')} removed - its Money has a source without it")
    # served: every route an asker now takes (never fewer than the owner declared)
    rel_t = "contracts/spine/tenancy.yaml"
    for q in sorted({q for entries in plan.values() for q, _r, _w in entries}):
        for route in sorted({r for entries in plan.values() for qq, r, _w in entries if qq == q}):
            texts[rel_t], changed = rr.add_served(text(rel_t), q.split("#", 1)[1], route, tenancy_dep)
            if changed:
                print(f"  served {q}: gains {route}")
    for kind in ("scope", "platform", "no venue", "no row"):
        items = held.get(kind) or []
        if items:
            print(f"\nFOR THE LEAD ({kind}, {len(items)}): {DECISIONS[kind]}")
            for s in items:
                print(f"  {s}")
    changed = [rel for rel, t in texts.items() if t != rr._read(ROOT / rel)]
    print(f"\n{n_gone} route(s) removed; {n_via} read route(s) in {len(plan)} operation(s); "
          f"{sum(len(v) for v in held.values())} held for the lead; {len(changed)} contract file(s) change"
          + ("" if a.apply else " (nothing written, pass --apply)"))
    if a.apply:
        for rel in changed:
            rr._write(ROOT / rel, texts[rel])
    return 0


if __name__ == "__main__":
    sys.exit(main())
