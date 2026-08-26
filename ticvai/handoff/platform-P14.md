# P14 Developer — platform

**Derived.** `python3 tools/derive-platform.py P14`. App `developer-portal-web` · partner · web

| | |
|---|---|
| Screens | 8 |
| Operations | 21 |
| Contracts | 1 |
| Modules | 1 |
| Undrawn | 0 |
| Operations with no screen | 1 |
| Waves | wave2 7 · wave3 1 |

## Gaps

### 1 operations with no screen here

**In a contract this platform uses, callable by its audience, and reaching no screen on any platform serving that audience.** Either a screen is missing or the endpoint should not exist — and the second is worth considering first.

| Operation | Contract | | |
|---|---|---|---|
| `issueApiToken` | public-api | POST | Exchange a credential for an access token |

### 1 modules split across waves

**A platform that sells in one wave and cannot refund until a later one can take money and not give it back.** Not always wrong — worth a look each time.

- **Developer & API** — waves 2, 3

## Modules

| Module | Screens | Waves |
|---|---|---|
| Developer & API | 8 | 2, 3 |

## Screens

| | Name | Module | Wave | Ops | Drawn |
|---|---|---|---|---|---|
| `DEV-001` | API Reference | Developer & API | 2 | 1 | yes |
| `DEV-002` | Register & Organisation | Developer & API | 2 | 2 | yes |
| `DEV-003` | Clients & Credentials | Developer & API | 2 | 4 | yes |
| `DEV-004` | Sandbox | Developer & API | 2 | 3 | yes |
| `DEV-005` | Webhooks | Developer & API | 2 | 4 | yes |
| `DEV-006` | Usage & Limits | Developer & API | 2 | 1 | yes |
| `DEV-007` | Marketplace Listing | Developer & API | 3 | 2 | yes |
| `DEV-008` | Programme Administration | Developer & API | 2 | 4 | yes |

