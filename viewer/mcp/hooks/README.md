# Telling ADAM how the agent is being used

Claude Code runs on your machine and ADAM does not. These hooks are how ADAM
can answer *is the agent actually being used, on what, and what keeps failing* —
the Agents page under Tasks.

## What gets sent

| sent | not sent |
|---|---|
| which tool ran | the prompt |
| whether it worked | tool arguments |
| how long it took | file contents or diffs |
| a classified error word — `timeout`, `refused`, `not-found`, `conflict` | the error message |
| which ticket was open | the path you are working in (only the folder's name) |
| when a prompt was sent and when Claude stopped — the times only | the words of either |
| the computer's name, and that it was Claude Code | anything from a folder ADAM is not connected to |

The host name and the prompt and stop times have been sent since the hook was
written and are only now in this table. The folder rule is new with the
settings.json install (13 October 2026), which puts the hooks in every folder.

That list is the whole point rather than a limitation. Anything richer would put
every prompt anybody ever typed — and any secret pasted into one — into a
database that gets exported as CSV and backed up. The service drops anything
outside the list, so editing the hook on your machine does not widen it.

The consequence worth knowing: the page can tell you Edit failed eleven times on
#6046 and cannot tell you what it was trying to edit. Open the ticket for that.

## Installing

**Nobody pastes anything any more.** Until 13 October 2026 this section was a
block of JSON to copy into your settings, and the Agents page showed 0 people,
0 sessions and 0 tool calls, because nobody had: the only automatic install was
the plugin's, and every developer was on the zip.

| install | how the hooks get in |
|---|---|
| the zip (`setup.cmd`) | setup copies `adam-hook.mjs` beside the connector and adds ADAM's five hooks to `~/.claude/settings.json` |
| an existing zip install | `/update-adam` brings `adam-hook.mjs` and adds the same five. From a build older than 13 October it takes **two runs**: the first brings an updater that knows the file exists, the second brings the file |
| the plugin | `hooks.json` in this folder, wired by the plugin manifest |

Restart Claude Code afterwards: hooks are read when a session starts.

`adam-hook.mjs` lives beside `client.mjs` in the connector folder, not in here:
the zip install is a flat copy of the files `version.mjs` lists, and the updater
refuses any name with a folder in it.

### What setup and `/update-adam` do to `settings.json`

Setup runs `update.mjs --install-hooks`; `/update-adam` runs the same code in its
own process, never the file it has just downloaded. It:

- reads the file whole and keeps every setting and every hook that is not
  ADAM's exactly as it was. ADAM's are recognised by the script they run,
  `adam-hook.mjs`, so one pasted by hand from the old version of this README is
  replaced rather than doubled — two would record every tool call twice;
- adds one entry each to `PreToolUse`, `PostToolUse`, `UserPromptSubmit` and
  `Stop` (`record`, `async`, 10 s) and to `SessionEnd` (`flush`, 30 s), the
  timings in `hooks.json`;
- keeps the file as it was beside it, as `settings.json.adam-<when>.bak`, and
  writes nothing at all when nothing would change — setup run twice leaves one
  set of hooks and one backup;
- leaves a file that is not valid JSON exactly as it is, and prints one line
  saying what to add by hand.

Each command is `node '<connector>/adam-hook.mjs' record` (or `flush`): forward
slashes in single quotes, because Claude Code on Windows runs a hook through Git
Bash when there is one and PowerShell when there is not, and that spelling means
the same in both, with a space, a `$` or a backtick in the path.

User scope, so one set covers every folder — but the hook only sends from a
folder ADAM is connected to (below). A session anywhere else is dropped on the
machine, so another repository's work is never filed against an ADAM project.

**`/update-adam` puts them in once and never puts them back.** If they were
installed on this machine and are gone now, somebody took them out; the update
says so, with the command to turn them back on, rather than overriding that.
Running setup again is asking for them, and does put them back.

### Who it signs in as

The session is filed against you by signing in as you, with what the connector
already has. The hook takes, in order:

1. `ADAM_VIEWER_URL`, `ADAM_EMAIL`, `ADAM_PASSWORD`, `ADAM_PROJECT` from its
   environment — for somebody overriding by hand;
2. the plugin's options, `CLAUDE_PLUGIN_OPTION_*`, which Claude Code exports to
   a plugin's hooks, the password out of the OS credential store;
3. the zip install's registration in `~/.claude.json`: the entry `claude mcp add`
   wrote for the folder the session is in (or a folder it is inside), else the
   every-folder one. Only an entry that launches this connector's `server.mjs`
   is read — the rule `update.mjs` uses for the address.

No new copy of the password is made anywhere: the third is where setup already
keeps it. With none of the three there is nobody to sign in as, and the session
file is kept for when there is.

Only `SessionEnd` touches the network.

### Checking it

```
TICVAI_DB=<scratch>.db python -m uvicorn api.main:app --port 8799      (in viewer/)
TICVAI_AUTH=http://127.0.0.1:8799 node server.mjs --port 4199           (in viewer/)
VIEWER=http://127.0.0.1:4199 node viewer/mcp/hooks-check.mjs
```

builds the zip, runs its setup into a throwaway home against a stand-in Claude
Code, checks the settings merge, plays a session through the hook, finds it in
`/api/agent/usage` (what the Agents page reads), uninstalls, and walks
`/update-adam` up from the last build without the hook. It refuses a viewer that
is not on this machine.

## Why it is split in two

`record` appends one line to a file and returns. No sign-in, no request, no
waiting — it sits in front of every tool call, and a hook that costs 200ms is a
hook somebody deletes within the week.

`flush` runs once when the session ends and sends the file in a single request.
If it fails — offline, ADAM down, laptop shut — the file stays, and goes when
that session ends again (a resumed session keeps its id). Sending is keyed on
the session id, so a file that goes twice is still one session. A file whose
session never ends again stays where it is: later sessions do not sweep it up.

Everything exits 0, always. A statistics hook does not get to interrupt your
work to report that a statistics upload did not happen.

## Where it writes

`~/.adam/agent/`, under your home directory rather than in the repository, so it
never turns up in `git status`. Files are removed once ADAM has them.

## Turning it off

Take ADAM's entries out of `~/.claude/settings.json`, or run

```
node "%USERPROFILE%\.adam\connector\update.mjs" --remove-hooks
```

which removes ADAM's and nothing else. `/update-adam` will not put them back;
`--install-hooks`, or setup, does. `uninstall.cmd` removes them with the
connector. Nothing else depends on them: the connector, the testing gate and
everything else work exactly the same without this.
