#!/usr/bin/env python3
"""Take tickets out of the plan when a decision took their work out of it.

Added 28 September for the audit decisions. R187 and R242 deferred seven guest screens to a later release,
R276 merged five duplicate screens into others, and other decisions moved or regrouped operations, so 20
pushed tickets have no row in tasks.csv any more. push-openproject.py only creates, so nothing else could
move them.

Every pushed ticket with no row in tasks.csv needs a reason below. One without a reason is listed as
unexplained and left alone: a ticket that silently vanished from the plan is a generator bug until someone
says otherwise.

A ticket is moved only if nobody has started it (status New). A started ticket is listed and left alone:
work in progress is a conversation, not a script.
- **Deferred:** the ticket and its sub-tasks go On hold, lose their Block A week (version) and their
  assignee, so they leave the developer's board. They get one comment saying why.
- **Merged:** the ticket and its sub-tasks go to Rejected (closed), with a comment naming the ticket that
  carries the screen now.
Sent with notify=false, so nobody is mailed. Dry run unless --apply. Token from TICVAI_OP_TOKEN.

    python tools/op-retire.py [--apply]
"""
import argparse
import csv
import base64
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "handoff" / "service-docs" / "pms-map.json"
BASE = "https://pms.softlabsgroup.in/api/v3"
ON_HOLD, REJECTED, NEW = 13, 14, 1

DEFERRED = {sid: "R187" for sid in ("GST-051", "GST-052", "GST-053", "GST-054", "GST-059")}
DEFERRED.update({sid: "R242" for sid in ("GST-030", "WEB-046")})
MERGED = {"BO-127": "BO-036", "BO-472": "BO-141", "CMS-020": "CMS-015", "BO-320": "BO-027", "BO-652": "BO-027"}
# Tickets out of the plan for a reason other than their own screen. "merge" names the ticket that carries
# the work now (closed as Rejected); "defer" is on hold, off the board.
OTHER = {
    "SVC-IDENTITY-MFA-2": ("merge", "SVC-IDENTITY-MFA-1", "verifyMfaChallenge and verifyMfaEnrolment were regrouped "
                           "into one task with the rest of MFA (audit R126, R135)"),
    "APP-SETUP-ADM-421": ("merge", "APP-SETUP-ADM-342", "its one setup operation, setPasswordPolicy, is built on "
                          "ADM-342 Authentication & MFA Policy Manager (audit R098, R126)"),
    "APP-SETUP-BO-746": ("defer", "", "setGuestMatchPolicy left the first release: there is no 'is this you?' step at "
                         "checkout any more (audit R120 (b))"),
    "SVC-MARKETING-GUESTS": ("defer", "", "guest checkout matching left the first release: a verified contact attaches "
                             "the order inside checkoutCart (audit R120 (b), ADR-0045)"),
    "SVC-MARKETING-GUESTS-1": ("defer", "", "guest checkout matching left the first release: a verified contact "
                               "attaches the order inside checkoutCart (audit R120 (b), ADR-0045)"),
    "SVC-IDENTITY-SSO": ("defer", "", "guests do not sign in with enterprise SSO, and no first-release screen calls it "
                         "(audit R167)"),
    "SVC-IDENTITY-SSO-1": ("defer", "", "guests do not sign in with enterprise SSO, and no first-release screen calls "
                           "it (audit R167)"),
    "VM-BO-027": ("defer", "", "BO-320 and BO-652 were merged into it (audit R276) and brought two operations the "
                  "client has not agreed yet; it returns once session S3 signs them off"),
    **{k: ("defer", "", "its operations moved to BO-735 Guest Directory, which is wave 3, outside the Venue "
                        "Management waves (audit R254)")
       for k in ("VM-MARKETING-CONSENT-1", "VM-MARKETING-GUEST-1", "VM-MARKETING-LOYALTY-1")},
    # 29-30 September: the phased build order and the Venue Management team rule (setup screens the Block A apps
    # use go first) moved work between the Block A and Venue Management keys. The work is the same; the ticket
    # under the new key carries it, and the one under the old key is closed.
    **{f"VM-BO-{n}": ("merge", f"APP-SETUP-BO-{n}", "a Block A app uses this screen, so it is built in Block A's "
                                                     "setup screens first (decided 30 September)")
       for n in ("005", "008", "009", "029", "045", "065", "075", "110", "117", "136")},
    **{f"APP-SETUP-BO-{n}": ("merge", f"VM-BO-{n}", "no Block A app uses this screen, so it is built with the "
                                                     "Venue Management waves (decided 30 September)")
       for n in ("013", "062", "086")},
    **{f"VM-{k}": ("merge", f"SVC-{k}", "a Block A screen calls these operations, so they are built in Block A "
                                        "(phased build order, decided 30 September)")
       for k in ("AI-GENERATE-1", "CATALOGUE-PROMOTIONS-1", "FNB-FNB-4", "LEDGER-ACCOUNTS-1", "LEDGER-TAX-1",
                 "LEDGER-TAX-2", "PLATFORM-PUBLICAPI-2", "REPORTING-CATALOGUE-1")},
    **{f"VM-MIG-{k}": ("merge", f"MIG-{k}", "one migration per schema, made once in Block A") for k in ("SEATING", "SYNC")},
    **{k: ("merge", "VM-CATALOGUE-UPSELL-1", "only the Venue Management back office calls the upsell rules, so they "
                                              "are built with the Venue Management waves (decided 30 September)")
       for k in ("SVC-CATALOGUE-UPSELL", "SVC-CATALOGUE-UPSELL-1")},
    "APP-SETUP-BO-857": ("defer", "", "BO-857 Resource Creation & Profile is wave 3, outside Block A and the Venue "
                         "Management waves 1-2"),
    "APP-SETUP-PTR-006": ("defer", "", "the partner portal (P10) screens are not in Block A or the Venue Management "
                          "waves 1-2; they come back when the partner portal is planned"),
    **{k: ("defer", "", "setReaderScannerPeripheral is still a draft operation, outside the first-release slice")
       for k in ("SVC-ACCESS-DRAFTED", "SVC-ACCESS-DRAFTED-1")},
    **{k: ("defer", "", "pauseCampaign, testSendCampaign and unscheduleCampaign are outside the first-release slice; "
                        "listCampaigns, stopCampaign and updateCampaign are built on VM-MARKETING-CAMPAIGN-1 and "
                        "SVC-MARKETING-CAMPAIGN-1")
       for k in ("VM-MARKETING-CAMPAIGN-2", "VM-MARKETING-CAMPAIGN-3")},
}


def build_plan():
    """(map, [(key, 'defer' | 'merge', comment)], [unexplained keys]). No network: tools/op-review.py reads it too."""
    mp = json.loads(MAP.read_text(encoding="utf-8"))
    with open(ROOT / "handoff" / "service-docs" / "tasks.csv", encoding="utf-8") as f:
        planned = {r["key"] for r in csv.DictReader(f)}
    gone = sorted({k.partition("#")[0] for k in mp if not k.startswith(("_", "VERSION"))} - planned)

    def keys_for(sid):
        # Only tickets the plan no longer has: a screen that moved to another ticket keeps that one.
        top = [k for k in mp if "#" not in k and re.search(rf"-{re.escape(sid)}$", k) and k not in planned]
        return [(k, [s for s in mp if s.startswith(k + "#")]) for k in top]

    def ticket_of(sid):
        return next((f"#{mp[k]}" for k in mp if "#" not in k and re.search(rf"-{re.escape(sid)}$", k)), sid)

    plan = []
    for sid, why in DEFERRED.items():
        note = (f"**Deferred to a later release** (decided 28 September, audit {why}). This screen is out of "
                "Block A, so the ticket is on hold and off the board. It comes back when its release is planned.")
        for k, subs in keys_for(sid):
            plan += [(x, "defer", note) for x in [k] + subs]
    for sid, into in MERGED.items():
        note = (f"**Merged into {into}** (decided 28 September, audit R276). {into}'s ticket "
                f"({ticket_of(into)}) now carries this screen's operations, so this ticket is closed.")
        for k, subs in keys_for(sid):
            plan += [(x, "merge", note) for x in [k] + subs]

    covered = {k.partition("#")[0] for k, _, _ in plan}
    for key, (kind, into, why) in OTHER.items():
        if key not in mp or key in planned:
            continue
        if kind == "merge":
            note = (f"**Merged into {into}** (decided 28 September): {why}. That ticket ({f'#{mp[into]}' if into in mp else into}) "
                    "carries the work now, so this ticket is closed.")
        else:
            note = (f"**Out of the first release** (decided 28 September): {why}. The ticket is on hold and off "
                    "the board; it comes back when its release is planned.")
        plan += [(x, kind, note) for x in [key] + [s_ for s_ in mp if s_.startswith(key + "#")]]
        covered.add(key)
    # A pushed sub-task whose task is still planned but whose operation or table is no longer under it (the task
    # was split or regrouped, 29-30 September): 128 on 1 October. Its work is either on another planned sub-task
    # (a duplicate in effect: closed, pointing at that one) or has left the plan (on hold). Decided 1 October.
    sys.path.insert(0, str(Path(__file__).parent))
    push = __import__("push-openproject")
    lineage = json.loads((ROOT / "handoff" / "api-data-lineage.json").read_text(encoding="utf-8"))
    with open(ROOT / "handoff" / "service-docs" / "tasks.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    subs = {k for r in rows for k, *_ in push.sub_tasks(r, lineage)}
    home = {}
    for k in sorted(subs):
        home.setdefault(k.partition("#")[2], k)
    done = {k for k, _, _ in plan}
    for k in sorted(mp):
        base, _, part = k.partition("#")
        if not part or k in subs or k in done or base not in planned or not isinstance(mp[k], int):
            continue
        other = home.get(part)
        if other and other in mp:
            plan.append((k, "merge", f"**Duplicate of #{mp[other]}** (decided 1 October): `{part}` moved to "
                                     f"{other.partition('#')[0]} when its task was regrouped; that sub-task carries "
                                     "it now, so this one is closed."))
        else:
            plan.append((k, "defer", f"**Out of the plan** (decided 1 October): `{part}` is no longer part of "
                                     f"{base}'s work in this release. The sub-task is on hold and comes back if "
                                     "its work is planned again."))
    unexplained = [g for g in gone if g not in covered]
    return mp, plan, unexplained



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    auth = "Basic " + base64.b64encode(f"apikey:{os.environ['TICVAI_OP_TOKEN']}".encode()).decode()
    head = {"Authorization": auth, "User-Agent": "curl/8.0", "Content-Type": "application/json"}

    def call(method, path, body=None):
        req = urllib.request.Request(BASE + path, json.dumps(body).encode() if body is not None else None,
                                     head, method=method)
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode() or "{}")

    mp, plan, unexplained = build_plan()
    for g in unexplained:
        print(f"  ??     #{mp[g]} {g}: out of tasks.csv with no reason in op-retire.py; left alone")

    skipped = 0
    for key, kind, note in plan:
        wp = call("GET", f"/work_packages/{mp[key]}")
        status = wp["_links"]["status"]["href"].rsplit("/", 1)[-1]
        if status != str(NEW):
            skipped += 1
            print(f"  leave  #{mp[key]} {key}: status is {wp['_links']['status']['title']}, not New")
            continue
        body = {"lockVersion": wp["lockVersion"], "_links": {"status": {"href": f"/api/v3/statuses/"
                                                                              f"{ON_HOLD if kind == 'defer' else REJECTED}"}}}
        if kind == "defer":
            body["_links"].update({"assignee": {"href": None}, "version": {"href": None}})
        print(f"  {kind:5}  #{mp[key]} {key}")
        if a.apply:
            call("PATCH", f"/work_packages/{mp[key]}?notify=false", body)
            call("POST", f"/work_packages/{mp[key]}/activities?notify=false", {"comment": {"raw": note}})
    moved = len(plan) - skipped
    print(f"{moved} to move, {skipped} left alone (already started), {len(unexplained)} unexplained"
          + ("" if a.apply else "; dry run, pass --apply"))


if __name__ == "__main__":
    sys.exit(main())
