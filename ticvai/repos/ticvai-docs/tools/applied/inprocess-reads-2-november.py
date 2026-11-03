#!/usr/bin/env python3
"""Re-routes in process every `service` read a host already asks in process (r13 lane r, 2 November 2026;
CHG-R13INP-001).

**The class.** Developers kept raising one request: an operation declares `x-ticvai-read-via` with `route: service`
for a query whose owner's queries already run in the same host, and the lead settled it the same way each time (CR-296,
CR-383, CR-385, CR-394, CR-426, CR-427, and on 2 November CR-475 to CR-478): in process, through the owner's own query
class, under the caller's row-level security, with an additive read grant where the host's role lacks one. For r13 the
lead asked for the whole class fixed at its source, once. A read is in the class when
tools/check-cross-module-reads.py `asked_in_process_by_host` names a reason (XR-INPROCESS-HOST): the owner runs in the
reader's deployable, the reader is an event consumer (workers), the lead granted the query to the reader's deployable,
or the reader's host composes the owner module's query classes (`composes` on a `reads` entry of
docs/active/cross-deployable-writes.yaml: XDR-073 to XDR-078 for the class). Left alone, and listed by the change
entry for the lead: a Control Plane operation (control.* tables, platform or cell scope), an Identity read
(Identity is not composed by any host but for XDR-010's narrow read and XDR-021/XDR-035's single queries), and every
read across a boundary no host has opened.

For each read in the class it writes `route: in-process` at the read's own line, and adds `in-process` to the query's
`served` where the owner served it on the service route only, with the rule's routes sentence saying who asks it in
process. Two `for` texts that named the service route are rewritten. A second run writes nothing.

    python tools/applied/inprocess-reads-2-november.py            # what it would write
    python tools/applied/inprocess-reads-2-november.py --apply    # then: python tools/derive-lineage.py --apply
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
import audit_guard as g  # noqa: E402

_spec = importlib.util.spec_from_file_location("xr", TOOLS / "check-cross-module-reads.py")
xr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xr)

TAG = "CHG-R13INP-001"
# `for` texts that said the read went over the service route (exact text -> new text).
FOR_TEXT = {
    ("openShift", "tenancy#deviceRecords"): (
        "its read of the registered device, Tenancy's data, through Tenancy's service route, the only one the query "
        "serves (CHG-MOD-001; R8 lineage request; CHG-R8INT-005)",
        "its read of the registered device, Tenancy's data, in process within commerce through Tenancy's query class "
        "(CHG-MOD-001; R8 lineage request; CHG-R8INT-005; in process since CHG-R13INP-001)"),
    ("getPublishedTenantConfig", "payments#providerConnectionRecords"): (
        "its read of payments.provider_connection, for `paymentTokenisation`, through the service route: White-label "
        "runs in operations, Payments in commerce (lineage request, r8; CHG-R8INT-005)",
        "its read of payments.provider_connection, for `paymentTokenisation`, in process: the operations host composes "
        "Orders' query classes, Payments among them (lineage request, r8; CHG-R8INT-005; in process since "
        "CHG-R13INP-001, XDR-075)"),
}
LABEL = {"TenancyService": "Tenancy", "CatalogueService": "Catalogue", "OrderService": "Orders",
         "AccessService": "Access"}


def _read(path: Path):
    raw = path.read_bytes().decode("utf-8")
    return raw.replace("\r\n", "\n"), "\r\n" in raw


def _write(path: Path, text: str, crlf: bool):
    path.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode("utf-8"))


def op_block(lines: list, op: str):
    i = next((n for n, l in enumerate(lines) if re.match(r"^\s+operationId:\s*%s\s*$" % re.escape(op), l)), None)
    if i is None:
        raise SystemExit(f"{op}: no such operationId")
    ind = re.match(r"^(\s+)", lines[i]).group(1)
    end = i + 1
    while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) >= len(ind)):
        end += 1
    return i, end


def flip(text: str, op: str, query: str):
    """`route: service` -> `route: in-process` on the read of `query` in `op`'s x-ticvai-read-via. (text, changed)."""
    lines = text.split("\n")
    i, end = op_block(lines, op)
    for n in range(i, end):
        m = re.match(r"^(\s*)- query:\s*(\S+)\s*$", lines[n])
        if not m or m.group(2) != query:
            continue
        ind = m.group(1) + "  "
        k = n + 1
        while k < end and lines[k].startswith(ind) and not lines[k].lstrip().startswith("- "):
            r = re.match(r"^(\s+)route:\s*service\s*$", lines[k])
            if r:
                lines[k] = f"{r.group(1)}route: in-process"
                return "\n".join(lines), True
            k += 1
    return text, False


def set_for(text: str, op: str, query: str, old: str, new: str):
    lines = text.split("\n")
    i, end = op_block(lines, op)
    blk = "\n".join(lines[i:end])
    want = "for: '" + old.replace("'", "''") + "'"
    if want not in blk:
        return text, False
    blk = blk.replace(want, "for: '" + new.replace("'", "''") + "'")
    lines[i:end] = blk.split("\n")
    return "\n".join(lines), True


def query_block(lines: list, name: str):
    i = next((n for n, l in enumerate(lines) if l == f"  {name}:"), None)
    if i is None:
        raise SystemExit(f"query {name}: not declared")
    end = i + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith("    ")):
        end += 1
    return i, end


def serve_in_process(text: str, name: str, label: str, hosts: list):
    """Adds `in-process` to query `name`'s served list and says in its rule who asks it in process. (text, changed)."""
    lines = text.split("\n")
    i, end = query_block(lines, name)
    s = next((n for n in range(i, end) if re.match(r"^    served:\s*\[", lines[n])), None)
    if s is None:
        raise SystemExit(f"query {name}: no served list")
    cur = [x.strip() for x in re.match(r"^    served:\s*\[(.*)\]", lines[s]).group(1).split(",") if x.strip()]
    if "in-process" in cur:
        return text, False
    new = [r for r in xr.ROUTES if r in cur + ["in-process"]]
    lines[s] = f"    served: [{', '.join(new)}]"
    r0 = next((n for n in range(i, end) if lines[n].startswith("    rule:")), None)
    body = [n for n in range(r0 + 1, end) if lines[n].startswith("      ")] if r0 is not None else []
    para = " ".join(lines[n].strip() for n in body)
    sentence = (f"It is asked in process by the {' and '.join(hosts)} host{'s' if len(hosts) > 1 else ''}, which "
                f"compose{'' if len(hosts) > 1 else 's'} {label}'s query classes, through the C# query class {label} "
                f"implements, under the caller's row-level security ({TAG}).")
    if body and "It is asked from another deployable" in para:
        k = para.index("It is asked from another deployable")
        para = para[:k] + sentence + " " + para[k:]
        lines[body[0]:body[-1] + 1] = textwrap.wrap(para, width=116, initial_indent="      ",
                                                     subsequent_indent="      ", break_long_words=False,
                                                     break_on_hyphens=False)
    return "\n".join(lines), True


def plan():
    """[(operation, contract file, query, reason)] for every read in the class, and {query: (stem, owner, hosts)}."""
    dec = g.load_json(g.ROOT / "handoff" / "service-decomposition.json", {}) or {}
    services = dec.get("services") or {}
    dep_of = {s: v.get("deployable") for s, v in services.items()}
    svc_of_contract = {c: s for s, v in services.items() for c in v.get("contracts") or []}
    lin = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    grants = xr.read_grants()
    granted, narrow, composes = xr.granted_reads(grants), xr.narrow_reads(grants), xr.composed_modules(grants)
    queries = xr.declared_queries()
    rows, served = [], {}
    for o, f in sorted(g.operations().items()):
        op = f["op"]
        reader = svc_of_contract.get(f["contract"])
        rdep = dep_of.get(reader)
        consumer = bool(op.get("x-ticvai-consumes"))
        if xr.control_plane(lin.get(o) or {}, op):
            continue
        for r in op.get("x-ticvai-read-via") or []:
            if not isinstance(r, dict) or str(r.get("route")) != "service":
                continue
            key = str(r.get("query"))
            if key not in queries:
                continue
            stem, q = queries[key]
            owner = svc_of_contract.get(stem)
            why = xr.asked_in_process_by_host(o, rdep, owner, dep_of.get(owner), key, consumer, granted, narrow,
                                              composes)
            if not why:
                continue
            if dep_of.get(owner) != rdep and not consumer and (rdep, key) not in granted:
                raise SystemExit(f"{o} asks {key}: {rdep} composes {owner} but no reads entry grants the query; "
                                 "add it to the host's XDR entry first")
            rows.append((o, f["file"], key, why))
            if "in-process" not in (q.get("served") or []):
                hosts = served.setdefault(key, (stem, owner, set()))[2]
                hosts.add(dep_of.get(owner) if dep_of.get(owner) == rdep else rdep)
    return rows, served


def main() -> int:
    g.force_utf8()
    apply = "--apply" in sys.argv[1:]
    rows, served = plan()
    files: dict = {}

    def text_of(rel):
        if rel not in files:
            files[rel] = list(_read(ROOT / rel))
        return files[rel]

    n = 0
    for o, rel, key, why in rows:
        t = text_of(rel)
        t[0], ch = flip(t[0], o, key)
        if not ch:
            raise SystemExit(f"{o}: no `route: service` line for {key} in {rel}")
        n += 1
        print(f"  ROUTE {o}: {key} in-process - {why}")
        if (o, key) in FOR_TEXT:
            t[0], ch = set_for(t[0], o, key, *FOR_TEXT[(o, key)])
            if ch:
                print(f"  FOR   {o}: {key}")
    m = 0
    for key, (stem, owner, hosts) in sorted(served.items()):
        crel = next(r for s_, r, d in g.contracts() if s_ == stem)
        t = text_of(crel)
        t[0], ch = serve_in_process(t[0], key.split("#", 1)[1], LABEL.get(owner, owner), sorted(hosts))
        if ch:
            m += 1
            print(f"  SERVED {key}: in-process added ({', '.join(sorted(hosts))})")
    if apply:
        for rel, (text, crlf) in files.items():
            _write(ROOT / rel, text, crlf)
    print(f"{n} read(s) re-routed in process in {len({r[0] for r in rows})} operation(s); {m} quer(ies) now served "
          f"in process; {'written' if apply else 'dry run (--apply writes)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
