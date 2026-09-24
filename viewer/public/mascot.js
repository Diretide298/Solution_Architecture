/**
 * Adam, floating in the corner of the viewer.
 *
 * Ported from the design handoff ("UI improvements and mascot integration"),
 * which is the source of truth for the numbers in here — the segment table, the
 * weighted mixes, the glitch timings and the keying. React in the prototype,
 * plain DOM here, same behaviour.
 *
 * **Two clips, ten segments, one hub.** Each MP4 is 15s at 24fps, made of five
 * 3-second segments that begin and end on a neutral pose. Playback runs a
 * segment, then at the hub picks the next one at random from the mix that
 * matches what the reader is doing. That is why it never looks like a loop: the
 * order is drawn, not scripted.
 *
 * **Two stacked videos, not one.** A single element cannot seek to the next
 * segment without a visible stall, so the front one plays while the back one
 * loads and seeks to its first frame, then they swap. The cut between them is
 * covered by a glitch, which also hides that the two files use slightly
 * different neutral poses — open hands against crossed arms — and would
 * otherwise pop.
 *
 * **The backdrop is keyed out on the GPU.** The renders are on black and near
 * black, and `mix-blend-mode: screen` would drop the character's own dark
 * edges with it. The WebGL keyer samples the frame's corners, removes that
 * colour and un-mixes the edge pixels, so the figure keeps its real colours
 * over whatever is behind it. Without WebGL it falls back to the still.
 */

// ── the clips ────────────────────────────────────────────────────────

const VFPS = 24;
const SEG_F = 72;                       // 3 seconds a segment
const VFILES = {
  idle: '/brand/mascot/mascot-idle.mp4',
  read: '/brand/mascot/mascot-read.mp4',
};
const STILL = '/brand/mascot/mascot-still.png';

/** Which file each segment lives in, and the frame it starts at. */
const SEG = {
  idle: ['idle', 0], working: ['idle', 72], sleeping: ['idle', 144],
  build: ['idle', 216], excited: ['idle', 288],
  reading: ['read', 0], thinking: ['read', 72], listening: ['read', 144],
  quick: ['read', 216], ready: ['read', 288],
};

/** How far each hub frame has drifted from frame 0. Bigger drift wants a longer
 *  cover, which is what fadeMs spends it on. Measured, not guessed — it comes
 *  from the handoff. */
const DRIFT = {
  'idle:0': 0, 'idle:72': 5, 'idle:144': 1, 'idle:216': 5, 'idle:288': 1, 'idle:360': 1,
  'read:0': 0, 'read:72': 7, 'read:144': 1, 'read:216': 1, 'read:288': 1, 'read:360': 2,
};

const fadeMs = (from, to) => {
  const [f1, a1] = SEG[from];
  const [f2, a2] = SEG[to];
  if (f1 !== f2) return 700;            // across files: the poses differ most
  const drift = Math.max(DRIFT[`${f1}:${a1 + SEG_F}`], DRIFT[`${f2}:${a2}`]);
  return drift > 3 ? 450 : 160;
};

/** What he is likely to do, by what is happening. Weights, not sequences. */
const MIX = {
  normal: { idle: 80, listening: 10, excited: 5, thinking: 5 },
  docs: { idle: 65, reading: 20, listening: 10, thinking: 5 },
  tracking: { idle: 70, working: 15, reading: 10, thinking: 5 },
  settings: { idle: 85, listening: 15 },
  chat: { listening: 55, idle: 35, thinking: 10 },
  drowsy: { sleeping: 90, idle: 10 },
  wake: { excited: 50, quick: 50 },
};

/** Which mix a page asks for. The viewer is a document, so it reads. */
const PAGE_MIX = {
  'index.html': 'docs', '': 'docs', 'document.html': 'docs', 'updates.html': 'docs',
  'reviews.html': 'docs', 'changes.html': 'docs', 'signoff.html': 'docs',
  'board.html': 'tracking', 'plan.html': 'tracking', 'costing.html': 'tracking',
  'audit.html': 'tracking', 'agents.html': 'tracking',
  'settings.html': 'settings', 'admin.html': 'settings',
  'chat.html': 'chat',
};

const DROWSY_MS = 25000;
const HIDDEN_KEY = 'adam-mascot-hidden';
const SOUND_KEY = 'adam-mascot-sound';
const VIDEO_KEY = 'adam-mascot-video';

// The still mode, and it is deliberately one frame.
//
// **No states here.** The thirty frames run from neutral to collapse and the
// temptation is to drive them from something; the answer is no. A still image
// that changes is an animation with a stutter, and picking a face without the
// motion to carry it turns a status light into a mood ring. Video on: he acts.
// Video off: he is present and says nothing. Those are the two honest settings.
//
// 5MB of video is also the whole reason this switch exists, so the off setting
// must never fetch either clip.
const FLAT = '/brand/mascot/01-neutral-start.png';

/** The next segment, drawn from the mix. Repeating a non-idle segment is
 *  allowed but unlikely — it is dropped from the draw rather than halved, which
 *  is what stops him reading twice in a row and looking stuck. */
function pickSeg(key, prev) {
  let weights = Object.entries(MIX[key] ?? MIX.normal)
    .filter(([k]) => k === 'idle' || k !== prev);
  if (!weights.length) weights = [['idle', 1]];
  let r = Math.random() * weights.reduce((a, b) => a + b[1], 0);
  for (const [k, v] of weights) { if ((r -= v) <= 0) return k; }
  return weights[0][0];
}

/** Browsers do not load video in a background tab, so every wait here starts
 *  only once the tab is actually on screen. Without this the load times out
 *  while nobody is looking and the still takes over for no reason. */
const whenVisible = () => (document.visibilityState === 'visible'
  ? Promise.resolve()
  : new Promise((resolve) => {
    const f = () => {
      if (document.visibilityState !== 'visible') return;
      document.removeEventListener('visibilitychange', f);
      resolve();
    };
    document.addEventListener('visibilitychange', f);
  }));

// ── the cut between two segments ─────────────────────────────────────

/**
 * A glitch rather than a dissolve. Steps of 40ms that jitter the top layer
 * sideways, sometimes slice it to a horizontal band, split it into red and cyan
 * and flicker the layer underneath — then a hard cut. It covers the pose
 * mismatch at the hub, and it reads as deliberate where a dissolve reads as a
 * video that did not load.
 */
function glitch(from, to, ms, done) {
  const steps = Math.max(3, Math.round(ms / 40));
  const rnd = (a, b) => a + Math.random() * (b - a);
  for (const v of [from, to]) v.style.transition = 'none';
  let i = 0;
  const step = () => {
    if (i >= steps) {
      for (const v of [from, to]) { v.style.transform = ''; v.style.clipPath = ''; v.style.filter = 'none'; }
      to.style.opacity = 1;
      from.style.opacity = 0;
      done();
      return;
    }
    const k = i / (steps - 1);
    const top = Math.random() < 0.35 + k * 0.55 ? to : from;
    const under = top === to ? from : to;
    const split = rnd(0.6, 1.4) * (1 - Math.abs(k - 0.5));
    top.style.opacity = 1;
    under.style.opacity = 1;
    const a = rnd(0, 70);
    const b = rnd(0, 100 - a - 8);
    top.style.clipPath = Math.random() < 0.2 ? `inset(${a.toFixed(0)}% 0 ${b.toFixed(0)}% 0)` : '';
    top.style.transform = `translateX(${rnd(-1.5, 1.5).toFixed(1)}px)`;
    under.style.transform = '';
    top.style.filter = `drop-shadow(${split.toFixed(1)}px 0 0 rgba(255,40,90,.25))`
      + ` drop-shadow(${(-split).toFixed(1)}px 0 0 rgba(0,220,255,.3))`;
    under.style.filter = `brightness(${rnd(1, 1.06).toFixed(2)})`;
    i += 1;
    setTimeout(step, 40);
  };
  step();
}

// ── keying the backdrop out ──────────────────────────────────────────

const KEY_FS = 'precision mediump float;varying vec2 v;uniform sampler2D t;uniform vec2 c0,c1;'
  + 'void main(){vec2 uv=vec2(mix(c0.x,c1.x,v.x),mix(c0.y,c1.y,v.y));vec3 c=texture2D(t,uv).rgb;'
  + 'vec3 bg=(texture2D(t,vec2(c0.x+.01,.02)).rgb+texture2D(t,vec2(c1.x-.01,.02)).rgb'
  + '+texture2D(t,vec2(c0.x+.01,.98)).rgb+texture2D(t,vec2(c1.x-.01,.98)).rgb)*.25;'
  + 'float a=smoothstep(.035,.12,distance(c,bg));'
  + 'vec3 col=a>.002?clamp(bg+(c-bg)/a,0.,1.):vec3(0.);gl_FragColor=vec4(col*a,a);}';

function makeKeyer(canvas) {
  const gl = canvas.getContext('webgl', { premultipliedAlpha: true, alpha: true });
  if (!gl) return null;
  const sh = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    return s;
  };
  const p = gl.createProgram();
  gl.attachShader(p, sh(gl.VERTEX_SHADER,
    'attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0,1);}'));
  gl.attachShader(p, sh(gl.FRAGMENT_SHADER, KEY_FS));
  gl.linkProgram(p);
  gl.useProgram(p);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(p, 'p');
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  for (const k of [gl.TEXTURE_WRAP_S, gl.TEXTURE_WRAP_T]) gl.texParameteri(gl.TEXTURE_2D, k, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  const u0 = gl.getUniformLocation(p, 'c0');
  const u1 = gl.getUniformLocation(p, 'c1');

  return (video) => {
    if (video.readyState < 2 || !video.videoWidth) return;
    const dpr = window.devicePixelRatio || 1;
    const pw = Math.round(canvas.clientWidth * dpr);
    const ph = Math.round(canvas.clientHeight * dpr);
    if (canvas.width !== pw || canvas.height !== ph) { canvas.width = pw; canvas.height = ph; }
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, video);
    // Crop rather than stretch, so the character keeps his proportions whatever
    // shape the dock is.
    const ca = (canvas.width || 1) / (canvas.height || 1);
    const va = video.videoWidth / video.videoHeight;
    const fx = ca < va ? ca / va : 1;
    const fy = ca < va ? 1 : va / ca;
    const x0 = (1 - fx) / 2;
    const y0 = (1 - fy) / 2;
    gl.uniform2f(u0, x0, y0);
    gl.uniform2f(u1, 1 - x0, 1 - y0);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  };
}

// ── the dock ─────────────────────────────────────────────────────────

const HTML = `
<div class="mascot-dock" id="mascot-dock" data-vid="loading">
  <div class="mascot-controls">
    <button class="mascot-sound" id="mascot-sound" type="button"></button>
    <button class="mascot-video" id="mascot-video" type="button"></button>
    <button class="mascot-dismiss" id="mascot-dismiss" type="button" aria-label="Hide Adam">
      <svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor"
           stroke-width="1.7" stroke-linecap="round"><path d="M4 4l8 8M12 4l-8 8" /></svg>
    </button>
  </div>
  <button class="mascot-hit" id="mascot-hit" type="button" aria-label="Ask Adam about the package">
    <span class="mascot-stage" id="mascot-stage">
      <video id="mascot-v0" muted playsinline preload="auto" aria-hidden="true"></video>
      <video id="mascot-v1" muted playsinline preload="auto" aria-hidden="true"></video>
      <canvas id="mascot-c0" aria-hidden="true"></canvas>
      <canvas id="mascot-c1" aria-hidden="true"></canvas>
      <img class="mascot-still" id="mascot-still" src="${STILL}" alt="" aria-hidden="true" />
      <img class="mascot-flat" id="mascot-flat" alt="" aria-hidden="true" />
    </span>
  </button>
</div>`;

const SPEAKER = 'M2.5 6h2.5L8.5 3v10L5 10H2.5z';
const WAVES = 'M10.8 5.8a3 3 0 0 1 0 4.4M12.7 4a5.5 5.5 0 0 1 0 8';
const CROSS = 'M11 6l3.5 4M14.5 6 11 10';

const read = (key, fallback) => {
  try { return localStorage.getItem(key) ?? fallback; } catch { return fallback; }
};
const write = (key, value) => {
  try { localStorage.setItem(key, value); } catch { /* nothing to do */ }
};

/** Set while a dock is mounted, so the toggle can take one down cleanly. A
 *  second requestAnimationFrame loop drawing into a detached canvas is a leak
 *  nobody sees until the fans come on. */
let teardown = null;

export function mountMascot() {
  if (document.getElementById('mascot-dock')) return;
  if (read(HIDDEN_KEY, '0') === '1') return;

  document.body.insertAdjacentHTML('beforeend', HTML);
  const dock = document.getElementById('mascot-dock');
  const vids = [document.getElementById('mascot-v0'), document.getElementById('mascot-v1')];
  const cvs = [document.getElementById('mascot-c0'), document.getElementById('mascot-c1')];

  // Sound off until asked, and off until the reader has clicked something —
  // browsers refuse to start audio before a gesture, and a control that claims
  // to be on while nothing plays is worse than one that is plainly off.
  let sound = read(SOUND_KEY, '0') === '1';
  let gestured = false;
  const soundBtn = document.getElementById('mascot-sound');
  const paintSound = () => {
    soundBtn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"'
      + ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
      + `<path d="${SPEAKER}" /><path d="${sound ? WAVES : CROSS}" /></svg>`;
    soundBtn.title = sound ? 'Mute Adam' : 'Unmute Adam';
    soundBtn.setAttribute('aria-label', soundBtn.title);
    dock.dataset.sound = sound ? 'on' : 'off';
  };
  paintSound();
  soundBtn.onclick = (event) => {
    event.stopPropagation();
    sound = !sound;
    gestured = true;
    write(SOUND_KEY, sound ? '1' : '0');
    paintSound();
  };
  addEventListener('pointerdown', () => { gestured = true; }, { once: true });

  document.getElementById('mascot-dismiss').onclick = (event) => {
    event.stopPropagation();
    if (teardown) teardown();
    dock.remove();
    write(HIDDEN_KEY, '1');
  };

  // Video on or off. Off is a real setting, not a degraded one: no clip is
  // fetched, nothing decodes, and the corner holds one still frame.
  let video = read(VIDEO_KEY, '1') === '1';
  const videoBtn = document.getElementById('mascot-video');
  const paintVideo = () => {
    videoBtn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor"'
      + ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
      + '<rect x="1.8" y="4" width="8.6" height="8" rx="1.6" />'
      + `<path d="M10.4 7.2 14.2 5v6l-3.8-2.2z" />${video ? '' : '<path d="M2.5 13.5 13.5 2.5" />'}`
      + '</svg>';
    videoBtn.title = video ? 'Turn the animation off' : 'Turn the animation on';
    videoBtn.setAttribute('aria-label', videoBtn.title);
    videoBtn.setAttribute('aria-pressed', String(video));
    dock.dataset.mode = video ? 'video' : 'flat';
  };
  paintVideo();
  videoBtn.onclick = (event) => {
    event.stopPropagation();
    video = !video;
    write(VIDEO_KEY, video ? '1' : '0');
    // Remounted rather than switched in place: the engine holds two videos, two
    // canvases, a keyer and a loop, and tearing all that down by hand on every
    // toggle is more moving parts than building it again.
    if (teardown) teardown();
    dock.remove();
    mountMascot();
  };

  if (!video) {
    // The still mode ends here. No <video>, no WebGL, no loop, no clip fetched:
    // the two source files are 5MB and the point of the switch is not paying it.
    document.getElementById('mascot-flat').src = FLAT;
    dock.dataset.vid = 'flat';
    document.getElementById('mascot-sound').hidden = true;
    teardown = () => { teardown = null; };
    return;
  }

  // Clicking him is how you ask. The floating chat panel belongs to the wider
  // redesign; until that lands this opens the chat page that already exists,
  // which is the same conversation on the same key.
  document.getElementById('mascot-hit').onclick = () => { location.href = '/chat.html'; };

  // ── the engine ─────────────────────────────────────────────────────

  const state = {
    front: 0,
    cur: 'idle',
    mix: PAGE_MIX[location.pathname.split('/').pop()] ?? 'normal',
    pending: null,
    busy: false,
  };
  let alive = true;
  let loaded = false;
  let lastMove = Date.now();
  let drowsing = false;

  for (const [i, v] of vids.entries()) {
    v._cv = cvs[i];
    v._draw = makeKeyer(cvs[i]);
  }
  const canvasOf = (v) => v._cv;

  const load = async (v, seg) => {
    const [file, at] = SEG[seg];
    if (v.dataset.f !== file) {
      v.dataset.f = file;
      for (let i = 0; ; i += 1) {
        await whenVisible();
        v.src = VFILES[file] + (i ? `?r=${Date.now()}${i}` : '');
        const ok = await new Promise((resolve) => {
          const t = setTimeout(() => resolve(false), 3500);
          v.onloadeddata = () => { clearTimeout(t); resolve(true); };
          v.onerror = () => { clearTimeout(t); resolve(false); };
        });
        if (ok) break;
        if (i >= 3) throw new Error('video load');
      }
    }
    await new Promise((resolve) => { v.onseeked = resolve; v.currentTime = at / VFPS + 0.001; });
  };

  const fail = () => { dock.dataset.vid = 'fail'; };

  let guard;
  whenVisible().then(() => {
    guard = setTimeout(() => { if (alive && !loaded) fail(); }, 16000);
  });

  load(vids[0], 'idle').then(() => {
    if (!alive) return;
    loaded = true;
    clearTimeout(guard);
    dock.dataset.vid = 'ready';
    vids[0].play().catch(() => {});
  }).catch(fail);

  const swap = async () => {
    state.busy = true;
    const v = vids[state.front];
    const o = vids[1 - state.front];
    const key = state.pending || state.mix;
    state.pending = null;
    const next = pickSeg(key, state.cur);
    try { await load(o, next); } catch { state.busy = false; return; }

    const end = (SEG[state.cur][1] + SEG_F - 1) / VFPS - 0.5 / VFPS;
    const wait = () => {
      if (!alive) return;
      const ms = Math.round(fadeMs(state.cur, next) * 0.45);
      if (v.currentTime >= end - ms / 2000 || v.ended) {
        o.play().catch(() => {});
        state.front = 1 - state.front;
        state.cur = next;
        glitch(canvasOf(v), canvasOf(o), ms, () => { v.pause(); state.busy = false; });
      } else requestAnimationFrame(wait);
    };
    wait();
  };

  const tick = () => {
    if (!alive) return;
    const v = vids[state.front];
    const back = vids[1 - state.front];

    const wantMuted = !(sound && gestured);
    if (v.muted !== wantMuted) v.muted = wantMuted;
    if (v.volume !== 0.35) v.volume = 0.35;
    if (!back.muted) back.muted = true;

    for (const x of vids) if (x._draw && (x === v || state.busy)) x._draw(x);
    if (loaded && v.paused && !state.busy) v.play().catch(() => {});

    // Dozing off, and waking up. Queued rather than ambient, so it wins the next
    // hub instead of waiting for the current mix to happen to pick it.
    const still = Date.now() - lastMove > DROWSY_MS;
    if (still && !drowsing) { drowsing = true; state.mix = 'drowsy'; state.pending = 'drowsy'; }
    if (!still && drowsing) {
      drowsing = false;
      state.mix = PAGE_MIX[location.pathname.split('/').pop()] ?? 'normal';
      state.pending = 'wake';
    }

    if (!state.busy && v.readyState >= 2 && !v.paused) {
      const end = (SEG[state.cur][1] + SEG_F - 1) / VFPS;
      if (end - v.currentTime < 1.0) swap();
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);

  const stir = () => { lastMove = Date.now(); };
  for (const ev of ['pointermove', 'keydown', 'pointerdown', 'wheel']) {
    addEventListener(ev, stir, { passive: true });
  }

  teardown = () => {
    alive = false;
    clearTimeout(guard);
    for (const v of vids) { try { v.pause(); v.removeAttribute('src'); v.load(); } catch { /* going away */ } }
    for (const ev of ['pointermove', 'keydown', 'pointerdown', 'wheel']) removeEventListener(ev, stir);
    teardown = null;
  };

  // A tab that comes back after a failure deserves another go: the usual cause
  // is that it was in the background when the load was given up on.
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible' && dock.dataset.vid === 'fail' && !loaded) {
      dock.dataset.vid = 'loading';
      load(vids[0], 'idle').then(() => {
        loaded = true;
        dock.dataset.vid = 'ready';
        vids[0].play().catch(() => {});
      }).catch(fail);
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', mountMascot, { once: true });
} else {
  mountMascot();
}
