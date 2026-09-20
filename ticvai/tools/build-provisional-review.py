#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CF-171: turn 577 operations awaiting sign-off into seven review sessions.

**There is no engineering work left on the 577.** They were drafted by
`draft-pack-operations.py` from the 590 screens in the workshop pack — 13 already had operations,
these are the rest — and `specify-pack-operations.py` has since given every one of them a request
and a response read out of the pack. All 577 carry a `$ref` response schema, a permission, an
audience, a scope level and a citation of `<pack>, page N`. The 8 September audit resolved
**577 of 577 citations to a real pack, with no page beyond that pack's length.**

**`x-ticvai-provisional` does not mean unfinished. It means not yet agreed with whoever has to
build it.** No amount of contract work clears it — rewriting all 577 descriptions would leave all
577 provisional, because what is missing is a backend engineer saying *"yes, that is the shape"*.
That is why CF-171 survived a month in which the package gained 430 specified operations, closed
seven conflicts and rewrote its retention model, and **not one of the 577 was opened**: everything
we changed went around it.

So this writes what a session needs rather than another measurement of the problem.

## Ordered by pack and page, not by contract path

**A reviewer opens a book.** Sorting by URL would make a session jump between seventeen documents
for the sake of grouping `/virtual-ticket` next to `/virtual-ticket/{id}`; sorting by pack and
page means somebody reads a pack once, in order, and answers as they go.

Each row carries the three things an answer needs and nothing else: **where it came from** (pack
and page, so the claim is checkable), **what the client's own screen said** (their words, not
ours), and **the shape we read out of it** (the part to agree or correct).

    python3 tools/build-provisional-review.py
"""
import collections
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "handoff", "provisional-review")

CITE = re.compile(r"not invented\.\*\*\s*(.+?),\s*page\s*(\d+)\.", re.S)
SAYS = re.compile(r"The screen says:\s*(.+?)(?:\n\n|$)", re.S)


def clean(s, n=None):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s[:n] + "…" if n and len(s) > n else s


# **Two signals for where a session's time actually goes.** `specify-pack-operations` read the
# pack's bullets as fields, and its own docstring concluded *"they are fields"* — which is true
# of nearly all of them and not of all. A bullet that is a lifecycle trigger, a UI behaviour or
# a table column heading becomes a property name that no engineer will recognise.
SENTENCE = re.compile(r"(Is|Are|Was|Were|Occurs|Exists?|Becomes|Requests?|Do|Does|Can|Should"
                      r"|Must|Subject|Where|When|If)[A-Z]")
LEADIN = re.compile(r"^(a|an|the|and|or|if|when|drag|click|select|view|allow|enable)[A-Z]")
WIDE = 25


def caution(props):
    """Why this row may need more than a yes. Empty where the shape reads cleanly."""
    if not props:
        return ""
    odd = [p for p in props if SENTENCE.search(p) or LEADIN.match(p)]
    notes = []
    if len(odd) / len(props) >= 0.25:
        notes.append("**%d of %d property names read as sentences** rather than fields — "
                     "likely the pack's bullets (triggers, behaviours) taken as a directory: %s"
                     % (len(odd), len(props), ", ".join("`%s`" % p for p in odd[:5])))
    if len(props) > WIDE:
        notes.append("**%d properties.** A response this wide, read off a directory screen, is "
                     "usually the screen's *filter set* rather than one record's fields."
                     % len(props))
    return " ".join(notes)


def fields_of(op, schemas, depth=0):
    """The property names of the response schema, which is what a reviewer agrees or corrects."""
    blob = json.dumps(op.get("responses") or {})
    m = re.search(r"#/components/schemas/([A-Za-z0-9_]+)", blob)
    if not m:
        return "", []
    name = m.group(1)
    sc = schemas.get(name) or {}
    props = sc.get("properties") or {}
    if not props and sc.get("items"):
        inner = re.search(r"#/components/schemas/([A-Za-z0-9_]+)", json.dumps(sc["items"]))
        if inner:
            props = (schemas.get(inner.group(1)) or {}).get("properties") or {}
    return name, sorted(props)


def main():
    rows = []
    for sub in ("spine", "satellite"):
        d = os.path.join(ROOT, "contracts", sub)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".yaml"):
                continue
            doc = yaml.safe_load(io.open(os.path.join(d, fn), encoding="utf-8")) or {}
            schemas = (doc.get("components") or {}).get("schemas") or {}
            for path, ops in (doc.get("paths") or {}).items():
                for verb, op in (ops or {}).items():
                    if not isinstance(op, dict) or not op.get("x-ticvai-provisional"):
                        continue
                    desc = str(op.get("description") or "")
                    mc, ms = CITE.search(desc), SAYS.search(desc)
                    schema, props = fields_of(op, schemas)
                    rows.append({
                        "contract": fn[:-5], "verb": verb.upper(), "path": path,
                        "op": op["operationId"], "summary": clean(op.get("summary")),
                        "pack": clean(mc.group(1)) if mc else "(uncited)",
                        "page": int(mc.group(2)) if mc else 0,
                        "says": clean(ms.group(1) if ms else "", 320),
                        "schema": schema, "props": props,
                        "perm": op.get("x-ticvai-permission") or "—",
                        "aud": ", ".join(op.get("x-ticvai-audience") or []) or "—",
                        "screens": [clean(s) for s in (op.get("x-ticvai-consumed-by") or [])],
                        "caution": caution(props),
                    })

    if not rows:
        print("  no provisional operations — CF-171 is closed")
        return 0

    by_contract = collections.defaultdict(list)
    for r in rows:
        by_contract[r["contract"]].append(r)

    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    for contract, rs in sorted(by_contract.items(), key=lambda kv: -len(kv[1])):
        rs.sort(key=lambda r: (r["pack"], r["page"], r["op"]))
        packs = collections.Counter(r["pack"] for r in rs)
        L = ["# %s — %d operations awaiting sign-off" % (contract, len(rs)), ""]
        L.append("> **These are specified, not unfinished.** Each has a request, a response and a "
                 "citation of\n> the pack page it was read from. `x-ticvai-provisional` means "
                 "**nobody who has to build it\n> has agreed it** — so the only thing that closes "
                 "one is a decision in this column: *agreed*,\n> *corrected* (say how), or "
                 "*not needed*.")
        L.append("")
        L.append("**%d pack(s), read in page order.** A session opens a book and walks it." % len(packs))
        L.append("")
        for p, n in packs.most_common():
            L.append("- %s — **%d**" % (p, n))
        L.append("")
        cur = None
        for r in rs:
            if r["pack"] != cur:
                cur = r["pack"]
                L += ["", "---", "", "## %s" % cur, ""]
            L.append("### p%-3d · `%s`" % (r["page"], r["op"]))
            L.append("")
            L.append("`%s %s` · %s · %s · **%s**"
                     % (r["verb"], r["path"], r["perm"], r["aud"], r["summary"]))
            L.append("")
            if r["says"]:
                L.append("> %s" % r["says"])
                L.append("")
            if r["props"]:
                L.append("**`%s`** — %s" % (r["schema"], ", ".join("`%s`" % p for p in r["props"])))
            elif r["schema"]:
                L.append("**`%s`** — no properties declared" % r["schema"])
            L.append("")
            if r["caution"]:
                L.append("> ⚠ %s" % r["caution"])
                L.append("")
            for s in r["screens"][:3]:
                L.append("- serves %s" % s)
            L.append("")
            L.append("**Decision:** ")
            L.append("")
        io.open(os.path.join(OUT, "%s.md" % contract), "w",
                encoding="utf-8", newline="\n").write("\n".join(L) + "\n")

    idx = ["# CF-171 — the sign-off backlog, as sessions", "",
           "**%d operations across %d contracts and %d packs.** Not 577 conversations."
           % (len(rows), len(by_contract), len({r["pack"] for r in rows})), "",
           "They are drafted, specified and cited. **What is missing is agreement**, which is why "
           "no\namount of contract work has moved this number since 8 September while the package "
           "gained\n430 specified operations around it.", "",
           "| Session | Operations | Packs | Flagged | Sheet |",
           "|---|---:|---:|---:|---|"]
    for contract, rs in sorted(by_contract.items(), key=lambda kv: -len(kv[1])):
        idx.append("| **%s** | %d | %d | %d | [%s.md](%s.md) |"
                   % (contract, len(rs), len({r["pack"] for r in rs}),
                      sum(1 for r in rs if r["caution"]), contract, contract))
    flagged = sum(1 for r in rows if r["caution"])
    uncited = sum(1 for r in rows if r["pack"] == "(uncited)")
    idx += ["", "**%d of %d carry a flag** — a shape worth more than a yes, either because its "
            "property\nnames read as sentences rather than fields or because it is wide enough "
            "to be a filter set\nrather than a record. **The other %d should be quick.**"
            % (flagged, len(rows), len(rows) - flagged), "",
            "**%d operation(s) carry no pack citation this could parse.**" % uncited
            if uncited else "", "",
            "**The other half of CF-171 is not here.** 26 of 43 design packs have no operation "
            "drafted\nfrom them at all — Retail (202pp), Inventory & Procurement (175pp), Resource "
            "Management\n(169pp), F&B Backend (130pp), Wallet (129pp), Finance (123pp). **That is "
            "a reading job,\nnot a review**, and it is where unknown scope lives."]
    io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8",
            newline="\n").write("\n".join(idx) + "\n")

    print("  %d provisional operation(s) · %d session sheet(s) · %d pack(s)"
          % (len(rows), len(by_contract), len({r["pack"] for r in rows})))
    for contract, rs in sorted(by_contract.items(), key=lambda kv: -len(kv[1]))[:10]:
        print("    %-18s %3d  across %d pack(s)"
              % (contract, len(rs), len({r["pack"] for r in rs})))
    if uncited:
        print("  %d with no parseable citation" % uncited)
    print("  -> handoff/provisional-review/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
