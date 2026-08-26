// The particle-field renderer: a slowly turning sphere of labelled hubs over an
// unlabelled mass, with directed links that carry a travelling packet.
//
// Lifted from `buildGalaxy()` / `drawGalaxy()` in the design package
// (`ui-design/designs/Viewer Redesign - Topbar Night.dc.html`, specified in
// `ui-design/GRAPH.md`). Every constant below is the design's; what is new here
// is that it takes its model from a caller instead of a hard-coded array, and
// that it can be clicked — the design has no hit test at all, and every view
// that uses this has to open something.
//
// WHAT IT IS FOR, AND WHAT IT IS NOT FOR
//
// Three ingredients, and a view wants this renderer only if it has all three:
//
//   hubs    a few dozen things worth naming
//   mass    hundreds or thousands of things not worth naming individually,
//           but very much worth weighing
//   flow    links where the direction is part of the claim
//
// The Domain event catalogue has all three; so does the database at whole-
// schema scope. A journey does not — its order is the content, and a rotating
// sphere destroys order. A state machine does not — direction there is a
// specific legal move, not a flow. Those keep their own renderers.
//
// WHY IT OWNS ITS PALETTE
//
// Everything else in the viewer reads its colours from the CSS custom
// properties so the day/night toggle reaches it. This does not: twelve kinds
// times two stops is twenty-four `getComputedStyle` reads a frame, on a canvas
// that redraws continuously. It carries the two tables instead and picks one
// per frame, which is the same answer the toggle would have given.
//
// THE PICTURE IS BUILT OUT OF BLENDING, AND BLENDING HAS A GROUND
//
// Everything except the labels is composited rather than painted in order, so
// overlap accumulates and the scene reads as a nebula rather than a scatter
// plot. That is the whole effect, and it is what made a light theme look
// impossible for a long time: `lighter` on a pale ground moves every colour
// toward white and the picture disappears.
//
// The way through is that `lighter` is not the effect — *accumulation* is. On
// a pale ground the same construction runs with `multiply` and dark ink: each
// overlap subtracts light instead of adding it, depth still reads as density,
// and no draw call had to change. So the two themes are one renderer with two
// grounds, and the ink table below has two halves for the same reason.
//
// The field is `.galaxy-field` in layers.css, per theme to match.

// ── the design's constants ──────────────────────────────────────────
const GOLD = Math.PI * (3 - Math.sqrt(5));

const YAW_RATE = 0.11;          // radians/sec — one turn in ~57s
const PITCH_BASE = -0.34;
const PITCH_SWING = 0.06;
const PITCH_RATE = 0.07;
const FOV = 3.1;

const CORE_SHELL = 0.34;        // where the innermost tier sits, as a fraction
// The flat layout's rings. The innermost was 0.17, which is right for the two
// shared contracts the design put there and wrong for every model built since:
// the Events flow puts six sources on it and the Data galaxy more. A ring that
// small has no circumference to seat anything on.
const RINGS = { core: 0.32, spine: 0.68, satellite: 1 };
const RING_OFFSET = { satellite: 0.22 }; // so satellites do not sit on the spokes

// A cluster's spread, and how many motes it is worth. Both compressed, for the
// same reason the hub radius is: a schema with 60 tables against one with 3
// should look bigger, not twenty times bigger.
const CLUSTER_MIN_R = 0.075;
const CLUSTER_SCALE = 0.019;
const CLUSTER_MAX_R = 0.30;
// How much of the gap to its neighbour a cluster may fill. Under a half so
// that two adjacent clouds have clear space between them rather than meeting.
const CLUSTER_CROWD = 0.40;
const CLUSTER_FLOOR = 4;        // a hub with any mass at all gets a visible halo
const CLUSTER_CEILING = 200;

const MOTE_MIN = 200;
const MOTE_MAX = 900;           // past this the O(n²) filament pass starts to cost
const FILAMENT_D2 = 0.011;      // tuned by the design at 900 motes — see below
const FILAMENT_NEAR = 3;

// The panel the design draws into is 520px tall, which puts its projection
// radius at about 192px. Ours is the whole main column. Every radius below is
// an absolute pixel count in the design, and absolute pixels do not survive
// that change of scale: at 520px they make a body, and at 900px the same
// numbers make a scatter of 1px dots with a great deal of black around them.
// So sizes are expressed against the design's own reference and scaled.
// Text is not — 10.5px is 10.5px whatever the panel does.
// Past this many lanes the flow treatment is switched off unless something is
// hovered. Two reasons, and they agree: a dashed stroke is by far the most
// expensive primitive here — 640 of them costs about ten times the frame budget
// — and 640 lanes all marching at once is a texture rather than a set of
// directions anybody can follow. Measured at 5fps before, 50 after.
const DENSE_LANES = 140;

// How much of the model is travelling at once, and how long the window takes to
// sweep all the way round. The floor keeps a small model from looking dead; the
// ceiling is the point of the whole thing — past a couple of dozen moving
// objects the eye reads static rather than direction.
const ACTIVE_SHARE = 0.16;
const ACTIVE_MIN = 4;
const ACTIVE_MAX = 7;
const ACTIVE_PERIOD = 11;      // seconds
// What a lane that is not travelling is worth. Drawn, so the structure holds,
// and clearly behind the ones that are.
const LANE_RESTING = 0.6;
// What an isolate leaves of everything it is not about. Low, but never zero:
// the scene has to keep its shape, or a hover reads as a filter that deleted
// the rest of the picture rather than as emphasis on part of it.
const DIM_HUB = 0.16;
const DIM_MASS = 0.1;
const DIM_WEB = 0.12;
const DIM_HOOP = 0.06;

// 2D lanes. Quiet at rest and loud under the pointer.
//
// The first pass at this made them prominent full stop, on the reasoning that
// 3D carries the structure in the motion and 2D has no motion to carry it. That
// was right about the resting state being too faint and wrong about the fix:
// sixty lanes all shouting is not a diagram, it is a mesh, and the thing a
// reader actually wants to know — what does *this* one touch — was no easier to
// see than before. So the resting weight is low enough to read as background,
// and hovering a hub lights the lanes that touch it and dims the rest.
const LINK_FLAT = 0.2;
const LINK_FLAT_DENSE = 0.13;
const LINK_FLAT_HOT = 0.8;
const LINK_FLAT_WIDTH = 1;
const LINK_FLAT_WIDTH_HOT = 1.7;

// The mote clouds in 2D. Kept, because the size of a cloud is the one thing
// that says how much a hub holds, and dropped to a fifth of their 3D weight,
// because in a still picture they stop reading as a cloud and start reading as
// grain over the top of the diagram. The cloud under the pointer comes back to
// full: at that moment it is the thing being looked at rather than background.
const MOTE_FLAT = 0.22;
const MOTE_FLAT_HOT = 1;

// No hub is a floodlight. See the note in the change that added this: the
// compression below is right and simply runs out of headroom when a caller
// hands it a weight two orders of magnitude past what the design ever saw.
// Set above the largest radius any existing view produces, so this only ever
// catches the outlier it was written for.
const HUB_R_MAX = 7;

// Roughly what a label occupies along a ring, in pixels. Used to work out how
// many names a ring can seat before they start overlapping each other.
const LABEL_SEAT = 84;

const REFERENCE_R = 192;
const UNIT_MIN = 0.85;
const UNIT_MAX = 2.2;

// Held frame for `prefers-reduced-motion` — far enough in that the packets are
// mid-flight and the sphere is off-axis, so the still frame is a picture rather
// than a diagram of the starting position.
const STILL_T = 4.2;

// What the reader's hand does. The drag rates are radians per pixel — a little
// under a full turn across a 1000px canvas, which is fast enough to get to the
// far side without being twitchy. Pitch is clamped short of the pole because
// past vertical the scene reads as upside down rather than as tilted.
const DRAG_YAW = 0.0062;
const DRAG_PITCH = 0.0052;
const PITCH_LIMIT = 1.25;
const DRAG_SLOP = 3;            // px of travel before it stops being a click
const ZOOM_STEP = 0.0014;       // per wheel pixel
const ZOOM_MIN = 0.35;
const ZOOM_MAX = 8;

// Where a cluster stops being a quantity and starts being a list. Below this a
// mote is anonymous, which is the point of it; above it, the ones that have
// names get them — nearest first, and never more than will fit being read.
const SUB_ZOOM = 1.7;
// The ring of views round a focused body. The radius is a floor plus the body's
// own cloud, so the ring sits outside the mass rather than inside it.
const VIEW_DOT = 4.2;
const VIEW_HIT = 20;

// How far apart two view motes have to be on screen, so their names do not
// land on top of each other, and how deep into the cloud to look for them.
const VIEW_GAP = 62;
const VIEW_POOL = 90;

// Flying into a body. Per frame rather than per millisecond, to match every
// other easing in this file — the loop is the clock here.
const WARP_STEP = 0.055;
const WARP_OUT = 2.4;   // how far the outgoing scene expands past the edge
const WARP_IN = 0.5;    // how small the incoming one starts
const SUB_LABELS = 34;

// The camera, for a scene that is navigated rather than watched. Its rotation
// is slower than the graph's because a body here is a destination and a reader
// is aiming at it; slower again once one is focused, so the thing just chosen
// does not walk out from under the pointer.
const CAM_YAW = 0.075;
const CAM_YAW_FOCUS = 0.03;
const CAM_PITCH_BASE = -0.2;
const CAM_PITCH_SWING = 0.05;
const CAM_PITCH_RATE = 0.06;
const CAM_UNIT_W = 0.175;       // world unit → px, against the shorter of these
const CAM_UNIT_H = 0.245;
// Near enough to orthographic. The sphere's 1.35 assumes every point is inside
// a unit radius; a constellation 1.5 units wide magnifies its near bodies by
// 2.9 under that divisor and walks them out of the window. See the note above.
const CAM_DEPTH = 0.55;
const CAM_ZOOM = 2.8;           // focused, in 3D
const CAM_ZOOM_FLAT = 1.7;      // flat has no depth to push through, so gentler
// Biased right of centre, which is what keeps the scene clear of the hero copy.
const CAM_AT = { x: 0.58, y: 0.5 };
const CAM_AT_FOCUS = { x: 0.66, y: 0.46 };
// Per frame, and deliberately not a duration: the target is recomputed every
// frame, so a second click mid-flight simply retargets. A tween would have to
// be cancelled and restarted, and would arrive at a stale position.
// How long the camera takes to fly to a body, in seconds, and the shape it
// flies on. See flight.py: a per-frame fraction of the remaining distance is
// fastest at the instant it starts and never arrives, which is why this used to
// read as a cut followed by a drift however small the fraction was made.
//
// Smoothstep: zero rate at both ends, so it leaves slowly, crosses the middle —
// where the relation between the two places is actually legible — quickly, and
// settles rather than stopping.
const CAM_FLIGHT = 1.15;
const smoothstep = (u) => u * u * (3 - 2 * u);

// The scale trails the pan slightly. Arriving together makes the body appear to
// rush its last few pixels; a scale that settles a moment afterwards reads as
// coming to rest.
const CAM_FLIGHT_ZOOM = 1.45;

const INK_DARK = {
  core: { core: '252,230,184', body: '224,174,82' },      // shared / innermost
  spine: { core: '214,248,246', body: '72,207,203' },
  satellite: { core: '175,235,232', body: '43,179,176' },
  mote: '150,232,228',
  moteHot: '224,250,248',
  moteMid: '96,214,210',
  moteRim: '72,207,203',
  filament: '120,214,210',
  linkCritical: '224,174,82',
  linkOrdinary: '120,214,210',
  packetCritical: '255,224,166',
  packetOrdinary: '207,247,245',
  label: '226,242,241',
  sublabel: '147,166,165',
  guide: 'rgba(143,207,204,.16)',
};

/**
 * What a thing is, as a core and a body — the same two-stop shape the tiers
 * use, so a kind and a tier are interchangeable everywhere a tint is asked for.
 *
 * Dark-field values. See the note at the head of this change for why they are
 * not read off --kind-*.
 */
const KIND_DARK = {
  contract:   { core: '214,248,246', body: '72,207,203' },
  operation:  { core: '198,222,255', body: '106,165,245' },
  schema:     { core: '198,240,216', body: '95,194,138' },
  enum:       { core: '226,214,248', body: '169,138,224' },
  permission: { core: '250,214,234', body: '224,122,176' },
  param:      { core: '252,230,184', body: '224,174,82' },
  response:   { core: '252,216,190', body: '224,133,79' },
  security:   { core: '224,228,228', body: '154,160,160' },
  screen:     { core: '252,220,208', body: '234,143,114' },
  table:      { core: '208,232,248', body: '111,179,224' },
  event:      { core: '232,220,250', body: '183,154,232' },
  decision:   { core: '212,238,246', body: '127,192,216' },
};

/**
 * The day half.
 *
 * Not an inversion of the table above — these are the viewer's own `--kind-*`
 * day tokens, so a contract is the same teal here as it is in the tree, the
 * legend and every chip. What *is* inverted is which stop is the loud one:
 * under `multiply` more ink means darker, so `core` is the deeper value and
 * `body` the lighter, exactly opposite to the night table where `core` is the
 * bright centre of a glow.
 */
const KIND_LIGHT = {
  contract:    { core: '33,141,174', body: '86,168,193' },
  operation:   { core: '43,187,215', body: '94,203,225' },
  schema:      { core: '18,86,107', body: '75,127,143' },
  enum:        { core: '108,79,163', body: '143,121,185' },
  permission:  { core: '194,37,92', body: '209,89,131' },
  param:       { core: '176,122,36', body: '195,154,89' },
  response:    { core: '217,84,31', body: '226,125,85' },
  security:    { core: '74,92,99', body: '117,131,136' },
  screen:      { core: '162,96,63', body: '184,134,109' },
  table:       { core: '58,111,181', body: '105,146,199' },
  event:       { core: '123,63,160', body: '155,109,183' },
  decision:    { core: '21,144,133', body: '77,171,162' },
};

const INK_LIGHT = {
  // Gold at the centre of the story, the two deeper blues stepping outward.
  // Warm against a cool ground, which is why one accent can hold the eye
  // across a picture this busy — and why the ground stayed cool.
  core: { core: '176,122,36', body: '195,154,89' },
  spine: { core: '18,86,107', body: '75,127,143' },
  satellite: { core: '33,141,174', body: '86,168,193' },
  // Dust carries real colour rather than being haze. On a pale field a grey
  // speck is the ground, so the mass has to be blue to exist at all.
  mote: '74,135,163',
  moteHot: '176,122,36',
  moteMid: '74,135,163',
  moteRim: '128,170,192',
  filament: '150,185,203',
  // Pale blue recedes, gold advances. Half the lanes in the real model are
  // critical, so the warm one is kept in check by alpha rather than by dulling
  // the hue — see STYLE_LIGHT.linkLoud.
  linkOrdinary: '143,180,198',
  linkCritical: '176,122,36',
  packetOrdinary: '33,141,174',
  packetCritical: '176,122,36',
  label: '14,43,54',
  sublabel: '90,122,136',
  guide: 'rgba(33,141,174,.20)',
};

/**
 * How hard to press, per ground.
 *
 * The palettes above answer "what colour"; this answers "how much", and it is
 * the half a straight port of the night theme gets wrong. Under `lighter` a
 * soft wide halo is light spilling off a body, and forty of them stacked build
 * a nebula. Under `multiply` the identical call is ink soaking outward, and
 * forty of those converge on mud — a dense cluster stops reading as bright and
 * starts reading as a grey thumbprint. Same geometry, same alphas, opposite
 * result.
 *
 * So the day column is not a dimmed night. The blooms pull in and lighten, and
 * the hard centres get *more* solid to pay for it: what carries a node on a
 * dark ground is its glow, and what carries it on a pale one is its edge.
 *
 * The two link multipliers are the other asymmetry. Additive on black, gold and
 * teal glow about equally, so gold needed only a nudge to lead. Multiplied on
 * white, gold has far more contrast to spend than pale teal has — left at the
 * night ratio the critical lanes read as a tan cross-hatch over a picture whose
 * ordinary lanes have gone missing. Day closes the gap from the other side.
 */
const STYLE_DARK = {
  // Depth and dimming both fade toward the ground, and "toward the ground"
  // means opposite things per theme. Additive on black, an alpha of .04 is
  // still a faint star; multiplied on paper it is the paper. Left alone the
  // back of the sphere and everything not currently lit simply wash out —
  // which is the white-out, and it is not a palette problem.
  zK: 1,           // how hard depth attenuates
  dim: 1,          // multiplier on the DIM_* constants
  floorHub: 0.24,  // alpha a hub cannot fall below
  floorMote: 0,
  floorLink: 0.04,
  bloom: 1,        // halo + packet radius
  halo: 1,         // hub halo alpha
  core: 1,         // hub centre alpha
  coreR: 1,        // hub centre radius
  mote: 1,         // mote cloud alpha
  moteCore: 1,     // promoted mote centre alpha
  web: 1,          // filament alpha
  linkLoud: 1,     // critical lane alpha
  linkQuiet: 0.8,  // ordinary lane alpha
  packet: 1,
};

const STYLE_LIGHT = {
  // Compressed, not merely raised: the far side has to stay *read* as far
  // without being able to spend the last of its contrast getting there.
  zK: 0.55,
  dim: 2.6,
  floorHub: 0.46,
  floorMote: 0.12,
  floorLink: 0.15,
  // Raised against the pre-buffer values. Those were mixed for `multiply`,
  // where every overlap compounds the picture darker on its own; laying the
  // accumulated ink over the ground once does not, so the same numbers came
  // out about a third too pale.
  bloom: 0.78,
  halo: 0.78,
  core: 1.25,
  coreR: 1.15,
  // Not as low as the mud argument alone suggests. Cut far enough to kill the
  // thumbprint and the sphere loses its mass with it — the starfield is what
  // makes the thing a body rather than a wire diagram, and a day picture that
  // drops it is tidy and says less than the night one.
  mote: 1.05,
  moteCore: 1.3,
  web: 0.95,
  // Coral leads, but it is carrying half the lanes in the real model, so the
  // lead is a small one — held by alpha, not by letting the hue shout.
  linkLoud: 0.9,
  linkQuiet: 1.35,
  packet: 0.85,
};

/**
 * The ground in force, swapped once per frame at the top of `draw()`.
 *
 * Module-level and mutable, rather than threaded through the nine private
 * draw methods as an argument. A frame is synchronous from `clearRect` to the
 * last label — there is no await anywhere inside it — so two instances drawing
 * in the same tick cannot interleave and see each other's palette.
 */
let INK = INK_DARK;
let KIND = KIND_DARK;
let STYLE = STYLE_DARK;

/** A tier, a kind, or the fallback — every tint lookup goes through here. */
const tintOf = (name) => KIND[name] ?? INK[name] ?? INK.spine;

/** Day unless the toggle says otherwise — the same test theme.js writes. */
const isNight = () => document.documentElement.dataset.theme === 'dark';

const LABEL_FONT = '600 10.5px "Plus Jakarta Sans", ui-sans-serif, system-ui, sans-serif';
const SUB_FONT = '500 9.5px "JetBrains Mono", ui-monospace, monospace';
const MOTE_FONT = '500 9px "JetBrains Mono", ui-monospace, monospace';

const reducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

export class Galaxy {
  /**
   * @param options.onSelect  (hub, { open }) — a click, and a double click
   * @param options.onHover   (hub | null)
   * @param options.onEmpty   a click that hit nothing
   * @param options.onZoom    (zoom) — the reader turned the wheel
   * @param options.onView    (hub, view) — a click on a focused body's view ring
   * @param options.sphere    false for a model with no meaningful third
   *                          dimension — a bipartite join, say — which pins it
   *                          to the flat rings and hides the 3D/2D tray
   * @param options.camera    a scene the reader moves through rather than
   *                          watches: `setFocus` pans and zooms to a body. Off
   *                          everywhere the whole model has to stay in frame.
   * @param options.hoops     draw each hub's mass as a dashed hoop in 2D rather
   *                          than as motes
   */
  constructor(canvas, {
    onSelect, onHover, onEmpty, onZoom, onView,
    sphere = true, camera = false, hoops = false, moteGain = 1,
  } = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.onSelect = onSelect ?? (() => {});
    this.onHover = onHover ?? (() => {});
    // A click on nothing, and a change of scale — both things a caller may want
    // to keep its own chrome in step with.
    this.onEmpty = onEmpty ?? (() => {});
    this.onZoom = onZoom ?? (() => {});
    // A click on one of the view nodes round a focused body.
    this.onView = onView ?? (() => {});
    this.hoverView = null;
    this.sphere = sphere;
    this.camera = Boolean(camera);
    this.hoops = Boolean(hoops);
    // A full-viewport scene of five bodies needs more light than a 900px panel
    // of thirty: the same alpha that reads as a nebula in a panel reads as a
    // faint smudge across a whole screen.
    this.moteGain = moteGain;

    this.focusId = null;
    // Added to the automatic rotation, never replacing it, so letting go of a
    // drag leaves the scene turning from where it was put rather than snapping.
    this.spin = { yaw: 0, pitch: 0 };
    this.zoom = 1;
    this._drag = null;
    // Null until the first frame, which is what seeds it at its own target
    // rather than easing in from the top-left corner on load.
    this._cam = null;
    this._yaw = null;      // lazily seeded on the first frame, see _frame
    this._lastFrame = null;

    this.model = null;
    this.mode = sphere ? '3d' : '2d';
    this.showLabels = true;
    this.selectedId = null;
    this.hover = null;
    this.moteCount = 0;
    this.moteSampled = false;

    this._raf = null;
    this._screen = [];   // hubs projected, refreshed each frame — the hit test
    this._t0 = performance.now();

    this._bindEvents();
  }

  // ── model ───────────────────────────────────────────────────────
  /**
   * @param data.hubs   [{ id, name, weight, tier, ...anything }]
   *                    `tier` is 'core' | 'spine' | 'satellite'. It decides the
   *                    colour and, in 3D, the shell: core sits *inside*
   *                    everything else, which is the one structural claim the
   *                    layout makes on the caller's behalf. Only pass core for
   *                    something that really is at the centre of the story.
   * @param data.hubs[].views [{ id, label }] — drawn as a ring when focused
   * @param data.hubs[].ink   a KIND name, tinting the body and its cloud
   * @param data.hubs[].mix   [[kind, count], …] — how its mass divides
   * @param data.links  [{ source, target, critical, kind }] — source → target is the
   *                    direction the packet travels. Do not symmetrise it.
   * @param data.motes  { count, hot } — the mass. `count` is the real number of
   *                    things; it is clamped for drawing, and `moteSampled`
   *                    says whether that happened so a hint can be honest.
   *                    `hot` is how many of them are brighter, same units.
   * @param options.seed  fix it to keep the field identical between reloads and
   *                      between the two themes. Defaults to the design's.
   */
  setData(
    { hubs = [], links = [], motes = null } = {},
    { seed = 20260821, spread = 1, ceiling = CLUSTER_CEILING, budget = MOTE_MAX } = {}
  ) {
    let sd = seed;
    const rnd = () => (sd = (sd * 1103515245 + 12345) % 2147483648) / 2147483648;

    // ---- hubs on a Fibonacci sphere ------------------------------------
    // Evenly spread with no clumping and no seams, which is the whole reason
    // for the golden angle — a naive lat/long grid piles everything at the
    // poles and puts a visible join down one side.
    // A hub may bring its own position instead. Where the arrangement is the
    // claim — this layer is between those two, that one is nearest the reader
    // — an even spread would erase exactly what the picture is for.
    // Each shell gets the whole sweep to itself. Sharing one sweep across every
    // hub does not produce concentric spheres — it produces one sphere cut into
    // latitude bands, with the inner shell bunched round a pole. See the note
    // at the top of this patch's history: it is why two shared contracts always
    // sat above the middle rather than at the centre of the Schemas scope.
    const shellOf = (hub) => hub.shell ?? (hub.tier === 'core' ? CORE_SHELL : 1);
    const bySeat = new Map();
    hubs.forEach((hub, i) => {
      const s = shellOf(hub);
      if (!bySeat.has(s)) bySeat.set(s, []);
      bySeat.get(s).push(i);
    });
    const seat = new Array(hubs.length);
    for (const list of bySeat.values()) {
      list.forEach((index, k) => { seat[index] = [k, list.length]; });
    }

    const placed = hubs.map((hub, i) => {
      const shell = shellOf(hub);
      const [k, count] = seat[i];
      const n = Math.max(1, count - 1);
      const y = 1 - ((k + 0.5) / n) * 2;
      const rad = Math.sqrt(Math.max(0, 1 - y * y));
      const th = GOLD * (k + 0.5);
      const at = hub.pos ?? null;
      return {
        ...hub,
        x: at ? at[0] : Math.cos(th) * rad * shell,
        y: at ? at[1] : y * shell,
        z: at ? at[2] : Math.sin(th) * rad * shell,
        // Compressed, and the exponent is the point. Sized linearly, a contract
        // with 89 operations is eleven times the area of one with 25 — which
        // reads as an importance nobody claimed.
        r: Math.min(HUB_R_MAX, 1.5 + Math.pow(Math.max(1, hub.weight ?? 1), 0.55) * 0.3),
      };
    });

    // ---- the same hubs on flat rings, for 2D ---------------------------
    // Counted from the data rather than fixed: the design hard-codes 8 spine /
    // 14 satellite / 2 core, and a package that grows a contract would space
    // its ring wrong for ever after.
    // Spaced by the ring they land on, not by their tier. Two tiers sharing a
    // ring — which is the normal case on a bipartite join, where colour and
    // side are different questions — would otherwise each be spread evenly
    // round the whole circle and sit on top of each other.
    const ringOf = (hub) => hub.ring ?? RINGS[hub.tier] ?? RINGS.spine;
    const per = {};
    for (const hub of placed) {
      if (hub.flat) continue;   // not on a ring, so not competing for its arc
      per[ringOf(hub)] = (per[ringOf(hub)] ?? 0) + 1;
    }
    const seen = {};
    for (const hub of placed) {
      // Same argument as `pos`, for the layout with no depth to fall back on.
      if (hub.flat) { hub.slot = 0; [hub.fx, hub.fy] = hub.flat; continue; }
      const tier = hub.tier ?? 'spine';
      const key = ringOf(hub);
      const i = (seen[key] = (seen[key] ?? 0) + 1) - 1;
      // Its place in the going-round order, so that thinning a crowded ring
      // takes every second or third one rather than an arbitrary subset.
      hub.slot = i;
      const a = (i / Math.max(1, per[key])) * Math.PI * 2
        - Math.PI / 2 + (RING_OFFSET[tier] ?? 0);
      const ring = hub.ring ?? RINGS[tier] ?? RINGS.spine;
      hub.fx = Math.cos(a) * ring;
      hub.fy = Math.sin(a) * ring;
    }

    const byId = new Map(placed.map((h) => [h.id, h]));
    const edges = [];
    for (const link of links) {
      const a = byId.get(link.source);
      const b = byId.get(link.target);
      if (!a || !b || a === b) continue;
      edges.push({ ...link, a, b });
    }

    // ---- the mass ------------------------------------------------------
    // Two kinds, and which one a caller wants is decided by whether the mass
    // belongs to anything. The contracts' components belong to a contract, so
    // they cluster round it and the cluster says how much that contract holds.
    // A field that belongs to the model as a whole — no hub owns it — is spread
    // over the sphere instead, which is the design's own arrangement.
    const clustered = placed.some((hub) => (hub.mass ?? 0) > 0);
    const dust = [];
    const web = [];

    if (clustered) {
      const share = (m) => Math.pow(Math.max(0, m), 0.62);
      const total = placed.reduce((a, h) => a + share(h.mass ?? 0), 0) || 1;

      // The ceiling on a cluster, per hub, from how much room that hub has.
      //
      // On a ring it is the arc between neighbours — 2πr/n. On the sphere there
      // is no single answer, so the usual approximation for n points spread
      // evenly over a unit sphere does: each occupies about 4π/n of surface, so
      // they sit roughly 2/√n apart. Both are then halved, because a radius
      // reaching the whole way to a neighbour is two clusters touching.
      const onRing = {};
      const onShell = {};
      for (const hub of placed) {
        const r = hub.ring ?? RINGS[hub.tier] ?? RINGS.spine;
        onRing[r] = (onRing[r] ?? 0) + 1;
        const sh = shellOf(hub);
        onShell[sh] = (onShell[sh] ?? 0) + 1;
      }
      // A hub that was placed by hand has no ring and no even spread to reason
      // from, so the room it has is the distance to whatever is actually
      // nearest it — which is the thing both approximations were estimating.
      const nearestGap = (hub) => {
        let best = Infinity;
        for (const other of placed) {
          if (other === hub) continue;
          best = Math.min(best, Math.hypot(
            other.x - hub.x, other.y - hub.y, other.z - hub.z
          ));
        }
        return Number.isFinite(best) ? best * CLUSTER_CROWD : Infinity;
      };
      const roomFor = (hub) => {
        if (hub.pos || hub.flat) return nearestGap(hub);
        // Per shell, not across the model. Counting all of them together told a
        // 31-service inner shell it had the elbow room of a 121-hub sphere and
        // shrank every halo to a quarter of what actually fits.
        const sh = shellOf(hub);
        const sphereGap =
          ((2 * sh) / Math.sqrt(Math.max(1, onShell[sh]))) * CLUSTER_CROWD;
        const r = hub.ring ?? RINGS[hub.tier] ?? RINGS.spine;
        const ringGap = ((2 * Math.PI * r) / Math.max(1, onRing[r])) * CLUSTER_CROWD;
        // Whichever layout is in use, the cluster has to fit in both — the same
        // model is drawn as a sphere and as rings, and rebuilding it on a mode
        // switch would restart the field from a different random draw.
        return Math.min(sphereGap, ringGap);
      };
      let realTotal = 0;

      for (const hub of placed) {
        const mass = hub.mass ?? 0;
        realTotal += mass;
        if (mass <= 0) continue;

        const n = Math.max(
          CLUSTER_FLOOR,
          Math.min(ceiling, Math.round((budget * share(mass)) / total))
        );
        // `spread` scales the formula, not the room: the geometry is a fact
        // about the layout and does not care what scale the caller wanted.
        const cr = Math.min(
          CLUSTER_MAX_R * spread,
          roomFor(hub),
          (CLUSTER_MIN_R + Math.log(1 + mass) * CLUSTER_SCALE) * spread
        );
        hub.cr = cr;
        const hotShare = mass ? Math.min(1, (hub.hot ?? 0) / mass) : 0;
        const first = dust.length;

        for (let i = 0; i < n; i++) {
          const u = rnd() * 2 - 1;
          const th = rnd() * Math.PI * 2;
          const rad = Math.sqrt(Math.max(0, 1 - u * u));
          // Shell-biased, same as the whole-sphere field: a defined edge, and
          // enough inside that the cluster is a body rather than a soap bubble.
          const rr = (rnd() > 0.22 ? 0.88 + (rnd() - 0.5) * 0.2 : 0.25 + rnd() * 0.55) * cr;
          dust.push({
            x: hub.x + Math.cos(th) * rad * rr,
            y: hub.y + u * rr,
            z: hub.z + Math.sin(th) * rad * rr,
            fx: hub.fx + Math.cos(th) * rad * rr,
            fy: hub.fy + u * rr,
            r: 0.3 + rnd() * 0.7,
            tw: rnd() * 6.283,
            hot: rnd() < hotShare,
            tier: hub.tier,
            // A body with its own ink hands it to everything inside it, so a
            // cluster is one colour through rather than a tinted rim round a
            // teal middle.
            ink: hub.ink ?? null,
            owner: hub.id,
            // A real thing from the layer, where the caller supplied a list.
            // Only the first `items.length` motes get one; the rest stay the
            // anonymous filler that makes the cloud the right size.
            name: hub.items?.[i] ?? null,
          });
        }
        // Filaments inside the cluster only. A thread between two clusters
        // would look like a relationship and there is none — the lanes are the
        // relationships. Cheap too: O(n²) per cluster rather than over all of
        // them at once.
        linkNearest(dust, first, dust.length, (cr * 0.62) ** 2, web);
      }

      this.moteCount = realTotal;
      this.moteSampled = dust.length < realTotal;
    } else {
      const real = Math.max(0, motes?.count ?? 0);
      const drawn = real ? Math.min(budget, Math.max(MOTE_MIN, real)) : 0;
      this.moteCount = real;
      this.moteSampled = real > MOTE_MAX;
      const hotShare = real ? Math.min(1, (motes?.hot ?? 0) / real) : 0.1;
      for (let i = 0; i < drawn; i++) {
        const u = rnd() * 2 - 1;
        const th = rnd() * Math.PI * 2;
        const rad = Math.sqrt(Math.max(0, 1 - u * u));
        // 78% on the shell — that is what gives the silhouette a defined edge —
        // and 22% inside, which is what stops the middle reading as an empty
        // balloon.
        const shell = rnd() > 0.22;
        const rr = shell ? 0.9 + (rnd() - 0.5) * 0.15 : 0.3 + rnd() * 0.52;
        dust.push({
          x: Math.cos(th) * rad * rr,
          y: u * rr,
          z: Math.sin(th) * rad * rr,
          r: 0.35 + rnd() * 0.95,
          tw: rnd() * 6.283,
          hot: rnd() < hotShare,
        });
      }

      // The threshold is a distance, and the right distance depends on how far
      // apart the motes are — a function of how many there are. Fixed at the
      // design's 0.011 it catches about three neighbours at 900 and barely one
      // at 380, so a smaller layer loses the web that is its texture. Motes sit
      // on a shell, so spacing goes as 1/√n and the squared threshold as 1/n.
      linkNearest(dust, 0, dust.length,
        FILAMENT_D2 * Math.min(4, MOTE_MAX / Math.max(1, dust.length)), web);
    }

    this.clustered = clustered;

    // which hubs each hub is joined to, for the hover isolate
    const neighbours = new Map(placed.map((h) => [h.id, new Set()]));
    for (const edge of edges) {
      neighbours.get(edge.a.id)?.add(edge.b.id);
      neighbours.get(edge.b.id)?.add(edge.a.id);
    }

    this.model = { hubs: placed, links: edges, dust, web, neighbours };
    this.start();
  }

  setMode(mode) {
    this.mode = this.sphere ? mode : '2d';
    // Coming back to 3D has to restart a loop that 2D parked.
    this.stop();
    this.start();
    this.draw();
  }

  /**
   * Whether this frame is the only frame.
   *
   * 2D holds still — no dashes, no packets, no pulse, no twinkle — so drawing
   * it sixty times a second paints the same pixels sixty times. A camera scene
   * is the exception even flat, because the pan and zoom are still easing and
   * that easing is the feedback for a click.
   */
  _still() {
    // A flight is the exception: it is eighteen frames long, it advances its
    // own clock inside draw(), and a scene that parks after the first of them
    // freezes the picture halfway through the transition.
    if (this._warp) return false;
    return (this.mode === '2d' && !this.camera) || reducedMotion();
  }

  /**
   * Whether this model has a meaningful third dimension.
   *
   * A join between two sets does not: putting services and tables on a sphere
   * would say the arrangement means something, and it would not. Those get the
   * rings, and the 3D/2D tray is not offered.
   */
  setSphere(on) {
    this.sphere = Boolean(on);
    if (!this.sphere) this.mode = '2d';
    this.draw();
  }

  /**
   * Back to the rotation and scale the view opened with.
   *
   * Not a reset of the selection or the focus — only of what the hand has done,
   * which is the thing a reader can get lost in.
   */
  resetView() {
    this.spin = { yaw: 0, pitch: 0 };
    this.zoom = 1;
    this._flight = 0;
    this.start();
    this.draw();
  }

  /** Whether the reader has moved the camera off its default. */
  moved() {
    return this.zoom !== 1 || this.spin.yaw !== 0 || this.spin.pitch !== 0;
  }

  setSelected(id) {
    this.selectedId = id;
    this.draw();
  }

  /**
   * The body the camera is on, or null for the whole scene.
   *
   * Sticky where hover is momentary, and they share one mechanism downstream:
   * whichever is set decides what is bright and what drops back. Focus wins,
   * because a reader who has chosen a layer and then moves the pointer across
   * the scene has not changed their mind.
   */
  setFocus(id) {
    // Back to zero so the ring grows again on the next focus rather than
    // appearing fully formed on a body that has only just been chosen.
    if (id !== this.focusId) this._viewRise = 0;
    const next = id ?? null;
    if (next === this.focusId) return;
    this.focusId = next;
    // From the top: this is the only thing that moves the camera's target, and
    // a flight that carried on from halfway would arrive in half the time.
    this._flight = 0;
    // The camera eases, so the loop has to be running for the move to happen
    // at all — including under reduced motion, where it is the only motion.
    this.start();
    this.draw();
  }

  /** The focused hub, or null. */
  focused() {
    return this.model?.hubs.find((h) => h.id === this.focusId) ?? null;
  }

  // ── the loop ────────────────────────────────────────────────────
  /**
   * Idempotent, and it parks itself.
   *
   * A hidden view measures 0×0, so a loop left running behind a switched-away
   * tab would burn a frame budget painting nothing. It stops instead, and the
   * caller starts it again on the way back in.
   *
   * The test is `getClientRects` and not `offsetParent`, which was the first
   * thing tried and is wrong twice over: it is null for a `position: fixed`
   * element that is perfectly visible — so a full-page scene parks itself on
   * its first frame and the page arrives dead — and it is null for a
   * `display: none` one, which is the case it was meant to catch. An element
   * that is not rendered has no client rects, whatever its position is.
   */
  start() {
    if (this._raf || !this.model) return;
    // Reduced motion paints one held frame — unless there is a camera, where
    // the easing is the feedback for a click and dropping it would leave a
    // selection with no visible result. The rotation and the packets still stop.
    // A still view is painted once and then has no loop to catch up with. That
    // matters because a caller may unhide the canvas in the same tick it asks
    // for a frame, and a canvas that measures 0x0 draws nothing at all — which
    // used to be harmless, since the loop would come round again a moment later
    // and find it. So the one frame waits for something to measure, and gives
    // up after a couple of seconds rather than spinning on a view that is not
    // coming back.
    if (this._still()) {
      let tries = 0;
      const once = () => {
        this._raf = null;
        const box = this.canvas.getBoundingClientRect();
        if (box.width && box.height) { this.draw(); return; }
        if (++tries > 120) return;
        this._raf = requestAnimationFrame(once);
      };
      once();
      return;
    }
    const tick = () => {
      if (!this.canvas.isConnected || this.canvas.getClientRects().length === 0) {
        this._raf = null;   // parked; start() again when the view comes back
        return;
      }
      this.draw();
      // A flight can start a loop on a scene that is meant to hold still — 2D,
      // or reduced motion. When it lands, the loop has to hand the scene back
      // the way it found it, or a 2D view quietly starts animating because
      // somebody once double-clicked something in it.
      if (this._still()) { this._raf = null; return; }
      this._raf = requestAnimationFrame(tick);
    };
    this._raf = requestAnimationFrame(tick);
  }

  stop() {
    if (this._raf) cancelAnimationFrame(this._raf);
    this._raf = null;
  }

  destroy() {
    this.stop();
    this.model = null;
  }

  // ── projection ──────────────────────────────────────────────────
  _frame() {
    const box = this.canvas.getBoundingClientRect();
    const W = box.width;
    const H = box.height;
    const t = reducedMotion() ? STILL_T : (performance.now() - this._t0) / 1000;
    const flat = this.mode === '2d';

    // Accumulated rather than `t × rate`, because the rate changes when a body
    // is focused and a rate change applied to elapsed time teleports the scene
    // backwards by however long it has been running.
    const now = performance.now();
    const dt = this._lastFrame == null
      ? 0
      : Math.min(0.1, (now - this._lastFrame) / 1000);   // capped: a backgrounded
    this._lastFrame = now;                               // tab must not lurch
    const still = reducedMotion();
    const rate = this.camera ? (this.focusId ? CAM_YAW_FOCUS : CAM_YAW) : YAW_RATE;
    // Seeded rather than started at zero: STILL_T is the pose the design chose
    // for a held frame, and it is as good a first frame as any.
    if (this._yaw == null) this._yaw = STILL_T * rate;
    // Not while the reader is holding it. A scene that keeps turning under a
    // pointer trying to aim at it is fighting them.
    if (!still && !this._drag?.active) this._yaw += dt * rate;

    const yaw = this._yaw + this.spin.yaw;
    const nod = this.camera
      ? CAM_PITCH_BASE + Math.sin(t * CAM_PITCH_RATE) * CAM_PITCH_SWING
      : PITCH_BASE + Math.sin(t * PITCH_RATE) * PITCH_SWING;
    const pitch = Math.max(-PITCH_LIMIT, Math.min(PITCH_LIMIT, nod + this.spin.pitch));

    let R = Math.min(W * 0.30, H * 0.37) * this.zoom;
    let FR = Math.min(W * 0.34, H * 0.36) * this.zoom;
    let cx = W / 2;
    // Lifted above centre: the legend strip owns the foot of the panel.
    let cy = H * 0.43;

    const cyw = Math.cos(yaw), syw = Math.sin(yaw);
    const cp = Math.cos(pitch), sp = Math.sin(pitch);

    // ---- the camera ----------------------------------------------------
    // Screen space, not world space. Moving the world would drag the mote
    // clouds through each other and change what is in front of what; moving
    // the frame changes only where the picture is and how big, which is what
    // "go to that one" means.
    if (this.camera) {
      // The reader's zoom goes into the unit rather than onto R alone, so the
      // anchor maths downstream stays in the same space and a focused body does
      // not slide off centre as the scale changes.
      const UNIT = Math.min(W * CAM_UNIT_W, H * CAM_UNIT_H) * this.zoom;
      const hub = this.focused();
      const at = hub ? CAM_AT_FOCUS : CAM_AT;
      const zoom = hub ? (flat ? CAM_ZOOM_FLAT : CAM_ZOOM) : 1;

      // Where the anchor lands under the current rotation, in world units —
      // recomputed every frame, so a focused body stays put while the scene
      // keeps turning underneath it.
      let ax = 0;
      let ay = 0;
      if (hub) {
        if (flat) {
          ax = hub.fx;
          ay = hub.fy;
        } else {
          const x1 = hub.x * cyw + hub.z * syw;
          const z1 = -hub.x * syw + hub.z * cyw;
          ax = x1;
          ay = hub.y * cp - z1 * sp;
        }
      }

      const want = {
        x: W * at.x - ax * UNIT * zoom,
        y: H * at.y - ay * UNIT * zoom,
        z: zoom,
      };
      // Seeded at the target, so the first frame is the scene and not a pan in
      // from wherever zero happens to be.
      if (!this._cam) this._cam = { ...want };

      // How much of what is left the curve says to close this frame. Expressed
      // as a fraction of the remainder rather than as an absolute position, so
      // the target may keep moving — and it does: the scene turns underneath,
      // and a second click part-way through simply retargets.
      // Seeded at the far end before anything reads it: at rest the camera has
      // already arrived, and a flight only means something once a focus has
      // asked for one.
      if (this._flight == null) this._flight = CAM_FLIGHT_ZOOM;
      const closes = (span) => {
        if (!(span > 0)) return 1;
        const was = smoothstep(Math.min(1, this._flight / span));
        const now = smoothstep(Math.min(1, (this._flight + dt) / span));
        return was >= 1 ? 1 : (now - was) / (1 - was);
      };
      const kPan = closes(CAM_FLIGHT);
      const kZoom = closes(CAM_FLIGHT_ZOOM);
      this._flight = Math.min(CAM_FLIGHT_ZOOM, this._flight + dt);

      this._cam.x += (want.x - this._cam.x) * kPan;
      this._cam.y += (want.y - this._cam.y) * kPan;
      this._cam.z += (want.z - this._cam.z) * kZoom;

      cx = this._cam.x;
      cy = this._cam.y;
      R = UNIT * this._cam.z;
      FR = R;
    }

    // Negative z is towards the viewer throughout; every depth expression
    // downstream reads −z as "near".
    const project = (p) => {
      const x1 = p.x * cyw + p.z * syw;
      const z1 = -p.x * syw + p.z * cyw;
      const y2 = p.y * cp - z1 * sp;
      const z2 = p.y * sp + z1 * cp;
      // k is reused as the size multiplier for every primitive at that point,
      // which is what makes the front of the sphere read as nearer rather than
      // merely brighter.
      const k = FOV / (FOV + z2 * (this.camera ? CAM_DEPTH : 1.35));
      return { sx: cx + x1 * R * k, sy: cy + y2 * R * k, k, z: z2 };
    };
    // In 2D every depth expression evaluates flat and unchanged, which is why
    // this is fifteen lines rather than a second renderer.
    const flatten = (h) => ({ sx: cx + h.fx * FR, sy: cy + h.fy * FR, k: 1, z: 0 });

    // One number, derived from the panel, that every absolute radius below is
    // multiplied by. Clamped at both ends: a short panel should not shrink the
    // hubs into nothing, and a very tall one should not inflate them into discs.
    const unit = Math.max(UNIT_MIN, Math.min(UNIT_MAX, R / REFERENCE_R));

    return { W, H, t, flat, cx, cy, R, FR, unit, project, flatten };
  }

  /**
   * The scratch canvas the day nebula is accumulated on, sized to the target.
   *
   * Kept on the instance rather than made per frame: allocating a
   * viewport-sized bitmap sixty times a second is its own stall, and this one
   * is fully cleared at the top of every frame so nothing carries over.
   */
  _inkBuffer(w, h) {
    let cv = this._ink;
    if (!cv) { cv = this._ink = document.createElement('canvas'); }
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
    return cv.getContext('2d');
  }

  /**
   * Fly into `hub` and let `swap` put a different model on screen behind the
   * flash. A no-op if the hub is not on the current frame, which is the right
   * failure: an animation nobody can anchor is worse than none.
   *
   * @param hubId  what was opened — the point everything scales about
   * @param swap   called once, at the midpoint, with the canvas empty
   */
  warpInto(hubId, swap) {
    const at = (this._screen ?? []).find((e) => e.hub.id === hubId);
    if (!at || this._warp) { swap(); return; }
    // Reduced motion asks for no journey, not for no destination.
    if (reducedMotion()) { swap(); return; }
    this._warp = { x: at.sx, y: at.sy, t: 0, swap };
    // A flat scene has already parked its loop after one frame. Cancel that
    // pending frame first, or `start` sees a live _raf and returns.
    if (this._raf) { cancelAnimationFrame(this._raf); this._raf = null; }
    this.start();
  }

  /**
   * The transform for the frame, or null. Advances the clock as a side effect,
   * which is why it is called exactly once per draw.
   */
  _warpFrame() {
    const w = this._warp;
    if (!w) return null;
    const was = w.t;
    w.t = Math.min(1, w.t + WARP_STEP);
    // At the midpoint the canvas is empty and the model changes underneath it.
    if (was < 0.5 && w.t >= 0.5) w.swap();
    if (w.t >= 1) { this._warp = null; return null; }

    // Out then in, each half eased so the two meet at a stop rather than at
    // full speed — a linear pair reads as one continuous rush past the reader.
    const half = w.t < 0.5 ? w.t * 2 : (w.t - 0.5) * 2;
    const ease = half * half * (3 - 2 * half);
    return w.t < 0.5
      ? { x: w.x, y: w.y, scale: 1 + (WARP_OUT - 1) * ease, alpha: 1 - ease }
      : { x: w.x, y: w.y, scale: WARP_IN + (1 - WARP_IN) * ease, alpha: ease };
  }

  // ── drawing ─────────────────────────────────────────────────────
  /**
   * Turn the scene by one keyboard step, the way a drag of the same sign turns
   * it.
   *
   * `dx` and `dy` are in the drag's own units — pixels of pointer travel — so
   * the two paths cannot drift: DRAG_YAW and DRAG_PITCH move both at once, and
   * the negation on yaw stays written down in exactly one place, above.
   *
   * The scene had no keyboard route at all: a reader could open a galaxy and
   * then only look at it, because turning and zooming were both pointer-only.
   */
  nudge(dx, dy) {
    this.spin.yaw -= dx * DRAG_YAW;
    this.spin.pitch += dy * DRAG_PITCH;
    this.start();
    // A parked loop — 2D, or reduced motion — draws no frames of its own, so
    // the scene would not move at all without this. Same reason as the drag.
    if (this._still()) this.draw();
  }

  /** Zoom by a factor, against the same stops the wheel is held to. */
  zoomBy(factor) {
    this.zoom = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, this.zoom * factor));
    this.onZoom(this.zoom);
    this.start();
    if (this._still()) this.draw();
  }

  draw() {
    const model = this.model;
    if (!model) return;
    const cv = this.canvas;
    const box = cv.getBoundingClientRect();
    if (!box.width || !box.height) return;   // hidden — nothing to measure against

    // devicePixelRatio capped at 2: at 3 the mote count starts costing real
    // milliseconds for no visible gain.
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const want = [Math.round(box.width * dpr), Math.round(box.height * dpr)];
    if (cv.width !== want[0] || cv.height !== want[1]) {
      cv.width = want[0];
      cv.height = want[1];
    }

    const g = this.ctx;
    const { W, H, t, flat, cx, cy, R, FR, unit, project, flatten } = this._frame();
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, W, H);

    // Mid-flight into a body. Applied to the whole frame, including the labels,
    // because a caption that stays put while its picture flies away is the one
    // thing that would give the trick away.
    const warp = this._warpFrame();
    if (warp) {
      g.translate(warp.x, warp.y);
      g.scale(warp.scale, warp.scale);
      g.translate(-warp.x, -warp.y);
      g.globalAlpha = warp.alpha;
    }

    // The ground for this frame, and the ink that belongs to it. Read here
    // rather than cached, so the day/night toggle lands on the very next frame
    // without anything having to tell the galaxy about it.
    const night = isNight();
    INK = night ? INK_DARK : INK_LIGHT;
    KIND = night ? KIND_DARK : KIND_LIGHT;
    STYLE = night ? STYLE_DARK : STYLE_LIGHT;

    // Everything but the labels is composited with depth-scaled alpha, so
    // overlap accumulates instead of needing a z-sort. That is the whole reason
    // this reads as a nebula rather than as a scatter plot — and it is the
    // accumulation that matters, not the direction. At night light adds; by day
    // ink subtracts it. Same picture, opposite ground.
    //
    // Both directions are drawn with `lighter`, and by day the result is turned
    // around once at the end rather than per call. `multiply` costs about 2.8x
    // `lighter` per draw here (24.7ms vs 9.0ms a frame, measured), and the
    // scene issues thousands of them — which made day run at a third of night's
    // frame rate for an identical picture.
    //
    // It is the same arithmetic. `lighter` sums premultiplied colour *and*
    // alpha, so a stack of draws leaves the weighted-average colour under the
    // summed coverage; laying that over white with source-over gives
    // 255 − Σαᵢ(255 − cᵢ), which is subtractive ink. The one place it parts
    // company with a true multiply is where coverage passes 1 and clamps: a
    // very dense core settles at its average tint instead of continuing down
    // toward black. That ceiling is worth 3x the frame rate.
    const buffered = !night;
    let ink = g;
    if (buffered) {
      ink = this._inkBuffer(cv.width, cv.height);
      ink.setTransform(1, 0, 0, 1, 0, 0);
      ink.clearRect(0, 0, cv.width, cv.height);
      ink.setTransform(dpr, 0, 0, dpr, 0, 0);
      // The flight is applied to the buffer instead of to the canvas, or it
      // would land twice — once on the ink and again on the composite.
      if (warp) {
        ink.translate(warp.x, warp.y);
        ink.scale(warp.scale, warp.scale);
        ink.translate(-warp.x, -warp.y);
        ink.globalAlpha = warp.alpha;
      }
    }
    ink.globalCompositeOperation = 'lighter';

    // Focus is sticky and hover is momentary, so focus wins: a reader who has
    // chosen a layer and then swept the pointer over the scene has not chosen
    // a different one. With a focus the neighbours drop back too — the claim
    // is "this one", not "this one and what it touches".
    const focus = this.focusId ?? this.hover?.id ?? null;
    const near = this.focusId ? null : (focus ? model.neighbours.get(focus) : null);
    const lit = (id) => !focus || id === focus || near?.has(id);

    if (flat) this._drawGuides(ink, cx, cy, FR, model);
    // A cluster belongs to a hub, so it is drawn wherever that hub is — the
    // ring layout included, where it reads as a halo of what the hub owns. A
    // field that belongs to the whole model is a sphere effect and has nothing
    // to say once the projection is off.
    // The hoop is a boundary, not a substitute. It was drawn instead of the
    // cloud, which left the flat landing page as five dotted circles with a dot
    // in each — a diagram of nothing, next to four other views that all show
    // their mass. Both now: the outline says how big, the motes say of what.
    if (flat && this.hoops) this._drawHoops(ink, model, lit, FR, cx, cy);
    if (!flat || this.clustered) {
      this._drawMass(ink, model, flat ? flatten : project, t, unit, flat, FR, cx, cy, lit);
    }
    const hp = model.hubs.map((h) => (flat ? flatten(h) : project(h)));
    this._drawLinks(ink, model, hp, t, lit, unit, flat);
    this._drawHubs(ink, model, hp, t, flat, lit, unit);

    // The one blend of the frame. save/restore because the labels below still
    // want the flight transform and its alpha, and the composite must run at
    // device scale with neither.
    if (buffered) {
      g.save();
      g.setTransform(1, 0, 0, 1, 0, 0);
      g.globalAlpha = 1;
      g.globalCompositeOperation = 'source-over';
      g.drawImage(ink.canvas, 0, 0);
      g.restore();
    }

    g.globalCompositeOperation = 'source-over';
    if (this._pendingMoteLabels) {
      this._drawMoteLabels(g, model, this._pendingMoteLabels);
      this._pendingMoteLabels = null;
    }
    this._drawLabels(g, model, hp, lit, unit, { x: cx, y: cy }, flat ? FR : R);
    // After the labels, and after the additive blending is off: these are
    // chrome that belongs to the scene, not part of the nebula.
    this._views = this._drawViews(g, model, unit);

    // Left as it was found. The alpha is the only piece of context that does
    // not reset with setTransform on the next frame.
    if (warp) g.globalAlpha = 1;

    // The hit test rides on the frame that drew it, so a click always resolves
    // against the positions the reader can actually see. Mid-flight it holds
    // the positions from before the swap, which is correct: those are the ones
    // that were on screen when the pointer went down.
    this._screen = model.hubs.map((hub, i) => ({
      hub,
      sx: hp[i].sx,
      sy: hp[i].sy,
      // What the reader is pointing at is the body, and on a clustered scene
      // the body is the cloud. Two thirds of it, so two adjacent clouds do not
      // both claim the space between them.
      r: Math.max(
        hub.r * hp[i].k * unit * (flat ? 1.5 : 1),
        hub.cr ? hub.cr * (flat ? FR : R) * hp[i].k * 0.66 : 0
      ),
    }));
  }

  /**
   * The views of the focused body, marked on motes it already has.
   *
   * Returns the hit list, so the same frame that drew them answers a click on
   * one. Empty whenever nothing is focused, the focused body declares no views,
   * or its cloud has not been projected this frame.
   */
  _drawViews(g, model, unit) {
    const hub = model.hubs.find((h) => h.id === this.focusId);
    const views = hub?.views ?? [];
    const dp = this._dustScreen;
    if (!views.length || !dp) return [];

    // Nearest first. These are the motes whose position is least ambiguous and
    // the ones a reader is looking at, which is where a door should be.
    const pool = [];
    for (let i = 0; i < model.dust.length; i++) {
      if (model.dust[i].owner !== hub.id) continue;
      const p = dp[i];
      if (!p) continue;
      pool.push([p.z, p]);
    }
    if (pool.length < views.length) return [];
    pool.sort((a, b) => a[0] - b[0]);

    // Held apart, or two names land on top of each other and the body ends up
    // with four doors in one corner of itself.
    const picked = [];
    for (const [, p] of pool.slice(0, VIEW_POOL)) {
      if (picked.every((q) => Math.hypot(q.sx - p.sx, q.sy - p.sy) > VIEW_GAP)) picked.push(p);
      if (picked.length === views.length) break;
    }
    // A tight cloud may not have room for all of them at that spacing; rather
    // than crowd, take what fits from the front and let the rest go.
    if (!picked.length) return [];

    // Eased in on the focus rather than snapped, so a body still travelling to
    // the middle does not arrive already marked up.
    this._viewRise = Math.min(1, (this._viewRise ?? 0) + 0.07);
    const rise = this._viewRise;
    const ink = tintOf(hub.ink ?? hub.tier);

    const out = [];
    picked.forEach((p, i) => {
      const view = views[i];
      const hot = this.hoverView === view.id;
      const r = (VIEW_DOT + (hot ? 2.5 : 0)) * unit;

      // A ring round a mote that is already drawn. That is the whole mark: the
      // dot underneath belongs to the scene, and this says it is also a way in.
      // At full strength rather than half: a thin ring at 50% on a cloud of
      // three hundred lit motes is not a mark, and these are the way in.
      g.strokeStyle = `rgba(${ink.core},${((hot ? 1 : 0.8) * rise).toFixed(3)})`;
      g.lineWidth = hot ? 1.8 : 1.4;
      g.beginPath();
      g.arc(p.sx, p.sy, r + 4.5 * unit, 0, 6.284);
      g.stroke();

      // Named on hover always, and once zoomed in the same way the mass is.
      if (hot || this.zoom >= SUB_ZOOM) {
        g.font = SUB_FONT;
        g.textAlign = 'center';
        g.textBaseline = 'middle';
        g.fillStyle = `rgba(${INK.label},${((hot ? 1 : 0.7) * rise).toFixed(2)})`;
        g.fillText(view.label, p.sx, p.sy - r - 9 * unit);
        g.textBaseline = 'alphabetic';
      }
      out.push({ view, hub, sx: p.sx, sy: p.sy });
    });
    return out;
  }

  /** The view node under a point, or null. */
  viewAt(sx, sy) {
    for (const entry of this._views ?? []) {
      if (Math.hypot(entry.sx - sx, entry.sy - sy) < VIEW_HIT) return entry;
    }
    return null;
  }

  /** The two rings, drawn as guides rather than left implicit. */
  _drawGuides(g, cx, cy, FR, model) {
    // Only where the rings are the layout. A scene placed by hand has none, and
    // falling back to the tier radii drew three dashed circles describing
    // nothing — guides to a structure that is not there.
    if (model.hubs.some((h) => h.flat)) return;
    const radii = new Set(
      model.hubs.map((h) => h.ring ?? RINGS[h.tier] ?? RINGS.spine)
    );
    g.strokeStyle = INK.guide;
    g.lineWidth = 1;
    g.setLineDash([1.5, 7]);
    for (const r of radii) {
      g.beginPath();
      g.arc(cx, cy, FR * r, 0, 6.284);
      g.stroke();
    }
    g.setLineDash([]);
  }

  _drawMass(g, model, project, t, unit, flat, FR, cx, cy, lit = null) {
    const dp = flat
      ? model.dust.map((d) => ({ sx: cx + d.fx * FR, sy: cy + d.fy * FR, k: 1, z: 0 }))
      : model.dust.map(project);

    // The web is texture and says nothing on its own — see the note where it is
    // built. In 3D it is what makes a cluster read as a body rather than a
    // scatter; flattened it is a thicket of hairlines over a picture that is
    // meant to be read at a glance, so it does not come along.
    for (const [i, j] of (flat ? [] : model.web)) {
      const a = dp[i];
      const b = dp[j];
      if (!a || !b) continue;
      const depth = (a.z + b.z) / 2;
      const web = (0.15 - depth * 0.08) * this.moteGain * STYLE.web
        * (!lit || !model.dust[i].owner || lit(model.dust[i].owner)
            ? 1 : Math.min(1, DIM_WEB * STYLE.dim));
      const owner = model.dust[i];
      g.strokeStyle = `rgba(${owner.ink ? tintOf(owner.ink).body : INK.filament},`
        + `${web.toFixed(3)})`;
      g.lineWidth = 0.5;
      g.beginPath();
      g.moveTo(a.sx, a.sy);
      g.lineTo(b.sx, b.sy);
      g.stroke();
    }

    // Handed to the label pass, which runs after the additive blending is
    // switched off — type drawn with 'lighter' comes out as a glow.
    this._pendingMoteLabels = this.zoom >= SUB_ZOOM ? dp : null;
    // And kept for the view pass, which marks motes that are already here
    // rather than adding any of its own. Unconditional: the marks are drawn
    // whether or not anything is being named.
    this._dustScreen = dp;
    model.dust.forEach((d, i) => {
      const p = dp[i];
      // Held at the twinkle's own mean, so a flat cluster is neither brighter
      // nor dimmer than the 3D one it is the same model as.
      const twinkle = flat ? 0.62 : 0.55 + Math.sin(t * 1.4 + d.tw) * 0.3;
      // A cluster follows its hub back: dimming the body and leaving its cloud
      // at full brightness would make the unfocused layers *more* prominent.
      const on = !lit || !d.owner || lit(d.owner);
      const mine = flat && d.owner && d.owner === this.hover?.id;
      // Once a reader is inside a body — focused on it, or zoomed in far enough
      // to be reading names — its contents stop being mass and start being
      // things. A promoted mote is drawn larger and brighter, with a hard core
      // on top, so it reads as a node rather than as a speck of a quantity.
      // Two steps rather than one. A camera scene is a place the reader is
      // inside rather than a panel they are looking at, so its mass reads as
      // things from the first frame; focusing a body or zooming into it
      // promotes further, and only the second step brings names.
      const near = d.owner && (d.owner === this.focusId || this.zoom >= SUB_ZOOM);
      const promoted = !flat && Boolean(d.owner) && (near || this.camera);
      const close = !flat && Boolean(near);
      const a = Math.max(STYLE.floorMote, 0.5 - p.z * 0.3 * STYLE.zK)
        * twinkle * (d.hot ? 2 : 1) * (on ? 1 : Math.min(1, DIM_MASS * STYLE.dim))
        * (flat ? (mine ? MOTE_FLAT_HOT : MOTE_FLAT) : 1) * this.moteGain
        * (close ? 1.45 : promoted ? 1.15 : 1) * STYLE.mote;
      // Floored so the back of the sphere stays a field rather than dropping out.
      const rad = Math.max(0.4, d.r * p.k * unit) * (close ? 2.4 : promoted ? 1.6 : 1);
      // Ink that spreads as far as light does reads as a stain, not a body.
      const bloom = rad * 2.4 * STYLE.bloom;
      const grd = g.createRadialGradient(p.sx, p.sy, 0, p.sx, p.sy, bloom);
      // Gold against teal, and nothing else. `hot` is the one channel these
      // clouds have for emphasis — an enum among schemas, a permission among
      // operations, a table whose SQL exists — and it only works while it is
      // the only thing in the picture that is a different colour.
      //
      // A clustered mote takes its owner's tint, so an amber body is amber all
      // the way through rather than a gold pin in a teal cloud.
      const tint = d.ink ? tintOf(d.ink) : d.tier ? tintOf(d.tier) : null;
      const core = d.hot ? INK.moteHot : (tint ? tint.core : INK.mote);
      const mid = tint ? tint.body : INK.moteMid;
      grd.addColorStop(0, `rgba(${core},${a.toFixed(3)})`);
      grd.addColorStop(0.5, `rgba(${mid},${(a * 0.45).toFixed(3)})`);
      grd.addColorStop(1, `rgba(${mid},0)`);
      g.fillStyle = grd;
      g.beginPath();
      g.arc(p.sx, p.sy, bloom, 0, 6.284);
      g.fill();

      if (promoted) {
        // The hard middle. A radial gradient alone stays a smudge however big
        // it gets; what makes a dot read as a node is an edge.
        g.fillStyle = `rgba(${core},${Math.min(1, a * 1.6 * STYLE.moteCore).toFixed(3)})`;
        g.beginPath();
        g.arc(p.sx, p.sy, Math.max(close ? 1.6 : 1.1, rad * 0.7), 0, 6.284);
        g.fill();
      }
    });
  }

  /**
   * Each hub's mass as a dashed circle, for the flat layout.
   *
   * A mote cloud with the projection off is a smudge: every mote lands at the
   * same depth, the twinkle has nothing to modulate, and the shell bias that
   * gives a 3D cluster its edge just fills a disc. The flat view is the one
   * that has to read at a glance and print, so the mass becomes an outline —
   * the same radius the cloud would have had, which keeps the two layouts
   * making the same claim about relative size.
   */
  _drawHoops(g, model, lit, FR, cx, cy) {
    g.setLineDash([2, 6]);
    g.lineWidth = 1;
    for (const hub of model.hubs) {
      if (!(hub.cr > 0)) continue;
      const ink = tintOf(hub.ink ?? hub.tier);
      const on = lit(hub.id);
      g.strokeStyle = `rgba(${ink.body},`
        + `${(on ? 0.5 : Math.min(0.5, DIM_HOOP * STYLE.dim)).toFixed(2)})`;
      g.beginPath();
      g.arc(cx + hub.fx * FR, cy + hub.fy * FR, hub.cr * FR, 0, 6.284);
      g.stroke();
    }
    g.setLineDash([]);
  }

  _drawLinks(g, model, hp, t, lit, unit, flat = false) {
    const index = new Map(model.hubs.map((h, i) => [h, i]));
    // A dense model draws quiet lanes until the pointer picks one out.
    const dense = model.links.length > DENSE_LANES;

    // The travelling window. `share` is the fraction of the model live at any
    // instant, bounded at both ends; a lane's place in the sweep comes from its
    // index, so which lanes are live is stable frame to frame and moves at a
    // readable pace rather than flickering.
    const lanes = Math.max(1, model.links.length);
    const live = Math.max(ACTIVE_MIN, Math.min(ACTIVE_MAX, lanes * ACTIVE_SHARE));
    const share = Math.min(1, live / lanes);

    model.links.forEach((link, i) => {
      const a = hp[index.get(link.a)];
      const b = hp[index.get(link.b)];
      if (!a || !b) return;
      // A lane that touches neither end of what is under the pointer is not
      // dimmed, it is gone. It was drawn at 18% before, and eighty of those on
      // an additive canvas is a bright mesh over the four lanes being asked
      // about.
      if (!lit(link.a.id) || !lit(link.b.id)) return;
      const on = true;
      // In a dense model only what the pointer has picked out flows. With
      // nothing hovered every lane is quiet, which is the resting state.
      //
      // In 2D nothing flows at all. See the note at the head of this change:
      // against faint lanes a travelling packet does not read as a packet, it
      // reads as another node.
      // Touching the hub under the pointer — not merely "lit", which also takes
      // in the lanes running between two of its neighbours. The question a
      // hover asks is what this one connects to.
      const hot = Boolean(this.hover) && (link.a === this.hover || link.b === this.hover);
      // Its turn in the sweep, or the pointer is on it. 2D never flows.
      const turn = ((i / lanes) + t / ACTIVE_PERIOD) % 1 < share;
      const flowing = !flat && (hot || turn);
      const depth = (a.z + b.z) / 2;
      const rest = flat
        ? (hot ? LINK_FLAT_HOT : (dense ? LINK_FLAT_DENSE : LINK_FLAT))
        : 0.34;
      const base = Math.max(STYLE.floorLink, rest - depth * 0.22 * STYLE.zK)
        * (on ? 1 : Math.min(1, 0.18 * STYLE.dim))
        // A lane waiting its turn is drawn, and drawn behind the ones that are
        // travelling. 2D is exempt: nothing there is travelling by definition,
        // so dimming against it would just make the whole picture fainter.
        * (!flowing && !flat ? LANE_RESTING : 1);
      // Gold is "look at this one" and teal is everything else. Two states,
      // because emphasis is a comparison and a comparison needs a background.
      const loud = Boolean(link.critical);
      const ink = loud
        ? { line: INK.linkCritical, packet: INK.packetCritical }
        : { line: INK.linkOrdinary, packet: INK.packetOrdinary };

      g.strokeStyle = `rgba(${ink.line},`
        + `${Math.min(1, base * (loud ? STYLE.linkLoud : STYLE.linkQuiet)).toFixed(3)})`;
      g.lineWidth = (loud ? 1.15 : 0.85)
        * (flat ? (hot ? LINK_FLAT_WIDTH_HOT : LINK_FLAT_WIDTH) : 1);
      if (flowing) {
        // The lane itself flows, so the direction is legible before any packet
        // reaches the eye.
        g.setLineDash([2.4, 7]);
        g.lineDashOffset = -((t * (loud ? 26 : 17) + i * 3) % 1000);
      }
      g.beginPath();
      g.moveTo(a.sx, a.sy);
      g.lineTo(b.sx, b.sy);
      g.stroke();
      if (flowing) g.setLineDash([]);

      if (!on || !flowing) return;
      // The packet runs source → target. The direction is the payload, so it is
      // never symmetrised.
      const phase = (t * (loud ? 0.34 : 0.22) + i * 0.13) % 1;
      const px = a.sx + (b.sx - a.sx) * phase;
      const py = a.sy + (b.sy - a.sy) * phase;
      const pr = (loud ? 2.6 : 1.9) * ((a.k + b.k) / 2) * unit;
      const pw = pr * 3 * STYLE.bloom;
      const pg = g.createRadialGradient(px, py, 0, px, py, pw);
      pg.addColorStop(0, `rgba(${ink.packet},${((loud ? 0.95 : 0.75) * STYLE.packet).toFixed(2)})`);
      pg.addColorStop(1, `rgba(${ink.line},0)`);
      g.fillStyle = pg;
      g.beginPath();
      g.arc(px, py, pw, 0, 6.284);
      g.fill();
    });
  }

  _drawHubs(g, model, hp, t, flat, lit, unit) {
    model.hubs.forEach((hub, i) => {
      const p = hp[i];
      const on = lit(hub.id);
      const pulse = flat ? 1 : 1 + Math.sin(t * 1.6 + i) * (hub.tier === 'satellite' ? 0.04 : 0.09);
      // ×1.5 in 2D, to hold the picture together without the dust behind it.
      const rad = hub.r * p.k * pulse * unit * (flat ? 1.5 : 1);
      const ink = tintOf(hub.ink ?? hub.tier);
      let front = Math.max(STYLE.floorHub, 0.9 - p.z * 0.55 * STYLE.zK)
        * (on ? 1 : Math.min(1, DIM_HUB * STYLE.dim));
      if (hub === this.hover || hub.id === this.selectedId) front = Math.min(1, front * 1.35);

      // The halo is what makes a hub read as a body rather than a dot, and it
      // is also the most expensive thing drawn per hub. Below about five pixels
      // there is no body to read — the gradient resolves to a smudge — so a
      // small hub skips it. On a join of three hundred tables that is most of
      // them, and it is the difference between 5fps and 50.
      const halo = rad * 2.8 * STYLE.bloom;
      if (halo >= 5) {
        const grd = g.createRadialGradient(p.sx, p.sy, 0, p.sx, p.sy, halo);
        grd.addColorStop(0, `rgba(${ink.core},${(front * 0.8 * STYLE.halo).toFixed(2)})`);
        grd.addColorStop(0.3, `rgba(${ink.body},${(front * 0.42 * STYLE.halo).toFixed(2)})`);
        grd.addColorStop(1, `rgba(${ink.body},0)`);
        g.fillStyle = grd;
        g.beginPath();
        g.arc(p.sx, p.sy, halo, 0, 6.284);
        g.fill();
      }

      g.fillStyle = `rgba(${ink.core},${Math.min(1, front * STYLE.core).toFixed(2)})`;
      g.beginPath();
      g.arc(p.sx, p.sy, rad * 0.8 * STYLE.coreR, 0, 6.284);
      g.fill();

      // The selection needs to survive the additive blend, which washes out a
      // thin stroke — so it is a second disc rather than an outline.
      if (hub.id === this.selectedId) {
        g.strokeStyle = `rgba(${INK.label},.85)`;
        g.lineWidth = 1.4;
        g.beginPath();
        g.arc(p.sx, p.sy, rad * 1.9, 0, 6.284);
        g.stroke();
      }
    });
  }

  /**
   * Labels are drawn last, in `source-over`, and only on the near face.
   *
   * `z ≤ 0.1` is the near hemisphere plus the terminator — nothing behind. A
   * label from the far side would read as belonging to whatever it happened to
   * land on, which is worse than no label.
   */
  _drawLabels(g, model, hp, lit, unit = 1, centre = null, scale = 0) {
    if (!this.showLabels) return;
    // A ring of 141 permissions cannot carry 141 names. Past the cap only what
    // the pointer is on is named — which is the only one being read anyway.
    const perTier = {};
    for (const hub of model.hubs) {
      const key = hub.ring ?? hub.tier;
      perTier[key] = (perTier[key] ?? 0) + 1;
    }

    // How many names this ring has room for, and therefore how many to skip.
    // On the sphere there is no ring, so the flat cap stands.
    const flatNow = this.mode === '2d' && scale > 0;
    const thin = {};
    for (const [key, count] of Object.entries(perTier)) {
      if (!flatNow) { thin[key] = 1; continue; }
      const r = Number(key) || RINGS[key] || RINGS.spine;
      const seats = Math.max(4, Math.floor((2 * Math.PI * r * scale) / LABEL_SEAT));
      thin[key] = Math.max(1, Math.ceil(count / seats));
    }

    const flat = this.mode === '2d';
    g.font = LABEL_FONT;
    g.textBaseline = 'alphabetic';
    model.hubs.forEach((hub, i) => {
      const p = hp[i];
      // The near hemisphere only — except on a camera scene, which is not a
      // hemisphere. Five names are the map, and culling by depth dropped three
      // of them from every frame.
      if (p.z > 0.1 && !this.camera) return;
      const key = hub.ring ?? hub.tier;
      const skip = (thin[key] ?? 1) > 1 && (hub.slot ?? 0) % thin[key] !== 0;
      const crowded = (perTier[key] ?? 0) > (this.labelMax ?? 40);
      const named = hub === this.hover || hub.id === this.selectedId;
      if ((crowded || skip) && !named) return;
      const on = lit(hub.id);
      // A dimmed layer keeps its name. On a graph of 300 tables dropping the
      // unlit labels is what makes a hover legible; on five bodies the names
      // are the map, and a reader who has focused one still has to be able to
      // see where the other four are to move between them.
      if (!on && !named && !this.camera) return;
      const a = (named ? 1 : Math.max(0.22, 0.92 - (p.z + 1) * 0.36)) * (on || named ? 1 : 0.34);
      g.fillStyle = `rgba(${INK.label},${a.toFixed(2)})`;
      // Clear of whichever is bigger — the dot, or the cloud around it.
      const gap = Math.max(
        hub.r * p.k * unit * (flat ? 1.5 : 1) * 2.2 + 11,
        hub.cr ? hub.cr * scale * p.k + 13 : 0
      );

      if (!flat || !centre) {
        g.textAlign = 'center';
        // `up` is the caller's, and it is a layout decision rather than a
        // property of the thing: it says which side of this body is empty.
        const ly = hub.up ? p.sy - gap : p.sy + gap + 1;
        // Above the name when the label sits above the body, so the pair reads
        // as one block in both directions rather than straddling the dot.
        g.fillText(hub.name, p.sx, ly);
        if (hub.sub) this._sublabel(g, hub.sub, p.sx, hub.up ? ly - 13 : ly + 13, a);
        g.font = LABEL_FONT;
        return;
      }

      // Outward along the spoke. The vertical nudge is a third of the cap
      // height rather than a baseline shift, so a label at three o'clock sits
      // on the dot's centreline instead of hanging below it.
      const dx = p.sx - centre.x;
      const dy = p.sy - centre.y;
      const d = Math.hypot(dx, dy);
      // A hub at the centre has no outward direction — the vector collapses and
      // the name lands on its own dot. Below is where a label goes when no
      // direction is better than any other.
      if (d < 1) {
        g.textAlign = 'center';
        g.fillText(hub.name, p.sx, p.sy + gap + 1);
        if (hub.sub) this._sublabel(g, hub.sub, p.sx, p.sy + gap + 14, a);
        g.font = LABEL_FONT;
        return;
      }
      g.textAlign = dx >= 0 ? 'left' : 'right';
      const lx = p.sx + (dx / d) * gap;
      const ly = p.sy + (dy / d) * gap + 3.5;
      g.fillText(hub.name, lx, ly);
      if (hub.sub) this._sublabel(g, hub.sub, lx, ly + 13, a);
      return;
    });
    g.textAlign = 'center';
  }

  /** The count under a name. Mono, so figures line up between bodies. */
  _sublabel(g, text, x, y, alpha) {
    g.font = SUB_FONT;
    g.fillStyle = `rgba(${INK.sublabel},${(alpha * 0.72).toFixed(2)})`;
    g.fillText(text, x, y);
    g.fillStyle = `rgba(${INK.label},${alpha.toFixed(2)})`;
    g.font = LABEL_FONT;
  }

  /**
   * What is inside a cluster, once the reader is close enough to ask.
   *
   * Nearest first and capped: a cluster can hold 340 motes and naming all of
   * them would replace a picture of a quantity with a wall of type. The ones
   * that get names are the ones nearest the eye, which are also the ones whose
   * positions are least ambiguous.
   */
  _drawMoteLabels(g, model, dp) {
    const near = [];
    for (let i = 0; i < model.dust.length; i++) {
      const d = model.dust[i];
      if (!d.name) continue;
      // A focused body owns the answer: naming the nearest 34 across the whole
      // model would spend most of them on whichever cluster happened to have
      // swung to the front, which is not the one being asked about.
      if (this.focusId && d.owner !== this.focusId) continue;
      const p = dp[i];
      if (!p || p.z > 0.1) continue;
      near.push([p.z, d.name, p]);
    }
    if (!near.length) return;
    near.sort((a, b) => a[0] - b[0]);

    g.font = MOTE_FONT;
    g.textAlign = 'left';
    g.textBaseline = 'middle';
    // Fades in over the threshold rather than snapping on, so zooming reads as
    // getting closer rather than as a mode change.
    const rise = Math.min(1, (this.zoom - SUB_ZOOM) / 0.6);
    for (const [z, name, p] of near.slice(0, SUB_LABELS)) {
      const a = Math.max(0.15, 0.85 - (z + 1) * 0.4) * rise;
      g.fillStyle = `rgba(${INK.sublabel},${a.toFixed(2)})`;
      g.fillText(name, p.sx + 6, p.sy);
    }
    g.textBaseline = 'alphabetic';
    g.textAlign = 'center';
  }

  // ── hit testing ─────────────────────────────────────────────────
  /**
   * The nearest projected hub to a point, or null.
   *
   * The floor matters more than it looks: the smallest bodies are a couple of
   * pixels across at the back of the sphere, and a hit radius of "the dot" makes
   * them unclickable exactly when a reader has finally spotted one.
   */
  hubAt(sx, sy) {
    let best = null;
    let bestD = Infinity;
    for (const entry of this._screen) {
      const d = Math.hypot(entry.sx - sx, entry.sy - sy);
      const hit = Math.max(this.camera ? 46 : 14, entry.r * 1.25);
      if (d < hit && d < bestD) { best = entry.hub; bestD = d; }
    }
    return best;
  }

  _bindEvents() {
    const canvas = this.canvas;
    const at = (e) => {
      const rect = canvas.getBoundingClientRect();
      return [e.clientX - rect.left, e.clientY - rect.top];
    };

    // ---- turning it ---------------------------------------------------
    canvas.addEventListener('mousedown', (e) => {
      if (e.button !== 0) return;
      this._drag = { x: e.clientX, y: e.clientY, active: true, moved: 0 };
      canvas.style.cursor = 'grabbing';
    });

    // On the window: a drag that leaves the canvas has not stopped being a
    // drag, and one that is released outside it has to end somewhere.
    window.addEventListener('mousemove', (e) => {
      const drag = this._drag;
      if (!drag?.active) return;
      const dx = e.clientX - drag.x;
      const dy = e.clientY - drag.y;
      drag.x = e.clientX;
      drag.y = e.clientY;
      drag.moved += Math.abs(dx) + Math.abs(dy);
      // Negated. `x1 = x·cos(yaw) + z·sin(yaw)`, so a growing yaw carries the
      // right-hand side of the sphere to the left — dragging right pushed the
      // scene away from the pointer instead of with it. Pitch is already the
      // right way round: a growing pitch brings the top down the front, which
      // is what pulling down should do.
      this.spin.yaw -= dx * DRAG_YAW;
      this.spin.pitch += dy * DRAG_PITCH;
      // A parked loop — 2D, or reduced motion — draws no frames of its own, so
      // the scene would not move at all without this.
      if (this._still()) this.draw();
    });

    window.addEventListener('mouseup', () => {
      const drag = this._drag;
      if (!drag) return;
      this._drag = null;
      // Past the slop it was a drag, and the click browsers fire after mouseup
      // has to be swallowed or turning the scene also selects something.
      this._swallowClick = drag.moved > DRAG_SLOP;
      canvas.style.cursor = 'default';
    });

    // ---- zoom -----------------------------------------------------------
    canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      // Exponential, so a notch out undoes a notch in exactly, whatever the
      // scale — linear steps crawl when zoomed in and lurch when zoomed out.
      const next = this.zoom * Math.exp(-e.deltaY * ZOOM_STEP);
      this.zoom = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, next));
      this.onZoom(this.zoom);
      this.start();
      if (this._still()) this.draw();
    }, { passive: false });

    canvas.addEventListener('mousemove', (e) => {
      if (this._drag?.active) return;
      const over = this.viewAt(...at(e));
      const wasView = this.hoverView;
      this.hoverView = over?.view.id ?? null;
      if (wasView !== this.hoverView && this._still()) this.draw();
      if (over) {
        canvas.style.cursor = 'pointer';
        this.onHover(null);
        return;
      }
      const hub = this.hubAt(...at(e));
      canvas.style.cursor = hub ? 'pointer' : 'grab';
      if (hub === this.hover) return;
      this.hover = hub;
      this.onHover(hub);
      // A parked loop draws no frames of its own, so the highlight has to be
      // painted here or hovering does nothing at all. That is reduced motion,
      // and it is now also every flat layout.
      if (this._still()) this.draw();
    });

    canvas.addEventListener('mouseleave', () => {
      if (!this.hover) return;
      this.hover = null;
      this.onHover(null);
      if (this._still()) this.draw();
    });

    canvas.addEventListener('click', (e) => {
      if (this._swallowClick) { this._swallowClick = false; return; }
      // Before the hubs: a view node sits on top of whatever it overlaps, and
      // the ring is drawn over the body it belongs to.
      const view = this.viewAt(...at(e));
      if (view) { this.onView(view.hub, view.view); return; }
      const hub = this.hubAt(...at(e));
      if (hub) this.onSelect(hub, { open: false });
      else this.onEmpty();
    });

    canvas.addEventListener('dblclick', (e) => {
      const hub = this.hubAt(...at(e));
      if (hub) this.onSelect(hub, { open: true });
    });

    // A tap is a click on every browser here, so touch needs nothing of its
    // own — there is no pan or pinch to conflict with, because the scene has no
    // camera the reader controls.
  }
}

/**
 * Tie every mote in [from, to) to its nearest neighbours within `reach`.
 *
 * O(n²) once at build and never again. This is the only structure in the
 * picture that is not data: it is texture, and it stays honest about that by
 * carrying no colour coding at all. Bounded to a slice so a clustered model
 * pays it per cluster rather than across every mote on screen at once — and so
 * a thread never joins two clusters, which would look like a relationship when
 * the lanes are the relationships.
 */
function linkNearest(dust, from, to, reach, out) {
  for (let i = from; i < to; i++) {
    const a = dust[i];
    const near = [];
    for (let j = from; j < to; j++) {
      if (i === j) continue;
      const b = dust[j];
      const d2 = (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2;
      if (d2 < reach) near.push([d2, j]);
    }
    near.sort((p, q) => p[0] - q[0]);
    for (const [, j] of near.slice(0, FILAMENT_NEAR)) if (j > i) out.push([i, j]);
  }
}

/**
 * The legend under a galaxy, in the viewer's own markup rather than painted.
 *
 * Painted text on an additive canvas has to fight the glow behind it; DOM text
 * on the scrim does not, and it stays selectable.
 */
export function galaxyLegend(container, entries, note) {
  container.innerHTML = '';
  for (const [tier, label] of entries) {
    const row = document.createElement('div');
    row.className = 'legend-row';
    const dot = document.createElement('span');
    dot.className = 'legend-dot';
    dot.style.background = `rgb(${tintOf(tier).body})`;
    row.append(dot);
    const text = document.createElement('span');
    text.textContent = label;
    row.append(text);
    container.append(row);
  }
  if (note) {
    const row = document.createElement('div');
    row.className = 'legend-row legend-note';
    row.textContent = note;
    container.append(row);
  }
}
