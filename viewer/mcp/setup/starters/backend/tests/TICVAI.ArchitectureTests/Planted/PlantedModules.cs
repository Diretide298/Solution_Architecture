// Types planted so ModuleBoundaryTests.The_rule_catches_what_it_is_for can prove the rule finds a
// violation in a method body, allows a Public API, and allows a composed read across deployables.
// Nothing outside this file uses them.

namespace TICVAI.ArchitectureTests.Planted.Features.Ledger.Internal
{
    public sealed class Journal
    {
        public static int Count() => 0;
    }
}

namespace TICVAI.ArchitectureTests.Planted.Features.Ledger.Public
{
    public sealed class LedgerQueries
    {
        public static int Balance() => 0;
    }
}

namespace TICVAI.ArchitectureTests.Planted.Features.Order.Public
{
    public sealed class OrderQueries
    {
        public static int Open() => 0;
    }
}

namespace TICVAI.ArchitectureTests.Planted.Features.Order
{
    public sealed class Checkout
    {
        // Allowed: the same deployable, through Ledger's Public API.
        public static int Allowed() => Ledger.Public.LedgerQueries.Balance();

        // Violation, inside a method body only: Ledger's internal type.
        public static int ReachesIn() => Ledger.Internal.Journal.Count();
    }
}

namespace TICVAI.ArchitectureTests.Planted.Features.FnB
{
    public sealed class Kitchen
    {
        // Allowed: operations composes Order's queries in process (cross-deployable-writes composes).
        public static int Allowed() => Order.Public.OrderQueries.Open();
    }
}

namespace TICVAI.ArchitectureTests.Planted.Features.Access
{
    public sealed class Gate
    {
        // Violation: access does not compose Order.
        public static int AcrossDeployables() => Order.Public.OrderQueries.Open();
    }
}

namespace TICVAI.ArchitectureTests.Planted.Features.Unknown
{
    public sealed class Stray
    {
    }
}
