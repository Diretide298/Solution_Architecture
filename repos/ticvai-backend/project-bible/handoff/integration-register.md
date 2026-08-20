# Integration register

**35 integrations named in the matrix — 19 software, 16 hardware.** Counted as "roughly 35"
since 30 July and never itemised against the contracts until 14 August.

Tested by searching every contract for each named system. A "no trace" result means nothing in
689 operations, no enum value, and no adaptor mentions it.

## Software — 19

| | System | Contract | State |
|---|---|---|---|
| 1 | UAE Pass | `identity` | Covered — SSO provider, OIDC |
| 2 | **DET Integration** | — | 🔴 **No trace.** Dubai Economy & Tourism |
| 3 | **DCT Integration** | — | 🔴 **No trace.** Dept of Culture & Tourism |
| 4 | WhatsApp | `marketing-crm` | Covered — dispatch channel |
| 5 | SMS Gateway | `marketing-crm` | Covered |
| 6 | Email Gateway | `marketing-crm` | Covered |
| 7 | **Stripe Payment Gateway** | `orders` | 🟡 **Payment exists; the provider does not** |
| 8 | **Stripe Payment Device** | `tenancy` | 🟡 `paymentTerminal` device kind only |
| 9 | Single Sign On | `identity` | Covered — OIDC and SAML2 |
| 10 | Azure Active Directory | `identity` | Covered — an SSO provider |
| 11 | MFA | `identity` | Covered — TOTP, SMS, email, biometric, hardware token |
| 12 | Resellers & OTA | `orders`, `subscription` | Covered — partner portal, allocations, credit |
| 13 | **SIEM** | — | 🔴 **No trace.** Security event forwarding |
| 14 | Application Monitoring | `subscription` | Covered — cell health, capacity |
| 15 | **Al Hosn App** | — | 🔴 **No trace.** UAE health pass |
| 16 | Apple ID | `identity` | Covered — guest-app social login |
| 17 | Google ID | `identity` | Covered — guest-app social login |
| 18 | **NI Payment Gateway** | — | 🔴 **No trace.** Network International |
| 19 | **NI Payment Device** | — | 🔴 **No trace** |

## Hardware — 16

All sixteen resolve to a `DeviceKind` and therefore to the driver pattern in ADR-0015 — a
named vendor is a driver behind a stable shape, not a core change.

`receiptPrinter` · `ticketPrinter` · `labelPrinter` · `cashDrawer` · `barcodeScanner` ·
`rfidReader` · `nfcReader` · `cardReader` · `idReader` · `biometricReader` · `accessReader` ·
`paymentTerminal` · `customerDisplay` · `signageDisplay` · `kitchenDisplay` ·
`turnstileController` · `wristbandEncoder` · `signaturePad` · `scale` · `camera`

Boca maps to `ticketPrinter`, Zebra Bluetooth to `labelPrinter`, Chainway to a handheld running
the venue-scanner app, Emirates ID to `idReader`, facial readers to `biometricReader`.

---

## The finding this exercise produced

**Two payment gateways are named and the contracts have no concept of a payment provider.**

There is no `PaymentProvider` enum, no provider field on `Payment`, and no way to say which
gateway a payment went through. That breaks settlement: `ingestSettlementFile` matches an
acquirer's file against payments, and without a provider on the payment there is nothing to
match on except amount and time, which is how two transactions of the same value in the same
minute get reconciled to each other.

Stripe and Network International are both named, so this is not hypothetical — the platform
will run two providers from day one.

## Four integrations with no trace at all

**DET and DCT** are the Dubai and Abu Dhabi tourism authorities. Both are almost certainly
mandatory reporting rather than optional — a venue in either emirate files visitor data. Nobody
has asked what the interface is.

**Al Hosn** is the UAE health pass. Likely dormant, and worth confirming rather than assuming.

**SIEM** is security event forwarding. It has no contract because security events have no
catalogue — `identity.authz_audit` exists and nothing ships it anywhere.

## What this changes

| | |
|---|---|
| `PaymentProvider` on `Payment` | Required before settlement can reconcile |
| DET, DCT | Ask what the interface is. If it is regulatory reporting, it is not optional |
| Al Hosn | Confirm in or out |
| SIEM | Needs a security event stream, which needs the audit register (still open) |

Hardware needs nothing new. The device driver pattern already covers all sixteen, which is
what ADR-0015 was for.
