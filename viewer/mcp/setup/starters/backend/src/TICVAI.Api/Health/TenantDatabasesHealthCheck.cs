using Microsoft.Extensions.Diagnostics.HealthChecks;
using Npgsql;
using TICVAI.Infrastructure.Tenancy;

namespace TICVAI.Api.Health;

/// <summary>
/// <c>/health</c> is unhealthy (503) when any tenant database this process serves does not answer, or
/// when it serves none: a process that cannot reach its data is not ready for traffic.
/// </summary>
public sealed class TenantDatabasesHealthCheck(ITenantConnections connections) : IHealthCheck
{
    public async Task<HealthCheckResult> CheckHealthAsync(HealthCheckContext context, CancellationToken cancellationToken = default)
    {
        if (connections.Tenants.Count == 0)
        {
            return HealthCheckResult.Unhealthy("No tenant database is configured");
        }

        var failed = new List<string>();
        foreach (var tenantId in connections.Tenants)
        {
            try
            {
                var builder = new NpgsqlConnectionStringBuilder(connections.ConnectionStringFor(tenantId)) { Timeout = 3 };
                await using var connection = new NpgsqlConnection(builder.ConnectionString);
                await connection.OpenAsync(cancellationToken);
                await using var ping = new NpgsqlCommand("SELECT 1", connection);
                await ping.ExecuteScalarAsync(cancellationToken);
            }
            catch (Exception exception) when (exception is not OperationCanceledException)
            {
                failed.Add(tenantId.ToString());
            }
        }

        return failed.Count == 0
            ? HealthCheckResult.Healthy()
            : HealthCheckResult.Unhealthy($"Tenant databases not answering: {string.Join(", ", failed)}");
    }
}
