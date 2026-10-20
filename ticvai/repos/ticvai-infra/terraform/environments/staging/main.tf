/**
 * Staging: the one shared pre-production environment (the lead, 20 October 2026, r8 causes
 * FOUNDATION-AI-C52 option B and FOUNDATION-AI-C23).
 *
 * - dev has no cloud environment: it runs on each developer's laptop with docker compose.
 * - staging runs in the Softlabs Azure subscription and Entra tenant (we host non-production ourselves),
 *   one cell in UAE North, and its Terraform state lives in a storage account in that subscription.
 * - production is hosted by the client later, from the tfvars in ../production with its own state.
 *
 * The state location is given at init time, not committed, so no account key or name leaks into the repository:
 *
 *   terraform init -backend-config=backend.hcl     # backend.hcl from backend.hcl.example, filled by the infra owner
 *   terraform plan        # azure_tenant_id and private_dns_zone_id from TF_VAR_azure_tenant_id and
 *                         # TF_VAR_private_dns_zone_id
 */

terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 4.53" }
  }

  # Azure Storage, in the Softlabs subscription; locked by blob lease. Partial configuration: the resource group,
  # storage account, container and key come from backend.hcl (see backend.hcl.example).
  backend "azurerm" {
    use_azuread_auth = true
  }
}

provider "azurerm" {
  features {}
  # The Softlabs subscription and Entra tenant, from ARM_SUBSCRIPTION_ID and ARM_TENANT_ID in the pipeline or
  # the operator's shell; never committed.
}

variable "azure_tenant_id" {
  type        = string
  description = "The Softlabs Entra tenant id (the key vault's tenant)."
}

variable "private_dns_zone_id" {
  type        = string
  description = "The private DNS zone of the PostgreSQL flexible server in the staging subscription."
}

module "cell" {
  source = "../../modules/cell"

  environment  = "staging"
  cell         = "ae1"
  jurisdiction = "ae"
  tier         = "dedicated"
  location     = "uaenorth"

  azure_tenant_id     = var.azure_tenant_id
  private_dns_zone_id = var.private_dns_zone_id

  # The costed "minimal pre-production" shape (docs/active/deployment-configs-costed.md): one of everything,
  # no high availability, no replicas, no GPU. Qdrant keeps three nodes, because SETUP-QDRANT's done-when is
  # that the cluster survives the loss of one.
  database_sku               = "GP_Standard_D2ds_v5"
  database_storage_mb        = 65536
  database_high_availability = false
  read_replica_count         = 0
  enable_reporting_replica   = false
  backup_retention_days      = 7

  redis_sku               = "Balanced_B0"
  redis_high_availability = false

  system_min_nodes    = 1
  nat_gateway_enabled = false
  workload_min_nodes  = 1
  workload_max_nodes  = 3
  ai_min_nodes        = 1
  ai_max_nodes        = 1
  ai_gpu_enabled      = false
  qdrant_enabled      = true
  qdrant_nodes        = 3
  broker_nodes        = 1

  tags = { CostCentre = "softlabs-preproduction" }
}

output "cell_name" {
  value = module.cell.cell_name
}
