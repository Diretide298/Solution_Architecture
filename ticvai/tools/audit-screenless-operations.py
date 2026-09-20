#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Operations no screen consumes, and which of them should have one.

**This question keeps coming back because nothing records the answer.** `link-screens-contracts`
prints *"N operations have no screen consuming them"* and says, correctly, that each is either a
screen not yet specified or an endpoint that should not exist — and then the number is read again
next month as if it were all backlog. It is not: **most of it is not missing anything.**

This is the same shape as `handoff/schema-storage-only.md`, which records the tables that
deliberately have no API so that `audit-unwired-tables` stops re-asking. The companion document
here is `handoff/operations-without-screens.md`.

## The five reasons an operation legitimately has no screen of its own

    actionOnExistingScreen   **the largest group by far.** `setJobTitle` is a PUT reached from
                             the screen that `listJobTitles` feeds. The linker matches a screen
                             to the operation it *reads*, so the write beside it looks uncovered
                             and is not — the button is on the screen already
    embeddedClient           **runs inside hardware and has no design surface.** A turnstile
                             runs a thick client; a KDS bumps a ticket; a scanner reads a code.
                             The device is the interface, and drawing a wireframe for it would
                             describe a screen nobody builds
    machineToMachine         `service` or `anonymous` audience only — webhooks, callbacks,
                             provider notifications. Nobody is looking at these
    crossCell                one cell calling another. The caller is a service, and the screen
                             that started it belongs to whichever cell the person is in
    scheduledJob             `x-ticvai-singleton: true` — a close, a revaluation, a sync run.
                             A person may trigger it from somewhere, but the operation is a job

Everything else needs a screen, and that number is the only one worth carrying in a backlog.

## How a judgement gets recorded

The first four are derived from what the contract already declares. **A case that is none of
them and still needs no screen is a judgement**, and it goes on the operation itself:

    x-ticvai-no-screen: why this one has no design surface

On the operation rather than in a list, because an operation that moves contracts takes its
reason with it — which is what `derive-lineage` learned the hard way about `service`.

    python3 tools/audit-screenless-operations.py
    python3 tools/audit-screenless-operations.py --csv handoff/screenless-operations.csv
"""
import collections
import csv
import io
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")

# An audience nobody looks at.
UNATTENDED = {"service", "anonymous", "device"}
WRITE_VERBS = {"post", "put", "patch", "delete"}


def resource(path):
    """`/agreements/{id}/items` and `/agreements` are one resource for this purpose."""
    return "/" + path.strip("/").split("/")[0]


def load():
    ops = []
    for sub in ("spine", "satellite", "shared"):
        d = os.path.join(ROOT, "contracts", sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith((".yaml", ".yml")):
                continue
            doc = yaml.safe_load(io.open(os.path.join(d, fn), encoding="utf-8").read()) or {}
            for path, item in (doc.get("paths") or {}).items():
                for verb, op in (item or {}).items():
                    if not isinstance(op, dict) or not op.get("operationId"):
                        continue
                    aud = op.get("x-ticvai-audience")
                    ops.append({
                        "contract": fn.rsplit(".", 1)[0],
                        "operationId": op["operationId"],
                        "path": path,
                        "verb": verb.lower(),
                        "screens": list(op.get("x-ticvai-consumed-by") or []),
                        "audience": set(aud if isinstance(aud, list) else ([aud] if aud else [])),
                        "singleton": bool(op.get("x-ticvai-singleton")),
                        "noScreenReason": op.get("x-ticvai-no-screen") or "",
                    })
    return ops


def classify(ops):
    covered = collections.defaultdict(set)
    for o in ops:
        if o["screens"]:
            covered[(o["contract"], resource(o["path"]))].add(o["operationId"])

    out = []
    for o in ops:
        if o["screens"]:
            continue
        aud = o["audience"]
        if o["noScreenReason"]:
            state = "declared"
        elif aud and aud <= UNATTENDED:
            # **`device` first**, because a turnstile's thick client is the clearest case and
            # the one people ask about: the hardware is the interface.
            state = "embeddedClient" if "device" in aud else "machineToMachine"
        elif o["contract"] == "cross-region" and "staff" not in aud and "guest" not in aud:
            state = "crossCell"
        elif o["singleton"]:
            state = "scheduledJob"
        elif covered.get((o["contract"], resource(o["path"]))):
            # A write beside a screened read is a button on that screen. A *read* beside one is
            # usually a detail view, which is a screen — so only writes are excused here.
            state = ("actionOnExistingScreen" if o["verb"] in WRITE_VERBS
                     else "needsScreen")
        else:
            state = "needsScreen"
        out.append(dict(o, state=state,
                        siblingScreens=" | ".join(sorted(
                            covered.get((o["contract"], resource(o["path"])), set()))[:2])))
    return out


def main():
    ops = load()
    rows = classify(ops)
    by = collections.Counter(r["state"] for r in rows)
    need = [r for r in rows if r["state"] == "needsScreen"]

    print("  %d operation(s), %d with no screen" % (len(ops), len(rows)))
    for k, label in (
            ("actionOnExistingScreen", "a write reached from the screen its sibling read feeds"),
            ("embeddedClient", "runs inside hardware — the device is the interface"),
            ("machineToMachine", "service or anonymous audience; nobody is looking"),
            ("crossCell", "one cell calling another"),
            ("scheduledJob", "a job, however it is triggered"),
            ("declared", "x-ticvai-no-screen says why"),
            ("needsScreen", "**a screen that has not been specified**")):
        if by[k]:
            print("    %-24s %3d   %s" % (k, by[k], label))

    if not need:
        print("\n  PASS — every screenless operation is explained")
        return 0

    print("\n  %d need a screen, by contract and resource:" % len(need))
    for (c, r), n in collections.Counter(
            (x["contract"], resource(x["path"])) for x in need).most_common(24):
        ex = [x["operationId"] for x in need
              if x["contract"] == c and resource(x["path"]) == r][:3]
        print("    %-16s %-28s %2d   %s" % (c, r, n, ", ".join(ex)))

    argv = sys.argv[1:]
    if "--csv" in argv:
        out = os.path.join(ROOT, argv[argv.index("--csv") + 1])
        with io.open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["contract", "operationId", "path", "verb",
                                               "state", "siblingScreens", "noScreenReason"])
            w.writeheader()
            for r in sorted(rows, key=lambda x: (x["state"] != "needsScreen", x["contract"],
                                                 x["path"])):
                w.writerow({k: r[k] for k in w.fieldnames})
        print("\n  -> %s" % os.path.relpath(out, ROOT))
    # **Reports, never fails.** Whether an operation needs a screen is a design judgement, and a
    # checker that fails the package on one gets silenced rather than answered.
    return 0


if __name__ == "__main__":
    sys.exit(main())
