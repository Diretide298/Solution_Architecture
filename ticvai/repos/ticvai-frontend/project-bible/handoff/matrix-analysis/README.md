# Matrix analysis

**The prerequisite pass, run before the requirement walk began on 18 August.** These five
artefacts established what the matrix actually contains, and two of them produced conflicts.

| File | What it is |
|---|---|
| `TICVAI_section_register.csv` / `.json` | Every section in the matrix with its row span and count. **146 sections, not 147** — the extra was a phantom orphan at row 1171 |
| `TICVAI_ref_collisions.csv` | **28 reference collision pairs — CF-120.** Two different requirements sharing one reference number, across 5.5, 5.6, 8.1, 8.3 and 22.3 |
| `TICVAI_domain_drift_scan.csv` | **Sub-domain labels drift from their content throughout the matrix.** 2.6 labelled *Call Center Sales* is the B2C website; 4.2 labelled *Promotions* is payments; 7.1 labelled *Retail POS* is RBAC; 12.1 labelled *Reporting and Dashboards* is accreditation |
| `TICVAI_canonical_section_map.csv` | The corrected mapping — what each section actually covers, used throughout the walk |

## Why these matter to anyone resuming

**A reference number alone does not identify a requirement.** 28 pairs collide, and the walk
handled them by suffixing the second block (`5.5.1b`, `8.3.55b`, `22.3.1b`) in
`traceability.json` while keeping `matrixRef` unsuffixed. Any analysis keyed on the raw
reference will silently merge two different requirements — this is how sixteen journey
automation requirements at 22.3b came to share numbers with case management.

**The section labels cannot be trusted.** Reading domain 4 as *Bundles and Promotions* would
miss that 4.2 is the payments section and 4.4 is retail POS and inventory. The canonical map
is the one to use.

`tools/scan-domain-drift.py` regenerates the drift scan. `sources/requirements/reference-map.json`
holds the resolved collision mapping used by the checkers.
