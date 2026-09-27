#!/usr/bin/env python3
"""Derive `transitions[].carries` from what the destination needs **and the source can supply**.

**`carries` is the field the whole transitions exercise exists for** — the state that travels with
a move, the thing a frontend developer cannot guess and otherwise finds by reading somebody's
JavaScript. It looked unobtainable: the flows do not record it, the boards do not, and inventing
it would be worse than leaving it blank.

**Half of it was already written down, on the other end of the edge.** Screens declare
`entryState.params` — `WEB-004 Attraction Details` needs `eventId` and `productId`; `POS-005
Payment` needs an order. That is the destination stating its own precondition.

**The other half is the source.** The first version of this tool (to 26 September) copied the
destination's params onto every `exitTo` edge and never asked whether the source had them. Exit
lists come from module nav-sets, so `BO-079 Stock Count` "carried" `eventId`, `feedId`, `queueId`
into `BO-001 Queue Directory` — ids a stock count never holds. The pull audit (R251) found 250
tickets built on edges like that. **An edge carries only what both ends agree on: a param the
destination declares and the source holds.** A source holds an id when it:

- declares it in its own `entryState.params` (any `from`, the session included);
- names it in `entryState.preloaded` (`Product.id` holds `productId`, `Event.venueId` holds
  `venueId`);
- calls an operation that takes it as a path parameter, or whose response returns it —
  a property of that name at any depth, or `id` on a schema whose name gives the id
  (`Reservation.id` is `reservationId`), including the rows of a `Page`.

A destination param `from: session` is never carried: the session resolves it (venue-scope rule).

**What this writes, in four passes. Idempotent; no arguments previews, `--apply` writes.**

1. **Mirror `entryFrom` into the parent's `exitTo`** (same platform only). The 4 September
   "Returns to X" pass set `entryFrom` on the child and never the parent's `exitTo`, so
   `POS-001` did not list `POS-017`, `BO-095` did not list `BO-098`, `ADM-002` did not list
   `ADM-037`. A handover across platforms is not a link and is not mirrored — the same rule
   derive-transitions-from-flows follows.
2. **Recompute the edges this tool owns** (provenance `derived — … declares entryState.params`):
   carries narrowed to what the source holds; an owned edge left carrying nothing is removed,
   because it says nothing a bare `exitTo` does not — unless a person has renamed its trigger,
   in which case it stays, without `carries`.
3. **Add owned edges** for `exitTo` targets with no transition yet, when there is something to
   carry.
4. **Fill `carries` on bare edges written by a flow, a board or a structural pass** (R262) —
   `GST-016 -> GST-017` needs `reservationId` and `GST-016` holds it. Only a transition with no
   `carries` key is touched; one that already says what it carries is a real source and wins.
   The flow tool rewrites its own edges each refresh without `carries`; this runs after it and
   puts them back, so a refresh ends where it started.

**What this does not claim.** The `trigger` on an owned edge is the destination's name, the same
convention the launcher and board-hub labels use — not a claim to know the button. `carries` is a
*requirement* both ends can meet, not an observation: a real source that says more is right.

**What it reports and does not repair:** a destination param that no inbound edge carries and
the session does not supply. Some are deep-link-only (`POS-014`, `GST-045`), some have no source
at all (`WEB-003` has no `q`). Which screen should supply them is a design decision.
"""

from __future__ import annotations
import glob
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
MINE = "derived — "
MINE_MARK = "declares entryState.params"
SESSION = "session"


def base(to) -> str:
    return str(to or "").partition("#")[0]


def lcfirst(s: str) -> str:
    return s[:1].lower() + s[1:]


def entry_params(screen: dict) -> list[dict]:
    out = []
    for p in ((screen.get("entryState") or {}).get("params") or []):
        if isinstance(p, dict) and p.get("name"):
            out.append(p)
        elif isinstance(p, str) and p:
            out.append({"name": p, "from": "navigation"})
    return out


def needed(screen: dict) -> list[str]:
    """What an edge arriving here must carry: every declared param the session does not supply."""
    return sorted({p["name"] for p in entry_params(screen) if p.get("from") != SESSION})


# ---------------------------------------------------------------- what an operation yields

class Contracts:
    def __init__(self) -> None:
        self.files: dict[pathlib.Path, dict] = {}
        self.ops: dict[str, tuple[pathlib.Path, dict, dict]] = {}
        for f in sorted((ROOT / "contracts").rglob("*.yaml")):
            doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
            self.files[f.resolve()] = doc
            for path_item in (doc.get("paths") or {}).values():
                if not isinstance(path_item, dict):
                    continue
                shared = path_item.get("parameters") or []
                for op in path_item.values():
                    if isinstance(op, dict) and op.get("operationId"):
                        self.ops.setdefault(op["operationId"], (f.resolve(), op,
                                                                {"shared": shared}))
        self._yield: dict[str, set[str]] = {}

    def deref(self, node, here: pathlib.Path):
        """Follow a $ref; return (node, file, schema name or None)."""
        name = None
        seen = 0
        while isinstance(node, dict) and "$ref" in node and seen < 20:
            seen += 1
            ref = node["$ref"]
            file_part, _, frag = ref.partition("#")
            target = (here.parent / file_part).resolve() if file_part else here
            doc = self.files.get(target)
            if doc is None:
                return {}, here, name
            cur = doc
            for part in [p for p in frag.split("/") if p]:
                cur = (cur or {}).get(part) if isinstance(cur, dict) else None
            name = frag.rsplit("/", 1)[-1] if "/schemas/" in frag else name
            node, here = cur or {}, target
        return node, here, name

    def names_in(self, node, here, out: set[str], name=None, depth=0, seen=None) -> None:
        seen = set() if seen is None else seen
        if depth > 6 or not isinstance(node, dict):
            return
        if "$ref" in node:
            key = (str(here), node["$ref"])
            if key in seen:
                return
            seen = seen | {key}
            node, here, name = self.deref(node, here)
            if not isinstance(node, dict):
                return
        for k in ("allOf", "oneOf", "anyOf"):
            for sub in node.get(k) or []:
                self.names_in(sub, here, out, name, depth + 1, seen)
        if isinstance(node.get("items"), dict):
            self.names_in(node["items"], here, out, None, depth + 1, seen)
        props = node.get("properties") or {}
        if isinstance(props, dict):
            if "id" in props and name and name not in ("Page", "Problem"):
                out.add(lcfirst(name) + "Id")
            for k, v in props.items():
                out.add(k)
                self.names_in(v, here, out, None, depth + 1, seen)

    def yields(self, operation_id: str) -> set[str]:
        """Every name an operation takes as a parameter or returns in a success body."""
        if operation_id in self._yield:
            return self._yield[operation_id]
        out: set[str] = set()
        hit = self.ops.get(operation_id)
        if hit:
            f, op, extra = hit
            for p in list(extra["shared"]) + list(op.get("parameters") or []):
                p, _, _ = self.deref(p, f)
                if isinstance(p, dict) and p.get("in") == "path" and p.get("name"):
                    out.add(p["name"])
            for code, resp in (op.get("responses") or {}).items():
                if not str(code).startswith("2"):
                    continue
                resp, rf, _ = self.deref(resp, f)
                for media in ((resp or {}).get("content") or {}).values():
                    if isinstance(media, dict) and media.get("schema"):
                        self.names_in(media["schema"], rf, out)
        self._yield[operation_id] = out
        return out

    def file_of(self, operation_id: str) -> str:
        hit = self.ops.get(operation_id)
        return str(hit[0]) if hit else ""


ANY = "*"


def holds(screen: dict, contracts: Contracts) -> dict[str, set[str]]:
    """Every id this screen has in hand to pass on, with the contract files it came from.

    An id the screen declares or preloads holds everywhere (`*`). An id read off an operation is
    scoped to that operation's contract, because a name alone is not an identity: a webhook
    delivery's `eventId` is a domain event, not the venue `Event` a queue screen wants.
    """
    out: dict[str, set[str]] = {}
    for p in entry_params(screen):
        out.setdefault(p["name"], set()).add(ANY)
    for pre in ((screen.get("entryState") or {}).get("preloaded") or []):
        ent, _, field = str(pre).partition(".")
        name = lcfirst(ent) + "Id" if field == "id" and ent else field
        if name:
            out.setdefault(name, set()).add(ANY)
    for a in (screen.get("apis") or []):
        if isinstance(a, dict) and a.get("operationId"):
            where = contracts.file_of(a["operationId"])
            for name in contracts.yields(a["operationId"]):
                out.setdefault(name, set()).add(where)
    return out


def contracts_of(screen: dict, contracts: Contracts) -> set[str]:
    return {contracts.file_of(a["operationId"]) for a in (screen.get("apis") or [])
            if isinstance(a, dict) and a.get("operationId")} - {""}


def provenance(src: str, dst: str, need: list[str], carries: list[str]) -> str:
    if carries:
        return (f"{MINE}{dst} {MINE_MARK} {', '.join(need)} and {src} holds "
                f"{', '.join(carries)}, so an edge into it carries them")
    return (f"{MINE}{dst} {MINE_MARK} {', '.join(need)} and {src} holds none of them, so the "
            f"edge carries nothing and {dst} opens cold")


def is_mine(t: dict) -> bool:
    p = str(t.get("provenance", ""))
    return p.startswith(MINE) and MINE_MARK in p


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    apply = "--apply" in sys.argv
    verbose = "--verbose" in sys.argv
    docs = {f: yaml.safe_load(open(f, encoding="utf-8"))
            for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml")))}
    screens = {s["id"]: s for d in docs.values() for s in d["screens"]}
    platform = {s["id"]: f for f, d in docs.items() for s in d["screens"]}
    contracts = Contracts()
    held = {sid: holds(s, contracts) for sid, s in screens.items()}
    reads = {sid: contracts_of(s, contracts) for sid, s in screens.items()}
    dirty: set[str] = set()
    counts = dict(mirrored=0, narrowed=0, added=0, filled=0)
    log: list[str] = []

    def owned(src: str, dst: str, old: dict | None) -> dict:
        """The edge this tool owns from src to dst. A trigger a person renamed is kept."""
        carries = carries_for(src, dst)
        entry = {"to": (old or {}).get("to", dst),
                 "trigger": (old or {}).get("trigger") or screens[dst]["name"]}
        if carries:
            entry["carries"] = carries
        entry["provenance"] = provenance(src, dst, needed(screens[dst]), carries)
        for k, v in (old or {}).items():
            if k not in ("to", "trigger", "carries", "provenance"):
                entry[k] = v
        return entry

    def carries_for(src: str, dst: str) -> list[str]:
        ok = reads[dst] | {ANY} if reads[dst] else None
        return [n for n in needed(screens[dst])
                if n in held[src] and (ok is None or held[src][n] & ok)]

    # 1. entryFrom -> parent's exitTo
    for sid, s in screens.items():
        for parent in ((s.get("navigation") or {}).get("entryFrom") or []):
            if parent not in screens or parent == sid or platform[parent] != platform[sid]:
                continue
            pnav = screens[parent].get("navigation")
            if pnav is None:
                pnav = screens[parent]["navigation"] = {}
            exits = pnav.get("exitTo")
            if exits is None:
                exits = pnav["exitTo"] = []
            if sid not in exits:
                exits.append(sid)
                exits.sort()
                counts["mirrored"] += 1
                dirty.add(platform[parent])
                log.append(f"mirror   {parent} exitTo += {sid} (from {sid}.entryFrom)")

    for sid, s in screens.items():
        nav = s.get("navigation") or {}
        trans = nav.get("transitions")
        if trans is None:
            trans = []
        kept = []
        changed = False

        # 2. owned edges, recomputed
        for t in trans:
            dst = base(t.get("to"))
            if not is_mine(t) or dst not in screens:
                kept.append(t)
                continue
            new = owned(sid, dst, t)
            if new != t:
                counts["narrowed"] += 1
                changed = True
                log.append(f"narrow   {sid} -> {dst}: {t.get('carries')} -> "
                           f"{new.get('carries') or '(nothing; arrives cold)'}")
            kept.append(new)

        # 3. new owned edges for exitTo targets that need something and have no transition
        done = {base(t.get("to")) for t in kept}
        for e in (nav.get("exitTo") or []):
            if e in done or e not in screens or not needed(screens[e]):
                continue
            new = owned(sid, e, None)
            kept.append(new)
            done.add(e)
            counts["added"] += 1
            changed = True
            log.append(f"add      {sid} -> {e}: {new.get('carries') or '(nothing; arrives cold)'}")

        # 4. bare edges from flows, boards, structure
        for i, t in enumerate(kept):
            dst = base(t.get("to"))
            if is_mine(t) or "carries" in t or dst not in screens:
                continue
            carries = carries_for(sid, dst)
            if carries:
                kept[i] = {**t, "carries": carries}
                counts["filled"] += 1
                changed = True
                log.append(f"fill     {sid} -> {dst} ({t.get('provenance', '')[:40]}): "
                           f"{carries}")

        if changed:
            dirty.add(platform[sid])
            # In memory either way, so the preview's report matches what --apply would leave;
            # only --apply writes a file.
            s.setdefault("navigation", nav)["transitions"] = kept

    # report: needed params no inbound edge carries
    inbound: dict[str, set[str]] = {}
    for sid, s in screens.items():
        for t in ((s.get("navigation") or {}).get("transitions") or []):
            inbound.setdefault(base(t.get("to")), set()).update(t.get("carries") or [])
    unsourced = []
    for sid, s in sorted(screens.items()):
        for p in entry_params(s):
            if p.get("from") == SESSION or p.get("optional") or p["name"] in inbound.get(sid, set()):
                continue
            unsourced.append((sid, p["name"], p.get("from")))

    if verbose or not apply:
        for line in log:
            print("  " + line)
    total = sum(counts.values())
    print(f"{counts['mirrored']} entryFrom mirrored into a parent exitTo; derived edges: "
          f"{counts['added']} added, {counts['narrowed']} recomputed to what the source holds; {counts['filled']} bare flow/board/structural edge(s) "
          f"given carries — {'written' if apply else 'pending (run with --apply)'}"
          if total else "nothing to do — every edge carries what both ends agree on")
    by_from: dict[str, int] = {}
    for _, _, fr in unsourced:
        key = "deepLink" if fr == "deepLink" else "navigation"
        by_from[key] = by_from.get(key, 0) + 1
    print(f"reported, not repaired: {len(unsourced)} required entry param(s) that no inbound edge "
          f"carries and the session does not supply ({by_from.get('deepLink', 0)} deep-link only, "
          f"{by_from.get('navigation', 0)} expected from navigation) — --verbose lists them")
    if verbose:
        for sid, name, fr in unsourced:
            print(f"  unsourced {sid} {name} (from: {fr})")

    if apply and dirty:
        for f in sorted(dirty):
            pathlib.Path(f).write_text(
                yaml.safe_dump(docs[f], sort_keys=False, allow_unicode=True, width=100),
                encoding="utf-8")
        print(f"written to {len(dirty)} platform file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
