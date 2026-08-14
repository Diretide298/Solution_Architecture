/**
 * Cell module.
 *
 * One instance of this module is one deployment cell: a single tenant in a
 * single jurisdiction (Project Direction §3.3.1). Splitting at Region is
 * mandatory rather than load-driven — a venue operating in a jurisdiction
 * expects its infrastructure in that jurisdiction.
 *
 * Everything holding personal data stays in-region, including backups and DR
 * replicas (§3.3.10). "Cross-region DR" means a second region within the same
 * jurisdiction, not the nearest cloud region.
 */

terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.0" }
  }
}

locals {
  cell_name = "${var.tenant_slug}-${var.jurisdiction}"

  tags = merge(var.tags, {
    Cell         = local.cell_name
    TenantId     = var.tenant_id
    Jurisdiction = var.jurisdiction
    Tier         = var.tier
    ManagedBy    = "terraform"
  })

  # Dedicated and isolated tiers get their own everything. Shared tier tenants
  # land on a pre-existing cell and only get a database.
  is_dedicated = contains(["dedicated", "isolated"], var.tier)
}

resource "azurerm_resource_group" "cell" {
  name     = "rg-ticvai-${local.cell_name}"
  location = var.location
  tags     = local.tags
}

# -----------------------------------------------------------------------------
# Database. One primary per cell, read replicas for scale, dedicated
# lag-tolerant replica for reporting.
#
# Reporting is physically separated because the single most likely cause of a
# venue spike taking down a tenant is a month-end report against the primary.
# -----------------------------------------------------------------------------
resource "azurerm_postgresql_flexible_server" "primary" {
  name                = "psql-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  version    = "16"
  sku_name   = var.database_sku
  storage_mb = var.database_storage_mb

  # PITR retention. The 7-year audit trail (31 Jul 2026) is satisfied by the
  # append-only ledger design, not by backup retention — do not conflate them.
  backup_retention_days        = var.backup_retention_days
  geo_redundant_backup_enabled = var.geo_redundant_backup_enabled

  high_availability {
    mode                      = local.is_dedicated ? "ZoneRedundant" : "SameZone"
    standby_availability_zone = local.is_dedicated ? "2" : null
  }

  maintenance_window {
    day_of_week  = var.maintenance_day
    start_hour   = var.maintenance_hour
    start_minute = 0
  }

  delegated_subnet_id = var.database_subnet_id
  private_dns_zone_id = var.private_dns_zone_id
  public_network_access_enabled = false

  tags = local.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_postgresql_flexible_server_configuration" "extensions" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.primary.id
  value     = "LTREE,PGCRYPTO,PG_STAT_STATEMENTS,VECTOR"
}

resource "azurerm_postgresql_flexible_server_configuration" "max_connections" {
  name      = "max_connections"
  server_id = azurerm_postgresql_flexible_server.primary.id
  value     = var.max_connections
}

# Read replicas. Reads route here by default; access validation deliberately
# does not (§3.3.8) — a ticket sold at the gate must not be refused seconds
# later by a lagging replica.
resource "azurerm_postgresql_flexible_server" "replica" {
  count = var.read_replica_count

  name                = "psql-ticvai-${local.cell_name}-ro${count.index + 1}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  create_mode      = "Replica"
  source_server_id = azurerm_postgresql_flexible_server.primary.id
  version          = "16"

  delegated_subnet_id           = var.database_subnet_id
  private_dns_zone_id           = var.private_dns_zone_id
  public_network_access_enabled = false

  tags = merge(local.tags, { Role = "read-replica" })
}

# Dedicated reporting replica. Granted no write access anywhere by the
# ticvai_reporting role created in the baseline migration.
resource "azurerm_postgresql_flexible_server" "reporting" {
  count = var.enable_reporting_replica ? 1 : 0

  name                = "psql-ticvai-${local.cell_name}-rpt"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  create_mode      = "Replica"
  source_server_id = azurerm_postgresql_flexible_server.primary.id
  version          = "16"

  delegated_subnet_id           = var.database_subnet_id
  private_dns_zone_id           = var.private_dns_zone_id
  public_network_access_enabled = false

  tags = merge(local.tags, { Role = "reporting" })
}

# -----------------------------------------------------------------------------
# Redis. Session registry (single-session enforcement), permission set cache,
# catalogue cache, capacity display counters.
# -----------------------------------------------------------------------------
resource "azurerm_redis_cache" "cell" {
  name                = "redis-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  capacity            = var.redis_capacity
  family              = local.is_dedicated ? "P" : "C"
  sku_name            = local.is_dedicated ? "Premium" : "Standard"
  non_ssl_port_enabled = false
  minimum_tls_version = "1.2"

  redis_configuration {
    maxmemory_policy = "volatile-lru"
  }

  tags = local.tags
}

# -----------------------------------------------------------------------------
# Compute. Stateless services; session state lives in Redis, never in-process.
# -----------------------------------------------------------------------------
resource "azurerm_kubernetes_cluster" "cell" {
  count = local.is_dedicated ? 1 : 0

  name                = "aks-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location
  dns_prefix          = "ticvai-${local.cell_name}"

  default_node_pool {
    name                 = "system"
    vm_size              = var.system_node_size
    auto_scaling_enabled = true
    min_count            = 2
    max_count            = 4
    vnet_subnet_id       = var.compute_subnet_id
    only_critical_addons_enabled = true
  }

  identity { type = "SystemAssigned" }

  network_profile {
    network_plugin = "azure"
    network_policy = "cilium"
    service_cidr   = var.service_cidr
    dns_service_ip = var.dns_service_ip
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  tags = local.tags
}

resource "azurerm_kubernetes_cluster_node_pool" "workload" {
  count = local.is_dedicated ? 1 : 0

  name                  = "workload"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.cell[0].id
  vm_size               = var.workload_node_size

  auto_scaling_enabled = true
  min_count            = var.workload_min_nodes
  max_count            = var.workload_max_nodes
  vnet_subnet_id       = var.compute_subnet_id

  tags = local.tags
}

# -----------------------------------------------------------------------------
# Key vault. Per-cell so a compromise is contained to one tenant, and so the
# isolated tier can hold customer-managed keys.
# -----------------------------------------------------------------------------
resource "azurerm_key_vault" "cell" {
  name                       = substr("kv-tv-${replace(local.cell_name, "-", "")}", 0, 24)
  resource_group_name        = azurerm_resource_group.cell.name
  location                   = azurerm_resource_group.cell.location
  tenant_id                  = var.azure_tenant_id
  sku_name                   = var.tier == "isolated" ? "premium" : "standard"
  purge_protection_enabled   = true
  soft_delete_retention_days = 90
  enable_rbac_authorization  = true

  tags = local.tags
}

# -----------------------------------------------------------------------------
# Storage for WAL archive and backups. In-jurisdiction, versioned, encrypted.
# -----------------------------------------------------------------------------
resource "azurerm_storage_account" "backups" {
  name                     = substr("sttv${replace(local.cell_name, "-", "")}bk", 0, 24)
  resource_group_name      = azurerm_resource_group.cell.name
  location                 = azurerm_resource_group.cell.location
  account_tier             = "Standard"
  account_replication_type = var.geo_redundant_backup_enabled ? "GZRS" : "ZRS"
  min_tls_version          = "TLS1_2"
  https_traffic_only_enabled = true

  blob_properties {
    versioning_enabled = true
    delete_retention_policy { days = var.backup_retention_days }
    container_delete_retention_policy { days = 30 }
  }

  tags = local.tags
}
