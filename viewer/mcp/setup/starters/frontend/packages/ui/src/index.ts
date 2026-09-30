/**
 * Shared components for the 13 apps, web (React) and native (React Native).
 *
 * The components themselves arrive with the first screen tickets. What is here now is what they
 * must agree on first: their props, and how a tone and a density turn into a style from
 * `@ticvai/design-tokens`. The style objects use numbers (pixels), which both React's inline
 * styles and React Native's StyleSheet accept, so a web and a native button render the same roles.
 */

import {
  density as densities,
  radius,
  spacing,
  tone as tones,
  typography,
  type Density,
  type Tone,
} from '@ticvai/design-tokens';

/** A token length such as `'12px'` as a number of pixels. */
export function px(value: string): number {
  const n = Number.parseFloat(value);
  if (!Number.isFinite(n)) {
    throw new Error(`Not a pixel length: ${value}`);
  }
  return n;
}

/** Props every interactive control shares. */
export interface ControlProps {
  /** The screen's declared density; it sets the control height and the touch target. */
  density: Density;
  disabled?: boolean;
  /** For tests and accessibility; never shown. */
  testId?: string;
}

export interface ButtonProps extends ControlProps {
  label: string;
  /** A semantic pair. `accentSolid` for the primary action, `dangerSubtle` or `danger` for destructive ones. */
  tone: Tone;
  onPress: () => void;
  /** Why it is disabled, shown to the person (frontend-patterns 4.4: never a silent disabled write). */
  disabledReason?: string;
}

export interface BadgeProps {
  label: string;
  tone: Tone;
}

/** A plain style object both renderers accept. */
export interface BoxStyle {
  backgroundColor: string;
  color: string;
  borderRadius: number;
  fontFamily: string;
  fontSize: number;
  fontWeight: number;
  minHeight: number;
  minWidth: number;
  paddingHorizontal: number;
}

/** The style of a button for its tone and density. The touch target never drops below the density's floor. */
export function buttonStyle(props: Pick<ButtonProps, 'tone' | 'density'>): BoxStyle {
  const pair = tones[props.tone];
  const d = densities[props.density];
  const height = Math.max(px(d.controlHeight), px(d.minTouchTarget));
  return {
    backgroundColor: pair.bg,
    color: pair.text,
    borderRadius: px(radius.medium),
    fontFamily: typography.family.ui,
    fontSize: px(typography.scale[d.baseFont]),
    fontWeight: typography.weight.strong,
    minHeight: height,
    minWidth: px(d.minTouchTarget),
    paddingHorizontal: px(d.controlHeight) / 2,
  };
}

/** The style of a status chip: the micro size and the wide letter spacing the boards use. */
export function badgeStyle(props: BadgeProps): Omit<BoxStyle, 'minHeight' | 'minWidth'> {
  const pair = tones[props.tone];
  return {
    backgroundColor: pair.bg,
    color: pair.text,
    borderRadius: px(radius.sharp),
    fontFamily: typography.family.ui,
    fontSize: px(typography.scale.micro),
    fontWeight: typography.weight.strong,
    paddingHorizontal: px(spacing.xs),
  };
}
