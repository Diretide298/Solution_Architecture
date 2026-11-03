namespace TICVAI.Application.Abstractions.Security;

/// <summary>
/// The lookup on the published per-scope set (spec 7.2 and 7.3, ADAM CR-367), the same rule a client
/// applies to <c>Session.permissionsByScope</c>.
/// </summary>
public static class PermissionsByScopeLookup
{
    /// <summary>
    /// A permission holds at <paramref name="node"/> when it is in the entry of the deepest listed path
    /// that contains the node: the node's own entry, else its nearest listed ancestor's. Entries are
    /// never combined, and a node no listed path contains holds nothing. Never "the node or any
    /// ancestor": an ancestor's entry cannot carry a deny that sits below it (vectors V07, V08, V12).
    /// </summary>
    public static bool Holds(IReadOnlyDictionary<string, IReadOnlySet<string>> permissionsByScope, string node, string permission)
    {
        ArgumentNullException.ThrowIfNull(permissionsByScope);
        string? deepest = null;
        foreach (var path in permissionsByScope.Keys)
        {
            if (ScopePath.Contains(path, node) && (deepest is null || path.Length > deepest.Length))
            {
                deepest = path;
            }
        }

        return deepest is not null && permissionsByScope[deepest].Contains(permission);
    }
}
