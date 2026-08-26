using Microsoft.Extensions.DependencyInjection;

namespace Ticvai.Shared.Kernel.Abstractions;

/// <summary>
/// Contract every module implements so the host can register it without
/// referencing its internals.
/// </summary>
/// <remarks>
/// The host composes modules; modules never reference each other. Cross-module
/// communication is via interfaces declared in this namespace or via the event
/// bus. Enforced by <c>Ticvai.ArchitectureTests</c>, not by convention.
/// </remarks>
public interface IModule
{
    /// <summary>Postgres schema this module owns, e.g. <c>orders</c>.</summary>
    static abstract string SchemaName { get; }

    static abstract void RegisterServices(IServiceCollection services);
}
