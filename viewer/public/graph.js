// Force-directed canvas graph.
//
// Naive O(n^2) repulsion — fine for the few hundred nodes any single scope
// renders, and it keeps the layout stable and dependency-free. The simulation
// cools with an alpha decay and parks itself, then only re-heats on interaction.

import { enableTouch } from './touch.js';

const TYPE_COLORS = {
  file: '#a78bfa',
  operation: '#60a5fa',
  schema: '#34d399',
  param: '#fbbf24',
  response: '#fb923c',
  requestBody: '#fbbf24',
  securityScheme: '#94a3b8',
  permission: '#f472b6',
};

const GROUP_COLORS = {
  spine: '#60a5fa',
  satellite: '#34d399',
  shared: '#fbbf24',
  permission: '#f472b6',
};

// Canvas cannot read CSS custom properties, so the light palette is mirrored
// here. These are the darker, higher-contrast variants used on light grounds.
const TYPE_COLORS_LIGHT = {
  file: '#7c3aed',
  operation: '#2563eb',
  schema: '#059669',
  param: '#b45309',
  response: '#c2410c',
  requestBody: '#b45309',
  securityScheme: '#475569',
  permission: '#db2777',
};

const GROUP_COLORS_LIGHT = {
  spine: '#2563eb',
  satellite: '#059669',
  shared: '#b45309',
  permission: '#db2777',
};

export function colorForNode(node, by = 'type') {
  const light = document.documentElement.dataset.theme === 'light';
  const types = light ? TYPE_COLORS_LIGHT : TYPE_COLORS;
  const groups = light ? GROUP_COLORS_LIGHT : GROUP_COLORS;
  if (by === 'group') return groups[node.group] ?? types[node.type] ?? '#8b8b93';
  return types[node.type] ?? '#8b8b93';
}

export class Graph {
  constructor(canvas, { onSelect, onHover } = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.onSelect = onSelect ?? (() => {});
    this.onHover = onHover ?? (() => {});

    this.nodes = [];
    this.links = [];
    this.byId = new Map();

    // seeded so a graph built while the view is hidden still has sane bounds
    this.width = 800;
    this.height = 600;
    this.transform = { x: 0, y: 0, k: 1 };
    this.alpha = 1;
    this.running = false;
    this.showLabels = true;
    this.colorBy = 'type';

    this.selectedId = null;
    this.hoverNode = null;
    this.highlighted = new Set(); // neighbours of hover/selection

    this._drag = null;
    this._pan = null;
    this._raf = null;

    this._bindEvents();
    this._resize();
    this._ro = new ResizeObserver(() => this._resize());
    this._ro.observe(canvas);
  }

  // ── data ────────────────────────────────────────────────────────
  /**
   * @param options.placed  the caller has set x/y on every node and the
   *                        simulation should leave them alone. Used by the
   *                        spine view, where position carries meaning — a
   *                        contract's ring is its tier — and a force layout
   *                        would throw that away.
   * @param options.directed  draw arrowheads. Publisher and consumer are not
   *                          interchangeable, so the direction has to be visible.
   */
  setData(nodes, links, options = {}) {
    this.placed = Boolean(options.placed);
    this.directed = Boolean(options.directed);
    // preserve positions of nodes that survive a reload so the layout doesn't jump
    const previous = new Map(this.nodes.map((n) => [n.id, n]));
    // Seed on a phyllotaxis spiral scaled to the node count. Spacing the seeds
    // properly matters: nodes that start nearly coincident produce enormous
    // repulsion spikes that blow the integrator up.
    const spread = 42 * Math.sqrt(Math.max(1, nodes.length));

    this.nodes = nodes.map((source, i) => {
      const old = previous.get(source.id);
      const angle = i * 2.399963; // golden angle
      const r = spread * Math.sqrt((i + 0.5) / nodes.length);
      const seeded = this.placed
        ? { x: source.x, y: source.y }
        : { x: old?.x ?? Math.cos(angle) * r, y: old?.y ?? Math.sin(angle) * r };
      return { ...source, ...seeded, vx: 0, vy: 0, degree: 0 };
    });

    this.byId = new Map(this.nodes.map((n) => [n.id, n]));

    this.links = [];
    for (const link of links) {
      const source = this.byId.get(link.source);
      const target = this.byId.get(link.target);
      if (!source || !target) continue;
      // carry the caller's own styling through — the spine view colours an edge
      // by whether the consumer is critical, which is the whole point of it
      this.links.push({
        source,
        target,
        weight: link.weight ?? 1,
        kind: link.kind,
        color: link.color,
        width: link.width,
        events: link.events,
      });
      source.degree += 1;
      target.degree += 1;
    }

    this.neighbours = new Map();
    for (const link of this.links) {
      if (!this.neighbours.has(link.source.id)) this.neighbours.set(link.source.id, new Set());
      if (!this.neighbours.has(link.target.id)) this.neighbours.set(link.target.id, new Set());
      this.neighbours.get(link.source.id).add(link.target.id);
      this.neighbours.get(link.target.id).add(link.source.id);
    }

    for (const node of this.nodes) {
      node.r = this._radius(node);
      // Half the width of the label drawn under this node. What makes a graph
      // look cluttered is almost never the dots touching — it is the names
      // overlapping, and a name is far wider than the dot it belongs to. So the
      // collision pass below separates on this rather than on the radius.
      const label = node.name.length > 30 ? 30 : node.name.length;
      node.halfLabel = Math.max(node.r, label * 2.9);
    }

    this.userAdjusted = false; // a fresh layout may frame itself again
    // a placed layout is already where it belongs; running the simulation over
    // it would only undo the arrangement
    if (this.placed) {
      this.alpha = 0;
      this.draw();
    } else {
      this.reheat(1);
    }
  }

  _radius(node) {
    // A caller that has worked out its own weight — operations, say — knows
    // better than the degree does. In the contracts view every file node has a
    // degree of zero, so sizing by it made every contract the same dot.
    if (node.weight != null) return 6 + Math.min(20, Math.sqrt(node.weight) * 1.5);
    const base = node.type === 'file' ? 7 : 4;
    return base + Math.min(11, Math.sqrt(node.degree) * 1.7);
  }

  // ── simulation ──────────────────────────────────────────────────
  reheat(alpha = 0.65) {
    // A placed layout has meaning in its coordinates. Dragging a node still
    // moves it — the mousemove handler writes x/y directly — but nothing else
    // is allowed to drift, so the simulation never restarts.
    if (this.placed) {
      this.draw();
      return;
    }
    this.alpha = Math.max(this.alpha, alpha);
    if (!this.running) {
      this.running = true;
      this._raf = requestAnimationFrame(() => this._tick());
    }
  }

  _tick() {
    const nodes = this.nodes;
    const n = nodes.length;

    if (this.alpha > 0.008 && n) {
      // Repulsion, scaled so dense graphs spread further apart. The near-field
      // distance is floored: an unclamped 1/d^2 term between two nearly
      // coincident nodes produces a velocity spike that diverges immediately.
      // The floor keeps small graphs (the contract view) well separated.
      const repulsion = Math.max(2600, 600 + n * 5);
      const MIN_DISTANCE = 18;
      const CUTOFF = 1.2e6; // beyond ~1100px the contribution is negligible
      for (let i = 0; i < n; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < n; j++) {
          const b = nodes[j];
          let dx = b.x - a.x;
          let dy = b.y - a.y;
          let d2 = dx * dx + dy * dy;
          if (d2 > CUTOFF) continue;
          if (d2 < 1e-6) {
            dx = (Math.random() - 0.5) * 2;
            dy = (Math.random() - 0.5) * 2;
            d2 = dx * dx + dy * dy;
          }
          const d = Math.sqrt(d2);
          const effective = Math.max(d, MIN_DISTANCE);
          const force = repulsion / (effective * effective);
          const fx = (dx / d) * force;
          const fy = (dy / d) * force;
          a.vx -= fx; a.vy -= fy;
          b.vx += fx; b.vy += fy;
        }
      }

      // springs
      for (const link of this.links) {
        const { source: a, target: b } = link;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const rest = 78 + (a.r + b.r) * 1.6;
        const strength = 0.032 * Math.min(3, Math.log2(link.weight + 1) + 1);
        const force = (d - rest) * strength;
        const fx = (dx / d) * force;
        const fy = (dy / d) * force;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }

      // Gravity to origin + integrate, with a speed cap as a divergence backstop.
      //
      // Gravity is only here to stop disconnected components drifting off; it is
      // not a layout force. Set too high it fights the repulsion and packs
      // everything into the middle, which is what "cluttered" looks like. It also
      // has to weaken as the graph grows, because it pulls on every node while
      // repulsion falls off with distance — so a constant here crushes a large
      // graph much harder than a small one.
      const gravity = 0.0032 * Math.min(1, 40 / Math.max(40, n));
      const MAX_SPEED = 55;
      for (const node of nodes) {
        if (node === this._drag?.node) continue;
        node.vx -= node.x * gravity;
        node.vy -= node.y * gravity;
        node.vx *= 0.82;
        node.vy *= 0.82;

        const speed = Math.hypot(node.vx, node.vy);
        if (speed > MAX_SPEED) {
          node.vx = (node.vx / speed) * MAX_SPEED;
          node.vy = (node.vy / speed) * MAX_SPEED;
        }

        node.x += node.vx * this.alpha;
        node.y += node.vy * this.alpha;
      }

      // Collision resolution. Hub nodes are pulled to the centre by dozens of
      // springs, which overwhelms the repulsion term and stacks them on top of
      // each other; separating positions directly guarantees readable labels.
      //
      // Two passes, because a node occupies two different shapes. The dot is a
      // circle; the label under it is a wide, short box, and the box is what
      // collides first — `removeBlacklistEntry` is ~90px wide against a 10px
      // dot. Resolving only the circles leaves the dots tidy and the names in a
      // heap, which is exactly the cluttered case.
      const LABEL_BAND = 16; // labels only clash if they sit on nearly the same line
      for (let i = 0; i < n; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < n; j++) {
          const b = nodes[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const d2 = dx * dx + dy * dy;

          // ---- the dots
          const minDistance = a.r + b.r + 14;
          if (d2 < minDistance * minDistance && d2 > 0) {
            const d = Math.sqrt(d2);
            const push = (minDistance - d) / 2;
            const ux = dx / d;
            const uy = dy / d;
            if (a !== this._drag?.node) { a.x -= ux * push; a.y -= uy * push; }
            if (b !== this._drag?.node) { b.x += ux * push; b.y += uy * push; }
          }

          // ---- the labels, pushed apart sideways only
          if (!this.showLabels) continue;
          if (Math.abs(b.y - a.y) > LABEL_BAND) continue;
          const gap = a.halfLabel + b.halfLabel + 6;
          const horizontal = b.x - a.x;
          const spread = Math.abs(horizontal);
          if (spread >= gap) continue;
          // pushing vertically would just fight the springs; sliding sideways
          // separates the text and leaves the graph's shape intact
          const push = (gap - spread) / 2;
          const dir = horizontal === 0 ? (i % 2 ? 1 : -1) : Math.sign(horizontal);
          if (a !== this._drag?.node) a.x -= dir * push * 0.5;
          if (b !== this._drag?.node) b.x += dir * push * 0.5;
        }
      }

      this.alpha *= 0.97;
    }

    this.draw();

    if (this.alpha > 0.008 || this._drag) {
      this._raf = requestAnimationFrame(() => this._tick());
    } else {
      this.running = false;
      this.onSettle?.(); // the layout has converged — a good moment to frame it
    }
  }

  // ── view helpers ────────────────────────────────────────────────
  /** Re-measure the canvas. Call this after unhiding the view. */
  resize() {
    this._resize();
  }

  _resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    // A hidden view measures 0x0. Keeping the last known size matters because
    // draw() culls by viewport bounds — zero dimensions would cull everything.
    if (rect.width === 0 || rect.height === 0) return;
    this.width = rect.width;
    this.height = rect.height;
    this.canvas.width = Math.max(1, Math.round(rect.width * dpr));
    this.canvas.height = Math.max(1, Math.round(rect.height * dpr));
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.draw();
  }

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

  recenter() {
    if (!this.nodes.length || !this.width || !this.height) return;
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    for (const node of this.nodes) {
      minX = Math.min(minX, node.x); maxX = Math.max(maxX, node.x);
      minY = Math.min(minY, node.y); maxY = Math.max(maxY, node.y);
    }
    const spanX = Math.max(1, maxX - minX);
    const spanY = Math.max(1, maxY - minY);
    // the legend sits over the bottom left; a node parked underneath it reads
    // as missing, so the frame gives it room rather than drawing behind it
    const reserve = this.reserveBottom ?? 0;
    const k = Math.min(this.width / (spanX + 120), (this.height - reserve) / (spanY + 120), 2.2);
    this.transform.k = Math.max(0.12, k);
    this.transform.x = -((minX + maxX) / 2) * this.transform.k;
    this.transform.y = -((minY + maxY) / 2) * this.transform.k - reserve / 2;
    this.draw();
  }

  focusNode(id, { zoom = 1.5 } = {}) {
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
    this._updateHighlight();
    this.draw();
  }

  _updateHighlight() {
    const anchor = this.hoverNode?.id ?? this.selectedId;
    // Only dim non-neighbours when the anchor is actually in this scope —
    // otherwise a selection made elsewhere fades the whole graph to 20%.
    this.highlighted =
      anchor && this.byId.has(anchor)
        ? new Set([anchor, ...(this.neighbours?.get(anchor) ?? [])])
        : new Set();
  }

  // ── hit testing ─────────────────────────────────────────────────
  /**
   * The click behaviour, addressed by position rather than by a node picked up
   * on mousedown. A tap has no press-then-release to hold a node across, so it
   * hit-tests where the finger landed and calls the same onSelect a click does.
   */
  _selectAt(sx, sy) {
    const node = this.nodeAt(sx, sy);
    if (node) this.onSelect(node);
    return Boolean(node);
  }

  nodeAt(sx, sy) {
    const world = this.toWorld(sx, sy);
    let best = null;
    let bestD = Infinity;
    for (const node of this.nodes) {
      const dx = node.x - world.x;
      const dy = node.y - world.y;
      const d = Math.sqrt(dx * dx + dy * dy);
      const hit = node.r + 6 / this.transform.k;
      if (d < hit && d < bestD) { best = node; bestD = d; }
    }
    return best;
  }

  // ── drawing ─────────────────────────────────────────────────────
  draw() {
    const ctx = this.ctx;
    const styles = getComputedStyle(document.documentElement);
    const dim = styles.getPropertyValue('--text-dim').trim() || '#9a9aa6';
    const text = styles.getPropertyValue('--text').trim() || '#dcdde3';
    const isLight = document.documentElement.dataset.theme === 'light';

    ctx.clearRect(0, 0, this.width, this.height);
    if (!this.nodes.length) {
      ctx.fillStyle = dim;
      ctx.font = '13px ui-sans-serif, system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('No nodes in this view', this.width / 2, this.height / 2);
      return;
    }

    const hasFocus = this.highlighted.size > 0;
    const { k } = this.transform;

    // links — active ones last so a highlighted edge is never drawn over
    const isActive = (link) =>
      hasFocus && this.highlighted.has(link.source.id) && this.highlighted.has(link.target.id);
    const ordered = this.directed
      ? [...this.links].sort((a, b) => Number(isActive(a)) - Number(isActive(b)))
      : this.links;

    for (const link of ordered) {
      const a = this.toScreen(link.source.x, link.source.y);
      const b = this.toScreen(link.target.x, link.target.y);
      const active = isActive(link);

      // A directed edge stops at the node's rim rather than its centre, or the
      // arrowhead disappears underneath the circle it is pointing at.
      const angle = Math.atan2(b.y - a.y, b.x - a.x);
      const rim = this.directed ? link.target.r * Math.min(1.8, Math.max(0.55, k)) + 2 : 0;
      const tip = { x: b.x - Math.cos(angle) * rim, y: b.y - Math.sin(angle) * rim };

      ctx.save();
      if (active && this.directed) {
        ctx.shadowColor = link.color ?? (isLight ? 'rgba(124,58,237,.6)' : 'rgba(167,139,250,.6)');
        ctx.shadowBlur = 10;
      }
      ctx.beginPath();
      ctx.moveTo(a.x, a.y);
      ctx.lineTo(tip.x, tip.y);
      ctx.lineWidth = link.width
        ? link.width * (active ? 2 : 1) * Math.min(1.7, Math.max(0.6, k))
        : Math.min(3.5, 0.5 + Math.log2(link.weight + 1) * 0.55) * Math.min(1.6, k);
      if (active) {
        ctx.strokeStyle = link.color ?? (isLight ? 'rgba(124,58,237,.75)' : 'rgba(167,139,250,.75)');
      } else if (hasFocus) {
        ctx.strokeStyle = isLight ? 'rgba(0,0,0,.05)' : 'rgba(255,255,255,.035)';
      } else {
        ctx.strokeStyle =
          link.color ?? (isLight ? 'rgba(0,0,0,.11)' : 'rgba(255,255,255,.09)');
      }
      ctx.stroke();
      ctx.restore();

      if (this.directed && !(hasFocus && !active)) {
        const size = (active ? 9 : 7) * Math.min(1.5, Math.max(0.6, k));
        ctx.beginPath();
        ctx.moveTo(tip.x, tip.y);
        ctx.lineTo(tip.x - size * Math.cos(angle - 0.4), tip.y - size * Math.sin(angle - 0.4));
        ctx.lineTo(tip.x - size * Math.cos(angle + 0.4), tip.y - size * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fillStyle = ctx.strokeStyle;
        ctx.fill();
      }
    }

    // nodes
    for (const node of this.nodes) {
      const p = this.toScreen(node.x, node.y);
      const r = node.r * Math.min(1.8, Math.max(0.55, k));
      if (p.x < -60 || p.x > this.width + 60 || p.y < -60 || p.y > this.height + 60) continue;

      const faded = hasFocus && !this.highlighted.has(node.id);
      const selected = node.id === this.selectedId;

      ctx.globalAlpha = faded ? 0.2 : 1;
      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fillStyle = colorForNode(node, this.colorBy);
      ctx.fill();

      if (selected) {
        ctx.lineWidth = 2.5;
        ctx.strokeStyle = text;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(p.x, p.y, r + 5, 0, Math.PI * 2);
        ctx.lineWidth = 1;
        ctx.strokeStyle = isLight ? 'rgba(124,58,237,.5)' : 'rgba(167,139,250,.5)';
        ctx.stroke();
      } else if (node === this.hoverNode) {
        ctx.lineWidth = 2;
        ctx.strokeStyle = text;
        ctx.stroke();
      }

      // labels — only when they will be readable and uncluttered
      const labelWorthy =
        this.showLabels &&
        !faded &&
        (k > 0.85 || node.type === 'file' || selected || node === this.hoverNode || node.degree > 12);

      if (labelWorthy) {
        const label = node.name.length > 30 ? node.name.slice(0, 29) + '…' : node.name;
        ctx.globalAlpha = faded ? 0.2 : 1;
        ctx.font = `${node.type === 'file' ? '600 ' : ''}${Math.max(9, 11 * k)}px ui-sans-serif, system-ui, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        const y = p.y + r + 3;
        ctx.lineWidth = 3;
        ctx.strokeStyle = isLight ? 'rgba(255,255,255,.85)' : 'rgba(20,20,26,.85)';
        ctx.strokeText(label, p.x, y);
        ctx.fillStyle = selected || node === this.hoverNode ? text : dim;
        ctx.fillText(label, p.x, y);
      }
      ctx.globalAlpha = 1;
    }
  }

  // ── interaction ─────────────────────────────────────────────────
  _bindEvents() {
    const canvas = this.canvas;

    canvas.addEventListener('mousedown', (e) => {
      const node = this.nodeAt(e.offsetX, e.offsetY);
      if (node) {
        this._drag = { node, moved: false };
        this.reheat(0.35);
      } else {
        this._pan = { x: e.offsetX, y: e.offsetY, tx: this.transform.x, ty: this.transform.y };
        canvas.classList.add('dragging');
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (this._drag) {
        const rect = canvas.getBoundingClientRect();
        const world = this.toWorld(e.clientX - rect.left, e.clientY - rect.top);
        this._drag.node.x = world.x;
        this._drag.node.y = world.y;
        this._drag.node.vx = 0;
        this._drag.node.vy = 0;
        this._drag.moved = true;
        this.reheat(0.25);
        return;
      }
      if (this._pan) {
        this.userAdjusted = true;
        this.transform.x = this._pan.tx + (e.offsetX - this._pan.x);
        this.transform.y = this._pan.ty + (e.offsetY - this._pan.y);
        this.draw();
      }
    });

    window.addEventListener('mouseup', () => {
      if (this._drag && !this._drag.moved) this.onSelect(this._drag.node);
      this._drag = null;
      this._pan = null;
      canvas.classList.remove('dragging');
    });

    canvas.addEventListener('mousemove', (e) => {
      if (this._drag || this._pan) return;
      const node = this.nodeAt(e.offsetX, e.offsetY);
      if (node !== this.hoverNode) {
        this.hoverNode = node;
        this._updateHighlight();
        this.draw();
        this.onHover(node, e);
      } else if (node) {
        this.onHover(node, e);
      }
    });

    canvas.addEventListener('mouseleave', () => {
      this.hoverNode = null;
      this._updateHighlight();
      this.draw();
      this.onHover(null);
    });

    canvas.addEventListener(
      'wheel',
      (e) => {
        e.preventDefault();
        this.userAdjusted = true;
        const factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
        const next = Math.max(0.08, Math.min(6, this.transform.k * factor));
        // zoom toward the cursor
        const before = this.toWorld(e.offsetX, e.offsetY);
        this.transform.k = next;
        const after = this.toWorld(e.offsetX, e.offsetY);
        this.transform.x += (after.x - before.x) * next;
        this.transform.y += (after.y - before.y) * next;
        this.draw();
      },
      { passive: false }
    );

    canvas.addEventListener('dblclick', (e) => {
      const node = this.nodeAt(e.offsetX, e.offsetY);
      if (node) this.onSelect(node, { open: true });
    });

    // Fingers. Dragging a node is deliberately not offered: one finger has to
    // pan, or the graph cannot be moved at all, and there is no second button
    // to put the other gesture on.
    enableTouch(canvas, this, {
      min: 0.08,
      max: 6,
      onTap: (x, y) => this._selectAt(x, y),
    });
  }

  destroy() {
    cancelAnimationFrame(this._raf);
    this._ro?.disconnect();
  }
}
