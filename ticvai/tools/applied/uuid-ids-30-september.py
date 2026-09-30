# -*- coding: utf-8 -*-
"""ADR-0056 on the wire: every id is a uuid, and a new one is a UUIDv7 (30 September). Re-runnable.

ADR-0056 settled the database half on 30 September: one id type, `uuid`, minted by the application
kernel's `Id.New()` (UUIDv7, time-ordered), with PostgreSQL staying on 16 and no `uuidv7()` in SQL.
`derive-ddl.py` already converts the columns. **The contracts still said ULID**: about 685 id
schemas carried the 26-character Crockford pattern `^[0-9A-HJKMNP-TV-Z]{26}$`, so a client
validating against the contract would refuse every id the service now mints. This makes the
contracts say what the database and the kernel say.

1. **Every ULID pattern becomes `format: uuid`**, in place. The package has 5,458 ids that are
   already inline `type: string, format: uuid`, and no shared id component the contracts point
   at, so the ULID ones join that convention rather than starting a second one. Path and query
   parameters, request and response fields, array items and the `Idempotency-Key` header alike.
   Every schema carrying the pattern was an id of ours (checked by name on 30 September: order,
   entitlement, ticket, line, case, work order, shift ... ids, and the `booking`/`ticket` fields of
   the waiver views, which are order and entitlement ids). **No human code carried it**: order
   numbers, ticket codes, card codes, booking and voucher codes, `*_code` and `reference` fields
   are plain text and are not touched, nor are provider, external and partner ids.
2. **The one named id component is shared now.** `transport.yaml` had a local `Ulid` schema
   (22 references). It is replaced by `shared/common.yaml#/components/schemas/Id`, which carries
   the UUIDv7 description once and stores as `uuid` (`x-ticvai-persistence-column`).
3. **Four ids were text because a ULID was not a uuid**: `inventory.StockReservation.sourceId`
   (a work order, a rental agreement or an order), `maintenance` asset history `referenceId`,
   the marketing opt-in `orderId`, and `tenancy.IdempotencyRecord.idempotencyKey` (26 characters).
   With one id type each is `format: uuid`.
   **And six references to a former ULID key that were plain strings**:
   `FinTaxInvoiceLine.orderLineId`, `ConsentQuestionVersion.questionId`,
   `FeedbackClassification.reviewId`, `WaiverRequirement.orderLineId`, `Refund.ledgerEntryId` and
   `ShopAndDrop.orderId`. `derive-ddl` made them uuid only because their target's key was being
   converted from text; with the target a uuid in the contract, nothing converts, and they fell
   back to text on the first derive after step 1. The contract now says what they hold.
4. **Prose.** Descriptions that said ULID say UUIDv7; the SD-046 retype note and the
   orders conventions are reworded where "ULID" was an argument, not a word.
5. **Events.** The envelope's `eventId` is a UUIDv7 and `aggregateId` a uuid; payload notes that
   said ULID say UUIDv7, and payload id fields typed `string` (order, entitlement, scan, shift ...
   ids, which were strings because they were ULIDs) are `uuid`.
6. **Docs and screens that described the ULID**: `docs/architecture/offline-and-sync.md`, the
   P09 grant overlay text, and one hand-written lineage note (`handoff/api-data-lineage.json`,
   "keyed by ruleId (ULID id)"), which `derive-lineage.py --apply` never rewrites.

Every edit is keyed on what is already there, so a second run reports nothing to do.

    python tools/applied/uuid-ids-30-september.py            dry run
    python tools/applied/uuid-ids-30-september.py --apply
"""
import glob
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv
CHANGED = []

ULID_RE = r"\^\[0-9A-HJKMNP-TV-Z\]\{26\}\$"
BLOCK = re.compile(r"^(\s*)pattern: '?" + ULID_RE + r"'?\s*$")
FLOW = re.compile(r"pattern: '" + ULID_RE + r"'")
EXAMPLE = "01a0f18a-ca80-7c4e-9a3f-5b2d8e1f6a04"

ID_SCHEMA = [
    "    Id:",
    "      type: string",
    "      format: uuid",
    "      x-ticvai-persistence-column: uuid",
    "      description: '**Every id is a uuid, and every new one is a UUIDv7** (ADR-0056, 30 September): time-ordered,",
    "        so a key in an index stays in insertion order, and minted by the service with the kernel''s `Id.New()`.",
    "        A client that creates a record offline (a sale, a scan, a case raised on a device) generates the id",
    "        itself **in the same format** with a UUIDv7 function, and that id doubles as the `Idempotency-Key`.",
    "        Ids are opaque: a client never reads a time or anything else out of one. Human codes a person reads",
    "        or types (order numbers, ticket, card, booking and voucher codes) are not ids and stay text; so do",
    "        provider, external and partner ids, which are not ours.",
    "",
    "        Inline `type: string, format: uuid` means the same thing; this component is for a contract that",
    "        wants one name for it.'",
    f"      example: {EXAMPLE}",
]


class Text:
    """A file read and written with its own line endings."""

    def __init__(self, path):
        self.path = Path(path)
        self.text = io.open(self.path, encoding="utf-8", newline="").read()
        self.orig = self.text
        self.nl = "\r\n" if "\r\n" in self.text else "\n"

    @property
    def rel(self):
        return self.path.relative_to(ROOT).as_posix()

    def sub(self, old, new, label, count=1):
        """Replace a literal. Silent when `new` is already there (a second run)."""
        if old in self.text:
            self.text = self.text.replace(old, new, count if count else -1)
            CHANGED.append(f"{self.rel}: {label}")
            return True
        return False

    def save(self):
        if self.text != self.orig and APPLY:
            io.open(self.path, "w", encoding="utf-8", newline="").write(self.text)
        return self.text != self.orig


# ---------------------------------------------------------------------------------------------
# 1-4. contracts
# ---------------------------------------------------------------------------------------------

SPECIAL = {
    # The retype note argued from the ULID; the argument is gone and the column is a uuid again.
    "satellite/fnb.yaml": [
        ("**Retyped 29 September (SD-046)**: `orders.sales_order.id` is a ULID, so a uuid here could never\n"
         "            join.",
         "**Retyped 29 September (SD-046)**, and `format: uuid` since ADR-0056 (30 September): every id is\n"
         "            a uuid, so this joins `orders.sales_order.id`.",
         "SD-046 note reworded"),
    ],
    "spine/orders.yaml": [
        ("are ULIDs (`^[0-9A-HJKMNP-TV-Z]{26}$`) everywhere",
         "are UUIDv7s (`format: uuid`) everywhere", "conventions: ids are UUIDv7"),
        ("template, a policy) is a uuid.",
         "template, a policy) is a uuid too, minted by the service (ADR-0056).", "conventions: one id type"),
    ],
}


def _prop_block(lines, i):
    """(start, end) of the property whose header is line i: every deeper line after it."""
    ind = len(lines[i]) - len(lines[i].lstrip())
    j = i + 1
    while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > ind):
        j += 1
    return i, j


def text_id_to_uuid(c, schema_hint, prop, drop, description=None, back=False):
    """A text id that was text only because a ULID is not a uuid: `format: uuid` in its block."""
    lines = c.text.split(c.nl)
    hint = next((n for n, l in enumerate(lines) if schema_hint in l), None)
    if hint is None:
        print(f"  !! {c.rel}: anchor {schema_hint!r} not found")
        return
    rng = range(hint, -1, -1) if back else range(hint, len(lines))
    i = next((n for n in rng if lines[n].strip() == f"{prop}:"), None)
    if i is None:
        print(f"  !! {c.rel}: {prop} not found after {schema_hint!r}")
        return
    s, e = _prop_block(lines, i)
    body = lines[s + 1:e]
    if any(l.strip() == "format: uuid" for l in body):
        return
    ind = " " * (len(lines[i]) - len(lines[i].lstrip()) + 2)
    body = [l for l in body if l.strip() not in drop]
    t = next(n for n, l in enumerate(body) if l.strip() == "type: string")
    body.insert(t + 1, f"{ind}format: uuid")
    if description:
        d = next(n for n, l in enumerate(body) if l.strip().startswith("description:"))
        k = d + 1
        while k < len(body) and len(body[k]) - len(body[k].lstrip()) > len(ind):
            k += 1
        body[d:k] = [f"{ind}{x}" if x else "" for x in description]
    lines[s + 1:e] = body
    c.text = c.nl.join(lines)
    CHANGED.append(f"{c.rel}: {prop} (under {schema_hint.strip()}) is format: uuid")


# (contract, schema, property): plain strings pointing at a key that was a ULID.
PLAIN_REFS = [
    ("spine/finance.yaml", "FinTaxInvoiceLine", "orderLineId"),
    ("satellite/marketing-crm.yaml", "ConsentQuestionVersion", "questionId"),
    ("satellite/marketing-crm.yaml", "FeedbackClassification", "reviewId"),
    ("satellite/marketing-crm.yaml", "WaiverRequirement", "orderLineId"),
    ("spine/orders.yaml", "Refund", "ledgerEntryId"),
    ("satellite/retail.yaml", "ShopAndDrop", "orderId"),
]


def plain_ref_to_uuid(c, schema, prop):
    lines = c.text.split(c.nl)
    s = next((n for n, l in enumerate(lines) if l.rstrip() == f"    {schema}:"), None)
    if s is None:
        print(f"  !! {c.rel}: schema {schema} not found")
        return
    _, e = _prop_block(lines, s)
    i = next((n for n in range(s, e) if lines[n].strip() == f"{prop}:"), None)
    if i is None:
        print(f"  !! {c.rel}: {schema}.{prop} not found")
        return
    _, pe = _prop_block(lines, i)
    body = [l.strip() for l in lines[i + 1:pe]]
    if "format: uuid" in body:
        return
    t = next(n for n in range(i + 1, pe) if lines[n].strip() == "type: string")
    ind = lines[t][:len(lines[t]) - len(lines[t].lstrip())]
    lines.insert(t + 1, f"{ind}format: uuid")
    c.text = c.nl.join(lines)
    CHANGED.append(f"{c.rel}: {schema}.{prop} is format: uuid")


def contracts():
    pats = 0
    for p in sorted(glob.glob(str(ROOT / "contracts" / "**" / "*.yaml"), recursive=True)):
        c = Text(p)
        rel = Path(p).relative_to(ROOT / "contracts").as_posix()

        # 1. the pattern, block and flow style
        lines = c.text.split(c.nl)
        n = 0
        for k, l in enumerate(lines):
            m = BLOCK.match(l)
            if m:
                lines[k] = f"{m.group(1)}format: uuid"
                n += 1
            elif FLOW.search(l):
                lines[k], x = FLOW.subn("format: uuid", l)
                n += x
        if n:
            c.text = c.nl.join(lines)
            CHANGED.append(f"{c.rel}: {n} ULID pattern(s) -> format: uuid")
            pats += n

        # 2. the one named id component
        if rel == "satellite/transport.yaml":
            k = c.text.count("'#/components/schemas/Ulid'")
            if k:
                c.text = c.text.replace("'#/components/schemas/Ulid'",
                                        "'../shared/common.yaml#/components/schemas/Id'")
                CHANGED.append(f"{c.rel}: {k} reference(s) to the local Ulid -> shared Id")
            lines = c.text.split(c.nl)
            s = next((n for n, l in enumerate(lines) if l.rstrip() == "    Ulid:"), None)
            if s is not None:
                _, e = _prop_block(lines, s)
                while e < len(lines) and not lines[e].strip():
                    e += 1
                del lines[s:e]
                c.text = c.nl.join(lines)
                CHANGED.append(f"{c.rel}: local Ulid schema removed")
        if rel == "shared/common.yaml" and "\n    Id:" not in c.text.replace("\r\n", "\n"):
            lines = c.text.split(c.nl)
            s = next(n for n, l in enumerate(lines) if l.rstrip() == "  schemas:")
            lines[s + 1:s + 1] = ID_SCHEMA
            c.text = c.nl.join(lines)
            CHANGED.append(f"{c.rel}: shared Id schema (UUIDv7) added")

        # 3. text ids that were text because of the ULID
        if rel == "satellite/inventory.yaml":
            text_id_to_uuid(c, "x-ticvai-persistence: inventory.stock_reservation", "sourceId",
                            {"maxLength: 64"}, [
                                "description: 'The id of what the stock is reserved for: a work order, a rental agreement or",
                                "  an order. A uuid, as every id is (ADR-0056); it was text from 29 September to 30 September",
                                "  because a work order id was then 26-character text (M17-02).'"])
        if rel == "satellite/maintenance.yaml":
            text_id_to_uuid(c, "enum: [workOrder, inspection, incident, statusChange, partReplaced, planCompleted]",
                            "referenceId", set(), [
                                "description: >",
                                "  The source row's id: a work order, inspection or incident, or an",
                                "  `asset_status_change` id. A uuid, as every id is (ADR-0056)."])
        if rel == "satellite/marketing-crm.yaml":
            text_id_to_uuid(c, "The order whose checkout carried the opt-in", "orderId", set(), back=True)
        if rel == "spine/tenancy.yaml":
            text_id_to_uuid(c, "x-ticvai-persistence: platform.idempotency_record", "idempotencyKey",
                            {"maxLength: 26"})

        for f, sch, prop in PLAIN_REFS:
            if f == rel:
                plain_ref_to_uuid(c, sch, prop)

        # 4. prose
        for old, new, label in SPECIAL.get(rel, []):
            c.sub(old.replace("\n", c.nl), new.replace("\n", c.nl), label)
        k = len(re.findall(r"\bULIDs?\b", c.text))
        if k:
            c.text = re.sub(r"\bULIDs\b", "UUIDv7s", c.text)
            c.text = re.sub(r"\bULID\b", "UUIDv7", c.text)
            CHANGED.append(f"{c.rel}: {k} mention(s) of ULID -> UUIDv7")
        c.save()
    return pats


# ---------------------------------------------------------------------------------------------
# 5. events
# ---------------------------------------------------------------------------------------------

EXTERNAL = ("provider", "external", "partner")


def events():
    c = Text(ROOT / "events" / "_schema.yaml")
    c.sub("`eventId` (ULID, the consumer inbox", "`eventId` (a UUIDv7, the consumer inbox", "eventId is a UUIDv7")
    c.sub("`aggregateId` (text: order ids are ULIDs),", "`aggregateId` (a uuid, as every id is: ADR-0056),",
          "aggregateId is a uuid")
    c.save()
    for p in sorted(glob.glob(str(ROOT / "events" / "*.yaml"))):
        if p.endswith("_schema.yaml"):
            continue
        c = Text(p)
        lines = c.text.split(c.nl)
        n = 0
        for k, l in enumerate(lines):
            m = re.match(r"^- field: (\w+)\s*$", l)
            if not m or k + 1 >= len(lines):
                continue
            f = m.group(1)
            if not (f == "id" or f.endswith("Id")) or f.lower().startswith(EXTERNAL):
                continue
            if lines[k + 1].strip() == "type: string":
                lines[k + 1] = lines[k + 1].replace("type: string", "type: uuid")
                n += 1
        if n:
            c.text = c.nl.join(lines)
            CHANGED.append(f"{c.rel}: {n} payload id field(s) string -> uuid")
        k = len(re.findall(r"\bULID\b", c.text))
        if k:
            c.text = re.sub(r"\bULID\b", "UUIDv7", c.text)
            CHANGED.append(f"{c.rel}: {k} note(s) ULID -> UUIDv7")
        c.save()


# ---------------------------------------------------------------------------------------------
# 6. docs and screens
# ---------------------------------------------------------------------------------------------

def docs():
    c = Text(ROOT / "docs" / "architecture" / "offline-and-sync.md")
    c.sub("| **Idempotency** | Client-generated ULID, sent as `Idempotency-Key`.",
          "| **Idempotency** | Client-generated UUIDv7 (the id format the service mints, ADR-0056), sent as "
          "`Idempotency-Key`.", "idempotency key is a UUIDv7")
    c.sub("| `ulid` | ID generation matching the backend's generator |",
          "| `id` | UUIDv7 generation (the `uuid` package's `v7`), the format the backend's `Id.New()` mints |",
          "id generation is UUIDv7")
    c.save()
    for p in sorted(glob.glob(str(ROOT / "screens" / "P09-*.yaml"))):
        c = Text(p)
        c.sub("Required: `id` (a client ULID)", "Required: `id` (a client UUIDv7)",
              "grant overlay: client UUIDv7", count=0)
        c.save()


def lineage_notes():
    import json
    p = ROOT / "handoff" / "api-data-lineage.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for op, v in d.items():
        note = v.get("lineageNote") if isinstance(v, dict) else None
        if isinstance(note, str) and re.search(r"\bULID\b", note):
            v["lineageNote"] = re.sub(r"\bULID\b", "UUIDv7", note)
            CHANGED.append(f"handoff/api-data-lineage.json: {op} note ULID -> UUIDv7")
            n += 1
    if n and APPLY:
        io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    n = contracts()
    lineage_notes()
    events()
    docs()
    for x in CHANGED:
        print(f"  {x}")
    print(f"  ULID patterns replaced: {n}")
    if not CHANGED:
        print("  nothing to do")
    print("  applied" if APPLY else "  dry run: pass --apply")
