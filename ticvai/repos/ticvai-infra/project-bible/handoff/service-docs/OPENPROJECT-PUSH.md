# Pushing the task sheet into OpenProject

How Block A went into OpenProject project 153 (`ticvai`) on pms.softlabsgroup.in, and the order to do it in next
time. Written after the first push on 23-24 September, which learned most of this the slow way.

## The order

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
