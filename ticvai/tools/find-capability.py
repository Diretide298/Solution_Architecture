#!/usr/bin/env python3
"""Search every contract, schema and screen for a capability.

    python3 tools/find-capability.py "wayfind" "venue map" "interactive map"
    python3 tools/find-capability.py --json "footer"
    python3 tools/find-capability.py --file queries.json

Each argument is a regular expression, matched case-insensitively. A capability is present if
**any** of them hits.

**Why this is a tool and not a grep.** The requirement walk marks a row `GAP_CONTRACT` when no
contract serves it, and on 18 August four of eighty-three verdicts in section 19.2 were wrong
because the search was over operation ids and summaries alone:

  * **Emergency notification** was called a gap. `workforce.publishAnnouncement` carries an
    `emergency` kind, with offline-queued acknowledgement and a screen behind it — the
    capability sits in a *description*, and the operation is called `publishAnnouncement`.
  * **Guest merchandise purchase** was called uncovered because the search looked for
    `x-ticvai-guest-callable` and the marker in use was `x-ticvai-audience: [guest]`.
  * **Family profiles** was called absent everywhere. `access.FacePassEnrolment` has a
    `guardianSubjectId` — a *schema property*, invisible to any operation-name scan.
  * **Fast track** was called covered, generously, as a product type. Nothing anywhere.

The corpus below is therefore everything a capability can hide in: descriptions, summaries,
titles, enum values, operation ids, the screens an operation is consumed by, schema names,
schema property names, and screen definitions with their purposes. **A gap verdict is only
worth writing after this returns nothing.**
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

import yaml

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


TEXT_KEYS = ("description", "summary", "title")


def _warn_escaped_pipe(terms):
    """`\\|` is an alternation in grep and a **literal pipe character** in Python's `re`.

    Terms here are joined with `|` already, so a caller who writes `"a\\|b"` out of grep habit
    searches for the one string `a|b`, matches nothing, and reads `NOTHING ANYWHERE` as
    evidence of a gap. That happened on 18 August: `"b2b credit\\|creditLimit"` reported
    nothing while `creditLimit` alone returns `setB2bCreditLimit`, `overrideCreditLimit` and
    `CreditPosition`. **A false negative here becomes a wrong GAP_CONTRACT verdict**, so it is
    worth interrupting for.
    """
    bad = [t for t in terms if "\\|" in t]
    if bad:
        print("  WARN  escaped pipe in " + ", ".join(repr(b) for b in bad) +
              " — `\\|` matches a literal '|' here, not alternation. Pass each alternative as "
              "its own argument. A miss caused by this reads exactly like a real gap.",
              file=sys.stderr)


def _walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in TEXT_KEYS and isinstance(v, str):
                out.append((f"{path}/{k}", v))
            elif k == "enum" and isinstance(v, list):
                out.append((f"{path}/enum", " ".join(str(x) for x in v)))
            elif k == "operationId":
                out.append((f"{path}/operationId", str(v)))
            elif k == "x-ticvai-consumed-by" and isinstance(v, list):
                out.append((f"{path}/consumed-by", " ".join(str(x) for x in v)))
            else:
                _walk(v, f"{path}/{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, f"{path}[{i}]", out)


def _walk_all(node, path, out):
    """Every string in the document, keyed by where it sits.

    Used for states, events and flows only. Contracts have a settled vocabulary and walking
    them this way would bury a real hit under boilerplate; these files do not, and a missed
    hit here becomes a wrong GAP_CONTRACT verdict.
    """
    if isinstance(node, dict):
        for k, v in node.items():
            _walk_all(v, f"{path}/{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk_all(v, f"{path}[{i}]", out)
    elif isinstance(node, str) and len(node) > 2:
        out.append((path, node))


def build_corpus():
    contracts, schemas, screens, models = [], [], [], []
    for f in sorted(glob.glob("contracts/*/*.yaml")):
        name = os.path.basename(f)[:-5]
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        found = []
        _walk(doc, "", found)
        for p, t in found:
            contracts.append((name, p, t))
        for sname, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            if isinstance(body, dict):
                props = " ".join((body.get("properties") or {}).keys())
                schemas.append((name, sname, props))
    for f in sorted(glob.glob("screens/P*.yaml")):
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        code = doc["platform"]["code"]
        for s in doc.get("screens") or []:
            ops = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
            screens.append((code, s["id"], s.get("name", ""), ops, str(s.get("purpose", ""))))

    # States, events and flows. **Searching contracts and screens alone made `NOTHING ANYWHERE`
    # mean less than it said.** A capability can be a state transition with no operation to
    # reach it — which is CF-117's shape exactly, where six states were checked against nothing
    # — or an async event with no synchronous caller, or a step a journey depends on and no
    # contract declares, which is CF-49's. Each is reported under its own kind rather than
    # merged, because *in a flow but not a contract* and *in a contract but no flow* are
    # opposite findings and lumping them together loses both.
    for kind, pattern in (("state", "states/*.yaml"),
                          ("event", "events/*.yaml"),
                          ("flow", "flows/*.yaml")):
        for f in sorted(glob.glob(pattern)):
            base = os.path.basename(f)
            if base.startswith("_"):          # _schema.yaml describes the shape, not a model
                continue
            doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
            found = []
            _walk(doc, "", found)
            # States and flows carry their meaning under their own key names — `action`,
            # `outcome`, `behaviour`, `condition`, `guard`, `trigger`, `notes` — none of which
            # is `description`. Walking for prose keys alone found three hits for `oversell`
            # and missed the two in `flows/F01` and `F07` that a plain grep finds, so the
            # sweep has to take every string value in these files.
            _walk_all(doc, "", found)
            for path, text in found:
                models.append((kind, base[:-5], path, text))
    return contracts, schemas, screens, models


def search(terms, corpus, limit=10):
    contracts, schemas, screens, models = corpus
    rx = re.compile("|".join(terms), re.I)
    hits = {"contracts": [], "schemas": [], "screens": [], "models": []}
    seen = set()
    for name, path, text in contracts:
        if rx.search(text):
            key = (name, text[:80])
            if key in seen:
                continue
            seen.add(key)
            hits["contracts"].append(
                {"contract": name, "at": path, "text": " ".join(text.split())[:200]})
    for name, sname, props in schemas:
        if rx.search(sname) or rx.search(props):
            hits["schemas"].append({"contract": name, "schema": sname, "properties": props[:200]})
    for code, sid, sname, ops, purpose in screens:
        if rx.search(sname) or rx.search(purpose):
            hits["screens"].append({"platform": code, "id": sid, "name": sname,
                                    "operations": ops, "purpose": purpose[:160]})
    for kind, name, path, text in models:
        if rx.search(text):
            key = (kind, name, text[:80])
            if key in seen:
                continue
            seen.add(key)
            hits["models"].append({"kind": kind, "name": name, "at": path,
                                   "text": " ".join(text.split())[:200]})
    hits["total"] = sum(len(hits[k]) for k in ("contracts", "schemas", "screens", "models"))
    # **The asymmetry is the finding.** Present in a flow or a state and absent from every
    # contract means a journey depends on something undeclared — CF-49's shape, a decision
    # reaching an artefact without passing through a requirement. The reverse means a contract
    # nothing exercises.
    hits["modelOnly"] = bool(hits["models"]) and not (hits["contracts"] or hits["schemas"])
    return hits


def render(label, hits, limit):
    print(f"\n{'=' * 94}\n{label}\n{'=' * 94}")
    if not hits["total"]:
        print("  NOTHING ANYWHERE — a gap verdict is safe")
        return
    for h in hits["contracts"][:limit]:
        print(f"  [{h['contract']}] {h['at'][-44:]:<44} {h['text'][:104]}")
    if len(hits["contracts"]) > limit:
        print(f"  … {len(hits['contracts']) - limit} more contract hits")
    for h in hits["schemas"][:limit]:
        print(f"  SCHEMA [{h['contract']}] {h['schema']:<28} {h['properties'][:88]}")
    for h in hits["screens"][:limit]:
        ops = ", ".join(h["operations"])[:62] or "(no operations)"
        print(f"  SCREEN [{h['platform']}] {h['id']:<9}{h['name'][:32]:<32} {ops}")
    for h in hits["models"][:limit]:
        print(f"  {h['kind'].upper():<6} [{h['name'][:22]:<22}] {h['text'][:88]}")
    if len(hits["models"]) > limit:
        print(f"  … {len(hits['models']) - limit} more state, event or flow hits")
    if hits["modelOnly"]:
        print("  >> ONLY in states, events or flows — no contract declares this. A journey or a"
              " state model depends on something undeclared (CF-49's shape).")
    print(f"  — {hits['total']} hit(s)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*", help="regular expressions, any of which may match")
    ap.add_argument("--file", help='JSON: [["label", ["term", ...]], ...]')
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    if not args.terms and not args.file:
        ap.error("give some terms, or --file")

    corpus = build_corpus()
    queries = json.load(open(args.file, encoding="utf-8")) if args.file \
        else [(" | ".join(args.terms), args.terms)]

    results = {}
    for label, terms in queries:
        _warn_escaped_pipe(terms)
        hits = search(terms, corpus)
        results[label] = hits
        if not args.json:
            render(label, hits, args.limit)

    if args.json:
        print(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
