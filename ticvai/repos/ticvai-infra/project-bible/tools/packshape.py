#!/usr/bin/env python3
"""Turn a workshop-pack screen record into typed schema properties.

**The pack is a specification, not decoration.** Every screen in `sources/workshop/pack.json`
carries the client's own bulleted directory of what the screen shows and what it configures —
*"Each zone receives capacity, operating schedule, security classification, entry requirements,
exit requirements, allowed credential classes"*. That is a field list written by the people who
own the requirement. Transcribing it into properties is reading, not inventing; the only thing
this module adds is a name and a type, and it records the sentence each property came from so a
reviewer can check the reading in one step.

**What it refuses to do is guess.** A bullet that is a sentence, an example, a comparison
(`Height >= 130 cm`), a hierarchy illustration (`-> Public Plaza`) or a page footer is dropped
rather than bent into a field, and the count of drops is reported so the loss is visible.

The section HEADING decides what its bullets are, because the pack is consistent about it:

  `Purpose`, `Acceptance Condition`, `Example`   prose            -> dropped
  `Dashboard should show`, `KPI cards`, `Track`  metrics          -> properties, plurals as counts
  `For each X`, `Each X receives`, `Configure`   fields           -> properties
  `Create`, `Statuses`, `Reasons`                enum             -> ONE enumerated property
  `Filter by`, `Search by`, `Analyze by`         query            -> query parameters
  `Actions`, `Authorized users can`              actions          -> not properties; verbs
  a bare noun phrase (`Finance`, `Security`)     a field group    -> properties

Used by `tools/specify-pack-operations.py`. Import it; do not copy it.
"""
from __future__ import annotations

import re

# -- classification -----------------------------------------------------------------------------
PROSE = re.compile(r"^(purpose|acceptance|example|for example|ai |board objective|architecture|"
                   r"note|scenario|outcome|benefit|result|summary|use case|if|and$|then$|or$|"
                   r"backend screen|frontend screen|recommended|system (should|must))", re.I)
QUERY = re.compile(r"^(filter|search|analy[sz]e|group|sort|segment|slice)\b.*\bby\b|"
                   r"^(filter|search)\b", re.I)
FIELD = re.compile(r"(for each|each \w+ (receives|has|carries|gets|shall|should|may)|"
                   r"should (include|display|show|have|contain)|must (include|have|contain)|"
                   r"^(configure|capture|record|field|define|specify|set|enter|provide)\b|"
                   r"attributes?|parameters?|properties|^per \b|directory|configuration|"
                   r"(shall|should|may|must|can) (show|display|include|have|contain|support|"
                   r"consider|depend|originate|preserve|apply))", re.I)
METRIC = re.compile(r"(dashboard|should show|^show\b|^display|kpi|metric|^track\b|^monitor\b|"
                    r"^measure\b|count|summar|overview|at a glance|statistic|^report)", re.I)
ENUMY = re.compile(r"(^create\b|types?$|statuses$|states$|options$|categories$|classes$|levels$|"
                   r"reasons?$|channels$|values$|kinds$|tiers$|^select\b)", re.I)
ACTION = re.compile(r"^(actions?|quick actions|authori[sz]ed users can|allow|support|operations|"
                    r"users? can|staff can|admin\w* can)\b", re.I)

# **An action heading does not make its bullets actions.** `Support` sits over
# *Minimum Quantity / Quantity Bands / Group Size* as often as over *Suspend / Escalate / Publish*,
# and reading the first list as verbs threw away a whole pricing directory. The bullet's own first
# word decides: an imperative verb is an action, anything else is a field.
VERBS = {
    "view", "create", "suspend", "escalate", "send", "publish", "freeze", "duplicate", "open",
    "close", "edit", "delete", "remove", "add", "assign", "approve", "reject", "cancel", "export",
    "import", "download", "upload", "refund", "void", "extend", "transfer", "merge", "split",
    "clone", "archive", "restore", "lock", "unlock", "enable", "disable", "activate", "resend",
    "deactivate", "retry", "override", "adjust", "apply", "revoke", "issue", "print", "notify",
    "schedule", "trigger", "run", "generate", "compare", "filter", "search", "sort", "select",
    "drag", "configure", "set", "update", "save", "submit", "block", "unblock", "pause", "resume",
    "reset", "sync", "validate", "verify", "convert", "upgrade", "downgrade", "reprint", "reissue",
    "reverse", "release", "withdraw", "flag", "tag", "link", "unlink", "move", "copy", "replace",
    "define", "review", "resolve", "dismiss", "acknowledge", "broadcast", "invite", "onboard",
}


def is_action(label):
    w = (label or "").split()
    return bool(w) and w[0].lower() in VERBS


# **A rule builder lists its operators, and they are not fields.** `PromotionRuleBuilderInput` came
# out with properties called `and`, `or` and `not` because the pack writes the boolean vocabulary
# as bullets under the condition editor. They are the grammar of the rule, not columns of it.
RESERVED = {"and", "or", "not", "then", "else", "if", "when", "true", "false", "yes", "no",
            "all", "any", "none", "both", "other", "others", "etc", "and or", "vs", "versus",
            "greater than", "less than", "equal to", "between", "contains", "in", "is"}


def classify(heading, items):
    h = (heading or "").strip()
    if PROSE.search(h):
        return "prose"
    if QUERY.search(h):
        return "query"
    if METRIC.search(h):
        return "metrics"
    if ENUMY.search(h):
        return "enum"
    if FIELD.search(h):
        return "fields"
    if ACTION.search(h):
        return "actions"
    # A heading that is itself a short noun phrase names a group of fields - `Finance`, `Security`,
    # `Membership & Loyalty`. This is the pack's most common shape and the residue without it.
    return "fields"


# -- one bullet -> a name and a type --------------------------------------------------------------
ACRO = {"id": "Id", "ids": "Ids", "url": "Url", "api": "Api", "sla": "Sla", "kpi": "Kpi",
        "ai": "Ai", "pii": "Pii", "qr": "Qr", "ota": "Ota", "b2b": "B2b", "b2c": "B2c",
        "crm": "Crm", "sms": "Sms", "vip": "Vip", "pos": "Pos", "utm": "Utm", "gdpr": "Gdpr",
        "nfc": "Nfc", "eta": "Eta", "ui": "Ui", "csv": "Csv", "pdf": "Pdf", "sso": "Sso"}

# **A bullet that is prose is dropped, not bent into a field.** An operator, an example marker or a
# modal verb means the sentence is describing behaviour; a field name never needs one.
REJECT = re.compile(u"[≥≤≠<>=]|\\bshould\\b|\\bmust\\b|\\bcan be\\b|\\bsuch as\\b|"
                    u"^e\\.?g\\.?\\b|\\bi\\.e\\.|\\bwithout\\b|\\brather than\\b|\\bso that\\b|"
                    u"\\bwhich\\b|\\bthat\\b|\\bwhen\\b|\\bif\\b", re.I)
FOOTER = re.compile(r"(\|\s*P\s*a\s*ge)|(^\d+\s*\|)|(^page\s+\d+)", re.I)
HIERARCHY = re.compile(u"^\\s*[→>]")     # `-> Public Plaza` illustrates a tree, not a field

INT = re.compile(r"^(total|number of|count of|no\. of|active|failed|open|closed|pending|queued|"
                 r"online|offline|new|expired|cancelled|approved|rejected)\b|"
                 r"\b(count|volume|quantity|qty|attempts|retries|breaches|alerts|errors|"
                 r"capacity|occupancy|headcount|attendance|threshold|limit|quota|slots|seats)\b|"
                 r"\b(online|offline|open|closed|active|failed|pending)$", re.I)
NUM = re.compile(r"\b(rate|ratio|percent|percentage|score|average|avg|index|margin|"
                 r"utili[sz]ation|conversion|uplift|elasticity|share)\b|%", re.I)
MONEY = re.compile(r"\b(revenue|amount|price|cost|fee|balance|refund|deposit|payout|spend|"
                   r"charge|commission|discount|subtotal|turnover|gmv)\b", re.I)
DATE = re.compile(r"\b(date|time|timestamp|expiry|expires?|scheduled|created|updated|deadline|"
                  r"window|period|duration)\b|^(last|next|since|until)\b", re.I)
BOOL = re.compile(r"^(is|has|can|allow|enable|require|permit)\b|"
                  r"\b(support|enabled|required|allowed|flag|toggle|consent)$", re.I)
ENUM_SUFFIX = re.compile(r"\b(status|state|type|mode|tier|level|class|category|channel|reason|"
                         r"stage|priority|severity|source|method|frequency)$", re.I)
IDENT = re.compile(r"\b(id|identifier|uuid)$", re.I)
# A plural bare noun under a metrics heading is a count: `Turnstiles`, `Overrides`, `Entry gates`.
PLURAL = re.compile(r"[a-rt-z]s$|[^s]es$", re.I)


def camel(text):
    toks = [t for t in re.split(r"[^A-Za-z0-9]+", text) if t]
    if not toks:
        return None
    out = []
    for i, t in enumerate(toks):
        low = t.lower()
        if i == 0:
            out.append(low)
        else:
            out.append(ACRO.get(low, (t[:1].upper() + t[1:].lower()) if not t.isupper()
                                else t.capitalize()))
    name = re.sub(r"[^A-Za-z0-9]", "", "".join(out))
    return name if name and name[0].isalpha() and len(name) > 1 else None


# `Devices online/offline` is TWO counts, not one string. The pack writes a paired metric with a
# slash and a shared noun; splitting it is what makes both countable.
PAIR = re.compile(r"^([A-Za-z][A-Za-z ]*?)\s+([A-Za-z]+)/([A-Za-z]+)$")


def split_pair(label):
    """`Devices online/offline` -> `Devices online`, `Devices offline`; otherwise None."""
    m = PAIR.match(label)
    if not m:
        return None
    noun, a, b = m.group(1).strip(), m.group(2), m.group(3)
    return ["%s %s" % (noun, a), "%s %s" % (noun, b)]


def clean(raw, relaxed=False):
    """The bullet as a field label, or None when it is not one."""
    if HIERARCHY.match(raw or ""):
        return None
    s = (raw or "").strip().lstrip(u"•-– ").strip().rstrip(".;,:")
    if not s or FOOTER.search(s) or s.lower() in RESERVED:
        return None
    if relaxed:
        # The second pass, for a screen whose every bullet is a sentence. Keep the noun phrase up
        # to the first modal or subordinator rather than dropping the requirement entirely.
        s = re.split(r"\b(should|must|which|that|when|if|so that|rather than)\b", s, 1, re.I)[0]
        s = s.strip().rstrip(".;,:")
        return s if s and len(s.split()) <= 7 and not re.match(r"^\d", s) else None
    if REJECT.search(s):
        return None
    if len(s.split()) > 5 or re.match(r"^\d", s):
        return None
    return s


def typeof(label, kind, money_ref="Money"):
    if IDENT.search(label):
        return {"type": "string"}
    if BOOL.search(label):
        return {"type": "boolean"}
    # **On a dashboard a plural noun is a count, even when it carries a date word.**
    # `Scheduled Changes` is how many are scheduled, not when; the date rule read it as a timestamp
    # until this took precedence over it.
    if kind == "metrics" and PLURAL.search(label) and len(label.split()) <= 3:
        return {"type": "integer"}
    if DATE.search(label):
        return {"type": "string", "format": "date-time"}
    if INT.search(label):
        return {"type": "integer"}
    if NUM.search(label):
        return {"type": "number"}
    if MONEY.search(label):
        return {"$ref": money_ref}
    if ENUM_SUFFIX.search(label):
        return {"type": "string"}
    # **Only under a metrics heading.** `Turnstiles` on a dashboard is how many there are; the same
    # word in a configuration directory is a name, and typing it as a number would be wrong.
    if kind == "metrics" and PLURAL.search(label) and len(label.split()) <= 3:
        return {"type": "integer"}
    return {"type": "string"}


def enum_property(heading, labels):
    """An enum section names ONE property, not one property per value.

    `Public Zone / Ticketed Zone / VIP Zone / Staff Zone ...` is the zone *type* vocabulary. The
    shared trailing word is what says so, and without one this is not an enum at all.
    """
    if len(labels) < 3:
        return None
    tails = [l.split()[-1].lower() for l in labels if l.split()]
    if not tails:
        return None
    common = max(set(tails), key=tails.count)
    if tails.count(common) < max(3, len(tails) * 0.6):
        # No shared noun - fall back to the heading, but only when the heading names a kind.
        if not ENUMY.search(heading) or len(heading.split()) > 3:
            return None
        common = heading.split()[-1].lower()
    base = common if common.endswith(("type", "status", "state", "reason", "channel")) \
        else common + " type"
    name = camel(base)
    vals = []
    for l in labels:
        stripped = re.sub(r"\b%s\b" % re.escape(common), "", l, flags=re.I).strip()
        v = camel(stripped or l)
        if v and v not in vals:
            vals.append(v)
    return (name, vals) if name and len(vals) >= 3 else None


# **A third pattern: the heading IS the field and the bullet is its example value.** Four screens
# lay out their numbers as `Current: 8,214`, `Capacity: 12,000`, `Occupancy: 68.5%`,
# `Kids Zone: 1,842 / 2,500`. Read bullet-first those screens have no fields at all; read this way
# they have exactly the ones the client drew.
VALUE_ONLY = re.compile(u"^[\\s0-9.,%/–—\\-+±=~<>$€£]*(aed|usd|eur|gbp|%)?[\\s0-9.,%/–—\\-+]*$", re.I)


def value_shaped(items):
    """True when every bullet is a bare value, so the heading is carrying the field name."""
    vals = [i.strip() for i in items if i and i.strip() and not FOOTER.search(i)]
    if not vals or len(vals) > 3:
        return False
    return all(VALUE_ONLY.match(re.sub(u"[🟢🟠🔴🟡⚪]", "", v).strip()) for v in vals)


def _shape(rec, money_ref, relaxed):
    props, sources, query, actions = {}, {}, {}, []
    kinds = {}
    dropped = 0
    for heading, items in (rec.get("sections") or {}).items():
        if value_shaped(items) and not PROSE.search(heading or ""):
            n = camel(heading)
            if n and n not in props:
                example = ", ".join(i.strip() for i in items if i.strip())
                props[n] = dict(typeof(heading, "metrics", money_ref),
                                description="%s (the pack shows %s)" % (heading, example))
                sources[n] = heading
                kinds[n] = "metrics"
            continue
        kind = classify(heading, items)
        labels = []
        for raw in items:
            c = clean(raw, relaxed)
            if c is None:
                dropped += 1
            else:
                labels += (split_pair(c) or [c])
        if kind == "prose" or not labels:
            continue
        if kind == "actions":
            actions += [l for l in labels if is_action(l)]
            labels = [l for l in labels if not is_action(l)]
            if not labels:
                continue
            kind = "fields"
        elif kind != "enum":
            # Even outside an action heading, a bullet that opens with an imperative verb is
            # something the screen DOES, not something it holds.
            actions += [l for l in labels if is_action(l)]
            labels = [l for l in labels if not is_action(l)]
            if not labels:
                continue
        if kind == "enum":
            got = enum_property(heading, labels)
            if got:
                n, vals = got
                if n not in props:
                    props[n] = {"type": "string", "enum": vals,
                                "description": "Vocabulary listed under %s." % heading}
                    sources[n] = heading
                    kinds[n] = "fields"
                continue
            kind = "fields"          # not an enum after all; treat it as a field group
        target = query if kind == "query" else props
        for l in labels:
            n = camel(l)
            if not n or n in props or n in query:
                continue
            target[n] = typeof(l, kind, money_ref)
            target[n]["description"] = l
            sources[n] = heading
            kinds[n] = kind
    return {"props": props, "query": query, "actions": actions, "kinds": kinds,
            "dropped": dropped, "sources": sources, "relaxed": relaxed}


def screen_shape(rec, money_ref="Money"):
    """`{props, query, actions, dropped, sources, relaxed}` for one pack screen record.

    **Six screens write every requirement as a sentence** — *"The system should display the current
    occupancy of each zone against its declared capacity"* — and the strict reading drops all of
    them, leaving a schema with no properties at all. That is a worse answer than a longer name, so
    those screens get a second pass that keeps longer phrases, and `relaxed` says which ones so a
    reviewer knows the names there were read out of prose.
    """
    out = _shape(rec, money_ref, relaxed=False)
    if not out["props"]:
        out = _shape(rec, money_ref, relaxed=True)
    return out
