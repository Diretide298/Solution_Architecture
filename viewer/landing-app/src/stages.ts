export type { StageProps, StageState } from './stages/primitives';
import { Finalising, Gathering, Strategy, Workshops } from './stages/early';
import { Handoff, SignOff, Updating } from './stages/late';

/** One diagram per journey card, in card order. */
export const STAGES = [Gathering, Workshops, Strategy, Finalising, Updating, SignOff, Handoff];
