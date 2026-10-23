ADAM setup for Claude Code
==========================

Creates your project folder - backend or frontend - and connects Claude Code
in it to ADAM, so Claude can read the design package (screens, journeys, API
contracts, tables, services) and your OpenProject tickets, as you.

  Backend:   setup creates the folder for you (a clone of the team repository).
  Frontend:  setup creates a workspace folder with ADAM's files; then you
             clone your app's repository inside it (see FRONTEND below).
             Setup builds no frontend code.

Only Claude Code sessions opened in that project folder - in VS Code or a
terminal - can use ADAM.

Build: {{BUILD}}


BEFORE YOU START
----------------
  * An ADAM account. Accounts are by invitation - ask an ADAM admin.
    Sign in once at https://adam.ainfinite.ai to be sure it works.
  * Node.js 22 or newer:       winget install --id OpenJS.NodeJS.LTS -e
  * Claude Code:               npm install -g @anthropic-ai/claude-code
    (open a new window after installing, run "claude" once and sign in)
  * Git:                       winget install --id Git.Git -e
  * Backend:  the .NET 10 SDK  winget install --id Microsoft.DotNet.SDK.10 -e
  * Frontend: access to your app's repository in GitLab (ask your lead),
              and what that repository's README asks for


SET IT UP
---------
  1. Make a folder for your work, for example C:\work, and unzip this file
     into it (right-click -> Extract All). You get:

        C:\work\adam-setup\setup.cmd
        C:\work\adam-setup\adam-connector\   (leave this folder alone)

  2. Double-click setup.cmd.
  3. Type your ADAM email and password. The password is hidden as you type.
     Setup checks them against ADAM before changing anything.
  4. Pick the ADAM project by number:

        1. TICVAI  (ticvai)
     Enter the project number [1-1]: 1

  5. Pick what you work on:

        1. Backend  (.NET 10 API, clean architecture)
        2. Frontend (your app's repository: React Native or React web)
     Enter the number [1-2]: 1

  6. Setup shows the new project folder:   Folder [C:\work\ticvai-backend]:
     Press Enter. (Or paste another path - a new or empty folder.)
     Frontend shows C:\work\ticvai-frontend: see FRONTEND below.

  For the backend, setup then creates that folder, ready to work in:

     the code skeleton          renamed for your project
     CLAUDE.md                  how the project is laid out and how to work a ticket
     .claude\                   permissions, and the /ticket, /board and /done commands
     project-bible\setup\       the team's coding standards for your role
     a git repository           with the skeleton as its first commit

  TICVAI backend developers get a clone of the team repository instead
  (http://gitlab.softlabsgroup.in/ticvai/ticvai-backend). Setup asks for your
  GitLab username, then Git asks for your GitLab password. Setup only adds
  CLAUDE.md, .claude\ and project-bible\setup\ where the repository lacks
  them, and commits nothing on top of the team's code. If the clone fails,
  you get the skeleton above and can clone later.

  and registers ADAM with Claude Code for that folder only. It can also run
  the full connection test for you at the end.

  7. Open the new folder in VS Code (File -> Open Folder).
     Backend:  dotnet test
     Start Claude Code and ask:   What's on my board?

  Claude Code opened in any other folder - including a parent or a
  subfolder of the project folder - does not see ADAM.

  Setup.cmd can also be run from a terminal: the folder is then created
  inside the folder you ran it from.


FRONTEND: SETUP FIRST, THEN CLONE YOUR APP INSIDE
-------------------------------------------------
  The TICVAI frontend is six repositories, one per app, in the GitLab group
  ticvai-frontend:

     ticvai-venue-management   P08 Venue Management - Back Office
     ticvai-guest-web          P01 Guest Web - Storefront
     ticvai-employee-app       P06 Venue Staff App
     ticvai-kiosk              P05 Guest Kiosk - Self-Service
     ticvai-guest-app          P02 Guest App - Mobile
     ticvai-pos                P04 Venue POS

  1. Run setup and pick Frontend. Press Enter at the folder question:
     setup creates C:\work\ticvai-frontend - your workspace - with ADAM's
     files only, and connects ADAM to it:

        CLAUDE.md                  how to work a ticket, and which repository
                                   builds which platform
        .claude\                   permissions, and the /ticket, /board and /done commands
        project-bible\setup\       the team's coding standards for frontend

     No code, and it is not a git repository. Setup asks for your GitLab
     username and ends by printing one clone command per repository.

  2. Clone your app's repository inside the workspace - copy the line for
     your app (on two apps, both lines). Git asks for your GitLab password:

        cd C:\work\ticvai-frontend
        git -c http.proactiveAuth=basic clone http://YOU@gitlab.softlabsgroup.in/ticvai-frontend/ticvai-pos.git

     That makes C:\work\ticvai-frontend\ticvai-pos. The six addresses:

        http://gitlab.softlabsgroup.in/ticvai-frontend/ticvai-venue-management.git
        http://gitlab.softlabsgroup.in/ticvai-frontend/ticvai-guest-web.git
        http://gitlab.softlabsgroup.in/ticvai-frontend/ticvai-employee-app.git
        http://gitlab.softlabsgroup.in/ticvai-frontend/ticvai-kiosk.git
        http://gitlab.softlabsgroup.in/ticvai-frontend/ticvai-guest-app.git
        http://gitlab.softlabsgroup.in/ticvai-frontend/ticvai-pos.git

  3. Open VS Code / Claude Code in C:\work\ticvai-frontend, NOT inside the
     repository folder, so ADAM and the project bible load. A session opened
     in C:\work\ticvai-frontend\ticvai-pos does not get ADAM: Claude Code
     connects it to the workspace only.

  Build, test and commit inside the repository folder, as its README says.
  ADAM's files stay in the workspace and never go into the team repository.

  Already cloned your app somewhere else? Run setup and give it that folder:
  setup changes none of its files and commits nothing; it adds CLAUDE.md,
  .claude\ and project-bible\setup\ where they are missing, and keeps what
  it added - with .adam\ and .claude\settings.local.json - out of git on
  your computer only (in .git\info\exclude; your team's .gitignore is not
  touched), so ADAM's files never go into the team's repository. A backend
  folder you already have gets the same treatment.

  Run setup again on the same folder (after a password change, say) and it
  finds ADAM's files there and adds nothing.

  (The old single workspace with every app in it is still there for a
  try-out: setup.cmd -UseStarter.)


SEE YOUR OPENPROJECT WORK TOO
-----------------------------
  1. In OpenProject: My account -> Access tokens -> API -> generate.
     It is shown once. Never paste it into chat or a ticket.
  2. Paste it at https://adam.ainfinite.ai/settings.html#openproject
  No need to run setup again.


WORKING A TICKET
----------------
  In Claude Code, in your project folder:

    /board
        Your open tickets, pulled into .adam\ and summarised by milestone.

    /ticket 6046
        Pulls the ticket and every screen, table and contract it is linked
        to under .adam\work\6046\, builds it, runs the tests, and proposes
        the OpenProject update. Nothing changes in OpenProject yet.

    Yes, apply it.
        Claude Code asks before it runs the tool that changes OpenProject
        (adam_apply) - allow it. OpenProject is updated as you, and the
        change is noted in .adam\work\6046\log.md.

    /done 6046
        When you built it yourself: proposes closing the ticket with a
        comment from your changes and the test results.

  Plain words work too: "Pull ticket 6046 and build it."
  Your own notes go in .adam\work\<ticket>\notes.md. Pulling again keeps
  notes.md and log.md. .adam\ is never committed.

  Never choose "always allow" for adam_apply.


WHAT ADAM IS TOLD ABOUT YOUR SESSIONS
-------------------------------------
  Setup also turns on ADAM's usage hooks, which fill the Agents page (under
  Tasks): is the agent being used, on which tickets, and which tools keep
  failing. When a Claude Code session ends, ADAM is sent:

    for each tool call: which tool ran, whether it worked, how long it took,
    and a one-word reason when it failed (timeout, refused, not-found,
    conflict, cancelled, error);
    when you sent a prompt and when Claude stopped - the times, not the words;
    which ticket was open (from .adam\work\), the folder's name and the
    computer's name.

  Never your prompts, tool arguments, file contents, diffs, commands or the
  error text, and never the folder's full path. Only sessions in folders ADAM
  is connected to are sent; anything else is dropped on your machine.

  The hooks are five entries in %USERPROFILE%\.claude\settings.json, added
  beside whatever is already there. Setup keeps the file as it was next to it
  (settings.json.adam-<date>.bak) and changes nothing else in it. If that file
  is not valid JSON, setup leaves it alone and prints what to add by hand.
  The hooks sign in with the same ADAM account as the connector; no new copy
  of your password is made.

  Turn them off:   node "%USERPROFILE%\.adam\connector\update.mjs" --remove-hooks
  Back on:         node "%USERPROFILE%\.adam\connector\update.mjs" --install-hooks
  /update-adam never turns them back on once you have turned them off.


LATER
-----
  * Changed your ADAM password?      Run setup.cmd again and give the same
                                     project folder; its files are not touched,
                                     and ADAM's are only added if missing.
  * Got a newer version of this zip? Run its setup.cmd the same way.
  * Keep the connector current:      /update-adam in Claude Code, then
                                     restart Claude Code. One run is
                                     enough from 23 October 2026: the new
                                     updater finishes the job itself. A
                                     connector older than that needs
                                     /update-adam twice, once.
  * Another project or role?         Run setup.cmd again and pick it.
  * Remove ADAM from one folder, in PowerShell:
        powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.adam\connector\setup.ps1" -RemoveFolder "C:\work\ticvai-backend"
    Setup prints this line, with your own folder, when it finishes.
  * Remove it everywhere:            Double-click uninstall.cmd. Project
                                     folders are left as they are. ADAM's
                                     usage hooks are taken out of your
                                     Claude Code settings; nothing else
                                     in that file changes.
  * Removing your token from ADAM does not revoke it in OpenProject -
    delete it there too.


IF SOMETHING GOES WRONG
-----------------------
  "Node.js is not installed" / "Claude Code is not installed"
      Install it (see BEFORE YOU START), open a NEW window, run setup again.

  "ADAM did not accept that email and password"
      Sign in at https://adam.ainfinite.ai to check them. A forgotten
      password is reset by an ADAM admin.

  "Your ADAM password contains one of  " & % ^ | < > !"
      Only with an old Claude Code install. Update it
      (npm install -g @anthropic-ai/claude-code) and run setup again.

  "Your ADAM account cannot open any project yet"
      Ask an ADAM admin to give you access to the project.

  "The ... starter is missing next to this script"
      Run setup.cmd from the unzipped adam-setup folder, not from
      %USERPROFILE%\.adam\connector.

  "No OpenProject project has been chosen" (from Claude)
      An ADAM admin has not picked which OpenProject project this ADAM
      project reads. Ask them - it is on the admin page, under Projects.

  "running scripts is disabled on this system"
      Use setup.cmd rather than setup.ps1 - it allows this one run.

  Claude does not list the ADAM tools
      Make sure VS Code has the project folder open - the same folder, not
      a parent or a subfolder of it. Restart Claude Code. Then, in that
      folder's terminal, run:  claude mcp get adam
      It should show ADAM_VIEWER_URL, ADAM_PROJECT, ADAM_EMAIL and
      ADAM_PASSWORD under "Environment". Do not send that output to anyone -
      it includes your password.


WHAT IS IN THIS FOLDER
----------------------
  setup.cmd        double-click to create a project folder and connect it
  uninstall.cmd    double-click to remove ADAM from every folder
  adam-connector\
    setup.ps1      what both of those run
    server.mjs     the connector Claude Code starts
    client.mjs     how it talks to ADAM
    tools.mjs      the 19 tools
    mcp-check.mjs  the connection test
    version.mjs    which build this is
    update.mjs     what /update-adam runs; also turns the usage hooks on/off
    adam-hook.mjs  the usage hook (see WHAT ADAM IS TOLD ABOUT YOUR SESSIONS)
    starters\      ADAM's CLAUDE.md, .claude\ and coding standards for each
                   role, and the backend and (old) frontend skeletons

Setup keeps a copy of the connector and its scripts in
%USERPROFILE%\.adam\connector, so you can delete this folder afterwards.

Your password is stored in Claude Code's own settings file
(%USERPROFILE%\.claude.json) and nowhere else. Use an ADAM password you do
not use anywhere else.
