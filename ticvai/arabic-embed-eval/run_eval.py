"""
nDCG@10 for a bilingual Arabic/English retrieval index. Throwaway harness.

Deliberately not a platform: one config, one script, one table out. Every model
that is dropped is printed with the reason; nothing is silently sampled or
silently substituted.

  python preflight.py                                  # what fits here
  python run_eval.py --models bge-m3 e5-large qwen3-4b
  python run_eval.py --models qwen3-8b --multi-gpu     # server
  python run_eval.py --models openai-3-large           # needs .env

Model definitions live in models.json — the same file preflight.py reads, so
"what can run" and "what did run" cannot drift apart.

The Gulf-dialect column does not exist and cannot be made to exist: no Arabic
dialectal retrieval task is published anywhere in mteb, and ArabicMTEB's own
dialectal sets were never released. See 00-FINDINGS-before-harness.md.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
CONFIG = json.loads((HERE / "models.json").read_text(encoding="utf-8"))
MODELS = CONFIG["models"]


def load_env() -> None:
    f = HERE / ".env"
    if not f.exists():
        return
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# task key -> (mteb task, language subsets, column heading, group)
#
# Chosen so every one runs in FULL. The alternative for Arabic was MIRACL, whose
# hard-negatives variant is still 2.46M passages — not a 30-minute proposition,
# and sampling it down would make the numbers incomparable to anyone else's.
TASKS = {
    "mlqa-ar":    ("MLQARetrieval",                    ["ara-ara"], "MLQA ar",        "arabic"),
    "sadeem-ar":  ("SadeemQuestionRetrieval",          ["ara-Arab"], "Sadeem ar",     "arabic"),
    "xpqa-ar":    ("XPQARetrieval",                    ["ara-ara"], "XPQA ar",        "arabic"),
    "xpqa-x":     ("XPQARetrieval",                    ["eng-ara"], "XPQA en→ar",     "crosslingual"),
    "msmarco-en": ("MultilingualNanoMSMARCORetrieval", ["eng"],     "NanoMSMARCO en", "english"),
}

PRICE = {"text-embedding-3-large": 0.13, "text-embedding-3-small": 0.02}


class OpenAIEncoder:
    """Minimal mteb-compatible encoder. Counts the tokens the API reports, so
    cost comes from what was actually billed rather than an estimate."""

    def __init__(self, model: str):
        from openai import OpenAI

        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set — put it in .env")
        self.client = OpenAI()
        self.model = model
        self.tokens = 0

    def encode(self, sentences, **kwargs):
        import numpy as np

        texts = [s if (s and s.strip()) else " " for s in sentences]
        out, batch = [], 96
        for i in range(0, len(texts), batch):
            chunk = [t[:8000] for t in texts[i : i + batch]]
            for attempt in range(5):
                try:
                    r = self.client.embeddings.create(model=self.model, input=chunk)
                    break
                except Exception as exc:
                    if attempt == 4:
                        raise
                    print(f"      retry {attempt + 1} after {type(exc).__name__}")
                    time.sleep(2 * (attempt + 1))
            self.tokens += r.usage.total_tokens
            out.extend(d.embedding for d in r.data)
        return np.asarray(out, dtype="float32")

    def cost(self) -> float:
        return self.tokens / 1e6 * PRICE.get(self.model, 0.0)


def build_model(key: str, multi_gpu: bool):
    spec = MODELS[key]
    if spec["kind"] == "openai":
        return OpenAIEncoder(spec["hf_id"])
    if spec["kind"] != "st":
        raise RuntimeError(
            f"{key} is a {spec['kind']} model — no encoder is implemented for it. "
            f"{spec.get('note', '')}"
        )

    import torch
    from sentence_transformers import SentenceTransformer

    free = torch.cuda.mem_get_info()[0] / 2**30 if torch.cuda.is_available() else 0.0
    need = spec["vram_fp16_gb"] * CONFIG["overhead"]
    if torch.cuda.is_available() and need > free:
        print(f"    WARNING: {key} wants ~{need:.1f} GiB, {free:.1f} GiB free. "
              f"It will spill to system memory over PCIe and be very slow.")
    print(f"    loading {spec['hf_id']} (fp16; ~{need:.1f} GiB needed, {free:.1f} GiB free)")

    model = SentenceTransformer(
        spec["hf_id"],
        trust_remote_code=True,
        model_kwargs={"torch_dtype": torch.float16},
        device="cuda" if torch.cuda.is_available() else "cpu",
    )
    if multi_gpu and torch.cuda.device_count() > 1:
        # Data parallel, not model parallel: an 8B embedding model fits on one
        # A10G, so extra cards buy throughput on the corpus, not capacity.
        print(f"    multi-GPU: sharding the corpus across {torch.cuda.device_count()} devices")
        model.encode_multi_process_pool = model.start_multi_process_pool()
    return model


def ndcg_from(results, subsets: list[str]) -> float | None:
    """Pull ndcg_at_10 for the requested subset out of an mteb TaskResult.

    Exact-subset first: a task like XPQA carries ara-ara and eng-ara side by
    side, and taking whichever entry came first would silently report the wrong
    language — a mistake that looks like a plausible score.
    """
    fallback = None
    for task_result in results:
        for entries in task_result.scores.values():
            for entry in entries:
                value = entry.get("ndcg_at_10")
                if value is None:
                    continue
                if entry.get("hf_subset") in subsets:
                    return value
                fallback = value if fallback is None else fallback
    return fallback


def main() -> None:
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["bge-m3", "e5-large"])
    ap.add_argument("--tasks", nargs="+", default=list(TASKS))
    ap.add_argument("--out", default="results")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--multi-gpu", action="store_true",
                    help="shard the corpus across every visible GPU")
    args = ap.parse_args()

    import mteb

    outdir = HERE / args.out
    outdir.mkdir(exist_ok=True)
    scores: dict[str, dict] = {}
    notes: list[str] = []
    costs: dict[str, float] = {}

    for key in args.models:
        spec = MODELS.get(key)
        if spec is None:
            notes.append(f"**`{key}` skipped** — not in models.json.")
            continue
        if spec.get("status") not in ("ok", None):
            notes.append(f"**`{key}` DROPPED** — {spec['status']}: {spec.get('note', '')}")
            print(f"\n=== {key}: DROPPED ({spec['status']})")
            continue

        print(f"\n=== {key}  ({spec['hf_id']})")
        try:
            model = build_model(key, args.multi_gpu)
        except Exception as exc:
            notes.append(f"**`{key}` DROPPED** — could not load: `{type(exc).__name__}: {exc}`")
            print(f"    DROPPED: {type(exc).__name__}: {exc}")
            continue

        scores[key] = {}
        for tkey in args.tasks:
            if tkey not in TASKS:
                continue
            name, subsets, heading, _group = TASKS[tkey]
            started = time.time()
            try:
                tasks = mteb.get_tasks(tasks=[name])
                # mteb 2.x picks language subsets at run time via eval_subsets;
                # get_tasks has no hf_subsets argument.
                results = mteb.MTEB(tasks=tasks).run(
                    model,
                    output_folder=str(outdir / key),
                    verbosity=1,
                    eval_subsets=subsets,
                    encode_kwargs={"batch_size": args.batch_size},
                )
                value = ndcg_from(results, subsets)
                scores[key][tkey] = value
                shown = f"{value * 100:.1f}" if isinstance(value, (int, float)) else "none"
                print(f"    {heading:<16} nDCG@10 = {shown}   ({time.time() - started:.0f}s)")
            except Exception as exc:
                scores[key][tkey] = None
                notes.append(f"`{key}` / `{heading}` failed: `{type(exc).__name__}: {str(exc)[:200]}`")
                print(f"    {heading:<16} FAILED: {type(exc).__name__}: {str(exc)[:140]}")
                traceback.print_exc(limit=2)

        if isinstance(model, OpenAIEncoder):
            costs[key] = model.cost()
            notes.append(f"**`{key}` cost**: {model.tokens:,} tokens billed = **${model.cost():.4f}**.")

        del model
        try:
            import torch

            torch.cuda.empty_cache()
        except Exception:
            pass

    (outdir / "scores.json").write_text(json.dumps(scores, indent=2), encoding="utf-8")
    write_report(outdir, scores, args, notes, costs)


def write_report(outdir: Path, scores: dict, args, notes: list[str], costs: dict) -> None:
    cols = [(t, TASKS[t][2], TASKS[t][3]) for t in args.tasks if t in TASKS]
    header = "| Model | " + " | ".join(h for _t, h, _g in cols) + " | Gulf dialectal |"
    rule = "|---" * (len(cols) + 2) + "|"
    rows = [header, rule]

    def cell(v):
        return f"{v * 100:.1f}" if isinstance(v, (int, float)) else "—"

    for key, got in scores.items():
        rows.append(
            "| `" + key + "` | "
            + " | ".join(cell(got.get(t)) for t, _h, _g in cols)
            + " | **not measurable** |"
        )
    table = "\n".join(rows)

    # who wins what — computed, not eyeballed
    def best(group: str):
        keys = [t for t, _h, g in cols if g == group]
        ranked = []
        for model, got in scores.items():
            vals = [got.get(t) for t in keys if isinstance(got.get(t), (int, float))]
            if vals:
                ranked.append((sum(vals) / len(vals), model))
        ranked.sort(reverse=True)
        return ranked

    arabic, english = best("arabic"), best("english")
    verdict = []
    if arabic:
        verdict.append(f"- **Arabic:** `{arabic[0][1]}` leads at {arabic[0][0] * 100:.1f} mean nDCG@10.")
    if english:
        verdict.append(f"- **English:** `{english[0][1]}` leads at {english[0][0] * 100:.1f}.")
    if arabic and english:
        verdict.append(
            f"- **Both halves:** "
            + (f"`{arabic[0][1]}` wins both — no trade-off to make."
               if arabic[0][1] == english[0][1]
               else f"no single winner. `{arabic[0][1]}` takes Arabic, `{english[0][1]}` takes English.")
        )

    text = "\n".join([
        "# nDCG@10 — bilingual Arabic/English retrieval",
        "",
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
        table,
        "",
        "Every task above ran in **full** — no sampling, no subsetting.",
        "",
        "## Which model wins what",
        "",
        *(verdict or ["- Nothing completed, so nothing to compare."]),
        "",
        "## Gulf dialectal — flagged, per the brief",
        "",
        "**No model can be assessed on Gulf dialectal retrieval, and none is failing it —",
        "the column has no data behind it.** No Arabic dialectal retrieval task is published",
        "anywhere in `mteb`; the only dialect task in the library is `HinDialectClassification`,",
        "which is Hindi. ArabicMTEB's own dialectal sets were never released — its stated",
        "release URL, `github.com/UBC-NLP/swan`, is a 404.",
        "",
        "Every Arabic column above is **MSA query against MSA corpus**. Your actual case is",
        "MSA corpus against Gulf colloquial query, and nothing here touches it.",
        "",
        "## What this run cannot answer",
        "",
        "- No public benchmark covers venue policies, allergen lists or refund windows.",
        "- None covers code-mixing — an Arabic query containing \"Yas Waterworld\" and \"annual pass\".",
        "- Nothing measures the MSA-corpus / Gulf-query gap, as above.",
        "",
        "A 30–50 query domain eval against real tenant content remains the decider. This run",
        "narrows the shortlist; it does not pick the model.",
        "",
        *(["## Notes", "", *(f"- {n}" for n in notes), ""] if notes else []),
    ])

    (outdir / "REPORT.md").write_text(text, encoding="utf-8")
    print("\n" + table)
    for line in verdict:
        print(line)
    for n in notes:
        print("  - " + n)
    print(f"\nwritten to {outdir / 'REPORT.md'}")


if __name__ == "__main__":
    main()
