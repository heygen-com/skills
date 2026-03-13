# Figma Connector

Apply a `visual-style.md` to generate Figma styles and components.

## Overview

This connector maps `visual-style.md` fields to Figma's style system: color styles, text styles, effect styles, and layout grids.

## Field Mapping

| visual-style.md field | Figma output |
|-----------------------|--------------|
| `colors.primary` | Color styles (`brand/primary`, `brand/secondary`) |
| `colors.accent` | Color styles (`accent/primary`, `accent/secondary`) |
| `colors.neutral` | Color styles (`neutral/100`, `neutral/200`, etc.) |
| `typography.display` | Text style (`heading/display`) |
| `typography.body` | Text style (`body/default`, `body/large`) |
| `typography.caption` | Text style (`label/default`, `label/small`) |
| `typography.rules` | Design review checklist |
| `layout.grid` | Layout grid preset |
| `layout.aspect_ratio` | Frame dimensions |
| `mood.avoid` | Design review checklist |
| `assets.reference_images` | Style guide frame |

## Color Styles

Generate Figma color styles from the `colors` object:

```
Folder: brand/
  - brand/black         → colors.primary[0].hex
  - brand/white         → colors.primary[1].hex

Folder: accent/
  - accent/primary      → colors.accent[0].hex
  - accent/secondary    → colors.accent[1].hex (if exists)

Folder: neutral/
  - neutral/light       → colors.neutral[0].hex
  - neutral/dark        → colors.neutral[1].hex
```

**Naming convention:** Use the `role` field for style descriptions.

## Text Styles

Generate Figma text styles from `typography`:

```
Folder: heading/
  - heading/display
    Font: typography.display.family
    Weight: typography.display.weight
    Size: 48px (or derive from style)

Folder: body/
  - body/default
    Font: typography.body.family
    Weight: typography.body.weight
    Size: 16px

Folder: label/
  - label/default
    Font: typography.caption.family
    Weight: typography.caption.weight
    Size: 12px
```

## Layout Grids

Generate layout grid presets from `layout.grid`:

```
"12 columns" →
  Columns: 12
  Type: Stretch
  Margin: 64px
  Gutter: 24px

"8-point grid" →
  Rows: Count
  Height: 8px

"Strict modular grid" →
  Both columns AND rows enabled
```

## Style Guide Frame

Create a style guide frame that documents the system:

```
┌─────────────────────────────────────────────────────┐
│  [name]                                             │
│  [style_prompt_short]                               │
├─────────────────────────────────────────────────────┤
│  COLORS                                             │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                │
│  │████│ │████│ │████│ │████│ │████│                │
│  └────┘ └────┘ └────┘ └────┘ └────┘                │
│  Primary  Secondary  Accent   Neutral              │
├─────────────────────────────────────────────────────┤
│  TYPOGRAPHY                                         │
│                                                     │
│  Display Heading                                    │
│  [typography.display.family] [weight]               │
│                                                     │
│  Body text paragraph                                │
│  [typography.body.family] [weight]                  │
│                                                     │
│  CAPTION / LABEL                                    │
│  [typography.caption.family] [weight]               │
├─────────────────────────────────────────────────────┤
│  RULES                                              │
│  ✓ [typography.rules[0]]                           │
│  ✓ [typography.rules[1]]                           │
│                                                     │
│  AVOID                                              │
│  ✗ [mood.avoid[0]]                                 │
│  ✗ [mood.avoid[1]]                                 │
└─────────────────────────────────────────────────────┘
```

## Workflow

1. **Read the style** — Load the `visual-style.md` file
2. **Create color styles** — One style per color in the palette
3. **Create text styles** — Display, body, and caption styles
4. **Set up layout grid** — Create grid presets
5. **Build style guide frame** — Document the system
6. **Add reference images** — Import `assets.reference_images` if available

## Figma Plugin Integration

If building a Figma plugin that reads `visual-style.md`:

```typescript
interface VisualStyle {
  name: string;
  version: string;
  style_prompt_short: string;
  style_prompt_full: string;
  colors: {
    primary: Color[];
    accent?: Color[];
    neutral?: Color[];
  };
  typography: {
    display: TypographyStyle;
    body: TypographyStyle;
    caption: TypographyStyle;
    rules?: string[];
  };
  // ... other fields
}

interface Color {
  name: string;
  hex: string;
  role: string;
}

interface TypographyStyle {
  family: string;
  weight: string;
  style?: string;
}
```

## Tips

- **Font availability** — Check that `typography.*.family` fonts are available in Figma (Google Fonts or locally installed)
- **Color organization** — Use folders to group color styles by purpose
- **Style descriptions** — Use the `role` field as the style description
- **Design review** — Create a checklist from `typography.rules` and `mood.avoid`
