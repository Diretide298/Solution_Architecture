# ticvai-infra

Cell provisioning and migration orchestration.

## Why this repo is first

The migration orchestrator is the most load-bearing component in the platform.
It deploys cells, fans migrations out across them, tracks per-cell schema
versions and gates progressive rollout. Every subsequent schema change depends
on it existing. It has been flagged unowned since 30 July 2026.

## Layout

    terraform/modules/cell            one tenant in one jurisdiction
    terraform/modules/control-plane   global registry, licensing, routing
    terraform/modules/network         per-cell VNet, subnets, private DNS
    terraform/environments/cells      one tfvars file per cell
    k8s/base + overlays               workloads, per-cell overlay
    ci/                               rollout pipeline, canary gating
    runbooks/                         DR, restore drills, cell promotion

## Rollout order

Never all cells at once. Canary cell, then 10%, then the rest, gated on health.
Version skew between cells is expected and acceptable — the Control Plane tracks
per-cell version, and contracts tolerate N-3 minor versions.

## Restore drills

An untested backup is not a backup. Restores run monthly, automated, into an
isolated environment. A single-tenant restore must not disturb other tenants:
restore to a scratch instance, then logically copy the tenant schema back.
