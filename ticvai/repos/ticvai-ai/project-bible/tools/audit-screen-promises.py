#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Candidates for a screen that promises more than its operation does, ranked per app for an AI sample (CHG-SWP-005).

**14 October 2026** (the sweep after #27741). GST-073 "Security & Sign-in" offers "Sign a lost device out" and binds
`revokeGuestDevice`, which only stops push notifications to a registered token: the screen promises a security
consequence the contract does not have. Whether a sentence on a screen is a promise the operation keeps is a reading,
not a rule, so this decides nothing. It is a cheap keyword heuristic that ranks (screen, operation) pairs for a
person or an AI to read:

  +3  a security consequence the screen states for the operation (sign out, credentials, lock, erase, revoke access,
      lost or stolen, irreversible) that the operation's summary and description never mention
  +1  any other consequence (cancel, refund, charge, notify, transfer, expire) the contract never mentions
  +2  the screen describes the one operation two ways (a button label and a purpose naming different consequences)

What the screen says of an operation: its `apis` purpose, the label and notes of every component calling it, and the
sentences of the screen's purpose, notes and states that name the operation or that label. Report-only: it is not in
run-checks.py and fails nothing.

    python3 tools/audit-screen-promises.py [--top N] [--out FILE.md]
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

# concept -> (weight, what the screen says, what the contract would say if it does it)
CONCEPTS = {
    "sign-out": (3, r"\bsign(s|ed|ing)?\b[\w ]{0,25}\bout\b|\blog(s|ged|ging)? ?(\w+ )?out\b",
                 r"sign-?out|signs? (\w+ )?out|log ?out|\bsessions?\b|invalidat"),
    "credentials": (3, r"credential|password|passkey|\bpin\b",
                    r"credential|password|passkey|\bpin\b|refresh token|access token"),
    "lost-stolen": (3, r"\blost\b|stolen|theft", r"\blost\b|stolen|theft|no longer ha"),
    "lock": (3, r"\block(s|ed)?\b|\bblock(s|ed)?\b|freez|suspend|disabl", r"\block|\bblock|freez|suspend|disabl"),
    "erase": (3, r"\berase|\bwipe|anonymi[sz]|delete (the|your|this) account|permanently delet",
              r"erase|wipe|anonymi[sz]|delet"),
    "revoke-access": (3, r"revok\w* (the )?access|no longer (get|gets) in|admission|\bentry\b",
                      r"access|admission|\bentry\b|entitlement"),
    "irreversible": (3, r"permanent|irreversib|cannot be undone|for good",
                     r"permanent|irreversib|cannot be undone|terminal|final"),
    "cancel": (1, r"\bcancel", r"cancel"),
    "refund": (1, r"refund|money back|reimburs", r"refund|reimburs|revers"),
    "charge": (1, r"\bcharge[sd]?\b|\bpays?\b|\bpaid\b|\bdebit", r"charge|pay|debit|capture|amount"),
    "notify": (1, r"notif|\bemail|\bsms\b|\bpush\b|\balert", r"notif|email|\bsms\b|push|alert|message"),
    "transfer": (1, r"transfer|hand(s|ed)? over|give (it )?to", r"transfer|hand ?over|recipient"),
    "expire": (1, r"expir|valid until|times? out", r"expir|ttl|valid until|time ?out"),
}
SENT = re.compile(r"(?<=[.!?])\s+")


def concepts(text: str, which: int) -> set:
    return {k for k, v in CONCEPTS.items() if re.search(v[which], text or "", re.I)}


def contract_text(f: dict) -> str:
    op = f["op"]
    bits = [str(op.get("summary") or ""), str(op.get("description") or "")]
    for code, r in (op.get("responses") or {}).items():
        if isinstance(r, dict) and str(code).startswith("2"):
            bits.append(str(r.get("description") or ""))
    return " ".join(bits)


def main() -> int:
    g.force_utf8()
    args = sys.argv[1:]
    top = int(args[args.index("--top") + 1]) if "--top" in args else 20
    out = args[args.index("--out") + 1] if "--out" in args else None
    ops = g.operations()
    rows = []
    for stem, s in g.screens():
        code = stem[:3]
        comps = []
        for reg in ((s.get("layout") or {}).get("regions") or []):
            for c in (reg.get("components") or []) if isinstance(reg, dict) else []:
                if isinstance(c, dict):
                    comps.append(c)
        prose = " ".join(str(x or "") for x in [s.get("purpose"), s.get("notes")]
                         + list((s.get("states") or {}).values()))
        sentences = [x for x in SENT.split(prose) if x.strip()]
        seen = set()
        for a in s.get("apis") or []:
            o = a.get("operationId") if isinstance(a, dict) else None
            f = ops.get(o)
            if not f or o in seen or f["method"] == "get":
                continue                      # a consequence is an act's: reads are not scored
            seen.add(o)
            labels = [str(c.get("label") or "") for c in comps if c.get("operation") == o]
            said = [str(a.get("purpose") or "")] + labels \
                + [str(c.get("notes") or "") for c in comps if c.get("operation") == o]
            said += [x for x in sentences if o in x or any(lb and lb.lower() in x.lower() for lb in labels)]
            screen_side = " ".join(said)
            have = concepts(contract_text(f), 2)
            claimed = concepts(screen_side, 1)
            missing = sorted(claimed - have)
            score = sum(CONCEPTS[k][0] for k in missing)
            purpose_c = concepts(str(a.get("purpose") or ""), 1)
            label_c = set().union(*(concepts(lb, 1) for lb in labels)) if labels else set()
            split = bool(purpose_c and label_c and not (purpose_c & label_c))
            if split:
                score += 2
            if score <= 0:
                continue
            rows.append((code, score, s["id"], o, f["method"].upper(), missing, split,
                         (labels[0] if labels else ""), str(a.get("purpose") or "")[:90],
                         str(f["op"].get("summary") or "")[:80]))
    by = collections.defaultdict(list)
    for r in rows:
        by[r[0]].append(r)
    lines = ["# Screen promises against their operations: candidates for an AI sample (CHG-SWP-005)", "",
             "Generated by `tools/audit-screen-promises.py`. A keyword heuristic: it ranks, it decides nothing. "
             f"{len(rows)} (screen, operation) pairs scored above 0; the top {top} per app follow.", ""]
    for code in sorted(by):
        rs = sorted(by[code], key=lambda r: (-r[1], r[2], r[3]))
        lines += [f"## {code} ({len(rs)} scored)", "",
                  "| # | score | screen | operation | screen says (label / purpose) | not in the contract | contract summary |",
                  "|---|---|---|---|---|---|---|"]
        for i, r in enumerate(rs[:top], 1):
            say = " / ".join(x for x in (r[7], r[8]) if x).replace("|", "/")
            miss = ", ".join(r[5]) + (" (label and purpose disagree)" if r[6] else "")
            lines.append(f"| {i} | {r[1]} | {r[2]} | {r[4]} {r[3]} | {say} | {miss} | {r[9].replace('|', '/')} |")
        lines.append("")
    text = "\n".join(lines) + "\n"
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"audit-screen-promises: {len(rows)} pair(s) scored; top {top} per app written to {out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
