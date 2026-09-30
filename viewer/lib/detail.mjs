// What /api/index holds back, and the split that holds it back.
//
// Moved out of server.mjs so a release view (lib/release-diff.mjs) splits an
// older tag's index exactly the way the served one is split: the connector's
// tools read the slim index and the per-file detail, and a diff between two
// tags is only honest if both sides went through the same door.

// Held out of the slim index and served per contract: an operation's parameters,
// responses and request body are what `adam_contract` with `operation` returns.
export const DETAIL_FIELDS = ['description', 'properties', 'parameters', 'responses', 'requestBody', 'body', 'security', 'extensions'];

export function splitDetail(full) {
  const slim = { ...full, nodes: [] };
  const byFile = new Map();
  for (const node of full.nodes) {
    const lean = {};
    const heavy = {};
    for (const [key, value] of Object.entries(node)) {
      if (DETAIL_FIELDS.includes(key)) heavy[key] = value;
      else lean[key] = value;
    }
    slim.nodes.push(lean);
    if (!Object.keys(heavy).length) continue;
    if (!byFile.has(node.file)) byFile.set(node.file, {});
    byFile.get(node.file)[node.id] = heavy;
  }
  return { slim, byFile };
}

