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

variable "redis_capacity" {
  type    = number
  default = 1
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

variable "database_subnet_id"  { type = string }
variable "compute_subnet_id"   { type = string }
variable "private_dns_zone_id" { type = string }
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
