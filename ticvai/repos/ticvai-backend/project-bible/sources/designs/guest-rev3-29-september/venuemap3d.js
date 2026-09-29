import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const MAT = {};
const mat = (c, rough) => (MAT[c + '|' + (rough == null ? 0.6 : rough)] = MAT[c + '|' + (rough == null ? 0.6 : rough)] || new THREE.MeshStandardMaterial({ color: c, roughness: rough == null ? 0.6 : rough, metalness: 0.04 }));

const KIND = {
  ride: '#f0a01e', show: '#c77dff', dining: '#e2603a', shop: '#7d8ea3',
  parking: '#4c9be8', service: '#4cc38a', gate: '#e8e2d6', queue: '#f0a01e'
};

function walker(color, scale) {
  const m = mat(color, 0.5);
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.09, 0.5, 3, 6), m); body.position.y = 0.95; g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.15, 10, 8), m); head.position.y = 1.38; g.add(head);
  const legL = new THREE.Group(), legR = new THREE.Group();
  [legL, legR].forEach((l, i) => {
    const s = new THREE.Mesh(new THREE.CapsuleGeometry(0.07, 0.5, 3, 6), m);
    s.position.y = -0.28; l.add(s); l.position.set(i ? 0.09 : -0.09, 0.68, 0); g.add(l);
  });
  g.scale.setScalar(scale || 1);
  return { group: g, legL, legR };
}

class VenueMap3D extends HTMLElement {
  static get observedAttributes() { return ['venue', 'accent', 'pins', 'selected', 'ground', 'route', 'progress', 'follow']; }

  connectedCallback() {
    if (this._built) {
      if (this._stop) { this._stop = false; if (this._renderer) { this._build(); this._loop(); } }
      return;
    }
    this._built = true;
    this._shadow = this.attachShadow({ mode: 'open' });
    this._shadow.innerHTML = `
      <style>
        :host { display:block; position:relative; min-height:360px; }
        canvas { display:block; width:100%; height:100%; touch-action:pan-y; cursor:grab; }
        canvas.picking { cursor:pointer; }
        .hint { position:absolute; left:11px; bottom:10px; font:700 10px/1.2 system-ui,sans-serif; letter-spacing:.12em;
                text-transform:uppercase; color:rgba(255,255,255,.72); pointer-events:none; }
        .zoom { position:absolute; right:10px; bottom:10px; display:flex; gap:6px; }
        .zoom button { width:30px; height:30px; padding:0; border-radius:8px; cursor:pointer; font:700 15px/1 system-ui,sans-serif;
                       color:#fff; background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.28); backdrop-filter:blur(6px); }
        .zoom button:hover { background:rgba(255,255,255,.26); }
        .tag { position:absolute; left:0; top:0; transform:translate(-50%,-140%); pointer-events:none; white-space:nowrap;
               font:700 11px/1.3 system-ui,sans-serif; color:#fff; background:rgba(12,16,24,.82); border:1px solid rgba(255,255,255,.22);
               padding:4px 9px; border-radius:7px; opacity:0; transition:opacity .15s ease; backdrop-filter:blur(6px); }
        .tag.on { opacity:1; }
        .tag i { font-style:normal; opacity:.72; font-weight:500; }
      </style>
      <div class="hint">Drag to orbit &middot; tap a pin</div>
      <div class="tag"></div>
      <div class="zoom">
        <button type="button" data-z="out" aria-label="Zoom out">&minus;</button>
        <button type="button" data-z="in" aria-label="Zoom in">+</button>
      </div>`;
    this._tag = this._shadow.querySelector('.tag');
    this._io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { this._start(); this._io.disconnect(); } }), { rootMargin: '150px' });
    this._io.observe(this);
    // the observer can miss an element that mounts at zero height; start anyway
    setTimeout(() => { if (!this._renderer && !this._stop) { this._start(); this._io && this._io.disconnect(); } }, 400);
  }

  disconnectedCallback() {
    this._stop = true;
    if (this._raf) cancelAnimationFrame(this._raf);
  }

  attributeChangedCallback(n) {
    if (!this._scene) return;
    if (n === 'selected') { this._paintPins(); return; }
    if (n === 'route') { this._routeLine(); return; }
    if (n === 'progress') return;
    if (n === 'follow') {
      const on = this.getAttribute('follow') === '1';
      if (this._controls) { this._controls.autoRotate = !on; }
      if (!on && this._cam) { this._cam.position.set(104, 108, 150); this._controls.target.set(0, 5, 0); this._controls.update(); }
      return;
    }
    this._build();
  }

  _size() { const w = this.clientWidth || 620; return { w, h: Math.max(360, Math.min(620, Math.round(w * 0.54))) }; }

  _start() {
    const { w, h } = this._size();
    const r = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    r.setPixelRatio(Math.min(devicePixelRatio, 2));
    r.setSize(w, h, false);
    r.outputColorSpace = THREE.SRGBColorSpace;
    this._shadow.appendChild(r.domElement);
    this._renderer = r;

    const sky = this.getAttribute('ground') || '#0e1826';
    const sc = new THREE.Scene();
    sc.background = new THREE.Color(sky);
    sc.fog = new THREE.Fog(sky, 190, 520);
    this._scene = sc;

    const cam = new THREE.PerspectiveCamera(38, w / h, 0.5, 2600);
    cam.position.set(104, 108, 150);
    this._cam = cam;

    sc.add(new THREE.HemisphereLight('#d9e9ff', '#1d2634', 1.15));
    const key = new THREE.DirectionalLight('#fff4e2', 1.4); key.position.set(90, 160, 70); sc.add(key);
    const rim = new THREE.DirectionalLight('#79b2ff', 0.5); rim.position.set(-110, 60, -95); sc.add(rim);

    const c = new OrbitControls(cam, r.domElement);
    c.enableDamping = true; c.dampingFactor = 0.08;
    c.maxPolarAngle = Math.PI * 0.46; c.minDistance = 80; c.maxDistance = 420;
    c.autoRotate = true; c.autoRotateSpeed = 0.35;
    c.enableZoom = false;
    c.enablePan = false;
    c.target.set(0, 5, 0);
    this._controls = c;

    this._shadow.querySelectorAll('.zoom button').forEach(b => {
      b.addEventListener('click', () => {
        const dir = b.getAttribute('data-z') === 'in' ? 0.82 : 1.22;
        const v = cam.position.clone().sub(c.target);
        const len = Math.min(c.maxDistance, Math.max(c.minDistance, v.length() * dir));
        cam.position.copy(c.target.clone().add(v.setLength(len)));
        c.update();
      });
    });

    const el = r.domElement;
    let downAt = null, dragged = false;
    el.addEventListener('pointerdown', e => { c.autoRotate = false; downAt = { x: e.clientX, y: e.clientY }; dragged = false; });
    el.addEventListener('pointermove', e => {
      if (downAt && (Math.abs(e.clientX - downAt.x) > 4 || Math.abs(e.clientY - downAt.y) > 4)) dragged = true;
      this._setHover(this._cast(e));
    });
    el.addEventListener('pointerup', e => { if (!dragged) this._pick(e); downAt = null; });
    el.addEventListener('pointerleave', () => { downAt = null; this._setHover(null); });

    this._raycaster = new THREE.Raycaster();
    this._pointer = new THREE.Vector2();
    this._clock = new THREE.Clock();
    this._build();
    this._loop();

    this._ro = new ResizeObserver(() => {
      const s = this._size();
      r.setSize(s.w, s.h, false);
      cam.aspect = s.w / s.h; cam.updateProjectionMatrix();
    });
    this._ro.observe(this);
  }

  // ---------- massing ----------
  _build() {
    const sc = this._scene;
    if (this._root) sc.remove(this._root);
    const root = new THREE.Group();
    this._root = root;
    this._pins = [];
    this._actors = [];
    this._spin = [];
    this._coaster = null; this._tower = null; this._water_ = null;
    sc.add(root);

    this._accent = this.getAttribute('accent') || '#c07c1e';
    const venue = this.getAttribute('venue') || 'park';
    const S = 1.9;
    this._S = S;
    this._px = v => (v - 50) * S;
    this._pz = v => (v - 50) * S;

    const groundTone = { park: '#1b2a1e', water: '#123043', stadium: '#141c29', theatre: '#1d1826', dining: '#241d17' }[venue] || '#141c29';
    const ground = new THREE.Mesh(new THREE.CircleGeometry(190, 56), mat(groundTone, 0.95));
    ground.rotation.x = -Math.PI / 2; ground.position.y = -0.4;
    root.add(ground);

    this._plan = (window.TICVAI_PLAN || {})[venue] || null;
    if (this._plan) this._plan.routes.forEach(r => this._path(root, r.pts, 5.4, venue === 'dining' ? '#33291f' : (venue === 'theatre' ? '#332d42' : (venue === 'water' ? '#3c4a52' : '#39413a'))));

    ({
      park: () => this._park(root),
      water: () => this._water(root),
      stadium: () => this._stadium(root),
      theatre: () => this._theatre(root),
      dining: () => this._dining(root)
    }[venue] || (() => this._park(root)))();

    this._addPins(root);
    this._crowd(root, venue);
    this._routeLine();
  }

  _path(root, pts, width, color, y) {
    const S = this._S;
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1];
      const ax = this._px(a[0]), az = this._pz(a[1]), bx = this._px(b[0]), bz = this._pz(b[1]);
      const len = Math.hypot(bx - ax, bz - az);
      const seg = new THREE.Mesh(new THREE.BoxGeometry(len + width * S * 0.6, 0.24, width * S), mat(color || '#3a4636', 0.95));
      seg.position.set((ax + bx) / 2, (y == null ? 0.03 : y), (az + bz) / 2);
      seg.rotation.y = -Math.atan2(bz - az, bx - ax);
      root.add(seg);
    }
  }

  _box(root, x, y, w, d, h, color, rough, lift) {
    const S = this._S;
    const m = new THREE.Mesh(new THREE.BoxGeometry(w * S, h, d * S), mat(color, rough));
    m.position.set(this._px(x + w / 2), h / 2 + (lift || 0), this._pz(y + d / 2));
    root.add(m);
    return m;
  }

  // a real building: shell, glazing bands, parapet, roof plant, entrance canopy
  _bldg(root, x, y, w, d, h, o) {
    const S = this._S, op = o || {};
    const wall = op.wall || '#5b6472';
    const glass = op.glass || '#9fd6ff';
    const W = w * S, D = d * S;
    const cx = this._px(x + w / 2), cz = this._pz(y + d / 2);

    const shell = new THREE.Mesh(new THREE.BoxGeometry(W, h, D), mat(wall, 0.82));
    shell.position.set(cx, h / 2, cz);
    root.add(shell);

    // glazing bands, one per floor, proud of all four faces
    const floors = Math.max(1, Math.round(h / (op.floor || 4.2)));
    const gm = new THREE.MeshStandardMaterial({ color: glass, roughness: 0.16, metalness: 0.3, emissive: new THREE.Color(glass), emissiveIntensity: op.lit == null ? 0.22 : op.lit });
    for (let f = 0; f < floors; f++) {
      const fy = (h / floors) * (f + 0.55);
      if (fy > h - 0.6) continue;
      const bandH = Math.min(1.5, (h / floors) * 0.42);
      const bz = new THREE.Mesh(new THREE.BoxGeometry(W * 0.86, bandH, D + 0.5), gm);
      bz.position.set(cx, fy, cz); root.add(bz);
      const bx = new THREE.Mesh(new THREE.BoxGeometry(W + 0.5, bandH, D * 0.86), gm);
      bx.position.set(cx, fy, cz); root.add(bx);
    }

    // parapet
    const par = new THREE.Mesh(new THREE.BoxGeometry(W + 1.2, 1.1, D + 1.2), mat(op.trim || '#39424f', 0.7));
    par.position.set(cx, h + 0.5, cz); root.add(par);

    // roof plant
    if (op.plant !== false) {
      for (let i = 0; i < 3; i++) {
        const p = new THREE.Mesh(new THREE.BoxGeometry(2.4 + (i % 2) * 1.6, 1.6, 2.2), mat('#4b5563', 0.85));
        p.position.set(cx + (i - 1) * W * 0.24, h + 1.8, cz + ((i % 2) ? 1 : -1) * D * 0.2);
        root.add(p);
      }
    }

    // entrance canopy on the +z face
    if (op.entry !== false) {
      const can = new THREE.Mesh(new THREE.BoxGeometry(W * 0.42, 0.5, 5.5), mat(op.canopy || this._accent, 0.5));
      can.position.set(cx, 5.2, cz + D / 2 + 2.4); root.add(can);
      [-1, 1].forEach(sg => {
        const col = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 5, 8), mat('#c9c5bd', 0.6));
        col.position.set(cx + sg * W * 0.17, 2.5, cz + D / 2 + 4.6); root.add(col);
      });
    }
    return { cx, cz, W, D, h };
  }

  _tree(root, x, y, s) {
    const sc = s || 1;
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.34 * sc, 0.5 * sc, 3.4 * sc, 7), mat('#4a3b2a', 0.9));
    trunk.position.set(this._px(x), 1.7 * sc, this._pz(y)); root.add(trunk);
    for (let i = 0; i < 2; i++) {
      const c = new THREE.Mesh(new THREE.ConeGeometry((3 - i * 0.9) * sc, (4.4 - i) * sc, 8), mat(i ? '#3f7d52' : '#2f5d3f', 0.92));
      c.position.set(trunk.position.x, (4.6 + i * 2.2) * sc, trunk.position.z); root.add(c);
    }
  }

  _palm(root, x, y) {
    const t = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.55, 9, 7), mat('#6b5a42', 0.9));
    t.position.set(this._px(x), 4.5, this._pz(y)); root.add(t);
    for (let i = 0; i < 7; i++) {
      const a = (i / 7) * Math.PI * 2;
      const f = new THREE.Mesh(new THREE.BoxGeometry(6, 0.22, 1.5), mat('#3f7d52', 0.9));
      f.position.set(t.position.x + Math.cos(a) * 2.8, 9.2, t.position.z + Math.sin(a) * 2.8);
      f.rotation.y = -a; f.rotation.z = 0.24; root.add(f);
    }
  }

  _lamp(root, x, y) {
    const p = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 7, 6), mat('#8b94a3', 0.7));
    p.position.set(this._px(x), 3.5, this._pz(y)); root.add(p);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.7, 10, 8), new THREE.MeshStandardMaterial({ color: '#fff3d0', emissive: new THREE.Color('#ffd98a'), emissiveIntensity: 0.9, roughness: 0.3 }));
    head.position.set(p.position.x, 7.2, p.position.z); root.add(head);
  }

  _car(root, x, y, rot, color) {
    const g = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(4.4, 1.3, 2.1), mat(color || '#7d8ea3', 0.5));
    body.position.y = 0.95; g.add(body);
    const cab = new THREE.Mesh(new THREE.BoxGeometry(2.3, 1.1, 1.9), mat('#2b3340', 0.35));
    cab.position.set(-0.2, 2.1, 0); g.add(cab);
    [[1.5, 1], [1.5, -1], [-1.5, 1], [-1.5, -1]].forEach(w => {
      const t = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 0.4, 10), mat('#1b1f26', 0.9));
      t.rotation.x = Math.PI / 2; t.position.set(w[0], 0.5, w[1]); g.add(t);
    });
    g.position.set(this._px(x), 0, this._pz(y));
    g.rotation.y = rot || 0;
    root.add(g);
  }

  _fence(root, pts, color) {
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1];
      const ax = this._px(a[0]), az = this._pz(a[1]), bx = this._px(b[0]), bz = this._pz(b[1]);
      const len = Math.hypot(bx - ax, bz - az);
      const rail = new THREE.Mesh(new THREE.BoxGeometry(len, 0.18, 0.18), mat(color || '#6b7482', 0.7));
      rail.position.set((ax + bx) / 2, 1.5, (az + bz) / 2);
      rail.rotation.y = -Math.atan2(bz - az, bx - ax);
      root.add(rail);
      const n = Math.max(2, Math.round(len / 7));
      for (let k = 0; k <= n; k++) {
        const p = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 1.8, 6), mat(color || '#6b7482', 0.7));
        p.position.set(ax + (bx - ax) * (k / n), 0.9, az + (bz - az) * (k / n)); root.add(p);
      }
    }
  }

  _plaza(root, x, y, r, color) {
    const p = new THREE.Mesh(new THREE.CircleGeometry(r, 40), mat(color || '#3a4048', 0.95));
    p.rotation.x = -Math.PI / 2; p.position.set(this._px(x), 0.02, this._pz(y)); root.add(p);
    return p;
  }

  _carpark(root, x, y, cols, rows, rot) {
    const pad = this._box(root, x, y, cols * 3.4, rows * 6, 0.3, '#2b3138', 0.95);
    void pad;
    const colors = ['#8d99ab', '#b8412f', '#e8e2d6', '#4c6b8a', '#6e7684'];
    for (let c = 0; c < cols; c++) {
      for (let r = 0; r < rows; r++) {
        if ((c + r) % 3 === 2) continue;
        this._car(root, x + 1.7 + c * 3.4, y + 3 + r * 6, rot || 0, colors[(c * 3 + r) % colors.length]);
      }
    }
  }

  // ---------------- theme park ----------------
  _park(root) {
    this._plaza(root, 50, 50, 22, '#3c443c');

    // main entrance building with turnstile wing
    this._bldg(root, 40, 4, 20, 9, 11, { wall: '#57606e', glass: '#ffe6ae', canopy: this._accent, floor: 5 });
    this._box(root, 34, 6, 5, 5, 6, '#4a5261', 0.85);
    this._box(root, 61, 6, 5, 5, 6, '#4a5261', 0.85);

    // coaster: tube track over a lift hill, with support bents and a train
    const P = [[24, 30, 2], [30, 24, 27], [38, 20, 12], [46, 22, 31], [52, 30, 9], [46, 38, 20], [36, 42, 6], [28, 38, 16], [24, 30, 2]];
    const curve = new THREE.CatmullRomCurve3(P.map(p => new THREE.Vector3(this._px(p[0]), p[2], this._pz(p[1]))), true);
    const track = new THREE.Mesh(new THREE.TubeGeometry(curve, 190, 0.62, 8, true), mat(this._accent, 0.42));
    root.add(track);
    const rail = new THREE.Mesh(new THREE.TubeGeometry(curve, 190, 0.24, 6, true), mat('#e8e2d6', 0.5));
    rail.position.y = 1.2; root.add(rail);
    for (let i = 0; i < 26; i++) {
      const p = curve.getPoint(i / 26);
      if (p.y < 3) continue;
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.42, p.y, 6), mat('#55606e', 0.8));
      leg.position.set(p.x, p.y / 2, p.z); root.add(leg);
    }
    const train = new THREE.Group();
    for (let i = 0; i < 3; i++) {
      const car = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.5, 1.9), mat(i ? '#ffe27a' : '#ff6b3d', 0.4));
      car.position.x = i * -3; train.add(car);
    }
    root.add(train);
    this._coaster = { curve, car: train };
    this._box(root, 20, 28, 9, 7, 5, '#4a5261', 0.85);   // station shed

    // drop tower with a lattice mast
    const tb = this._box(root, 64, 28, 7, 7, 3, '#4a5261', 0.85);
    void tb;
    const mast = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 2.2, 46, 10), mat('#6b7482', 0.7));
    mast.position.set(this._px(67.5), 23, this._pz(31.5)); root.add(mast);
    for (let i = 0; i < 5; i++) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(2.6, 0.16, 6, 18), mat('#8b94a3', 0.7));
      ring.rotation.x = -Math.PI / 2; ring.position.set(mast.position.x, 8 + i * 9, mast.position.z); root.add(ring);
    }
    const carr = new THREE.Mesh(new THREE.TorusGeometry(3.8, 1, 8, 20), mat(this._accent, 0.4));
    carr.rotation.x = -Math.PI / 2; carr.position.set(mast.position.x, 30, mast.position.z);
    root.add(carr); this._tower = carr;

    // carousel under a canopy
    const base = new THREE.Mesh(new THREE.CylinderGeometry(8, 8.4, 1.6, 26), mat('#3d4a5c', 0.85));
    base.position.set(this._px(34), 0.8, this._pz(64)); root.add(base);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(9.4, 6.5, 18), mat(this._accent, 0.5));
    roof.position.set(base.position.x, 10, base.position.z); root.add(roof);
    this._spin.push(roof);
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2;
      const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 6, 6), mat('#e8e2d6', 0.6));
      pole.position.set(base.position.x + Math.cos(a) * 6.6, 4.6, base.position.z + Math.sin(a) * 6.6); root.add(pole);
    }

    // dining hall, arcade shed and retail parade
    this._bldg(root, 58, 56, 18, 12, 9, { wall: '#6a5442', glass: '#ffd79a', canopy: '#e2603a', floor: 4.5 });
    this._bldg(root, 16, 56, 13, 10, 8, { wall: '#4f5867', glass: '#bfe4ff', canopy: '#4c9be8' });
    for (let i = 0; i < 4; i++) {
      this._box(root, 30 + i * 7, 74, 6, 7, 5.5, i % 2 ? '#5a6374' : '#4f5867', 0.85);
      const awn = new THREE.Mesh(new THREE.BoxGeometry(6 * this._S, 0.3, 2.6), mat(i % 2 ? this._accent : '#e8e2d6', 0.6));
      awn.position.set(this._px(33 + i * 7), 5.2, this._pz(81.4)); root.add(awn);
    }

    // water feature on the central plaza
    const pond = new THREE.Mesh(new THREE.CircleGeometry(9, 30), mat('#1b7fa8', 0.25));
    pond.rotation.x = -Math.PI / 2; pond.position.set(this._px(50), 0.06, this._pz(50)); root.add(pond);
    const jet = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 1.4, 7, 10), new THREE.MeshStandardMaterial({ color: '#cfefff', roughness: 0.2, transparent: true, opacity: 0.7 }));
    jet.position.set(pond.position.x, 3.5, pond.position.z); root.add(jet);

    this._carpark(root, 78, 62, 6, 4, Math.PI / 2);
    this._fence(root, [[8, 14], [92, 14], [94, 90], [8, 92], [8, 14]]);
    [[12, 30], [14, 44], [20, 72], [44, 88], [60, 86], [78, 40], [86, 30], [74, 18], [26, 14], [58, 24], [42, 52], [56, 44]].forEach(t => this._tree(root, t[0], t[1], 1 + ((t[0] + t[1]) % 3) * 0.18));
    [[50, 22], [50, 40], [50, 64], [34, 50], [66, 50], [24, 66]].forEach(l => this._lamp(root, l[0], l[1]));
  }

  // ---------------- water park ----------------
  _water(root) {
    const pool = new THREE.Mesh(new THREE.CircleGeometry(30, 44), mat('#1b7fa8', 0.22));
    pool.rotation.x = -Math.PI / 2; pool.position.set(this._px(40), 0.06, this._pz(54));
    root.add(pool); this._water_ = pool;
    const deck = new THREE.Mesh(new THREE.TorusGeometry(32, 2.4, 8, 46), mat('#d9d2c4', 0.9));
    deck.rotation.x = -Math.PI / 2; deck.position.set(pool.position.x, 0.2, pool.position.z); root.add(deck);

    const river = new THREE.Mesh(new THREE.TorusGeometry(54, 4.8, 10, 50), mat('#2494bd', 0.22));
    river.rotation.x = -Math.PI / 2; river.position.y = 0.3; root.add(river);
    for (let i = 0; i < 9; i++) {
      const a = (i / 9) * Math.PI * 2;
      const ring = new THREE.Mesh(new THREE.TorusGeometry(1.9, 0.55, 7, 14), mat(i % 2 ? '#ffe27a' : '#ff6b3d', 0.5));
      ring.rotation.x = -Math.PI / 2;
      ring.position.set(Math.cos(a) * 54, 0.9, Math.sin(a) * 54); root.add(ring);
    }

    // slide towers: stair core, platforms, helical flumes
    [[70, 24, 36, '#22c8d8'], [80, 44, 27, null]].forEach((t, ti) => {
      const [x, y, h, col] = t;
      const core = this._bldg(root, x, y, 6, 6, h, { wall: '#54606f', glass: '#bfe4ff', entry: false, plant: false, floor: 6 });
      for (let f = 1; f * 7 < h; f++) {
        const plat = new THREE.Mesh(new THREE.BoxGeometry(core.W + 5, 0.5, core.D + 5), mat('#6b7482', 0.8));
        plat.position.set(core.cx, f * 7, core.cz); root.add(plat);
      }
      const pts = [];
      for (let i = 0; i <= 70; i++) {
        const a = (i / 70) * Math.PI * 3.4;
        const rr = 3 + (i / 70) * 18;
        pts.push(new THREE.Vector3(core.cx + Math.cos(a) * rr, h - (i / 70) * (h - 1.6), core.cz + Math.sin(a) * rr));
      }
      const flume = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 110, 1.35, 9, false), mat(col || this._accent, 0.34));
      root.add(flume);
      const splash = new THREE.Mesh(new THREE.CircleGeometry(7, 24), mat('#2494bd', 0.25));
      splash.rotation.x = -Math.PI / 2;
      splash.position.set(pts[70].x, 0.1, pts[70].z); root.add(splash);
      void ti;
    });

    // cabana row with pitched roofs and loungers
    for (let i = 0; i < 8; i++) {
      const x = 13 + i * 5.4;
      this._box(root, x, 74, 3.8, 4, 3.2, '#6b5a49', 0.88);
      const roof = new THREE.Mesh(new THREE.ConeGeometry(4.4, 2.6, 4), mat(i % 2 ? '#e8e2d6' : this._accent, 0.7));
      roof.rotation.y = Math.PI / 4;
      roof.position.set(this._px(x + 1.9), 4.6, this._pz(76)); root.add(roof);
      const lg = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.4, 1.4), mat('#e8e2d6', 0.8));
      lg.position.set(this._px(x + 1.9), 0.6, this._pz(70)); lg.rotation.z = 0.14; root.add(lg);
    }

    // entrance pavilion, changing block, canteen
    this._bldg(root, 16, 12, 18, 9, 10, { wall: '#4f5867', glass: '#ffe6ae', canopy: this._accent, floor: 5 });
    this._bldg(root, 46, 12, 14, 8, 7, { wall: '#5a6374', glass: '#bfe4ff', canopy: '#4c9be8' });
    this._bldg(root, 62, 66, 14, 10, 8, { wall: '#6a5442', glass: '#ffd79a', canopy: '#e2603a' });

    this._carpark(root, 82, 58, 5, 4, Math.PI / 2);
    [[18, 30], [22, 44], [30, 22], [60, 82], [46, 86], [74, 76], [86, 30], [12, 62]].forEach(p => this._palm(root, p[0], p[1]));
    [[40, 26], [40, 82], [20, 54], [62, 54]].forEach(l => this._lamp(root, l[0], l[1]));
  }

  // ---------------- stadium ----------------
  _stadium(root) {
    const pitch = new THREE.Mesh(new THREE.BoxGeometry(42 * this._S, 0.5, 30 * this._S), mat('#2f6b3a', 0.95));
    pitch.position.set(0, 0.25, 0); root.add(pitch);
    for (let i = 0; i < 7; i++) {
      const stripe = new THREE.Mesh(new THREE.BoxGeometry(42 * this._S / 7, 0.06, 30 * this._S), mat(i % 2 ? '#356f3f' : '#2b6335', 0.95));
      stripe.position.set(-42 * this._S / 2 + (i + 0.5) * (42 * this._S / 7), 0.53, 0); root.add(stripe);
    }
    const circle = new THREE.Mesh(new THREE.TorusGeometry(7, 0.3, 6, 40), mat('#eef4ee', 0.6));
    circle.rotation.x = -Math.PI / 2; circle.position.y = 0.58; root.add(circle);
    [[-1, 0], [1, 0]].forEach(s => {
      const box = new THREE.Mesh(new THREE.BoxGeometry(8, 0.1, 26), mat('#eef4ee', 0.6));
      box.position.set(s[0] * (42 * this._S / 2 - 4), 0.58, 0); root.add(box);
    });

    // two tiers of stands plus corner infill
    for (let i = 0; i < 28; i++) {
      const a = (i / 28) * Math.PI * 2;
      const lower = new THREE.Mesh(new THREE.BoxGeometry(10, 9, 8), mat(i % 7 === 0 ? this._accent : '#58657a', 0.78));
      lower.position.set(Math.cos(a) * 50, 4.5, Math.sin(a) * 50 * 0.8);
      lower.rotation.y = -a; root.add(lower);
      const upper = new THREE.Mesh(new THREE.BoxGeometry(10, 11, 7), mat('#44506180'.slice(0, 7), 0.8));
      upper.position.set(Math.cos(a) * 60, 15, Math.sin(a) * 60 * 0.8);
      upper.rotation.y = -a; root.add(upper);
      // seat rows as thin bands
      const seats = new THREE.Mesh(new THREE.BoxGeometry(9.2, 0.4, 7.4), mat(i % 3 ? '#8d99ab' : '#b9c4d4', 0.85));
      seats.position.set(Math.cos(a) * 50, 9.3, Math.sin(a) * 50 * 0.8);
      seats.rotation.y = -a; root.add(seats);
    }
    const roof = new THREE.Mesh(new THREE.TorusGeometry(64, 3.2, 10, 46), mat('#39424f', 0.6));
    roof.rotation.x = -Math.PI / 2; roof.position.y = 27; roof.scale.z = 0.8; root.add(roof);
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2;
      const mastH = 30;
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.9, mastH, 8), mat('#4b5563', 0.7));
      m.position.set(Math.cos(a) * 64, mastH / 2, Math.sin(a) * 64 * 0.8); root.add(m);
    }
    // floodlights
    [[1, 1], [1, -1], [-1, 1], [-1, -1]].forEach(c => {
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 1.1, 40, 8), mat('#6b7482', 0.7));
      p.position.set(c[0] * 62, 20, c[1] * 50); root.add(p);
      const rig = new THREE.Mesh(new THREE.BoxGeometry(9, 5, 1.2), new THREE.MeshStandardMaterial({ color: '#fff6dd', emissive: new THREE.Color('#ffe9a8'), emissiveIntensity: 0.8, roughness: 0.3 }));
      rig.position.set(c[0] * 62, 41, c[1] * 50); rig.lookAt(0, 10, 0); root.add(rig);
    });
    // concourse ring and approach
    const conc = new THREE.Mesh(new THREE.TorusGeometry(76, 5, 8, 46), mat('#333b46', 0.95));
    conc.rotation.x = -Math.PI / 2; conc.position.y = 0.1; conc.scale.z = 0.84; root.add(conc);
    this._bldg(root, 84, 42, 12, 14, 12, { wall: '#4f5867', glass: '#bfe4ff', canopy: this._accent });
    this._bldg(root, 16, 58, 12, 10, 9, { wall: '#5a6374', glass: '#ffd79a', canopy: '#e2603a' });
    this._carpark(root, 88, 62, 5, 5, Math.PI / 2);
    [[80, 30], [82, 70], [20, 30], [18, 74]].forEach(l => this._lamp(root, l[0], l[1]));
  }

  // ---------------- theatre ----------------
  _theatre(root) {
    // auditorium block with fly tower and colonnaded portico
    this._bldg(root, 32, 28, 34, 26, 18, { wall: '#3f3850', glass: '#ffd79a', entry: false, floor: 6 });
    this._bldg(root, 44, 24, 12, 10, 34, { wall: '#332d42', glass: '#5c5470', entry: false, plant: false, floor: 9, lit: 0.08 });
    const portico = new THREE.Mesh(new THREE.BoxGeometry(40 * this._S, 3, 8 * this._S), mat('#4a4257', 0.75));
    portico.position.set(this._px(50), 14.5, this._pz(58)); root.add(portico);
    const ped = new THREE.Mesh(new THREE.BoxGeometry(42 * this._S, 1.4, 10 * this._S), mat('#3d3749', 0.85));
    ped.position.set(this._px(50), 0.7, this._pz(58)); root.add(ped);
    for (let i = 0; i < 9; i++) {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.7, 12, 14), mat('#5e5670', 0.7));
      col.position.set(this._px(31 + i * 4.75), 7.4, this._pz(60)); root.add(col);
      const cap = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.9, 4.2), mat('#6a6280', 0.7));
      cap.position.set(col.position.x, 13.6, col.position.z); root.add(cap);
    }
    const pedimentGeo = new THREE.ConeGeometry(42, 7, 4);
    const pediment = new THREE.Mesh(pedimentGeo, mat('#4a4257', 0.75));
    pediment.rotation.y = Math.PI / 4; pediment.scale.set(1, 1, 0.28);
    pediment.position.set(this._px(50), 19, this._pz(58)); root.add(pediment);

    // lit marquee
    const sign = new THREE.Mesh(new THREE.BoxGeometry(26, 4, 1), new THREE.MeshStandardMaterial({ color: this._accent, emissive: new THREE.Color(this._accent), emissiveIntensity: 0.75, roughness: 0.4 }));
    sign.position.set(this._px(50), 17.5, this._pz(63.6)); root.add(sign);
    for (let i = 0; i < 14; i++) {
      const b = new THREE.Mesh(new THREE.SphereGeometry(0.42, 8, 6), new THREE.MeshStandardMaterial({ color: '#fff3d0', emissive: new THREE.Color('#ffe08a'), emissiveIntensity: 1, roughness: 0.3 }));
      b.position.set(this._px(50) - 13 + i * 2, 20.2, this._pz(63.6)); root.add(b);
    }

    // forecourt, steps, terrace café, box office
    this._plaza(root, 50, 80, 30, '#2a2535');
    for (let i = 0; i < 4; i++) {
      const st = new THREE.Mesh(new THREE.BoxGeometry(40 * this._S, 0.6, 2.4), mat('#3d3749', 0.9));
      st.position.set(this._px(50), 0.3 + i * 0.6, this._pz(64 + i * 1.3)); root.add(st);
    }
    this._bldg(root, 66, 66, 12, 9, 7, { wall: '#4a4257', glass: '#ffd79a', canopy: '#e2603a' });
    this._bldg(root, 24, 66, 10, 8, 7, { wall: '#453e55', glass: '#bfe4ff', canopy: this._accent });
    this._carpark(root, 78, 40, 4, 4, Math.PI / 2);
    this._fence(root, [[18, 88], [82, 88]], '#6a6280');
    [[22, 82], [78, 82], [36, 90], [64, 90]].forEach(l => this._lamp(root, l[0], l[1]));
    [[14, 40], [14, 58], [88, 70], [30, 94], [70, 94]].forEach(t => this._tree(root, t[0], t[1], 1.1));
  }

  // ---------------- restaurant ----------------
  _dining(root) {
    // doll's-house cutaway: floor, low walls, open roof frame — so the room reads from above
    const floor = new THREE.Mesh(new THREE.BoxGeometry(44 * this._S, 0.8, 26 * this._S), mat('#4a3b2f', 0.9));
    floor.position.set(this._px(50), 0.4, this._pz(41)); root.add(floor);
    [[28, 28, 44, 1.4], [28, 28, 1.4, 26], [70.6, 28, 1.4, 26], [28, 52.6, 44, 1.4]].forEach(w => {
      this._box(root, w[0], w[1], w[2], w[3], 2.6, '#332920', 0.9);
    });
    // glazed frontage onto the terrace
    const glassW = new THREE.Mesh(new THREE.BoxGeometry(44 * this._S, 7, 0.6), new THREE.MeshStandardMaterial({ color: '#ffd79a', roughness: 0.16, metalness: 0.3, transparent: true, opacity: 0.32, emissive: new THREE.Color('#ffd79a'), emissiveIntensity: 0.3 }));
    glassW.position.set(this._px(50), 5.5, this._pz(54)); root.add(glassW);
    // open roof frame on columns
    [[30, 30], [70, 30], [30, 52], [70, 52], [50, 30], [50, 52]].forEach(c => {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.8, 10, 10), mat('#2e241d', 0.8));
      col.position.set(this._px(c[0]), 5, this._pz(c[1])); root.add(col);
    });
    for (let i = 0; i < 6; i++) {
      const beam = new THREE.Mesh(new THREE.BoxGeometry(46 * this._S, 0.7, 1.2), mat('#2e241d', 0.85));
      beam.position.set(this._px(50), 10.2, this._pz(30 + i * 4.6)); root.add(beam);
    }
    this._bldg(root, 62, 22, 14, 10, 7, { wall: '#332920', glass: '#ffe6ae', entry: false, plant: false });
    const pass = this._box(root, 42, 30, 18, 4, 3.4, '#6b543f', 0.75);
    void pass;
    for (let i = 0; i < 12; i++) {
      const cx = 33 + (i % 4) * 11, cz = 38 + Math.floor(i / 4) * 7;
      const t = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 0.7, 0.9, 18), mat('#8a6f50', 0.65));
      t.position.set(this._px(cx), 2.6, this._pz(cz)); root.add(t);
      const cloth = new THREE.Mesh(new THREE.CylinderGeometry(3.6, 3.6, 0.2, 18), mat('#e8e2d6', 0.85));
      cloth.position.set(t.position.x, 3.1, t.position.z); root.add(cloth);
      for (let k = 0; k < 4; k++) {
        const a = (k / 4) * Math.PI * 2 + 0.4;
        const seat = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.4, 2.1), mat('#6b543f', 0.85));
        seat.position.set(t.position.x + Math.cos(a) * 6.2, 2.4, t.position.z + Math.sin(a) * 6.2); root.add(seat);
        const back = new THREE.Mesh(new THREE.BoxGeometry(2.1, 2.4, 0.4), mat('#5d4a39', 0.85));
        back.position.set(t.position.x + Math.cos(a) * 7.2, 3.4, t.position.z + Math.sin(a) * 7.2);
        back.rotation.y = -a; root.add(back);
      }
      const candle = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 1, 8), new THREE.MeshStandardMaterial({ color: '#fff3d0', emissive: new THREE.Color('#ffcf7a'), emissiveIntensity: 1, roughness: 0.3 }));
      candle.position.set(t.position.x, 3.7, t.position.z); root.add(candle);
    }

    // terrace: decking, planters, umbrellas, heaters
    const terrace = new THREE.Mesh(new THREE.BoxGeometry(44 * this._S, 0.6, 16 * this._S), mat('#5a4838', 0.9));
    terrace.position.set(this._px(50), 0.3, this._pz(72)); root.add(terrace);
    for (let i = 0; i < 6; i++) {
      const t = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.6, 0.7, 14), mat('#8a6f50', 0.7));
      t.position.set(this._px(32 + i * 7.5), 2.2, this._pz(72)); root.add(t);
      const post = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 8, 8), mat('#e8e2d6', 0.7));
      post.position.set(t.position.x, 4.4, t.position.z); root.add(post);
      const u = new THREE.Mesh(new THREE.ConeGeometry(5.4, 2.8, 12), mat(this._accent, 0.6));
      u.position.set(t.position.x, 9.2, t.position.z); root.add(u);
    }
    for (let i = 0; i < 7; i++) {
      const pl = new THREE.Mesh(new THREE.BoxGeometry(5, 2.4, 4), mat('#4a3b2f', 0.9));
      pl.position.set(this._px(28 + i * 7.4), 1.2, this._pz(81)); root.add(pl);
      const bush = new THREE.Mesh(new THREE.SphereGeometry(2.6, 10, 8), mat('#2f5d3f', 0.92));
      bush.position.set(pl.position.x, 3.6, pl.position.z); root.add(bush);
    }

    this._plaza(root, 50, 90, 18, '#2a231c');
    this._carpark(root, 12, 62, 3, 4, 0);
    [[22, 88], [78, 88], [16, 40], [86, 52]].forEach(l => this._lamp(root, l[0], l[1]));
    [[14, 28], [88, 30], [12, 78], [90, 78]].forEach(t => this._tree(root, t[0], t[1], 1.1));
  }


  _routeLine() {
    const sc = this._scene;
    if (!sc) return;
    if (this._routeGroup) { sc.remove(this._routeGroup); this._routeGroup = null; }
    let pts = [];
    try { pts = JSON.parse(this.getAttribute('route') || '[]'); } catch (e) { pts = []; }
    if (!pts || pts.length < 2) return;
    const g = new THREE.Group();
    this._routeGroup = g;
    sc.add(g);
    const v3 = pts.map(p => new THREE.Vector3(this._px(p[0]), 1.4, this._pz(p[1])));
    const curve = new THREE.CatmullRomCurve3(v3, false, 'catmullrom', 0.25);
    const ribbon = new THREE.Mesh(
      new THREE.TubeGeometry(curve, Math.max(40, pts.length * 14), 1.5, 8, false),
      new THREE.MeshStandardMaterial({ color: this._accent, roughness: 0.3, emissive: new THREE.Color(this._accent), emissiveIntensity: 0.65 })
    );
    g.add(ribbon);
    const glow = new THREE.Mesh(
      new THREE.TubeGeometry(curve, Math.max(40, pts.length * 14), 3.4, 8, false),
      new THREE.MeshStandardMaterial({ color: this._accent, transparent: true, opacity: 0.16, roughness: 0.6 })
    );
    glow.position.y = -0.4;
    g.add(glow);
    // start and end markers
    [[v3[0], '#4cc38a'], [v3[v3.length - 1], this._accent]].forEach((m, i) => {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(4.4, 0.5, 8, 30), new THREE.MeshStandardMaterial({ color: m[1], emissive: new THREE.Color(m[1]), emissiveIntensity: 0.5, roughness: 0.4 }));
      ring.rotation.x = -Math.PI / 2;
      ring.position.set(m[0].x, 0.6, m[0].z);
      g.add(ring);
      if (i === 1) this._destRing = ring;
    });
    this._routeCurve = curve;
    const dot = new THREE.Mesh(new THREE.SphereGeometry(2.2, 14, 10), new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: new THREE.Color('#ffffff'), emissiveIntensity: 0.8, roughness: 0.3 }));
    g.add(dot);
    this._routeDot = dot;
  }

  // ---------- pins ----------
  _addPins(root) {
    let list = [];
    try { list = JSON.parse(this.getAttribute('pins') || '[]'); } catch (e) { list = []; }
    this._list = list;
    list.forEach(p => {
      const color = KIND[p.kind] || this._accent;
      const g = new THREE.Group();
      const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 9, 8), mat('#e8e2d6', 0.6));
      stem.position.y = 4.5; g.add(stem);
      const head = new THREE.Mesh(new THREE.SphereGeometry(2.8, 16, 12), new THREE.MeshStandardMaterial({ color, roughness: 0.32, metalness: 0.06, emissive: new THREE.Color(color), emissiveIntensity: 0.25 }));
      head.position.y = 11; g.add(head);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(4, 0.32, 8, 28), new THREE.MeshStandardMaterial({ color, roughness: 0.4, transparent: true, opacity: 0.55 }));
      ring.rotation.x = -Math.PI / 2; ring.position.y = 0.3; g.add(ring);
      g.position.set(this._px(p.x), 0, this._pz(p.y));
      g.userData = { id: p.id, label: p.label, meta: p.meta || '', color };
      head.userData = g.userData;
      root.add(g);
      this._pins.push({ group: g, head, ring, data: p, color });
    });
    this._paintPins();
  }

  _paintPins() {
    const sel = this.getAttribute('selected') || '';
    (this._pins || []).forEach(p => {
      const on = p.data.id === sel;
      p.head.scale.setScalar(on ? 1.45 : 1);
      p.head.material.emissive && p.head.material.emissive.setHex(on ? 0x332200 : 0x000000);
      p.ring.material.opacity = on ? 0.9 : 0.5;
    });
  }

  _crowd(root, venue) {
    const n = venue === 'dining' ? 12 : 30;
    for (let i = 0; i < n; i++) {
      const a = Math.random() * Math.PI * 2, rr = 22 + Math.random() * 74;
      const w = walker(i % 3 ? '#ffffff' : '#ffe27a', 2.2);
      w.group.position.set(Math.cos(a) * rr, 0, Math.sin(a) * rr);
      w.orbit = { a, r: rr, sp: 0.16 + Math.random() * 0.3 };
      w.seed = Math.random() * 6;
      root.add(w.group);
      this._actors.push(w);
    }
  }

  _cast(e) {
    const r = this._renderer.domElement.getBoundingClientRect();
    this._pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    this._raycaster.setFromCamera(this._pointer, this._cam);
    const hit = this._raycaster.intersectObjects((this._pins || []).map(p => p.head), false)[0];
    return hit ? hit.object : null;
  }

  _setHover(obj) {
    if (this._hovered === obj) return;
    this._hovered = obj || null;
    const canvas = this._renderer.domElement;
    if (obj) {
      canvas.classList.add('picking');
      this._tag.innerHTML = obj.userData.label + (obj.userData.meta ? ' <i>' + obj.userData.meta + '</i>' : '');
      this._tag.classList.add('on');
    } else {
      canvas.classList.remove('picking');
      this._tag.classList.remove('on');
    }
  }

  _pick(e) {
    const obj = this._cast(e);
    if (!obj) return;
    this.dispatchEvent(new CustomEvent('pinpick', { detail: { id: obj.userData.id }, bubbles: true, composed: true }));
  }

  _tagFollow() {
    if (!this._hovered || !this._tag.classList.contains('on')) return;
    const v = this._hovered.getWorldPosition(new THREE.Vector3()).project(this._cam);
    const r = this._renderer.domElement;
    this._tag.style.left = ((v.x * 0.5 + 0.5) * r.clientWidth) + 'px';
    this._tag.style.top = ((-v.y * 0.5 + 0.5) * r.clientHeight) + 'px';
  }

  _loop() {
    if (this._stop) return;
    this._raf = requestAnimationFrame(() => this._loop());
    const t = this._clock.getElapsedTime();

    (this._actors || []).forEach(a => {
      a.orbit.a += a.orbit.sp * 0.003;
      a.group.position.x = Math.cos(a.orbit.a) * a.orbit.r;
      a.group.position.z = Math.sin(a.orbit.a * 1.15) * a.orbit.r * 0.82;
      a.group.rotation.y = -a.orbit.a * 1.1;
      const p = t * 2.4 + a.seed;
      a.legL.rotation.x = Math.sin(p) * 0.85;
      a.legR.rotation.x = -Math.sin(p) * 0.85;
    });

    (this._pins || []).forEach((p, i) => {
      p.head.position.y = 11 + Math.sin(t * 1.6 + i) * 0.6;
      p.ring.scale.setScalar(1 + (Math.sin(t * 1.6 + i) * 0.5 + 0.5) * 0.3);
    });

    (this._spin || []).forEach(m => { m.rotation.y = t * 0.6; });
    if (this._routeDot && this._routeCurve) {
      const pa = this.getAttribute('progress');
      const driven = pa !== null && pa !== '';
      const u = driven ? Math.max(0, Math.min(0.999, parseFloat(pa) || 0)) : (t * 0.13) % 1;
      const p = this._routeCurve.getPoint(u);
      this._routeDot.position.set(p.x, p.y + 1.6, p.z);
      this._routeDot.scale.setScalar(driven ? 1.5 : 1);
      if (driven && this.getAttribute('follow') === '1' && this._controls) {
        const ahead = this._routeCurve.getPoint(Math.min(0.999, u + 0.03));
        const dir = ahead.clone().sub(p).normalize();
        const want = p.clone().add(new THREE.Vector3(-dir.x * 46, 34, -dir.z * 46));
        this._cam.position.lerp(want, 0.06);
        this._controls.target.lerp(new THREE.Vector3(p.x, p.y + 2, p.z), 0.09);
      }
    }
    if (this._destRing) this._destRing.scale.setScalar(1 + (Math.sin(t * 2.4) * 0.5 + 0.5) * 0.22);
    if (this._tower) this._tower.position.y = 8 + (Math.sin(t * 0.7) * 0.5 + 0.5) * 26;
    if (this._coaster && this._coaster.car) {
      const u = (t * 0.09) % 1;
      const p = this._coaster.curve.getPoint(u);
      const q = this._coaster.curve.getPoint((u + 0.01) % 1);
      this._coaster.car.position.copy(p);
      this._coaster.car.lookAt(q);
    }
    if (this._water_) this._water_.material.color.offsetHSL(0, 0, Math.sin(t * 2) * 0.0006);

    this._tagFollow();
    this._controls.update();
    this._renderer.render(this._scene, this._cam);
  }
}

if (!customElements.get('venue-map-3d')) customElements.define('venue-map-3d', VenueMap3D);
