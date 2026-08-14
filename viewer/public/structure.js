// Block diagram of a YAML document's actual structure.
//
// Every mapping and sequence renders as a container block with its children
// nested inside it, so the shape of the document is carried by the boxes rather
// than by indentation alone. Scalars are single rows. Folding a block collapses
// it to its header with a count of what is hidden.

const KIND_COLORS = {
  map: '#60a5fa',
  seq: '#fbbf24',
  scalar: '#34d399',
  ref: '#a78bfa',
  alias: '#f472b6',
};

const KIND_COLORS_LIGHT = {
  map: '#2563eb',
  seq: '#b45309',
  scalar: '#059669',
  ref: '#7c3aed',
  alias: '#db2777',
};

const ROW_H = 21;      // a scalar / folded block
const HEADER_H = 23;   // the title bar of an open container
const INDENT = 14;     // how far children sit inside their parent
const PAD = 6;
const GAP = 2;
const ROOT_W = 540;
const MIN_W = 250;

// left-to-right tree mode: each level is a column, siblings stack vertically
const NODE_W = 210;
const NODE_H = 30;      // a block with no rows
const BLOCK_HEAD = 28;  // title bar of a block that carries rows
const FIELD_H = 15;     // a scalar shown as a row inside its parent
const V_GAP = 8;
const LEVEL_W = 250;

export function kindColor(kind) {
  const light = document.documentElement.dataset.theme === 'light';
  return (light ? KIND_COLORS_LIGHT : KIND_COLORS)[kind] ?? '#8b8b93';
}

export class StructureTree {
  constructor(canvas, { onSelect, onRef } = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.onSelect = onSelect ?? (() => {});
    this.onRef = onRef ?? (() => {});

    this.root = null;
    this.visible = [];
    this.collapsed = new Set();
    this.selectedPath = null;
    this.hover = null;
    this.filter = '';
    this.showLinks = true;
    this.showFields = true; // scalar leaves listed inside their parent block
    this.links = [];
    this.layoutMode = 'tree'; // 'tree' = left-to-right blocks, 'nested' = containment

    this.width = 900;
    this.height = 600;
    this.transform = { x: 40, y: 30, k: 1 };

    this._pan = null;
    this._bindEvents();
    this._resize();
    this._ro = new ResizeObserver(() => this._resize());
    this._ro.observe(canvas);
  }

  // ── data ────────────────────────────────────────────────────────
  setData(root, { expandDepth = 2 } = {}) {
    this.root = root;
    this.collapsed = new Set();
    const fold = (node, depth) => {
      if (node.children.length && depth >= expandDepth) this.collapsed.add(node.path);
      for (const child of node.children) fold(child, depth + 1);
    };
    fold(root, 0);
    this.layout();
    this.fit();
  }

  /**
   * Open every ancestor of `path`, and the target's own subtree when it is
   * small enough to be worth showing — otherwise selecting an operation lands
   * on a block whose contents (and so whose $ref arcs) are all still folded.
   */
  revealPath(path, { expandSubtree = 260 } = {}) {
    if (!this.root) return;
    const parts = String(path).split('/');
    let current = '';
    for (let i = 0; i < parts.length; i++) {
      current = i === 0 ? parts[0] : `${current}/${parts[i]}`;
      this.collapsed.delete(current);
    }
    this.collapsed.delete('');

    const target = this._findNode(path);
    if (target && target.descendants <= expandSubtree) {
      const unfold = (node) => {
        this.collapsed.delete(node.path);
        for (const child of node.children) unfold(child);
      };
      unfold(target);
    }
    this.layout();
  }

  _findNode(path) {
    const search = (node) => {
      if (node.path === path) return node;
      for (const child of node.children) {
        const found = search(child);
        if (found) return found;
      }
      return null;
    };
    return this.root ? search(this.root) : null;
  }

  /**
   * Unfolding a whole contract produces tens of thousands of pixels of height;
   * fitting that vertically would shrink it to an illegible sliver, so hold a
   * readable zoom and stay with whatever is selected.
   */
  expandAll() {
    this.collapsed.clear();
    this.layout();
    const k = Math.min(1, Math.max(this.transform.k, 0.6));
    this.transform.k = k;
    if (this.selectedPath && this.byPath.has(this.selectedPath)) {
      this.focusPath(this.selectedPath, { zoom: k });
    } else {
      this.transform.x = 40;
      this.transform.y = 24;
      this.draw();
    }
  }

  collapseAll() {
    this.collapsed = new Set();
    const fold = (node, depth) => {
      if (node.children.length && depth >= 1) this.collapsed.add(node.path);
      for (const child of node.children) fold(child, depth + 1);
    };
    if (this.root) fold(this.root, 0);
    this.layout();
    this.fit();
  }

  isCollapsed(node) {
    return this.collapsed.has(node.path) && node.children.length > 0;
  }

  _matches(node) {
    if (!this.filter) return true;
    const needle = this.filter;
    if ((node.key ?? '').toLowerCase().includes(needle)) return true;
    if ((node.value ?? '').toString().toLowerCase().includes(needle)) return true;
    return node.children.some((child) => this._matches(child));
  }

  // ── layout ──────────────────────────────────────────────────────
  layout() {
    this.visible = [];
    if (!this.root) return;
    if (this.layoutMode === 'tree') return this._layoutTree();
    return this._layoutNested();
  }

  /**
   * Left-to-right tree: depth picks the column, siblings stack down it, and a
   * parent centres against the span of its children (Reingold-Tilford, rotated).
   * Reading across is the natural direction for nested keys, and the aspect
   * ratio stays usable — a top-down version of the same data is 12,000px wide
   * and only 800 tall, which fits to an unreadable sliver.
   */
  _layoutTree() {
    let cursor = 0;

    const walk = (node, depth) => {
      const collapsed = this.isCollapsed(node);
      const kids = collapsed ? [] : node.children.filter((child) => this._matches(child));

      // Leaf scalars (and $refs) become rows inside this block rather than
      // blocks of their own — an operation is one card with its fields listed,
      // not eleven separate boxes.
      const rows = this.showFields ? kids.filter((child) => !child.children.length) : [];
      const branches = kids.filter((child) => child.children.length);
      const hiddenRows = this.showFields ? 0 : kids.filter((c) => !c.children.length).length;

      const entry = {
        node,
        depth,
        collapsed,
        rows,
        hiddenRows,
        width: NODE_W,
        height: rows.length ? BLOCK_HEAD + rows.length * FIELD_H + 5 : NODE_H,
        x: depth * LEVEL_W,
        children: [],
      };

      if (!branches.length) {
        entry.y = cursor;
        cursor += entry.height + V_GAP;
      } else {
        for (const child of branches) entry.children.push(walk(child, depth + 1));
        const first = entry.children[0];
        const last = entry.children[entry.children.length - 1];
        entry.y = (first.y + last.y + last.height - entry.height) / 2;
        // a tall parent can overlap the block above it, so never sit above the cursor
        cursor = Math.max(cursor, last.y + last.height + V_GAP);
      }

      this.visible.push(entry);
      return entry;
    };

    this.rootEntry = walk(this.root, 0);
    this.byPath = new Map(this.visible.map((e) => [e.node.path, e]));

    let maxX = 0;
    let maxY = 0;
    for (const entry of this.visible) {
      maxX = Math.max(maxX, entry.x + entry.width);
      maxY = Math.max(maxY, entry.y + entry.height);
    }
    this.totalWidth = maxX;
    this.totalHeight = maxY;
    this._buildLinks();
    this.draw();
  }

  // Measure heights bottom-up, then place blocks top-down.
  _layoutNested() {
    const measure = (node, depth, width) => {
      const collapsed = this.isCollapsed(node);
      const children = collapsed
        ? []
        : node.children.filter((child) => this._matches(child));

      const entry = {
        node,
        depth,
        width,
        collapsed,
        isContainer: children.length > 0,
        children: [],
      };

      if (!children.length) {
        entry.height = ROW_H;
        return entry;
      }

      const childWidth = Math.max(MIN_W, width - INDENT - PAD);
      let inner = 0;
      for (const child of children) {
        const childEntry = measure(child, depth + 1, childWidth);
        entry.children.push(childEntry);
        inner += childEntry.height + GAP;
      }
      entry.height = HEADER_H + PAD + Math.max(0, inner - GAP) + PAD;
      return entry;
    };

    const place = (entry, x, y) => {
      entry.x = x;
      entry.y = y;
      this.visible.push(entry);
      let childY = y + HEADER_H + PAD;
      for (const child of entry.children) {
        place(child, x + INDENT, childY);
        childY += child.height + GAP;
      }
    };

    this.rootEntry = measure(this.root, 0, ROOT_W);
    place(this.rootEntry, 0, 0);
    this.byPath = new Map(this.visible.map((e) => [e.node.path, e]));
    this.totalHeight = this.rootEntry.height;
    this._buildLinks();
    this.draw();
  }

  /**
   * Same-document `$ref`s become arcs between blocks. `#/components/schemas/X`
   * maps onto the structure path `components/schemas/X`, so a ref only links up
   * when its target block is currently laid out (not folded away).
   */
  _buildLinks() {
    this.links = [];
    let lane = 0;
    // a $ref may be a block of its own (nested mode) or a row inside one (tree)
    const sources = [];
    for (const entry of this.visible) {
      if (entry.node.kind === 'ref') sources.push({ entry, node: entry.node, rowIndex: -1 });
      (entry.rows ?? []).forEach((row, index) => {
        if (row.kind === 'ref') sources.push({ entry, node: row, rowIndex: index });
      });
    }

    for (const source of sources) {
      const { node, entry, rowIndex } = source;
      if (typeof node.value !== 'string') continue;
      if (!node.value.startsWith('#/')) continue; // cross-file refs have no block here

      // If the exact target is folded away, aim at the nearest visible ancestor
      // so the arc still points somewhere true instead of vanishing.
      const parts = node.value.slice(2).split('/');
      let target = null;
      let exact = true;
      for (let take = parts.length; take > 0 && !target; take--) {
        target = this.byPath.get(parts.slice(0, take).join('/')) ?? null;
        if (target && take < parts.length) exact = false;
      }
      if (!target || target === entry) continue;

      this.links.push({
        from: entry,
        fromNode: node,
        rowIndex,
        to: target,
        exact,
        lane: lane % 4,
        label: parts[parts.length - 1],
      });
      lane += 1;
    }
  }

  /** Where a link leaves its source: a row's height, or the block's middle. */
  _linkOrigin(link) {
    const entry = link.from;
    const y = link.rowIndex >= 0
      ? entry.y + BLOCK_HEAD + (link.rowIndex + 0.5) * FIELD_H
      : entry.y + entry.height / 2;
    return { x: entry.x + entry.width, y };
  }

  /**
   * `min` floors the zoom. A fully expanded contract is over 12,000px wide, and
   * fitting that literally leaves 4px-tall blocks that cannot be read or
   * clicked — so the default keeps blocks usable and only the explicit Fit
   * button asks for the true whole-tree view.
   */
  fit({ min = 0.3 } = {}) {
    if (!this.rootEntry || !this.width) return;

    if (this.layoutMode === 'tree') {
      // Fit the depth (width) and scroll through the leaves vertically — the
      // tree is a few columns across but can be tens of thousands of px tall.
      const ideal = Math.min(1, (this.width - 60) / Math.max(1, this.totalWidth));
      const k = Math.max(min, ideal);
      this.transform.k = k;
      this.transform.x = 30;
      if (this.selectedPath && this.byPath.has(this.selectedPath)) {
        this.focusPath(this.selectedPath);
      } else {
        // A parent centres against its whole subtree, so the root sits halfway
        // down a very tall span — land on it rather than in empty space.
        this.transform.y = this.height / 2 - (this.rootEntry.y + NODE_H / 2) * k;
      }
      this.draw();
      return;
    }

    const k = Math.min(1, (this.height - 60) / Math.max(1, this.totalHeight), this.width / (ROOT_W + 80));
    this.transform.k = Math.max(0.08, Math.min(1, k));
    this.transform.x = 40;
    this.transform.y = 24;
    this.draw();
  }

  focusPath(path, { zoom } = {}) {
    const entry = this.byPath?.get(path);
    if (!entry) return false;
    if (zoom) this.transform.k = zoom;
    const { k } = this.transform;

    if (this.layoutMode === 'tree') {
      // keep the ancestor columns to the left in view rather than centring
      this.transform.x = Math.min(30, this.width * 0.34 - entry.x * k);
      this.transform.y = this.height / 2 - (entry.y + entry.height / 2) * k;
      this.draw();
      return true;
    }

    this.transform.x = Math.min(60, this.width / 2 - entry.x * k - (entry.width * k) / 2);
    this.transform.y = this.height / 2 - entry.y * k - Math.min(entry.height, 200) * k / 2;
    this.draw();
    return true;
  }

  // ── view helpers ────────────────────────────────────────────────
  _resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    this.width = rect.width;
    this.height = rect.height;
    this.canvas.width = Math.round(rect.width * dpr);
    this.canvas.height = Math.round(rect.height * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.draw();
  }

  resize() { this._resize(); }

  toScreen(x, y) {
    return { x: x * this.transform.k + this.transform.x, y: y * this.transform.k + this.transform.y };
  }

  entryAt(sx, sy) {
    const { k } = this.transform;
    const x = (sx - this.transform.x) / k;
    const y = (sy - this.transform.y) / k;

    if (this.layoutMode === 'tree') {
      for (const entry of this.visible) {
        if (
          x >= entry.x && x <= entry.x + entry.width &&
          y >= entry.y && y <= entry.y + entry.height
        ) return entry;
      }
      return null;
    }

    // deepest block whose header band contains the point wins, so clicking a
    // child never toggles the parent wrapped around it
    let best = null;
    for (const entry of this.visible) {
      if (x < entry.x || x > entry.x + entry.width) continue;
      const bandHeight = entry.children.length ? HEADER_H : entry.height;
      if (y < entry.y || y > entry.y + bandHeight) continue;
      if (!best || entry.depth > best.depth) best = entry;
    }
    return best;
  }

  // ── drawing ─────────────────────────────────────────────────────
  draw() {
    const ctx = this.ctx;
    const styles = getComputedStyle(document.documentElement);
    const text = styles.getPropertyValue('--text').trim() || '#dcdde3';
    const dim = styles.getPropertyValue('--text-dim').trim() || '#9a9aa6';
    const faint = styles.getPropertyValue('--text-faint').trim() || '#6b6b78';
    const accent = styles.getPropertyValue('--accent').trim() || '#a78bfa';
    const light = document.documentElement.dataset.theme === 'light';

    ctx.clearRect(0, 0, this.width, this.height);
    if (!this.visible.length) {
      ctx.fillStyle = dim;
      ctx.font = '13px ui-sans-serif, system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Select a contract to diagram its structure', this.width / 2, this.height / 2);
      return;
    }

    const { k } = this.transform;
    ctx.textBaseline = 'middle';

    if (this.layoutMode === 'tree') {
      return this._drawTree({ ctx, k, text, dim, faint, accent, light });
    }

    // ── parent → child guides ──
    // The gutter line plus a stub into each child makes the parent/child
    // relationship explicit rather than leaving it to indentation alone.
    ctx.strokeStyle = light ? 'rgba(0,0,0,.16)' : 'rgba(255,255,255,.14)';
    ctx.lineWidth = Math.max(0.6, 1 * k);
    for (const entry of this.visible) {
      if (!entry.children.length) continue;
      const gutterX = this.toScreen(entry.x + INDENT / 2, 0).x;
      const last = entry.children[entry.children.length - 1];
      const top = this.toScreen(0, entry.y + HEADER_H).y;
      const bottom = this.toScreen(0, last.y + Math.min(last.height, ROW_H) / 2).y;
      if (bottom < -20 || top > this.height + 20) continue;

      ctx.beginPath();
      ctx.moveTo(gutterX, top);
      ctx.lineTo(gutterX, bottom);
      ctx.stroke();

      for (const child of entry.children) {
        const y = this.toScreen(0, child.y + Math.min(child.height, ROW_H) / 2).y;
        if (y < -20 || y > this.height + 20) continue;
        ctx.beginPath();
        ctx.moveTo(gutterX, y);
        ctx.lineTo(this.toScreen(child.x, 0).x, y);
        ctx.stroke();
      }
    }

    // ── $ref arcs, routed in lanes to the right of the blocks ──
    if (this.showLinks && this.links.length) {
      const anchorPath = this.hover?.node.path ?? this.selectedPath;
      for (const link of this.links) {
        const fromY = this.toScreen(0, link.from.y + ROW_H / 2).y;
        const toY = this.toScreen(0, link.to.y + HEADER_H / 2).y;
        if (Math.max(fromY, toY) < -40 || Math.min(fromY, toY) > this.height + 40) continue;

        const startX = this.toScreen(link.from.x + link.from.width, 0).x;
        const endX = this.toScreen(link.to.x + link.to.width, 0).x;
        const laneX = this.toScreen(ROOT_W + 26 + link.lane * 22, 0).x;

        // A ref sits several levels under the block it belongs to, so match the
        // whole subtree — selecting `Order` should light up everything Order refs.
        const touches = (path) =>
          path === anchorPath || path.startsWith(`${anchorPath}/`);
        const active =
          Boolean(anchorPath) && (touches(link.from.node.path) || touches(link.to.node.path));
        ctx.strokeStyle = active
          ? (light ? 'rgba(124,58,237,.85)' : 'rgba(167,139,250,.85)')
          : (light ? 'rgba(0,0,0,.14)' : 'rgba(255,255,255,.12)');
        ctx.lineWidth = (active ? 1.8 : 1) * Math.max(0.5, Math.min(1.5, k));
        // dashed when it lands on a container rather than the target itself
        ctx.setLineDash(link.exact ? [] : [4 * k, 3 * k]);

        ctx.beginPath();
        ctx.moveTo(startX, fromY);
        ctx.bezierCurveTo(laneX, fromY, laneX, toY, endX, toY);
        ctx.stroke();
        ctx.setLineDash([]);

        if (active && k > 0.4) {
          const size = 5 * Math.min(1.4, k);
          ctx.beginPath();
          ctx.moveTo(endX, toY);
          ctx.lineTo(endX + size, toY - size * 0.7);
          ctx.lineTo(endX + size, toY + size * 0.7);
          ctx.closePath();
          ctx.fillStyle = ctx.strokeStyle;
          ctx.fill();
        }
      }
    }

    for (const entry of this.visible) {
      const p = this.toScreen(entry.x, entry.y);
      const w = entry.width * k;
      const h = entry.height * k;
      if (p.y + h < -20 || p.y > this.height + 20) continue;
      if (p.x > this.width + 20 || p.x + w < -20) continue;

      const node = entry.node;
      const color = kindColor(node.kind);
      const selected = node.path === this.selectedPath;
      const hovered = entry === this.hover;
      const isHit =
        this.filter &&
        ((node.key ?? '').toLowerCase().includes(this.filter) ||
          (node.value ?? '').toString().toLowerCase().includes(this.filter));

      // block body — nested levels get progressively lighter so containment reads
      if (entry.children.length || entry.collapsed) {
        const shade = light
          ? `rgba(0,0,0,${0.02 + Math.min(entry.depth, 6) * 0.012})`
          : `rgba(255,255,255,${0.022 + Math.min(entry.depth, 6) * 0.011})`;
        ctx.beginPath();
        ctx.roundRect(p.x, p.y, w, h, 5 * Math.min(1.4, k));
        ctx.fillStyle = shade;
        ctx.fill();
        ctx.lineWidth = selected ? 1.6 : 1;
        ctx.strokeStyle = selected
          ? accent
          : light ? 'rgba(0,0,0,.10)' : 'rgba(255,255,255,.08)';
        ctx.stroke();

        // colour spine on the left edge
        ctx.fillStyle = color;
        ctx.globalAlpha = selected || hovered ? 1 : 0.65;
        ctx.fillRect(p.x, p.y, Math.max(1.5, 2.5 * k), h);
        ctx.globalAlpha = 1;
      } else if (selected || hovered || isHit) {
        ctx.beginPath();
        ctx.roundRect(p.x, p.y, w, h, 4 * Math.min(1.4, k));
        ctx.fillStyle = selected ? accent + '26' : light ? 'rgba(0,0,0,.04)' : 'rgba(255,255,255,.05)';
        ctx.fill();
      }

      if (k < 0.3) continue; // text would be illegible

      const fontSize = Math.min(12.5, Math.max(6.5, 11.5 * k));
      const bandCentre = p.y + ((entry.children.length ? HEADER_H : ROW_H) / 2) * k;
      let cursor = p.x + 8 * k;

      // fold marker
      if (node.children.length) {
        ctx.beginPath();
        const r = 3.2 * Math.min(1.4, k);
        if (entry.collapsed) {
          ctx.arc(cursor + r, bandCentre, r, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();
        } else {
          ctx.arc(cursor + r, bandCentre, r, 0, Math.PI * 2);
          ctx.strokeStyle = color;
          ctx.lineWidth = Math.max(1, 1.3 * k);
          ctx.stroke();
        }
        cursor += r * 2 + 6 * k;
      }

      // key
      const label =
        node.key != null && node.key !== ''
          ? node.key
          : node.index != null
            ? `[${node.index}]`
            : node.kind === 'ref' ? '$ref' : 'document';

      ctx.textAlign = 'left';
      ctx.font = `${entry.children.length || selected || isHit ? '600 ' : ''}${fontSize}px ui-sans-serif, system-ui, sans-serif`;
      ctx.fillStyle = isHit ? accent : selected ? accent : entry.children.length ? text : dim;
      const keyText = fit(ctx, label, w * 0.5);
      ctx.fillText(keyText, cursor, bandCentre);
      cursor += ctx.measureText(keyText).width + 8 * k;

      // value / summary
      let detail = '';
      if (node.kind === 'scalar') detail = node.value;
      else if (node.kind === 'ref') detail = node.value;
      else if (node.kind === 'alias') detail = node.value;
      else if (entry.collapsed) detail = `${node.summary ?? ''}  +${node.descendants}`;
      else if (node.kind === 'seq') detail = `${node.children.length} items`;

      if (detail) {
        ctx.font = `${fontSize}px ui-monospace, "Cascadia Code", Menlo, monospace`;
        ctx.fillStyle = node.kind === 'ref' ? color : faint;
        ctx.fillText(fit(ctx, detail, p.x + w - cursor - 8 * k), cursor, bandCentre);
      }
    }
  }

  /** Top-down tree: links from a parent's underside to each child's top. */
  _drawTree({ ctx, k, text, dim, faint, accent, light }) {
    const panel = getComputedStyle(document.documentElement).getPropertyValue('--bg-panel').trim() || '#1a1a21';
    const border = getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#2c2c36';

    // ── parent → child links, left edge to right edge ──
    ctx.strokeStyle = light ? 'rgba(0,0,0,.28)' : 'rgba(255,255,255,.24)';
    ctx.lineWidth = Math.max(0.5, 1.1 * k);
    for (const entry of this.visible) {
      if (!entry.children.length) continue;
      const from = this.toScreen(entry.x + entry.width, entry.y + entry.height / 2);
      for (const child of entry.children) {
        const to = this.toScreen(child.x, child.y + child.height / 2);
        if (Math.max(from.y, to.y) < -60 || Math.min(from.y, to.y) > this.height + 60) continue;
        if (Math.max(from.x, to.x) < -60 || Math.min(from.x, to.x) > this.width + 60) continue;
        const midX = (from.x + to.x) / 2;
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.bezierCurveTo(midX, from.y, midX, to.y, to.x, to.y);
        ctx.stroke();
      }
    }

    // ── $ref links, drawn directly between the two blocks ──
    if (this.showLinks && this.links.length) {
      const anchorPath = this.hover?.node.path ?? this.selectedPath;
      const touches = (path) => anchorPath && (path === anchorPath || path.startsWith(`${anchorPath}/`));
      for (const link of this.links) {
        // both ends leave from the right so the curve bows clear of the columns
        const origin = this._linkOrigin(link);
        const from = this.toScreen(origin.x, origin.y);
        const to = this.toScreen(link.to.x + link.to.width, link.to.y + link.to.height / 2);
        if (Math.max(from.x, to.x) < -80 || Math.min(from.x, to.x) > this.width + 80) continue;
        if (Math.max(from.y, to.y) < -80 || Math.min(from.y, to.y) > this.height + 80) continue;

        const active = Boolean(anchorPath) && (touches(link.fromNode.path) || touches(link.to.node.path));
        ctx.strokeStyle = active
          ? (light ? 'rgba(124,58,237,.85)' : 'rgba(167,139,250,.85)')
          : (light ? 'rgba(124,58,237,.2)' : 'rgba(167,139,250,.18)');
        ctx.lineWidth = (active ? 1.8 : 1) * Math.max(0.5, Math.min(1.5, k));
        ctx.setLineDash(link.exact ? [] : [4 * k, 3 * k]);
        const bow = Math.min(180, Math.abs(to.y - from.y) * 0.25 + 50) * Math.min(1.4, k);
        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.bezierCurveTo(from.x + bow, from.y, to.x + bow, to.y, to.x, to.y);
        ctx.stroke();
        ctx.setLineDash([]);

        if (active && k > 0.4) {
          const size = 5 * Math.min(1.4, k);
          ctx.beginPath();
          ctx.moveTo(to.x, to.y);
          ctx.lineTo(to.x + size, to.y - size * 0.7);
          ctx.lineTo(to.x + size, to.y + size * 0.7);
          ctx.closePath();
          ctx.fillStyle = ctx.strokeStyle;
          ctx.fill();
        }
      }
    }

    if (k < 0.12) return; // blocks would be sub-pixel

    // ── blocks ──
    for (const entry of this.visible) {
      const p = this.toScreen(entry.x, entry.y);
      const w = entry.width * k;
      const h = entry.height * k;
      if (p.x + w < -40 || p.x > this.width + 40 || p.y + h < -40 || p.y > this.height + 40) continue;

      const node = entry.node;
      const color = kindColor(node.kind);
      const selected = node.path === this.selectedPath;
      const hovered = entry === this.hover;
      const isHit =
        this.filter &&
        ((node.key ?? '').toLowerCase().includes(this.filter) ||
          (node.value ?? '').toString().toLowerCase().includes(this.filter));

      ctx.beginPath();
      ctx.roundRect(p.x, p.y, w, h, 5 * Math.min(1.4, k));
      ctx.fillStyle = panel;
      ctx.fill();
      ctx.lineWidth = selected || hovered ? 2 : 1;
      ctx.strokeStyle = selected ? accent : isHit ? accent : hovered ? text : border;
      ctx.stroke();

      // colour band across the top identifies the YAML kind
      ctx.save();
      ctx.beginPath();
      ctx.roundRect(p.x, p.y, w, h, 5 * Math.min(1.4, k));
      ctx.clip();
      ctx.fillStyle = color;
      ctx.fillRect(p.x, p.y, w, Math.max(2, 3 * k));
      if (entry.collapsed) {
        ctx.globalAlpha = light ? 0.1 : 0.14;
        ctx.fillRect(p.x, p.y, w, h);
        ctx.globalAlpha = 1;
      }
      ctx.restore();

      if (k < 0.3) continue;

      const label =
        node.key != null && node.key !== ''
          ? node.key
          : node.index != null
            ? `[${node.index}]`
            : node.kind === 'ref' ? '$ref' : 'document';

      ctx.textAlign = 'left';
      let textLeft = p.x + 7 * k;
      const rowList = entry.rows ?? [];
      // a block carrying rows has a fixed-height title bar; a bare one centres
      const titleY = rowList.length ? p.y + (BLOCK_HEAD / 2) * k : p.y + h * 0.36;

      // ▸ / ▾ so it is obvious which blocks open, and which way they are set
      if (node.children.length) {
        ctx.font = `${Math.min(11, Math.max(6, 10 * k))}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillStyle = color;
        ctx.fillText(entry.collapsed ? '▸' : '▾', textLeft, titleY);
        textLeft += 10 * k;
      }

      ctx.font = `600 ${Math.min(12, Math.max(6, 11 * k))}px ui-sans-serif, system-ui, sans-serif`;
      ctx.fillStyle = selected || isHit ? accent : text;
      ctx.fillText(fit(ctx, label, p.x + w * 0.55 - textLeft), textLeft, titleY);

      let detail = '';
      if (node.kind === 'scalar') detail = node.value;
      else if (node.kind === 'ref' || node.kind === 'alias') detail = node.value;
      else if (entry.collapsed) detail = `${node.children.length} keys · +${node.descendants}`;
      else detail = node.kind === 'seq' ? `${node.children.length} items` : `${node.children.length} keys`;

      if (detail) {
        ctx.font = `${Math.min(10.5, Math.max(5, 9.5 * k))}px ui-monospace, Menlo, monospace`;
        ctx.fillStyle = faint;
        const detailY = rowList.length ? p.y + (BLOCK_HEAD / 2) * k : p.y + h * 0.72;
        ctx.textAlign = 'right';
        ctx.fillText(fit(ctx, detail, w * 0.45), p.x + w - 7 * k, detailY);
        ctx.textAlign = 'left';
      }

      // ── scalar fields, listed inside the block ──
      if (!rowList.length || k < 0.4) continue;
      let rowY = p.y + (BLOCK_HEAD + FIELD_H / 2) * k;
      for (const row of rowList) {
        const isRef = row.kind === 'ref' || row.kind === 'alias';
        ctx.font = `${Math.min(10, Math.max(5, 9 * k))}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillStyle = isRef ? kindColor(row.kind) : dim;
        const key = row.key ?? (row.index != null ? `[${row.index}]` : '·');
        const keyText = fit(ctx, key, w * 0.5);
        ctx.fillText(keyText, p.x + 8 * k, rowY);

        const value = isRef ? String(row.value).split('/').pop() : row.value;
        if (value) {
          ctx.font = `${Math.min(10, Math.max(5, 9 * k))}px ui-monospace, Menlo, monospace`;
          ctx.fillStyle = isRef ? kindColor(row.kind) : faint;
          ctx.textAlign = 'right';
          ctx.fillText(fit(ctx, String(value), w * 0.44), p.x + w - 8 * k, rowY);
          ctx.textAlign = 'left';
        }
        rowY += FIELD_H * k;
      }
    }
  }

  // ── interaction ─────────────────────────────────────────────────
  _bindEvents() {
    const canvas = this.canvas;

    canvas.addEventListener('mousedown', (e) => {
      this._pan = {
        x: e.offsetX, y: e.offsetY,
        tx: this.transform.x, ty: this.transform.y,
        moved: false,
      };
    });

    canvas.addEventListener('mousemove', (e) => {
      if (this._pan) {
        const dx = e.offsetX - this._pan.x;
        const dy = e.offsetY - this._pan.y;
        if (Math.abs(dx) > 3 || Math.abs(dy) > 3) this._pan.moved = true;
        this.transform.x = this._pan.tx + dx;
        this.transform.y = this._pan.ty + dy;
        this.draw();
        return;
      }
      const entry = this.entryAt(e.offsetX, e.offsetY);
      if (entry !== this.hover) {
        this.hover = entry;
        canvas.style.cursor = entry ? 'pointer' : 'grab';
        this.draw();
      }
    });

    window.addEventListener('mouseup', (e) => {
      if (!this._pan) return;
      const wasClick = !this._pan.moved;
      this._pan = null;
      if (!wasClick) return;

      const rect = canvas.getBoundingClientRect();
      const entry = this.entryAt(e.clientX - rect.left, e.clientY - rect.top);
      if (!entry) return;

      // a click on a $ref row follows it rather than folding the block
      if (this.layoutMode === 'tree' && entry.rows?.length) {
        const world = (e.clientY - rect.top - this.transform.y) / this.transform.k;
        const index = Math.floor((world - entry.y - BLOCK_HEAD) / FIELD_H);
        const row = index >= 0 && index < entry.rows.length ? entry.rows[index] : null;
        if (row) {
          this.selectedPath = row.path;
          if (row.kind === 'ref') this.onRef(row);
          this.onSelect(row);
          this.draw();
          return;
        }
      }

      const node = entry.node;
      this.selectedPath = node.path;

      if (node.kind === 'ref') {
        this.onRef(node);
      } else if (node.children.length) {
        if (this.collapsed.has(node.path)) this.collapsed.delete(node.path);
        else this.collapsed.add(node.path);
        this.layout();
      }
      this.onSelect(node);
      this.draw();
    });

    // Double-click folds a whole branch shut again. Single-click toggles one
    // level, which is fiddly to undo once a subtree has been opened up.
    canvas.addEventListener('dblclick', (e) => {
      const entry = this.entryAt(e.offsetX, e.offsetY);
      if (!entry) return;
      e.preventDefault();

      const node = entry.node;
      if (!node.children.length) return;

      const foldAll = (target) => {
        if (target.children.length) this.collapsed.add(target.path);
        for (const child of target.children) foldAll(child);
      };
      foldAll(node);

      this.selectedPath = node.path;
      this.layout();
      this.focusPath(node.path);
      this.onSelect(node);
    });

    canvas.addEventListener('mouseleave', () => {
      this.hover = null;
      this.draw();
    });

    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      const next = Math.max(0.1, Math.min(3, this.transform.k * factor));
      const wx = (e.offsetX - this.transform.x) / this.transform.k;
      const wy = (e.offsetY - this.transform.y) / this.transform.k;
      this.transform.k = next;
      this.transform.x = e.offsetX - wx * next;
      this.transform.y = e.offsetY - wy * next;
      this.draw();
    }, { passive: false });
  }

  destroy() {
    this._ro?.disconnect();
  }
}

function fit(ctx, text, maxWidth) {
  const value = String(text ?? '');
  if (maxWidth <= 0) return '';
  if (ctx.measureText(value).width <= maxWidth) return value;
  let out = value;
  while (out.length > 1 && ctx.measureText(out + '…').width > maxWidth) out = out.slice(0, -1);
  return out + '…';
}
