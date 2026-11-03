using Microsoft.EntityFrameworkCore;
using Npgsql;
using TICVAI.Application.Abstractions.Security;
using TICVAI.Infrastructure.Persistence;
using TICVAI.Infrastructure.Persistence.DbContexts;
using TICVAI.Infrastructure.Tenancy;

namespace TICVAI.IntegrationTests;

/// <summary>
/// Against a real PostgreSQL (quality-gates 4: "Real Postgres ... RLS enforcement"): the transaction
/// runner sets the connection context with SET LOCAL, a query without it sees no rows, and nothing
/// carries over on a pooled connection. Set <c>TICVAI_TEST_DATABASE</c> to a superuser connection
/// string to run it (the pipeline's postgres service does); with <c>TICVAI_REQUIRE_DATABASE=1</c>,
/// which the pipeline sets, a missing database fails instead of skipping.
/// </summary>
public class RowSecurityContextTests
{
    private static readonly string? Admin = Environment.GetEnvironmentVariable("TICVAI_TEST_DATABASE");

    [DatabaseFact]
    public async Task A_transaction_sees_only_its_scope_and_nothing_leaks_to_the_next_user_of_the_connection()
    {
        Assert.False(string.IsNullOrEmpty(Admin), "TICVAI_REQUIRE_DATABASE=1 but TICVAI_TEST_DATABASE is not set");
        var probe = await PrepareAsync(Admin!);

        var tenant = new RequestTenantContext();
        tenant.Resolve(new TenantRoute(Guid.Parse("01920000-0000-7000-8000-00000000000a"), "t_a"));

        await using (var db = Context(probe, tenant))
        {
            // Nothing bound: the context is set, empty, and row security shows nothing.
            Assert.Equal(0, await new EfTransactionRunner(db).RunAsync(ct => CountAsync(db, ct), default));

            tenant.Bind(["t_a.v_1"], principalId: null, subjectId: null);
            Assert.Equal(1, await new EfTransactionRunner(db).RunAsync(ct => CountAsync(db, ct), default));

            // The same pooled connection, outside any transaction: SET LOCAL ended with the commit.
            Assert.Equal(0, await CountAsync(db, default));
        }
    }

    private static TicvaiDbContext Context(string connectionString, ITenantContext tenant) => new(
        new DbContextOptionsBuilder<TicvaiDbContext>()
            .UseNpgsql(connectionString)
            .AddInterceptors(new ScopeContextInterceptor(tenant))
            .Options);

    private static async Task<int> CountAsync(TicvaiDbContext db, CancellationToken cancellationToken) =>
        await db.Database.SqlQueryRaw<int>("SELECT count(*)::int AS \"Value\" FROM rls_probe.item").SingleAsync(cancellationToken);

    /// <summary>A table with FORCE ROW LEVEL SECURITY on scope_path (as 920 makes them) and a role that is not its owner's superuser.</summary>
    private static async Task<string> PrepareAsync(string admin)
    {
        await using var connection = new NpgsqlConnection(admin);
        await connection.OpenAsync();
        await using var setup = new NpgsqlCommand(
            """
            CREATE EXTENSION IF NOT EXISTS ltree;
            DROP SCHEMA IF EXISTS rls_probe CASCADE;
            CREATE SCHEMA rls_probe;
            CREATE TABLE rls_probe.item (id int PRIMARY KEY, scope_path ltree NOT NULL);
            INSERT INTO rls_probe.item VALUES (1, 't_a.v_1'), (2, 't_a.v_2');
            ALTER TABLE rls_probe.item ENABLE ROW LEVEL SECURITY;
            ALTER TABLE rls_probe.item FORCE ROW LEVEL SECURITY;
            CREATE POLICY item_scope ON rls_probe.item USING (
                scope_path <@ ANY (COALESCE(string_to_array(NULLIF(current_setting('ticvai.scope_paths', true), ''), ',')::ltree[], ARRAY[]::ltree[])));
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'rls_probe_app') THEN
                    CREATE ROLE rls_probe_app LOGIN PASSWORD 'rls_probe_app';
                END IF;
            END $$;
            GRANT USAGE ON SCHEMA rls_probe TO rls_probe_app;
            GRANT SELECT ON rls_probe.item TO rls_probe_app;
            """,
            connection);
        await setup.ExecuteNonQueryAsync();
        return new NpgsqlConnectionStringBuilder(admin) { Username = "rls_probe_app", Password = "rls_probe_app", MaxPoolSize = 1 }.ConnectionString;
    }
}

/// <summary>Runs when TICVAI_TEST_DATABASE is set; skips otherwise, unless TICVAI_REQUIRE_DATABASE=1 makes the absence a failure.</summary>
public sealed class DatabaseFactAttribute : FactAttribute
{
    public DatabaseFactAttribute()
    {
        if (string.IsNullOrEmpty(Environment.GetEnvironmentVariable("TICVAI_TEST_DATABASE"))
            && Environment.GetEnvironmentVariable("TICVAI_REQUIRE_DATABASE") != "1")
        {
            Skip = "No TICVAI_TEST_DATABASE: the pipeline runs this against its postgres service";
        }
    }
}
