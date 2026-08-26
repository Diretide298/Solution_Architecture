// Turns a YAML document into a structural tree — every mapping key, sequence
// item and scalar becomes a node the frontend can draw as a diagram.
//
// Uses the `yaml` package rather than js-yaml because it exposes byte ranges on
// every node, which is what lets each diagram node point back at its source line.

import { parseDocument, isMap, isSeq, isScalar, isAlias } from 'yaml';

/** Byte offset -> 1-based line number. */
function makeLineLookup(text) {
  const starts = [0];
  for (let i = 0; i < text.length; i++) {
    if (text[i] === '\n') starts.push(i + 1);
  }
  return (offset) => {
    let low = 0;
    let high = starts.length - 1;
    while (low < high) {
      const mid = (low + high + 1) >> 1;
      if (starts[mid] <= offset) low = mid;
      else high = mid - 1;
    }
    return low + 1;
  };
}

const MAX_PREVIEW = 120;

function previewScalar(value) {
  if (value === null) return 'null';
  if (typeof value === 'string') {
    const flat = value.replace(/\s+/g, ' ').trim();
    return flat.length > MAX_PREVIEW ? flat.slice(0, MAX_PREVIEW - 1) + '…' : flat;
  }
  return String(value);
}

/** A compact one-line summary so collapsed nodes still say something useful. */
function summarise(node) {
  if (isMap(node)) {
    const keys = node.items.map((i) => String(i.key?.value ?? '')).filter(Boolean);
    const shown = keys.slice(0, 4).join(', ');
    return `{ ${shown}${keys.length > 4 ? `, +${keys.length - 4}` : ''} }`;
  }
  if (isSeq(node)) return `[ ${node.items.length} item${node.items.length === 1 ? '' : 's'} ]`;
  return '';
}

/**
 * Recursively convert a yaml AST node into a plain tree.
 * `key` is the mapping key this node sits under (null at the root / in sequences).
 */
function convert(node, key, lineOf, path, index = null) {
  if (node == null) {
    return { key, kind: 'scalar', value: 'null', path, line: 1, children: [] };
  }

  const line = node.range ? lineOf(node.range[0]) : 1;
  const endLine = node.range ? lineOf(node.range[2] ?? node.range[1]) : line;

  // an alias (`*anchor`) — treat as a leaf that names its target
  if (isAlias(node)) {
    return { key, kind: 'alias', value: `*${node.source}`, path, line, endLine, children: [] };
  }

  if (isScalar(node)) {
    return {
      key,
      kind: 'scalar',
      value: previewScalar(node.value),
      valueType: node.value === null ? 'null' : typeof node.value,
      path,
      line,
      endLine,
      index,
      children: [],
    };
  }

  if (isMap(node)) {
    // `$ref` is the one mapping worth collapsing into a single link node
    const refItem = node.items.find((i) => String(i.key?.value) === '$ref');
    if (refItem && node.items.length === 1) {
      return {
        key,
        kind: 'ref',
        value: String(refItem.value?.value ?? ''),
        path,
        line,
        endLine,
        index,
        children: [],
      };
    }

    return {
      key,
      kind: 'map',
      summary: summarise(node),
      path,
      line,
      endLine,
      index,
      children: node.items.map((item) => {
        const childKey = String(item.key?.value ?? '');
        return convert(item.value, childKey, lineOf, path ? `${path}/${childKey}` : childKey);
      }),
    };
  }

  if (isSeq(node)) {
    return {
      key,
      kind: 'seq',
      summary: summarise(node),
      path,
      line,
      endLine,
      index,
      children: node.items.map((item, i) => convert(item, null, lineOf, `${path}/${i}`, i)),
    };
  }

  return { key, kind: 'scalar', value: String(node), path, line, endLine, children: [] };
}

/** Count descendants so collapsed nodes can show how much they hide. */
function annotate(node) {
  let total = 0;
  let maxDepth = 0;
  for (const child of node.children) {
    const info = annotate(child);
    total += 1 + info.total;
    maxDepth = Math.max(maxDepth, 1 + info.maxDepth);
  }
  node.descendants = total;
  node.depth = maxDepth;
  return { total, maxDepth };
}

export function buildStructure(text) {
  const doc = parseDocument(text, { keepSourceTokens: false });
  const lineOf = makeLineLookup(text);

  const root = convert(doc.contents, null, lineOf, '');
  root.key = 'document';
  annotate(root);

  return {
    root,
    lineCount: text.split(/\r?\n/).length,
    errors: doc.errors.map((e) => ({
      message: e.message,
      line: e.pos ? lineOf(e.pos[0]) : 1,
    })),
    warnings: doc.warnings.map((w) => ({
      message: w.message,
      line: w.pos ? lineOf(w.pos[0]) : 1,
    })),
  };
}
