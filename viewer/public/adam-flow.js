/* The ADAM → developer → production flow scene.
 *
 * Ported verbatim from the Softlabs landing build (the canvas painters behind
 * adam-landing-dark.gif / adam-landing-light.gif): the orbiting pixel ring, the
 * ADAM mark, the developer's desk with its three live screens and 16-frame
 * sprite, the finished-product plate, and the dotted beams that carry artefact
 * sprites between the three columns.
 *
 * Rewired off the design component's props/state onto plain options so it can
 * run under any host: window.AdamFlow.start({ root, accent, theme, assets }).
 */
(function () {
  function Scene(opts) {
    this.root = opts.root;
    this.assets = opts.assets || 'assets/';
    this.accentHex = opts.accent || '#2bb3b0';
    this.theme = opts.theme === 'Dark' ? 'Dark' : 'Light';
    this.fps = opts.fps || 6;
    this._ro = {};
    this._raf = {};
  }

  Scene.prototype.asset = function (p) { return this.assets + p.replace(/^assets\//, ''); };
  Scene.prototype.themeName = function () { return this.theme; };
  Scene.prototype.accent = function () { return this.accentHex; };
  Scene.prototype.rgbInk = function () { return this.themeName() === 'Light' ? '20,22,26' : '242,242,240'; };
  Scene.prototype.rgbAccent = function () {
    const n = parseInt(this.accent().replace('#', ''), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255].join(',');
  };

  // rAF does not fire in a preview the visibility API calls hidden, and a scene
  // mounted while visible would then freeze for good. Race rAF against a 34ms
  // timer and let whichever arrives first drive the next frame.
  Scene.prototype.schedule = function (fn) {
    var done = false, h = {};
    h.t = setTimeout(function () {
      if (done) return; done = true; cancelAnimationFrame(h.r); fn(performance.now());
    }, 34);
    h.r = requestAnimationFrame(function (ts) {
      if (done) return; done = true; clearTimeout(h.t); fn(ts);
    });
    return h;
  };
  Scene.prototype.unschedule = function (h) {
    if (!h) return;
    clearTimeout(h.t); cancelAnimationFrame(h.r);
  };

  // 16 frames a loop; `cont` is the un-quantised clock so travel is smooth
  // while state changes still land on whole beats
  Scene.prototype.loopPhase = function (now) {
    const cont = (now / 1000) * this.fps;
    const step = Math.floor(cont);
    const F = ((step % 16) + 16) % 16;
    return { f: F, p: F / 16, step: step, cont: cont };
  };

  // typing is the base pose, with a break dropped in at random — seeded per
  // cycle so the choice is stable across frames, and no two breaks run together
  Scene.prototype.spriteFrame = function (step) {
    const POSE = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]];
    const cycle = Math.floor(step / 4);
    const roll = function (c) { const s = Math.sin(c * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
    let prev = 0, pose = 0;
    for (let c = Math.max(0, cycle - 6); c <= cycle; c++) {
      const r = roll(c);
      pose = r < 0.7 || prev !== 0 ? 0 : r < 0.82 ? 1 : r < 0.94 ? 2 : 3;
      prev = pose;
    }
    return POSE[pose][((step % 4) + 4) % 4];
  };

  // the ring, drawn in the canvas's own pixel grid
  Scene.prototype.orbit = function (ctx, cx, cy, phase, P, rx0, ry0) {
    const TAU = Math.PI * 2;
    const acc = this.rgbAccent(), ink = this.rgbInk();
    const pix = function (x, y, n, fill) {
      ctx.fillStyle = fill;
      ctx.fillRect(Math.round(x / P) * P, Math.round(y / P) * P, n * P, n * P);
    };
    for (let ring = 0; ring < 2; ring++) {
      const rx = ring ? rx0 * 1.17 : rx0, ry = ring ? ry0 * 0.75 : ry0;
      const dir = ring ? -1 : 1, count = ring ? 9 : 12;
      for (let i = 0; i < count; i++) {
        const a = (i / count) * TAU + dir * phase * TAU;
        const depth = (Math.sin(a) + 1) / 2;
        pix(cx + Math.cos(a) * rx, cy + Math.sin(a) * ry, depth > 0.6 ? 2 : 1,
          'rgba(' + (i % 4 === 0 ? acc : ink) + ',' + (0.2 + depth * 0.55).toFixed(2) + ')');
      }
    }
    for (let k = 0; k < 3; k++) {
      const a = phase * TAU + k * 2.1;
      for (let tail = 0; tail < 4; tail++) {
        const aa = a - tail * 0.12;
        pix(cx + Math.cos(aa) * rx0 * 1.08, cy + Math.sin(aa) * ry0 * 0.88,
          tail === 0 ? 2 : 1, 'rgba(' + acc + ',' + (0.85 - tail * 0.2).toFixed(2) + ')');
      }
    }
  };

  // the ADAM mark, static, with 16-bit pixel motion around it
  Scene.prototype.initAdam = function (canvas) {
    if (!canvas) return;
    const self = this;
    const FW = 300, FH = 300, LW = 236, P = 3;
    const ctx = canvas.getContext('2d');
    const markFor = function () {
      const wantLight = self.themeName() === 'Light';
      if (!self._adamMark || self._adamMarkLight !== wantLight) {
        const im = new Image();
        im.src = self.asset(wantLight ? 'assets/adam-mark-light.png' : 'assets/adam-mark-night.png');
        self._adamMark = im; self._adamMarkLight = wantLight;
      }
      return self._adamMark;
    };
    const size = function () {
      const r = canvas.getBoundingClientRect();
      if (!r.width) return;
      const SS = Math.max(2, Math.round(Math.min(2, window.devicePixelRatio || 1) * 2));
      canvas.width = FW * SS; canvas.height = FH * SS;
      ctx.setTransform(SS, 0, 0, SS, 0, 0);
      ctx.imageSmoothingEnabled = false;
    };
    if (window.ResizeObserver) { this._ro.adam = new ResizeObserver(size); this._ro.adam.observe(canvas); }
    const until = function () { size(); if (!canvas.width) self.schedule(until); };
    until();
    const draw = function (now) {
      self._raf.adam = self.schedule(draw);
      if (!canvas.isConnected) return;
      const r = canvas.getBoundingClientRect();
      if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
      const L = self.loopPhase(now);
      ctx.clearRect(0, 0, FW, FH);
      self.orbit(ctx, FW / 2, FH / 2, L.p, P, 118, 128);
      const mark = markFor();
      if (mark.complete && mark.naturalWidth) {
        const sc = Math.min(LW / mark.naturalWidth, LW / mark.naturalHeight);
        const dw = mark.naturalWidth * sc, dh = mark.naturalHeight * sc;
        // the mark is smooth artwork, not pixel art — filter it when scaling
        ctx.imageSmoothingEnabled = true;
        ctx.drawImage(mark, FW / 2 - dw / 2, FH / 2 - dh / 2, dw, dh);
        ctx.imageSmoothingEnabled = false;
      }
    };
    this._raf.adam = this.schedule(draw);
  };

  // the finished product, with the same motion around it as the mark
  Scene.prototype.initOut = function (canvas) {
    if (!canvas) return;
    const self = this;
    const FW = 300, FH = 300, P = 3;
    const ctx = canvas.getContext('2d');
    if (!this._outArt) {
      const im = new Image();
      im.src = this.asset(this.themeName() === 'Light' ? 'assets/live-software-light.png' : 'assets/live-software.png');
      this._outArt = im;
    }
    const art = this._outArt;
    const size = function () {
      const r = canvas.getBoundingClientRect();
      if (!r.width) return;
      const SS = Math.max(2, Math.round(Math.min(2, window.devicePixelRatio || 1) * 2));
      canvas.width = FW * SS; canvas.height = FH * SS;
      ctx.setTransform(SS, 0, 0, SS, 0, 0);
      ctx.imageSmoothingEnabled = false;
    };
    if (window.ResizeObserver) { this._ro.out = new ResizeObserver(size); this._ro.out.observe(canvas); }
    const until = function () { size(); if (!canvas.width) self.schedule(until); };
    until();
    const draw = function (now) {
      self._raf.out = self.schedule(draw);
      if (!canvas.isConnected) return;
      const r = canvas.getBoundingClientRect();
      if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
      const L = self.loopPhase(now);
      ctx.clearRect(0, 0, FW, FH);
      self.orbit(ctx, FW / 2, FH / 2, L.p, P, 132, 138);
      if (art.complete && art.naturalWidth) {
        const box = 232;
        const sc = Math.min(box / art.naturalWidth, box / art.naturalHeight);
        const dw = art.naturalWidth * sc, dh = art.naturalHeight * sc;
        const bob = Math.round(Math.sin(L.p * Math.PI * 2) * 2);
        ctx.drawImage(art, FW / 2 - dw / 2, FH / 2 - dh / 2 + bob, dw, dh);
      }
    };
    this._raf.out = this.schedule(draw);
  };

  // the desk. The person is a 16-frame sprite composited into the chair; the
  // screens are blacked out in the art so the code on them is drawn here.
  Scene.prototype.initDev = function (canvas) {
    if (!canvas) return;
    const self = this;
    const FW = 816, FH = 574;
    const DY = 150, DESKH = 482;
    const SPW = 192, SPH = 135, SPS = 2.8, SPX = 0, SPY = 20;
    const SCR = [[243, 126, 465, 258], [487, 117, 753, 262], [78, 202, 194, 260]];
    const ctx = canvas.getContext('2d');
    const load = function (src) { const i = new Image(); i.src = src; return i; };
    if (!this._deskB) this._deskB = load(this.asset('assets/desk-b.png'));
    const deskB = this._deskB;
    const stripFor = function () {
      const light = self.themeName() === 'Light';
      if (!self._devStrip || self._devStripLight !== light) {
        self._devStrip = load(self.asset(light ? 'assets/dev-person-light.png' : 'assets/dev-person.png'));
        self._devStripLight = light;
      }
      return self._devStrip;
    };
    const size = function () {
      const r = canvas.getBoundingClientRect();
      if (!r.width) return;
      const SS = Math.max(2, Math.round(Math.min(2, window.devicePixelRatio || 1) * 2));
      canvas.width = FW * SS;
      canvas.height = FH * SS;
      ctx.setTransform(SS, 0, 0, SS, 0, 0);
      ctx.imageSmoothingEnabled = false;
    };
    if (window.ResizeObserver) { this._ro.dev = new ResizeObserver(size); this._ro.dev.observe(canvas); }
    const sizeUntil = function () { size(); if (!canvas.width || canvas.width === 300) self.schedule(sizeUntil); };
    sizeUntil();

    const draw = function (now, once) {
      if (!once) self._raf.dev = self.schedule(draw);
      if (!canvas.isConnected) return;
      if (!stripFor().complete || !stripFor().naturalWidth) return;
      const r = canvas.getBoundingClientRect();
      if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
      const L = self.loopPhase(now), fr = self.spriteFrame(L.step), TAU = Math.PI * 2;
      ctx.clearRect(0, 0, FW, FH);

      ctx.save();
      ctx.translate(0, DY);
      const desk = deskB;
      if (desk.complete && desk.naturalWidth) ctx.drawImage(desk, 0, 0, FW, DESKH);

      const acc = self.accent();
      const tick = fr;
      const rnd = function (n) { const s = Math.sin(n * 12.9898) * 43758.5453; return s - Math.floor(s); };

      // left monitor: the editor
      const editor = function (x0, y0, x1, y1) {
        const w = x1 - x0, h = y1 - y0, side = Math.round(w * 0.17);
        ctx.fillStyle = 'rgba(255,255,255,.05)'; ctx.fillRect(x0, y0, side, h);
        ctx.fillStyle = 'rgba(255,255,255,.08)'; ctx.fillRect(x0, y0, w, 8);
        for (let i = 0; i < 3; i++) { ctx.fillStyle = i === 0 ? acc : 'rgba(255,255,255,.32)'; ctx.fillRect(x0 + 5 + i * 6, y0 + 3, 3, 3); }
        for (let i = 0; i < Math.floor((h - 14) / 9); i++) {
          ctx.fillStyle = 'rgba(255,255,255,.14)'; ctx.fillRect(x0 + 5, y0 + 14 + i * 9, 4, 4);
          ctx.fillStyle = 'rgba(255,255,255,.09)'; ctx.fillRect(x0 + 12, y0 + 15 + i * 9, Math.round(side * (0.3 + rnd(i) * 0.42)), 3);
        }
        const rows = Math.floor((h - 18) / 8), scroll = fr;
        for (let i = 0; i < rows; i++) {
          const li = (i + scroll) % 16, y = y0 + 14 + i * 8;
          const indent = Math.floor(rnd(li * 3) * 4) * 6;
          let x = x0 + side + 10 + indent;
          const segs = 1 + Math.floor(rnd(li * 7) * 3);
          for (let k = 0; k < segs; k++) {
            const sd = rnd(li * 11 + k * 5);
            const lw = Math.round(7 + sd * (w - side - 34 - indent) / (segs + 0.6));
            if (x + lw > x1 - 7) break;
            ctx.fillStyle = sd > 0.68 ? acc : sd > 0.42 ? 'rgba(255,255,255,.72)' : sd > 0.2 ? 'rgba(120,170,230,.6)' : 'rgba(255,255,255,.26)';
            ctx.fillRect(x, y, lw, 3); x += lw + 6;
          }
          if (i === rows - 3 && tick % 2 === 0) { ctx.fillStyle = acc; ctx.fillRect(x, y - 1, 2, 5); }
        }
      };

      // right monitor: the frontend being built
      const frontend = function (x0, y0, x1, y1) {
        const w = x1 - x0, h = y1 - y0;
        ctx.fillStyle = 'rgba(255,255,255,.09)'; ctx.fillRect(x0, y0, w, 11);
        for (let i = 0; i < 3; i++) { ctx.fillStyle = 'rgba(255,255,255,.3)'; ctx.fillRect(x0 + 5 + i * 6, y0 + 4, 3, 3); }
        ctx.fillStyle = 'rgba(255,255,255,.14)'; ctx.fillRect(x0 + 26, y0 + 3, w - 34, 5);
        const py = y0 + 11;
        ctx.fillStyle = 'rgba(255,255,255,.05)'; ctx.fillRect(x0, py, w, 14);
        ctx.fillStyle = acc; ctx.fillRect(x0 + 8, py + 5, 14, 4);
        for (let i = 0; i < 4; i++) { ctx.fillStyle = 'rgba(255,255,255,.3)'; ctx.fillRect(x0 + 34 + i * 22, py + 6, 15, 3); }
        ctx.fillStyle = acc; ctx.fillRect(x1 - 34, py + 4, 26, 6);
        const hw = Math.round((w - 40) * 0.62);
        const grow = (Math.sin(L.p * TAU) * 0.5 + 0.5);
        ctx.fillStyle = 'rgba(255,255,255,.82)'; ctx.fillRect(x0 + 12, py + 26, Math.round(hw * (0.5 + grow * 0.5)), 7);
        ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.fillRect(x0 + 12, py + 37, Math.round(hw * 0.72), 7);
        ctx.fillStyle = 'rgba(255,255,255,.2)'; ctx.fillRect(x0 + 12, py + 50, hw - 30, 3); ctx.fillRect(x0 + 12, py + 57, hw - 66, 3);
        ctx.fillStyle = acc; ctx.fillRect(x0 + 12, py + 68, 34, 9);
        ctx.strokeStyle = 'rgba(255,255,255,.28)'; ctx.lineWidth = 1; ctx.strokeRect(x0 + 51.5, py + 68.5, 33, 8);
        const bx = x0 + hw + 22, bw = x1 - 12 - bx;
        if (bw > 30) {
          ctx.strokeStyle = 'rgba(255,255,255,.16)'; ctx.strokeRect(bx + 0.5, py + 26.5, bw - 1, 52);
          for (let i = 0; i < 5; i++) {
            const v = 0.25 + (Math.sin(L.p * TAU * 2 + i * 0.9) * 0.5 + 0.5) * 0.7;
            const bh = Math.round(38 * v);
            ctx.fillStyle = i === 4 ? acc : 'rgba(255,255,255,.32)';
            ctx.fillRect(bx + 7 + i * Math.floor((bw - 14) / 5), py + 70 - bh, Math.max(3, Math.floor((bw - 14) / 5) - 4), bh);
          }
        }
        const cw = Math.floor((w - 32) / 3);
        for (let i = 0; i < 3; i++) {
          const cx = x0 + 12 + i * (cw + 4), cy = py + 86;
          const on = tick % 3 === i;
          ctx.strokeStyle = on ? acc : 'rgba(255,255,255,.16)';
          ctx.strokeRect(cx + 0.5, cy + 0.5, cw - 5, Math.min(34, y1 - cy - 8));
          ctx.fillStyle = on ? acc : 'rgba(255,255,255,.3)'; ctx.fillRect(cx + 6, cy + 7, 8, 8);
          ctx.fillStyle = 'rgba(255,255,255,.42)'; ctx.fillRect(cx + 6, cy + 19, cw - 20, 3);
          ctx.fillStyle = 'rgba(255,255,255,.2)'; ctx.fillRect(cx + 6, cy + 25, cw - 30, 3);
        }
      };

      // the laptop lid is angled, so its code is sheared into the screen plane
      const laptopCode = function (x0, y0, x1, y1) {
        const w = x1 - x0, h = y1 - y0, K = 0.2;
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(x0, y0); ctx.lineTo(x1, y0);
        ctx.lineTo(x1 + K * h, y1); ctx.lineTo(x0 + K * h, y1);
        ctx.closePath(); ctx.clip();
        ctx.transform(1, 0, K, 1, -K * y0, 0);
        const rows = Math.floor((h - 8) / 7), step = fr;
        for (let i = 0; i < rows; i++) {
          const li = (i + step) % 16, y = y0 + 5 + i * 7;
          const indent = Math.floor(rnd(li * 5) * 3) * 5;
          let x = x0 + 6 + indent;
          const segs = 1 + Math.floor(rnd(li * 9) * 2);
          for (let k = 0; k < segs; k++) {
            const sd = rnd(li * 13 + k * 3);
            const lw = Math.round(6 + sd * (w - 22 - indent) / (segs + 0.5));
            if (x + lw > x1 - 8) break;
            ctx.fillStyle = sd > 0.74 ? acc : sd > 0.4 ? 'rgba(255,255,255,.62)' : 'rgba(255,255,255,.26)';
            ctx.fillRect(x, y, lw, 3); x += lw + 5;
          }
        }
        const ax = x1 - 22, ay = y1 - 7, aw = 11, ah = 9;
        ctx.strokeStyle = acc; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ax + aw / 2, ay - ah); ctx.lineTo(ax + aw, ay); ctx.stroke();
        ctx.restore();
        ctx.lineWidth = 1;
      };

      editor(SCR[0][0], SCR[0][1], SCR[0][2], SCR[0][3]);
      frontend(SCR[1][0], SCR[1][1], SCR[1][2], SCR[1][3]);
      laptopCode(SCR[2][0], SCR[2][1], SCR[2][2], SCR[2][3]);

      const strip = stripFor();
      if (strip.complete && strip.naturalWidth) ctx.drawImage(strip, fr * SPW, 0, SPW, SPH, SPX, SPY, SPW * SPS, SPH * SPS);
      ctx.restore();

      const P = 3;
      const pix = function (x, y, w, h, fill) { ctx.fillStyle = fill; ctx.fillRect(Math.round(x / P) * P, Math.round(y / P) * P, w * P, h * P); };
      // language tokens drifting up through the headroom
      const token = function (x, y0, kind, ph) {
        const u = (L.p * 2 + ph) % 1;
        const a = Math.sin(u * Math.PI) * 0.95;
        if (a < 0.05) return;
        const y = y0 - u * 78;
        const c = kind === 'brace' || kind === 'arrow' ? 'rgba(' + self.rgbAccent() + ',' + a.toFixed(2) + ')' : 'rgba(' + self.rgbInk() + ',' + (a * 0.9).toFixed(2) + ')';
        const dots = {
          brace: [[1, 0], [0, 1], [0, 2], [1, 3], [4, 0], [5, 1], [5, 2], [4, 3]],
          angle: [[2, 0], [1, 1], [0, 2], [1, 3], [2, 4], [4, 0], [5, 1], [6, 2], [5, 3], [4, 4]],
          paren: [[1, 0], [0, 1], [0, 2], [1, 3], [4, 0], [5, 1], [5, 2], [4, 3]],
          arrow: [[0, 1], [1, 1], [2, 1], [3, 1], [2, 0], [3, 1], [2, 2]],
          semi: [[0, 0], [0, 2], [0, 3]]
        }[kind];
        dots.forEach(function (d) { pix(x + d[0] * P * 2, y + d[1] * P * 2, 2, 2, c); });
      };
      token(176, 132, 'brace', 0);
      token(202, 120, 'angle', 0.45);
      token(500, 130, 'arrow', 0.24);
      token(526, 122, 'semi', 0.68);

      const inkA = function (a) { return 'rgba(' + self.rgbInk() + ',' + a + ')'; };
      const plate = self.themeName() === 'Light' ? 'rgba(255,255,255,.9)' : 'rgba(8,9,11,.9)';

      // build output streaming past
      const bw = 250, bh = 96, bx0 = 236, by0 = 20;
      ctx.fillStyle = plate; ctx.fillRect(bx0, by0, bw, bh);
      ctx.strokeStyle = inkA('.16'); ctx.lineWidth = 1;
      ctx.strokeRect(bx0 + 0.5, by0 + 0.5, bw - 1, bh - 1);
      for (let i = 0; i < 5; i++) pix(bx0 + 30 + i * P, by0 + bh + i * P, 1, 1, inkA('.16'));
      ctx.fillStyle = inkA('.06'); ctx.fillRect(bx0 + 1, by0 + 1, bw - 2, 12);
      pix(bx0 + 6, by0 + 4, 1, 1, acc);
      ctx.fillStyle = inkA('.22'); ctx.fillRect(bx0 + 18, by0 + 5, 78, 3);
      for (let i = 0; i < 6; i++) {
        const li = (i + fr) % 16, y = by0 + 20 + i * 12;
        const sd = rnd(li * 23);
        pix(bx0 + 7, y, 1, 1, sd > 0.78 ? acc : 'rgba(120,200,150,.8)');
        ctx.fillStyle = inkA('.36');
        ctx.fillRect(bx0 + 16, y, Math.round((bw - 46) * (0.3 + sd * 0.66)), 3);
        if (i === 5 && fr % 2 === 0) pix(bx0 + 18 + Math.round((bw - 46) * (0.3 + sd * 0.66)), y - 1, 1, 2, acc);
      }

      // code card — a function typing itself out
      const cx0 = 10, cy0 = 14, cwd = 150, chd = 116;
      ctx.fillStyle = plate; ctx.fillRect(cx0, cy0, cwd, chd);
      ctx.strokeStyle = inkA('.14'); ctx.strokeRect(cx0 + 0.5, cy0 + 0.5, cwd - 1, chd - 1);
      pix(cx0 + 6, cy0 + 6, 1, 1, acc);
      ctx.fillStyle = inkA('.2'); ctx.fillRect(cx0 + 18, cy0 + 7, 46, 3);
      const typed = Math.floor((fr / 16) * 26);
      [[0, 24, 3], [8, 38, 4], [8, 52, 2], [16, 66, 3], [8, 80, 4], [0, 94, 2]].forEach(function (row, li) {
        const ind = row[0], ly = row[1], segs = row[2];
        let x = cx0 + 8 + ind;
        for (let k = 0; k < segs; k++) {
          const sd = rnd(li * 9 + k * 3);
          const lwd = Math.round(9 + sd * 26);
          if (x + lwd > cx0 + cwd - 8) break;
          if (li * 4 + k <= typed) {
            ctx.fillStyle = sd > 0.72 ? 'rgba(' + self.rgbAccent() + ',.9)' : sd > 0.45 ? inkA('.62') : 'rgba(120,170,230,.6)';
            ctx.fillRect(x, cy0 + ly, lwd, 3);
          }
          x += lwd + 5;
        }
        if (li * 4 <= typed && (li + 1) * 4 > typed && fr % 2 === 0) pix(x, cy0 + ly - 1, 1, 2, acc);
      });

      // git graph — commits landing on main, a branch merging back
      const gx0 = 596, gy0 = 18;
      for (let i = 0; i < 7; i++) {
        const y = gy0 + i * 17;
        pix(gx0, y, 1, 1, inkA('.22')); pix(gx0, y + 6, 1, 1, inkA('.22')); pix(gx0, y + 12, 1, 1, inkA('.22'));
        const live = i === (fr % 7);
        pix(gx0 - 1, y, 2, 2, live ? 'rgba(' + self.rgbAccent() + ',.95)' : inkA('.4'));
        ctx.fillStyle = inkA(live ? '.5' : '.22');
        ctx.fillRect(gx0 + 14, y + 1, 48 + Math.round(rnd(i * 5) * 40), 3);
        if (i === 2 || i === 3) {
          pix(gx0 + 24, y + (i === 2 ? -5 : 5), 1, 1, inkA('.3'));
          pix(gx0 + 30, y, 2, 2, i === 3 ? 'rgba(' + self.rgbAccent() + ',.6)' : inkA('.35'));
        }
      }
    };
    const first = function () { if (canvas.width && canvas.width !== 300) draw(performance.now(), true); };
    const s0 = stripFor();
    if (s0.complete && s0.naturalWidth) first();
    else s0.addEventListener('load', first, { once: true });
    document.addEventListener('visibilitychange', function () { if (!document.hidden) first(); });
    this._raf.dev = this.schedule(draw);
  };

  // data flowing between the columns, drawn as the same square pixels as the
  // page ground: ADAM → inputs → developer → finished software
  Scene.prototype.initFlow = function (canvas) {
    if (!canvas) return;
    const self = this;
    const ctx = canvas.getContext('2d', { alpha: true });
    const CELL = 2.5;
    const spritesFor = function () {
      if (self._sprites && self._spriteTheme === self.themeName()) return self._sprites;
      const sfx = self.themeName() === 'Light' ? '-light' : '';
      const load = function (n) { const i = new Image(); i.src = self.asset('assets/' + n + sfx + '.png'); return i; };
      self._spriteTheme = self.themeName();
      self._sprites = {
        in: ['in-algorithms', 'in-documents', 'in-code', 'in-designs', 'in-algorithms'].map(load),
        out: ['out-web', 'out-mobile', 'out-api', 'out-cloud', 'out-docs'].map(load)
      };
      return self._sprites;
    };
    let w = 0, h = 0, paths = [], labels = [], dpr = 1;

    const measure = function () {
      const host = canvas.parentElement;
      if (!host) return;
      const hr = host.getBoundingClientRect();
      if (!hr.width || !hr.height) return;
      dpr = Math.min(2, window.devicePixelRatio || 1);
      w = hr.width; h = hr.height;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const box = function (el) {
        const r = el.getBoundingClientRect();
        return { x: r.left - hr.left, y: r.top - hr.top, w: r.width, h: r.height };
      };
      const SP = spritesFor();
      self._flowTheme = self.themeName();
      const src = host.querySelector('[data-focus="src"]');
      const hub = host.querySelector('[data-focus="hub"]');
      const dst = host.querySelector('[data-focus="dst"]');
      if (!src || !hub || !dst) { paths = []; labels = []; return; }
      const S = box(src), H = box(hub), D = box(dst);
      // one shared centre line, so the streams read as level
      const mid = (S.y + S.h / 2 + H.y + H.h / 2 + D.y + D.h / 2) / 3;
      const PAD = 26;
      // five lanes converge out of ADAM into one point at the developer, then
      // one point fans back out into five lanes to the product
      const sO = { x: S.x + S.w + PAD, y: mid };
      const hI = { x: H.x - PAD, y: mid };
      const hO = { x: H.x + H.w + PAD, y: mid };
      const dI = { x: D.x - PAD, y: mid };
      const next = [];
      const spread = Math.min(190, H.h * 0.8);
      for (let i = 0; i < 5; i++) {
        const off = (i - 2) * (spread / 4);
        next.push({ a: { x: sO.x, y: sO.y + off }, b: hI, accent: false, seed: i * 0.2, sprite: SP.in[i % SP.in.length] });
        next.push({ a: hO, b: { x: dI.x, y: dI.y + off }, accent: true, seed: 0.5 + i * 0.2, sprite: SP.out[i % SP.out.length] });
      }
      // stream captions, so the diagram explains itself
      labels = [
        { x: (sO.x + hI.x) / 2, y: mid - spread / 2 - 30, t: 'DATA IN', s: 'YOUR INPUT' },
        { x: (hO.x + dI.x) / 2, y: mid - spread / 2 - 30, t: 'PROCESSING', s: 'AI + ENGINEERING' }
      ];
      paths = next;
    };
    if (window.ResizeObserver) {
      const host = canvas.parentElement;
      if (host) { this._ro.flow = new ResizeObserver(measure); this._ro.flow.observe(host); }
    }
    const measureUntil = function () { measure(); if (!w) self.schedule(measureUntil); };
    measureUntil();
    this.remeasureFlow = measure;

    const draw = function (now, once) {
      if (!once) self._raf.flow = self.schedule(draw);
      if (!canvas.isConnected) return;
      if (self._flowTheme !== self.themeName()) measure();
      if (!w || !paths.length) return;
      const r = canvas.getBoundingClientRect();
      if (r.bottom < -200 || r.top > window.innerHeight + 200) { ctx.clearRect(0, 0, w, h); return; }
      const ink = self.rgbInk(), acc = self.rgbAccent();
      const L = self.loopPhase(now);
      ctx.clearRect(0, 0, w, h);
      ctx.textAlign = 'center';
      ctx.textBaseline = 'alphabetic';
      for (let i = 0; i < labels.length; i++) {
        const lb = labels[i];
        ctx.font = "500 10px 'JetBrains Mono', monospace";
        ctx.fillStyle = 'rgba(' + ink + ',.62)';
        ctx.fillText(lb.t.split('').join(' '), lb.x, lb.y);
        ctx.font = "400 9px 'JetBrains Mono', monospace";
        ctx.fillStyle = 'rgba(' + ink + ',.34)';
        ctx.fillText(lb.s.split('').join(' '), lb.x, lb.y + 13);
      }
      ctx.textAlign = 'left';
      for (let p = 0; p < paths.length; p++) {
        const path = paths[p];
        const ax = path.a.x, ay = path.a.y, bx = path.b.x, by = path.b.y;
        const mx = (ax + bx) / 2;
        const rgb = path.accent ? acc : ink;
        // static dotted spine
        const DOTS = 44;
        for (let s = 0; s <= DOTS; s++) {
          const u = s / DOTS, iu = 1 - u;
          const x = iu * iu * iu * ax + 3 * iu * iu * u * mx + 3 * iu * u * u * mx + u * u * u * bx;
          const y = iu * iu * iu * ay + 3 * iu * iu * u * ay + 3 * iu * u * u * by + u * u * u * by;
          ctx.fillStyle = 'rgba(' + rgb + ',' + (path.accent ? 0.3 : 0.22) + ')';
          ctx.fillRect(Math.round(x), Math.round(y), CELL, CELL);
        }
        // the artefact sprite itself rides the path
        if (path.sprite && path.sprite.complete && path.sprite.naturalWidth) {
          const u = (L.p + path.seed) % 1;
          const iu = 1 - u;
          const x = iu * iu * iu * ax + 3 * iu * iu * u * mx + 3 * iu * u * u * mx + u * u * u * bx;
          const y = iu * iu * iu * ay + 3 * iu * iu * u * ay + 3 * iu * u * u * by + u * u * u * by;
          const fade = Math.min(1, Math.sin(u * Math.PI) * 1.9);
          if (fade > 0.02) {
            const sp = path.sprite;
            const sh = 36, sw = Math.round(sh * (sp.naturalWidth / sp.naturalHeight));
            ctx.globalAlpha = fade;
            ctx.imageSmoothingEnabled = false;
            ctx.drawImage(sp, Math.round(x - sw / 2), Math.round(y - sh / 2), sw, sh);
            ctx.globalAlpha = 1;
          }
        }
      }
    };
    const flowFirst = function () { if (w && paths.length) draw(performance.now(), true); };
    document.addEventListener('visibilitychange', function () { if (!document.hidden) flowFirst(); });
    setTimeout(flowFirst, 60);
    this._raf.flow = this.schedule(draw);
  };

  Scene.prototype.start = function () {
    const r = this.root;
    if (!r) return this;
    this.initAdam(r.querySelector('[data-scene="adam"]'));
    this.initDev(r.querySelector('[data-scene="dev"]'));
    this.initOut(r.querySelector('[data-scene="out"]'));
    this.initFlow(r.querySelector('[data-scene="flow"]'));
    return this;
  };

  Scene.prototype.stop = function () {
    const self = this;
    Object.keys(this._raf).forEach(function (k) { self.unschedule(self._raf[k]); });
    Object.keys(this._ro).forEach(function (k) { self._ro[k].disconnect(); });
    this._raf = {}; this._ro = {};
  };

  Scene.prototype.setTheme = function (name) {
    this.theme = name === 'Dark' ? 'Dark' : 'Light';
    this._adamMark = null; this._outArt = null; this._devStrip = null; this._sprites = null;
    if (this.remeasureFlow) this.remeasureFlow();
  };

  window.AdamFlow = {
    start: function (opts) { return new Scene(opts).start(); }
  };
})();
