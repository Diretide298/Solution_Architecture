using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;
using Npgsql;
using TICVAI.Application.Abstractions.Persistence;
using TICVAI.Application.Abstractions.Security;
using TICVAI.Infrastructure.Persistence.DbContexts;

namespace TICVAI.Infrastructure.Idempotency;

/// <summary>
/// <see cref="IIdempotencyStore"/> on <c>platform.idempotency_record</c>, in the request's transaction
/// (<c>common.yaml</c> <c>IdempotencyKey</c>; ADAM CR-182): the row is written once, on completion, with
/// <c>status</c> <c>completed</c>, <c>scope_path</c> the tenant root and <c>expires_at</c> 24 hours on.
/// The unique index <c>idempotency_record_operation_id_idempotency_key_uniq</c> is the guarantee: a
/// concurrent second insert waits on it and fails when the first commits.
/// </summary>
public sealed class PostgresIdempotencyStore(TicvaiDbContext db, ITenantContext tenant, ICurrentPrincipal principal, TimeProvider clock)
    : IIdempotencyStore
{
    /// <summary>How long a record replays (CR-182: <c>expires_at</c> is <c>created_at</c> plus 24 hours).</summary>
    public static readonly TimeSpan Keep = TimeSpan.FromHours(24);

    public async Task<IdempotencyRecord?> FindAsync(Guid key, string operationId, CancellationToken cancellationToken)
    {
        await using var command = Command(
            "SELECT request_hash, response_status, response_body::text FROM platform.idempotency_record " +
            "WHERE operation_id = @operation_id AND idempotency_key = @key AND expires_at > @now");
        command.Parameters.AddWithValue("operation_id", operationId);
        command.Parameters.AddWithValue("key", key);
        command.Parameters.AddWithValue("now", clock.GetUtcNow());
        await using var reader = await command.ExecuteReaderAsync(cancellationToken).ConfigureAwait(false);
        if (!await reader.ReadAsync(cancellationToken).ConfigureAwait(false))
        {
            return null;
        }

        return new IdempotencyRecord(
            reader.GetString(0),
            new IdempotentResponse(reader.IsDBNull(1) ? 0 : reader.GetInt32(1), reader.IsDBNull(2) ? string.Empty : reader.GetString(2)));
    }

    public async Task RecordAsync(IdempotencyRequest request, IdempotentResponse response, CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(request);
        ArgumentNullException.ThrowIfNull(response);
        var now = clock.GetUtcNow();
        await using var command = Command(
            "INSERT INTO platform.idempotency_record (id, idempotency_key, operation_id, request_hash, status, " +
            "response_status, response_body, principal_id, created_at, expires_at, scope_path) VALUES " +
            "(@id, @key, @operation_id, @request_hash, 'completed', @status, @body::jsonb, @principal_id, @now, @expires, @root::ltree)");
        command.Parameters.AddWithValue("id", TICVAI.Domain.Identity.Id.New());
        command.Parameters.AddWithValue("key", request.Key);
        command.Parameters.AddWithValue("operation_id", request.OperationId);
        command.Parameters.AddWithValue("request_hash", request.RequestHash);
        command.Parameters.AddWithValue("status", response.StatusCode);
        command.Parameters.AddWithValue("body", string.IsNullOrEmpty(response.Body) ? "null" : response.Body);
        command.Parameters.AddWithValue("principal_id", (object?)principal.PrincipalId ?? DBNull.Value);
        command.Parameters.AddWithValue("now", now);
        command.Parameters.AddWithValue("expires", now.Add(Keep));
        command.Parameters.AddWithValue("root", tenant.TenantRootPath);
        try
        {
            await command.ExecuteNonQueryAsync(cancellationToken).ConfigureAwait(false);
        }
        catch (PostgresException exception) when (exception.SqlState == PostgresErrorCodes.UniqueViolation)
        {
            throw new IdempotencyKeyTakenException(request.Key, request.OperationId, exception);
        }
    }

    private NpgsqlCommand Command(string sql)
    {
        var transaction = db.Database.CurrentTransaction
            ?? throw new InvalidOperationException("The idempotency record is read and written inside the change's transaction (ITransactionRunner)");
        return new NpgsqlCommand(sql, (NpgsqlConnection)db.Database.GetDbConnection(), (NpgsqlTransaction)transaction.GetDbTransaction());
    }
}
