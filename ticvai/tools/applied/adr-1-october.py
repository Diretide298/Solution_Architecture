# -*- coding: utf-8 -*-
"""ADR-0064, ADR-0067 and ADR-0068, accepted 1 October: the renames and the `429` sweep. Re-runnable.

The content of those decisions (the placement table, the merged device register, the admission rule
format, the waiting room, the plan's request limits) was written into the contracts by hand. This
script does the part that is mechanical and would otherwise be half-done: **a rename in the contract
alone does not land** (see `schema-merge-phase-1-renames-20-september.py`, which has the same shape).
`derive-schema.py` merges into the previous `schema-reference.json`, `derive-lineage.py` adds and never
removes, and the relationship graph is rebuilt from both, so each of the three would keep the old
name alive and the next refresh would rebuild the dropped table from it.

1. **ADR-0068: "access policy" means one thing.** Identity's staff-authorisation engine is renamed:
   the tables `identity.access_policy` and `identity.access_policy_version` become
   `identity.authorisation_policy` and `identity.authorisation_policy_version`, its eleven operations
   `*AccessPolic*` become `*AuthorisationPolic*`, its four schemas likewise, and its paths
   `/access-policies`, `/access-policy-templates`, `/access-policy-effectiveness` become
   `/authorisation-*`. Access's guest-admission names (`AccessDynamicPolicy`, `rollbackAccessPolicy`,
   `AccessPolicyScopeAssignment`, `AccessPolicyEvaluationSetting`) are the one meaning left and stay.
2. **ADR-0067: one device register.** `access.access_device` becomes `access.device_placement` (the
   identity, versions, health and lifecycle columns moved to `platform.device` by hand in the
   contracts), `AccessAccessDevice` becomes `AccessDevicePlacement`, `registerAccessDevice` becomes
   `placeAccessDevice` and `updateAccessDevice` becomes `updateAccessDevicePlacement`, on
   `/device-placements`. `access.device_binding` is untouched: it is a guest's phone bound to an
   entitlement, a different thing.
3. **The three derived files that cannot repoint themselves** (`schema-reference.json`,
   `relationship-graph.json`, `api-data-lineage.json`) are repointed textually, so their formatting
   and every judgement they carry stay exactly as they were.
4. **The renames are declared** in `derive-schema-history.py`, so a workbook diff reads three
   renames rather than three deletions and three additions, and `check-doc-tables.py` can name a
   document that still uses an old table name.
5. **ADR-0064 (SD-043): every operation declares `429`.** An operation with no `429` response gets
   the shared `TooManyRequests` (problem type `rate-limited`, `Retry-After` and the `RateLimit-*`
   headers), appended as the last entry of its `responses`. One that already declares its own `429`
   keeps it; it is reported if it carries no `Retry-After`.

    python3 tools/applied/adr-1-october.py            # report
    python3 tools/applied/adr-1-october.py --apply    # write
"""
import io
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RENAMED_ON = "2026-10-01"

OPS = {
    # ADR-0068: identity's staff-authorisation operations
    "listAccessPolicies": "listAuthorisationPolicies",
    "createAccessPolicy": "createAuthorisationPolicy",
    "getAccessPolicy": "getAuthorisationPolicy",
    "updateAccessPolicy": "updateAuthorisationPolicy",
    "setAccessPolicyState": "setAuthorisationPolicyState",
    "simulateAccessPolicy": "simulateAuthorisationPolicy",
    "getAccessPolicyBundle": "getAuthorisationPolicyBundle",
    "listAccessPolicyTemplates": "listAuthorisationPolicyTemplates",
    "listAccessPolicyHistory": "listAuthorisationPolicyHistory",
    "restoreAccessPolicyVersion": "restoreAuthorisationPolicyVersion",
    "listAccessPolicyEffectiveness": "listAuthorisationPolicyEffectiveness",
    # ADR-0067: access keeps only where a device is placed
    "registerAccessDevice": "placeAccessDevice",
    "updateAccessDevice": "updateAccessDevicePlacement",
}

SCHEMAS = {
    "AccessPolicyBundle": "AuthorisationPolicyBundle",
    "AccessPolicyVersion": "AuthorisationPolicyVersion",
    "AccessPolicy": "AuthorisationPolicy",
    "IdentityAccessPolicyEffectiveness": "AuthorisationPolicyEffectiveness",
    "AccessAccessDevice": "AccessDevicePlacement",
}

# old, new, why (the why is what derive-schema-history.py records)
TABLES = [
    ("identity.access_policy_version", "identity.authorisation_policy_version",
     "ADR-0068: moved with identity.authorisation_policy; each version of a staff-authorisation policy"),
    ("identity.access_policy", "identity.authorisation_policy",
     "ADR-0068: it is staff authorisation, not access. Guest admission at the gate is access.dynamic_policy, "
     "so 'access policy' now means one thing"),
    ("access.access_device", "access.device_placement",
     "ADR-0067: platform.device is the one device register; identity, versions, health and lifecycle moved "
     "there and this table keeps only where a device is placed in the gate topology. Not access.device_binding, "
     "which already names a guest's phone bound to an entitlement"),
]

PATHS = [
    (r"/access-policy-templates(?![\w-])", "/authorisation-policy-templates"),
    (r"/access-policy-effectiveness(?![\w-])", "/authorisation-policy-effectiveness"),
    (r"/access-policies(?![\w-])", "/authorisation-policies"),
    (r"/access-devices/\{deviceId\}", "/device-placements/{placementId}"),
    (r"/access-devices(?![\w/-])", "/device-placements"),
]

# Where the names live. P01 and P02 are the guest import's and name none of these; they are
# checked rather than trusted.
SOURCES = (sorted((ROOT / "contracts").rglob("*.yaml")) + sorted((ROOT / "screens").glob("P*.yaml"))
           + sorted((ROOT / "states").glob("*.yaml")) + sorted((ROOT / "events").glob("*.yaml"))
           + sorted((ROOT / "flows").glob("*.yaml")))
DERIVED = [ROOT / "handoff" / n for n in
           ("api-data-lineage.json", "schema-reference.json", "relationship-graph.json")]
NOT_OURS = ("P01-", "P02-")


def _word(name):
    return re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])")


def _table(name):
    return re.compile(r"(?<![\w.])" + re.escape(name) + r"(?![\w])")


RULES = ([(_word(o), n, "op") for o, n in OPS.items()]
         + [(_word(o), n, "schema") for o, n in SCHEMAS.items()]
         + [(_table(o), n, "table") for o, n, _ in TABLES]
         + [(re.compile(p), n, "path") for p, n in PATHS])


def rename_text(text):
    counts = {}
    for pat, new, kind in RULES:
        text, k = pat.subn(new, text)
        if k:
            counts[kind] = counts.get(kind, 0) + k
    return text, counts


def renames():
    total = 0
    for p in SOURCES + DERIVED:
        raw = io.open(p, encoding="utf-8", newline="").read()
        out, counts = rename_text(raw)
        if out == raw:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if p.name.startswith(NOT_OURS):
            print("    !! %s names a renamed operation or table; not ours to edit, left alone" % rel)
            continue
        total += sum(counts.values())
        print("    %-58s %s" % (rel, ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="").write(out)
    print("  renames: %d name(s) %s" % (total, "rewritten" if APPLY else "to rewrite"))


def declare():
    hp = ROOT / "tools" / "derive-schema-history.py"
    s = io.open(hp, encoding="utf-8", newline="").read()
    if '"to": "access.device_placement"' in s:
        print("  derive-schema-history.py: renames already declared")
        return
    block = "".join('    {"from": "%s", "to": "%s", "on": "%s",\n     "why": "%s"},\n'
                    % (o, n, RENAMED_ON, why.replace('"', "'")) for o, n, why in TABLES)
    marker = "\n]\n\n\ndef tables():"
    if marker not in s:
        print("  !! derive-schema-history.py: end of RENAMES not found; declare the renames by hand")
        return
    print("  derive-schema-history.py: %d rename(s) to declare" % len(TABLES))
    if APPLY:
        io.open(hp, "w", encoding="utf-8", newline="").write(s.replace(marker, "\n" + block.rstrip("\n") + marker, 1))


# --- ADR-0064: 429 on every operation -----------------------------------------------------------

VERBS = ("get", "put", "post", "patch", "delete", "head", "options")
REF_429 = "$ref: '../shared/common.yaml#/components/responses/TooManyRequests'"


def sweep_429():
    added = own = 0
    for p in sorted((ROOT / "contracts").rglob("*.yaml")):
        if p.parent.name == "shared":
            continue
        raw = io.open(p, encoding="utf-8", newline="").read()
        doc = yaml.safe_load(raw) or {}
        need = set()
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for verb, op in item.items():
                if verb not in VERBS or not isinstance(op, dict) or not op.get("operationId"):
                    continue
                rs = op.get("responses") or {}
                r429 = rs.get("429", rs.get(429))
                if r429 is None:
                    need.add((path, verb))
                elif isinstance(r429, dict) and "$ref" not in r429 and "Retry-After" not in (r429.get("headers") or {}):
                    own += 1
                    print("    %s.%s declares its own 429 without Retry-After" % (p.stem, op["operationId"]))
        if not need:
            continue
        nl = "\r\n" if "\r\n" in raw else "\n"     # a Windows checkout keeps CRLF, and so does the edit
        lines = raw.split(nl)
        out, i, n_here = [], 0, 0
        cur_path = cur_verb = None
        while i < len(lines):
            line = lines[i]
            m_path = re.match(r"^  (/\S*):\s*$", line) or re.match(r"^  '(/[^']*)':\s*$", line)
            if m_path:
                cur_path, cur_verb = m_path.group(1), None
            m_verb = re.match(r"^    (get|put|post|patch|delete|head|options):\s*$", line)
            if m_verb and cur_path is not None:
                cur_verb = m_verb.group(1)
            out.append(line)
            if (cur_path, cur_verb) in need and re.match(r"^      responses:\s*$", line):
                # the block is every following line indented deeper than `responses:` (or blank)
                j = i + 1
                while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > 6):
                    j += 1
                k = j
                while k > i + 1 and not lines[k - 1].strip():
                    k -= 1
                child = next((len(l) - len(l.lstrip()) for l in lines[i + 1:k] if l.strip()), 8)
                out.extend(lines[i + 1:k])
                out.append(" " * child + "'429':")
                out.append(" " * (child + 2) + REF_429)
                out.extend(lines[k:j])
                need.discard((cur_path, cur_verb))
                n_here += 1
                i = j
                continue
            i += 1
        if need:
            print("    !! %s: %d operation(s) whose responses block was not found: %s"
                  % (p.stem, len(need), sorted(need)[:3]))
        new = nl.join(out)
        # the edit must add responses and change nothing else
        before, after = yaml.safe_load(raw), yaml.safe_load(new)
        for path, item in (after.get("paths") or {}).items():
            for verb, op in item.items():
                if verb in VERBS and isinstance(op, dict):
                    (op.get("responses") or {}).pop("429", None)
        for path, item in (before.get("paths") or {}).items():
            for verb, op in item.items():
                if verb in VERBS and isinstance(op, dict):
                    (op.get("responses") or {}).pop("429", None)
        if before != after:
            print("    !! %s: the sweep changed more than responses; nothing written" % p.name)
            continue
        added += n_here
        print("    %-40s %d operation(s)" % (p.relative_to(ROOT).as_posix(), n_here))
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="").write(new)
    print("  429: %d operation(s) %s; %d declare their own 429 without Retry-After"
          % (added, "given the shared response" if APPLY else "to give the shared response", own))


def main():
    print("  ADR-0067 and ADR-0068 renames")
    renames()
    declare()
    print("\n  ADR-0064: 429 on every operation")
    sweep_429()
    if not APPLY:
        print("\n  nothing written - pass --apply")
    else:
        print("\n  Next: tools/refresh-safe.sh. derive-schema reads the new tags; the lineage, schema\n"
              "  reference and relationship graph were repointed above because none of them can\n"
              "  repoint itself.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
