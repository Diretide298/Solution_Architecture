# Git & Merge Requests

## 9. Code Review

Every change reviewed. Elevated-review areas per `AI_AUTHORSHIP.md` §5 need a second
reviewer with domain knowledge.

**Reviewer checklist:**

- [ ] Tenant scope enforced on every data path
- [ ] Permission checked at the right scope level
- [ ] Money uses `Money`, correct currency scale
- [ ] Timestamps distinguish `recorded_at` from `synced_at` where offline applies
- [ ] Errors handled; nothing swallowed
- [ ] Idempotency key on mutations
- [ ] Naming conforms to `NOMENCLATURE.md`
- [ ] Tests assert behaviour and cover failure paths
- [ ] No secrets, no PII in logs
- [ ] External API references verified against real documentation
- [ ] Comments explain *why*, citing the decision where non-obvious

---

## 10. Commits and Branches

**Conventional Commits**, scoped to the context:

```
feat(orders): add dual-authorisation to refund flow
fix(access): correct re-entry count on group media
chore(contracts): bump identity spec to v1.2.0
```

Types: `feat` `fix` `refactor` `perf` `test` `docs` `chore` `build` `ci`

Trailers per `AI_AUTHORSHIP.md`:

```
Refs: C04, 2.12.3
Assisted-By: Claude (Anthropic) <ai@softlabs.example>
```

Branches: `<type>/<context>/<short-description>` — `feat/orders/dual-auth-refund`.

Squash on merge. One logical change per commit on `main`.
