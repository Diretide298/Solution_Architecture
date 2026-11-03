#!/usr/bin/env python3
"""Which of a screen record's notes and gaps its own record has overtaken (r13 review, 3 November 2026, CHG-R13RVB-004).

The 9 September pack regeneration (tools/generate-screens-from-pack.py) and the 2 October wiring pass (CHG-WIR-*)
wrote gaps from the operations a screen declared that day: "declares no operation that writes anything", "this
screen's operations return no schema with described properties", "the screen declares 0 operations", "No read of
production plans", "(setFacePassEnrollment has no get)". Later lanes added the operations and left the gaps, so the
record told a developer an operation was missing that the same record declares, and a careful agent stopped. The 14
August board import wrote "Components, states and operations still to be written" on 87 screens; 85 of them have
had all three for weeks.

One judgement, two users: check-screen-wiring S-NOTES-STALE fails on what this finds, and
tools/applied/r13-review-stale-screen-text.py removed what it found on 3 November 2026.

    stale_gaps(screen, ops, schemas)   -> [(index into screen['gaps'], kind, fix)]
        kind  gap-no-write | gap-no-schema | gap-op-count | gap-no-read | gap-built
        fix   "drop", or ("count", n) for gap-op-count: the count is corrected, the unserved actions kept
    still_to_be_written(screen)        -> True when the board-import sentence sits on a screen with a layout, states
                                          and operations
"""
from __future__ import annotations

import re

import contract_shapes as cs

WRITES = {"post", "put", "patch", "delete"}
STILL = re.compile(r"Components, states and operations\s+still to be written\.")
NO_WRITE = re.compile(r"declares no operation that writes anything")
NO_SCHEMA = re.compile(r"operations return no schema with described properties")
OP_COUNT = re.compile(r"(and the screen\s+declares\s+)(\d+)(\s+operations?)\b")
NO_READ = re.compile(r"\bNo (?:read of|operation (?:lists|reads|returns))\s+([^.;(]+)|\(`?(\w+)`? has no get\)")
RECORDED = re.compile(r"Contract gap recorded [^(]*\((CHG-WIR-\d+)\)")
_STOP = {"the", "a", "an", "of", "its", "their", "or", "and", "for", "to", "by", "in", "on", "any", "one", "list",
         "get", "read", "configuration"}


def _stem(w: str) -> str:
    w = w.lower().replace("enrolment", "enrollment")
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    for suf in ("es", "s"):
        if w.endswith(suf) and len(w) > 4:
            return w[: -len(suf)]
    return w


def _op_words(op_id: str) -> set:
    return {_stem(x) for x in re.findall(r"[A-Z]?[a-z]+", op_id)}


def _text(gap) -> str:
    return re.sub(r"\s+", " ", str(gap.get("why") if isinstance(gap, dict) else gap))


def _declared(screen: dict, ops: dict) -> list:
    return [a.get("operationId") for a in screen.get("apis") or [] if isinstance(a, dict) and a.get("operationId")]


def _answers_fields(op_id: str, ops: dict, schemas: dict) -> bool:
    op = (ops.get(op_id) or {}).get("op") or {}
    return any(cs.schema_fields(n, schemas) for n in cs.response_schemas(op)[:1])


def twins(screens) -> set:
    """Ids on either side of a `source.sameAs` copy: their generated gaps are the copying tool's, kept identical by
    check-screens, so they are not judged here (the copy's narrower operations make one count right for one only)."""
    out = set()
    for _p, s in screens:
        t = (s.get("source") or {}).get("sameAs") if isinstance(s.get("source"), dict) else None
        if t:
            out |= {s.get("id"), t}
    return out


def stale_gaps(screen: dict, ops: dict, schemas: dict, skip=frozenset()) -> list:
    """The gaps the screen's own declarations now contradict (see the module text). A screen in `skip` (twins()) is
    not judged."""
    if screen.get("id") in skip:
        return []
    apis = _declared(screen, ops)
    known = [o for o in apis if o in ops]
    gets = [o for o in known if ops[o]["method"] == "get"]
    out = []
    for i, gap in enumerate(screen.get("gaps") or []):
        if isinstance(gap, dict) and gap.get("removed"):
            continue
        t = _text(gap)
        if NO_WRITE.search(t) and any(ops[o]["method"] in WRITES for o in known):
            out.append((i, "gap-no-write", "drop"))
            continue
        if NO_SCHEMA.search(t) and any(_answers_fields(o, ops, schemas) for o in known):
            out.append((i, "gap-no-schema", "drop"))
            continue
        m = OP_COUNT.search(t)
        if m and int(m.group(2)) != len(apis):
            out.append((i, "gap-op-count", ("count", len(apis))))
            continue
        if isinstance(gap, dict) and gap.get("operation"):
            continue
        served = False
        for nm in NO_READ.finditer(t):
            if nm.group(1):
                words = {_stem(w) for w in re.findall(r"[A-Za-z]+", nm.group(1).split(" or ")[0])
                         if w.lower() not in _STOP}
            else:
                words = _op_words(nm.group(2)) - {"set", "update", "create"}
            if words and any(words <= _op_words(o) for o in gets):
                served = True
        if served:
            out.append((i, "gap-no-read", "drop"))
            continue
        rec = RECORDED.search(t)
        if rec:
            built = re.compile(r"gap logged in %s for %s\b[^)]*\bbuilt\b" % (re.escape(rec.group(1)),
                                                                           re.escape(str(screen.get("id")))))
            if any(built.search(str(ops[o]["op"].get("description") or "")) for o in known):
                out.append((i, "gap-built", "drop"))
    return out


def still_to_be_written(screen: dict) -> bool:
    return bool(STILL.search(str(screen.get("notes") or ""))) and bool(screen.get("layout")) \
        and bool(screen.get("states")) and bool(screen.get("apis"))
