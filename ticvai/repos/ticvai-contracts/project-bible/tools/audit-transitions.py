#!/usr/bin/env python3
"""How much of the navigation graph says more than a destination, per platform.

**The graph has never been the problem.** All 2,684 `exitTo` entries resolve to a real screen and
there is not one dangling reference in the package. What none of them said was *how* — which
control makes the move, what gates it, what state travels with it, where cancel goes, and what
happens when the payment declines.

This counts that gap. An exit is **labelled** when `navigation.transitions[]` carries an entry
for it, and **bare** when nothing does. Bare is not an error — it is unwritten, and the point of
counting is to know how much is left rather than to fail a build over a screen nobody has reached.

**Why it reads a parallel list rather than the exits themselves.** Labelling `exitTo` in place was
built on 9 September and reverted the same day: eleven tools read those entries as bare strings,
and not one of them crashed on a dict. They compared it to a set of ids and reported a dangling
link to a screen named `{'to': 'POS-005'}` — loud enough to notice, quiet enough to be mistaken
for a data error. So `exitTo` stays the graph and `transitions` is the same edge with the answers
attached, joined on `to`.

The vocabulary is read from `screens/_schema.yaml` rather than listed here, so a field added to
the schema is counted the next time this runs instead of being silently ignored.

Read alongside `screen-ledger.py`, which counts whether a screen is *in* the graph. This counts
whether its edges mean anything. `check-screens.py` is what fails a build; this only measures.
"""

from __future__ import annotations
import collections
import glob
import os
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def vocabulary() -> list[str]:
    """The transition fields the schema declares, minus `to`, which every entry has."""
    doc = yaml.safe_load((ROOT / "screens" / "_schema.yaml").read_text(encoding="utf-8"))
    nav = doc["properties"]["screens"]["items"]["properties"]["navigation"]
    tr = (nav.get("properties") or {}).get("transitions", {}).get("items", {})
    return [k for k in (tr.get("properties") or {}) if k != "to"]


def main() -> int:
    fields = vocabulary()
    rows = []
    field_use: collections.Counter = collections.Counter()
    total_l = total_b = 0
    denied_needed = denied_have = 0
    uses_count = 0
    unresolved_sets: set = set()

    for f in sorted(glob.glob(str(ROOT / "screens" / "P*.yaml"))):
        code = os.path.basename(f)[:3]
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        lab = bare = 0
        for s in doc.get("screens") or []:
            nav = s.get("navigation") or {}
            if nav.get("uses"):
                uses_count += 1
                unresolved_sets.update(nav["uses"])

            transitions = nav.get("transitions") or []
            # An entry may point at `SCREEN#anchor`; the exit it labels is the screen.
            labelled_to = {str(t.get("to", "")).partition("#")[0]
                           for t in transitions if isinstance(t, dict)}
            gated = False
            for t in transitions:
                if not isinstance(t, dict):
                    continue
                for k in fields:
                    if t.get(k) not in (None, "", [], {}):
                        field_use[k] += 1
                if t.get("guard"):
                    gated = True

            for e in (nav.get("exitTo") or []):
                if e in labelled_to:
                    lab += 1
                else:
                    bare += 1

            # **The pairing that is the whole reason roles.yaml exists.** A move that can be
            # refused needs a screen state for the refusal, and `denied` stood at 3 screens out of
            # 1,231 because nothing connected the two.
            if gated:
                denied_needed += 1
                if (s.get("states") or {}).get("denied"):
                    denied_have += 1

        rows.append((code, lab, bare))
        total_l += lab
        total_b += bare

    print("Transition labelling — how much of the graph says more than a destination\n")
    print(f"{'':5} {'edges':>7} {'labelled':>9} {'bare':>7}")
    for code, lab, bare in rows:
        tot = lab + bare
        pct = f"{lab * 100 // tot}%" if tot else "—"
        bar = "#" * (lab * 20 // tot) if tot else ""
        print(f"{code:5} {tot:7} {lab:9} {bare:7}   {pct:>4} {bar}")

    tot = total_l + total_b
    print(f"\n{'ALL':5} {tot:7} {total_l:9} {total_b:7}   "
          f"{total_l * 100 // tot if tot else 0}%")

    print("\nWhich labels are actually being used:")
    for k in fields:
        n = field_use.get(k, 0)
        print(f"  {k:14} {n:5}" + ("" if n else "   <- nothing uses this yet"))

    print(f"\nScreens naming a shared navigation set: {uses_count}")
    if unresolved_sets:
        # Nothing in the package defines these. `check-screens.py` warns; this says which.
        print(f"  sets named: {', '.join(sorted(unresolved_sets))}  <- none of them is defined")

    print(f"\nScreens with a permission-gated transition: {denied_needed}")
    print(f"  of those, declaring states.denied     : {denied_have}"
          + ("" if denied_have == denied_needed else "   <- the rest refuse into nothing"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
