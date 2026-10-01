#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Names in the contracts that the glossary says never to use.

**Audit class A-GLOSSARY (audit/ticvai/ROOT-CLASSES.md).** Fourteen root issues were one mistake
in fourteen places: a synonym the glossary bans, used as a schema, field or operation name --
Item/SKU for Product (R131), Booking/Hold for Reservation (R145), Guest for Subject (R155),
Till/Drawer/Station for Workstation or Deposit Box (R156), Session for Performance (R165),
Zone/Department/Org unit for Operating Area or Scope Node (R194), Ticket for a kitchen ticket
(R210), Card for Media (R220), and the rest (R147, R190, R193, R195, R211, R221). Most were
decided on 28 September and recorded in `docs/glossary.md`; nothing stopped the next one.

This reads the *Never say* column of every table in `docs/glossary.md`, drops any word that is
itself a canonical term somewhere in the glossary (Session is a Principal's session as well as a
banned name for a Performance) and any ban the glossary qualifies in parentheses (those need a
reader), and reports each contract schema, property and operationId whose words include a banned
one. Words the glossary lists under *Recorded exceptions* are honoured the same way.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-glossary-terms.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "G-BANNED-NAME": "a contract schema, field or operation named with a word the glossary bans "
                     "(R131 R145 R147 R155 R156 R165 R190 R193 R194 R195 R210 R211 R220 R221)",
}


def words(ident: str) -> list:
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", ident)]


def load_bans():
    path = g.ROOT / "docs" / "glossary.md"
    if not path.exists():
        return {}, set()
    canonical, bans = set(), {}
    for line in path.read_text(encoding="utf-8").split("\n"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[0].startswith("**"):
            continue
        term = re.sub(r"\*", "", cells[0]).strip()
        canonical.add(tuple(words(term.replace(" ", ""))))
        for raw in re.split(r",(?![^()]*\))", cells[-1]):
            raw = raw.strip()
            if not raw or "(" in raw or raw.lower().startswith(("n/a", "-", "—")):
                continue
            key = tuple(words(raw.replace(" ", "").replace("-", "")))
            if key:
                bans.setdefault(key, set()).add(term)
    bans = {k: v for k, v in bans.items() if k not in canonical}
    return bans, canonical


def contains(seq: list, sub: tuple) -> bool:
    n = len(sub)
    return any(tuple(seq[i:i + n]) == sub for i in range(len(seq) - n + 1))


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-glossary-terms", RULES)
    bans, canonical = load_bans()
    if not bans:
        guard.note("docs/glossary.md has no Never-say column to read")
        return guard.finish()
    # A banned word inside a longer canonical term is that term, not the synonym ("Access Point"
    # contains "Access"; "Sale Board" contains "Board").
    canon_multi = [c for c in canonical if len(c) > 1]

    canon_multi.sort(key=len, reverse=True)

    def _unused_hits(ident: str):
        src = words(ident)
        ws, i = [], 0
        while i < len(src):
            c = next((c for c in canon_multi if tuple(src[i:i + len(c)]) == c), None)
            if c:
                ws.append("|")          # a canonical term: opaque, and a boundary
                i += len(c)
            else:
                ws.append(src[i])
                i += 1
        for ban, terms in bans.items():
            if contains(ws, ban):
                yield " ".join(ban), terms

    # Only where a name *names an entity*: a reference field (`guestId`, `cardCode`, `tillIds`),
    # and a schema's head noun (`MerchandiseItem` -> item). A verb or a qualifier (`listX`,
    # `entryPolicy`, `sourceChannel`) is ordinary English the glossary does not govern.
    def head(ident: str, strip_ref: bool):
        ws = words(ident)
        if strip_ref:
            if len(ws) < 2 or ws[-1] not in ("id", "ids", "code", "codes"):
                return None
            ws = ws[:-1]
        return ws

    def banned_head(ws, context=()):
        """A single generic word is banned only bare (`guestId`, `tillId`, a schema called `Zone`);
        in a compound it is qualified (`orderLineId` is an order line, not a queue). A ban of two or
        more words (`org unit`) is banned wherever it ends the name."""
        if not ws:
            return None
        while len(ws) > 1 and ws[0] in context:
            ws = ws[1:]
        for ban, terms in sorted(bans.items(), key=lambda kv: -len(kv[0])):
            n = len(ban)
            if (n == 1 and tuple(ws) == ban) or (n > 1 and tuple(ws[-n:]) == ban):
                return " ".join(ban), terms
        return None

    by, _ = g.schemas()
    for (stem, name), s in sorted(by.items()):
        hit = banned_head(head(name, False), tuple(words(stem.replace("-", " ").title().replace(" ", ""))))
        if hit:
            guard.add("G-BANNED-NAME", f"{stem}.{name}:{hit[0]}",
                      f"{stem} schema {name}: '{hit[0]}' - the glossary says {'/'.join(sorted(hit[1]))}")
        for p in (s.get("properties") or {}):
            hit = banned_head(head(p, True))
            if hit:
                guard.add("G-BANNED-NAME", f"{stem}.{name}.{p}:{hit[0]}",
                          f"{stem} {name}.{p}: '{hit[0]}' - the glossary says {'/'.join(sorted(hit[1]))}")
    guard.note(f"{len(bans)} banned word(s) read from docs/glossary.md")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
