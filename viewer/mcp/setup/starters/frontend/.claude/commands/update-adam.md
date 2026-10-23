---
description: Update the ADAM connector to the build ADAM is serving
---

Run this, and show me exactly what it prints:

```
node "%USERPROFILE%\.adam\connector\update.mjs"
```

It compares the connector on this machine with the one ADAM is serving, and replaces it only if
they differ. It keeps the build it replaced in a `backup-<build>` folder beside the connector.

If it says an update was applied, it has also stopped the old connector. Tell me to run **`/mcp`**,
choose **adam** and **Reconnect**: that starts the new build, with no need to close VS Code. If it says
it could not stop it, tell me to restart Claude Code instead.

To check the whole connector against ADAM afterwards, run:

```
node "%USERPROFILE%\.adam\connector\mcp-check.mjs"
```

If it cannot reach ADAM, say so and stop. Do not try another address: the one it uses is the one
this machine is already configured with.
