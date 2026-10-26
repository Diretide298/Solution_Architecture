#!/usr/bin/env python3
"""The default rulings for check-list-order and check-state-refusals, written into the contracts (r10, CHG-R10GEN-004,
CHG-R10GEN-005). For integration to run once on the merged tree, after the CR lanes, and only once the lead has
accepted the default rulings; a finding the lead rules otherwise goes in OVERRIDE (or is fixed by hand first).

  LO-NULLABLE-KEY         the operation's description gains: "Where `x` is null the row sorts after the rows that
                          have it (NULLS LAST), and `id` breaks every tie." (the default CR-236 recommended)
  LO-UNORDERED            the description gains an order on a key that cannot be null, the package's own phrases:
                          "Sorted by `name` ascending, then by `id`." where the items have a never-null name
                          (displayName, name, title, label, code, in that order), else "Newest first, by `createdAt`
                          descending, then by `id`.", else "Sorted by `id` descending (a UUIDv7, so newest first)."
  SR-TERMINAL-UNANSWERED  the 409's description gains: "Also refused when the <entity> is `a` or `b`; states/<model>
                          moves this call only from `c`." (the default: the state model is right)

SR-ALLOWS-NO-MOVE and SR-REFUSES-ALLOWED are not written: each needs the lead to say which side is right. They are
printed. Every finding is read from the checks at run time, so a second run writes nothing and a tree another lane
changed is read as it is. The contracts keep their own line endings.

    python tools/fix-order-and-refusals.py            # what it would write
    python tools/fix-order-and-refusals.py --apply
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_guard as g  # noqa: E402

TAG = "(r10 default ruling, CHG-R10GEN-004)"
TAG_SR = "(r10 default ruling, CHG-R10GEN-005)"
NAME_KEYS = ("displayName", "name", "title", "label", "code")
# A ruling the lead gave that is not the default: operationId -> the sentence to append instead.
OVERRIDE: dict = {}


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), TOOLS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_CRLF: dict = {}


def _read(path: Path) -> str:
    raw = path.read_bytes().decode("utf-8")
    _CRLF[path] = "\r\n" in raw
    return raw.replace("\r\n", "\n")


def _write(path: Path, text: str) -> None:
    if _CRLF.get(path):
        text = text.replace("\n", "\r\n")
    path.write_bytes(text.encode("utf-8"))


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def op_block(lines: list, op: str):
    """(start, end, indent) of the operation's mapping: every line at the operationId's indent or deeper around it."""
    i = next((n for n, l in enumerate(lines) if re.match(r"^\s+operationId:\s*%s\s*$" % re.escape(op), l)), None)
    if i is None:
        raise SystemExit(f"{op}: no such operationId")
    ind = _indent(lines[i])
    start = i
    while start > 0 and (not lines[start - 1].strip() or _indent(lines[start - 1]) >= ind):
        start -= 1
    while start < i and not lines[start].strip():
        start += 1
    end = i + 1
    while end < len(lines) and (not lines[end].strip() or _indent(lines[end]) >= ind):
        end += 1
    while end > i + 1 and not lines[end - 1].strip():
        end -= 1
    return start, end, ind


def _scalar_end(lines: list, k: int, col: int, quote: str):
    """(line, column) of the closing quote of a quoted scalar opening at lines[k][col]."""
    n, c = k, col + 1
    while n < len(lines):
        s = lines[n]
        while c < len(s):
            if quote == "'" and s[c] == "'":
                if c + 1 < len(s) and s[c + 1] == "'":
                    c += 2
                    continue
                return n, c
            if quote == '"':
                if s[c] == "\\":
                    c += 2
                    continue
                if s[c] == '"':
                    return n, c
            c += 1
        n, c = n + 1, 0
    raise SystemExit(f"unterminated {quote}-quoted scalar at line {k + 1}")


def append_to(lines: list, k: int, ind: int, key: str, sentence: str) -> None:
    """Appends `sentence` to the scalar of `key:` at lines[k] (indent `ind`), whatever its style."""
    head = lines[k]
    rest = head[ind + len(key) + 1:]
    v = rest.strip()
    col = ind + len(key) + 1 + (len(rest) - len(rest.lstrip()))
    if v[:1] in (">", "|"):
        end = k + 1
        while end < len(lines) and (not lines[end].strip() or _indent(lines[end]) > ind):
            end += 1
        while end > k + 1 and not lines[end - 1].strip():
            end -= 1
        body = [l for l in lines[k + 1:end] if l.strip()]
        cind = min(_indent(l) for l in body) if body else ind + 2
        lines[end:end] = ["", " " * cind + sentence] if body else [" " * cind + sentence]
    elif v[:1] in ("'", '"'):
        q = v[0]
        n, c = _scalar_end(lines, k, col, q)
        add = sentence.replace("'", "''") if q == "'" else sentence.replace("\\", "\\\\").replace('"', '\\"')
        lines[n] = lines[n][:c] + " " + add + lines[n][c:]
    elif v:
        if ": " in sentence or " #" in sentence:
            raise SystemExit(f"line {k + 1}: a plain {key} cannot take this sentence; write it by hand")
        end = k + 1
        while end < len(lines) and lines[end].strip() and _indent(lines[end]) > ind:
            end += 1
        lines[end - 1] = lines[end - 1].rstrip() + " " + sentence
    else:
        raise SystemExit(f"line {k + 1}: an empty {key}")


def add_description(text: str, op: str, sentence: str):
    """Appends `sentence` to the operation's description (or writes one after summary). Returns (text, changed)."""
    lines = text.split("\n")
    s, e, ind = op_block(lines, op)
    pre = " " * ind
    if any(sentence in l for l in lines[s:e]):
        return text, False
    k = next((n for n in range(s, e) if lines[n].startswith(pre + "description:")), None)
    if k is None:
        at = next((n for n in range(s, e) if lines[n].startswith(pre + "summary:")), None)
        at = (at if at is not None else next(n for n in range(s, e) if lines[n].startswith(pre + "operationId:")))
        at += 1
        while at < e and lines[at].strip() and _indent(lines[at]) > ind:
            at += 1
        lines[at:at] = [pre + "description: >-", pre + "  " + sentence]
    else:
        append_to(lines, k, ind, "description", sentence)
    return "\n".join(lines), True


def add_409(text: str, op: str, sentence: str):
    """Appends `sentence` to the description of the operation's inline 409. Returns (text, changed)."""
    lines = text.split("\n")
    s, e, ind = op_block(lines, op)
    if any(sentence in l for l in lines[s:e]):
        return text, False
    r = next((n for n in range(s, e) if re.match(r"^\s+'?409'?:", lines[n]) and _indent(lines[n]) > ind), None)
    if r is None:
        raise SystemExit(f"{op}: no inline 409")
    rind = _indent(lines[r])
    if "$ref" in lines[r] or "{" in lines[r]:
        raise SystemExit(f"{op}: its 409 is a $ref or a flow mapping; write the sentence by hand")
    k = next((n for n in range(r + 1, e) if lines[n].lstrip().startswith("description:")
              and _indent(lines[n]) > rind), None)
    if k is None or any(_indent(lines[n]) <= rind and lines[n].strip() for n in range(r + 1, k)):
        raise SystemExit(f"{op}: its 409 has no description")
    append_to(lines, k, _indent(lines[k]), "description", sentence)
    return "\n".join(lines), True


def tick_list(xs) -> str:
    xs = [f"`{x}`" for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " or " + xs[-1]


def unordered_sentence(item: dict, lo, docs, idoc, sname, stem, cols) -> str:
    props = item.get("properties") or {}
    for k in NAME_KEYS:
        if k in props:
            prop, _ = lo.resolve(props[k], idoc, docs)
            if not lo.can_be_null(k, item, prop or {}, cols.get(f"{stem}.{sname}.{k}", [])):
                return f"**Order.** Sorted by `{k}` ascending, then by `id`. {TAG}"
    if "createdAt" in props:
        return f"**Order.** Newest first, by `createdAt` descending, then by `id`. {TAG}"
    return f"**Order.** Sorted by `id` descending (a UUIDv7, so newest first). {TAG}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    lo, sr = _load("check-list-order"), _load("check-state-refusals")
    ops = g.operations()
    docs = {s: d for s, _, d in g.contracts()}
    cols = lo.column_index()
    texts: dict = {}

    def text(rel):
        if rel not in texts:
            texts[rel] = _read(ROOT / rel)
        return texts[rel]

    plan, ruling = [], []
    for rule, key, _msg in lo.findings():
        op = key.split(":")[0]
        if rule == "LO-NULLABLE-KEY":
            fld = key.split(":")[1]
            plan.append(("d", op, OVERRIDE.get(op) or f"Where `{fld}` is null the row sorts after the rows that have "
                                                      f"it (NULLS LAST), and `id` breaks every tie. {TAG}"))
        else:
            f = ops[op]
            _k, item, idoc, sname = lo.list_items(f["op"], docs[f["contract"]], docs)
            stem = next((s for s, d in docs.items() if d is idoc), f["contract"])
            plan.append(("d", op, OVERRIDE.get(op) or unordered_sentence(item, lo, docs, idoc, sname, stem, cols)))
    models = dict(sr.load_models())
    for rule, key, msg in sr.findings():
        mf, op = key.split(":")[:2]
        if rule != "SR-TERMINAL-UNANSWERED":
            ruling.append(f"  NEEDS A RULING {rule}: {msg}")
            continue
        m = models[mf + ".yaml"]
        f = ops[op]
        t409, types = sr.conflict_409(f["op"], docs[f["contract"]])
        r = sr.read_409(t409, types, sr.model_states(m))
        moves = sr.moves_from(m).get(op, set())
        frm = {x for x, _ in moves}
        left = sorted(sr.model_states(m) - r["covered"] - frm)
        ent = str(m.get("entity") or "record").lower()
        plan.append(("409", op, OVERRIDE.get(op) or f"Also refused when the {ent} is {tick_list(left)}; "
                                                    f"states/{mf}.yaml moves this call only from "
                                                    f"{tick_list(sorted(frm))}. {TAG_SR}"))
    n = 0
    for kind, op, sentence in plan:
        rel = ops[op]["file"]
        try:
            texts[rel], changed = (add_description if kind == "d" else add_409)(text(rel), op, sentence)
        except SystemExit as e:
            ruling.append(f"  BY HAND {op}: {e}")
            continue
        if changed:
            n += 1
            print(f"  {op}: {sentence}")
    for line in ruling:
        print(line)
    import yaml
    changed = []
    for rel, t in sorted(texts.items()):
        if t == _read(ROOT / rel):
            continue
        try:
            yaml.safe_load(t)
        except yaml.YAMLError as e:
            print(f"  NOT WRITTEN {rel}: the result does not parse ({str(e).splitlines()[0]})")
            continue
        changed.append(rel)
    print(f"{n} sentence(s) in {len(changed)} contract file(s)" + ("" if a.apply else " (nothing written, pass --apply)"))
    if a.apply:
        for rel in changed:
            _write(ROOT / rel, texts[rel])
    return 0


if __name__ == "__main__":
    sys.exit(main())
