#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A rank with no name is a hole on the board. Give it `Player-4821`.

The leaderboard shipped this afternoon with `nickname` nullable and a stated rule: a guest who
has not chosen one appears as a rank with no name, because standings that skip people are wrong
about who is second. **The first half was right and the second half was a worse answer than it
looked.** A board reading

    1  Sara        4,910
    2  —           4,780
    3  Marwan      4,655

is a board that has told second place they do not count, every time they look at it. **The whole
point of a leaderboard is being on it.**

**Decided 20 September, Chinmay: default to a generated name — `Player-4821`.** Everyone has a
name, nobody is a dash, and the nickname the guest chooses replaces it.

## Generated, stable, and carrying nothing

    generated from    the loyalty position's own id, not the subject id and not a counter
    stable            the same guest is the same Player-N next month; a name that changes
                      between views is one nobody can be congratulated by
    carries nothing   it is not a rank, not a join date, not a sequence somebody can
                      count backwards from to learn how many guests a programme has

**It is a fallback, not a value.** `leaderboardNickname` stays null until the guest sets one, and
the generated name is computed at read time — storing it would make "has this guest chosen a
name" unanswerable, which is the flag the prompt-on-entry depends on.

**The window is confirmed monthly.** `week` and `season` stay available; `month` is the default
and what the product runs on.

    python3 tools/applied/bl-173-default-nickname-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CRM = os.path.join(ROOT, "contracts", "satellite", "marketing-crm.yaml")

OLD_ENTRY = """        nickname:
          type: string
          nullable: true
          description: >
            **Null where the guest has not chosen one, and never their real name.** The row still
            appears, because standings that skip people are wrong about who is second.
"""

NEW_ENTRY = """        nickname:
          type: string
          description: >
            **Always present, and never their real name.** The guest's chosen
            `leaderboardNickname` where they have set one, and otherwise a generated
            `Player-4821`.

            **Not nullable, because a rank with no name is a hole on the board.** The first cut
            of this returned null and left second place reading as a dash, which tells somebody
            they do not count every time they look — and being on the board is the whole point of
            the board.

            **Generated from the loyalty position's own id**, not from the subject id and not
            from a counter: it is stable across months, so the same guest is the same
            `Player-N` and can be congratulated by it, and it carries nothing — no rank, no join
            date, and no sequence anybody can count backwards from to learn how many guests a
            programme has.
"""

OLD_NICK = """            **Null means no name on the board, not a fallback to a real one.** Displaying
            `pii.subject.display_name` because a nickname was missing would disclose, silently,
            on the day a guest first placed — which is the case this field exists to prevent.
"""

NEW_NICK = """            **Null means the guest has not chosen one yet, and the board shows a generated
            `Player-4821` in its place** — never `pii.subject.display_name`, which would
            disclose silently on the day a guest first placed and is the case this field exists
            to prevent.

            **The generated name is computed at read time and not stored here.** Writing it would
            make *"has this guest chosen a name"* unanswerable, and that flag is what the
            prompt-on-reaching-the-board depends on.
"""

OLD_WINDOW = """      - name: window
        in: query
        description: '**Bounded on purpose.** An all-time board is won once and then stops being a
          reason to come back.'
        schema:
          type: string
          enum: [week, month, season]
          default: month
"""

NEW_WINDOW = """      - name: window
        in: query
        description: '**Monthly, confirmed 20 September.** `week` and `season` remain available and
          the product runs on `month`.

          **Bounded on purpose** — an all-time board is won once and then stops being a reason to
          come back.'
        schema:
          type: string
          enum: [week, month, season]
          default: month
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(CRM, encoding="utf-8").read()

    if "Player-4821" in s:
        print("  already applied")
        return 0

    for label, old, new in (("LeaderboardEntry.nickname", OLD_ENTRY, NEW_ENTRY),
                            ("LoyaltyPosition.leaderboardNickname", OLD_NICK, NEW_NICK),
                            ("listLeaderboard window", OLD_WINDOW, NEW_WINDOW)):
        if s.count(old) != 1:
            print("  !! %s matched %d times" % (label, s.count(old)))
            return 1
        s = s.replace(old, new)
        print("    %s" % label)

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1
    entry = (doc["components"]["schemas"]["LeaderboardEntry"] or {})
    props = entry.get("properties") or {}
    if props.get("nickname", {}).get("nullable"):
        print("  !! nickname is still nullable")
        return 1
    if "subjectId" in props:
        print("  !! LeaderboardEntry carries a subjectId — that defeats the nickname")
        return 1
    req = set(entry.get("required") or [])
    if "nickname" not in req:
        entry.setdefault("required", []).append("nickname")
        s = s.replace("""      required:
      - rank
      - points
""", """      required:
      - rank
      - nickname
      - points
""", 1)
        print("    LeaderboardEntry  nickname now required")
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (yaml.safe_load(s).get("paths") or {}).values()
                   for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1
    print("    parses · %d operations intact" % parsed_n)

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(CRM, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/marketing-crm.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
