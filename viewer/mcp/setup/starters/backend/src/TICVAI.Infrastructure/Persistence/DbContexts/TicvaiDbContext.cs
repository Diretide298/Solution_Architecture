using Microsoft.EntityFrameworkCore;

namespace TICVAI.Infrastructure.Persistence.DbContexts;

public class TicvaiDbContext : DbContext
{
    public TicvaiDbContext(
        DbContextOptions<TicvaiDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
    }
}