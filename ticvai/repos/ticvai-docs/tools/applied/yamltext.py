#!/usr/bin/env python3
"""Text edits to a contract YAML that keep every other line as it is (4 October 2026, CHG-FXC).

A round trip through a YAML library rewrites thousands of lines of a hand-authored contract (folded
descriptions, quoting, wrapping), so the one-offs that change a contract insert and replace text instead,
anchored on a schema's or an operation's own lines, and the file is parsed afterwards to prove it still loads.

    add_props(path, schema, block)            properties appended to a component schema
    replace_in_schema(path, schema, old, new) one exact replacement inside a schema
    replace_in_op(path, operation_id, old, new)
    insert_after_in_op(path, operation_id, anchor, block)
    add_schema_after(path, existing, block)   a new component schema after an existing one
"""
from __future__ import annotations

import io
import textwrap

import yaml


def _read(path):
    return io.open(path, encoding="utf-8").read().split("\n")


def _write(path, lines):
    text = "\n".join(lines)
    yaml.load(text, Loader=yaml.CSafeLoader)  # still a contract
    from ruamel.yaml import YAML  # and no key twice: PyYAML keeps the last of two silently
    YAML(typ="safe").load(text)
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _span(lines, start, base):
    """From `start` to the first later non-blank line indented at or above `base`."""
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or _indent(lines[end]) > base):
        end += 1
    return end


def schema_span(lines, name):
    key = "    %s:" % name
    hits = [i for i, l in enumerate(lines) if l == key]
    if len(hits) != 1:
        raise SystemExit("schema %s: %d matches" % (name, len(hits)))
    return hits[0], _span(lines, hits[0], 4)


def op_span(lines, op_id):
    hits = [i for i, l in enumerate(lines) if l.strip() == "operationId: %s" % op_id]
    if len(hits) != 1:
        raise SystemExit("operation %s: %d matches" % (op_id, len(hits)))
    i = hits[0]
    ind = _indent(lines[i]) - 2
    s = i
    while _indent(lines[s]) != ind or not lines[s].strip():
        s -= 1
    return s, _span(lines, s, ind)


def _block(text, indent):
    return [(" " * indent + l) if l.strip() else "" for l in textwrap.dedent(text).strip("\n").split("\n")]


def add_props(path, schema, text):
    lines = _read(path)
    s, e = schema_span(lines, schema)
    p = next((i for i in range(s, e) if lines[i] == "      properties:"), None)
    if p is None:
        raise SystemExit("schema %s has no top-level properties" % schema)
    pe = _span(lines, p, 6)
    new = _block(text, 8)
    names = {l.strip()[:-1] for l in new if _indent(l) == 8 and l.rstrip().endswith(":")}
    have = {lines[i].strip()[:-1] for i in range(p + 1, pe) if _indent(lines[i]) == 8 and lines[i].rstrip().endswith(":")}
    if names & have:
        return False
    while pe > p + 1 and not lines[pe - 1].strip():
        pe -= 1
    lines[pe:pe] = new
    _write(path, lines)
    return True


def _replace_span(path, span_fn, key, old, new):
    lines = _read(path)
    s, e = span_fn(lines, key)
    seg = "\n".join(lines[s:e])
    if new in seg:
        return False
    if seg.count(old) != 1:
        raise SystemExit("%s: %r found %d times" % (key, old[:60], seg.count(old)))
    lines[s:e] = seg.replace(old, new).split("\n")
    _write(path, lines)
    return True


def replace_in_schema(path, schema, old, new):
    return _replace_span(path, schema_span, schema, old, new)


def replace_in_op(path, op_id, old, new):
    return _replace_span(path, op_span, op_id, old, new)


def insert_after_in_op(path, op_id, anchor, text, indent):
    lines = _read(path)
    s, e = op_span(lines, op_id)
    block = _block(text, indent)
    if "\n".join(block).strip() in "\n".join(lines[s:e]):
        return False
    hits = [i for i in range(s, e) if lines[i].strip() == anchor.strip() and _indent(lines[i]) == _indent(anchor)]
    if len(hits) != 1:
        raise SystemExit("%s: anchor %r found %d times" % (op_id, anchor, len(hits)))
    at = _span(lines, hits[0], _indent(lines[hits[0]]))
    lines[at:at] = block
    _write(path, lines)
    return True


def add_schema_after(path, existing, text):
    lines = _read(path)
    block = _block(text, 4)
    if block[0] in lines:
        return False
    s, e = schema_span(lines, existing)
    lines[e:e] = block
    _write(path, lines)
    return True


def _append_desc(lines, s, e, ind, text, marker):
    """Append a paragraph to the `description:` at indent `ind` within lines[s:e]; rewritten as a `|-` block."""
    hits = [i for i in range(s, e) if _indent(lines[i]) == ind and lines[i].lstrip().startswith("description:")]
    if not hits:
        at = s + 1
        lines[at:at] = [" " * ind + "description: |-"] + [" " * (ind + 2) + l if l else "" for l in text.split("\n")]
        return True
    i = hits[0]
    j = _span(lines, i, ind)
    old = yaml.load("\n".join(l[ind:] if l.strip() else "" for l in lines[i:j]), Loader=yaml.CSafeLoader)["description"] or ""
    if marker and marker in old:
        return False
    new = old.rstrip("\n") + "\n\n" + text.strip("\n")
    lines[i:j] = [" " * ind + "description: |-"] + [(" " * (ind + 2) + l) if l.strip() else "" for l in new.split("\n")]
    return True


def append_op_description(path, op_id, text, marker=None):
    lines = _read(path)
    s, e = op_span(lines, op_id)
    ind = _indent(lines[s]) + 2
    if _append_desc(lines, s, e, ind, textwrap.dedent(text).strip("\n"), marker):
        _write(path, lines)
        return True
    return False


def append_schema_description(path, schema, text, marker=None):
    lines = _read(path)
    s, e = schema_span(lines, schema)
    if _append_desc(lines, s, e, 6, textwrap.dedent(text).strip("\n"), marker):
        _write(path, lines)
        return True
    return False


def append_prop_description(path, schema, prop, text, marker=None, depth_path=None):
    """Append to the description of a property; `depth_path` lists nested keys below the property
    (e.g. ["items", "properties", "check"]) to reach a nested property."""
    lines = _read(path)
    s, e = schema_span(lines, schema)
    p = next(i for i in range(s, e) if lines[i] == "      properties:")
    q = next(i for i in range(p, e) if lines[i] == " " * 8 + prop + ":")
    ind = 10
    qe = _span(lines, q, 8)
    for key in depth_path or []:
        q = next(i for i in range(q + 1, qe) if lines[i] == " " * ind + key + ":")
        qe = _span(lines, q, ind)
        ind += 2
    if _append_desc(lines, q + 1, qe, ind, textwrap.dedent(text).strip("\n"), marker):
        _write(path, lines)
        return True
    return False


def set_persistence(path, schema, value):
    """Replace a schema's `x-ticvai-persistence` (with its continuation lines) by `value`, single-quoted."""
    lines = _read(path)
    s, e = schema_span(lines, schema)
    i = next(i for i in range(s, e) if lines[i].startswith("      x-ticvai-persistence:"))
    j = _span(lines, i, 6)
    new = "      x-ticvai-persistence: '%s'" % value.replace("'", "''")
    if lines[i:j] == [new]:
        return False
    lines[i:j] = [new]
    _write(path, lines)
    return True
