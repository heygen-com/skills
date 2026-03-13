# Extract from PDF / Brand Guide

Generate a `visual-style.md` from a PDF brand guide or style document.

## Workflow

1. **Receive PDF** — User uploads a brand guide, style guide, or design document
2. **Parse sections** — Identify color, typography, layout, and guidelines sections
3. **Map to fields** — Translate brand guide specifications to visual-style.md fields
4. **Fill gaps** — Generate `style_prompt_full` from the structured data
5. **Output** — Complete `visual-style.md`
6. **Validate** — Ensure all required fields are present

## Common Brand Guide Sections

| Brand Guide Section | Maps To |
|--------------------|---------|
| Brand Overview / Mission | `style_prompt_short`, `mood.keywords` |
| Color Palette | `colors.*` |
| Primary Colors | `colors.primary` |
| Secondary/Accent Colors | `colors.accent` |
| Typography | `typography.*` |
| Headlines | `typography.display` |
| Body Copy | `typography.body` |
| Grid System | `layout.grid` |
| Spacing | `layout.notes` |
| Do's and Don'ts | `typography.rules`, `mood.avoid` |
| Voice & Tone | `mood.keywords`, `style_prompt_full` |
| Photography Style | `mood.keywords`, `mood.avoid` |
| Iconography | `style_prompt_full` |

## Extraction Prompt

Use this prompt when parsing a brand guide PDF:

```
Parse this brand guide PDF and generate a visual-style.md.

Map the brand guide sections to visual-style.md fields:

REQUIRED:
- name: Brand name + "Brand Style"
- version: "1.0"
- style_prompt_short: Synthesize from brand overview/mission
- style_prompt_full: Combine ALL visual specifications into a coherent
  generation prompt. Include specific hex codes, font names, spacing
  values, and design principles.
- colors.primary: From "Primary Colors" section

FROM COLOR SECTIONS:
- colors.primary: Primary palette (convert all color specs to hex)
- colors.accent: Secondary/accent colors
- colors.neutral: Grays, backgrounds, supporting colors

FROM TYPOGRAPHY SECTIONS:
- typography.display: Headline font specs
- typography.body: Body copy font specs
- typography.caption: Caption/label specs (if defined)
- typography.rules: Any typography guidelines or restrictions

FROM LAYOUT SECTIONS:
- layout.grid: Grid system specifications
- layout.alignment: Alignment rules
- layout.notes: Spacing, margins, padding guidelines

FROM GUIDELINES SECTIONS:
- mood.keywords: Extract from voice/tone/personality sections
- mood.avoid: Extract from "Don't" lists, incorrect usage examples

Be precise:
- Convert all color specifications to hex (RGB, CMYK, Pantone → hex)
- Use exact font family names as specified
- Include specific measurements where given
- Preserve the brand's stated values in style_prompt_full

Output format:
Complete YAML frontmatter between --- delimiters
Plus Markdown body sections (## Design Principles from brand philosophy)
```

## Color Conversion Reference

Brand guides often specify colors in multiple formats:

| Format | Example | Hex Conversion |
|--------|---------|----------------|
| Hex | #FF5500 | Use directly |
| RGB | 255, 85, 0 | → #FF5500 |
| CMYK | 0, 67, 100, 0 | Approximate to hex |
| Pantone | PMS 021 C | Look up hex equivalent |
| HSL | 20°, 100%, 50% | Convert to hex |

For Pantone colors, use the official Pantone-to-hex mapping or note the Pantone code in the `role` field.

## Example Output

Given a corporate brand guide PDF:

```yaml
---
name: "Acme Corp Brand Style"
version: "1.0"
tags:
  - corporate
  - technology
author: "Extracted from Acme Brand Guidelines v2.3"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  Professional tech brand with bold blue accents.
  Clean, trustworthy, forward-thinking.

style_prompt_full: >
  Acme Corp brand style. Professional technology company aesthetic.
  Primary blue (#0052CC) for brand elements, CTAs, and emphasis.
  Navy (#172B4D) for headings and high-contrast text. Clean white
  (#FFFFFF) backgrounds with generous whitespace. Neutral grays
  for supporting content. Typography uses Roboto for digital
  and Avenir for print — clean, geometric sans-serifs that convey
  precision. 8-point spacing grid. Rounded corners (4px) on
  interactive elements. Photography should be authentic, diverse,
  and optimistic — no stock photo clichés. Iconography is outlined,
  2px stroke, rounded caps. Professional but approachable. Never
  corporate-stuffy or overly playful.

colors:
  primary:
    - name: "Acme Blue"
      hex: "#0052CC"
      role: "primary brand color, CTAs, links"
    - name: "Navy"
      hex: "#172B4D"
      role: "headings, high-contrast text"
  accent:
    - name: "Success Green"
      hex: "#36B37E"
      role: "positive states, confirmations"
    - name: "Warning Yellow"
      hex: "#FFAB00"
      role: "warnings, attention"
    - name: "Error Red"
      hex: "#DE350B"
      role: "errors, destructive actions"
  neutral:
    - name: "White"
      hex: "#FFFFFF"
      role: "primary background"
    - name: "Light Gray"
      hex: "#F4F5F7"
      role: "secondary backgrounds, cards"
    - name: "Mid Gray"
      hex: "#6B778C"
      role: "secondary text, placeholders"
    - name: "Dark Gray"
      hex: "#42526E"
      role: "body text"

typography:
  display:
    family: "Roboto"
    weight: "700"
    style: "sentence case, -0.02em tracking"
  body:
    family: "Roboto"
    weight: "400"
    style: "16px base, 1.5 line height"
  caption:
    family: "Roboto"
    weight: "500"
    style: "12px, uppercase for labels"
  rules:
    - "Roboto for all digital applications"
    - "Avenir for print materials"
    - "Minimum body text size: 14px"
    - "Maximum line length: 75 characters"
    - "Use Medium (500) weight for emphasis, not bold"

layout:
  grid: "8-point grid, 12 columns"
  alignment: "Left-aligned text, center-aligned hero content"
  aspect_ratio: "16:9 for presentations"
  notes:
    - "Minimum margin: 24px (mobile), 48px (desktop)"
    - "Standard spacing: 8, 16, 24, 32, 48, 64px"
    - "Card border-radius: 4px"
    - "Button border-radius: 4px"

motion:
  transitions:
    - "ease-out, 200ms for micro-interactions"
    - "ease-in-out, 300ms for page transitions"
  animation_style: "Subtle, purposeful. Animation should clarify, not decorate."
  pacing: "Quick, responsive feedback"

mood:
  keywords:
    - "professional"
    - "trustworthy"
    - "innovative"
    - "approachable"
    - "precise"
  era: "Contemporary tech (2020s)"
  cultural_reference: "Enterprise SaaS, developer tools"
  avoid:
    - "overly playful or casual tone"
    - "generic stock photography"
    - "gradients on brand elements"
    - "more than 3 colors in one composition"
    - "centered body text"
    - "all-caps body text"
    - "drop shadows deeper than 2px"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

From Acme Brand Guidelines:

1. **Clarity over cleverness** — Communication should be immediately understood
2. **Consistency builds trust** — Every touchpoint reinforces the brand
3. **Purposeful restraint** — Add only what adds value
4. **Accessible by default** — Design for everyone

## Extraction Notes

Extracted from "Acme Brand Guidelines v2.3" (PDF, 48 pages).
Color values converted from Pantone specifications.
Typography mapped from "Digital Standards" section.
Do's and Don'ts synthesized into mood.avoid list.
```

## Tips

- **Prioritize specificity** — Brand guides are precise; preserve exact values
- **Don't invent** — If a section isn't in the PDF, leave the field empty
- **Synthesize style_prompt_full** — This should read like a brief you'd give a designer
- **Capture the don'ts** — `mood.avoid` is often explicitly stated in brand guides
- **Note the source** — Include page numbers or section names in Extraction Notes
