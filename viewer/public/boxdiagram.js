// Force-directed diagram of *boxes* rather than dots — used by both the ER view
// (entities with their fields) and the Flow view (operations with their inputs
// and outputs). Boxes carry rows, so collision has to work on rectangles.
//
// The force recipe mirrors graph.js: clamped near-field repulsion, springs,
// a speed cap, then hard collision resolution to guarantee nothing overlaps.

const HEADER_H = 26;
const ROW_H = 17;
const BOX_W = 216;
const PAD_Y = 6;
const MAX_ROWS = 11;

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
    const spread = 90 * Math.sqrt(Math.max(1, nodes.length));

    this.nodes = nodes.map((source, i) => {
      const old = previous.get(source.id);
      const angle = i * 2.399963;
      const r = spread * Math.sqrt((i + 0.5) / nodes.length);
      const shown = Math.min(source.rows?.length ?? 0, MAX_ROWS);
      const hidden = (source.rows?.length ?? 0) - shown;
      return {
        ...source,
        shownRows: shown,
        hiddenRows: hidden,
        w: BOX_W,
        h: HEADER_H + PAD_Y * 2 + shown * ROW_H + (hidden > 0 ? ROW_H : 0),
        x: old?.x ?? Math.cos(angle) * r,
        y: old?.y ?? Math.sin(angle) * r,
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

    this.userAdjusted = false;
    this.alpha = 1;
    this._run();
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
    const k = Math.min(this.width / (maxX - minX + 100), this.height / (maxY - minY + 100), 1.4);
    this.transform.k = Math.max(0.08, k);
    this.transform.x = -((minX + maxX) / 2) * this.transform.k;
    this.transform.y = -((minY + maxY) / 2) * this.transform.k;
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

  rowAt(node, sx, sy) {
    if (!node?.rows?.length) return null;
    const world = this.toWorld(sx, sy);
    const top = node.y - node.h / 2 + HEADER_H + PAD_Y;
    const index = Math.floor((world.y - top) / ROW_H);
    return index >= 0 && index < node.shownRows ? node.rows[index] : null;
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
    for (const edge of this.edges) {
      const a = edge.source;
      const b = edge.target;
      const active = related && related.has(a.id) && related.has(b.id);
      if (related && !active) {
        ctx.strokeStyle = light ? 'rgba(0,0,0,.05)' : 'rgba(255,255,255,.04)';
      } else {
        ctx.strokeStyle = active
          ? (light ? 'rgba(124,58,237,.8)' : 'rgba(167,139,250,.85)')
          : (light ? 'rgba(0,0,0,.3)' : 'rgba(255,255,255,.3)');
      }

      // anchor the line on the facing edges of the two boxes
      const dx = b.x - a.x;
      const from = this.toScreen(a.x + Math.sign(dx) * (a.w / 2), a.y);
      const to = this.toScreen(b.x - Math.sign(dx) * (b.w / 2), b.y);
      if (Math.max(from.y, to.y) < -60 || Math.min(from.y, to.y) > this.height + 60) continue;

      ctx.lineWidth = (active ? 1.8 : 1) * Math.min(1.6, Math.max(0.5, k));
      const midX = (from.x + to.x) / 2;
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.bezierCurveTo(midX, from.y, midX, to.y, to.x, to.y);
      ctx.stroke();

      // arrowhead + label, only when zoomed enough to read
      if (k > 0.45) {
        const angle = Math.atan2(to.y - from.y, to.x - midX);
        const size = 6 * Math.min(1.4, k);
        ctx.beginPath();
        ctx.moveTo(to.x, to.y);
        ctx.lineTo(to.x - size * Math.cos(angle - 0.4), to.y - size * Math.sin(angle - 0.4));
        ctx.lineTo(to.x - size * Math.cos(angle + 0.4), to.y - size * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fillStyle = ctx.strokeStyle;
        ctx.fill();

        if (edge.label && (active || k > 0.8)) {
          ctx.font = `${Math.min(11, 9 * k + 2)}px ui-monospace, Menlo, monospace`;
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          const lx = (from.x + to.x) / 2;
          const ly = (from.y + to.y) / 2;
          const metrics = ctx.measureText(edge.label);
          ctx.fillStyle = light ? 'rgba(255,255,255,.9)' : 'rgba(20,20,26,.9)';
          ctx.fillRect(lx - metrics.width / 2 - 3, ly - 7, metrics.width + 6, 14);
          ctx.fillStyle = active ? accent : faint;
          ctx.fillText(edge.label, lx, ly);
        }
      }
    }

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
      ctx.globalAlpha = faded ? 0.25 : 1;

      // body
      ctx.beginPath();
      ctx.roundRect(left, top, w, h, 6 * Math.min(1.5, k));
      ctx.fillStyle = panel;
      ctx.fill();
      ctx.lineWidth = selected ? 2 : 1;
      ctx.strokeStyle = selected ? accent : border;
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
      const titleSize = Math.min(12.5, Math.max(7, 11.5 * k));
      ctx.font = `600 ${titleSize}px ui-sans-serif, system-ui, sans-serif`;
      ctx.fillStyle = selected ? accent : text;
      ctx.fillText(fit(ctx, node.title, w - 16 * k), left + 8 * k, top + (HEADER_H / 2) * k);

      if (node.badge && k > 0.5) {
        ctx.font = `${Math.min(10, 9 * k)}px ui-monospace, Menlo, monospace`;
        ctx.fillStyle = faint;
        ctx.textAlign = 'right';
        ctx.fillText(node.badge, left + w - 7 * k, top + (HEADER_H / 2) * k);
        ctx.textAlign = 'left';
      }

      if (!this.showRows || k < 0.42 || !node.rows?.length) { ctx.globalAlpha = 1; continue; }

      // rows
      const rowSize = Math.min(11, Math.max(6, 10 * k));
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

      if (node.hiddenRows > 0) {
        ctx.font = `italic ${rowSize}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillStyle = faint;
        ctx.fillText(`+${node.hiddenRows} more`, left + 9 * k, y);
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
        const row = this.rowAt(node, e.clientX - rect.left, e.clientY - rect.top);
        if (row?.refTarget) this.onRow(row, node);
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
      if (node !== this.hover || row !== this.hoverRow) {
        this.hover = node;
        this.hoverRow = row;
        canvas.style.cursor = row?.refTarget ? 'pointer' : node ? 'pointer' : 'grab';
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
