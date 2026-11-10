// Desktop's main.css tokens per scheme.
export type MobileColorScheme = 'light' | 'dark'

const darkColors = {
  // --background, --sidebar
  bgBase: '#0a0a0a',
  bgPanel: '#171717',
  borderSubtle: 'rgba(255, 255, 255, 0.07)',
  textPrimary: '#fafafa'
}

const lightColors: MobilePalette = {
  bgBase: '#ffffff',
  bgPanel: '#fafafa',
  borderSubtle: '#e5e5e5',
  textPrimary: '#0a0a0a'
}

export const spacing = {
  xs: 4,
  sm: 8
} as const

export const radii = {
  /** Everything you tap. */
  control: 12,
  pill: 999
} as const

export const typography = {
  titleSize: 18,
  bodySize: 14,
  monoFamily: 'monospace' as const
} as const
