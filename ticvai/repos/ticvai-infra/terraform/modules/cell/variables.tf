variable "tenant_id" {
  type        = string
  description = "TICVAI tenant UUID. Recorded in the Control Plane registry."
}

variable "tenant_slug" {
  type        = string
  description = "Short lowercase tenant identifier used in resource names."
  validation {
    condition     = can(regex("^[a-z0-9]{2,16}$", var.tenant_slug))
    error_message = "tenant_slug must be 2-16 lowercase alphanumeric characters."
  }
}

variable "jurisdiction" {
  type        = string
  description = "ISO 3166-1 alpha-2 country code this cell serves. A cell never spans jurisdictions."
  validation {
    condition     = can(regex("^[a-z]{2}$", var.jurisdiction))
    error_message = "jurisdiction must be a two-letter lowercase country code, e.g. ae, om."
  }
}

variable "tier" {
  type        = string
  description = "shared | dedicated | isolated | client_hosted"
  validation {
    condition     = contains(["shared", "dedicated", "isolated", "client_hosted"], var.tier)
    error_message = "tier must be one of: shared, dedicated, isolated, client_hosted."
  }
}

variable "location" {
  type        = string
  description = "Cloud region. MUST be in-jurisdiction. Verify hyperscaler presence before assuming availability."
}

variable "azure_tenant_id" { type = string }

variable "database_sku" {
  type    = string
  default = "GP_Standard_D4ds_v5"
  description = "Sized to tenant aggregate load with correlated venue peaks, not per-venue load."
}

variable "database_storage_mb" {
  type    = number
  default = 262144
}

variable "max_connections" {
  type        = string
  default     = "500"
  description = "PgBouncer in transaction mode sits in front. Direct connections are capped per service."
}

variable "read_replica_count" {
  type    = number
  default = 2
  validation {
    condition     = var.read_replica_count >= 0 && var.read_replica_count <= 5
    error_message = "Replicas give diminishing returns past 5."
  }
}

variable "enable_reporting_replica" {
  type        = bool
  default     = true
  description = "Dedicated lag-tolerant replica. Reporting must never touch OLTP replicas."
}

variable "backup_retention_days" {
  type    = number
  default = 35
}

variable "geo_redundant_backup_enabled" {
  type        = bool
  default     = false
  description = "Only enable where the paired region is IN THE SAME JURISDICTION. Verify before setting true."
}

variable "maintenance_day" {
  type    = number
  default = 2
}
variable "maintenance_hour" {
  type    = number
  default = 2
}

variable "redis_sku" {
  type        = string
  default     = "Balanced_B10"
  description = "Azure Managed Redis SKU. Balanced_B10 (12 GB) for production; Balanced_B1 for pre-production."
}
variable "redis_high_availability" {
  type        = bool
  default     = true
  description = "Two nodes, zone-redundant. false only for pre-production. Changing it recreates the cache."
}
variable "redis_private_dns_zone_id" {
  type        = string
  default     = null
  description = "privatelink.redis.azure.net zone for the Redis private endpoint."
}
variable "system_node_size" {
  type    = string
  default = "Standard_D4s_v5"
}
variable "workload_node_size" {
  type    = string
  default = "Standard_D8s_v5"
}
variable "workload_min_nodes" {
  type    = number
  default = 3
}
variable "workload_max_nodes" {
  type    = number
  default = 20
}
variable "ai_node_size" {
  type    = string
  default = "Standard_D8s_v5"
}
variable "ai_min_nodes" {
  type    = number
  default = 2
}
variable "ai_max_nodes" {
  type    = number
  default = 4
}
variable "qdrant_node_size" {
  type    = string
  default = "Standard_E4s_v5"
}
variable "qdrant_nodes" {
  type        = number
  default     = 3
  description = "One per zone, replication factor 2 (ADR-0049)."
}
variable "broker_self_hosted" {
  type        = bool
  default     = true
  description = "false once the client picks a managed broker (CloudAMQP, Event Hubs); ADR-0057."
}
variable "broker_node_size" {
  type    = string
  default = "Standard_D2s_v5"
}
variable "broker_nodes" {
  type    = number
  default = 3
}
variable "zones" {
  type    = list(string)
  default = ["1", "2", "3"]
}

variable "create_network" {
  type        = bool
  default     = true
  description = "Dedicated and isolated cells: build the VNet, subnets, NAT Gateway and edge NSGs (network.tf)."
}
variable "vnet_address_space" {
  type    = string
  default = "10.20.0.0/16"
}
variable "address_plan" {
  type        = map(string)
  description = "Subnets created in the VNet. Mirrors SUBNETS in ticvai/tools/build-hld-lld.py; change both together."
  default = {
    "snet-ingress"           = "10.20.0.0/24"
    "snet-aks-system"        = "10.20.4.0/22"
    "snet-aks-workload"      = "10.20.8.0/21"
    "snet-aks-ai"            = "10.20.16.0/22"
    "snet-aks-data"          = "10.20.20.0/23"
    "snet-postgres"          = "10.20.24.0/24"
    "snet-private-endpoints" = "10.20.25.0/24"
    "AzureBastionSubnet"     = "10.20.26.0/26"
    "GatewaySubnet"          = "10.20.27.0/27"
  }
}
variable "existing_subnet_ids" {
  type        = map(string)
  default     = {}
  description = "When create_network is false: keys system, workload, ai, data, private_endpoints."
}
variable "database_subnet_id" {
  type        = string
  default     = null
  description = "Delegated PostgreSQL subnet when the module does not own the network (shared tier)."
}
variable "private_dns_zone_id" { type = string }
variable "pod_cidr" {
  type        = string
  default     = "10.244.0.0/16"
  description = "CNI Overlay pod range, outside the VNet. Must not overlap a venue LAN on the VPN; 100.64.0.0/16 if in doubt."
}
variable "service_cidr" {
  type    = string
  default = "10.100.0.0/16"
}
variable "dns_service_ip" {
  type    = string
  default = "10.100.0.10"
}

variable "tags" {
  type    = map(string)
  default = {}
}
