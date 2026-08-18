# Package layout

**One tree. Directories are artefact kinds, and the domains cut across them** — `ai.yaml` lives in
`contracts/`, `conversation.yaml` in `states/`, and `handoff/domain-markers.json` says which
domains each belongs to. That is why there is no `ai/` folder and no `finance/` either.

| | |
|---|---|
| `contracts/` | OpenAPI, in `spine/`, `satellite/` and `shared/`. **Authoritative** — every validator reads from here |
| `states/` | One lifecycle per file. `enumKind` says whether it anchors on a named enum or an inline `status` |
| `events/` | Publisher, payload, consumers, and which consumer is critical |
| `flows/` | Journeys. `primaryContract` and `contracts` are derived, not typed |
| `screens/` | One file per platform, `P01`–`P13` |
| `frontend/` | App manifests, derived from `screens/` |
| `wireframes/` | The boards screens anchor into |
| `docs/` | ADRs, architecture, registers, active working documents |
| `handoff/` | **Everything derived.** Nothing here is edited by hand |
| `tools/` | Validators and generators. `./tools/refresh.sh` runs the lot |
| `sources/` | The requirement matrix, MoMs, design PDFs |
| `designs/` `repos/` | Reference material |

## Directories this package does not ship

`backend/`, `viewer/` and `arabic-embed-eval/` are built outside it and are not overwritten by
unpacking this archive over an existing tree.

## The package is self-contained

`handoff/schema-reference.json` and `handoff/relationship-graph.json` were read from a sibling
`work/` directory until 18 August, so the tools resolved them in one working copy and silently
returned empty results everywhere else. **They are in the package now**, and
`python3 tools/refresh.sh` produces identical output from a bare checkout with nothing beside it.
