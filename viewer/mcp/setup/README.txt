ADAM connector for Claude Code
==============================

Lets Claude Code on your computer read a design package in ADAM - screens,
journeys, API contracts, tables, services, modules and architecture
decisions - and your OpenProject work, as you. Nothing to clone, nothing to
build.

It is set up for ONE code folder at a time. Only Claude Code sessions opened
in that folder - in VS Code or a terminal - can use ADAM.

Build: {{BUILD}}


BEFORE YOU START
----------------
  * An ADAM account. Accounts are by invitation - ask an ADAM admin.
    Sign in once at https://adam.ainfinite.ai to be sure it works.
  * Node.js 22 or newer:       winget install --id OpenJS.NodeJS.LTS -e
  * Claude Code:               npm install -g @anthropic-ai/claude-code
    (open a new window after installing, run "claude" once and sign in)


SET IT UP
---------
  1. Unzip this folder anywhere (right-click -> Extract All), for example
     to C:\Downloads\adam-connector.
  2. Open PowerShell (or the VS Code terminal) IN YOUR CODE FOLDER - the
     folder you open in VS Code - and run setup.cmd from there:

        cd C:\work\ticvai-backend
        C:\Downloads\adam-connector\setup.cmd

  3. Type your ADAM email and password. The password is hidden as you type.
     Setup checks them against ADAM before changing anything.
  4. Pick the ADAM project by number:

        1. TICVAI  (ticvai)
        2. ...
     Enter the project number [1-2]: 1

  5. Setup shows your code folder:   Folder [C:\work\ticvai-backend]:
     Press Enter. (You can paste a different folder instead, or type all
     to let every folder use ADAM.)

  Setup copies the connector to %USERPROFILE%\.adam\connector and registers
  it with Claude Code for that folder only. It can also run the full
  connection test for you at the end.

  6. Open that folder in VS Code (File -> Open Folder) and start Claude Code,
     then ask:   What's on my board?

  Claude Code opened in any other folder - including a subfolder of this
  one - does not see ADAM. For another code folder, run setup from it too.

  Double-clicking setup.cmd works as well; it then asks you to paste the
  folder's path.


SEE YOUR OPENPROJECT WORK TOO
-----------------------------
  1. In OpenProject: My account -> Access tokens -> API -> generate.
     It is shown once. Never paste it into chat or a ticket.
  2. Paste it at https://adam.ainfinite.ai/settings.html#openproject
  No need to run setup again.


WORKING A TICKET
----------------
  Start Claude Code in your code folder and ask in plain words:

    What's on my board?
        Your open tickets in this project, and what each one touches.

    Pull ticket 6046 into this folder.
        Saves the ticket and every screen, table, contract and decision it
        is linked to under .adam\work\6046\ - README.md first. Claude reads
        those files as it needs them. .adam\ is never committed.

    Pull my whole board.
        Every open ticket, plus .adam\board.md grouped by milestone.

    I have finished 6046 - propose closing it with a comment.
        Claude shows you exactly what would change in OpenProject. Nothing
        changes until you say yes. Then it applies it as you, and notes it
        in .adam\work\6046\log.md.

  Your own notes go in .adam\work\<ticket>\notes.md. Pulling again keeps
  notes.md and log.md and refreshes everything else.

  Claude Code asks before it runs the tool that changes OpenProject
  (adam_apply). Do not choose "always allow" for that one.


LATER
-----
  * Changed your ADAM password?      Run setup again from each folder.
  * Got a newer version of this zip? Run its setup.cmd - it replaces the old one.
  * Another code folder?             Run setup from that folder.
  * Remove ADAM from one folder, in PowerShell:
        powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.adam\connector\setup.ps1" -RemoveFolder "C:\work\ticvai-backend"
    Setup prints this line, with your own folder, when it finishes.
  * Remove it everywhere:            Double-click uninstall.cmd (here, or in
                                     %USERPROFILE%\.adam\connector).
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

  "No OpenProject project has been chosen" (from Claude)
      An ADAM admin has not picked which OpenProject project this ADAM
      project reads. Ask them - it is on the admin page, under Projects.

  "running scripts is disabled on this system"
      Use setup.cmd rather than setup.ps1 - it allows this one run.

  Claude does not list the ADAM tools
      Make sure VS Code has the folder you set up open - the same folder,
      not a parent or a subfolder of it. Restart Claude Code. Then, in that
      folder's terminal, run:  claude mcp get adam
      It should show ADAM_VIEWER_URL, ADAM_PROJECT, ADAM_EMAIL and
      ADAM_PASSWORD under "Environment". Do not send that output to anyone -
      it includes your password.


WHAT IS IN THIS FOLDER
----------------------
  setup.cmd       run from your code folder to set it up (or to update)
  uninstall.cmd   double-click to remove ADAM from every folder
  setup.ps1       what both of those run
  server.mjs      the connector Claude Code starts
  client.mjs      how it talks to ADAM
  tools.mjs       the 16 tools
  mcp-check.mjs   the connection test

Setup keeps a copy of setup.ps1, setup.cmd and uninstall.cmd beside the
installed connector, so you can delete this folder afterwards.

Your password is stored in Claude Code's own settings file
(%USERPROFILE%\.claude.json) and nowhere else. Use an ADAM password you do
not use anywhere else.
