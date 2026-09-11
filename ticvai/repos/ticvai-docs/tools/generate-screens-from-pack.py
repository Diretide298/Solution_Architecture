#!/usr/bin/env python3
"""Rebuild screen specifications from the workshop pack the screens were named after.

**The specification was parsed on 3 September and never reached the screens.**
`sources/workshop/pack.json` holds, for `ADM-145 Promotion Approval Inbox`, the eleven columns the
table needs — Promotion, Request type, Requested by, Requested date, Discount exposure, Revenue
impact estimate, Margin impact, Campaign budget, Risk level, Requested activation date, Current
approval level — and the five decisions a reviewer can take: Approve, Reject, Return for Change,
Request Information, Delegate. **The screen says *"Find a record"*.**

Across `P09 · Commercial` that is 9,826 parsed bullets, a median of 36 per screen, against three
declared components. **The regeneration is not a matter of inventing content.** It is a matter of
carrying content that already exists across a join nobody wrote.

## The pack has a grammar, and it is worth reading properly

`ADM-048` is typical, and the headings are doing real work:

    §Display                       Total Price Lists, Active Price Lists, ...   the metric row
    §Each price list should show   Price List ID, Name, Code, Type, ...         the table columns
    §Status                        Draft / Configured / Validated / Active      the lifecycle enum
    §Filter by                     Venue, Brand, Market, Country, ...           the filters
    §Quick Actions                 Create, Duplicate, Compare, Archive          the buttons
    §Separate permissions for      View Pricing, Create Price Lists, ...        component permissions

**`Display` and `Each price list should show` are different things** — one is a count across the
population, the other is a field of one row — and a classifier that reads both as "columns" puts
`totalPriceLists` in a table of price lists. So the two are separated, and a screen carrying both
is a command centre by that evidence rather than by having the words in its name.

**`Separate permissions for` is the answer to a question the package has been failing.** Four
components in 3,496 declare a permission, against a schema rule saying hiding is the default; the
packs have been naming them per screen the whole time.

## The join, and why it is exact rather than fuzzy

The contracts were drafted from the same pack, and every drafted property records the sentence it
came from:

    CommercialPricingCommandCenterView:
      properties:
        totalPriceLists: { type: integer, description: "Total Price Lists" }

So a pack bullet is matched to a contract property **by its own text**, normalised for case and
trailing punctuation. No similarity scoring, no threshold to tune, no silent near-miss.

**This is naming, not corroboration.** The screen and the contract descend from the same pack
sentence, so their agreeing proves nothing about whether the sentence is right. What it buys is
that the frontend and the contract use one name for one field, and `check-bindings.py` keeps them
that way. Claiming any more for it would repeat the mistake this rebuild exists to undo: **two
derived artefacts agreeing is not corroboration when they share a parent.**

## Where the pattern comes from

**Not the title.** The first generation read everything off the screen name, which is why 577
operations are named after their screens and 337 screens share three components. Here the pattern
is chosen from the pack's section grammar above, and every screen records `patternReason` naming
the sections that decided it. A screen whose pack supports no pattern falls to `listDetail` and
**says so in the reason** rather than passing as a considered choice.

## What is carried, and what is deliberately left behind

Carried: metrics, columns, filters, fields, actions, permissions, status enums, and the acceptance
condition. Left in the pack: acceptance prose beyond the first condition, worked examples, and the
AI narrative — **roughly two thirds of the bullets by count, and that is correct.** An example of a
price-list type belongs in the contract's enum documentation and a requirement belongs in the
matrix; copying them onto a screen is padding, and padding is what this rebuild is removing. The
counts are reported so the choice is visible rather than assumed.

## What is preserved untouched

Ids, names, modules, waves, `requiresModule`, `source`, `implementation`, `navigation`, hand-written
`coldEntry` paragraphs, `notes` and `openQuestions`. **The inventory is sound** — the workbook audit
confirmed the matrix side of it independently — and only the layout, binding and state layer is
rebuilt, because only that layer is filler.

Run: python tools/generate-screens-from-pack.py --platform P09 --module Commercial [--write]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

# Provenance prefixes this generator owns; anything else on an overlay is somebody's
# decision and is carried through a rebuild.
GAPS_MINE = ("pack ", "contract ")
OVERLAYS_MINE = ("pack ", "contract ", "authored \u2014 ")

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
CONTRACTS = ROOT / "contracts"
PACK = ROOT / "sources" / "workshop" / "pack.json"

STAMP = "9 September 2026"

# --------------------------------------------------------------------------------------------
# Reading the pack
# --------------------------------------------------------------------------------------------

# **Page furniture the PDF parser could not tell from a bullet.** `Pag e 15 | 158TICVAI • 15` sits
# in the middle of ADM-145's approval-type list, and `6 | Pag e` sits in the middle of ADM-048's
# examples, because the footer fell between two list items and the two packs number their pages in
# opposite orders. They are dropped and counted — **a generator that drops silently is one nobody
# can audit**, and one of these reached a table header in the last generation.
ARTEFACT = re.compile(r"Pag\s?e\b|TICVAI\s*[•�?]\s*\d+|^\s*\d+\s*\|")

# A label is a thing that fits in a column header or on a button. **Seven words is the ceiling**:
# `Requested activation date` is a column, `All decisions shall become part of the permanent audit
# trail` is a policy statement, and putting the second in a table header is how the last generation
# produced screens nobody could read.
LABEL_WORDS = 7

# Section headings are free text from the PDF — 1,384 distinct across 230 screens, 1,226 of them
# appearing exactly once — so they are classified by keyword family, **most specific first**.
# Anything unrecognised keeps its heading and its bullets as a named group: `Membership & Loyalty`,
# `Payment Orchestration` and `B2B / Reseller` are real detail sections, and discarding them
# because the heading is a domain noun would be the worst possible reading of "only write what you
# can cite".
FAMILIES: list[tuple[str, str]] = [
    ("permissions", r"permission|authori[sz]ed users|role[s]? can|access rights"),
    # `Each price list should show` — the row. Must beat `tiles` and it must beat `columns`.
    # `The system shall display` and `The screen shall show` are the 9 September books' way of
    # heading a directory, and they carried 18 KPIs on `Executive Command Center` alone.
    ("rowColumns", r"^the (system|screen|table|grid|list|dashboard) shall (display|show|list)$|"
                   r"^key functions$|"
                   r"each\b.*\b(show|display)|should show|should display|per (row|record|listing)|"
                   r"\bcolumns?\b|list shows|grid shows|listing shows|row shows|table shows"),
    # **A bare metric verb heads a directory of measures**, and the pack uses eight of them:
    # `Analyze`, `Measure`, `Track`, `Monitor`, `Compare`, `Identify`, `Detect`, `Forecast`. They
    # were unclaimed, so 600 bullets under them were read as nothing at all — the `filters` family
    # already took `analyse by`, which made the omission of the bare form easy to miss.
    ("tiles",      r"^(analy[sz]e|measure|track|monitor|compare|identify|detect|forecast)$|"
                   r"\bkpi|\bmetric|\bcard[s]?\b|counter|\btile[s]?\b|^display[s]?$|^show[s]?$|"
                   r"^dashboard|summary (bar|row|strip)|headline"),
    ("statusEnum", r"^status\b|^state[s]?\b|lifecycle|^stage[s]?\b"),
    ("filters",    r"\bfilter|search by|analy[sz]e by|group by|slice|sort by|drill|segment by"),
    # `Supports`, `Allows` and `Enables` head lists of *things supported* — `Event`, `B2B`,
    # `Venue`, `Auditor`, `Per Ticket` — and reading them as actions put 722 distinct "actions" on
    # 230 screens, most of them nouns. **The heading is not what disqualifies them; the verb test
    # is.** So the heading stays broad, `Create` under `Supports` is still a button, and `Auditor`
    # under it is not.
    ("actions",    r"^(quick |bulk |available |supported )?actions?\b|^buttons?\b|\bquick actions?\b|"
                   r"^allow[s]?\b|^support[s]?\b|^enable[s]?\b|users? can\b|operator can\b|"
                   r"can perform|^perform\b|^operations?\b"),
    ("fields",     r"configure|configuration|capture|set[ -]?up|\bdefine|\bfield[s]?\b|parameter|"
                   r"\bsetting[s]?\b|\boption[s]?\b|specify|^select\b"),
    ("accept",     r"acceptance"),
    ("purpose",    r"^purpose|objective|^goal"),
    ("ai",         r"^ai\b|\bai |intelligence|recommend|predict|forecast|\bmodel\b"),
    ("example",    r"^example|\bexamples\b|e\.g"),
    ("rules",      r"\brule[s]?\b|guardrail|\blimit[s]?\b|validation|constraint|policy|threshold"),
]


def family(heading: str) -> str:
    low = heading.lower().strip()
    for name, pattern in FAMILIES:
        if re.search(pattern, low):
            return name
    return "group"


def norm(text: str) -> str:
    """The join key. Case, whitespace and trailing punctuation only — no stemming, no fuzz."""
    return " ".join(str(text).lower().split()).strip(" .:;,")


def is_label(text: str) -> bool:
    words = text.split()
    if not 1 <= len(words) <= LABEL_WORDS:
        return False
    if text.rstrip().endswith((".", ";", ":")):
        return False
    # A bullet opening with a subordinating word is the tail of the sentence above it, split by the
    # parser at a line break. `and audit tracking for promotion creation` is not a button.
    return words[0].lower() not in {"and", "or", "the", "a", "an", "of", "for", "to", "with",
                                    "this", "that", "these", "all", "it", "which", "shall",
                                    "such", "including", "e.g", "i.e"}


def load_pack() -> dict:
    entries = json.loads(PACK.read_text(encoding="utf-8"))
    return {(e["source"], str(e["number"]), str(e["page"])): e for e in entries}


# --------------------------------------------------------------------------------------------
# Reading the contracts
# --------------------------------------------------------------------------------------------

def load_contracts() -> tuple[dict, dict]:
    ops, schemas = {}, {}
    for f in sorted(CONTRACTS.rglob("*.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — an unreadable contract is check-package's business
            continue
        if not isinstance(doc, dict):
            continue
        for name, body in ((doc.get("components") or {}).get("schemas") or {}).items():
            if isinstance(body, dict):
                schemas.setdefault(name, body)
        for path, item in (doc.get("paths") or {}).items():
            if not isinstance(item, dict):
                continue
            for method, op in item.items():
                if isinstance(op, dict) and "operationId" in op:
                    ops[op["operationId"]] = {"file": f.name, "path": path, "method": method,
                                              "op": op}
    return ops, schemas


REF = re.compile(r"#/components/schemas/(\w+)")


# **The pagination envelope is not the row.** A list response is
# `allOf: [Page, {properties: {items: {items: {$ref: Promotion}}}}]`, and taking the first `$ref`
# in the document returns `Page` — so `ADM-145` bound its queue of approval requests to a schema
# whose three properties are `items`, `nextCursor` and `hasMore`. Every list operation in the
# package is shaped this way, so the defect was uniform and invisible.
ENVELOPES = {"Page", "Cursor", "Paged", "PageMeta"}


def response_schemas(op: dict) -> list[str]:
    """The schemas a response carries, **innermost first** — the row before its wrapper."""
    responses = op.get("responses") or {}
    for code in ("200", "201", "default"):
        for body in ((responses.get(code) or {}).get("content") or {}).values():
            schema = body.get("schema") or {}
            # The element type of a paginated list, wherever the branch that declares it sits.
            for branch in ([schema] + (schema.get("allOf") or [])):
                if not isinstance(branch, dict):
                    continue
                items = ((branch.get("properties") or {}).get("items") or {}).get("items") or {}
                found = REF.findall(json.dumps(items))
                if found:
                    return found
            found = REF.findall(json.dumps(schema))
            # An envelope is only the answer when nothing else is.
            ranked = [f for f in found if f not in ENVELOPES] + [f for f in found if f in ENVELOPES]
            if ranked:
                return ranked
    return []


def property_index(names: list[str], schemas: dict) -> dict:
    """normalised description -> `Schema.property`, for the schemas a screen's operations return.

    Only the first hop. A description that repeats keeps the first binding — the pack occasionally
    lists a label under two headings, and binding two components to one field is right in that case.
    """
    index = {}
    for name in names:
        for prop, body in (schemas.get(name, {}).get("properties") or {}).items():
            if isinstance(body, dict) and (key := norm(body.get("description") or "")):
                index.setdefault(key, f"{name}.{prop}")
    return index


# --------------------------------------------------------------------------------------------
# Vocabulary
# --------------------------------------------------------------------------------------------

DECIDES = {"approve", "reject", "return for change", "request information", "delegate",
           "escalate", "decline", "endorse", "approve with conditions"}

# **Destructive is a property of the verb, not of the screen.** A screen offering Cancel needs a
# confirmation whatever it is called, and the last generation declared zero `confirmDialog`s across
# a platform whose packs name Suspend, Revoke and Rollback by hand.
DESTRUCTIVE = re.compile(
    r"^(reject|delete|remove|cancel|suspend|revoke|void|terminate|rollback|roll back|archive|"
    r"deactivate|expire|refuse|purge|close|withdraw|force|override|reset|discard|unpublish|"
    r"stop|halt|disable|end)\b", re.I)

PUBLISHES = re.compile(r"^(publish|deploy|promote|activate)[A-Z]")

# **The verbs a button may start with, read off the packs rather than invented.** Every bullet
# under a heading that is literally `Actions` or `Quick Actions`, across all 590 pack entries,
# contributes its first word — 71 of them, from `Create` and `Approve` down to `Republish` and
# `Freeze`. A lexicon I wrote myself would encode my vocabulary; this one encodes the client's.
def action_lexicon(entries: list[dict]) -> set[str]:
    strict = re.compile(r"^(quick |bulk |available |supported )?actions?$|^buttons?$", re.I)
    words = set()
    for e in entries:
        for heading, bullets in (e.get("sections") or {}).items():
            if not strict.match(heading.strip()):
                continue
            for b in bullets:
                for w in b.split()[:2]:
                    w = w.strip(":,").lower()
                    if w.isalpha() and len(w) >= 3:
                        words.add(w)
    # The parser contributes a little rubble — a page number, a stray `Depending`. Removing the
    # ones that are plainly not imperatives is a judgement, and it is a small and visible one.
    return (words - {"depending", "platform", "full", "new", "bulk", "temporarily", "the", "and",
                     "for", "all", "system", "auto", "user", "each"}) | {
        # Destructive and publishing verbs are added unconditionally: **a confirmation that is
        # missing because the pack happened not to use the word is the failure mode this whole
        # rebuild exists to stop**, and 0 screens declared a confirmDialog before it.
        "delete", "remove", "reject", "revoke", "deactivate", "rollback", "unpublish", "void",
        "terminate", "purge", "withdraw", "expire", "refuse", "override", "reset", "deploy",
        "promote", "decline", "close", "cancel", "suspend", "archive", "publish", "activate"}


# What a mutating operation offers the user, when the pack names no actions at all. **185 of the
# 230 Commercial screens declare nothing but a `list*` read**, so for most of them there is no
# verb to take from the contract either — which is a finding, not a gap in this table.
OPERATION_VERBS = {"set": "Save changes", "create": "Create", "publish": "Publish",
                   "approve": "Approve", "decide": "Decide", "simulate": "Run simulation",
                   "update": "Save changes", "delete": "Delete", "cancel": "Cancel",
                   "assign": "Assign", "merge": "Merge", "import": "Import", "export": "Export"}

# **A label that names a measure, not an attribute of a record.** Used only to decide whether a
# lone `Display` directory is a metric row or a table — see `sort_sections`.
MEASURE = re.compile(
    r"%|\bvs\b|\bper\b|"
    r"^(total|average|avg|median|current|peak|net|gross|number of|no\. of|count of)\b|"
    r"\b(rate|ratio|count|volume|utili[sz]ation|occupancy|throughput|score|index|"
    r"variance|margin|yield|uptime|breaches?|conversion)\b|"
    r"\b(today|yesterday|mtd|ytd|this hour|this week|this month|last week|last month)$|"
    r"^(revenue|sales|spend|attendance|footfall|visitors|transactions|tickets sold)\b|"
    r"^(active|pending|open|closed|completed|approved|rejected|escalated|expired|failed|"
    r"overdue|unassigned|available|booked|used|remaining|new|at risk|breached|within)\s+\S",
    re.I)

# A `tiles` heading that names the metric row itself, as against a bare `Display` or `Track`.
# **Named, not merely mentioned.** The first cut took any heading containing `KPI` or `cards`, and
# that promoted `For each KPI` (Target · Minimum · Maximum — a table's columns), `KPI Categories`
# and `KPI Components` (lists of kinds), and `Display dashboard cards/table containing` (a library
# of dashboards) into metric rows. Those are headings *about* KPIs; these are headings *of* them.
EXPLICIT_TILES = re.compile(
    # `Revenue Metrics`, `Performance KPIs`, `KPIs & Dashboards` name a row; `Card Information`
    # on the Game & Ride book is an RFID card, which is why `card` alone is no longer enough.
    r"\bkpi (cards?|tiles?|row|strip|bar)\b|\bkpis\b|\bmetrics\s*$|"
    r"\b(metric|summary|stat|statistic|headline)s? (cards?|tiles?)\b",
    re.I)

AUTHORING = re.compile(r"\b(builder|configurator|editor|designer|setup|manager|wizard|"
                       r"studio|composer|authoring|creation)\b", re.I)

TEMPLATES = {"commandCentre": "dashboard", "listDetail": "split", "approvalInbox": "split",
             "configEditor": "form"}


def subject(name: str) -> str:
    """The screen's own noun, for state sentences that differ from one another."""
    cleaned = re.sub(r"\b(command cent(er|re)|dashboard|manager|management|monitor|builder|"
                     r"configurator|studio|workspace|explorer|center|centre|configuration|setup|"
                     r"engine|inbox|directory|library|matrix|hub|assignment|control)\b",
                     "", name, flags=re.I)
    cleaned = re.sub(r"[&/,]", " ", cleaned)
    words = [w for w in cleaned.split() if len(w) > 2][:3]
    return " ".join(words).lower() or "record"


def leaf_label(path: str) -> str:
    """`CommercialPricingView.priceListId` -> `price list id`, for prose that reads."""
    tail = str(path).split(".")[-1]
    return re.sub(r"(?<!^)(?=[A-Z])", " ", tail).lower() if "." in str(path) else str(path).lower()


def cite(entry: dict, heading: str | None = None) -> str:
    return f"pack {entry['source']}, page {entry['page']}" + (f" §{heading}" if heading else "")


# --------------------------------------------------------------------------------------------
# Building one screen
# --------------------------------------------------------------------------------------------

PRESERVE = ["id", "name", "module", "requiresModule", "wave", "capability", "source",
            "implementation", "navigation", "notes", "openQuestions", "density", "densityReason",
            "resolvedQuestions", "audience", "offline", "machine",
            # **A note explaining a name or a purpose is not the name or the purpose.** Both were
            # dropped by this whitelist: `nameNote` records why BO-047 stopped being called F&B
            # Order Management, and `purposeNote` carries what a collapsed duplicate said before
            # it was removed — 528 screens hold one. Losing them leaves the decision unexplained
            # and the collapse indistinguishable from a deletion.
            "purposeNote", "nameNote"]


def sort_sections(entry: dict, report: Counter) -> tuple[dict, int, int]:
    """Pack sections into families, with the artefacts dropped and counted."""
    roles: dict[str, dict[str, list[str]]] = defaultdict(dict)
    dropped = kept_total = 0
    for heading, bullets in (entry.get("sections") or {}).items():
        kept = []
        for b in bullets:
            if ARTEFACT.search(b):
                dropped += 1
                continue
            kept.append(b)
        kept_total += len(kept)
        if kept:
            roles[family(heading)][heading] = kept
    report["artefacts dropped"] += dropped

    # **`Display` alone is usually the table, not a metric row** — the two only mean different
    # things when the pack draws the distinction itself by also giving a per-row section, and
    # reading every lone display directory as a dashboard put a metric row on 97 screens with no
    # metrics.
    #
    # **Unless the labels are measures.** `Revenue vs Target`, `Occupancy %`, `Within SLA — 92%`
    # and `Average Approval — 34 min` are not columns of anything; a table of them would have one
    # row. The 9 September BI book is why this now has an exception: its ten boards are dashboards
    # and every one of them writes its KPIs under `Display`, so the demotion turned 71 metric
    # directories into tables of one row each. Reading the labels rather than the heading also
    # corrects 16 screens of the original 590, among them `Cases Today | Open Cases | Unassigned
    # Cases` and `Within SLA | At Risk | Breached`.
    #
    # Half is the threshold because these blocks mix: a KPI list often ends with a sentence, and a
    # column list often opens with a count. `My Approval Inbox` scores 0.09 and stays a table,
    # which is right — its labels are `Request ID`, `Requested by`, `Venue`.
    #
    # **Unless the heading already says so.** `KPI Cards`, `Header KPIs`, `Performance KPIs` are
    # the pack naming a metric row, and the share test is a guess for when it has not. Found on 11
    # September on `BO-494 Rental Product Command Center`: `Active Products`, `Serialized Products`
    # and `Products Awaiting Approval` score 2 in 8 as measures and became the column headers of a
    # product table. 15 screens older than that day carried it and were rebuilt with `--only`.
    #
    # **The heading vouches for itself, not for its neighbours.** This first kept the whole block
    # as tiles when any one heading named KPIs, so `BO-454 Card Lifecycle Command Center` drew its
    # `Card Activity Table` as eight more tiles and no table. Now a named heading stays a tile, and
    # the headings beside it take the same measure test a block with no named heading would.
    if roles.get("tiles") and not roles.get("rowColumns"):
        named = {h: v for h, v in roles["tiles"].items() if EXPLICIT_TILES.search(h)}
        rest = {h: v for h, v in roles["tiles"].items() if h not in named}
        if named:
            report["display kept as metrics"] += 1
            if rest and measure_share(rest) < 0.5:
                roles["tiles"] = named
                roles["rowColumns"] = rest
                report["named KPIs kept, the rest read as columns"] += 1
        elif measure_share(roles["tiles"]) >= 0.5:
            report["display kept as metrics"] += 1
        else:
            roles["rowColumns"] = roles.pop("tiles")
            report["display read as columns"] += 1
    return roles, dropped, kept_total


def measure_share(block: dict[str, list[str]]) -> float:
    """How much of a display directory reads as a measure rather than a record attribute."""
    labels = [b for v in block.values() for b in v if len(b.split()) <= 9]
    if not labels:
        return 0.0
    return sum(1 for b in labels if MEASURE.search(b)) / len(labels)


def choose_pattern(roles: dict, actions: list[str], ops: list[str],
                   has_tiles: bool, has_rows: bool, has_fields: bool) -> tuple[str, str]:
    """The pattern, and the evidence in the pack that chose it. **The name is never consulted.**

    `has_tiles` / `has_rows` / `has_fields` say whether those sections yielded any *labels*. A
    heading alone is not evidence: `ADM-150`'s `Configure whether` heads six sentences of prose,
    and choosing `configEditor` from it produced a form with no fields in it.
    """
    lowered = {a.lower() for a in actions}
    if {"approve", "reject"} <= lowered:
        return "approvalInbox", ("the pack lists Approve and Reject among this screen's own "
                                 "actions — every row is waiting for a decision, so the empty "
                                 "state is success rather than a prompt to create something")
    if has_tiles and has_rows and roles.get("tiles") and roles.get("rowColumns"):
        return "commandCentre", (f"the pack gives this screen both a metric directory "
                                 f"(§{'; '.join(roles['tiles'])}) and a per-row directory "
                                 f"(§{'; '.join(roles['rowColumns'])}) — counts over a population, "
                                 f"then the population")
    # **A metric directory and no population is still a dashboard.** Before the `Display` labels
    # were read, this case could not arise: a lone display directory was demoted to columns and
    # every screen had a population. The BI book's boards are the opposite shape — `Revenue Pulse`
    # names twelve measures and no record — and without this branch they fell to `listDetail`,
    # whose builder emits nothing for tiles, so the screens came out empty.
    #
    # `commandCentre` is the only pattern with a `headline` slot. Its `moduleTiles` slot is the
    # one composed from a tenant's licence, and these screens do not fill it: **their tiles are
    # named by the pack, and `patternReason` says so** — so the runtime-composition claim in the
    # design brief still refers to the screens it always did.
    if has_tiles and not has_rows and not has_fields:
        return "commandCentre", (f"the pack gives this screen a metric directory "
                                 f"(§{'; '.join(list(roles['tiles'])[:3])}) and no per-row "
                                 f"directory — measures over a population the screen does not "
                                 f"itself list. The tiles are the pack's, not a tenant licence's")
    if has_fields and not has_rows:
        return "configEditor", (f"the pack gives this screen a configuration directory "
                                f"(§{'; '.join(list(roles['fields'])[:3])}) and no display "
                                f"directory — it is settings, not a population")
    if any(o and PUBLISHES.match(o) for o in ops) and has_fields:
        return "configEditor", ("the screen declares a publishing operation over fields the pack "
                                "configures")
    if has_rows:
        return "listDetail", (f"the pack gives this screen a display directory "
                              f"(§{'; '.join(list(roles['rowColumns'])[:3])}) and no metric row")
    return "listDetail", ("**nothing in the pack chooses a pattern for this screen** — no metric "
                          "directory, no display directory, no configuration directory. It falls "
                          "to the default, and the fallback is recorded rather than passed off as "
                          "a decision")


def labels_of(roles: dict, role: str) -> list[tuple[str, str]]:
    out, seen = [], set()
    for heading, bullets in roles.get(role, {}).items():
        for b in bullets:
            if is_label(b) and norm(b) not in seen:
                seen.add(norm(b))
                out.append((b, heading))
    return out


def build(screen: dict, entry: dict, ops: dict, schemas: dict, report: Counter,
          verbs: set[str]) -> dict:
    sid = screen["id"]
    op_ids = [a.get("operationId") for a in (screen.get("apis") or []) if a.get("operationId")]
    roles, dropped, kept_total = sort_sections(entry, report)

    returned: list[str] = []
    for oid in op_ids:
        if oid in ops:
            returned += response_schemas(ops[oid]["op"])
    props = property_index(returned, schemas)
    # **The schema the collection is a collection of.** `columns` names the fields; `bindsTo` names
    # the shape, and `check-bindings.py` reads the second — a screen carrying twenty verified
    # column paths and no `bindsTo` counts as unbound, which is how P09 read as 7.8% bound after
    # its columns were written.
    row_schema = returned[0] if returned else None
    # (reassigned below once `collection_op` is known — the table binds to the shape returned by
    #  the call that fills it, not by whichever operation the screen happens to declare first.)

    counts = Counter()

    def bind(text: str) -> tuple[str, bool]:
        hit = props.get(norm(text))
        counts["bound" if hit else "unbound"] += 1
        return (hit or text), bool(hit)

    tiles_raw = labels_of(roles, "tiles")
    rows_raw = labels_of(roles, "rowColumns")
    filters_raw = labels_of(roles, "filters")
    fields_raw = labels_of(roles, "fields")
    perms_raw = [p for p, _ in labels_of(roles, "permissions")]
    status_raw = [s for s, _ in labels_of(roles, "statusEnum")]
    # **An action starts with a verb.** Without this the pack's `Supports: Event, Venue, B2B`
    # became three buttons. Either of the first two words may carry it, because the packs write
    # `Temporarily suspend` and `Bulk import`.
    actions_raw = [(b, h) for b, h in labels_of(roles, "actions")
                   if {w.strip(":,").lower() for w in b.split()[:2]} & verbs]

    # **The pattern is chosen on the labels, not on the headings.** `ADM-057` has a section headed
    # `Board 2 defines` whose six bullets are all prose, and reading the heading alone made it a
    # configuration editor with an empty form. A metric directory containing no metric is not a
    # metric directory.
    pattern, reason = choose_pattern(roles, [a for a, _ in actions_raw], op_ids,
                                     bool(tiles_raw), bool(rows_raw), bool(fields_raw))
    # Where the pack names no actions, the screen's own mutating operation does. Cited to the
    # contract, never to the pack, so a reader can tell the two apart.
    from_contract: list[tuple[str, str]] = []
    for oid in op_ids:
        stem = re.match(r"^([a-z]+)", oid)
        label = OPERATION_VERBS.get(stem.group(1) if stem else "")
        if label and not actions_raw:
            from_contract.append((label, f"contract operation {oid}"))

    noun = subject(screen["name"])

    row_columns = [bind(b)[0] for b, _ in rows_raw]
    row_heading = rows_raw[0][1] if rows_raw else None

    # **Which of the screen's calls fills the table.** `op_ids[0]` is declaration order, and on
    # ADM-145 that is `listPromotions` against a queue of approval requests. A read is preferred
    # over a write, and a queue prefers the call that names what is queued.
    reads = [o for o in op_ids if o.startswith(("list", "get", "search"))]
    collection_op = next(
        (o for o in reads if pattern == "approvalInbox"
         and re.search(r"approval|request|queue|pending", o, re.I)),
        (reads or op_ids or [None])[0])
    # **The table's shape is its own operation's response.** `ADM-145` declares `listPromotions`
    # first and lists approval requests, so taking `returned[0]` bound a queue of requests to
    # `Promotion`. Same defect as the pagination envelope, one level along.
    if collection_op and collection_op in ops:
        own = response_schemas(ops[collection_op]["op"])
        if own:
            row_schema = own[0]

    # --- regions ------------------------------------------------------------------------------
    regions: list[dict] = []

    if filters_raw:
        filter_fields = [bind(b)[0] for b, _ in filters_raw]
        regions.append({"name": "contentBody", "slot": "filters", "components": [
            {"kind": "searchField", "label": f"Search {noun}",
             "provenance": cite(entry, filters_raw[0][1])},
            {"kind": "multiSelect", "label": "Filter by", "columns": filter_fields,
             # **Naming the count is not naming the filters.** This note appeared verbatim on 19
             # screens in the first package-wide run, which is the boilerplate detector's whole
             # point — so it now says what the filters are.
             "notes": ("The pack filters this screen by "
                       + ", ".join(leaf_label(f) for f in filter_fields[:6])
                       + (f" and {len(filter_fields) - 6} more" if len(filter_fields) > 6 else "")
                       + " — which are present is a decision the pack already made."),
             "provenance": cite(entry, filters_raw[0][1])}]})

    if pattern == "commandCentre":
        regions.append({"name": "contentBody", "slot": "headline", "components": [
            dict({"kind": "metricTile", "label": b, "provenance": cite(entry, h)},
                 **({"bindsTo": bind(b)[0]} if norm(b) in props else {}))
            for b, h in tiles_raw]})
        if row_columns:
            regions.append({"name": "contentBody", "slot": "moduleTiles", "components": [{
                "kind": "dataTable", "label": f"Every {noun}", "columns": list(row_columns),
                "bindsTo": row_schema, "operation": collection_op,
                "provenance": cite(entry, row_heading)}]})
    elif pattern == "configEditor":
        source_labels = fields_raw or rows_raw
        regions.append({"name": "contentBody", "slot": "fields", "components": [
            {"kind": "selectField" if len(b.split()) <= 3 else "textField", "label": b,
             "provenance": cite(entry, h)} for b, h in source_labels[:30]]})
        if len(source_labels) > 30:
            report["fields truncated"] += 1
    elif row_columns:
        # **Only when there is something to put in it.** Appending the table unconditionally gave
        # 72 screens a `dataTable` and a `detailPanel` with no columns in either — an empty box,
        # which is precisely what the plan says the generator must refuse to draw. Those screens
        # now carry no content region and a gap that says why.
        slot = "queue" if pattern == "approvalInbox" else "collection"
        regions.append({"name": "contentBody", "slot": slot, "components": [{
            "kind": "dataTable",
            "label": ("Waiting for a decision" if pattern == "approvalInbox" else f"Every {noun}"),
            "columns": list(row_columns),
            "bindsTo": row_schema,
            "operation": collection_op,
            "provenance": cite(entry, row_heading)}]})

    if pattern != "configEditor" and row_columns:
        detail_groups = list(roles.get("group", {}))[:6]
        regions.append({"name": "contextPanel",
                        "slot": "item" if pattern == "approvalInbox" else "selection",
                        "components": [{
                            "kind": "detailPanel",
                            "label": f"The selected {noun}",
                            "bindsTo": row_schema,
                            "columns": list(row_columns),
                            "notes": ("The pack groups this record's detail under its own "
                                      "headings: "
                                      + ", ".join(f"“{g}”" for g in detail_groups)
                                      + ".") if detail_groups else None,
                            "provenance": cite(entry, row_heading)}]})

    # **A region with no components is a claim with nothing behind it**, and the checker
    # says so. Where a pattern's slot yields nothing the region is dropped and the screen
    # records the gap below rather than drawing an empty box.
    regions = [r for r in regions if r.get("components")]

    # --- actions, permissions and the overlays they raise --------------------------------------
    overlays, action_components = [], []
    matched_perms = set()
    for label, heading in (actions_raw[:8] + from_contract):
        destructive = bool(DESTRUCTIVE.match(label))
        kind = ("destructiveButton" if destructive
                else "primaryButton" if not action_components else "secondaryButton")
        where = heading if heading.startswith("contract ") else cite(entry, heading)
        component = {"kind": kind, "label": label, "provenance": where}
        # **The pack names the permissions and the package has never used them.** Matched on the
        # action's own verb-object, so `Create Price List` takes `Create Price Lists` and nothing
        # takes a permission it does not resemble — a wrong permission is worse than none.
        for perm in perms_raw:
            if norm(perm).rstrip("s") in norm(label).rstrip("s") or \
               norm(label).rstrip("s") in norm(perm).rstrip("s"):
                component["permission"] = perm
                matched_perms.add(perm)
                counts["permissions"] += 1
                break
        action_components.append(component)
        if destructive:
            overlays.append({
                "id": "confirm" + re.sub(r"[^A-Za-z]", "", label.title())[:24],
                "component": "confirmDialog",
                "trigger": label,
                "body": (f"**{label} on a {noun} is not reversible from this screen.** Names what "
                         f"it affects and what it leaves alone. The pack requires the decision to "
                         f"reach the audit trail, so the dialog states that it is recorded."),
                "provenance": where})
    # **A permission the pack names and no button claimed is still the pack's statement.** Dropping
    # it would lose the only place in the package where component permissions are written down.
    if (spare := [p for p in perms_raw if p not in matched_perms]):
        action_components.append({
            "kind": "banner", "label": "Permissions this screen separates",
            "notes": ("**The pack separates these permissions and no action on the screen claims "
                      "them yet:** " + ", ".join(spare) + ". Each needs attaching to the control "
                      "it gates, or the screen needs the control."),
            "provenance": cite(entry, next(iter(roles.get("permissions", {})), None))})
    if any(PUBLISHES.match(o) for o in op_ids):
        action_components.append({
            "kind": "publishGate", "label": "What publishing changes",
            "notes": "**Names what goes live, where, and from when.** A publish with no stated "
                     "consequence is one somebody presses meaning to save.",
            "provenance": f"authored — required by check-screens for {op_ids[0]}"})
    if action_components:
        regions.append({"name": "actionBar",
                        "slot": {"approvalInbox": "decision", "configEditor": "publish"}
                                .get(pattern, "rowActions"),
                        "components": action_components})

    # --- gaps -----------------------------------------------------------------------------------
    gaps = []
    unserved = [a for a, _ in actions_raw
                if not any(norm(a).split()[0] in norm(o) for o in op_ids)]
    # **Not suppressed on multi-operation screens.** The old test was `len(op_ids) <= 1`, so
    # ADM-145 — offering Return for Change, Request Information and Delegate against one
    # `decideApprovalRequest` — recorded nothing. Three real actions with nothing behind them.
    if unserved:
        gaps.append({
            "operation": None,
            "why": (f"**The pack names {len(actions_raw)} actions on this screen and the screen "
                    f"declares {len(op_ids)} operation"
                    f"{'s' if len(op_ids) != 1 else ''}.** Unserved: {', '.join(unserved[:8])}"
                    f"{' …' if len(unserved) > 8 else ''}. Each needs an operation, or needs "
                    f"removing from the screen; this is the Phase 3 reconciliation seen from the "
                    f"screen side rather than the contract side."),
            "source": cite(entry, actions_raw[0][1])})
    if row_columns and not props:
        gaps.append({
            "operation": collection_op,
            "why": ("**This screen's operations return no schema with described properties**, so "
                    "not one of its columns can be bound. The columns are the pack's own labels "
                    "and are carried as text until the response shape exists."),
            "source": cite(entry, row_heading)})
    # **A builder that cannot build.** The screen's own name promises authoring and its only
    # declared operation reads. 185 of the 230 Commercial screens declare nothing but a `list*`,
    # and the ones whose names promise otherwise are the clearest statement of the gap.
    if AUTHORING.search(screen["name"]) and all(o.startswith(("list", "get")) for o in op_ids):
        gaps.append({
            "operation": None,
            "why": (f"**{screen['name']} declares no operation that writes anything** — its only "
                    f"declared call is `{op_ids[0] if op_ids else 'none'}`, a read. The name "
                    f"promises authoring and the contract offers none, so either the write "
                    f"operations are missing or this screen is a view of something another screen "
                    f"builds."),
            "source": f"contract — the screen's declared operations"})
        report["authoring with no write"] += 1
    if not any(r["name"] == "contentBody" for r in regions):
        gaps.append({
            "operation": None,
            "why": ("**The pack gives this screen nothing that can be drawn.** Its sections are "
                    "prose — purpose, acceptance conditions, worked examples — with no directory "
                    "of metrics, columns or fields anywhere in them. The screen has no content "
                    "region rather than an empty one, and it needs a person before it is built."),
            "source": cite(entry)})
        report["no drawable content"] += 1
    if pattern == "listDetail" and reason.startswith("**nothing"):
        gaps.append({
            "operation": None,
            "why": ("**The pack gives this screen no display, metric or configuration directory**, "
                    "so its shape is a default rather than a reading. It needs a person before it "
                    "is built."),
            "source": cite(entry)})

    # --- states -----------------------------------------------------------------------------------
    states = {
        "loading": (f"The {noun} configuration as saved." if pattern == "configEditor"
                    else f"The {noun} list; the counts above it resolve separately."
                    if pattern == "commandCentre" else f"The {noun} list."),
        "error": (f"Could not load. Names which read failed and leaves the {noun} untouched."),
    }
    if pattern == "approvalInbox":
        states["emptyFirstRun"] = ("**Nothing is waiting, which is the good outcome.** An empty "
                                   "queue means every request has been decided — this state "
                                   "offers no create action, because creating work is not what "
                                   "an empty inbox needs.")
    elif pattern == "configEditor":
        states["emptyFirstRun"] = (f"No {noun} configured yet. Carries the create action and says "
                                   f"what the platform does in the meantime.")
    else:
        states["emptyFirstRun"] = (f"No {noun} yet. Carries the create action; distinct from a "
                                   f"filter that matched nothing.")
    # **A configuration editor with a filter is still filtering.** ADM-275 and ADM-296 are
    # `configEditor` screens whose packs give them a filter directory, and a screen that can
    # narrow its content has to say what narrowed-to-nothing looks like.
    if pattern != "configEditor" or filters_raw:
        states["emptyNoResults"] = (
            (f"The filter narrowed it and the {noun} are still there. The pack's own statuses are "
             f"{', '.join(status_raw[:1])} — the state names which is selected."
             if status_raw else
             f"The filter narrowed it and the {noun} are still there. Names the active filter and "
             f"offers to clear it."))
    states["emptyNoAccess"] = ("Names the missing permission. **Never an empty table** — that "
                               "reads as *there is no data* and sends somebody to support with "
                               "the wrong question.")

    # **A state this generator does not write is not a state it may delete.** It owns six names
    # — loading, error, the three empties, offline — and owning six names does not make it the
    # owner of the block. `denied` is written by the permission work, and the failure states that
    # `navigation.transitions[].onFailure` anchors point at are written by hand; assigning this
    # dict wholesale deleted all of them. Same rule as overlays and gaps, for the same reason.
    for k, v in (screen.get("states") or {}).items():
        if k not in states and v:
            states[k] = v

    # --- assemble ------------------------------------------------------------------------------
    out = {k: screen[k] for k in PRESERVE if k in screen}
    out["pattern"] = pattern
    out["patternReason"] = reason
    purpose = " ".join(" ".join(roles.get("purpose", {}).get(h, [])) for h in
                       roles.get("purpose", {})) or entry.get("purpose") or screen.get("purpose")
    out["purpose"] = " ".join(str(purpose).split())
    if entry.get("acceptance"):
        out["purposeNote"] = " ".join(str(entry["acceptance"]).split())
    # **A gap this generator did not raise is carried, as overlays and components are.** Both
    # generators rebuild `gaps` from what they can see in a pack page or a contract, and assigning
    # that list wholesale deleted every question any other source had recorded on the screen —
    # including the ones the schema calls "a real question" and the brief says never to draw over.
    # `POS-003` and `POS-004` lost theirs on the first rebuild after they were written, which is
    # how this was found.
    kept_gaps = [g for g in (screen.get("gaps") or [])
                 if not str(g.get("source", "")).startswith(GAPS_MINE)
                 and str(g.get("source", "")) != "the screen's own declarations"]
    if gaps or kept_gaps:
        out["gaps"] = gaps + kept_gaps
    out["layout"] = {"template": TEMPLATES[pattern], "regions": regions}
    # **An overlay this generator did not write is carried, exactly as a component is.** Both
    # generators build `overlays` fresh from the destructive actions they find, and assigning that
    # list wholesale deleted every popup any other source had put on the screen. It went unnoticed
    # because until the 3 August UI/UX decisions were applied, nothing else had ever written one —
    # so the first drawer added to the POS would have survived until the next rebuild and then
    # vanished, with no check able to say what had been lost.
    # **A rebuilt overlay keeps what another source said about closing it.** This generator owns
    # the dialog's existence, its trigger and its body. It does not own `confirm` and `dismiss`,
    # which say where accepting and dismissing land and what each carries or throws away — those
    # come from §2.3 and from the minutes. Rebuilding the dict wholesale dropped them from 13 of
    # P04's 16 overlays the first time it ran after they were written, and the three that survived
    # did so only because their provenance kept them out of this generator's hands entirely.
    _prior = {o.get("id"): o for o in (screen.get("overlays") or [])}
    for _o in overlays:
        _was = _prior.get(_o.get("id")) or {}
        for _half in ("confirm", "dismiss"):
            if _was.get(_half) and _half not in _o:
                _o[_half] = _was[_half]

    kept_overlays = [o for o in (screen.get("overlays") or [])
                     if not str(o.get("provenance", "")).startswith(OVERLAYS_MINE)
                     and o.get("id") not in {x.get("id") for x in overlays}]
    if overlays or kept_overlays:
        out["overlays"] = overlays + kept_overlays
    out["states"] = states
    # **A mutation invalidates the query it changes.** `decideApprovalRequest` recorded
    # `invalidates: [listPromotions]` because `op_ids[0]` is declaration order; the queue it
    # actually changes is `listApprovalRequests`, which `collection_op` already names.
    out["apis"] = [dict(a, **({"invalidates": [collection_op]}
                              if a.get("trigger") == "onAction" and collection_op else {}))
                   for a in (screen.get("apis") or [])]
    entry_state = dict(screen.get("entryState") or {})
    if pattern in ("listDetail", "approvalInbox") and row_columns:
        # **The row is already on screen when the panel opens.** No screen in the package declared
        # this, which is the difference between a detail panel that flashes a skeleton and one that
        # shows what was just clicked.
        entry_state["preloaded"] = list(row_columns[:6])
    if entry_state:
        out["entryState"] = entry_state
    if screen.get("wireframe"):
        out["wireframe"] = screen["wireframe"]
    carried = (len(tiles_raw) + len(rows_raw) + len(filters_raw) + len(fields_raw)
               + len(actions_raw) + len(perms_raw) + len(status_raw))
    out["apisNote"] = (
        f"Regenerated {STAMP} from {entry['source']} page {entry['page']}. "
        f"{counts['bound']} of {counts['bound'] + counts['unbound']} labels bound to a contract "
        f"property; {carried} of {kept_total} pack bullets carried onto the screen — the rest are "
        f"acceptance prose, worked examples and AI narrative, which belong to the matrix and the "
        f"contracts rather than here.")

    report["bound"] += counts["bound"]
    report["unbound"] += counts["unbound"]
    report["permissions"] += counts["permissions"]
    report["overlays"] += len(overlays)
    report["gaps"] += len(gaps)
    report["carried"] += carried
    report["available"] += kept_total
    report[f"pattern:{pattern}"] += 1
    return out


# --------------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--platform", required=True)
    ap.add_argument("--module")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sample", default="")
    # **A module is the wrong unit for a repair.** P09 Commercial is 230 screens; fixing the 13 a
    # rule change reaches should not rebuild the 217 it does not. Added 11 September for the KPI-card
    # screens, whose layouts predate the rule.
    ap.add_argument("--only", default="", help="comma-separated screen ids; rebuild these and no others")
    args = ap.parse_args()
    only = {i.strip() for i in args.only.split(",") if i.strip()}

    path = next(SCREENS.glob(f"{args.platform}-*.yaml"))
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    pack = load_pack()
    ops, schemas = load_contracts()

    verbs = action_lexicon(json.loads(PACK.read_text(encoding="utf-8")))
    report, rebuilt, missing = Counter(), 0, 0
    for i, screen in enumerate(doc["screens"]):
        # **Reach is decided by the pack, not by the module name.** With no `--module` every screen
        # whose `source` resolves to a pack entry is rebuilt and the rest are left exactly as they
        # are — 501 of the package's 1,091 screens have no pack behind them and this tool has
        # nothing to say about them.
        if args.module and screen.get("module") != args.module:
            continue
        if only and screen["id"] not in only:
            continue
        src = screen.get("source") or {}
        key = (src.get("pack"), str(src.get("number")), str(src.get("page")))
        if key not in pack:
            missing += 1
            continue
        doc["screens"][i] = build(screen, pack[key], ops, schemas, report, verbs)
        rebuilt += 1

    if only - {s["id"] for s in doc["screens"]}:
        print("not on this platform:", ", ".join(sorted(only - {s["id"] for s in doc["screens"]})))
        return 1
    print(f"{rebuilt} screens rebuilt from the pack, {missing} with no pack entry\n")
    for k in sorted(report):
        print(f"  {k:<26} {report[k]}")
    total = report["bound"] + report["unbound"]
    if total:
        print(f"\n  {report['bound']} of {total} labels bound ({report['bound'] / total * 100:.0f}%)")

    if args.sample:
        wanted = set(args.sample.split(","))
        for screen in doc["screens"]:
            if screen["id"] in wanted:
                print("\n" + "=" * 92)
                print(yaml.safe_dump(screen, sort_keys=False, allow_unicode=True, width=100))

    if args.write:
        tmp = path.with_suffix(".yaml.tmp")
        tmp.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                       encoding="utf-8")
        os.replace(tmp, path)
        print(f"\nwritten: {path.name}")
    else:
        print("\n(dry run — pass --write)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
