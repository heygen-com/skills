---
name: visual-style
description: |
  Create, extract, and apply portable visual design systems via visual-style.md files. Use when: (1) Creating a visual-style.md design system from scratch, (2) Extracting a visual style from a website URL, video, or PDF brand guide, (3) Applying a visual style to HeyGen videos, HTML slides, Figma, or paper.design, (4) Browsing the gallery of pre-built visual styles (Swiss, Saul Bass, Game Boy, etc.), (5) User mentions "visual style", "design system", "brand style", or "style guide", (6) Styling a HeyGen video with a consistent design language.
---

# Visual Style

Create, extract, and apply portable visual design systems. A `visual-style.md` file defines colors, typography, layout, motion, and mood in one file that any AI tool can consume.

## Quick Reference

| Mode | Trigger | What it does |
|------|---------|--------------|
| **Create** | "Create a visual-style.md for..." | Build a style from scratch via guided prompts |
| **Extract** | "Extract a visual-style.md from [URL/image/video]" | Analyze a source and generate a style file |
| **Apply** | "Apply this visual-style.md to [tool]" | Use a style with a specific connector |
| **Gallery** | "Show me available visual styles" | Browse and use example styles |

## Default Workflow

### Create

1. **Gather vibe** — Ask about mood, era, references, inspiration
2. **Define colors** — Primary (2+), accent, neutrals with hex values and roles
3. **Set typography** — Display, body, caption families + weight/style rules
4. **Layout & motion** — Grid system, transitions, pacing
5. **Generate** — Output complete `visual-style.md` using [references/templates/minimal.visual-style.md](references/templates/minimal.visual-style.md) or [references/templates/full.visual-style.md](references/templates/full.visual-style.md)
6. **Preview** — Show a small HTML swatch or describe the visual result
7. **Optionally apply** — Ask if user wants to use it with a connector

Questions to batch:
1. What's the vibe? (mood keywords, era, references)
2. Any specific colors? (or derive from the vibe?)
3. Typography preference? (clean, editorial, technical, playful?)
4. What tool will you use this with? (HeyGen, slides, paper.design, Figma?)

### Extract

1. **Receive source** — URL, image, video, or PDF
2. **Load extractor** — Read the appropriate extractor reference file
3. **Extract raw values** — Pull exact CSS hex codes, font-family names, font-size/line-height/letter-spacing values, and CSS custom properties from the source
4. **Analyze deeply** — Map extracted values to colors (background, text, accent, neutral), typography (with precise size/line_height/letter_spacing), imagery style classification, layout, motion, and mood
5. **Generate** — Output complete `visual-style.md` with `source_url` set, exact values, and imagery section
6. **Validate** — Ensure all required fields are present, colors are exact hex from source, and typography includes measured values

### Apply

1. **Read the style** — Load the `visual-style.md` file
2. **Ask which connector** — Or detect from context
3. **Load connector** — Read the appropriate connector reference file
4. **Transform** — Map style fields to tool-specific format
5. **Generate output** — Produce tool-ready instructions or code

### Gallery

1. **List styles** — Show available styles from [references/gallery/](references/gallery/)
2. **Preview** — Describe the selected style's visual character
3. **Load** — Read the full `visual-style.md`
4. **Apply** — Use with a connector

## Format Quick Reference

### Required fields

```yaml
name: "Style Name"
version: "1.0"
style_prompt_short: "1-2 sentence elevator pitch"
style_prompt_full: "Detailed generation prompt — THE most important field"
colors:
  primary:
    - name: "Color Name"
      hex: "#000000"
      role: "how this color is used"
```

**`style_prompt_full` is king.** If a tool can only read one field, it reads this one. Everything else is structured data for tools that want finer control.

Full spec: [references/spec.md](references/spec.md)

## Reference Files

### Connectors (Apply mode)

| Connector | Use case | File |
|-----------|----------|------|
| HeyGen Video Agent | AI video generation | [references/connectors/heygen-video-agent.md](references/connectors/heygen-video-agent.md) |
| HTML Slides | Web presentations | [references/connectors/html-slides.md](references/connectors/html-slides.md) |
| paper.design | Design documents | [references/connectors/paper-design.md](references/connectors/paper-design.md) |
| Figma | Design tool styles | [references/connectors/figma.md](references/connectors/figma.md) |

### Extractors (Extract mode)

| Source | File |
|--------|------|
| Website URL | [references/extractors/from-website.md](references/extractors/from-website.md) |
| Video keyframes | [references/extractors/from-video.md](references/extractors/from-video.md) |
| PDF / Brand guide | [references/extractors/from-pdf.md](references/extractors/from-pdf.md) |

### Gallery (pre-built styles)

| Style | Era | File |
|-------|-----|------|
| Müller-Brockmann Swiss | 1950s–70s | [references/gallery/mueller-brockmann-swiss.visual-style.md](references/gallery/mueller-brockmann-swiss.visual-style.md) |
| Neville Brody Industrial | Late 1980s–90s | [references/gallery/neville-brody-industrial.visual-style.md](references/gallery/neville-brody-industrial.visual-style.md) |
| Saul Bass Cinematic | 1950s–60s | [references/gallery/saul-bass-cinematic.visual-style.md](references/gallery/saul-bass-cinematic.visual-style.md) |
| Game Boy Color | 1998–2003 | [references/gallery/game-boy-color.visual-style.md](references/gallery/game-boy-color.visual-style.md) |
| HeyGen AI Video | 2020s | [references/gallery/heygen-ai-video.visual-style.md](references/gallery/heygen-ai-video.visual-style.md) |

### Templates & Spec

- [references/templates/minimal.visual-style.md](references/templates/minimal.visual-style.md) — Bare minimum template
- [references/templates/full.visual-style.md](references/templates/full.visual-style.md) — Complete template with all fields
- [references/spec.md](references/spec.md) — Full format specification

## Best Practices

1. **`style_prompt_full` is king** — Always usable as a standalone generation prompt
2. **One style, one file** — No multi-style bundling
3. **Assets are URLs** — Never embed binary data
4. **Show, don't tell** — Generate previews when creating styles
5. **Opinionated defaults, flexible extensions** — Core schema is fixed; `x_*` for tool-specific config
