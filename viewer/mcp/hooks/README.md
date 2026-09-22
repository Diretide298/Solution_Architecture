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

That list is the whole point rather than a limitation. Anything richer would put
every prompt anybody ever typed — and any secret pasted into one — into a
database that gets exported as CSV and backed up. The service drops anything
outside the list, so editing the hook on your machine does not widen it.

The consequence worth knowing: the page can tell you Edit failed eleven times on
#6046 and cannot tell you what it was trying to edit. Open the ticket for that.

## Installing

The hooks need the same two variables the connector already uses —
`ADAM_EMAIL` and `ADAM_PASSWORD` — because the session is filed against you by
signing in as you. If the ADAM connector works, these will.

In `~/.claude/settings.json` (or a project's `.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse":       [{ "hooks": [{ "type": "command", "command": "node <path>/adam-hook.mjs record" }] }],
    "PostToolUse":      [{ "hooks": [{ "type": "command", "command": "node <path>/adam-hook.mjs record" }] }],
    "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "node <path>/adam-hook.mjs record" }] }],
    "Stop":             [{ "hooks": [{ "type": "command", "command": "node <path>/adam-hook.mjs record" }] }],
    "SessionEnd":       [{ "hooks": [{ "type": "command", "command": "node <path>/adam-hook.mjs flush"  }] }]
  }
}
```

`<path>` is this folder. Only `SessionEnd` touches the network.

## Why it is split in two

`record` appends one line to a file and returns. No sign-in, no request, no
waiting — it sits in front of every tool call, and a hook that costs 200ms is a
hook somebody deletes within the week.

`flush` runs once when the session ends and sends the file in a single request.
If it fails — offline, ADAM down, laptop shut — the file stays and goes with the
next flush. Sending is keyed on the session id, so a file that goes twice is
still one session.

Everything exits 0, always. A statistics hook does not get to interrupt your
work to report that a statistics upload did not happen.

## Where it writes

`~/.adam/agent/`, under your home directory rather than in the repository, so it
never turns up in `git status`. Files are removed once ADAM has them.

## Turning it off

Remove the hooks. Nothing else depends on them: the connector, the testing gate
and everything else work exactly the same without this.
