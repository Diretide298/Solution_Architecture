"""
What can this machine actually run, and what needs the server.

  python preflight.py                    # report for this box
  python preflight.py --vram 80          # what an 80 GB card would change
  python preflight.py --out REPORT-capacity.md

Writes a markdown report rather than only printing, because the point of it is
to be pasted into a decision about where to run, by someone who is not sitting
at this terminal.

It reports three separate reasons a model cannot run, and never conflates them:
memory, a missing key, and a licence. Only the first is fixed by a bigger card.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent


def load_env() -> None:
    f = HERE / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def hardware(vram_override: float | None) -> dict:
    info = {"gpu": None, "vram_total": 0.0, "vram_free": 0.0, "ram_total": 0.0, "disk_free": 0.0}
    try:
        import torch

        if torch.cuda.is_available():
            p = torch.cuda.get_device_properties(0)
            free, total = torch.cuda.mem_get_info()
            info["gpu"] = p.name
            info["vram_total"] = total / 2**30
            info["vram_free"] = free / 2**30
    except Exception:
        pass
    try:
        import psutil

        info["ram_total"] = psutil.virtual_memory().total / 2**30
    except Exception:
        try:  # stdlib fallback, good enough for a report
            info["ram_total"] = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 2**30
        except Exception:
            pass
    info["disk_free"] = shutil.disk_usage(HERE).free / 2**30

    if vram_override is not None:
        info["gpu"] = f"(hypothetical {vram_override:.0f} GiB card)"
        info["vram_total"] = info["vram_free"] = vram_override
    return info


VERDICT_ORDER = {"RUNS": 0, "TIGHT": 1, "NEEDS A BIGGER CARD": 2,
                 "NEEDS A KEY": 3, "LICENCE": 4, "UNAVAILABLE": 5, "WRONG SHAPE": 6}


def judge(key: str, m: dict, hw: dict, overhead: float) -> tuple[str, str]:
    status = m.get("status", "ok")
    if status == "unavailable":
        return "UNAVAILABLE", m["note"]
    if status == "licence-blocked":
        return "LICENCE", m["note"]
    if status == "english-only":
        return "WRONG SHAPE", m["note"]

    if m["kind"] != "st":
        env = m.get("env", "")
        if os.environ.get(env):
            return "RUNS", f"{env} is set · ${m.get('price_per_m', 0)}/M tokens"
        return "NEEDS A KEY", f"{env} is not set"

    need = m["vram_fp16_gb"] * overhead
    free = hw["vram_free"] or hw["vram_total"]
    if need <= free:
        return "RUNS", f"needs ~{need:.1f} GiB of {free:.1f} GiB free"
    if need <= hw["vram_total"]:
        return "TIGHT", f"needs ~{need:.1f} GiB, card has {hw['vram_total']:.1f} but only {free:.1f} free"
    return "NEEDS A BIGGER CARD", (
        f"needs ~{need:.1f} GiB, card has {hw['vram_total']:.1f}. "
        f"4-bit would need ~{m['vram_fp16_gb'] / 4 * overhead:.1f} GiB but changes what is measured"
    )


def main() -> None:
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--vram", type=float, default=None, help="pretend the card has this many GiB")
    ap.add_argument("--out", default="REPORT-capacity.md")
    args = ap.parse_args()

    cfg = json.loads((HERE / "models.json").read_text(encoding="utf-8"))
    overhead = cfg["overhead"]
    hw = hardware(args.vram)

    rows = []
    for key, m in cfg["models"].items():
        verdict, why = judge(key, m, hw, overhead)
        rows.append((VERDICT_ORDER[verdict], key, m, verdict, why))
    rows.sort(key=lambda r: (r[0], -(r[2].get("vram_fp16_gb") or 0)))

    out = [
        "# What this machine can run",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
        "| | |",
        "|---|---|",
        f"| GPU | {hw['gpu'] or '**none detected**'} |",
        f"| VRAM | {hw['vram_total']:.1f} GiB total, {hw['vram_free']:.1f} GiB free |",
        f"| System RAM | {hw['ram_total']:.1f} GiB |",
        f"| Disk free | {hw['disk_free']:.0f} GiB |",
        "",
        f"VRAM figures are fp16 weights x {overhead} for encoding headroom.",
        "",
        "**Shared/system GPU memory is not counted and should not be.** CUDA reports only",
        "dedicated VRAM; the driver will spill into system RAM over PCIe rather than OOM,",
        "but weights then stream across the bus every forward pass. It turns minutes into",
        "hours, which defeats the point of a quick benchmark.",
        "",
        "| Model | Verdict | fp16 | Dims | Licence | Why |",
        "|---|---|---|---|---|---|",
    ]
    for _o, key, m, verdict, why in rows:
        vram = f"{m['vram_fp16_gb']:.1f} GB" if m["vram_fp16_gb"] else "API"
        out.append(
            f"| `{key}` | **{verdict}** | {vram} | {m.get('dims', '?')} | "
            f"{m.get('license', 'n/a')} | {why} |"
        )

    runs = [r[1] for r in rows if r[3] == "RUNS"]
    bigger = [r[1] for r in rows if r[3] in ("NEEDS A BIGGER CARD", "TIGHT")]
    keys = [r[1] for r in rows if r[3] == "NEEDS A KEY"]

    out += [
        "",
        "## What that means",
        "",
        f"**Runs here now ({len(runs)}):** " + (", ".join(f"`{k}`" for k in runs) or "none"),
        "",
        f"**Would run on a bigger card ({len(bigger)}):** " + (", ".join(f"`{k}`" for k in bigger) or "none"),
        "",
        f"**Blocked on a key, not on hardware ({len(keys)}):** " + (", ".join(f"`{k}`" for k in keys) or "none"),
        "",
        "A bigger card fixes only the first group. `swan-large` has no public checkpoint",
        "at any size, and `jina-v3` is licence-blocked for commercial use however much",
        "VRAM you point at it.",
        "",
        "## To run on the server",
        "",
        "```bash",
        "python preflight.py                      # confirm there first",
        "python run_eval.py --models " + " ".join(runs[:4] or ["bge-m3"]),
        "```",
        "",
        "## The gap no hardware closes",
        "",
        "No Arabic **dialectal retrieval** task is published anywhere in `mteb` — checked",
        "across every task type, not just retrieval; the only dialect task in the library",
        "is `HinDialectClassification`, which is Hindi. ArabicMTEB's own dialectal sets",
        "were never released. So the Gulf column stays empty on any machine, and the",
        "MSA-corpus / Gulf-colloquial-query case this eval exists to test is measured by",
        "nothing here.",
        "",
    ]

    text = "\n".join(out)
    (HERE / args.out).write_text(text, encoding="utf-8")
    print(text)
    print(f"\nwritten to {HERE / args.out}")


if __name__ == "__main__":
    main()
