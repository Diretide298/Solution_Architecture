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

variable "database_high_availability" {
  type        = bool
  default     = true
  description = "Zone-redundant standby for the primary, on every tier (ADR-0060, 1 October 2026). false only for pre-production."
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
# The AI GPU node pool (CHG-R11-001; CHG-R4-008): one node without HA, two with HA (one per zone).
variable "ai_gpu_enabled" {
  type        = bool
  default     = true
  description = "The AI GPU node pool: BGE-M3, the reranker, Presidio and the Arabic NER; never an LLM (CHG-R11-001)."
}
variable "ai_gpu_node_size" {
  type    = string
  default = "Standard_NV6ads_A10_v5"
}
variable "ai_gpu_nodes" {
  type        = number
  default     = 1
  description = "1 without HA, 2 with HA (one per zone)."
  validation {
    condition     = var.ai_gpu_nodes >= 1 && var.ai_gpu_nodes <= 2
    error_message = "The AI GPU pool has one node without HA and two with HA (CHG-R11-001)."
  }
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

# Replica floors per deployable (ADR-0055 five units, ADR-0061 floors, accepted 1 October 2026). A floor
# is survivability, not load: enough replicas to lose one zone and keep serving. Above it each deployable
# autoscales on requests per second (ADR-0032); there is no maximum here. The bootstrap Helm values read
# this output (replica_floors) as each Deployment's minReplicas. The same numbers are DEPLOYABLE_FLOORS and
# AI_PROCESS_GROUP_FLOORS in ticvai/tools/derive-sizing.py; change both together. A large cell sets
# ai-realtime to 3 (AI design 4.3). A burst environment does not use these: its floor is the expected
# peak (ADR-0035).
variable "replica_floors" {
  type = map(number)
  default = {
    "commerce"       = 3 # one per zone: the sale path survives a zone loss without a cold start
    "access"         = 2 # cloud side only; the gate decides locally (ADR-0013)
    "operations"     = 2 # back office tolerates a short scale-out
    "workers"        = 2 # relay leases fail over between replicas (ADR-0058)
    "ai-realtime"    = 2 # fraud scoring, recommendations; fail open
    "ai-interactive" = 1 # assistants tolerate a short outage
    "ai-batch"       = 0 # scales from zero on queue depth
  }
  description = "Minimum replicas per deployable (ADR-0061): 12 in a small cell."
  validation {
    condition = (
      length(setsubtract(["commerce", "access", "operations", "workers", "ai-realtime", "ai-interactive", "ai-batch"], keys(var.replica_floors))) == 0
      && lookup(var.replica_floors, "commerce", 0) >= 3
      && lookup(var.replica_floors, "workers", 0) >= 2
      && lookup(var.replica_floors, "access", 0) >= 2
      && lookup(var.replica_floors, "operations", 0) >= 2
      && alltrue([for v in values(var.replica_floors) : v >= 0])
    )
    error_message = "replica_floors names all seven units (commerce, access, operations, workers, ai-realtime, ai-interactive, ai-batch); commerce is at least 3 (one per zone) and access, operations and workers at least 2 (ADR-0061)."
  }
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
