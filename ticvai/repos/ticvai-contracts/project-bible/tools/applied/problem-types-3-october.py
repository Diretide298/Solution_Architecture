#!/usr/bin/env python3
"""Name the problem type of every Sprint 1 error response whose description already names its cause (CHG-R1S-021).

**Found by the r1 gate on 3 October 2026**: on SVC-ORDER-ORDERS-12, SVC-WHITELABEL-CONTENT-7, SVC-LEDGER-TAX-4 and
SVC-TENANCY-MATRIX-1 the judge could not write the contract test for an operation-specific error, because the
response declared no `x-ticvai-problem-types` although the shared `Problem` says "an operation-specific error
declares its own type, one per cause". Scripted: 735 such responses across the package, 99 on Sprint 1 operations.

**Most already name their causes in the description**, in backticks (`shareNotActive`, `cartExpired`,
`alreadyCaptured`) or as "problem type `deposit-box-closed`". This writes those names, in kebab case, as the
response's `x-ticvai-problem-types`. A backticked word that is a property or parameter name or an operation
somewhere in the contracts (`lineIds`, `createRefund`), or a single word (`accepted`), is not a cause and is skipped; a response with no cause
left is not guessed at and stays on the ratchet in `tools/check-problem-types.py`.

Edits are spliced into the text (one line after the response's `description`), so nothing else in a contract moves.

    python tools/applied/problem-types-3-october.py [--apply]
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOK = re.compile(r"`([a-z][a-zA-Z0-9]+(?:-[a-z0-9]+)*)`")


def kebab(s: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", s).lower()


def sprint1_ops() -> set:
    p = os.path.join(ROOT, "handoff", "service-docs", "op-release.json")
    rel = json.load(io.open(p, encoding="utf-8"))
    out = set()
    for t in rel["tickets"]:
        if t.get("type") == "Task" and str(t.get("sprint") or "") == "1":
            for b in t.get("builds") or []:
                k, _, v = b.partition(" ")
                if k == "operation":
                    out.add(v.split("#")[-1])
    return out


def field_words(docs) -> set:
    words = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in (x.get("properties") or {}).items():
                words.add(k)
            for k, v in x.items():
                if k == "parameters" and isinstance(v, list):
                    words.update(str(p.get("name")) for p in v if isinstance(p, dict) and p.get("name"))
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for d in docs.values():
        walk(d)
        # a status value is a state, not a cause: `onSale`, `pendingClosure`
        for n, s in ((d.get("components") or {}).get("schemas") or {}).items():
            if isinstance(s, dict) and n.endswith("Status"):
                words.update(str(e) for e in s.get("enum") or [])
        for item in (d.get("paths") or {}).values():
            for op in (item or {}).values():
                if isinstance(op, dict) and op.get("operationId"):
                    words.add(op["operationId"])
    return words


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    s1 = sprint1_ops()
    files = sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml")))
    docs = {f: yaml.load(io.open(f, encoding="utf-8"), Loader=yaml.CSafeLoader) or {} for f in files}
    fields = field_words(docs)
    done, skipped = [], []
    for f in files:
        targets = []
        for p, item in (docs[f].get("paths") or {}).items():
            for v, op in (item or {}).items():
                if not isinstance(op, dict) or op.get("operationId") not in s1:
                    continue
                for code, r in (op.get("responses") or {}).items():
                    c = str(code)
                    if c[0] not in "45" or c == "429" or not isinstance(r, dict) or "$ref" in r \
                            or r.get("x-ticvai-problem-types"):
                        continue
                    desc = str(r.get("description") or "")
                    named = re.findall(r"problem type `([a-z0-9-]+)`", desc)
                    toks = [t for t in TOK.findall(desc) if t not in fields and len(t) > 4]
                    slugs = list(dict.fromkeys(named + [kebab(t) for t in toks if "-" in t or re.search("[A-Z]", t)]))
                    if not slugs:
                        skipped.append((op["operationId"], c))
                        continue
                    targets.append((op["operationId"], c, slugs))
        if not targets:
            continue
        raw = io.open(f, encoding="utf-8", newline="").read()
        crlf = "\r\n" in raw
        lines = raw.replace("\r\n", "\n").split("\n")
        for oid, code, slugs in targets:
            i = next(n for n, l in enumerate(lines) if re.match(rf"^\s+operationId: {re.escape(oid)}\s*$", l))
            j = next(n for n in range(i, len(lines)) if re.match(rf"^\s+'{code}':\s*$", lines[n]))
            ind = len(lines[j]) - len(lines[j].lstrip()) + 2
            k = j + 1
            while k < len(lines) and not lines[k].startswith(" " * ind + "content:") and \
                    (len(lines[k]) - len(lines[k].lstrip()) >= ind or not lines[k].strip()):
                if lines[k].startswith(" " * ind) and not lines[k].startswith(" " * (ind + 1)) \
                        and not lines[k].lstrip().startswith("description"):
                    break
                k += 1
            lines.insert(k, " " * ind + f"x-ticvai-problem-types: [{', '.join(slugs)}]")
            done.append((oid, code, slugs))
        t = "\n".join(lines)
        if crlf:
            t = t.replace("\n", "\r\n")
        yaml.load(t, Loader=yaml.CSafeLoader)
        if a.apply:
            io.open(f, "w", encoding="utf-8", newline="").write(t)
    for oid, code, slugs in done:
        print(f"  {oid} {code}: {', '.join(slugs)}")
    print(f"{len(done)} response(s) given their problem types; {len(skipped)} left (no cause named): "
          + ", ".join(f"{o} {c}" for o, c in skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
