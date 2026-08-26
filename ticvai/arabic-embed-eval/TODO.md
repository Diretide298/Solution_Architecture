# Arabic embedding eval — work index

**7 items parked — A-01 to A-07.**

Generated from `00-FINDINGS-before-harness.md`, which holds the evidence for what
does and does not exist, and the `REPORT-capacity-*.md` files, which hold the
hardware answers. This is the index: one line per item.

| State | Count |
|---|---|
| BLOCKED — needs a key from you | **2** |
| OPEN | **2** |
| CANNOT BE DONE | **1** |
| DONE | **4** |
| **Total open** | **5** |

**Blocking: A-03.** The commercial rows cannot run without an API key. The local
rows can run today.

---

## Cannot be done — 1

| ID | Item | Why |
|---|---|---|
| **A-01** | The **Gulf dialectal column stays empty** | Not a scheduling problem. ArabicMTEB was never released — the paper URL 404s, `github.com/UBC-NLP/swan` is a 404, all 70 org repos were enumerated, and there are 0 matching HF datasets. **No Arabic dialectal retrieval task exists anywhere in `mteb`.** MSA sets exist under `gagan3012/dolphin-retrival-*`, but 3 of 8 have a corpus of one row reading "No Context", LAREQA's corpus is 50 rows, and XSQUAD has no qrels. Any Gulf number in the output would be invented |

## Blocked — needs a key — 2

| ID | Item | Note |
|---|---|---|
| **A-02** | OpenAI row — put `OPENAI_API_KEY` in `arabic-embed-eval/.env` | `.env` is gitignored. It is the only commercial key you said you have |
| **A-03** | Cohere embed-v4 and Gemini Embedding 2 rows | No keys. Either obtain them or drop both from the table and say so in the output rather than leaving blanks that read as failures |

## Open — 2

| ID | Item | Note |
|---|---|---|
| **A-04** | Read the finished smoke-test output in `smoke/` | It completed; nobody has looked at it |
| **A-05** | Full local run — bge-m3, e5-large, qwen3-4b across the five runnable tasks | Runs on this machine. Swan-Large does not fit the local card; see the capacity reports before substituting anything, and **do not** silently swap in a smaller variant |

## Done — 4

| ID | Item |
|---|---|
| **A-D1** | Located ArabicMTEB, or rather established that it does not exist — see A-01 |
| **A-D2** | Isolated venv on Python 3.13 with CUDA torch + mteb, in `.venv/` |
| **A-D3** | `models.json` (16 models) and `preflight.py`, which sorts every model into runs-here / needs-a-bigger-card / needs-a-key / licence-blocked |
| **A-D4** | Capacity answered for g5.16xlarge (1 GPU) vs g5.12xlarge (4 GPU) — `REPORT-capacity-g5-16xl.md`, `REPORT-capacity-server.md` |

---

## Integrity

- **Numbering:** A-01 to A-05, no gaps; done items carry A-D prefixes
- `results/`, `smoke/` and `.cache/` are gitignored, as are `*.safetensors` and
  `*.arrow` — the harness is committed, its outputs are not
- **Subset sizes:** if a full run is too slow, say so in the output. Do not
  sample silently
