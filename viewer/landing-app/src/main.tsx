/**
 * Mounts the seven journey diagrams into the landing page's card bands.
 *
 * The signal engine (public/adam-journey.js) owns the clock and dispatches a
 * `journey:frame` event on the host every frame: which stage is running, how
 * far through it is, and whether the run is holding or fading. This file turns
 * that into a small store and renders one React diagram into each
 * `[data-stage]` band through a portal — the cards stay the page's own DOM.
 *
 *   import('/landing-journey/journey.js').then((m) => m.mount(hostEl));
 */
import './journey.css';
import { memo, useSyncExternalStore } from 'react';
import { createPortal } from 'react-dom';
import { createRoot } from 'react-dom/client';
import { STAGES, type StageProps, type StageState } from './stages';

type Frame = { idx: number; p: number; phase: 'idle' | 'run' | 'hold' | 'fade'; fade: number; cycle: number };

let frame: Frame = { idx: -1, p: 0, phase: 'idle', fade: 0, cycle: -1 };
const listeners = new Set<() => void>();
const subscribe = (fn: () => void) => { listeners.add(fn); return () => { listeners.delete(fn); }; };
const getFrame = () => frame;

function receive(detail: Frame) {
  // Two decimals is finer than any diagram can show, and it keeps a stage that
  // is not moving from re-rendering sixty times a second.
  const next: Frame = { ...detail, p: Math.round(detail.p * 100) / 100, fade: Math.round(detail.fade * 50) / 50 };
  if (next.idx === frame.idx && next.p === frame.p && next.phase === frame.phase
    && next.fade === frame.fade && next.cycle === frame.cycle) return;
  frame = next;
  listeners.forEach((fn) => fn());
}

function stateOf(f: Frame, i: number): StageState {
  if (f.phase === 'idle') return 'pending';
  if (f.phase !== 'run') return 'done';
  return i < f.idx ? 'done' : i === f.idx ? 'active' : 'pending';
}

const Stage = memo(function Stage({ index, ...props }: StageProps & { index: number }) {
  const Draw = STAGES[index];
  return <Draw {...props} />;
});

function Diagrams({ bands }: { bands: HTMLElement[] }) {
  const f = useSyncExternalStore(subscribe, getFrame);
  const dim = f.phase === 'fade' ? 1 - 0.75 * f.fade : 1;
  return (
    <>
      {bands.map((band, i) => {
        const state = stateOf(f, i);
        const p = state === 'done' ? 1 : state === 'active' ? f.p : 0;
        return createPortal(
          <div className="jd-root" style={{ opacity: dim }}>
            <Stage index={i} p={p} state={state} cycle={Math.max(0, f.cycle)} />
          </div>,
          band,
          `stage-${i}`,
        );
      })}
    </>
  );
}

export function mount(host: HTMLElement) {
  const bands = Array.from({ length: 7 }, (_, i) => host.querySelector<HTMLElement>(`[data-stage="${i + 1}"]`));
  if (bands.some((b) => !b)) throw new Error('journey diagrams: the seven [data-stage] bands are not on the page');
  host.addEventListener('journey:frame', (e) => receive((e as CustomEvent<Frame>).detail));
  const shell = document.createElement('div');
  shell.hidden = true;
  host.appendChild(shell);
  const root = createRoot(shell);
  root.render(<Diagrams bands={bands as HTMLElement[]} />);
  return { unmount: () => root.unmount() };
}
