#!/usr/bin/env python3
"""An operation-specific error response names its problem types; the count without them only falls (CHG-R1S-021).

**Found by the r1 gate on 3 October 2026**: a developer cannot contract-test an error whose `type` nobody named,
and the shared `Problem` says an operation-specific error "declares its own type, one per cause" in
`x-ticvai-problem-types`. The package had 735 4xx/5xx responses (not `$ref`s to the shared ones, not 429) without
it; `tools/applied/problem-types-3-october.py` named the 28 Sprint 1 responses whose descriptions already named
their causes. The rest is a ratchet: **a new response without problem types fails**, and the ceiling is lowered
as they are named.

**One status per shared problem type** (r12, ADAM CR-366, CHG-CR366-001). A type the package uses for one cause
everywhere answers with one status everywhere: CR-366 proposed `400 unknown-reference` where the package's code for a
reference the caller cannot use is `422` (ADAM CR-103). `FIXED_STATUS` names them; any other status fails.

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
# r12 (ADAM CR-366): the shared types whose status is fixed. Add a type here when it is settled; never remove one.
FIXED_STATUS = {
    "unknown-reference": "422",  # a reference in the body names nothing the caller can use (ADAM CR-103, CR-366)
    "validation": "400",         # the shared BadRequest (contracts/shared/common.yaml)
}
CEILING = 112  # 26 October 2026, r10 (was 114: the r10 lanes named two, CHG-R10GEN-008); 20 October 2026, the r8 walk fix (was 115: removeLicenceAddOn 409 named, CHG-R8WFC-003); the r8 integration pass (was 117, CHG-R8INT-011); 15 October: 117 at the r6 gate (was 168, CHG-SHP-001): 531 operation-specific errors named in the Block A audit


def main() -> int:
    missing = []
    wrong_status = []
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
                    for t in r.get("x-ticvai-problem-types") or []:
                        if t in FIXED_STATUS and FIXED_STATUS[t] != c:
                            wrong_status.append((os.path.basename(f), op["operationId"], c, t))
                    if not r.get("x-ticvai-problem-types"):
                        missing.append((os.path.basename(f), op["operationId"], c))
    if "--list" in sys.argv:
        for f, o, c in missing:
            print(f"  {f:<24} {o:<40} {c}")
    for f, o, c, t in wrong_status:
        print(f"FAIL {f} {o} answers {t} with {c}; the package answers it with {FIXED_STATUS[t]} everywhere (CR-366)")
    if wrong_status:
        return 1
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
