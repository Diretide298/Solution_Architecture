#!/usr/bin/env python3
"""A form stops asking for a field its operation now marks readOnly (CHG-GT1-002, r6 gate, 14 October 2026).

**CHG-SHP-005 marked the server-owned fields of write bodies `readOnly: true`** (id, scopePath, a server-moved
status) on 97 declarations, and the screens' generated forms still listed them under Required / Optional and in
their discards: 71 overlays on 50 screens asked a person for the record's id or its scope path
(check-screen-patterns P1, CHG-SPF-001). This takes each such field out of the overlay's generated `body` lists and
its `dismiss.discards` and says the server sets it, exactly as the 3 October fix did
(tools/applied/spec-screen-patterns-3-october.py, fix_p1). Both are invisible metadata (check-approved-ui does not
compare an overlay's generated body or discards): no component, label, trigger or confirm changes.

**Line edits only.** Each overlay's `body` scalar is re-emitted in place at the width it was written with (proved by
re-emitting the old body first), each discarded field's list line is deleted, and nothing else in the file moves.
The file is parsed afterwards. A second run finds nothing to do.

    python tools/applied/gt1-overlays-stop-asking-readonly-14-october.py [--apply]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

TOOLS = Path(__file__).resolve().parents[1]
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import screen_patterns as sp  # noqa: E402

NOTE = ("Not asked, because the server sets {it} (readOnly in the contract since 14 October 2026, CHG-SHP-005): "
        "{fields} (CHG-GT1-002).")


def clean_lists(body: str, fields: set) -> str:
    """Take each `field` out of the body's Required: and Optional: lists (spec-screen-patterns-3-october strip_listed)."""
    def clean(seg: str) -> str:
        for f in sorted(fields):
            tok = r"`" + re.escape(f) + r"`(\s*\([^)]*\))?"
            seg = re.sub(tok + r",\s*", "", seg)
            seg = re.sub(r",?\s*(and\s+)?" + tok, "", seg)
        return seg
    m = re.search(r"(Required:)(.*?)(?=Optional:|Dismissing|$)", body, re.S)
    if m:
        seg = clean(m.group(2))
        if not re.search(r"`\w+`", seg):
            body = body[:m.start()] + "Nothing in the body is required. " + body[m.end():].lstrip()
        else:
            body = body[:m.start(2)] + seg + body[m.end(2):]
    m = re.search(r"(Optional:)(.*?)(?=Dismissing|$)", body, re.S)
    if m:
        seg = clean(m.group(2))
        if not re.search(r"`\w+`", seg):
            body = body[:m.start()] + body[m.end():].lstrip()
        else:
            body = body[:m.start(2)] + seg + body[m.end(2):]
    body = re.sub(r" +\.", ".", re.sub(r"  +", " ", body))
    return body.rstrip() + " " + NOTE.format(it="it" if len(fields) == 1 else "them",
                                              fields=", ".join(f"`{f}`" for f in sorted(fields)))


def indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def emit(key: str, value: str, ind: int, width: int) -> list:
    out = yaml.dump({key: value}, Dumper=yaml.SafeDumper, allow_unicode=True, width=width, sort_keys=False)
    lines = out.rstrip("\n").split("\n")
    return [" " * ind + lines[0]] + [" " * ind + ln if ln.strip() else ln for ln in lines[1:]]


def fix_file(path: Path, todo: dict, log: list) -> bool:
    """todo: {screen id: {overlay id: set(fields)}}"""
    raw = path.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(eol)
    starts = [i for i, l in enumerate(lines) if l.startswith("- id: ")]
    bounds = {}
    for k, i in enumerate(starts):
        sid = lines[i][6:].strip().strip("'\"")
        bounds[sid] = (i, starts[k + 1] if k + 1 < len(starts) else len(lines))
    edits = []                      # (start, end, new lines), applied bottom-up
    for sid, overlays in todo.items():
        s0, s1 = bounds[sid]
        for oid, fields in overlays.items():
            hits = [i for i in range(s0, s1) if re.match(r"^\s*- id: ['\"]?" + re.escape(oid) + r"['\"]?$", lines[i])]
            ov = None
            for i in hits:          # the overlay item, not a region or component of the same id
                j, ind_ = i - 1, indent(lines[i])
                while j > s0 and (not lines[j].strip() or indent(lines[j]) > ind_
                                  or (indent(lines[j]) == ind_ and lines[j].lstrip().startswith("- "))):
                    j -= 1
                if lines[j].strip() == "overlays:":
                    ov = i
            if ov is None:
                raise SystemExit(f"{sid} {oid}: overlay not found in {path.name}")
            item_ind = indent(lines[ov]) + 2         # the overlay's keys
            o1 = ov + 1
            while o1 < s1 and (not lines[o1].strip() or indent(lines[o1]) >= item_ind):
                o1 += 1
            # body
            b0 = next(i for i in range(ov, o1) if re.match(r"^\s*body: ", lines[i]) and indent(lines[i]) == item_ind)
            b1 = b0 + 1
            while b1 < o1 and (not lines[b1].strip() or indent(lines[b1]) > item_ind):
                b1 += 1
            old = yaml.safe_load("\n".join(l[item_ind:] if l.strip() else l for l in lines[b0:b1]))["body"]
            width = next((w for w in range(60, 160) if emit("body", old, item_ind, w) == lines[b0:b1]), None)
            if width is None:
                raise SystemExit(f"{sid} {oid}: the body's width could not be found; nothing written")
            if re.search(r"Required:|Optional:", old):     # a generated form's lists; a hand-written body is left alone
                edits.append((b0, b1, emit("body", clean_lists(old, fields), item_ind, width)))
            # discards
            d0 = next((i for i in range(ov, o1) if lines[i].strip() == "discards:"), None)
            if d0 is not None:
                d_ind = indent(lines[d0])
                i = d0 + 1
                while i < o1 and lines[i].strip().startswith("- ") and indent(lines[i]) >= d_ind:
                    if lines[i].strip()[2:].strip("'\"") in fields:
                        edits.append((i, i + 1, []))
                    i += 1
            log.append(f"{sid} {oid}: stops asking for {', '.join(sorted(fields))}")
    if not edits:
        return False
    for a, b, new in sorted(edits, reverse=True):
        lines[a:b] = new
    text = eol.join(lines)
    yaml.load(text, Loader=yaml.CSafeLoader)
    path.write_bytes(text.encode("utf-8"))
    return True


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    pk = sp.Package(str(ROOT))
    todo = defaultdict(lambda: defaultdict(dict))
    n = 0
    for sid, s in pk.screens.items():
        for o in s.get("overlays") or []:
            if not isinstance(o, dict):
                continue
            op = (o.get("confirm") or {}).get("operation")
            sch = pk.request_schema(op) if op else None
            if not sch:
                continue
            ro = {f for f in sp.overlay_asked(o) if sp.read_only(sch, f)}
            if ro:
                todo[pk.files[s["_plat"]]][sid][o["id"]] = ro
                n += 1
    print(f"{n} overlay(s) ask for a readOnly field, on {sum(len(v) for v in todo.values())} screen(s)")
    log: list = []
    if a.apply:
        for f, t in sorted(todo.items()):
            if fix_file(Path(f), t, log):
                print(f"  wrote {Path(f).name}")
    for line in log:
        print("  " + line)
    if not a.apply:
        print("dry run: pass --apply to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
