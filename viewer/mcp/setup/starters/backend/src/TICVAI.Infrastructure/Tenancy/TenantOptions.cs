namespace TICVAI.Infrastructure.Tenancy;

/// <summary>
/// The tenants this cell serves, bound from the <c>Tenants</c> configuration section: one entry per
/// tenant, each with its own database (ADR-0038: a cell holds many tenants, a database each).
/// </summary>
/// <remarks>
/// In development, appsettings.Development.json lists them. In a cell the list and each tenant's
/// connection string come from the control plane's <c>TenantDomain</c> rows and the cell's Key Vault
/// (config-and-secrets): replace <see cref="ConfiguredTenantDirectory"/>'s registration, not the interfaces.
/// </remarks>
public sealed class TenantOptions
{
    public const string SectionName = "Tenants";

    public List<TenantEntry> Entries { get; set; } = [];
}

public sealed class TenantEntry
{
    public Guid TenantId { get; set; }

    /// <summary>The hosts the tenant is served at (its platform subdomain and custom domains).</summary>
    public List<string> Hosts { get; set; } = [];

    /// <summary>The tenant's root scope path (ltree text), for example <c>t_ref</c>.</summary>
    public string RootScopePath { get; set; } = string.Empty;

    /// <summary>The tenant database. Never in source: a Key Vault reference in a cell.</summary>
    public string ConnectionString { get; set; } = string.Empty;
}
