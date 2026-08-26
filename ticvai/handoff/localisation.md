# Localisation

**3,088 translation keys are derivable from what already exists.** The artefact audit said
there was no key inventory; there was no *file*, but the keys were all sitting in the screens,
the contracts and the state models.

| Source | Keys | |
|---|---|---|
| Screen states | 1,244 | Loading, empty, error and offline text. **The largest source, and the one nobody counts** |
| Enum value labels | 1,224 | Across 223 enums. `paid`, `awaitingParts`, `blindCount` — every one is shown to a person |
| Refusal messages | 194 | Extracted in `validation-rules.md`. **These matter most**: a refusal is where a person needs to understand |
| Screen titles | 364 | |
| Component labels | 62 | Only where a screen names one; most are generated |
| **Total** | **3,088** | |

## Two things the count changes

**Enum labels are not free.** 1,224 of them, and each is a word a user reads — `awaitingParts`
renders as *Awaiting parts* in English and needs a real translation in Arabic. **Shipping the
enum value itself is the failure mode**, and it looks fine in English right up to go-live.

**Refusal messages are the ones to translate first.** A guest or a cashier meets an interface
when it says no, and an untranslated refusal is the worst possible place to fall back to
English.

## Rules

**Keys are structural, not English.** `orders.refund.refused.periodClosed`, not
`"Cannot refund - period closed"`. An English string as a key means changing the English
changes every translation file.

**One key per meaning, not per screen.** *Cancel* on a form and *Cancel* on an order are
different words in Arabic — one abandons, one revokes — and sharing a key produces a
translation that is wrong in one of the two places.

**Plurals and gender are Arabic requirements, not niceties.** Arabic has dual as well as plural,
so a key carrying a count needs three forms rather than two, and a library that only handles
one/many will be wrong for every pair.

**Numbers, dates and currency are formatted, never translated** — see `rtl-and-theming.md`.

## What is missing

| | |
|---|---|
| **The extraction tool** | The keys are derivable; nothing derives them. A generator over `screens/`, the contracts and `states/` would produce the base file |
| **Which locales** | English and Arabic certain. **The white-label board shows a Francais tab** and nobody has confirmed it is real (CF-42) |
| **Tenant-authored content** | Pages, FAQs and policies are the tenant's to translate, not ours. The CMS must make the gap visible per locale |
| **Who translates** | A vendor, the client, or machine translation with review. Changes the timeline, not the design |
