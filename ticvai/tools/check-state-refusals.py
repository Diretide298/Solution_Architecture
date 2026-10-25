#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An operation's wrong-state refusals agree with the state model that names it (r10, CHG-R10GEN-005).

**What it found.** `check-states` checks that the operations a state model names exist, that a GET moves nothing and
that nothing leaves a terminal state. It never read what the operation itself says about states, so the two could
describe different actions and both pass. ADAM CR-237 (23 October 2026, #33058): overrideWaitingGuest refuses only a
`redeemed`, `cancelled` or `released` entry, so its text lets an `expired` or `noShow` entry be overridden, while
states/queue-entry.yaml gives it exactly two moves, both from `called`, and makes `expired` and `noShow` terminal. The
build could not tell which states the operation acts from, nor what an admitted party's entry ends in. The other
r9 members of the class are the same shape: a refusal list that covers some of the states the model never moves the
operation from and leaves others unanswered, or a 409 that names as allowed a state the model has no move from.

**What is compared.** For every state model (`states/*.yaml`) and every operation its transitions name, the states
the model lets the operation move from (`from` of its transitions) against what the operation's 409 says:

  * refused states: a state written in backticks in the 409's description (`redeemed`), "already <state>", or a
    problem type `<...>-already-<state>`;
  * allowed states: the states a 409 names after "not", "only", "unless", "other than" or "must be" ("is not
    `sending` or `paused`", "only a `draft`"), or a problem type `<...>-not-<state>`.

A model is compared only when every state the 409 names in backticks is one of its states, so an operation named
in two models (decideApprovalRequest, createOrder) is judged against the entity its 409 is about.

Rules:

    SR-REFUSES-ALLOWED      the 409 refuses a state the model moves the operation from
    SR-ALLOWS-NO-MOVE       the 409 names as allowed a state the model has no move from for the operation, or the
                            model moves it from a state the 409's allowed list leaves out
    SR-TERMINAL-UNANSWERED  the 409 refuses some terminal states and leaves another terminal state of the model
                            with neither a move nor a refusal: the text lets the operation act on a state nothing
                            leaves (overrideWaitingGuest's `expired` and `noShow`, CR-237)

Each finding needs a ruling (which of the two is right); `--all` prints every one. No baseline: the class arrived
in r10, and its findings are fixed in r10 (the lead's rule for a new check).

    python tools/check-state-refusals.py [--all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import audit_guard as g  # noqa: E402

RULES = {
    "SR-REFUSES-ALLOWED": "a 409 refuses a state the state model moves the operation from (CR-237, CHG-R10GEN-005)",
    "SR-ALLOWS-NO-MOVE": "a 409's allowed states differ from the states the model moves the operation from "
                         "(CHG-R10GEN-005)",
    "SR-TERMINAL-UNANSWERED": "a 409 refuses some terminal states and leaves another with neither a move nor a "
                              "refusal (overrideWaitingGuest, CR-237; CHG-R10GEN-005)",
}
STATES = g.ROOT / "states"
TICK = re.compile(r"`([A-Za-z][A-Za-z0-9]*)`")
_ST = r"`[A-Za-z][A-Za-z0-9]*`"
_LIST = r"(" + _ST + r"(?:\s*(?:,\s*(?:or\s+|and\s+|nor\s+)?|or\s+|and\s+|nor\s+|/\s*)" + _ST + r")*)"
# A marker that turns the states listed right after it into the ones the operation is allowed from: "is not
# `sending` or `paused`", "no longer `open`", "only a `draft`", "neither `open`, `suspended` nor `pendingVariance`".
ALLOW_LIST = re.compile(
    r"\b(?:not|no longer|only|unless|other than|must be|except|neither)\s+"
    r"(?:(?:be|in|a|an|the|from|when|while|yet|its|been|currently|status|state|one|of|still)\s+)*" + _LIST, re.I)
# A refusal names the state the record is in: "is `x`", "was `x`", "already `x`", "where the order is `x`". A list
# followed by "and", "with", "while" or "but" is a condition on more than the state ("is `published` and the body
# changes"), not a refusal of the state.
REFUSE_LIST = re.compile(
    r"\b(?:is|was|are|were|already|still|been|in)\s+(?:(?:a|an|the|now|already|fully|being|still)\s+)*" + _LIST
    + r"(?!\s*(?:and|with|while|but)\b)", re.I)
# "already redeemed" in plain words: an ended state the 409 answers.
ALREADY = re.compile(r"\balready\s+(?:fully\s+|been\s+)?`?([A-Za-z][A-Za-z0-9]*)`?", re.I)
# Words that answer every terminal state at once ("the case already has an outcome", "already decided").
ENDED = re.compile(r"\balready\s+(?:has\s+an\s+outcome|decided|ended|finished|closed|terminal|complete[d]?|final)\b|"
                   r"\b(?:is|was)\s+(?:closed|finished|ended|final|terminal)\b|\bno longer open\b", re.I)
# The transitions a state model credits to an operation that it does not make from the record it was called on: a
# trigger other than the call, or the older record a new version supersedes.
NOT_THE_CALL = {"cascade", "supersede", "job", "timer", "system", "externalEvent", "time"}


def kebab(s: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r"-\1", s).lower()


def load_models() -> list:
    """[(file name, model)] for every state model."""
    out = []
    for f in sorted(STATES.glob("*.yaml")):
        if f.name == "_schema.yaml":
            continue
        m = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if isinstance(m, dict):
            out.append((f.name, m))
    return out


def model_states(m: dict) -> set:
    tr = [t for t in m.get("transitions") or [] if isinstance(t, dict)]
    return ({str(s) for s in m.get("initial") or []} | {str(s) for s in m.get("terminal") or []}
            | {str(t.get("from")) for t in tr} | {str(t.get("to")) for t in tr}) - {"None"}


def moves_from(m: dict) -> dict:
    """operationId -> {(from, to)}: the moves the model credits to the call itself."""
    out: dict = {}
    for t in m.get("transitions") or []:
        if not isinstance(t, dict) or not t.get("operation"):
            continue
        if str(t.get("trigger") or "operation") in NOT_THE_CALL or str(t.get("to")) == "superseded":
            continue
        out.setdefault(str(t["operation"]), set()).add((str(t.get("from")), str(t.get("to"))))
    return out


def read_409(text: str, types: list, states: set) -> dict:
    """What a 409 says about the states of `states`:
    `refused`  states it refuses in words (backticked, after "is", "was", "already" ...);
    `already`  those of them it refuses as "already `x`" (the state the call would move the record into);
    `said`     those, plus "already <state>" in plain words and a problem type `...-already-<state>`;
    `covered`  every state it answers at all: also any backticked state, or a state in plain words;
    `ended`    whether it answers every ended state at once ("already decided", "already has an outcome");
    `allowed`  states it names as the ones the operation is allowed from (text only: problem type names are looser);
    `named`    every backticked word, to tell which model the 409 is about."""
    named = {m.group(1) for m in TICK.finditer(text)}
    allowed, spans = set(), []
    for m in ALLOW_LIST.finditer(text):
        allowed |= {s for s in TICK.findall(m.group(1)) if s in states}
        spans.append(m.span(1))
    refused, already = set(), set()
    for m in REFUSE_LIST.finditer(text):
        if any(a <= m.start(1) < b for a, b in spans):
            continue
        got = {s for s in TICK.findall(m.group(1)) if s in states}
        refused |= got
        if re.search(r"already\s+(?:\w+\s+)*$", text[m.start():m.start(1)], re.I):
            already |= got
    said = set(refused)          # refused in so many words: the evidence that the 409 lists ended states
    low = {s.lower(): s for s in states}
    for m in ALREADY.finditer(text):
        if m.group(1).lower() in low:
            said.add(low[m.group(1).lower()])
    for ty in types:
        for s in states:
            if re.search(r"(?:^|-)already-" + re.escape(kebab(s)) + r"$", ty):
                said.add(s)
    # answered at all: also any backticked state ("`refusedReason` says which: `withdrawn`, `expired`") and a
    # state in plain words ("Hold expired, already captured")
    covered = said | (named & states)
    for s in states:
        if len(s) > 3 and re.search(r"(?<![`\w])" + re.escape(s) + r"(?![`\w])", text, re.I):
            covered.add(s)
    refused -= allowed
    return {"refused": refused, "already": already & refused, "said": said - allowed, "covered": covered - allowed,
            "allowed": allowed, "named": named, "ended": bool(ENDED.search(text))}


def conflict_409(op: dict, doc: dict) -> tuple:
    """(description, problem types) of the operation's 409, through a local or shared $ref."""
    r = (op.get("responses") or {}).get("409")
    seen = 0
    while isinstance(r, dict) and "$ref" in r and seen < 5:
        seen += 1
        fp, _, frag = r["$ref"].partition("#")
        cur = doc
        if fp:
            stem = fp.rsplit("/", 1)[-1].removesuffix(".yaml")
            cur = next((d for s, _, d in g.contracts() if s == stem), {})
        for p in [p for p in frag.split("/") if p]:
            cur = cur.get(p) if isinstance(cur, dict) else None
        r = cur
    if not isinstance(r, dict):
        return None, []
    return str(r.get("description") or ""), [str(t) for t in r.get("x-ticvai-problem-types") or []]


def judge(model_file: str, m: dict, op_id: str, frm: set, into: set, text: str, types: list) -> list:
    """[(rule, key, message)] for one operation in one model. `frm`: the states the model moves it from by the
    call; `into`: the states those moves end in."""
    states = model_states(m)
    r = read_409(text, types, states)
    refused, allowed = r["refused"], r["allowed"]
    # the 409 is about this model's entity only when every state word it backticks is one of its states
    if (not r["covered"] and not allowed) or (r["named"] & ALL_STATES) - states:
        return []
    term = {str(s) for s in m.get("terminal") or []}
    ent = m.get("entity") or model_file
    out = []
    key = f"{model_file[:-5]}:{op_id}"
    # "already `active`" where the call moves records into `active` refuses the repeat of that move, not the other
    # moves the model credits to the same call from `active` (activateJourney pausing an active journey)
    bad = sorted((refused - (r["already"] & into)) & frm)
    if bad:
        out.append(("SR-REFUSES-ALLOWED", key,
                    f"{op_id}: its 409 refuses {', '.join(bad)}, and states/{model_file} moves it from "
                    f"{', '.join(sorted(frm))} ({ent})"))
    if allowed and allowed != frm:
        extra, missing = sorted(allowed - frm), sorted(frm - allowed)
        parts = []
        if extra:
            parts.append(f"its 409 allows {', '.join(extra)}, which states/{model_file} has no move from")
        if missing:
            parts.append(f"states/{model_file} moves it from {', '.join(missing)}, which its 409 refuses")
        out.append(("SR-ALLOWS-NO-MOVE", key, f"{op_id}: " + "; ".join(parts) + f" ({ent}; moves from "
                    f"{', '.join(sorted(frm))})"))
    if r["said"] & term and not allowed and not r["ended"]:
        open_ = sorted(term - r["covered"] - frm)
        if open_:
            rest = sorted(states - r["covered"] - frm - term)
            out.append(("SR-TERMINAL-UNANSWERED", key,
                        f"{op_id}: its 409 refuses {', '.join(sorted(r['covered']))} only, so it acts on "
                        f"{', '.join(open_)}, which states/{model_file} makes terminal; the model moves it from "
                        f"{', '.join(sorted(frm))} only" + (f" (no answer either for {', '.join(rest)})"
                                                             if rest else "") + f" ({ent})"))
    return out


ALL_STATES: set = set()


def findings() -> list:
    """[(rule, key, message)] over the package."""
    models = load_models()
    ALL_STATES.clear()
    for _, m in models:
        ALL_STATES.update(model_states(m))
    ops = g.operations()
    docs = {s: d for s, _, d in g.contracts()}
    out = []
    for name, m in models:
        for op_id, moves in sorted(moves_from(m).items()):
            f = ops.get(op_id)
            if not f:
                continue
            text, types = conflict_409(f["op"], docs[f["contract"]])
            if text is None:
                continue
            out += judge(name, m, op_id, {a for a, _ in moves}, {b for _, b in moves}, text, types)
    return out


def main() -> int:
    g.force_utf8()
    guard = g.Guard("check-state-refusals", RULES)
    found = findings()
    for rule, key, msg in found:
        guard.add(rule, key, msg)
    guard.note(f"{len(load_models())} state model(s) read; {len(found)} disagreement(s)")
    return guard.finish()


if __name__ == "__main__":
    sys.exit(main())
