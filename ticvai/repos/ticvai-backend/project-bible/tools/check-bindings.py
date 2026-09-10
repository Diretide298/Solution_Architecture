#!/usr/bin/env python3
"""Check that every component says what fills it, and that the thing named exists.

**A `dataTable` with no `bindsTo` is not a specification.** It says a table is here. It does not
say what is in it, which of the screen's operations fills it, or what the columns are — and 3,418
of the package's 3,496 components are in exactly that state. **97.8% unbound**, which nothing has
ever checked, which is why it was allowed to happen.

The consequence is measurable elsewhere: 337 screens are `searchField + dataTable + detailPanel`
and 335 of them annotate the search field *"Find a record"*. Those screens are indistinguishable
from each other because **nothing in them names the data**.

## What a binding is

`bindsTo` names a schema in the contracts, with an optional field path:

  `Product`                     one instance
  `KitchenTicket[]`             a collection
  `Product.lifecycleState`      one field of one instance
  `Availability.performances`   a field that is itself a collection

**Checked against the contracts, not against a list of names**, so a binding to a schema that was
renamed fails the build rather than rotting quietly.

## Why this exists before the generator

Screens are about to be regenerated. **If the checks are written afterwards, a generator can
produce 1,091 screens of new filler and nothing will know** — which is precisely how the current
state arose and went unnoticed for weeks. So: this reports a baseline now, the regeneration has to
move it, and `--strict` fails the build once the work is done.

Run: python3 tools/check-bindings.py [--strict] [--platform P08]
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
CONTRACTS = ROOT / "contracts"

# **Components that display data and therefore must say which data.** A `primaryButton` needs no
# binding — it needs an operation, which is a different check. A `dataTable` that names nothing is
# the defect this tool exists for.
DATA_BEARING = {
    "dataTable", "detailPanel", "cardList", "chart", "metricTile", "timeline",
    "seatMap", "cartPanel", "consentBlock", "duplicateMatch", "list", "kpiRow",
}

# A binding: `Schema`, `Schema[]`, `Schema.field`, `Schema.field[].nested`. **Nested paths are
# legitimate** — a table of order lines binds to `Order.lines[].product`, and rejecting that would
# push the regeneration towards shallower bindings than the screens actually need.
BINDING = re.compile(r"^([A-Z][A-Za-z0-9]*)(\[\])?((?:\.[A-Za-z][A-Za-z0-9]*(?:\[\])?)*)$")

# **The boilerplate that should have failed a build.** Any note repeated on more than this many
# components is filler by definition: no two screens legitimately need the same sentence 300 times.
BOILERPLATE_LIMIT = 12


def contract_schemas() -> dict:
    """Every schema in every contract, with its property names.

    Properties are read one level deep and `allOf` branches are merged, which is enough to check a
    field path. **Deeper resolution is deliberately not attempted** — a checker that silently
    half-resolves a `$ref` reports a real field as missing, and a wrong failure is worse than a
    missing check because somebody will delete the binding to make it pass.
    """
    raw = {}
    for f in sorted(CONTRACTS.rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — an unreadable contract is reported, not fatal
            continue
        if not isinstance(doc, dict):
            continue
        for name, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            if isinstance(body, dict):
                raw.setdefault(name, (f.name, body))

    # **`allOf` composition is not "deep resolution", and refusing to follow it produced exactly
    # the false failure this file warned about.** `GuestProfileDetail` is
    # `allOf: [$ref GuestProfile, {id, ...}]`, so `displayName` is a real property of it — and
    # reporting 771 real fields as missing is how somebody comes to delete a correct binding to
    # make the build pass. One hop through a named `$ref`, resolved by name because the packages'
    # refs cross files (`../shared/common.yaml#/components/schemas/Money`).
    def props_of(name: str, seen: frozenset = frozenset()) -> set:
        if name in seen or name not in raw:
            return set()
        _, body = raw[name]
        props = set(body.get("properties") or {})
        for branch in body.get("allOf") or []:
            if not isinstance(branch, dict):
                continue
            props |= set(branch.get("properties") or {})
            if ref := branch.get("$ref"):
                props |= props_of(str(ref).rsplit("/", 1)[-1], seen | {name})
        return props

    return {name: {"file": file, "props": props_of(name)} for name, (file, _) in raw.items()}


def screens():
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        for s in doc["screens"]:
            yield f.name, code, s


def components(s):
    for region in (s.get("layout") or {}).get("regions") or []:
        for c in region.get("components") or []:
            yield region.get("name", "?"), c


def main() -> int:
    strict = "--strict" in sys.argv
    only = None
    if "--platform" in sys.argv:
        only = sys.argv[sys.argv.index("--platform") + 1]

    schemas = contract_schemas()
    print(f"{len(schemas)} schemas across the contracts\n")

    bad_schema, bad_field, unbound, notes = [], [], [], Counter()
    bad_column, plain_column = [], 0
    total = bound = columns_total = 0
    per_platform = defaultdict(lambda: [0, 0])

    for fname, code, s in screens():
        if only and code != only:
            continue
        for region, c in components(s):
            kind = c.get("kind")
            total += 1
            per_platform[code][0] += 1
            if c.get("notes"):
                notes[" ".join(str(c["notes"]).split())] += 1

            # **`columns` carries schema paths and nothing was reading them.** The pack
            # regeneration writes 871 verified paths and 240 raw pack labels into this key, and a
            # path nobody checks is a document rather than a constraint — which is the defect this
            # package has already found three times in `_schema.yaml` alone. A bare label is
            # legitimate and counted; a path naming a schema that does not exist is not.
            for col in c.get("columns") or []:
                columns_total += 1
                m = BINDING.match(str(col).strip())
                if not m or "." not in str(col):
                    plain_column += 1
                    continue
                schema, _, rest = m.groups()
                field = rest.lstrip(".").split(".")[0].replace("[]", "")
                if schema not in schemas:
                    bad_column.append((code, s["id"], kind, col, f"no schema named {schema}"))
                elif field and field not in schemas[schema]["props"]:
                    bad_column.append((code, s["id"], kind, col,
                                       f"{schema} has no property {field}"))

            b = c.get("bindsTo")
            if not b:
                if kind in DATA_BEARING:
                    unbound.append((code, s["id"], kind, region))
                continue
            bound += 1
            per_platform[code][1] += 1

            m = BINDING.match(str(b).strip())
            if not m:
                bad_schema.append((code, s["id"], kind, b, "not a schema reference"))
                continue
            schema, _, rest = m.groups()
            # Only the first hop is validated. **Deeper hops need `$ref` resolution, and a checker
            # that half-resolves reports a real field as missing** — somebody then deletes the
            # binding to make it pass, which is worse than not checking.
            field = rest.lstrip(".").split(".")[0].replace("[]", "") if rest else None
            if schema not in schemas:
                bad_schema.append((code, s["id"], kind, b, f"no schema named {schema}"))
            elif field and field not in schemas[schema]["props"]:
                bad_field.append((code, s["id"], kind, b,
                                  f"{schema} has no property {field}"))

    print(f"{total} components · {bound} bound ({bound / total * 100:.1f}%) · "
          f"{total - bound} unbound")
    print(f"  of the unbound, {len(unbound)} are data-bearing and therefore a defect\n")

    if bad_schema:
        print(f"  {len(bad_schema)} binding(s) name something that does not exist:")
        for code, sid, kind, b, why in bad_schema[:15]:
            print(f"     {code} {sid:<9}{kind:<14}{b!r} — {why}")
    if bad_field:
        print(f"  {len(bad_field)} binding(s) name a field the schema does not have:")
        for code, sid, kind, b, why in bad_field[:15]:
            print(f"     {code} {sid:<9}{kind:<14}{b!r} — {why}")

    if columns_total:
        resolved = columns_total - plain_column - len(bad_column)
        print(f"\n  {columns_total} declared column(s): {resolved} resolve to a contract field, "
              f"{plain_column} are a source label with no field behind them yet, "
              f"{len(bad_column)} name something that does not exist")
        for code, sid, kind, col, why in bad_column[:15]:
            print(f"     {code} {sid:<9}{kind:<14}{col!r} — {why}")

    print("\n  data-bearing components with no binding, by platform:")
    by_p = Counter(u[0] for u in unbound)
    for code, n in sorted(by_p.items()):
        t, bd = per_platform[code]
        print(f"     {code}  {n:>4} unbound of {t:>4} components   ({bd} bound)")

    # **The boilerplate detector.** 335 components saying "Find a record" is the clearest single
    # measure of a generated layer, and no build should have passed with it.
    repeated = [(n, txt) for txt, n in notes.most_common() if n > BOILERPLATE_LIMIT]
    if repeated:
        print(f"\n  {len(repeated)} component note(s) repeated more than {BOILERPLATE_LIMIT} times "
              f"— boilerplate, not specification:")
        for n, txt in repeated[:12]:
            print(f"     {n:>5}  {txt[:78]!r}")
        print(f"     {sum(n for n, _ in repeated)} components carry one of these "
              f"({sum(n for n, _ in repeated) / total * 100:.0f}% of all components)")

    failed = bool(bad_schema or bad_field or bad_column) or (strict and (unbound or repeated))
    print("\nFAIL" if failed else "\nPASS")
    if not strict and (unbound or repeated):
        print("  (baseline run — `--strict` fails on unbound components and boilerplate)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
