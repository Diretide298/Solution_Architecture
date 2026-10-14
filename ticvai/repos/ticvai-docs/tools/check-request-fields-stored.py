#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A field a configuration write takes is stored, or says it is not.

**Found by ADAM CR-082 (14 October 2026, CHG-TEN-005).** `configureWorkstation` took `cashierInputMode`,
`guestDisplayContent` and `loadedMediaStockId` on `ConfigureWorkstationRequest` and answered with a `Workstation`
that has none of them, persisted to `platform.workstation`, which has no column for any. BL-061 and BL-095 were
closed on the strength of the request fields. A developer building the operation has a value and nowhere to put it,
and the till reads back a default every time. `check-contract-storage` could not see it: it asks whether a
*persisted* schema's field has a column, and a request schema is not persisted. The audit of 14 October found the
same shape on 32 operations and 52 fields (createPrincipal `roleIds`, setPathClosure `expectedReopenAt`,
updatePriceList `isActive`, ...).

**The rule.** For a write named `create*`, `update*`, `configure*` or `set*` whose request is not itself a
persisted schema and whose `200`/`201` resource is (`x-ticvai-persistence` names a table), every request field that
is not `readOnly` must be one of:

  * on the resource, by name (`fooId` and `fooIds` also match `foo`);
  * a column of a table the resource persists to or the operation's lineage writes: its `snake_case`, with `_id`,
    `_ids`, `is_` or `_amount`, its `x-ticvai-column` (or the resource field's of the same name), a column whose
    schema-reference `source` is that field, or the same words with plurals ignored (`paymentTermDays` and
    `payment_terms_days`);
  * an array held as rows of a written child table named for it (`openingHours` in `outlet_opening_hours`);
  * marked `x-ticvai-stored-as: <schema>.<table>.<column>`, a column of a table it writes (CHG-STO-017);
  * marked `x-ticvai-persisted: false`: a field that travels and is not stored, said so where it is declared.

RF-REQUEST-NOT-STORED is that rule. RF-READONLY-REQUEST: a `readOnly` field on a request-only schema, which no
response returns, so nobody can ever read it (`ConfigureWorkstationRequest.mediaStockRemaining`); a field
`deprecated: true` and `x-ticvai-persisted: false` is on its way out and is not reported.

Read-only. Exit 1 on a finding not in `handoff/audit-baseline.json` (tools/audit_guard.py); today's other findings
are its baseline, and the list only shrinks.

    python3 tools/check-request-fields-stored.py [--all] [--update-baseline]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "RF-REQUEST-NOT-STORED": "a configuration write's request field is not on its persisted resource, has no column "
                             "in a table it writes, and is not marked x-ticvai-persisted: false (CR-082)",
    "RF-READONLY-REQUEST": "a readOnly field on a request-only schema, which nothing returns (CR-082)",
}
WRITES = re.compile(r"^(create|update|configure|set)[A-Z]")
TABLE = re.compile(r"[a-z_]+\.[a-z_0-9]+")


def words(name: str) -> tuple:
    """`payment_terms_days` and `paymentTermDays` alike: the snake words with a plural `s` dropped."""
    return tuple(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in g.snake(name).split("_") if w)


class Resolver:
    """`$ref`, `allOf` and properties across contract files, as the contracts write them."""

    def __init__(self):
        self.docs = {stem: doc for stem, _rel, doc in g.contracts()}

    def ref(self, ref: str, cur: str):
        m = re.match(r"^(?:(?:\.\./)?(?:\w+/)?([\w-]+)\.yaml)?#/components/schemas/([\w.-]+)$", ref or "")
        if not m:
            return None, None, cur
        stem = m.group(1) or cur
        body = ((self.docs.get(stem) or {}).get("components") or {}).get("schemas", {}).get(m.group(2))
        return m.group(2), body, stem

    def props(self, body, cur, depth=0) -> dict:
        out = {}
        if not isinstance(body, dict) or depth > 8:
            return out
        if "$ref" in body:
            _n, b, k = self.ref(body["$ref"], cur)
            return self.props(b, k, depth + 1)
        for part in body.get("allOf") or []:
            out.update(self.props(part, cur, depth + 1))
        for p, s in (body.get("properties") or {}).items():
            out[p] = s if isinstance(s, dict) else {}
        return out

    def persistence(self, body, cur, depth=0):
        if not isinstance(body, dict) or depth > 8:
            return None
        if isinstance(body.get("x-ticvai-persistence"), str):
            return body["x-ticvai-persistence"]
        if "$ref" in body:
            _n, b, k = self.ref(body["$ref"], cur)
            return self.persistence(b, k, depth + 1)
        for part in body.get("allOf") or []:
            p = self.persistence(part, cur, depth + 1)
            if p:
                return p
        return None

    def body(self, container, cur):
        """(name, schema, contract) of a request body or response's JSON schema."""
        for media in ((container or {}).get("content") or {}).values():
            s = (media or {}).get("schema")
            if isinstance(s, dict) and "$ref" in s:
                return self.ref(s["$ref"], cur)
            if isinstance(s, dict):
                return "(inline)", s, cur
        return None, None, cur


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-request-fields-stored", RULES)
    R = Resolver()
    ref = g.load_json(g.ROOT / "handoff" / "schema-reference.json", {}) or {}
    lineage = g.load_json(g.ROOT / "handoff" / "api-data-lineage.json", {}) or {}
    cols: dict = {}
    sources: dict = {}
    for t, cs in (ref.get("cols") or {}).items():
        for c in cs:
            cols.setdefault(t, set()).add(c["column"])
            sources.setdefault(t, set()).add(str(c.get("source") or "").rsplit(".", 1)[-1])
    tables_all = {t for t in cols if TABLE.fullmatch(t)}
    seen_ro: set = set()
    n_ops = 0
    for stem, doc in R.docs.items():
        for _path, item in ((doc or {}).get("paths") or {}).items():
            for verb, op in (item or {}).items():
                if verb not in ("post", "put", "patch") or not isinstance(op, dict) or not op.get("requestBody"):
                    continue
                oid = str(op.get("operationId") or "")
                rq_name, rq, rk = R.body(op["requestBody"], stem)
                if not isinstance(rq, dict) or R.persistence(rq, rk):
                    continue       # a persisted request is the resource: derive-schema gives it its columns
                rprops = R.props(rq, rk)
                # RF-READONLY-REQUEST, once per request-only schema (or per operation for an inline one).
                for p, spec in rprops.items():
                    if spec.get("readOnly") and not (spec.get("deprecated") and spec.get("x-ticvai-persisted") is False):
                        key = f"{rk}.{rq_name}.{p}" if rq_name != "(inline)" else f"{oid}.{p}"
                        if key not in seen_ro:
                            seen_ro.add(key)
                            guard.add("RF-READONLY-REQUEST", key,
                                      f"{key}: readOnly on a request schema nothing returns")
                if not WRITES.match(oid):
                    continue
                resp = (None, None, stem)
                for code in ("200", "201"):
                    r = (op.get("responses") or {}).get(code)
                    if isinstance(r, dict) and r.get("content"):
                        resp = R.body(r, stem)
                        break
                rs_name, rs, rsk = resp
                pers = R.persistence(rs, rsk) if isinstance(rs, dict) else None
                if not pers or not TABLE.match(pers) or "—" in pers:
                    continue       # only a resource that lands in a table
                n_ops += 1
                rs_props = R.props(rs, rsk)
                tables = {t for t in TABLE.findall(pers) if t in tables_all}
                tables |= {t for t in ((lineage.get(oid) or {}).get("writes") or []) if t in tables_all}
                tcols = set().union(*[cols[t] for t in tables]) if tables else set()
                tsrc = set().union(*[sources[t] for t in tables]) if tables else set()
                twords = {words(c) for c in tcols}
                # **A request that is the value of one of the resource's fields is stored as that field**
                # (`setAccessPointGeofence` sends an `AccessPointGeofence`, which is `AccessPoint.geofence`, one
                # jsonb column): the whole body is accounted for.
                if rq_name != "(inline)" and any(
                        str(v.get("$ref") or "").endswith("/" + rq_name)
                        or any(str(x.get("$ref") or "").endswith("/" + rq_name)
                               for x in (v.get("allOf") or v.get("oneOf") or []) if isinstance(x, dict))
                        for v in rs_props.values()):
                    continue
                for p, spec in rprops.items():
                    if spec.get("readOnly") or spec.get("x-ticvai-persisted") is False:
                        continue
                    base = p[:-3] if p.endswith("Ids") else p[:-2] if p.endswith("Id") else p
                    if p in rs_props or base in rs_props or base + "s" in rs_props:
                        continue
                    sn, sb = g.snake(p), g.snake(base)
                    cand = {sn, sb, sb + "_id", sb + "_ids", "is_" + sn, sn + "_amount"}
                    for s in (spec, rs_props.get(p) or {}):
                        if s.get("x-ticvai-column"):
                            cand.add(s["x-ticvai-column"])
                    if cand & tcols or p in tsrc or words(p) in twords or words(base) in twords:
                        continue
                    # **`x-ticvai-stored-as: <table>.<column>` names the column**, as check-stored-request-fields reads
                    # it (CHG-STO-017): a column of a table the resource persists to or the operation writes.
                    sa = str(spec.get("x-ticvai-stored-as") or "")
                    st, _, sc = sa.rpartition(".")
                    if sa and st in tables and sc in cols.get(st, set()):
                        continue
                    # a column that qualifies a field of two words or more: `expiresAt` as `credential_expires_at`
                    wp = words(p)
                    if len(wp) >= 2 and any(w[-len(wp):] == wp for w in twords):
                        continue
                    # an array held as the rows of a written child table named for it
                    if spec.get("type") == "array" and any(
                            t.split(".", 1)[1].endswith("_" + "_".join(words(base)))
                            or t.split(".", 1)[1].endswith("_" + sb) for t in tables):
                        continue
                    guard.add("RF-REQUEST-NOT-STORED", f"{oid}.{p}",
                              f"{oid}.{p}: on {rq_name}, not on {rs_name} ({pers.split('+')[0].strip()}), "
                              f"no column in {', '.join(sorted(tables)) or 'any written table'}")
    guard.note(f"{n_ops} configuration writes whose resource is persisted were read")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
