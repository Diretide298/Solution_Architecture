# P11 Accreditation Web — platform

**Derived.** `python3 tools/derive-platform.py P11`. App `accreditation-web` · public · web

| | |
|---|---|
| Screens | 8 |
| Operations | 3 |
| Contracts | 2 |
| Modules | 4 |
| Undrawn | 0 |
| Operations with no screen | 0 |
| Waves | wave3 8 |

## Gaps

**None derivable.** Every operation this platform's contracts expose to its audience reaches a screen, every module spans one wave, everything is drawn, and no flow names a screen that does not exist.

## Modules

| Module | Screens | Waves |
|---|---|---|
| Applicant Journey | 3 | 3 |
| approvals | 3 | 3 |
| queue | 1 | 3 |
| Reviewer (Internal) | 1 | 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `ACC-001` | Landing / Programme Overview | Applicant Journey | 3 | 0 | yes |
| `ACC-002` | Registration Form | approvals | 3 | 1 | yes |
| `ACC-003` | Application Review & Submit | Applicant Journey | 3 | 0 | yes |
| `ACC-004` | Application Status Tracking | Applicant Journey | 3 | 0 | yes |
| `ACC-005` | Accreditation Badge | approvals | 3 | 1 | yes |
| `ACC-006` | Reviewer Queue | queue | 3 | 1 | yes |
| `ACC-007` | Reviewer Application Detail | approvals | 3 | 2 | yes |
| `ACC-008` | Credential Register | Reviewer (Internal) | 3 | 0 | yes |

