# -*- coding: utf-8 -*-
"""The check failures after the 29 September pass (30 September). Re-runnable.

1. Hand-written lineage named tables that do not exist:
   - createFnbOrder read `fnb.station` and `fnb.kitchen_routing_rule`. Stations are
     `fnb.kitchen_station`; a line is routed by its menu item's station (`fnb.menu_item`, already read),
     so there is no separate routing table.
   - applyCartPromoCode read `promotions.coupon`. A code is `promotions.coupon_code` under its
     `promotions.coupon_campaign`.
2. `cache:ai-breaker` (the AI provider circuit breaker listAiCapabilityHealth reads) is a Redis store
   the schema reference did not register.
3. relinquishWalletAuthorisation became a write in the second wave (it releases a wallet hold) and
   declares no X-Consistency-Token on its 200.
"""
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv
RENAME = {"fnb.station": "fnb.kitchen_station", "fnb.kitchen_routing_rule": None,
          "promotions.coupon": ["promotions.coupon_code", "promotions.coupon_campaign"]}


def lineage():
    p = ROOT / "handoff" / "api-data-lineage.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for op, v in d.items():
        if not isinstance(v, dict):
            continue
        for k in ("reads", "writes"):
            old = v.get(k) or []
            new = []
            for t in old:
                r = RENAME.get(t, t)
                new += r if isinstance(r, list) else ([r] if r else [])
            new = sorted(set(new))
            if new != old:
                v[k] = new
                n += 1
    print(f"  lineage lists fixed: {n}")
    if APPLY and n:
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")


def cache():
    p = ROOT / "handoff" / "schema-reference.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    k = "cache:ai-breaker"
    if k in d["storage"]:
        print("  cache:ai-breaker: already registered")
        return
    d["storage"][k] = ("**The AI provider circuit breaker per tenant and capability**: open, half-open or closed, "
                       "with the failure count that opened it. Read by listAiCapabilityHealth; losable, since a "
                       "lost breaker simply closes and the next failures reopen it.")
    d["store"][k] = "redis"
    d["module"][k] = "ai"
    d["cols"][k] = [{"column": c, "type": t, "required": "yes", "source": f"{k}.{c}", "description": ds, "table": k}
                    for c, t, ds in (("key", "text", "tenant id + capability + provider"),
                                     ("state", "text", "open, halfOpen or closed"),
                                     ("failures", "integer", "failures in the current window"))]
    print("  cache:ai-breaker: registered")
    if APPLY:
        p.write_text(json.dumps(d), encoding="utf-8")


def token():
    p = ROOT / "contracts" / "spine" / "cross-region.yaml"
    t = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    lines = t.split(nl)
    i = next(n for n, l in enumerate(lines) if l.strip() == "operationId: relinquishWalletAuthorisation")
    r = next(n for n in range(i, len(lines)) if lines[n].strip() == "responses:")
    c = next(n for n in range(r, len(lines)) if lines[n].strip().startswith("'2"))
    if "headers:" in lines[c + 1] or "X-Consistency-Token" in "".join(lines[c:c + 6]):
        print("  relinquishWalletAuthorisation: token already declared")
        return
    ind = " " * (len(lines[c]) - len(lines[c].lstrip()) + 2)
    lines[c + 1:c + 1] = [f"{ind}headers:", f"{ind}  X-Consistency-Token:",
                          f"{ind}    $ref: '../shared/common.yaml#/components/headers/ConsistencyToken'"]
    print("  relinquishWalletAuthorisation: token added")
    if APPLY:
        io.open(p, "w", encoding="utf-8", newline="").write(nl.join(lines))


if __name__ == "__main__":
    lineage(); cache(); token()
    print("  applied" if APPLY else "  dry run: pass --apply")
