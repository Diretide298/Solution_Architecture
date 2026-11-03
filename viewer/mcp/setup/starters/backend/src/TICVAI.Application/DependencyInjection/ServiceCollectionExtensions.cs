using Microsoft.Extensions.DependencyInjection;
using TICVAI.Application.Abstractions.Persistence;

namespace TICVAI.Application;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplication(
        this IServiceCollection services)
    {
        // Every mutating operation's Idempotency-Key goes through this one rule.
        services.AddScoped<IdempotentExecution>();

        return services;
    }
}
