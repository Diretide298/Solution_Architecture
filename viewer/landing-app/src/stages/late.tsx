/**
 * Journey diagrams 05–07: the decision is written into the package, validated,
 * signed, and becomes an engineering-ready graph.
 *
 * The code in these panels is illustrative — the shape of what each step
 * writes, not a quotation from the package.
 */
import { AnimatePresence, motion } from 'motion/react';
import CountUp from '../components/rb/CountUp';
import ShinyText from '../components/rb/ShinyText';
import TextType from '../components/rb/TextType';
import {
  AdamMark, Check, Code, EASE, Panel, Pill, Reveal, SLOW, Stage, reached,
  type StageProps,
} from './primitives';

/* ── 05 Updating it inside Adam ───────────────────────────────────────── */

const LAYERS = [
  { name: 'contracts', file: 'orders.yaml', lines: ['/orders/{id}/refund:', '+  post: refundOrder', '+  x-permission: pos.refund'] },
  { name: 'screens', file: 'POS-044.yaml', lines: ['id: POS-044', '+ apis: [refundOrder]', '+ guard: pos.refund'] },
  { name: 'states', file: 'order.yaml', lines: ['PAID:', '+  to: REFUNDED', '+  guard: manager'] },
  { name: 'flows', file: 'F61.yaml', lines: ['steps:', '+ - POS-031 → POS-044', '+ - reprint receipt'] },
];
const LIGHT_AT = (i: number) => 0.2 + i * 0.1;
const ROW_Y = (i: number) => 12 + i * 28;

export function Updating(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const active = s.state === 'active';
  let current = -1;
  LAYERS.forEach((_, i) => { if (on(LIGHT_AT(i))) current = i; });
  const joined = on(0.64);
  const shown = LAYERS[Math.max(0, current)];
  return (
    <Stage state={s.state} className="flex flex-col gap-1.5">
      <div className="flex h-[112px] items-stretch">
        <div className="flex w-[94px] shrink-0 flex-col justify-between py-0.5">
          {LAYERS.map((layer, i) => {
            const lit = active && s.p >= LIGHT_AT(i) && s.p < LIGHT_AT(i) + 0.14;
            const set = on(LIGHT_AT(i));
            return (
              <Reveal key={layer.name} on={on(0.02 + i * 0.04)} x={-8} y={0}>
                <div className={`flex h-6 items-center gap-1.5 rounded border px-1.5 transition-colors duration-200 ${lit ? 'border-adam-line bg-adam-soft' : 'border-adam-rule bg-white'}`}>
                  <span className={`size-[9px] shrink-0 rounded-[3px] border transition-colors duration-200 ${set ? 'border-adam-deep bg-gradient-to-br from-adam-deep to-adam-bright' : 'border-[#9cd9ec] bg-adam-soft'}`} />
                  <span className={`font-mono text-[9px] transition-colors duration-200 ${lit ? 'text-adam-deep' : 'text-adam-strong'}`}>{layer.name}</span>
                </div>
              </Reveal>
            );
          })}
        </div>
        <div className="relative w-[58px] shrink-0">
          <svg className="absolute inset-0 h-full w-full overflow-visible" viewBox="0 0 58 112" preserveAspectRatio="none" aria-hidden="true">
            {LAYERS.map((layer, i) => {
              const set = on(LIGHT_AT(i));
              return (
                <g key={layer.name}>
                  <path d={`M0 ${ROW_Y(i)} C26 ${ROW_Y(i)} 22 56 44 56`} fill="none" stroke="#dfe8ec" strokeWidth="1" />
                  <motion.path
                    d={`M0 ${ROW_Y(i)} C26 ${ROW_Y(i)} 22 56 44 56`}
                    fill="none" stroke="#04d8f2" strokeWidth="1.6" strokeLinecap="round"
                    initial={false} animate={{ pathLength: set ? 1 : 0, opacity: set ? 1 : 0 }}
                    transition={{ duration: 0.6, ease: EASE }}
                  />
                </g>
              );
            })}
          </svg>
          <div className="absolute top-1/2 right-[-12px] -translate-y-1/2">
            <AdamMark lit={joined} size={28} />
          </div>
        </div>
        <div className="relative ml-4 w-[18px] shrink-0">
          <svg className="absolute inset-0 h-full w-full overflow-visible" viewBox="0 0 18 112" preserveAspectRatio="none" aria-hidden="true">
            <motion.path d="M0 56 H18" fill="none" stroke="#0268ce" strokeWidth="2" strokeLinecap="round"
              initial={false} animate={{ pathLength: on(0.7) ? 1 : 0 }} transition={{ duration: 0.5, ease: EASE }} />
          </svg>
        </div>
        <Panel
          className="min-w-0 flex-1"
          lit={active && current >= 0}
          title={joined ? '4 files written' : current >= 0 ? `${shown.name}/${shown.file}` : 'contracts/…'}
          meta={joined ? <Pill tone="ok"><Check size={7} />saved</Pill> : null}
        >
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={joined ? 'all' : current}
              initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }}
              transition={{ duration: 0.22, ease: EASE }}
            >
              <Code className="text-[9px] leading-[15px]">
                {(joined
                  ? LAYERS.map((l) => `+ ${l.name}/${l.file}`)
                  : shown.lines
                ).map((line, k) => (
                  <div key={k} className={`truncate rounded-sm px-1 ${line.startsWith('+') ? 'bg-[#e8f7f0] text-adam-ok' : 'text-adam-muted'}`}>{line}</div>
                ))}
              </Code>
            </motion.div>
          </AnimatePresence>
        </Panel>
      </div>
      <Reveal on={on(0.72)} y={6}>
        <div className="@container flex items-center gap-2 rounded border border-adam-rule bg-adam-raised px-2 py-1">
          <span className="font-mono text-[8.5px] uppercase tracking-wider text-adam-muted">validators</span>
          <span className="font-mono text-[10px] font-medium text-adam-ink">
            {on(0.72) ? <CountUp key={`val-${s.cycle}`} to={9} duration={0.8} /> : 0}/9
          </span>
          <span className="flex gap-[3px]">
            {Array.from({ length: 9 }, (_, k) => (
              <motion.i key={k} className="block size-[6px] rounded-full" initial={false}
                animate={{ backgroundColor: on(0.72 + k * 0.012) ? '#0f9d6e' : '#dfe8ec' }} transition={{ duration: 0.2 }} />
            ))}
          </span>
          {/* Only where the strip has room: in a narrow card it wraps under the dots. */}
          {on(0.84)
            ? <span className="ml-auto hidden text-[9px] font-semibold whitespace-nowrap @min-[330px]:inline"><ShinyText text="no contradictions" color="#0268ce" shineColor="#04d8f2" speed={2.2} /></span>
            : null}
        </div>
      </Reveal>
    </Stage>
  );
}

/* ── 06 Sign-off ──────────────────────────────────────────────────────── */

export function SignOff(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const approved = on(0.54);
  return (
    <Stage state={s.state} className="grid place-items-center">
      <div className="relative">
        <svg className="pointer-events-none absolute -inset-[10px] h-[calc(100%+20px)] w-[calc(100%+20px)] overflow-visible" aria-hidden="true">
          <rect x="1" y="1" width="calc(100% - 2px)" height="calc(100% - 2px)" rx="16" fill="none" stroke="#dfe8ec" strokeWidth="1" />
          <motion.rect
            x="1" y="1" width="calc(100% - 2px)" height="calc(100% - 2px)" rx="16"
            fill="none" stroke="#04d8f2" strokeWidth="2" strokeLinecap="round"
            initial={false} animate={{ pathLength: on(0.06) ? 1 : 0, opacity: on(0.06) ? 1 : 0 }}
            transition={{ duration: 1.1, ease: EASE }}
          />
        </svg>
        <Reveal on={on(0.02)} y={6}>
          <div className="w-[212px] rounded-lg border border-adam-rule bg-white p-2 shadow-[0_2px_10px_rgba(13,35,51,.07)]">
            <div className="flex items-center gap-1.5">
              <span className="grid size-[22px] shrink-0 place-items-center rounded-full bg-gradient-to-br from-adam-deep to-adam-bright font-mono text-[8.5px] font-medium text-white">DL</span>
              <div className="min-w-0">
                <div className="text-[9.5px] font-semibold leading-tight text-adam-ink">Design lead</div>
                <div className="font-mono text-[8px] text-adam-muted">reviewer</div>
              </div>
              <span className="ml-auto">
                {approved
                  ? <Pill tone="solid"><Check size={7} /><ShinyText text="Approved" color="#ffffff" shineColor="#9ee9fb" speed={2.4} /></Pill>
                  : <Pill tone="open">Pending</Pill>}
              </span>
            </div>
            <div className="mt-1.5 flex items-center justify-between rounded border border-adam-rule bg-adam-raised px-1.5 py-1">
              <span className="font-mono text-[8.5px] text-adam-strong">POS-044 · Refund at till</span>
              <span className="font-mono text-[8px] text-adam-muted">v3</span>
            </div>
            <div className="mt-1 flex items-end justify-between">
              <svg width="92" height="24" viewBox="0 0 92 24" aria-hidden="true">
                <motion.path
                  d="M3 17c6-10 10 6 16-3s8-6 10 2 7-9 13-4 6 7 11 1 6-6 10-1 9 3 24-4"
                  fill="none" stroke="#0268ce" strokeWidth="1.5" strokeLinecap="round"
                  initial={false} animate={{ pathLength: on(0.38) ? 1 : 0 }} transition={{ duration: 0.7, ease: EASE }}
                />
              </svg>
              <Reveal on={on(0.62)} y={0} x={6}>
                <span className="flex items-center gap-1 font-mono text-[8px] text-adam-muted">
                  signed 16 Sep · 10:42
                  <span className="grid size-[14px] place-items-center rounded-full bg-adam-deep text-white"><Check size={8} /></span>
                </span>
              </Reveal>
            </div>
          </div>
        </Reveal>
      </div>
    </Stage>
  );
}

/* ── 07 Handoff to engineering ────────────────────────────────────────── */

const SCATTER = [[18, 20], [70, 96], [34, 62], [96, 14], [88, 64]];
const TIDY = [[14, 56], [52, 22], [52, 90], [92, 38], [92, 74]];
const LINKS = [[0, 1], [0, 2], [1, 3], [2, 4], [3, 4]];
const OUTPUTS = ['web', 'api', 'docs'];

export function Handoff(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const tidy = on(0.3);
  const pts = (tidy ? TIDY : SCATTER).map(([x, y]) => ({ x, y }));
  return (
    <Stage state={s.state} className="flex gap-2">
      {/* Dark only once the stage has started: a ghosted dark panel reads as a grey slab. */}
      <Panel className="w-[54%] shrink-0" dark={s.state !== 'pending'} title="assistant · MCP" lit={false} bodyClassName="py-2">
        <Code dark={s.state !== 'pending'} className="text-[9px] leading-[15px]">
          <div className="flex gap-1 whitespace-nowrap">
            <span className="text-[#04d8f2]">$</span>
            {on(0.05)
              ? <TextType key={`t-${s.cycle}`} as="span" text='adam_screen("POS-044")' typingSpeed={38} loop={false} showCursor cursorCharacter="▍" cursorClassName="text-[#04d8f2]" />
              : <span className="text-[#5d7a8c]">_</span>}
          </div>
          {[
            ['operations', 6],
            ['states', 4],
            ['flows', 2],
          ].map(([label, n], k) => (
            <Reveal key={label as string} on={on(0.42 + k * 0.06)} x={-6} y={0} dim={0}>
              <div className="whitespace-nowrap">
                <span className="text-[#5d7a8c]">→ </span>
                <span className="text-[#ffd79a]">{on(0.42 + k * 0.06) ? <CountUp key={`${s.cycle}-${label}`} to={n as number} duration={0.6} /> : 0}</span>
                <span> {label}</span>
              </div>
            </Reveal>
          ))}
          <Reveal on={on(0.62)} x={-6} y={0} dim={0}>
            <div className="whitespace-nowrap"><span className="text-[#5d7a8c]">→ </span>table <span className="text-[#9ee9fb]">order_refund</span></div>
          </Reveal>
        </Code>
      </Panel>
      <div className="relative min-w-0 flex-1">
        <svg className="absolute inset-0 h-full w-full overflow-visible" viewBox="0 0 150 112" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
          {LINKS.map(([a, b], k) => (
            <motion.line key={k} stroke="#0389d7" strokeWidth="1.3" strokeLinecap="round"
              initial={false}
              animate={{ x1: pts[a].x, y1: pts[a].y, x2: pts[b].x, y2: pts[b].y, pathLength: on(0.44) ? 1 : 0.0001, opacity: on(0.44) ? 0.85 : 0.25 }}
              transition={SLOW}
            />
          ))}
          {pts.map((pt, k) => (
            <motion.circle key={k} r="4.2" initial={false}
              animate={{ cx: pt.x, cy: pt.y, fill: on(0.52) ? '#04d8f2' : '#f8fbfc', stroke: on(0.52) ? '#0268ce' : '#9cd9ec' }}
              strokeWidth="1.2" transition={SLOW}
            />
          ))}
          {OUTPUTS.map((name, k) => {
            const y = 22 + k * 34;
            return (
              <g key={name}>
                <motion.path d={`M96 ${k === 0 ? 38 : 74} C112 ${k === 0 ? 38 : 74} 108 ${y} 120 ${y}`} fill="none" stroke="#0389d7" strokeWidth="1"
                  initial={false} animate={{ pathLength: on(0.68 + k * 0.04) ? 1 : 0 }} transition={{ duration: 0.5, ease: EASE }} />
                <motion.g initial={false} animate={{ opacity: on(0.7 + k * 0.04) ? 1 : 0.2 }} transition={SLOW}>
                  <rect x="120" y={y - 9} width="30" height="18" rx="4" fill="#e3f5fb" stroke="#9cd9ec" />
                  <text x="135" y={y + 3} textAnchor="middle" fontFamily="JetBrains Mono, monospace" fontSize="7.5" fill="#0268ce">{name}</text>
                </motion.g>
              </g>
            );
          })}
        </svg>
      </div>
    </Stage>
  );
}
