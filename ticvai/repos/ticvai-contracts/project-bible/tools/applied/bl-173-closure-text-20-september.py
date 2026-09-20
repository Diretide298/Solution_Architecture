#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite BL-173's closure note, which a shell ate — the second time today.

Passing prose through `bash -c "..."` makes every `` `identifier` `` a command substitution, so
the names get executed and the text comes back with holes. It happened to BL-179's note an hour
ago, was fixed the same way, **and then happened again here** because the shell was quicker to
reach for than a file.

The entry closed correctly both times; only the prose was damaged. Notes like this one are
written to a file from now on.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PATH = os.path.join(ROOT, "handoff", "contract-backlog.json")

CLOSED_BY = (
    "**Closed 20 September.** Challenges, streaks, milestones, badges and achievements were "
    "already built — `createChallenge`, `getMyChallenges`, `listBadges`, `setBadge`, "
    "`awardBadge`, `listCustomerBadges`, and `Challenge.kind` carrying `streak` and `milestone`. "
    "**The leaderboard was the last piece, and it was a privacy decision before it was an "
    "operation**: a leaderboard shows one guest something about another.\n\n"
    "**Decided by Chinmay: a guest always gets to add a nickname when they reach the board, and "
    "the nickname is what is shown. Always.** `setLeaderboardNickname` writes "
    "`marketing.loyalty_position.leaderboard_nickname`, and **setting it is the consent** — "
    "nothing reads `pii.subject.display_name`, because a name given for one purpose and reused "
    "on a public board is a use nobody agreed to.\n\n"
    "**`LeaderboardEntry` carries `rank`, `nickname`, `points` and no subject identifier, and "
    "that is the whole design.** A nickname beside an id the client can resolve elsewhere is "
    "decoration over a disclosure. The caller finds their own row by `isMe` rather than by "
    "matching identifiers — which is also why the apply script asserts that `subjectId` is "
    "absent rather than trusting it to stay so.\n\n"
    "**A guest with no nickname yet appears as a rank with no name.** Not hidden — standings "
    "that skip people are wrong about who is second — and **never filled in from their real "
    "name**, which would disclose silently on the day they first placed.\n\n"
    "**The window is bounded** (`week`, `month`, `season`): an all-time board is won once and "
    "then stops being a reason to come back. **Moderation is named rather than invented** — "
    "length and pattern stop markup and impersonating whitespace and nothing else, and a "
    "nickname impersonating staff needs a review queue, which is a product decision.\n\n"
    "`x-ticvai-config-scope: subject` is declared on the setter rather than the checker being "
    "widened to excuse it: a nickname is a setting the guest holds, and `subject` is a level "
    "five other operations already use."
)


def main():
    apply = "--apply" in sys.argv[1:]
    B = json.load(io.open(PATH, encoding="utf-8"))
    e = next(x for x in B["entries"] if x["id"] == "BL-173")
    if e.get("closedBy") == CLOSED_BY:
        print("  already applied")
        return 0
    print("    BL-173 closedBy  %d chars -> %d"
          % (len(e.get("closedBy") or ""), len(CLOSED_BY)))
    e["closedBy"] = CLOSED_BY
    print("    status %s · lane %s · closed %s"
          % (e.get("status"), e.get("lane"), e.get("closed")))
    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(
        json.dumps(B, indent=1, ensure_ascii=False))
    print("  -> handoff/contract-backlog.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
