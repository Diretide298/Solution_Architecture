// Diagram of *boxes* rather than dots — used by the ER view (entities with
// their fields) and the Data view (tables with their columns). Boxes carry
// rows, so collision has to work on rectangles.
//
// **There is no simulation.** Boxes are placed in a hierarchy — a table sits
// below the tables it references — so the diagram opens as something you can
// read top to bottom, and then nothing moves it but a hand.
//
// There was one, and it was the whole problem. Repulsion, springs, gravity
// toward the origin and two collision passes ran under a decaying alpha, and
// **every interaction re-heated them**: `mousedown` on a box re-heated by 0.25,
// so *clicking a table to read it* set the entire diagram drifting for a second
// and a half and left it somewhere else. A reader who had spent a minute
// learning the shape of a schema lost it by pointing at one table.
//
// Pinning the dropped box was tried first and is not enough. It fixes the box
// you touched and leaves every other box on the canvas free to wander, which is
// the same complaint one box smaller: the structure is the thing being read,
// and a structure that rearranges itself when you look at it cannot be read at
// all.
//
// So the arrangement is deterministic and it is final. `relayout()` computes it
// and records where it put each box; a drag moves one box and nothing else; a
// double-click puts that box back where the layout had it; re-picking the scope
// lays the whole thing out again. The only loop left is the pulse that animates
// a hovered box's edges, which moves nothing.

import { enableTouch } from './touch.js';
import { hue, alpha } from './core.js';

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

/**
 * The relationship, walked from the parent to the child.
 *
 * An edge is stored as `(child, parent)` — the child is the row holding the key,
 * which is why it is the source and why the arrowhead points the other way. A
 * parent row exists first and the child hangs off it, though, so that is the
 * direction worth walking the eye in, and a *positive* `lineDashOffset` walks
 * the dash pattern back along the path, which is exactly that direction.
 *
 * A pulse rather than a dash because on this diagram a dashed line already means
 * something — inferred from a column name rather than declared in
 * relationships.csv. Dashing everything would erase that. So the edge is drawn
 * exactly as it was and a short segment of accent is stroked over it.
 */
const PULSE = 18;        // px of accent
const PULSE_GAP = 190;   // px from one pulse to the next, along the curve
const PULSE_SPEED = 2.2; // px per frame

/** Asked for stillness. Read per frame, so the answer follows the setting. */
const stillWanted = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

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

    this._drag = null;
    this._pan = null;
    this._raf = null;
    // The pulse runs on its own loop. The simulation's stops when the layout
    // settles, and borrowing it would hold `onSettle` — which the auto-fit waits
    // on — for as long as a pointer rested on a box.
    this._flowing = false;
    this._flowPhase = 0;
    this._flowRaf = null;

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
        // A box the reader dropped somewhere is pinned there, and the pin
        // survives a live reload of the same scope for exactly the reason the
        // position does — it is the reader's arrangement, not ours.
        fx: keepPositions ? old.fx : undefined,
        fy: keepPositions ? old.fy : undefined,
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
    // The layout is the answer, so there is nothing to converge on. `onSettle`
    // still has to fire — the auto-fit waits on it — so it fires on the next
    // frame, which is when the first draw has happened and the extent it wants
    // to fit is real.
    this._settle();
  }

  /**
   * Places the boxes in layers: a box sits below everything it points at, so
   * the most-referenced things — the tables the rest of the schema hangs off —
   * end up along the top. Deterministic, so the same data always draws the
   * same picture.
   *
   * This is the reset, so it also drops every hand-placed box: a tidy layout
   * that half its boxes were still nailed out of is not the tidy layout.
   *
   * @param {{keep?: boolean}} [opts]  `keep` holds the boxes the reader moved
   *   where they left them. Used when a box is folded open and the rows have to
   *   re-flow around its new height — re-flowing is expected there, throwing
   *   away somebody's arrangement is not.
   */
  relayout({ keep = false } = {}) {
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
      delete node._bary;
      // Where the layout put it. Kept on the node so a double-click can put it
      // back — with no simulation to hand a box to, "release" has to mean
      // something, and the only meaningful thing it can mean is *here*.
      node.lx = node.x;
      node.ly = node.y;
      if (keep && node.fx != null) {
        node.x = node.fx;
        node.y = node.fy;
      } else {
        node.fx = undefined;
        node.fy = undefined;
      }
    }
    this.draw();
  }

  /**
   * Put a hand-placed box — or, with no argument, all of them — back where the
   * layout had it. Double-click is the gesture.
   *
   * It snaps rather than animating. An animation here would be a box moving on
   * its own, which is the thing this file no longer does, and the reader asked
   * for it this time so there is nothing to soften.
   */
  unpin(node) {
    let any = false;
    for (const n of node ? [node] : this.nodes) {
      if (n.fx == null) continue;
      n.fx = undefined;
      n.fy = undefined;
      if (n.lx != null) { n.x = n.lx; n.y = n.ly; }
      any = true;
    }
    if (any) {
      this.userAdjusted = true;
      this.draw();
    }
    return any;
  }

  /** How many boxes the reader has placed by hand. Read by the harness. */
  pinnedCount() {
    return this.nodes.reduce((n, node) => n + (node.fx == null ? 0 : 1), 0);
  }

  /** Draw, then tell whoever is waiting that the picture is final. */
  _settle() {
    cancelAnimationFrame(this._raf);
    this._raf = requestAnimationFrame(() => {
      this._raf = null;
      this.draw();
      this.onSettle?.();
    });
  }

  /**
   * Kept because callers outside this file say it, and because a name that
   * still exists and does nothing is easier to find than one that was deleted
   * from under them. There is no field to heat.
   */
  reheat() {
    this._settle();
  }

  /**
   * Redraw while a box is hovered, so the pulse has frames to move in. Draws
   * nothing itself while the simulation is already drawing, and stops the moment
   * the pointer leaves the box — a diagram nobody is pointing at costs nothing.
   */
  _flowRun() {
    if (this._flowRaf || stillWanted()) return;
    const step = () => {
      if (!this._flowing) {
        this._flowRaf = null;
        this._flowPhase = 0;
        this.draw();
        return;
      }
      this._flowPhase = (this._flowPhase + PULSE_SPEED) % PULSE_GAP;
      this.draw();
      this._flowRaf = requestAnimationFrame(step);
    };
    this._flowRaf = requestAnimationFrame(step);
  }

  // ── no simulation ───────────────────────────────────────────────
  // What used to be here: an O(n²) repulsion pass, a spring pass over the
  // edges, gravity toward the origin, a velocity integrator and two rectangle
  // collision passes, all under a decaying alpha that every interaction
  // re-heated. Thirty-odd tables' worth of that ran on every click.
  //
  // The layered placement in `relayout()` already puts the boxes where they
  // belong and leaves no overlaps to resolve, so all of it was work spent
  // undoing a good arrangement. A drag repaints; nothing else moves.

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
    // the pin is on the box, so it moves with it rather than snapping the box
    // back to where its header used to be halfway through the next frame
    if (node.fx != null) node.fy = node.y;
    this.userAdjusted = true;
    this.relayout({ keep: true });
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
    const panel = styles.getPropertyValue('--node-fill').trim() || '#1b2360';
    const border = styles.getPropertyValue('--border').trim() || '#2c2c36';
    const accent = styles.getPropertyValue('--accent').trim() || hue('accent');
    const light = document.documentElement.dataset.theme !== 'dark';

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
          ? accent
          : (light ? 'rgba(0,0,0,.42)' : 'rgba(255,255,255,.46)');

      // a child edge is the strongest statement on the diagram — this row
      // belongs to that row — so it is drawn heaviest
      const weight = edge.kind === 'child' ? 2.4 : 1.5;
      ctx.lineWidth = (active ? 2.8 : muted ? 1 : weight) * Math.min(1.6, Math.max(0.55, k));
      if (active) {
        ctx.shadowColor = alpha(accent, .45);
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

      // The pulse, parent to child, on the edges of the box under the pointer.
      // A second pass over the path that is still current, so the line beneath
      // keeps its own weight, colour and — the one that matters — whether it is
      // dashed, which here means inferred rather than declared.
      if (active && this._flowing && !stillWanted()) {
        ctx.save();
        ctx.setLineDash([PULSE * Math.min(1.5, k), (PULSE_GAP - PULSE) * Math.min(1.5, k)]);
        ctx.lineDashOffset = this._flowPhase * Math.min(1.5, k);
        ctx.strokeStyle = accent;
        ctx.lineWidth = 3 * Math.min(1.6, Math.max(0.55, k));
        ctx.lineCap = 'round';
        ctx.stroke();
        ctx.restore();
        ctx.setLineDash([]);
      }

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
            ctx.strokeStyle = alpha(accent, .5);
            ctx.lineWidth = 1;
            ctx.strokeRect(midX - metrics.width / 2 - 4, midY - 8, metrics.width + 8, 16);
          }
          ctx.fillStyle = active ? accent : faint;
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
      // A box the reader nailed down. Said with the border, which is the one
      // thing on this box already carrying "how much does this matter to you"
      // — selected is heaviest, a neighbour of it next, this next, the rest
      // hairline. No new colour and no badge: it is a state of the reader's
      // arrangement, not a fact about the schema.
      const pinned = node.fx != null;
      ctx.globalAlpha = faded ? 0.18 : 1;

      // body
      ctx.beginPath();
      ctx.roundRect(left, top, w, h, 6 * Math.min(1.5, k));
      ctx.fillStyle = panel;
      ctx.fill();
      if (selected || neighbour) {
        ctx.shadowColor = selected
          ? alpha(accent, .5)
          : alpha(accent, .22);
        ctx.shadowBlur = selected ? 18 : 9;
        ctx.fill();
        ctx.shadowBlur = 0;
      }
      ctx.lineWidth = selected ? 2.6 : neighbour ? 1.8 : pinned ? 1.6 : 1;
      ctx.strokeStyle = selected
        ? accent
        : neighbour
          ? alpha(accent, .55)
          : pinned
            ? dim
            : border;
      ctx.stroke();

      // A caption above the box, not inside it.
      //
      // The header band is already carrying the table name and a badge, and a
      // third thing in it would crowd the name — which is the one word a
      // reader is scanning for. Above the box there is empty gutter, and a
      // caption there reads as a label on the box rather than as content.
      // Shown from the zoom where the table name is legible, not higher. A
      // label that appears only when you are already zoomed in on one box
      // cannot answer "which of these is a parent", which is the question.
      if (node.caption && k > 0.3) {
        // Sized off the same floor as the title, so it stays legible when the
        // whole schema is fitted — which is the zoom this question gets asked
        // at. Offset from the actual font size rather than from k, or at low
        // zoom the label would sit on top of the box it labels.
        const capSize = textSize(8, k, 6);
        ctx.font = `600 ${capSize}px ui-sans-serif, system-ui, sans-serif`;
        ctx.fillStyle = node.captionColor ?? faint;
        ctx.textAlign = 'left';
        ctx.fillText(node.caption.toUpperCase(), left + 1 * k, top - capSize * 0.62);
      }

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
        // No re-heat. This line was `this.reheat(0.25)`, and it is the whole
        // bug: pressing on a table to read it set every box on the canvas
        // moving.
        this._drag = { node, moved: false, sx: e.offsetX, sy: e.offsetY };
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
        // Both axes. This asked about x alone, so a box dragged straight up or
        // down was released as an unmoved *click* — it selected the box and,
        // worse, never counted as an arrangement worth keeping.
        if (Math.abs(e.clientX - rect.left - this._drag.sx) > 3 ||
            Math.abs(e.clientY - rect.top - this._drag.sy) > 3) this._drag.moved = true;
        this.draw();
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
      } else if (this._drag) {
        // Dropped. Pin it here — see the note at the top of the file for what
        // happened when it was simply handed back.
        // Dropped. `fx`/`fy` is now a record of "a hand put this here", not a
        // pin against a field — there is no field. It survives a fold, and a
        // double-click reads it to know there is something to undo.
        const node = this._drag.node;
        node.fx = node.x;
        node.fy = node.y;
        this.userAdjusted = true;
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
        // A box under the pointer is the question the pulse answers, so it runs
        // while there is one and stops when there is not.
        this._flowing = Boolean(node);
        if (this._flowing) this._flowRun();
        this.draw();
      }
    });

    // Double-click a box somebody moved to put it back where the layout had
    // it. The conventional gesture, and — short of re-picking the scope — the
    // only way back. On a box nobody moved it does nothing, so the single-click
    // behaviour above is untouched for every box on a fresh diagram.
    canvas.addEventListener('dblclick', (e) => {
      const node = this.nodeAt(e.offsetX, e.offsetY);
      if (node) this.unpin(node);
    });

    canvas.addEventListener('mouseleave', () => {
      this.hover = null;
      this.hoverRow = null;
      // The loop clears the phase and repaints on its way out, so the last frame
      // is the diagram at rest rather than a pulse frozen mid-curve.
      this._flowing = false;
      if (!this._flowRaf) this.draw();
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
    cancelAnimationFrame(this._flowRaf);
    this._flowing = false;
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
