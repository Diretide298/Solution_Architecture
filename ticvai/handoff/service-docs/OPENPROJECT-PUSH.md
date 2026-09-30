# Pushing the task sheet into OpenProject

How Block A went into OpenProject project 153 (`ticvai`) on pms.softlabsgroup.in, and the order to do it in next
time. Written after the first push on 23-24 September, which learned most of this the slow way.

**From release `r1` on, a release reaches OpenProject through the release push below: three commands, pulled from
git on the server.** The step-by-step order after it is how the first pushes were done, and its scripts stay in
`tools/` for repairs and one-off jobs.

## The release push (from r1; council items C6 and C7, 1 October)

OpenProject holds who, when, state and order. The package, served by ADAM at a release tag, holds what. So a
ticket's description is a **pointer**: a one-line summary, its key, the artefact ids it builds (operations,
tables, screen, service), `Pull via ADAM: /ticket <id>` and the release it was written at.

### Here, before tagging (Stage 3 of the release)

```
python3 tools/op-release.py --release r1        # writes handoff/service-docs/op-release.json
```

It refuses (and writes nothing) if two keys share one OpenProject id, a new ticket's parent is nowhere, the plan's
waits have a cycle, or check-key-stability fails. `pms-map.json` is authoritative: a pushed key is never made
again or re-keyed. Commit the bundle, then tag `r1`: the server checks out the tag and refuses a bundle built for
another release. `--show KEY ...` prints a ticket's entry and pointer.

### On the OpenProject server: the three commands

```
/opt/ticvai-release/ticvai/tools/op-release-server.sh dry-run r1
/opt/ticvai-release/ticvai/tools/op-release-server.sh apply r1
/opt/ticvai-release/ticvai/tools/op-release-server.sh apply r1 ONLY=descriptions BATCH=200    # staged pointers, repeat
```

- **dry-run** fetches the tags, checks out `r1` (a checkout with local changes is refused), copies
  `tools/op-release.rb` and `op-release.json` into the container and prints the full plan of every phase (the
  first 40 lines of each list; `SHOW=all` for all). The log is kept in `/opt/ticvai-release/.release-out/`.
- **apply** refuses unless a dry run of the same tag and the same bundle came first, takes the database backup
  (`/root/databaseBackup/openproject-<time>-r1.dump`), runs it, then copies the new ticket ids out of the
  container to `.release-out/op-created-r1.json` and prints them.
- Then, here: `scp root@193.34.144.157:/opt/ticvai-release/.release-out/op-created-r1.json .` (or paste the
  printed JSON into a file), `python3 tools/op-created-merge.py op-created-r1.json`, commit `pms-map.json`.
  Only when the create phase made tickets.

`op-release.rb` runs these phases in order, each in one transaction, with no mail, authored by Chinmay Parab
(`AUTHOR=<login>` if his account is not found by name). It is safe to run again: every phase compares first.

| Phase | What it does |
|---|---|
| guard | Refuses if two keys map to one id, or a pushed plan ticket is missing from the project. Runs again after create with the new ids |
| create | Makes the tickets with no id, parents before children, with assignee, accountable, week, Priority_No. and the pointer. A ticket with the same subject under the same parent and no key of its own is taken, not made twice. A New ticket under the wrong parent is moved under the plan's; a started one is listed. Writes `/tmp/op-created.json` |
| priority | Priority_No. (the build order) on every plan ticket, started and closed ones too: it is an order, not content |
| assign | Assignee, accountable and Block A week on New tickets (Surendra is `Surendra Loke`, from the bundle's aliases). A started ticket keeps its people and gets one comment per release naming the plan's (`ASSIGN_COMMENT=0`: none) |
| links | Removes a direct follows link between two plan tasks that the plan no longer orders, even through a chain, then adds the missing ones. Duplicates are skipped |
| retire | Tickets that left the plan, New only: on hold (off the board: no assignee, no week) or rejected, with `op-retire.py`'s reason as a comment. Tickets with no reason, and stale sub-tasks, are listed and never touched |
| descriptions | A New ticket's description becomes its pointer. A started ticket keeps the text its work began against and gets **one** comment: its spec lives in ADAM from this release (found again by its wording, so never twice). New tickets are retitled to the plan (`RETITLE=all`: started ones too). `BATCH=n` limits rewrites and comments per run, earliest build order first |
| health | Read-only: duplicates, missing, wrong type or parent, tickets the plan does not know, links to Rejected tickets, and how many New tickets still lack their pointer |

`ONLY=phase,phase` runs just those phases (the guard always runs); `LIMIT=n` adds only n links, to time them.
ADAM's links for new tickets are still loaded on the ADAM box (step 4 below).

### Once: the checkout on the OpenProject server

The repository is cloned read-only, and only the two folders the push needs are checked out. Use a GitLab
**deploy key** (read-only) or a **deploy token** with `read_repository` only; never a personal token.

```
ssh-keygen -t ed25519 -N '' -f /root/.ssh/ticvai_release -C 'ticvai release (read-only)'
cat /root/.ssh/ticvai_release.pub        # add it in GitLab: the project > Settings > Repository > Deploy keys, write access OFF
export GIT_SSH_COMMAND='ssh -i /root/.ssh/ticvai_release -o IdentitiesOnly=yes'
git clone --filter=blob:none --no-checkout git@gitlab.softlabsgroup.in:chinmay/ticvai_architecture.git /opt/ticvai-release
git -C /opt/ticvai-release config core.sshCommand 'ssh -i /root/.ssh/ticvai_release -o IdentitiesOnly=yes'
git -C /opt/ticvai-release sparse-checkout init --cone
git -C /opt/ticvai-release sparse-checkout set ticvai/tools ticvai/handoff/service-docs
git -C /opt/ticvai-release checkout main
```

With a deploy token over HTTPS instead, the clone URL is
`https://<token name>:<token>@gitlab.softlabsgroup.in/chinmay/ticvai_architecture.git`. The token then sits in
`/opt/ticvai-release/.git/config`: `chmod 700 /opt/ticvai-release/.git`. If the server refuses the partial clone,
drop `--filter=blob:none`. The checkout only ever holds a release tag; nothing is edited or committed there.

## The order (the first pushes, 23-30 September)

1. **Tickets** (from here, through the API). Epics, features and tasks, then sub-tasks, parents first, with full
   descriptions from the start:

   ```
   TICVAI_OP_TOKEN=... python3 tools/push-openproject.py --schedule <schedule.json>
   ```

   About 40 tickets a minute. Resumable: `pms-map.json` records each one as it is made, and a re-run carries on.
   Stop it before step 3 if it reaches the links; see below.

2. **Check the tree.** Every ticket's parent in OpenProject should match `tasks.csv`. Nothing should be missing.

3. **"Follows" links, on the OpenProject server, not through the API.** Through the API each link takes ~40 s once
   the graph is large, because OpenProject 10 writes a row for every derived connection (typed_dag) and re-walks
   the graph to check for loops. On the server:

   ```
   python3 tools/op-bulk-links.py                 # here: checks the graph once, writes op-links.json
   ```

   Copy `tools/op-bulk-links.rb` and `op-links.json` to the server, take a database backup, then run the script,
   dry run first (the commands are in the script's header). 1,474 links took 94 s. Implied links (A>C when A>B>C)
   are left out by default: the order they enforce is exactly the same.

4. **ADAM links**, so a pulled ticket arrives with its contract, tables, service and screens:

   ```
   TICVAI_OP_TOKEN=... python3 tools/adam-links.py    # here: writes adam-links.json
   ```

   On the ADAM server: back up `/srv/ticvai/viewer/api/ticvai.db`, then run
   `viewer/api/load_links.py adam-links.json --email <you> --db /srv/ticvai/viewer/api/ticvai.db`, dry run first,
   then `--apply` as the `ticvai` user. 17,124 links load in about a second; a re-run adds nothing.

5. **Descriptions**, only for tickets pushed before the push script wrote them (step 1 does it now):
   `tools/op-descriptions.py` here, `tools/op-descriptions.rb` on the server. It writes directly, so no notification
   email per ticket.

6. **The list view.** OpenProject nests children only when they are on the same page as their parent, so the
   server's `per_page_options` needs a page big enough for the project (`20, 100, 500, 3000`). The shared
   views "Hierarchy (all levels)" (396) and "Hierarchy (to tasks)" (397) show the tree.

## The server

- pms.softlabsgroup.in is Contabo host `vmi163716` (193.34.144.157) behind Cloudflare. Apache proxies to
  `localhost:8080`, the Docker container `openproject` (OpenProject 10.0.2).
- Rails runner: `docker exec openproject bash -c 'cd /app && bundle exec rails runner <script> <args>'`. It takes
  about 75 s to start and prints nothing until then; do not interrupt it.
- Backup first, every time:
  `docker exec openproject bash -c 'pg_dump -Fc "$DATABASE_URL"' > /root/databaseBackup/openproject-<date>.dump`
- The same server runs SuiteCRM, Mailtrain and the support CRM. Paste only command blocks into its shell, never
  output: on 24 September a pasted "command not found" hint ran `apt install openafs-client` as root.

## What not to do

- Do not send links through the API in parallel. Four at once took the server's reads from 1 s to 30-40 s.
- Do not link at feature level to save calls. It adds tens of thousands of waits the plan does not have.
- Do not edit 2,816 descriptions through the API. Every edit emails the assignee.
