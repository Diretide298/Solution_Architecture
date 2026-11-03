using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TICVAI.Api.Health;
using TICVAI.Api.Security;
using TICVAI.Application;
using TICVAI.Infrastructure.DependencyInjection;

namespace TICVAI.Api.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddTicvaiApplication(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddApplication();

        return services;
    }

    public static IServiceCollection AddTicvaiInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddInfrastructure(configuration);
        services.AddTicvaiAuthentication(configuration);

        return services;
    }

    public static IServiceCollection AddTicvaiHealthChecks(
    this IServiceCollection services)
    {
        services.AddHealthChecks()
            .AddCheck<TenantDatabasesHealthCheck>("tenant-databases");

        return services;
    }
}
