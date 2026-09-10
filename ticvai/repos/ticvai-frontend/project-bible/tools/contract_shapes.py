#!/usr/bin/env python3
"""Read operations and response shapes out of the contracts, once, for every generator.

Two tools rebuild screens — `generate-screens-from-pack.py` for the 590 screens a workshop pack
describes, and `generate-screens-from-contracts.py` for the 501 it does not — and both need the
same three answers: what operations exist, what a given operation returns, and what fields that
shape has. **Two copies of that logic is two places for the pagination bug to live**, and it lived
in one of them for a day already.

## The pagination envelope is not the row

Every list response in this package is shaped

    allOf:
      - $ref: '.../Page'                       # items, nextCursor, hasMore
      - properties: { items: { items: { $ref: '#/.../Promotion' } } }

so taking the first `$ref` in the document returns `Page`, and a queue of approval requests binds
to a schema whose only properties are `items`, `nextCursor` and `hasMore`. That went unnoticed
because it is uniform: **every list operation was wrong in the same way**, so nothing looked odd
next to anything else. `response_schemas` returns the element type first.

## One level deep, deliberately

`schema_fields` merges `allOf` branches and reads properties one level down. **A checker that
half-resolves a `$ref` reports a real field as missing, and a wrong failure is worse than a missing
one** because somebody deletes the binding to make it pass.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

REF = re.compile(r"#/components/schemas/(\w+)")

# Wrappers, not subjects. A response that carries only one of these is a response whose element
# type was never declared, which is a finding rather than a binding.
ENVELOPES = {"Page", "Paged", "Cursor", "PageMeta", "Envelope"}


def load_contracts(root: Path) -> tuple[dict, dict]:
    """`(operations by operationId, schemas by name)` across every contract file."""
    ops, schemas = {}, {}
    for f in sorted((root / "contracts").rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — an unreadable contract is check-package's business
            continue
        if not isinstance(doc, dict):
            continue
        for name, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            if isinstance(body, dict):
                schemas.setdefault(name, body)
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for method, op in item.items():
                if isinstance(op, dict) and "operationId" in op:
                    ops[op["operationId"]] = {"file": f.name, "path": path, "method": method,
                                              "op": op}
    return ops, schemas


def response_schemas(op: dict) -> list[str]:
    """Schema names a success response carries, **element type before envelope**."""
    responses = op.get("responses") or {}
    for code in ("200", "201", "default"):
        for body in ((responses.get(code) or {}).get("content") or {}).values():
            schema = body.get("schema") or {}
            for branch in [schema] + (schema.get("allOf") or []):
                if not isinstance(branch, dict):
                    continue
                items = ((branch.get("properties") or {}).get("items") or {}).get("items") or {}
                if found := REF.findall(json.dumps(items)):
                    return found
            found = REF.findall(json.dumps(schema))
            ranked = ([f for f in found if f not in ENVELOPES]
                      + [f for f in found if f in ENVELOPES])
            if ranked:
                return ranked
    return []


def schema_fields(name: str, schemas: dict) -> dict:
    """`{property: body}` for one schema, with `allOf` branches merged. One level, no deeper."""
    body = schemas.get(name)
    if not isinstance(body, dict):
        return {}
    props = dict(body.get("properties") or {})
    for branch in body.get("allOf") or []:
        if isinstance(branch, dict):
            props.update(branch.get("properties") or {})
            for ref in REF.findall(json.dumps(branch.get("$ref") or "")):
                props.update((schemas.get(ref) or {}).get("properties") or {})
    return props


def path_params(op_entry: dict) -> list[str]:
    """Path parameters an operation requires — what the screen must arrive holding."""
    return re.findall(r"\{(\w+)\}", op_entry.get("path", ""))


def is_write(operation_id: str) -> bool:
    return not str(operation_id).startswith(("list", "get", "search", "export", "simulate",
                                             "preview", "validate"))
