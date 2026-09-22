/**
 * Taking a diagram away as a picture.
 *
 * **A redraw, not a screenshot.** Every renderer here sizes its backing store
 * to `devicePixelRatio` and then works in CSS pixels, so raising that multiplier
 * and drawing again produces the same picture with more pixels in it — crisp
 * text, crisp strokes, at any scale. Scaling up the bitmap that is already on
 * screen would produce a blurry version of a diagram whose whole value is that
 * the labels are readable. The one line that makes it possible is `exportScale`
 * in each renderer's `_resize`.
 *
 * **What you see is what you get, deliberately.** The export keeps the current
 * zoom, pan, filters and theme rather than fitting everything first. A button
 * that rearranged the view before saving would hand somebody a picture they had
 * not looked at — and on a graph of four hundred nodes, "everything" fitted into
 * one frame is an unreadable smudge that nobody wanted. Fit it yourself, then
 * save what you can read.
 *
 * PNG rather than SVG, because these are canvas renderers and always have been.
 * An SVG export would mean a second implementation of every draw call in the
 * four files, kept in step by hand — which is how the picture on screen and the
 * picture in the document start disagreeing.
 */

/** Chrome refuses a canvas over 65,535 in either direction and starts failing on
 *  total area well before that; Safari is stricter still. The scale is reduced
 *  until it fits rather than the export failing, because a 2× picture is worth
 *  having and a silent blank PNG is not. */
const MAX_SIDE = 16000;
const MAX_AREA = 64e6;

/** Three times what is on screen: a 1400-pixel canvas becomes 4200 across,
 *  which is a full-width figure in a document or a slide without looking soft.
 *  Higher stops paying for itself and starts hitting the limits above. */
const SCALE = 3;

function safeScale(canvas, wanted) {
  // The backing store already carries devicePixelRatio, so this is measured
  // from what is actually there rather than from the CSS size — on a 2× screen
  // the picture is already twice the size the page thinks it is.
  const w = canvas.width;
  const h = canvas.height;
  if (!w || !h) return 1;
  let scale = wanted;
  while (scale > 1 && (w * scale > MAX_SIDE || h * scale > MAX_SIDE
                       || w * scale * h * scale > MAX_AREA)) {
    scale -= 0.5;
  }
  return Math.max(1, scale);
}

/** The colour behind the drawing.
 *
 *  A canvas is transparent wherever nothing was painted, and a PNG with a
 *  transparent background looks fine in a browser and broken in Word, Slack and
 *  every slide deck — black-on-black or white-on-white depending on the viewer.
 *  So the export composites onto the page's own panel colour, which is also why
 *  a diagram saved in night mode comes out dark: it is the diagram as it was on
 *  screen, and the alternative is recolouring somebody's picture without asking.
 */
function backdrop(canvas) {
  const styles = getComputedStyle(canvas);
  for (const value of [styles.backgroundColor,
                       getComputedStyle(canvas.parentElement ?? document.body).backgroundColor,
                       getComputedStyle(document.body).backgroundColor]) {
    if (value && value !== 'transparent' && !/rgba\(\s*0,\s*0,\s*0,\s*0\s*\)/.test(value)) {
      return value;
    }
  }
  return '#ffffff';
}

const today = () => new Date().toISOString().slice(0, 10);

/** `adam-data-model-2026-09-23.png`. Lower case, hyphens, no spaces: this ends
 *  up in a downloads folder, an email and sometimes a URL. */
function fileName(name) {
  const clean = String(name ?? 'diagram').toLowerCase()
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  return `adam-${clean || 'diagram'}-${today()}.png`;
}

/** Repaint at whatever `exportScale` now says.
 *
 *  The box renderers resize and draw; the galaxy sizes itself inside `draw`,
 *  every frame, because it animates. One name for "put the picture back on the
 *  canvas" rather than a branch at each call site. */
const repaint = (view) => (typeof view.resize === 'function' ? view.resize() : view.draw());

/**
 * Draw `view` at `scale`, composite it onto a background, and hand back a blob.
 *
 * The live canvas is restored before this returns, including when the draw
 * throws — a failed export that leaves somebody's diagram rendered at three
 * times the size, with every hit test off by a factor of three, would be a far
 * worse bug than the one that caused it.
 */
async function render(view, canvas, scale) {
  const before = view.exportScale ?? 1;
  let shot;
  try {
    view.exportScale = scale;
    repaint(view);
    shot = document.createElement('canvas');
    shot.width = canvas.width;
    shot.height = canvas.height;
    const ctx = shot.getContext('2d');
    ctx.fillStyle = backdrop(canvas);
    ctx.fillRect(0, 0, shot.width, shot.height);
    ctx.drawImage(canvas, 0, 0);
  } finally {
    view.exportScale = before;
    repaint(view);
  }
  return new Promise((resolve) => shot.toBlob(resolve, 'image/png'));
}

/** Which of a view's canvases is on screen right now.
 *
 *  **A view often has two.** The contract graph is a force layout at some
 *  scopes and a particle field at others; the data model is the same. Which one
 *  is showing is decided by state this module has no business knowing about, so
 *  it asks the only question that matters and that cannot drift: which of them
 *  has been given a size by the layout.
 *
 *  It also answers the other case for free. A canvas in a hidden view measures
 *  zero, its renderer's `_resize` returns early rather than culling everything,
 *  and the backing store stays at the 300×150 a canvas element is born with —
 *  so exporting one produces an entirely plausible PNG of nothing, which is
 *  worse than a refusal because nobody opens a file they have just saved.
 */
function onScreen(targets) {
  for (const [canvas, view] of targets) {
    if (!canvas || !view) continue;
    const box = canvas.getBoundingClientRect();
    if (box.width > 1 && box.height > 1) return { canvas, view };
  }
  return null;
}

/**
 * Put a save button in a toolbar.
 *
 * `targets` is every canvas this toolbar might be sitting above, best first;
 * the one that is on screen when the button is pressed is the one that is
 * saved. `name` may be a function, so a view whose scope changes — the data
 * model per module, the graph per scope — names its file after what is actually
 * on screen rather than after the tab it lives in.
 */
export function mountDiagramExport({ toolbar, targets, name, label = 'PNG' }) {
  if (!toolbar || !targets?.length) return;
  const canvas = targets[0][0];
  if (!canvas) return;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'ghost-btn';
  button.id = `${canvas.id}-png`;
  button.textContent = label;
  button.title = `Save this diagram as a PNG, ${SCALE}× what is on screen. `
    + 'It saves exactly what you can see — zoom, filters and all — so fit it '
    + 'first. Night mode saves a dark picture; switch to day for a document.';

  button.onclick = async () => {
    const was = button.textContent;
    button.disabled = true;
    button.textContent = 'Saving…';
    try {
      const shown = onScreen(targets);
      if (!shown) throw new Error('this diagram is not on screen, so there is nothing to save');
      const scale = safeScale(shown.canvas, SCALE);
      const blob = await render(shown.view, shown.canvas, scale);
      if (!blob) throw new Error('the browser would not encode the picture');
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = fileName(typeof name === 'function' ? name() : name);
      link.click();
      // Freed on the next turn of the loop rather than immediately: revoking
      // before the browser has started the download cancels it in Firefox.
      setTimeout(() => URL.revokeObjectURL(url), 10_000);
      button.textContent = scale < SCALE ? `Saved at ${scale}×` : 'Saved';
    } catch (error) {
      // Said on the button rather than in a console nobody has open. The
      // realistic failure is a canvas too large for the browser to encode, and
      // the person needs to know to zoom in rather than to try again.
      button.textContent = 'Could not save';
      console.error('diagram export failed', error);
    } finally {
      setTimeout(() => { button.textContent = was; button.disabled = false; }, 2400);
    }
  };

  // Before the hint, which is the element that stretches. Appending would put
  // the button after it and leave it stranded at the far right of the bar.
  const hint = toolbar.querySelector('.graph-hint');
  if (hint) toolbar.insertBefore(button, hint);
  else toolbar.append(button);
  return button;
}
