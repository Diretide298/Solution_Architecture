#!/usr/bin/env python3
"""The lineage half of ADAM CR-078 and the written stub tables (14 October 2026, CHG-CRD-001 to CHG-CRD-008).

**Found by the r6 settlement of 14 October** (ADAM CR-078, ticket 27750): `identity.principal_credential` held only
`id` and a nullable `principal_id`, and five other tables the lineage writes were the same skeleton
(`identity.mfa_challenge`, `identity.mfa_recovery_code`, `identity.otp_challenge`, `approvals.escalation`,
`ai.index_entry`, `games.credit_ledger`). The contracts now give each a schema with the columns its operations need
(`PrincipalCredential`, `MfaChallenge`, `MfaRecoveryCode`, `OtpChallenge`, `ApprovalRequest.escalations[]`,
`IndexEntry`, `GameCreditMovement`), edited by hand in the same commits. This one-off gives the existing lineage
entries the tables those operations' own descriptions now say they read and write, as
`contracts-s12-4-october.py` did for CHG-FXC-004: `derive-lineage` only adds missing operations and never updates an
entry, so a change to an existing entry is made here and its result committed.

The new operation `verifySupervisorStepUp` (CHG-CRD-004) is added to the lineage by `derive-lineage --apply` first;
a run of this script after it fills its reads and writes.

    python tools/applied/credentials-and-stubs-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# Tables the contracts declare and the schema reference has not seen until the next derive-schema.
NEW_TABLES = {"identity.principal_credential_history"}

PC, PCH, PP = "identity.principal_credential", "identity.principal_credential_history", "identity.password_policy"

# operationId -> (reads to add, writes to add, writes to drop, reads to drop, why)
LINEAGE = {
    # ── CHG-CRD-001: the staff credential ───────────────────────────────────────────────────────────────────────
    "login": ([PP], [PC], [], [],
              "the credential's hash, its lockout counted against the tenant's policy (PrincipalCredential)"),
    "changeOwnCredential": ([PCH], [PCH, "identity.principal"], [], [],
                            "the reuse check reads the history; the replaced hash is kept there; mustChangeCredential is "
                            "cleared on the principal"),
    "resetPrincipalCredential": ([PP], [PCH, "identity.principal"], [], [],
                                 "the PIN length and policy; the replaced hash is kept; mustChangeCredential is set"),
    "createPrincipal": ([PP], [], [], [],
                        "initialCredential is held to the policy before its hash is stored"),
    "forceLogout": ([PP], [PC], [], [],
                    "a wrong supervisor PIN counts towards the PIN lockout"),
    # ── CHG-CRD-004: the step-up query's service route ──────────────────────────────────────────────────────────
    "verifySupervisorStepUp": (["identity.principal", PC, PP, "identity.delegated_access", "identity.role_permission"],
                               [PC], [], [],
                               "the PIN against its hash and lockout, the permission through live grants; a wrong PIN "
                               "is counted"),
    # ── CHG-CRD-005: MFA and one-time codes ─────────────────────────────────────────────────────────────────────
    "createMfaChallenge": (["identity.mfa_challenge", "identity.session"], [], [], [],
                           "an earlier pending challenge for the action is voided; the challenge is bound to the session"),
    "verifyMfaChallenge": ([PP], [], [], [],
                           "five wrong codes lock step-up for the policy's lockout minutes"),
    "requestGuestOtp": (["identity.otp_challenge"], [], [], [],
                        "a newer code invalidates the older one for the identifier and purpose; resendAfter"),
    "verifyGuestOtp": ([], ["identity.otp_challenge"], [], [],
                       "wrong codes are counted and a correct one is consumed"),
}


def apply_lineage(apply: bool) -> int:
    path = os.path.join(ROOT, "handoff", "api-data-lineage.json")
    lin = json.load(io.open(path, encoding="utf-8"))
    sref = json.load(io.open(os.path.join(ROOT, "handoff", "schema-reference.json"), encoding="utf-8"))["cols"]
    n = 0
    for op, (r_add, w_add, w_del, r_del, why) in LINEAGE.items():
        e = lin.get(op)
        if e is None:  # a new operation: derive-lineage adds it first, then a second run fills it
            print("  %s: not in the lineage yet (run tools/derive-lineage.py --apply first)" % op)
            continue
        for t in r_add + w_add:
            if t not in sref and t not in NEW_TABLES:
                raise SystemExit("%s: %s is not a table" % (op, t))
        reads = (set(e.get("reads") or []) | set(r_add)) - set(r_del)
        writes = (set(e.get("writes") or []) | set(w_add)) - set(w_del)
        if sorted(reads) != sorted(e.get("reads") or []) or sorted(writes) != sorted(e.get("writes") or []):
            e["reads"], e["writes"] = sorted(reads), sorted(writes)
            e["fixNote"] = "14 October 2026 (CHG-CRD-%s, ADAM CR-078): %s" % (
                "004" if op == "verifySupervisorStepUp" else "005" if op in (
                    "createMfaChallenge", "verifyMfaChallenge", "requestGuestOtp", "verifyGuestOtp") else "001", why)
            n += 1
        if e.get("pure") and [t for t in e["writes"] if ":" not in t]:
            del e["pure"]
            n += 1
    if apply:
        io.open(path, "w", encoding="utf-8").write(json.dumps(lin, indent=1, ensure_ascii=False))
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not a.apply:
        print("%d lineage entries listed; pass --apply" % len(LINEAGE))
        return 0
    print("lineage entries changed: %d" % apply_lineage(True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
