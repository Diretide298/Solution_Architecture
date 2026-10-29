#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract shapes a reviewer misses on the four-hundredth operation.

**Audit classes A-CONTRACT-CONVENTION and A-CONTRACT-VOCAB (docs/active/root-classes.md).**
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
                           (R078, R095); an operation marked `x-ticvai-no-wrong-state: <why>` is exempt and printed
                           (CHG-R8RES-007)
  C-ENUM-OTHER             `other` in an enum with no note field beside it (R222: allowed only with
                           a required note, decided 28 September)
  C-ENUM-NON-STRING        an enum value YAML read as a boolean (`false`, `no`) (R238)
  C-EVENT-NAME             an event not named <aggregate>.<pastTenseVerb> (R186, rule changed 1 October)
  C-MONEY-NUMBER           a money-named field typed number/integer instead of Money (R122, R177)
  C-UNTYPED-BODY           a request or 2xx body that is a bare object with no properties (R088)
  C-PAGED-ORDER            a cursor-paged list that says nothing about its order, or an order that names
                           no field ("most recent first" alone) (R154, CHG-GEN-002, CR-077)
  C-PROSE-SPLIT            a word split by line-wrap or find-and-replace (`s ervice`) (R138)
  C-SEGREGATION-409        a write whose description cites `SegregationRule` declares no 409 carrying the
                           `segregation-breach` problem type, or a response carries that type with a status
                           other than 409 (ADAM CR-079, CHG-IDR-003: one rule, one type, one status)
  C-PATCH-FULL-BODY        a PATCH whose body is a persisted resource schema with a `required` list naming a
                           field the caller may send, so a partial update has to resend the whole resource
                           (ADAM CR-089, CHG-CNS-001). The package's partial update is an `Update<X>Request`:
                           `minProperties: 1`, no `required`, no defaults, `x-ticvai-persistence: none — request
                           only` (UpdateProductRequest, UpdateParkingEntitlementRequest). C-REQUEST-SERVER-FIELDS
                           saw `updateConsentQuestion` only for `status` and it was baselined; the client-owned
                           required fields (`kind`, `text`, ...) are what a PATCH must not require.
  C-PAGED-STATUS           a cursor-paged list whose items' status can end (revoked, cancelled, expired ...) that
                           says neither which statuses it returns nor takes a status filter (ADAM CR-088, CHG-MKT-003)
  C-PUT-KEY                a PUT whose path id carries the stock "Addresses the item this write creates or
                           replaces" text while its description keys the write on something else (`code`, `kind`
                           and the scope, a selector set); a path parameter promising `409 <noun>-id-mismatch` on an
                           operation whose 409 does not list it; or a PUT with a path id whose description still says
                           "there is no id in the path" (ADAM CR-245, CHG-R10CRF-005). The rule CR-245 decided: the
                           path id is the record's id, a create takes it, and a mismatch with the record the natural
                           key finds is 409 and changes nothing.
  C-REFUSAL-UNDECLARED     an operation's own text promises a refusal by status, "(409 when the batch has fewer
                           left)", "is refused (422)", "refused with 404", and its responses declare no such status,
                           so the refusal has no problem type and QA cannot test it (ADAM CR-316, CHG-CR316-001:
                           setCodeDistributionManager's 409 was described and not declared)
  C-FINDING-RULE           a validation's finding-kind enum (a schema named `*FindingKind`) whose description tables
                           its kinds (`| kind | ... |`) without a `reported when` column, or a kind with no row or an
                           empty `reported when` cell: a publish gate that blocks on a kind no rule defines
                           (ADAM CR-320, CHG-CR320-001: 7 of ConfigFindingKind's 11 kinds had no rule)

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-contract-shapes.py [--all] [--update-baseline]
"""
import json
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
    "C-PAGED-ORDER": "a cursor-paged list that states no order naming the field it sorts on (R154, CHG-GEN-002)",
    "C-PROSE-SPLIT": "a word split in contract prose (R138)",
    "C-TWO-IDEMPOTENCY": "a body idempotency key beside the Idempotency-Key header (R153)",
    "C-SEARCH-PARAM": "a search/q parameter that says nothing about what it matches (R182)",
    "C-NO-ADDRESS": "a PUT/PATCH/DELETE with no path key and no x-ticvai-singleton or x-ticvai-body-key (R162 R103)",
    "C-SINGLETON-KEYED": "a write flagged x-ticvai-singleton whose body picks the record (its note names the body's key, "
                         "or the body requires a record id other than venueId or tenantId): it is x-ticvai-body-key "
                         "(r8 walk, CHG-R8WFC-001)",
    "C-BODY-KEY": "x-ticvai-body-key names a field the write's body does not have (r8 walk, CHG-R8WFC-001)",
    "C-COLOUR-PATTERN": "a colour field typed string with no pattern (R246)",
    "C-FIELD-TYPE-DRIFT": "one field typed two ways across an entity's schemas (R237 R227)",
    "C-ID-FORMAT": "an id field typed other than uuid (ADR-0056) (R074)",
    "C-APPEND-ONLY": "an append-only schema written by PUT/PATCH/DELETE (R185)",
    "C-GUEST-INTERNAL": "a guest-callable read returns principal ids or internal fields not marked "
                        "x-ticvai-staff-only (R164, CHG-SHP-010)",
    "C-CODE-409": "a create that takes a business code declares no 409 for a duplicate (R108, CHG-R4-015)",
    "C-CLONE-CODE": "a clone of an entity with a unique code takes no new code (R108, CHG-R4-016)",
    "C-NAME-LOCALISED": "an entity localises other text but not its name (CHG-R4-011)",
    "C-SERIES-WINDOW": "a series repeating every N minutes has no last start time of the day (DI-995, CHG-R4-014)",
    "C-SEGREGATION-409": "a segregation check answered other than 409 segregation-breach (ADAM CR-079, CHG-IDR-003)",
    "C-PATCH-FULL-BODY": "a PATCH body is the full resource schema with its required list (ADAM CR-089, CHG-CNS-001)",
    "C-PAGED-STATUS": "a paged list of items whose status can end (revoked, cancelled ...) that says neither which "
                      "statuses it returns nor takes a status filter (ADAM CR-088, CHG-MKT-003)",
    "C-PUT-KEY": "a PUT keyed on a natural key whose path id carries the stock 'creates or replaces' text, a promised "
                 "409 <noun>-id-mismatch its 409 does not list, or 'no id in the path' beside a path id (ADAM CR-245, "
                 "CHG-R10CRF-005)",
    "C-REFUSAL-UNDECLARED": "an operation's own text promises a refusal by status ('(409 when ...)', 'refused (422)') "
                            "that its responses do not declare (ADAM CR-316, CHG-CR316-001)",
    "C-FINDING-RULE": "a finding-kind enum whose kind table gives a kind no 'reported when' rule (ADAM CR-320, "
                      "CHG-CR320-001)",
}
# ADAM CR-316 (CHG-CR316-001): a refusal the operation's own text promises by status. Only the forms that say
# this operation refuses: "(409 when|if|once|while ...)", "refused (409)", "refused with 409", "refused `409 ...`".
# Statuses the shared responses carry for every operation (400 validation, 401, 403, 429) are not read.
PROMISED_STATUS = re.compile(r"\(\s*`?(404|409|410|412|422)\b[^)]{0,40}?\b(?:when|if|once|while)\b"
                             r"|\brefused\s*(?:with\s*)?\(?`?(404|409|410|412|422)\b", re.I)


def finding_rule_gaps(schema: dict) -> list:
    """The kinds of a finding-kind enum that its description's kind table gives no rule (C-FINDING-RULE; ADAM CR-320,
    CHG-CR320-001). The table is markdown, `| kind | severity | reported when |`, one row per kind. A description with
    no `| kind |` table is not judged; a table without a `reported when` column leaves every kind without a rule."""
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")]
            for ln in str(schema.get("description") or "").splitlines() if ln.strip().startswith("|")]
    head = next((r for r in rows if r and r[0].lower() == "kind"), None)
    if head is None:
        return []
    col = next((i for i, c in enumerate(head) if c.lower() == "reported when"), None)
    rule = {r[0].strip("`"): (r[col] if col is not None and col < len(r) else "") for r in rows
            if r and r is not head and not set(r[0]) <= set("-: ")}
    return [v for v in schema.get("enum") or [] if not str(rule.get(str(v), "")).strip()]


def promised_statuses(text: str) -> set:
    """The refusal statuses an operation's own description or body-key note promises (C-REFUSAL-UNDECLARED)."""
    return {a or b for a, b in PROMISED_STATUS.findall(text or "")}
# ADAM CR-245 (CHG-R10CRF-005): the text the 14 October shapes pass stamped on every PUT path id it added
# (tools/applied/shp-contract-shapes-14-october/apply_noaddr.py), right only for a PUT keyed on that id.
STOCK_ADDRESS = "Addresses the item this write creates or replaces"
PUT_KEYED = re.compile(r"(?:\bkeyed (?:on|by)|\bmatched on)\s*(.{0,160})", re.I | re.S)
ID_MISMATCH = re.compile(r"`409 ([a-z0-9-]+-id-mismatch)`")


def put_natural_keys(text: str, path_names: set) -> list:
    """The phrases of a PUT's description that key the write on something other than its path id: `keyed on|by X`
    or `matched on X`, where X is not the record's `id` (the body's or the path's) and is not led by a path parameter
    (a path that names the key itself, `/{formId}/{key}`, is keyed on it). "never on an id" always counts."""
    out = []
    for mm in PUT_KEYED.finditer(text):
        ph = re.split(r"[.:;(]\s|\*\*|\.$", " ".join(mm.group(1).split()))[0].strip()
        lead = re.match(r"^(?:the (?:body's|path's) )?`?([A-Za-z][A-Za-z0-9]*)`?", ph)
        tok = lead.group(1) if lead else ""
        if tok == "id" or tok in path_names:
            continue
        out.append(ph)
    if re.search(r"never on an id", text, re.I):
        out.append("never on an id")
    return out
# CHG-IDR-003: a write that says it runs the segregation check names the rule schema in its description.
SEGREGATION = re.compile(r"\bSegregationRule\b")
CREATES = re.compile(r"^(create|add|register|import)[A-Z]")
LOCALISED = re.compile(r"schemas/(LocalisedText|LocalisedRichText)['\"]")
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


SCOPE_IDS = ("venueId", "tenantId")


def _body_fields(node, doc, depth=0):
    """(properties, required) of a request body schema, through local refs and allOf."""
    node, _ = deref(node, doc)
    if not isinstance(node, dict) or depth > 8:
        return {}, []
    props, req = dict(node.get("properties") or {}), list(node.get("required") or [])
    for part in node.get("allOf") or []:
        p, r = _body_fields(part, doc, depth + 1)
        props.update(p)
        req += r
    return props, req


def body_schema(container):
    content = (container or {}).get("content") or {}
    for media in content.values():
        if isinstance(media, dict) and media.get("schema") is not None:
            return media["schema"]
    return None


def response_props(op, doc) -> set:
    """Every property name reachable from an operation's 200 body (local refs, allOf, array items): the fields a
    list can be ordered on."""
    out, seen = set(), set()

    def walk(node, depth=0):
        if depth > 8 or not isinstance(node, dict):
            return
        if "$ref" in node:
            if node["$ref"] in seen:
                return
            seen.add(node["$ref"])
            node, _ = deref(node, doc)
            if not isinstance(node, dict):
                return
        for k in ("allOf", "oneOf", "anyOf"):
            for part in node.get(k) or []:
                walk(part, depth + 1)
        if isinstance(node.get("items"), dict):
            walk(node["items"], depth + 1)
        for p, v in (node.get("properties") or {}).items():
            out.add(str(p))
            walk(v, depth + 1)

    walk(body_schema(((op.get("responses") or {}).get("200")) or {}) or {})
    return out


# CHG-MKT-003 (ADAM CR-088): a status value that ends an item's life, and the parameters that choose among them.
ENDED_STATUSES = {"revoked", "cancelled", "canceled", "deleted", "archived", "expired", "failed", "closed",
                  "withdrawn", "voided", "retired", "inactive", "rejected", "lapsed", "superseded", "removed"}
STATUS_PARAMS = {"status", "statuses", "state", "states", "includeinactive", "includerevoked", "includearchived",
                 "includeexpired", "includeclosed", "isactive", "active"}


def item_status_values(op, doc) -> set:
    """The `status` enum of the items a paged 200 body lists (`items[]`, through local refs and allOf)."""
    vals, seen = set(), set()

    def resolve(node):
        while isinstance(node, dict) and "$ref" in node and node["$ref"] not in seen:
            seen.add(node["$ref"])
            node, _ = deref(node, doc)
        return node if isinstance(node, dict) else {}

    def item_schema(node, depth=0):
        node = resolve(node)
        if depth > 6:
            return []
        out = []
        for part in node.get("allOf") or []:
            out += item_schema(part, depth + 1)
        items = (node.get("properties") or {}).get("items")
        if isinstance(items, dict):
            out.append(resolve(items.get("items") or {}))
        return out

    def status_of(node, depth=0):
        node = resolve(node)
        if depth > 6:
            return
        for part in node.get("allOf") or []:
            status_of(part, depth + 1)
        st = resolve((node.get("properties") or {}).get("status") or {})
        for v in st.get("enum") or []:
            vals.add(str(v).lower())

    for it in item_schema(body_schema(((op.get("responses") or {}).get("200")) or {}) or {}):
        status_of(it)
    return vals


# An order statement and the field it names: "sorted by `openedAt` descending", "ordered by name", "openedAt
# descending", "most recent first, by `startedAt`", "newest `resolvedAt` first", "ordered by creation (`id`, a
# UUIDv7)", "keyset on (startsAt, id)", "... then `name`".
_TOK = r"[`(]*[A-Za-z_][A-Za-z0-9_.']*[`),]*"
ORDER_WORD = re.compile(r"\b(?:sorted|ordered|order|sort|sorts|keyset|newest|oldest|most recent|latest|earliest|"
                        r"soonest|ascending|descending|in the order)\b", re.I)
ORDER_BY = re.compile(r"\b(?:sorted|ordered|order|sort|sorts|keyset|newest|oldest|most recent|latest|earliest|"
                      r"soonest|first|last|in the order)\b(?:[\s,]+\w+){0,3}?[\s,]+(?:by|on|of)\s+"
                      r"(?:the\s+|its\s+|their\s+)?((?:" + _TOK + r"\s*){1,3})", re.I)
FIRST_FIELD = re.compile(r"\b(?:newest|oldest|most recent|latest|earliest|soonest|highest|lowest)\s+`?"
                         r"([A-Za-z_][A-Za-z0-9_]*)`?\s+first\b", re.I)
FIELD_DIRECTION = re.compile(r"(" + _TOK + r")\s*,?\s*\(?(?:ascending|descending|asc|desc|alphabetical(?:ly)?)\b",
                             re.I)
THEN_FIELD = re.compile(r"\bthen\s+(?:by\s+)?((?:" + _TOK + r"\s*){1,3})", re.I)
NOT_A_FIELD = {"the", "a", "an", "its", "their", "which", "what", "when", "default", "order", "them", "it",
               "this", "that", "date", "time", "most", "recent", "first", "last", "and", "or", "then", "by",
               "creation", "age", "value", "uuidv7", "row", "rows"}


def order_names_field(text: str, props: set) -> bool:
    """True when an order statement in `text` names a field: a property of the listed items (one word, or two or
    three run together: "visit date" is `visitDate`), a backticked name, or a camelCase / snake_case identifier."""
    text = text.replace("**", "")
    lowered = {p.lower() for p in props}

    def names_field(chunk: str, backtick_ok: bool = True) -> bool:
        toks = re.findall(r"`?[A-Za-z_][A-Za-z0-9_.']*`?", chunk)
        words = [t.strip("`").split(".")[-1].removesuffix("'s").strip("'") for t in toks]
        for i, (raw, w) in enumerate(zip(toks, words)):
            if not w or w.lower() in NOT_A_FIELD:
                continue
            if w.lower() in lowered or re.search(r"[a-z][A-Z]|_", w) or (backtick_ok and raw.startswith("`")):
                return True
            for n in (2, 3):
                if "".join(words[i:i + n]).lower() in lowered and len(words[i:i + n]) == n:
                    return True
        return False

    for m in ORDER_BY.finditer(text):
        if names_field(m.group(1)):
            return True
    for m in FIRST_FIELD.finditer(text):
        if names_field(m.group(1), backtick_ok=False):
            return True
    for m in FIELD_DIRECTION.finditer(text):
        if names_field(m.group(1)):
            return True
    if ORDER_WORD.search(text):
        for m in THEN_FIELD.finditer(text):
            if names_field(m.group(1)):
                return True
    return False


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
                # A member of the schema's natural key (x-ticvai-unique-together, x-ticvai-unique) is the caller's to
                # name, whatever its name: a firmware release's `version` is its vendor's and the 409 refuses a second
                # one (ADAM CR-285 (3), 28 October 2026, CHG-R11TEN-006), not a row version the server moves.
                natural = {k for grp in node.get("x-ticvai-unique-together") or [] for k in (grp or [])}
                natural |= {k for k, v in props.items() if isinstance(v, dict) and v.get("x-ticvai-unique")}
                bad = [p for p in bad if p not in natural]
                if bad and persisted:
                    guard.add("C-REQUEST-SERVER-FIELDS", oid,
                              f"{oid}: request body requires server-owned {', '.join(bad)}")
                # CR-089: a partial update names only what changes; the resource's required list is the response's.
                sent = sorted(p for p in req if not (isinstance(props.get(p), dict) and props[p].get("readOnly")))
                if m == "patch" and persisted and sent:
                    guard.add("C-PATCH-FULL-BODY", oid,
                              f"{oid}: PATCH body is the persisted schema "
                              f"{g.ref_name(str((sch or {}).get('$ref') or '')) or '(inline)'} and requires "
                              f"{', '.join(sent)}; use an Update<X>Request with minProperties: 1 and no required")
                if node.get("type") == "object" and not props and not node.get("allOf") \
                        and not node.get("oneOf") and not node.get("anyOf") \
                        and not isinstance(node.get("additionalProperties"), dict):
                    guard.add("C-UNTYPED-BODY", f"{oid}:request", f"{oid}: request body is a bare object")
                # R108, CHG-R4-015: a create that takes a business code must say what a duplicate gets.
                codes_ = {str(c) for c in (op.get("responses") or {})}
                if m == "post" and CREATES.match(oid) and "code" in props and "409" not in codes_:
                    guard.add("C-CODE-409", oid, f"{oid}: creates with a `code` and declares no 409 for a duplicate")
                # R108, CHG-R4-016: a copy of an entity whose code is unique must be given a code of its own.
                cm = re.match(r"^clone([A-Z]\w*)$", oid)
                if m == "post" and cm:
                    create, _ = deref({"$ref": f"#/components/schemas/Create{cm.group(1)}Request"}, doc)
                    ccode = ((create or {}).get("properties") or {}).get("code") if isinstance(create, dict) else None
                    if isinstance(ccode, dict) and ccode.get("x-ticvai-unique") \
                            and not [p for p in props if p == "code" or p.endswith("Code")]:
                        guard.add("C-CLONE-CODE", oid, f"{oid}: copies a {cm.group(1)} whose code is unique "
                                                       f"({ccode.get('x-ticvai-unique')}) and takes no new code")
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
        # C-REFUSAL-UNDECLARED (ADAM CR-316, CHG-CR316-001): a refusal promised in the text is a declared response.
        promised = promised_statuses(" ".join(str(op.get(k) or "") for k in
                                              ("description", "x-ticvai-body-key-note", "x-ticvai-singleton-note")))
        for st in sorted(promised - codes):
            guard.add("C-REFUSAL-UNDECLARED", f"{oid}:{st}",
                      f"{oid}: its text promises a {st} refusal and its responses declare no {st}: declare it with "
                      f"its problem type")
        last = f["path"].rstrip("/").rsplit("/", 1)[-1]
        if m == "post" and re.search(r"/\{[^}]+\}/[a-z][a-z-]*$", f["path"]) and "409" not in codes \
                and not last.endswith("s") \
                and not re.match(r"^(get|list|search|evaluate|preview|calculate|quote|check|validate|"
                                 r"estimate|resolve|decide|run|export|simulate|render|test)", oid):
            # **An action with no wrong state says so, with its reason** (r8 gate residue, 20 October 2026,
            # CHG-R8RES-007): `x-ticvai-no-wrong-state: <why>` on the operation. eraseSubject acts on a subject the
            # AI side keeps no state for: a subject with nothing indexed answers zeros, so there is no state to be
            # wrong in. Printed every run, so the reason stays in view; a baseline entry would hide it.
            if str(op.get("x-ticvai-no-wrong-state") or "").strip():
                guard.note(f"C-ACTION-409 exempt {oid}: {str(op['x-ticvai-no-wrong-state']).strip()[:140]}")
            else:
                guard.add("C-ACTION-409", oid, f"{oid}: POST {f['path']} acts on an item and declares no 409")
        # --- paging order ----------------------------------------------------------------------
        params = [deref(p, doc)[0] or {} for p in (op.get("parameters") or [])]
        pnames = {str(p.get("name")) for p in params if isinstance(p, dict)}
        refs = {g.ref_name(p.get("$ref", "")) for p in (op.get("parameters") or []) if isinstance(p, dict)}
        if m == "get" and ("PageCursor" in refs or "cursor" in pnames):
            text = " ".join(str(op.get(k) or "") for k in ("description", "summary", "x-ticvai-note"))
            # **The order names the field it sorts on** (CHG-GEN-002, ADAM CR-077, 14 October 2026). "Most recent
            # first" passed this rule while naming no column, so listOwnPlatformStaffGrants and
            # listPlatformStaffGrants could be built in any order a developer guessed (identity.yaml:4273,4641).
            if not ({"sort", "orderBy", "order", "sortBy"} & pnames) and \
                    not order_names_field(text, response_props(op, doc)):
                guard.add("C-PAGED-ORDER", oid, f"{oid}: paged by cursor and states no order that names a field")
            # **Which rows are in the list** (CHG-MKT-003, ADAM CR-088, 14 October 2026). listGuestDevices pages
            # devices whose status may be revoked or failed and said neither whether they are listed nor how to ask
            # for them, so the guest's device screen could show a revoked phone as live or drop it silently. A list
            # whose items carry a status with an ended value, and that takes no status filter, says in words which
            # statuses it returns.
            ended = sorted(item_status_values(op, doc) & ENDED_STATUSES)
            if ended and not (STATUS_PARAMS & {p.lower() for p in pnames}) \
                    and not re.search(r"\bstatus(es)?\b|`status`", text, re.I):
                guard.add("C-PAGED-STATUS", oid, f"{oid}: lists items whose status can be {', '.join(ended)} and "
                          "says neither which statuses it returns nor takes a status filter")
        prose.append((f"{oid}", " ".join(str(op.get(k) or "") for k in ("description", "summary"))))

    for (stem, name), s in sorted(g.schemas()[0].items()):
        if "parameters" in s:
            guard.add("C-SCHEMA-PARAMETERS", f"{stem}.{name}", f"{stem}.{name}: carries a parameters key")
        # CHG-R4-014 (DI-995): a series repeating every N minutes needs the day's last start, or it runs all night.
        sp = s.get("properties") or {}
        for p, ps in sp.items():
            rp = (ps.get("properties") or {}) if isinstance(ps, dict) else {}
            if "intervalMinutes" in rp and not ({"lastStartTime", "dailyEndTime", "lastStart"} & set(rp)):
                guard.add("C-SERIES-WINDOW", f"{stem}.{name}.{p}",
                          f"{stem}.{name}.{p}: repeats every intervalMinutes with no last start time of the day")
        # CHG-R4-011: an entity that localises some of what a guest reads localises its name too.
        persisted_ = not str(s.get("x-ticvai-persistence") or "none").strip().startswith("none")
        if persisted_ and isinstance(sp.get("name"), dict) and sp["name"].get("type") == "string" \
                and not ({"nameLocalised", "nameTranslations", "localisedName"} & set(sp)) \
                and [p for p, v in sp.items() if p != "name" and LOCALISED.search(json.dumps(v, default=str))]:
            guard.add("C-NAME-LOCALISED", f"{stem}.{name}",
                      f"{stem}.{name}: localises other text (LocalisedText) but its name is one plain string")
        # C-FINDING-RULE (ADAM CR-320, CHG-CR320-001): every kind a validation reports has its rule beside it.
        if name.endswith("FindingKind") and s.get("enum"):
            gaps = finding_rule_gaps(s)
            if gaps:
                guard.add("C-FINDING-RULE", f"{stem}.{name}",
                          f"{stem}.{name}: its kind table gives no 'reported when' rule for {', '.join(map(str, gaps))}")
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
    segregation_rules(guard, ops, docs)
    return guard.finish()


def segregation_rules(guard, ops, docs):
    """**One segregation rule, one answer** (14 October 2026, ADAM CR-079; CHG-IDR-003). The same check was `422
    segregation-breach` on createRole, a bare 409 on setRolePermissions and setPrincipalModuleAccess, and nothing on
    createDelegatedAccess, so a client could not switch on it and a grant could bypass it. Every write whose
    description says it runs the check (it names `SegregationRule`) declares a 409 listing `segregation-breach`, and no
    response anywhere carries that type with another status. Reads that name the rule (listPermissionFindings) report
    conflicts and refuse nothing, so they are not asked for a 409."""
    for oid, f in sorted(ops.items()):
        op, doc, m = f["op"], docs[f["contract"]], f["method"]
        carried = {}
        for code, r in (op.get("responses") or {}).items():
            rr, _ = deref(r, doc)
            types = (rr or {}).get("x-ticvai-problem-types") if isinstance(rr, dict) else None
            if isinstance(types, list) and "segregation-breach" in types:
                carried[str(code)] = True
        for c in sorted(carried):
            if c != "409":
                guard.add("C-SEGREGATION-409", f"{oid}:{c}",
                          f"{oid}: {c} carries segregation-breach; the one status for it is 409")
        if m in ("post", "put", "patch") and SEGREGATION.search(str(op.get("description") or "")) \
                and "409" not in carried:
            guard.add("C-SEGREGATION-409", oid,
                      f"{oid}: its description runs the SegregationRule check and no 409 lists segregation-breach")


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
        # **A write addressed by a key in its body says which** (r8 walk, 20 October 2026, CHG-R8WFC-001). The 14 October
        # shapes pass stamped `x-ticvai-singleton` ("one per venue, a PUT replaces it whole") on 121 writes whose note
        # named the body field that picks the record (setGateLane's `gateId`), and on approveManualOverrideSupervisor,
        # whose body names the denied scan; a developer read "singleton" and could not tell one row from one per gate.
        # Such a write declares `x-ticvai-body-key: [field]` instead, and the field must be in its body.
        body_props, body_req = _body_fields(body_node, doc)
        body_key = op.get("x-ticvai-body-key") or []
        if isinstance(body_key, str):
            body_key = [body_key]
        missing_key = [k for k in body_key if k not in body_props]
        if missing_key:
            guard.add("C-BODY-KEY", oid, f"{oid}: x-ticvai-body-key names {', '.join(missing_key)}, not in its body")
        if op.get("x-ticvai-singleton") and m in ("put", "patch", "delete"):
            named = re.findall(r"body's `([A-Za-z]+)`", str(op.get("x-ticvai-singleton-note") or ""))
            ids = [k for k in body_req if k.endswith("Id") and k not in SCOPE_IDS]
            if named or ids:
                guard.add("C-SINGLETON-KEYED", oid,
                          f"{oid}: flagged a singleton, but its body picks the record ({', '.join(named or ids)}): "
                          f"declare x-ticvai-body-key")
        if m in ("put", "patch", "delete") and not path_params and not op.get("x-ticvai-singleton")                 and not (f["item"] or {}).get("x-ticvai-singleton") and not (body_key and not missing_key):
            guard.add("C-NO-ADDRESS", oid, f"{oid}: {m.upper()} {path} has no path key and is not a singleton")
        # C-PUT-KEY (ADAM CR-245, CHG-R10CRF-005): a PUT path id says what it is against the write's key.
        if m == "put" and path_params:
            ptext = " ".join(str(op.get(k) or "") for k in ("description", "summary"))
            pnodes = [n for n, _ in params if n.get("in") == "path"]
            natural = put_natural_keys(ptext, {str(n.get("name")) for n in pnodes})
            r409, _ = deref((op.get("responses") or {}).get("409"), doc)
            listed = (r409.get("x-ticvai-problem-types") or []) if isinstance(r409, dict) else []
            for n in pnodes:
                pd = str(n.get("description") or "")
                if pd.startswith(STOCK_ADDRESS) and natural:
                    guard.add("C-PUT-KEY", f"{oid}:{n.get('name')}",
                              f"{oid}: path {{{n.get('name')}}} says it addresses the item, but the write is keyed on "
                              f"{natural[0][:80]!r}: say the path id is the record's id, a create takes it and a "
                              f"mismatch is 409 <noun>-id-mismatch (ADAM CR-245)")
                for t in ID_MISMATCH.findall(pd):
                    if t not in listed:
                        guard.add("C-PUT-KEY", f"{oid}:{t}",
                                  f"{oid}: path {{{n.get('name')}}} promises 409 {t}, which its 409 does not list")
            if re.search(r"there is no id in the path", ptext, re.I):
                guard.add("C-PUT-KEY", f"{oid}:no-id", f"{oid}: says there is no id in the path, and {path} has one")
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
                    # A field the server omits for a guest caller says so with `x-ticvai-staff-only` (CHG-SHP-010):
                    # the shared schema still serves staff, and the guest never receives it.
                    leak = sorted(k for k, v in (node.get("properties") or {}).items() if INTERNAL.match(k)
                                  and not (isinstance(v, dict) and v.get("x-ticvai-staff-only")))
                    if leak:
                        guard.add("C-GUEST-INTERNAL", oid, f"{oid}: a guest read returns {', '.join(leak)}")
    fam = {}
    for (stem, name), s in sorted(by.items()):
        for p, ps in (s.get("properties") or {}).items():
            if not isinstance(ps, dict):
                continue
            # A property that is a reference to another schema's property of the same contract
            # (`#/components/schemas/DepositBox/properties/id`) is that one definition, not a second typing
            # of the field: compare the property it points to (20 October 2026, r8 integration, CHG-R8INT-001).
            pref = re.fullmatch(r"#/components/schemas/([^/]+)/properties/([^/]+)", str(ps.get("$ref", "")))
            if pref:
                tgt = ((by.get((stem, pref.group(1))) or {}).get("properties") or {}).get(pref.group(2))
                if isinstance(tgt, dict):
                    ps = tgt
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
