# visual-style.md Format Specification

**Version:** 1.0
**Status:** Draft

## Overview

A `visual-style.md` file is a Markdown document with YAML frontmatter that defines a complete visual design system. The format is designed to be:

- **Human-readable** — Understandable in any text editor
- **AI-consumable** — Every field directly usable by AI models
- **Portable** — Works across any tool that reads the format

## File Structure

```
---
[YAML frontmatter]
---

[Markdown body sections]
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Display name for the style |
| `version` | string | Spec version (currently `1.0`) |
| `style_prompt_short` | string | 1-2 sentence elevator pitch |
| `style_prompt_full` | string | Full natural language generation prompt — **the most important field** |
| `colors.primary` | array | At least 2 colors, each with `name`, `hex`, `role` |

## Optional Fields

### Metadata

| Field | Type | Description |
|-------|------|-------------|
| `tags` | array | Categorical tags (e.g., "iconic design", "retro tech") |
| `author` | string | Credit for the style creator |
| `source_url` | string | URL this style was extracted from |
| `created` | string | ISO date (YYYY-MM-DD) |

### Colors

| Field | Type | Description |
|-------|------|-------------|
| `colors.accent` | array | Accent colors with name/hex/role |
| `colors.neutral` | array | Neutral colors with name/hex/role |

**Color object schema:**
```yaml
- name: "Descriptive Name"
  hex: "#RRGGBB"
  role: "how this color is used in the system"
```

### Typography

| Field | Type | Description |
|-------|------|-------------|
| `typography.display` | object | Display/heading typography |
| `typography.body` | object | Body text typography |
| `typography.caption` | object | Caption/label typography |
| `typography.rules` | array | Typography rules and constraints |

**Typography object schema:**
```yaml
display:
  family: "Font Family Name"
  weight: "bold"
  style: "uppercase, tight tracking"
  size: "48px"
  line_height: "1.1"
  letter_spacing: "-0.02em"
```

| Sub-field | Type | Required | Description |
|-----------|------|----------|-------------|
| `family` | string | yes | Font family name with fallbacks (e.g., `"Inter, system-ui, sans-serif"`) |
| `weight` | string | yes | Font weight — numeric (`"600"`) or named (`"bold"`) |
| `style` | string | yes | Descriptive style notes (case, tracking description, etc.) |
| `size` | string | no | Reference font size with unit (e.g., `"48px"`, `"3rem"`) |
| `line_height` | string | no | Line height as unitless ratio or with unit (e.g., `"1.2"`, `"56px"`) |
| `letter_spacing` | string | no | Letter spacing / tracking (e.g., `"-0.02em"`, `"0.05em"`, `"normal"`) |

**Note:** `size`, `line_height`, and `letter_spacing` capture the actual computed CSS values. These are critical for faithful style reproduction. Extract them from the site's CSS or computed styles, not approximations.

### Imagery

| Field | Type | Description |
|-------|------|-------------|
| `imagery.style` | string | Visual style classification (e.g., `"photographic"`, `"illustrated"`, `"3d-rendered"`, `"sketch"`, `"abstract-geometric"`, `"collage"`, `"pixel-art"`) |
| `imagery.treatment` | string | How images are treated (e.g., `"full-bleed hero photos"`, `"duotone filter"`, `"rounded corners with shadow"`, `"masked into shapes"`) |
| `imagery.subjects` | array | Common subject matter (e.g., `"product screenshots"`, `"lifestyle photography"`, `"abstract patterns"`) |
| `imagery.notes` | array | Additional observations about visual content |

**Imagery example:**
```yaml
imagery:
  style: "photographic with illustrated overlays"
  treatment: "desaturated photos with gradient overlays, rounded 16px corners"
  subjects:
    - "product UI screenshots"
    - "lifestyle team photography"
    - "abstract gradient backgrounds"
  notes:
    - "No stock photos — all custom photography"
    - "Illustrations use brand accent colors only"
```

### Layout

| Field | Type | Description |
|-------|------|-------------|
| `layout.grid` | string | Grid system description |
| `layout.alignment` | string | Alignment approach |
| `layout.aspect_ratio` | string | Default aspect ratio (e.g., "16:9") |
| `layout.notes` | array | Additional layout guidelines |

### Motion

| Field | Type | Description |
|-------|------|-------------|
| `motion.transitions` | array | Transition types used |
| `motion.animation_style` | string | Overall animation approach |
| `motion.pacing` | string | Timing/rhythm description |
| `motion.audio_cues` | array | Sound design notes |

### Mood

| Field | Type | Description |
|-------|------|-------------|
| `mood.keywords` | array | Mood/feeling keywords |
| `mood.era` | string | Time period reference |
| `mood.cultural_reference` | string | Cultural/historical context |
| `mood.avoid` | array | **Anti-patterns** — things to explicitly avoid |

### Assets

| Field | Type | Description |
|-------|------|-------------|
| `assets.reference_images` | array | URLs to reference images |
| `assets.gsep_elements` | array | URLs to overlay/graphic elements |
| `assets.html_snippets` | array | URLs to HTML component examples |
| `assets.color_palette_image` | object | URL to color palette visualization |

**Important:** Assets are always URLs, never embedded binary data.

### Extensions

| Field | Type | Description |
|-------|------|-------------|
| `x_*` | object | Namespaced tool-specific extensions |

Example:
```yaml
x_heygen:
  video_id: "abc123"
  orientation: "landscape"

x_figma:
  library_id: "xyz789"
```

## Markdown Body Sections

After the YAML frontmatter, include these optional Markdown sections:

### `## Connectors`

Tool-specific translation notes:

```markdown
## Connectors

### HeyGen Video Agent
Feed `style_prompt_full` as the visual style block. Use `motion.transitions`
for scene cuts. Orientation: landscape.

### HTML Slides
Map colors to CSS variables. Use `typography.display` for h1-h3.
```

### `## Design Principles`

Freeform design philosophy:

```markdown
## Design Principles

Typography drives hierarchy. Color is used sparingly and intentionally.
Every element snaps to a baseline grid. White space is a feature.
```

### `## Extraction Notes`

Source documentation (when extracted):

```markdown
## Extraction Notes

Extracted from https://example.com on 2026-03-12.
Primary colors sampled from hero section.
Typography identified via browser dev tools.
```

## Complete Example

```yaml
---
name: "Josef Müller-Brockmann Swiss International Style"
version: "1.0"
tags:
  - iconic design
  - sleek minimal
author: "Bin"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  Grid-locked Swiss precision. Black and white base with electric blue
  accent. Helvetica only. Data visualizations as hero elements.

style_prompt_full: >
  Josef Müller-Brockmann Swiss International Style. Grid-locked layouts
  with mathematical precision. Black and white base with ONE accent color
  (electric blue #0066FF). Strong diagonal compositions. Helvetica
  typography only. Data visualizations are the hero — animated charts,
  counters, grids. Every frame snaps to a grid. Transitions are horizontal
  grid wipes. No organic shapes. No gradients. No stock photography.
  Everything is geometric, systematic, precise.

colors:
  primary:
    - name: "Pure Black"
      hex: "#000000"
      role: "dominant ground, text, structural elements"
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "background fields, negative space"
  accent:
    - name: "Electric Blue"
      hex: "#0066FF"
      role: "the ONE accent — data highlights, key emphasis"
  neutral:
    - name: "Grid Gray"
      hex: "#CCCCCC"
      role: "grid lines, secondary structure"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "uppercase or sentence case, tight tracking"
    size: "72px"
    line_height: "1.05"
    letter_spacing: "-0.02em"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "flush left, ragged right, generous leading"
    size: "16px"
    line_height: "1.6"
    letter_spacing: "normal"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "small, uppercase, wide tracking"
    size: "11px"
    line_height: "1.4"
    letter_spacing: "0.1em"
  rules:
    - "Helvetica ONLY — no other typeface"
    - "Type sizes follow a mathematical scale"
    - "Always flush left — never centered"

imagery:
  style: "abstract-geometric"
  treatment: "flat geometric shapes, no photography"
  subjects:
    - "data visualizations"
    - "geometric compositions"
    - "typographic posters"
  notes:
    - "Imagery IS the data — charts, grids, counters"
    - "No photographs or illustrations of people"

layout:
  grid: "Strict modular grid — 12 columns"
  alignment: "Flush left, grid-snapped"
  aspect_ratio: "16:9"
  notes:
    - "Every element locked to the grid"
    - "Data visualizations are the hero elements"

motion:
  transitions:
    - "horizontal grid wipes"
    - "elements snapping to grid positions"
    - "clean hard cuts"
  animation_style: >
    Geometric precision. Elements snap to grid positions.
    Charts animate systematically. Nothing bounces.
  pacing: "Measured, confident, unhurried"

mood:
  keywords:
    - "precise"
    - "systematic"
    - "authoritative"
    - "geometric"
  era: "1950s–1970s (timeless)"
  cultural_reference: "Müller-Brockmann, Grid Systems in Graphic Design"
  avoid:
    - "organic or curved shapes"
    - "gradients"
    - "stock photography"
    - "centered text"
    - "decorative elements"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""
---

## Design Principles

Typography and the grid are the only design elements needed.
Mathematical relationships create visual harmony.
Restraint is the ultimate sophistication.

## Connectors

### HeyGen Video Agent
Use `style_prompt_full` verbatim. No avatar, no b-roll — pure motion graphics.
Hard cuts between scenes.

### HTML Slides
Map to CSS: `--color-bg: #000`, `--color-text: #FFF`, `--color-accent: #0066FF`.
Use Helvetica via system fonts or Google Fonts equivalent.
```

## Validation

A valid `visual-style.md` must have:

1. Valid YAML frontmatter between `---` delimiters
2. All required fields present
3. `colors.primary` with at least 2 color objects
4. Each color object with `name`, `hex`, and `role`
5. `version` set to `1.0`

## Versioning

The `version` field refers to the spec version, not the style version. When the spec changes:

- **Minor changes** (new optional fields): Version stays `1.0`
- **Breaking changes** (required field changes): Version increments to `2.0`

## Design Decisions

### Why `style_prompt_full` is required

Many AI tools only accept a text prompt. By requiring a complete, natural language description of the style, we ensure every `visual-style.md` file is immediately usable by any tool — even ones that don't parse the structured fields.

### Why no embedded binary data

URLs keep files small, versionable, and portable. Binary assets should be hosted externally and referenced by URL.

### Why `x_*` namespacing

Different tools have different capabilities. The `x_` prefix allows tool-specific configuration without polluting the core schema. Examples: `x_heygen`, `x_figma`, `x_paper`.

### Why `mood.avoid`

Negative constraints are as important as positive ones. Telling an AI what NOT to do is often more effective than telling it what to do.
