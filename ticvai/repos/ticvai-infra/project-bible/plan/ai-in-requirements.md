# AI in Requirements Work

> **Purpose:** Using AI on a 3,184-requirement matrix  
> **Owner:** Chinmay  
> **Status:** Living


Distinct from [setup/llm-conventions](../setup/llm-conventions.md), which governs AI assistance in **writing code**. This page covers AI applied to **requirements analysis**.

## What it is used for

| Use | Value |
|---|---|
| Keyword sweeps across 3,184 requirements | Found 399 AI-related requirements across 19 domains; found 998 hardware-dependent |
| Cross-referencing matrix against seven MoM documents | Surfaced four domains with zero MoM coverage; surfaced contradictions between dated decisions |
| Coverage gap detection | Found 59 sub-domains with no mapped capability — 42.6% of the matrix |
| Duplicate and defect detection | Found duplicate requirement IDs 5.6.1–5.6.8 |

## Where it must not be trusted

| Hazard | Mitigation |
|---|---|
| **Keyword sweeps have high false-positive rates** | "gate", "device", "offline", "till" match unrelated text. Classification output is **always verified against source text** before it enters a register |
| Confident classification of ambiguous text | A sub-domain named "Retail POS" whose only content is "Wallet" needs a human to notice the mismatch |
| Inferring intent from requirement wording | 9.2% of requirements name a human actor. The other 91% is a **decision to be taken**, not a fact to be extracted |
| Summarising instead of citing | Registers cite Requirement IDs. A summary without an ID is not traceable |

## Rules

1. **Reproducible scripts over one-off prompts.** A sweep that cannot be re-run when the matrix updates is a one-time answer to a recurring question.
2. **Every register entry cites its Requirement ID or MoM section.** No exceptions.
3. **Provenance tagging is mandatory** — `MATRIX` / `MOM` / `REF` / `DESIGN`. See [user-story-to-spec](user-story-to-spec.md).
4. **Reference-system material is inspiration, never scope.** Documented exception: revenue recognition rules, by client instruction (12 Aug §8).
5. **Counts are stated with their method.** "998 hardware-dependent requirements" means nothing without the classification rule that produced it.

## Known matrix quirks

- Sheet name is `'Funactionality '` — trailing space
- Requirement IDs 5.6.1–5.6.8 appear twice with different text
- Requirement text spans columns 6 and 7 and must be joined
- Domain in column 2, sub-domain column 4, ID column 5
