# What this machine can run

_Generated 2026-08-17 14:26 UTC_

| | |
|---|---|
| GPU | NVIDIA GeForce RTX 4080 Laptop GPU |
| VRAM | 12.0 GiB total, 10.8 GiB free |
| System RAM | 31.6 GiB |
| Disk free | 286 GiB |

VRAM figures are fp16 weights x 1.25 for encoding headroom.

**Shared/system GPU memory is not counted and should not be.** CUDA reports only
dedicated VRAM; the driver will spill into system RAM over PCIe rather than OOM,
but weights then stream across the bus every forward pass. It turns minutes into
hours, which defeats the point of a quick benchmark.

| Model | Verdict | fp16 | Dims | Licence | Why |
|---|---|---|---|---|---|
| `qwen3-4b` | **RUNS** | 8.0 GB | 2560 | apache-2.0 | needs ~10.0 GiB of 10.8 GiB free |
| `qwen3-0.6b` | **RUNS** | 1.2 GB | 1024 | apache-2.0 | needs ~1.5 GiB of 10.8 GiB free |
| `bge-m3` | **RUNS** | 1.1 GB | 1024 | mit | needs ~1.4 GiB of 10.8 GiB free |
| `e5-large` | **RUNS** | 1.1 GB | 1024 | mit | needs ~1.4 GiB of 10.8 GiB free |
| `nomic-v1.5` | **RUNS** | 0.3 GB | 768 | apache-2.0 | needs ~0.4 GiB of 10.8 GiB free |
| `qwen3-8b` | **NEEDS A BIGGER CARD** | 16.0 GB | 4096 | apache-2.0 | needs ~20.0 GiB, card has 12.0. 4-bit would need ~5.0 GiB but changes what is measured |
| `gte-qwen2-7b` | **NEEDS A BIGGER CARD** | 15.2 GB | 3584 | apache-2.0 | needs ~19.0 GiB, card has 12.0. 4-bit would need ~4.8 GiB but changes what is measured |
| `openai-3-large` | **NEEDS A KEY** | API | 3072 | n/a | OPENAI_API_KEY is not set |
| `openai-3-small` | **NEEDS A KEY** | API | 1536 | n/a | OPENAI_API_KEY is not set |
| `cohere-v4` | **NEEDS A KEY** | API | 1024 | n/a | COHERE_API_KEY is not set |
| `voyage-3-large` | **NEEDS A KEY** | API | 1024 | n/a | VOYAGE_API_KEY is not set |
| `gemini-embed-2` | **NEEDS A KEY** | API | 3072 | n/a | GEMINI_API_KEY is not set |
| `jina-v3` | **LICENCE** | 1.1 GB | 1024 | cc-by-nc-4.0 | weights are public but NON-COMMERCIAL. Self-hosting in a paid product is not licensed. Their API, or drop it. |
| `swan-large` | **UNAVAILABLE** | 14.0 GB | 4096 | unknown | NO PUBLIC CHECKPOINT. github.com/UBC-NLP/swan is a 404 and no Swan model exists on HF. Not substituted. |
| `bge-large-en` | **WRONG SHAPE** | 0.7 GB | 1024 | mit | English-only — cannot serve the Arabic half of the index |
| `e5-large-v2` | **WRONG SHAPE** | 0.7 GB | 1024 | mit | English-only — not the multilingual e5 |

## What that means

**Runs here now (5):** `qwen3-4b`, `qwen3-0.6b`, `bge-m3`, `e5-large`, `nomic-v1.5`

**Would run on a bigger card (2):** `qwen3-8b`, `gte-qwen2-7b`

**Blocked on a key, not on hardware (5):** `openai-3-large`, `openai-3-small`, `cohere-v4`, `voyage-3-large`, `gemini-embed-2`

A bigger card fixes only the first group. `swan-large` has no public checkpoint
at any size, and `jina-v3` is licence-blocked for commercial use however much
VRAM you point at it.

## To run on the server

```bash
python preflight.py                      # confirm there first
python run_eval.py --models qwen3-4b qwen3-0.6b bge-m3 e5-large
```

## The gap no hardware closes

No Arabic **dialectal retrieval** task is published anywhere in `mteb` — checked
across every task type, not just retrieval; the only dialect task in the library
is `HinDialectClassification`, which is Hindi. ArabicMTEB's own dialectal sets
were never released. So the Gulf column stays empty on any machine, and the
MSA-corpus / Gulf-colloquial-query case this eval exists to test is measured by
nothing here.
