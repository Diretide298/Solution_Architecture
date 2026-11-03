namespace TICVAI.Application.Abstractions.Security;

/// <summary>Scope-tree paths as ltree text: <c>t_ref.b_alpha.r_north.v_alpha1</c> (spec 1.1).</summary>
public static class ScopePath
{
    /// <summary>
    /// <paramref name="ancestor"/> contains <paramref name="node"/> when they are equal or the node
    /// starts with the ancestor plus a dot (spec 1.2). Downward only: <c>t_a.b_x</c> does not contain
    /// <c>t_a.b_xy</c>, and a venue does not contain its region.
    /// </summary>
    public static bool Contains(string ancestor, string node)
    {
        ArgumentException.ThrowIfNullOrEmpty(ancestor);
        ArgumentException.ThrowIfNullOrEmpty(node);
        return node.Length == ancestor.Length
            ? string.Equals(node, ancestor, StringComparison.Ordinal)
            : node.Length > ancestor.Length && node[ancestor.Length] == '.' && node.StartsWith(ancestor, StringComparison.Ordinal);
    }
}
