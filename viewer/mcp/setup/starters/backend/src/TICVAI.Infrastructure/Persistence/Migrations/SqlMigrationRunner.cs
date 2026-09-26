using Npgsql;

namespace TICVAI.Infrastructure.Persistence.Migrations;

/// <summary>
/// Applies the package's derived DDL to a database, in file order, once each.
///
/// The package writes the schema as numbered SQL per database (backend/tenant/*.sql and
/// backend/control/*.sql: 000 schemas, 001 extensions, 002 the migration register, 010 per
/// module, 900 foreign keys, 910 indexes, 920 row-level security). That is the migration
/// model; EF Core migrations are not used for the schema. Each applied file is recorded in
/// platform.schema_version (created by 002), so a second run applies only what is new.
///
/// Copy the package's backend/ folder into this repository's db/ folder (or point at it), then:
///     await new SqlMigrationRunner(connectionString).ApplyAsync("db/tenant", ct);
/// A [DB] ticket's migration is a new numbered file here, tested by applying the folder to an
/// empty database twice (the second run must apply nothing).
/// </summary>
public sealed class SqlMigrationRunner(string connectionString)
{
    public async Task<IReadOnlyList<string>> ApplyAsync(string folder, CancellationToken cancellationToken)
    {
        var files = Directory.GetFiles(folder, "*.sql").OrderBy(Path.GetFileName, StringComparer.Ordinal).ToList();
        await using var connection = new NpgsqlConnection(connectionString);
        await connection.OpenAsync(cancellationToken);

        var applied = new List<string>();
        foreach (var file in files)
        {
            var name = Path.GetFileName(file);
            var sql = await File.ReadAllTextAsync(file, cancellationToken);
            var checksum = Convert.ToHexString(System.Security.Cryptography.SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(sql)));
            var recorded = await RecordedChecksumAsync(connection, name, cancellationToken);
            if (recorded is not null)
            {
                // An applied file that has changed since is drift, not something to skip quietly.
                if (!string.Equals(recorded, checksum, StringComparison.OrdinalIgnoreCase))
                {
                    throw new InvalidOperationException($"{name} was applied with checksum {recorded} and now reads {checksum}; add a new file instead of editing an applied one");
                }

                continue;
            }

            var started = System.Diagnostics.Stopwatch.StartNew();
            await using var transaction = await connection.BeginTransactionAsync(cancellationToken);
            await using (var apply = new NpgsqlCommand(sql, connection, transaction))
            {
                await apply.ExecuteNonQueryAsync(cancellationToken);
            }

            await using (var record = new NpgsqlCommand(
                "INSERT INTO platform.schema_version (version, description, checksum, execution_ms) VALUES (@v, @d, @c, @ms)",
                connection, transaction))
            {
                record.Parameters.AddWithValue("v", name);
                record.Parameters.AddWithValue("d", $"applied from {folder}");
                record.Parameters.AddWithValue("c", checksum);
                record.Parameters.AddWithValue("ms", (int)started.ElapsedMilliseconds);
                await record.ExecuteNonQueryAsync(cancellationToken);
            }

            await transaction.CommitAsync(cancellationToken);
            applied.Add(name);
        }

        return applied;
    }

    private static async Task<string?> RecordedChecksumAsync(NpgsqlConnection connection, string name, CancellationToken cancellationToken)
    {
        // Before 002 has run there is no register, so nothing counts as applied.
        await using var exists = new NpgsqlCommand("SELECT to_regclass('platform.schema_version') IS NOT NULL", connection);
        if (!(bool)(await exists.ExecuteScalarAsync(cancellationToken))!)
        {
            return null;
        }

        await using var check = new NpgsqlCommand("SELECT checksum FROM platform.schema_version WHERE version = @v", connection);
        check.Parameters.AddWithValue("v", name);
        return await check.ExecuteScalarAsync(cancellationToken) as string;
    }
}
