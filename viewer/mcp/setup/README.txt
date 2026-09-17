ADAM connector for Claude Code
==============================

Lets Claude Code on your computer read the TICVAI design in ADAM - screens,
journeys, API contracts, tables, services, modules and architecture
decisions - and your OpenProject work, as you. Nothing to clone, nothing to
build.

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
  1. Unzip this folder anywhere (right-click -> Extract All).
  2. Double-click setup.cmd.
  3. Type your ADAM email and password. The password is hidden as you type.

  Setup checks your password against ADAM before changing anything, copies
  the connector to %USERPROFILE%\.adam\connector, and registers it with
  Claude Code for every project you open. It can also run the full
  connection test for you at the end.

  4. Restart Claude Code and ask:   What's on my board?


SEE YOUR OPENPROJECT WORK TOO
-----------------------------
  1. In OpenProject: My account -> Access tokens -> API -> generate.
     It is shown once. Never paste it into chat or a ticket.
  2. Paste it at https://adam.ainfinite.ai/settings.html#openproject
  No need to run setup again.


LATER
-----
  * Changed your ADAM password?     Run setup.cmd again.
  * Got a newer version of this zip? Run its setup.cmd - it replaces the old one.
  * Remove it:                      Double-click uninstall.cmd.
  * Removing your token from ADAM does not revoke it in OpenProject -
    delete it there too.


IF SOMETHING GOES WRONG
-----------------------
  "Node.js is not installed" / "Claude Code is not installed"
      Install it (see BEFORE YOU START), open a NEW window, run setup again.

  "ADAM did not accept that email and password"
      Sign in at https://adam.ainfinite.ai to check them. A forgotten
      password is reset by an ADAM admin.

  "Your ADAM password contains a double quote"
      Windows PowerShell cannot pass that character on. Change your ADAM
      password (Settings -> Password) to one without quotes, run setup again.

  "running scripts is disabled on this system"
      Use setup.cmd rather than setup.ps1 - it allows this one run.

  Claude does not list the ADAM tools
      Restart Claude Code. Then run:  claude mcp get adam
      It should show ADAM_VIEWER_URL, ADAM_EMAIL and ADAM_PASSWORD under
      "Environment". Do not send that output to anyone - it includes your
      password.


WHAT IS IN THIS FOLDER
----------------------
  setup.cmd       double-click to set up (or to update)
  uninstall.cmd   double-click to remove
  setup.ps1       what both of those run
  server.mjs      the connector Claude Code starts
  client.mjs      how it talks to ADAM
  tools.mjs       the 13 tools
  mcp-check.mjs   the connection test

Your password is stored in Claude Code's own settings file
(%USERPROFILE%\.claude.json) and nowhere else. Use an ADAM password you do
not use anywhere else.
