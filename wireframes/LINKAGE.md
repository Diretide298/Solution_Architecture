# How the boards link to everything else

The boards are 364 screens of design intent. The definitions are the same 347 in YAML. **They
resolve to each other in both directions, and a checker keeps them that way.**

## The chain

    board anchor  ──►  screen definition  ──►  operations  ──►  service
                                                    │
                                                    ▼
                                              tables · stored procedure

`P07 Staff Scanner.dc.html#scn-004` is `SCN-004 Admitted`, which calls `validateAccess`, which
lives in `AccessService`, reads `access_point`, `admission_profile`, `blacklist` and
`entitlement_template`, writes `scan_event`, and is one of the ten stored procedures —
`access.sp_validate_and_record`.

## Where each link lives

| Direction | Where |
|---|---|
| Screen → board | `wireframe.board` on every screen: `wireframes/<file>#<id>` |
| Platform → board | `platform.wireframeBoard` |
| Board → screen | The anchor `id` on each frame, matched by id |
| Screen → operations | `apis[].operationId`, validated against 689 |
| Operation → tables | `handoff/api-data-lineage.json` |
| Screen → everything | **`handoff/screen-index.json`** — the join, pre-computed |

## screen-index.json

One entry per screen, keyed by id. For a design tool this is the only file needed:

```json
"SCN-004": {
  "name": "Admitted", "platform": "P07", "app": "venue-scanner",
  "route": "/access/admitted",
  "board": "wireframes/P07 Staff Scanner.dc.html#scn-004",
  "operations": ["validateAccess"],
  "services": ["AccessService"],
  "reads": ["access.access_point", "access.admission_profile", ...],
  "writes": ["access.scan_event"],
  "storedProcedures": ["access.sp_validate_and_record"],
  "offline": true
}
```

**155 of 347 have operations. 108 resolve to a table.** The rest are screens with a purpose and
no declared operation — real screens, not yet specified, and the index says so by returning
empty arrays rather than guessing.

## What the checker enforces

`tools/check-wireframes.py`:

- Every screen points at a board that exists, and at an anchor inside it. **A link to `#scn-004`
  in a board with no such anchor is a click that silently does nothing**, which is worse than no
  link at all.
- Every anchor in a board has a screen definition. A screen someone drew and nobody specified is
  the gap this exercise was closing.
- Every href inside the boards resolves — 668 of them, file and anchor both.
- A platform's board matches its code, so P07's screens cannot point at P06's board.

Verified by breaking it deliberately: pointing `SCN-004` at `#scn-999` fails with the reason,
and restoring it passes.

## Board to board

| | |
|---|---|
| Index → every board | 12 of 12 |
| **Every board → index** | **12 of 12** — added 14 August; there was no way home |
| Board → board | 5 links, on P11, P12 and P13 |

The five cross-board links are board-level **"Reaches other platforms"** panels rather than
per-screen jumps, and they are now recorded on the platform as `reachesOtherPlatforms` so the
definitions say what the boards say. `check-wireframes.py` resolves each one to a file and an
anchor.

**Nine boards have no outbound cross-link, and that is correct.** A guest-app never reaches a
back-office screen, and a cashier never reaches the platform console. Where a jump is real it
is drawn — the accreditation-web portal reaching `SCN-003` is the one worth knowing, because it
means a steward scans an accreditation-web credential on the same handheld as a guest-app ticket.

## When a board is regenerated

Anchors are derived from screen ids, so a regenerated board keeps working as long as the ids
do. **Renaming a screen id breaks both directions**, and the checker will say which — run it
after any board change.
