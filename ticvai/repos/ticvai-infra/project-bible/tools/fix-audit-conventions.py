#!/usr/bin/env python3
"""Apply three package conventions to every operation that lacks them (audit R076, R142, R192).

check-package.py now checks each of them, and the audit found them half-applied:

  46  an operation taking PageCursor returns the shared Page envelope          (R076)
  48  every mutating operation takes IdempotencyKey (common.yaml: "required on
      every mutating request because offline clients replay their outbox")    (R142)
  49  every write the lineage says lands in Postgres declares X-Consistency-Token
      on a 2xx response (api-conventions 3)                                    (R192)

The decisions come from the parsed YAML and handoff/api-data-lineage.json, exactly as the checker
makes them; the edits are line insertions, so comments, CRLF and hand-authored layout survive.
Anything whose layout it does not recognise (a 2xx that is a $ref to a shared response, a flow-style
schema, an unexpected indent) is listed and left for a person rather than guessed at.

    python tools/fix-audit-conventions.py [--apply]
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
APPLY = "--apply" in sys.argv
MUTATING = ("post", "put", "patch", "delete")

lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
stores = {}
try:
    ref = json.loads((ROOT / "handoff" / "schema-reference.json").read_text(encoding="utf-8"))
    for t in ref.get("tables", []) if isinstance(ref, dict) else []:
        if isinstance(t, dict) and t.get("name"):
            stores[t["name"]] = t.get("store", "postgres")
except (OSError, ValueError):
    pass


def params_text(item, op):
    return str(item.get("parameters") or []) + str(op.get("parameters") or [])


def writes_postgres(oid):
    w = [t for t in (lineage.get(oid, {}).get("writes") or []) if not t.startswith(("cache:", "qdrant"))]
    return any(stores.get(t, "postgres") in ("postgres", "postgres-analytical") for t in w)


def block_end(lines, start, indent):
    """First line after `start` whose indent is <= indent (blank lines and comments do not end a block)."""
    i = start + 1
    while i < len(lines):
        s = lines[i]
        if s.strip() and not s.lstrip().startswith("#") and len(s) - len(s.lstrip(" ")) <= indent:
            return i
        i += 1
    return i


def indent_of(s):
    return len(s) - len(s.lstrip(" "))


tally = collections.Counter()
manual = []

for f in sorted((ROOT / "contracts").rglob("*.yaml")):
    raw = f.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    doc = yaml.safe_load(raw) or {}
    shared = "#/components" if f.parent.name == "shared" else "../shared/common.yaml#/components"
    lines = raw.split(eol)
    edits = []   # (line index, action, payload); applied bottom-up

    # locate each operation's block: path keys at indent 2 under `paths:`, methods at indent 4
    in_paths, path = False, None
    for i, s in enumerate(lines):
        if re.match(r"^paths:\s*$", s):
            in_paths = True
            continue
        if in_paths and s and not s.startswith(" ") and not s.startswith("#"):
            in_paths = False
        if not in_paths:
            continue
        m = re.match(r"^  (['\"]?)(/[^'\"]*)\1:\s*$", s)
        if m:
            path = m.group(2)
            continue
        m = re.match(r"^    (get|post|put|patch|delete):\s*$", s)
        if not (m and path):
            continue
        verb = m.group(1)
        item = (doc.get("paths") or {}).get(path) or {}
        op = item.get(verb) or {}
        oid = op.get("operationId")
        if not oid:
            continue
        end = block_end(lines, i, 4)
        resp_at = next((j for j in range(i + 1, end) if re.match(r"^      responses:\s*$", lines[j])), None)

        # 48 Idempotency-Key on every mutating operation
        if verb in MUTATING and not op.get("x-ticvai-idempotency-exempt") \
                and "IdempotencyKey" not in params_text(item, op) and "Idempotency-Key" not in params_text(item, op):
            pk = next((j for j in range(i + 1, end) if re.match(r"^      parameters:\s*$", lines[j])), None)
            if pk is not None:
                nxt = next((j for j in range(pk + 1, end) if lines[j].strip()), pk + 1)
                ind = indent_of(lines[nxt]) if lines[nxt].lstrip().startswith("-") else 8
                edits.append((pk + 1, "insert", [" " * ind + f"- $ref: '{shared}/parameters/IdempotencyKey'"]))
                tally["idempotency"] += 1
            elif resp_at is not None:
                edits.append((resp_at, "insert", ["      parameters:", f"        - $ref: '{shared}/parameters/IdempotencyKey'"]))
                tally["idempotency"] += 1
            else:
                manual.append(f"{f.stem}.{oid}: idempotency - no responses/parameters key at the expected indent")

        # 49 X-Consistency-Token on a 2xx of a Postgres write
        if verb in MUTATING and writes_postgres(oid) and resp_at is not None:
            rs = op.get("responses") or {}
            has = any(str(c).startswith("2") and ("X-Consistency-Token" in str((r or {}).get("headers"))
                                                 or "headers/ConsistencyToken" in str((r or {}).get("headers")))
                      for c, r in rs.items() if isinstance(r, dict))
            if not has:
                rend = block_end(lines, resp_at, 6)
                code_at = next((j for j in range(resp_at + 1, rend)
                                if re.match(r"^        ['\"]?2\d\d['\"]?:\s*$", lines[j])), None)
                if code_at is None:
                    manual.append(f"{f.stem}.{oid}: consistency token - no block-style 2xx response at indent 8")
                else:
                    cend = block_end(lines, code_at, 8)
                    first = next((lines[j] for j in range(code_at + 1, cend) if lines[j].strip()), "")
                    if first.strip().startswith("$ref"):
                        manual.append(f"{f.stem}.{oid}: consistency token - its 2xx is a $ref to a shared response")
                    else:
                        hk = next((j for j in range(code_at + 1, cend) if re.match(r"^          headers:\s*$", lines[j])), None)
                        hdr = ["            X-Consistency-Token:", f"              $ref: '{shared}/headers/ConsistencyToken'"]
                        edits.append((hk + 1, "insert", hdr) if hk is not None
                                     else (code_at + 1, "insert", ["          headers:"] + hdr))
                        tally["consistency"] += 1

        # 46 Page envelope for a cursor-paged list
        if "PageCursor" in params_text(item, op) and resp_at is not None:
            r200 = (op.get("responses") or {}).get("200") or (op.get("responses") or {}).get(200) or {}
            sch = ((r200.get("content") or {}).get("application/json") or {}).get("schema") if isinstance(r200, dict) else None
            local = sch
            if isinstance(sch, dict) and str(sch.get("$ref", "")).startswith("#/components/schemas/"):
                local = ((doc.get("components") or {}).get("schemas") or {}).get(sch["$ref"].rsplit("/", 1)[-1])
            if sch is not None and "components/schemas/Page" not in str(local) and "nextCursor" not in str(local):
                rend = block_end(lines, resp_at, 6)
                c200 = next((j for j in range(resp_at + 1, rend) if re.match(r"^        ['\"]?200['\"]?:\s*$", lines[j])), None)
                sat = next((j for j in range(c200 + 1, block_end(lines, c200, 8)) if re.match(r"^ +schema:\s*$", lines[j])), None) \
                    if c200 is not None else None
                if sat is None:
                    manual.append(f"{f.stem}.{oid}: page envelope - 200 schema is not block style")
                else:
                    s0 = indent_of(lines[sat])
                    send = block_end(lines, sat, s0)
                    body = [ln[s0 + 2:] if ln.strip() else "" for ln in lines[sat + 1:send]]
                    wrapped = [" " * (s0 + 2) + "allOf:",
                               " " * (s0 + 4) + f"- $ref: '{shared}/schemas/Page'",
                               " " * (s0 + 4) + "- type: object",
                               " " * (s0 + 6) + "properties:",
                               " " * (s0 + 8) + "items:"] + \
                              [(" " * (s0 + 10) + b) if b else "" for b in body]
                    edits.append((sat + 1, "replace", (send, wrapped)))
                    tally["page"] += 1

    if not edits:
        continue
    for at, action, payload in sorted(edits, key=lambda e: e[0], reverse=True):
        if action == "insert":
            lines[at:at] = payload
        else:
            stop, new = payload
            lines[at:stop] = new
    text = eol.join(lines)
    try:
        yaml.safe_load(text)
    except yaml.YAMLError as e:
        manual.append(f"{f.stem}: edits would not parse ({str(e).splitlines()[0]}); file left unchanged")
        continue
    if APPLY:
        f.write_bytes(text.encode("utf-8"))

print(f"idempotency keys added: {tally['idempotency']}; consistency tokens added: {tally['consistency']}; "
      f"page envelopes: {tally['page']}")
for m in manual:
    print("  left", m)
print(f"{len(manual)} left for a person" + ("" if APPLY else " (dry run - pass --apply)"))
