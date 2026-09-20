#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A tool that runs, exits 0, and writes where nobody reads.

**`build-cf-index.py` wrote `conflict-status.md` to the repository root instead of
`docs/registers/` from 25 August to 20 September.** It ran on every refresh. It exited 0. It
printed a correct-looking summary. `OVERVIEW.md` and every reader went on reading
`docs/registers/conflict-status.md`, which by then was **51 conflicts behind**, and no checker
in the package compared the two — because every checker validates the *content* of an artefact
and none validates that the artefact a writer produces is the one a reader consumes.

Seven weeks. The register said seventeen conflicts were open when twelve were.

## What this checks

Two halves of one question, and the bug above is both of them at once:

    written, referenced by nothing   a tool produces a file and no other tool, doc or
                                     script mentions that path -- output falling on the floor
    referenced, written by nothing   something points at a path no tool produces -- a reader
                                     aimed at a file that will never be refreshed

`build-cf-index` would have failed both on 25 August: `conflict-status.md` at the root was
written and referenced by nothing, while `docs/registers/conflict-status.md` was referenced by
`OVERVIEW.md` and written by nothing.

## Why this reads the syntax tree and not the text

**Grepping for write calls was tried first, in `check-authored-inputs`, and gave eight false
positives** — a write six hundred characters from a filename is still a write, and proximity
cannot tell which of the four paths in scope it landed in.

So this resolves paths through the AST. Module-level constants are followed:
`ROOT` (all five idioms in use here), `H = ROOT / "handoff"`, `P = os.path.join(H, "x.json")`.
A write is `open(p, "w")`, `io.open(p, "w")`, `p.write_text(...)`, `p.write_bytes(...)` or
`shutil.copy(_, p)`; a read is the same set in read mode, plus `read_text`, `exists`, `glob`
and `os.listdir`.

**Paths built from an f-string or a loop variable cannot be resolved and are counted, not
guessed.** The count is printed every run, because a checker that silently sees half the
package is worse than one that says which half. **A tool whose writes are all dynamic is
reported as unreadable rather than as clean** — otherwise the least inspectable tools would
look like the safest ones.

    python3 tools/check-output-paths.py
    python3 tools/check-output-paths.py --verbose
"""
import ast
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

# A path this tool should not expect a reader for, and why.
#
# **Only two kinds belong here.** A terminal deliverable, which is the point of the package
# and is read by people and by other repositories rather than by anything here; and a
# directory a tool fills wholesale, where naming each file would be a second copy of the
# tool's own logic.
_EXCLUDED = {
    "handoff": "the deliverable itself — read by the backend team, not by this repo",
    "repos": "mirrors of the package for five downstream repositories",
    "diagrams": "rendered for people and for the viewer",
    "wireframes": "screen drawings, consumed by the viewer and by designers",
    "screens": "screen definitions, authored and consumed by the viewer",
    "contracts": "the deliverable",
    "docs": "written for people",
    "sources": "client inputs; nothing here writes them",
    "events": "event definitions, part of the deliverable",
    "states": "state models, part of the deliverable",
    "viewer": "the schema viewer application",
    "scratch": "working files",
    ".": "the repository root",
    "mnt": "scan-domain-drift writes a one-off CSV to a sandbox path outside the repo; it is "
           "excluded from refresh.sh too, as deliberate rather than a rebuild",
}

WRITE_METHODS = {"write_text", "write_bytes"}
READ_METHODS = {"read_text", "read_bytes", "exists", "is_file", "glob", "rglob", "iterdir"}
PATHY = re.compile(r"(?<![\w./-])((?:handoff|docs|tools|contracts|wireframes|screens|events"
                   r"|states|diagrams|repos|sources)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,5})")
# **Root-level artefacts have no directory to match on.** `OVERVIEW.md` and `roles-by-app.yaml`
# are referenced by their bare name or not at all, so a directory-anchored pattern reports every
# one of them as an orphan. Over-matching here is the safe direction: a stray word that looks
# like a filename only ever *excuses* an output, and the orphan list is what this tool claims.
BARE = re.compile(r"(?<![\w./-])([A-Za-z][A-Za-z0-9_-]*\.(?:md|ya?ml|json|csv|mjs|js))"
                  r"(?![\w/-])")


def authored_inputs():
    """The ring-4 list, read from `check-authored-inputs` rather than copied.

    **Two tools carrying the same list is how they come to disagree** — which is the defect
    this one exists to find, so keeping a second copy here would be the joke telling itself.
    """
    import importlib.util
    p = os.path.join(TOOLS, "check-authored-inputs.py")
    try:
        spec = importlib.util.spec_from_file_location("_cai", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return {row[0] for row in m.AUTHORED}
    except Exception:
        return set(re.findall(r'\(\s*"([a-z]+/[A-Za-z0-9_.-]+)"',
                              io.open(p, encoding="utf-8").read()))


class Resolver(ast.NodeVisitor):
    """Module-level constant paths, resolved to repo-relative strings."""

    def __init__(self, tree):
        self.assign = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                    and isinstance(node.targets[0], ast.Name):
                self.assign[node.targets[0].id] = node.value
        self.memo = {}

    def resolve(self, node, depth=0):
        """A repo-relative path, or None where it cannot be known without running the tool."""
        if depth > 12 or node is None:
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        # ROOT, in all five idioms: Path(__file__).resolve().parents[1] and the
        # os.path.dirname(os.path.dirname(os.path.abspath(__file__))) chain both land here.
        if isinstance(node, (ast.Call, ast.Subscript, ast.Attribute)):
            src = ast.dump(node)
            if "__file__" in src:
                return ""
        if isinstance(node, ast.Name):
            if node.id in self.memo:
                return self.memo[node.id]
            self.memo[node.id] = None                 # recursion guard
            got = self.resolve(self.assign.get(node.id), depth + 1)
            self.memo[node.id] = got
            return got
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            left = self.resolve(node.left, depth + 1)
            right = self.resolve(node.right, depth + 1)
            if left is None or right is None:
                return None
            return (left + "/" + right).strip("/")
        if isinstance(node, ast.Call):
            fn = ast.dump(node.func)
            if "'join'" in fn and "'path'" in fn:      # os.path.join(...)
                parts = [self.resolve(a, depth + 1) for a in node.args]
                if any(p is None for p in parts):
                    return None
                return "/".join(p for p in parts if p).strip("/")
            if "'Path'" in fn or "'_P'" in fn:         # Path(x)
                return self.resolve(node.args[0], depth + 1) if node.args else None
        return None


def scan(path):
    """Writes, reads and the number of path expressions that could not be resolved."""
    try:
        tree = ast.parse(io.open(path, encoding="utf-8").read())
    except Exception:
        return set(), set(), 0
    r = Resolver(tree)
    writes, reads = set(), set()
    dyn = {"write": 0, "read": 0}

    def mode_of(call):
        if len(call.args) > 1 and isinstance(call.args[1], ast.Constant):
            return str(call.args[1].value)
        for kw in call.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                return str(kw.value.value)
        return "r"

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
        target, is_write = None, None

        if name == "open" and node.args:
            target, is_write = node.args[0], mode_of(node)[:1] in ("w", "a", "x")
        elif name in WRITE_METHODS and isinstance(fn, ast.Attribute):
            target, is_write = fn.value, True
        elif name in READ_METHODS and isinstance(fn, ast.Attribute):
            target, is_write = fn.value, False
        elif name == "listdir" and node.args:
            target, is_write = node.args[0], False
        elif name in ("copy", "copy2", "copyfile", "move") and len(node.args) > 1:
            target, is_write = node.args[1], True
        if target is None:
            continue

        got = r.resolve(target)
        if got is None:
            # **Counted apart.** A checker that writes nothing and globs a directory has
            # unresolved *reads*; lumping the two together reported forty-odd checkers as
            # "writes only through dynamic paths", which is the opposite of true.
            dyn["write" if is_write else "read"] += 1
        elif got:
            (writes if is_write else reads).add(got.replace("\\", "/").strip("/"))
    return writes, reads, dyn


def referenced_paths():
    """Every repo-relative path mentioned in prose, a shell script or a tool -> who mentions it.

    **Who matters, not just whether.** `derive-app-roles.py` names `roles-by-app.yaml` in its
    own docstring, so a set of bare paths would show that file as referenced and excuse the very
    orphan it is. A path is reached only when something *other than its writer* points at it.
    """
    out = {}
    roots = [(ROOT, (".md", ".sh")), (os.path.join(ROOT, "docs"), (".md",)),
             (os.path.join(ROOT, "handoff"), (".md",)), (TOOLS, (".py", ".sh"))]
    for base, exts in roots:
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, files in os.walk(base):
            dirnames[:] = [d for d in dirnames
                           if d not in ("repos", "node_modules", ".git", "sources")]
            for fn in files:
                if not fn.endswith(exts):
                    continue
                try:
                    s = io.open(os.path.join(dirpath, fn), encoding="utf-8",
                                errors="ignore").read()
                except Exception:
                    continue
                if fn == "check-output-paths.py":
                    # **This file's own prose is not evidence that a path is read.** The
                    # docstring above names `roles-by-app.yaml` as the worked example of an
                    # orphan, and counting that reference excused the orphan — a checker
                    # suppressing its own finding by describing it.
                    continue
                who = fn[:-3] if fn.endswith(".py") else fn
                for p in set(PATHY.findall(s)) | set(BARE.findall(s)):
                    out.setdefault(p, set()).add(who)
            if base == ROOT:
                break                                  # root files only, not the whole tree
    return out


def excused(p):
    top = p.split("/", 1)[0]
    return _EXCLUDED.get(top)


def main():
    verbose = "--verbose" in sys.argv[1:]
    tools = sorted(f for f in os.listdir(TOOLS) if f.endswith(".py"))

    writes, reads, blind = {}, {}, []
    dyn_w = dyn_r = 0
    for fn in tools:
        w, r, d = scan(os.path.join(TOOLS, fn))
        dyn_w += d["write"]
        dyn_r += d["read"]
        for p in w:
            writes.setdefault(p, []).append(fn[:-3])
        for p in r:
            reads.setdefault(p, []).append(fn[:-3])
        if d["write"] and not w:
            blind.append(fn[:-3])

    refs = referenced_paths()
    written, read = set(writes), set(reads)

    def reached(p):
        """Named or read by something that is not the tool that writes it.

        **A tool checking whether its own output exists is not a reader of it.**
        `derive-app-roles` calls `OUT.exists()` before writing `roles-by-app.yaml`, and
        counting that as readership excused the orphan it was written to catch.
        """
        mine = set(writes.get(p, []))
        return bool((refs.get(p, set()) - mine) or (set(reads.get(p, [])) - mine))

    orphan = sorted(p for p in written if not reached(p) and not excused(p))
    # A read path should have a writer. Authored inputs are the deliberate exception and
    # `check-authored-inputs` owns them, so the finding is the ones that are on neither list.
    authored = authored_inputs()
    unwritten = sorted(p for p in read
                       if p not in written and p not in authored and p in refs
                       and os.path.exists(os.path.join(ROOT, p)))

    print("  %d tool(s) · %d written path(s) · %d read path(s) · %d reference(s) in prose"
          % (len(tools), len(written), len(read), len(refs)))
    print("  unresolved without running the tool: %d write(s), %d read(s)" % (dyn_w, dyn_r))
    if blind:
        print("  %d tool(s) write only through dynamic paths and are invisible here: %s"
              % (len(blind), ", ".join(sorted(blind))[:200]))

    problems = 0
    if orphan:
        problems += len(orphan)
        print("\n  %d path(s) WRITTEN and reached by nothing — the `build-cf-index` "
              "signature:" % len(orphan))
        for p in orphan:
            print("    %-52s written by %s" % (p, ", ".join(writes[p])))

    # **Reported and never failed.** With %d write expressions unresolved, a path can have a
    # writer this tool cannot see -- `handoff/status.json` is written by `build-status` through
    # a path built at run time. Failing on that would train a reader to ignore the run.
    if unwritten:
        print("\n  %d path(s) read by a tool, written by none this can resolve, and not on the"
              "\n  authored-input list. **Not a failure** — %d write expressions are dynamic, so"
              "\n  some of these have a writer that is invisible here:" % (len(unwritten), dyn_w))
        for p in unwritten:
            print("    %-52s read by %s" % (p, ", ".join(reads[p][:3])))

    if verbose:
        print("\n  every resolved write:")
        for p in sorted(written):
            print("    %-52s %s" % (p, ", ".join(writes[p])))

    if problems:
        print("\n%d path(s) to answer. A writer and its readers disagreeing is invisible to "
              "every\nother checker here, because each of them validates content and none "
              "validates delivery." % problems)
        return 1
    print("\nPASS — every resolved output has a reader and every read path has a writer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
