# -*- coding: utf-8 -*-
"""The check-package errors left by the build of 29 September. Re-runnable.

1. ai.yaml names two platforms by old names (P12 Support Console, P13 White-label CMS). One code, one name.
2. Four Redis caches the AI lineage reads (cache:governance-policy, cache:rec-candidates,
   cache:rec-features, cache:risk-features) are not registered as stores in the schema reference.
3. Five AI operations list platform.outbox among their writes. ADR-0020: AI writes only its own stores.
   Their events leave through AiService's own outbox in the AI log database (design 2.4), so the
   lineage names no platform table.
4. ledger.tax_invoice and ledger.credit_memo store a currency. That is right: a tax invoice is a legal
   document fixed at issue, and the FTA requires the invoice currency (with the AED equivalent) on it.
   A later change to the region's currency must not rewrite an issued invoice. Added to CURRENCY_OK.
5. enrolFaceTag and concludeRecommendationExperiment are writes with no X-Consistency-Token on 2xx.
"""
import io, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
APPLY = "--apply" in sys.argv


def rw(rel, fn):
    p = ROOT / rel
    t = io.open(p, encoding="utf-8", newline="").read()
    n = fn(t)
    if n != t:
        print(f"  {rel}: changed")
        if APPLY:
            io.open(p, "w", encoding="utf-8", newline="").write(n)
    else:
        print(f"  {rel}: already done")


# 1
rw("contracts/satellite/ai.yaml", lambda t: t.replace("  - P12 Support Console", "  - P12 Venue Support")
   .replace("  - P13 White-label CMS", "  - P13 Venue CMS"))

# 2
CACHES = {
    "cache:governance-policy": ("**The effective AI governance policy per tenant and capability**, resolved once and "
                                "read on every AI call. Invalidated when a policy version is published; losable, "
                                "since the policy versions in `ai` are the source of truth.",
                                [("key", "text", "tenant id + capability"), ("policy", "jsonb", "the resolved policy"),
                                 ("version", "text", "the policy version it was resolved from")]),
    "cache:rec-candidates": ("**Recommendation candidates per tenant and context**, kept current from the "
                             "promotions strategy events. Read by `decideRecommendations`; rebuilt from promotions "
                             "if lost.",
                             [("key", "text", "tenant id + placement + context"), ("candidates", "jsonb", "candidate items with eligibility")]),
    "cache:rec-features": ("**Per-guest and per-item recommendation features** (recency, frequency, affinities). "
                           "Rebuilt from orders and recommendation events if lost.",
                           [("key", "text", "tenant id + subject"), ("features", "jsonb", "feature vector and its as-of time")]),
    "cache:risk-features": ("**Velocity counters and entity features for risk scoring** (attempts per card, "
                            "device and account in rolling windows). Short-lived by design; losing it resets "
                            "the windows, which the rules tolerate.",
                            [("key", "text", "tenant id + entity"), ("counters", "jsonb", "rolling-window counts")]),
}


def caches(t):
    d = json.loads(t)
    for k, (desc, cols) in CACHES.items():
        d["storage"].setdefault(k, desc)
        d["store"].setdefault(k, "redis")
        d["module"].setdefault(k, "ai")
        d["cols"].setdefault(k, [{"column": c, "type": ty, "required": "yes", "source": f"{k}.{c}",
                                  "description": ds, "table": k} for c, ty, ds in cols])
    return json.dumps(d)  # the file is stored compact and ASCII-escaped


rw("handoff/schema-reference.json", caches)

# 3
AI_OUTBOX = ["closeRiskCase", "decideOperationalRequirement", "openAiIncident", "pauseAiCapability", "publishForecastVersion"]


def outbox(t):
    d = json.loads(t)
    L = d.get("lineage", d) if isinstance(d.get("lineage"), dict) else d
    for o in AI_OUTBOX:
        v = L.get(o)
        if v and "platform.outbox" in (v.get("writes") or []):
            v["writes"] = [w for w in v["writes"] if w != "platform.outbox"]
            v["note"] = ((v.get("note") or "") + " Its event leaves through AiService's own outbox in the AI log "
                         "database (design 2.4); AI writes no platform table (ADR-0020).").strip()
    return json.dumps(d, indent=1, ensure_ascii=False) + ("\n" if t.endswith("\n") else "")


rw("handoff/api-data-lineage.json", outbox)

# 4
rw("tools/check-package.py", lambda t: t if '"ledger.tax_invoice"' in t else t.replace(
    '    CURRENCY_OK = {\n',
    '    CURRENCY_OK = {\n'
    '        # **A tax invoice and its credit memo are fixed at issue** (29 September). The FTA requires the\n'
    '        # invoice currency, with the AED equivalent, on the document, and a later change to the\n'
    '        # region\'s currency must not rewrite an issued invoice.\n'
    '        "ledger.tax_invoice", "ledger.credit_memo",\n', 1))

# 5
TOKEN = ("          headers:\n            X-Consistency-Token:\n"
         "              $ref: '../shared/common.yaml#/components/headers/ConsistencyToken'\n")


def token(op, code):
    def f(t):
        nl = "\r\n" if "\r\n" in t else "\n"
        lines = t.split(nl)
        i = next(n for n, l in enumerate(lines) if l.strip() == f"operationId: {op}")
        r = next(n for n in range(i, len(lines)) if lines[n].strip() == "responses:")
        c = r + 1
        assert lines[c].strip() == f"'{code}':", lines[c]
        if "X-Consistency-Token" in lines[c + 1] or lines[c + 1].strip() == "headers:":
            return t
        lines[c + 1:c + 1] = TOKEN.rstrip("\n").split("\n")
        return nl.join(lines)
    return f


rw("contracts/spine/access.yaml", token("enrolFaceTag", "201"))
rw("contracts/satellite/promotions.yaml", token("concludeRecommendationExperiment", "200"))
print("  applied" if APPLY else "  dry run: pass --apply")
