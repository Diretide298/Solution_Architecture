using Microsoft.Extensions.DependencyInjection;

namespace TICVAI.Application;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplication(
        this IServiceCollection services)
    {
        return services;
    }
}