#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run each refresh step that writes into an authored input twice, and fail if the second run changes anything.

**Why** (20 October 2026, r8 second fix round, generators lane extra item 2, CHG-R8GEN-002). Some refresh steps write
into files people also author: the screens, the flows, the contracts' `x-ticvai-consumed-by`, roles-by-app.yaml, the
lineage, the screen id register, the service decomposition's counts. A step like that is only safe in a rebuild if it
is a fixed point: run on its own output it must write the same bytes. One that is not either flips a value back and
forth between refreshes or grows a file every run, and the difference lands in a commit as a change nobody made.
`refresh.sh` says "all six are idempotent" about the screen tools; this measures it instead of saying it.

**What it does.** For each step in `WRITE_BACK` (the list in the r8 generators report, item 1): keep every file the
step may write (its `writes` globs), run the step, keep them again, run it a second time, and compare. A file the
second run changed is a finding (RT-UNSTABLE), with the first lines that differ. A file the first run changed is
reported as a note: the tree was not at a refreshed state for that step, which is expected on a branch and is what the
refresh is for. A step that fails to run is RT-ERROR. Afterwards every file is put back as it was before the first
run, and a file the step created is removed, so the check leaves the package as it found it (`--keep` leaves the
first run's output instead, which is what a refresh would have written).

    python tools/check-regenerate-twice.py                 # every step in WRITE_BACK
    python tools/check-regenerate-twice.py --steps derive-lineage,link-screens-contracts
    python tools/check-regenerate-twice.py --list          # the steps and what each writes
    python tools/check-regenerate-twice.py --self-test     # the comparison on made-up files (also run first, always)
    python tools/check-regenerate-twice.py --chain        # what run-checks runs, after a refresh

**`--chain` is the form for a refreshed tree** (CHG-R8GEN-017). It runs every step once more, in refresh order, and
fails on a file the whole chain leaves different (RT-CHAIN), naming the steps that changed it. A step on its own need
not be a fixed point of the refreshed tree: derive-transitions-from-flows rewrites its edges without `carries` and
derive-carries-from-entrystate, after it, puts them back, so `--once` fails on a refresh that is in fact stable. The
chain form found the one real case on 20 October: derive-entrystate-params ran after derive-carries-from-entrystate,
so a parameter it added (ADM-018 challengeId) was carried only by the following refresh; refresh.sh now runs it first.

**`--once` is the form for a refreshed tree.** run-checks runs after refresh.sh, so each step has already run once on
its own output's inputs: one more run that changes anything is the second run changing something, and is a finding.
On a branch that was not refreshed, use the default (twice): the first run's changes are only noted. `--skip-slow`
leaves out the steps in SLOW (none since link-screens-contracts went from eleven minutes to 34 seconds, CHG-R8GEN-016).

**The diagrams are in the chain** (P-31, CHG-R11DES-002). derive-diagrams writes no authored input, but it draws the
screens, flows and contracts the steps above write, and it ran before them in refresh.sh, so each refresh drew the
previous run's screens (r10, fixed by hand in cd306cce). It is the last step here, as in refresh.sh: a diagram the
chain changes is RT-CHAIN, which is a second regeneration changing a diagram.

It writes into the package while it runs, so run-checks.py runs it alone (SERIAL) and it never runs beside a refresh.
"""
import argparse
import difflib
import glob
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The refresh steps that write into authored inputs, in refresh.sh order, with the files each may write. Kept beside
# the list in the generators report (item 1); a step added to refresh.sh that writes into contracts/, screens/,
# flows/, states/, events/, roles*.yaml or the lineage belongs here.
# Every file derive-diagrams writes (the README, the HLD and the four LLD sets).
DIAGRAMS = ["diagrams/*.yaml", "diagrams/hld/*.yaml", "diagrams/lld/*/*.yaml"]

WRITE_BACK = [
    ("derive-lineage", ["--apply"], ["handoff/api-data-lineage.json"]),
    ("derive-read-columns", ["--apply"], ["handoff/api-data-lineage.json"]),
    ("derive-service-counts", ["--apply"], ["handoff/service-decomposition.json"]),
    ("derive-frontend", [], ["frontend/*.yaml"]),
    ("derive-board-flows", ["--apply"], ["flows/*.yaml", "screens/P*.yaml"]),
    ("derive-transitions-from-flows", ["--apply", "--adopt"], ["screens/P*.yaml"]),
    ("label-launcher-edges", ["--apply"], ["screens/P*.yaml"]),
    ("derive-entrystate-params", ["--apply"], ["screens/P*.yaml"]),
    ("derive-carries-from-entrystate", ["--apply"], ["screens/P*.yaml"]),
    ("derive-components", ["--apply"], ["screens/P*.yaml"]),
    ("derive-screen-wiring", ["--apply"], ["screens/P*.yaml"]),
    ("derive-board-anchors", ["--apply"], ["screens/P*.yaml"]),
    # wireframe.stateViews on the client-verified screens (21 October 2026, CHG-R9UI-003)
    ("derive-state-views", ["--apply"], ["screens/P*.yaml", "handoff/design-frames.json"]),
    ("build-design-inputs", [], ["handoff/design-inputs/README.md", "handoff/design-batches/apps/*/*.md"]),
    ("derive-app-roles", [], ["roles-by-app.yaml"]),
    ("derive-id-register", ["--apply"], ["screens/_id-register.yaml"]),
    ("link-screens-contracts", [], ["screens/P*.yaml", "contracts/*/*.yaml"]),
    # Not a write-back: the diagrams are derived. They are drawn from everything above (the screens, flows, contracts and
    # lineage), so they run last here as in refresh.sh, and --chain fails on a diagram a second regeneration changes
    # (P-31, CHG-R11DES-002: derive-diagrams ran before the screen steps, so every refresh drew the previous run's
    # screens; r10's second rebuild changed P01 and P02, fixed by hand in cd306cce).
    ("derive-diagrams", [], DIAGRAMS),
]


# Steps too slow for every gate run (seconds per run); the full form runs them. link-screens-contracts was here at 670 s
# until its per-operation search was replaced (CHG-R8GEN-016, 34 s, byte-identical output); none is slow now.
SLOW = {}


def files_of(globs, root=ROOT):
    out = set()
    for g in globs:
        for p in glob.glob(os.path.join(root, g)):
            if os.path.isfile(p):
                out.add(os.path.normpath(p))
    return out


def snapshot(globs, root=ROOT):
    snap = {}
    for p in files_of(globs, root):
        with open(p, "rb") as fh:
            snap[p] = fh.read()
    return snap


def compare(a, b):
    """{path: (before bytes or None, after bytes or None)} for every path whose bytes differ."""
    return {p: (a.get(p), b.get(p)) for p in set(a) | set(b) if a.get(p) != b.get(p)}


def first_lines(before, after, n=6):
    x = (before or b"").decode("utf-8", "replace").splitlines()
    y = (after or b"").decode("utf-8", "replace").splitlines()
    d = [ln for ln in difflib.unified_diff(x, y, lineterm="", n=0) if not ln.startswith(("---", "+++", "@@"))]
    return d[:n]


def restore(snap, globs, root=ROOT):
    for p, data in snap.items():
        with open(p, "rb") as fh:
            if fh.read() == data:
                continue
        with open(p, "wb") as fh:
            fh.write(data)
    for p in files_of(globs, root) - set(snap):
        os.remove(p)             # a file the step created; it did not exist before the first run


def run_step(name, args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    t = time.time()
    r = subprocess.run([sys.executable, os.path.join("tools", name + ".py")] + list(args), cwd=ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or ""), time.time() - t


def chain(steps, want=None, keep=False):
    """RT-CHAIN: every step once more, in order; a file the chain as a whole leaves changed is a finding."""
    globs = sorted({g for _n, _a, gs in steps for g in gs})
    s0 = snapshot(globs)
    findings, touched = [], {}
    try:
        prev = s0
        for name, args, gs in steps:
            if want and name not in want:
                continue
            rc, out, secs = run_step(name, args)
            cur = snapshot(globs)
            changed = compare(prev, cur)
            for pth in changed:
                touched.setdefault(pth, []).append(name)
            print("  %-8s %-32s %5.1fs changed %3d" % ("ERROR" if rc else "ran", name, secs, len(changed)))
            if rc:
                findings.append("RT-ERROR %s exited %d: %s" % (name, rc, " | ".join(out.strip().splitlines()[-3:])))
            prev = cur
        for pth, (x, y) in sorted(compare(s0, prev).items()):
            findings.append("RT-CHAIN %s: the chain changed it (%s): %s"
                            % (os.path.relpath(pth, ROOT).replace("\\", "/"), ", ".join(touched.get(pth, [])),
                               " / ".join(first_lines(x, y))))
    finally:
        if not keep:
            restore(s0, globs)
    for f in findings:
        print("  " + f)
    print("%s - %d finding(s); the chain of %d step(s) %s" % ("FAIL" if findings else "PASS", len(findings),
                                                             len(steps), "left the files as it found them"
                                                             if not findings else "is not a fixed point"))
    return 1 if findings else 0


def self_test():
    """The comparison and the restore on made-up files in a temporary folder."""
    import tempfile
    fails = []
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.yaml"), os.path.join(d, "b.yaml")
        for p, s in ((a, b"x: 1\n"), (b, b"y: 2\n")):
            with open(p, "wb") as fh:
                fh.write(s)
        s0 = snapshot(["*.yaml"], d)
        with open(a, "wb") as fh:
            fh.write(b"x: 2\n")
        with open(os.path.join(d, "c.yaml"), "wb") as fh:
            fh.write(b"z: 3\n")
        s1 = snapshot(["*.yaml"], d)
        diff = compare(s0, s1)
        if set(map(os.path.basename, diff)) != {"a.yaml", "c.yaml"}:
            fails.append("compare: expected a.yaml and c.yaml to differ, got %s" % sorted(diff))
        if compare(s1, snapshot(["*.yaml"], d)):
            fails.append("compare: an unchanged tree differs from itself")
        if first_lines(b"x: 1\n", b"x: 2\n") != ["-x: 1", "+x: 2"]:
            fails.append("first_lines: %r" % first_lines(b"x: 1\n", b"x: 2\n"))
        restore(s0, ["*.yaml"], d)
        if compare(s0, snapshot(["*.yaml"], d)):
            fails.append("restore: the tree is not as it was")
    return fails


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", help="comma-separated tool names from WRITE_BACK (default: all)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--keep", action="store_true", help="leave the first run's output instead of restoring")
    ap.add_argument("--once", action="store_true", help="one run per step: on a refreshed tree any change is a finding")
    ap.add_argument("--skip-slow", action="store_true", help="leave out the steps in SLOW")
    ap.add_argument("--chain", action="store_true",
                    help="run every step once more in order; fail on a file the chain leaves changed")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    fails = self_test()
    if fails or a.self_test:
        for f in fails:
            print("  SELF-TEST FAIL  " + f)
        print("%s - %d self-test(s) failed" % ("FAIL" if fails else "PASS", len(fails)))
        return 1 if fails else 0
    if a.list:
        for name, args, globs in WRITE_BACK:
            print("  %-32s %-18s %s" % (name, " ".join(args), ", ".join(globs)))
        return 0
    want = set(a.steps.split(",")) if a.steps else None
    unknown = (want or set()) - {n for n, _a, _g in WRITE_BACK}
    if unknown:
        print("FAIL - not in WRITE_BACK: %s" % ", ".join(sorted(unknown)))
        return 1
    findings, notes = [], []
    if a.chain:
        return chain(WRITE_BACK, want, a.keep)
    for name, args, globs in WRITE_BACK:
        if want and name not in want:
            continue
        if a.skip_slow and name in SLOW and not want:
            print("  skip     %-32s slow (%ds a run); the full form runs it" % (name, SLOW[name]))
            continue
        s0 = snapshot(globs)
        try:
            if a.once:
                # On a refreshed tree the refresh was the first run: this one is the second.
                rc1, out1, t1, s1 = 0, "", 0.0, s0
            else:
                rc1, out1, t1 = run_step(name, args)
                s1 = snapshot(globs)
            rc2, out2, t2 = run_step(name, args) if rc1 == 0 else (rc1, out1, 0.0)
            s2 = snapshot(globs)
        finally:
            if not a.keep:
                restore(s0, globs)
        if rc1 or rc2:
            tail = (out2 or out1).strip().splitlines()[-3:]
            findings.append("RT-ERROR %s exited %d: %s" % (name, rc1 or rc2, " | ".join(tail)))
            print("  ERROR    %-32s exit %d" % (name, rc1 or rc2))
            continue
        first, second = compare(s0, s1), compare(s1, s2)
        if first:
            notes.append("%s: the first run changed %d file(s) (%s); the tree was not refreshed for this step"
                         % (name, len(first), ", ".join(sorted(os.path.relpath(p, ROOT) for p in first)[:4])))
        for p, (x, y) in sorted(second.items()):
            findings.append("RT-UNSTABLE %s: %s changed %s: %s"
                            % (name, "run after the refresh, it" if a.once else "a second run",
                               os.path.relpath(p, ROOT).replace("\\", "/"), " / ".join(first_lines(x, y))))
        print("  %-8s %-32s run 1 %5.1fs changed %3d, run 2 %5.1fs changed %3d"
              % ("FAIL" if second else "ok", name, t1, len(first), t2, len(second)))
    for n in notes:
        print("  note  " + n)
    for f in findings:
        print("  " + f)
    print("%s - %d finding(s); every step's files %s" % ("FAIL" if findings else "PASS", len(findings),
                                                       "left as the first run wrote them" if a.keep
                                                       else "put back as they were"))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
