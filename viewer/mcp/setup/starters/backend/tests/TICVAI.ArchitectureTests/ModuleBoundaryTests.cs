using System.Text.Json;
using System.Text.RegularExpressions;
using Mono.Cecil;
using Mono.Cecil.Cil;

namespace TICVAI.ArchitectureTests;

/// <summary>
/// ADR-0055's ownership rule over <b>every</b> module (<c>modules.json</c>: the ADR's module map), read
/// from the compiled IL, method bodies included, so a use inside a method is caught as surely as one in
/// a signature. A module is a folder <c>Features/&lt;Module&gt;/</c> in Application, Infrastructure or Api.
/// </summary>
/// <remarks>
/// <list type="bullet">
/// <item>A module uses another module only through that module's <c>Features/&lt;Other&gt;/Public/</c>
/// types (its in-process query and write API; ADR-0055 rules 2 and 3), never its other types.</item>
/// <item>Across deployables not even that (rule 4: by event or the published contract), except where the
/// reader's host composes the other module's queries in process (<c>composes</c>,
/// docs/active/cross-deployable-writes.yaml).</item>
/// <item>A folder under <c>Features/</c> that is not a module of the map fails: add it to the map with
/// its ADR first.</item>
/// </list>
/// </remarks>
public class ModuleBoundaryTests
{
    private static readonly Regex Production = new(@"^TICVAI\.(?:Application|Infrastructure|Api)\.Features\.(?<module>[A-Za-z]+)(?<rest>\..*)?$");
    private static readonly Regex Planted = new(@"^TICVAI\.ArchitectureTests\.Planted\.Features\.(?<module>[A-Za-z]+)(?<rest>\..*)?$");

    [Fact]
    public void The_map_has_every_module_of_adr_0055()
    {
        var map = ModuleMap.Load();

        Assert.Equal(16, map.Deployable.Count);
        Assert.Equal(["access", "commerce", "operations"], map.Deployable.Values.Distinct().Order());
        Assert.All(map.Composes, c => Assert.True(map.Deployable.ContainsKey(c.Module), c.Module));
    }

    [Fact]
    public void Modules_use_one_another_only_through_what_the_rule_allows()
    {
        var map = ModuleMap.Load();
        var violations = new[] { "TICVAI.Application", "TICVAI.Infrastructure", "TICVAI.Api" }
            .SelectMany(name => Check(Path.Combine(AppContext.BaseDirectory, name + ".dll"), Production, map))
            .ToList();

        Assert.Empty(violations);
    }

    [Fact]
    public void The_rule_catches_what_it_is_for()
    {
        // Planted types in this assembly (Planted/PlantedModules.cs): the check must find exactly these.
        var violations = Check(typeof(ModuleBoundaryTests).Assembly.Location, Planted, ModuleMap.Load()).Order().ToList();

        Assert.Equal(
            [
                "Access uses Order across deployables (access -> commerce, not composed)",
                "Order uses Ledger's TICVAI.ArchitectureTests.Planted.Features.Ledger.Internal.Journal, not its Public API",
                "Unknown is not a module of ADR-0055 (modules.json)",
            ],
            violations);
    }

    private static IEnumerable<string> Check(string assemblyPath, Regex pattern, ModuleMap map)
    {
        using var assembly = AssemblyDefinition.ReadAssembly(assemblyPath);
        var found = new SortedSet<string>(StringComparer.Ordinal);
        foreach (var type in assembly.MainModule.GetTypes())
        {
            var owner = ModuleOf(type, pattern);
            if (owner is null)
            {
                continue;
            }

            if (!map.Deployable.ContainsKey(owner.Value.Module))
            {
                found.Add($"{owner.Value.Module} is not a module of ADR-0055 (modules.json)");
                continue;
            }

            foreach (var used in References(type))
            {
                var target = ModuleOf(used, pattern);
                if (target is null || target.Value.Module == owner.Value.Module || !map.Deployable.ContainsKey(target.Value.Module))
                {
                    continue;
                }

                var from = map.Deployable[owner.Value.Module];
                var to = map.Deployable[target.Value.Module];
                if (!target.Value.IsPublic)
                {
                    found.Add($"{owner.Value.Module} uses {target.Value.Module}'s {used.FullName}, not its Public API");
                }
                else if (from != to && !map.Composes.Contains((from, target.Value.Module)))
                {
                    found.Add($"{owner.Value.Module} uses {target.Value.Module} across deployables ({from} -> {to}, not composed)");
                }
            }
        }

        return found;
    }

    private static (string Module, bool IsPublic)? ModuleOf(TypeReference type, Regex pattern)
    {
        while (type.DeclaringType is not null)
        {
            type = type.DeclaringType;
        }

        var match = pattern.Match(type.Namespace ?? string.Empty);
        return match.Success
            ? (match.Groups["module"].Value, match.Groups["rest"].Value is ".Public" || match.Groups["rest"].Value.StartsWith(".Public.", StringComparison.Ordinal))
            : null;
    }

    private static IEnumerable<TypeReference> References(TypeDefinition type)
    {
        var all = new List<TypeReference>();
        void Add(TypeReference? reference)
        {
            switch (reference)
            {
                case null:
                    return;
                case GenericInstanceType generic:
                    Add(generic.ElementType);
                    generic.GenericArguments.ToList().ForEach(Add);
                    return;
                case TypeSpecification specification:
                    Add(specification.ElementType);
                    return;
                default:
                    all.Add(reference);
                    return;
            }
        }

        void Attributes(ICustomAttributeProvider provider)
        {
            foreach (var attribute in provider.CustomAttributes)
            {
                Add(attribute.AttributeType);
            }
        }

        Add(type.BaseType);
        Attributes(type);
        type.Interfaces.ToList().ForEach(i => Add(i.InterfaceType));
        type.Fields.ToList().ForEach(f => { Add(f.FieldType); Attributes(f); });
        type.Properties.ToList().ForEach(p => { Add(p.PropertyType); Attributes(p); });
        type.Events.ToList().ForEach(e => Add(e.EventType));
        foreach (var method in type.Methods)
        {
            Attributes(method);
            Add(method.ReturnType);
            method.Parameters.ToList().ForEach(p => Add(p.ParameterType));
            if (!method.HasBody)
            {
                continue;
            }

            method.Body.Variables.ToList().ForEach(v => Add(v.VariableType));
            foreach (var instruction in method.Body.Instructions)
            {
                switch (instruction.Operand)
                {
                    case TypeReference t:
                        Add(t);
                        break;
                    case MethodReference m:
                        Add(m.DeclaringType);
                        Add(m.ReturnType);
                        m.Parameters.ToList().ForEach(p => Add(p.ParameterType));
                        if (m is GenericInstanceMethod gm)
                        {
                            gm.GenericArguments.ToList().ForEach(Add);
                        }

                        break;
                    case FieldReference f:
                        Add(f.DeclaringType);
                        Add(f.FieldType);
                        break;
                }
            }
        }

        return all;
    }

    private sealed record ModuleMap(IReadOnlyDictionary<string, string> Deployable, IReadOnlySet<(string Reader, string Module)> Composes)
    {
        public static ModuleMap Load()
        {
            using var document = JsonDocument.Parse(File.ReadAllText(Path.Combine(AppContext.BaseDirectory, "modules.json")));
            var root = document.RootElement;
            return new ModuleMap(
                root.GetProperty("modules").EnumerateArray().ToDictionary(m => m.GetProperty("name").GetString()!, m => m.GetProperty("deployable").GetString()!),
                root.GetProperty("composes").EnumerateArray().Select(c => (c.GetProperty("reader").GetString()!, c.GetProperty("module").GetString()!)).ToHashSet());
        }
    }
}
