output "cell_name" {
  value = local.cell_name
}

output "primary_fqdn" {
  value = azurerm_postgresql_flexible_server.primary.fqdn
}

output "replica_fqdns" {
  value = [for r in azurerm_postgresql_flexible_server.replica : r.fqdn]
}

output "reporting_fqdn" {
  value = try(azurerm_postgresql_flexible_server.reporting[0].fqdn, null)
}

output "redis_hostname" {
  value = azurerm_managed_redis.cell.hostname
}

output "redis_port" {
  value = azurerm_managed_redis.cell.default_database[0].port
}

output "vnet_id" {
  description = "Link the private DNS zones to this VNet."
  value       = try(azurerm_virtual_network.cell[0].id, null)
}

output "nat_egress_ip" {
  description = "The one static egress IP payment and e-invoicing providers allow-list."
  value       = try(azurerm_public_ip.nat[0].ip_address, null)
}

output "key_vault_uri" {
  value = azurerm_key_vault.cell.vault_uri
}

output "backup_storage_account" {
  value = azurerm_storage_account.backups.name
}

output "replica_floors" {
  description = "Minimum replicas per deployable (ADR-0061), for the bootstrap Helm values."
  value       = var.replica_floors
}

output "kubernetes_cluster_id" {
  value = try(azurerm_kubernetes_cluster.cell[0].id, null)
}

output "control_plane_registration" {
  description = "Payload the Control Plane stores against this tenant's region record."
  value = {
    tenant_id      = var.tenant_id
    jurisdiction   = var.jurisdiction
    tier           = var.tier
    cell_name      = local.cell_name
    location       = var.location
    primary_fqdn   = azurerm_postgresql_flexible_server.primary.fqdn
    redis_hostname = azurerm_managed_redis.cell.hostname
  }
}
