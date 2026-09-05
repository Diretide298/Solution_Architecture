#!/usr/bin/env python3
"""Give the 577 drafted pack operations a request and a response, read out of the pack.

**They were drafted without a shape on purpose.** `tools/draft-pack-operations.py` gave every
workshop-pack screen an operation with a name, an audience, a scope, a permission and an envelope,
and said in each description that the shape was the part a person writes. That was the right call
at the time: the pack had not been read closely enough to know whether its bullets were fields or
captions. They are fields. *"Each zone receives capacity, operating schedule, security
classification, entry requirements, exit requirements, allowed credential classes"* is a directory
written by the people who own the requirement, and 13,312 such bullets survive the reading.

So this tool replaces the envelope with a schema derived from the screen's own words, and every
property carries the sentence it came from in its `description` so the reading can be checked
against the PDF in one step.

**Three things it will not do.**

1. **It does not invent a table.** Every schema it writes declares its persistence in the
   package's own existing vocabulary - `none — projection over ...` for a read, `none — request
   only` for a write - which is a positive statement that the shape is not a row, not the silence
   that means nobody has decided. 234 of the package's 766 schemas already say exactly this. Which
   drafted writes deserve a table is a separate question, and `--entities` reports the grouped
   answer without acting on it. **The em dash is load-bearing**: `derive-schema` treats a
   persistence value containing `—` as "not a table", and these strings name a real table inside
   their evidence, so a hyphen there would have registered `access.parking_facility at 6%` as a
   table of its own.
2. **It does not invent a permission, a scope or an audience.** Those were derived once and are
   read back off the existing operation unchanged, `x-ticvai-config-scope` included - that tag was
   applied wrongly once already and the repair is not going to be undone by a regeneration.
3. **It does not drop `x-ticvai-provisional`.** A shape read out of a PDF is still a draft. What
   changes is what the draft contains: an operation somebody can review line by line instead of an
   envelope nobody can.

**How it writes.** In every contract the drafted paths are one contiguous run ending at
`components:`, because they were appended there. That run is regenerated wholesale and nothing
above it is touched; the new schemas go in immediately before `securitySchemes:`, or at the end
where `schemas:` is last. Emission goes through `yaml.safe_dump`, so the apostrophe that broke
`workforce.yaml` on `roster's` cannot happen here.

Run: `python tools/specify-pack-operations.py [--apply] [--only <contract>] [--entities]`
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from packshape import screen_shape                                    # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MONEY = "../shared/common.yaml#/components/schemas/Money"

# A schema this wide is a screen, not a record; past this the list stops being reviewable and the
# extra names are the least confident ones anyway.
MAX_PROPS = 40
MAX_QUERY = 8


# -- joining an operation to the screen and the pack record it came from -------------------------
def screens_by_id() -> dict:
    out = {}
    for f in sorted((ROOT / "screens").glob("P*.yaml")):
        doc = yaml.safe_load(io.open(f, encoding="utf-8").read()) or {}
        for s in doc.get("screens") or []:
            out[s["id"]] = s
    return out


def pack_by_key() -> dict:
    recs = json.loads(io.open(ROOT / "sources" / "workshop" / "pack.json",
                              encoding="utf-8").read())
    return {(r["source"], str(r["board"]), str(r["number"])): r for r in recs}


def pascal(text: str) -> str:
    toks = [t for t in re.split(r"[^A-Za-z0-9]+", text) if t]
    return "".join(t[:1].upper() + t[1:] if not t.isupper() else t.capitalize() for t in toks)


MARK = "x-ticvai-drafted-shape"

# **The client's own words for a record definition.** `For each attraction: Attraction ID, Name,
# Venue, Zone, Capacity ...` is somebody specifying a row. Thirteen of the 153 drafted writes have
# one; the rest describe a screen, which is why the pack cannot be read as a data model.
RECORD_HEADING = re.compile(
    r"^(for each|each \w+ (receives|has|carries|gets|shall (show|contain)|"
    r"should (display|include|contain)))|^(every|per) \w+", re.I)


def ddl_columns() -> dict:
    """`{schema.table: {column, ...}}` straight out of the DDL the package already applies.

    Used to answer, with evidence rather than a name match, whether a drafted write is really an
    update to something that exists. Fuzzy-matching the screen TITLE against table names said yes
    77 times and was wrong nearly every time - `setMinorGuardianAge` does not write
    `marketing.privacy_incident`. Comparing the FIELDS says no 152 times out of 152.
    """
    cols = {}
    for f in sorted((ROOT / "backend").glob("*/0*.sql")):
        t = io.open(f, encoding="utf-8").read()
        for m in re.finditer(r"CREATE TABLE (?:IF NOT EXISTS )?([a-z_]+)\.([a-z_]+)\s*\((.*?)\n\);",
                             t, re.S | re.I):
            got = set()
            for line in m.group(3).split("\n"):
                c = re.match(r"\s+([a-z_]+)\s+[A-Za-z]", line)
                if c:
                    got.add(c.group(1))
            cols["%s.%s" % (m.group(1), m.group(2))] = got
    return cols


# Present on nearly every table, so their overlap says nothing about whether the record matches.
GENERIC_COLUMNS = {"id", "tenant_id", "venue_id", "created_at", "updated_at", "name", "status",
                   "type", "version", "notes", "code", "description"}


def snake(n: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", n).lower()


def nearest_table(props: dict, schemas_owned: set, cols: dict) -> tuple:
    want = {snake(x) for x in props} - GENERIC_COLUMNS
    if not want:
        return 0.0, None
    best = (0.0, None)
    for tb, cs in cols.items():
        if tb.split(".")[0] not in schemas_owned:
            continue
        ov = len(want & cs) / float(len(want))
        if ov > best[0]:
            best = (ov, tb)
    return best


def owned_schemas():
    """Which database schemas each contract's tables live in, read off its own persistence tags."""
    out = collections.defaultdict(set)
    for c in sorted((ROOT / "contracts").rglob("*.yaml")):
        doc = yaml.safe_load(io.open(c, encoding="utf-8").read()) or {}
        for n, s in ((doc.get("components") or {}).get("schemas") or {}).items():
            t = (s or {}).get("x-ticvai-persistence") if isinstance(s, dict) else None
            if isinstance(t, str) and "." in t and not t.startswith("none"):
                out[c.stem].add(t.split(".")[0].strip('"'))
    return out


def existing_schema_names() -> set:
    """Every schema name already taken - EXCEPT the ones this tool wrote.

    **Otherwise a second run collides with its own first.** The names are derived from the screen
    title, so re-running would find `RulesWorkflowCommandCenterView` already present, rename to
    `RulesWorkflowCommandCenter2View`, and leave the original orphaned. Skipping schemas that carry
    this tool's own persistence tag makes the run idempotent, which is what lets the shaping be
    corrected and re-applied.
    """
    names = set()
    for c in sorted((ROOT / "contracts").rglob("*.yaml")):
        doc = yaml.safe_load(io.open(c, encoding="utf-8").read()) or {}
        for n, s in ((doc.get("components") or {}).get("schemas") or {}).items():
            if isinstance(s, dict) and s.get(MARK):
                continue
            names.add(n)
    return names


# -- the shape of one drafted operation ----------------------------------------------------------
DERIVED_NOTE = (
    "**Drafted from the workshop pack; the shape below is read out of it, not invented.** "
    "%(module)s, page %(page)s. The screen says: %(purpose)s\n\n"
    "**Every property carries the sentence it came from.** %(nprops)d were read from the screen's "
    "own bulleted directory and %(ndropped)d bullets were dropped as prose, examples or hierarchy "
    "illustrations rather than bent into fields. Names and types are this package's reading of "
    "those sentences and are the part to check; the sentences themselves are the client's.\n\n"
    "**Still provisional.** A shape read out of a PDF has not been agreed with anyone who has to "
    "build it, and the schema says so in its own persistence tag: it is %(persist)s."
)


def build(op, rec, name, contract, owned, cols):
    """Returns (new op dict, {schema name: schema}) for one drafted operation."""
    shape = screen_shape(rec, money_ref=MONEY)
    props = dict(list(shape["props"].items())[:MAX_PROPS])
    kinds = shape["kinds"]
    verb_is_read = (op.get("operationId") or "").startswith(("list", "get", "search"))

    schemas = {}
    view = name + "View"
    projection = ("none — projection over %s state, assembled at read time from tables that "
                  "already exist" % contract)
    schemas[view] = {
        "type": "object",
        "x-ticvai-drafted-shape": True,
        "x-ticvai-persistence": projection,
        "description": ("**What %s displays.** Read from the workshop pack's own display and "
                        "configuration directory for this screen; each property names the "
                        "sentence it came from. **Not a row** - the screen is a view over the "
                        "module's existing state." % rec["title"]),
        "properties": props or {"note": {"type": "string"}},
    }
    body = None
    if not verb_is_read:
        # A write may only send what the screen configures. A number the dashboard displays is
        # something the system computed; accepting it back would let a client overwrite a total.
        writable = {k: v for k, v in props.items() if kinds.get(k) != "metrics"} or props
        inp = name + "Input"
        # **The table question, answered with evidence and written where it will not rot.**
        ov, tb = nearest_table(writable, owned, cols)
        if tb and ov >= 0.5:
            verdict = ("none — request only; these fields are already columns of %s (%d%% "
                       "overlap), so this updates an existing table" % (tb, round(ov * 100)))
        elif tb:
            verdict = ("none — request only; **no existing table covers these fields** — the "
                       "closest is %s at %d%%, so this is not an update to anything the package "
                       "stores today and no new table has been decided" % (tb, round(ov * 100)))
        else:
            verdict = ("none — request only; **no existing table shares a single field with "
                       "this**, so nothing the package stores today is what this configures")
        rd = next((h for h in (rec.get("sections") or {}) if RECORD_HEADING.match(h)), None)
        schemas[inp] = {
            "type": "object",
            "x-ticvai-drafted-shape": True,
            "x-ticvai-persistence": verdict,
            "description": ("**What %s submits.** The configurable fields from the pack's "
                            "directory for this screen; the metrics the screen displays are "
                            "deliberately absent, because a figure the system computed is not a "
                            "figure a client may send back.%s" % (
                                rec["title"],
                                ("\n\n**The pack defines this as a record**, under *%s* - one of "
                                 "only 13 drafted writes that does. That is the client writing a "
                                 "row rather than a screen, and it is where the table "
                                 "conversation should start." % rd) if rd else "")),
            "properties": writable,
        }
        if rd:
            schemas[inp]["x-ticvai-record-definition"] = rd
        body = inp

    new = {}
    # Everything already decided is copied across untouched.
    for k in ("operationId", "x-ticvai-consumed-by", "x-ticvai-audience", "x-ticvai-provisional",
              "summary"):
        if k in op:
            new[k] = op[k]
    new["description"] = DERIVED_NOTE % {
        "module": rec["module"], "page": rec["page"],
        "purpose": (rec.get("purpose") or rec["title"]).strip(),
        "nprops": len(props), "ndropped": shape["dropped"],
        "persist": "a projection, not a table" if verb_is_read else "a request, not a table",
    }
    new["tags"] = op.get("tags") or ["drafted"]
    for k in ("x-ticvai-permission", "x-ticvai-scope-level", "x-ticvai-config-scope",
              "x-ticvai-offline-capable", "x-ticvai-conflict-policy", "x-ticvai-read-routing"):
        if k in op:
            new[k] = op[k]

    if verb_is_read and shape["query"]:
        # `Filter by` and `Search by` are the pack telling us what the list is narrowed on.
        new["parameters"] = [
            {"name": q, "in": "query", "required": False, "schema": {"type": s.get("type", "string")},
             "description": s.get("description", q)}
            for q, s in list(shape["query"].items())[:MAX_QUERY]
        ]
    if body:
        new["requestBody"] = {"required": True, "content": {
            "application/json": {"schema": {"$ref": "#/components/schemas/%s" % body}}}}

    ref = {"$ref": "#/components/schemas/%s" % view}
    new["responses"] = {"200": {
        "description": rec["title"],
        "content": {"application/json": {
            "schema": {"type": "array", "items": ref} if verb_is_read else ref}}}}
    return new, schemas


# -- writing ------------------------------------------------------------------------------------
class NoAlias(yaml.SafeDumper):
    """Emit no anchors.

    **A repeated object becomes `&id001` / `*id001`, and the contracts already use that name.**
    Two schemas sharing a property dict is enough to trigger it, and the collision made the whole
    file unloadable. Every value here is small; writing it out in full costs nothing.
    """

    def ignore_aliases(self, data):
        return True

    def increase_indent(self, flow=False, indentless=False):
        """Indent sequence items under their key, the way the rest of the package writes them.

        **PyYAML's default puts list items at the parent's indent**, and
        `link-screens-contracts.py` looks for `x-ticvai-consumed-by` written the package's way. It
        did not recognise the flat form, re-added its own, and every one of the 577 drafted
        operations ended up with the key twice - which YAML resolves by silently keeping the last.
        """
        return super(NoAlias, self).increase_indent(flow, False)


def dump(node):
    return yaml.dump(node, Dumper=NoAlias, sort_keys=False, allow_unicode=True, width=98,
                     default_flow_style=False)


def indent(block: str, spaces: int) -> str:
    pad = " " * spaces
    return "".join((pad + l if l.strip() else l) + "\n" for l in block.rstrip("\n").split("\n"))


def rewrite(path: Path, ops: dict, schemas: dict, apply: bool) -> str:
    text = io.open(path, encoding="utf-8").read()
    lines = text.split("\n")
    comp = next(i for i, l in enumerate(lines) if l.startswith("components:"))
    starts = [i for i, l in enumerate(lines[:comp]) if re.match(r"^  /\S*:\s*$", l)]
    first = next(i for i in starts
                 if "x-ticvai-provisional: true" in "\n".join(
                     lines[i:next((j for j in starts if j > i), comp)]))

    paths_block = indent(dump(ops), 2)
    schema_block = indent(dump(schemas), 4)

    # **The new schemas go at the end of `schemas:`, not before `securitySchemes:`.**
    # `approvals.yaml` orders the two the other way round, and anchoring on the security block put
    # schema definitions directly under `components:` where nothing could parse them.
    tail_lines = lines[comp:]
    s0 = next(i for i, l in enumerate(tail_lines) if re.match(r"^  schemas:\s*$", l))
    s1 = next((i for i in range(s0 + 1, len(tail_lines))
               if tail_lines[i].strip() and not tail_lines[i].startswith("    ")), len(tail_lines))
    # **Drop the previous generation first.** Appending without removing would leave the old
    # schemas behind on every re-run, orphaned and still counted.
    kept, entry = [], []
    for l in tail_lines[s0 + 1:s1]:
        if re.match(r"^    \S.*:\s*$", l):
            if entry and MARK not in "\n".join(entry):
                kept += entry
            entry = [l]
        else:
            entry.append(l)
    if entry and MARK not in "\n".join(entry):
        kept += entry
    tail_lines = tail_lines[:s0 + 1] + kept + tail_lines[s1:]
    s1 = s0 + 1 + len(kept)
    tail = "\n".join(tail_lines[:s1] + [schema_block.rstrip("\n")] + tail_lines[s1:])
    out = "\n".join(lines[:first]) + "\n" + paths_block + tail
    yaml.safe_load(out)                       # never write a file that will not parse
    if apply:
        io.open(path, "w", encoding="utf-8", newline="\n").write(out)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="one contract stem, to prove it on the smallest first")
    ap.add_argument("--entities", action="store_true",
                    help="report which entities the drafted WRITES configure, and act on none")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    scr, pack, taken = screens_by_id(), pack_by_key(), existing_schema_names()
    cols, owned = ddl_columns(), owned_schemas()
    entities = collections.defaultdict(list)
    total_ops = total_schemas = unjoined = 0

    for path in sorted((ROOT / "contracts").rglob("*.yaml")):
        if a.only and path.stem != a.only:
            continue
        doc = yaml.safe_load(io.open(path, encoding="utf-8").read()) or {}
        drafted, schemas = {}, {}
        for route, item in (doc.get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if not isinstance(op, dict) or not op.get("x-ticvai-provisional"):
                    continue
                cb = (op.get("x-ticvai-consumed-by") or [""])[0]
                m = re.match(r"\S+\s+(\S+)\s", cb)
                s = scr.get(m.group(1)) if m else None
                src = (s or {}).get("source") or {}
                rec = pack.get((src.get("pack"), str(src.get("board")), str(src.get("number"))))
                if not rec:
                    unjoined += 1
                    continue
                base = pascal(rec["title"])[:52] or pascal(op["operationId"])
                name, k = base, 2
                while (name + "View") in taken:
                    name, k = "%s%d" % (base, k), k + 1
                taken.add(name + "View")
                taken.add(name + "Input")
                new, sch = build(op, rec, name, path.stem, owned[path.stem], cols)
                drafted.setdefault(route, {})[verb] = new
                schemas.update(sch)
                if not op["operationId"].startswith(("list", "get", "search")):
                    entities[entity_of(rec["title"])].append(
                        (path.stem, op["operationId"], rec["title"]))
        if not drafted:
            continue
        rewrite(path, drafted, schemas, a.apply)
        total_ops += sum(len(v) for v in drafted.values())
        total_schemas += len(schemas)
        print("  %-22s %4d operations  %4d schemas" % (path.name, sum(len(v) for v in
                                                                      drafted.values()),
                                                       len(schemas)))

    print("%d operations shaped, %d schemas written%s"
          % (total_ops, total_schemas, "" if a.apply else "  (dry run - pass --apply)"))
    if unjoined:
        print("  %d drafted operations could not be joined to a pack record" % unjoined)

    if a.entities:
        print("\nEntities the drafted WRITES configure - the table question, grouped:")
        for ent, rows in sorted(entities.items(), key=lambda kv: -len(kv[1])):
            print("  %-30s %2d  %s" % (ent, len(rows), ", ".join(r[1] for r in rows)[:70]))
    return 0


STOP = {"and", "or", "the", "a", "of", "for", "management", "configuration", "settings", "setup",
        "builder", "center", "centre", "command", "console", "dashboard", "screen", "engine",
        "rules", "rule", "control", "controls", "designer", "editor", "manager", "panel"}


def entity_of(title: str) -> str:
    """The principal noun a configuration screen configures - `Access Area & Zone Builder` -> zone.

    Used only by `--entities`, to group the drafted writes so the table question is asked once per
    entity instead of once per screen.
    """
    toks = [t.lower() for t in re.split(r"[^A-Za-z]+", title) if t and t.lower() not in STOP]
    return " ".join(toks[-2:]) if toks else title.lower()


if __name__ == "__main__":
    sys.exit(main())
