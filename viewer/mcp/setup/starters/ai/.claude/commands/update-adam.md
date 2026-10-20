---
description: Update the ADAM connector to the build ADAM is serving
---

Run this, and show me exactly what it prints:

```
node "%USERPROFILE%\.adam\connector\update.mjs"
```

It compares the connector on this machine with the one ADAM is serving, and replaces it only if
they differ. It keeps the build it replaced in a `backup-<build>` folder beside the connector.

If it says an update was applied, tell me to **restart Claude Code** — the connector running in
this session is still the old one, and will be until it is started again.

If it cannot reach ADAM, say so and stop. Do not try another address: the one it uses is the one
this machine is already configured with.
