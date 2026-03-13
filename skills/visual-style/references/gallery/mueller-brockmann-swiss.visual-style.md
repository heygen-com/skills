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
  accent. Helvetica only. Data visualizations as hero elements. Every
  frame snaps to a mathematical grid. Geometric, systematic, exact.

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
    - name: "Dark Gray"
      hex: "#333333"
      role: "supporting text, secondary labels"

typography:
  display:
    family: "Helvetica"
    weight: "bold"
    style: "uppercase or sentence case, tight tracking"
  body:
    family: "Helvetica"
    weight: "regular"
    style: "flush left, ragged right, generous leading"
  caption:
    family: "Helvetica"
    weight: "light"
    style: "small, uppercase, wide tracking"
  rules:
    - "Helvetica ONLY — no other typeface"
    - "Type sizes follow a mathematical scale"
    - "Always flush left — never centered"
    - "Weight contrast does the hierarchy"

layout:
  grid: "Strict modular grid — 12 columns"
  alignment: "Flush left, grid-snapped"
  aspect_ratio: "16:9"
  notes:
    - "Every element locked to the grid"
    - "Strong diagonal compositions within orthogonal grid"
    - "Data visualizations are the hero elements"

motion:
  transitions:
    - "horizontal grid wipes"
    - "elements snapping to grid positions"
    - "clean hard cuts"
  animation_style: >
    Geometric precision. Elements snap to grid positions. Charts animate
    systematically. Counters tick mechanically. Nothing bounces.
  pacing: "Measured, confident, unhurried"

mood:
  keywords:
    - "precise"
    - "systematic"
    - "authoritative"
    - "geometric"
  era: "1950s–1970s (timeless)"
  cultural_reference: "Müller-Brockmann, Grid Systems in Graphic Design, Zurich School"
  avoid:
    - "organic or curved shapes"
    - "gradients"
    - "stock photography"
    - "more than one accent color"
    - "centered text"
    - "decorative elements"
    - "handwritten or serif typefaces"
    - "drop shadows or glows"
    - "rounded corners"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  video_id: ""
  orientation: "landscape"
---

## Design Principles

Typography and the grid are the only design elements needed.
Mathematical relationships create visual harmony.
Restraint is the ultimate sophistication.
The grid is not a limitation — it is liberation through structure.

## Connectors

### HeyGen Video Agent
Use `style_prompt_full` verbatim. Specify: No avatar, no b-roll — pure motion graphics.
Hard cuts between scenes. Data visualizations should animate systematically.

### HTML Slides
CSS variables: `--color-bg: #000`, `--color-text: #FFF`, `--color-accent: #0066FF`.
All text flush left. 12-column grid. Helvetica or system sans-serif fallback.

### paper.design
Set up 12-column grid. Background black, text white. Single accent color.
Every element should snap to grid intersections.

### Figma
Color styles: `brand/black`, `brand/white`, `accent/electric-blue`, `neutral/grid-gray`.
Text styles: `heading/display` (Helvetica Bold), `body/default` (Helvetica Regular).
Layout grid: 12 columns, strict alignment.
