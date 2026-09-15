/* The decision pipeline — one persistent signal through seven stages.
 *
 * SVG over the cards: the signal is a path whose travelled part and head are
 * drawn with stroke-dashoffset, the stage drawings are small SVG groups whose
 * parts draw, fade and translate, and the cards themselves only ever move by
 * the one reveal. One clock drives all of it, so a frame is a pure function of
 * elapsed time — which is what lets it loop, resize and seek without drift.
 *
 * Information enters → gets interpreted → decisions become structured → gets
 * validated → becomes an engineering-ready graph. Each stage then lands on its
 * own artefact path at the foot of the card, because each one leaves a record.
 *
 *   window.AdamJourney.mount(hostEl, { canvas, accent });   // canvas is hidden
 *   instance.seek(ms) · instance.pause() · instance.play() · instance.stop()
 *
 * Stage drawings live in adam-journey-stages.js (window.AdamJourneyStages).
 */
(function () {
  'use strict';

  var NS = 'http://www.w3.org/2000/svg';
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  // cubic-bezier(.22,1,.36,1) is an ease-out; a cubic ease-out is close enough
  // for per-frame maths, and the DOM reveal uses the real curve.
  var EASE = function (t) { return 1 - Math.pow(1 - t, 3); };
  var INOUT = function (t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  var win = function (p, a, b) { return EASE(clamp((p - a) / (b - a))); };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var CURVE = 'cubic-bezier(.22,1,.36,1)';

  var C = {
    node: '#ffffff', raised: '#f8fbfc', border: '#dfe8ec', strong: '#c7d5db',
    text: '#1d2c33', ink: '#5d7280', deep: '#0389d7', path: '#0268ce',
    soft: '#e3f5fb', line: '#9cd9ec',
  };

  var GHOST = 0.15;   // idle nodes
  var DONE = 0.72;    // a stage that has run, at rest
  var RAIL = 26;      // corridor at the foot of each illustration band
  // 01–07; 05 is the long one, 06 carries the 400ms sign-off hold
  var DUR = [2600, 2800, 2600, 2800, 3400, 3000, 2800];
  var RUN = DUR.reduce(function (a, b) { return a + b; }, 0);
  var HOLD = 2600, FADE = 800;
  var CYCLE = RUN + HOLD + FADE;

  function S(tag, attrs, parent) {
    var el = document.createElementNS(NS, tag);
    for (var k in attrs) if (attrs[k] != null) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  }

  // rAF stops in a preview the visibility API calls hidden; race it against a
  // timer so the loop survives either way.
  function sched(fn) {
    var done = false, h = {};
    h.t = setTimeout(function () { if (done) return; done = true; cancelAnimationFrame(h.r); fn(performance.now()); }, 34);
    h.r = requestAnimationFrame(function (ts) { if (done) return; done = true; clearTimeout(h.t); fn(ts); });
    return h;
  }
  function unsched(h) { if (h) { clearTimeout(h.t); cancelAnimationFrame(h.r); } }

  function Journey(host, opts) {
    this.host = host;
    this.canvas = opts.canvas || null;
    this.accent = opts.accent || '#04d8f2';
    // `art: false` keeps the signal, the card light and the record lines, and
    // leaves the drawings to whoever listens for `journey:frame` (the React
    // diagrams on the landing page). The stage modules still steer the head.
    this.art = opts.art !== false;
    this.elapsed = 0;
    this.started = false;
    this.visible = true;
    this.paused = false;
    this.reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /* ── geometry ─────────────────────────────────────────────────────── */

  Journey.prototype.measure = function () {
    var hr = this.host.getBoundingClientRect();
    if (!hr.width || !hr.height || !window.AdamJourneyStages) return false;
    var box = function (el) {
      var r = el.getBoundingClientRect();
      return { x: r.left - hr.left, y: r.top - hr.top, w: r.width, h: r.height,
        r: r.right - hr.left, b: r.bottom - hr.top,
        cx: r.left - hr.left + r.width / 2, cy: r.top - hr.top + r.height / 2 };
    };
    var cards = [], bands = [], nums = [], labels = [];
    for (var i = 1; i <= 7; i++) {
      var card = this.host.querySelector('[data-card="' + i + '"]');
      var band = this.host.querySelector('[data-stage="' + i + '"]');
      if (!card || !band) return false;
      cards.push(box(card)); bands.push(box(band));
      nums.push(card.firstElementChild);
      labels.push(card.lastElementChild);
    }
    this.cardEls = [].map.call(this.host.querySelectorAll('[data-card]'), function (e) { return e; });
    this.numEls = nums;
    this.labelEls = labels;
    this.labels = labels.map(box);
    this.exitEl = this.host.querySelector('[data-exit]');
    this.w = hr.width; this.h = hr.height;
    this.K = cards; this.B = bands;

    var mean = function (a, b) {
      var s = 0;
      for (var j = a; j <= b; j++) s += bands[j].y + bands[j].h - RAIL / 2;
      return s / (b - a + 1);
    };
    var rowY = [mean(0, 3), mean(4, 6)];
    this.rowY = rowY;
    var gapY = (cards[3].b + cards[4].y) / 2;

    // The run, on the cards' own lines only: through each card's corridor,
    // down 04's right border, back along the divider between the rows, down
    // 05's left border, and out to the right after 07. Nothing is drawn in
    // the margin. Points marked `end` close a stage.
    var pts = [];
    var push = function (x, y, end) { pts.push({ x: x, y: y, end: end }); };
    push(cards[0].x + 1, rowY[0]);
    for (i = 0; i < 4; i++) { push(cards[i].x, rowY[0]); push(cards[i].r, rowY[0], true); }
    push(cards[3].r, gapY);
    push(cards[4].x + 0.5, gapY);
    push(cards[4].x + 0.5, rowY[1]);
    for (i = 4; i < 7; i++) { push(cards[i].x, rowY[1]); push(cards[i].r, rowY[1], true); }
    var tail = Math.max(18, Math.min(34, hr.width - cards[6].r + 30));
    push(cards[6].r + tail, rowY[1]);

    var total = 0, cum = [0];
    for (i = 1; i < pts.length; i++) {
      total += Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y);
      cum.push(total);
    }
    var ends = [];
    pts.forEach(function (p, k) { if (p.end) ends.push(cum[k]); });
    ends[6] = total;               // 07 runs on to the exit
    this.total = total;
    this.span = ends.map(function (b, k) { return { a: k ? ends[k - 1] : 0, b: b }; });
    // length at which a card's content edge sits on its rail
    var cardLeft = [];
    pts.forEach(function (p, k) { if (p.end) cardLeft.push(cum[k - 1]); });
    this.contentAt = function (k) { return cardLeft[k] + 22; };
    this.pts = pts;
    this.build();
    return true;
  };

  /* ── the drawing ──────────────────────────────────────────────────── */

  Journey.prototype.build = function () {
    if (this.canvas) this.canvas.style.display = 'none';
    if (!this.svg) {
      this.svg = S('svg', { 'aria-hidden': 'true', focusable: 'false' });
      this.svg.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;z-index:2';
      this.host.appendChild(this.svg);
    }
    var svg = this.svg;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.setAttribute('viewBox', '0 0 ' + this.w + ' ' + this.h);

    var A = this.accent, self = this;
    var gCards = S('g', {}, svg);
    var gArt = S('g', {}, svg);
    var gDeliver = S('g', {}, svg);
    var gRail = S('g', {}, svg);

    this.overlays = this.K.map(function (k) {
      return S('rect', { x: k.x + 1, y: k.y + 1, width: k.w - 2, height: k.h - 2,
        fill: A, 'fill-opacity': 0.035, stroke: A, 'stroke-opacity': 0.45, opacity: 0 }, gCards);
    });

    var d = this.pts.map(function (p, k) { return (k ? 'L' : 'M') + p.x.toFixed(1) + ' ' + p.y.toFixed(1); }).join(' ');
    this.base = S('path', { d: d, fill: 'none', stroke: C.deep, 'stroke-opacity': 0.16, 'stroke-width': 1 }, gRail);
    this.trail = S('path', { d: d, fill: 'none', stroke: C.deep, 'stroke-opacity': 0.55, 'stroke-width': 1.6,
      'stroke-dasharray': this.total + ' ' + this.total, 'stroke-dashoffset': this.total }, gRail);
    this.SEG = 46;
    this.headSeg = S('path', { d: d, fill: 'none', stroke: A, 'stroke-width': 2.4, 'stroke-linecap': 'round',
      'stroke-dasharray': this.SEG + ' ' + (this.total + this.SEG) }, gRail);
    this.nodes = this.K.map(function (k, i) {
      return S('circle', { cx: k.r, cy: self.rowY[i < 4 ? 0 : 1], r: 3, fill: C.strong }, gRail);
    });
    var end = this.pts[this.pts.length - 1];
    this.arrow = S('path', { d: 'M' + end.x + ' ' + end.y + ' l-7 -4 v8 z', fill: A, opacity: 0 }, gRail);
    this.halo = S('circle', { r: 8, fill: A, 'fill-opacity': 0.22 }, gRail);
    this.head = S('circle', { r: 3.4, fill: A }, gRail);

    var api = { S: S, C: C, win: win, lerp: lerp, EASE: EASE, clamp: clamp, accent: A, GHOST: GHOST };
    this.stages = [];
    this.delivers = [];
    for (var i = 0; i < 7; i++) {
      var band = this.B[i];
      var g = S('g', {}, gArt);
      var art = { x: band.x, y: band.y, w: band.w, h: band.h - RAIL };
      art.cx = art.x + art.w / 2; art.cy = art.y + art.h / 2;
      var ctx = Object.assign({ g: g, card: this.K[i], railY: this.rowY[i < 4 ? 0 : 1] }, api);
      var inst = window.AdamJourneyStages.build(i + 1, art, ctx);
      if (!this.art) g.style.display = 'none';
      this.stages.push({ g: g, inst: inst });
      this.delivers.push(this.deliver(gDeliver, i, inst.emit || { x: art.cx, y: art.y + art.h }));
    }
  };

  // The record each stage leaves: down the card's gutter to its artefact path.
  Journey.prototype.deliver = function (parent, i, emit) {
    var lb = this.labels[i], k = this.K[i];
    var gx = k.x + 10, ly = lb.y + lb.h / 2;
    var d = 'M' + emit.x + ' ' + emit.y + ' L' + gx + ' ' + emit.y + ' L' + gx + ' ' + ly + ' L' + (lb.x - 4) + ' ' + ly;
    var g = S('g', {}, parent);
    var ghost = S('path', { d: d, fill: 'none', stroke: C.deep, 'stroke-opacity': 0.22, 'stroke-dasharray': '2 4', opacity: 0 }, g);
    var live = S('path', { d: d, fill: 'none', stroke: C.deep, 'stroke-width': 1.2, 'stroke-opacity': 0.7 }, g);
    var len = live.getTotalLength();
    live.setAttribute('stroke-dasharray', len + ' ' + len);
    var dots = [0, 1, 2].map(function () { return S('circle', { r: 2.2, fill: this.accent, opacity: 0 }, g); }, this);
    var under = S('line', { x1: lb.x, y1: lb.b + 1.5, x2: lb.x + Math.min(lb.w, this.textWidth(this.labelEls[i])), y2: lb.b + 1.5,
      stroke: this.accent, 'stroke-width': 1.4, 'stroke-linecap': 'round' }, g);
    var ulen = Math.max(1, Math.min(lb.w, this.textWidth(this.labelEls[i])));
    under.setAttribute('stroke-dasharray', ulen + ' ' + ulen);
    return { ghost: ghost, live: live, len: len, dots: dots, under: under, ulen: ulen };
  };

  Journey.prototype.textWidth = function (el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    return range.getBoundingClientRect().width || el.getBoundingClientRect().width;
  };

  /* ── one frame ────────────────────────────────────────────────────── */

  Journey.prototype.frame = function () {
    if (!this.stages) return;
    var t = this.started ? this.elapsed % CYCLE : 0;
    var idx = -1, p = 0, acc = 0, phase = 'idle';
    if (this.started) {
      if (t < RUN) {
        phase = 'run';
        for (var i = 0; i < 7; i++) {
          if (t < acc + DUR[i]) { idx = i; p = (t - acc) / DUR[i]; break; }
          acc += DUR[i];
        }
      } else if (t < RUN + HOLD) { phase = 'hold'; idx = 7; }
      else { phase = 'fade'; idx = 7; }
    }
    var fade = phase === 'fade' ? EASE(clamp((t - RUN - HOLD) / FADE)) : 0;

    // stages
    for (i = 0; i < 7; i++) {
      var st = this.stages[i];
      var pi = i < idx ? 1 : i === idx ? p : 0;
      var op = i < idx ? DONE : 1;
      if (phase === 'hold') op = DONE;
      if (phase === 'fade') op = lerp(DONE, GHOST, fade);
      st.inst.update(pi, i === idx);
      st.g.setAttribute('opacity', op.toFixed(3));
      this.paintDeliver(i, pi, i === idx, phase, fade);
      this.overlays[i].setAttribute('opacity', i === idx ? Math.min(1, p / 0.06, (1 - p) / 0.06).toFixed(3) : 0);
      this.setColor(this.numEls[i], i === idx && p < 0.94 ? C.deep : '#5d7280');
    }

    // signal
    var u = 0, hide = false, hold = false;
    if (phase === 'run') {
      var sp = this.span[idx], inst = this.stages[idx].inst;
      if (inst.head) {
        var m = inst.head(p, sp.a, sp.b, this.contentAt(idx), INOUT);
        u = m.u; hide = !!m.hide; hold = !!m.hold;
      } else u = lerp(sp.a, sp.b, INOUT(p));
    } else if (phase !== 'idle') u = this.total;
    this.trail.setAttribute('stroke-dashoffset', (this.total - u).toFixed(1));
    this.trail.setAttribute('opacity', (1 - fade).toFixed(3));
    this.headSeg.setAttribute('stroke-dashoffset', (-(u - this.SEG)).toFixed(1));
    var headOn = phase === 'run' && !hide;
    this.headSeg.setAttribute('opacity', headOn ? 1 : 0);
    var pt = this.base.getPointAtLength(Math.max(0, Math.min(this.total, u)));
    var pulse = hold ? 8 + 4 * Math.abs(Math.sin(performance.now() / 160)) : 8;
    this.head.setAttribute('cx', pt.x); this.head.setAttribute('cy', pt.y);
    this.halo.setAttribute('cx', pt.x); this.halo.setAttribute('cy', pt.y);
    this.halo.setAttribute('r', pulse.toFixed(1));
    this.head.setAttribute('opacity', phase === 'idle' ? 0.35 : headOn ? 1 : 0);
    this.halo.setAttribute('opacity', phase === 'idle' ? 0.3 : headOn ? 1 : 0);
    for (i = 0; i < 7; i++) {
      var passed = phase !== 'idle' && u >= this.span[i].b - 0.5 && phase !== 'fade';
      this.nodes[i].setAttribute('fill', passed ? this.accent : C.strong);
    }
    var out = phase === 'hold' || (phase === 'run' && u >= this.total - 1);
    this.arrow.setAttribute('opacity', out ? 1 : phase === 'fade' ? 1 - fade : 0);
    if (this.exitEl) this.setColor(this.exitEl, out ? C.deep : C.path);

    // One event per frame, for drawings that live outside this file.
    this.host.dispatchEvent(new CustomEvent('journey:frame', {
      detail: { idx: idx, p: p, phase: phase, fade: fade, cycle: this.started ? Math.floor(this.elapsed / CYCLE) : -1 },
    }));
  };

  Journey.prototype.paintDeliver = function (i, p, live, phase, fade) {
    var dv = this.delivers[i];
    var drawn = win(p, 0.72, 0.86);
    dv.live.setAttribute('stroke-dashoffset', (dv.len * (1 - drawn)).toFixed(1));
    dv.live.setAttribute('opacity', live ? 1 : 0);
    // the record a finished stage left, kept faint so seven of them do not
    // turn the grid into a lattice
    dv.ghost.setAttribute('opacity', p >= 1 ? (phase === 'fade' ? 0.5 * (1 - fade) : 0.5) : 0);
    dv.dots.forEach(function (dot, k) {
      var q = clamp((p - 0.74 - k * 0.045) / 0.18);
      if (!live || q <= 0 || q >= 1) { dot.setAttribute('opacity', 0); return; }
      var at = dv.live.getPointAtLength(dv.len * EASE(q));
      dot.setAttribute('cx', at.x); dot.setAttribute('cy', at.y);
      dot.setAttribute('opacity', Math.min(1, (1 - q) * 4));
    });
    var ul = win(p, 0.86, 0.97);
    dv.under.setAttribute('stroke-dashoffset', (dv.ulen * (1 - ul)).toFixed(1));
    dv.under.setAttribute('opacity', live ? 1 : p >= 1 ? (phase === 'fade' ? 0.45 * (1 - fade) : 0.45) : 0);
  };

  Journey.prototype.setColor = function (el, color) {
    if (!el || el.__c === color) return;
    el.__c = color;
    el.style.transition = 'color .2s ease';
    el.style.color = color;
  };

  /* ── reveal ───────────────────────────────────────────────────────── */

  Journey.prototype.reveal = function () {
    var self = this;
    var section = this.host.parentElement;
    var lead = section ? [].filter.call(section.children, function (el) { return el !== self.host; }) : [];
    var cards = this.cardEls || [].slice.call(this.host.querySelectorAll('[data-card]'));
    var all = lead.concat([this.host], cards);
    var prep = function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = 'opacity .8s ' + CURVE + ', transform .8s ' + CURVE;
    };
    var on = function (el, delay) {
      setTimeout(function () { el.style.opacity = '1'; el.style.transform = 'none'; }, delay);
    };
    if (this.reduced) return;
    all.forEach(prep);
    this.host.style.transform = 'none';   // the host fades; only the cards travel
    var shown = false;
    var show = function () {
      if (shown) return;
      shown = true;
      lead.forEach(function (el, k) { on(el, k * 90); });
      on(self.host, 120);
      cards.forEach(function (el, k) { on(el, 260 + k * 120 + (k >= 4 ? 180 : 0)); });
      self.startAt = performance.now() + 260 + 7 * 120 + 180 + 500;
    };
    // The copy must never be stranded by an observer that does not fire.
    setTimeout(show, 1400);
    if (!('IntersectionObserver' in window)) return show();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { show(); io.disconnect(); } });
    }, { threshold: 0.12 });
    io.observe(this.host);
  };

  /* ── lifecycle ────────────────────────────────────────────────────── */

  Journey.prototype.mount = function () {
    var self = this;
    // A replaced instance must not finish building after it was stopped.
    var ready = function () {
      if (self._stopped) return;
      if (!self.measure()) setTimeout(ready, 120); else self.frame();
    };
    ready();
    if (window.ResizeObserver) {
      var last = '';
      this._ro = new ResizeObserver(function () {
        var r = self.host.getBoundingClientRect();
        var key = Math.round(r.width) + 'x' + Math.round(r.height);
        if (key !== last) { last = key; if (self.measure()) self.frame(); }
      });
      this._ro.observe(this.host);
    }
    if ('IntersectionObserver' in window) {
      this._vis = new IntersectionObserver(function (es) { self.visible = es[es.length - 1].isIntersecting; }, { rootMargin: '200px' });
      this._vis.observe(this.host);
    }
    if (this.reduced) {
      // No travel: the finished pipeline, still.
      this.started = true; this.paused = true; this.elapsed = RUN + 10;
    } else {
      this.reveal();
    }
    var prev = performance.now();
    var loop = function (now) {
      self._tick = Date.now();
      self._raf = sched(loop);
      var dt = Math.min(100, Math.max(0, now - prev));
      prev = now;
      if (!self.host.isConnected || !self.stages) return;
      if (!self.started && self.startAt && now >= self.startAt) self.started = true;
      if (!self.visible) return;
      if (self.started && !self.paused) self.elapsed += dt;
      self.frame();
    };
    this._raf = sched(loop);
    this._watch = setInterval(function () {
      if (self._stopped) return;
      if (Date.now() - (self._tick || 0) > 1200) { unsched(self._raf); self._raf = sched(loop); }
    }, 1000);
    return this;
  };

  Journey.prototype.stop = function () {
    this._stopped = true;
    clearInterval(this._watch);
    unsched(this._raf);
    if (this._ro) this._ro.disconnect();
    if (this._vis) this._vis.disconnect();
  };
  Journey.prototype.seek = function (ms) {
    this.started = true; this.paused = true; this.elapsed = ms;
    this.cardEls && this.cardEls.forEach(function (el) { el.style.opacity = '1'; el.style.transform = 'none'; });
    this.frame();
  };
  Journey.prototype.pause = function () { this.paused = true; };
  Journey.prototype.play = function () { this.started = true; this.paused = false; };

  window.AdamJourney = {
    DUR: DUR, CYCLE: CYCLE,
    // One instance per host. The prototype runtime mounts twice — once for the
    // host ref and again when the canvas ref arrives, often on a fresh canvas —
    // so keying on the canvas alone left two SVGs painting the same cards.
    mount: function (host, opts) {
      opts = opts || {};
      [host.__adamJourney, opts.canvas && opts.canvas.__adamJourney].forEach(function (old) {
        if (!old) return;
        old.stop();
        if (old.svg && old.svg.parentNode) old.svg.parentNode.removeChild(old.svg);
      });
      var inst = new Journey(host, opts).mount();
      host.__adamJourney = inst;
      if (opts.canvas) opts.canvas.__adamJourney = inst;
      window.__journey = inst;
      return inst;
    },
  };
})();
