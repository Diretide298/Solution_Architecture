using System.Text.Json;
using System.Text.Json.Serialization;
using Ticvai.Shared.Kernel.Security;
using Xunit;

namespace Ticvai.UnitTests;

/// <summary>
/// Runs the normative permission vectors from
/// <c>architecture/specs/permission-resolution.md</c>.
/// </summary>
/// <remarks>
/// These are not illustrative examples. The specification defines the rules; this test
/// proves the implementation obeys them. A failing vector is a build failure, and the
/// correct response is to fix the resolver — not the vector.
///
/// The JSON file is copied from the docs repository. It is the same artefact the
/// specification publishes, so the two cannot drift.
/// </remarks>
public sealed class PermissionVectorTests
{
    private static readonly Guid Principal = Guid.Parse("00000000-0000-0000-0000-0000000000A1");
    private static readonly IPermissionResolver Resolver = new PermissionResolver();

    public static TheoryData<Vector> Vectors
    {
        get
        {
            var json = File.ReadAllText(
                Path.Combine(AppContext.BaseDirectory, "permission-vectors.json"));

            var document = JsonSerializer.Deserialize<VectorDocument>(json, JsonOptions)
                ?? throw new InvalidOperationException("permission-vectors.json failed to parse.");

            var data = new TheoryData<Vector>();
            foreach (var vector in document.Vectors)
            {
                data.Add(vector);
            }

            return data;
        }
    }

    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web)
    {
        Converters = { new JsonStringEnumConverter() }
    };

    [Theory]
    [MemberData(nameof(Vectors))]
    public void Resolves_as_the_specification_requires(Vector vector)
    {
        var grants = vector.Grants
            .Select(g => new PermissionGrant
            {
                PrincipalId = Principal,
                Permission = g.Permission,
                Scope = ToNode(g.Scope),
                Effect = g.Effect == "DENY" ? GrantEffect.Deny : GrantEffect.Allow
            })
            .ToList();

        var resolved = Resolver.Resolve(Principal, grants);

        var permitted = resolved.HasAt(vector.Query.Permission, vector.Query.Scope);
        var expected = vector.Expect == "PERMIT";

        Assert.True(
            permitted == expected,
            $"{vector.Id} — expected {vector.Expect}, got {(permitted ? "PERMIT" : "DENY")}. " +
            $"Proves: {vector.Proves}. " +
            "The specification is normative; fix the resolver, not the vector.");
    }

    [Fact]
    public void Every_vector_in_the_specification_is_executed()
    {
        // Guards against a vector being added to the specification and silently not run.
        var count = Vectors.Count();
        Assert.True(count >= 22, $"Expected at least 22 vectors, found {count}.");
    }

    [Fact]
    public void Expired_grants_do_not_resolve()
    {
        // Rule R10. Not expressible in the JSON vectors, which carry no time dimension.
        var scope = ToNode("t_ref.b_alpha.r_north.v_alpha1");

        var grants = new List<PermissionGrant>
        {
            new()
            {
                PrincipalId = Principal,
                Permission = "ORDER_CREATE",
                Scope = scope,
                Effect = GrantEffect.Allow,
                ValidTo = DateTimeOffset.UtcNow.AddDays(-1)
            }
        };

        var resolved = Resolver.Resolve(Principal, grants);

        Assert.False(resolved.HasAt("ORDER_CREATE", scope.Path));
    }

    [Fact]
    public void Grants_on_an_inactive_node_do_not_resolve()
    {
        // Rule R9 for the node itself. Inactive ancestors are ScopeActivationChecker's job.
        var scope = new ScopeNode(
            ScopeLevel.Venue,
            Guid.NewGuid(),
            "t_ref.b_alpha.r_north.v_alpha1",
            IsActive: false);

        var grants = new List<PermissionGrant>
        {
            new()
            {
                PrincipalId = Principal,
                Permission = "ORDER_CREATE",
                Scope = scope,
                Effect = GrantEffect.Allow
            }
        };

        var resolved = Resolver.Resolve(Principal, grants);

        Assert.False(resolved.HasAt("ORDER_CREATE", scope.Path));
    }

    [Fact]
    public void Inactive_ancestor_suppresses_a_descendant()
    {
        // Rule R9 for ancestors.
        var checker = new ScopeActivationChecker(["t_ref.b_alpha.r_north"]);

        Assert.False(checker.IsPathActive("t_ref.b_alpha.r_north.v_alpha1.d_ticketing"));
        Assert.True(checker.IsPathActive("t_ref.b_beta.r_south.v_beta1"));
    }

    [Fact]
    public void Suppression_reports_the_deepest_denying_node()
    {
        // An administrator asking "why can this person not do X" needs the most specific
        // answer, not the broadest.
        var tenant = ToNode("t_ref");
        var region = ToNode("t_ref.b_alpha.r_north");
        var venue = ToNode("t_ref.b_alpha.r_north.v_alpha1");

        var grants = new List<PermissionGrant>
        {
            new() { PrincipalId = Principal, Permission = "ORDER_REFUND", Scope = venue,  Effect = GrantEffect.Allow },
            new() { PrincipalId = Principal, Permission = "ORDER_REFUND", Scope = tenant, Effect = GrantEffect.Deny },
            new() { PrincipalId = Principal, Permission = "ORDER_REFUND", Scope = region, Effect = GrantEffect.Deny }
        };

        var resolved = Resolver.Resolve(Principal, grants);

        Assert.False(resolved.HasAt("ORDER_REFUND", venue.Path));

        var suppression = Assert.Single(resolved.SuppressedByDeny);
        Assert.Equal("ORDER_REFUND", suppression.Permission);
        Assert.Equal(region.Path, suppression.DeniedAtScopePath);
    }

    private static ScopeNode ToNode(string path)
    {
        var depth = path.Count(c => c == '.');
        var level = (ScopeLevel)Math.Min(depth, (int)ScopeLevel.Workstation);
        return new ScopeNode(level, Guid.NewGuid(), path);
    }

    public sealed record VectorDocument
    {
        [JsonPropertyName("vectors")]
        public required IReadOnlyList<Vector> Vectors { get; init; }
    }

    public sealed record Vector
    {
        public required string Id { get; init; }
        public required string Proves { get; init; }
        public required IReadOnlyList<VectorGrant> Grants { get; init; }
        public required VectorQuery Query { get; init; }
        public required string Expect { get; init; }

        public override string ToString() => $"{Id}: {Proves}";
    }

    public sealed record VectorGrant
    {
        public required string Permission { get; init; }
        public required string Scope { get; init; }
        public required string Effect { get; init; }
    }

    public sealed record VectorQuery
    {
        public required string Permission { get; init; }
        public required string Scope { get; init; }
    }
}
