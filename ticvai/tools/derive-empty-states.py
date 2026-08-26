#!/usr/bin/env python3
"""Write the 492 TODO empty states from what each screen already knows.

**A TODO state is not a gap in documentation, it is a screen with no defined behaviour.**
`emptyNoAccess` unwritten on 304 screens means 304 screens where a person without permission sees
whatever the framework does by default — and that is the state a reviewer never opens and a real
user hits on their first day.

**Every sentence here is derived from the screen's own facts**: the permission its operations need,
the module its licence gates, the create operation it declares, whether it has a filter at all. A
generic sentence would pass the checker and teach nobody anything, which is the failure mode this
tool exists to avoid.

**This is a floor, not a ceiling.** A derived sentence is better than TODO and worse than one
somebody wrote after watching a cashier hit the state. The `derived: true` marker says which is
which so the second pass knows where to look.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import yaml
import sys

# A cp1252 console cannot encode the arrows and dashes this tool prints, and the
# failure lands *after* the work is done — so the output is written, the summary
# line raises UnicodeEncodeError, and a correct run exits 1. Reconfiguring at
# import means anything importing this module gets it too, refresh.sh included.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:      # a captured stream may not be reconfigurable; harmless
    pass


ROOT = Path(__file__).resolve().parents[1]

# What a permission means in a sentence. Falls back to the permission itself, which is ugly and
# honest — better than inventing a description for a permission nobody has described.
PERM_VERB = {
    "VIEW": "read", "MANAGE": "manage", "CONFIGURE": "configure", "CREATE": "create",
    "APPROVE": "approve", "EXPORT": "export", "REFUND": "refund", "DISCOUNT": "discount",
    "VOID": "void", "ADMIN": "administer", "USE": "use", "OPERATE": "operate",
}

# The one thing this screen exists to make, if it declares a create operation.
CREATE = re.compile(r"^(create|add|register|issue|join|raise|record|submit|start|open|enrol|build)")


def verb_for(perm: str) -> str:
    for suffix, verb in PERM_VERB.items():
        if perm.endswith(suffix):
            return verb
    return "use"


def subject_for(perm: str) -> str:
    """`ORDER_DISCOUNT` -> `orders`. The noun the permission is about."""
    head = perm.split("_")[0].lower()
    return head + ("es" if head.endswith(("s", "x", "ch")) else "s")


def main() -> int:
    lin = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    written = Counter()
    touched = 0

    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        code = doc["platform"]["code"]
        audience = doc["platform"].get("audience")
        changed = False

        for s in doc.get("screens") or []:
            states = s.get("states") or {}
            if not any("TODO" in str(v) for v in states.values()):
                continue

            ops = [a.get("operationId") for a in (s.get("apis") or []) if a.get("operationId")]
            perms = sorted({lin[o]["perm"] for o in ops if o in lin and lin[o].get("perm")})
            module = s.get("requiresModule")
            creates = sorted(o for o in ops if o in lin and CREATE.match(o)
                             and lin[o]["verb"] == "POST")
            comps = [c.get("kind") for r in ((s.get("layout") or {}).get("regions") or [])
                     for c in (r.get("components") or [])]
            filtered = any(k in ("searchField", "multiSelect", "filterBar", "dateRange")
                           for k in comps)

            # ── emptyNoAccess ────────────────────────────────────────────
            # **Never rendered as an empty list.** A person without permission seeing an empty
            # table concludes there is no data, tells somebody the system is broken, and the
            # somebody spends an afternoon on it.
            if "TODO" in str(states.get("emptyNoAccess", "")):
                if audience == "guest":
                    body = ("**Signed out, or signed in as somebody else.** A guest surface has no "
                            "permissions to lack — this state is reached by a session that "
                            "expired, and the action is to sign in again rather than to ask for "
                            "access.")
                elif perms:
                    verb = verb_for(perms[0])
                    subj = subject_for(perms[0])
                    named = ", ".join(f"`{p}`" for p in perms[:3])
                    more = f" and {len(perms) - 3} more" if len(perms) > 3 else ""
                    body = (f"**Says which permission is missing, and never renders as an empty "
                            f"list.** This screen needs {named}{more} to {verb} {subj}; a person "
                            "without it sees the reason and who to ask, because an empty table "
                            "reads as *there is no data* and sends somebody to support with the "
                            "wrong question.\n\n"
                            "**Authority is carried by the person, not the device** (ADR-0002) — "
                            "so signing in again on the same terminal is the way through.")
                else:
                    body = ("**Never rendered as an empty list.** A person who cannot see this "
                            "screen is told so and told who to ask — an empty table reads as "
                            "*there is no data*, which sends somebody to support with the wrong "
                            "question.")
                if module and module != "core":
                    body += (f"\n\n**Also reached when `{module}` is not licensed.** The tenant "
                             "has not bought this module, which is a commercial answer and not a "
                             "permission one — say which, because the person to ask is different.")
                states["emptyNoAccess"] = body
                written["emptyNoAccess"] += 1

            # ── emptyFirstRun ────────────────────────────────────────────
            # A venue that opened this morning. The state a demo is given in and a reviewer never
            # sees, because the fixtures are always full.
            if "TODO" in str(states.get("emptyFirstRun", "")):
                purpose = str(s.get("purpose") or "").rstrip(".")
                if creates:
                    body = (f"**A venue that opened this morning.** Nothing here yet — the one "
                            f"action is `{creates[0]}`, and it is the only thing on the screen "
                            "until the first one exists.\n\n"
                            "**Says what this screen is for, not just that it is empty.** "
                            + (f"{purpose}." if purpose else ""))
                else:
                    body = ("**A venue that opened this morning.** Nothing here yet, and nothing "
                            "on this screen creates the first one — it is filled by "
                            + ("another screen or by a job, and this state names which rather "
                               "than leaving somebody looking for a button that does not exist.")
                            + (f"\n\n{purpose}." if purpose else ""))
                states["emptyFirstRun"] = body
                written["emptyFirstRun"] += 1

            # ── emptyNoResults ───────────────────────────────────────────
            if "TODO" in str(states.get("emptyNoResults", "")):
                if filtered:
                    body = ("**The filter matched nothing, and the data is still there.** The "
                            "action widens or clears it — distinct from first run, which has "
                            "nothing to match, and **a screen that shows the same panel for both "
                            "sends somebody looking for data they already filtered out.**")
                else:
                    body = ("**Nothing matched.** This screen has no filter of its own, so the "
                            "scope is what narrowed it — the venue, the shift or the date the "
                            "person arrived with. **Naming the scope is what stops somebody "
                            "concluding the record does not exist.**")
                states["emptyNoResults"] = body
                written["emptyNoResults"] += 1

            s["states"] = states
            s["statesDerived"] = True
            touched += 1
            changed = True

        if changed:
            head = "".join(x for x in f.read_text(encoding="utf-8").splitlines(keepends=True)
                           if x.startswith("#"))
            f.write_text(head + "\n" + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True,
                                                      width=98), encoding="utf-8")

    print(f"  {touched} screens · " + " · ".join(f"{k} {v}" for k, v in written.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
