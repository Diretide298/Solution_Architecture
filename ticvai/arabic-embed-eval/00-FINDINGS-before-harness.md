# Where ArabicMTEB actually lives — and what that costs the eval

Answer to the first job, before any harness code. Checked 17 Aug 2026.

**Short version: your read of the wheel was right, and the reason is worse than a packaging
gap. ArabicMTEB was never released as a benchmark. The paper's only stated URL is dead, and
the half of it you care about most — dialectal retrieval, Gulf — is not published anywhere I
can find.**

---

## 1. The paper's release URL is a 404

The paper states, once, in the abstract and nowhere else:

> "Our models and benchmark are available at our GitHub page: https://github.com/UBC-NLP/swan"

```
GET https://github.com/UBC-NLP/swan          -> HTTP 404
GET https://api.github.com/repos/UBC-NLP/Swan -> {"message": "Not Found"}
```

Not a redirect, not a rename. I enumerated **all 70 public repos in the UBC-NLP org**: there
is no `swan`, no `ArabicMTEB`, nothing embedding-related. The only Arabic repos are
`wanlp2020_arabic_fake_news_detection` and `Arabic-Dangerous-Dataset`, both from 2020.

## 2. It is not on Hugging Face under any obvious name

| query | result |
|---|---|
| `datasets?search=arabicmteb` | **0 results** |
| `models?search=swan` | 20 results, all unrelated (`Ron_Swanson-Parks_and_Rec`, `swang2000/...`) |
| `models?author=UBC-NLP` | 60 models — `ARBERT`, `ARBERTv2`, `MARBERT`, `MARBERTv2`. **No Swan.** |
| `datasets?search=MoroccoDIA` / `GulfDIA` / `dialectal arabic retrieval` | **0 results** |

`ARBERTv2` is the *base* Swan-Small was built from, not Swan itself.

## 3. It is not in `mteb`, and not just in 2.19.3

`mteb/benchmarks/benchmarks.py` on `main` contains **no case-insensitive match for "arabic"**.
There is no `MTEB(Arabic)` benchmark object and no ArabicMTEB task group. So this is not a
wheel-packaging problem you can fix with a source install — the tasks were never contributed
upstream.

## 4. What *does* exist: the MSA retrieval half, on a personal account, undocumented

Gagan Bhatia (`gagan3012`), a paper co-author, has the retrieval datasets on his personal
account under the prefix **`dolphin-retrival-`** — note the misspelling, which is why every
search for "retrieval" misses them. Uploaded March 2024, no README on most, not linked from
the paper.

| paper name | HF repo | structure |
|---|---|---|
| LAREQA | `gagan3012/dolphin-retrival-LAREQA-QA` | **complete** — `corpus/corpus`, `corpus/queries`, `qrels/test` |
| DAWQS | `dolphin-retrival-DAWQS-QA-corpus` + `-qrels` | corpus+queries parquet, qrels separate |
| EXAMS | `dolphin-retrival-EXAMS-QA-corpus` + `-qrels` | same |
| MKQA | `dolphin-retrival-MKQA-QA-corpus` + `-qrels` | same |
| MLQA | `dolphin-retrival-MLQA-QA-corpus` + `-qrels` | same |
| ARCD | `dolphin-retrival-ARCD-QA-corpus` + `-qrels` | same |
| TyDiQA | `dolphin-retrival-TyDiQA-QA-corpus` + `-qrels` | same |
| XSQUAD | `dolphin-retrival-XSQUAD-QA-corpus` | **corpus only — no qrels repo exists** |

These are the MSA retrieval sets named in the paper. They are usable: BEIR-shaped, public,
ungated. They would need registering as **custom `mteb` tasks** — there is no shortcut.

`gagan3012/armtbench` looked promising by name and is a red herring: 80 examples of
`question_id / category / turns / reference`. That is Arabic **MT-Bench**, a judge set, not
ArabicMTEB.

## 5. What does **not** exist — and this is the priority-1 task

- **Dialectal ArabicMTEB retrieval: not found.** The paper names only `MoroccoDIA` and
  `EgyptDIA` in its tables and describes coverage of "Algeria, Egypt, Morocco, and the Gulf".
  No repo for any of them, under either author account, the org, or a global HF search.
  **There is no published Gulf dialectal retrieval set.**
- **Cross-lingual retrieval (`ar2en`, `en2ar`, `ar2de`…): not found.**
- **Swan-Large: not downloadable.** No Swan checkpoint exists publicly, small or large.

---

## What this costs your four tasks

| # | task | status |
|---|---|---|
| 1 | **Dialectal ArabicMTEB, Gulf** | **Cannot run.** Not published. This is the one you said matters. |
| 2 | ArabicMTEB Retrieval | **Partial** — 7 of 8 MSA sets (XSQUAD lacks qrels), as custom tasks. Cross-lingual: cannot run. |
| 3 | MIRACL Arabic | **Runs.** `MIRACLRetrieval` ships in `mteb` with an `ar` split. |
| 4 | English retrieval | **Runs.** Any standard MTEB retrieval task. |

## What this costs your four models

| model | status |
|---|---|
| BAAI/bge-m3 | **Runs.** Open, ~2.2 GB, fits the GPU. |
| UBC-NLP Swan-Large | **Cannot run — no public checkpoint.** Flagged, not substituted, per your instruction. Even if released: ArMistral is 7B, ≈14 GB in fp16, and the GPU is 12.9 GB. |
| Cohere embed-v4 | **Blocked — `COHERE_API_KEY` is unset.** |
| Gemini Embedding 2 | **Blocked — `GEMINI_API_KEY` is unset.** |

## Environment

```
python (default)  3.9.0   <- mteb needs >=3.10
python (miniconda) 3.13    C:\ProgramData\miniconda3\python.exe   <- use this
torch             2.7.1+cu118, CUDA available
GPU               RTX 4080 Laptop, 12.9 GB
mteb              not installed
COHERE_API_KEY    MISSING
GEMINI_API_KEY    MISSING
HF_TOKEN          MISSING (not needed — all the above repos are ungated)
```

## The honest position

As specified, the run would produce **one model against three of four tasks**, with the
decisive Gulf column empty. That is not a shortlist-narrowing result; it is a table with one
row.

Two things unblock most of it, and only you can do them:

1. **The two API keys** — takes it from 1 model to 3, which is a real comparison.
2. **A decision on Gulf.** No public benchmark covers it. Options, none silent:
   - *Accept the gap* — run MSA + MIRACL + English, and treat Gulf as unmeasured until the
     domain eval. Defensible, and the domain eval was always going to decide it.
   - *Build a proxy* — `UBC-NLP/alexandria` is English↔dialectal Arabic across 13 Arab
     countries including Gulf, and `gagan3012/habibi_dialects_data` exists. Either could be
     turned into a bitext-retrieval proxy for Gulf. **This is a substitution and a weaker
     claim than the paper's benchmark** — it measures dialect sensitivity, not your task.
   - *Ask the authors* — the paper claims public release and the URL is dead; that is worth
     an email, but it is not a 30-minute path.

## What this run still cannot answer

Unchanged from your brief, and worth restating because the gaps above make it sharper:

- No public benchmark covers venue policies, allergen lists or refund windows.
- None covers code-mixing — an Arabic query containing "Yas Waterworld" and "annual pass".
- With Gulf dialectal retrieval unpublished, **nothing here measures MSA-corpus /
  Gulf-colloquial-query retrieval, which is your actual failure mode.**

A 30–50 query domain eval against real tenant content is now not just the decider — it is the
only thing that will measure the case you are worried about.
