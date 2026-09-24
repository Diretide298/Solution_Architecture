#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Values the platform applies, with nothing that says what they should be.

**`fnb.sub_bill.service_charge` is a stored `numeric(18,4)` and no row anywhere holds the rate.**
`F29` says tax and service charge recompute per bill on a split, so a number is being calculated;
nothing in 632 tables, no operation and no screen says from what. It was found by reading, not by
a checker, and **every one of the thirty checks in `run-checks` passes on it**:

    audit-unwired-tables        `fnb.sub_bill` is reached, so the table never enters the report
    check-config-scope          validates the scope of configuration operations that exist. There
                                is no operation, so there is nothing to validate
    audit-screenless-operations walks operations. Again - no operation
    check-spec-coverage         lexical, against capability names. "Service charge" is not a
                                capability row; it is a field inside one
    check-rfp-coverage          same shape, same blind spot

**The gap is a class, not an instance.** Every existing check walks a structure and asks whether
its edges are present: a table to an operation, an operation to a screen, a screen to a pack
citation. A value with no configuration source has no missing edge - it has a missing *node*, one
nobody drew, and walking edges will never find a node that was never there.

## The question it asks

For every column carrying a value somebody ought to have set, it asks: **is there anywhere a
person sets it?** Four classes, because the defect is the same shape in each and a checker that
only read money would have missed a break length and a cold-chain threshold:

    charge      fee, charge, surcharge, commission, gratuity, tip, levy
    threshold   limit, quota, threshold, ceiling, allowance, tolerance
    rate        rate, multiplier, ratio
    duration    minutes, hours, days, seconds, timeout, ttl, window, interval

**A value on a definition is already configured; a value on a transaction is not.**
`catalogue.space.setup_minutes` is what an administrator maintains about a space - it *is* the
control. `rental.settlement.late_fee` is what one return cost, and the rate behind it has to live
somewhere else. So the table is classified first, by whether its rows record something that
happened, and only transactional rows are asked the question.

**Measurements are excluded outright.** `elapsed_minutes`, `downtime_minutes` and `variance` are
observations. Nobody configures what a stopwatch read.

## The four states

    CONTROLLED      `rental.settlement.late_fee` <- `rental.fee_policy.late_fee_amount`,
                    `late_fee_basis`, `grace_period_minutes`. This is the shape when it is right
    CROSS-SCHEMA    a control with the same stem exists, in another schema. `orders.payment.fx_rate`
                    against `ledger.fx_rate.rate`. **Usually correct and worth seeing** - a rate
                    owned by one module and applied in another is normal, and a rate that only
                    looks owned is not
    ANSWERED        ruled not-a-defect in `handoff/values-without-configuration.md`
    CONFIRMED GAP   ruled `genuinelyMissing` or `fixedByLaw`. **Triaged, still open**
    UNCONTROLLED    stored, applied, and nothing names it - not yet looked at

**Six verdicts, and only a person can say which applies. Four of them close a row; two do not.**

**A verdict is not the same as a dismissal.** `genuinelyMissing` and `fixedByLaw` are findings -
recording one triages the row, it does not answer it, and the report keeps showing it as a
CONFIRMED GAP until somebody builds the control. Silencing those would turn this ledger into the
place gaps go to be forgotten, which is the failure it exists to prevent.

    setByAProvider      `orders.chargeback.fee_amount` is what the bank took. Nobody configures
                        it and a control would be a fiction
    enteredPerIncident  a damage fee assessed against an actual dent. The control is an approval
                        limit, not a rate
    derivedFromAnother  `rental.settlement.chargeable_late_minutes` falls out of the grace period
                        and the return time. It has a control; the control is upstream
    observedNotSet      how long a kitchen exception lasted. A reading the name did not mark as
                        one - the `MEASUREMENT` list catches `elapsed_minutes` and cannot catch
                        `duration_minutes`, which is the same thing wearing a neutral word
    fixedByLaw          a statutory rest break or a retention period. Still needs a row, because
                        the law differs by jurisdiction and the platform is multi-region
    genuinelyMissing    `fnb.sub_bill.service_charge`

That is a judgement, which is why this **reports and does not gate** - the same argument
`run-checks` already records for `audit-unwired-tables`. The answers go in the ledger and are read
back, so a question answered once stops being asked. That document is the point of the tool; the
tool exists to keep it honest.

    python3 tools/audit-uncontrolled-values.py
    python3 tools/audit-uncontrolled-values.py --class charge
    python3 tools/audit-uncontrolled-values.py --csv handoff/uncontrolled-values.csv
"""
import collections
import csv
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(ROOT, "handoff")
REF = os.path.join(H, "schema-reference.json")
LEDGER = os.path.join(H, "values-without-configuration.md")

# **A row that records something that happened.** Everything else is a definition an administrator
# maintains, and a value sitting on a definition is its own configuration. This list is the one
# judgement the tool makes by itself, so it is deliberately the narrower of the two - a table
# wrongly called a definition goes quiet, which is the failure this whole tool exists to catch,
# and a table wrongly called a transaction only costs a line in the report.
TRANSACTION_NAME = re.compile(
    r"(^|_)(order|bill|settlement|payment|refund|chargeback|listing|booking|reservation|entry|"
    r"transaction|movement|scan|visit|session|invoice|obligation|balance|exception|assignment|"
    r"redemption|claim|case|request|attempt|log|usage|draw|authorisation|capture|adjustment|"
    r"event|ticket|split|sale|return|shift)s?$")

# A table whose name says it holds settings, even if it also looks transactional.
CONTROL_NAME = re.compile(
    r"(^|_)(rule|policy|policies|profile|config|configuration|setting|settings|plan|band|"
    r"tier|scheme|template|definition|matrix|threshold)s?$")

# The head noun that makes a column a configured value rather than a fact.
CLASSES = collections.OrderedDict([
    ("charge", {"fee", "charge", "surcharge", "commission", "gratuity", "tip", "levy"}),
    ("threshold", {"limit", "quota", "threshold", "ceiling", "allowance", "tolerance"}),
    ("rate", {"rate", "multiplier", "ratio"}),
    ("duration", {"minutes", "hours", "days", "seconds", "timeout", "ttl", "window", "interval"}),
])
ALL_HEADS = set().union(*CLASSES.values())

# How much, in what form, at what moment. Stripped so that `late_fee_amount` on the policy and
# `late_fee` on the settlement reach the same stem and pair up.
QUALIFIER = {"amount", "value", "total", "percent", "pct", "basis", "cap", "min", "max",
             "minimum", "maximum", "accrued", "applied", "calculated", "charged", "per", "unit",
             "default", "standard", "period"}

# **Units of measure — the vocabulary the four classes could not see.** Added 22 September.
# `fnb.temperature_log` stored `min_celsius` and `max_celsius` on every reading and nothing defined
# them, and its `check_point_id` was NOT NULL against a table that existed nowhere. **The checker
# missed both**: `celsius` is in no head-noun class, and `threshold_celsius` surfaced only because it
# happens to contain the word *threshold*. The defect class is vocabulary-independent and the
# detector was not. `db` is left out on purpose — it reads as *database* as often as *decibels*.
UNITS = {"celsius", "fahrenheit", "kelvin", "kg", "kilograms", "grams", "litres", "liters", "ml",
         "millilitres", "metres", "meters", "cm", "mm", "lux", "psi", "decibels", "kwh", "watts",
         "volts", "rpm"}

# What turns a unit from a reading into a limit.
LIMIT_QUALIFIER = {"min", "max", "minimum", "maximum", "lower", "upper", "threshold", "target",
                   "limit", "tolerance", "floor", "ceiling"}

# **An observation, not a setting.** Nobody configures what a stopwatch read.
MEASUREMENT = {"elapsed", "actual", "downtime", "recorded", "observed", "used", "consumed",
               "counted", "remaining", "progress", "age", "taken", "spent", "paused", "achieved",
               "current", "last", "overdue", "variance", "estimated", "first"}

# Stems that name the whole bill rather than one charge on it.
NOT_A_VALUE = {"tax", "net", "gross", "sub", "paid", "refund", "balance", "due", "line",
               "order", "base", "list", "original", "final", "expected", "actual"}

# **A stem this generic pairs with anything, so it pairs with nothing.** `duration_minutes` on a
# kitchen exception and `duration_seconds` on a media asset share the word and not the subject;
# matching them proposed an audio length as the control for a kitchen delay. Treated like a bare
# stem - still reported, never paired.
GENERIC_STEM = {"", "duration", "wait", "time", "value", "default"}

# **A control table named after the thing it controls is that thing's control**, whatever its
# columns are called. `rental.fee_policy` pairs on a column because it holds several fee kinds and
# has to say which is which - `late_fee_amount`, `late_fee_basis`. `fnb.service_charge_policy`
# holds one, so its columns are `basis` and `rate_percent` and nothing in them carries the word
# `service`. Reading only columns, the checker went on reporting a gap that had just been filled,
# which is the most expensive way for a checker to be wrong.
CONTROL_SUFFIX = {"policy", "policies", "rule", "rules", "config", "configuration", "setting",
                  "settings", "profile", "plan", "template", "definition", "scheme", "matrix",
                  "band", "tier", "threshold", "checkpoint", "limits"}

# Platform's own plumbing. `control.scaling_policy` is infrastructure and pairs with nothing.
INFRA_SCHEMA = {"control", "platform"}

NUMERIC = re.compile(r"^(numeric|decimal|integer|bigint|money|smallint)")

# **These four say the row is not a defect, so the row goes quiet.** `genuinelyMissing` and
# `fixedByLaw` are findings and keep reporting - a ledger that silenced its own gaps would be
# worse than no ledger.
CLOSING_VERDICT = {"setByAProvider", "enteredPerIncident", "derivedFromAnother", "observedNotSet"}

BACKTICKED_COL = re.compile(r"`([a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*)`")


def classify(column):
    """-> (class, stem) if the column carries a configured value, else None.

    **The stem is what pairs an outcome to its control**, so it is the tokens that survive both
    the head noun and every qualifier. `seller_fee_percent` and `seller_fee_amount` are the same
    stem seen from two sides; `late_fee` and `late_fee_amount` likewise. A bare `fee` or
    `surcharge` stems to the empty string and is reported on its own, because an empty stem
    pairs with anything and would manufacture a match.
    """
    tokens = [t for t in column.split("_") if t]
    seen = set(tokens)
    if seen & MEASUREMENT:
        return None
    cls = next((c for c, heads in CLASSES.items() if seen & heads), None)
    if cls is None:
        # **A unit is a limit when something bounds it, and a reading when nothing does.**
        # `min_celsius` is a setting; `value_celsius` is what a probe said. The unit is kept in the
        # stem — `min_celsius` on a log pairs with `min_celsius` on the checkpoint that defines it,
        # which is the pairing this rule exists to make visible.
        if seen & UNITS and seen & LIMIT_QUALIFIER:
            stem = "_".join(t for t in tokens if t not in ALL_HEADS and t not in QUALIFIER
                            and t not in LIMIT_QUALIFIER)
            return ("threshold", stem) if stem and stem not in NOT_A_VALUE else None
        return None
    stem = "_".join(t for t in tokens if t not in ALL_HEADS and t not in QUALIFIER)
    if stem in NOT_A_VALUE:
        return None
    return cls, stem


def answered():
    """Rows the package has already ruled on, from `handoff/values-without-configuration.md`.

    The table is `| `schema.table.column` | verdict | why |`. Missing file means nothing has
    been answered yet, which is a state, not an error.
    """
    out = {}
    if not os.path.exists(LEDGER):
        return out
    with io.open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            for col in BACKTICKED_COL.findall(cells[0]):
                out[col] = (cells[1], cells[2])
    return out


def main():
    argv = sys.argv[1:]
    only = argv[argv.index("--class") + 1] if "--class" in argv else None

    with io.open(REF, encoding="utf-8") as fh:
        cols = json.load(fh)["cols"]

    control = collections.defaultdict(list)
    outcome = []

    for table, rows in cols.items():
        schema, _, short = table.partition(".")
        names = set(r["column"] for r in rows)
        # A definition is its own configuration; only a transactional row is asked the question.
        #
        # **An effective-dated row is a definition whatever it is called.** `effective_from` says
        # the row states what holds over a period, and an event does not have a period — it
        # happened. Added 22 September after `resources.venue_assignment.travel_buffer_minutes`
        # was reported, triaged as `genuinelyMissing`, and turned out to *be* the control: the
        # row is a resource's standing venue footprint with `effective_from`, `effective_to` and
        # `scope_path`, and only its name ends in `assignment`. **The name made a definition look
        # like an event and nobody checked the columns.** Exactly two tables were affected, both
        # standing records; `workforce.work_assignment` carries no value columns, so the change
        # moves nothing else.
        is_control = ((not TRANSACTION_NAME.search(short)) or bool(CONTROL_NAME.search(short))
                      or "effective_from" in names)
        for r in rows:
            hit = classify(r["column"])
            if hit is None:
                continue
            cls, stem = hit
            if is_control:
                control[(schema, cls, stem)].append((table, r["column"]))
                # The table's own name is a control for what it is named after.
                named = classify("_".join(
                    t for t in short.split("_") if t not in CONTROL_SUFFIX))
                if named and named[1] not in GENERIC_STEM:
                    control[(schema, named[0], named[1])].append((table, r["column"]))
            elif schema not in INFRA_SCHEMA and NUMERIC.match(r.get("type") or ""):
                outcome.append((table, r["column"], cls, stem))

    ruled = answered()
    controlled, cross, closed, confirmed, uncontrolled = [], [], [], [], []

    for table, column, cls, stem in sorted(set(outcome)):
        if only and cls != only:
            continue
        schema = table.partition(".")[0]
        key = "%s.%s" % (table, column)
        # A bare or generic stem pairs with anything, so it never claims a control.
        pairs = stem not in GENERIC_STEM
        hits = control.get((schema, cls, stem), []) if pairs else []
        if hits:
            controlled.append((cls, key, hits))
            continue
        if key in ruled and ruled[key][0] in CLOSING_VERDICT:
            closed.append((cls, key, ruled[key]))
            continue
        if key in ruled:
            confirmed.append((cls, key, ruled[key]))
            continue
        elsewhere = []
        if pairs:
            for (sch2, cls2, stem2), v in control.items():
                if cls2 == cls and stem2 == stem and sch2 != schema:
                    elsewhere.extend(v)
        if elsewhere:
            cross.append((cls, key, elsewhere))
        else:
            uncontrolled.append((cls, key, stem))

    out = io.StringIO()
    out.write("Applied values with no configuration behind them\n")
    out.write("=" * 48 + "\n\n")

    if uncontrolled:
        out.write("UNCONTROLLED - %d, not yet answered\n\n" % len(uncontrolled))
        for cls, key, stem in uncontrolled:
            out.write("  %-10s %-46s no control for %r\n" % (cls, key, stem or "<bare>"))
        out.write("\n  Each is setByAProvider, enteredPerIncident, derivedFromAnother,\n")
        out.write("  observedNotSet, fixedByLaw or genuinelyMissing. Record which in\n")
        out.write("  handoff/values-without-configuration.md. The last two keep reporting.\n\n")
    else:
        out.write("UNCONTROLLED - none\n\n")

    if confirmed:
        out.write("CONFIRMED GAP - %d, triaged and still open\n\n" % len(confirmed))
        for cls, key, verdict_why in confirmed:
            out.write("  %-10s %-46s %-17s %s\n"
                      % (cls, key, verdict_why[0], verdict_why[1][:54]))
        out.write("\n")

    if cross:
        out.write("CROSS-SCHEMA - %d, a control exists but another module owns it\n\n" % len(cross))
        for cls, key, hits in cross:
            out.write("  %-10s %-46s <- %s\n"
                      % (cls, key, ", ".join("%s.%s" % h for h in hits[:2])))
        out.write("\n")

    if closed:
        out.write("ANSWERED - %d, ruled on in the ledger\n\n" % len(closed))
        for cls, key, verdict_why in closed:
            out.write("  %-10s %-46s %-19s %s\n"
                      % (cls, key, verdict_why[0], verdict_why[1][:52]))
        out.write("\n")

    out.write("CONTROLLED - %d\n\n" % len(controlled))
    for cls, key, hits in controlled:
        out.write("  %-10s %-46s <- %s\n"
                  % (cls, key, ", ".join("%s.%s" % h for h in hits[:2])))

    total = (len(controlled) + len(cross) + len(closed) + len(confirmed)
             + len(uncontrolled))
    out.write("\n%d applied value(s), %d controlled, %d cross-schema, %d answered, "
              "%d confirmed gap(s), %d untriaged\n"
              % (total, len(controlled), len(cross), len(closed), len(confirmed),
                 len(uncontrolled)))

    sys.stdout.write(out.getvalue())

    if "--csv" in argv:
        path = argv[argv.index("--csv") + 1]
        with io.open(path, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["column", "class", "state", "detail"])
            for cls, key, stem in uncontrolled:
                w.writerow([key, cls, "uncontrolled", stem])
            for cls, key, hits in cross:
                w.writerow([key, cls, "crossSchema", "; ".join("%s.%s" % h for h in hits)])
            for cls, key, verdict_why in closed + confirmed:
                w.writerow([key, cls, verdict_why[0], verdict_why[1]])
            for cls, key, hits in controlled:
                w.writerow([key, cls, "controlled", "; ".join("%s.%s" % h for h in hits)])
        sys.stdout.write("\nwrote %s\n" % path)

    # Reports, does not gate. Whether an outcome needs a control is a judgement.
    return 0


if __name__ == "__main__":
    sys.exit(main())
