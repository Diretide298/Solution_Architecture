# Blind requirement extraction — shared spec

You are extracting requirements from meeting minutes / specification text for a
ticketing-and-venue platform. This is a BLIND extraction.

## Blind rules (hard constraints)

1. Read ONLY the `.txt` files you are explicitly assigned, all of which live under
   the scratchpad `raw/` directory. Read each assigned file IN FULL.
2. Do NOT read, glob, grep or list ANYTHING under `D:\Chinmay\adam` (the project
   repository). No requirement matrix, no coverage docs, no handoff notes, no
   existing requirement lists, no source PDFs/DOCX. If you find yourself about to
   look at a repo file, stop.
3. Do NOT run any existing project script, tool or test. Do not run `run-checks.py`
   or anything like it. Write your own throwaway code if you need code at all.
4. Do NOT search the web.
5. Your output must be derivable from your assigned files alone. Every row carries a
   verbatim quote proving it.

The point of the blindness: these requirements will later be compared, independently,
against a requirements matrix you are not allowed to see. Any leakage destroys the test.

## What counts as a requirement

Anything in the text that states, implies or decides that the system must do, show,
store, enforce, integrate or report something. Include:

- explicit statements ("the dashboard must show live occupancy")
- decisions recorded in the minutes ("agreed: refunds need supervisor approval")
- client asks / expectations, even loosely worded
- open questions that carry an implied requirement — mark them as such
- data, reporting, KPI, filter, drill-down, export, alerting and access-control needs
- non-functional needs (performance, refresh cadence, offline, localisation, audit)

Exclude: pure scheduling chatter, attendee lists, pleasantries, action items with no
system implication.

Be exhaustive. A meeting of 20k characters typically yields 40-120 requirements.
Split compound statements into separate atomic requirements — one testable
statement per row.

## Board / dashboard classification (mandatory on every row)

- `Direct`   — about a board, dashboard, screen, panel, widget, KPI, chart, report
               view, tile, drill-down, filter, or dashboard access/refresh.
- `Indirect` — a capability or data rule that a board or dashboard must surface or
               depend on (e.g. a status a board displays, a metric it aggregates).
- `Not`      — no board/dashboard bearing.

## Output

Write ONE JSON Lines file to the path given in your task. One JSON object per line,
no wrapping array, no markdown fences, UTF-8. Fields, all required, strings unless noted:

```
req_id            Your group prefix + 3-digit sequence, e.g. "G1-001"
source_file       filename of the .txt you took it from (without extension)
meeting_date      ISO date if the filename or text gives one, else ""
source_section    the heading / agenda item / table row it sits under, verbatim-ish
requirement       ONE atomic normative sentence, starting "The system shall " or
                  "The <surface> shall " — precise, testable, no hedging
evidence_quote    verbatim extract from the source, <= 300 chars, proving the row
category          one of: Board | Dashboard | Report | KPI/Metric | Chart/Visualisation |
                  Filter/Drill-down | Alert/Notification | Export | Access/Permission |
                  Data/Model | Workflow/Process | Integration | Configuration |
                  Non-functional | Open question
bd_scope          one of: Direct | Indirect | Not
surface           which app/user surface it belongs to, as the text names it
                  (e.g. "Venue POS", "Admin Web", "Guest App", "Back office", "" if unclear)
persona           the role that uses it, as named (e.g. "Supervisor", "Finance", "")
module            the business domain, as the text names it (e.g. "F&B", "Ticketing",
                  "Inventory", "Access Control", "Reporting/BI")
decision_status   one of: Agreed | Proposed | Client to confirm | Open question | Noted
confidence        one of: High | Medium | Low  (how firmly the text supports the row)
```

## Quality bar

- No invention. If the text does not say it, it does not go in the file.
- No duplicates within your own file. Near-duplicates across different meetings ARE
  allowed — record both, they are evidence of repetition.
- Keep `requirement` self-contained: a reader who cannot see the quote must still
  understand it. Expand pronouns and acronyms as the source defines them.
- Preserve the client's own vocabulary for nouns (screen names, module names).

## Final message back to your caller

Report: the number of rows written, the output path, the per-file row counts, the
Direct/Indirect/Not split, and any source file that was unreadable, empty or
noticeably truncated. Nothing else. Do not paste the rows.
