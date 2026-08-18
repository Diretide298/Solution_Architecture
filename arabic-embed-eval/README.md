# Bilingual Arabic/English embedding benchmark

Throwaway harness. Four files, one table out.

| file | what it is |
|---|---|
| `00-FINDINGS-before-harness.md` | where ArabicMTEB actually lives, and why most of it is unusable. **Read first.** |
| `models.json` | every candidate, its VRAM, licence and status. Single source of truth. |
| `preflight.py` | what this machine can run, and what needs a bigger card. Writes a report. |
| `run_eval.py` | the benchmark. Writes `results/REPORT.md`. |

## Run it

```bash
python preflight.py                                     # check capacity first
python run_eval.py --models bge-m3 e5-large qwen3-4b
python run_eval.py --models qwen3-8b --multi-gpu        # on a server
python run_eval.py --models openai-3-large              # needs .env
```

The OpenAI key goes in `.env` beside these files, never on the command line:

```
OPENAI_API_KEY=sk-...
```

`.env` is not committed and this whole folder sits outside the ticvai repo.

## Hardware

`preflight.py` reads `models.json` and reports three *different* reasons a model
cannot run, because only one of them is fixed by hardware:

- **memory** — a bigger card fixes it
- **a missing key** — a bigger card does not
- **a licence** — a bigger card does not

```bash
python preflight.py --vram 22.35   # what an A10G would change
python preflight.py --vram 80      # what an A100/H100 would
```

### On AWS g5

| instance | GPUs | VRAM | notes |
|---|---|---|---|
| `g5.16xlarge` | **1** × A10G | 22.35 GiB | 64 vCPU, 256 GiB RAM — but **one GPU** |
| `g5.12xlarge` | **4** × A10G | 4 × 22.35 GiB | 48 vCPU, 192 GiB RAM |

`g5.16xlarge` is the counterintuitive one: despite being the larger instance by
vCPU and RAM, it has a **single** GPU. `g5.12xlarge` has four.

**One A10G at 22.35 GiB is enough for every open model here**, including
`qwen3-8b` (~20 GiB with encoding headroom) and `gte-qwen2-7b` (~19 GiB). No
quantisation needed. So `g5.16xlarge` is sufficient on capacity.

**Multi-GPU buys wall-clock, not capacity.** An 8B embedding model fits on one
card, so extra GPUs are not needed to load it — `--multi-gpu` shards the *corpus*
across devices instead. On `g5.12xlarge` that is roughly 4× the encoding
throughput, and encoding the corpus is where essentially all the time goes. If
the question is "can I run the 8B models", `g5.16xlarge` answers it. If it is
"can I finish quickly", `g5.12xlarge` is the better buy per unit of work despite
fewer vCPUs.

Verify on the box before trusting either claim:

```bash
python preflight.py --out REPORT-capacity-server.md
```

## Tasks

Five, all run in **full** — nothing sampled, so the numbers are comparable to
anyone else's.

| key | task | subset | column |
|---|---|---|---|
| `mlqa-ar` | MLQARetrieval | `ara-ara` | Arabic |
| `sadeem-ar` | SadeemQuestionRetrieval | `ara-Arab` | Arabic |
| `xpqa-ar` | XPQARetrieval | `ara-ara` | Arabic |
| `xpqa-x` | XPQARetrieval | `eng-ara` | cross-lingual |
| `msmarco-en` | MultilingualNanoMSMARCORetrieval | `eng` | English |

MIRACL is deliberately absent: its hard-negatives variant is still 2.46M
passages, which is not a 30-minute run, and sampling it would make the score
incomparable to every published MIRACL number.

## What is missing, and why it is not fixable here

- **Gulf dialectal retrieval — does not exist.** No Arabic dialectal retrieval
  task is published anywhere in `mteb`. ArabicMTEB's own dialectal sets were
  never released; its stated release URL is a 404.
- **Swan-Large — no public checkpoint**, at any size. Not substituted.
- **Cohere, Voyage, Gemini — no keys.**
- **Jina v3 — `cc-by-nc-4.0`**, so self-hosting it in a paid product is not
  licensed regardless of hardware.

Every Arabic column here is MSA-query against MSA-corpus. The real case — MSA
corpus, Gulf colloquial query — is measured by nothing in this run. That is what
the 30–50 query domain eval is for.
