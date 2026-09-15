/* The seven stage drawings for the decision pipeline (adam-journey.js).
 *
 *   window.AdamJourneyStages.build(n, art, ctx) → { update(p, live), emit, head? }
 *
 * `art` is the card's illustration band less the signal corridor. `update` is
 * a pure function of the stage's own progress p (0 = not yet run, 1 = run), so
 * p = 0 is the idle picture at ghost opacity and p = 1 is the resting record.
 * `emit` is where the stage hands its record to the artefact path below.
 * `head`, when present, steers the signal through the card instead of the
 * default glide — 05 splits it, 06 holds it.
 *
 * Nothing here moves a card. Parts draw (stroke-dashoffset), fade (opacity)
 * and settle (translate) inside their band.
 */
(function () {
  'use strict';

  var MONO = "'JetBrains Mono', ui-monospace, monospace";

  function kit(ctx) {
    var S = ctx.S, g = ctx.g, C = ctx.C, G = ctx.GHOST;
    var k = {
      fade: function (el, w) { el.setAttribute('opacity', (G + (1 - G) * w).toFixed(3)); },
      // a ghost that is always there, and a live copy drawn over it
      line: function (d, attrs, parent) {
        var a = Object.assign({ d: d, fill: 'none', stroke: C.deep, 'stroke-width': 1 }, attrs || {});
        var ghost = S('path', Object.assign({}, a, { opacity: G, stroke: C.ink }), parent || g);
        var live = S('path', a, parent || g);
        var len = Math.max(1, live.getTotalLength());
        live.setAttribute('stroke-dasharray', len + ' ' + len);
        return {
          ghost: ghost, live: live, len: len,
          draw: function (w) {
            live.setAttribute('stroke-dashoffset', (len * (1 - w)).toFixed(1));
            live.setAttribute('opacity', w > 0 ? 1 : 0);
          },
          at: function (q) { return live.getPointAtLength(len * Math.max(0, Math.min(1, q))); },
        };
      },
      rect: function (x, y, w, h, r, fill, stroke, parent) {
        return S('rect', { x: x, y: y, width: w, height: h, rx: r, fill: fill, stroke: stroke }, parent || g);
      },
      text: function (x, y, s, size, fill, parent, anchor) {
        var t = S('text', { x: x, y: y, 'font-family': MONO, 'font-size': size, 'font-weight': 500,
          fill: fill, 'dominant-baseline': 'middle', 'text-anchor': anchor || 'start' }, parent || g);
        t.textContent = s;
        return t;
      },
      dot: function (r, fill, parent) { return S('circle', { r: r, fill: fill, opacity: 0 }, parent || g); },
      place: function (el, pt, on) {
        el.setAttribute('cx', pt.x); el.setAttribute('cy', pt.y);
        el.setAttribute('opacity', on ? 1 : 0);
      },
      bars: function (x, y, w, n, gap, parent) {
        var out = [];
        for (var i = 0; i < n; i++) {
          var bw = w * (0.58 + ((i * 37) % 11) / 26);
          out.push(k.line('M' + x + ' ' + (y + i * gap) + ' h' + bw.toFixed(1),
            { stroke: C.ink, 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-opacity': 0.55 }, parent));
        }
        return out;
      },
    };
    return k;
  }

  var build = {};

  /* 01 — Requirement gathering: sources fan into one record, particles carry it */
  build[1] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win;
    var kinds = ['DOC', 'PDF', 'PNG', 'XLS'];
    var rx = b.x + b.w * 0.64, ry = b.y + 8, rw = 46, rh = b.h - 16;
    var hub = { x: rx - 10, y: b.cy };
    var chips = [], curves = [], parts = [];
    kinds.forEach(function (name, i) {
      var y = b.y + 10 + i * 26;
      var grp = S('g', {}, ctx.g);
      k.rect(b.x, y, 40, 16, 3, C.node, C.border, grp);
      k.text(b.x + 20, y + 8.5, name, 8, C.ink, grp, 'middle');
      chips.push(grp);
      var sx = b.x + 42, sy = y + 8;
      curves.push(k.line('M' + sx + ' ' + sy + ' Q' + ((sx + hub.x) / 2) + ' ' + sy + ' ' + hub.x + ' ' + hub.y,
        { stroke: C.deep, 'stroke-opacity': 0.55 }));
      parts.push(k.dot(2.3, A));
    });
    var page = k.rect(rx, ry, rw, rh, 4, C.node, C.line);
    var rows = k.bars(rx + 8, ry + 13, rw - 16, 7, Math.min(11, (rh - 22) / 7));
    var hubDot = S('circle', { cx: hub.x, cy: hub.y, r: 3.4, fill: C.deep }, ctx.g);
    return {
      emit: { x: rx + rw / 2, y: b.y + b.h - 3 },
      update: function (p, live) {
        chips.forEach(function (c, i) {
          var w = win(p, 0.05 + i * 0.05, 0.22 + i * 0.05);
          k.fade(c, w);
          c.setAttribute('transform', 'translate(' + (-4 * (1 - w)).toFixed(2) + ' 0)');
          curves[i].draw(win(p, 0.14 + i * 0.05, 0.42 + i * 0.05));
          var q = (p - 0.34 - i * 0.06) / 0.26;
          var on = live && q > 0 && q < 1;
          if (on) k.place(parts[i], curves[i].at(ctx.EASE(q)), true); else parts[i].setAttribute('opacity', 0);
        });
        k.fade(page, win(p, 0.1, 0.3));
        k.fade(hubDot, win(p, 0.3, 0.45));
        rows.forEach(function (r, j) { r.draw(win(p, 0.46 + j * 0.045, 0.56 + j * 0.045)); });
      },
    };
  };

  /* 02 — Workshops: nodes gather into a graph, one edge is recorded, it collapses */
  build[2] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win, lerp = ctx.lerp;
    var hub = { x: b.x + b.w * 0.58, y: b.cy };
    var ppl = S('g', {}, ctx.g);
    S('circle', { cx: b.x + 15, cy: b.cy, r: 13, fill: C.soft, stroke: C.line }, ppl);
    [[-4, -3, 3.3], [5, -1, 2.9], [0, 6, 4.4]].forEach(function (d) {
      S('circle', { cx: b.x + 15 + d[0], cy: b.cy + d[1], r: d[2], fill: C.deep }, ppl);
    });
    var talk = k.line('M' + (b.x + 29) + ' ' + b.cy + ' L' + hub.x + ' ' + hub.y, { stroke: C.deep, 'stroke-opacity': 0.5 });
    var spots = [[0.30, 0.06], [0.64, 0.0], [0.30, 0.74], [0.64, 0.80], [0.84, 0.38]];
    var notes = spots.map(function (s, i) {
      var nx = b.x + b.w * s[0], ny = b.y + b.h * s[1];
      var c = { x: nx + 17, y: ny + 8 };
      var edge = k.line('M' + c.x + ' ' + c.y + ' L' + hub.x + ' ' + hub.y, { stroke: C.deep, 'stroke-opacity': 0.45 });
      var grp = S('g', {}, ctx.g);
      var box = k.rect(nx, ny, 34, 16, 3, C.node, C.border, grp);
      S('path', { d: 'M' + (nx + 6) + ' ' + (ny + 6) + ' h20 M' + (nx + 6) + ' ' + (ny + 10.5) + ' h14',
        stroke: C.ink, 'stroke-opacity': 0.5, 'stroke-width': 1.4, 'stroke-linecap': 'round' }, grp);
      return { grp: grp, box: box, edge: edge, c: c, i: i };
    });
    var pick = notes[4];
    var chosen = k.line('M' + pick.c.x + ' ' + pick.c.y + ' L' + hub.x + ' ' + hub.y, { stroke: A, 'stroke-width': 2, 'stroke-linecap': 'round' });
    chosen.ghost.setAttribute('opacity', 0);
    var hubDot = S('circle', { cx: hub.x, cy: hub.y, r: 3.2, fill: C.deep }, ctx.g);
    var reg = S('g', {}, ctx.g);
    k.rect(hub.x - 13, hub.y - 17, 26, 34, 3, C.soft, C.deep, reg);
    S('path', { d: 'M' + (hub.x - 7) + ' ' + (hub.y - 9) + ' h14 M' + (hub.x - 7) + ' ' + (hub.y - 3) + ' h14 M' + (hub.x - 7) + ' ' + (hub.y + 3) + ' h10 M' + (hub.x - 7) + ' ' + (hub.y + 9) + ' h12',
      stroke: C.deep, 'stroke-width': 1.5, 'stroke-linecap': 'round' }, reg);
    return {
      emit: { x: hub.x, y: b.y + b.h - 3 },
      update: function (p) {
        k.fade(ppl, win(p, 0, 0.12));
        talk.draw(win(p, 0.1, 0.24) * (1 - win(p, 0.64, 0.8)));
        var collapse = win(p, 0.62, 0.8);
        notes.forEach(function (n) {
          var w = win(p, 0.1 + n.i * 0.06, 0.24 + n.i * 0.06);
          n.edge.draw(win(p, 0.2 + n.i * 0.05, 0.38 + n.i * 0.05) * (1 - collapse));
          var dx = (hub.x - n.c.x) * collapse, dy = (hub.y - n.c.y) * collapse + 4 * (1 - w);
          n.grp.setAttribute('transform', 'translate(' + dx.toFixed(2) + ' ' + dy.toFixed(2) + ')');
          k.fade(n.grp, w * (1 - collapse));
        });
        var rec = win(p, 0.44, 0.56);
        chosen.draw(rec * (1 - collapse));
        pick.box.setAttribute('stroke', rec > 0.5 && collapse < 1 ? A : C.border);
        k.fade(hubDot, win(p, 0.2, 0.3) * (1 - collapse));
        k.fade(reg, win(p, 0.7, 0.86));
      },
    };
  };

  /* 03 — Choosing the strategy: faint paths, one goes solid, the rest fade */
  build[3] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win;
    var ox = b.x + 10, oy = b.cy, bx = b.x + b.w - 34;
    var PICK = 1;
    var opts = [0, 1, 2].map(function (i) {
      var ty = b.y + 14 + i * ((b.h - 28) / 2);
      var d = 'M' + ox + ' ' + oy + ' C' + (ox + (bx - ox) * 0.45) + ' ' + oy + ' ' + (ox + (bx - ox) * 0.55) + ' ' + ty + ' ' + (bx - 2) + ' ' + ty;
      var dashed = S('path', { d: d, fill: 'none', stroke: C.ink, 'stroke-dasharray': '3 4' }, ctx.g);
      var box = S('g', {}, ctx.g);
      var frame = k.rect(bx, ty - 10, 28, 20, 3, C.node, C.border, box);
      S('path', { d: 'M' + (bx + 6) + ' ' + (ty - 3) + ' h16 M' + (bx + 6) + ' ' + (ty + 3) + ' h11',
        stroke: C.ink, 'stroke-opacity': 0.55, 'stroke-width': 1.4, 'stroke-linecap': 'round' }, box);
      return { dashed: dashed, box: box, frame: frame, ty: ty, d: d };
    });
    var solid = k.line(opts[PICK].d, { stroke: A, 'stroke-width': 2, 'stroke-linecap': 'round' });
    solid.ghost.setAttribute('opacity', 0);
    var origin = S('circle', { cx: ox, cy: oy, r: 3.6, fill: C.deep }, ctx.g);
    var G = ctx.GHOST;
    return {
      emit: { x: bx + 14, y: b.y + b.h - 3 },
      update: function (p) {
        k.fade(origin, win(p, 0, 0.1));
        var appear = win(p, 0.08, 0.3);
        var gone = win(p, 0.56, 0.74);
        opts.forEach(function (o, i) {
          var pickd = i === PICK;
          var op = pickd ? G + (0.5 - G) * appear * (1 - win(p, 0.5, 0.62))
            : Math.max(G * 0.5, G + (0.5 - G) * appear * (1 - gone));
          o.dashed.setAttribute('opacity', op.toFixed(3));
          k.fade(o.box, pickd ? appear : appear * (1 - gone));
          o.frame.setAttribute('stroke', pickd && p > 0.62 ? A : C.border);
          o.frame.setAttribute('fill', pickd && p > 0.62 ? C.soft : C.node);
        });
        solid.draw(win(p, 0.34, 0.62));
      },
    };
  };

  /* 04 — Finalising: numbered questions resolve one by one, the last is confirmed */
  build[4] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win;
    var rows = [0, 1, 2, 3].map(function (i) {
      var y = b.y + 5 + i * 29, cy = y + 8;
      var row = S('g', {}, ctx.g);
      var marker = S('g', {}, row);
      var ring = S('circle', { cx: b.x + 9, cy: cy, r: 8.5, fill: C.raised, stroke: C.border }, marker);
      var num = k.text(b.x + 9, cy + 0.5, String(i + 1), 8, C.ink, marker, 'middle');
      var bar = k.rect(b.x + 26, y + 1, b.w - 60, 14, 3, C.node, C.border, row);
      S('path', { d: 'M' + (b.x + 32) + ' ' + (cy - 1.5) + ' h' + (b.w - 90) + ' M' + (b.x + 32) + ' ' + (cy + 2.5) + ' h' + (b.w - 120),
        stroke: C.ink, 'stroke-opacity': 0.4, 'stroke-width': 1.3, 'stroke-linecap': 'round' }, row);
      var cxr = b.x + b.w - 12;
      var chk = S('circle', { cx: cxr, cy: cy, r: 7.5, fill: C.raised, stroke: C.border }, row);
      var tick = k.line('M' + (cxr - 3.6) + ' ' + cy + ' l2.8 3 l5 -6', { stroke: C.deep, 'stroke-width': 1.6, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, row);
      var inner = k.line('M' + (b.x + 5) + ' ' + cy + ' l3 3.2 l5.2 -6.4', { stroke: '#fff', 'stroke-width': 1.8, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, marker);
      inner.ghost.setAttribute('opacity', 0);
      return { row: row, marker: marker, ring: ring, num: num, bar: bar, chk: chk, tick: tick, inner: inner, i: i };
    });
    return {
      emit: { x: b.x + b.w - 12, y: b.y + b.h - 3 },
      update: function (p) {
        rows.forEach(function (r) {
          var i = r.i, last = i === 3;
          var appear = win(p, 0.04 + i * 0.05, 0.16 + i * 0.05);
          k.fade(r.row, appear);
          r.row.setAttribute('transform', 'translate(0 ' + (3 * (1 - appear)).toFixed(2) + ')');
          var at = last ? 0.72 : 0.28 + i * 0.14;
          var solved = win(p, at, at + 0.1);
          r.tick.draw(solved);
          r.chk.setAttribute('fill', solved > 0.5 ? (last ? C.soft : C.soft) : C.raised);
          r.chk.setAttribute('stroke', solved > 0.5 ? C.line : C.border);
          r.bar.setAttribute('stroke', solved > 0.5 ? C.line : C.border);
          if (!last) {
            var sink = win(p, at + 0.06, at + 0.16);
            r.marker.setAttribute('transform', 'translate(' + (14 * sink).toFixed(2) + ' 0)');
            r.marker.setAttribute('opacity', (1 - sink).toFixed(3));
          } else {
            r.num.setAttribute('opacity', (1 - win(p, 0.72, 0.8)).toFixed(3));
            var fill = win(p, 0.74, 0.84);
            r.ring.setAttribute('fill', fill > 0.5 ? A : C.raised);
            r.ring.setAttribute('stroke', fill > 0.5 ? C.deep : C.border);
            r.inner.draw(win(p, 0.8, 0.94));
          }
        });
      },
    };
  };

  /* 05 — Updating it inside Adam: the signal splits four ways and rejoins */
  build[5] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win, lerp = ctx.lerp;
    var names = ['contracts', 'screens', 'states', 'flows'];
    var E = { x: b.x, y: ctx.railY };
    var H = { x: b.x + b.w - 30, y: b.cy };
    var pw = Math.min(92, b.w * 0.34), px = b.x + 26;
    var lanes = names.map(function (name, i) {
      var y = b.y + 5 + i * 27, py = y + 8.5;
      var inb = k.line('M' + E.x + ' ' + E.y + ' C' + (E.x + 4) + ' ' + (E.y - 24) + ' ' + (px - 18) + ' ' + py + ' ' + px + ' ' + py,
        { stroke: A, 'stroke-width': 1.5, 'stroke-linecap': 'round' });
      var out = k.line('M' + (px + pw) + ' ' + py + ' C' + (H.x - 34) + ' ' + py + ' ' + (H.x - 34) + ' ' + H.y + ' ' + (H.x - 17) + ' ' + H.y,
        { stroke: A, 'stroke-width': 1.5, 'stroke-linecap': 'round' });
      var pill = S('g', {}, ctx.g);
      var frame = k.rect(px, y, pw, 17, 4, C.node, C.border, pill);
      var sq = k.rect(px + 4, y + 3, 11, 11, 2.5, C.soft, C.line, pill);
      var label = k.text(px + 21, py + 0.5, name, 8.5, C.ink, pill);
      return { inb: inb, out: out, pill: pill, frame: frame, sq: sq, label: label, i: i,
        headIn: k.dot(2.6, A), headOut: k.dot(2.6, A) };
    });
    var ringOuter = S('circle', { cx: H.x, cy: H.y, r: 22, fill: 'none', stroke: A, 'stroke-opacity': 0.35 }, ctx.g);
    var ring = S('circle', { cx: H.x, cy: H.y, r: 16, fill: C.node, stroke: C.line }, ctx.g);
    var mark = S('path', { d: 'M' + (H.x - 7) + ' ' + (H.y + 6) + ' L' + H.x + ' ' + (H.y - 7) + ' L' + (H.x + 7) + ' ' + (H.y + 6),
      fill: 'none', stroke: C.text, 'stroke-width': 2.4, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, ctx.g);
    var rejoin = k.line('M' + (H.x + 17) + ' ' + H.y + ' C' + (H.x + 30) + ' ' + H.y + ' ' + (ctx.card.r - 14) + ' ' + ctx.railY + ' ' + ctx.card.r + ' ' + ctx.railY,
      { stroke: A, 'stroke-width': 2, 'stroke-linecap': 'round' });
    var rejoinHead = k.dot(3.2, A);
    return {
      emit: { x: H.x, y: b.y + b.h - 3 },
      head: function (p, a, bEnd, uE, INOUT) {
        if (p < 0.18) return { u: lerp(a, uE, INOUT(p / 0.18)) };
        if (p < 0.96) return { u: p < 0.78 ? uE : lerp(uE, bEnd, INOUT((p - 0.78) / 0.18)), hide: true };
        return { u: bEnd };
      },
      update: function (p, live) {
        lanes.forEach(function (l) {
          var i = l.i;
          var split = win(p, 0.18 + i * 0.025, 0.4 + i * 0.025);
          l.inb.draw(split);
          var qi = (p - 0.18 - i * 0.025) / 0.22;
          if (live && qi > 0 && qi < 1) k.place(l.headIn, l.inb.at(ctx.EASE(qi)), true); else l.headIn.setAttribute('opacity', 0);
          k.fade(l.pill, win(p, 0.02 + i * 0.04, 0.16 + i * 0.04));
          var at = 0.38 + i * 0.06;
          var lit = live ? Math.min(win(p, at, at + 0.04), 1 - win(p, at + 0.12, at + 0.2)) : 0;
          var set = p >= at + 0.04;
          l.frame.setAttribute('fill', lit > 0.3 ? C.soft : C.node);
          l.frame.setAttribute('stroke', lit > 0.3 ? A : set ? C.line : C.border);
          l.frame.setAttribute('stroke-width', lit > 0.3 ? 1.5 : 1);
          l.sq.setAttribute('fill', lit > 0.3 || set ? A : C.soft);
          l.label.setAttribute('fill', lit > 0.3 ? C.deep : C.ink);
          var conv = win(p, 0.6 + i * 0.02, 0.76 + i * 0.02);
          l.out.draw(conv);
          var qo = (p - 0.6 - i * 0.02) / 0.16;
          if (live && qo > 0 && qo < 1) k.place(l.headOut, l.out.at(ctx.EASE(qo)), true); else l.headOut.setAttribute('opacity', 0);
        });
        var joined = win(p, 0.72, 0.8);
        var breathe = live ? Math.sin(Math.min(1, p) * Math.PI * 3) * 2 : 0;
        ringOuter.setAttribute('r', (22 + breathe).toFixed(2));
        ringOuter.setAttribute('opacity', (ctx.GHOST + (1 - ctx.GHOST) * joined).toFixed(3));
        k.fade(ring, win(p, 0.04, 0.2));
        mark.setAttribute('stroke', joined > 0.5 ? C.deep : C.text);
        k.fade(mark, win(p, 0.04, 0.2));
        rejoin.draw(win(p, 0.78, 0.95));
        var qr = (p - 0.78) / 0.17;
        if (live && qr > 0 && qr < 1) k.place(rejoinHead, rejoin.at(ctx.EASE(qr)), true); else rejoinHead.setAttribute('opacity', 0);
      },
    };
  };

  /* 06 — Sign-off: a verification stroke draws round the verdict, the signal holds */
  build[6] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win, lerp = ctx.lerp;
    var cx = b.cx, cy = b.cy, R = Math.min(b.w, b.h) * 0.44;
    S('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: C.ink, opacity: ctx.GHOST }, ctx.g);
    var circ = 2 * Math.PI * R;
    var stroke = S('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: A, 'stroke-width': 2, 'stroke-linecap': 'round',
      transform: 'rotate(-90 ' + cx + ' ' + cy + ')', 'stroke-dasharray': circ + ' ' + circ, 'stroke-dashoffset': circ }, ctx.g);
    var doc = S('g', {}, ctx.g);
    k.rect(cx - 19, cy - 25, 38, 50, 4, C.node, C.border, doc);
    S('path', { d: 'M' + (cx - 12) + ' ' + (cy - 16) + ' h24 M' + (cx - 12) + ' ' + (cy - 9) + ' h20 M' + (cx - 12) + ' ' + (cy - 2) + ' h22',
      stroke: C.ink, 'stroke-opacity': 0.45, 'stroke-width': 1.6, 'stroke-linecap': 'round' }, doc);
    var sig = k.line('M' + (cx - 12) + ' ' + (cy + 14) + ' c6 -9 9 7 15 -4 c3 -5 5 6 9 1',
      { stroke: C.deep, 'stroke-width': 1.5, 'stroke-linecap': 'round' });
    var sx = cx + R * 0.72, sy = cy + R * 0.5;
    var seal = S('circle', { cx: sx, cy: sy, r: 10, fill: C.raised, stroke: C.border }, ctx.g);
    var tick = k.line('M' + (sx - 4.5) + ' ' + sy + ' l3.4 3.8 l6 -7.6', { stroke: '#fff', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' });
    tick.ghost.setAttribute('opacity', 0);
    return {
      emit: { x: cx, y: b.y + b.h - 3 },
      head: function (p, a, bEnd, uE, INOUT) {
        var mid = uE - 22 + ctx.card.w / 2;
        if (p < 0.38) return { u: lerp(a, mid, INOUT(p / 0.38)) };
        if (p < 0.52) return { u: mid, hold: true };            // ~420ms of 3000
        return { u: lerp(mid, bEnd, INOUT((p - 0.52) / 0.48)) };
      },
      update: function (p) {
        var w = win(p, 0.08, 0.42);
        stroke.setAttribute('stroke-dashoffset', (circ * (1 - w)).toFixed(1));
        stroke.setAttribute('opacity', w > 0 ? 1 : 0);
        k.fade(doc, win(p, 0.02, 0.16));
        sig.draw(win(p, 0.42, 0.56));
        var sealed = win(p, 0.54, 0.62);
        seal.setAttribute('fill', sealed > 0.5 ? A : C.raised);
        seal.setAttribute('stroke', sealed > 0.5 ? C.deep : C.border);
        k.fade(seal, Math.max(0.35, sealed));
        tick.draw(win(p, 0.58, 0.7));
      },
    };
  };

  /* 07 — Handoff: scattered parts become one connected graph, and it leaves */
  build[7] = function (b, ctx, k) {
    var S = ctx.S, C = ctx.C, A = ctx.accent, win = ctx.win, lerp = ctx.lerp;
    var scatter = [[0.06, 0.18], [0.3, 0.8], [0.16, 0.5], [0.44, 0.12], [0.38, 0.6]];
    var tidy = [[0.08, 0.5], [0.28, 0.2], [0.28, 0.8], [0.5, 0.34], [0.5, 0.66]];
    var links = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 4]];
    var edges = links.map(function () {
      return S('line', { stroke: C.deep, 'stroke-width': 1.2, 'stroke-linecap': 'round' }, ctx.g);
    });
    var nodes = scatter.map(function () { return S('circle', { r: 4.2, fill: C.raised, stroke: C.line }, ctx.g); });
    var outs = [0.2, 0.5, 0.8].map(function (fy, i) {
      var x = b.x + b.w * 0.8, y = b.y + b.h * fy;
      var wire = k.line('M' + (b.x + b.w * 0.5 + 5) + ' ' + (b.y + b.h * (i < 2 ? 0.34 : 0.66)) + ' C' + (b.x + b.w * 0.66) + ' ' + (b.y + b.h * (i < 2 ? 0.34 : 0.66)) + ' ' + (x - 20) + ' ' + y + ' ' + x + ' ' + y,
        { stroke: C.deep, 'stroke-opacity': 0.7 });
      var chip = S('g', {}, ctx.g);
      var frame = k.rect(x, y - 11, 26, 22, 4, C.node, C.border, chip);
      S('path', { d: 'M' + (x + 10) + ' ' + (y - 4) + ' l4 4 l-4 4', fill: 'none', stroke: C.deep, 'stroke-width': 1.5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, chip);
      return { wire: wire, chip: chip, frame: frame, i: i };
    });
    return {
      emit: { x: b.x + b.w * 0.8 + 13, y: b.y + b.h - 3 },
      update: function (p) {
        var t = win(p, 0.18, 0.6);
        var pts = scatter.map(function (s, i) {
          return { x: b.x + b.w * lerp(s[0], tidy[i][0], t), y: b.y + b.h * lerp(s[1], tidy[i][1], t) };
        });
        var draw = win(p, 0.34, 0.7);
        links.forEach(function (l, i) {
          var a = pts[l[0]], c = pts[l[1]], e = edges[i];
          var len = Math.hypot(c.x - a.x, c.y - a.y);
          e.setAttribute('x1', a.x); e.setAttribute('y1', a.y); e.setAttribute('x2', c.x); e.setAttribute('y2', c.y);
          e.setAttribute('stroke-dasharray', len + ' ' + len);
          e.setAttribute('stroke-dashoffset', (len * (1 - draw)).toFixed(1));
          e.setAttribute('opacity', (ctx.GHOST + (1 - ctx.GHOST) * draw).toFixed(3));
          if (draw === 0) { e.setAttribute('stroke-dashoffset', 0); e.setAttribute('opacity', ctx.GHOST * 0.8); }
        });
        var appear = win(p, 0.04, 0.18);
        nodes.forEach(function (n, i) {
          n.setAttribute('cx', pts[i].x); n.setAttribute('cy', pts[i].y);
          k.fade(n, appear);
          n.setAttribute('fill', t > 0.85 ? A : C.raised);
          n.setAttribute('stroke', t > 0.85 ? C.deep : C.line);
        });
        outs.forEach(function (o) {
          k.fade(o.chip, win(p, 0.6 + o.i * 0.04, 0.74 + o.i * 0.04));
          o.wire.draw(win(p, 0.62 + o.i * 0.04, 0.8 + o.i * 0.04));
          o.frame.setAttribute('stroke', p > 0.78 + o.i * 0.04 ? C.line : C.border);
          o.frame.setAttribute('fill', p > 0.78 + o.i * 0.04 ? C.soft : C.node);
        });
      },
    };
  };

  window.AdamJourneyStages = {
    build: function (n, art, ctx) {
      var k = kit(ctx);
      var inst = build[n](art, ctx, k);
      inst.update(0, false);
      return inst;
    },
  };
})();
