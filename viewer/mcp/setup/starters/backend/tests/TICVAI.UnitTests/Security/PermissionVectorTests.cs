using System.Text.Json;
using TICVAI.Application.Abstractions.Security;

namespace TICVAI.UnitTests.Security;

/// <summary>
/// <b>Normative</b> (permission-resolution spec, section 5): every vector of
/// <c>PermissionVectors.json</c>, a byte-identical copy of the package's
/// <c>docs/architecture/specs/permission-vectors.json</c>, run through the seam operations decide with
/// (<see cref="ResolvedAuthority.Permits"/>) and through the published per-scope set's lookup
/// (<see cref="PermissionsByScopeLookup.Holds"/>, spec 7.2, ADAM CR-367). A failing vector is a build failure.
/// </summary>
public class PermissionVectorTests
{
    private static readonly DateTimeOffset Now = new(2026, 11, 3, 9, 0, 0, TimeSpan.Zero);

    public static TheoryData<string> Vectors()
    {
        var data = new TheoryData<string>();
        foreach (var vector in Load())
        {
            data.Add(vector.GetProperty("id").GetString()!);
        }

        return data;
    }

    [Fact]
    public void Every_vector_of_the_spec_file_is_here()
    {
        Assert.Equal(22, Load().Count);
    }

    [Theory]
    [MemberData(nameof(Vectors))]
    public void The_seam_answers_what_the_vector_expects(string id)
    {
        var (authority, permission, scope, expect) = Vector(id);

        Assert.Equal(expect, authority.Permits(permission, scope));
    }

    [Theory]
    [MemberData(nameof(Vectors))]
    public void The_published_set_looked_up_by_the_deepest_entry_answers_the_same(string id)
    {
        var (authority, permission, scope, expect) = Vector(id);

        Assert.Equal(expect, PermissionsByScopeLookup.Holds(authority.PermissionsByScope(), scope, permission));
    }

    [Fact]
    public void An_expired_grant_is_excluded_before_resolution_R10()
    {
        var authority = new ResolvedAuthority([new Grant("USER_MANAGE", "t_ref", GrantEffect.Allow, Now.AddDays(-1))], Now);

        Assert.False(authority.Permits("USER_MANAGE", "t_ref.b_alpha.r_north.v_alpha1"));
    }

    [Fact]
    public void A_target_under_an_inactive_node_is_denied_R9()
    {
        var authority = new ResolvedAuthority(
            [new Grant("USER_MANAGE", "t_ref.b_alpha.r_north.v_alpha1", GrantEffect.Allow)], Now, ["t_ref.b_alpha.r_north.v_alpha1"]);

        Assert.False(authority.Permits("USER_MANAGE", "t_ref.b_alpha.r_north.v_alpha1"));
    }

    [Fact]
    public void A_wildcard_allow_grants_nothing_R4()
    {
        var authority = new ResolvedAuthority([new Grant(Grant.Wildcard, "t_ref", GrantEffect.Allow)], Now);

        Assert.False(authority.Permits("ORDER_CREATE", "t_ref"));
        Assert.Empty(authority.EffectivePermissions);
    }

    [Fact]
    public void The_flat_set_holds_a_permission_the_seam_refuses_at_another_venue()
    {
        // Why the flat set never decides an operation (spec 7.2): ORDER_REFUND at venue A is in it,
        // and venue B still refuses.
        var authority = new ResolvedAuthority([new Grant("ORDER_REFUND", "t_ref.b_alpha.r_north.v_alpha1", GrantEffect.Allow)], Now);

        Assert.Contains("ORDER_REFUND", authority.EffectivePermissions);
        Assert.False(authority.Permits("ORDER_REFUND", "t_ref.b_beta.r_south.v_beta1"));
    }

    [Fact]
    public void Containment_is_by_whole_labels()
    {
        Assert.True(ScopePath.Contains("t_a.b_x", "t_a.b_x.v_1"));
        Assert.False(ScopePath.Contains("t_a.b_x", "t_a.b_xy"));
        Assert.False(ScopePath.Contains("t_a.b_x.v_1", "t_a.b_x"));
    }

    private static (ResolvedAuthority Authority, string Permission, string Scope, bool Expect) Vector(string id)
    {
        var vector = Load().Single(v => v.GetProperty("id").GetString() == id);
        var grants = vector.GetProperty("grants").EnumerateArray().Select(g => new Grant(
            g.GetProperty("permission").GetString()!,
            g.GetProperty("scope").GetString()!,
            g.GetProperty("effect").GetString() == "DENY" ? GrantEffect.Deny : GrantEffect.Allow));
        var query = vector.GetProperty("query");
        return (
            new ResolvedAuthority(grants, Now),
            query.GetProperty("permission").GetString()!,
            query.GetProperty("scope").GetString()!,
            vector.GetProperty("expect").GetString() == "PERMIT");
    }

    private static List<JsonElement> Load()
    {
        var path = Path.Combine(AppContext.BaseDirectory, "PermissionVectors.json");
        using var document = JsonDocument.Parse(File.ReadAllText(path));
        return document.RootElement.GetProperty("vectors").EnumerateArray().Select(v => v.Clone()).ToList();
    }
}
