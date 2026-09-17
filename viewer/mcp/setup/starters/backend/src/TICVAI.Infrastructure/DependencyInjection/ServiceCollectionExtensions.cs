using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using TICVAI.Infrastructure.Configuration;
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

        return services;
    }
}