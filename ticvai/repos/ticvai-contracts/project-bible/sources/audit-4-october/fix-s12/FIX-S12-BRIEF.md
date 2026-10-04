# Fix round on the Sprint 1-2 judging (4 October 2026): shared brief

The judge read every Sprint 1 and Sprint 2 ticket of the r1 package (main 857986c1) the way a developer pulls it, with zero tools, and said whether it can be built. Results: 1,030 tickets; 16 buildable as written, 893 with guesses, **121 not buildable**; **436 blocker findings**. Chinmay: fix all of it in one round, then one refresh, then r1. Sprint 1 starts Monday 5 Oct.

## Read first
- `D:\Chinmay\adam\audit\ticvai\apply\SPEC-FIX-BRIEF.md`: the rules of the last fix round. **They all apply here** (own worktree and branch; only your files; fix the cause, generator and instances; prevention as a check registered in run-checks; contracts additive and the new-operation gates; commit authored files only; scoped checks; keep tokens low; concise report). Your branch and batch code are in your prompt.
- `D:\Chinmay\adam\audit\ticvai\answers-2-oct-batch1.md`: Chinmay's decisions. Binding: "Pattern 4", "Block A audit business rules" with "Asked as questions instead of defaults", "Defaults taken during the spec fixes", "r1 additions", and every later section. Later overrides earlier.
- Your findings: `D:\Chinmay\adam\audit\ticvai\runs\fix-s12\<area>.tsv` (key, verdict NO/guess, kind, category, issue, evidence). The full set is `findings-s12.json`. The judged packs (what the developer saw) are in `D:\Chinmay\adam\audit\ticvai\runs\r1-regate\packed-s1|packed-s2|packed-s12m|packed\<KEY>\`.

## Verify before you fix
The judge saw only the pulled pack, cut at 150k characters (cut files are named in each row's `cut` list in `runs/r1-regate/direct/*.jsonl`). A finding can be false: the thing exists but was not in the pack. Check the package first. If it exists but the pull did not carry it, that is a **link/pull** problem: give it to the plan agent through the ledger (below), don't change the spec.

## Order of priority
1. Every **NO** ticket in your file: after your fix, a developer can build it without guessing.
2. Every blocker on a "guess" ticket.
3. Systemic causes (one fix removes many rows): fix the generator or add the missing rule, then the instances.

## The cross-agent ledger
`D:\Chinmay\adam\audit\ticvai\runs\fix-s12\LEDGER.md`. Append-only, one line per request: `[from -> to] KEY: what is needed (agreed name)`. Read it before you start, after each batch of fixes, and before you report. Answer a request by appending `[done by <area>] ...` or `[refused by <area>] ... because ...`. Use agreed operation and field names exactly as written there.

## Limits
- **Block A AI tasks:** do not change any AI-ENGINE-* task, its dates, owner or dependencies. If a fix needs one, write it in your report under "Needs Chinmay".
- Don't change the AI phase plan (`docs/active/ai-phase-plan.json`, branch r1-ai-phase) or refresh tooling (`tools/refresh*.sh`, `run-checks.py` internals, branch refresh-speedup). You may register a new check in run-checks' list; say so in the report so the merge can carry it.
- Questions only Chinmay can answer go in the report, each with the default you took and applied. Client-only questions (e.g. a fiscal field mapping the client must give) get a default plus an entry in the client questions list, not a stop.
- No full refresh. Scoped derive steps and scoped checks only.
- Usage is tight (the wireframes need a reserve): script bulk edits, read only what you need, no whole-file reads of big YAML.

## Report (concise)
Commits; NO tickets fixed (count, and any still NO with why); blockers fixed by kind; generators changed; new checks; change entries; ledger requests made and answered; "Needs Chinmay" with defaults.
