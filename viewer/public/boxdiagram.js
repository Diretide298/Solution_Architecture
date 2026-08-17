// Diagram of *boxes* rather than dots — used by the ER view (entities with
// their fields) and the Data view (tables with their columns). Boxes carry
// rows, so collision has to work on rectangles.
//
// Boxes are placed in a hierarchy, not thrown into a force simulation: a table
// sits below the tables it references, so the diagram opens as something you
// can read top to bottom. Anything can then be dragged anywhere, and stays
// where it is put — the physics is only used to settle a drag, never to decide
// the initial arrangement. Re-picking the scope restores the tidy layout.

import { enableTouch } from './touch.js';

const HEADER_H = 26;
const ROW_H = 17;
const BOX_W = 216;
const PAD_Y = 6;
const MAX_ROWS = 11;

// layout spacing
const GAP_X = 34;
const GAP_Y = 58;
const MAX_PER_ROW = 8; // a layer wider than this wraps rather than running off

/**
 * Text scales with the zoom, like everything else on the canvas. It used to be
 * capped, which meant zooming in grew the boxes while their labels stayed the
 * same size — the one thing you zoom in to read. The floor keeps a zoomed-out
 * label legible; the k thresholds in draw() stop drawing text well before it
 * would turn into noise.
 */
const textSize = (base, k, floor = 6) => Math.max(floor, base * k);

export class BoxDiagram {
  constructor(canvas, { onSelect, onRow } = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.onSelect = onSelect ?? (() => {});
    this.onRow = onRow ?? (() => {});

    this.nodes = [];
    this.edges = [];
    this.byId = new Map();
    this.selectedId = null;
    this.hover = null;
    this.hoverRow = null;
    this.showRows = true;
    // Boxes the user opened out to their full column list. Kept by id so the
    // choice survives a relayout, a rescope and a live reload of the data.
    this.expanded = new Set();

    this.width = 900;
    this.height = 600;
    this.transform = { x: 0, y: 0, k: 1 };
    this.alpha = 0;
    this.running = false;

    this._drag = null;
    this._pan = null;
    this._raf = null;

    this._bind();
    this._resize();
    this._ro = new ResizeObserver(() => this._resize());
    this._ro.observe(canvas);
  }

  // ── data ────────────────────────────────────────────────────────
  setData(nodes, edges) {
    const previous = new Map(this.nodes.map((n) => [n.id, n]));
    // An arrangement the user made by hand is theirs to keep — but only while
    // the same boxes are on screen. A different scope gets a fresh layout.
    const sameSet =
      previous.size === nodes.length && nodes.every((n) => previous.has(n.id));
    const keepPositions = this.userAdjusted && sameSet;

    this.nodes = nodes.map((source) => {
      const old = previous.get(source.id);
      const total = source.rows?.length ?? 0;
      const open = this.expanded.has(source.id);
      const shown = open ? total : Math.min(total, MAX_ROWS);
      const hidden = total - shown;
      return {
        ...source,
        shownRows: shown,
        hiddenRows: hidden,
        // the fold row is drawn whenever there is something to fold either way
        foldable: total > MAX_ROWS,
        w: BOX_W,
        h: HEADER_H + PAD_Y * 2 + shown * ROW_H + (total > MAX_ROWS ? ROW_H : 0),
        x: keepPositions ? old.x : 0,
        y: keepPositions ? old.y : 0,
        vx: 0,
        vy: 0,
        degree: 0,
      };
    });

    this.byId = new Map(this.nodes.map((n) => [n.id, n]));

    this.edges = [];
    for (const edge of edges) {
      const source = this.byId.get(edge.source);
      const target = this.byId.get(edge.target);
      if (!source || !target || source === target) continue;
      this.edges.push({ ...edge, source, target });
      source.degree += 1;
      target.degree += 1;
    }

    this.neighbours = new Map();
    for (const edge of this.edges) {
      if (!this.neighbours.has(edge.source.id)) this.neighbours.set(edge.source.id, new Set());
      if (!this.neighbours.has(edge.target.id)) this.neighbours.set(edge.target.id, new Set());
      this.neighbours.get(edge.source.id).add(edge.target.id);
      this.neighbours.get(edge.target.id).add(edge.source.id);
    }

    if (!keepPositions) {
      this.userAdjusted = false;
      this.relayout();
    }
    // no simulation on open — the layout is already the answer
    this.alpha = 0;
    this._run();
  }

  /**
   * Places the boxes in layers: a box sits below everything it points at, so
   * the most-referenced things — the tables the rest of the schema hangs off —
   * end up along the top. Deterministic, so the same data always draws the
   * same picture.
   */
  relayout() {
    const nodes = this.nodes;
    if (!nodes.length) return;

    const outgoing = new Map(nodes.map((n) => [n.id, new Set()]));
    for (const edge of this.edges) {
      if (edge.source !== edge.target) outgoing.get(edge.source.id).add(edge.target.id);
    }

    // depth = longest chain of references leaving this box. A box that
    // references nothing is depth 0 and sits at the top; a cycle stops at the
    // box that closes it rather than looping forever.
    const depth = new Map();
    const visiting = new Set();
    const measure = (id) => {
      if (depth.has(id)) return depth.get(id);
      if (visiting.has(id)) return 0;
      visiting.add(id);
      let d = 0;
      for (const next of outgoing.get(id) ?? []) d = Math.max(d, measure(next) + 1);
      visiting.delete(id);
      depth.set(id, d);
      return d;
    };

    // boxes with no relationships at all are not part of the hierarchy; they
    // go in a block underneath rather than padding out the top row
    const linked = nodes.filter((n) => n.degree > 0);
    const loose = nodes.filter((n) => n.degree === 0);
    for (const node of linked) measure(node.id);

    const layers = [];
    for (const node of linked) {
      const d = depth.get(node.id) ?? 0;
      (layers[d] ??= []).push(node);
    }

    // order each layer so its edges cross as little as possible: start from the
    // busiest boxes, then sweep down putting each box near the average position
    // of the ones above it that point at it
    const index = new Map();
    const reindex = (layer) => layer.forEach((n, i) => index.set(n.id, i));
    if (layers[0]) {
      layers[0].sort((a, b) => b.degree - a.degree || String(a.label ?? a.id).localeCompare(String(b.label ?? b.id)));
      reindex(layers[0]);
    }
    for (let pass = 0; pass < 3; pass++) {
      for (let d = 1; d < layers.length; d++) {
        const layer = layers[d] ?? [];
        const above = new Set((layers[d - 1] ?? []).map((n) => n.id));
        for (const node of layer) {
          const anchors = [...(this.neighbours.get(node.id) ?? [])]
            .filter((id) => above.has(id))
            .map((id) => index.get(id))
            .filter((i) => i != null);
          node._bary = anchors.length
            ? anchors.reduce((a, b) => a + b, 0) / anchors.length
            : Number.MAX_SAFE_INTEGER;
        }
        layer.sort(
          (a, b) => a._bary - b._bary || String(a.label ?? a.id).localeCompare(String(b.label ?? b.id))
        );
        reindex(layer);
      }
    }

    // each layer is one band, wrapped when it is wider than a screen can use
    let y = 0;
    const placeRow = (row) => {
      const height = Math.max(...row.map((n) => n.h));
      const width = row.reduce((a, n) => a + n.w, 0) + GAP_X * (row.length - 1);
      let x = -width / 2;
      for (const node of row) {
        node.x = x + node.w / 2;
        // tops aligned rather than centres — boxes in one layer differ in
        // height by however many columns they have, and a ragged top edge
        // reads as disorder rather than as a row
        node.y = y + node.h / 2;
        x += node.w + GAP_X;
      }
      y += height + GAP_Y;
    };

    for (const layer of layers) {
      if (!layer?.length) continue;
      for (let i = 0; i < layer.length; i += MAX_PER_ROW) placeRow(layer.slice(i, i + MAX_PER_ROW));
    }
    if (loose.length) {
      loose.sort((a, b) => String(a.label ?? a.id).localeCompare(String(b.label ?? b.id)));
      for (let i = 0; i < loose.length; i += MAX_PER_ROW) placeRow(loose.slice(i, i + MAX_PER_ROW));
    }

    // centre the whole thing on the origin, which is where the view is framed
    const midY = y / 2;
    for (const node of nodes) {
      node.y -= midY;
      node.vx = 0;
      node.vy = 0;
      delete node._bary;
    }
    this.draw();
  }

  _run() {
    if (this.running) return;
    this.running = true;
    this._raf = requestAnimationFrame(() => this._tick());
  }

  reheat(alpha = 0.5) {
    this.alpha = Math.max(this.alpha, alpha);
    this._run();
  }

  // ── simulation ──────────────────────────────────────────────────
  _tick() {
    const nodes = this.nodes;
    const n = nodes.length;

    if (this.alpha > 0.01 && n) {
      const repulsion = Math.max(60000, 20000 + n * 900);

      for (let i = 0; i < n; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < n; j++) {
          const b = nodes[j];
          let dx = b.x - a.x;
          let dy = b.y - a.y;
          let d2 = dx * dx + dy * dy;
          if (d2 > 4.5e6) continue;
          if (d2 < 1e-6) {
            dx = (Math.random() - 0.5) * 2;
            dy = (Math.random() - 0.5) * 2;
            d2 = dx * dx + dy * dy;
          }
          const d = Math.sqrt(d2);
          const effective = Math.max(d, 90);
          const force = repulsion / (effective * effective);
          a.vx -= (dx / d) * force; a.vy -= (dy / d) * force;
          b.vx += (dx / d) * force; b.vy += (dy / d) * force;
        }
      }

      for (const edge of this.edges) {
        const { source: a, target: b } = edge;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const rest = 300;
        const force = (d - rest) * 0.03;
        a.vx += (dx / d) * force; a.vy += (dy / d) * force;
        b.vx -= (dx / d) * force; b.vy -= (dy / d) * force;
      }

      const MAX_SPEED = 90;
      for (const node of nodes) {
        if (node === this._drag?.node) continue;
        node.vx -= node.x * 0.01;
        node.vy -= node.y * 0.01;
        node.vx *= 0.8;
        node.vy *= 0.8;
        const speed = Math.hypot(node.vx, node.vy);
        if (speed > MAX_SPEED) {
          node.vx = (node.vx / speed) * MAX_SPEED;
          node.vy = (node.vy / speed) * MAX_SPEED;
        }
        node.x += node.vx * this.alpha;
        node.y += node.vy * this.alpha;
      }

      // rectangle collision — push apart along the axis of least overlap
      for (let pass = 0; pass < 2; pass++) {
        for (let i = 0; i < n; i++) {
          const a = nodes[i];
          for (let j = i + 1; j < n; j++) {
            const b = nodes[j];
            const gapX = (a.w + b.w) / 2 + 26;
            const gapY = (a.h + b.h) / 2 + 20;
            const dx = b.x - a.x;
            const dy = b.y - a.y;
            const overlapX = gapX - Math.abs(dx);
            const overlapY = gapY - Math.abs(dy);
            if (overlapX <= 0 || overlapY <= 0) continue;

            if (overlapX < overlapY) {
              const push = (overlapX / 2) * (dx < 0 ? -1 : 1);
              if (a !== this._drag?.node) a.x -= push;
              if (b !== this._drag?.node) b.x += push;
            } else {
              const push = (overlapY / 2) * (dy < 0 ? -1 : 1);
              if (a !== this._drag?.node) a.y -= push;
              if (b !== this._drag?.node) b.y += push;
            }
          }
        }
      }

      this.alpha *= 0.965;
    }

    this.draw();

    if (this.alpha > 0.01 || this._drag) {
      this._raf = requestAnimationFrame(() => this._tick());
    } else {
      this.running = false;
      this.onSettle?.();
    }
  }

  // ── view ────────────────────────────────────────────────────────
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
    return {
      x: x * this.transform.k + this.transform.x + this.width / 2,
      y: y * this.transform.k + this.transform.y + this.height / 2,
    };
  }

  toWorld(sx, sy) {
    return {
      x: (sx - this.width / 2 - this.transform.x) / this.transform.k,
      y: (sy - this.height / 2 - this.transform.y) / this.transform.k,
    };
  }

  fit() {
    if (!this.nodes.length || !this.width) return;
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const node of this.nodes) {
      minX = Math.min(minX, node.x - node.w / 2);
      maxX = Math.max(maxX, node.x + node.w / 2);
      minY = Math.min(minY, node.y - node.h / 2);
      maxY = Math.max(maxY, node.y + node.h / 2);
    }
    // the legend sits over the bottom-left corner, so the frame keeps clear of it
    const LEGEND_H = 96;
    const k = Math.min(
      this.width / (maxX - minX + 100),
      (this.height - LEGEND_H) / (maxY - minY + 60),
      1.4
    );
    this.transform.k = Math.max(0.08, k);
    this.transform.x = -((minX + maxX) / 2) * this.transform.k;
    this.transform.y = -((minY + maxY) / 2) * this.transform.k - LEGEND_H / 2;
    this.draw();
  }

  focus(id, { zoom = 1 } = {}) {
    const node = this.byId.get(id);
    if (!node) return false;
    this.transform.k = zoom;
    this.transform.x = -node.x * zoom;
    this.transform.y = -node.y * zoom;
    this.draw();
    return true;
  }

  setSelected(id) {
    this.selectedId = id;
    this.draw();
  }

  // ── hit testing ─────────────────────────────────────────────────
  nodeAt(sx, sy) {
    const world = this.toWorld(sx, sy);
    for (let i = this.nodes.length - 1; i >= 0; i--) {
      const node = this.nodes[i];
      if (
        world.x >= node.x - node.w / 2 && world.x <= node.x + node.w / 2 &&
        world.y >= node.y - node.h / 2 && world.y <= node.y + node.h / 2
      ) return node;
    }
    return null;
  }

  /**
   * The click behaviour, addressed by position. mouseup resolves the row against
   * the box it picked up on mousedown; a tap has no such box, so it finds one
   * first and then follows the same rule — a $ref row opens the reference, the
   * rest of the box selects it.
   */
  _selectAt(sx, sy) {
    const node = this.nodeAt(sx, sy);
    if (!node) return false;
    const row = this.rowAt(node, sx, sy);
    if (this.foldAt(node, sx, sy)) this.toggleFold(node);
    else if (row?.refTarget) this.onRow(row, node);
    else this.onSelect(node);
    return true;
  }

  rowAt(node, sx, sy) {
    if (!node?.rows?.length) return null;
    const world = this.toWorld(sx, sy);
    const top = node.y - node.h / 2 + HEADER_H + PAD_Y;
    const index = Math.floor((world.y - top) / ROW_H);
    return index >= 0 && index < node.shownRows ? node.rows[index] : null;
  }

  /** True when the point is on the "+N more" / "show less" line of the box. */
  foldAt(node, sx, sy) {
    if (!node?.foldable) return false;
    const world = this.toWorld(sx, sy);
    const top = node.y - node.h / 2 + HEADER_H + PAD_Y;
    const index = Math.floor((world.y - top) / ROW_H);
    return index === node.shownRows;
  }

  /**
   * Open a box out to every column, or fold it back to the first MAX_ROWS.
   * The box grows downward from where it sits rather than re-running the
   * layout, so the one you opened does not walk off under your cursor.
   */
  toggleFold(node) {
    if (!node?.foldable) return false;
    const total = node.rows.length;
    const open = !this.expanded.has(node.id);
    if (open) this.expanded.add(node.id);
    else this.expanded.delete(node.id);

    const shown = open ? total : Math.min(total, MAX_ROWS);
    const grew = (shown - node.shownRows) * ROW_H;
    node.shownRows = shown;
    node.hiddenRows = total - shown;
    node.h += grew;
    node.y += grew / 2; // keep the header still; the box opens downward
    this.userAdjusted = true;
    this.reheat(0.12);
    this.draw();
    return true;
  }

  // ── drawing ─────────────────────────────────────────────────────
  draw() {
    const ctx = this.ctx;
    const styles = getComputedStyle(document.documentElement);
    const text = styles.getPropertyValue('--text').trim() || '#dcdde3';
    const dim = styles.getPropertyValue('--text-dim').trim() || '#9a9aa6';
    const faint = styles.getPropertyValue('--text-faint').trim() || '#6b6b78';
    const panel = styles.getPropertyValue('--bg-panel').trim() || '#1a1a21';
    const border = styles.getPropertyValue('--border').trim() || '#2c2c36';
    const accent = styles.getPropertyValue('--accent').trim() || '#a78bfa';
    const light = document.documentElement.dataset.theme === 'light';

    ctx.clearRect(0, 0, this.width, this.height);
    if (!this.nodes.length) {
      ctx.fillStyle = dim;
      ctx.font = '13px ui-sans-serif, system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Nothing to diagram in this scope', this.width / 2, this.height / 2);
      return;
    }

    const { k } = this.transform;
    // Only dim non-neighbours when the anchor is actually in this diagram —
    // a selection made in another view would otherwise fade everything.
    const anchor = this.hover?.id ?? this.selectedId;
    const related =
      anchor && this.byId.has(anchor)
        ? new Set([anchor, ...(this.neighbours?.get(anchor) ?? [])])
        : null;

    // ── edges ──
    // Related edges are drawn last so they sit on top of everything rather than
    // disappearing under a box, and they are drawn thicker, brighter and with a
    // glow — following one relationship out of a busy schema is the whole job.
    const drawEdge = (edge, active) => {
      const a = edge.source;
      const b = edge.target;

      // Anchor on the facing edges of the two boxes, choosing the axis they
      // are actually separated along — the layout stacks related boxes
      // vertically, so most lines leave the bottom of one and enter the top
      // of the next rather than crawling around their sides.
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const vertical = Math.abs(dy) > Math.abs(dx) * 0.8;
      const from = vertical
        ? this.toScreen(a.x, a.y + Math.sign(dy) * (a.h / 2))
        : this.toScreen(a.x + Math.sign(dx) * (a.w / 2), a.y);
      const to = vertical
        ? this.toScreen(b.x, b.y - Math.sign(dy) * (b.h / 2))
        : this.toScreen(b.x - Math.sign(dx) * (b.w / 2), b.y);
      if (Math.max(from.y, to.y) < -60 || Math.min(from.y, to.y) > this.height + 60) return;

      const muted = related && !active;
      ctx.strokeStyle = muted
        ? (light ? 'rgba(0,0,0,.10)' : 'rgba(255,255,255,.09)')
        : active
          ? (light ? '#6d28d9' : '#c4b5fd')
          : (light ? 'rgba(0,0,0,.42)' : 'rgba(255,255,255,.46)');

      // a child edge is the strongest statement on the diagram — this row
      // belongs to that row — so it is drawn heaviest
      const weight = edge.kind === 'child' ? 2.4 : 1.5;
      ctx.lineWidth = (active ? 2.8 : muted ? 1 : weight) * Math.min(1.6, Math.max(0.55, k));
      if (active) {
        ctx.shadowColor = light ? 'rgba(109,40,217,.45)' : 'rgba(196,181,253,.55)';
        ctx.shadowBlur = 10;
      }
      // dashed marks a relationship that was inferred rather than declared
      ctx.setLineDash(edge.dashed ? [5 * Math.min(1.5, k), 4 * Math.min(1.5, k)] : []);

      // control points, kept so the arrowhead can follow the curve's approach
      const midX = (from.x + to.x) / 2;
      const midY = (from.y + to.y) / 2;
      const c1 = vertical ? { x: from.x, y: midY } : { x: midX, y: from.y };
      const c2 = vertical ? { x: to.x, y: midY } : { x: midX, y: to.y };

      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.bezierCurveTo(c1.x, c1.y, c2.x, c2.y, to.x, to.y);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.shadowBlur = 0;

      // arrowhead + label, once the view is zoomed enough to read them
      if (k > 0.35 && !muted) {
        const angle = Math.atan2(to.y - c2.y, to.x - c2.x);
        const size = (active ? 8 : 6.5) * Math.min(2, Math.max(0.6, k));
        ctx.beginPath();
        ctx.moveTo(to.x, to.y);
        ctx.lineTo(to.x - size * Math.cos(angle - 0.4), to.y - size * Math.sin(angle - 0.4));
        ctx.lineTo(to.x - size * Math.cos(angle + 0.4), to.y - size * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fillStyle = ctx.strokeStyle;
        ctx.fill();

        if (edge.label && (active || k > 0.8)) {
          ctx.font = `${active ? 600 : 400} ${textSize(10, k, 8)}px ui-monospace, Menlo, monospace`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          const metrics = ctx.measureText(edge.label);
          ctx.fillStyle = light ? 'rgba(255,255,255,.92)' : 'rgba(20,20,26,.92)';
          ctx.fillRect(midX - metrics.width / 2 - 4, midY - 8, metrics.width + 8, 16);
          if (active) {
            ctx.strokeStyle = light ? 'rgba(109,40,217,.5)' : 'rgba(196,181,253,.5)';
            ctx.lineWidth = 1;
            ctx.strokeRect(midX - metrics.width / 2 - 4, midY - 8, metrics.width + 8, 16);
          }
          ctx.fillStyle = active ? (light ? '#6d28d9' : '#c4b5fd') : faint;
          ctx.fillText(edge.label, midX, midY);
        }
      }
    };

    const activeEdges = [];
    for (const edge of this.edges) {
      const active = Boolean(related && related.has(edge.source.id) && related.has(edge.target.id));
      if (active) activeEdges.push(edge);
      else drawEdge(edge, false);
    }
    for (const edge of activeEdges) drawEdge(edge, true);

    // ── boxes ──
    ctx.textBaseline = 'middle';
    for (const node of this.nodes) {
      const p = this.toScreen(node.x, node.y);
      const w = node.w * k;
      const h = node.h * k;
      const left = p.x - w / 2;
      const top = p.y - h / 2;
      if (left > this.width + 40 || left + w < -40 || top > this.height + 40 || top + h < -40) continue;

      const faded = related && !related.has(node.id);
      const selected = node.id === this.selectedId;
      // a neighbour of the selection — not the thing itself, but part of the
      // answer to "what is connected to this", so it is marked rather than
      // merely left undimmed
      const neighbour = !selected && related?.has(node.id);
      ctx.globalAlpha = faded ? 0.18 : 1;

      // body
      ctx.beginPath();
      ctx.roundRect(left, top, w, h, 6 * Math.min(1.5, k));
      ctx.fillStyle = panel;
      ctx.fill();
      if (selected || neighbour) {
        ctx.shadowColor = selected
          ? (light ? 'rgba(109,40,217,.5)' : 'rgba(167,139,250,.55)')
          : (light ? 'rgba(109,40,217,.22)' : 'rgba(167,139,250,.25)');
        ctx.shadowBlur = selected ? 18 : 9;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
      ctx.lineWidth = selected ? 2.6 : neighbour ? 1.8 : 1;
      ctx.strokeStyle = selected
        ? accent
        : neighbour
          ? (light ? 'rgba(109,40,217,.55)' : 'rgba(167,139,250,.6)')
          : border;
      ctx.stroke();

      // header band in the node's own colour
      ctx.save();
      ctx.beginPath();
      ctx.roundRect(left, top, w, h, 6 * Math.min(1.5, k));
      ctx.clip();
      ctx.fillStyle = node.color + (light ? '26' : '22');
      ctx.fillRect(left, top, w, HEADER_H * k);
      ctx.fillStyle = node.color;
      ctx.fillRect(left, top, 3 * Math.min(1.5, k), h);
      ctx.restore();

      if (k < 0.28) { ctx.globalAlpha = 1; continue; }

      // title
      ctx.textAlign = 'left';
      const titleSize = textSize(11.5, k, 7);
      ctx.font = `600 ${titleSize}px ui-sans-serif, system-ui, sans-serif`;
      ctx.fillStyle = selected ? accent : text;
      ctx.fillText(fit(ctx, node.title, w - 16 * k), left + 8 * k, top + (HEADER_H / 2) * k);

      if (node.badge && k > 0.5) {
        ctx.font = `${textSize(9, k, 6)}px ui-monospace, Menlo, monospace`;
        ctx.fillStyle = faint;
        ctx.textAlign = 'right';
        ctx.fillText(node.badge, left + w - 7 * k, top + (HEADER_H / 2) * k);
        ctx.textAlign = 'left';
      }

      if (!this.showRows || k < 0.42 || !node.rows?.length) { ctx.globalAlpha = 1; continue; }

      // rows
      const rowSize = textSize(10, k, 6);
      let y = top + (HEADER_H + PAD_Y) * k + (ROW_H * k) / 2;
      for (let i = 0; i < node.shownRows; i++) {
        const row = node.rows[i];
        ctx.font = `${row.strong ? '600 ' : ''}${rowSize}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillStyle = row.refTarget ? node.color : dim;
        ctx.fillText(fit(ctx, row.label, w * 0.56), left + 9 * k, y);

        if (row.value) {
          ctx.font = `${rowSize}px ui-monospace, Menlo, monospace`;
          ctx.fillStyle = faint;
          ctx.textAlign = 'right';
          ctx.fillText(fit(ctx, row.value, w * 0.4), left + w - 8 * k, y);
          ctx.textAlign = 'left';
        }
        y += ROW_H * k;
      }

      // The fold line. It is a control, so it says so: underlined on hover and
      // lit in the box's own colour, rather than sitting there looking like the
      // note that it used to be.
      if (node.foldable) {
        const open = node.hiddenRows === 0;
        const label = open ? '− show less' : `+${node.hiddenRows} more`;
        const hot = this.hover === node && this.hoverFold;
        ctx.font = `italic ${rowSize}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillStyle = hot ? node.color : faint;
        ctx.fillText(label, left + 9 * k, y);
        if (hot) {
          const w2 = ctx.measureText(label).width;
          ctx.fillRect(left + 9 * k, y + rowSize * 0.62, w2, Math.max(1, k));
        }
      }

      ctx.globalAlpha = 1;
    }
  }

  // ── interaction ─────────────────────────────────────────────────
  _bind() {
    const canvas = this.canvas;

    canvas.addEventListener('mousedown', (e) => {
      const node = this.nodeAt(e.offsetX, e.offsetY);
      if (node) {
        this._drag = { node, moved: false, sx: e.offsetX, sy: e.offsetY };
        this.reheat(0.25);
      } else {
        this._pan = { x: e.offsetX, y: e.offsetY, tx: this.transform.x, ty: this.transform.y };
        canvas.style.cursor = 'grabbing';
      }
    });

    window.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      if (this._drag) {
        const world = this.toWorld(e.clientX - rect.left, e.clientY - rect.top);
        this._drag.node.x = world.x;
        this._drag.node.y = world.y;
        this._drag.node.vx = 0;
        this._drag.node.vy = 0;
        if (Math.abs(e.clientX - rect.left - this._drag.sx) > 3) this._drag.moved = true;
        this.reheat(0.2);
        return;
      }
      if (this._pan) {
        this.transform.x = this._pan.tx + (e.clientX - rect.left - this._pan.x);
        this.transform.y = this._pan.ty + (e.clientY - rect.top - this._pan.y);
        this.userAdjusted = true;
        this.draw();
      }
    });

    window.addEventListener('mouseup', (e) => {
      if (this._drag && !this._drag.moved) {
        const rect = canvas.getBoundingClientRect();
        const node = this._drag.node;
        const x = e.clientX - rect.left, y = e.clientY - rect.top;
        const row = this.rowAt(node, x, y);
        if (this.foldAt(node, x, y)) this.toggleFold(node);
        else if (row?.refTarget) this.onRow(row, node);
        else this.onSelect(node);
      }
      this._drag = null;
      this._pan = null;
      canvas.style.cursor = 'grab';
    });

    canvas.addEventListener('mousemove', (e) => {
      if (this._drag || this._pan) return;
      const node = this.nodeAt(e.offsetX, e.offsetY);
      const row = node ? this.rowAt(node, e.offsetX, e.offsetY) : null;
      const fold = node ? this.foldAt(node, e.offsetX, e.offsetY) : false;
      if (node !== this.hover || row !== this.hoverRow || fold !== this.hoverFold) {
        this.hover = node;
        this.hoverRow = row;
        this.hoverFold = fold;
        canvas.style.cursor = node ? 'pointer' : 'grab';
        this.draw();
      }
    });

    canvas.addEventListener('mouseleave', () => {
      this.hover = null;
      this.hoverRow = null;
      this.draw();
    });

    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.userAdjusted = true;
      const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
      const next = Math.max(0.06, Math.min(3, this.transform.k * factor));
      const before = this.toWorld(e.offsetX, e.offsetY);
      this.transform.k = next;
      const after = this.toWorld(e.offsetX, e.offsetY);
      this.transform.x += (after.x - before.x) * next;
      this.transform.y += (after.y - before.y) * next;
      this.draw();
    }, { passive: false });

    // Fingers. Boxes stay where they are put on touch — one finger has to pan,
    // and the layout is already arranged sensibly without being dragged.
    enableTouch(canvas, this, {
      min: 0.06,
      max: 3,
      onTap: (x, y) => this._selectAt(x, y),
    });
  }

  destroy() {
    cancelAnimationFrame(this._raf);
    this._ro?.disconnect();
  }
}

/** Trim text to fit `maxWidth` in the current font, adding an ellipsis. */
function fit(ctx, text, maxWidth) {
  const value = String(text ?? '');
  if (ctx.measureText(value).width <= maxWidth) return value;
  let out = value;
  while (out.length > 1 && ctx.measureText(out + '…').width > maxWidth) out = out.slice(0, -1);
  return out + '…';
}
