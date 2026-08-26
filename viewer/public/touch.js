// Touch gestures for the canvas renderers.
//
// The four canvases were built mouse-first: mousedown/mousemove/mouseup pan and
// drag, wheel zooms. On a phone none of that exists, so this adds the three
// gestures a canvas is expected to answer to — one finger pans, two fingers
// pinch and pan, a tap selects — once, here, rather than four times over.
//
// WHY POINTER EVENTS, AND WHY ONLY FOR pointerType === 'touch'
//
// Pointer Events are used because they carry a pointerId, which is what makes a
// two-finger gesture tractable: a Map keyed by id, rather than reconciling
// TouchList identifiers by hand. They are NOT used to replace the mouse path.
// A mouse produces both pointer events and mouse events, so a unified handler
// would run alongside the existing one and double every pan. Rewriting the
// mouse path onto pointer events instead would mean re-deriving node dragging,
// hover highlighting, row clicks and dblclick in four files — the one thing
// this change must not disturb. So this listener ignores everything that is not
// a real finger, and the mouse keeps the code it already had.
//
// Pen is left to the mouse path too: a stylus emits compatibility mouse events,
// so it already pans, drags nodes and hovers, which is more than this file
// would give it.
//
// THE COMPATIBILITY MOUSE EVENTS HAVE TO GO
//
// A finger also synthesises mousedown/mousemove/mouseup/click, and those would
// reach the renderers' own handlers — a one-finger drag would pan twice, and
// lifting off a node would fire a select the pan was never meant to produce.
// Cancelling the touch events kills the synthesised mouse events at the source.
// It also stops the page scrolling under the gesture, so the canvases behave
// correctly whether or not `touch-action: none` is set on them in CSS.

const TAP_SLOP = 8; // px of travel still counted as a tap, not a pan
const TAP_MS = 300; // longer than this reads as a press, not a tap

/**
 * @param canvas   the element the renderer draws into
 * @param target   the renderer instance — needs `transform` and `draw()`
 * @param options.min      smallest allowed transform.k (each renderer differs)
 * @param options.max      largest allowed transform.k
 * @param options.toWorld  (sx, sy) -> world point, in canvas-relative CSS px.
 *                         Defaults to the renderer's own method. Passed
 *                         explicitly by renderers that project differently.
 * @param options.onTap    (sx, sy) -> void, the click behaviour for a tap
 */
export function enableTouch(canvas, target, options = {}) {
  const { min = 0.08, max = 6, onTap } = options;
  const toWorld = options.toWorld ?? ((sx, sy) => target.toWorld(sx, sy));

  // live fingers, in canvas-relative CSS pixels
  const points = new Map();
  let pinch = null; // { distance, x, y } from the previous move
  let tap = null; // candidate tap, discarded as soon as the gesture grows

  // Touch events carry no offsetX/offsetY, and the canvases are DPR-scaled — the
  // backing store is larger than the box. Every hit test and every transform in
  // these renderers works in CSS pixels relative to the canvas, which is what
  // the bounding rect gives us, and what offsetX gives the mouse handlers.
  const at = (e) => {
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  };

  const adjusted = () => {
    // Auto-framing backs off once the view is the user's. StructureTree does not
    // read the flag, but setting it costs nothing and keeps one code path here.
    target.userAdjusted = true;
  };

  const pan = (dx, dy) => {
    target.transform.x += dx;
    target.transform.y += dy;
  };

  // Zoom about a fixed screen point, by the same route the wheel handlers take:
  // measure the world point under it, change k, measure again, and translate by
  // the difference. That works for both projections in use here — the centred
  // one in graph/boxdiagram/statemachine and the top-left one in structure —
  // because it never needs to know where the origin is.
  const zoomAbout = (factor, sx, sy) => {
    const next = Math.max(min, Math.min(max, target.transform.k * factor));
    if (next === target.transform.k) return;
    const before = toWorld(sx, sy);
    target.transform.k = next;
    const after = toWorld(sx, sy);
    target.transform.x += (after.x - before.x) * next;
    target.transform.y += (after.y - before.y) * next;
  };

  const centre = () => {
    const [a, b] = [...points.values()];
    return {
      x: (a.x + b.x) / 2,
      y: (a.y + b.y) / 2,
      distance: Math.max(1, Math.hypot(b.x - a.x, b.y - a.y)),
    };
  };

  canvas.addEventListener('pointerdown', (e) => {
    if (e.pointerType !== 'touch') return;
    const p = at(e);
    points.set(e.pointerId, p);
    // Keep receiving moves once a finger slides off the canvas — a pan that
    // stops dead at the edge feels broken.
    canvas.setPointerCapture?.(e.pointerId);

    if (points.size === 1) {
      tap = { x: p.x, y: p.y, at: performance.now() };
      pinch = null;
    } else {
      // A second finger turns whatever was happening into a pinch, and a pinch
      // is never a selection — so the pending tap goes. This is also what stops
      // a two-finger gesture that started on a node from dragging it: the touch
      // path never drags nodes, it only pans, zooms and taps.
      tap = null;
      if (points.size === 2) pinch = centre();
    }
  });

  canvas.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'touch' || !points.has(e.pointerId)) return;
    const previous = points.get(e.pointerId);
    const p = at(e);
    points.set(e.pointerId, p);

    if (points.size >= 2) {
      if (!pinch) { pinch = centre(); return; }
      const now = centre();
      adjusted();
      zoomAbout(now.distance / pinch.distance, now.x, now.y);
      // Two fingers translate as well as scale. Without this the diagram is
      // pinned under the gesture and only grows, which reads as a stuck view.
      pan(now.x - pinch.x, now.y - pinch.y);
      pinch = now;
      target.draw();
      return;
    }

    if (tap && (Math.abs(p.x - tap.x) > TAP_SLOP || Math.abs(p.y - tap.y) > TAP_SLOP)) {
      tap = null; // travelled too far — this is a pan, and must not select
    }
    adjusted();
    pan(p.x - previous.x, p.y - previous.y);
    target.draw();
  });

  const release = (e) => {
    if (e.pointerType !== 'touch' || !points.has(e.pointerId)) return;
    points.delete(e.pointerId);
    canvas.releasePointerCapture?.(e.pointerId);

    if (points.size >= 1) {
      // Down to one finger after a pinch. Re-seed so the survivor pans from
      // where it is rather than jumping by the gap between the two fingers, and
      // leave `tap` null so lifting a finger cannot select.
      pinch = points.size >= 2 ? centre() : null;
      return;
    }

    pinch = null;
    const candidate = tap;
    tap = null;
    if (!candidate || e.type !== 'pointerup') return;
    if (performance.now() - candidate.at > TAP_MS) return;
    const p = at(e);
    if (Math.abs(p.x - candidate.x) > TAP_SLOP || Math.abs(p.y - candidate.y) > TAP_SLOP) return;
    onTap?.(p.x, p.y);
  };

  canvas.addEventListener('pointerup', release);
  canvas.addEventListener('pointercancel', release);

  // See the note at the top: this is what keeps the synthesised mouse events —
  // and the page's own scrolling — out of the way of the gesture.
  const swallow = (e) => { if (e.cancelable) e.preventDefault(); };
  canvas.addEventListener('touchstart', swallow, { passive: false });
  canvas.addEventListener('touchmove', swallow, { passive: false });
  canvas.addEventListener('touchend', swallow, { passive: false });
}
