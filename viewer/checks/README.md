# Checks

Puppeteer harnesses run against a viewer that is already up. Both halves have to be
running and an account has to exist, because the viewer is behind a sign-in:

```
./start.ps1                       # frontend on 4173, accounts on 8787
node checks/paging-check.mjs
node checks/contract-trace-check.mjs
```

They sign in as `harness.admin@softlabsgroup.com`. Create that account once — through
`/admin.html` if you already have an administrator, or as the first account at the door
on an empty database.

| | what it holds still |
|---|---|
| `paging-check.mjs` | the boot payload is split and compressed, every held-back field comes back from `/api/detail`, and the long list is built a group and a page at a time without losing a row |
| `contract-trace-check.mjs` | a schema names the tables it is stored as, an operation names the tables it reaches, and an operation the lineage never resolved says so rather than reading as "touches nothing" |

Both check on a **cold tab** — one navigation, no visiting another layer first. The parts
these views read arrive after the layer is already drawn, which is exactly where a block
like this fails quietly.

`api/api-check.mjs`, `api/extras-check.mjs`, `api/gate-check.mjs` and `api/ui-auth-check.mjs`
cover the accounts service and the sign-in gate, and run the same way.
