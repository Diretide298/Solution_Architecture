# Integrations

> **Purpose:** Third-party and hardware  
> **Owner:** Chinmay  
> **Status:** Stub

194 requirements depend on external systems; 998 on hardware or on-location infrastructure.

**Standard pattern (10 Aug):** TICVAI exposes an inbound API; the client's chosen
third-party feeds into it. Direct integration with a named vendor is bespoke work, quoted
separately.

**Exception:** payment gateways require full end-to-end integration including recovery
paths, not just the happy path.

| Page | Covers |
|---|---|
| [hardware-lab](hardware-lab.md) | Devices, drivers, simulators |
| [payment](payment.md) | Gateways, terminals, status-inquiry recovery |
| [identity-providers](identity-providers.md) | UAE Pass, SSO, MFA |
| [venue-systems](venue-systems.md) | Turnstiles, queue feeds, KDS, lockers, signage |
| [distribution](distribution.md) | OTAs, resellers, channel management |
