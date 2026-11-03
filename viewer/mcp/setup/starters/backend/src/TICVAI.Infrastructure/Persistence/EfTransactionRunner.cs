using Microsoft.EntityFrameworkCore;
using TICVAI.Application.Abstractions.Persistence;
using TICVAI.Infrastructure.Persistence.DbContexts;

namespace TICVAI.Infrastructure.Persistence;

/// <summary>
/// <see cref="ITransactionRunner"/> on the request's <see cref="TicvaiDbContext"/>, which is the
/// request's tenant database. Beginning the transaction fires <see cref="ScopeContextInterceptor"/>, so
/// the connection context is set before the work's first statement.
/// </summary>
public sealed class EfTransactionRunner(TicvaiDbContext db) : ITransactionRunner
{
    public async Task<T> RunAsync<T>(Func<CancellationToken, Task<T>> work, CancellationToken cancellationToken)
    {
        ArgumentNullException.ThrowIfNull(work);
        if (db.Database.CurrentTransaction is not null)
        {
            // Already inside one: the work joins it, so order, payment and ledger commit together.
            return await work(cancellationToken).ConfigureAwait(false);
        }

        await using var transaction = await db.Database.BeginTransactionAsync(cancellationToken).ConfigureAwait(false);
        var result = await work(cancellationToken).ConfigureAwait(false);
        await db.SaveChangesAsync(cancellationToken).ConfigureAwait(false);
        await transaction.CommitAsync(cancellationToken).ConfigureAwait(false);
        return result;
    }
}
