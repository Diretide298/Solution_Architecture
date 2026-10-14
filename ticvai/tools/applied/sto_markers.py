#!/usr/bin/env python3
"""Line-level `x-ticvai-*` marker edits to the contracts, for the Block A storage audit (batch STO, 14 October 2026).

A round trip through a YAML library rewrites thousands of hand-authored lines, so a marker is inserted as one line
under the property it speaks for (or replaced where the property already carries it), and each file is parsed after
the edits to prove it still loads with no key twice. The line endings the file has are kept.

    Contracts(root)                  the contract files, read once, written by save()
    .find_prop(stem, schema, path)   (file, line index, indent) of a property; `path` is `prop` or `arr[].leaf`,
                                     followed through `allOf`, `items` and local `$ref`s to where it is written
    .set_marker(stem, schema, path, key, value)     add or replace `key: value` on the property
    .set_schema_marker(stem, schema, key, value)    add or replace `key: value` on the schema itself
    .add_required(stem, schema, prop)               add a name to the schema's own `required:` list
    .save()                                         write every changed file, after parsing it
"""
from __future__ import annotations

import io
import re
from pathlib import Path

import yaml


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _span(lines, start, base):
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or _indent(lines[end]) > base
                                or lines[end].lstrip().startswith("#") and _indent(lines[end]) > base):
        end += 1
    return end


class Contracts:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.files = {}
        for f in sorted((self.root / "contracts").glob("*/*.yaml")):
            raw = io.open(f, encoding="utf-8", newline="").read()
            nl = "\r\n" if "\r\n" in raw else "\n"
            self.files[f.stem] = {"path": f, "nl": nl, "lines": raw.split(nl), "dirty": False,
                                  "doc": yaml.load(raw, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))}

    # ---- locating -----------------------------------------------------------------------------------
    def schema_span(self, stem, schema):
        lines = self.files[stem]["lines"]
        key = "    %s:" % schema
        hits = [i for i, l in enumerate(lines) if l.rstrip() == key or l.startswith(key + " ")]
        if len(hits) != 1:
            raise LookupError("%s.%s: %d schema lines" % (stem, schema, len(hits)))
        return hits[0], _span(lines, hits[0], 4)

    def _schema(self, stem, name):
        return ((self.files[stem]["doc"].get("components") or {}).get("schemas") or {}).get(name)

    def _owner(self, stem, schema, prop, depth=0):
        """(stem, schema) whose own text carries `prop`: the schema, or one it includes through `allOf`."""
        s = self._schema(stem, schema)
        if not isinstance(s, dict) or depth > 6:
            return None
        if prop in (s.get("properties") or {}):
            return stem, schema
        for part in s.get("allOf") or []:
            if not isinstance(part, dict):
                continue
            if prop in (part.get("properties") or {}):
                return stem, schema
            ref = str(part.get("$ref") or "")
            m = re.match(r"^(?:(?:\.\./)?(?:[\w-]+/)?([\w-]+)\.yaml)?#/components/schemas/(\w+)$", ref)
            if m:
                hit = self._owner(m.group(1) or stem, m.group(2), prop, depth + 1)
                if hit:
                    return hit
        return None

    def _prop_line(self, lines, s, e, prop, min_indent=8):
        """The line of `prop:` directly under a `properties:` inside lines[s:e] (the shallowest)."""
        best = None
        for i in range(s + 1, e):
            l = lines[i]
            m = re.match(r"^(\s+)(['\"]?)" + re.escape(prop) + r"\2:(\s|$)", l)
            if not m or _indent(l) < min_indent:
                continue
            ind = _indent(l)
            j = i - 1
            while j > s and (not lines[j].strip() or _indent(lines[j]) >= ind):
                j -= 1
            if lines[j].strip() == "properties:" and _indent(lines[j]) == ind - 2:
                if best is None or ind < _indent(lines[best]):
                    best = i
        return best

    def find_prop(self, stem, schema, path):
        parts = path.split("[].")
        cur_stem, cur_schema = stem, schema
        own = self._owner(cur_stem, cur_schema, parts[0])
        if not own:
            raise LookupError("%s.%s: no property %s" % (stem, schema, parts[0]))
        cur_stem, cur_schema = own
        lines = self.files[cur_stem]["lines"]
        s, e = self.schema_span(cur_stem, cur_schema)
        i = self._prop_line(lines, s, e, parts[0])
        if i is None:
            raise LookupError("%s.%s: property %s not found in text" % (cur_stem, cur_schema, parts[0]))
        for leaf in parts[1:]:
            ind = _indent(lines[i])
            pe = _span(lines, i, ind)
            it = next((k for k in range(i + 1, pe) if lines[k].strip().startswith("items:")
                       and _indent(lines[k]) == ind + 2), None)
            if it is None:
                raise LookupError("%s.%s.%s: no items" % (cur_stem, cur_schema, path))
            ie = _span(lines, it, ind + 2)
            inline = self._prop_line(lines, it, ie, leaf, min_indent=ind + 6)
            if inline is not None:
                i = inline
                continue
            own = None
            for k in range(it, ie):           # `items: {$ref}`, `items:\n $ref`, or `items:\n allOf:\n - $ref`
                ref = re.search(r"\$ref:\s*['\"]?([^'\"\s}]+)", lines[k])
                if not ref:
                    continue
                m = re.match(r"^(?:(?:\.\./)?(?:[\w-]+/)?([\w-]+)\.yaml)?#/components/schemas/(\w+)$", ref.group(1))
                own = self._owner(m.group(1) or cur_stem, m.group(2), leaf) if m else None
                if own:
                    break
            if not own:
                raise LookupError("%s.%s.%s: leaf %s not found" % (cur_stem, cur_schema, path, leaf))
            cur_stem, cur_schema = own
            lines = self.files[cur_stem]["lines"]
            s, e = self.schema_span(cur_stem, cur_schema)
            i = self._prop_line(lines, s, e, leaf)
            if i is None:
                raise LookupError("%s.%s: property %s not found in text" % (cur_stem, cur_schema, leaf))
        return cur_stem, cur_schema, i

    # ---- editing ------------------------------------------------------------------------------------
    def _set(self, stem, i, key, value):
        """Add or replace `key: value` on the mapping whose key line is lines[i]."""
        f = self.files[stem]
        lines = f["lines"]
        line = lines[i]
        ind = _indent(line)
        val = value if isinstance(value, str) else ("true" if value is True else "false" if value is False
                                                     else str(value))
        m = re.match(r"^(\s+\S+:\s*)\{(.*)\}\s*$", line)
        if m:                                          # a flow mapping on one line
            body = m.group(2)
            if re.search(r"(^|,)\s*" + re.escape(key) + r"\s*:", body):
                new = re.sub(r"((?:^|,)\s*" + re.escape(key) + r"\s*:\s*)([^,]*?)(\s*)(?=,|$)",
                             lambda x: x.group(1) + val + x.group(3), body)
                if new == body:
                    return "="
                lines[i] = "%s{%s}" % (m.group(1), new)
            else:
                pad = " " if body.endswith(" ") else ""
                lines[i] = "%s{%s, %s: %s%s}" % (m.group(1), body.rstrip(), key, val, pad)
            f["dirty"] = True
            return "+"
        if line.rstrip().endswith(":") is False and not re.match(r"^\s+\S+:\s*(#.*)?$", line):
            raise ValueError("%s line %d is not a mapping key: %r" % (stem, i + 1, line))
        e = _span(lines, i, ind)
        for k in range(i + 1, e):
            if _indent(lines[k]) == ind + 2 and re.match(r"^\s+" + re.escape(key) + r":", lines[k]):
                ke = _span(lines, k, ind + 2)
                new = " " * (ind + 2) + "%s: %s" % (key, val)
                if lines[k:ke] == [new]:
                    return "="
                lines[k:ke] = [new]
                f["dirty"] = True
                return "~"
        lines.insert(i + 1, " " * (ind + 2) + "%s: %s" % (key, val))
        f["dirty"] = True
        return "+"

    def set_marker(self, stem, schema, path, key, value):
        st, sc, i = self.find_prop(stem, schema, path)
        return self._set(st, i, key, value), "%s.%s" % (st, sc)

    def set_schema_marker(self, stem, schema, key, value):
        s, _e = self.schema_span(stem, schema)
        return self._set(stem, s, key, value)

    def add_retired(self, stem, schema, column):
        """Add a column name to the schema's `x-ticvai-retired-columns` (kept as a flow list), keeping any already there."""
        f = self.files[stem]
        lines = f["lines"]
        s, e = self.schema_span(stem, schema)
        k = next((i for i in range(s + 1, e) if _indent(lines[i]) == 6
                  and lines[i].lstrip().startswith("x-ticvai-retired-columns:")), None)
        if k is None:
            lines.insert(s + 1, "      x-ticvai-retired-columns: [%s]" % column)
            f["dirty"] = True
            return "+"
        ke = _span(lines, k, 6)
        have = []
        m = re.match(r"^\s+x-ticvai-retired-columns:\s*\[(.*)\]\s*$", lines[k])
        if m:
            have = [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
        else:
            k2 = k + 1
            while k2 < len(lines) and lines[k2].strip().startswith("- ") and _indent(lines[k2]) >= 6:
                have.append(lines[k2].strip()[2:].strip().strip("'\""))
                k2 += 1
            ke = k2
        if column in have:
            return "="
        lines[k:ke] = ["      x-ticvai-retired-columns: [%s]" % ", ".join(have + [column])]
        f["dirty"] = True
        return "+"

    def add_required(self, stem, schema, prop):
        f = self.files[stem]
        lines = f["lines"]
        s, e = self.schema_span(stem, schema)
        r = next((i for i in range(s + 1, e) if lines[i].rstrip() == "      required:"), None)
        if r is None:
            r = next((i for i in range(s + 1, e) if re.match(r"^      required:\s*\[", lines[i])), None)
            if r is not None:
                names = [x.strip().strip("'\"") for x in lines[r].split("[", 1)[1].rsplit("]", 1)[0].split(",") if x.strip()]
                if prop in names:
                    return "="
                lines[r] = "      required: [%s]" % ", ".join(names + [prop])
                f["dirty"] = True
                return "+"
            p = next(i for i in range(s + 1, e) if lines[i].rstrip() == "      properties:")
            lines[p:p] = ["      required:", "      - %s" % prop]
            f["dirty"] = True
            return "+"
        items, k = [], r + 1
        while k < len(lines) and lines[k].strip().startswith("- ") and _indent(lines[k]) >= 6:
            items.append(k)
            k += 1
        if any(lines[i].strip()[2:].strip().strip("'\"") == prop for i in items):
            return "="
        ind = _indent(lines[items[0]]) if items else 6
        at = (items[-1] + 1) if items else r + 1
        lines.insert(at, " " * ind + "- %s" % prop)
        f["dirty"] = True
        return "+"

    def replace_in_schema(self, stem, schema, old, new):
        """One exact replacement of `old` (lines joined by \\n) inside the schema's text; "=" when `new` is there."""
        f = self.files[stem]
        lines = f["lines"]
        s, e = self.schema_span(stem, schema)
        seg = "\n".join(lines[s:e])
        if new and new in seg and (old not in seg or old in new):
            return "="
        if seg.count(old) != 1:
            raise LookupError("%s.%s: %r found %d times" % (stem, schema, old[:70], seg.count(old)))
        lines[s:e] = seg.replace(old, new).split("\n")
        f["dirty"] = True
        return "~"

    def replace_in_op(self, stem, op_id, old, new):
        """One exact replacement inside an operation's text (from its method line to the next sibling)."""
        f = self.files[stem]
        lines = f["lines"]
        hits = [i for i, l in enumerate(lines) if l.strip() == "operationId: %s" % op_id]
        if len(hits) != 1:
            raise LookupError("operation %s: %d matches in %s" % (op_id, len(hits), stem))
        k = hits[0]
        ind = _indent(lines[k]) - 2
        s = k
        while _indent(lines[s]) != ind or not lines[s].strip():
            s -= 1
        e = _span(lines, s, ind)
        seg = "\n".join(lines[s:e])
        if new and new in seg and (old not in seg or old in new):
            return "="
        if seg.count(old) != 1:
            raise LookupError("%s: %r found %d times" % (op_id, old[:70], seg.count(old)))
        lines[s:e] = seg.replace(old, new).split("\n")
        f["dirty"] = True
        return "~"

    def add_property(self, stem, schema, name, block):
        """Append property `name` (its body as YAML text, indented as under the property) to the schema's own
        `properties:` (the shallowest one in its text); "=" when the schema already has it."""
        f = self.files[stem]
        lines = f["lines"]
        s, e = self.schema_span(stem, schema)
        props = [i for i in range(s + 1, e) if lines[i].strip() == "properties:"]
        if not props:
            raise LookupError("%s.%s: no properties" % (stem, schema))
        p = min(props, key=lambda i: _indent(lines[i]))
        ind = _indent(lines[p]) + 2
        pe = _span(lines, p, _indent(lines[p]))
        if any(re.match(r"^\s{%d}%s:" % (ind, re.escape(name)), lines[i]) for i in range(p + 1, pe)):
            return "="
        while pe > p + 1 and not lines[pe - 1].strip():
            pe -= 1
        body = [" " * (ind + 2) + l if l.strip() else "" for l in block.strip("\n").split("\n")]
        lines[pe:pe] = [" " * ind + name + ":"] + body
        f["dirty"] = True
        return "+"

    def op_span(self, stem, op_id):
        lines = self.files[stem]["lines"]
        hits = [i for i, l in enumerate(lines) if l.strip() == "operationId: %s" % op_id]
        if len(hits) != 1:
            raise LookupError("operation %s: %d matches in %s" % (op_id, len(hits), stem))
        k = hits[0]
        ind = _indent(lines[k]) - 2
        s = k
        while _indent(lines[s]) != ind or not lines[s].strip():
            s -= 1
        return s, _span(lines, s, ind)

    def set_body_marker(self, stem, op_id, prop, key, value):
        """`key: value` on a property of an operation's inline request body (the first `prop:` after requestBody)."""
        lines = self.files[stem]["lines"]
        s, e = self.op_span(stem, op_id)
        rb = next((i for i in range(s, e) if lines[i].strip() == "requestBody:"), None)
        if rb is None:
            raise LookupError("%s: no requestBody" % op_id)
        rbe = _span(lines, rb, _indent(lines[rb]))
        hits = [i for i in range(rb, rbe) if re.match(r"^\s+" + re.escape(prop) + r":(\s|$)", lines[i])]
        if not hits:
            raise LookupError("%s: no body property %s" % (op_id, prop))
        i = min(hits, key=lambda k: (_indent(lines[k]), k))     # the body's own field, not a nested one's
        return self._set(stem, i, key, value)

    def replace_text(self, stem, old, new):
        """One exact replacement anywhere in the file."""
        f = self.files[stem]
        text = "\n".join(f["lines"])
        if new and new in text and (old not in text or old in new):
            return "="
        if text.count(old) != 1:
            raise LookupError("%s: %r found %d times" % (stem, old[:70], text.count(old)))
        f["lines"] = text.replace(old, new).split("\n")
        f["dirty"] = True
        return "~"

    def save(self):
        from ruamel.yaml import YAML
        out = []
        for stem, f in self.files.items():
            if not f["dirty"]:
                continue
            text = f["nl"].join(f["lines"])
            yaml.load(text, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
            YAML(typ="safe").load(text)
            io.open(f["path"], "w", encoding="utf-8", newline="").write(text)
            f["dirty"] = False
            out.append(stem)
        return out
