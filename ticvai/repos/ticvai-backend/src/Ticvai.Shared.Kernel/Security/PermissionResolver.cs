namespace Ticvai.Shared.Kernel.Security;

public enum ScopeLevel
{
    Tenant = 0,
    Brand = 1,
    Region = 2,
    Venue = 3,
    Department = 4,
    SubDepartment = 5,
    Workstation = 6
}

public enum GrantEffect
{
    Allow = 0,
    Deny = 1
}

/// <summary>A node in the tenant hierarchy, addressed by materialised ltree path.</summary>
/// <param name="Level">Hierarchy level of this node.</param>
/// <param name="Id">Node identifier.</param>
/// <param name="Path">Materialised path, e.g. <c>t_miral.b_themepark.r_oman.v_f1oman</c>.</param>
/// <param name="IsActive">
/// False suppresses every permission at or beneath this node. Rule R9.
/// </param>
public readonly record struct ScopeNode(ScopeLevel Level, Guid Id, string Path, bool IsActive = true)
{
    /// <summary>True when <paramref name="other"/> is this node or beneath it.</summary>
    public bool Contains(ScopeNode other) =>
        other.Path.Equals(Path, StringComparison.Ordinal) ||
        other.Path.StartsWith(Path + ".", StringComparison.Ordinal);

    public int Depth => Path.Count(c => c == '.');
}

/// <summary>A permission grant attached to a principal at a scope node.</summary>
public sealed record PermissionGrant
{
    public required Guid PrincipalId { get; init; }
    public required string Permission { get; init; }
    public required ScopeNode Scope { get; init; }
    public required GrantEffect Effect { get; init; }

    /// <summary>Rule R10. Null means no lower bound.</summary>
    public DateTimeOffset? ValidFrom { get; init; }

    /// <summary>Rule R10. Null means no upper bound.</summary>
    public DateTimeOffset? ValidTo { get; init; }

    public bool IsEffectiveAt(DateTimeOffset at) =>
        (ValidFrom is null || ValidFrom <= at) &&
        (ValidTo is null || ValidTo > at);
}

/// <summary>The resolved permission set for a session.</summary>
public sealed record EffectivePermissions
{
    public required Guid PrincipalId { get; init; }
    public required IReadOnlySet<string> Permissions { get; init; }
    public required IReadOnlyList<ScopeNode> Scopes { get; init; }

    /// <summary>Permissions keyed by the scope paths at which they are effective.</summary>
    public required IReadOnlyDictionary<string, IReadOnlySet<string>> ByScopePath { get; init; }

    /// <summary>
    /// Permissions that would have been allowed but for a deny, with the node that
    /// suppressed them.
    /// </summary>
    /// <remarks>
    /// Surfaced by <c>POST /permissions/resolve</c>. Under deny-overrides-allow across seven
    /// levels, "why can this person not do X" is otherwise unanswerable without reading the
    /// whole grant set by hand.
    /// </remarks>
    public required IReadOnlyList<SuppressedPermission> SuppressedByDeny { get; init; }

    public bool Has(string permission) => Permissions.Contains(permission);

    /// <summary>
    /// True when <paramref name="permission"/> is effective at <paramref name="scopePath"/>
    /// or at any ancestor of it.
    /// </summary>
    public bool HasAt(string permission, string scopePath)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(permission);
        ArgumentException.ThrowIfNullOrWhiteSpace(scopePath);

        var segments = scopePath.Split('.');
        for (var take = segments.Length; take > 0; take--)
        {
            var ancestor = string.Join('.', segments[..take]);
            if (ByScopePath.TryGetValue(ancestor, out var permissions) && permissions.Contains(permission))
            {
                return true;
            }
        }

        return false;
    }
}

/// <param name="Permission">The permission that was suppressed.</param>
/// <param name="AllowedAtScopePath">Where it was granted.</param>
/// <param name="DeniedAtScopePath">The node whose deny suppressed it.</param>
public readonly record struct SuppressedPermission(
    string Permission,
    string AllowedAtScopePath,
    string DeniedAtScopePath);

/// <summary>
/// Resolves a principal's effective permissions across the tenant hierarchy.
/// </summary>
/// <remarks>
/// <para>
/// Project Direction §3.1.1: authorisation is user/role-driven. A user logs in from
/// any device and carries their access. Workstation determines presentation,
/// hardware binding, till identity and reporting dimension — never authorisation.
/// </para>
/// <para>
/// §3.1.8: resolution is <b>deny-overrides-allow</b>. A deny at any node in a
/// principal's grant set suppresses that permission for the node and everything
/// beneath it, regardless of allows at other depths. This is deliberately strict:
/// the hierarchy diagram asserts "no cross-venue data access unless explicitly
/// permitted", and a permissive default would silently violate it.
/// </para>
/// <para>
/// Resolved once at login and cached in the session registry, not evaluated per
/// request. A 7-level tree across 70+ venues cannot be walked with recursive CTEs
/// at 1,000 req/s.
/// </para>
/// </remarks>
public interface IPermissionResolver
{
    EffectivePermissions Resolve(
        Guid principalId,
        IReadOnlyList<PermissionGrant> grants,
        DateTimeOffset? asAt = null);
}

public sealed class PermissionResolver : IPermissionResolver
{
    private const string Wildcard = "*";

    public EffectivePermissions Resolve(
        Guid principalId,
        IReadOnlyList<PermissionGrant> grants,
        DateTimeOffset? asAt = null)
    {
        ArgumentNullException.ThrowIfNull(grants);

        var evaluationTime = asAt ?? DateTimeOffset.UtcNow;

        // R10 - expired or not-yet-valid grants are excluded BEFORE resolution, not filtered
        // afterwards. A grant outside its window is not a grant.
        //
        // R9 - a grant whose own node is inactive is excluded here. Inactive ANCESTORS are
        // handled by IScopeActivationChecker, because the grant may sit above the inactive
        // node and the resolver does not hold the tree.
        var owned = grants
            .Where(g => g.PrincipalId == principalId)
            .Where(g => g.IsEffectiveAt(evaluationTime))
            .Where(g => g.Scope.IsActive)
            .ToArray();

        var denies = owned.Where(g => g.Effect == GrantEffect.Deny).ToArray();
        var allows = owned.Where(g => g.Effect == GrantEffect.Allow).ToArray();

        var byScopePath = new Dictionary<string, IReadOnlySet<string>>(StringComparer.Ordinal);
        var flattened = new HashSet<string>(StringComparer.Ordinal);
        var effectiveScopes = new List<ScopeNode>();
        var suppressed = new List<SuppressedPermission>();

        foreach (var group in allows.GroupBy(g => g.Scope.Path, StringComparer.Ordinal))
        {
            var scope = group.First().Scope;
            var permissions = new HashSet<string>(StringComparer.Ordinal);

            foreach (var grant in group)
            {
                var denyingNode = FindDenyingNode(grant.Permission, scope, denies);

                if (denyingNode is not null)
                {
                    suppressed.Add(new SuppressedPermission(grant.Permission, scope.Path, denyingNode));
                    continue;
                }

                permissions.Add(grant.Permission);
            }

            if (permissions.Count == 0)
            {
                continue;
            }

            byScopePath[group.Key] = permissions;
            flattened.UnionWith(permissions);
            effectiveScopes.Add(scope);
        }

        return new EffectivePermissions
        {
            PrincipalId = principalId,
            Permissions = flattened,
            Scopes = effectiveScopes
                .OrderBy(s => s.Depth)
                .ThenBy(s => s.Path, StringComparer.Ordinal)
                .ToList(),
            ByScopePath = byScopePath,
            SuppressedByDeny = suppressed
        };
    }

    /// <summary>
    /// Returns the path of the node whose deny suppresses <paramref name="permission"/> at
    /// <paramref name="scope"/>, or null when nothing denies it.
    /// </summary>
    /// <remarks>
    /// A permission is denied when a deny grant sits at the scope itself or at any ancestor.
    /// Denies inherit downward and are never overridden by a more specific allow - R2.
    ///
    /// The wildcard applies to denies only - R4. A wildcard allow would be an accident
    /// waiting to happen; it is rejected at grant creation and not honoured here.
    /// </remarks>
    private static string? FindDenyingNode(
        string permission,
        ScopeNode scope,
        IReadOnlyList<PermissionGrant> denies)
    {
        string? deepest = null;
        var deepestDepth = -1;

        foreach (var deny in denies)
        {
            var matchesPermission =
                string.Equals(deny.Permission, permission, StringComparison.Ordinal) ||
                string.Equals(deny.Permission, Wildcard, StringComparison.Ordinal);

            if (!matchesPermission || !deny.Scope.Contains(scope))
            {
                continue;
            }

            // Report the DEEPEST denying node. The most specific explanation is the most
            // useful one when an administrator asks why a permission is missing.
            if (deny.Scope.Depth > deepestDepth)
            {
                deepest = deny.Scope.Path;
                deepestDepth = deny.Scope.Depth;
            }
        }

        return deepest;
    }
}

/// <summary>
/// Checks whether every node on a path is active. Rule R9.
/// </summary>
/// <remarks>
/// Separate from <see cref="PermissionResolver"/> because it needs the tree, not the grant
/// set. The caller loads the inactive-node set once at login and passes it in - walking the
/// tree per query would defeat resolving once (R7).
/// </remarks>
public interface IScopeActivationChecker
{
    /// <summary>False when the node or any ancestor is inactive.</summary>
    bool IsPathActive(string scopePath);
}

public sealed class ScopeActivationChecker : IScopeActivationChecker
{
    private readonly HashSet<string> _inactivePaths;

    /// <param name="inactivePaths">
    /// Paths of every inactive node in the tenant. Loaded once at login; small, because
    /// inactive nodes are rare.
    /// </param>
    public ScopeActivationChecker(IEnumerable<string> inactivePaths)
    {
        ArgumentNullException.ThrowIfNull(inactivePaths);
        _inactivePaths = inactivePaths.ToHashSet(StringComparer.Ordinal);
    }

    public bool IsPathActive(string scopePath)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(scopePath);

        if (_inactivePaths.Count == 0)
        {
            return true;
        }

        var segments = scopePath.Split('.');

        for (var take = 1; take <= segments.Length; take++)
        {
            var ancestor = string.Join('.', segments[..take]);
            if (_inactivePaths.Contains(ancestor))
            {
                return false;
            }
        }

        return true;
    }
}
