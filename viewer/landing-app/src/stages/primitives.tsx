/**
 * The small parts every journey diagram is built from.
 *
 * A diagram is a pure function of its stage's progress `p` and `state`: parts
 * switch on at thresholds of `p`, and the transitions (0.7s for reveals, 0.22s
 * for state flips, cubic-bezier(.22,1,.36,1)) carry the motion between frames.
 * Nothing here moves a card; the diagrams live inside the card's band.
 */
import { motion } from 'motion/react';
import type { ReactNode } from 'react';

export type StageState = 'pending' | 'active' | 'done';
export type StageProps = { p: number; state: StageState; cycle: number };

export const EASE: [number, number, number, number] = [0.22, 1, 0.36, 1];
export const SLOW = { duration: 0.7, ease: EASE };
export const QUICK = { duration: 0.22, ease: EASE };

export const clamp = (v: number) => (v < 0 ? 0 : v > 1 ? 1 : v);
/** Has this stage got as far as `t`? A finished stage has got everywhere. */
export const reached = (s: StageProps, t: number) => s.state === 'done' || (s.state === 'active' && s.p >= t);
/** 0..1 across a window of the stage, for bars and counters. */
export const span = (s: StageProps, a: number, b: number) =>
  s.state === 'done' ? 1 : s.state === 'active' ? clamp((s.p - a) / (b - a)) : 0;

/** The whole diagram: ghosted until its stage runs, full while it runs, settled after. */
export function Stage({ state, children, className = '' }: { state: StageState; children: ReactNode; className?: string }) {
  return (
    <motion.div
      className={`relative h-full w-full ${className}`}
      initial={false}
      animate={{ opacity: state === 'pending' ? 0.3 : state === 'done' ? 0.86 : 1 }}
      transition={SLOW}
    >
      {children}
    </motion.div>
  );
}

/** Fades and settles a part in; `rest` is its opacity once something later has superseded it. */
export function Reveal({
  on, children, className = '', x = 0, y = 6, delay = 0, dim = 0.18, rest = 1,
}: { on: boolean; children: ReactNode; className?: string; x?: number; y?: number; delay?: number; dim?: number; rest?: number }) {
  return (
    <motion.div
      className={className}
      initial={false}
      animate={{ opacity: on ? rest : dim, x: on ? 0 : x, y: on ? 0 : y }}
      transition={{ ...SLOW, delay }}
    >
      {children}
    </motion.div>
  );
}

/** A file or record, drawn the way the viewer draws one: a header strip and a body. */
export function Panel({
  title, meta, lit = false, dark = false, className = '', bodyClassName = '', children,
}: { title: ReactNode; meta?: ReactNode; lit?: boolean; dark?: boolean; className?: string; bodyClassName?: string; children: ReactNode }) {
  return (
    <div
      className={`overflow-hidden rounded-md border shadow-[0_1px_3px_rgba(13,35,51,.07)] transition-colors duration-300 ${
        dark ? 'border-[#16324a] bg-[#0b1c2c]' : lit ? 'border-adam-line bg-white' : 'border-adam-rule bg-white'
      } ${className}`}
    >
      <div className={`flex items-center gap-1.5 border-b px-2 py-[3px] ${dark ? 'border-[#16324a] bg-[#0f2436]' : 'border-adam-rule bg-adam-raised'}`}>
        <span className="flex shrink-0 gap-[3px]">
          {[0, 1, 2].map((i) => <i key={i} className={`block size-[5px] rounded-full ${dark ? 'bg-[#29445c]' : 'bg-adam-rule'}`} />)}
        </span>
        <span className={`min-w-0 truncate font-mono text-[9px] ${dark ? 'text-[#9fc3d8]' : 'text-adam-strong'}`}>{title}</span>
        {meta ? <span className="ml-auto flex shrink-0 items-center font-mono text-[8.5px] text-adam-muted">{meta}</span> : null}
      </div>
      <div className={`px-2 py-1.5 ${bodyClassName}`}>{children}</div>
    </div>
  );
}

const TONES = {
  open: 'border-[#eadfc8] bg-[#fbf6ec] text-adam-warn',
  ok: 'border-[#bfe6d5] bg-[#e8f7f0] text-adam-ok',
  accent: 'border-[#9cd9ec] bg-adam-soft text-adam-deep',
  solid: 'border-adam-deep bg-adam-deep text-white',
  muted: 'border-adam-rule bg-adam-raised text-adam-muted',
} as const;

export function Pill({ tone = 'muted', children, className = '' }: { tone?: keyof typeof TONES; children: ReactNode; className?: string }) {
  return (
    <span className={`inline-flex shrink-0 items-center gap-1 rounded-full border px-1.5 font-mono text-[8px] leading-[13px] tracking-wide transition-colors duration-200 ${TONES[tone]} ${className}`}>
      {children}
    </span>
  );
}

export function Skeleton({ w = '100%', className = '' }: { w?: string; className?: string }) {
  return <span className={`block h-[3px] rounded-full bg-[#dfe8ec] ${className}`} style={{ width: w }} />;
}

export function Check({ className = '', size = 9 }: { className?: string; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 10 10" className={className} aria-hidden="true">
      <path d="M2 5.2 4.1 7.3 8 2.9" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

/** Monospace lines. `dark` is for a terminal panel: the light ink has to be
 *  the only colour class, or the default one wins on stylesheet order. */
export function Code({ children, className = '', dark = false }: { children: ReactNode; className?: string; dark?: boolean }) {
  return <div className={`font-mono text-[9.5px] leading-[14px] ${dark ? 'text-[#cfe3ee]' : 'text-adam-strong'} ${className}`}>{children}</div>;
}

export const Key = ({ children }: { children: ReactNode }) => <span className="text-adam-deep">{children}</span>;
export const Num = ({ children }: { children: ReactNode }) => <span className="text-[#9a5a2a]">{children}</span>;

/** The chevron from the lockup, in a ring. */
export function AdamMark({ lit, size = 30 }: { lit: boolean; size?: number }) {
  return (
    <motion.div
      className="relative grid shrink-0 place-items-center rounded-full border bg-white"
      style={{ width: size, height: size }}
      initial={false}
      animate={{
        borderColor: lit ? '#0389d7' : '#dfe8ec',
        boxShadow: lit ? '0 0 0 4px rgba(4,216,242,.18)' : '0 0 0 0 rgba(4,216,242,0)',
      }}
      transition={SLOW}
    >
      <svg width={size * 0.46} height={size * 0.46} viewBox="0 0 14 14" aria-hidden="true">
        <path d="M2 12 7 2l5 10" fill="none" stroke={lit ? '#0268ce' : '#1d2c33'} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    </motion.div>
  );
}
