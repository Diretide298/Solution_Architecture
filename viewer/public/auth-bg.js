/**
 * The node field behind the invite card. From `ui-design/INVITE.md`.
 *
 * The Atlas mark is a network drawn on a sphere, so the page it sits on draws
 * the same thing at large: a lattice that continuously forms and dissolves.
 *
 * The load-bearing detail is that **there is no edge list**. Every frame, every
 * pair of nodes closer than `linkDistance` is stroked, with alpha scaled by
 * `1 - d/linkDistance`. Links therefore fade in as two nodes drift together and
 * fade out as they part, and the lattice is never twice the same — a fixed set
 * of edges dragged around would read as a rigid mesh being panned.
 *
 * Four rules it is built around:
 *
 *   1. It never competes with the card. Low alpha throughout, and the canvas
 *      takes no pointer events — a background that can steal a click from a
 *      password field is a bug, not a flourish.
 *   2. It stops when nobody is looking. A hidden tab pauses, and a reader who
 *      asked for reduced motion gets one static frame rather than a rAF loop
 *      burning a core on a sign-in screen.
 *   3. It is seeded fresh on every load and every resize, so no two visits draw
 *      the same field.
 *   4. It tears down cleanly: the returned `stop()` cancels the frame and
 *      disconnects the observer, so nothing runs on against a detached canvas.
 *
 * Self-contained on purpose: importing the app's core.js would pull tooltips
 * and the glossary onto a page that has neither, and each of those files would
 * then need adding to the server's public allowlist.
 */

const MAX_NODES = 240;
const AREA_PER_NODE = 6800;
const HUB_CHANCE = 0.08;
const MAX_BEAMS = 3;
const BEAM_CHANCE = 0.006;

/** The two palettes, from the handoff's table. Alpha is applied at the point of
 *  use, so each entry is the colour without one. */
const PALETTE = {
  night: {
    hub: '160, 245, 242',
    node: '88, 216, 212',
    hubEdge: '110, 232, 228',
    edge: '72, 178, 180',
    beam: '150, 235, 232',
    blend: 'lighter',
  },
  day: {
    hub: '14, 105, 107',
    node: '36, 150, 152',
    hubEdge: '20, 120, 122',
    edge: '60, 140, 142',
    beam: '70, 195, 192',
    // Day composites `multiply`; `lighter` over a pale stage washes the beams
    // out to nothing at all.
    blend: 'multiply',
  },
};

const rand = (lo, hi) => lo + Math.random() * (hi - lo);

/**
 * Whether to hold still, with a way to say otherwise.
 *
 * Both animations on the auth pages — this lattice and the sign-in page's
 * typing demo — freeze on `prefers-reduced-motion: reduce`, which is right:
 * a drifting field is exactly the kind of ambient motion that setting exists
 * to stop. But the two failing together is indistinguishable from both being
 * broken, and on Windows the switch behind it (Settings > Accessibility >
 * Visual effects > Animation effects) is one people turn off years earlier for
 * unrelated reasons and never think about again. That cost an afternoon here.
 *
 * So the query still decides by default, and `ticvai-motion` overrides it in
 * either direction for anyone who wants to make their own call:
 *
 *   localStorage.setItem('ticvai-motion', 'always')  // animate regardless
 *   localStorage.setItem('ticvai-motion', 'never')   // hold still regardless
 *   localStorage.removeItem('ticvai-motion')         // back to the OS
 */
export function prefersStillness() {
  // The query string first, and it also *sets* the preference — localStorage is
  // per-origin, so `localhost:4173` and `127.0.0.1:4173` are two different
  // stores and a value typed into the console of one silently does nothing on
  // the other. A link works wherever you paste it, and sticks afterwards.
  let forced = null;
  try {
    forced = new URLSearchParams(location.search).get('motion');
  } catch { /* a malformed URL is not worth failing over */ }

  try {
    if (forced === 'always' || forced === 'never') localStorage.setItem('ticvai-motion', forced);
    else if (forced === 'auto') localStorage.removeItem('ticvai-motion');
    else forced = localStorage.getItem('ticvai-motion');
  } catch { /* storage can be denied outright; the query alone still decides */ }

  if (forced === 'always') return false;
  if (forced === 'never') return true;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function startAuthBackground(canvas, options = {}) {
  if (!canvas) return () => {};

  const {
    density = 1,
    linkDistance = 168,
    beams: wantBeams = true,
    speed = 2.6,
  } = options;

  const ctx = canvas.getContext('2d');
  const still = prefersStillness();
  const palette = () =>
    PALETTE[document.documentElement.dataset.theme === 'dark' ? 'night' : 'day'];

  let w = 0;
  let h = 0;
  let nodes = [];
  let beams = [];

  function seed() {
    const want = Math.min(MAX_NODES, Math.round(((w * h) / AREA_PER_NODE) * density));
    nodes = Array.from({ length: Math.max(24, want) }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      // The handoff specifies ±0.16 px/frame. That is ~10px in two seconds on a
      // 1200px stage — measurably animating and perceptually frozen, which is
      // exactly how it was read. `speed` scales it; the lattice reforms at a
      // rate you can actually see, and the option is there for anyone who wants
      // the paper value back.
      vx: rand(-0.16, 0.16) * speed,
      vy: rand(-0.16, 0.16) * speed,
      r: rand(1.3, 3.4),
      hub: Math.random() < HUB_CHANCE,
      phase: Math.random() * Math.PI * 2,
      twinkle: rand(0.014, 0.04),
    }));
    beams = [];
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth;
    h = canvas.clientHeight;
    if (!w || !h) return;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed();
  }

  /** A long, soft, round-capped stroke crossing the field. Transparent at both
   *  ends, so it reads as light passing through rather than a drawn line. */
  function spawnBeam() {
    const fromTop = Math.random() < 0.5;
    beams.push({
      x: fromTop ? rand(-w * 0.2, w) : -w * 0.15,
      y: fromTop ? -h * 0.15 : rand(-h * 0.2, h),
      angle: rand(0.5, 1.15),
      len: Math.hypot(w, h) * 1.3,
      width: rand(22, 74),
      life: 0,
      max: rand(150, 320),
    });
  }

  function step() {
    for (const n of nodes) {
      n.x += n.vx;
      n.y += n.vy;
      // wrap rather than bounce: an edge that reflects reads as a wall, and
      // there is no wall here
      if (n.x < -40) n.x = w + 40;
      if (n.x > w + 40) n.x = -40;
      if (n.y < -40) n.y = h + 40;
      if (n.y > h + 40) n.y = -40;
      n.phase += n.twinkle;
    }

    if (wantBeams) {
      if (beams.length < MAX_BEAMS && Math.random() < BEAM_CHANCE) spawnBeam();
      beams = beams.filter((b) => (b.life += 1) < b.max);
    }
  }

  function drawBeams(p) {
    if (!beams.length) return;
    ctx.save();
    ctx.globalCompositeOperation = p.blend;
    ctx.lineCap = 'round';
    for (const b of beams) {
      // in and out over the beam's life, so it never appears or vanishes
      const fade = Math.sin((b.life / b.max) * Math.PI) * 0.5;
      if (fade <= 0) continue;
      const x2 = b.x + Math.cos(b.angle) * b.len;
      const y2 = b.y + Math.sin(b.angle) * b.len;
      const g = ctx.createLinearGradient(b.x, b.y, x2, y2);
      g.addColorStop(0, `rgba(${p.beam}, 0)`);
      g.addColorStop(0.5, `rgba(${p.beam}, ${fade})`);
      g.addColorStop(1, `rgba(${p.beam}, 0)`);
      ctx.strokeStyle = g;
      ctx.lineWidth = b.width;
      ctx.beginPath();
      ctx.moveTo(b.x, b.y);
      ctx.lineTo(x2, y2);
      ctx.stroke();
    }
    ctx.restore();
  }

  function draw() {
    const p = palette();
    ctx.clearRect(0, 0, w, h);
    drawBeams(p);

    // Edges, recomputed in full. O(n²), but the axis test throws out most pairs
    // before the square root: at 240 nodes that is ~29k comparisons a frame,
    // which a desktop invite page can afford.
    for (let i = 0; i < nodes.length; i += 1) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j += 1) {
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        if (Math.abs(dx) > linkDistance || Math.abs(dy) > linkDistance) continue;
        const d = Math.hypot(dx, dy);
        if (d > linkDistance) continue;
        const near = 1 - d / linkDistance;
        const hub = a.hub || b.hub;
        ctx.strokeStyle = `rgba(${hub ? p.hubEdge : p.edge}, ${near * (hub ? 0.5 : 0.32)})`;
        ctx.lineWidth = hub ? 1.2 : 0.85;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
    }

    // Nodes last, so each sits on top of its own threads.
    for (const n of nodes) {
      const tw = 0.65 + Math.sin(n.phase) * 0.35;
      if (n.hub) {
        const glow = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 9);
        glow.addColorStop(0, `rgba(${p.hub}, ${0.3 * tw})`);
        glow.addColorStop(1, `rgba(${p.hub}, 0)`);
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r * 9, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.fillStyle = `rgba(${n.hub ? p.hub : p.node}, ${(n.hub ? 0.95 : 0.72) * tw})`;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  let raf = null;
  const frame = () => { step(); draw(); raf = requestAnimationFrame(frame); };
  const play = () => { if (raf == null && !still) raf = requestAnimationFrame(frame); };
  const pause = () => { if (raf != null) { cancelAnimationFrame(raf); raf = null; } };
  const onVisibility = () => (document.hidden ? pause() : play());

  const observer = new ResizeObserver(() => { resize(); if (still) draw(); });
  observer.observe(canvas);
  resize();

  // Nothing to animate for somebody who asked for stillness — but the lattice
  // is part of the page, so they still get it, once.
  if (still) {
    draw();
    return () => observer.disconnect();
  }

  document.addEventListener('visibilitychange', onVisibility);
  play();

  return function stop() {
    pause();
    observer.disconnect();
    document.removeEventListener('visibilitychange', onVisibility);
  };
}
