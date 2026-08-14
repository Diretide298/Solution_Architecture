# Screen definitions

**One file per platform.** A team owns a platform, a platform owns a file, and two teams
never edit the same one.

    _schema.yaml        the meta-schema — every field and why it exists
    _components.yaml    the component vocabulary. A `kind` not in here fails validation
    P01-…yaml           per-platform screen definitions

    ../tools/check-screens.py

## What these are for

They sit between the page inventory and the wireframes. The inventory answers *what screens
exist*; these answer *what is on them* — regions, components, states, navigation, and the
permissions that gate each one.

A wireframe is authoritative for how a screen looks. It is a poor source for what a screen
*does*: which endpoint fills each region, what happens when that endpoint returns empty,
which permission hides a button. Those answers live here, and a designer and an engineer
reading the same file cannot drift.

This is the contract a wireframe implements, in the same sense OpenAPI is the contract an
endpoint implements.

## What validation catches

| Check | Why it matters |
|---|---|
| **Component vocabulary** | A screen calling for `fancyDatePickerV2` either needs it adding deliberately, or is asking for something the design system already has. Free-text names are how a product ends up with four date pickers |
| **operationIds resolve** | Catches a wireframe drawn against an endpoint that does not exist. The expensive one — it survives design review, survives estimation, and surfaces at build |
| **Four states** | `loading`, `empty`, `error`, and `offline` where the platform is offline-capable. The empty state is the one that reaches production unconsidered |
| **Navigation resolves** | Every entry and exit points at a screen that exists |

`operationIds` validate against all 554 in the contracts. That link is the point of the
exercise, and it caught two wrong ids on first run — `listVariants` (actually
`listProductVariants`) and `inquirePayment` (actually `inquirePaymentStatus`). Both looked
right and neither existed.

## Status

| Platform | Screens | Detail |
|---|---|---|
| P01 Guest Web Storefront | 29 | **Purchase path fully specified** (WEB-001→013) |
| P09 Platform Admin Console | 36 | Structure and open questions |
| P10 Partner & Reseller Portal | 21 | Structure and open questions |
| P11 Accreditation Portal | 8 | **Blocked** on the workshop |
| P12 Support Agent Console | 8 | Structure and open questions |

The 203 screens on platforms that have UI/UX boards are not here yet — the boards are more
detailed than these files would be, and converting them is worth doing when the wireframes
are next revised, not before.

Warnings are expected on anything not yet detailed. **Errors are not** — a TODO state is a
warning; an unknown component or a dangling operationId is a failure.

## Open questions that block work

- **Wishlist** (WEB-009) has no contract anywhere. Add it or drop the screen
- **Virtual Waiting Room** (WEB-015) is Q2 infrastructure, not the Q1 queue contract
- **Seat maps with no geometry** (WEB-007) — does the storefront fall back to a category
  list, or refuse the seated flow?
- **19 of 36 Platform Admin screens** have no contract. Thirteen are the release-management
  scope raised on 30 July that never reached a requirement
