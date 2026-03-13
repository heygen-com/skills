---
name: "Game Boy Color"
version: "1.0"
tags:
  - pixel retro
  - gaming
author: "Visual Style Gallery"
created: "2026-03-12"

style_prompt_short: >
  Late 90s handheld gaming nostalgia. Limited color palette,
  chunky pixels, portable adventures in your pocket.

style_prompt_full: >
  Game Boy Color aesthetic from the late 1990s. Limited color palette
  per scene (originally 56 colors, often using 4-10 per sprite).
  Characteristic GBC colors: that specific teal-green (#0F380F to
  #9BBC0F gradient), purple shell (#663399), berry (#CC3366), teal
  (#339999), atomic purple (#6B3FA0). Chunky pixel graphics at low
  resolution (160x144 native). Dithering patterns for shading.
  Simple sprite animations at low frame rates (10-15fps). UI elements
  have that distinctive GBC border style. Sound design would be
  chiptune — 4-channel audio aesthetic. Portable, colorful, charming.
  Not as limited as original Game Boy, but still clearly constrained.
  Pokemon Crystal, Link's Awakening DX, Wario Land 3 as references.

colors:
  primary:
    - name: "GBC Dark Green"
      hex: "#0F380F"
      role: "darkest tone, outlines"
    - name: "GBC Light Green"
      hex: "#9BBC0F"
      role: "lightest tone, highlights"
  accent:
    - name: "GBC Purple"
      hex: "#663399"
      role: "original shell color, brand accent"
    - name: "Berry Pink"
      hex: "#CC3366"
      role: "berry shell variant"
    - name: "Teal"
      hex: "#339999"
      role: "teal shell variant"
    - name: "Atomic Purple"
      hex: "#6B3FA0"
      role: "atomic purple shell, special emphasis"
  neutral:
    - name: "GBC Mid Green"
      hex: "#306230"
      role: "mid-tone, secondary elements"
    - name: "GBC Pale Green"
      hex: "#8BAC0F"
      role: "light mid-tone"

typography:
  display:
    family: "Pixel font (8x8 or 16x16)"
    weight: "regular (pixels are pixels)"
    style: "uppercase or mixed, chunky"
  body:
    family: "Pixel font"
    weight: "regular"
    style: "dialogue box style"
  caption:
    family: "Pixel font"
    weight: "regular"
    style: "small, menu text"
  rules:
    - "All text must be pixel-perfect"
    - "Limited character sets (like actual GBC)"
    - "Text boxes with characteristic borders"
    - "Text reveals character by character"

layout:
  grid: "8-pixel base unit"
  alignment: "Centered menus, left-aligned dialogue"
  aspect_ratio: "10:9 (GBC native) or 16:9 (modern)"
  notes:
    - "160x144 native resolution, scale up evenly"
    - "HUD elements at screen edges"
    - "Dialogue boxes at bottom third"
    - "Sprite-based compositions"

motion:
  transitions:
    - "screen wipes (iris, horizontal, vertical)"
    - "palette fade (to white or black)"
    - "no smooth transitions"
  animation_style: >
    Low frame rate sprite animation (10-15fps). Two-frame walk cycles.
    Screen transitions are instant or use classic wipes.
    UI elements appear and disappear, don't fade.
  pacing: "Quick, responsive, game-like"
  audio_cues:
    - "chiptune"
    - "4-channel audio"
    - "8-bit sound effects"
    - "menu blips and bloops"

mood:
  keywords:
    - "nostalgic"
    - "portable"
    - "colorful"
    - "charming"
    - "playful"
    - "adventure"
  era: "1998-2003"
  cultural_reference: "Pokemon Crystal, Link's Awakening DX, Wario Land 3, Game Boy Color hardware"
  avoid:
    - "smooth gradients"
    - "high resolution graphics"
    - "photorealistic elements"
    - "modern UI patterns"
    - "more than 56 colors total"
    - "smooth animations"
    - "anti-aliasing"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: "94e43f67cbe546b783e1f5c6f2b66125"
  orientation: "landscape"
---

## Design Principles

Constraints breed creativity.
Every pixel counts when you only have 160x144.
Color is precious — use it intentionally.
Charm comes from character, not complexity.

## Connectors

### HeyGen Video Agent
Use `style_prompt_full` verbatim. Emphasize: chunky pixels, limited colors,
low frame rate animations. Screen wipe transitions. Chiptune audio aesthetic.
No smooth movements — everything is discrete pixel steps.

### HTML Slides
Use pixel fonts (Press Start 2P, VT323). Scale graphics at integer multiples
only (2x, 3x, 4x) to maintain pixel crispness. GBC green palette as default,
shell colors for accents. Dialogue box borders.

### paper.design
Design at low resolution, scale up. Use GBC color palette.
Dithering patterns for shading. Sprite-based compositions.
8-pixel grid for all elements.

### Figma
Color styles: `gbc/dark-green`, `gbc/mid-green`, `gbc/pale-green`, `gbc/light-green`,
plus shell color variants. 8x8 pixel grid. Use pixel fonts or
design custom pixel type. No anti-aliasing on exports.
