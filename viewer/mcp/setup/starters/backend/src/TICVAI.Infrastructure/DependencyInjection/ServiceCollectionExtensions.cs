using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TICVAI.Application.Abstractions.Persistence;
using TICVAI.Application.Abstractions.Security;
using TICVAI.Infrastructure.Idempotency;
using TICVAI.Infrastructure.Messaging;
using TICVAI.Infrastructure.Persistence;
using TICVAI.Infrastructure.Persistence.DbContexts;
using TICVAI.Infrastructure.Tenancy;

namespace TICVAI.Infrastructure.DependencyInjection;

public static class ServiceCollectionExtensions
{
    /// <summary>
    /// The data path: <b>one process serves every tenant of the cell, each request on its own tenant's
    /// database</b> (ADR-0038). The request's host picks the tenant (<see cref="ITenantDirectory"/>), the
    /// tenant picks the connection (<see cref="ITenantConnections"/>), and every transaction opens with the
    /// caller's context set by <see cref="ScopeContextInterceptor"/>.
    /// </summary>
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.Configure<TenantOptions>(configuration.GetSection(TenantOptions.SectionName));
        services.AddSingleton<ConfiguredTenantDirectory>();
        services.AddSingleton<ITenantDirectory>(sp => sp.GetRequiredService<ConfiguredTenantDirectory>());
        services.AddSingleton<ITenantConnections>(sp => sp.GetRequiredService<ConfiguredTenantDirectory>());

        // Per request: filled by the host (tenant), then by authentication (the caller's scope).
        services.AddScoped<RequestTenantContext>();
        services.AddScoped<ITenantContext>(sp => sp.GetRequiredService<RequestTenantContext>());
        services.AddScoped<RequestPrincipal>();
        services.AddScoped<ICurrentPrincipal>(sp => sp.GetRequiredService<RequestPrincipal>());
        services.AddSingleton<ISessionRegistry, NoSessionRegistry>();

        services.AddScoped<ScopeContextInterceptor>();
        services.AddDbContext<TicvaiDbContext>((sp, options) =>
        {
            var tenant = sp.GetRequiredService<ITenantContext>();
            if (!tenant.IsResolved)
            {
                throw new InvalidOperationException("No tenant database without a tenant: the request's host resolved to none");
            }

            options.UseNpgsql(sp.GetRequiredService<ITenantConnections>().ConnectionStringFor(tenant.TenantId));
            options.AddInterceptors(sp.GetRequiredService<ScopeContextInterceptor>());
        });
        services.AddScoped<ITransactionRunner, EfTransactionRunner>();

        // The durable idempotency record, in the change's transaction (SD-024, CR-182). Never Redis.
        services.AddScoped<IIdempotencyStore, PostgresIdempotencyStore>();

        // The relay's batch size and poll intervals (ADR-0058, amended 1 October 2026). The
        // flash-sale burst environment raises Relay:BatchSize; nothing else changes.
        services.Configure<RelayOptions>(
            configuration.GetSection(RelayOptions.SectionName));

        services.AddSingleton(TimeProvider.System);

        return services;
    }
}
