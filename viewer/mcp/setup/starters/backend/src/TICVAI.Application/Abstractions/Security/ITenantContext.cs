namespace TICVAI.Application.Abstractions.Security;

/// <summary>The tenant the current request is scoped to. Every data path reads it.</summary>
public interface ITenantContext
{
    string TenantId { get; }
}
