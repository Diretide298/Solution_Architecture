/**
 * Journey diagrams 01–04: information enters, gets interpreted, and decisions
 * become structured.
 */
import { motion } from 'motion/react';
import CountUp from '../components/rb/CountUp';
import DecryptedText from '../components/rb/DecryptedText';
import ShinyText from '../components/rb/ShinyText';
import {
  Check, Code, Key, Num, Panel, Pill, QUICK, Reveal, Skeleton, Stage, reached, span,
  type StageProps,
} from './primitives';

/* ── 01 Requirement gathering ─────────────────────────────────────────── */

const FILES: [string, string][] = [['DOC', '312 pp'], ['PDF', '486 pp'], ['PNG', '59 boards'], ['XLS', '201 rows']];
const PACK: [string, number][] = [['modules', 17], ['pages', 1058], ['boards', 59], ['screens', 590]];

export function Gathering(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const parsed = span(s, 0.18, 0.62);
  return (
    <Stage state={s.state} className="flex flex-col">
      <div className="grid grid-cols-4 gap-1">
        {FILES.map(([kind, size], i) => (
          <Reveal key={kind} on={on(0.04 + i * 0.05)} y={5}>
            <div className="rounded border border-adam-rule bg-white px-1 py-[3px] text-center">
              <div className="font-mono text-[8.5px] font-medium text-adam-strong">{kind}</div>
              <div className="truncate font-mono text-[7.5px] text-adam-muted">{size}</div>
            </div>
          </Reveal>
        ))}
      </div>
      <div className="mt-1.5 flex items-center gap-1.5">
        <div className="h-[3px] flex-1 overflow-hidden rounded-full bg-adam-rule">
          <motion.div className="h-full rounded-full bg-gradient-to-r from-adam-deep to-adam-bright" initial={false} animate={{ width: `${parsed * 100}%` }} transition={QUICK} />
        </div>
        <span className="font-mono text-[8px] text-adam-muted">{Math.round(parsed * 100)}%</span>
      </div>
      <Panel
        className="mt-1.5"
        title="sources/workshop/pack.json"
        lit={s.state === 'active'}
        meta={on(0.66) ? <Pill tone="ok"><Check size={7} />parsed</Pill> : <Pill tone="muted">parsing</Pill>}
      >
        <Code>
          <div>{'{'}</div>
          {PACK.map(([key, value], i) => {
            const shown = on(0.28 + i * 0.08);
            return (
              <Reveal key={key} on={shown} x={-6} y={0} dim={0.22}>
                <div className="pl-3">
                  <Key>"{key}"</Key>: <Num>{shown ? <CountUp key={`${s.cycle}-${key}`} to={value} separator="," duration={0.9} /> : 0}</Num>
                  {i < PACK.length - 1 ? ',' : ''}
                </div>
              </Reveal>
            );
          })}
          <div>{'}'}</div>
        </Code>
      </Panel>
    </Stage>
  );
}

/* ── 02 Workshops with the client ─────────────────────────────────────── */

const MINUTES = [0.92, 0.74, 0.86, 0.64, 0.9, 0.7, 0.8];
const MARKS: Record<number, 'accent' | 'open' | 'ok'> = { 1: 'accent', 3: 'open', 5: 'ok' };
const EXTRACTED = [
  { tag: 'DECISION', tone: 'accent' as const, text: 'POS splits by venue' },
  { tag: 'ACTION', tone: 'open' as const, text: 'Draft the refund flow' },
  { tag: 'CONFIRM', tone: 'ok' as const, text: 'Seat hold is 8 min' },
];

export function Workshops(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const filed = on(0.74);
  return (
    <Stage state={s.state} className="flex gap-2">
      <Panel className="w-[40%] shrink-0" title="MoM · 12 Aug" lit={s.state === 'active' && !filed} bodyClassName="flex flex-col gap-[5px] py-2">
        {MINUTES.map((w, i) => {
          const tone = MARKS[i];
          const lit = tone && on(0.1 + i * 0.05);
          return (
            <div key={i} className={`relative flex items-center gap-1 rounded-sm px-0.5 py-[2px] transition-colors duration-300 ${lit ? 'bg-adam-soft' : ''}`}>
              <span className={`h-[7px] w-[2px] shrink-0 rounded-full transition-colors duration-300 ${lit ? (tone === 'open' ? 'bg-adam-warn' : tone === 'ok' ? 'bg-adam-ok' : 'bg-adam-deep') : 'bg-transparent'}`} />
              <Skeleton w={`${w * 100}%`} />
            </div>
          );
        })}
      </Panel>
      <div className="flex min-w-0 flex-1 flex-col gap-1">
        {EXTRACTED.map((item, i) => {
          const recorded = i === 0 && on(0.56);
          return (
            <Reveal key={item.tag} on={on(0.3 + i * 0.08)} x={-10} y={0} rest={filed ? 0.5 : 1}>
              <div className={`flex items-center gap-1 rounded border bg-white px-1 py-[3px] transition-colors duration-300 ${recorded ? 'border-adam-line ring-2 ring-adam-bright/20' : 'border-adam-rule'}`}>
                <Pill tone={item.tone}>{item.tag}</Pill>
                <span className="min-w-0 truncate text-[9px] text-adam-strong">{item.text}</span>
                {recorded ? <Check size={9} className="ml-auto shrink-0 text-adam-deep" /> : null}
              </div>
            </Reveal>
          );
        })}
        <Reveal on={filed} className="mt-auto" y={8}>
          <div className="flex items-center gap-1.5 rounded border border-adam-line bg-adam-soft px-1.5 py-1">
            <span className="font-mono text-[8.5px] text-adam-deep">decisions register</span>
            <span className="ml-auto font-mono text-[9px] font-medium text-adam-ink">
              +{filed ? <CountUp key={`${s.cycle}-reg`} to={3} duration={0.6} /> : 0}
            </span>
          </div>
        </Reveal>
      </div>
    </Stage>
  );
}

/* ── 03 Choosing the strategy ─────────────────────────────────────────── */

const OPTIONS: [string, string][] = [['A', 'One service per contract'], ['B', 'Split on the data boundary'], ['C', 'One shared service']];
const PICK = 1;

export function Strategy(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const chosen = on(0.6);
  // the weighing: a highlight walks the options before one is chosen
  const weighing = s.state === 'active' && s.p >= 0.32 && s.p < 0.6 ? Math.min(2, Math.floor((s.p - 0.32) / 0.093)) : -1;
  return (
    <Stage state={s.state}>
      <Panel
        title={s.state === 'pending' ? 'ADR-0028' : <DecryptedText key={`adr-${s.cycle}`} text="ADR-0028" animateOn="view" sequential speed={40} />}
        lit={s.state === 'active'}
        meta={on(0.72)
          ? <Pill tone="solid"><ShinyText text="Accepted" color="#ffffff" shineColor="#9ee9fb" speed={2.4} /></Pill>
          : <Pill tone="open">Proposed</Pill>}
        bodyClassName="flex flex-col gap-1"
      >
        <Reveal on={on(0.04)} y={4}>
          <div className="text-[10.5px] font-semibold leading-tight text-adam-ink">Service decomposition</div>
        </Reveal>
        {OPTIONS.map(([id, text], i) => {
          const isPick = i === PICK;
          const ruledOut = chosen && !isPick;
          return (
            <Reveal key={id} on={on(0.1 + i * 0.07)} x={-8} y={0} rest={ruledOut ? 0.42 : 1}>
              <div className={`flex items-center gap-1.5 rounded border px-1.5 py-[3px] transition-colors duration-300 ${
                chosen && isPick ? 'border-adam-line bg-adam-soft' : weighing === i ? 'border-adam-rule bg-adam-raised' : 'border-adam-rule bg-white'
              }`}>
                <span className={`grid size-[11px] shrink-0 place-items-center rounded-full border transition-colors duration-300 ${chosen && isPick ? 'border-adam-deep bg-adam-deep text-white' : 'border-[#c7d5db] bg-white'}`}>
                  {chosen && isPick ? <Check size={7} /> : null}
                </span>
                <span className="font-mono text-[8.5px] text-adam-muted">{id}</span>
                <span className={`min-w-0 truncate text-[9px] ${ruledOut ? 'text-adam-muted line-through' : 'text-adam-strong'}`}>{text}</span>
              </div>
            </Reveal>
          );
        })}
        <Reveal on={on(0.78)} y={4}>
          <div className="flex items-center gap-1 pt-0.5">
            <span className="font-mono text-[8px] uppercase tracking-wider text-adam-muted">rules out</span>
            <Pill tone="muted">cross-schema writes</Pill>
          </div>
        </Reveal>
      </Panel>
    </Stage>
  );
}

/* ── 04 Finalising it ─────────────────────────────────────────────────── */

const CONFLICTS: [string, string][] = [
  ['C-031', 'Does this deserve a table?'],
  ['C-032', 'Who owns a refund?'],
  ['C-033', 'How long is a seat held?'],
  ['C-034', 'Is tax set per venue?'],
];
const ANSWER_AT = [0.28, 0.41, 0.54, 0.72];

export function Finalising(s: StageProps) {
  const on = (t: number) => reached(s, t);
  const open = ANSWER_AT.filter((t) => !on(t)).length;
  return (
    <Stage state={s.state}>
      <Panel
        title="docs/registers/conflicts.md"
        lit={s.state === 'active'}
        meta={<Pill tone={open ? 'open' : 'ok'}>{open ? `${open} open` : <><Check size={7} />closed</>}</Pill>}
        bodyClassName="flex flex-col gap-1"
      >
        {CONFLICTS.map(([id, question], i) => {
          const answered = on(ANSWER_AT[i]);
          const last = i === CONFLICTS.length - 1;
          return (
            <Reveal key={id} on={on(0.04 + i * 0.05)} y={4} rest={answered && !last ? 0.55 : 1}>
              <motion.div
                className={`flex items-center gap-1.5 rounded border px-1.5 py-[3px] transition-colors duration-300 ${answered && last ? 'border-adam-line bg-adam-soft' : 'border-adam-rule bg-white'}`}
                initial={false}
                animate={{ x: answered && !last ? 4 : 0 }}
                transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
              >
                <span className="font-mono text-[8px] text-adam-muted">{id}</span>
                <span className={`min-w-0 flex-1 truncate text-[9px] ${answered && !last ? 'text-adam-muted' : 'text-adam-strong'}`}>{question}</span>
                {!answered ? <Pill tone="open">open</Pill>
                  : last ? <Pill tone="solid"><Check size={7} />confirmed</Pill>
                    : <Pill tone="ok">answered</Pill>}
              </motion.div>
            </Reveal>
          );
        })}
      </Panel>
    </Stage>
  );
}
