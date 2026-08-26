using System.Reflection;
using NetArchTest.Rules;
using Xunit;

namespace Ticvai.ArchitectureTests;

/// <summary>
/// Enforces the module boundaries described in the Project Direction.
/// </summary>
/// <remarks>
/// These are not style checks. Without automated enforcement, module boundaries
/// decay within weeks, and extracting a service later becomes a rewrite rather
/// than a week's work. Every one of these tests failing is a build failure.
/// </remarks>
public sealed class ModuleBoundaryTests
{
    private static readonly string[] Modules =
    [
        "Ticvai.Modules.Identity",
        "Ticvai.Modules.Tenancy",
        "Ticvai.Modules.Catalogue",
        "Ticvai.Modules.Orders",
        "Ticvai.Modules.AccessControl",
        "Ticvai.Modules.Sync"
    ];

    private static IEnumerable<Assembly> LoadModules() =>
        Modules.Select(m => Assembly.Load(m));

    [Fact]
    public void Modules_do_not_reference_each_other()
    {
        foreach (var module in LoadModules())
        {
            var others = Modules.Where(m => m != module.GetName().Name).ToArray();

            var result = Types.InAssembly(module)
                .ShouldNot()
                .HaveDependencyOnAny(others)
                .GetResult();

            Assert.True(result.IsSuccessful,
                $"{module.GetName().Name} references another module directly. " +
                "Cross-module communication goes through Shared.Kernel.Abstractions or the event bus. " +
                $"Offenders: {string.Join(", ", result.FailingTypeNames ?? [])}");
        }
    }

    [Fact]
    public void Shared_kernel_holds_primitives_only()
    {
        var result = Types.InAssembly(Assembly.Load("Ticvai.Shared.Kernel"))
            .ShouldNot()
            .HaveDependencyOnAny([.. Modules, "Ticvai.Api", "Ticvai.ControlPlane"])
            .GetResult();

        Assert.True(result.IsSuccessful,
            "Shared.Kernel depends on a module. It must hold primitives only — " +
            "tenant context, money, IDs, result types. The moment domain logic lands " +
            "there the module boundaries are gone. " +
            $"Offenders: {string.Join(", ", result.FailingTypeNames ?? [])}");
    }

    [Fact]
    public void Domain_layers_do_not_depend_on_infrastructure()
    {
        foreach (var module in LoadModules())
        {
            var name = module.GetName().Name!;

            var result = Types.InAssembly(module)
                .That().ResideInNamespace($"{name}.Domain")
                .ShouldNot()
                .HaveDependencyOnAny(
                    "Npgsql",
                    "Microsoft.EntityFrameworkCore",
                    "StackExchange.Redis",
                    "Microsoft.AspNetCore",
                    $"{name}.Infrastructure")
                .GetResult();

            Assert.True(result.IsSuccessful,
                $"{name}.Domain depends on infrastructure. Domain must be persistence-ignorant. " +
                $"Offenders: {string.Join(", ", result.FailingTypeNames ?? [])}");
        }
    }

    [Fact]
    public void Entities_are_not_exposed_from_api_layer()
    {
        foreach (var module in LoadModules())
        {
            var name = module.GetName().Name!;

            var result = Types.InAssembly(module)
                .That().ResideInNamespace($"{name}.Api")
                .And().AreClasses()
                .ShouldNot()
                .HaveDependencyOn($"{name}.Domain.Entities")
                .GetResult();

            Assert.True(result.IsSuccessful,
                $"{name}.Api returns domain entities directly. Map to contract DTOs — " +
                "leaking entities couples the wire format to the schema. " +
                $"Offenders: {string.Join(", ", result.FailingTypeNames ?? [])}");
        }
    }

    [Fact]
    public void Modules_do_not_reference_the_api_host()
    {
        foreach (var module in LoadModules())
        {
            var result = Types.InAssembly(module)
                .ShouldNot()
                .HaveDependencyOnAny("Ticvai.Api", "Ticvai.ControlPlane")
                .GetResult();

            Assert.True(result.IsSuccessful,
                $"{module.GetName().Name} references the host. Dependencies point inward: " +
                "the host composes modules, modules never reach back. " +
                $"Offenders: {string.Join(", ", result.FailingTypeNames ?? [])}");
        }
    }

    // NOTE: DateTime.Now is banned via a BannedSymbols analyzer, not here.
    // NetArchTest resolves type-level dependencies only, so a rule written against
    // "System.DateTime.Now" silently passes and gives false assurance — the exact
    // failure mode these tests exist to prevent. See BannedSymbols.txt.
}
