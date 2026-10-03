#!/usr/bin/env python3
"""An operation-specific error response names its problem types; the count without them only falls (CHG-R1S-021).

**Found by the r1 gate on 3 October 2026**: a developer cannot contract-test an error whose `type` nobody named,
and the shared `Problem` says an operation-specific error "declares its own type, one per cause" in
`x-ticvai-problem-types`. The package had 735 4xx/5xx responses (not `$ref`s to the shared ones, not 429) without
it; `tools/applied/problem-types-3-october.py` named the 28 Sprint 1 responses whose descriptions already named
their causes. The rest is a ratchet: **a new response without problem types fails**, and the ceiling is lowered
as they are named.

    python tools/check-problem-types.py [--list]
"""
from __future__ import annotations

import glob
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 3 October 2026, after CHG-R1S-021 (and the problem types added with CHG-R1S-007/017/018/020). Lower it as
# responses are named; never raise it.
CEILING = 707


def main() -> int:
    missing = []
    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        d = yaml.load(io.open(f, encoding="utf-8"), Loader=yaml.CSafeLoader) or {}
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
    n = len(missing)
    if n > CEILING:
        print(f"FAIL {n} operation-specific error responses without x-ticvai-problem-types, above the ceiling of "
              f"{CEILING}: a new one must name its causes (CHG-R1S-021)")
        return 1
    print(f"ok: {n} error responses still without problem types (ceiling {CEILING}; it only falls)"
          + ("  -- lower CEILING to %d" % n if n < CEILING else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
