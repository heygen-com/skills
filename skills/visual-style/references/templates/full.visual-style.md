---
name: "Style Name"
version: "1.0"
tags:
  - tag1
  - tag2
author: "Your Name"
source_url: ""
created: "YYYY-MM-DD"

style_prompt_short: >
  One to two sentences capturing the visual essence of this style.
  This is the elevator pitch.

style_prompt_full: >
  Detailed generation prompt. Include specific hex colors, font names,
  layout structure, motion patterns, and overall mood. This is THE most
  important field — any AI tool should be able to read this and generate
  consistent visuals. Be specific about what TO do and what NOT to do.
  Include hex codes inline (like #FF5500) so tools can extract them.

colors:
  primary:
    - name: "Descriptive Color Name"
      hex: "#000000"
      role: "dominant background, structural elements"
    - name: "Descriptive Color Name"
      hex: "#FFFFFF"
      role: "primary text, negative space"
  accent:
    - name: "Accent Color Name"
      hex: "#FF5500"
      role: "CTAs, emphasis, key highlights"
  neutral:
    - name: "Neutral Color Name"
      hex: "#888888"
      role: "supporting text, borders, secondary elements"

typography:
  display:
    family: "Font Family Name"
    weight: "bold"
    style: "uppercase, tight tracking"
    size: "48px"
    line_height: "1.1"
    letter_spacing: "-0.02em"
  body:
    family: "Font Family Name"
    weight: "regular"
    style: "sentence case, comfortable line height"
    size: "16px"
    line_height: "1.6"
    letter_spacing: "normal"
  caption:
    family: "Font Family Name"
    weight: "medium"
    style: "small, uppercase for labels"
    size: "12px"
    line_height: "1.4"
    letter_spacing: "0.05em"
  rules:
    - "Type scale: 48px → 32px → 24px → 16px → 12px"
    - "Typography rule or constraint"
    - "Font usage restriction"

imagery:
  style: "photographic | illustrated | 3d-rendered | sketch | abstract-geometric | collage | icon-driven"
  treatment: "how images are cropped, filtered, masked, or framed"
  subjects:
    - "common subject matter"
    - "another subject type"
  notes:
    - "observation about visual content"
    - "what imagery is deliberately absent"

layout:
  grid: "Grid system description (e.g., 12 columns, 8px base unit)"
  alignment: "Alignment approach (e.g., flush left, centered hero)"
  aspect_ratio: "Default aspect ratio (e.g., 16:9, 4:3)"
  notes:
    - "Additional layout guideline"
    - "Spacing or composition note"

motion:
  transitions:
    - "transition type 1"
    - "transition type 2"
  animation_style: >
    Description of how elements move and animate. Include easing,
    timing, and overall feel.
  pacing: "Overall rhythm description"
  audio_cues:
    - "sound design note"

mood:
  keywords:
    - "mood word 1"
    - "mood word 2"
    - "mood word 3"
    - "mood word 4"
  era: "Time period reference (e.g., 1990s, contemporary)"
  cultural_reference: "Designers, movements, or works that inspire this style"
  avoid:
    - "thing to explicitly avoid"
    - "another anti-pattern"
    - "design element that doesn't fit"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: ""
  orientation: "landscape"

x_figma:
  library_id: ""
---

## Design Principles

Freeform section for design philosophy and guiding principles.
What beliefs drive this visual system?
What trade-offs does it make intentionally?

## Connectors

### HeyGen Video Agent
Notes on how to apply this style to HeyGen Video Agent.
What to emphasize in the prompt, what motion patterns to use.

### HTML Slides
Notes on CSS mapping, layout approach, font loading.

### paper.design
Notes on document setup, grid configuration, AI guidance.

### Figma
Notes on style generation, component patterns, design tokens.

## Extraction Notes

If this style was extracted from a source, document it here.
Include the source URL, extraction date, and any notable decisions.
