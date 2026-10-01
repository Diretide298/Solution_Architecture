import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const MAT = {};
const mat = (c, rough) => (MAT[c + (rough || 0)] = MAT[c + (rough || 0)] || new THREE.MeshStandardMaterial({ color: c, roughness: rough == null ? 0.6 : rough, metalness: 0.04 }));

function limb(m, r, len) { return new THREE.Mesh(new THREE.CapsuleGeometry(r, len, 3, 6), m); }

function makeStickman(color, scale) {
  const m = mat(color, 0.5);
  const g = new THREE.Group();
  const torso = limb(m, 0.09, 0.5); torso.position.y = 0.95; g.add(torso);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.15, 10, 8), m); head.position.y = 1.38; g.add(head);
  const armL = new THREE.Group(), armR = new THREE.Group();
  [armL, armR].forEach((a, i) => { const s = limb(m, 0.06, 0.42); s.position.y = -0.24; a.add(s); a.position.set(i ? 0.17 : -0.17, 1.16, 0); g.add(a); });
  const legL = new THREE.Group(), legR = new THREE.Group();
  [legL, legR].forEach((l, i) => { const s = limb(m, 0.07, 0.5); s.position.y = -0.28; l.add(s); l.position.set(i ? 0.09 : -0.09, 0.68, 0); g.add(l); });
  g.scale.setScalar(scale || 1);
  return { group: g, armL, armR, legL, legR, head, torso };
}

class Stadium3D extends HTMLElement {
  static get observedAttributes() { return ['mode', 'accent', 'sections', 'floor']; }

  connectedCallback() {
    if (this._built) {
      if (this._stop) {
        this._stop = false;
        if (this._renderer && this._renderer.domElement) this._renderer.domElement.remove();
        this._renderer = null; this._scene = null;
        this._io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { this._start(); this._io.disconnect(); } }), { rootMargin: '150px' });
        this._io.observe(this);
    setTimeout(() => { if (!this._renderer && !this._stop && this.isConnected) { try { this._io.disconnect(); } catch (e) { } this._start(); } }, 450);
      }
      return;
    }
    this._built = true;
    this._shadow = this.attachShadow({ mode: 'open' });
    this._shadow.innerHTML = `
      <style>
        :host { display:block; position:relative; min-height:250px; }
        canvas { display:block; width:100%; height:100%; touch-action:pan-y; cursor:grab; }
        canvas.picking { cursor:pointer; }
        .hint { position:absolute; left:11px; bottom:10px; font:700 10px/1.2 system-ui,sans-serif; letter-spacing:.12em;
                text-transform:uppercase; color:rgba(255,255,255,.78); pointer-events:none; }
        .zoom { position:absolute; right:10px; bottom:10px; display:flex; gap:6px; }
        .zoom button { width:30px; height:30px; padding:0; border-radius:8px; cursor:pointer; font:700 15px/1 system-ui,sans-serif;
                       color:#fff; background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.28); backdrop-filter:blur(6px); }
        .zoom button:hover { background:rgba(255,255,255,.26); }
      </style>
      <div class="hint">Drag to orbit</div>
      <div class="zoom">
        <button type="button" data-z="out" aria-label="Zoom out">&minus;</button>
        <button type="button" data-z="in" aria-label="Zoom in">+</button>
      </div>`;
    this._io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { this._start(); this._io.disconnect(); } }), { rootMargin: '150px' });
    this._io.observe(this);
    setTimeout(() => { if (!this._renderer && !this._stop && this.isConnected) { try { this._io.disconnect(); } catch (e) { } this._start(); } }, 450);
  }

  disconnectedCallback() {
    this._stop = true;
    if (this._raf) cancelAnimationFrame(this._raf);
    if (this._ro) this._ro.disconnect();
    if (this._io) this._io.disconnect();
    if (this._renderer) { this._renderer.dispose(); this._renderer.forceContextLoss && this._renderer.forceContextLoss(); }
  }

  attributeChangedCallback(n) { if (this._scene) this._build(); }

  _size() { const w = this.clientWidth || 620; return { w, h: Math.max(250, Math.round(w * 0.58)) }; }

  _start() {
    const { w, h } = this._size();
    const r = new THREE.WebGLRenderer({ antialias: true });
    r.setPixelRatio(Math.min(devicePixelRatio, 2));
    r.setSize(w, h, false);
    r.outputColorSpace = THREE.SRGBColorSpace;
    this._shadow.appendChild(r.domElement);
    this._renderer = r;

    const sc = new THREE.Scene();
    sc.background = new THREE.Color('#0c1420');
    sc.fog = new THREE.Fog('#0c1420', 170, 460);
    this._scene = sc;

    const cam = new THREE.PerspectiveCamera(40, w / h, 0.5, 2000);
    cam.position.set(96, 78, 118);
    this._cam = cam;

    sc.add(new THREE.HemisphereLight('#d3e6ff', '#1d2634', 1.1));
    const key = new THREE.DirectionalLight('#fff3dd', 1.45); key.position.set(90, 150, 70); sc.add(key);
    const rim = new THREE.DirectionalLight('#78b0ff', 0.55); rim.position.set(-110, 50, -90); sc.add(rim);

    const c = new OrbitControls(cam, r.domElement);
    c.enableDamping = true; c.dampingFactor = 0.08;
    c.maxPolarAngle = Math.PI * 0.47; c.minDistance = 60; c.maxDistance = 320;
    c.autoRotate = true; c.autoRotateSpeed = 0.4;
    c.enableZoom = false;              // wheel always belongs to the page
    c.enablePan = false;
    c.target.set(0, 6, 0);
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
    el.addEventListener('pointerdown', e => {
      c.autoRotate = false;
      downAt = { x: e.clientX, y: e.clientY };
      dragged = false;
    });
    el.addEventListener('pointermove', e => {
      if (downAt && (Math.abs(e.clientX - downAt.x) > 4 || Math.abs(e.clientY - downAt.y) > 4)) dragged = true;
      this._hover(e);
    });
    el.addEventListener('pointerup', e => {
      if (!dragged) this._pick(e);
      downAt = null;
    });
    el.addEventListener('pointerleave', () => { downAt = null; this._setHover(null); });
    this._raycaster = new THREE.Raycaster();
    this._pointer = new THREE.Vector2();

    this._clock = new THREE.Clock();
    this._picky = [];
    this._build();
    this._loop();

    this._ro = new ResizeObserver(() => {
      const s = this._size();
      r.setSize(s.w, s.h, false);
      cam.aspect = s.w / s.h; cam.updateProjectionMatrix();
    });
    this._ro.observe(this);
  }

  // the bowl, built from blocks that mirror the 2D plan
  _build() {
    const sc = this._scene;
    if (this._root) sc.remove(this._root);
    const root = new THREE.Group();
    this._root = root;
    this._picky = [];
    sc.add(root);
    this._actors = [];

    const accent = this.getAttribute('accent') || '#c07c1e';
    const concert = (this.getAttribute('mode') || 'sport') === 'concert';
    let secs = [];
    try { secs = JSON.parse(this.getAttribute('sections') || '[]'); } catch (e) { secs = []; }
    try { this._floor = JSON.parse(this.getAttribute('floor') || '[]'); } catch (e) { this._floor = []; }

    const S = 1.9;                       // plan units (0..100) → world units
    const px = v => (v - 50) * S;        // plan x → world x
    const pz = v => (v - 50) * S;        // plan y → world z

    // ground
    const ground = new THREE.Mesh(new THREE.CircleGeometry(150, 48), mat('#141c29', 0.9));
    ground.rotation.x = -Math.PI / 2; ground.position.y = -0.4;
    root.add(ground);

    const tierColor = { Premium: accent, Standard: '#7d8ea3', Economy: '#4c5a6d' };
    const tierH = { Premium: 7, Standard: 9.5, Economy: 12.5 };

    secs.forEach(sx => {
      const isUpper = Number(sx.label) >= 200;
      const h = (tierH[sx.tier] || 8) * (isUpper ? 1.55 : 1);
      const w = sx.w * S, d = sx.h * S;
      const blocked = sx.kind === 'blocked';
      const standMat = new THREE.MeshStandardMaterial({
        color: blocked ? '#2a3240' : (tierColor[sx.tier] || '#6b7a8c'),
        roughness: 0.72, metalness: 0.04
      });
      const stand = new THREE.Mesh(new THREE.BoxGeometry(w * 0.94, h, d * 0.94), standMat);
      stand.position.set(px(sx.x + sx.w / 2), h / 2 + (isUpper ? 9 : 0), pz(sx.y + sx.h / 2));
      stand.userData = { label: sx.label, blocked: blocked, baseColor: standMat.color.getHex() };
      root.add(stand);
      if (!blocked) this._picky.push(stand);

      // crowd sits straight on the stand, in a high-contrast colour
      const per = blocked ? 0 : (isUpper ? 2 : 3);
      for (let i = 0; i < per; i++) {
        const s = makeStickman(i % 2 ? '#ffe27a' : '#ffffff', 2.1);
        s.group.position.set(
          stand.position.x + (Math.random() - 0.5) * w * 0.55,
          stand.position.y + h / 2,
          stand.position.z + (Math.random() - 0.5) * d * 0.55
        );
        s.group.lookAt(0, s.group.position.y, 0);
        s.kind = Math.random() > 0.5 ? 'cheer' : 'wave';
        s.seed = Math.random() * 6;
        root.add(s.group);
        this._actors.push(s);
      }
    });

    if (concert) {
      // end stage on the east side, mirroring the 2D plan
      const stageW = 8 * S, stageD = 34 * S;
      const stage = new THREE.Mesh(new THREE.BoxGeometry(stageW, 4, stageD), mat('#22262e', 0.7));
      stage.position.set(px(65), 2, pz(50));
      root.add(stage);
      const screen = new THREE.Mesh(new THREE.BoxGeometry(1.2, 14, stageD * 0.7), mat('#0a0d13', 0.35));
      screen.position.set(px(69.5), 11, pz(50));
      root.add(screen);
      [-1, 1].forEach(sgn => {
        const truss = new THREE.Mesh(new THREE.BoxGeometry(1.4, 22, 1.4), mat('#2e3440', 0.6));
        truss.position.set(px(62), 11, pz(50) + sgn * stageD * 0.42);
        root.add(truss);
      });
      for (let i = 0; i < 3; i++) {
        const s = makeStickman('#ffe27a', 3.4);
        s.group.position.set(px(64), 4, pz(50) + (i - 1) * 9);
        s.group.rotation.y = -Math.PI / 2;
        s.kind = 'perform'; s.seed = i * 1.1;
        root.add(s.group);
        this._actors.push(s);
      }

      // general-admission standing blocks, one raised pad each
      const ga = (this._floor || []).filter(g => g.kind === 'standing');
      const blocks = ga.length ? ga : [];
      blocks.forEach((g, gi) => {
        const bw = g.w * S, bd = g.h * S;
        const pad = new THREE.Mesh(
          new THREE.BoxGeometry(bw * 0.94, 1.1, bd * 0.9),
          new THREE.MeshStandardMaterial({ color: gi % 2 ? '#6c4b8a' : '#7d569c', roughness: 0.85 })
        );
        pad.position.set(px(g.x + g.w / 2), 0.55, pz(g.y + g.h / 2));
        pad.userData = { label: 'ga-' + g.label, ga: true, baseColor: pad.material.color.getHex() };
        root.add(pad);
        this._picky.push(pad);
        for (let i = 0; i < 5; i++) {
          const s = makeStickman(i % 2 ? '#ffffff' : '#ffe27a', 2.4);
          s.group.position.set(
            px(g.x + 1 + Math.random() * (g.w - 2)),
            1.1,
            pz(g.y + 1 + Math.random() * (g.h - 2))
          );
          s.group.rotation.y = -Math.PI / 2;
          s.kind = 'cheer'; s.seed = Math.random() * 6;
          root.add(s.group);
          this._actors.push(s);
        }
      });
    } else {
      const pitch = new THREE.Mesh(new THREE.BoxGeometry(38 * S, 0.5, 40 * S), mat('#2f6b3a', 0.95));
      pitch.position.set(px(50), 0.25, pz(50));
      root.add(pitch);
      const line = new THREE.Mesh(new THREE.BoxGeometry(38 * S, 0.06, 0.7), mat('#eef4ee', 0.6));
      line.position.set(px(50), 0.55, pz(50));
      root.add(line);
      const circle = new THREE.Mesh(new THREE.TorusGeometry(7, 0.32, 6, 40), mat('#eef4ee', 0.6));
      circle.rotation.x = -Math.PI / 2; circle.position.set(px(50), 0.55, pz(50));
      root.add(circle);
      for (let i = 0; i < 10; i++) {
        const s = makeStickman(i < 5 ? '#ffe27a' : '#ffffff', 3.2);
        const a = (i / 10) * Math.PI * 2;
        s.group.position.set(px(50) + Math.cos(a) * 18, 0.5, pz(50) + Math.sin(a) * 14);
        s.kind = 'play';
        s.orbit = { a, r: 12 + (i % 4) * 5, sp: 0.5 + (i % 5) * 0.16, cx: px(50), cz: pz(50) };
        s.seed = i * 0.7;
        root.add(s.group);
        this._actors.push(s);
      }
      const ball = new THREE.Mesh(new THREE.SphereGeometry(1.1, 12, 10), mat('#f8fafc', 0.4));
      ball.position.set(px(50), 1.1, pz(50));
      root.add(ball);
      this._ball = ball;
    }
  }

  _cast(e) {
    const r = this._renderer.domElement.getBoundingClientRect();
    this._pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    this._raycaster.setFromCamera(this._pointer, this._cam);
    const hit = this._raycaster.intersectObjects(this._picky || [], false)[0];
    return hit ? hit.object : null;
  }

  _setHover(obj) {
    if (this._hovered === obj) return;
    if (this._hovered) {
      this._hovered.material.emissive && this._hovered.material.emissive.setHex(0x000000);
      this._hovered.scale.set(1, 1, 1);
    }
    this._hovered = obj || null;
    const canvas = this._renderer.domElement;
    if (obj) {
      obj.material.emissive && obj.material.emissive.setHex(0x553311);
      obj.scale.set(1.06, 1.14, 1.06);
      canvas.classList.add('picking');
    } else {
      canvas.classList.remove('picking');
    }
  }

  _hover(e) { this._setHover(this._cast(e)); }

  _pick(e) {
    const obj = this._cast(e);
    if (!obj || !obj.userData || obj.userData.blocked) return;
    this.dispatchEvent(new CustomEvent('sectionpick', {
      detail: { label: obj.userData.label }, bubbles: true, composed: true
    }));
  }

  _loop() {
    if (this._stop) return;
    this._raf = requestAnimationFrame(() => this._loop());
    const t = this._clock.getElapsedTime();

    (this._actors || []).forEach(a => {
      const p = t * 2.3 + a.seed;
      if (a.kind === 'wave') {
        a.armR.rotation.z = -2.3 + Math.sin(p) * 0.75;
        a.armL.rotation.z = 0.3;
      } else if (a.kind === 'cheer') {
        const hop = Math.max(0, Math.sin(p));
        a.armL.rotation.z = 2.5; a.armR.rotation.z = -2.5;
        a.torso.position.y = 0.95 + hop * 0.14;
        a.head.position.y = 1.38 + hop * 0.14;
      } else if (a.kind === 'perform') {
        a.armL.rotation.z = 1.7 + Math.sin(p * 1.4) * 0.9;
        a.armR.rotation.z = -1.7 - Math.cos(p * 1.2) * 0.9;
        a.group.rotation.y = Math.sin(p * 0.5) * 0.5;
      } else if (a.kind === 'play' && a.orbit) {
        a.orbit.a += a.orbit.sp * 0.004;
        a.group.position.x = a.orbit.cx + Math.cos(a.orbit.a) * a.orbit.r;
        a.group.position.z = a.orbit.cz + Math.sin(a.orbit.a * 1.25) * a.orbit.r * 0.72;
        a.group.rotation.y = -a.orbit.a * 1.2;
        a.legL.rotation.x = Math.sin(p * 2.2) * 0.95;
        a.legR.rotation.x = -Math.sin(p * 2.2) * 0.95;
        a.armL.rotation.x = -Math.sin(p * 2.2) * 0.7;
        a.armR.rotation.x = Math.sin(p * 2.2) * 0.7;
      }
    });

    if (this._ball) {
      this._ball.position.x = Math.sin(t * 0.7) * 22;
      this._ball.position.z = Math.cos(t * 0.9) * 16;
      this._ball.position.y = 1.1 + Math.abs(Math.sin(t * 3)) * 3;
    }

    this._controls.update();
    this._renderer.render(this._scene, this._cam);
  }
}

if (!customElements.get('stadium-3d')) customElements.define('stadium-3d', Stadium3D);
