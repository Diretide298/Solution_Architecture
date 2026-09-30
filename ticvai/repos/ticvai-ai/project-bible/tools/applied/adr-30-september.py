# -*- coding: utf-8 -*-
"""ADR-0056, ADR-0058 and ADR-0049, accepted 30 September: the root-file half. Re-runnable.

The DDL is derived, so these decisions reach `backend/` through what `derive-schema` and
`derive-ddl` read. This script edits those roots and nothing else; `derive-ddl.py` carries the
rules (one id type, range partitioning, composite venue keys, vector columns).

1. **ADR-0056: which tables are append-only is a fact about the schema, so the schema says it.**
   `x-ticvai-append-only: <time property>` on the contract schema a table is derived from.
   `derive-ddl` partitions such a table by month on that column when it also has no inbound
   foreign key. Marked: `access.ScanEvent` (recordedAt), `platform-ops.OutboxEntry` (createdAt),
   `platform-ops.DeadLetter` (createdAt), `tenancy.AuditRecord` (occurredAt),
   `finance.JournalLine` (postedAt, **new**, copied from its entry), `marketing-crm.MessageDispatch`
   (queuedAt), and the two inboxes below (eventId: a UUIDv7 is time-ordered, see derive-ddl).
2. **ADR-0056 and ADR-0058: the outbox's ids are uuids.** `OutboxEntry.eventId` was a ULID pattern
   and `aggregateId` free text of 64 characters, because order ids were ULIDs. With one id type
   both are `format: uuid`; `eventId` is the outbox row's own id (UUIDv7).
3. **ADR-0058: the inbox and the relay lease.** `platform-ops.InboxEntry` -> `kernel.inbox`,
   `ai.AiInboxEntry` -> `ai.inbox` (only AI writes AI tables, ADR-0020), and
   `platform-ops.OutboxRelay` -> `control.outbox_relay`, the relay lease table, in the regional
   control database. **Not called `relay_lease`**: derive-relationships reads a `*_lease_id` column
   as a reference to any table ending `_lease`, and `catalogue.inventory_hold.parent_lease_id`
   (a venue edge node's sub-lease) pointed at it on the first run.
   `x-ticvai-primary-key` names a key that is not a single `id`.
4. **Vectors live in Qdrant from day one** (Chinmay, 30 September; the ADR-0049 draft's in-database
   vector option was not taken). One Qdrant collection per tenant and embedding model behind the alias
   `tenant_<tenantId>`, a JWT per tenant scoped to its collection, and venue scope as a payload
   filter the retrieval client always adds. **So `ai.chunk_embedding` holds no vector**: its
   `dense` and `sparse` columns are retired and it keeps the reference to the Qdrant point
   (collection alias, point id, embedding model, content hash, indexed_at), which is what lets
   erasure and a re-embed be tracked in the tenant database.
5. **The lineage store stays `qdrant`** on the AI operations. `qdrant` is added to `stores` where an
   operation reads or writes the vector tables (`ai.chunk_embedding`, `ai.chunk_ref`,
   `qdrant:knowledge`) and does not name it; on 30 September there were none.

Every edit is textual and keyed on what is already there, so a second run reports nothing to do.
"""
import io
import re
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv
CHANGED = []


class Contract:
    def __init__(self, rel):
        self.path = ROOT / "contracts" / rel
        self.text = io.open(self.path, encoding="utf-8", newline="").read()
        self.nl = "\r\n" if "\r\n" in self.text else "\n"
        self.lines = self.text.split(self.nl)
        self.dirty = False

    def schema(self, name):
        """Index of the `    <name>:` line under components/schemas."""
        for i, l in enumerate(self.lines):
            if l.rstrip() == f"    {name}:":
                return i
        return None

    def block_end(self, start, indent):
        """First line after `start` whose indent is <= `indent` (and is not blank)."""
        for j in range(start + 1, len(self.lines)):
            l = self.lines[j]
            if l.strip() and (len(l) - len(l.lstrip())) <= indent:
                return j
        return len(self.lines)

    def has_key(self, s, key):
        end = self.block_end(s, 4)
        return any(self.lines[j].startswith(f"      {key}:") for j in range(s + 1, end))

    def mark(self, name, key, value, label):
        s = self.schema(name)
        if s is None:
            raise SystemExit(f"  ! {self.path.name}: no schema {name}")
        if self.has_key(s, key):
            return
        self.lines.insert(s + 1, f"      {key}: {value}")
        self.dirty = True
        CHANGED.append(label)

    def prop(self, schema, prop):
        """(start, end) of `        <prop>:` inside the schema's own `properties:`."""
        s = self.schema(schema)
        end = self.block_end(s, 4)
        p = next(j for j in range(s + 1, end) if self.lines[j].rstrip() == "      properties:")
        for j in range(p + 1, end):
            if self.lines[j].rstrip() == f"        {prop}:":
                return j, self.block_end(j, 8)
        return None, None

    def replace_prop(self, schema, prop, body, label, done_if):
        a, b = self.prop(schema, prop)
        if a is None:
            raise SystemExit(f"  ! {self.path.name}: {schema}.{prop} not found")
        current = self.lines[a + 1:b]
        if any(done_if in l for l in current):
            return
        self.lines[a + 1:b] = [f"          {l}" for l in body]
        self.dirty = True
        CHANGED.append(label)

    def add_prop(self, schema, prop, body, label, required=False):
        a, _ = self.prop(schema, prop)
        if a is not None:
            return
        s = self.schema(schema)
        end = self.block_end(s, 4)
        self.lines[end:end] = [f"        {prop}:"] + [f"          {l}" for l in body]
        if required:
            r = next(j for j in range(s + 1, end) if self.lines[j].rstrip() == "      required:")
            k = r + 1
            while self.lines[k].startswith("      - "):
                k += 1
            self.lines.insert(k, f"      - {prop}")
        self.dirty = True
        CHANGED.append(label)

    def add_schema(self, name, block, label):
        if self.schema(name) is not None:
            return
        at = next(i for i, l in enumerate(self.lines) if l.rstrip() == "  schemas:")
        self.lines[at + 1:at + 1] = [f"    {name}:"] + [f"      {l}" for l in block]
        self.dirty = True
        CHANGED.append(label)

    def save(self):
        if self.dirty and APPLY:
            io.open(self.path, "w", encoding="utf-8", newline="").write(self.nl.join(self.lines))


def inbox_schema(table, who, extra):
    return [
        "type: object",
        f"x-ticvai-persistence: {table}",
        "x-ticvai-primary-key:",
        "- consumer",
        "- eventId",
        "x-ticvai-append-only: eventId",
        "description: '**The consumer''s record of every event it has processed** (ADR-0058). "
        "Inserted in the same",
        "  transaction as the effect, with `ON CONFLICT DO NOTHING`; no row inserted means "
        "already processed, so skip",
        f"  and acknowledge. {who} Kept 30 days, longer than any redelivery window, and dropped "
        "a month at a",
        "  time: partitioned by month on `eventId`, which is a UUIDv7 and so sorts by time "
        f"(ADR-0056).{extra}'",
        "required:",
        "- consumer",
        "- eventId",
        "- processedAt",
        "properties:",
        "  consumer:",
        "    type: string",
        "    maxLength: 200",
        "    description: The consumer's stable name (`<service>.<handler>`); one event is "
        "processed once per consumer.",
        "  eventId:",
        "    type: string",
        "    format: uuid",
        "    description: The envelope's `eventId`, which is the producing outbox row's id "
        "(UUIDv7).",
        "  processedAt:",
        "    type: string",
        "    format: date-time",
    ]


CHUNK_EMBEDDING = [
    "type: object",
    "x-ticvai-persistence: ai.chunk_embedding",
    "x-ticvai-retired-columns:",
    "- dense",
    "- sparse",
    "description: '**The tenant database''s record of one chunk''s point in Qdrant** (decided 30 September:",
    "  vectors go to Qdrant from day one). The vectors themselves live in the tenant''s own Qdrant collection,",
    "  one per embedding model behind the alias `tenant_<tenantId>`, reached with a JWT scoped to that",
    "  collection; venue scope is a payload filter the retrieval client always adds. **This row is how erasure",
    "  and a re-embed are tracked where the rest of the tenant''s data is**: which point, in which collection,",
    "  from which model and which content, indexed when. It holds no vector. **Scoped through its document**",
    "  (`platform.apply_parent_rls`).'",
    "required:",
    "- documentId",
    "- chunkIndex",
    "- embeddingModel",
    "- collectionAlias",
    "- pointId",
    "properties:",
    "  id:",
    "    type: string",
    "    format: uuid",
    "    readOnly: true",
    "  documentId:",
    "    type: string",
    "    format: uuid",
    "    x-ticvai-references: ai.knowledge_document",
    "  chunkIndex:",
    "    type: integer",
    "    minimum: 0",
    "  parentChunkId:",
    "    type: string",
    "    format: uuid",
    "    nullable: true",
    "    description: The parent section, where the source uses `parentChild` chunking.",
    "  content:",
    "    type: string",
    "    description: The chunk text. Kept so an answer can cite it.",
    "  embeddingModel:",
    "    type: string",
    "    description: The model that produced the point; a model change re-embeds into a new collection.",
    "  collectionAlias:",
    "    type: string",
    "    maxLength: 200",
    "    readOnly: true",
    "    description: 'The Qdrant collection alias the point is in: `tenant_<tenantId>` for the current model.'",
    "  pointId:",
    "    type: string",
    "    format: uuid",
    "    readOnly: true",
    "    description: The Qdrant point id. Deleting the chunk deletes this point; erasure reads it from here.",
    "  tokenCount:",
    "    type: integer",
    "  contentHash:",
    "    type: string",
    "    description: Hash of `content`; a chunk whose hash is unchanged is not re-embedded.",
    "  indexedAt:",
    "    type: string",
    "    format: date-time",
    "    nullable: true",
    "    readOnly: true",
    "    description: When the point was last written to Qdrant; null until it has been.",
    "  createdAt:",
    "    type: string",
    "    format: date-time",
    "    readOnly: true",
]


def contracts():
    # --- platform-ops: outbox, dead letter, inbox, relay lease --------------------------------
    c = Contract("satellite/platform-ops.yaml")
    c.mark("OutboxEntry", "x-ticvai-append-only", "createdAt",
           "OutboxEntry: append-only on createdAt")
    c.mark("DeadLetter", "x-ticvai-append-only", "createdAt",
           "DeadLetter: append-only on createdAt")
    c.replace_prop("OutboxEntry", "eventId", [
        "type: string",
        "format: uuid",
        "description: '**The envelope''s event id, which is this row''s `id`** (ADR-0058; "
        "UUIDv7, ADR-0056). The",
        "  consumer inbox key, so a redelivery is recognised as the same event. "
        "`events/_schema.yaml` defines",
        "  the envelope.'",
    ], "OutboxEntry.eventId: uuid", done_if="ADR-0058")
    c.replace_prop("OutboxEntry", "aggregateId", [
        "type: string",
        "format: uuid",
        "description: '**Which row changed** (ADR-0056: every id is a uuid, so every aggregate "
        "fits). Also the",
        "  broker ordering key (ADR-0058): a partition key in Kafka, a consistent-hash or "
        "single-active-consumer key",
        "  in RabbitMQ, so one aggregate''s events arrive in `sequence` order.'",
    ], "OutboxEntry.aggregateId: uuid", done_if="ADR-0056")
    c.add_schema("InboxEntry", inbox_schema(
        "kernel.inbox", "One per tenant database, written by every consumer through the "
        "kernel's inbox wrapper.", ""), "InboxEntry -> kernel.inbox")
    c.add_schema("OutboxRelay", [
        "type: object",
        "x-ticvai-persistence: control.outbox_relay",
        "x-ticvai-primary-key:",
        "- cellTenantId",
        "description: '**Which worker replica relays which tenant database''s outbox** "
        "(ADR-0058). One row per tenant",
        "  database in the region, in the regional control database. A replica holds a lease by "
        "renewing it every",
        "  few seconds; when it dies the lease expires and another replica takes it, so exactly "
        "one publisher per",
        "  tenant database keeps per-tenant order. pgbouncer runs in transaction mode, so this "
        "is a row and not a",
        "  session advisory lock.'",
        "required:",
        "- cellTenantId",
        "- holder",
        "- leaseExpiresAt",
        "properties:",
        "  cellTenantId:",
        "    type: string",
        "    format: uuid",
        "    x-ticvai-references: control.cell_tenant",
        "    description: The tenant database this lease covers (`control.cell_tenant`).",
        "  holder:",
        "    type: string",
        "    maxLength: 200",
        "    description: The worker replica holding the lease (pod name plus a start nonce).",
        "  leaseExpiresAt:",
        "    type: string",
        "    format: date-time",
        "    description: Another replica may take the lease after this instant.",
        "  acquiredAt:",
        "    type: string",
        "    format: date-time",
        "  renewedAt:",
        "    type: string",
        "    format: date-time",
        "  lastPolledAt:",
        "    type: string",
        "    format: date-time",
        "    nullable: true",
        "    description: The end of the last poll, for the relay-lag dashboard.",
    ], "OutboxRelay -> control.outbox_relay")
    c.save()

    # --- ai: the AI inbox and the vector columns ---------------------------------------------
    c = Contract("satellite/ai.yaml")
    c.add_schema("AiInboxEntry", inbox_schema(
        "ai.inbox", "AI consumers write this rather than `kernel.inbox`, because only AI writes "
        "AI tables (ADR-0020).", ""), "AiInboxEntry -> ai.inbox")
    s = c.schema("AiChunkEmbedding")
    e = c.block_end(s, 4)
    if not any(l.strip() == "pointId:" for l in c.lines[s:e]):
        c.lines[s + 1:e] = [f"      {l}" for l in CHUNK_EMBEDDING]
        c.dirty = True
        CHANGED.append("AiChunkEmbedding: the Qdrant point reference, no vector columns")
    c.save()

    # --- the other append-only tables -----------------------------------------------------------
    for rel, name, col in (("spine/access.yaml", "ScanEvent", "recordedAt"),
                           ("spine/tenancy.yaml", "AuditRecord", "occurredAt"),
                           ("satellite/marketing-crm.yaml", "MessageDispatch", "queuedAt"),
                           ("spine/finance.yaml", "JournalLine", "postedAt")):
        c = Contract(rel)
        c.mark(name, "x-ticvai-append-only", col, f"{name}: append-only on {col}")
        if name == "JournalLine":
            c.add_prop("JournalLine", "postedAt", [
                "type: string",
                "format: date-time",
                "readOnly: true",
                "description: '**Copied from the journal entry when it posts** (ADR-0056), so the "
                "line table can be",
                "  partitioned by month on its own column. Never differs from its entry''s.'",
            ], "JournalLine.postedAt added")
        c.save()


OLD_NOTE_RE = re.compile(r"ai\.chunk_ref and qdrant:knowledge replaced by ai\.chunk_embedding "
                         r"\([^)]*design 5\.8\)\.?")
NEW_NOTE = ("ai.chunk_embedding records each chunk's point in the tenant's Qdrant collection "
            "(qdrant:knowledge); vectors live in Qdrant from day one (decided 30 September).")
VECTOR_TABLES = {"ai.chunk_embedding", "ai.chunk_ref", "qdrant:knowledge"}


def lineage():
    """`qdrant` in `stores` wherever an operation touches the vector tables and does not name it."""
    p = ROOT / "handoff" / "api-data-lineage.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for op, v in d.items():
        if not isinstance(v, dict):
            continue
        touched = set(v.get("reads") or []) | set(v.get("writes") or [])
        st = v.get("stores") or []
        if touched & VECTOR_TABLES and "qdrant" not in st:
            v["stores"] = sorted(set(st) | {"qdrant"})
            n += 1
        # Two notes of 29 September said the vectors had moved into the tenant database.
        note = v.get("lineageNote")
        if isinstance(note, str) and OLD_NOTE_RE.search(note):
            v["lineageNote"] = OLD_NOTE_RE.sub(NEW_NOTE, note)
            n += 1
    print(f"  lineage: {n} change(s) -- qdrant in stores where the vector tables are touched, notes")
    if APPLY and n:
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            json.dumps(d, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    contracts()
    for c in CHANGED:
        print(f"  {c}")
    if not CHANGED:
        print("  contracts: nothing to do")
    lineage()
    print("  applied" if APPLY else "  dry run: pass --apply")
