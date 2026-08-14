# Actor Register

> **Purpose:** 33 human actors, non-user humans, system actors  
> **Owner:** Chinmay  
> **Status:** Living


**Actors are compositions of capabilities, not a source of diagrams.** Flows are drawn per capability; actors validate coverage. A person selling tickets, selling food, or doing both is the same persona with different grants.

## Platform tier

| ID | Actor | Surface | Evidence |
|---|---|---|---|
| A01 | Platform Super Admin | Back office | 10 Aug §4.12; Subscription & Licensing (59) |
| A02 | Device / IT Administrator | Back office | 16.1–16.9 (60) |

## Tenant governance

| ID | Actor | Surface | Evidence |
|---|---|---|---|
| A03 | Tenant Admin | Back office | Hierarchy diagram; 10 Aug §4.1 |
| A04 | Venue Admin / Configurator | Back office | 07 Aug §§2–19 |
| A05 | Super User | Back office | Training sheet Ref 2 |
| A06 | Finance Controller *(posts)* | Back office | 07 Aug §10; 5.7, 5.12 |
| A32 | Finance Manager / Director *(approves)* | Back office | 12 Aug §15 |
| A07 | Approver *(parameterised)* | Back office + employee app | 10 Aug §5.5; 11.1.x |
| A08 | Marketing User | Back office | 7.1.12; 22.1.5 |
| A09 | Accreditation Officer | Back office | 12.1.x (58) |

A06 and A32 sit either side of a segregation-of-duties boundary — a finance user posts a voucher, a manager approves before it reaches the ledger.

A07 is **one** actor. Ops Manager, Finance and CEO perform an identical interaction; only chain position differs.

## Venue operations — selling

| ID | Actor | Surface | Evidence |
|---|---|---|---|
| A10 | Ticketing Cashier | POS | 03 Aug §2; 07 Aug §20 |
| A11 | F&B Cashier | POS | 03 Aug §§4–5 |
| A12 | Retail Cashier | POS | 31 Jul §11 |
| A13 | Universal Cashier | POS | Composition |
| A14 | Front Gate Operator *(sells + scans)* | POS + scan | 2.13.6; 3.2.17 |
| A15 | Rental Operator | POS | 7.6.14 |
| A16 | Redemption / Arcade Operator | Operator kiosk | 10.2.3, 10.2.4 |
| A17 | Membership / Annual Pass Counter | POS | 2.14.6; 3.2.43 |
| A18 | Call Centre Agent *(no till)* | Web POS | 2.8.x (67) |

## Access control

| ID | Actor | Surface | Evidence |
|---|---|---|---|
| A19 | Gate / Turnstile Scanner Operator | Dedicated scanner app | 03 Aug §12; 10 Aug §5.7 |
| A20 | Podium / Turnstile Supervisor | Handheld or turnstile keyboard | 3.2.73 |

A19 scans. A20 supervises turnstiles — lookup, override, mode switching. Different job, different device.

## Back of house

| ID | Actor | Surface | Evidence |
|---|---|---|---|
| A21 | Duty Supervisor | POS + employee app | 07 Aug §4; 5.8.8, 5.9.5, 7.1.4 |
| A22 | Venue Manager | Back office + employee app | 7.1.12 |
| A23 | Maintenance Technician | Employee app | 10 Aug §5.3 |
| A24 | Storekeeper / Procurement Officer | Employee app + back office | 10 Aug §5.4 |
| A25 | Guest Services / Lost & Found | Employee app + back office | 10 Aug §4.6, §5.6 |
| A26 | CRM Case Agent *(async, SLA)* | Back office | 22.3.3 |
| A31 | CR Representative *(live chat)* | Back office | 12 Aug §10 |

## External

| ID | Actor | Surface | Evidence |
|---|---|---|---|
| A27 | Guest (B2C) | Guest app, web, kiosk | 10 Aug §§4.1–4.12 |
| A34 | Refund Requester *(guest self-service)* | Guest app | 12 Aug §9 |
| A28 | B2B Partner Admin | B2B portal | 05 Aug §2 |
| A29 | B2B Partner Agent *(child account)* | B2B portal | 07 Aug §11 |
| A30 | Partner Developer | Developer portal | 13.1–13.3 (94) |

## Non-user humans — no login, no flows

| Category | Members | Modelling |
|---|---|---|
| Bookable staff resources | Event managers, ushers, security, performers, technical crew, mascots, hosts, drivers, instructors | `StaffResource` — skills, availability, block reasons. **Separate entity from `User`** |
| Credential holders | Contractors, vendors, media, VIPs, government | Accreditation entity → access rights |

Conflating `User` and `StaffResource` means rostering a mascot creates a login.

## System actors — sequence diagrams, not user flows

| Class | Members |
|---|---|
| Identity | UAE Pass, Azure AD, MFA, Apple ID, Google ID, Al Hosn |
| Payment | Stripe gateway + device, NI N-Genius + device, DCT |
| Messaging | WhatsApp, SMS gateway, Email gateway |
| Distribution | OTAs and resellers, channel manager |
| Venue systems | Turnstile controllers, ANPR, queue sensors, KDS, lockers, signage |
| Hardware | Emirates ID, Chainway, RFID, NFC, biometric, facial, Boca, Zebra, cash drawers |
| Platform | LLM provider, vector store, FX, SIEM, APM, ERP, wallets |

## Retired

**A33 TVM/Kiosk Supervisor** — folded into the CF-09 decision. Kiosk attendant access is a permission on a login page, assignable to any custom role, not a separate persona.
