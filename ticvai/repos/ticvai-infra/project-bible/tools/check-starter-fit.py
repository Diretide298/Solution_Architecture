#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The starter repositories a developer is handed, against the package that describes them.

**Audit class A-STARTER (docs/active/root-classes.md), roots R025-R040 and R249.** The setup zip
creates `ticvai-backend` and `ticvai-frontend` from ADAM's `viewer/mcp/setup/starters/`. The pull
audit found screens naming apps the starter does not have (R249, R037), a back office tagged one
runtime in the starter and another in the package (R031), standards documents describing types and
projects the starter code does not contain (R025, R028), two id rules (R030), empty package stubs
(R029), and a CLAUDE.md with no path for migration, DevOps or onboarding tickets and no warning that
`.adam/` is git-ignored (R033, R039). S002 fixed those at the source; nothing held them.

**It compares the starter with the authored spec, contracts and ADRs, and fails closed** (r13 system
review G-08, 3 November 2026; the lead's "All four, one release"; CHG-R14G-008). At r13 it passed with
no starters present, with `Money.cs` and `Id.cs` deleted and with a standards doc rewritten against
ADR-0008/0038, while the starter's only permission check failed 8 of the 22 normative vectors and its
api-conventions rule g carried the wording CR-367 had replaced. It compared the docs only with the
ticvai/repos/ mirror, which was equally stale. Now:

- a missing input (the starters, the frontend/backend/docs folders, op-descriptions.json, the
  permission vectors, ADR-0055, cross-deployable-writes.yaml) is a finding that cannot be baselined
  (SF-INPUTS); `--no-starters` says explicitly that a package-only checkout has no starters;
- the kernel the ADRs fix is held to them: the permission seam runs the spec's vectors file
  byte-for-byte (SF-VECTORS), Money carries its scale and goes on the wire as a decimal string with
  the contract's minor units (SF-MONEY), every transaction sets the three settings MIGRATIONS.md names
  with SET LOCAL (SF-RLS-CONTEXT), the tenant is the host's and a token is bound to it (SF-TENANT),
  the idempotency record is durable with a 409 on a conflicting reuse (SF-IDEMPOTENCY), the module map
  is ADR-0055's (SF-MODULES), CI runs every test project (SF-CI), ids are UUIDv7 on both sides
  (SF-ID-RULE), offline-core keeps one device's order under failure and concurrency (SF-OUTBOX-ORDER),
  and every type a standards doc names exists (SF-DOC-TYPES);
- a starter doc citing a change request that a later decision corrected, without citing the later one,
  is a finding (SF-SPEC-CR): how the CR-189 wording outlived CR-367.

`--run` also builds and tests the starters (dotnet test over the backend, pnpm/vitest over
offline-core, in a copy) and fails when a test project runs nothing; the gate runs the static rules,
the starters' own pipelines (.gitlab-ci.yml) run the tests. `--self-test` runs the review's sabotage
cases against a copy and expects each to fail.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (see tools/audit_guard.py).

    python3 tools/check-starter-fit.py [--all] [--update-baseline] [--no-starters] [--run] [--self-test]
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SF-INPUTS": "an input the comparison needs is missing (the starters, op-descriptions.json, the spec's vectors) (G-08)",
    "SF-APP-MISSING": "a screen's implementation.app has no app in the frontend starter (R249 R037)",
    "SF-APP-RUNTIME": "a starter app's platform tag disagrees with the package manifest's runtime (R031)",
    "SF-DOC-TYPES": "a standards doc names a type, member, project or host the starter code does not declare (R025 R028 G-08)",
    "SF-ID-RULE": "the starter carries a second id type beside UUIDv7, or lacks the UUIDv7 minting (ADR-0056) (R030 G-08)",
    "SF-EMPTY-STUB": "a shared frontend package is an empty `export {}` stub (R029)",
    "SF-CLAUDE-PATHS": "CLAUDE.md lacks the migration/DevOps paths or the .adam grep note (R033 R039)",
    "SF-DONE-GATES": "a Done-when gate names a command or runner the starter cannot run (R027 R032 R034)",
    "SF-OUTBOX-POLICIES": "a conflict policy the contracts use that offline-core does not declare (R035)",
    "SF-OUTBOX-ORDER": "offline-core can give two entries one sequence, strand a batch inFlight after a transient "
                       "failure, or pass its tests with none (ADR-0013) (G-04 D-05)",
    "SF-GLOSSARY": "a starter type named with a word the glossary bans (User for Principal) (R040)",
    "SF-FIXTURE-SEED": "a currency the reference fixture names has no denomination seed in "
                       "docs/active/seed-data-proposal.md (ADAM CR-159, CHG-CRA-001)",
    "SF-VECTORS": "the permission seam does not run the spec's permission-vectors.json, byte for byte, through "
                  "Permits and the deepest-entry lookup (spec 5 and 7.2, CR-367) (G-01)",
    "SF-SPEC-CR": "a starter doc cites a change request a later decision corrected, without the later one (G-02)",
    "SF-MONEY": "Money lacks its scale, its decimal-string wire form or the contract's minor units, or a doc "
                "prescribes a fixed decimal (ADR-0008, common.yaml Money, CR-192) (G-07)",
    "SF-RLS-CONTEXT": "a transaction does not set every connection-context setting MIGRATIONS.md names with "
                      "SET LOCAL, or something sets one on the session (G-03)",
    "SF-TENANT": "the tenant is not the host's, a tenant header is read or prescribed, the token is not bound "
                 "to the host's tenant, or one connection string serves the process (ADR-0038, C-05) (G-03)",
    "SF-IDEMPOTENCY": "the idempotency seam has no conflict outcome or durable record, or a doc makes Redis the "
                      "store (common.yaml IdempotencyKey, SD-024, CR-182) (G-06)",
    "SF-MODULES": "the architecture tests' module map is not ADR-0055's, or its compositions are not "
                  "cross-deployable-writes.yaml's (D-07)",
    "SF-CI": "a starter has no GitLab pipeline running its tests, a test project has no test, or a pipeline is "
             "green on the default branch by construction (G-05 D-07)",
}

# Backticked names a standards doc may use that the starter does not declare: framework and SDK names,
# build switches and the contract's own words. A kernel type is never on this list.
EXTERNAL_NAMES = {
    "BannedApiAnalyzers", "BannedSymbols", "CancellationToken", "DateTime", "DateTimeOffset", "DbContext",
    "EnforceCodeStyleInBuild", "Guid", "TimeProvider", "TimeZoneInfo", "TreatWarningsAsErrors", "Nullable",
    "IdempotencyKey", "PermissionVectors", "TICVAI", "Ticvai",
}

# The contradictions the review planted (G-08 run C) and their class: a doc line prescribing what an
# ADR forbids. A line that negates it ("never", "not", "no") is not one.
DOC_CONTRADICTIONS = [
    ("SF-MONEY", r"\b(money|amount)s?\b[^.|]{0,30}\b(is|are|as|use|uses|stored as)\b[^.|]{0,20}"
                 r"(bare decimal|decimal\s*\(\s*18\s*,\s*2\s*\)|fixed 2\s*dp|a float|double)", "ADR-0008: Money carries its scale"),
    ("SF-TENANT", r"tenant\b[^.|]{0,40}\b(comes from|is read from|is taken from|from|picked by|chosen by)\b[^.|]{0,30}"
                  r"\b(header|X-Tenant|X-Ticvai-Tenant)", "ADR-0038 / C-05: the tenant is the host's"),
    ("SF-IDEMPOTENCY", r"Redis in production|keys in Redis|Redis[^.|]{0,40}\b(store|guarantee)",
     "SD-024: the durable record in the change's transaction is the guarantee"),
    ("SF-RLS-CONTEXT", r"set on the connection|session-level SET|SET ticvai\.", "MIGRATIONS.md: SET LOCAL per transaction"),
]
NEGATION = re.compile(r"\b(never|not|no|nothing|without|instead of|refus\w*|rather than)\b", re.I)

STARTERS_DEFAULT = g.ROOT.parent / "viewer" / "mcp" / "setup" / "starters"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def code_files(root: Path, pattern: str):
    return [p for p in root.rglob(pattern) if "/obj/" not in p.as_posix() and "/bin/" not in p.as_posix()
            and "node_modules" not in p.as_posix()]


def strip_comments(cs: str) -> str:
    cs = re.sub(r"/\*.*?\*/", " ", cs, flags=re.S)
    return re.sub(r"//[^\n]*", " ", cs)


def adr0055_modules() -> dict:
    """The module map of ADR-0055's decision table: module -> deployable (ticvai-ai and workers hold none)."""
    adr = next(iter(sorted((g.ROOT / "docs" / "adr").glob("0055-*.md"))), None)
    out = {}
    for line in read(adr).splitlines() if adr else []:
        m = re.match(r"\|\s*`(commerce|access|operations)`\s*\|\s*([^|]+)\|", line)
        if not m:
            continue
        cell = re.sub(r"\([^)]*\)", "", m.group(2))
        for name in cell.split(","):
            name = name.strip().replace("&", "n").replace(" ", "")
            if name:
                out[name] = m.group(1)
    return out


def composed_modules() -> set:
    data = g.load_yaml(g.ROOT / "docs" / "active" / "cross-deployable-writes.yaml") or {}
    return {(r.get("reader"), re.sub(r"Service$", "", str(r.get("composes"))))
            for r in data.get("reads") or [] if isinstance(r, dict) and r.get("composes")}


def superseded_crs() -> dict:
    """CR-X -> {CR-Y}: a change entry for CR-Y says it corrects, replaces or supersedes CR-X."""
    out = {}
    for f in sorted((g.ROOT / "changes" / "entries").glob("*.yaml")):
        text = read(f)
        try:
            doc = g.load_yaml(f) or {}
        except Exception:
            continue
        later = re.findall(r"CR-\d+", str(doc.get("adam_cr") or ""))
        if not later:
            continue
        for m in re.finditer(r"\b(?:correct|replac|supersed)\w*\b([^.;]{0,140}?)\bCR-(\d+)", text):
            x = "CR-" + m.group(2)
            if x in later:
                continue  # the entry settles both
            for y in later:
                if y != x:
                    out.setdefault(x, set()).add(y)
    return out


def money_scales_from_contract() -> dict:
    """The fixed scales common.yaml's Money states: 'OMR uses 3 decimal places and AED uses 2'."""
    text = read(g.ROOT / "contracts" / "shared" / "common.yaml")
    out = {}
    for m in re.finditer(r"\b([A-Z]{3}) uses (\d)\b", text):
        out[m.group(1)] = int(m.group(2))
    return out


def minor_units(cs: str) -> dict:
    """CurrencyMinorUnits' list: the code groups and the scale each is added with."""
    groups = dict(re.findall(r'const string (\w+)\s*=\s*((?:"[^"]*"\s*\+?\s*)+);', cs))
    out = {}
    for name, scale in re.findall(r"\((\w+),\s*(\d)\)", cs):
        for code in re.findall(r"[A-Z]{3}", "".join(re.findall(r'"([^"]*)"', groups.get(name, "")))):
            out[code] = int(scale)
    return out


def check(starters: Path, guard, no_starters: bool = False) -> None:
    if not starters.exists():
        if no_starters:
            guard.note(f"--no-starters: no starter beside the package ({starters}); nothing compared")
            return
        guard.add("SF-INPUTS", "starters", f"no starters at {starters}: the comparison cannot run (pass --no-starters "
                                          f"only in a checkout that has no ADAM viewer)", strict=True)
        return
    fe, be, docs = starters / "frontend", starters / "backend", starters / "docs"
    for need in (fe, be, docs):
        if not need.exists():
            guard.add("SF-INPUTS", need.name, f"starters/{need.name}/ is missing", strict=True)
    spec_vectors = g.ROOT / "docs" / "architecture" / "specs" / "permission-vectors.json"
    op_desc = g.ROOT / "handoff" / "service-docs" / "op-descriptions.json"
    for need, why in ((spec_vectors, "the normative permission vectors"), (op_desc, "the tickets' Done-when lines"),
                      (g.ROOT / "docs" / "active" / "cross-deployable-writes.yaml", "the module compositions")):
        if not need.exists():
            guard.add("SF-INPUTS", need.name, f"{need.relative_to(g.ROOT).as_posix()} ({why}) is missing", strict=True)
    if not adr0055_modules():
        guard.add("SF-INPUTS", "ADR-0055", "ADR-0055's module table could not be read", strict=True)

    apps = {p.parent.name: p for p in (fe / "apps").glob("*/project.json")}
    for plat, s in g.screens():
        app = ((s.get("implementation") or {}).get("app"))
        if app and app not in apps:
            guard.add("SF-APP-MISSING", f"{app}", f"screens name app {app!r} (e.g. {s['id']}); the frontend starter has no apps/{app}")

    for m in sorted((g.ROOT / "frontend").glob("*.yaml")):
        man = g.load_yaml(m) or {}
        app = man.get("app") or m.stem
        if app not in apps:
            if app not in {k.split(":")[0] for k in guard.found.get("SF-APP-MISSING", {})}:
                guard.add("SF-APP-MISSING", app, f"frontend/{m.name} describes {app!r}; the frontend starter has no apps/{app}")
            continue
        try:
            tags = json.loads(apps[app].read_text(encoding="utf-8")).get("tags") or []
        except Exception:
            tags = []
        plat_tag = next((t.split(":", 1)[1] for t in tags if str(t).startswith("platform:")), None)
        runtime = str(man.get("runtime") or "")
        want = "web" if runtime.lower().endswith("web") or man.get("formFactor") == "web" else "native"
        tag_kind = "web" if plat_tag in ("web", "desktop", "browser") else "native"
        if plat_tag and tag_kind != want:
            guard.add("SF-APP-RUNTIME", app, f"apps/{app} is tagged platform:{plat_tag}; frontend/{m.name} says runtime {runtime}")

    src_files = code_files(be / "src", "*.cs")
    test_files = code_files(be / "tests", "*.cs")
    code = " ".join(read(p) for p in src_files)
    all_code = strip_comments(" ".join(read(p) for p in src_files + test_files))
    declared = set(re.findall(r"\b(?:interface|class|record|struct|enum)\s+([A-Z]\w+)", code + " " + all_code))
    identifiers = set(re.findall(r"\b[A-Z]\w*\b", all_code))
    projects = {p.stem for p in code_files(be, "*.csproj")}
    module_map = json.loads(read(be / "tests" / "TICVAI.ArchitectureTests" / "modules.json") or "{}")
    module_names = {m.get("name") for m in module_map.get("modules") or []}

    # SF-DOC-TYPES: "Where a type is named here, it exists there" (backend-patterns.md line 6), for every name.
    for doc in [docs / "backend-patterns.md", be / "CLAUDE.md"]:
        if not doc.exists():
            continue
        text = read(doc)
        for t in sorted(set(re.findall(r"`([A-Z][A-Za-z0-9]+)(?:<\w+>)?(?:\.\w+(?:\(\))?)?`", text))):
            if t.isupper() or t in EXTERNAL_NAMES or t in module_names:
                continue
            if t not in declared and t not in identifiers:
                guard.add("SF-DOC-TYPES", f"{doc.name}:{t}", f"{doc.name} names {t}; no backend starter file declares or uses it")
        for proj in sorted(set(re.findall(r"`((?:TICVAI|Ticvai)\.[A-Z][A-Za-z.]+)`", text))):
            if proj not in projects and not any(proj.startswith(p + ".") for p in projects):
                guard.add("SF-DOC-TYPES", f"{doc.name}:{proj}", f"{doc.name} names project {proj}; the starter has {', '.join(sorted(projects))}")
        for host in sorted(set(re.findall(r"`([a-z]+)` host\b", text))):
            if not any(p.lower().endswith("." + host) for p in projects):
                guard.add("SF-DOC-TYPES", f"{doc.name}:host:{host}", f"{doc.name} names the `{host}` host; the starter has no TICVAI.{host.title()} project")

    # SF-ID-RULE (ADR-0056): UUIDv7 on both sides, and nothing else.
    if re.search(r"\b(Ulid|ULID)\w*", code):
        guard.add("SF-ID-RULE", "backend:Ulid", "the backend starter still declares or uses a ULID type (ADR-0056: UUIDv7 only)")
    if "Guid.CreateVersion7" not in read(be / "src" / "TICVAI.Domain" / "Identity" / "Id.cs"):
        guard.add("SF-ID-RULE", "backend:Id.New", "TICVAI.Domain/Identity/Id.cs is missing or does not mint with Guid.CreateVersion7()")
    if "M:System.Guid.NewGuid" not in read(be / "BannedSymbols.txt"):
        guard.add("SF-ID-RULE", "backend:banned", "BannedSymbols.txt no longer bans Guid.NewGuid()")
    id_ts = read(fe / "packages" / "offline-core" / "src" / "id.ts")
    if not re.search(r"\bv7\b", id_ts) or re.search(r"\bv4\b|randomUUID|NewGuid|Math\.random\(\)", strip_comments(id_ts)):
        guard.add("SF-ID-RULE", "offline-core:newId", "offline-core/src/id.ts does not mint UUIDv7 with uuid's v7 only")
    for d in sorted(docs.glob("*.md")):
        for line in read(d).split("\n"):
            if re.search(r"\bULID\b|\bUlid", line) and not re.search(r"not|never|instead|replac|was|superseded", line, re.I):
                guard.add("SF-ID-RULE", f"{d.name}", f"{d.name} prescribes a ULID: {line.strip()[:80]}")
                break

    for pkg in sorted((fe / "packages").glob("*/src/index.ts")):
        if re.fullmatch(r"\s*export\s*\{\s*\}\s*;?\s*", read(pkg)):
            guard.add("SF-EMPTY-STUB", pkg.parent.parent.name, f"packages/{pkg.parent.parent.name} is `export {{}}`")

    for repo, needs in (("backend", [r"MIG-", r"SETUP-", r"\.adam/"]), ("frontend", [r"\.adam/"])):
        text = read(starters / repo / "CLAUDE.md")
        for pat in needs:
            if not re.search(pat, text):
                guard.add("SF-CLAUDE-PATHS", f"{repo}:{pat}", f"{repo}/CLAUDE.md never mentions {pat.replace(chr(92), '')}")
        if ".adam/" in text and not re.search(r"(git-?ignored|--no-ignore|skips it)", text):
            guard.add("SF-CLAUDE-PATHS", f"{repo}:grep-note", f"{repo}/CLAUDE.md mentions .adam/ without saying Grep skips it")

    # R027 R032 R034: what the tickets' Done-when lines ask a developer to run.
    desc = g.load_json(op_desc, {}) or {}
    blob = "\n".join(desc.values())
    try:
        scripts = json.loads(read(fe / "package.json") or "{}").get("scripts") or {}
    except Exception:
        scripts = {}
    for cmd in sorted(set(re.findall(r"`pnpm (\w+)`", blob))):
        if cmd not in scripts:
            guard.add("SF-DONE-GATES", f"pnpm:{cmd}", f"tickets ask for `pnpm {cmd}`; frontend package.json has no {cmd} script")
    # CHG-RPO-003: a screen built in a repository whose layout was read is gated by that repository's own package
    # manager and scripts (frontend_repos.profile), not the one-workspace starter's: #27741's guest app is npm with no
    # typecheck script, and its tickets asked for `pnpm typecheck`.
    sys.path.insert(0, str(g.ROOT / "tools"))
    import frontend_repos as fr  # noqa: E402
    idx = fr.screen_index()
    for key, text in sorted(desc.items()):
        gates = [l for l in str(text).splitlines() if l.startswith("- [ ]") and
                 re.search(r"\bpnpm\b|\bnpm\b|\byarn\b|typecheck|scripts pass", l)]
        if not gates:
            continue
        for sid in sorted(set(re.findall(r"^### ([A-Z]{2,5}-\d{3,4}) ", str(text), re.M))):
            p = fr.profile((idx.get(sid) or {}).get("platform") or "")
            if not p.get("read"):
                continue
            pm = str(p.get("packageManager") or "")
            lack = [k for k, v in (p.get("scripts") or {}).items() if v in ("none", False)]
            for l in gates:
                other = [m for m in re.findall(r"`(pnpm|npm|yarn)\b", l) if m != pm]
                missing = [k for k in lack if re.search(rf"`[a-z]+ (run )?{k}`", l)]
                if other or missing:
                    guard.add("SF-DONE-GATES", f"{key}:{sid}",
                              f"ticket {key} ({sid}) gates {p['repo']} with {l[6:90]!r}; the repository uses {pm}"
                              + (f" and has no {', '.join(missing)} script" if missing else ""))
                    break
    tests = [p for p in code_files(be, "*.csproj") if "Tests" in p.stem]
    if "dotnet test" in blob and not tests:
        guard.add("SF-DONE-GATES", "dotnet:test", "tickets ask for `dotnet test`; the backend starter has no test project")
    for runner in sorted(set(re.findall(r"`?\b([A-Z][A-Za-z]+Runner)\b`?", blob))):
        if runner not in declared:
            guard.add("SF-DONE-GATES", f"runner:{runner}", f"tickets name {runner}; no backend starter file declares it")
    if re.search(r"reference fixture", blob, re.I) and not any(
            re.search(r"fixture", p.name, re.I) for p in list(be.rglob("*")) if "/obj/" not in p.as_posix()):
        guard.add("SF-DONE-GATES", "fixture", "tickets require the reference fixture; nothing in the backend "
                                              "starter is named for it (SETUP-SEED builds it)")

    # **Every currency the fixture runs in has its cash seeded** (ADAM CR-159, 18 October 2026; CHG-CRA-001). Quality
    # gates 8 runs every test on AED and OMR, and the only denomination seed was the UAE's, so a shift count or a
    # cash-up in Muscat had nothing to count. A seed section is a heading of seed-data-proposal.md naming
    # denominations and the currency code in brackets ("## 1. UAE denominations (AED)").
    fixture_text = " ".join(read(p) for p in (docs / "quality-gates.md", be / "db" / "seed" / "reference-fixture.md"))
    m = re.search(r"((?:[A-Z]{3}(?:, | and | or ))+[A-Z]{3})\b", fixture_text)
    fixture_ccy = sorted(set(re.findall(r"\b[A-Z]{3}\b", m.group(1)))) if m else []
    seed_doc = g.ROOT / "docs" / "active" / "seed-data-proposal.md"
    seeded = set(re.findall(r"^#+ .*denominations? \(([A-Z]{3})\)", read(seed_doc), re.M | re.I))
    for ccy in fixture_ccy:
        if ccy not in seeded:
            guard.add("SF-FIXTURE-SEED", ccy, f"the reference fixture runs in {ccy}; docs/active/seed-data-proposal.md "
                                              f"has no denominations section for it, so SETUP-SEED has no cash to seed")

    # R035: the conflict policies offline-core must carry through its outbox.
    oc = fe / "packages" / "offline-core" / "src"
    oc_text = " ".join(read(p) for p in oc.glob("*.ts")) if oc.exists() else ""
    used = {str(f["op"].get("x-ticvai-conflict-policy")) for f in g.operations().values()
            if f["op"].get("x-ticvai-offline-capable") and f["op"].get("x-ticvai-conflict-policy")}
    for pol in sorted(used):
        if f"'{pol}'" not in oc_text and f'"{pol}"' not in oc_text:
            guard.add("SF-OUTBOX-POLICIES", pol, f"offline operations use conflict policy {pol!r}; "
                                                 f"offline-core's ConflictPolicy does not declare it")

    # SF-OUTBOX-ORDER (G-04, D-05; ADR-0013): one device's writes reach the server in sequence order, once each.
    outbox_ts = strip_comments(read(oc / "outbox.ts"))
    orchestrator_ts = strip_comments(read(oc / "sync-orchestrator.ts"))
    if not re.search(r"CREATE UNIQUE INDEX[^;]*\(\s*sequence\s*\)", outbox_ts):
        guard.add("SF-OUTBOX-ORDER", "unique-sequence", "offline-core's outbox has no UNIQUE(sequence)")
    enqueue = re.search(r"async enqueue\b[\s\S]*?\n  \}", outbox_ts)
    if not enqueue or ".transaction(" not in enqueue.group(0):
        guard.add("SF-OUTBOX-ORDER", "enqueue-transaction", "offline-core allocates the sequence and inserts outside one transaction")
    if re.search(r"markInFlight\(\s*batch", orchestrator_ts) or "markInFlight([entry.id])" not in orchestrator_ts:
        guard.add("SF-OUTBOX-ORDER", "in-flight", "the orchestrator marks more than the entry it is sending inFlight, so a "
                                                  "halt strands the rest and later entries overtake them")
    for name in ("outbox.test.ts", "sync-orchestrator.test.ts"):
        if not (oc / name).exists():
            guard.add("SF-OUTBOX-ORDER", f"test:{name}", f"offline-core has no {name}")
    for pj in sorted((fe / "packages").glob("*/project.json")):
        has_tests = any(pj.parent.glob("src/**/*.test.ts"))
        if has_tests and "--passWithNoTests" in read(pj):
            guard.add("SF-OUTBOX-ORDER", f"pass-with-no-tests:{pj.parent.name}", f"packages/{pj.parent.name} has tests and still "
                                                                              f"passes with none (--passWithNoTests)")

    # R040: naming-and-style section 3 - Principal, never User.
    for t in sorted(declared):
        if re.search(r"User(?!Agent)", t) and not t.startswith("Test"):
            guard.add("SF-GLOSSARY", t, f"backend starter declares {t}; the glossary says Principal, never User")

    sec = be / "src" / "TICVAI.Application" / "Abstractions" / "Security"

    # SF-VECTORS (G-01): the seam operations decide with is the spec's algorithm, proven on the spec's own vectors.
    starter_vectors = be / "tests" / "TICVAI.UnitTests" / "PermissionVectors.json"
    norm = lambda t: t.replace("\r\n", "\n").strip()  # noqa: E731
    if spec_vectors.exists() and norm(read(starter_vectors)) != norm(read(spec_vectors)):
        guard.add("SF-VECTORS", "PermissionVectors.json", "tests/TICVAI.UnitTests/PermissionVectors.json is missing or differs "
                                                          "from docs/architecture/specs/permission-vectors.json")
    vector_tests = [p for p in test_files if "PermissionVectors.json" in read(p)]
    if not any(".Permits(" in read(p) and "PermissionsByScopeLookup.Holds(" in read(p) for p in vector_tests):
        guard.add("SF-VECTORS", "vector-test", "no unit test runs PermissionVectors.json through ResolvedAuthority.Permits "
                                               "and PermissionsByScopeLookup.Holds")
    authority = strip_comments(read(sec / "ResolvedAuthority.cs"))
    if not (re.search(r"bool Permits\(string permission, string scopePath\)", authority)
            and "GrantEffect.Deny" in authority and "Grant.Wildcard" in authority):
        guard.add("SF-VECTORS", "ResolvedAuthority", "ResolvedAuthority.Permits(permission, scopePath) with deny-wins and the "
                                                     "wildcard deny is missing")
    principal = strip_comments(read(sec / "ICurrentPrincipal.cs"))
    if "Permits(string permission, string scopePath)" not in principal or re.search(r"\bbool Has\(", principal):
        guard.add("SF-VECTORS", "ICurrentPrincipal", "ICurrentPrincipal must decide with Permits(permission, scopePath) and "
                                                     "offer no flat Has(permission)")
    for d in sorted(docs.glob("*.md")) + [be / "CLAUDE.md", fe / "CLAUDE.md"]:
        for i, line in enumerate(read(d).split("\n"), 1):
            if re.search(r"\.Has\(\"[A-Z_]+\"\)", line):
                guard.add("SF-VECTORS", f"{d.name}:{i}", f"{d.name}:{i} decides a permission with a flat Has(): {line.strip()[:80]}")

    # SF-SPEC-CR (G-02): a rule restated from a spec moves when the spec does.
    later = superseded_crs()
    for d in sorted(docs.glob("*.md")) + [be / "CLAUDE.md", fe / "CLAUDE.md", starters / "ai" / "CLAUDE.md",
                                          fe / ".eslintrc.cjs"]:
        for i, line in enumerate(read(d).split("\n"), 1):
            cited = set(re.findall(r"CR-\d+", line))
            for x in sorted(cited):
                missing = sorted(later.get(x, set()) - cited)
                if missing:
                    guard.add("SF-SPEC-CR", f"{d.name}:{x}", f"{d.name}:{i} restates {x}, which {', '.join(missing)} "
                                                             f"corrected; restate it from the spec and cite {', '.join(missing)}")

    # SF-MONEY (G-07): ADR-0008 and common.yaml Money.
    money = strip_comments(read(be / "src" / "TICVAI.Domain" / "ValueObjects" / "Money.cs"))
    converter = read(be / "src" / "TICVAI.Domain" / "ValueObjects" / "MoneyJsonConverter.cs")
    if not re.search(r"\bint Scale\b", money):
        guard.add("SF-MONEY", "Money.Scale", "TICVAI.Domain Money has no Scale (ADR-0008: { amount, currency, scale })")
    if "JsonConverter(typeof(MoneyJsonConverter))" not in money or 'WriteString("amount"' not in converter \
            or 'WriteNumber("scale"' not in converter:
        guard.add("SF-MONEY", "Money.wire", "Money is not written as {amount: decimal string, currency, scale} by "
                                            "MoneyJsonConverter (common.yaml Money)")
    units = minor_units(read(be / "src" / "TICVAI.Domain" / "ValueObjects" / "CurrencyMinorUnits.cs"))
    for ccy, scale in sorted(money_scales_from_contract().items()):
        if units.get(ccy) != scale:
            guard.add("SF-MONEY", f"minor-units:{ccy}", f"common.yaml says {ccy} uses {scale} decimal places; the kernel's "
                                                        f"CurrencyMinorUnits has {units.get(ccy)}")
    if "Allocate(" not in money:
        guard.add("SF-MONEY", "Money.Allocate", "Money has no Allocate (ADR-0008: allocation distributes the remainder)")

    # SF-RLS-CONTEXT (G-03): MIGRATIONS.md "The connection context".
    mig = read(g.ROOT / "backend" / "MIGRATIONS.md")
    section = re.search(r"## The connection context(.*?)\n## ", mig, re.S)
    settings = sorted(set(re.findall(r"`(ticvai\.[a-z_]+)`", section.group(1)))) if section else []
    infra_code = strip_comments(" ".join(read(p) for p in code_files(be / "src" / "TICVAI.Infrastructure", "*.cs")))
    for setting in settings:
        if not re.search(rf"set_config\('{re.escape(setting)}',\s*@\w+,\s*true\)|SET LOCAL {re.escape(setting)}\b", infra_code):
            guard.add("SF-RLS-CONTEXT", setting, f"no Infrastructure code sets {setting} with SET LOCAL (set_config(..., true)) "
                                                 f"at the start of a transaction")
    if "DbTransactionInterceptor" not in infra_code:
        guard.add("SF-RLS-CONTEXT", "interceptor", "no transaction interceptor sets the context when a transaction begins")
    if re.search(r"set_config\('ticvai\.[a-z_]+',[^)]*,\s*false\)|\bSET\s+(SESSION\s+)?ticvai\.", strip_comments(code), re.I):
        guard.add("SF-RLS-CONTEXT", "session-set", "starter code sets a ticvai.* setting on the session, which a pooled "
                                                   "connection carries into the next request")

    # SF-TENANT (G-03, C-05): ADR-0038, resolveTenantHost, the token bound to the host's tenant.
    src_strip = strip_comments(code)
    if re.search(r"X-(?:Ticvai-)?Tenant(?:-Id)?", src_strip, re.I):
        guard.add("SF-TENANT", "header", "starter code reads a tenant header; the tenant is the request's host's")
    if not re.search(r"Request\.Host", src_strip) or "ITenantDirectory" not in src_strip:
        guard.add("SF-TENANT", "host", "nothing resolves the request's host to its tenant (ITenantDirectory)")
    binding = strip_comments(read(be / "src" / "TICVAI.Infrastructure" / "Tenancy" / "TenantBinding.cs"))
    if not ('"tenant"' in binding and '"tid"' in binding and '"sid"' in binding and "TenantId" in binding):
        guard.add("SF-TENANT", "binding", "no TenantBinding refuses a token whose tenant (tid) or session is another tenant's")
    if not re.search(r"OnTokenValidated[\s\S]{0,400}TenantBinding", src_strip):
        guard.add("SF-TENANT", "pipeline", "authentication does not apply TenantBinding when a token is validated")
    if re.search(r"GetValue<string>\(\s*nameof\(\w*\.ConnectionString\)\)|\"Database:ConnectionString\"|UseNpgsql\(connectionString\)", src_strip):
        guard.add("SF-TENANT", "one-database", "one connection string serves the process (ADR-0038: a database per tenant)")
    if "Guid TenantId" not in strip_comments(read(sec / "ITenantContext.cs")):
        guard.add("SF-TENANT", "TenantId:Guid", "ITenantContext.TenantId is not a Guid (ADR-0056: one id type)")

    # SF-IDEMPOTENCY (G-06): common.yaml IdempotencyKey, SD-024, CR-182.
    persistence = be / "src" / "TICVAI.Application" / "Abstractions" / "Persistence"
    execution = strip_comments(read(persistence / "IdempotentExecution.cs"))
    if not re.search(r"\bConflict\b", execution) or "RecordAsync" not in execution or "ITransactionRunner" not in execution:
        guard.add("SF-IDEMPOTENCY", "execution", "IdempotentExecution with a conflict outcome and the record written in the "
                                                 "change's transaction is missing")
    if "platform.idempotency_record" not in infra_code or "UniqueViolation" not in infra_code:
        guard.add("SF-IDEMPOTENCY", "durable", "no store writes platform.idempotency_record and turns its unique index into a replay")
    if re.search(r"AddSingleton<IIdempotencyStore,\s*InMemoryIdempotencyStore>", src_strip):
        guard.add("SF-IDEMPOTENCY", "in-memory", "the in-memory idempotency store is registered for the API")

    for rule, pattern, why in DOC_CONTRADICTIONS:
        for d in sorted(docs.glob("*.md")) + [be / "CLAUDE.md", be / "README.md", fe / "CLAUDE.md"]:
            for i, line in enumerate(read(d).split("\n"), 1):
                if re.search(pattern, line, re.I) and not NEGATION.search(line):
                    guard.add(rule, f"{d.name}:{i}", f"{d.name}:{i} contradicts {why}: {line.strip()[:90]}")

    # SF-MODULES (D-07): ADR-0055's map and the recorded compositions.
    want = adr0055_modules()
    have = {m.get("name"): m.get("deployable") for m in module_map.get("modules") or []}
    if want and have != want:
        for name in sorted(set(want) | set(have)):
            if want.get(name) != have.get(name):
                guard.add("SF-MODULES", name, f"modules.json has {name} in {have.get(name)}; ADR-0055 has it in {want.get(name)}")
    want_c = composed_modules()
    have_c = {(c.get("reader"), c.get("module")) for c in module_map.get("composes") or []}
    for pair in sorted((want_c ^ have_c), key=str):
        side = "cross-deployable-writes.yaml" if pair in want_c else "modules.json"
        guard.add("SF-MODULES", f"composes:{pair[0]}:{pair[1]}", f"the {pair[0]} host composing {pair[1]} is only in {side}")
    if "ModuleBoundaryTests" not in declared or "Planted" not in " ".join(p.as_posix() for p in test_files):
        guard.add("SF-MODULES", "test", "ModuleBoundaryTests, with its planted violations, is missing")

    # SF-CI (G-05, D-07): the gates the standards call blocking run where the code lives.
    be_ci, fe_ci = read(be / ".gitlab-ci.yml"), read(fe / ".gitlab-ci.yml")
    if not re.search(r"dotnet test", be_ci) or "TICVAI_REQUIRE_DATABASE" not in be_ci or "ran no tests" not in be_ci:
        guard.add("SF-CI", "backend", "backend/.gitlab-ci.yml does not run every test project against PostgreSQL and fail "
                                      "an empty one")
    if not all(t in fe_ci for t in ("lint", "typecheck", "test")) or re.search(r"--base=origin/main", fe_ci) \
            or "run-many" not in fe_ci:
        guard.add("SF-CI", "frontend", "frontend/.gitlab-ci.yml does not run lint, typecheck and test on every project on "
                                       "the default branch")
    for wf in sorted(starters.glob("*/.github/workflows/*")):
        guard.add("SF-CI", f"github:{wf.parent.parent.parent.name}", f"{wf.relative_to(starters).as_posix()}: GitLab never "
                                                                     f"runs a GitHub workflow")
    for proj in sorted(code_files(be / "tests", "*.csproj")):
        if not any(re.search(r"\[(Fact|Theory|DatabaseFact)\b", read(p)) for p in code_files(proj.parent, "*.cs")):
            guard.add("SF-CI", f"empty:{proj.stem}", f"{proj.stem} has no test: `dotnet test` passes it by finding nothing")


def run_behaviour(starters: Path) -> int:
    """--run: build and test a copy of the starters. Fails on a red test or a test project that runs none."""
    fails = 0
    with tempfile.TemporaryDirectory(prefix="starter-fit-") as tmp:
        be = Path(tmp) / "backend"
        shutil.copytree(starters / "backend", be, ignore=shutil.ignore_patterns("bin", "obj", "TestResults"))
        res = Path(tmp) / "trx"
        p = subprocess.run(["dotnet", "test", "TICVAI-Backend.slnx", "--logger", "trx", "--results-directory", str(res)],
                           cwd=be, capture_output=True, text=True, encoding="utf-8", errors="replace")
        summary = [l.strip() for l in p.stdout.splitlines() if re.search(r"Passed!|Failed!|No test is available|error", l)]
        print("backend:", *summary, sep="\n  ")
        ran = " ".join(read(t) for t in res.glob("*.trx"))
        for proj in sorted((be / "tests").glob("*/*.csproj")):
            if proj.stem not in ran:
                print(f"  FAIL {proj.stem} ran no tests")
                fails += 1
        if p.returncode != 0:
            fails += 1
        if not re.search(r'testName="[^"]*PermissionVectorTests\.The_seam_answers[^"]*V28', ran):
            print("  FAIL the permission vectors did not run through the seam")
            fails += 1
        fe = starters / "frontend"
        npx = shutil.which("pnpm")
        if npx and (fe / "node_modules").exists():
            q = subprocess.run([npx, "--dir", str(fe / "packages" / "offline-core"), "exec", "vitest", "run"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            print("offline-core:", q.stdout.strip().splitlines()[-3:] if q.stdout else q.stderr[-300:])
            fails += q.returncode != 0
        else:
            print("offline-core: not installed here (pnpm install in a copy runs it; its pipeline runs it)")
    print("PASS - the starters build and test" if not fails else f"FAIL - {fails} behavioural failure(s)")
    return 1 if fails else 0


SABOTAGE = {
    # The review's runs (G-08): each must fail the check.
    "no starters": (lambda s: shutil.rmtree(s), {"SF-INPUTS"}),
    "Money.cs deleted": (lambda s: (s / "backend/src/TICVAI.Domain/ValueObjects/Money.cs").unlink(), {"SF-MONEY"}),
    "Id.cs deleted": (lambda s: (s / "backend/src/TICVAI.Domain/Identity/Id.cs").unlink(), {"SF-ID-RULE"}),
    "offline id.ts mints Guid.NewGuid()": (lambda s: _edit(s / "frontend/packages/offline-core/src/id.ts",
                                                          "return uuidv7();", "return Guid.NewGuid();"), {"SF-ID-RULE"}),
    "doc: bare decimal(18,2), tenant from a header": (
        lambda s: _append(s / "docs/backend-patterns.md",
                          "\nMoney is a bare decimal(18,2); tenant comes from the X-Tenant-Id header.\n"),
        {"SF-MONEY", "SF-TENANT"}),
    "rule g back in the CR-189 wording": (lambda s: _edit(s / "docs/api-conventions.md", "(CR-189, CR-367)", "(CR-189)"),
                                          {"SF-SPEC-CR"}),
    "a flat Has() permission check": (lambda s: _edit(s / "backend/src/TICVAI.Application/Abstractions/Security/ICurrentPrincipal.cs",
                                                     "ResolvedAuthority Authority { get; }",
                                                     "ResolvedAuthority Authority { get; }\n    bool Has(string permission);"),
                                      {"SF-VECTORS"}),
    "vectors drift from the spec": (lambda s: _edit(s / "backend/tests/TICVAI.UnitTests/PermissionVectors.json",
                                                   '"expect": "DENY"', '"expect": "PERMIT"'), {"SF-VECTORS"}),
    "session-level SET": (lambda s: _edit(s / "backend/src/TICVAI.Infrastructure/Persistence/ScopeContextInterceptor.cs",
                                          "@scope_paths, true)", "@scope_paths, false)"), {"SF-RLS-CONTEXT"}),
    "a tenant header read": (lambda s: _append(s / "backend/src/TICVAI.Api/Middleware/TenantResolutionMiddleware.cs",
                                               '\ninternal static class H { public const string T = "X-Ticvai-Tenant"; }\n'),
                             {"SF-TENANT"}),
    "idempotency store in memory for the API": (
        lambda s: _edit(s / "backend/src/TICVAI.Infrastructure/DependencyInjection/ServiceCollectionExtensions.cs",
                        "AddScoped<IIdempotencyStore, PostgresIdempotencyStore>()",
                        "AddSingleton<IIdempotencyStore, InMemoryIdempotencyStore>()"), {"SF-IDEMPOTENCY"}),
    "a module missing from the map": (lambda s: _edit(s / "backend/tests/TICVAI.ArchitectureTests/modules.json",
                                                     '    { "name": "Wallet", "deployable": "commerce" },\n', ""),
                                      {"SF-MODULES"}),
    "an empty integration test project": (lambda s: [p.unlink() for p in (s / "backend/tests/TICVAI.IntegrationTests").glob("*.cs")],
                                          {"SF-CI"}),
    "the whole batch marked inFlight again": (
        lambda s: _edit(s / "frontend/packages/offline-core/src/sync-orchestrator.ts", "markInFlight([entry.id])", "markInFlight(batch.map((e) => e.id))"),
        {"SF-OUTBOX-ORDER"}),
    "a doc naming a type that does not exist": (lambda s: _append(s / "docs/backend-patterns.md",
                                                                 "\nUse `ScopeNode` for a node.\n"), {"SF-DOC-TYPES"}),
}


def _edit(p: Path, old: str, new: str):
    t = p.read_text(encoding="utf-8")
    t2 = t.replace(old.replace("\n", "\r\n"), new) if old.replace("\n", "\r\n") in t else t.replace(old, new)
    if t2 == t:
        raise AssertionError(f"self-test sabotage found nothing to change in {p}: {old!r}")
    p.write_text(t2, encoding="utf-8")


def _append(p: Path, text: str):
    p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")


def self_test() -> int:
    bad = 0
    for name, (sabotage, expect) in SABOTAGE.items():
        with tempfile.TemporaryDirectory(prefix="starter-fit-self-") as tmp:
            copy = Path(tmp) / "starters"
            shutil.copytree(STARTERS_DEFAULT, copy, ignore=shutil.ignore_patterns("bin", "obj", "node_modules", "TestResults"))
            clean = g.Guard("check-starter-fit", RULES)
            check(copy, clean)
            before = {r for r, k in clean.found.items() if k}
            sabotage(copy)
            guard = g.Guard("check-starter-fit", RULES)
            check(copy, guard)
            fired = {r for r, k in guard.found.items() if k}
            got = {r for r in fired if len(guard.found[r]) > len(clean.found.get(r, {}))} | (fired - before)
            ok = expect <= got
            bad += not ok
            print(f"  {'ok  ' if ok else 'FAIL'} {name}: expected {sorted(expect)}, the check found {sorted(got) or 'nothing new'}")
    print("PASS - every sabotage case fails the check" if not bad else f"FAIL - {bad} sabotage case(s) passed the check")
    return 1 if bad else 0


def main() -> int:
    g.force_utf8()
    if "--self-test" in sys.argv:
        return self_test()
    if "--run" in sys.argv:
        return run_behaviour(STARTERS_DEFAULT)
    guard = g.Guard("check-starter-fit", RULES)
    check(STARTERS_DEFAULT, guard, no_starters="--no-starters" in sys.argv)
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
