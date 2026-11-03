using System.Data.Common;
using Microsoft.EntityFrameworkCore.Diagnostics;
using Npgsql;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.Infrastructure.Persistence;

/// <summary>
/// Sets the connection context row-level security reads, <b>with <c>SET LOCAL</c> semantics at the start
/// of every transaction</b> (backend/MIGRATIONS.md, "The connection context"): <c>ticvai.scope_paths</c>,
/// <c>ticvai.subject_id</c> and <c>ticvai.principal_id</c> from <see cref="ITenantContext"/>.
/// </summary>
/// <remarks>
/// <para>
/// <c>set_config(name, value, true)</c> is <c>SET LOCAL</c> that takes parameters: the values end with
/// the transaction, so a pooled connection never carries one request's scope into the next. A
/// session-level <c>SET</c> (or <c>set_config(..., false)</c>) would.
/// </para>
/// <para>
/// A statement outside a transaction runs with no context and sees no scoped rows (920's default deny).
/// Run data access through <c>ITransactionRunner</c>.
/// </para>
/// </remarks>
public sealed class ScopeContextInterceptor(ITenantContext tenant) : DbTransactionInterceptor
{
    /// <summary>The statement, with its three parameters; <c>true</c> makes each setting transaction-local.</summary>
    public const string Sql =
        "SELECT set_config('ticvai.scope_paths', @scope_paths, true), " +
        "set_config('ticvai.subject_id', @subject_id, true), " +
        "set_config('ticvai.principal_id', @principal_id, true)";

    public override DbTransaction TransactionStarted(DbConnection connection, TransactionEndEventData eventData, DbTransaction result)
    {
        using var command = Build(connection, result, tenant);
        command.ExecuteNonQuery();
        return result;
    }

    public override async ValueTask<DbTransaction> TransactionStartedAsync(
        DbConnection connection,
        TransactionEndEventData eventData,
        DbTransaction result,
        CancellationToken cancellationToken = default)
    {
        await using var command = Build(connection, result, tenant);
        await command.ExecuteNonQueryAsync(cancellationToken).ConfigureAwait(false);
        return result;
    }

    /// <summary>The command for <paramref name="context"/>: empty values for what the caller does not have.</summary>
    public static DbCommand Build(DbConnection connection, DbTransaction transaction, ITenantContext context)
    {
        ArgumentNullException.ThrowIfNull(connection);
        ArgumentNullException.ThrowIfNull(context);
        var command = connection.CreateCommand();
        command.Transaction = transaction;
        command.CommandText = Sql;
        foreach (var (name, value) in Values(context))
        {
            command.Parameters.Add(new NpgsqlParameter(name, value));
        }

        return command;
    }

    /// <summary>The three settings' values: scope paths comma-separated (as platform.current_scope_paths() splits them).</summary>
    public static IReadOnlyList<(string Name, string Value)> Values(ITenantContext context)
    {
        ArgumentNullException.ThrowIfNull(context);
        return
        [
            ("scope_paths", string.Join(',', context.ScopePaths)),
            ("subject_id", context.SubjectId?.ToString() ?? string.Empty),
            ("principal_id", context.PrincipalId?.ToString() ?? string.Empty),
        ];
    }
}
