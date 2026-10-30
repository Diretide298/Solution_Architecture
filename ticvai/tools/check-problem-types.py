#!/usr/bin/env python3
"""An operation-specific error response names its problem types; the count without them only falls (CHG-R1S-021).

**Found by the r1 gate on 3 October 2026**: a developer cannot contract-test an error whose `type` nobody named,
and the shared `Problem` says an operation-specific error "declares its own type, one per cause" in
`x-ticvai-problem-types`. The package had 735 4xx/5xx responses (not `$ref`s to the shared ones, not 429) without
it; `tools/applied/problem-types-3-october.py` named the 28 Sprint 1 responses whose descriptions already named
their causes. The rest is a ratchet: **a new response without problem types fails**, and the ceiling is lowered
as they are named.

**An amendment that can clash on a unique code says so** (ADAM CR-340, CHG-CR340-001):
`updateAccreditationProgramme` replaced a programme whole, `code` included (`x-ticvai-unique: tenant`), and its `409`
listed only `programme-is-template`, so a code another programme held surfaced as a 500. A PUT or PATCH on one
resource (a path parameter) whose body carries a writable `x-ticvai-unique` field, other than the key the path names
the row by, answers a `409` that lists `duplicate-code` (in `x-ticvai-problem-types`, or the shared `DuplicateCode`).
The ones still without it are a second ratchet (UNIQUE_CEILING): a new one fails.

    python tools/check-problem-types.py [--list]
"""
from __future__ import annotations

import glob
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 3 October 2026, after CHG-R1S-021 (and the problem types added with CHG-R1S-007/017/018/020). Lower it as
# responses are named; never raise it.
CEILING = 112  # 26 October 2026, r10 (was 114: the r10 lanes named two, CHG-R10GEN-008); 20 October 2026, the r8 walk fix (was 115: removeLicenceAddOn 409 named, CHG-R8WFC-003); the r8 integration pass (was 117, CHG-R8INT-011); 15 October: 117 at the r6 gate (was 168, CHG-SHP-001): 531 operation-specific errors named in the Block A audit

# 30 October 2026, CHG-CR340-001: setApprovalExternalProvider, updateResourceCategory, updateResourceType,
# updateWalletType. Lower it as their 409s name duplicate-code; never raise it.
UNIQUE_CEILING = 4


def _deref(node, stem, by, depth=0):
    while isinstance(node, dict) and "$ref" in node and depth < 10:
        m = re.match(r"^(?:(?:\.\./)?(?:[\w-]+/)?([\w-]+)\.yaml)?#/components/schemas/(\w+)$", str(node["$ref"]))
        if not m:
            return {}, stem
        stem = m.group(1) or stem
        node = by.get((stem, m.group(2))) or {}
        depth += 1
    return node, stem


def _props(node, stem, by, depth=0) -> dict:
    node, stem = _deref(node, stem, by)
    out = {}
    if not isinstance(node, dict) or depth > 5:
        return out
    for sub in node.get("allOf") or []:
        out.update(_props(sub, stem, by, depth + 1))
    out.update({k: v for k, v in (node.get("properties") or {}).items() if isinstance(v, dict)})
    return out


def unique_unanswered(docs) -> list:
    """(file, operationId, field) for a PUT/PATCH on one resource whose body carries a writable x-ticvai-unique
    field (not the key the path names the row by) and whose 409 does not list duplicate-code (ADAM CR-340)."""
    by = {}
    for f, d in docs:
        stem = os.path.splitext(os.path.basename(f))[0]
        for n, s in (((d.get("components") or {}).get("schemas")) or {}).items():
            if isinstance(s, dict):
                by[(stem, n)] = s
    out = []
    for f, d in docs:
        stem = os.path.splitext(os.path.basename(f))[0]
        for p, item in (d.get("paths") or {}).items():
            keys = re.findall(r"\{(\w+)\}", str(p))
            if not keys or not isinstance(item, dict):
                continue
            for v in ("put", "patch"):
                op = item.get(v)
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                body = next((m.get("schema") for m in ((op.get("requestBody") or {}).get("content") or {}).values()
                             if isinstance(m, dict) and m.get("schema") is not None), None)
                if body is None:
                    continue
                uniq = [k for k, s in _props(body, stem, by).items()
                        if s.get("x-ticvai-unique") and not s.get("readOnly") and k != keys[-1]]
                if not uniq:
                    continue
                r = (op.get("responses") or {}).get("409") or (op.get("responses") or {}).get(409)
                ok = isinstance(r, dict) and (str(r.get("$ref") or "").endswith("/DuplicateCode")
                                              or "duplicate-code" in [str(x) for x in r.get("x-ticvai-problem-types") or []])
                if not ok:
                    out.append((os.path.basename(f), op["operationId"], ", ".join(uniq)))
    return out


def main() -> int:
    missing = []
    docs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        d = yaml.load(io.open(f, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}
        docs.append((f, d))
        for p, item in (d.get("paths") or {}).items():
            for v, op in (item or {}).items():
                if not isinstance(op, dict) or not op.get("operationId"):
                    continue
                for code, r in (op.get("responses") or {}).items():
                    c = str(code)
                    if c[0] not in "45" or c == "429" or not isinstance(r, dict) or "$ref" in r:
                        continue
                    if not r.get("x-ticvai-problem-types"):
                        missing.append((os.path.basename(f), op["operationId"], c))
    if "--list" in sys.argv:
        for f, o, c in missing:
            print(f"  {f:<24} {o:<40} {c}")
    rc = 0
    unanswered = unique_unanswered(docs)
    if "--list" in sys.argv:
        for f, o, k in unanswered:
            print(f"  {f:<24} {o:<40} 409 lists no duplicate-code for {k}")
    u = len(unanswered)
    if u > UNIQUE_CEILING:
        print(f"FAIL {u} amendments whose body carries a unique field and whose 409 lists no duplicate-code, above the "
              f"ceiling of {UNIQUE_CEILING}: a new one must answer the clash (ADAM CR-340, CHG-CR340-001)")
        for f, o, k in unanswered:
            print(f"  {f:<24} {o:<40} {k}")
        rc = 1
    else:
        print(f"ok: {u} amendments with a unique field and no duplicate-code 409 (ceiling {UNIQUE_CEILING}; it only falls)"
              + ("  -- lower UNIQUE_CEILING to %d" % u if u < UNIQUE_CEILING else ""))
    n = len(missing)
    if n > CEILING:
        print(f"FAIL {n} operation-specific error responses without x-ticvai-problem-types, above the ceiling of "
              f"{CEILING}: a new one must name its causes (CHG-R1S-021)")
        return 1
    print(f"ok: {n} error responses still without problem types (ceiling {CEILING}; it only falls)"
          + ("  -- lower CEILING to %d" % n if n < CEILING else ""))
    return rc


if __name__ == "__main__":
    sys.exit(main())
