# Blind extraction — addendum for rendered board screens (vision)

Read `EXTRACTION-SPEC.md` in the same directory first. Everything in it applies.
This addendum changes only what a "source" is and how finely you extract.

## Your sources are PNG renderings of board/dashboard design pages

Each PNG is one **board**: a dark left navigation rail, and a grid of numbered
**frames** (1, 2, 3 ...) each with a title, a subtitle, and a dense UI design —
tiles, tables, charts, forms, toggles, buttons, status chips, tabs.

Read each image with the Read tool. Look closely: the value is in the small text.

## Extract at frame granularity, then at element granularity

For every frame on every page, record rows for:

- the frame itself — what board it belongs to, what it is for
- every **navigation item** in the left rail (each is a screen the product must have)
- every **KPI tile / stat** (name it, and note its unit, delta or comparison)
- every **table** — name it and list its visible columns in the requirement text
- every **chart or visual** — say what type it is and what it plots
- every **filter, selector, date range, tab and toggle**
- every **action button** (each is an operation the system must support)
- every **status value / chip** you can read (these are state machines)
- every **form field** where the frame is a configuration screen
- every **validation, warning or health message** shown
- every **role / persona** named anywhere on the page

One atomic requirement per row. A dense page legitimately yields 40-100 rows.
Do not summarise a table as "a table exists" — the columns ARE the requirement.

## Field notes specific to this addendum

- `source_file`   — the PNG basename without extension, e.g. "FB-p02"
- `source_section`— "<png> — frame <n>: <frame title>" or "<png> — left nav"
- `evidence_quote`— the literal on-screen text you are reading (labels, column
                    headers, button text). Quote what is written, not your reading of it.
- `meeting_date`  — leave "" (these are design packs, not minutes)
- `decision_status` — use "Noted" for anything simply shown in the design
- `confidence`    — "Low" whenever the text is too small to read with certainty;
                    never guess a label you cannot actually read. If a region is
                    illegible, say so in your final report rather than inventing.
- `bd_scope`      — almost everything here is "Direct"; use "Indirect" for
                    underlying data/config rules the board merely implies.

## Second output: a board inventory

Alongside your JSONL, write a plain-text inventory listing, for each page:
the board name (from the left rail's highlighted item or the page header), and
each frame number with its exact title. This is the structural map of the pack.
