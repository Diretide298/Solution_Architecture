#!/usr/bin/env python3
"""Draft the contract operations the workshop pack's screens need, one module at a time.

**590 screens specify what a screen shows and nothing says what serves it.** The pack is a design
document: it names a board, a screen, a purpose and a list of things on display. It does not name
an endpoint, and `derive-pack-linkage.py` could match only 13 of 590 against operations that
already exist. The other 577 need operations authored, and this drafts them.

## What is derived, and what is deliberately not

**Derived, because the package already knows it:**

  `operationId`   the entity from the screen title crossed with the verb its archetype implies -
                  the same derivation `derive-pack-linkage.py` uses to name the gap
  `audience`      the platform's own audience. A screen on P10 Partner Web serves a partner.
  `scope-level`   the platform's level - a venue back office is `venue`, a platform console is
                  `tenant`. Taken from what the contract's existing operations use.
  `permission`    the contract's own convention, split by verb: the permission its reads use and
                  the permission its writes use. **No new permission is invented** - 134 exist and
                  a 135th that nothing else grants is a permission nobody can hold.

**NOT derived, and the reason matters:**

  the response shape.  The pack lists what a screen DISPLAYS - "17 conversions rejected by
  eligibility rules", "Active Upgrade Paths" - and those are captions, not fields. Turning 37
  captions into 37 properties would produce a schema that looks authoritative and describes
  nothing. So the response is a **provisional envelope**: an id, a name, a state and the screen it
  was drafted for, marked `x-ticvai-provisional: true`.

**And no `x-ticvai-persistence`, which is the important half.** A drafted operation does not
assert a table. Six hundred speculative tables would reach `derive-ddl`, the workbook and the ER
model, and every one of them would be a storage decision nobody made. **An operation can exist
before its storage is decided; a table cannot.**

## So what is this good for

It closes the gap between a screen and an endpoint so the estate is navigable and countable, and
it puts a named, permissioned, audience-correct stub in front of whoever writes the real one.
**It is not a substitute for that person.** Every operation it writes says so in its description.

Run: `python3 tools/draft-pack-operations.py --module "Ticket Upgrade" [--apply]`
     `python3 tools/draft-pack-operations.py --list`
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCREENS = ROOT / "screens"
LINEAGE = ROOT / "handoff" / "api-data-lineage.json"

VERBS = ("list", "get", "create", "update", "set", "delete", "remove", "add", "approve",
         "reject", "publish", "activate", "deactivate", "cancel", "void", "assign", "validate",
         "simulate", "export", "import", "record", "submit", "configure", "search", "resolve",
         "revoke", "issue", "enrol", "enroll", "override", "register", "release", "reconcile")

ARCHETYPE_VERB = {
    "command": "list", "center": "list", "centre": "list", "dashboard": "list",
    "monitor": "list", "directory": "list", "register": "list", "registry": "list",
    "library": "list", "explorer": "list", "inbox": "list", "management": "list",
    "audit": "list", "history": "list", "log": "list", "analytics": "list",
    "intelligence": "list", "optimization": "list", "forecasting": "list", "overview": "list",
    "builder": "set", "designer": "set", "workspace": "set", "studio": "set",
    "configuration": "set", "config": "set", "setup": "set", "assignment": "set",
    "simulation": "simulate", "approval": "approve", "publication": "publish",
    "creation": "create", "execution": "create",
}
NOISE = set(ARCHETYPE_VERB) | {"and", "the", "of", "for", "with", "ai", "amp", "screen",
                               "operations", "operation", "control", "controls", "engine"}

# **Which contract owns a module**, taken from where its nearest existing operations already live.
CONTRACT_OF = {
    "Access Control": "access",
    "B2B, Reseller & OTA Partner Management": "subscription",
    "Communication & Notification Platform Services": "marketing-crm",
    "Customer Service": "marketing-crm",
    "Group Sales   Corporate Booking Management": "orders",
    "Membership   Annual Pass Management": "subscription",
    "Order   Reservation Management": "orders",
    "Pricing   Revenue Management": "catalogue",
    "Privacy  Consent   Preference Management": "marketing-crm",
    "Product Lifecycle   Catalogue Governance": "catalogue",
    "Promotions   Bundles Management": "promotions",
    "Rules  Workflow  Approval   Automation Engine": "approvals",
    "Sales Channel Management": "catalogue",
    "Ticket Media   Credential Management": "access",
    "Ticket Resale Marketplace": "orders",
    "Ticket Upgrade, Exchange & Conversion": "orders",
    "Waiver, Consent & Digital Form Management": "marketing-crm",
}

PLAT_AUD = {"staff": "staff", "platformAdmin": "staff", "guest": "guest",
            "public": "public", "partner": "partner"}


# **Words that end in `s` and are already singular.** Stripping the last letter turned `status`
# into `statu` and `analysis` into `analysi`, and six operation names shipped that way before
# anyone read them aloud. This is not a general pluraliser and does not need to be; it needs to
# stop mangling the handful of words the pack's screen titles actually end on.
NOT_PLURAL = {"status", "analysis", "autonomous", "bonus", "campus", "census", "consensus",
              "focus", "basis", "crisis", "diagnosis", "emphasis", "hypothesis", "synopsis",
              "access", "address", "business", "process", "class", "gas", "bus", "lens",
              "series", "species", "means", "news", "previous", "various", "continuous",
              "simultaneous", "miscellaneous", "anonymous", "synchronous"}


def singular(w: str) -> str:
    if w.lower() in NOT_PLURAL:
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith("ss") or w.endswith("us") or w.endswith("is"):
        return w
    if w.endswith("s") and len(w) > 3:
        return w[:-1]
    return w


def screen_tokens(title: str):
    words = [w.lower() for w in re.findall(r"[A-Za-z]+", title)]
    verbs = {ARCHETYPE_VERB[w] for w in words if w in ARCHETYPE_VERB} or {"list"}
    seq, seen = [], set()
    for w in words:
        t = singular(w)
        if w not in NOISE and len(w) > 2 and t not in seen:
            seen.add(t)
            seq.append(t)
    return sorted(verbs)[0], seq


def pascal(words) -> str:
    return "".join(w.capitalize() for w in words)


def module_of(pack: str) -> str:
    stem = re.sub(r"\.pdf$", "", pack, flags=re.I)
    stem = re.sub(r"[_ ]*Reference$", "", stem, flags=re.I)
    stem = re.sub(r"[_ ]*Module$", "", stem, flags=re.I)
    return stem.replace("_", " ").strip()


def conventions(lin: dict) -> dict:
    """Each contract's own permission and scope habits, split by read and write."""
    out = {}
    by = collections.defaultdict(lambda: {"r": collections.Counter(), "w": collections.Counter(),
                                          "s": collections.Counter()})
    for v in lin.values():
        c = v.get("contract")
        if not c or not v.get("perm"):
            continue
        (by[c]["r"] if v.get("verb") == "GET" else by[c]["w"])[v["perm"]] += 1
        by[c]["s"][v.get("scope")] += 1
    for c, d in by.items():
        out[c] = {
            "read": d["r"].most_common(1)[0][0] if d["r"] else None,
            "write": d["w"].most_common(1)[0][0] if d["w"] else (
                d["r"].most_common(1)[0][0] if d["r"] else None),
            "scope": d["s"].most_common(1)[0][0] if d["s"] else "venue",
        }
    return out


def collect():
    rows = []
    for f in sorted(SCREENS.glob("P*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        p = doc["platform"]
        for s in doc["screens"]:
            src = s.get("source") or {}
            if not src.get("pack") or s.get("apis"):
                continue
            rows.append({"screen": s, "plat": p, "file": f,
                         "module": module_of(src["pack"]), "board": src.get("board")})
    return rows


def block(oid, verb, screen_ref, summary, purpose, perm, scope, aud, ref, array, page, module):
    q = lambda t: str(t).replace("'", "''")
    # ADR-0018: every configuration operation declares its level, and a drafted one is no
    # exception — `check-config-scope` failed 17 of these before this line existed.
    cfg = "" if verb == "get" else "      x-ticvai-config-scope: %s\n" % scope
    items = ("                type: array\n                items:\n"
             "                  $ref: '#/components/schemas/%s'\n" % ref) if array else (
        "                $ref: '#/components/schemas/%s'\n" % ref)
    return f"""      operationId: {oid}
      x-ticvai-consumed-by:
        - "{screen_ref}"
      x-ticvai-audience:
      - {aud}
      x-ticvai-provisional: true
      summary: {q(summary)}
      description: '**Drafted from the workshop pack and not yet specified.** {q(module)}, page
        {page}. The screen says: {q(purpose)[:300]}

        **The response below is an envelope, not a schema.** The pack lists what the screen
        DISPLAYS and those are captions rather than fields, so inventing properties from them
        would produce something that looks authoritative and describes nothing. **No
        `x-ticvai-persistence` either** - an operation can exist before its storage is decided and
        a table cannot. The name, the permission, the scope and the audience are derived; the
        shape is the part a person writes.

        '
      tags:
      - drafted
      x-ticvai-permission: {perm}
      x-ticvai-scope-level: {scope}
{cfg}      x-ticvai-offline-capable: false
      x-ticvai-conflict-policy: serverWins
      x-ticvai-read-routing: {"replica" if verb == "get" else "primary"}
      responses:
        '200':
          description: {q(summary)}
          content:
            application/json:
              schema:
{items}"""


ENVELOPE = """      type: object
      x-ticvai-provisional: true
      description: '**A provisional envelope, drafted %s from the workshop pack.** It carries what
        every one of these screens needs to address a row and nothing it has not earned. **There is
        deliberately no `x-ticvai-persistence`** - naming a table here would put a storage decision
        nobody made into the ER model and the DDL.'
      required:
      - id
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        state:
          type: string
        updatedAt:
          type: string
          format: date-time"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", help="substring of the workshop module to draft")
    ap.add_argument("--list", action="store_true", help="show the modules and their sizes")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    lin = json.loads(LINEAGE.read_text(encoding="utf-8"))
    conv = conventions(lin)
    rows = collect()

    if a.list or not a.module:
        by = collections.Counter(r["module"] for r in rows)
        print("%d pack screen(s) still calling no operation\n" % len(rows))
        for m, n in sorted(by.items()):
            print("  %-52s %3d  -> contracts/*/%s.yaml" % (m[:52], n, CONTRACT_OF.get(m, "?")))
        if not a.module:
            print("\n  pass --module to draft one")
        return 0

    todo = [r for r in rows if a.module.lower() in r["module"].lower()]
    if not todo:
        print("no pack screens match %r" % a.module)
        return 1
    module = todo[0]["module"]
    contract = CONTRACT_OF.get(module)
    if not contract:
        print("no contract mapped for %r" % module)
        return 1
    path = next((ROOT / "contracts").rglob("%s.yaml" % contract), None)
    assert path, contract
    conv_c = conv.get(contract, {"read": None, "write": None, "scope": "venue"})

    text = path.read_text(encoding="utf-8")
    existing = {m for m in re.findall(r"operationId: (\w+)", text)}
    made, wiring = [], {}
    used_routes = set(re.findall(r"^  (/\S+):$", text, re.M))
    for r in todo:
        s, p = r["screen"], r["plat"]
        verb, seq = screen_tokens(s["name"])
        oid = verb + pascal(seq[:3])
        n = 2
        while oid in existing:
            oid = verb + pascal(seq[:3]) + str(n)
            n += 1
        existing.add(oid)
        # **A route has to be as unique as the operation id.** Two screens whose first three
        # tokens agree produced the same path AND the same verb, so the second overwrote the
        # first as a duplicate YAML key — the operation vanished silently while its screen was
        # still wired to it, and `check-screens` found nine of them.
        route = "/" + "-".join(seq[:3]).lower()
        if route in used_routes:
            route = "/" + "-".join(seq[:4]).lower() if len(seq) > 3 else route
        k = 2
        while route in used_routes:
            route = "/%s-%d" % ("-".join(seq[:3]).lower(), k)
            k += 1
        used_routes.add(route)
        http = "get" if verb in ("list", "get", "search", "export") else (
            "post" if verb in ("create", "submit", "record", "issue", "register") else "put")
        made.append((route, http, block(
            oid, http, "%s %s %s" % (p["code"], s["id"], s["name"]),
            s["name"][:70], (s.get("purpose") or "")[:300],
            conv_c["read"] if http == "get" else conv_c["write"],
            conv_c["scope"], PLAT_AUD.get(p.get("audience"), "staff"),
            "DraftedRecord", http == "get", (s.get("source") or {}).get("page"), module)))
        wiring.setdefault(str(r["file"]), {})[s["id"]] = (oid, contract, s["name"][:70], http)

    print("%s -> contracts/.../%s.yaml" % (module, contract))
    print("  %d screen(s) · %d operation(s) · permission %s / %s · scope %s"
          % (len(todo), len(made), conv_c["read"], conv_c["write"], conv_c["scope"]))
    for route, http, b in made[:12]:
        print("     %-4s %-34s %s" % (http.upper(), route, re.search(r"operationId: (\w+)", b).group(1)))
    if not a.apply:
        print("\n  nothing written - pass --apply")
        return 0

    add = []
    for route, http, b in made:
        add.append("  %s:\n    %s:\n%s" % (route, http, b))
    m = re.search(r"^components:$", text, re.M)
    text = text[:m.start()] + "".join(add) + text[m.start():]
    if "\n    DraftedRecord:\n" not in text:
        ms = re.search(r"^  schemas:$", text, re.M)
        cut = ms.end() + 1
        import datetime
        text = text[:cut] + "    DraftedRecord:\n%s\n" % (ENVELOPE % datetime.date.today()) + text[cut:]
    path.write_text(text, encoding="utf-8")
    yaml.safe_load(path.read_text(encoding="utf-8"))
    print("  -> %s (parses)" % path.relative_to(ROOT))

    n = 0
    for f, plan in wiring.items():
        doc = yaml.safe_load(Path(f).read_text(encoding="utf-8"))
        for s in doc["screens"]:
            if s["id"] not in plan:
                continue
            oid, c, summary, http = plan[s["id"]]
            s["apis"] = [{"operationId": oid, "contract": c, "purpose": summary,
                          "trigger": "onLoad" if http == "get" else "onAction"}]
            n += 1
        Path(f).write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
                           encoding="utf-8")
    print("  %d screen(s) wired" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
