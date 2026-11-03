namespace TICVAI.Application.Abstractions.Persistence;

/// <summary>
/// One explicit transaction on the tenant's database. Its first statement sets the connection context
/// with <c>SET LOCAL</c> (<c>ticvai.scope_paths</c>, <c>ticvai.subject_id</c>, <c>ticvai.principal_id</c>
/// from <c>ITenantContext</c>; backend/MIGRATIONS.md, "The connection context"), so row-level security
/// sees this request's scope and nothing carries over to the next user of the pooled connection.
/// </summary>
/// <remarks>
/// Order + payment + entitlement + ledger is one transaction: run them inside one call. A query outside
/// any transaction runs with no context set and sees no scoped rows (fail closed).
/// </remarks>
public interface ITransactionRunner
{
    /// <summary>Runs <paramref name="work"/> in one transaction: committed when it returns, rolled back when it throws.</summary>
    Task<T> RunAsync<T>(Func<CancellationToken, Task<T>> work, CancellationToken cancellationToken);
}
