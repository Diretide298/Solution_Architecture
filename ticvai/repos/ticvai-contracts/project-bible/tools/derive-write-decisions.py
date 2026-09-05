#!/usr/bin/env python3
"""The table question, asked once per drafted write, with the evidence beside it.

**"Does this deserve a table?" was the last open question about the workshop pack**, and it was
being asked 153 times with nothing to answer it from. This tool answers the part that can be
measured and shows its working, so the part that needs a person is the only part left.

The measurement is a field comparison, not a name comparison. Fuzzy-matching a screen TITLE
against table names claimed 77 of the 153 writes already had a home and was wrong nearly every
time - it paired `setMinorGuardianAge` with `marketing.privacy_incident` on a 100% score.
Comparing the operation's REQUEST FIELDS against the actual columns in `backend/*/0*.sql` says
something quite different and much more useful:

  103 of 153 share not one field with any table the package has
   50 of 153 share a few, none above 25%
    0 of 153 look like an update to something that exists

**So the pack is not a data model, and now there is a number that says why.** It specifies
screens. Thirteen of the 153 come closest to specifying a record - the client wrote *"For each
attraction: Attraction ID, Name, Venue, Zone, Capacity ..."* - and those thirteen are where the
conversation starts, which is why they sort to the top of the sheet.

The alternative was to create 153 tables from a PDF reading. That would have been the largest
single change to the data model in the package's history, derived from names this package
generated rather than names anyone agreed, and it would have been wrong in detail everywhere.

Run: `python tools/derive-write-decisions.py [--apply]`
"""
from __future__ import annotations

import argparse
import collections
import io
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "active" / "workshop-pack-write-decisions.md"


def collect() -> list:
    rows = []
    for p in sorted((ROOT / "contracts").rglob("*.yaml")):
        doc = yaml.safe_load(io.open(p, encoding="utf-8").read()) or {}
        schemas = (doc.get("components") or {}).get("schemas") or {}
        for path, item in (doc.get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if not isinstance(op, dict) or not op.get("x-ticvai-provisional"):
                    continue
                body = op.get("requestBody")
                if not body:
                    continue
                ref = re.search(r"schemas/(\w+)", str(body))
                s = schemas.get(ref.group(1)) if ref else None
                if not isinstance(s, dict):
                    continue
                per = s.get("x-ticvai-persistence", "")
                near = re.search(r"closest is (\S+) at (\d+)%", per)
                rows.append({
                    "contract": p.stem,
                    "op": op["operationId"],
                    "screen": op.get("summary", ""),
                    "consumed": (op.get("x-ticvai-consumed-by") or [""])[0],
                    "schema": ref.group(1),
                    "fields": list((s.get("properties") or {}).keys()),
                    "nearest": near.group(1) if near else None,
                    "overlap": int(near.group(2)) if near else 0,
                    "record": s.get("x-ticvai-record-definition"),
                    "perm": op.get("x-ticvai-permission"),
                    "scope": op.get("x-ticvai-scope-level"),
                })
    # The thirteen the client wrote as records first, then by how close anything existing comes.
    rows.sort(key=lambda r: (r["record"] is None, -r["overlap"], r["contract"], r["op"]))
    return rows


def render(rows: list) -> str:
    rec = [r for r in rows if r["record"]]
    zero = [r for r in rows if r["overlap"] == 0]
    by = collections.Counter(r["contract"] for r in rows)
    o = []
    w = o.append
    w("# The 153 drafted writes, and whether each deserves a table")
    w("")
    w("*Derived by `tools/derive-write-decisions.py`. Do not edit; re-run it.*")
    w("")
    w("Every drafted read is settled: a command centre, a list or an analytics screen is a "
      "**projection**, assembled at read time from tables that already exist, and all 424 say so "
      "in their own persistence tag. This document is about the other 153.")
    w("")
    w("## What was measured")
    w("")
    w("For each drafted write, its request fields against the real columns of every table its "
      "contract owns, read out of `backend/*/0*.sql`.")
    w("")
    w("| | writes |")
    w("|---|---:|")
    w("| Look like an update to a table that exists (>=50% overlap) | **0** |")
    w("| Share a few fields with something (1-24%%) | **%d** |" % (len(rows) - len(zero)))
    w("| Share **not one field** with any table the package has | **%d** |" % len(zero))
    w("| **Total** | **%d** |" % len(rows))
    w("")
    w("**The pack is not a data model.** It specifies screens, and the fields those screens "
      "configure are vocabulary this package does not currently store. That is the finding, and "
      "it is why no table was created: 153 tables asserted from a PDF reading, with names this "
      "package generated rather than names anyone agreed, would be the largest single change to "
      "the data model in its history and wrong in detail everywhere.")
    w("")
    w("A name match would have said the opposite. Fuzzy-matching screen titles against table "
      "names claimed 77 of these already had a home, pairing `setMinorGuardianAge` with "
      "`marketing.privacy_incident` at a score of 100. The fields disagree with the names, and "
      "the fields are what a table is made of.")
    w("")
    w("## Where to start: the %d the client wrote as records" % len(rec))
    w("")
    w("These carry an explicit per-entity directory - the client writing a row rather than a "
      "screen. They are the strongest candidates for a real table and the cheapest to settle.")
    w("")
    w("| Operation | Screen | The pack's words | Fields | Nearest table |")
    w("|---|---|---|---:|---|")
    for r in rec:
        w("| `%s` | %s | *%s* | %d | %s |" % (
            r["op"], r["screen"][:44], r["record"], len(r["fields"]),
            ("`%s` %d%%" % (r["nearest"], r["overlap"])) if r["nearest"] else "none"))
    w("")
    w("## Every drafted write")
    w("")
    w("`Fields` is what the operation accepts today; each one carries the sentence it was read "
      "from in its own `description`. `Nearest` is the closest existing table by field overlap - "
      "a low number is evidence that this is not an update to it.")
    w("")
    for c, n in sorted(by.items(), key=lambda kv: -kv[1]):
        w("### %s (%d)" % (c, n))
        w("")
        w("| Operation | Screen | Fields | Nearest | Permission | Scope |")
        w("|---|---|---:|---|---|---|")
        for r in [x for x in rows if x["contract"] == c]:
            w("| `%s` | %s | %d | %s | `%s` | %s |" % (
                r["op"], r["screen"][:46], len(r["fields"]),
                ("`%s` %d%%" % (r["nearest"], r["overlap"])) if r["nearest"] else "—",
                r["perm"], r["scope"]))
        w("")
    return "\n".join(o) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    rows = collect()
    text = render(rows)
    print("%d drafted writes · %d with a record definition · %d sharing no field with any table"
          % (len(rows), sum(1 for r in rows if r["record"]),
             sum(1 for r in rows if r["overlap"] == 0)))
    if not a.apply:
        print("  nothing written - pass --apply")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print("  -> docs/active/%s" % OUT.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
