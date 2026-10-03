#!/usr/bin/env python3
"""Tag the A1 controls whose AI producer moved to Block A2 'Later' (CHG-RONEP-010, 3 October 2026). A one-off.

Chinmay, 3 October ("Block A pace and AI scope"; docs/active/decisions/answers-3-october-r1-plan.md): no AI-engineer
overtime; the AI work no A1 screen needs to work end to end moves to Block A2. AI-ENGINE-PLANNER (the planner agent) and
AI-ENGINE-SUGGESTIONS (the day-one suggestions) moved (block-a-extra-tasks.json `drop: A2`). The operation the A1
screens call, requestSuggestion, is still built in A1 (its back-end task), so the completeness rule holds; what moves
is the AI that answers it. So the binding on each A1 screen that calls it for those answers says 'Later' in its
purpose: BO-005 (queue balancing), GST-031 and WEB-044 (wait time and upsell, from the conversation), GST-054 (the
planner's refinement; the rules plan still answers). Only these screens are spliced back, at their file's dump width
(tools/applied/spec-screen-patterns-3-october.py ScreenFiles). A second run says there is nothing to tag. Revert it
with the commit of CHG-RONEP-010.

    python3 tools/applied/ai-later-r1-plan-3-october.py [--dry-run]
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAGS = {
    "BO-005": "the queue-balancing suggestion of the day-one suggestions (AI-ENGINE-SUGGESTIONS)",
    "GST-031": "the wait-time and upsell suggestions of the day-one suggestions (AI-ENGINE-SUGGESTIONS)",
    "WEB-044": "the wait-time and upsell suggestions of the day-one suggestions (AI-ENGINE-SUGGESTIONS)",
    "GST-054": "the planner agent's refinement in chat (AI-ENGINE-PLANNER); the rules plan still answers in A1",
}


def main() -> int:
    spec = importlib.util.spec_from_file_location("ssp", ROOT / "tools" / "applied" / "spec-screen-patterns-3-october.py")
    ssp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ssp)
    sf = ssp.ScreenFiles()
    done = []
    for sid, what in TAGS.items():
        for a in sf.screens[sid].get("apis") or []:
            if isinstance(a, dict) and a.get("operationId") == "requestSuggestion" and "CHG-RONEP-010" not in a.get("purpose", ""):
                p_ = a.get("purpose", "").rstrip()
                a["purpose"] = (f"{p_}{'' if p_.endswith('.') else '.'} Later (CHG-RONEP-010): {what} ships in Block A2 "
                                "(Chinmay, 3 October); until then the control shows 'Later'.")
                sf.dirty.add(sid)
                done.append(sid)
    if not done:
        print("nothing to tag")
        return 0
    print("tagged:", ", ".join(done))
    if "--dry-run" not in sys.argv:
        print("written:", ", ".join(sf.write()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
