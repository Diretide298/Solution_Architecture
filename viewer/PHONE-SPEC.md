# ADAM on the phone: spec

4 November 2026. The lead (Chinmay): "I want the watcher to be deployed in server. I need a mobile app for adam on
which I can review the decision from watcher, and then pass on my own, the exact way we do here", "it's for smaller,
quicker decisions so my laptop doesn't run all day", "we will power with claude api key", "I would like all the pages
in the phone version as well", "just build the apk file here I will install it on my phone", "make sure the UI UX is
banger, maybe even for main website".

## What it is for

The change-request watcher runs on the ADAM server instead of the lead's laptop. It drafts and tells the lead; it
never settles. The lead reads a draft on the phone, asks about it, and approves, changes or rejects it; then settles
what he decided, after seeing exactly what will be posted. Success: a blocking request is decided from the phone the
same hour it arrives, with the same safety as REVIEW.md today (a decision binds to the draft it was made on; nothing
reaches a ticket before the lead presses Settle), and every ADAM page is usable on a phone.

Out of scope: changing how the watcher drafts, what settling does, or any TICVAI package rule. iPhone app (the same
pages work in Safari as a home-screen web app).

## 1. The watcher on the server

- **Where.** A PM2 job `ticvai-cr-watch` beside `ticvai-api` (viewer/deploy/deploy.sh `ecosystem.config.cjs`), run as
  `ticvai`, hourly (`cron_restart`, `autorestart: false`). It runs `cr-watch.py run` from its own clone,
  `/srv/ticvai/cr-watch/repo`, whose origin is a mirror `/var/lib/ticvai/cr-watch-mirror.git` that deploy.sh (root)
  refreshes from `~/adam` on every deploy, so a new release tag reaches the watcher with the deploy and the watcher
  needs no git credential. The mirror is root's (`ticvai` reads it and cannot write it), and root's git runs no hook or
  file-system monitor there (security review of 6 November 2026, H1). Output: `/srv/ticvai/cr-watch/out` (state.json,
  drafts/, REVIEW.md, runs.log).
- **One run at a time.** The run lock (cr-watch.py `locked`) is made atomically and is stale as soon as the process
  that made it is gone, so a run PM2 killed does not lock the next one out; a PM2 stop kills the run's Claude turns
  with it.
- **Credentials.** `/etc/ticvai/cr-watch.env`, mode 600, owner ticvai, never in git: `ANTHROPIC_API_KEY`,
  `ADAM_EMAIL`, `ADAM_PASSWORD`, `TICVAI_OP_TOKEN`. A Claude turn's environment is an allowlist (cr-watch.py
  `child_env`, `CHILD_ENV`): PATH, HOME, the locale, the temporary folder, what Windows needs to start a process,
  `ANTHROPIC_API_KEY` and `CLAUDE_*`; nothing else reaches it. It loads no settings file (the release tree's
  `.claude/` could hold hooks): `--restricted` with only `--settings {"disableAllHooks":true}` from the command line.
- **Claude Code** installed on the box for ticvai (`npm i -g @anthropic-ai/claude-code`), signed in by the API key.
- **Spending.** Before each turn the watcher reserves the turn's whole budget in `out/spend.jsonl` (under a file
  lock, so the run's batches and the phone's questions cannot all find room at once), and a turn that would take
  today past the daily cap (`CR_WATCH_DAILY_USD`, default 50) is not started; drafting stops, state.json records why,
  and the summary shows it. When the turn ends the reservation is reconciled to the cost in Claude's JSON answer
  (`total_cost_usd`); a turn that times out, is killed or answers no cost keeps its budget as the estimate. Today's
  spend therefore counts the turns still running. Per batch stays $10; an ask-back turn is capped at $2
  (`CR_WATCH_ASK_USD`).
- **Room under the cap, and saying why** (6 November 2026: a $20 cap fitted two $10 reservations, nine requests waited
  an hour for a run that cost $1.78, and the page said "stopped at the daily cap: $0.00 spent; until tomorrow"). A
  batch refused only because the turns beside it hold the room waits for one to settle and starts in the same run,
  within `CAP_WAIT_SECONDS` (15 minutes) of the run's start; it is skipped only when today's real spend (the ledger
  less what running turns hold) leaves no room. A request not tried this run drops an earlier run's failure. state.json
  `paused` says what happened (`drafting_note`): "Drafting failed: <reason>; N requests wait for a draft", "Drafting is
  held: N failed twice (<reason>)", "Daily cap reached: $X of $Y spent today; N wait until tomorrow (UTC)", or that N
  wait for the next hourly run because only K batches fit under the cap at once. The first failure is also
  `last_error`. While a run drafts, state.json says since when (`running_since`) and the summary shows that rather
  than the last run's note.
- **Draft again.** A request whose drafting failed `MAX_TRIES` (2) times waits for the lead: Draft again on the page,
  or `cr-watch.py redraft CR-nnn [CR-nnn ...] | --all-failed` from a shell (run as the watcher's account), resets it
  for the next run. Neither starts a Claude turn.
- **Never settles on its own.** The server job runs `run` without `--auto` (no automatic closes): the lead decides
  everything ("the watcher never replied on its own, it gives me a notification and I make the decision").

## 2. The decision API (viewer/api/watcher.py, an APIRouter included by main.py)

Only the owner, the System Architect (security.py `DECIDERS = ("owner",)`; the lead, 6 November 2026: "the decide
page only I can see it, no one else"). Every route, the device-token routes too, answers 403 to anybody else, a Team
Lead included, and a device token a Team Lead made earlier reads nothing. Every route but `history` reads the
watcher's output folder `CR_WATCH_OUT`; with none configured they answer 503, and the page says "The watcher is not
running on this server". With the folder there but no env file (the job stopped: 6 November 2026, the PM2 job deleted
and the env file shredded; change requests are drafted on the lead's machine), the summary says `watching: false`,
with no error and no pause, and Draft again and Ask are refused 409 `not-running`.

| Route | Does |
|---|---|
| `GET /api/watcher/summary` | waiting, blocking, needs-lead, needs-client counts; new since a time; last run and its error; today's spend and the cap; `watching`; `running_since` while a run drafts (its lock held by a live process; the last run's `paused` is then empty); `not_drafted` and `draft_failed` |
| `GET /api/watcher/requests` | the waiting requests as REVIEW.md lists them: number, title, verdict, class, blocking, needs, decision mark, ticket, developer, raised at, draft hash, `mark_digest`; for one with no draft, why (`draft_reason`), its tries and whether the watcher gave up on it (`gave_up`) |
| `GET /api/watcher/requests/{cr}` | one request: the draft (recommendation, resolution, misread, facts, the agent's full answer), its draft hash, the current mark and its `mark_digest`, the ask-back thread, and the developer's own request (`request`: problem, evidence, options, recommendation, as ADAM's export has it; the watcher keeps it in state.json, while drafts/CR-n.md holds the facts, the draft and the agent's answer) |
| `POST /api/watcher/requests/{cr}/decision` | `{decision: approve, change or reject, draft_hash, expected_mark, resolution?, status?, ref?, note?}`; written into REVIEW.md under the watcher's lock exactly as the lead types it today. Refused 409 `{detail, reason}` when the request has no draft (`not-drafted`: nothing to decide; draft it again), the draft hash moved (`draft-moved`) or the mark is no longer `expected_mark` (`mark-moved`: decided again elsewhere, or an offline replay after a newer mark). The same decision sent again over the mark it made answers `unchanged: true`. An approve puts the draft's status, ref and resolution back. Answers the new `mark_digest` |
| `DELETE /api/watcher/requests/{cr}/decision` | `{draft_hash, expected_mark}`; takes the mark back (the drafted lines return); bound and refused like a decision |
| `POST /api/watcher/requests/{cr}/ask` | `{question}`; starts one read-only Claude turn in the release worktree (same tools and denials as drafting, $2, 30 turns) with the draft, the thread so far and the question; answers 202 with the thread entry; the page polls. Ten an hour per account (429) |
| `POST /api/watcher/settle/preview` | runs `cr-watch.py settle` (dry run); answers the lines it printed and a fingerprint of the decisions file. One per account every 10 seconds (429); one settle preview or apply at a time (423) |
| `POST /api/watcher/settle/apply` | `{fingerprint}`; refuses 409 if REVIEW.md's marks changed since the preview; else runs `settle --apply` (mail off) and answers `{applied, settled, lines}`; `applied` is false when nothing was settled. A settle that fails part way answers 502 and each request it was attempting goes in the audit trail |
| `POST /api/watcher/device-token` | the owner makes a token the phone app keeps for background checks; it reads `summary` only (counts, no titles); one per device, five per account, 90 days, 30 days unused; revocable, and revoked whenever the account's sessions end |
| `POST /api/watcher/requests/{cr}/redraft` | Draft again: a request with no draft (none yet, or failed `MAX_TRIES` times) has its tries and failure reset under the watcher's review lock (cr-watch.py `redraft`), and is queued in out/redraft.json so a run drafting at that moment takes it in when it publishes. Starts no Claude turn: the next hourly run drafts it. Refused 409 for a request with a draft or a mark, 404 for one not waiting, 409 `not-running` with no watcher. Twenty a minute per account (429); each in the audit trail (`redraft`) |
| `POST /api/watcher/redraft` | `{all_failed: true}` or `{crs: [...]}`: the same for every failed request ("Draft all again") or the ones named |
| `GET /api/watcher/history` | the requests settled from Decide, newest first, from `watcher_event`: when, who, the decision, the new status, the release, the ticket it told and what it posted; a settle that failed part way is marked failed. Reads ADAM's database only, so it answers with no watcher too |
| `GET /api/watcher/health` | the summary's run fields, the last twelve lines of runs.log (time and counts line), today's spend and what of it running turns hold, a batch's budget, and when the next hourly run is due (`CR_WATCH_RUN_MINUTE`, default 7, past the hour in the server's time; none with no watcher) |

An ask-back answer may end with a proposed resolution in a fenced `json` block; the page offers "Use this answer",
which fills the Change box. Asking never changes a decision on its own.

Records: every decision, take-back, Draft again, settle (from the fingerprinted marks, with the ticket it told and
what it posted), failed settle, and device token made or revoked (with why) is stored in ADAM's database (`watcher_event`: who, when, cr, decision, draft hash) as the audit
trail; the thread in `watcher_thread`. What a route answers is cleaned of the env file's values (plain, base64 and
URL-encoded) and of anything shaped like a token. Request bodies to these routes are capped at 64 KB (413), in the
viewer's proxy and in the API.

## 3. The phone app (Capacitor, Android; its own repository)

The source lives in its own GitHub-only repository, github.com/Diretide298/test-apks (private), checked out at
D:/Chinmay/test-apks; never in this repository (the lead, 4 November 2026: "Code on GitHub only"). Built APKs are
not committed anywhere; they are kept in D:/Chinmay/adam/adam-app/ (gitignored).


- A native shell that opens `https://adam.ainfinite.ai/decide` full screen; the pages come from ADAM, so a deploy
  updates the app. Navigation stays inside adam.ainfinite.ai; other links open the browser.
- Fingerprint or phone-lock check on opening and before Settle (a settle-capable app on a phone).
- Haptics on approve, reject and settle. Status bar and splash in ADAM's colours; ADAM's icon.
- Notifications without Firebase: a background check every 15 minutes (Android's minimum) reads `summary` with the
  device token and raises a local notification for a new blocking request at once, and one evening digest for the
  rest.
- Built here with the installed JDK 17 and Android SDK; signed with a keystore kept outside the repository; the
  `.apk` is installed by hand. A debug build can point at a local ADAM over Wi-Fi for testing before deploy.

## 4. The decision page (`/decide`, public/decide.html, .js, .css)

- **Inbox:** blocking first, then needs-lead, then the rest; each row shows the number, title, ticket and developer,
  how long it has waited, and chips for blocking / needs you / needs the client. Swipe right to approve (with an
  undo), left to open. "Approve all that need nobody" lists them before it marks anything. A search over number,
  title and ticket; filters with counts (blocking, needs you, needs the client, not drafted) and a developer.
- **Not drafted yet:** a request with no draft (none yet, or its drafting failed) is never decided here: no swipe, no
  Approve, not in "Approve all that need nobody", not counted in the headline ("16 new, none drafted yet" and why,
  until drafts exist). It sits in its own section with the reason in plain words and Draft again, and "Draft all
  again" for the failed ones; opened, it says why and shows the developer's request, with Draft again only.
- **Request:** the ticket (a link to OpenProject, https://pms.softlabsgroup.in/work_packages/<id>), the developer,
  when it was raised and its class; the recommendation; the exact text that would be posted with its length against
  the 4,000 characters ADAM takes (a warning above it); the developer's own request; the facts; the agent's full
  answer (folded). Buttons: Approve, Change (edit the text, the count live), Reject (with a note), Ask.
- **Ask:** a thread under the request; each answer cites file:line like the drafts.
- **Decided tray and Settle:** decisions collect in a tray; Settle shows the dry run (each request, its new status,
  the ticket it tells) and applies after a fingerprint check.
- **History:** the requests settled from Decide, newest first, grouped by day: the decision, when, the ticket it
  told, and what was posted (folded).
- **Health:** the last run (or "Drafting now" while one runs), when the next is due, why drafting is held in the
  watcher's own honest words (cr-watch.py `drafting_note`: a failure and its reason, the real cap, or only a wait for
  room), the last error, today's spend against the cap and what running turns hold, and the last runs from runs.log.
- **No watcher on this server:** the inbox and Health say plainly "The watcher is not running on this server", with
  no error banner and no stale pause; Draft again and Ask are off with that reason; History still reads.
- A phone (420 by 933, in the app) has the bottom bar (Inbox, Decided, History, Health); a desktop has a rail and two
  panes, the list on the left and the request on the right.
- Works offline for reading (the last list is cached); a decision made offline is sent when back online and refused
  if its draft changed meanwhile, or if the request was decided again elsewhere (the page says which).

## 5. Every ADAM page on a phone, and the website's design

One design system for phone and desktop (tokens, type scale, spacing, touch sizes, motion), applied first to the
shared frame (menu, sheet table, drawers, chat panel, account drawer) and then to the pages in batches from
PHONE-INVENTORY.md. On a phone: the menu becomes a bottom bar with a drawer, wide tables become cards, drawers become
full-screen sheets, hover-only actions get a tap target. Big diagrams, canvases and drag-heavy boards are view and
zoom only on a phone (the recommended choice the lead approved with the plan, 4 November); editing stays on desktop.
The same system then refreshes the desktop pages so the phone and the website look like one product; what each page
does does not change.

## Safety rules carried over

- A decision binds to the draft hash it was made on and to the mark it was made over; a moved draft or a newer mark
  is refused (cr-watch.py `decisions_for`, `mark_digest`).
- Nothing reaches ADAM or a ticket before the lead presses Settle; settling is the existing `settle` step, mail off.
- Turns that read developers' text hold no credential and have read-only tools inside the release worktree.
- No credential in git, in the app, or in a page; the device token reads counts only, and ends with the account's
  sessions (sign out everywhere, a password change or reset, deactivation).

## Tests

- `api/watcher-check.mjs` (the changes-import-check.mjs pattern): a uvicorn on a temporary database, a fake watcher
  folder, fake-openproject.mjs; covers roles, the 409 on a moved draft, the preview fingerprint, the device token's
  reach, offline replay.
- cr-watch.py `--self-test` gains the spend cap and the server paths.
- Phone screenshots (390 by 844) and desktop of every page, before and after, for each batch.

## Contracts between the pieces (built in parallel; each side keeps to these)

**Summary** (`GET /api/watcher/summary?since=<ISO time>`; the owner's session, or `Authorization: Bearer <device
token>`, which may read this route and nothing else):

    {"waiting": 19, "blocking": 9, "needs_lead": 5, "needs_client": 2,
     "new": [{"cr": "CR-650", "title": "...", "blocking": true, "needs": "none", "raised_at": "2026-11-04T12:22:42Z"}],
     "last_run_at": "2026-11-04T13:23:10Z", "last_error": "", "paused": "",
     "spend_today_usd": 12.40, "daily_cap_usd": 50.0, "decided": 3,
     "watching": true, "running_since": "", "not_drafted": 0, "draft_failed": 0}

`new` holds requests drafted after `since` (all waiting ones when `since` is absent). `paused` is empty or the reason
drafting stopped (the cap). `decided` counts marks waiting in the tray for Settle. **With a device token, `title` is
always `""`** (counts only; security review of 6 November 2026, M3); `cr`, `blocking`, `needs` and `raised_at` keep
their shape, so the app's background check (test-apks `www/runners/watch.js`, which reads `new[].cr`, `blocking` and
`raised_at`) works unchanged, and a notification reads "CR-650 is blocking: " with no title. The lead's session
still reads the titles.

**Device token:** `POST /api/watcher/device-token {"device": "Pixel 8"}` answers `{"token": "...", "id": n}` once (only
its hash is stored); `DELETE /api/watcher/device-token/{id}` revokes it. A token ends 90 days after it was made, after
30 days unused, when a sixth is made for the account (the longest unused goes), and whenever the account's sessions
are ended; the summary then answers 401 and the app turns its watch off and says so.

**The page and the app.** The decide page runs in a browser and in the app; in the app `window.Capacitor` exists and
the page uses, when present:
- `Capacitor.Plugins.Haptics.impact({style: "LIGHT"})` on approve and reject, `notification({type: "SUCCESS"})` on a
  settle;
- `Capacitor.Plugins.BiometricAuthNative` through the app's shim `window.AdamApp.unlock(reason) -> Promise<boolean>`
  before Settle (the app also locks on open);
- `window.AdamApp.setWatch({base, token})` after the lead turns notifications on: the app's background check (every
  15 minutes) then calls the summary with that token and `since` = its last check, notifies at once for a new
  blocking request, and once at 19:00 local for the rest. `window.AdamApp.watchStatus() -> Promise<{on, lastCheck}>`.
Without `window.AdamApp` (a browser), the page offers no notification switch and settles after a plain confirm.
