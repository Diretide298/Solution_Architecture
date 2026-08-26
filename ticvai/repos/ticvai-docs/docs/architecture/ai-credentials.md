# AI provider credentials — where the key lives and who can reach it

**Decided 17 August.** One provider key per tenant, optionally per venue, so usage is attributable
at the provider rather than only in our own meter.

---

## Why per tenant rather than one platform key

**A tenant's usage bills against their own key**, which gives an independent reconciliation source:
the provider's invoice and our `settleAiUsage` figure should agree, and when they do not, the
difference is a fact rather than an argument.

One platform key would put every tenant's spend in one bill and leave us apportioning it from our
own numbers — **marking our own homework on the largest variable cost in the platform.**

**Per venue exists for two cases**: one venue's volume justifies its own key, or a venue is billed
separately from the rest of its tenant. It is not the default, because a key is a thing that
expires and each one is a rotation somebody has to remember.

---

## The rule that decides the whole design

**No surface ever holds a provider key.**

    guest kiosk ─┐
    guest app   ─┤
    guest web   ─┼──▶  TICVAI API  ──▶  vault  ──▶  provider
    staff app   ─┤        (in cell)
    back office ─┘

Every surface calls TICVAI. **TICVAI calls the provider.** A token that reaches a client is a
token that bills the tenant from somebody else's machine, and a kiosk in an entrance hall is the
worst possible place to put one.

This is not a new pattern — it is the same reason no surface holds a payment gateway credential.
It is written down because the temptation on a kiosk is real: a direct call would be one hop
faster and it would be a key sitting in a device anyone can walk up to.

## What is stored, and what is not

| | |
|---|---|
| **In the database** | `credentialRef` — a vault reference. Never the secret |
| **In the vault** | The secret, written once by `setAiCredential` |
| **Returned by any read** | The reference, the rotation date, the expiry, the last-verified date |
| **In `ai.interaction`** | Prompt, response, tokens, cost. **Never a credential** |
| **In an audit record** | That the credential was set, by whom. **The value is masked** |

`setAiCredential` is the only operation that carries a secret, and it carries it once.

## Rotation

**The same operation.** The previous key stays valid for a grace window — fifteen minutes by
default — so a request in flight does not fail mid-answer.

`credentialExpiresAt` is surfaced because **a key that lapses silently takes the assistant down
with no error anyone reads.** The failure presents as an assistant that stopped answering, which
is diagnosed slowly and usually by a guest.

## Verification

`testAiProvider` makes a minimal call using the stored credential. **Run before activating, and on
a schedule after.**

It costs a handful of tokens and **is billed to the tenant like any other call** — pretending
otherwise would put a hole in the reconciliation this whole design exists to make possible.

Failure reasons are specific: `invalidKey`, `expiredKey`, `quotaExceeded`, `modelUnavailable`,
`unreachable`, `residencyRefused`. **The last one matters** — a provider refusing on residency
grounds is a compliance signal, not an outage.

## Scope resolution

`AiProvider.scopeLevel` is `platform`, `tenant` or `venue`, and resolution is the same as every
other configuration: **nearest ancestor wins, venue is the floor** (ADR-0018).

A venue with no provider of its own uses the tenant's. A tenant with none uses the platform's,
which exists for trials and for tenants who have not been onboarded to their own key yet — and
**a tenant left on the platform key is a tenant whose spend we are absorbing**, which the
provider screen should make obvious rather than quiet.

## Where a key must not be shared

**Residency.** ADR-0009 and ADR-0020: a region with no adequacy finding gets a locally hosted
model, and that provider config cannot be inherited from a tenant whose key points at a US
endpoint. `residency` on the provider is what prevents that inheritance.

## Screens

| | |
|---|---|
| `ADM-037` **AI Provider & Credentials** — ticvai-web | Configure, store, rotate, test |
| `BO-091` **AI Policy & Spend** — back office | What the assistant may do here, what it has cost, what happens at the ceiling |
