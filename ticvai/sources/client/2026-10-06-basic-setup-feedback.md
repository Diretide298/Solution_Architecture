# Basic setup in Venue Management: the client's feedback of 6 October 2026

> **From:** the client, before the 10:00 UAE walkthrough · **Date:** 6 October 2026 · **Filed:** 12 October 2026
> (CHG-R6-040), so the package can cite it (`ticvai/CLAUDE.md` rule 12). The quotation and the wireframe intent below are
> copied verbatim from the "ADDED 6 Oct" section of the Claude Design master command (`design-r1/COMMAND.md`, which git
> ignores). Read-only, like everything in `sources/`.

---

ADDED 6 Oct (client feedback before the 10:00 UAE walkthrough: "some of the basic setup is not there such as Departments, Sub Departments, entitlement for the tickets, and it's confusing"). Keep these in every later run:
- Organisation (proposed new screen, in Setup, not under Zones & Areas): the department -> sub-department -> outlet tree, using the package's org units (listOrgUnits, createOrgUnit, getOrgUnit, updateOrgUnit). Add, edit, move and archive, with the counts under each node (outlets, staff, products). Zones & Areas (#BO-064) keeps zones and areas only and links here. Every "choose a department" field (outlets, Rota & Scheduling #BO-055, products) reads this tree.
- Entitlements (proposed new screen, in Ticketing, not under Memberships): the list of entitlement templates first, with the products and tickets that use each. Then numbered steps: what it admits, validity (kind and offsets), re-entry, transfer, limits and blackout dates, then a check and publish. Membership Products (#BO-012) and Fast Pass lanes link to it. The ticket creator gets an "Entitlement" step that picks or creates one.
- Both follow the builder pattern: list first, steps with a live viewer, check, publish, versions. Both are in the Flows board's "set up the venue" flow.
