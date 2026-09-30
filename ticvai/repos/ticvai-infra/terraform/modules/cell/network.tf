# -----------------------------------------------------------------------------
# Network. The cell's VNet, per the LLD's address plan (30 September 2026).
#
# **The address plan mirrors SUBNETS in ticvai/tools/build-hld-lld.py** (the
# LLD's Network table and the cost workbook's Network sheet). Change both
# together. Reserved ranges that are not created here:
#   snet-agc   10.20.2.0/24   only if Application Gateway for Containers is chosen
#   snet-jump  10.20.28.0/27  only if the AKS API server is private and Bastion stays Basic
# Pods (CNI Overlay) take var.pod_cidr, outside the VNet; services take
# var.service_cidr. Neither may overlap a peered VNet, the client's ranges or a
# venue LAN reached over the site-to-site VPN.
#
# Created only for dedicated and isolated cells when create_network is true.
# Otherwise the caller passes existing_subnet_ids (and database_subnet_id).
#
# NSGs sit at the edges only: Postgres, private endpoints and ingress. Node
# subnets get none; east-west rules are Cilium network policies (main.tf).
# AzureBastionSubnet gets no NSG here: Azure requires a fixed rule set on it,
# and Bastion works without one.
#
# The caller still links the private DNS zones (PostgreSQL, Redis, Key Vault,
# Blob, registry) to this VNet: output vnet_id.
# -----------------------------------------------------------------------------

locals {
  create_network = local.is_dedicated && var.create_network

  aks_subnet_names = {
    system   = "snet-aks-system"
    workload = "snet-aks-workload"
    ai       = "snet-aks-ai"
    data     = "snet-aks-data"
  }

  aks_subnet_ids = local.create_network ? {
    for k, n in local.aks_subnet_names : k => azurerm_subnet.cell[n].id
    } : {
    for k, n in local.aks_subnet_names : k => lookup(var.existing_subnet_ids, k, null)
  }

  database_subnet_id = local.create_network ? azurerm_subnet.cell["snet-postgres"].id : var.database_subnet_id

  has_private_endpoint_subnet = local.create_network || lookup(var.existing_subnet_ids, "private_endpoints", null) != null
  private_endpoint_subnet_id  = local.create_network ? azurerm_subnet.cell["snet-private-endpoints"].id : lookup(var.existing_subnet_ids, "private_endpoints", null)

  aks_node_ranges = [for n in values(local.aks_subnet_names) : var.address_plan[n]]
}

resource "azurerm_virtual_network" "cell" {
  count = local.create_network ? 1 : 0

  name                = "vnet-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location
  address_space       = [var.vnet_address_space]

  tags = local.tags
}

resource "azurerm_subnet" "cell" {
  for_each = local.create_network ? var.address_plan : {}

  name                 = each.key
  resource_group_name  = azurerm_resource_group.cell.name
  virtual_network_name = azurerm_virtual_network.cell[0].name
  address_prefixes     = [each.value]

  # Front Door reaches the ingress through a Private Link service in snet-ingress.
  private_link_service_network_policies_enabled = each.key == "snet-ingress" ? false : true

  # Private endpoints honour the subnet's NSG only when this is enabled.
  private_endpoint_network_policies = each.key == "snet-private-endpoints" ? "NetworkSecurityGroupEnabled" : "Disabled"

  dynamic "delegation" {
    for_each = each.key == "snet-postgres" ? [1] : []
    content {
      name = "postgres"
      service_delegation {
        name    = "Microsoft.DBforPostgreSQL/flexibleServers"
        actions = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
      }
    }
  }
}

# -----------------------------------------------------------------------------
# Egress: one static IP for provider allow-lists. AKS uses it through
# outbound_type = "userAssignedNATGateway".
# -----------------------------------------------------------------------------
resource "azurerm_public_ip" "nat" {
  count = local.create_network ? 1 : 0

  name                = "pip-nat-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = local.tags
}

resource "azurerm_nat_gateway" "cell" {
  count = local.create_network ? 1 : 0

  name                    = "nat-ticvai-${local.cell_name}"
  resource_group_name     = azurerm_resource_group.cell.name
  location                = azurerm_resource_group.cell.location
  sku_name                = "Standard"
  idle_timeout_in_minutes = 4

  tags = local.tags
}

resource "azurerm_nat_gateway_public_ip_association" "cell" {
  count = local.create_network ? 1 : 0

  nat_gateway_id       = azurerm_nat_gateway.cell[0].id
  public_ip_address_id = azurerm_public_ip.nat[0].id
}

resource "azurerm_subnet_nat_gateway_association" "aks" {
  for_each = local.create_network ? local.aks_subnet_names : {}

  subnet_id      = azurerm_subnet.cell[each.value].id
  nat_gateway_id = azurerm_nat_gateway.cell[0].id
}

# -----------------------------------------------------------------------------
# NSGs at the edges.
# -----------------------------------------------------------------------------

# PostgreSQL: 5432 (and 6432 for the built-in PgBouncer) from the AKS node
# subnets; everything inside the subnet (zone-redundant HA replication); outbound
# to Storage for the WAL archive. Without the last two, HA fails.
resource "azurerm_network_security_group" "postgres" {
  count = local.create_network ? 1 : 0

  name                = "nsg-postgres-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  security_rule {
    name                       = "allow-aks-postgres"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_ranges    = ["5432", "6432"]
    source_address_prefixes    = local.aks_node_ranges
    destination_address_prefix = var.address_plan["snet-postgres"]
  }

  security_rule {
    name                       = "allow-ha-replication"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = var.address_plan["snet-postgres"]
    destination_address_prefix = var.address_plan["snet-postgres"]
  }

  security_rule {
    name                       = "deny-other-vnet"
    priority                   = 4000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "VirtualNetwork"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "allow-intra-subnet-out"
    priority                   = 100
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = var.address_plan["snet-postgres"]
    destination_address_prefix = var.address_plan["snet-postgres"]
  }

  security_rule {
    name                       = "allow-storage-wal-archive"
    priority                   = 110
    direction                  = "Outbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = var.address_plan["snet-postgres"]
    destination_address_prefix = "Storage"
  }

  tags = local.tags
}

# Private endpoints (Redis, Key Vault, Blob, registry, and a managed broker if
# chosen): reachable from the AKS node subnets only.
resource "azurerm_network_security_group" "private_endpoints" {
  count = local.create_network ? 1 : 0

  name                = "nsg-pe-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  security_rule {
    name                       = "allow-aks"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefixes    = local.aks_node_ranges
    destination_address_prefix = var.address_plan["snet-private-endpoints"]
  }

  security_rule {
    name                       = "deny-other-vnet"
    priority                   = 4000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "VirtualNetwork"
    destination_address_prefix = "*"
  }

  tags = local.tags
}

# Ingress: no Internet inbound. Front Door arrives through the Private Link
# service, whose NAT addresses are inside this subnet, and the Azure load
# balancer probes are allowed by the default rules.
resource "azurerm_network_security_group" "ingress" {
  count = local.create_network ? 1 : 0

  name                = "nsg-ingress-ticvai-${local.cell_name}"
  resource_group_name = azurerm_resource_group.cell.name
  location            = azurerm_resource_group.cell.location

  security_rule {
    name                       = "deny-internet"
    priority                   = 4000
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }

  tags = local.tags
}

resource "azurerm_subnet_network_security_group_association" "edges" {
  for_each = local.create_network ? {
    "snet-postgres"          = azurerm_network_security_group.postgres[0].id
    "snet-private-endpoints" = azurerm_network_security_group.private_endpoints[0].id
    "snet-ingress"           = azurerm_network_security_group.ingress[0].id
  } : {}

  subnet_id                 = azurerm_subnet.cell[each.key].id
  network_security_group_id = each.value
}
