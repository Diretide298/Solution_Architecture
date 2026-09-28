/**
 * The mascot as a still that becomes a video when that is worth doing.
 *
 * The corner dock in `mascot.js` is a different thing: it reacts to what the
 * reader is doing, draws its next segment from a weighted mix, and glitches
 * between clips. A figure standing beside a heading needs none of that. It
 * loops one clip and that is the whole behaviour — so this is about 80 lines
 * rather than 500, and it shares the one keyer instead of carrying a second.
 *
 * **The still is the page, and the video is an upgrade.** The `<img>` is in the
 * markup and renders on the first paint; nothing here is needed for the page to
 * look right. The clip is fetched only once all of these hold:
 *
 *   - the reader has not turned video off (the same `adam-mascot-video` switch
 *     the dock offers — one switch for the mascot, wherever it appears);
 *   - they have not asked for reduced motion;
 *   - the figure is actually on screen, so a mascot below the fold costs
 *     nothing on a page nobody scrolls;
 *   - the connection is not metered or slow, and `Save-Data` is not set.
 *
 * That last one matters more here than in the viewer: the clips are 2.5 MB each
 * and `landing.html` is a public page that people open on phones. A marketing
 * page that spends 2.5 MB of somebody's data on a decoration has made a choice
 * on their behalf, and this is the choice made the other way.
 *
 * If WebGL is missing the keyer returns null and the still simply stays, which
 * is also what happens if the clip 404s or the decode fails.
 */

import { makeKeyer } from '/mascot-keyer.js';

const VIDEO_KEY = 'adam-mascot-video';

/** Video is on unless the reader turned it off. Storage can throw in a private
 *  window, and a decoration is not worth a thrown exception. */
function videoWanted() {
  try {
    return localStorage.getItem(VIDEO_KEY) !== 'off';
  } catch {
    return true;
  }
}

/** Whether it is polite to spend a couple of megabytes here. `connection` is
 *  absent on Safari and Firefox, where the answer is a plain yes. */
function connectionAllows() {
  const c = navigator.connection;
  if (!c) return true;
  if (c.saveData) return false;
  return !/(^|-)2g$/.test(c.effectiveType ?? '');
}

/**
 * Upgrade one figure to video.
 *
 * `figure` is the element holding the still `<img>`. The canvas is inserted
 * beside it and the still is faded out only once a frame has actually been
 * drawn — never on `canplay`, which fires before there is anything to show and
 * would flash an empty box.
 */
export function mountFigure(figure, { clip, poster } = {}) {
  if (!figure || figure.dataset.figure === 'on') return () => {};
  const still = figure.querySelector('img');
  if (!clip || !videoWanted()) return () => {};
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return () => {};
  if (!connectionAllows()) return () => {};

  let stop = () => {};
  const start = () => {
    figure.dataset.figure = 'on';

    const canvas = document.createElement('canvas');
    canvas.className = 'mascot-figure-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    figure.append(canvas);

    const draw = makeKeyer(canvas);
    if (!draw) { canvas.remove(); return; }          // no WebGL: keep the still

    const video = document.createElement('video');
    Object.assign(video, {
      src: clip, muted: true, loop: true, playsInline: true,
      preload: 'auto', crossOrigin: 'anonymous',
    });
    if (poster) video.poster = poster;
    video.style.display = 'none';
    figure.append(video);

    let raf = 0;
    let shown = false;
    const tick = () => {
      draw(video);
      // The still goes only after the first real frame is on the canvas.
      if (!shown && video.readyState >= 2 && video.videoWidth) {
        shown = true;
        figure.dataset.figure = 'playing';
      }
      raf = requestAnimationFrame(tick);
    };

    video.play().then(() => { raf = requestAnimationFrame(tick); }).catch(() => {
      // Autoplay refused, or the file is unreachable. The still is already
      // correct, so there is nothing to recover from.
      canvas.remove();
      video.remove();
      delete figure.dataset.figure;
    });

    stop = () => {
      cancelAnimationFrame(raf);
      video.pause();
      video.removeAttribute('src');
      video.load();
      canvas.remove();
      video.remove();
      delete figure.dataset.figure;
    };
  };

  // Only once it is on screen. `IntersectionObserver` is everywhere that has
  // WebGL, but the fallback is to start rather than to never start.
  if (typeof IntersectionObserver !== 'function') { start(); return () => stop(); }
  const seen = new IntersectionObserver((entries) => {
    if (!entries.some((e) => e.isIntersecting)) return;
    seen.disconnect();
    start();
  }, { rootMargin: '200px' });
  seen.observe(still ?? figure);
  return () => { seen.disconnect(); stop(); };
}
