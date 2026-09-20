#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per module, the checklist of things a person can be allowed to do.

**Decided 21 September, Chinmay.** *"Permissions are tricky — essentially it is a configuration.
We have accounts or users to whom we can grant access and a role within a module, and the roles of
the modules are not really defined... How about, while creating a user or granting them access to a
module, we have a checklist of things they can do in that module?"*

**That is the right shape and it dissolves the problem rather than solving it.** Defining roles per
module means inventing a taxonomy nobody has agreed — Supervisor, Manager, Lead — and then arguing
about which one may void a transaction. A checklist asks the only question the person granting
access can actually answer: **may this person do this specific thing, yes or no.** A role becomes a
saved checklist, which is a convenience, rather than a prerequisite, which is a blocker.

**And it is derivable, which is why it is worth doing now.** The package already knows every
capability of every module: `contracts/shared/permissions.yaml` carries 167 permission keys with a
group heading and, for 89 of them, a one-line description of what it lets somebody do. Every
contract declares `x-ticvai-permission` on every operation. Crossing the two gives, per module, the
list of things a person could be permitted — **232 (module, capability) pairs, none of them
invented here.**

## This is also the answer to the 167-against-44 conflict

`roles.yaml` holds 44 lowercase action keys lifted from the POS board and shares **zero** keys with
the 167 in `permissions.yaml`, so `check-screens` could only validate POS guards. The conflict was
framed as *reconcile the two vocabularies*. **There is only one vocabulary** — the 167 — and
`roles.yaml` is a saved checklist for one surface that got mistaken for the alphabet. Generating
the catalogue from `permissions.yaml` makes that explicit.

## Two flags, both derived from a signal that already exists

    elevated                guards at least one operation carrying `x-ticvai-step-up`
    segregationConstrained  named in a SegregationRule's conflictingPermissions,
                            so ticking it may conflict with something already held

**Neither is a judgement this tool makes.** A capability is elevated because an operation behind it
already said it needs a second factor, not because its name sounds dangerous.

## What this deliberately does not do

**It does not decide who gets what.** It produces the checklist; the grant is
`setPrincipalModuleAccess`, and the choice is a person's.

**It does not invent labels.** 78 of the 167 permissions have no description in
`permissions.yaml`, and they are emitted with `label: null` rather than a sentence generated from
the key. **A checklist item nobody can read is worse than a missing one**, because it will be
ticked anyway — so the gap is counted and reported, not papered over.

    python3 tools/derive-capabilities.py [--apply]
"""
import argparse
import collections
import glob
import io
import json
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERMS = os.path.join(ROOT, "contracts", "shared", "permissions.yaml")
OUT = os.path.join(ROOT, "handoff", "module-capabilities.json")

SKIP = {"common", "permissions"}


def read_vocabulary():
    """Key -> (label, group), read from the file's own layout.

    The labels are trailing `#` comments and the groups are `# --- Heading ---` rules, so this
    reads the text rather than the parse. A YAML loader throws both away.
    """
    group = None
    out = {}
    for line in io.open(PERMS, encoding="utf-8"):
        h = re.match(r"^\s*#\s*---+\s*(.+?)\s*-*\s*$", line)
        if h:
            group = h.group(1).strip()
            continue
        m = re.match(r"^\s*-\s+([A-Z][A-Z0-9_]+)\s*(?:#\s*(.*?))?\s*$", line)
        if m:
            out[m.group(1)] = ((m.group(2) or "").strip() or None, group)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    vocab = read_vocabulary()
    print("  %d permission key(s) in the vocabulary, %d with a description"
          % (len(vocab), sum(1 for v in vocab.values() if v[0])))

    modules = collections.defaultdict(lambda: collections.defaultdict(list))
    stepup = set()
    titles = {}
    unguarded = collections.Counter()
    segregated = set()

    for f in sorted(glob.glob(os.path.join(ROOT, "contracts", "*", "*.yaml"))):
        name = os.path.splitext(os.path.basename(f))[0]
        if name in SKIP:
            continue
        d = yaml.safe_load(io.open(f, encoding="utf-8").read())
        titles[name] = ((d.get("info") or {}).get("x-ticvai-module")
                        or (d.get("info") or {}).get("title") or name)
        for path, ms in (d.get("paths") or {}).items():
            for _, o in (ms or {}).items():
                if not isinstance(o, dict) or not o.get("operationId"):
                    continue
                key = o.get("x-ticvai-permission")
                if not key:
                    unguarded[name] += 1
                    continue
                modules[name][key].append(o["operationId"])
                if o.get("x-ticvai-step-up"):
                    stepup.add(key)
        # A rule's conflicting set is authored in identity, not here; read it where it lives.
        for s in ((d.get("components") or {}).get("schemas") or {}).values():
            if not isinstance(s, dict):
                continue
            props = s.get("properties") or {}
            for field in ("permissionA", "permissionB"):
                ex = (props.get(field) or {}).get("example")
                if ex:
                    segregated.add(ex)

    unknown = {k for m in modules.values() for k in m} - set(vocab)
    if unknown:
        print("  !! %d permission(s) used by a contract and absent from the vocabulary: %s"
              % (len(unknown), sorted(unknown)[:6]))
        return 1

    out = {"generated": "21 September 2026",
           "note": ("Per module, the capabilities a person can be granted. Derived from "
                    "contracts/shared/permissions.yaml crossed with every contract's "
                    "x-ticvai-permission. **The checklist a grant screen renders** — not a role "
                    "taxonomy, because a role is a saved checklist rather than a prerequisite."),
           "modules": {}}

    n_caps = n_unlabelled = 0
    for name in sorted(modules):
        caps = []
        for key in sorted(modules[name]):
            label, group = vocab[key]
            if label is None:
                n_unlabelled += 1
            caps.append({
                "key": key,
                "label": label,
                "group": group,
                "operationCount": len(modules[name][key]),
                "operations": sorted(modules[name][key])[:6],
                "elevated": key in stepup,
                "segregationConstrained": key in segregated,
            })
        n_caps += len(caps)
        out["modules"][name] = {
            "title": titles.get(name, name),
            "capabilityCount": len(caps),
            "unguardedOperations": unguarded.get(name, 0),
            "capabilities": caps,
        }

    print("  %d module(s) · %d capability pair(s) · %d elevated · %d with no label"
          % (len(out["modules"]), n_caps, len(stepup), n_unlabelled))
    print("  %d operation(s) carry no permission and are therefore on no checklist"
          % sum(unguarded.values()))

    # **The gap is listed, not just counted.** A checklist item that renders as `ORDER_VOID` asks
    # the person granting access to know what the platform calls things, which is the opposite of
    # the point. These are one line each and the operations behind them are named beside each key,
    # so whoever writes them is not guessing.
    missing = sorted({k for m in modules.values() for k in m if vocab[k][0] is None})
    out["unlabelled"] = {
        "note": ("Permission keys used by a contract with no description in "
                 "contracts/shared/permissions.yaml. **A checklist item nobody can read gets "
                 "ticked anyway**, so these are the blocker for shipping the grant screen -- not "
                 "the contract, which is done. One line each, written next to the key in "
                 "permissions.yaml."),
        "count": len(missing),
        "keys": {k: sorted({o for m in modules.values() for o in m.get(k, [])})[:4]
                 for k in missing},
    }
    if missing:
        print("  %d distinct key(s) have no description — listed in the output with the "
              "operations behind each" % len(missing))

    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, indent=1, ensure_ascii=False))
    print("  -> handoff/module-capabilities.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
