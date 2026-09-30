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
    # 4.53 or later: azurerm_managed_redis arrived in 4.50.0 and its public_network_access in 4.53.0.
    # Was "~> 4.0" until 30 September 2026, which also admitted versions without the resource.
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.53" }
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

  # Zone-redundant on every tier in production (ADR-0060, decided 1 October 2026). Until then the
  # shared tier was SameZone while the LLD promised zone-redundant; a shared cell holds every tenant
  # in it, so a zone loss there is the larger outage, not the smaller one. Pre-production runs
  # without a standby (database_high_availability = false). UAE Central has no zone-redundant HA
  # (infra answers, 30 September): a production cell there cannot be stood up until it does.
  zone = "1"

  dynamic "high_availability" {
    for_each = var.database_high_availability ? [1] : []
    content {
      mode                      = "ZoneRedundant"
      standby_availability_zone = "2"
    }
  }

  maintenance_window {
    day_of_week  = var.maintenance_day
    start_hour   = var.maintenance_hour
    start_minute = 0
  }

  delegated_subnet_id           = local.database_subnet_id
  private_dns_zone_id           = var.private_dns_zone_id
  public_network_access_enabled = false

  tags = local.tags

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_postgresql_flexible_server_configuration" "extensions" {
  name      = "azure.extensions"
  server_id = azurerm_postgresql_flexible_server.primary.id
  # Every extension the migrations create (backend/tenant/001-extensions.sql). No VECTOR: vectors live in
  # Qdrant, one collection per tenant (ADR-0049, 30 September 2026).
  value     = "LTREE,BTREE_GIST,PGCRYPTO,PG_STAT_STATEMENTS"
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

  delegated_subnet_id           = local.database_subnet_id
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

  delegated_subnet_id           = local.database_subnet_id
  private_dns_zone_id           = var.private_dns_zone_id
  public_network_access_enabled = false

  tags = merge(local.tags, { Role = "reporting" })
}

# -----------------------------------------------------------------------------
# Redis. Session registry (single-session enforcement), permission set cache,
# catalogue cache, capacity display counters.
#
# Azure Managed Redis, not Azure Cache for Redis (30 September 2026). Azure
# Cache for Redis (Basic, Standard, Premium) retires on 30 September 2028 and
# new customers cannot create it from 1 October 2026. The resource it replaces
# was also P1 (6 GB) against the LLD's 13 GB. Balanced_B10 is 12 GB; high
# availability is on, and Managed Redis is zone-redundant by default.
# Access keys are off: services authenticate with Entra ID (workload identity).
# -----------------------------------------------------------------------------
resource "azurerm_managed_redis" "cell" {
  name                = "redis-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  sku_name                  = var.redis_sku
  high_availability_enabled = var.redis_high_availability
  public_network_access     = "Disabled"

  default_database {
    client_protocol                    = "Encrypted"
    eviction_policy                    = "VolatileLRU"
    access_keys_authentication_enabled = false
  }

  tags = local.tags
}

resource "azurerm_private_endpoint" "redis" {
  count = local.has_private_endpoint_subnet ? 1 : 0

  name                = "pe-redis-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location
  subnet_id           = local.private_endpoint_subnet_id

  private_service_connection {
    name                           = "redis"
    private_connection_resource_id = azurerm_managed_redis.cell.id
    subresource_names              = ["redisEnterprise"]
    is_manual_connection           = false
  }

  dynamic "private_dns_zone_group" {
    # privatelink.redis.azure.net, owned by the hub or platform subscription.
    for_each = var.redis_private_dns_zone_id == null ? [] : [var.redis_private_dns_zone_id]
    content {
      name                 = "redis"
      private_dns_zone_ids = [private_dns_zone_group.value]
    }
  }

  tags = local.tags
}

# -----------------------------------------------------------------------------
# Compute. Stateless services; session state lives in Redis, never in-process.
#
# Azure CNI Overlay (30 September 2026): nodes take VNet addresses, pods take
# addresses from pod_cidr, outside the VNet. Each pool has its own subnet
# (LLD, Network). Egress leaves through the NAT Gateway's one static IP, which
# payment and e-invoicing providers allow-list; the NAT Gateway must be
# associated with every node subnet before the cluster is created (network.tf
# does this when the module owns the network).
#
# Ingress: a Gateway API ingress, not NGINX (ingress-nginx is out of
# maintenance; the App Routing add-on's NGINX is supported only through
# November 2026). It is installed at bootstrap, not here. Its gateway pods run
# on the system pool and must tolerate CriticalAddonsOnly, because that pool is
# tainted by only_critical_addons_enabled.
#
# East-west rules (workload -> data, AI -> Qdrant) are Cilium network policies,
# not NSGs between node subnets: ingress pods and CoreDNS on the system pool
# must reach every node, and an NSG per node subnet would break that.
# -----------------------------------------------------------------------------
resource "azurerm_kubernetes_cluster" "cell" {
  count = local.is_dedicated ? 1 : 0

  name                = "aks-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location
  dns_prefix          = "ticvai-${local.cell_name}"
  sku_tier            = "Standard"

  default_node_pool {
    name                         = "system"
    vm_size                      = var.system_node_size
    auto_scaling_enabled         = true
    min_count                    = 2
    max_count                    = 4
    zones                        = var.zones
    vnet_subnet_id               = local.aks_subnet_ids.system
    only_critical_addons_enabled = true
  }

  identity { type = "SystemAssigned" }

  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    network_policy      = "cilium"
    network_data_plane  = "cilium"
    pod_cidr            = var.pod_cidr
    service_cidr        = var.service_cidr
    dns_service_ip      = var.dns_service_ip
    outbound_type       = "userAssignedNATGateway"
  }

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  tags = local.tags

  depends_on = [azurerm_subnet_nat_gateway_association.aks]
}

resource "azurerm_kubernetes_cluster_node_pool" "workload" {
  count = local.is_dedicated ? 1 : 0

  name                  = "workload"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.cell[0].id
  vm_size               = var.workload_node_size

  auto_scaling_enabled = true
  min_count            = var.workload_min_nodes
  max_count            = var.workload_max_nodes
  zones                = var.zones
  vnet_subnet_id       = local.aks_subnet_ids.workload

  tags = local.tags
}

# AI pool: ticvai-ai, the embedding model and the reranker (CPU).
resource "azurerm_kubernetes_cluster_node_pool" "ai" {
  count = local.is_dedicated ? 1 : 0

  name                  = "ai"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.cell[0].id
  vm_size               = var.ai_node_size

  auto_scaling_enabled = true
  min_count            = var.ai_min_nodes
  max_count            = var.ai_max_nodes
  zones                = var.zones
  vnet_subnet_id       = local.aks_subnet_ids.ai
  node_labels          = { "ticvai.io/pool" = "ai" }
  node_taints          = ["ticvai.io/pool=ai:NoSchedule"]

  tags = local.tags
}

# Data pool, part 1: Qdrant, one node per zone, replication factor 2 (ADR-0049).
# Self-hosted open-source Qdrant from the official Helm chart, installed at bootstrap.
resource "azurerm_kubernetes_cluster_node_pool" "qdrant" {
  count = local.is_dedicated ? 1 : 0

  name                  = "qdrant"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.cell[0].id
  vm_size               = var.qdrant_node_size
  node_count            = var.qdrant_nodes
  zones                 = var.zones
  vnet_subnet_id        = local.aks_subnet_ids.data
  node_labels           = { "ticvai.io/pool" = "data", "ticvai.io/store" = "qdrant" }
  node_taints           = ["ticvai.io/pool=data:NoSchedule"]

  tags = local.tags
}

# Data pool, part 2: the broker, only while it is self-run on AKS (RabbitMQ Cluster
# Operator, or a Kafka operator). A managed broker (CloudAMQP, Event Hubs) removes
# this pool and adds a private endpoint in snet-private-endpoints (ADR-0057).
resource "azurerm_kubernetes_cluster_node_pool" "broker" {
  count = local.is_dedicated && var.broker_self_hosted ? 1 : 0

  name                  = "broker"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.cell[0].id
  vm_size               = var.broker_node_size
  node_count            = var.broker_nodes
  zones                 = var.zones
  vnet_subnet_id        = local.aks_subnet_ids.data
  node_labels           = { "ticvai.io/pool" = "data", "ticvai.io/store" = "broker" }
  node_taints           = ["ticvai.io/pool=data:NoSchedule"]

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
