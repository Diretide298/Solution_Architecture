# -*- coding: utf-8 -*-
"""The declared background work: every timer, queued job and event consumer, as the contracts declare it (r13).

**Why** (2 November 2026, the r13 job scan; CHG-R13JOB-001). The plan made a task for each contract operation only.
148 state models moved on a timer or a job that named no operation, and of 266 event consumers 10 had an operation:
no task built the rest, and SETUP-HOSTS said only that the workers host runs "every module's consumers". So each
owning contract now declares its background work in a top-level `x-ticvai-jobs:` map, beside `x-ticvai-queries:`
(the same shape of a top-level declaration, ADR-0055 amendment of 14 October):

    <name>:
      module:   the contract's module (its file stem)
      host:     workers (ADR-0055: every module's event consumers and scheduled jobs) or ticvai-ai (ADR-0020)
      trigger:  {kind: timer | queue | event | state, every: <ISO-8601 duration, where the text gives one>, on: <state>}
      context:  the consumer context in events/, where it is not the module's own (ai's `cache`)
      consumes: the events whose consumer of this module it is (events/<event>.yaml `consumers`)
      moves:    [{model, from, to}] the job and timer transitions it makes (states/<model>.yaml, no `operation`)
      reads, writes: the tables, the module's own (ADR-0055 rule 3: another module's rows are written by its owner)
      emits:    the events it writes to the outbox
      reliesOn: the operations that hand it work, where no state model or event says so
      builtBy:  the task key or ticket (#nnnnn) that builds it, where that is not its own plan task
      for, source

A consumer with an `operation` in events/ stays an operation (SD-026) and is built by that operation's task.

Shared by tools/build-service-docs.py (one plan task per declared job: key, block, owner, waits) and
tools/check-jobs.py (what is declared, and that a task builds it). No main.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {"workers", "ticvai-ai"}
KINDS = {"timer", "queue", "event", "state"}
DURATION = re.compile(r"^P(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$")
# the consumer context in events/ of each contract's module, where the two names differ
CONTEXT_OF = {"marketing-crm": "marketing", "finance": "ledger"}
# consumer contexts that are server modules, by the contract that owns them (`cache` is AI's answer cache, ADR-0034;
# `platform` on sync.rejectionRaised raises BO-133 Offline Alerts, a reporting screen). Any other context (a client
# app such as `guest-app`) is not a server consumer and is reported, never planned.
CONTEXT_CONTRACT = {"marketing": "marketing-crm", "ledger": "finance", "cache": "ai", "platform": "reporting"}


def contract_files(root: Path = ROOT) -> dict:
    return {p.stem: p for p in sorted((root / "contracts").glob("*/*.yaml")) if p.parent.name != "shared"}


def context_of(contract: str) -> str:
    return CONTEXT_OF.get(contract, contract)


def contract_of_context(ctx: str, contracts) -> str | None:
    c = CONTEXT_CONTRACT.get(ctx, ctx)
    return c if c in contracts else None


def kebab(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name).upper()


def key_of(contract: str, name: str, decl: dict) -> str:
    """The plan task key: CONS-<CONTRACT>-<NAME> for an event consumer, JOB-<CONTRACT>-<NAME> otherwise."""
    pre = "CONS" if (decl.get("trigger") or {}).get("kind") == "event" else "JOB"
    return f"{pre}-{contract.upper()}-{kebab(name)}"


def load(root: Path = ROOT, docs: dict | None = None) -> dict:
    """{'<contract>#<name>': decl + contract, name, key, file} over every contract's x-ticvai-jobs."""
    out = {}
    for c, p in contract_files(root).items():
        d = docs[c] if docs is not None and c in docs else (
            yaml.safe_load(p.read_text(encoding="utf-8")) if docs is None else None)
        if not isinstance(d, dict):
            continue
        for n, j in (d.get("x-ticvai-jobs") or {}).items():
            if isinstance(j, dict):
                out[f"{c}#{n}"] = dict(j, contract=c, name=n, key=key_of(c, n, j),
                                       file=p.relative_to(root).as_posix() if p.is_relative_to(root) else str(p))
    return out


def load_states(root: Path = ROOT) -> dict:
    return {p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted((root / "states").glob("*.yaml"))
            if p.stem != "_schema"}


def load_events(root: Path = ROOT) -> dict:
    out = {}
    for p in sorted((root / "events").glob("*.yaml")):
        if p.stem == "_schema":
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("name"):
            out[d["name"]] = dict(d, _file=p.relative_to(root).as_posix())
    return out


def is_job_move(t: dict) -> bool:
    """A transition a job or timer makes: no operation causes it."""
    return not t.get("operation") and t.get("trigger") in ("timer", "job")


def relies_on(job: dict, states: dict, events: dict) -> set:
    """The operations that hand a job its work: those it names (`reliesOn`), the emitters of the events it consumes,
    and the operations that move the state models it moves (they create and advance the rows it acts on)."""
    out = set(job.get("reliesOn") or [])
    for e in job.get("consumes") or []:
        out |= {str(o).split(".")[-1] for o in (events.get(e) or {}).get("emittedBy") or []}
    for m in {mv.get("model") for mv in job.get("moves") or []}:
        out |= {t["operation"] for t in (states.get(m) or {}).get("transitions") or [] if t.get("operation")}
    return out


def points_raw(job: dict) -> float:
    """Its size on the operations' scale (build-service-docs op_raw): a base of one, half a point a table written, a
    fifth a state move (up to 20), three tenths an event consumed (up to 10), one for a clock."""
    trig = job.get("trigger") or {}
    return (1 + 0.5 * len(job.get("writes") or []) + 0.2 * min(len(job.get("moves") or []), 20)
            + 0.3 * min(len(job.get("consumes") or []), 10) + (1 if trig.get("kind") == "timer" else 0))
