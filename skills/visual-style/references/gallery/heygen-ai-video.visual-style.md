---
name: "HeyGen AI Video Platform"
version: "1.0"
tags:
  - ai
  - video
  - tech
  - modern
author: "Extracted"
source_url: "https://heygen.com"
created: "2026-03-12"

style_prompt_short: >
  Vibrant AI-forward design. Cyan-to-pink gradient energy on clean white.
  Approachable tech that feels premium without being cold.

style_prompt_full: >
  Modern AI video platform aesthetic inspired by HeyGen. Clean white
  backgrounds with generous whitespace. Signature cyan-pink gradient
  (#00C3FF to #95AAFE to #FEA5FE) as the hero visual element. Primary
  accent is Hey Blue (#00C3FF) for CTAs and interactive elements. Prism
  Pink (#F3A6FF) as secondary accent for emphasis and warmth. Typography
  uses geometric sans-serifs (ABC Solar, TT Norms Pro, or similar) with
  clear hierarchy. Large rounded corners (12-48px) on cards and buttons.
  Smooth fade-in animations and subtle hover transitions. Tech-forward
  but approachable — innovation meets accessibility. Avoid harsh corporate
  blue, avoid dark mode unless specifically requested, avoid overly
  complex gradients or 3D effects.

colors:
  primary:
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "primary background, clean canvas"
    - name: "Carbon"
      hex: "#333333"
      role: "primary text, headings"
  accent:
    - name: "Hey Blue"
      hex: "#00C3FF"
      role: "CTAs, links, primary brand accent"
    - name: "Prism Pink"
      hex: "#F3A6FF"
      role: "secondary accent, gradient endpoint, emphasis"
    - name: "Gen Green"
      hex: "#35C838"
      role: "success states, positive feedback"
  neutral:
    - name: "Mist"
      hex: "#F2F2F2"
      role: "section backgrounds, cards"
    - name: "Cloud"
      hex: "#D9D9D9"
      role: "borders, dividers"
    - name: "Deep Teal"
      hex: "#033337"
      role: "dark backgrounds, footer, contrast sections"

typography:
  display:
    family: "ABC Solar, TT Norms Pro, system-ui"
    weight: "700-800"
    style: "large, confident, generous tracking"
  body:
    family: "TT Norms Pro, system-ui, sans-serif"
    weight: "400-500"
    style: "comfortable reading, 18px base"
  caption:
    family: "TT Norms Pro, system-ui, sans-serif"
    weight: "500"
    style: "14-15px, medium weight for labels"
  rules:
    - "Size scale: 80px → 60px → 44px → 32px → 24px → 18px → 14px"
    - "Generous line heights for readability"
    - "Medium weight (500-600) for UI elements"
    - "Bold (700-800) for headlines only"

layout:
  grid: "12 columns, max-width 1200px, flex-based"
  alignment: "Center-aligned sections, left-aligned content"
  aspect_ratio: "16:9 for video content, varied for features"
  notes:
    - "4px base spacing unit (8, 16, 24, 32, 40, 60, 80px scale)"
    - "Large rounded corners: 12px cards, 20px buttons, 48px hero elements"
    - "Generous padding: 16-24px internal, 60-120px section gaps"
    - "Cards with subtle borders, minimal shadows"

motion:
  transitions:
    - "fadeInUp (300ms) for content reveals"
    - "slideDown (250ms) for dropdowns"
    - "smooth hover transitions (150-200ms)"
  animation_style: >
    Smooth and modern. Elements fade and slide in gracefully.
    Subtle scale effects on hover. Nothing bouncy or playful —
    confident and professional with a touch of polish.
  pacing: "Quick, responsive, modern feel"
  audio_cues:
    - "electronic ambient"
    - "modern corporate"
    - "upbeat but professional"

mood:
  keywords:
    - "innovative"
    - "approachable"
    - "premium"
    - "modern"
    - "creative"
    - "tech-forward"
  era: "2020s AI/SaaS"
  cultural_reference: "Modern AI tools, creative tech platforms, Figma/Notion energy"
  avoid:
    - "harsh corporate blue"
    - "dark, heavy interfaces"
    - "overly complex 3D effects"
    - "stock photography feel"
    - "cluttered layouts"
    - "small, cramped typography"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_heygen:
  brand_gradient: "linear-gradient(328deg, #00c3ff, #95aafe 50%, #fea5fe)"
  orientation: "landscape"
---

## Design Principles

AI should feel accessible, not intimidating.
White space communicates premium quality.
The cyan-pink gradient is the hero — use it sparingly but boldly.
Every interaction should feel smooth and responsive.

## Extraction Notes

Extracted from https://heygen.com on 2026-03-12.
Primary colors sampled from CSS variables and brand guidelines.
Typography identified via computed styles (ABC Solar, TT Norms Pro).
Gradient extracted from hero sections and brand elements.
Spacing system follows 4px base unit pattern.

## Connectors

### HeyGen Video Agent
Use the signature gradient as background or overlay element.
Hey Blue for text emphasis and CTAs. Clean white backgrounds.
Modern, confident pacing. Approachable AI energy.

### HTML Slides
White backgrounds with gradient accent strips or hero elements.
Large rounded corners on cards. Generous whitespace.
Hey Blue for interactive elements, Prism Pink for highlights.

### paper.design
Clean layouts with the gradient as a bold accent element.
Large typography with clear hierarchy. Rounded card patterns.
Avoid heavy shadows — use subtle borders instead.

### Figma
Color styles: `brand/hey-blue`, `brand/prism-pink`, `brand/gradient`.
Text styles following the 80-60-44-32-24-18-14px scale.
Component variants with large border-radius (12-48px).
