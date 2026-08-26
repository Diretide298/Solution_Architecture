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
  value = azurerm_redis_cache.cell.hostname
}

output "key_vault_uri" {
  value = azurerm_key_vault.cell.vault_uri
}

output "backup_storage_account" {
  value = azurerm_storage_account.backups.name
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
    redis_hostname = azurerm_redis_cache.cell.hostname
  }
}
