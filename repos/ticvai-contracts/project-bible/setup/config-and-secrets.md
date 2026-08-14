# Config & Secrets

> **Purpose:** Where configuration lives  
> **Owner:** Dinesh  
> **Status:** **Week 1**


## Key vault per cell

A compromise is contained to one tenant. The isolated tier can hold customer-managed keys. Vault references, never inline values.

## Build-time vs runtime — guest apps

This distinction costs real money. **Every build-time value change costs a store review cycle.**

| Build-time — rebuild + review | Runtime — config API + OTA |
|---|---|
| Bundle ID, app name | Colour palette, fonts, logos |
| Icon, splash | Banner and hero imagery |
| Signing identity | Copy, translations |
| **Tenant ID** | **Module visibility** (licensing) |
| Push certificates | Venue list, catalogue, layouts |
| Deep-link domains | Feature flags, promotions |

Everything a tenant admin touches day to day is on the right. **A rebrand is a config publish, not a release.**

## Rules

- No secrets, credentials, connection strings or tenant IDs in source
- Local development uses a `.env.local` that is gitignored and contains only synthetic values
- Rotation is scheduled, not incident-driven
- Gateway credentials, signing keys and vector store credentials live in the per-cell vault
- Configuration that varies per cell lives in the Control Plane, not in the deployment
