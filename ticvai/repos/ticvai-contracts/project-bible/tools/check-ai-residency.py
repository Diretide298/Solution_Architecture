#!/usr/bin/env python3
"""The AI residency and scrubbing safeguards stay in the contracts (CHG-R1S-002, CHG-R1S-016).

**Decided by Chinmay on 2 and 3 October 2026**: a residency class per tenant (DEC-539), mandatory offline
scrubbing (DEC-542), and on 3 October "we are not hosting anything unless client asks it" (the guard is the
provider's content-safety service, no in-cell model; `docs/active/decisions/answers-3-october-gate-and-hosting.md`).
On 4 October he corrected the embeddings: we host the embedding model, its reranker, Presidio and the Arabic NER on
the AI GPU node pool in our cell, never an LLM (CHG-R11-001, reversing the mis-recorded CHG-R1S-026).
The legal research of 3 October (`docs/active/research/openai-key-uae-3-october.md`, "What this means for
TICVAI") added the safeguards that make "personal data never leaves the UAE in clear" a claim that can be made.
Each is a contract fact, and a contract fact is easy to lose in an edit. This check holds them:

    R-CATEGORY   tenancy RegionSettings.tenantCategory exists, and updateRegionSettings declares
                 `residency-category-refused`
    R-PATTERN    AiPolicy.scrubbing carries `residualPatternCheck` (all five patterns) and `scrubberVersion`
    R-EXCLUDE    AiPolicy.globalEndpointExclusions names allergy, accessibility and familyAndChildren and
                 blocks image, audio and file
    R-STATELESS  AiProvider.isStatelessOnly exists
    R-AUDIT      AiInteraction.scrubAudit carries entityCounts and no field that could hold a value
    R-UAE-OPENAI common AiResidencyClass names `ae.api.openai.com` and says failover never widens residency
    R-NOHOST     no contract names Qwen3Guard or an in-cell gpt-oss fallback as ours (only on a client's estate)
    R-EMBED      the embedding model (BGE-M3) and its reranker are OURS, self-hosted on the AI GPU node pool in
                 the cell (Chinmay, 4 October, CHG-R11-001, which reverses the mis-recorded CHG-R1S-026): the
                 uaeOnly routing text and the scrubbing text say so, and no contract line sends embeddings to a
                 provider or says no embedding model is hosted. A self-hosted LLM stays refused: a line that
                 makes an LLM ours (vLLM, a self-hosted LLM or chat model) fails unless it is a client's estate.

    python tools/check-ai-residency.py          (the self-tests run first, every time)
"""
from __future__ import annotations

import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    return yaml.load(io.open(os.path.join(ROOT, rel), encoding="utf-8"), Loader=yaml.CSafeLoader) or {}


# A line that sends embeddings to a provider, or says we host no embedding model (CHG-R1S-026's wording).
PROVIDER_EMBED = re.compile(r"text-embedding-3|no embedding model|embeddings? (?:are|is) the provider|"
                            r"provider'?'?s embedding model|provider embeddings", re.I)
# A line that makes an LLM ours. A client's estate (onPrem, a client's own GPU) is the one exception.
SELF_LLM = re.compile(r"\bvllm\b|self-hosted (?:open )?(?:LLM|language model|chat model)|we host (?:an? )?(?:LLM|language model)"
                      r"|(?:GPU|embeddings) (?:server|node|pool)[^.]*\b(?:runs|hosts|serves) (?:an? )?(?:LLM|language model|chat model)",
                      re.I)
NOT_OURS = re.compile(r"\bnever\b|\bno\b|\bnot\b|unless|client|on-?prem|supersede|reverse|no longer", re.I)


def line_findings(rel: str, n: int, line: str) -> list:
    """The per-line rules (R-NOHOST, R-EMBED) for one contract line."""
    out = []
    if re.search(r"qwen3guard", line, re.I) and not re.search(r"not a hosted|not hosted|self-host|client", line, re.I):
        out.append(("R-NOHOST", f"{rel}:{n} names Qwen3Guard as ours"))
    if re.search(r"in-cell (gpt-oss|open-weights|open model|model)", line, re.I) and \
            not re.search(r"dropped|no in-cell|there is no|host none", line, re.I):
        out.append(("R-NOHOST", f"{rel}:{n} names an in-cell model as a fallback"))
    if PROVIDER_EMBED.search(line) and not re.search(r"supersede|reverse|no longer|was ", line, re.I):
        out.append(("R-EMBED", f"{rel}:{n} sends embeddings to a provider or hosts no embedding model; "
                               f"BGE-M3 and its reranker are ours, in the cell (CHG-R11-001)"))
    if SELF_LLM.search(line) and not NOT_OURS.search(line):
        out.append(("R-EMBED", f"{rel}:{n} makes an LLM ours; we host the embedding model, never an LLM (CHG-R11-001)"))
    return out


def embed_findings(provider: dict, policy: dict) -> list:
    """The uaeOnly routing text names our self-hosted embedder and reranker on the GPU node pool in the cell; the
    scrubbing text puts Presidio on the same pool."""
    out = []
    route = str(((provider.get("properties") or {}).get("residencyClasses") or {}).get("description") or "")
    if not (re.search(r"bge-m3", route, re.I) and re.search(r"reranker", route, re.I)
            and re.search(r"GPU", route) and re.search(r"in the cell|our cell|our own cell", route, re.I)):
        out.append(("R-EMBED", "AiProvider.residencyClasses does not say BGE-M3 and its reranker run on our GPU "
                               "node pool in the cell (CHG-R11-001)"))
    scrub = str((((policy.get("properties") or {}).get("scrubbing") or {}).get("description")) or "")
    if not (re.search(r"presidio", scrub, re.I) and re.search(r"GPU", scrub)):
        out.append(("R-EMBED", "AiPolicy.scrubbing does not put Presidio and the Arabic NER on the AI GPU node pool "
                               "(CHG-R11-001)"))
    return out


def self_test() -> list:
    """Each rule against a line it must pass and one it must fail. Returns the failures."""
    fails = []
    lines = [
        ("the provider's embedding model on the UAE route (OpenAI UAE `text-embedding-3-large`)", True),
        ("no embedding model is hosted.", True),
        ("BGE-M3 and its reranker run on our AI GPU node pool in the cell.", False),
        ("CHG-R1S-026 said provider embeddings; CHG-R11-001 reverses it.", False),
        ("The GPU node pool also serves an LLM for the concierge.", True),
        ("We serve the model with vLLM in UAE North.", True),
        ("We never host an LLM unless a client asks: the LLM calls stay with the providers.", False),
        ("Qwen3Guard is our guard.", True),
        ("the guard is the provider's content-safety service, not a model we host", False),
    ]
    for text, want_bad in lines:
        got = bool(line_findings("t", 1, text))
        if got != want_bad:
            fails.append(f"line {text!r}: expected {'a finding' if want_bad else 'no finding'}")
    good_p = {"properties": {"residencyClasses": {"description":
              "Embeddings are ours: BGE-M3 and its reranker on the AI GPU node pool in the cell."}}}
    good_s = {"properties": {"scrubbing": {"description": "Presidio and the Arabic NER run on the AI GPU node pool."}}}
    if embed_findings(good_p, good_s):
        fails.append("embed_findings refused the self-hosted embedder text")
    bad_p = {"properties": {"residencyClasses": {"description": "Embedding calls route to the provider."}}}
    bad_s = {"properties": {"scrubbing": {"description": "The scrubber stays a CPU library in our worker."}}}
    if len(embed_findings(bad_p, bad_s)) != 2:
        fails.append("embed_findings passed contracts that do not host the embedder and scrubber in the cell")
    return fails


def main() -> int:
    fails = self_test()
    for f in fails:
        print(f"  SELF-TEST    {f}")
    if fails:
        print(f"FAIL {len(fails)} self-test(s)")
        return 1
    bad = []
    ten, ai, com = load("contracts/spine/tenancy.yaml"), load("contracts/satellite/ai.yaml"), \
        load("contracts/shared/common.yaml")
    S = lambda d, n: ((d.get("components") or {}).get("schemas") or {}).get(n) or {}  # noqa: E731

    rs = (S(ten, "RegionSettings").get("properties") or {})
    cat = rs.get("tenantCategory") or {}
    if "private" not in (cat.get("enum") or []) or len(cat.get("enum") or []) < 2:
        bad.append(("R-CATEGORY", "RegionSettings.tenantCategory is missing or has no private value"))
    found = False
    for item in (ten.get("paths") or {}).values():
        for op in (item or {}).values():
            if isinstance(op, dict) and op.get("operationId") == "updateRegionSettings":
                for r in (op.get("responses") or {}).values():
                    if isinstance(r, dict) and "residency-category-refused" in (r.get("x-ticvai-problem-types") or []):
                        found = True
    if not found:
        bad.append(("R-CATEGORY", "updateRegionSettings declares no residency-category-refused"))

    pol = S(ai, "AiPolicy").get("properties") or {}
    scr = (pol.get("scrubbing") or {}).get("properties") or {}
    pats = set(((scr.get("residualPatternCheck") or {}).get("items") or {}).get("enum") or [])
    if pats != {"emiratesId", "uaePhone", "cardPan", "iban", "email"}:
        bad.append(("R-PATTERN", f"AiPolicy.scrubbing.residualPatternCheck is {sorted(pats)}"))
    if "scrubberVersion" not in scr:
        bad.append(("R-PATTERN", "AiPolicy.scrubbing.scrubberVersion (the pinned Presidio release) is missing"))
    exc = (pol.get("globalEndpointExclusions") or {}).get("properties") or {}
    cats = set(((exc.get("fieldCategories") or {}).get("items") or {}).get("enum") or [])
    media = set(((exc.get("blockedMedia") or {}).get("items") or {}).get("enum") or [])
    if not {"allergy", "accessibility", "familyAndChildren"} <= cats or media != {"image", "audio", "file"}:
        bad.append(("R-EXCLUDE", f"AiPolicy.globalEndpointExclusions is {sorted(cats)} / {sorted(media)}"))
    if "isStatelessOnly" not in (S(ai, "AiProvider").get("properties") or {}):
        bad.append(("R-STATELESS", "AiProvider.isStatelessOnly is missing"))
    aud = ((S(ai, "AiInteraction").get("properties") or {}).get("scrubAudit") or {}).get("properties") or {}
    if "entityCounts" not in aud or any(k in aud for k in ("entities", "values", "matches")):
        bad.append(("R-AUDIT", "AiInteraction.scrubAudit must carry entityCounts and never the values"))
    desc = str(S(com, "AiResidencyClass").get("description") or "")
    if "ae.api.openai.com" not in desc or "never widens residency" not in desc.lower().replace("**", ""):
        bad.append(("R-UAE-OPENAI", "AiResidencyClass does not name ae.api.openai.com and the no-widening rule"))

    bad += embed_findings(S(ai, "AiProvider"), S(ai, "AiPolicy"))
    for rel in ("contracts/satellite/ai.yaml", "contracts/shared/common.yaml", "contracts/spine/tenancy.yaml"):
        for n, line in enumerate(io.open(os.path.join(ROOT, rel), encoding="utf-8"), 1):
            bad += line_findings(rel, n, line)

    for r, d in bad:
        print(f"  {r:<12} {d}")
    if bad:
        print(f"FAIL {len(bad)} finding(s)")
        return 1
    print("ok: tenant category lock, residual pattern pass, pinned scrubber, global exclusions, stateless global "
          "calls, count-only audit, the UAE OpenAI project, our in-cell embedder and reranker and no hosted LLM are all "
          "in the contracts (and the self-tests pass)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
