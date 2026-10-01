# Design notes per process

**What this folder is.** One authored YAML file per business process (`<process>.yaml`), written by
someone who read the screens together with their contracts, flows, meeting inputs, matrix rows and
trackers. The batch exporter (`tools/export-design-batch.py`) already writes each screen's fields,
data, states, navigation and permissions mechanically. These files add what a generator cannot: the
business rule behind a field, the format and order of what is shown, the edge cases worth drawing,
where two screens must match, realistic sample data, and where the package itself is wrong.

The exporter renders each file's `processSummary` and `vocabulary` at the top of a batch and each
`screens.<id>` entry inside that screen's block in `BUNDLE.md`.

**Authored, not generated.** Edit these files by hand. Nothing regenerates them. They are read-only
inputs to the exporter and change nothing else in the package.

## Files

| File | Process |
|---|---|
| `white-label.yaml` | White Label & CMS: branding, theming, the configurable guest surfaces |
| `<process>.yaml` | One per TSV in the process split (fnb-retail, ticketing-guest, ticketing-backoffice, customer-marketing, finance-insights, venue-operations, platform-foundation, ai) |

## Schema

```yaml
process: white-label            # the file name without .yaml
title: White Label & CMS
owner: <who, date>
coverage: >                     # optional: which screens are written in full, which in brief, which not at all
  ...
processSummary: >               # a folded string: how the process runs end to end, the apps, the rules
  ...
# or, where a process needs structure (white-label does), a mapping:
# processSummary:
#   text: >                     # the paragraph above
#   source: [ ... ]
#   elements:                   # white-label only: every tenant-configurable element
#     - element: Primary colour
#       configuredOn: [CMS-005]
#       field: Theme.primaryColour
#       values: '#RRGGBB'
#       default: none (required)
#       changeScope: runtime | buildTime | live
#       changes: [WEB-001, GST-001, ...]   # the guest screens it changes
#       source: [ ... ]
vocabulary:                     # words the UI must use consistently
  - term: Publish
    meaning: ...
    avoid: [Save, Go live]
    source: ...
screens:
  CMS-005:                      # any screen id in ticvai/screens/*.yaml
    block: A                    # optional: A, B or later
    summary: >                  # 2-5 sentences: what the screen must achieve and the one thing to get right
    inputs:     [{field, rule, source}]          # rules on what the user enters
    outputs:    [{element, rule, source}]        # what is shown and how
    actions:    [{action, result, source}]       # each button or gesture, its confirmation and results
    edgeCases:  [{case, expected, source}]       # offline, refusals, limits, races
    consistency: [{with, note}]                  # where this screen must match another
    sampleData: {...}                            # realistic values (AED, Arabic and English names)
    corrections: [{what, why, source}]           # where the package is wrong; the lead raises these as change requests
    openQuestions: [{question, default, source}] # what to draw until it is answered
inputToOutput:                  # white-label only: worked examples, configuration in, guest screen out
  - input: CMS-005 Primary colour #0E7C86
    output: ...
    screens: [WEB-005, GST-008]
    source: ...
```

## Rules for authors

- **Every rule, output, action, edge case and correction carries a `source`**: `contracts/<file>#<pointer or
  operationId>`, `F<n> step <k>`, `DI-<n>`, `MATRIX <ref>`, `TRACKER <sheet> row <n>`, `ADR-<n>`,
  `R<n>`, `REV3-<n>`, `REV3 <ref>` (`23SEP-<n>`, `DG-<n>`, `GAP-<x><n>`), `F<n> branch at step <k>`, a screen id,
  `MoM <date> <section>`, `Vision Book p<n>`, `screens/<file>#<screen id>`, a design-round document
  (`CLIENT-RESPONSE-30SEP <n>`, `AUDIT-29SEP (<heading or phrase in it>)`), or a named design source under
  `sources/designs/` (spaces in the file name are fine). `designer default` only where nothing else applies,
  and bare: what the default is goes in the rule, not in the source.
- **A contract source's parentheses name only what the contract has**: fields, enum values, parameters and
  response codes reachable from the operation or schema (`#addCartLine (recommendationId, 422)`), a field's
  constraint (`(ttlSeconds default 480, max 1800)`), or a "quoted phrase" from its text. Prose goes in the rule.
- **Do not restate the generator.** No plain field lists or state names; add the rule, the format, the
  edge case or the correction.
- **Corrections are not applied here.** The screens, contracts and flows stay as they are until the
  lead raises a change request. Draw what the note says; the corrections list says why it differs.
- Validate with `python tools/check-design-notes.py`: it parses every file, checks every screen id, and
  resolves every source against the register, contract, flow or file it names (0 errors to commit).
