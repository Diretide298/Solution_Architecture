#!/usr/bin/env python3
"""The AI residency and scrubbing safeguards stay in the contracts (CHG-R1S-002, CHG-R1S-016).

**Decided by Chinmay on 2 and 3 October 2026**: a residency class per tenant (DEC-539), mandatory offline
scrubbing (DEC-542), and on 3 October "we are not hosting anything unless client asks it" (the guard is the
provider's content-safety service, no in-cell model; `docs/active/decisions/answers-3-october-gate-and-hosting.md`).
The legal research of 3 October (`docs/active/research/openai-key-uae-3-october.md`, "What this means for
TICVAI") added the safeguards that make "personal data never leaves the UAE in clear" a claim that can be made.
Each is a contract fact, and a contract fact is easy to lose in an edit. This check holds them:

    R-CATEGORY   tenancy RegionSettings.tenantCategory exists, and updateRegionSettings declares
                 `residency-category-refused`
    R-PATTERN    AiPolicy.scrubbing carries `residualPatternCheck` (all five patterns) and `scrubberVersion`
    R-EXCLUDE    AiPolicy.globalEndpointExclusions names allergy, accessibility and familyAndChildren and
                 blocks image, audio and file
    R-STATELESS  AiProvider.statelessOnly exists
    R-AUDIT      AiInteraction.scrubAudit carries entityCounts and no field that could hold a value
    R-UAE-OPENAI common AiResidencyClass names `ae.api.openai.com` and says failover never widens residency
    R-NOHOST     no contract names Qwen3Guard or an in-cell gpt-oss fallback as ours (only on a client's estate)
    R-EMBED      no contract names a self-hosted embedding or reranking model: embeddings are the provider's on
                 the UAE route (Chinmay, 3 October evening, CHG-R1S-026)

    python tools/check-ai-residency.py
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


def main() -> int:
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
    if "statelessOnly" not in (S(ai, "AiProvider").get("properties") or {}):
        bad.append(("R-STATELESS", "AiProvider.statelessOnly is missing"))
    aud = ((S(ai, "AiInteraction").get("properties") or {}).get("scrubAudit") or {}).get("properties") or {}
    if "entityCounts" not in aud or any(k in aud for k in ("entities", "values", "matches")):
        bad.append(("R-AUDIT", "AiInteraction.scrubAudit must carry entityCounts and never the values"))
    desc = str(S(com, "AiResidencyClass").get("description") or "")
    if "ae.api.openai.com" not in desc or "never widens residency" not in desc.lower().replace("**", ""):
        bad.append(("R-UAE-OPENAI", "AiResidencyClass does not name ae.api.openai.com and the no-widening rule"))

    for rel in ("contracts/satellite/ai.yaml", "contracts/shared/common.yaml", "contracts/spine/tenancy.yaml"):
        for n, line in enumerate(io.open(os.path.join(ROOT, rel), encoding="utf-8"), 1):
            if re.search(r"qwen3guard", line, re.I) and not re.search(r"not a hosted|not hosted|self-host|client", line, re.I):
                bad.append(("R-NOHOST", f"{rel}:{n} names Qwen3Guard as ours"))
            if re.search(r"in-cell (gpt-oss|open-weights|open model|model)", line, re.I) and \
                    not re.search(r"dropped|no in-cell|there is no|host none", line, re.I):
                bad.append(("R-NOHOST", f"{rel}:{n} names an in-cell model as a fallback"))
            if re.search(r"bge-m3|cross-encoder", line, re.I) and not re.search(r"supersede|went with|no longer", line, re.I):
                bad.append(("R-EMBED", f"{rel}:{n} names a self-hosted embedding or reranking model (CHG-R1S-026)"))

    for r, d in bad:
        print(f"  {r:<12} {d}")
    if bad:
        print(f"FAIL {len(bad)} finding(s)")
        return 1
    print("ok: tenant category lock, residual pattern pass, pinned scrubber, global exclusions, stateless global "
          "calls, count-only audit, the UAE OpenAI project and no hosted model are all in the contracts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
