using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TICVAI.Application.Abstractions.Persistence;
using TICVAI.Infrastructure.Configuration;
using TICVAI.Infrastructure.Idempotency;
using TICVAI.Infrastructure.Messaging;
using TICVAI.Infrastructure.Persistence.DbContexts;

namespace TICVAI.Infrastructure.DependencyInjection;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var connectionString = configuration
            .GetSection(DatabaseOptions.SectionName)
            .GetValue<string>(nameof(DatabaseOptions.ConnectionString));

        if (string.IsNullOrWhiteSpace(connectionString))
        {
            throw new InvalidOperationException(
                "Database connection string is not configured.");
        }

        services.Configure<DatabaseOptions>(
            configuration.GetSection(DatabaseOptions.SectionName));

        services.AddDbContext<TicvaiDbContext>(options =>
        {
            options.UseNpgsql(connectionString);
        });

        // The relay's batch size and poll intervals (ADR-0058, amended 1 October 2026). The
        // flash-sale burst environment raises Relay:BatchSize; nothing else changes.
        services.Configure<RelayOptions>(
            configuration.GetSection(RelayOptions.SectionName));

        services.AddSingleton(TimeProvider.System);
        services.AddSingleton<IIdempotencyStore, InMemoryIdempotencyStore>();

        return services;
    }
}