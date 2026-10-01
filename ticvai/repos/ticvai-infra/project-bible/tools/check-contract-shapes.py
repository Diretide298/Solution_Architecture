#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract shapes a reviewer misses on the four-hundredth operation.

**Audit classes A-CONTRACT-CONVENTION and A-CONTRACT-VOCAB (audit/ticvai/ROOT-CLASSES.md).**
`check-package.py` rules 46-50 hold the Page envelope, one route per operation, Idempotency-Key,
X-Consistency-Token and path naming (R076 R176 R142 R192 R118). The same audit found more of the
same kind that nothing held:

  C-REQUEST-SERVER-FIELDS  a write body that requires `id`, `status`, `scopePath` or a timestamp
                           the server owns, not marked readOnly (R079)
  C-SUCCESS-PROBLEM        a 2xx typed as Problem (R235)
  C-SCHEMA-PARAMETERS      a `parameters:` key inside a component schema (R212)
  C-ERROR-PROBLEM-TYPE     an inline 4xx/5xx with no `x-ticvai-problem-types` and no Problem
                           schema of its own (R075, R133)
  C-ACTION-409             a POST action on an item (`/{id}/verb`) with no 409 for the wrong state
                           (R078, R095)
  C-ENUM-OTHER             `other` in an enum with no note field beside it (R222: allowed only with
                           a required note, decided 28 September)
  C-ENUM-NON-STRING        an enum value YAML read as a boolean (`false`, `no`) (R238)
  C-EVENT-NAME             an event not named <aggregate>.<pastTenseVerb> (R186, rule changed 1 October)
  C-MONEY-NUMBER           a money-named field typed number/integer instead of Money (R122, R177)
  C-UNTYPED-BODY           a request or 2xx body that is a bare object with no properties (R088)
  C-PAGED-ORDER            a cursor-paged list that says nothing about its order (R154)
  C-PROSE-SPLIT            a word split by line-wrap or find-and-replace (`s ervice`) (R138)

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-contract-shapes.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "C-REQUEST-SERVER-FIELDS": "a write body requires server-owned fields not marked readOnly (R079)",
    "C-SUCCESS-PROBLEM": "a 2xx response typed as Problem (R235)",
    "C-SCHEMA-PARAMETERS": "a parameters key inside a component schema (R212)",
    "C-ERROR-PROBLEM-TYPE": "an inline error response names no problem type (R075 R133)",
    "C-ACTION-409": "a POST action on an item declares no 409 for the wrong state (R078 R095)",
    "C-ENUM-OTHER": "an enum carries 'other' with no note field beside it (R222, decided 28 Sep)",
    "C-ENUM-NON-STRING": "an enum value that YAML reads as a boolean (R238)",
    "C-EVENT-NAME": "an event name breaks <aggregate>.<pastTenseVerb> (R186)",
    "C-MONEY-NUMBER": "a money-named field typed number/integer, not Money (R122 R177)",
    "C-UNTYPED-BODY": "a request or 2xx body that is a bare object (R088)",
    "C-PAGED-ORDER": "a cursor-paged list that states no order (R154)",
    "C-PROSE-SPLIT": "a word split in contract prose (R138)",
    "C-TWO-IDEMPOTENCY": "a body idempotency key beside the Idempotency-Key header (R153)",
    "C-SEARCH-PARAM": "a search/q parameter that says nothing about what it matches (R182)",
    "C-NO-ADDRESS": "a PUT/PATCH/DELETE with no path key and no x-ticvai-singleton (R162 R103)",
    "C-COLOUR-PATTERN": "a colour field typed string with no pattern (R246)",
    "C-FIELD-TYPE-DRIFT": "one field typed two ways across an entity's schemas (R237 R227)",
    "C-ID-FORMAT": "an id field typed other than uuid (ADR-0056) (R074)",
    "C-APPEND-ONLY": "an append-only schema written by PUT/PATCH/DELETE (R185)",
    "C-GUEST-INTERNAL": "a guest-callable read returns principal ids or internal fields (R164)",
}
INTERNAL = re.compile(r"^(createdByPrincipalId|updatedByPrincipalId|principalId|approvedByPrincipalId|"
                      r"internalNote|internalNotes|budgetCap|costPrice|marginPercent)$")

SERVER_OWNED = {"id", "status", "scopePath", "createdAt", "updatedAt", "tenantId", "createdBy",
                "updatedBy", "version", "createdByPrincipalId"}
MONEY = re.compile(r"^(price|amount|total|subtotal|grandTotal|fee|balance|cost|charge|tip|"
                   r"[a-z]+(Price|Amount|Fee))$")
# naming-and-style 6.3 (changed 1 October): `<aggregate>.<pastTenseVerb>`, the version in the payload's `version`.
EVENT = re.compile(r"^[a-z][a-zA-Z0-9]*\.[a-z][a-zA-Z0-9]*$")
NOTE_FIELD = re.compile(r"(note|detail|text|description|comment|other|explanation|freeText)", re.I)
SPLIT = re.compile(r"(?<![\w'’`-])([b-hj-z]) ([a-z]{3,})\b")


def deref(node, doc, depth=0):
    """Resolve a local `#/components/...` $ref; foreign refs come back as (None, name)."""
    while isinstance(node, dict) and "$ref" in node and depth < 10:
        ref = node["$ref"]
        file_part, _, frag = ref.partition("#")
        if file_part:
            return None, g.ref_name(ref)
        cur = doc
        for part in [p for p in frag.split("/") if p]:
            cur = cur.get(part) if isinstance(cur, dict) else None
        node = cur
        depth += 1
    return node, None


def body_schema(container):
    content = (container or {}).get("content") or {}
    for media in content.values():
        if isinstance(media, dict) and media.get("schema") is not None:
            return media["schema"]
    return None


def walk_enums(node, where, out, depth=0):
    if depth > 8 or not isinstance(node, (dict, list)):
        return
    if isinstance(node, list):
        for i, x in enumerate(node):
            walk_enums(x, where, out, depth + 1)
        return
    if isinstance(node.get("enum"), list):
        out.append((where, node["enum"]))
    for k, v in node.items():
        if k in ("enum", "example", "examples", "default"):
            continue
        walk_enums(v, f"{where}.{k}" if k not in ("properties", "items") else where, out, depth + 1)


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-contract-shapes", RULES)
    ops = g.operations()
    docs = {stem: doc for stem, _, doc in g.contracts()}
    vocab = set()
    prose = []

    for oid, f in sorted(ops.items()):
        op, doc, m = f["op"], docs[f["contract"]], f["method"]
        # --- request bodies --------------------------------------------------------------------
        if m in ("post", "put", "patch"):
            rb, _ = deref(op.get("requestBody"), doc)
            sch = body_schema(rb) if isinstance(rb, dict) else None
            node, foreign = deref(sch, doc)
            if isinstance(node, dict):
                req = set(node.get("required") or [])
                props = node.get("properties") or {}
                # R079 is a *resource* schema reused as the write body: the request names a schema
                # that persists to a table, and requires what the server owns.
                persisted = not str(node.get("x-ticvai-persistence") or "none").strip().startswith("none")
                bad = sorted(p for p in req & SERVER_OWNED
                             if not (isinstance(props.get(p), dict) and props[p].get("readOnly")))
                if "id" in bad and op.get("x-ticvai-offline-capable"):
                    bad.remove("id")  # an offline client mints the id it replays under (ADR-0056)
                if "tenantId" in bad and op.get("x-ticvai-scope-level") == "platform":
                    bad.remove("tenantId")  # the platform console names the tenant it acts on
                if bad and persisted:
                    guard.add("C-REQUEST-SERVER-FIELDS", oid,
                              f"{oid}: request body requires server-owned {', '.join(bad)}")
                if node.get("type") == "object" and not props and not node.get("allOf") \
                        and not node.get("oneOf") and not node.get("anyOf") \
                        and not isinstance(node.get("additionalProperties"), dict):
                    guard.add("C-UNTYPED-BODY", f"{oid}:request", f"{oid}: request body is a bare object")
        # --- responses -------------------------------------------------------------------------
        codes = {str(c) for c in (op.get("responses") or {})}
        for code, r in (op.get("responses") or {}).items():
            c = str(code)
            rr, foreign = deref(r, doc)
            if c.startswith("2"):
                sch = body_schema(rr) if isinstance(rr, dict) else None
                if isinstance(sch, dict) and g.ref_name(sch.get("$ref", "")) == "Problem":
                    guard.add("C-SUCCESS-PROBLEM", f"{oid}:{c}", f"{oid}: {c} is typed as Problem")
                node, _ = deref(sch, doc)
                if isinstance(node, dict) and node.get("type") == "object" and not node.get("properties") \
                        and not any(node.get(k) for k in ("allOf", "oneOf", "anyOf")) \
                        and not isinstance(node.get("additionalProperties"), dict):
                    guard.add("C-UNTYPED-BODY", f"{oid}:{c}", f"{oid}: {c} body is a bare object")
            elif c[:1] in "45" and isinstance(r, dict) and "$ref" not in r:
                sch = body_schema(r)
                name = g.ref_name(sch.get("$ref", "")) if isinstance(sch, dict) else ""
                if not r.get("x-ticvai-problem-types") and not (name.endswith("Problem") and name != "Problem"):
                    guard.add("C-ERROR-PROBLEM-TYPE", f"{oid}:{c}",
                              f"{oid}: {c} ({str(r.get('description') or '')[:40]}) names no problem type")
        last = f["path"].rstrip("/").rsplit("/", 1)[-1]
        if m == "post" and re.search(r"/\{[^}]+\}/[a-z][a-z-]*$", f["path"]) and "409" not in codes \
                and not last.endswith("s") \
                and not re.match(r"^(get|list|search|evaluate|preview|calculate|quote|check|validate|"
                                 r"estimate|resolve|decide|run|export|simulate|render|test)", oid):
            guard.add("C-ACTION-409", oid, f"{oid}: POST {f['path']} acts on an item and declares no 409")
        # --- paging order ----------------------------------------------------------------------
        params = [deref(p, doc)[0] or {} for p in (op.get("parameters") or [])]
        pnames = {str(p.get("name")) for p in params if isinstance(p, dict)}
        refs = {g.ref_name(p.get("$ref", "")) for p in (op.get("parameters") or []) if isinstance(p, dict)}
        if m == "get" and ("PageCursor" in refs or "cursor" in pnames):
            text = " ".join(str(op.get(k) or "") for k in ("description", "summary", "x-ticvai-note"))
            if not ({"sort", "orderBy", "order", "sortBy"} & pnames) and \
                    not re.search(r"\b(sorted|ordered|order(ed)? by|newest|oldest|most recent|"
                                  r"ascending|descending|keyset|in the order)\b", text, re.I):
                guard.add("C-PAGED-ORDER", oid, f"{oid}: paged by cursor and states no order")
        prose.append((f"{oid}", " ".join(str(op.get(k) or "") for k in ("description", "summary"))))

    for (stem, name), s in sorted(g.schemas()[0].items()):
        if "parameters" in s:
            guard.add("C-SCHEMA-PARAMETERS", f"{stem}.{name}", f"{stem}.{name}: carries a parameters key")
        enums = []
        walk_enums(s, f"{stem}.{name}", enums)
        siblings = set((s.get("properties") or {}).keys())
        for where, values in enums:
            # Decided 28 September (audit R222): 'other' is allowed only beside a required note.
            if any(isinstance(v, str) and v.lower() == "other" for v in values):
                field = where.rsplit(".", 1)[-1]
                if not [x for x in siblings if x != field and NOTE_FIELD.search(x)]:
                    guard.add("C-ENUM-OTHER", where,
                              f"{where}: enum carries 'other' and the schema has no note field for it")
            odd = [v for v in values if isinstance(v, bool)]
            if odd:
                guard.add("C-ENUM-NON-STRING", where, f"{where}: enum value(s) {odd} are not strings")
        for p, ps in (s.get("properties") or {}).items():
            vocab.add(p.lower())
            if isinstance(ps, dict) and MONEY.match(p) and ps.get("type") in ("number", "integer") \
                    and not ps.get("x-ticvai-column") and not re.search(r"minor|percent|rate|points|count",
                                                                        str(ps.get("description") or ""), re.I):
                guard.add("C-MONEY-NUMBER", f"{stem}.{name}.{p}",
                          f"{stem}.{name}.{p}: money-named and typed {ps.get('type')}, not Money")
            if isinstance(ps, dict) and ps.get("description"):
                prose.append((f"{stem}.{name}.{p}", str(ps["description"])))
        if s.get("description"):
            prose.append((f"{stem}.{name}", str(s["description"])))

    for ev in sorted((g.ROOT / "events").glob("*.yaml")):
        if ev.name.startswith("_"):
            continue
        doc = g.load_yaml(ev) or {}
        name = doc.get("name") or doc.get("event") or doc.get("type")
        if not isinstance(doc.get("version"), int):
            guard.add("C-EVENT-NAME", ev.stem, f"events/{ev.name}: no integer `version` field (the version lives in the payload)")
        if isinstance(name, str) and not EVENT.match(name):
            guard.add("C-EVENT-NAME", ev.stem, f"events/{ev.name}: name {name!r} is not <aggregate>.<pastTenseVerb>")

    # A split word: a lone consonant then a fragment, where the joined word is used elsewhere in the
    # contracts and the fragment is not a word on its own.
    for text in [t for _, t in prose]:
        for w in re.findall(r"[A-Za-z]{3,}", text):
            vocab.add(w.lower())
    for where, text in prose:
        for a, b in SPLIT.findall(text):
            if (a + b) in vocab and b not in vocab:
                guard.add("C-PROSE-SPLIT", f"{where}:{a} {b}", f"{where}: '{a} {b}' reads as a split '{a + b}'")
    extra_rules(guard, ops, docs)
    return guard.finish()


def family(name: str) -> str:
    return re.sub(r"^(Create|Update|Patch|Replace|Set)|(Request|Summary|Detail|Input|View|Result|Response)$",
                  "", name)


def extra_rules(guard, ops, docs):
    """R153 R103/R162 R182 R246 R237 R074 R185 R164."""
    by, _ = g.schemas()
    append_only = {(st, n) for (st, n), s in by.items() if s.get("x-ticvai-append-only")}
    for oid, f in sorted(ops.items()):
        op, doc, m, path = f["op"], docs[f["contract"]], f["method"], f["path"]
        params = []
        for p in list((f["item"] or {}).get("parameters") or []) + list(op.get("parameters") or []):
            node, foreign = deref(p, doc)
            params.append((node or {}, foreign or g.ref_name((p or {}).get("$ref", "")) if isinstance(p, dict) else ""))
        refs = {r for _, r in params if r}
        path_params = re.findall(r"\{([^}]+)\}", path)
        body_node = None
        body_name = None
        if m in ("post", "put", "patch"):
            rb, _ = deref(op.get("requestBody"), doc)
            sch = body_schema(rb) if isinstance(rb, dict) else None
            if isinstance(sch, dict) and "$ref" in sch:
                body_name = g.ref_name(sch["$ref"])
            body_node, _ = deref(sch, doc)
        if "IdempotencyKey" in refs and isinstance(body_node, dict):
            keys = [k for k in (body_node.get("properties") or {})
                    if re.fullmatch(r"(idempotencyKey|clientRequestId|requestId|clientMutationId)", k)]
            if keys:
                guard.add("C-TWO-IDEMPOTENCY", oid, f"{oid}: body {keys[0]} beside the Idempotency-Key header")
        for node, r in params:
            if node.get("in") == "query" and node.get("name") in ("q", "search", "query", "searchTerm")                     and len(str(node.get("description") or "")) < 12:
                guard.add("C-SEARCH-PARAM", f"{oid}:{node.get('name')}",
                          f"{oid}: ?{node.get('name')} does not say what it matches")
        if m in ("put", "patch", "delete") and not path_params and not op.get("x-ticvai-singleton")                 and not (f["item"] or {}).get("x-ticvai-singleton"):
            guard.add("C-NO-ADDRESS", oid, f"{oid}: {m.upper()} {path} has no path key and is not a singleton")
        if m in ("put", "patch", "delete") and body_name and (f["contract"], body_name) in append_only:
            guard.add("C-APPEND-ONLY", oid, f"{oid}: {m.upper()} writes {body_name}, declared append-only")
        aud = op.get("x-ticvai-audience") or []
        if m == "get" and ("guest" in aud or op.get("x-ticvai-guest-callable")):
            for code, r in (op.get("responses") or {}).items():
                if not str(code).startswith("2"):
                    continue
                rr, _ = deref(r, doc)
                node, _ = deref(body_schema(rr) if isinstance(rr, dict) else None, doc)
                if isinstance(node, dict) and isinstance(node.get("items"), dict):
                    node, _ = deref(node["items"], doc)
                if isinstance(node, dict):
                    leak = sorted(k for k in (node.get("properties") or {}) if INTERNAL.match(k))
                    if leak:
                        guard.add("C-GUEST-INTERNAL", oid, f"{oid}: a guest read returns {', '.join(leak)}")
    fam = {}
    for (stem, name), s in sorted(by.items()):
        for p, ps in (s.get("properties") or {}).items():
            if not isinstance(ps, dict):
                continue
            if re.search(r"colou?r$", p, re.I) and ps.get("type") == "string" and not ps.get("pattern")                     and not ps.get("enum") and not ps.get("format"):
                guard.add("C-COLOUR-PATTERN", f"{stem}.{name}.{p}", f"{stem}.{name}.{p}: a colour with no pattern")
            if re.search(r"Id$", p) and ps.get("type") == "string" and ps.get("format") not in (None, "uuid")                     and not re.search(r"(external|provider|vendor|stripe|device|serial|code|slug|key)", p, re.I):
                guard.add("C-ID-FORMAT", f"{stem}.{name}.{p}", f"{stem}.{name}.{p}: format {ps.get('format')}, not uuid")
            t = ps.get("type")
            t = "|".join(sorted(str(x) for x in t if x != "null")) if isinstance(t, list) else (t or "?")
            items = ps.get("items") if isinstance(ps.get("items"), dict) else {}
            it = items.get("type")
            it = "|".join(sorted(str(x) for x in it if x != "null")) if isinstance(it, list) else it
            shape = g.ref_name(ps["$ref"]) if "$ref" in ps else (
                t + ("[" + str(it or g.ref_name(items.get("$ref", "")) or "?") + "]" if t == "array" else ""))
            fam.setdefault((stem, family(name), p), {}).setdefault(shape, []).append(name)
    for (stem, fname, p), shapes in sorted(fam.items()):
        real = {k: v for k, v in shapes.items() if k not in ("?",)}
        prim = {k for k in real if re.fullmatch(r"(string|integer|number|boolean)(\[(string|integer|number|boolean)\])?|array\[(string|integer|number|boolean)\]", k)}
        if len(real) > 1 and fname and prim and not ({"object", "?"} & set(real)):
            desc = "; ".join(f"{k} in {', '.join(v[:2])}" for k, v in sorted(real.items()))
            guard.add("C-FIELD-TYPE-DRIFT", f"{stem}.{fname}.{p}", f"{stem} {fname}.{p}: {desc}")


if __name__ == "__main__":
    sys.exit(main())
