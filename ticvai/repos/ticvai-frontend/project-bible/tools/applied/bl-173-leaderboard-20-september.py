#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BL-173's last piece: a leaderboard, where every guest on it is a nickname.

Everything else in gamification is built — `createChallenge` ("define a challenge, mission or
streak"), `getMyChallenges`, `listBadges`, `setBadge`, `awardBadge`, `listCustomerBadges`, and
`Challenge.kind` carrying `streak` and `milestone`. **Ranking guests against each other was
not.** `BO-831 Progress, Leaderboards & Hub` is served by `getLoyaltyPosition`, which returns a
guest *their own* points and tier, and `Challenge` has no ranking field.

**Decided 20 September, Chinmay: a guest always gets to add a nickname when they reach the
leaderboard, and the nickname is what is shown. Always.**

## The nickname is only privacy if the response withholds the rest

A leaderboard shows one guest something about another, which is a disclosure before it is a
feature. A nickname protects nobody if the entry beside it carries a `subjectId` — the client
then holds an identifier it can resolve elsewhere, and the nickname is decoration over a
disclosure.

    LeaderboardEntry     rank, nickname, points -- and NO subjectId
    the caller's own row  `isMe: true`, which is how a client highlights it without
                          needing to know who anybody else is

**A position with no nickname yet appears as a rank with no name.** It is not hidden — the
standings would be wrong, and a board that quietly omits people is a board that lies about who
is second. It is not filled in from `pii.subject.display_name` either: **a real name shown
because somebody had not chosen a nickname is the exact disclosure this is designed to prevent**,
and it would arrive silently, on the day they first placed.

**The nickname lives on `marketing.loyalty_position`, not in `pii`.** It is personal data, and
it is the one piece a guest has deliberately chosen for display — the act of setting it is the
consent, which is not true of anything in the PII vault.

**Moderation is not built here.** A nickname is length-bounded and pattern-bounded, which stops
markup and impersonating whitespace, and stops nothing else. **A nickname that impersonates
staff is a product decision and a review queue**, and inventing one inside this change would be
worse than naming the gap.

    python3 tools/applied/bl-173-leaderboard-20-september.py --apply
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CRM = os.path.join(ROOT, "contracts", "satellite", "marketing-crm.yaml")

ANCHOR = "  /guests:\n"

PATHS = """  /loyalty/leaderboard:
    get:
      operationId: listLeaderboard
      x-ticvai-consumed-by:
        - "P08 BO-831 Progress, Leaderboards & Hub"
        - "P02 GST-036 Loyalty & Rewards"
      x-ticvai-audience:
      - guest
      summary: Standings, by nickname
      description: '22.6. **Everyone on the board is a nickname.** A leaderboard shows one guest
        something about another, so the entry carries a rank, a nickname and a score and **no
        subject identifier** — a nickname beside an id the client can resolve elsewhere is
        decoration over a disclosure.

        **The caller''s own row is marked `isMe` rather than named**, which is how a client
        highlights it without being told who anybody else is.

        **A guest who has not set a nickname appears as a rank with no name.** Not hidden — the
        standings would be wrong and a board that omits people lies about who is second — and
        **never filled in from their real name**, which is the disclosure this exists to prevent
        and would arrive silently on the day they first placed.

        '
      tags:
      - loyalty
      x-ticvai-permission: null
      x-ticvai-self-scoped: subject
      x-ticvai-scope-level: tenant
      security:
      - guestAuth: []
      parameters:
      - name: programmeId
        in: query
        required: true
        schema:
          type: string
          format: uuid
      - name: window
        in: query
        description: '**Bounded on purpose.** An all-time board is won once and then stops being a
          reason to come back.'
        schema:
          type: string
          enum: [week, month, season]
          default: month
      - $ref: ../shared/common.yaml#/components/parameters/PageSize
      - $ref: ../shared/common.yaml#/components/parameters/PageCursor
      responses:
        '200':
          description: Standings
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/LeaderboardEntry'
  /loyalty/leaderboard-nickname:
    put:
      operationId: setLeaderboardNickname
      x-ticvai-consumed-by:
        - "P02 GST-036 Loyalty & Rewards"
      x-ticvai-audience:
      - guest
      summary: Choose the name shown on the board
      description: '22.6. **The guest''s own choice, and the only name a leaderboard ever shows.**
        Offered whenever they reach the board, and changeable afterwards.

        **Setting it is the consent.** Nothing here reads `pii.subject`: a display name held in
        the PII vault was given for a different purpose, and reusing it on a public board is a
        use nobody agreed to.

        **Length and pattern bounded, not moderated.** That stops markup and impersonating
        whitespace and stops nothing else — **a nickname impersonating staff needs a review
        queue**, which is a product decision rather than a field constraint.

        '
      tags:
      - loyalty
      x-ticvai-permission: null
      x-ticvai-self-scoped: subject
      x-ticvai-scope-level: tenant
      security:
      - guestAuth: []
      parameters:
      - $ref: ../shared/common.yaml#/components/parameters/IdempotencyKey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
              - nickname
              properties:
                nickname:
                  type: string
                  minLength: 2
                  maxLength: 24
                  pattern: '^[\\p{L}\\p{N}][\\p{L}\\p{N} _.-]{0,22}[\\p{L}\\p{N}]$'
      responses:
        '200':
          description: Set
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoyaltyPosition'
        '409':
          description: Refused by moderation
          content:
            application/problem+json:
              schema:
                $ref: ../shared/common.yaml#/components/schemas/Problem
"""

ENTRY = """    LeaderboardEntry:
      x-ticvai-persistence: none — computed from marketing.loyalty_position
      type: object
      description: >
        22.6. **One row of a leaderboard, and deliberately not enough to identify anybody.**
        There is no `subjectId` here and that is the whole design: a nickname beside a resolvable
        identifier protects nothing.
      required:
      - rank
      - points
      properties:
        rank:
          type: integer
          minimum: 1
        nickname:
          type: string
          nullable: true
          description: >
            **Null where the guest has not chosen one, and never their real name.** The row still
            appears, because standings that skip people are wrong about who is second.
        points:
          type: integer
        isMe:
          type: boolean
          default: false
          description: >
            **How a client highlights the caller's own row without learning who anybody else
            is.** The alternative — returning identifiers and letting the client match — is the
            disclosure this schema exists to avoid.

"""

NICK = """        leaderboardNickname:
          type: string
          nullable: true
          maxLength: 24
          description: >
            BL-173. **The name shown on a leaderboard, chosen by the guest.** Offered whenever
            they reach the board and changeable afterwards; `setLeaderboardNickname` is the only
            thing that writes it.

            **Null means no name on the board, not a fallback to a real one.** Displaying
            `pii.subject.display_name` because a nickname was missing would disclose, silently,
            on the day a guest first placed — which is the case this field exists to prevent.
"""


def main():
    apply = "--apply" in sys.argv[1:]
    s = io.open(CRM, encoding="utf-8").read()

    if "operationId: listLeaderboard" in s:
        print("  already applied")
        return 0

    if s.count(ANCHOR) != 1:
        print("  !! /guests anchor matched %d times" % s.count(ANCHOR))
        return 1
    s = s.replace(ANCHOR, PATHS + ANCHOR)
    print("    +listLeaderboard, +setLeaderboardNickname")

    tag = "      x-ticvai-persistence: marketing.loyalty_position\n"
    i = s.find(tag)
    if i < 0:
        print("  !! LoyaltyPosition persistence tag not found")
        return 1
    j = s.find("        subjectId:\n", i)
    if j < 0:
        print("  !! LoyaltyPosition.subjectId anchor not found")
        return 1
    s = s[:j] + NICK + s[j:]
    print("    LoyaltyPosition  +leaderboardNickname")

    k = s.find("    LoyaltyPosition:\n")
    if k < 0:
        print("  !! LoyaltyPosition schema not found")
        return 1
    s = s[:k] + ENTRY + s[k:]
    print("    LeaderboardEntry  new schema — no subjectId, by design")

    try:
        doc = yaml.safe_load(s)
    except Exception as e:
        print("  !! would not parse: %s" % str(e)[:200])
        return 1
    have = set((doc.get("components") or {}).get("schemas") or {})
    for ref in set(re.findall(r"(?<![\w./-])#/components/schemas/([A-Za-z0-9_]+)",
                              yaml.safe_dump(doc))):
        if ref not in have:
            print("  !! refs %s and does not define it" % ref)
            return 1
    text_n = len(re.findall(r"^      operationId:", s, re.M))
    parsed_n = sum(1 for p in (doc.get("paths") or {}).values() for o in (p or {}).values()
                   if isinstance(o, dict) and o.get("operationId"))
    if text_n != parsed_n:
        print("  !! %d operationId lines, %d parsed" % (text_n, parsed_n))
        return 1

    entry = have and (doc["components"]["schemas"]["LeaderboardEntry"].get("properties") or {})
    if "subjectId" in entry:
        print("  !! LeaderboardEntry carries a subjectId — that defeats the nickname")
        return 1
    print("    parses · %d operations · LeaderboardEntry: %s"
          % (parsed_n, ", ".join(sorted(entry))))

    if not apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(CRM, "w", encoding="utf-8", newline="\n").write(s)
    print("  -> contracts/satellite/marketing-crm.yaml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
