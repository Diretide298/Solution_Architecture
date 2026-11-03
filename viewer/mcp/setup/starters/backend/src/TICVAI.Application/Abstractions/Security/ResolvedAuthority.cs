using System.Collections.Frozen;

namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// What the signed-in principal may do, resolved once at login from the selected role's grants (R6,
/// R7) and cached in the session registry. <b>The seam every operation's permission check goes
/// through</b>: <see cref="Permits"/> answers section 2 of
/// <c>docs/architecture/specs/permission-resolution.md</c> at the scope the operation acts on
/// (spec 7.2, ADAM CR-189 and CR-367).
/// </summary>
/// <remarks>
/// <para>
/// The algorithm: a deny of the permission (or a wildcard deny) at the target or any ancestor of it
/// denies, always (R2, R4); otherwise an allow of the permission at the target or an ancestor permits
/// (R3: downward only); otherwise deny (R1). Expired grants are dropped before resolution (R10), and a
/// target under an inactive scope node is denied (R9). Grants from another cell never reach this cell's
/// session (R8: another cell is another database).
/// </para>
/// <para>
/// <b>The flat set is for coarse checks only.</b> <see cref="EffectivePermissions"/> says a permission
/// is held somewhere; it never decides an operation, because a permission held at venue A plus anything
/// at venue B puts it in the flat set (spec 7.2). Decide with <see cref="Permits"/>.
/// </para>
/// <para>
/// <see cref="PermissionsByScope"/> is the published per-scope set the session hands clients
/// (<c>Session.permissionsByScope</c>, CR-367): one entry for every path where the role holds a grant,
/// allow or deny; a node's answer is the entry of the deepest listed path that contains it
/// (<see cref="PermissionsByScopeLookup"/>). Both forms give the same answer on every vector of
/// <c>permission-vectors.json</c>; the unit tests run all of them through both.
/// </para>
/// </remarks>
public sealed class ResolvedAuthority
{
    private readonly IReadOnlyList<Grant> _grants;
    private readonly IReadOnlySet<string> _inactiveScopePaths;

    /// <param name="selectedRoleGrants">The grants of the role the principal signed in with, and no other (R6).</param>
    /// <param name="now">The resolution time: grants whose <c>ValidTo</c> is before it are excluded (R10).</param>
    /// <param name="inactiveScopePaths">Scope nodes with <c>is_active = false</c>; a target at or under one is denied (R9).</param>
    public ResolvedAuthority(IEnumerable<Grant> selectedRoleGrants, DateTimeOffset now, IEnumerable<string>? inactiveScopePaths = null)
    {
        ArgumentNullException.ThrowIfNull(selectedRoleGrants);
        _grants = selectedRoleGrants.Where(g => g.ValidTo is null || g.ValidTo >= now).ToList();
        _inactiveScopePaths = (inactiveScopePaths ?? []).ToFrozenSet(StringComparer.Ordinal);
        EffectivePermissions = _grants
            .Where(g => g.Effect == GrantEffect.Allow && g.Permission != Grant.Wildcard)
            .Select(g => g.Permission)
            .Distinct(StringComparer.Ordinal)
            .Where(p => _grants.Any(g => Permits(p, g.ScopePath)))
            .ToFrozenSet(StringComparer.Ordinal);
    }

    /// <summary>No grants: everything is denied (R1). The seam's value before sign-in fills it.</summary>
    public static ResolvedAuthority None { get; } = new([], DateTimeOffset.MinValue);

    /// <summary>
    /// Permissions permitted at one scope path at least. Coarse checks only (a menu, a first gate);
    /// never decides an operation (spec 7.2).
    /// </summary>
    public IReadOnlySet<string> EffectivePermissions { get; }

    /// <summary>
    /// Section 2: may this principal use <paramref name="permission"/> at <paramref name="scopePath"/>?
    /// Call it with the scope the operation acts on (its <c>x-ticvai-scope-level</c>): the venue, the
    /// workstation, or the tenant root for a tenant-level operation.
    /// </summary>
    public bool Permits(string permission, string scopePath)
    {
        ArgumentException.ThrowIfNullOrEmpty(permission);
        ArgumentException.ThrowIfNullOrEmpty(scopePath);
        if (permission == Grant.Wildcard || _inactiveScopePaths.Any(inactive => ScopePath.Contains(inactive, scopePath)))
        {
            return false;
        }

        var denied = _grants.Any(g => g.Effect == GrantEffect.Deny
            && (g.Permission == permission || g.Permission == Grant.Wildcard)
            && ScopePath.Contains(g.ScopePath, scopePath));
        if (denied)
        {
            return false;
        }

        return _grants.Any(g => g.Effect == GrantEffect.Allow
            && g.Permission == permission
            && ScopePath.Contains(g.ScopePath, scopePath));
    }

    /// <summary>
    /// The scope paths of <paramref name="permission"/>'s allows that are still permitted after deny
    /// processing: the resolved allow set the session puts in <c>ticvai.scope_paths</c> for an
    /// operation that needs it (spec 7.1). A list's reach is these paths; a filter outside them is 403.
    /// </summary>
    public IReadOnlyList<string> ScopePathsPermitting(string permission) => _grants
        .Where(g => g.Effect == GrantEffect.Allow && g.Permission == permission && Permits(permission, g.ScopePath))
        .Select(g => g.ScopePath)
        .Distinct(StringComparer.Ordinal)
        .OrderBy(p => p, StringComparer.Ordinal)
        .ToList();

    /// <summary>
    /// The published per-scope set (spec 7.2, CR-367): one entry for every scope path where the role
    /// holds a grant, allow or deny (a wildcard deny included); each entry is the full section 2 result
    /// at that path. Entries are never combined: look a node up with <see cref="PermissionsByScopeLookup.Holds"/>.
    /// </summary>
    public IReadOnlyDictionary<string, IReadOnlySet<string>> PermissionsByScope()
    {
        var allowed = _grants
            .Where(g => g.Effect == GrantEffect.Allow && g.Permission != Grant.Wildcard)
            .Select(g => g.Permission)
            .Distinct(StringComparer.Ordinal)
            .ToList();
        return _grants
            .Select(g => g.ScopePath)
            .Distinct(StringComparer.Ordinal)
            .ToDictionary(
                path => path,
                path => (IReadOnlySet<string>)allowed.Where(p => Permits(p, path)).ToFrozenSet(StringComparer.Ordinal),
                StringComparer.Ordinal);
    }
}
