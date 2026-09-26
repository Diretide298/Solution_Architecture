using System.Reflection;

namespace TICVAI.ArchitectureTests;

/// <summary>The reference rules in CLAUDE.md, checked on the built assemblies.</summary>
public class LayerTests
{
    private static readonly string[] Layers = ["TICVAI.Domain", "TICVAI.Contracts", "TICVAI.Application", "TICVAI.Infrastructure", "TICVAI.Api"];

    [Theory]
    [InlineData("TICVAI.Domain")]
    [InlineData("TICVAI.Contracts")]
    [InlineData("TICVAI.Application", "TICVAI.Domain", "TICVAI.Contracts")]
    [InlineData("TICVAI.Infrastructure", "TICVAI.Application", "TICVAI.Domain", "TICVAI.Contracts")]
    public void A_layer_references_only_what_it_may(string layer, params string[] allowed)
    {
        var references = Assembly.Load(layer).GetReferencedAssemblies()
            .Select(a => a.Name!)
            .Where(name => Layers.Contains(name))
            .ToList();

        Assert.Empty(references.Except(allowed));
    }
}
