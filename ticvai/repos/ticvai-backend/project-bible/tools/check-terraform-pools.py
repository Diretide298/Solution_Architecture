#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every AKS node pool the LLD draws is a node pool of the Terraform cell module, at the size the LLD gives it.

**6 October 2026, CHG-R4-008.** CHG-R11-001 (4 October) decided one AI GPU node pool in the cell (Azure
Standard_NV6ads_A10_v5, tainted for the AI pods, one node without HA, two with HA), and the HLD/LLD and the cost were
rebuilt for it; the Terraform the package carries (repos/ticvai-infra/terraform/modules/cell) kept only its CPU "ai"
pool, so the cell it would build had no GPU at all. Nothing compared the two.

**What fails** (handoff/design-batches/HLD-LLD/architecture.json `lld`, repos/ticvai-infra/terraform/modules/cell/*.tf):

  T-POOL-MISSING   a node the LLD labels "AKS <name> pool" whose VM size (its first line, e.g. "NV6ads A10 v5 x2" ->
                   Standard_NV6ads_A10_v5) is the vm_size of no node pool in the module (the default node pool included,
                   a `var.` size read from its default in variables.tf)

Read-only, no HCL library: the sizes are read with patterns from the module's own layout. Exit 1 on any finding.

    python3 tools/check-terraform-pools.py
"""
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
ARCH = ROOT / "handoff" / "design-batches" / "HLD-LLD" / "architecture.json"
MOD = ROOT / "repos" / "ticvai-infra" / "terraform" / "modules" / "cell"


def lld_sizes() -> dict:
    """{pool label: Standard_<size>} for every 'AKS ... pool' node of the LLD."""
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    out = {}
    for n in (arch.get("lld") or {}).get("nodes") or []:
        label = str(n.get("label") or "")
        if not re.match(r"AKS .*pool", label):
            continue
        first = str((n.get("lines") or [""])[0]).split(",")[0]
        size = re.sub(r"\s+x\d+.*$", "", first).strip()
        if re.match(r"^[A-Z]+\d", size):
            out[label] = "Standard_" + size.replace(" ", "_")
    return out


def module_sizes() -> set:
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(MOD.glob("*.tf")))
    defaults = {m.group(1): m.group(2) for m in re.finditer(
        r'variable\s+"(\w+)"\s*\{[^}]*?default\s*=\s*"([^"]+)"', text, re.S)}
    out = set()
    for m in re.finditer(r'vm_size\s*=\s*(var\.(\w+)|"([^"]+)")', text):
        out.add(defaults.get(m.group(2), "") if m.group(2) else m.group(3))
    return out


def main() -> int:
    if not ARCH.exists() or not MOD.exists():
        print("check-terraform-pools: architecture.json or the cell module is missing; nothing to compare")
        return 0
    want, have = lld_sizes(), module_sizes()
    bad = {k: v for k, v in want.items() if v not in have}
    print(f"check-terraform-pools: {len(want)} AKS pool(s) in the LLD, {len(have)} node pool size(s) in the module")
    for k, v in sorted(bad.items()):
        print(f"  FAIL T-POOL-MISSING  the LLD's {k} ({v}) is no node pool of repos/ticvai-infra/terraform/modules/cell")
    if bad:
        print(f"FAIL - {len(bad)} pool(s) the Terraform does not build")
        return 1
    print("PASS - every AKS pool the LLD draws is a node pool of the Terraform cell module")
    return 0


if __name__ == "__main__":
    sys.exit(main())
