# Ticketing Sales

> **Purpose:** Domain reference  
> **Owner:** Chinmay  
> **Status:** Mapped

| | |
|---|---|
| **Requirements** | 343 |
| **Sub-domains** | 12 |
| **Bounded context** | Order & Payment (spine) |
| **Capabilities** | C01, C02, C03, C04, C34, C85, C22 |
| **AI applications** | AI-04, AI-07, AI-30, AI-31, AI-40 |
| **Primary actors** | A10, A13, A14, A17, A18, A21 |
| **Wave** | 1 |

## Sub-domains

| Sub-domain | Reqs | ID prefixes |
|---|---|---|
| Sales Channels | 33 | 2.1 |
| Ticketing POS and Kiosks | 2 | 2.2 |
| Flying POS | 1 | 2.3 |
| B2B Sales | 4 | 2.4, 2.5 |
| Call Center Sales | 67 | 2.6 |
| Pricing | 67 | 2.7, 2.8 |
| Ticket Upgrades | 30 | 2.11, 2.9 |
| Digital Waiver Management | 18 | 2.10, 2.15 |
| Order Management | 36 | 2.12 |
| Front Gate Sales | 45 | 2.13 |
| Membership | 23 | 2.14 |
| Ticket Media | 17 | 2.16 |

## Notes

Front Gate Sales (45) requires sell **and** scan on one terminal. Call Center Sales is 67 reqs — larger than most domains.

## Links

[Capability register](../../registers/capabilities.md) · [Actor register](../../registers/actors.md) · [Waves](../../delivery/waves.md) · [Conflicts](../../registers/conflicts.md)
