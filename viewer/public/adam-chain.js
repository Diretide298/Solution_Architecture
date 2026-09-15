/* The derivation chain, drawn in the viewer's own diagram language.
 *
 * Lifted from how Adam already draws itself, so a stage on the landing page and
 * the view it stands for read the same way:
 *
 *   viewer/public/boxdiagram.js  entities as boxes with a header and rows, laid
 *                               out in a hierarchy — a table sits below the one
 *                               it references — and nothing moves but a hand
 *   viewer/public/statemachine.js  direction carries meaning: solid where an
 *                               operation causes it, dashed where a timer or a
 *                               job does, amber for a reversal
 *   viewer/public/styles.css    the palette, named for what it is in the
 *                               drawing: node-fill, card-head, border, accent,
 *                               accent-soft, warm-fill, amber, red, enum
 *
 * The one loop is the pulse that walks an edge — the same PULSE/PULSE_GAP idea
 * as the ER view, on the hero animation's clock.
 *
 *   const scene = window.AdamChain.mount(canvas, { accent });
 *   scene.setStep(4);
 */
(function () {
  const W = 352, H = 198;

  // viewer/public/styles.css, day theme
  const C = {
    node: '#ffffff', head: '#edf3f6', raised: '#f8fbfc',
    border: '#dfe8ec', strong: '#c7d5db', divider: '#edf3f6',
    text: '#1d2c33', dim: '#5d7079', faint: '#7a8c94',
    accent: '#0078a0', bright: '#00b4e0', soft: '#e3f5fb', line: '#9cd9ec',
    warmFill: '#fbf6ec', warmLine: '#eadfc8', warmText: '#7a6534',
    amber: '#c08a2e', red: '#c0564f', enum: '#7c5fc0', grid: '#dbe6eb',
  };

  // rAF stops in a preview the visibility API calls hidden, and a page mounted
  // while visible would then freeze for good. So each frame races rAF against a
  // 34ms timer and whichever arrives first drives the next one.
  function sched(fn) {
    var done = false;
    var h = {};
    h.t = setTimeout(function () {
      if (done) return; done = true; cancelAnimationFrame(h.r); fn(performance.now());
    }, 34);
    h.r = requestAnimationFrame(function (ts) {
      if (done) return; done = true; clearTimeout(h.t); fn(ts);
    });
    return h;
  }
  function unsched(h) {
    if (!h) return;
    clearTimeout(h.t); cancelAnimationFrame(h.r);
  }

  function Chain(canvas, opts) {
    this.c = canvas;
    this.ctx = canvas.getContext('2d');
    this.pulse = (opts && opts.accent) || C.bright;
    this.fps = (opts && opts.fps) || 6;
    this.step = 1;
  }

  Chain.prototype.size = function () {
    const r = this.c.getBoundingClientRect();
    if (!r.width) return;
    const S = Math.min(3, Math.max(1, (r.width / W) * Math.min(2, window.devicePixelRatio || 1)));
    const bw = Math.round(W * S), bh = Math.round(H * S);
    if (this.c.width !== bw || this.c.height !== bh) { this.c.width = bw; this.c.height = bh; }
    this.ctx.setTransform(S, 0, 0, S, 0, 0);
  };

  Chain.prototype.setStep = function (n) { this.step = n; };
  Chain.prototype.mount = function () {
    const self = this;
    this.size();
    if (window.ResizeObserver) {
      this._ro = new ResizeObserver(function () { self.size(); });
      this._ro.observe(this.c);
    }
    const until = function () { self.size(); if (!self.c.width) sched(until); };
    until();
    const loop = function (now) {
      self._raf = sched(loop);
      if (!self.c.isConnected) return;
      const r = self.c.getBoundingClientRect();
      if (r.bottom < -120 || r.top > window.innerHeight + 120) return;
      self.paint(now);
    };
    this._raf = sched(loop);
    return this;
  };
  Chain.prototype.stop = function () {
    unsched(this._raf);
    if (this._ro) this._ro.disconnect();
  };

  Chain.prototype.paint = function (now) {
    const ctx = this.ctx;
    if (!this.c.width) return;
    const t = now / 1000;
    const k = Math.floor(t * this.fps);
    const P = this.pulse;

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = C.node; ctx.fillRect(0, 0, W, H);
    ctx.lineWidth = 1;

    const mono = function (s, wt) { return (wt || 400) + ' ' + s + "px 'JetBrains Mono', ui-monospace, monospace"; };
    const label = function (txt, x, y, size, col, wt, spread) {
      ctx.save();
      ctx.fillStyle = col; ctx.textBaseline = 'top'; ctx.textAlign = 'left';
      ctx.font = mono(size || 8, wt);
      if (spread) {
        let cx = x;
        const s = String(txt);
        for (let i = 0; i < s.length; i++) { ctx.fillText(s[i], cx, y); cx += size * 0.62 + spread; }
      } else ctx.fillText(String(txt), x, y);
      ctx.restore();
    };
    const rect = function (x, y, w, h, fill, stroke, r) {
      const rr = r == null ? 3 : r;
      ctx.beginPath();
      ctx.moveTo(x + rr, y); ctx.lineTo(x + w - rr, y); ctx.quadraticCurveTo(x + w, y, x + w, y + rr);
      ctx.lineTo(x + w, y + h - rr); ctx.quadraticCurveTo(x + w, y + h, x + w - rr, y + h);
      ctx.lineTo(x + rr, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - rr);
      ctx.lineTo(x, y + rr); ctx.quadraticCurveTo(x, y, x + rr, y);
      ctx.closePath();
      if (fill) { ctx.fillStyle = fill; ctx.fill(); }
      if (stroke) { ctx.strokeStyle = stroke; ctx.stroke(); }
    };

    // An entity: header strip with its name, then one row per field — the ER
    // view's box, at a third of its size.
    const HEAD = 15, ROW = 12;
    const box = function (x, y, w, title, rows, o) {
      const opt = o || {};
      const h = HEAD + (rows ? rows.length : 0) * ROW + 5;
      rect(x, y, w, h, C.node, opt.tone || C.border);
      if (opt.tone) { ctx.save(); ctx.strokeStyle = opt.tone; ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1); ctx.restore(); }
      ctx.save();
      ctx.beginPath(); ctx.rect(x + 1, y + 1, w - 2, HEAD - 1); ctx.clip();
      ctx.fillStyle = opt.headFill || C.head; ctx.fillRect(x, y, w, HEAD);
      ctx.restore();
      ctx.strokeStyle = C.border; ctx.beginPath();
      ctx.moveTo(x, y + HEAD); ctx.lineTo(x + w, y + HEAD); ctx.stroke();
      label(title, x + 6, y + 4.5, 7.5, opt.titleCol || C.text, 700);
      for (let i = 0; i < (rows ? rows.length : 0); i++) {
        const r = rows[i];
        const isObj = r && typeof r === 'object';
        const txt = isObj ? r.t : r;
        const on = isObj && r.on;
        ctx.fillStyle = on ? P : C.strong;
        ctx.beginPath(); ctx.arc(x + 8, y + HEAD + 8 + i * ROW, on ? 2.2 : 1.6, 0, Math.PI * 2); ctx.fill();
        label(txt, x + 14, y + HEAD + 4.5 + i * ROW, 7, on ? C.text : C.dim, on ? 600 : 400);
      }
      return { x: x, y: y, w: w, h: h, cx: x + w / 2, cy: y + h / 2, r: x + w, b: y + h };
    };

    // An edge, walked parent → child. Solid where something declares it,
    // dashed where it is inferred; one short pulse of accent walks it.
    const edge = function (a, b, o) {
      const opt = o || {};
      const x0 = opt.from === 'b' ? a.cx : a.r, y0 = opt.from === 'b' ? a.b : a.cy;
      const x1 = opt.to === 't' ? b.cx : b.x, y1 = opt.to === 't' ? b.y : b.cy;
      const mx = (x0 + x1) / 2;
      const at = function (u) {
        const iu = 1 - u;
        return opt.to === 't' || opt.from === 'b'
          ? { x: iu * iu * x0 + 2 * iu * u * x0 + u * u * x1, y: iu * iu * y0 + 2 * iu * u * y1 + u * u * y1 }
          : { x: iu * iu * iu * x0 + 3 * iu * iu * u * mx + 3 * iu * u * u * mx + u * u * u * x1,
              y: iu * iu * iu * y0 + 3 * iu * iu * u * y0 + 3 * iu * u * u * y1 + u * u * u * y1 };
      };
      ctx.save();
      ctx.strokeStyle = opt.tone || C.line;
      ctx.lineWidth = 1;
      if (opt.dashed) ctx.setLineDash([3, 3]);
      ctx.beginPath();
      for (let i = 0; i <= 24; i++) { const p = at(i / 24); i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y); }
      ctx.stroke();
      ctx.setLineDash([]);
      // arrowhead
      const e = at(1), n = at(0.94);
      const ang = Math.atan2(e.y - n.y, e.x - n.x);
      ctx.fillStyle = opt.tone || C.line;
      ctx.beginPath();
      ctx.moveTo(e.x, e.y);
      ctx.lineTo(e.x - Math.cos(ang - 0.5) * 5, e.y - Math.sin(ang - 0.5) * 5);
      ctx.lineTo(e.x - Math.cos(ang + 0.5) * 5, e.y - Math.sin(ang + 0.5) * 5);
      ctx.closePath(); ctx.fill();
      // the pulse
      if (!opt.still) {
        const u0 = ((t * 0.42) + (opt.seed || 0)) % 1.35;
        if (u0 <= 1) {
          ctx.strokeStyle = P; ctx.lineWidth = 1.6;
          ctx.beginPath();
          for (let i = 0; i <= 6; i++) {
            const u = Math.max(0, Math.min(1, u0 - 0.055 + (i / 6) * 0.055));
            const p = at(u); i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y);
          }
          ctx.stroke();
        }
      }
      ctx.restore();
    };

    const tag = function (x, y, txt, tone) {
      ctx.save();
      ctx.font = mono(7, 600);
      const w = ctx.measureText(String(txt).toUpperCase()).width + 12;
      const fill = tone === 'accent' ? C.soft : tone === 'warm' ? C.warmFill : C.raised;
      const line = tone === 'accent' ? C.line : tone === 'warm' ? C.warmLine : C.border;
      const col = tone === 'accent' ? C.accent : tone === 'warm' ? C.warmText : C.dim;
      rect(x, y, w, 14, fill, line, 7);
      ctx.fillStyle = col; ctx.textBaseline = 'top'; ctx.textAlign = 'left';
      ctx.fillText(String(txt).toUpperCase(), x + 6, y + 3.5);
      ctx.restore();
      return x + w;
    };

    const metric = function (x, y, w, value, caption) {
      rect(x, y, w, 40, C.raised, C.border);
      label(value, x + 8, y + 7, 15, C.accent, 700);
      label(caption, x + 8, y + 26, 6.5, C.faint, 600, 0.8);
    };

    const cells = function (x, y, cols, rows, lit, cw, ch) {
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const i = r * cols + c;
          const on = typeof lit === 'function' ? lit(i) : i < lit;
          rect(x + c * (cw + 3), y + r * (ch + 3), cw, ch, on ? C.soft : C.raised, on ? C.line : C.border, 2);
        }
      }
    };

    const bars = function (x, y, vals, cw, maxh, hot) {
      for (let i = 0; i < vals.length; i++) {
        const h = Math.max(1.5, vals[i] * maxh);
        rect(x + i * (cw + 4), y + maxh - h, cw, h, hot === i ? P : C.line, null, 1.5);
      }
      ctx.strokeStyle = C.border; ctx.beginPath();
      ctx.moveTo(x, y + maxh + 1.5); ctx.lineTo(x + vals.length * (cw + 4) - 4, y + maxh + 1.5); ctx.stroke();
    };

    const head = function (txt) { label(txt, 12, 11, 7, C.faint, 700, 1.1); };
    const S = this.step;

    if (S === 1) {
      head('OPERATION → WHAT IT TOUCHES');
      const op = box(12, 32, 132, 'listOrders', [
        { t: 'service · order', on: k % 3 === 0 },
        { t: 'audience · staff' },
        { t: 'stores · postgres', on: k % 3 === 2 },
      ]);
      const reads = box(214, 30, 126, 'reads', ['orders.order', 'orders.line_item', 'catalogue.product']);
      const writes = box(214, 122, 126, 'writes', ['orders.audit_entry']);
      edge(op, reads, { seed: 0 });
      edge(op, writes, { seed: 0.45 });
      tag(12, 118, '1,628 operations');
      tag(12, 140, 'read as authoritative', 'accent');
      label('handoff/api-data-lineage.json', 12, 168, 7, C.faint);
    } else if (S === 2) {
      head('SCHEMA → COLUMNS');
      const sch = box(12, 30, 146, 'access.Ticket', [
        'ticketId · string', 'isValid · boolean', 'entriesUsed · integer',
      ], { tone: C.border });
      const tbl = box(206, 30, 134, 'access.entitlement', [
        { t: 'ticket_id', on: k % 4 > 0 },
        { t: 'is_valid', on: k % 4 > 1 },
        { t: 'entries_used', on: k % 4 > 2 },
      ], { tone: C.line });
      edge(sch, tbl, { seed: 0.1 });
      tag(12, 112, 'x-ticvai-persistence', 'accent');
      tag(12, 134, 'nothing here is typed by hand');
      label('handoff/schema-reference.json', 12, 168, 7, C.faint);
    } else if (S === 3) {
      head('EVERY EDGE, STRONGEST FIRST');
      const parent = box(12, 34, 128, 'orders.order', ['id · uuid', 'org_unit_id · uuid']);
      const child = box(200, 34, 140, 'orders.payment', ['order_id → order', 'amount_minor']);
      const inferred = box(200, 118, 140, 'marketing.touch', ['order_id · uuid']);
      edge(parent, child, { seed: 0 });
      edge(parent, inferred, { dashed: true, tone: C.strong, seed: 0.5 });
      tag(12, 108, 'references · 52', 'accent');
      tag(12, 130, 'declared in a contract');
      tag(12, 152, 'inferred from a name');
    } else if (S === 4) {
      head('MIGRATIONS AS THEY STAND');
      const files = ['V0001 · schemas', 'V0002 · identity', 'V0003a · platform', 'V0004 · orders'];
      for (let i = 0; i < files.length; i++) {
        const on = i === k % 4;
        rect(12, 32 + i * 22, 168, 18, on ? C.soft : C.raised, on ? C.line : C.border);
        label(files[i], 20, 37 + i * 22, 7.5, on ? C.text : C.dim, on ? 600 : 400);
      }
      const tables = box(206, 32, 134, 'tables created', [
        { t: 'platform.org_unit', on: true },
        { t: 'orders.payment', on: true },
        { t: 'finance.ledger' },
        { t: 'ai.index_entry' },
      ]);
      void tables;
      metric(206, 132, 64, '39', 'WRITTEN');
      metric(276, 132, 64, '224', 'DERIVED');
      label('backend/**/*.sql', 12, 168, 7, C.faint);
    } else if (S === 5) {
      head('WHAT A SALE ACTUALLY RUNS');
      const flows = box(12, 30, 116, 'flows walked', [
        { t: 'F43 · concurrency', on: k % 3 === 0 },
        { t: 'F58 · till sale', on: k % 3 === 1 },
        { t: 'F59 · seat held', on: k % 3 === 2 },
      ]);
      const svc = box(190, 30, 150, 'services on the path', [
        { t: 'catalogue · 64%', on: true },
        { t: 'order · 22%', on: true },
        { t: 'access · 7%' },
        { t: 'finance · 4%' },
        { t: 'inventory · deployed: false' },
      ]);
      edge(flows, svc, { seed: 0.2 });
      tag(12, 112, 'weighted by calls per buyer', 'accent');
      tag(12, 134, '2 of 7 carry 86%', 'warm');
      label('handoff/burst-scope.json', 12, 168, 7, C.faint);
    } else if (S === 6) {
      head('TWO LOADS, TWO MIXES');
      rect(12, 28, 156, 84, C.raised, C.border);
      label('NORMAL', 20, 34, 7, C.dim, 700, 1);
      bars(22, 50, [0.4, 0.55, 0.3, 0.48, 0.34, 0.26], 16, 52, -1);
      rect(184, 28, 156, 84, C.raised, C.border);
      label('SALE', 192, 34, 7, C.accent, 700, 1);
      bars(194, 50, [0.3, 0.95, 0.18, 0.66, 0.12, 0.08], 16, 52, 1);
      rect(12, 122, 328, 44, C.node, C.border);
      label('REPLICAS PROVISIONED', 20, 128, 7, C.faint, 700, 1);
      cells(20, 142, 16, 1, function (i) { return i < 5 + (k % 4); }, 17, 14);
      label('handoff/sizing.json', 12, 176, 7, C.faint);
    } else if (S === 7) {
      head('WHAT A TABLE HOLDS');
      const tbl = box(12, 30, 150, 'platform.org_unit', [
        'id · uuid', 'level · enum', 'parent_id · uuid', 'venue_id · uuid',
      ], { tone: C.line });
      const note = box(196, 30, 144, 'note', [
        { t: 'what it holds' }, { t: 'what it hangs off' }, { t: 'what reaches it' },
      ], { headFill: C.warmFill, titleCol: C.warmText, tone: C.warmLine });
      edge(tbl, note, { seed: 0.3, tone: C.warmLine });
      metric(196, 118, 68, '165', 'HAD A NOTE');
      metric(272, 118, 68, '368', 'TABLES');
      tag(12, 128, 'most-referenced had none', 'warm');
    } else if (S === 8) {
      head('THE TABLE A SCHEMA IS ABOUT');
      const root = box(104, 26, 146, 'access.entitlement', ['root of the schema'],
        { tone: C.accent, headFill: C.soft, titleCol: C.accent });
      const kids = [
        box(12, 112, 100, 'access_point', ['entitlement_id']),
        box(126, 112, 100, 'redemption', ['entitlement_id']),
        box(240, 112, 100, 'transfer', ['entitlement_id']),
      ];
      for (let i = 0; i < kids.length; i++) {
        edge(root, kids[i], { from: 'b', to: 't', seed: i * 0.3 });
      }
      tag(12, 172, 'a gate is equipment', 'warm');
      tag(150, 172, 'the thing admitted is the point', 'accent');
    } else if (S === 9) {
      head('SCREENS → APP MANIFEST');
      rect(12, 28, 150, 96, C.raised, C.border);
      label('SCREENS/P04.YAML', 20, 34, 7, C.dim, 700, 1);
      cells(20, 48, 7, 4, function (i) { return i === k % 28; }, 17, 15);
      const app = box(206, 28, 134, 'frontend/pos.yaml', [
        { t: 'platforms · P04 P08', on: k % 4 === 0 },
        { t: 'contracts · 6', on: k % 4 === 1 },
        { t: 'packages · offline', on: k % 4 === 2 },
        { t: 'route collisions · 0', on: k % 4 === 3 },
      ]);
      const src = { x: 12, y: 28, w: 150, h: 96, cx: 87, cy: 76, r: 162, b: 124 };
      edge(src, app, { seed: 0.15 });
      label('do not hand-edit — derived from the screens', 12, 172, 7, C.faint);
    } else if (S === 10) {
      head('A PANEL IS NOT AN ENDPOINT');
      const panels = [
        box(12, 26, 132, 'getKitchenLoad', ['aggregate']),
        box(12, 84, 132, 'getKitchenSla', ['aggregate']),
        box(12, 142, 132, 'listKitchenExceptions', ['filter']),
      ];
      const op = box(204, 76, 136, 'listKitchenTickets', ['one operation', 'filter + aggregate'],
        { tone: C.accent, headFill: C.soft, titleCol: C.accent });
      for (let i = 0; i < panels.length; i++) edge(panels[i], op, { seed: i * 0.3 });
      tag(204, 150, '86 of 210 are reads', 'accent');
    } else if (S === 11) {
      head('HLD · FIVE TIERS, WRITES BETWEEN THEM');
      const tiers = ['edge', 'spine', 'satellite', 'shared', 'store'];
      const tones = [C.line, C.accent, C.bright, C.amber, C.strong];
      const boxes = [];
      for (let i = 0; i < 5; i++) {
        const on = i === k % 5;
        boxes.push(box(12 + i * 68, 40, 60, tiers[i], [{ t: i === 3 ? 'amber' : 'svc', on: on }],
          { tone: on ? tones[i] : C.border, headFill: on ? C.soft : C.head }));
      }
      for (let i = 0; i < 4; i++) edge(boxes[i], boxes[i + 1], { seed: i * 0.22, tone: tones[i] });
      label('LLD · 16 SERVICES', 12, 108, 7, C.faint, 700, 1);
      cells(12, 122, 16, 1, function (i) { return i < 8 + (k % 8); }, 18, 16);
      tag(12, 152, 'derived, never authored', 'accent');
      tag(170, 152, 'a stale diagram fails nothing', 'warm');
    } else if (S === 12) {
      head('THE REASONING IS THE DELIVERABLE');
      const sheets = ['schema reference', 'services + segregation'];
      for (let s = 0; s < 2; s++) {
        const x = 12 + s * 172;
        rect(x, 28, 156, 116, C.node, C.border);
        rect(x, 28, 156, 16, C.head, C.border);
        label(sheets[s], x + 6, 32.5, 7, C.text, 700);
        for (let r = 0; r < 5; r++) {
          const filled = (k % 6) > r;
          for (let c = 0; c < 4; c++) {
            rect(x + 6 + c * 36, 50 + r * 18, 34, 16,
              filled ? (c === 3 ? C.soft : C.raised) : C.node, C.divider, 1.5);
          }
        }
      }
      tag(12, 154, '224 tables → 26 schemas → 16 services', 'accent');
    } else if (S === 13) {
      head('THE SCREEN IS THE SPECIFICATION');
      const spec = box(12, 30, 132, 'screens/P04.yaml', [
        { t: 'regions · 4', on: k % 3 === 0 },
        { t: 'components · 17', on: k % 3 === 1 },
        { t: 'states · 4', on: k % 3 === 2 },
      ]);
      const frame = { x: 196, y: 26, w: 144, h: 132, cx: 268, cy: 92, r: 340, b: 158 };
      rect(frame.x, frame.y, frame.w, frame.h, C.node, C.border);
      rect(frame.x, frame.y, frame.w, 14, C.head, C.border);
      label('POS-002 · BOARD', frame.x + 6, frame.y + 3.5, 7, C.dim, 700);
      const regions = [[6, 22, 62, 38], [74, 22, 62, 38], [6, 66, 130, 26], [6, 98, 92, 26]];
      for (let i = 0; i < regions.length; i++) {
        const r = regions[i], on = i === k % 4;
        rect(frame.x + r[0], frame.y + r[1], r[2], r[3], on ? C.soft : C.raised, on ? C.line : C.border, 2);
      }
      edge(spec, frame, { seed: 0.2 });
      tag(12, 118, 'generated, not maintained', 'accent');
      tag(12, 140, '180 screens · 180 boards');
    } else if (S === 14) {
      head('A BOARD IS READ ONCE');
      // the boards themselves: a header bar and two rows each, one being read
      const names = ['P04 POS', 'P08 KIOSK', 'WEB GUEST', 'MARKETING 1', 'BO ADMIN', 'FNB 3A',
        'P11 GATE', 'FINANCE', 'WS 07'];
      const lit = k % names.length;
      let litBox = null;
      for (let i = 0; i < names.length; i++) {
        const col = i % 3, row = (i / 3) | 0;
        const x = 12 + col * 56, y = 28 + row * 40;
        const on = i === lit;
        rect(x, y, 52, 34, on ? C.soft : C.raised, on ? C.line : C.border, 2);
        rect(x, y, 52, 11, on ? C.node : C.head, on ? C.line : C.border, 2);
        label(names[i], x + 3, y + 2.5, 5.6, on ? C.accent : C.dim, 700);
        for (let r = 0; r < 2; r++) {
          rect(x + 4, y + 16 + r * 7, (r ? 30 : 42) - (i % 3) * 3, 3.5, on ? C.line : C.grid, null, 1.5);
        }
        if (on) litBox = { x: x, y: y, w: 52, h: 34, cx: x + 26, cy: y + 17, r: x + 52, b: y + 34 };
      }
      const rec = box(196, 40, 144, 'board-index.json', [
        { t: 'sha256 · 9f3c1a…', on: true },
        { t: 'anchors · 304' },
        { t: 'frames · 12' },
        { t: 'unchanged → not re-read' },
      ], { tone: C.line });
      if (litBox) edge(litBox, rec, { seed: 0.2 });
      tag(196, 128, '165 boards, read once', 'accent');
      tag(196, 150, '141 of 170 were gone', 'warm');
      label('a number that is expensive to derive gets derived carelessly', 12, 176, 6.5, C.faint);
    } else if (S === 15) {
      head('A NUMBER HERE IS SPENT');
      const reg = box(12, 28, 160, 'screen-ids · issued', [
        { t: 'ADM-036', on: true }, { t: 'ADM-037', on: true },
        { t: 'ADM-038', on: true }, { t: 'ADM-039' },
      ]);
      const a = box(214, 26, 126, 'workstream A', ['ADM-038 · dead letters'],
        { tone: C.accent, headFill: C.soft, titleCol: C.accent });
      const b = box(214, 100, 126, 'workstream B', ['ADM-038 · refused'],
        { tone: C.red, headFill: C.warmFill, titleCol: C.red });
      edge(reg, a, { seed: 0.1 });
      edge(reg, b, { seed: 0.5, tone: C.red, dashed: true });
      tag(12, 140, 'both computed max + 1', 'warm');
      tag(12, 162, 'neither could see the other');
    }
  };

  window.AdamChain = {
    mount: function (canvas, opts) { return new Chain(canvas, opts).mount(); },
  };
})();
