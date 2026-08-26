#!/usr/bin/env python3
"""Render a derived domain set as a page.

    python3 tools/derive-domain.py ai && python3 tools/render-domain.py ai

The second surface. `handoff/ai-index.md` was written by hand and drifted four times in one day;
this replaces it with the same closure that drives the in-tree markers, so the page and the dots
can never disagree.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "handoff"


def render(d: dict) -> str:
    n = d["domain"]
    c = d["counts"]
    L: list[str] = []
    w = L.append

    w(f"# {n.upper()} — the whole set")
    w("")
    w(f"**Derived, not written.** Regenerate with `python3 tools/derive-domain.py {n} && "
      f"python3 tools/render-domain.py {n}`. Nothing below is hand-typed, so nothing here goes "
      f"stale — which the hand-maintained version did four times on 17 August alone.")
    w("")
    w(f"**{n} has no folder and should not.** The package is organised by artefact kind, and a "
      f"single domain folder would raise the question of why there is no `finance/`. This page "
      f"gathers what is spread across layers; each artefact stays where it belongs.")
    w("")
    w("| | |")
    w("|---|---|")
    for k, v in c.items():
        label = "".join(" " + ch.lower() if ch.isupper() else ch for ch in k).strip().capitalize()
        w(f"| **{label}** | {v} |")
    w("")

    foreign = [s for s in d["states"] if s.get("foreignContract")]
    if foreign:
        w("## Reached outside the contract")
        w("")
        w("**The closure follows behaviour, not folders.** These state models live under other "
          "contracts and specify things this domain depends on — the hand-written index named "
          "none of them.")
        w("")
        w("| Model | Lives under | Reached via |")
        w("|---|---|---|")
        for s in foreign:
            via = ", ".join(f"`{x}`" for x in s.get("reachedVia", [])) or "domain enum"
            w(f"| `{s['file']}` | `{s['contract']}` | {via} |")
        w("")

    # the boundary section, from status-<domain>.json where it exists
    import json as _json
    sp = HANDOFF / f"status-{n}.json"
    if sp.exists():
        st = _json.loads(sp.read_text(encoding="utf-8"))
        if st.get("boundaries"):
            w("## What it is walled off from")
            w("")
            w("**A page showing only what a domain *is* answers half the question.** The other half "
              "is what it cannot reach, and what keeps that true rather than merely true today.")
            w("")
            w("| | Holds | Enforced by |")
            w("|---|---|---|")
            for b in st["boundaries"]:
                mark = "yes" if b["holds"] else "**NO**"
                w(f"| **{b['name']}** — {b['detail']} | {mark} | {b['enforcedBy']} |")
            w("")
            if st.get("stores"):
                w("**Storage tiers** — " + " · ".join(f"`{k}` {v}" for k, v in sorted(st["stores"].items())))
                w("")

    w("## Operations")
    w("")
    own = {k: v for k, v in d["operations"].items() if not v.get("foreignContract")}
    ext = {k: v for k, v in d["operations"].items() if v.get("foreignContract")}
    w(f"**{len(own)} in the contract.**")
    w("")
    w("| Operation | Verb | Guest | Scope |")
    w("|---|---|---|---|")
    for k, v in own.items():
        w(f"| `{k}` | {v['verb']} | {'yes' if 'guest' in (v.get('audience') or []) else ''} | {v.get('scopeLevel') or ''} |")
    w("")
    if ext:
        w(f"**{len(ext)} elsewhere, writing a `{n}.*` table.** Each one is another contract "
          f"reaching into this domain, which is worth seeing rather than hiding.")
        w("")
        for k, v in ext.items():
            w(f"- `{k}` in `{v['foreignContract']}`")
        w("")

    w("## States")
    w("")
    w("| Model | Contract | Enum | Emits |")
    w("|---|---|---|---|")
    for s in d["states"]:
        w(f"| `{s['file']}` | {s['contract']} | `{s['enum']}` | {', '.join(f'`{e}`' for e in s['emits']) or '—'} |")
    w("")

    w("## Events")
    w("")
    w("| Event | Role | Publisher | Critical consumer |")
    w("|---|---|---|---|")
    for e in d["events"]:
        w(f"| `{e['name']}` | {e['role']} | {e['publisher']} | {'yes' if e['critical'] else 'no'} |")
    w("")

    w("## Storage")
    w("")
    for store, tables in sorted(d["tables"]["byStore"].items()):
        w(f"**`{store}`** — {len(tables)}")
        w("")
        w("".join(f"`{t}` · " for t in tables).rstrip(" ·"))
        w("")
    inbound = d["tables"].get("inboundKeys") or []
    if inbound:
        w("**Keys pointing in from other domains.** Each is a place another part of the platform "
          "depends on this one.")
        w("")
        for r in inbound:
            w(f"- `{r['from']}.{r['column']}` → `{r['to']}`")
        w("")

    w("## Screens")
    w("")
    by_platform: dict[str, list] = {}
    for s in d["screens"]:
        by_platform.setdefault(f"{s['platform']} {s['platformName']}", []).append(s)
    for p, rows in sorted(by_platform.items()):
        w(f"**{p}**")
        w("")
        for s in sorted(rows, key=lambda x: x["id"]):
            w(f"- `{s['id']}` {s['name']} — wave {s['wave']}, {len(s['operations'])} operation"
              f"{'s' if len(s['operations']) != 1 else ''}")
        w("")

    if d["flows"]:
        w("## Flows")
        w("")
        for f in d["flows"]:
            w(f"- **{f['id']}** {f['name']} — wave {f['wave']}")
        w("")

    w("## Decisions and documents")
    w("")
    w("| Document | Status | Mentions |")
    w("|---|---|---|")
    for doc in d["documents"]:
        w(f"| [{doc['title']}]({Path('..') / doc['file']}) | {doc['status']} | {doc['mentions']} |")
    w("")

    if d["conflicts"]:
        openc = [x for x in d["conflicts"] if x["open"]]
        closed = [x for x in d["conflicts"] if not x["open"]]
        w("## Conflicts")
        w("")
        if openc:
            w(f"**{len(openc)} open** — " + " · ".join(f"**{x['id']}**" for x in openc))
        if closed:
            w("")
            w(f"{len(closed)} closed — " + " · ".join(x["id"] for x in closed))
        w("")

    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("domain")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    src = HANDOFF / f"domain-{args.domain}.json"
    if not src.exists():
        raise SystemExit(f"run `python3 tools/derive-domain.py {args.domain}` first")

    data = json.loads(src.read_text(encoding="utf-8"))
    out = Path(args.out) if args.out else HANDOFF / f"{args.domain}-index.md"
    out.write_text(render(data), encoding="utf-8")
    print(f"{args.domain}: {out.relative_to(ROOT)} ({len(out.read_text(encoding='utf-8').splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
