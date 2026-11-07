"""The change-request watcher's decision API: ADAM on the phone (viewer/PHONE-SPEC.md section 2, 4 November 2026).

The watcher (ticvai/tools/cr-watch.py) runs on the server as a PM2 job, drafts an answer to every new change request
and lists them in its REVIEW.md. These routes let the lead do from a page what they do in that file by hand: read a
draft, ask about it, mark it approve, change or reject, and settle what they marked after seeing the dry run.

**The watcher's folder stays the record.** Nothing here keeps its own copy of what is waiting or how it was marked:
every route reads CR_WATCH_OUT (state.json, drafts/, REVIEW.md), every decision is written into REVIEW.md with the
watcher's own mark_review under its review lock, and settling is the watcher's own `settle` step run as a subprocess.
The REVIEW.md format is cr-watch.py's alone; this file imports it rather than restating it.

The safety rules carried over (PHONE-SPEC.md, "Safety rules"):

- a decision binds to the draft hash it was made on and to the mark it was made over (`expected_mark`, the request's
  mark_digest): a moved draft or a newer mark answers 409 and nothing is written;
- nothing reaches ADAM or a ticket before the lead presses Settle, and Settle applies only the marks the preview
  showed (the fingerprint; 409 otherwise); OpenProject mail stays off (settle_changes.py without --notify); one
  settle at a time;
- the ask-back turn is cr-watch.py's: read-only tools inside the release worktree, no credential in its environment;
- only the System Architect decides (security.DECIDERS, the owner alone since 6 November 2026: "the decide page
  only I can see it, no one else"); a phone's device token reads the summary's counts and nothing else, only its hash is stored, and it ends after DEVICE_DAYS, after DEVICE_IDLE_DAYS unused, and whenever
  its account's sessions are ended (sign out everywhere, a password change or reset, deactivation).

What ADAM adds is the audit trail (`watcher_event`), the ask-back thread (`watcher_thread`) and the device tokens
(`watcher_device`), in its own database. Asking for a failed draft to be drafted again (`redraft`) starts no Claude
turn: it resets the request in state.json under the review lock with the watcher's own `redraft`, and the next
hourly run drafts it.

Environment: CR_WATCH_OUT (the watcher's folder; unset, every route answers 503), CR_WATCH_SCRIPT (cr-watch.py,
default the one in this repository), CR_WATCH_ENV_FILE (the watcher's credentials for settling and asking, default
/etc/ticvai/cr-watch.env when it exists), CR_WATCH_CLAUDE (the claude command, default found on PATH),
CR_WATCH_PREVIEW_EVERY (seconds between one account's settle previews, default 10; the checks shorten it),
CR_WATCH_RUN_MINUTE (the minute past each hour the watcher's job starts, default 7: deploy.sh's cron_restart).
"""
from __future__ import annotations

import base64
import datetime as _dt
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from . import db, security

router = APIRouter(prefix="/api/watcher", tags=["watcher"])

DEFAULT_SCRIPT = Path(__file__).resolve().parents[2] / "ticvai" / "tools" / "cr-watch.py"
DEFAULT_ENV_FILE = Path("/etc/ticvai/cr-watch.env")
REF = re.compile(r"^CR-[0-9]{1,6}$")
FINGERPRINT = re.compile(r"^[0-9a-f]{32}$")
SETTLE_REF = re.compile(r"^[A-Za-z0-9._-]{0,40}$")
PREVIEW_SECONDS = 5 * 60
APPLY_SECONDS = 20 * 60
ASK_STALE_MINUTES = 20               # an ask still "asking" after this never came back (the service restarted)
MAX_LINES, MAX_LINE = 400, 500       # what a settle's printed lines are cut to
ASK_SLOTS = threading.BoundedSemaphore(2)
ASKS_PER_HOUR = 10                   # one account's questions (security review, L1)
PREVIEW_EVERY = 10                   # seconds between one account's settle previews (L1)
DEVICE_DAYS = 90                     # a device token's life (M3)
DEVICE_IDLE_DAYS = 30                # and how long it may go unused
DEVICE_MAX = 5                       # live tokens per account; a new one past it revokes the longest unused
REDRAFTS_PER_MINUTE = 20             # one account's Draft again presses (each a write to the watcher's state)
RUN_MINUTE = 7                       # the PM2 job's cron_restart, "7 * * * *" in the server's local time
HISTORY_MAX = 200                    # settled requests History lists at most
RUNS_SHOWN = 12                      # lines of runs.log Health shows
BODY_MAX = 64 * 1024                 # bytes a request body to these routes may carry (M6)
DRAIN_MAX = 1024 * 1024              # what of a refused body is read and dropped before the 413

NOT_SET_UP = "The watcher is not set up on this server."
BUSY = "The watcher is writing its list right now; try again in a moment."

_SETTLING = threading.Lock()         # one settle preview or apply at a time (M1)
_previews: dict = {}                 # account id -> when it last previewed
_previews_lock = threading.Lock()
_redrafts: dict = {}                 # account id -> when its recent Draft again presses were
_redrafts_lock = threading.Lock()


# ── the watcher's own code ───────────────────────────────────────────

_module = None
_module_lock = threading.Lock()


def _script() -> Path:
    return Path(os.environ.get("CR_WATCH_SCRIPT") or DEFAULT_SCRIPT)


def cw():
    """cr-watch.py as a module, loaded once. Its folder goes on sys.path only while it loads (it imports
    audit_guard beside it), so nothing in ticvai/tools can shadow a module this service imports later."""
    global _module
    with _module_lock:
        if _module is None:
            path = _script()
            saved = list(sys.path)
            try:
                spec = importlib.util.spec_from_file_location("cr_watch", str(path))
                if spec is None or spec.loader is None:
                    raise ImportError(str(path))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            except Exception:  # noqa: BLE001 - any failure to load is "not set up", never a 500
                raise HTTPException(503, NOT_SET_UP + " Its script could not be loaded.") from None
            finally:
                sys.path[:] = saved
            _module = mod
        return _module


def _out() -> Path:
    raw = os.environ.get("CR_WATCH_OUT", "").strip()
    if not raw:
        raise HTTPException(503, NOT_SET_UP)
    out = Path(raw)
    if not out.is_dir():
        raise HTTPException(503, NOT_SET_UP + " Its output folder does not exist yet.")
    return out


def _env_file() -> Optional[Path]:
    raw = os.environ.get("CR_WATCH_ENV_FILE", "").strip()
    path = Path(raw) if raw else DEFAULT_ENV_FILE
    return path if path.is_file() else None


def _state(out: Path) -> dict:
    try:
        state = cw().load_state(out)
    except (OSError, ValueError):
        raise HTTPException(503, "The watcher's state could not be read; try again in a minute.") from None
    state = state or {}
    state.setdefault("pending", {})
    return state


def _review(out: Path):
    """(the REVIEW.md text, its marks, the refs in its order)."""
    path = out / "REVIEW.md"
    try:
        text = path.read_text(encoding="utf-8") if path.exists() else ""
    except OSError:
        raise HTTPException(503, "The watcher's REVIEW.md could not be read; try again in a minute.") from None
    m = cw()
    return text, m.parse_review(text), m.BLOCK.findall(text)


def _ref(cr: str) -> str:
    ref = (cr or "").strip().upper()
    if not REF.match(ref):
        raise HTTPException(400, "That is not a change request number; one looks like CR-650.")
    return ref


def _now() -> str:
    return security.stamp()


def _parse_time(value: str) -> Optional[_dt.datetime]:
    try:
        t = _dt.datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return t if t.tzinfo else t.replace(tzinfo=_dt.timezone.utc)


# ── what no answer may carry ─────────────────────────────────────────

# Anything shaped like a credential, whoever's (security review, L3): an Anthropic key, a value after Bearer, Basic,
# token or apikey, and a long run of letters and digits with both in it (an OpenProject token is 64 hex digits). A
# 32-digit settle fingerprint and a 12-digit draft hash are shorter and stay readable.
TOKEN_SHAPED = re.compile(
    r"sk-ant-[A-Za-z0-9_\-]{8,}"
    r"|(?i:\b(?:bearer|basic|token|apikey|api_key|password)\b[\s:=]+)[A-Za-z0-9._~+/=\-]{8,}"
    r"|\b(?=[A-Za-z0-9_\-]*[0-9])(?=[A-Za-z0-9_\-]*[A-Za-z])[A-Za-z0-9_\-]{40,}\b")


def _forms(value: str) -> set:
    """`value` as a printed line could carry it: as it is, in base64 (with and without padding, standard and URL-safe)
    and URL-encoded."""
    raw = value.encode("utf-8")
    out = {value, urllib.parse.quote(value, safe=""), urllib.parse.quote_plus(value), urllib.parse.quote(value)}
    for enc in (base64.b64encode(raw).decode("ascii"), base64.urlsafe_b64encode(raw).decode("ascii")):
        out |= {enc, enc.rstrip("=")}
    return {x for x in out if len(x) >= 6}


def _hidden_values() -> List[str]:
    """The values in the watcher's env file in every form _forms knows, and the pairs that travel as one Basic
    login (ADAM's email and password, OpenProject's apikey and token), longest first."""
    path = _env_file()
    if not path:
        return []
    try:
        env = cw().read_env_file(path)
    except (OSError, ValueError):
        return []
    found = set()
    for v in env.values():
        if len(v) >= 6:
            found |= _forms(v)
    for pair in (f"{env.get('ADAM_EMAIL', '')}:{env.get('ADAM_PASSWORD', '')}",
                 f"apikey:{env.get('TICVAI_OP_TOKEN', '')}"):
        if len(pair) > 8:
            found |= _forms(pair)
    return sorted(found, key=len, reverse=True)


def _redact(text: str, hidden: Optional[List[str]] = None, shaped: bool = True) -> str:
    text = str(text or "")
    for v in (_hidden_values() if hidden is None else hidden):
        text = text.replace(v, "[hidden]")
    return TOKEN_SHAPED.sub("[hidden]", text) if shaped else text


# ── who may ──────────────────────────────────────────────────────────

def _account(request: Request) -> Optional[dict]:
    # The session rule is main.py's (current_account), looked up lazily: main imports this module.
    from . import main
    return main.current_account(request.cookies.get(main.SESSION_COOKIE))


def require_decider(request: Request) -> dict:
    """The System Architect, signed in (security.DECIDERS). Mirrors main.py's require_* guards; a device token is
    not a session. Every route here takes it, the device-token routes too: a Team Lead is refused 403."""
    account = _account(request)
    if not account:
        raise HTTPException(401, "Sign in to do that.")
    if account["role"] not in security.DECIDERS:
        raise HTTPException(403, "Only the System Architect can decide change requests.")
    return account


def _device_live(row, now: Optional[_dt.datetime] = None) -> bool:
    """A device token is live for DEVICE_DAYS from when it was made and DEVICE_IDLE_DAYS from when it was last used."""
    now = now or security.now()
    made = _parse_time(row["made_at"] or "")
    used = _parse_time(row["last_used_at"] or "") or made
    return bool(made) and now - made < _dt.timedelta(days=DEVICE_DAYS) \
        and now - used < _dt.timedelta(days=DEVICE_IDLE_DAYS)


def _device(request: Request) -> Optional[dict]:
    """The account behind `Authorization: Bearer <device token>`, or None when there is no such header. A token that
    is unknown, revoked or expired, or whose account is gone or no longer a decider, is refused."""
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    token = header[7:].strip()
    row = None
    if token and len(token) <= 200:
        row = db.one(
            """SELECT d.id, d.device, d.made_at, d.last_used_at, a.id AS account_id, a.email, a.name, a.role, a.active
                 FROM watcher_device d JOIN account a ON a.id = d.account_id
                WHERE d.token_hash = ? AND d.revoked_at IS NULL""",
            (security.token_hash(token),))
    if row and not _device_live(row):
        _revoke(db.all_rows("SELECT id, account_id, device FROM watcher_device WHERE id = ?", (row["id"],)),
                {"id": row["account_id"], "email": row["email"]}, "expired")
        raise HTTPException(401, "That device token has expired; turn notifications on again in the app.")
    if not row or not row["active"] or row["role"] not in security.DECIDERS:
        raise HTTPException(401, "That device token is not valid; turn notifications on again in the app.")
    db.change("UPDATE watcher_device SET last_used_at = ? WHERE id = ?", (_now(), row["id"]))
    return dict(row)


def _event(account: dict, kind: str, cr: str, decision: str = "", draft_hash: str = "", detail: str = "") -> None:
    db.write(
        "INSERT INTO watcher_event (account_id, who, at, kind, cr, decision, draft_hash, detail) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (account["id"], account["email"], _now(), kind, cr, decision, draft_hash, detail[:12000]))


# ── what the pages read ──────────────────────────────────────────────

_tags = {"at": 0.0, "value": ("", "")}


def _releases(state: dict) -> tuple:
    """(the release the drafts answer against, the next one): what the watcher's last run recorded, else the release
    tags of the watcher's checkout (read, never fetched), kept ten minutes."""
    if state.get("release"):
        return state["release"], state.get("next") or ""
    if time.time() - _tags["at"] > 600:
        try:
            _tags["value"] = cw().releases_from(cw()._git("tag", "--list", "r*").split())
        except (RuntimeError, OSError):
            _tags["value"] = ("", "")
        _tags["at"] = time.time()
    return _tags["value"]


def _settles_as(p: dict, rel: tuple) -> tuple:
    """(status, ref) the request is settled with if the lead approves the draft as it stands (cr-watch.py
    settle_as); empty with no draft."""
    d = p.get("draft") or {}
    if not d.get("verdict"):
        return "", ""
    return cw().settle_as(d["verdict"], rel[0], rel[1])


def _row(p: dict, mark: dict, rel: tuple, hidden: Optional[List[str]] = None) -> dict:
    m = cw()
    d = p.get("draft") or {}
    cr = p.get("cr") or {}
    settle_status, settle_ref = _settles_as(p, rel)
    return {"cr": p["ref"], "title": p.get("title") or "", "verdict": d.get("verdict") or "",
            "class": (p.get("facts") or {}).get("class_name") or d.get("class") or "",
            "blocking": p.get("blocking") == "yes", "needs": d.get("needs") or "",
            "decision": mark.get("decision") or "", "ticket": str(p.get("ticket") or ""),
            "developer": cr.get("raised by") or "", "raised_at": p.get("raised") or "",
            "settle_status": settle_status, "settle_ref": settle_ref,
            "drafted_at": p.get("drafted_at") or "", "draft_hash": m.draft_hash(d) if d else "",
            "mark_digest": m.mark_digest(mark),
            "draft_error": _redact(p.get("draft_error") or "", hidden),
            # Why it has no draft, without the watcher's "failed twice" wrapping, and whether the watcher has given up
            # on it until Draft again (MAX_TRIES).
            "draft_reason": _redact(p.get("draft_reason") or p.get("draft_error") or "", hidden),
            "draft_tries": int(p.get("draft_tries") or 0),
            "gave_up": not d and int(p.get("draft_tries") or 0) >= m.MAX_TRIES,
            "redraft_asked_at": p.get("redraft_asked_at") or ""}


def _mark(mark: dict) -> dict:
    return {"decision": mark.get("decision") or "", "note": mark.get("note") or "", "status": mark.get("status") or "",
            "ref": mark.get("ref_to") or "", "resolution": mark.get("resolution") or ""}


def _summary(out: Path, since: Optional[str], titles: bool = True) -> dict:
    m = cw()
    when = None
    if since:
        when = _parse_time(since)
        if when is None:
            raise HTTPException(400, "The since value is not a time; send one like 2026-11-04T12:00:00Z.")
    state = _state(out)
    pending = state["pending"]
    _, marks, _ = _review(out)
    drafts = [p.get("draft") or {} for p in pending.values()]
    new = []
    for p in sorted(pending.values(), key=lambda x: x.get("id") or 0):
        if when is not None:
            drafted = _parse_time(p.get("drafted_at") or "")
            if drafted is None or drafted <= when:
                continue
        # A device token reads counts only (PHONE-SPEC.md, safety rules; security review, M3): its entries keep
        # their shape for the app's background check, with the title left empty. A session reads the title.
        new.append({"cr": p["ref"], "title": (p.get("title") or "") if titles else "",
                    "blocking": p.get("blocking") == "yes",
                    "needs": (p.get("draft") or {}).get("needs") or "", "raised_at": p.get("raised") or ""})
    cap = state.get("daily_cap_usd") or m.DAILY_USD
    watching = _watching()
    running = _running(out, state) if watching else ""
    return {"waiting": len(pending),
            "blocking": sum(1 for p in pending.values() if p.get("blocking") == "yes"),
            "needs_lead": sum(1 for d in drafts if d.get("needs") == "lead"),
            "needs_client": sum(1 for d in drafts if d.get("needs") == "client"),
            "new": new,
            # With no watcher running here, what its last run said no longer stands: no error, no pause.
            "watching": watching,
            "last_run_at": state.get("last_run_at") or "",
            "last_error": _redact(state.get("last_error") or "") if watching else "",
            # While a run drafts, what the last run said no longer stands (6 November 2026: a stale "stopped at the
            # daily cap" stood all through a run); `running_since` says since when it drafts.
            "paused": "" if running or not watching else _redact(state.get("paused") or ""),
            "running_since": running,
            "spend_today_usd": round(m.spend_today(out), 2), "daily_cap_usd": float(cap),
            "decided": sum(1 for r, mk in marks.items() if r in pending and mk["decision"] in ("approve", "change")),
            # requests with no draft: none yet, or failed; they are never decided, only drafted again
            "not_drafted": sum(1 for p in pending.values() if not p.get("draft")),
            "draft_failed": sum(1 for p in pending.values() if not p.get("draft") and p.get("draft_error"))}


NOT_RUNNING = "The watcher is not running on this server"


def _watching() -> bool:
    """Whether the watcher's job runs on this server: deploy.sh starts it only with its env file, and the lead stops
    it by taking the env file away (6 November 2026: the PM2 job deleted, the env file shredded, change requests
    drafted on the lead's own machine). Its folder may still be here, read for History's sake; nothing drafts it."""
    return _env_file() is not None


def _running(out: Path, state: dict) -> str:
    """When the watcher's run now drafting started, or "": the run marks its start in state.json, and it counts
    only while the run lock is held by a live process (a run PM2 killed leaves the mark behind)."""
    since = state.get("running_since") or ""
    if not since:
        return ""
    try:
        held = (out / "cr-watch.lock").read_text(encoding="utf-8")
    except OSError:
        return ""
    m = cw()
    pid = m._lock_pid(held)
    return since if pid and m.pid_alive(pid) else ""


@router.get("/summary")
def summary(request: Request, since: Optional[str] = None):
    """The counts the inbox and the phone's background check read. A device token may read this and nothing else,
    and reads no titles."""
    device = _device(request)
    if device is None:
        require_decider(request)
    return _summary(_out(), since, titles=device is None)


@router.get("/requests")
def requests(account: dict = Depends(require_decider)):
    out = _out()
    state = _state(out)
    pending = state["pending"]
    _, marks, order = _review(out)
    refs = [r for r in order if r in pending] + sorted((r for r in pending if r not in order),
                                                     key=lambda r: pending[r].get("id") or 0)
    rel = _releases(state)
    hidden = _hidden_values()
    return {"items": [_row(pending[r], marks.get(r, {}), rel, hidden) for r in refs],
            "last_run_at": state.get("last_run_at") or ""}


def _full_answer(out: Path, ref: str) -> str:
    path = out / "drafts" / f"{ref}.md"
    try:
        text = path.read_text(encoding="utf-8") if path.exists() else ""
    except OSError:
        return ""
    head = "## The agent's answer in full"
    return text.split(head, 1)[1].strip() if head in text else ""


def _thread(ref: str) -> List[dict]:
    rows = db.all_rows("SELECT * FROM watcher_thread WHERE cr = ? ORDER BY id", (ref,))
    out = []
    stale = security.now() - _dt.timedelta(minutes=ASK_STALE_MINUTES)
    for r in rows:
        entry = _entry(r)
        if entry["state"] == "asking":
            asked = _parse_time(entry["asked_at"])
            if asked is not None and asked < stale:
                entry.update(state="failed", error="The answer never came back; ask again.")
        out.append(entry)
    return out


def _entry(r) -> dict:
    try:
        proposal = json.loads(r["proposal"]) if r["proposal"] else None
    except ValueError:
        proposal = None
    return {"id": r["id"], "question": r["question"], "asked_by": r["asked_by"], "asked_at": r["asked_at"],
            "draft_hash": r["draft_hash"], "state": r["state"], "answer": r["answer"], "proposal": proposal,
            "cost_usd": r["cost_usd"], "error": r["error"], "answered_at": r["answered_at"] or ""}


@router.get("/requests/{cr}")
def one_request(cr: str, account: dict = Depends(require_decider)):
    ref = _ref(cr)
    out = _out()
    state = _state(out)
    p = state["pending"].get(ref)
    if not p:
        raise HTTPException(404, f"{ref} is not waiting in the watcher's list.")
    _, marks, _ = _review(out)
    d = p.get("draft") or {}
    row = _row(p, marks.get(ref, {}), _releases(state))
    cr_row = p.get("cr") or {}
    row.update(
        draft={"verdict": d.get("verdict") or "", "class": d.get("class") or "", "needs": d.get("needs") or "",
               "recommendation": d.get("recommendation") or "", "resolution": d.get("resolution") or "",
               "misread": d.get("misread") or "", "question": d.get("question") or "",
               "new_ticket": d.get("new_ticket"), "facts": list(p.get("facts_lines") or []),
               "answer": _full_answer(out, ref)} if d else None,
        request={k: cr_row.get(src) or "" for k, src in (("problem", "problem"), ("evidence", "evidence"),
                                                           ("options", "options"),
                                                           ("recommendation", "recommendation"),
                                                           ("artefact", "artefact"), ("kind", "kind"))},
        facts=list(p.get("facts_lines") or []),
        mark=_mark(marks.get(ref, {})),
        thread=_thread(ref))
    return row


# ── deciding ─────────────────────────────────────────────────────────

class DecisionIn(BaseModel):
    decision: str = Field(max_length=20)
    draft_hash: str = Field(default="", max_length=64)
    # the request's mark_digest as the page read it (security review, M4)
    expected_mark: str = Field(default="", max_length=64)
    resolution: Optional[str] = Field(default=None, max_length=8000)
    status: Optional[str] = Field(default=None, max_length=20)
    ref: Optional[str] = Field(default=None, max_length=60)
    note: Optional[str] = Field(default=None, max_length=2000)


class TakeBackIn(BaseModel):
    draft_hash: str = Field(default="", max_length=64)
    expected_mark: str = Field(default="", max_length=64)


class _Conflict(Exception):
    """A 409 with a reason the page can tell apart: draft-moved, mark-moved, not-listed or not-drafted."""

    def __init__(self, detail: str, reason: str):
        super().__init__(detail)
        self.detail, self.reason = detail, reason

    def answer(self) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": self.detail, "reason": self.reason})


def _bound(ref: str, m, shown: Optional[dict], current: str, draft_hash: str, expected_mark: str) -> None:
    """The checks a decision and a take-back share, under the review lock: REVIEW.md lists the request, the draft
    is the one the page read, and so is the mark."""
    if shown is None:
        raise _Conflict(f"REVIEW.md does not list {ref} yet; wait for the watcher's next run.", "not-listed")
    if draft_hash.strip() != current or shown["draft_hash"] != current:
        raise _Conflict(f"The draft of {ref} changed since you read it; read it again and decide again.",
                        "draft-moved")
    if expected_mark.strip() != m.mark_digest(shown):
        raise _Conflict(f"{ref} was marked again after you read it (on another device, or a decision sent "
                        f"earlier); read it again and decide again.", "mark-moved")


@router.post("/requests/{cr}/decision")
def decide(cr: str, body: DecisionIn, account: dict = Depends(require_decider)):
    """approve, change or reject, written into REVIEW.md as the lead types it, bound to the draft hash and the mark
    they read. Sending the same decision again over the mark it made changes nothing and is answered as done."""
    ref = _ref(cr)
    out = _out()
    m = cw()
    decision = body.decision.strip().lower()
    if decision not in ("approve", "change", "reject"):
        raise HTTPException(400, "A decision is approve, change or reject.")
    status = ref_to = resolution = None
    if decision == "change":
        if body.status is not None and body.status.strip():
            status = body.status.strip().lower()
            if status not in m.STATUSES:
                raise HTTPException(400, f"A status is one of {', '.join(m.STATUSES)}.")
        if body.ref is not None:
            ref_to = body.ref.strip()
            if not SETTLE_REF.match(ref_to):
                raise HTTPException(400, "A ref is a release or record name like r14, with no spaces.")
        if body.resolution is not None and body.resolution.strip():
            resolution = m._clean(body.resolution)
            if len(resolution) > m.RESOLUTION_LIMIT:
                raise HTTPException(400, f"The resolution is {len(resolution):,} characters; ADAM takes at most "
                                         f"{m.RESOLUTION_LIMIT:,} here.")
    review = out / "REVIEW.md"
    try:
        with m.review_lock(out):
            state = _state(out)
            p = state["pending"].get(ref)
            if not p:
                raise HTTPException(404, f"{ref} is not waiting in the watcher's list.")
            current = m.draft_hash(p.get("draft"))
            if not current:
                # Nothing drafted (none yet, or the drafting failed): there is nothing to approve, change or reject
                # here. Draft it again (redraft); an answer in the lead's own words goes in REVIEW.md by hand.
                raise _Conflict(f"{ref} has no draft yet, so there is nothing to decide; draft it again.",
                                "not-drafted")
            text, marks, _ = _review(out)
            shown = marks.get(ref)
            if decision == "approve":
                # An approve settles the draft as drafted (security review, L6): the status, ref and resolution lines
                # go back to the draft's, as a take-back puts them, whatever an earlier change left there.
                status, ref_to = _settles_as(p, _releases(state))
                resolution = (p.get("draft") or {}).get("resolution") or ""
            if shown is not None and shown["draft_hash"] == current == body.draft_hash.strip():
                same = m.mark_review(text, ref, decision, note=body.note or "", status=status, ref_to=ref_to,
                                     resolution=resolution)
                if same == text:                          # already marked exactly so: an offline replay of itself
                    return {"cr": ref, "mark": _mark(shown), "draft_hash": current, "mark_digest": m.mark_digest(shown),
                            "unchanged": True}
            _bound(ref, m, shown, current, body.draft_hash, body.expected_mark)
            if decision == "approve" and not current:
                raise HTTPException(400, f"Nothing was drafted for {ref} to approve; change it with your own words.")
            if decision == "change" and not (resolution or shown["resolution"]):
                raise HTTPException(400, "A change needs the resolution the developer will read.")
            written = m.mark_review(text, ref, decision, note=body.note or "", status=status, ref_to=ref_to,
                                    resolution=resolution)
            got = m.parse_review(written).get(ref) or {}
            if got.get("decision") != decision or got.get("draft_hash") != current:
                raise HTTPException(500, "The decision could not be written the way REVIEW.md reads it; nothing "
                                         "was changed.")
            m._write(review, written)
    except m.Busy:
        raise HTTPException(423, BUSY) from None
    except _Conflict as c:
        return c.answer()
    _event(account, "decision", ref, decision, current, json.dumps(_mark(got), ensure_ascii=False))
    return {"cr": ref, "mark": _mark(got), "draft_hash": current, "mark_digest": m.mark_digest(got)}


@router.delete("/requests/{cr}/decision")
def take_back(cr: str, body: TakeBackIn, account: dict = Depends(require_decider)):
    """Take a mark back: REVIEW.md's decision line is emptied and the status, ref and resolution lines go back to
    what the draft would settle with, under the same lock. Bound like a decision to the draft hash and the mark the
    page read. Taking back what is not marked changes nothing."""
    ref = _ref(cr)
    if not body.draft_hash.strip():
        raise HTTPException(400, "A take-back carries the draft hash it was made on; read the request again.")
    out = _out()
    m = cw()
    review = out / "REVIEW.md"
    try:
        with m.review_lock(out):
            state = _state(out)
            p = state["pending"].get(ref)
            if not p:
                raise HTTPException(404, f"{ref} is not waiting in the watcher's list.")
            current = m.draft_hash(p.get("draft"))
            text, marks, _ = _review(out)
            shown = marks.get(ref)
            if shown is not None and not shown["decision"] and shown["draft_hash"] == current:
                return {"cr": ref, "mark": _mark(shown), "draft_hash": current, "mark_digest": m.mark_digest(shown),
                        "taken_back": False}
            _bound(ref, m, shown, current, body.draft_hash, body.expected_mark)
            status, ref_to = _settles_as(p, _releases(state))
            resolution = (p.get("draft") or {}).get("resolution") or ""
            written = m.mark_review(text, ref, "", status=status, ref_to=ref_to, resolution=resolution)
            got = m.parse_review(written).get(ref) or {}
            if got.get("decision") or got.get("draft_hash") != shown["draft_hash"]:
                raise HTTPException(500, "The mark could not be taken back the way REVIEW.md reads it; nothing "
                                         "was changed.")
            m._write(review, written)
    except m.Busy:
        raise HTTPException(423, BUSY) from None
    except _Conflict as c:
        return c.answer()
    _event(account, "take-back", ref, shown["decision"], current, json.dumps(_mark(shown), ensure_ascii=False))
    return {"cr": ref, "mark": _mark(got), "draft_hash": current, "mark_digest": m.mark_digest(got),
            "taken_back": True}


# ── drafting again ───────────────────────────────────────────────────

class RedraftIn(BaseModel):
    # POST /redraft: every request whose draft failed ("Draft all again"), or the ones named
    all_failed: bool = False
    crs: List[str] = Field(default_factory=list, max_length=200)


def _redraft_allowed(account: dict, presses: int = 1) -> None:
    """At most REDRAFTS_PER_MINUTE Draft again presses a minute per account (429): each writes the watcher's state
    under its lock, though none starts a Claude turn."""
    now = time.monotonic()
    with _redrafts_lock:
        recent = [t for t in _redrafts.get(account["id"], []) if now - t < 60]
        if len(recent) + presses > REDRAFTS_PER_MINUTE:
            _redrafts[account["id"]] = recent
            raise HTTPException(429, f"You asked for {len(recent)} drafts again in the last minute, the most there "
                                     f"can be; ask again in a minute.")
        _redrafts[account["id"]] = recent + [now] * presses


def _not_running(why: str) -> JSONResponse:
    """409 not-running: the watcher's folder is here but its job is not (no env file), so a Draft again or a question
    would wait for a turn that never comes."""
    return JSONResponse(status_code=409, content={"detail": f"{NOT_RUNNING}, {why}.", "reason": "not-running"})


def _redraft(account: dict, refs: List[str], all_failed: bool) -> dict:
    """The watcher's own redraft (cr-watch.py): under its review lock, each request's tries and failure are reset so
    the next hourly run drafts it. No Claude turn is started here. Each request reset is in the audit trail."""
    out = _out()
    m = cw()
    try:
        got = m.redraft(out, refs, all_failed=all_failed)
    except m.Busy:
        raise HTTPException(423, BUSY) from None
    except ValueError:
        raise HTTPException(503, "The watcher's state could not be read; try again in a minute.") from None
    for ref in got["redraft"]:
        _event(account, "redraft", ref, detail=json.dumps({"all_failed": all_failed}))
    return {"redraft": got["redraft"], "skipped": got["skipped"],
            "detail": (f"{len(got['redraft'])} request{'' if len(got['redraft']) == 1 else 's'} will be drafted "
                       f"again at the next hourly run." if got["redraft"] else "Nothing was asked to be drafted "
                                                                                 "again.")}


@router.post("/requests/{cr}/redraft")
def redraft_one(cr: str, account: dict = Depends(require_decider)):
    """Draft again: a request with no draft (none yet, or failed MAX_TRIES times) is drafted at the next hourly run.
    A request that has a draft, or is marked, is refused 409 with why."""
    ref = _ref(cr)
    _out()
    if not _watching():
        return _not_running("so nothing would draft it again")
    _redraft_allowed(account)
    got = _redraft(account, [ref], False)
    if not got["redraft"]:
        why = got["skipped"].get(ref) or "it cannot be drafted again"
        return JSONResponse(status_code=404 if "not waiting" in why else 409,
                            content={"detail": f"{ref} was not asked to be drafted again: {why}.",
                                     "reason": "not-redraftable"})
    return got


@router.post("/redraft")
def redraft_many(body: RedraftIn, account: dict = Depends(require_decider)):
    """Draft all again: every request whose draft failed (all_failed), or the ones named in crs."""
    refs = [_ref(c) for c in body.crs]
    if not body.all_failed and not refs:
        raise HTTPException(400, "Name the requests to draft again, or ask for every failed one.")
    _out()
    if not _watching():
        return _not_running("so nothing would draft them again")
    _redraft_allowed(account)
    return _redraft(account, refs, body.all_failed)


# ── what was settled, and how the watcher is ─────────────────────────

@router.get("/history")
def history(limit: int = 100, account: dict = Depends(require_decider)):
    """The requests settled from Decide, newest first, from the audit trail: what was decided, when, by whom, the
    ticket it told and what it posted there. A settle that failed part way is listed too, marked failed."""
    limit = max(1, min(int(limit), HISTORY_MAX))
    rows = db.all_rows("SELECT id, who, at, kind, cr, decision, draft_hash, detail FROM watcher_event "
                       "WHERE kind IN ('settle', 'settle-failed') ORDER BY id DESC LIMIT ?", (limit,))
    hidden = _hidden_values()
    items = []
    for r in rows:
        try:
            d = json.loads(r["detail"] or "{}")
        except ValueError:
            d = {}
        d = d if isinstance(d, dict) else {}
        items.append({"id": r["id"], "cr": r["cr"], "at": r["at"], "who": r["who"], "failed": r["kind"] != "settle",
                      "status": r["decision"] or "", "decision": str(d.get("decision") or ""),
                      "ref": str(d.get("ref") or ""), "ticket": str(d.get("ticket") or ""),
                      "title": _redact(str(d.get("title") or ""), hidden, shaped=False),
                      "resolution": _redact(str(d.get("resolution") or ""), hidden, shaped=False),
                      "draft_hash": r["draft_hash"] or ""})
    return {"items": items}


def _next_run(now: Optional[_dt.datetime] = None) -> str:
    """When the PM2 job next starts the watcher: RUN_MINUTE past the hour, in the server's local time (PM2's cron
    is local; a zone half an hour off UTC moves the minute), as a UTC time."""
    minute = RUN_MINUTE
    try:
        minute = int(os.environ.get("CR_WATCH_RUN_MINUTE") or RUN_MINUTE) % 60
    except ValueError:
        pass
    local = (now or _dt.datetime.now(_dt.timezone.utc)).astimezone()
    nxt = local.replace(minute=minute, second=0, microsecond=0)
    if nxt <= local:
        nxt += _dt.timedelta(hours=1)
    return security.stamp(nxt.astimezone(_dt.timezone.utc))


def _runs(out: Path, hidden: List[str]) -> List[dict]:
    """The last RUNS_SHOWN lines of runs.log, newest first: the time and the counts line the run wrote."""
    path = out / "runs.log"
    try:
        with path.open("rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 64 * 1024))
            tail = f.read().decode("utf-8", "replace")
    except OSError:
        return []
    lines = [x for x in tail.splitlines() if x.strip()][-RUNS_SHOWN:]
    got = []
    for x in reversed(lines):
        at, _, rest = x.partition(" ")
        if _parse_time(at) is None:
            at, rest = "", x
        got.append({"at": at, "line": _redact(rest, hidden)[:400]})
    return got


@router.get("/health")
def health(account: dict = Depends(require_decider)):
    """How the watcher is: its last runs, today's spend against the cap, why drafting stopped, the last error, and
    when the next hourly run is due."""
    out = _out()
    s = _summary(out, None)
    m = cw()
    hidden = _hidden_values()
    return {k: s[k] for k in ("watching", "last_run_at", "last_error", "paused", "running_since", "spend_today_usd",
                              "daily_cap_usd", "waiting", "not_drafted", "draft_failed")} | {
        "spend_held_usd": round(m.spend_held(out), 2), "next_run_at": _next_run() if s["watching"] else "", "runs": _runs(out, hidden),
        "batch_usd": float(m.MAX_BUDGET_USD)}


# ── asking back ──────────────────────────────────────────────────────

class AskIn(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


def _watcher_argv(command: str, *extra: str) -> List[str]:
    argv = [sys.executable, str(_script()), command, "--out", os.environ.get("CR_WATCH_OUT", "")]
    env_file = _env_file()
    if env_file:
        argv += ["--env-file", str(env_file)]
    return argv + list(extra)


def _run_watcher(argv: List[str], input_text: Optional[str], timeout: int):
    """cr-watch.py as a subprocess in a process group of its own (security review, M1): on a timeout the whole group
    is killed, so a settle_changes.py or a Claude turn under it is never left running on its own."""
    return cw().run_group(argv, input_text, timeout, str(_script().parent))


def _answer(entry_id: int, ref: str, question: str, thread: List[dict]) -> None:
    """The ask-back turn, in a thread of its own: cr-watch.py ask, its one JSON line written into the entry."""
    try:
        claude = os.environ.get("CR_WATCH_CLAUDE", "").strip()
        argv = _watcher_argv("ask", "--cr", ref, *(["--claude", claude] if claude else []))
        got = {}
        try:
            p = _run_watcher(argv, json.dumps({"question": question, "thread": thread}), (cw().ASK_MINUTES + 2) * 60)
            last = (p.stdout or "").strip().splitlines()[-1:] or [""]
            got = json.loads(last[0]) if last[0].startswith("{") else {}
            if not got:
                got = {"error": "The watcher's ask did not answer (its self-tests may have failed)."}
        except subprocess.TimeoutExpired:
            got = {"error": "The question took too long and was stopped."}
        except (OSError, ValueError) as e:
            got = {"error": f"The question could not be asked ({e.__class__.__name__})."}
        hidden = _hidden_values()
        if got.get("error"):
            db.change("UPDATE watcher_thread SET state = 'failed', error = ?, answered_at = ? WHERE id = ?",
                      (_redact(str(got["error"]), hidden)[:500], _now(), entry_id))
        else:
            proposal = got.get("proposal")
            db.change(
                "UPDATE watcher_thread SET state = 'answered', answer = ?, proposal = ?, cost_usd = ?, answered_at = ? "
                "WHERE id = ?",
                # An answer cites commits and ids, so only the env file's values and keys are taken out of it.
                (_redact(str(got.get("text") or ""), hidden, shaped=False)[:60000],
                 json.dumps(proposal, ensure_ascii=False) if isinstance(proposal, dict) else "",
                 float(got.get("cost_usd") or 0), _now(), entry_id))
    finally:
        ASK_SLOTS.release()


@router.post("/requests/{cr}/ask", status_code=202)
def ask(cr: str, body: AskIn, account: dict = Depends(require_decider)):
    """One read-only Claude turn about the draft; answers at once with the thread entry, which the page polls."""
    ref = _ref(cr)
    out = _out()
    m = cw()
    state = _state(out)
    p = state["pending"].get(ref)
    if not p:
        raise HTTPException(404, f"{ref} is not waiting in the watcher's list.")
    if not (out / "drafts" / f"{ref}.md").is_file():
        raise HTTPException(409, f"{ref} has no draft to ask about yet.")
    if not _watching():
        return _not_running("so there is no Claude turn to ask")
    question = body.question.strip()
    if not question:
        raise HTTPException(400, "There is no question to ask.")
    hour_ago = security.stamp(security.now() - _dt.timedelta(hours=1))
    asked = db.one("SELECT COUNT(*) AS n FROM watcher_thread WHERE account_id = ? AND asked_at > ?",
                   (account["id"], hour_ago))["n"]
    if asked >= ASKS_PER_HOUR:
        raise HTTPException(429, f"You have asked {asked} questions in the last hour, the most there can be; ask "
                                 f"again in a while.")
    spent, cap = m.spend_today(out), float(state.get("daily_cap_usd") or m.DAILY_USD)
    if spent >= cap:
        raise HTTPException(429, f"Today's spend (${spent:.2f}) has reached the daily cap (${cap:.2f}); ask again "
                                 f"tomorrow.")
    if not ASK_SLOTS.acquire(blocking=False):
        raise HTTPException(429, "Two questions are being answered already; ask again when one comes back.")
    try:
        thread = [{"question": t["question"], "answer": t["answer"]} for t in _thread(ref) if t["state"] == "answered"]
        entry_id = db.write(
            "INSERT INTO watcher_thread (cr, account_id, asked_by, asked_at, question, draft_hash, state) "
            "VALUES (?, ?, ?, ?, ?, ?, 'asking')",
            (ref, account["id"], account["email"], _now(), question, m.draft_hash(p.get("draft"))))
        threading.Thread(target=_answer, args=(entry_id, ref, question, thread), daemon=True,
                         name=f"watcher-ask-{ref}").start()
    except Exception:
        ASK_SLOTS.release()
        raise
    return _entry(db.one("SELECT * FROM watcher_thread WHERE id = ?", (entry_id,)))


# ── settling ─────────────────────────────────────────────────────────

class ApplyIn(BaseModel):
    fingerprint: str = Field(max_length=64)


def _settle(apply: bool, fingerprint: str = ""):
    """cr-watch.py settle as a subprocess: (exit code, printed lines, the fingerprint it printed, what it attempted,
    what it applied). The last two are the JSON lines settle prints from the marks its fingerprint was taken from."""
    extra = ["--apply", "--fingerprint", fingerprint] if apply else []
    try:
        p = _run_watcher(_watcher_argv("settle", *extra), None, APPLY_SECONDS if apply else PREVIEW_SECONDS)
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "Settling took too long and was stopped; preview again to see where it got to.") \
            from None
    except OSError:
        raise HTTPException(503, NOT_SET_UP + " Its settle step could not be started.") from None
    hidden = _hidden_values()
    raw = (p.stdout or "") + (p.stderr or "")
    lines = [_redact(x, hidden)[:MAX_LINE] for x in raw.splitlines() if x.strip()
             and not re.match(r"^cr-watch settle: (attempted|applied) ", x)]
    lines = lines[:MAX_LINES]
    found = re.findall(r"cr-watch settle: fingerprint ([0-9a-f]{32})", p.stdout or "")

    def made(word):
        for x in (p.stdout or "").splitlines():
            if x.startswith(f"cr-watch settle: {word} "):
                try:
                    got = json.loads(x.split(" ", 3)[3])
                except (ValueError, IndexError):
                    return []
                return [it for it in got if isinstance(it, dict) and REF.match(str(it.get("cr") or ""))]
        return []

    return p.returncode, lines, found[0] if found else "", made("attempted"), made("applied")


@router.post("/settle/preview")
def settle_preview(account: dict = Depends(require_decider)):
    """The dry run of what the marks would settle, and the fingerprint an apply must carry back."""
    _out()
    cw()
    every = PREVIEW_EVERY
    try:
        every = float(os.environ.get("CR_WATCH_PREVIEW_EVERY") or PREVIEW_EVERY)
    except ValueError:
        pass
    with _previews_lock:
        last = _previews.get(account["id"], 0.0)
        if time.monotonic() - last < every:
            raise HTTPException(429, "You previewed a moment ago; preview again in a few seconds.")
        _previews[account["id"]] = time.monotonic()
    if not _SETTLING.acquire(blocking=False):
        raise HTTPException(423, "A settle is running already; wait for it to finish and preview again.")
    try:
        rc, lines, fingerprint, _, _ = _settle(False)
    finally:
        _SETTLING.release()
        with _previews_lock:                      # the wait counts from when the preview ended
            _previews[account["id"]] = time.monotonic()
    if rc == 4:
        raise HTTPException(423, "The watcher is drafting right now; preview again when its run ends.")
    return {"lines": lines, "fingerprint": fingerprint, "exit": rc, "ok": rc == 0}


@router.post("/settle/apply")
def settle_apply(body: ApplyIn, account: dict = Depends(require_decider)):
    """settle --apply, only when REVIEW.md's marks are still the ones the preview's fingerprint was taken from. The
    audit trail records what settle reports it settled, from the fingerprinted marks; a settle that fails part way
    records what it was attempting."""
    fingerprint = body.fingerprint.strip().lower()
    if not FINGERPRINT.match(fingerprint):
        raise HTTPException(400, "That is not a fingerprint from a preview; preview again.")
    _out()
    if not _SETTLING.acquire(blocking=False):
        raise HTTPException(423, "A settle is running already; wait for it to finish and preview again.")
    try:
        rc, lines, _, attempted, applied = _settle(True, fingerprint)
    finally:
        _SETTLING.release()
    if rc == 3:
        raise HTTPException(409, "The marks or a draft changed since your preview; preview again and settle what "
                                 "it shows.")
    if rc == 4:
        raise HTTPException(423, "The watcher is drafting right now; settle again when its run ends.")
    if rc != 0:
        # settle_changes.py may have settled some of them in ADAM before it failed: each is recorded as attempted,
        # with the lines that name it, and the watcher's list keeps them all (it is safe to settle again).
        for it in attempted:
            said = [x for x in lines if it["cr"] in x][:6]
            _event(account, "settle-failed", it["cr"], it.get("status") or "", it.get("draft_hash") or "",
                   json.dumps({"fingerprint": fingerprint, "exit": rc, "mark": it.get("mark") or "", "lines": said},
                              ensure_ascii=False))
        return JSONResponse(status_code=502, content={
            "detail": "Settling failed; nothing was taken off the list, but some requests may have been settled in "
                      "ADAM already. The lines say which; settling again is safe.", "lines": lines, "exit": rc})
    for it in applied:
        _event(account, "settle", it["cr"], it.get("status") or "", it.get("draft_hash") or "",
               json.dumps({"fingerprint": fingerprint, "decision": it.get("decision") or "", "ref": it.get("ref") or "",
                           "mark": it.get("mark") or "", "ticket": str(it.get("ticket") or "")[:20],
                           "title": str(it.get("title") or "")[:500],
                           "resolution": str(it.get("resolution") or "")[:8000]}, ensure_ascii=False))
    done = [it["cr"] for it in applied]
    if not done:
        return {"applied": False, "settled": [], "lines": lines, "exit": rc,
                "detail": "Nothing was settled: no request is marked approve or change the way settling takes it."}
    return {"applied": True, "settled": done, "lines": lines, "exit": rc}


# ── the phone's device token ─────────────────────────────────────────

class DeviceIn(BaseModel):
    device: str = Field(min_length=1, max_length=80)


def _revoke(rows, actor: Optional[dict], reason: str) -> int:
    """Revoke the device tokens in `rows` (id, account_id, device) and put each in the audit trail."""
    now, n = _now(), 0
    for r in rows:
        if db.change("UPDATE watcher_device SET revoked_at = ? WHERE id = ? AND revoked_at IS NULL", (now, r["id"])):
            n += 1
            if actor:
                _event(actor, "device-revoke", "", detail=json.dumps(
                    {"id": r["id"], "device": r["device"], "account_id": r["account_id"], "reason": reason},
                    ensure_ascii=False))
    return n


def revoke_devices(account_id: int, reason: str, actor: Optional[dict] = None) -> int:
    """Every live device token of an account, revoked. main.py and cli.py call it wherever they end the account's
    sessions (sign out everywhere, a password change or reset, deactivation): a phone's token outlives no session.
    `actor` is who did it (an admin), else the account itself."""
    rows = db.all_rows("SELECT id, account_id, device FROM watcher_device WHERE account_id = ? AND revoked_at IS NULL",
                       (account_id,))
    if not rows:
        return 0
    who = actor or db.one("SELECT id, email FROM account WHERE id = ?", (account_id,))
    return _revoke(rows, dict(who) if who else None, reason)


@router.post("/device-token")
def make_device_token(body: DeviceIn, account: dict = Depends(require_decider)):
    """A token the app keeps for its background check of the summary. Shown once; only its hash is stored. A new one
    for the same device revokes the old; past DEVICE_MAX live tokens the longest unused is revoked."""
    device = re.sub(r"[\x00-\x1f\x7f]", " ", body.device).strip()[:80]
    if not device:
        raise HTTPException(400, "Name the device, like Pixel 8.")
    live = db.all_rows("SELECT id, account_id, device, made_at, last_used_at FROM watcher_device "
                       "WHERE account_id = ? AND revoked_at IS NULL ORDER BY COALESCE(last_used_at, made_at), id",
                       (account["id"],))
    _revoke([r for r in live if r["device"] == device], account, "a new token for the same device")
    _revoke([r for r in live if r["device"] != device and not _device_live(r)], account, "expired")
    keep = [r for r in live if r["device"] != device and _device_live(r)]
    if len(keep) >= DEVICE_MAX:
        _revoke(keep[:len(keep) - DEVICE_MAX + 1], account, f"more than {DEVICE_MAX} devices: the longest unused")
    token = security.new_token()
    made = db.write("INSERT INTO watcher_device (account_id, device, token_hash, made_at) VALUES (?, ?, ?, ?)",
                    (account["id"], device, security.token_hash(token), _now()))
    _event(account, "device-token", "", detail=json.dumps({"id": made, "device": device}, ensure_ascii=False))
    return {"token": token, "id": made}


@router.get("/device-tokens")
def list_device_tokens(account: dict = Depends(require_decider)):
    rows = db.all_rows("SELECT id, account_id, device, made_at, last_used_at FROM watcher_device "
                       "WHERE account_id = ? AND revoked_at IS NULL ORDER BY id", (account["id"],))
    return {"items": [{k: r[k] for k in ("id", "device", "made_at", "last_used_at")} for r in rows if _device_live(r)]}


@router.delete("/device-token/{token_id}")
def revoke_device_token(token_id: int, account: dict = Depends(require_decider)):
    row = db.one("SELECT id, account_id, device FROM watcher_device WHERE id = ? AND revoked_at IS NULL", (token_id,))
    if not row:
        raise HTTPException(404, "There is no such device token.")
    if row["account_id"] != account["id"] and not security.is_owner(account["role"]):
        raise HTTPException(403, "Only the person who made a device token, or the System Architect, can revoke it.")
    _revoke([row], account, "revoked by hand")
    return {"ok": True, "id": token_id}


# ── how much a request may carry ─────────────────────────────────────

class BodyCap:
    """ASGI middleware: a request body to /api/watcher/ over BODY_MAX bytes is answered 413 before any route reads
    it, whether it says its length or streams in chunks (security review, M6). main.py installs it innermost, inside
    the CORS layer, so the browser can read the refusal."""

    def __init__(self, app, limit: int = BODY_MAX):
        self.app, self.limit = app, limit

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http" or not scope.get("path", "").startswith("/api/watcher/") \
                or scope.get("method") in ("GET", "HEAD", "OPTIONS"):
            return await self.app(scope, receive, send)
        for name, value in scope.get("headers") or []:
            if name == b"content-length":
                try:
                    if int(value) > self.limit:
                        return await self._too_big(receive, send, 0)
                except ValueError:
                    return await self._too_big(receive, send, 0)
        chunks, size = [], 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            chunk = message.get("body", b"")
            size += len(chunk)
            if size > self.limit:
                if not message.get("more_body", False):
                    return await self._too_big(None, send, size)
                return await self._too_big(receive, send, size)
            chunks.append(chunk)
            if not message.get("more_body", False):
                break
        body, given = b"".join(chunks), False

        async def replay():
            nonlocal given
            if not given:
                given = True
                return {"type": "http.request", "body": body, "more_body": False}
            return await receive()

        return await self.app(scope, replay, send)

    async def _too_big(self, receive, send, seen: int):
        # What is still coming is read and dropped, never kept, up to DRAIN_MAX, so the caller is not cut off before
        # it can read the refusal; past that the connection is closed on it.
        while receive is not None and seen <= DRAIN_MAX:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            seen += len(message.get("body", b""))
            if not message.get("more_body", False):
                break
        text = json.dumps({"detail": f"That request is larger than the {self.limit // 1024} KB these routes take."})
        await send({"type": "http.response.start", "status": 413,
                    "headers": [(b"content-type", b"application/json"), (b"connection", b"close")]})
        await send({"type": "http.response.body", "body": text.encode("utf-8")})
