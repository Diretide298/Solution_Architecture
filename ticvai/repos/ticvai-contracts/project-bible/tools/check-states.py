#!/usr/bin/env python3
"""
Validate state models and the event catalogue against each other and against the contracts.

These two artefacts are worth having because they check each other. Separately, each is a
document that drifts. Together they answer a question neither can alone: **does every fact the
business claims to publish actually have a publisher, and does every publisher have a
consumer?**

Checks:

  1. Every state in a model exists in the contract enum, and every enum value is modelled. A
     state in the enum and not the model is one nobody has thought about.
  2. Every state is reachable from an initial state.
  3. Every state reaches a terminal state, unless the entity has none by design.
  4. Every operation named in a transition exists in the contracts.
  5. **Every event a transition emits is in the catalogue.** This is the one that matters —
     a state model claiming to publish something nobody catalogued is a consumer waiting for a
     message that never arrives.
  6. Every catalogued event has a publisher somewhere in the state models, or says why not.
  7. Every event has at least one consumer, and every consumer declares an idempotency key.
  8. Offline-reachable states are a subset of the states the entity actually has.
  9. No contract declares the same path twice. YAML resolves duplicates silently, so the
     first block vanishes and every other check passes on what survives.
 10. A transition is not credited to a read. A GET cannot move a state; a model that says
     `listSerialisedItems` reserves an item hands the reserve to an operation nobody will build.
 11. Nothing leaves a terminal state. `_schema.yaml` defines terminal as "a state nothing
     leaves", and check 3 means nothing if a terminal state has outgoing transitions.
 12. A model's notes do not contradict its transitions ("no transition back to `draft`"
     beside a transition into `draft`).
 13. (warning) A transition's operation writes the entity's table, per the lineage; and an
     operation does not "move" a record to the state it is already in.

Run: python3 tools/check-states.py
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATES = ROOT / "states"
EVENTS = ROOT / "events"
# The shipped `contracts/` is authoritative. Until 17 August these pointed at a sibling repo
# outside the package, so every validator passed for whoever had that repo checked out and read
# nothing for anyone working from the zip — which is the worst failure a checker can have, because
# it is silent and it looks like success.
CONTRACTS = ROOT / "contracts"
if not CONTRACTS.exists():
    CONTRACTS = ROOT.parent / "ticvai" / "ticvai-contracts" / "openapi"

ERRORS: list[str] = []
# "No transition back to `draft`", "no way back into `open`" -- a note that forbids a move.
NO_TRANSITION_NOTE = re.compile(
    r"no (?:transitions?|way|path|moves?) (?:back )?(?:to|into) `?(\w+)`?", re.I)
WARNINGS: list[str] = []


def check_duplicate_paths() -> None:
    """Duplicate path keys are silent in YAML — the last one wins and the first vanishes.

    Found on 14 August: `/reservations` appeared twice in orders.yaml, and `createReservation`
    had been silently absent for as long as the file existed. Every other check passed on the
    surviving half, because there was nothing left to be inconsistent with.
    """
    import re as _re
    for f in list((CONTRACTS / "spine").glob("*.yaml")) + list((CONTRACTS / "satellite").glob("*.yaml")):
        seen: set[str] = set()
        for m in _re.finditer(r"^  (/[^\s:]*):\s*$", f.read_text(encoding="utf-8"), _re.M):
            if m.group(1) in seen:
                ERRORS.append(f"{f.name}: path '{m.group(1)}' declared twice — YAML keeps the "
                              "last and drops the first, silently")
            seen.add(m.group(1))


OP_VERBS: dict[str, str] = {}


def load_contracts() -> tuple[dict[str, list[str]], set[str], dict[str, set[str]]]:
    """Status enums by contract.SchemaName, every operationId, and object schemas by contract.

    Also fills OP_VERBS (operationId -> HTTP verb), which check 10 needs.
    """
    enums: dict[str, list[str]] = {}
    object_schemas: dict[str, set[str]] = {}
    ops: set[str] = set()
    if not CONTRACTS.exists():
        return enums, ops, object_schemas
    for f in list((CONTRACTS / "spine").glob("*.yaml")) + list((CONTRACTS / "satellite").glob("*.yaml")):
        doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        ctx = f.stem
        for name, sch in ((doc.get("components") or {}).get("schemas") or {}).items():
            if not isinstance(sch, dict):
                continue
            if sch.get("type") == "string" and "enum" in sch:
                enums[f"{ctx}.{name}"] = sch["enum"]
            elif isinstance(sch, dict) and sch.get("type") == "object":
                object_schemas.setdefault(ctx, set()).add(name)
            # A lifecycle declared inline on a property rather than as a named enum. Thirty-one
            # of these existed on 17 August and the checker had never seen one, because it only
            # looked for schemas called *Status. `Payment.status` and `Refund.status` are two of
            # them — an object's lifecycle is a lifecycle wherever it is written down.
            for pname, prop in (sch.get("properties") or {}).items():
                if (isinstance(prop, dict) and "enum" in prop
                        and pname.lower() in ("status", "state")):
                    enums[f"{ctx}.{name}.{pname}"] = prop["enum"]
        for item in (doc.get("paths") or {}).values():
            if isinstance(item, dict):
                for verb, op in item.items():
                    if verb in ("get", "post", "put", "patch", "delete") and isinstance(op, dict):
                        if oid := op.get("operationId"):
                            ops.add(oid)
                            OP_VERBS[oid] = verb
    return enums, ops, object_schemas


def main() -> int:
    check_duplicate_paths()
    enums, ops, object_schemas = load_contracts()
    state_files = sorted(f for f in STATES.glob("*.yaml") if f.name != "_schema.yaml")
    event_files = sorted(f for f in EVENTS.glob("*.yaml") if f.name != "_schema.yaml")

    catalogued = {}
    for f in event_files:
        e = yaml.safe_load(f.read_text(encoding="utf-8"))
        catalogued[e["name"]] = e

    emitted: dict[str, list[str]] = {}
    print(f"checking {len(state_files)} state model(s) and {len(event_files)} event(s)")
    print(f"  against {len(enums)} contract enums and {len(ops)} operations\n")

    modelled = {f"{d['contract']}.{d['enum']}"
                for d in (yaml.safe_load(f.read_text(encoding="utf-8")) for f in state_files)}
    for key, values in sorted(enums.items()):
        if key in modelled or key.count(".") < 2:
            continue
        WARNINGS.append(f"{key} is a lifecycle with {len(values)} states and no state model")

    for f in state_files:
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        name = f.name
        key = f"{d['contract']}.{d['enum']}"
        states = {t["from"] for t in d["transitions"]} | {t["to"] for t in d["transitions"]}
        states |= set(d["initial"]) | set(d["terminal"])

        # 1. against the contract enum
        if key in enums:
            declared = set(enums[key])
            for s in sorted(declared - states):
                ERRORS.append(f"{name}: '{s}' is in the contract enum and not in the model — "
                              "a state nobody has thought about")
            for s in sorted(states - declared):
                ERRORS.append(f"{name}: '{s}' is in the model and not in the contract enum")
        else:
            # An anchor that does not resolve is an error, and `openQuestions` used to downgrade
            # it to a warning — so a model could excuse its own broken anchor by declaring an
            # open question about something else. `states/entitlement.yaml` did exactly that for
            # a day: it anchored on `access.TicketStatus`, which is an object with no values, and
            # the warning read as a known exception rather than the defect it was.
            hint = ""
            if key.split(".", 1)[-1] in object_schemas.get(d["contract"], set()):
                hint = (" — that schema exists and is an object, not an enum, so these states are "
                        "checked against nothing")
            ERRORS.append(f"{name}: enum {key} not found in the contracts{hint}")

        # 2. reachability
        reachable = set(d["initial"])
        changed = True
        while changed:
            changed = False
            for t in d["transitions"]:
                if t["from"] in reachable and t["to"] not in reachable:
                    reachable.add(t["to"])
                    changed = True
        for s in sorted(states - reachable):
            ERRORS.append(f"{name}: '{s}' is unreachable from any initial state")

        # 3. every state reaches a terminal one
        if d["terminal"]:
            back = set(d["terminal"])
            changed = True
            while changed:
                changed = False
                for t in d["transitions"]:
                    if t["to"] in back and t["from"] not in back:
                        back.add(t["from"])
                        changed = True
            for s in sorted(states - back):
                ERRORS.append(f"{name}: '{s}' cannot reach a terminal state — it traps records")

        # 4. operations exist
        for t in d["transitions"]:
            if (o := t.get("operation")) and ops and o not in ops:
                ERRORS.append(f"{name}: transition {t['from']}->{t['to']} names unknown operation '{o}'")

        # 10. a read does not move a state. The audit of 26 September found listSerialisedItems
        # credited with reserve, release, restock and writeOff, listCustomDomains with expiry and
        # getPaymentLink with expiry -- check 4 passed every one, because each operation exists.
        for t in d["transitions"]:
            o = t.get("operation")
            if o and OP_VERBS.get(o) == "get":
                ERRORS.append(f"{name}: transition {t['from']}->{t['to']} is credited to '{o}', "
                              "which is a GET -- a read cannot move a state. Name the operation "
                              "that writes it, or drop `operation` and mark the trigger timer/job")

        # 11. nothing leaves a terminal state. Journal posted->reversed, work-order verified->closed,
        # guest-device failed->active and period closed->closing all passed check 3, because a
        # terminal state that is left again still counts as "reached".
        terminal = set(d["terminal"])
        for t in d["transitions"]:
            if t["from"] in terminal:
                ERRORS.append(f"{name}: '{t['from']}' is declared terminal but transitions to "
                              f"'{t['to']}' via {t.get('operation') or t.get('trigger') or '?'} -- "
                              "either the state is not terminal or the transition is not real")

        # 12. notes that contradict the transitions. journal.yaml said "no transition back to
        # `draft`" above a rejectJournal transition pendingApproval->draft.
        notes = d.get("notes") or ""
        if isinstance(notes, str):
            for m in NO_TRANSITION_NOTE.finditer(notes):
                target = m.group(1)
                into = [t for t in d["transitions"] if t["to"] == target]
                if target in states and into:
                    ops_into = ", ".join(sorted({t.get("operation") or t.get("trigger") or "?"
                                                 for t in into}))
                    ERRORS.append(f"{name}: notes say '{m.group(0)}' but the model declares "
                                  f"{len(into)} transition(s) into '{target}' ({ops_into})")

        # 13a. an operation that "moves" a record to where it already is
        for t in d["transitions"]:
            if t["from"] == t["to"] and t.get("operation"):
                WARNINGS.append(f"{name}: {t['from']}->{t['to']} via {t['operation']} changes no "
                                "state -- if the operation moves the record, name the state it "
                                "moves to; if it does not, it is not a transition")

        # 5. emitted events are catalogued
        for t in d["transitions"]:
            for e in (t.get("emits") or []):
                emitted.setdefault(e, []).append(d["entity"])
                if e not in catalogued:
                    ERRORS.append(f"{name}: emits '{e}', which is not in the event catalogue — "
                                  "a consumer would wait for a message nobody publishes")

        # 8. offline states exist
        for s in d.get("offlineReachable", []) or []:
            if s not in states:
                ERRORS.append(f"{name}: offlineReachable names '{s}', which is not a state")

        print(f"  {d['entity']:22}{len(states):>3} states, {len(d['transitions']):>3} transitions")

    print()
    for n, e in sorted(catalogued.items()):
        # 6. someone publishes it
        if n not in emitted and "No state model emits this" not in e.get("notes", ""):
            WARNINGS.append(f"{n}: no state model emits this. Either the model is missing, or "
                            "the event is speculative")
        # 7. consumers and idempotency
        if not e.get("consumers"):
            ERRORS.append(f"{n}: no consumers. An event nobody consumes is a write nobody reads")
        for c in e.get("consumers", []):
            if not c.get("idempotencyKey"):
                ERRORS.append(f"{n}: consumer '{c['context']}' declares no idempotency key — "
                              "at-least-once delivery makes that a bug waiting for a Saturday")
        crit = sum(1 for c in e.get("consumers", []) if c.get("isCritical"))
        print(f"  {n:26}{len(e['consumers'])} consumers, {crit} critical")

    print()
    # **ADR-0033: a state change that must reach anything outside its own transaction writes an
    # outbox row in that transaction.** The ADR was written on 31 August and the lineage still had
    # one operation writing `platform.outbox` against thirty declared events — **the decision was
    # recorded and nothing enforced it**, which is how an ADR becomes a document nobody follows.
    #
    # **Not a queue write inside a transaction.** A broker acknowledging a publish that then rolls
    # back is the exactly-once problem restated; the row and the state change commit together or
    # neither does.
    _lin_path = ROOT / "handoff" / "api-data-lineage.json"
    if _lin_path.exists():
        _lin = json.loads(_lin_path.read_text(encoding="utf-8"))
        for f in sorted(STATES.glob("*.yaml")):
            if f.stem.startswith("_"):
                continue
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            for tr in (doc.get("transitions") or []):
                ev = tr.get("emits") or tr.get("emit")
                op = tr.get("operation")
                if not ev or not op or op not in _lin:
                    continue
                if "platform.outbox" not in (_lin[op].get("writes") or []):
                    WARNINGS.append(
                        f"{f.stem}: {tr.get('from')}->{tr.get('to')} emits {ev} but {op} does not "
                        "write platform.outbox — the event and the state change must commit "
                        "together (ADR-0033)")

        # 13b. the operation on a transition writes the entity's table. A transition credited to an
        # operation whose lineage never touches the record (suspendShift moving a deposit box,
        # revokeApprovalDelegation withdrawing a shift swap) is a transition nobody implements.
        # Only checked where the table named after the model file is a real table in the lineage,
        # so a model whose table has a different name is not flagged on a guess.
        _by_name: dict[str, set[str]] = {}
        for _v in _lin.values():
            for _w in (_v.get("writes") or []) + (_v.get("reads") or []):
                if isinstance(_w, str) and "." in _w and not _w.startswith("cache:"):
                    _by_name.setdefault(_w.split(".", 1)[1], set()).add(_w)
        for f in sorted(STATES.glob("*.yaml")):
            if f.stem.startswith("_"):
                continue
            doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            owned = _by_name.get(f.stem.replace("-", "_"))
            if not owned:
                continue
            for tr in (doc.get("transitions") or []):
                op = tr.get("operation")
                if not op or op not in _lin or OP_VERBS.get(op) == "get":
                    continue
                writes = _lin[op].get("writes") or []
                # pos_shift for shift, fiscal_period for period: a table that carries the stem
                # counts, so only an operation that touches no such table is reported.
                stem = f.stem.replace("-", "_")
                if not owned & set(writes) and not any(stem in w for w in writes):
                    WARNINGS.append(
                        f"{f.stem}: {tr.get('from')}->{tr.get('to')} is credited to {op}, whose "
                        f"lineage writes {sorted(writes) or 'nothing'} and not "
                        f"{'/'.join(sorted(owned))} -- either the operation is wrong or its "
                        "writes are")

    for w in WARNINGS:
        print(f"  WARN  {w}")
    for x in ERRORS:
        print(f"  FAIL  {x}")
    print()
    if ERRORS:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1
    print(f"PASS — {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
