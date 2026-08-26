// Parses the TICVAI OpenAPI contracts into a link graph.
//
// Node ids are stable strings so the frontend can address anything by url hash:
//   file:contracts/spine/orders.yaml
//   op:contracts/spine/orders.yaml#listOrders
//   schema:contracts/shared/common.yaml#Money
//   param:contracts/shared/common.yaml#PageSize
//   response:contracts/shared/common.yaml#NotFound
//   perm:ORDER_VIEW

import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import yaml from 'js-yaml';
import { loadDeclaredConsumers, loadPlatforms, normalisePath } from './consumers.mjs';

const METHODS = ['get', 'put', 'post', 'delete', 'patch', 'head', 'options', 'trace'];

const REQUIRED_EXTENSIONS = [
  'x-ticvai-permission',
  'x-ticvai-scope-level',
  'x-ticvai-offline-capable',
  'x-ticvai-conflict-policy',
];

// components section -> node id prefix
const COMPONENT_KINDS = {
  schemas: 'schema',
  parameters: 'param',
  responses: 'response',
  requestBodies: 'requestBody',
  securitySchemes: 'securityScheme',
};

/** Recursively list every .yaml/.yml file under `dir`, as paths relative to `root`. */
async function listYamlFiles(dir, root) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      out.push(...(await listYamlFiles(full, root)));
    } else if (/\.ya?ml$/i.test(entry.name)) {
      out.push(path.relative(root, full).split(path.sep).join('/'));
    }
  }
  return out;
}

/**
 * Maps a YAML path ("components/schemas/Money") to its 1-based line number.
 *
 * Line-based rather than AST-based because js-yaml discards position info for
 * plain values. Block scalars are skipped wholesale so prose inside a
 * `description: >` block cannot register as a key.
 */
function buildLineMap(text) {
  const lines = text.split(/\r?\n/);
  const map = new Map();
  const stack = [];
  let blockScalarIndent = null;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];

    if (blockScalarIndent !== null) {
      if (!raw.trim()) continue; // blank lines belong to the block
      const indent = raw.length - raw.trimStart().length;
      if (indent > blockScalarIndent) continue; // still inside the block
      blockScalarIndent = null;
    }

    if (!raw.trim() || /^\s*#/.test(raw)) continue;

    const m = raw.match(/^(\s*)(?:-\s+)?(['"]?)([^\s#][^:]*?)\2\s*:(\s|$)/);
    if (!m) continue;

    const indent = m[1].length;
    const key = m[3].trim();

    while (stack.length && stack[stack.length - 1].indent >= indent) stack.pop();
    stack.push({ indent, key });
    map.set(stack.map((s) => s.key).join('/'), i + 1);

    // `description: >`, `description: |-` etc. open a block scalar
    if (/:\s*[|>][+-]?\d*\s*(#.*)?$/.test(raw)) blockScalarIndent = indent;
  }
  return map;
}

/**
 * Find repeated path keys inside the top-level `paths:` mapping.
 *
 * The parser cannot report these — by the time YAML is loaded the earlier block
 * is already gone — so this scans the source text and names the operations that
 * get shadowed.
 */
function findDuplicatePathKeys(text) {
  const lines = text.split(/\r?\n/);
  const seen = new Map();
  let inPaths = false;
  let current = null;

  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    if (/^paths:\s*$/.test(raw)) {
      inPaths = true;
      continue;
    }
    if (inPaths && /^[a-zA-Z]/.test(raw)) break; // next top-level key ends paths
    if (!inPaths) continue;

    const pathMatch = raw.match(/^  (\/\S*)\s*:\s*$/);
    if (pathMatch) {
      const key = pathMatch[1];
      if (!seen.has(key)) seen.set(key, { key, lines: [], blocks: [] });
      const record = seen.get(key);
      record.lines.push(i + 1);
      current = [];
      record.blocks.push(current);
      continue;
    }

    const opMatch = raw.match(/^\s+operationId:\s*(\S+)\s*$/);
    if (opMatch && current) current.push(opMatch[1]);
  }

  return [...seen.values()]
    .filter((record) => record.lines.length > 1)
    .map((record) => ({
      key: record.key,
      firstLine: record.lines[0],
      lines: record.lines,
      // every block but the last is discarded by the parser
      shadowed: record.blocks.slice(0, -1).flat(),
    }));
}

/** Collect every `$ref` string inside an arbitrary parsed subtree. */
function collectRefs(node, out = []) {
  if (!node || typeof node !== 'object') return out;
  if (Array.isArray(node)) {
    for (const item of node) collectRefs(item, out);
    return out;
  }
  for (const [key, value] of Object.entries(node)) {
    if (key === '$ref' && typeof value === 'string') out.push(value);
    else collectRefs(value, out);
  }
  return out;
}

/**
 * Turn a raw $ref into a node id.
 * Returns null for pointers we do not model as nodes (e.g. inline sub-paths).
 */
function resolveRef(ref, fromFile) {
  const [rawTarget, pointer = ''] = ref.split('#');
  const targetFile = rawTarget
    ? path.posix.normalize(path.posix.join(path.posix.dirname(fromFile), rawTarget))
    : fromFile;

  const parts = pointer.split('/').filter(Boolean); // ['components','schemas','Money']
  if (parts[0] !== 'components' || parts.length < 3) return null;

  const kind = COMPONENT_KINDS[parts[1]];
  if (!kind) return null;

  return { id: `${kind}:${targetFile}#${parts[2]}`, file: targetFile, kind, name: parts[2] };
}

/**
 * Resolve the schema a subtree points at, seeing through the array and
 * composition wrappers OpenAPI uses (`items`, `allOf`, `oneOf`, `anyOf`).
 */
function schemaTargetOf(spec, fromFile, depth = 0) {
  if (!spec || typeof spec !== 'object' || depth > 4) return null;

  if (typeof spec.$ref === 'string') {
    const resolved = resolveRef(spec.$ref, fromFile);
    return resolved?.kind === 'schema' ? { id: resolved.id, isArray: false } : null;
  }
  if (spec.type === 'array' && spec.items) {
    const inner = schemaTargetOf(spec.items, fromFile, depth + 1);
    return inner ? { ...inner, isArray: true } : null;
  }
  for (const key of ['allOf', 'oneOf', 'anyOf']) {
    if (Array.isArray(spec[key])) {
      for (const member of spec[key]) {
        const inner = schemaTargetOf(member, fromFile, depth + 1);
        if (inner) return inner;
      }
    }
  }
  return null;
}

/** Flatten a schema's own properties into displayable rows for the ER view. */
function describeProperties(definition, fromFile) {
  const properties = definition?.properties;
  if (!properties || typeof properties !== 'object') return [];
  const required = new Set(Array.isArray(definition.required) ? definition.required : []);

  return Object.entries(properties).map(([name, spec]) => {
    const target = schemaTargetOf(spec, fromFile);
    let type = spec?.type ?? (spec?.enum ? 'enum' : '');
    if (spec?.type === 'array') {
      type = `${spec.items?.type ?? (target ? '' : 'any')}[]`;
    }
    return {
      name,
      type: target ? '' : String(type ?? ''),
      format: spec?.format ?? null,
      required: required.has(name),
      refTarget: target?.id ?? null,
      isArray: Boolean(target?.isArray) || spec?.type === 'array',
      enumValues: Array.isArray(spec?.enum) ? spec.enum : null,
    };
  });
}

/** Schemas an operation reads in (request) and hands back (responses). */
function operationIO(op, fromFile) {
  const collect = (root) => {
    const found = new Map();
    const walk = (node, depth = 0) => {
      if (!node || typeof node !== 'object' || depth > 6) return;
      if (Array.isArray(node)) {
        for (const item of node) walk(item, depth + 1);
        return;
      }
      const target = schemaTargetOf(node, fromFile);
      if (target) found.set(target.id, target);
      for (const [key, value] of Object.entries(node)) {
        if (key === '$ref') continue;
        walk(value, depth + 1);
      }
    };
    walk(root);
    return [...found.keys()];
  };

  return {
    consumes: collect({ body: op.requestBody, params: op.parameters }),
    produces: collect(op.responses),
  };
}

/**
 * Platforms are declared as `"P04 POS"` — a code plus a label. Some entries
 * carry no code (`All platforms`, `Control Plane`), so the code is optional and
 * the raw string stays the identity.
 */
export function parsePlatform(raw) {
  const value = String(raw ?? '').trim();
  const match = value.match(/^(P\d+)\s+(.*)$/);
  return {
    raw: value,
    code: match ? match[1] : null,
    label: match ? match[2] : value,
    wildcard: /^all platforms$/i.test(value),
  };
}

/** The `info` block carries the module / platform taxonomy. */
function readTaxonomy(doc) {
  const info = doc.info ?? {};
  const platforms = (Array.isArray(info['x-ticvai-platforms']) ? info['x-ticvai-platforms'] : [])
    .map(parsePlatform)
    .filter((p) => p.raw);

  const capabilities = Array.isArray(info['x-ticvai-capabilities'])
    ? info['x-ticvai-capabilities'].map((c) => String(c).trim()).filter(Boolean)
    : [];

  return {
    tier: info['x-ticvai-tier'] ? String(info['x-ticvai-tier']).trim() : null,
    module: info['x-ticvai-module'] ? String(info['x-ticvai-module']).trim() : null,
    // Domain lens membership, declared once on the contract rather than on each
    // of its operations — the same inheritance the module and tier already use.
    // An operation may still override it, which is how one contract can put a
    // single operation in a different lens from the rest of its file.
    domains: info['x-ticvai-domain'] ?? null,
    platforms,
    capabilities,
    requirements: Number.isFinite(info['x-ticvai-requirements'])
      ? info['x-ticvai-requirements']
      : null,
  };
}

/** Modules read `"13 — Inventory Management"`; sort by that leading number. */
function moduleOrder(name) {
  const match = String(name).match(/^(\d+)/);
  return match ? Number(match[1]) : 999;
}

function titleFromFile(relPath) {
  return path.posix.basename(relPath).replace(/\.ya?ml$/i, '');
}

/** Group a contract by its folder: spine / satellite / shared / other. */
function groupFromFile(relPath) {
  const segments = relPath.split('/');
  return segments[segments.length - 2] ?? 'root';
}

export async function buildIndex(root, contractsDir = 'contracts') {
  const absContracts = path.join(root, contractsDir);
  const files = (await listYamlFiles(absContracts, root)).sort();

  const nodes = new Map();
  const edges = [];
  const problems = [];

  const addNode = (node) => {
    if (!nodes.has(node.id)) nodes.set(node.id, node);
    return nodes.get(node.id);
  };

  const addEdge = (source, target, kind) => {
    if (source === target) return;
    edges.push({ source, target, kind });
  };

  const permissionEnum = new Set();
  const usedPermissions = new Map(); // permission -> [opId]
  const declared = await loadDeclaredConsumers(root);
  const platformRoster = await loadPlatforms(root);
  let consumerMatches = 0;

  // ---- pass 1: parse every file -------------------------------------------
  for (const rel of files) {
    const text = await readFile(path.join(root, rel), 'utf8');
    const lineMap = buildLineMap(text);

    let doc;
    try {
      doc = yaml.load(text);
    } catch (err) {
      // Duplicate keys are the interesting failure: YAML silently keeps the last
      // definition, so a whole block of operations can vanish from the spec. Load
      // leniently so the viewer still works, then report what was shadowed.
      if (/duplicated mapping key/i.test(err.message)) {
        doc = yaml.load(text, { json: true });
      } else {
        problems.push({
          severity: 'error',
          kind: 'parse-error',
          file: rel,
          message: `YAML failed to parse: ${err.message}`,
        });
        continue;
      }
    }
    if (!doc || typeof doc !== 'object') continue;

    for (const dup of findDuplicatePathKeys(text)) {
      problems.push({
        severity: 'error',
        kind: 'duplicate-path',
        file: rel,
        line: dup.firstLine,
        message:
          `Path "${dup.key}" is defined twice (lines ${dup.firstLine} and ${dup.lines.slice(1).join(', ')}). ` +
          `YAML keeps only the last block, so ${dup.shadowed.length ? dup.shadowed.join(', ') : 'the earlier operations'} ` +
          `${dup.shadowed.length === 1 ? 'is' : 'are'} silently dropped from the spec. Merge the blocks.`,
      });
    }

    const fileId = `file:${rel}`;
    const taxonomy = readTaxonomy(doc);
    addNode({
      id: fileId,
      type: 'file',
      name: titleFromFile(rel),
      title: doc.info?.title ?? titleFromFile(rel),
      description: doc.info?.description ?? '',
      version: doc.info?.version ?? '',
      group: groupFromFile(rel),
      // declared taxonomy — authoritative, unlike the folder name
      tier: taxonomy.tier,
      module: taxonomy.module,
      platforms: taxonomy.platforms,
      capabilities: taxonomy.capabilities,
      requirements: taxonomy.requirements,
      file: rel,
      line: 1,
      lineCount: text.split(/\r?\n/).length,
      byteSize: Buffer.byteLength(text, 'utf8'),
      tags: (doc.tags ?? []).map((t) => t.name).filter(Boolean),
    });

    // ---- operations --------------------------------------------------------
    for (const [urlPath, pathItem] of Object.entries(doc.paths ?? {})) {
      if (!pathItem || typeof pathItem !== 'object') continue;

      for (const method of METHODS) {
        const op = pathItem[method];
        if (!op || typeof op !== 'object') continue;

        const operationId = op.operationId ?? `${method}${urlPath}`;
        const opId = `op:${rel}#${operationId}`;
        const permission = op['x-ticvai-permission'];
        const io = operationIO(op, rel);
        const consumers = declared.map.get(`${method.toUpperCase()} ${normalisePath(urlPath)}`) ?? [];
        if (consumers.length) consumerMatches += 1;

        addNode({
          id: opId,
          type: 'operation',
          name: operationId,
          title: op.summary ?? operationId,
          description: op.description ?? '',
          method: method.toUpperCase(),
          path: urlPath,
          file: rel,
          group: groupFromFile(rel),
          line: lineMap.get(`paths/${urlPath}/${method}`) ?? lineMap.get(`paths/${urlPath}`) ?? 1,
          tags: op.tags ?? [],
          deprecated: Boolean(op.deprecated),
          permission: permission ?? null,
          scopeLevel: op['x-ticvai-scope-level'] ?? null,
          offlineCapable: op['x-ticvai-offline-capable'] ?? null,
          conflictPolicy: op['x-ticvai-conflict-policy'] ?? null,
          auth: op['x-ticvai-auth'] ?? null,
          selfScoped: op['x-ticvai-self-scoped'] ?? null,
          // Which domain lens claims this, when a person has said so. The lens
          // also derives membership from the graph; this is the half that
          // carries intent, and the two are reconciled in lib/domains.mjs.
          domain: op['x-ticvai-domain'] ?? taxonomy.domains ?? null,
          guestCallable: op['x-ticvai-guest-callable'] ?? null,
          consumes: io.consumes,
          produces: io.produces,
          consumers,
          // inherited from the contract's info block, where the taxonomy lives
          module: taxonomy.module,
          tier: taxonomy.tier,
          platforms: taxonomy.platforms.map((p) => p.raw),
        });
        addEdge(fileId, opId, 'contains');

        // required extension audit — an op is exempt when it declares
        // x-ticvai-auth (service call) or an empty security block (public)
        const exempt = op['x-ticvai-auth'] || op['x-ticvai-self-scoped'] ||
          (Array.isArray(op.security) && op.security.length === 0);
        for (const ext of REQUIRED_EXTENSIONS) {
          if (op[ext] === undefined && !(exempt && ext === 'x-ticvai-permission')) {
            problems.push({
              severity: 'warning',
              kind: 'missing-extension',
              file: rel,
              line: lineMap.get(`paths/${urlPath}/${method}`) ?? 1,
              nodeId: opId,
              message: `${operationId} is missing ${ext}`,
            });
          }
        }

        if (permission) {
          if (!usedPermissions.has(permission)) usedPermissions.set(permission, []);
          usedPermissions.get(permission).push(opId);
        }

        for (const ref of collectRefs(op)) {
          const resolved = resolveRef(ref, rel);
          if (resolved) addEdge(opId, resolved.id, 'ref');
        }
      }
    }

    // ---- components --------------------------------------------------------
    for (const [section, kind] of Object.entries(COMPONENT_KINDS)) {
      const bucket = doc.components?.[section];
      if (!bucket || typeof bucket !== 'object') continue;

      for (const [name, definition] of Object.entries(bucket)) {
        const nodeId = `${kind}:${rel}#${name}`;
        addNode({
          id: nodeId,
          type: kind,
          name,
          title: name,
          description: definition?.description ?? '',
          file: rel,
          group: groupFromFile(rel),
          line: lineMap.get(`components/${section}/${name}`) ?? 1,
          dataType: definition?.type ?? null,
          required: definition?.required ?? [],
          propertyCount: definition?.properties ? Object.keys(definition.properties).length : 0,
          enumValues: Array.isArray(definition?.enum) ? definition.enum : null,
          properties: kind === 'schema' ? describeProperties(definition, rel) : [],
        });
        addEdge(fileId, nodeId, 'contains');

        for (const ref of collectRefs(definition)) {
          const resolved = resolveRef(ref, rel);
          if (resolved) addEdge(nodeId, resolved.id, 'ref');
        }

        // the permission vocabulary itself
        if (name === 'Permission' && Array.isArray(definition?.enum)) {
          for (const value of definition.enum) permissionEnum.add(value);
        }
      }
    }
  }

  // ---- taxonomy roll-up and audit -----------------------------------------
  const modules = new Map();
  const platformIndex = new Map();
  const codeLabels = new Map();
  const capabilityIndex = new Map();

  for (const node of nodes.values()) {
    if (node.type !== 'file') continue;
    const isShared = node.file.includes('/shared/');

    if (node.module) {
      if (!modules.has(node.module)) modules.set(node.module, []);
      modules.get(node.module).push(node.file);
    } else if (!isShared) {
      problems.push({
        severity: 'warning',
        kind: 'missing-taxonomy',
        file: node.file,
        nodeId: node.id,
        message: `${node.name} declares no x-ticvai-module`,
      });
    }

    if (!node.tier && !isShared) {
      problems.push({
        severity: 'warning',
        kind: 'missing-taxonomy',
        file: node.file,
        nodeId: node.id,
        message: `${node.name} declares no x-ticvai-tier`,
      });
    } else if (node.tier && node.tier !== node.group) {
      problems.push({
        severity: 'info',
        kind: 'tier-mismatch',
        file: node.file,
        nodeId: node.id,
        message: `${node.name} declares tier "${node.tier}" but sits in the ${node.group}/ folder`,
      });
    }

    if (!node.platforms?.length && !isShared) {
      problems.push({
        severity: 'warning',
        kind: 'missing-taxonomy',
        file: node.file,
        nodeId: node.id,
        message: `${node.name} declares no x-ticvai-platforms`,
      });
    }

    for (const platform of node.platforms ?? []) {
      if (!platformIndex.has(platform.raw)) {
        platformIndex.set(platform.raw, { ...platform, files: [] });
      }
      platformIndex.get(platform.raw).files.push(node.file);
      if (platform.code) {
        if (!codeLabels.has(platform.code)) codeLabels.set(platform.code, new Set());
        codeLabels.get(platform.code).add(platform.label);
      }
    }

    for (const capability of node.capabilities ?? []) {
      if (!capabilityIndex.has(capability)) capabilityIndex.set(capability, []);
      capabilityIndex.get(capability).push(node.file);
    }
  }

  // one code, two spellings — the enum problem all over again, in the taxonomy
  for (const [code, labels] of codeLabels) {
    if (labels.size > 1) {
      problems.push({
        severity: 'error',
        kind: 'platform-code-collision',
        file: 'contracts',
        message:
          `Platform code ${code} is used with ${labels.size} different names ` +
          `(${[...labels].map((l) => `"${l}"`).join(' and ')}). One code must mean one platform.`,
      });
    }
  }

  // ---- pass 2: permission nodes -------------------------------------------
  const allPermissions = new Set([...permissionEnum, ...usedPermissions.keys()]);
  for (const permission of allPermissions) {
    const users = usedPermissions.get(permission) ?? [];
    addNode({
      id: `perm:${permission}`,
      type: 'permission',
      name: permission,
      title: permission,
      group: 'permission',
      domain: permission.split('_')[0],
      declared: permissionEnum.has(permission),
      useCount: users.length,
      file: 'contracts/shared/permissions.yaml',
    });
    for (const opId of users) addEdge(opId, `perm:${permission}`, 'permission');

    if (!permissionEnum.has(permission)) {
      problems.push({
        severity: 'error',
        kind: 'undeclared-permission',
        file: nodes.get(users[0])?.file ?? '',
        nodeId: users[0],
        message: `${permission} is used by ${users.length} operation(s) but is not in the Permission enum`,
      });
    } else if (users.length === 0) {
      problems.push({
        severity: 'info',
        kind: 'unused-permission',
        file: 'contracts/shared/permissions.yaml',
        nodeId: `perm:${permission}`,
        message: `${permission} is declared but no operation uses it`,
      });
    }
  }

  // ---- pass 3: validate edges, compute backlinks ---------------------------
  const validEdges = [];
  for (const edge of edges) {
    if (!nodes.has(edge.target)) {
      const from = nodes.get(edge.source);
      problems.push({
        severity: 'error',
        kind: 'broken-ref',
        file: from?.file ?? '',
        line: from?.line,
        nodeId: edge.source,
        message: `${from?.name ?? edge.source} references ${edge.target.split('#').pop()} which does not exist`,
      });
      continue;
    }
    validEdges.push(edge);
  }

  // de-duplicate: many operations $ref the same schema repeatedly
  const seen = new Map();
  for (const edge of validEdges) {
    const key = `${edge.source}|${edge.target}|${edge.kind}`;
    if (seen.has(key)) seen.get(key).weight += 1;
    else seen.set(key, { ...edge, weight: 1 });
  }
  const uniqueEdges = [...seen.values()];

  const outgoing = new Map();
  const incoming = new Map();
  for (const edge of uniqueEdges) {
    if (edge.kind === 'contains') continue; // structural, not a link
    if (!outgoing.has(edge.source)) outgoing.set(edge.source, []);
    if (!incoming.has(edge.target)) incoming.set(edge.target, []);
    outgoing.get(edge.source).push(edge);
    incoming.get(edge.target).push(edge);
  }

  for (const node of nodes.values()) {
    node.outCount = (outgoing.get(node.id) ?? []).length;
    node.inCount = (incoming.get(node.id) ?? []).length;
  }

  // orphan components — defined but nothing links to them
  for (const node of nodes.values()) {
    const isComponent = ['schema', 'param', 'response', 'requestBody'].includes(node.type);
    if (isComponent && node.inCount === 0) {
      problems.push({
        severity: 'info',
        kind: 'orphan-component',
        file: node.file,
        line: node.line,
        nodeId: node.id,
        message: `${node.name} is defined but nothing references it`,
      });
    }
  }

  // ---- file-level aggregate graph -----------------------------------------
  const fileEdgeMap = new Map();
  for (const edge of uniqueEdges) {
    if (edge.kind === 'contains') continue;
    const sourceFile = nodes.get(edge.source)?.file;
    const targetFile = nodes.get(edge.target)?.file;
    if (!sourceFile || !targetFile || sourceFile === targetFile) continue;
    const key = `${sourceFile}|${targetFile}`;
    if (fileEdgeMap.has(key)) fileEdgeMap.get(key).weight += edge.weight;
    else
      fileEdgeMap.set(key, {
        source: `file:${sourceFile}`,
        target: `file:${targetFile}`,
        kind: 'ref',
        weight: edge.weight,
      });
  }

  const nodeList = [...nodes.values()];
  const operationCount = nodeList.filter((n) => n.type === 'operation').length;

  return {
    generatedAt: new Date().toISOString(),
    root,
    contractsDir,
    consumerCoverage: {
      source: declared.source,
      platforms: platformRoster,
      apps: declared.apps,
      declaredRows: declared.map.size,
      matchedOperations: consumerMatches,
      totalOperations: operationCount,
    },
    taxonomy: {
      modules: [...modules.entries()]
        .map(([name, list]) => ({ name, files: list }))
        .sort((a, b) => moduleOrder(a.name) - moduleOrder(b.name) || a.name.localeCompare(b.name)),
      platforms: [...platformIndex.values()].sort(
        (a, b) => (a.code ?? 'zz').localeCompare(b.code ?? 'zz') || a.label.localeCompare(b.label)
      ),
      capabilities: [...capabilityIndex.entries()]
        .map(([name, list]) => ({ name, files: list }))
        .sort((a, b) => a.name.localeCompare(b.name)),
    },
    nodes: nodeList,
    edges: uniqueEdges,
    fileEdges: [...fileEdgeMap.values()],
    problems,
    stats: {
      files: nodeList.filter((n) => n.type === 'file').length,
      operations: operationCount,
      schemas: nodeList.filter((n) => n.type === 'schema').length,
      permissions: nodeList.filter((n) => n.type === 'permission').length,
      links: uniqueEdges.filter((e) => e.kind !== 'contains').length,
      errors: problems.filter((p) => p.severity === 'error').length,
      warnings: problems.filter((p) => p.severity === 'warning').length,
    },
  };
}
