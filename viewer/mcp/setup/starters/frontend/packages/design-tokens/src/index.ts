/**
 * TICVAI design tokens, from the package's `screens/_design-tokens.yaml` (extracted 9 September
 * 2026 from Claude Design's boards and the client's own POS design, which agree). Regenerate from
 * that file; do not edit values here by hand.
 *
 * Colour is named by role, never by hex. The semantic pairs are a background and the text that
 * sits on it, chosen together: keep them paired. A tenant may override only `whiteLabel.overridable`.
 *
 * Depends on nothing (the lint rules keep it a leaf).
 */

export const typography = {
  family: {
    ui: 'Manrope, system-ui, sans-serif',
    mono: "'IBM Plex Mono', ui-monospace, monospace",
  },
  scale: {
    micro: '9.5px',
    small: '10px',
    body: '11px',
    bodyLarge: '11.5px',
    label: '12px',
    subheading: '12.5px',
    heading: '13px',
    title: '16.5px',
  },
  weight: {
    regular: 400,
    medium: 600,
    strong: 700,
    heavy: 800,
  },
  letterSpacing: {
    tight: '-.015em',
    wide: '.07em',
    wider: '.15em',
  },
} as const;

/** Surfaces, text and lines, by role. */
export const colour = {
  ground: '#F7F9FC',
  surface: '#FAFBFD',
  surfaceSunken: '#F2F5F9',
  surfaceRaised: '#FFFFFF',
  groundDark: '#0B1324',
  surfaceDark: '#171B22',
  surfaceDarkAlt: '#0F1E33',
  borderDark: '#262C36',
  textBody: '#5A6577',
  textStrong: '#4A5566',
  textMuted: '#8494A8',
  textFaint: '#9FB6CF',
  textOnDark: '#E8ECF2',
  textOnDarkMuted: '#C4CCD8',
  hairline: '#E8ECF3',
  border: '#E3E8F0',
  borderStrong: '#DCE3ED',
  warningBorder: '#F0DFB8',
  dangerBorder: '#F5C9C9',
  successBorder: '#C7E4DF',
} as const;

/** Background and text pairs. They must stay paired: the contrast was chosen together. */
export const tone = {
  accent: {
    bg: '#EDF3FF',
    text: '#0A4FB8',
  },
  accentAlt: {
    bg: '#EAF4FF',
    text: '#0A4FB8',
  },
  accentSolid: {
    bg: '#0D6EFD',
    text: '#FFFFFF',
  },
  success: {
    bg: '#E7F4F2',
    text: '#0B5B41',
  },
  successSolid: {
    bg: '#0E6B62',
    text: '#FFFFFF',
  },
  warning: {
    bg: '#FFF7E6',
    text: '#8A6D00',
  },
  warningAlt: {
    bg: '#FFF7E6',
    text: '#7A5F14',
  },
  caution: {
    bg: '#FFF1E6',
    text: '#9A5B00',
  },
  danger: {
    bg: '#FDEDED',
    text: '#8A2020',
  },
  dangerSubtle: {
    bg: '#FEF7F7',
    text: '#8A2020',
  },
  neutral: {
    bg: '#F7F9FC',
    text: '#5A6577',
  },
  neutralSunken: {
    bg: '#F2F5F9',
    text: '#5A6577',
  },
  onDark: {
    bg: '#0E1116',
    text: '#E8ECF2',
  },
} as const;

export type Tone = keyof typeof tone;

export const radius = {
  sharp: '5px',
  small: '9px',
  medium: '10px',
  large: '12px',
  xlarge: '16px',
} as const;

/** A 3px base, as the sources use; not a 4 or 8 grid. */
export const spacing = {
  xxs: '3px',
  xs: '6px',
  sm: '9px',
  md: '13px',
  lg: '18px',
  xl: '28px',
  xxl: '46px',
} as const;

/**
 * Density is hardware, not taste: every screen declares one. `touchLarge` controls clear 44px,
 * the floor for a gloved finger on a wet POS screen.
 */
export const density = {
  compact: {
    baseFont: 'body',
    rowHeight: '28px',
    controlHeight: '28px',
    gap: 'sm',
    minTouchTarget: '24px',
  },
  comfortable: {
    baseFont: 'bodyLarge',
    rowHeight: '36px',
    controlHeight: '34px',
    gap: 'md',
    minTouchTarget: '32px',
  },
  touchLarge: {
    baseFont: 'heading',
    rowHeight: '56px',
    controlHeight: '52px',
    gap: 'lg',
    minTouchTarget: '44px',
  },
} as const;

export type Density = keyof typeof density;

export const elevation = {
  flat: 'none',
  raised: '0 1px 2px rgba(11,19,36,.06)',
  overlay: '0 8px 28px rgba(11,19,36,.18)',
  scrim: 'rgba(11,19,36,.42)',
} as const;

export const overlay = {
  confirmDialog: {
    width: '420px',
    radius: 'large',
    elevation: 'overlay',
  },
  modal: {
    width: '640px',
    radius: 'large',
    elevation: 'overlay',
  },
  drawer: {
    width: '480px',
    radius: 'large',
    elevation: 'overlay',
    edge: 'right',
  },
  sheet: {
    height: '60%',
    radius: 'large',
    elevation: 'overlay',
    edge: 'bottom',
  },
  toast: {
    width: '360px',
    radius: 'medium',
    elevation: 'raised',
    edge: 'bottom',
  },
} as const;

/** What a tenant's brand may replace. Semantic pairs are never overridable. */
export const whiteLabel = {
  overridable: ['accentSolid', 'surfaceRaised', 'typography.family.ui'],
  fixedFooterCredit: true,
} as const;

export const tokens = { typography, colour, tone, radius, spacing, density, elevation, overlay, whiteLabel } as const;

export type Tokens = typeof tokens;
