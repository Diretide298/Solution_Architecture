#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A list's stated order is total: no sort key that can be null without a stated place, and a stated order on every
whole list a screen shows (r10, CHG-R10GEN-004).

**What it found.** `check-contract-shapes` C-PAGED-ORDER makes a cursor-paged list name the field it sorts on
(CHG-GEN-002, ADAM CR-077). Nothing asked whether that field can be null, or whether an unpaged list states an order
at all, and three CRs of 21 to 23 October 2026 were exactly that:

  * listMyWaitingGuests (CR-236, #33057): "Ordered by `estimatedCallAt`, soonest first, then `joinedAt`", and
    WaitingGuest.estimatedCallAt is nullable (queue.entry.estimated_call_at has no NOT NULL), so an entry with no
    estimate had no place in the order or in the keyset cursor;
  * listShifts (CR-206, #32645): "Newest first, by `recordedAt` descending", and recordedAt is optional on
    openShift and nullable on orders.pos_shift; the lead settled it as coalesce(recordedAt, openedAt);
  * listSsoProviders (CR-190, #30730): the SSO buttons of every sign-in door, an unpaged array of
    identity.sso_provider rows with no order at all, so two calls may draw the buttons in different orders.

Rules:

    LO-NULLABLE-KEY   a list (GET, paged or a whole array) whose stated order names a field of its items that can be
                      null: `nullable: true` in the schema, or not required in the schema and its column (handoff/
                      schema-reference.json, by the column's `source`) not NOT NULL; and the text states no place
                      for the rows without it (NULLS FIRST/LAST, "a row with no `x` sorts last", coalesce, "or
                      its `openedAt` where it has none"). `id`, a `...Id` key and `createdAt` (written with the row)
                      are never null keys.
    LO-UNORDERED      a whole list (GET answering an unpaged array) that a screen calls (x-ticvai-consumed-by),
                      whose items are rows of a table (x-ticvai-persistence) with no position field of their own
                      (displayOrder, sortOrder, position, rank, ...), and whose text states no order at all.
                      A paged list is C-PAGED-ORDER's; a computed answer (a report row, a finding) is left out, its
                      order being part of the computation that makes it.

An order is read from the operation's summary, description, x-ticvai-note and its 200's description, with the field
finders of check-contract-shapes (`order_names_field`). Each finding needs a ruling: where the rows without the key
go (NULLS LAST, or a fallback key as CR-206), or which order a whole list takes. No baseline: the class arrived in
r10, and its findings are fixed in r10 (the lead's rule for a new check).

    python tools/check-list-order.py [--all]
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "LO-NULLABLE-KEY": "a list's stated order names a field that can be null and states no place for the rows "
                       "without it (CR-236, CR-206; CHG-R10GEN-004)",
    "LO-UNORDERED": "a whole list of stored rows a screen shows states no order (CR-190; CHG-R10GEN-004)",
}
_spec = importlib.util.spec_from_file_location("contract_shapes", Path(__file__).resolve().parent /
                                               "check-contract-shapes.py")
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)

NEVER_NULL = {"id", "createdAt"}
POSITION = re.compile(r"^(?:displayOrder|sortOrder|position|rank|sequence|ordinal|order|priority|seq|sortIndex|"
                      r"displayIndex|sortKey)$", re.I)
# Any statement of an order, for LO-UNORDERED (looser than C-PAGED-ORDER: an unpaged list that says "critical first,
# then unacknowledged" has an order, even with no field named). "order" alone is the noun (a sales order).
ORDER_STATED = re.compile(r"\b(?:sorted|sorts|keyset|newest|oldest|most recent|latest first|earliest first|soonest|"
                          r"ascending|descending|alphabetical(?:ly)?|ordered\s+(?:by|on|as|from)|order(?:ed)?\s+by|"
                          r"in\s+(?:the\s+)?(?:[\w`-]+\s+){0,3}order\b|\w+\s+first,?\s+then)", re.I)
# A place for the rows without the key: the words, in a sentence that names the key.
NULL_WORD = re.compile(r"\bnulls?\b|\bwith no\b|\bwithout\b|\bno\s+`|\bhas none\b|\bhave none\b|\babsent\b|"
                       r"\bmissing\b|\bunset\b|\bnot set\b|\bwhere it has none\b|\bfalls? back\b|\bfallback\b|"
                       r"\bor (?:its|the|their)\b|\bcoalesce\b|\botherwise\b|\binstead\b", re.I)
PLACE_WORD = re.compile(r"\b(?:first|last|after|before|end|top|bottom|start)\b|\bcoalesce\b|\bfalls? back\b|"
                        r"\bfallback\b|\bor (?:its|the|their) `?\w+`?\b|\btakes?\b|\binstead\b|\bsorts? (?:by|as)\b",
                        re.I)
ANYWHERE = re.compile(r"\bNULLS\s+(?:FIRST|LAST)\b|\bcoalesce\s*\(", re.I)


def _docs() -> dict:
    return {stem: doc for stem, _, doc in g.contracts()}


def resolve(node, doc, docs):
    """(node, the document it lives in): a $ref followed, local or into another contract."""
    seen = 0
    while isinstance(node, dict) and "$ref" in node and seen < 10:
        seen += 1
        fp, _, frag = node["$ref"].partition("#")
        if fp:
            doc = docs.get(fp.rsplit("/", 1)[-1].removesuffix(".yaml")) or {}
        cur = doc
        for p in [p for p in frag.split("/") if p]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        node = cur
    return node, doc


def list_items(op: dict, doc: dict, docs: dict):
    """('array' | 'page', item schema, its document, the item's schema name) for a 200 that answers a list."""
    r, d = resolve(((op.get("responses") or {}).get("200")), doc, docs)
    sch = cs.body_schema(r) if isinstance(r, dict) else None
    ref = (sch or {}).get("$ref", "") if isinstance(sch, dict) else ""
    sch, d = resolve(sch, d, docs)
    if not isinstance(sch, dict):
        return None
    if sch.get("type") == "array" and isinstance(sch.get("items"), dict):
        it, d2 = resolve(sch["items"], d, docs)
        return "array", it, d2, g.ref_name(sch["items"].get("$ref", ""))
    for part in [sch] + list(sch.get("allOf") or []):
        p, dp = resolve(part, d, docs)
        items = ((p or {}).get("properties") or {}).get("items")
        if isinstance(items, dict) and items.get("type") == "array" and items.get("items"):
            it, d2 = resolve(items["items"], dp, docs)
            return "page", it, d2, g.ref_name(items["items"].get("$ref", ""))
    return None


def order_text(op: dict, doc: dict, docs: dict) -> str:
    r, _ = resolve(((op.get("responses") or {}).get("200")), doc, docs)
    return " ".join(str(op.get(k) or "") for k in ("summary", "description", "x-ticvai-note")) + " " + \
        str((r or {}).get("description") or "")


def order_fields(text: str, props) -> list:
    """The item fields an order statement names, in the order they are named."""
    text = text.replace("**", "")
    low = {str(p).lower(): str(p) for p in props}
    out: list = []

    def take(chunk):
        toks = re.findall(r"`?[A-Za-z_][A-Za-z0-9_.']*`?", chunk)
        words = [t.strip("`").split(".")[-1].removesuffix("'s").strip("'") for t in toks]
        i = 0
        while i < len(words):
            w = words[i]
            hit = None
            if w and w.lower() not in cs.NOT_A_FIELD:
                for n in (3, 2, 1):
                    if i + n <= len(words) and "".join(words[i:i + n]).lower() in low:
                        hit = (low["".join(words[i:i + n]).lower()], n)
                        break
            if hit:
                if hit[0] not in out:
                    out.append(hit[0])
                i += hit[1]
            else:
                i += 1

    for rx in (cs.ORDER_BY, cs.FIRST_FIELD, cs.FIELD_DIRECTION):
        for m in rx.finditer(text):
            take(m.group(1))
    if cs.ORDER_WORD.search(text):
        for m in cs.THEN_FIELD.finditer(text):
            take(m.group(1))
    return out


def column_index() -> dict:
    """`<contract>.<Schema>.<field>` -> [(table, column, NOT NULL?)] from the schema reference's `source`."""
    cols = (g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {}
    out: dict = {}
    for t, rows in cols.items():
        for c in rows or []:
            for s in str(c.get("source") or "").split(","):
                if s.strip():
                    out.setdefault(s.strip(), []).append((t, c.get("column"), c.get("required") == "yes"))
    return out


def can_be_null(field: str, item: dict, prop: dict, cols: list) -> str:
    """Why the field can be null ('' when it cannot): the schema says so, or it is optional and its column is not
    NOT NULL."""
    if field in NEVER_NULL or field.endswith("Id"):
        return ""
    if (prop or {}).get("nullable"):
        return "nullable in the schema"
    if field not in set(item.get("required") or []):
        loose = [f"{t}.{c}" for t, c, req in cols if not req]
        if loose and not any(req for _t, _c, req in cols):
            return f"optional, and {', '.join(loose)} is not NOT NULL"
    return ""


def null_place_stated(text: str, field: str, cols: list) -> bool:
    """The text says where the rows without `field` go, in a sentence that names it (or anywhere, by NULLS FIRST /
    LAST or coalesce())."""
    text = text.replace("**", "")
    if ANYWHERE.search(text):
        return True
    names = {field.lower(), re.sub(r"(?<!^)([A-Z])", r" \1", field).lower()} | {str(c).lower() for _t, c, _r in cols}
    for sent in re.split(r"(?<=[.;])\s+|\n\s*\n", text):
        s = sent.lower()
        if any(n in s for n in names) and NULL_WORD.search(sent) and PLACE_WORD.search(sent):
            return True
    return False


def findings() -> list:
    """[(rule, key, message)] over the package."""
    docs = _docs()
    cols = column_index()
    tables = set((g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}).get("cols") or {})
    out = []
    for oid, f in sorted(g.operations().items()):
        if f["method"] != "get":
            continue
        op, doc = f["op"], docs[f["contract"]]
        li = list_items(op, doc, docs)
        if not li or not isinstance(li[1], dict) or not li[1].get("properties"):
            continue
        kind, item, idoc, sname = li
        stem = next((s for s, d in docs.items() if d is idoc), f["contract"])
        props = item.get("properties") or {}
        text = order_text(op, doc, docs)
        for fld in order_fields(text, props):
            prop, _ = resolve(props.get(fld), idoc, docs)
            fc = cols.get(f"{stem}.{sname}.{fld}", []) if sname else []
            why = can_be_null(fld, item, prop or {}, fc)
            if why and not null_place_stated(text, fld, fc):
                out.append(("LO-NULLABLE-KEY", f"{oid}:{fld}",
                            f"{oid}: ordered on `{fld}`, which can be null ({why}), and says nowhere where the rows "
                            f"without it go (NULLS LAST, or a fallback key as listShifts' CR-206)"))
        if kind == "array" and op.get("x-ticvai-consumed-by") and not ORDER_STATED.search(text.replace("**", "")) \
                and not cs.order_names_field(text, set(props)) and not any(POSITION.match(str(p)) for p in props):
            m = re.match(r'\s*"?([a-z][a-z0-9_]*\.[a-z][a-z0-9_]+)', str(item.get("x-ticvai-persistence") or ""))
            if m and m.group(1) in tables:
                n = len(op.get("x-ticvai-consumed-by") or [])
                out.append(("LO-UNORDERED", oid,
                            f"{oid}: answers every {m.group(1)} row it lists as one array, shown on {n} screen(s), "
                            f"and states no order: two calls may list them differently (CR-190)"))
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-list-order", RULES)
    found = findings()
    for rule, key, msg in found:
        guard.add(rule, key, msg)
    guard.note(f"{len(found)} finding(s)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
