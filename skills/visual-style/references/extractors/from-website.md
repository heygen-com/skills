# Extract from Website

Generate a `visual-style.md` from a website URL.

## Workflow

1. **Receive URL** — User provides a website URL
2. **Fetch the page** — Use web fetch to get the HTML/CSS
3. **Take screenshots** — Capture the page visually if possible
4. **Analyze** — Identify colors, typography, layout, motion, mood
5. **Generate** — Output complete `visual-style.md`
6. **Validate** — Ensure all required fields are present

## Extraction Prompt

Use this prompt template when analyzing a website:

```
Analyze this website and extract a visual-style.md following the spec.

URL: [URL]

Identify and output these fields:

REQUIRED:
- name: A descriptive name for this style (e.g., "[Brand] Web Style")
- version: "1.0"
- style_prompt_short: 1-2 sentence hook capturing the visual essence
- style_prompt_full: Detailed generation prompt with specific:
  - Hex color codes (use exact values, don't guess)
  - Font family names (check the CSS)
  - Layout structure (grid system, spacing patterns)
  - Motion patterns (animations, transitions)
  - Overall mood and feel
- colors.primary: At least 2 colors with name, hex, role

RECOMMENDED:
- colors.accent: Accent colors with name, hex, role
- colors.neutral: Neutral/gray colors with name, hex, role
- typography.display: Heading font family, weight, style
- typography.body: Body font family, weight, style
- typography.caption: Caption/label font family, weight, style
- typography.rules: Typography constraints and patterns
- layout.grid: Grid system description
- layout.alignment: Alignment patterns
- layout.notes: Additional layout observations
- motion.transitions: Transition types used
- motion.animation_style: Overall animation approach
- mood.keywords: 4-6 mood/feeling words
- mood.era: Design era reference
- mood.avoid: Anti-patterns to avoid

Be specific:
- Use exact hex values from the CSS, not approximations
- Name every color descriptively (not "Blue 1", but "Ocean Blue")
- Describe the role of each color in the system
- Note any custom fonts and their fallbacks

Output format:
Complete YAML frontmatter between --- delimiters
Plus Markdown body sections (## Design Principles, ## Extraction Notes)
```

## Analysis Checklist

When extracting, look for:

### Colors
- [ ] Background colors (primary surfaces)
- [ ] Text colors (headings vs body)
- [ ] Accent/CTA button colors
- [ ] Link colors (default, hover, visited)
- [ ] Border/divider colors
- [ ] Gradient usage (if any)

### Typography
- [ ] Heading font family
- [ ] Body font family
- [ ] Font weights used (light, regular, bold, etc.)
- [ ] Text sizes (heading scale)
- [ ] Line heights
- [ ] Letter spacing patterns
- [ ] Text transform (uppercase, lowercase)

### Layout
- [ ] Max content width
- [ ] Grid columns (if visible)
- [ ] Spacing rhythm (consistent gaps)
- [ ] Alignment patterns (left, center, mixed)
- [ ] Card/component patterns
- [ ] Negative space usage

### Motion
- [ ] Page transitions
- [ ] Hover effects
- [ ] Scroll animations
- [ ] Loading states
- [ ] Micro-interactions

### Mood
- [ ] Overall feeling (professional, playful, minimal, bold)
- [ ] Design era (modern, retro, timeless)
- [ ] Brand personality (serious, friendly, technical)
- [ ] What they explicitly avoid

## Example Output

Given URL `https://stripe.com`:

```yaml
---
name: "Stripe Web Style"
version: "1.0"
tags:
  - fintech
  - sleek minimal
author: "Extracted"
source_url: "https://stripe.com"
created: "2026-03-12"

style_prompt_short: >
  Clean fintech minimalism with deep purple accents on white.
  Generous whitespace, clear typography, subtle gradients.

style_prompt_full: >
  Modern fintech design inspired by Stripe. Clean white backgrounds
  with generous whitespace. Deep purple (#635BFF) as the primary
  accent color. Typography uses a custom geometric sans-serif
  (similar to Inter or Söhne) with clear hierarchy. Subtle mesh
  gradients in backgrounds. Rounded corners on cards and buttons.
  Smooth, subtle animations on scroll. Professional, trustworthy,
  approachable. No harsh colors, no busy patterns, no stock photos.

colors:
  primary:
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "primary background, negative space"
    - name: "Slate Dark"
      hex: "#0A2540"
      role: "primary text, headings"
  accent:
    - name: "Stripe Purple"
      hex: "#635BFF"
      role: "CTAs, links, brand accent"
    - name: "Cyan Accent"
      hex: "#00D4FF"
      role: "secondary accent, gradients"
  neutral:
    - name: "Slate Gray"
      hex: "#425466"
      role: "body text, secondary content"
    - name: "Light Gray"
      hex: "#F6F9FC"
      role: "section backgrounds, cards"

typography:
  display:
    family: "Söhne, Inter, system-ui"
    weight: "600"
    style: "sentence case, tight tracking"
  body:
    family: "Söhne, Inter, system-ui"
    weight: "400"
    style: "generous line height, comfortable reading"
  caption:
    family: "Söhne Mono, monospace"
    weight: "400"
    style: "code blocks, technical details"
  rules:
    - "Clear size hierarchy: 64px → 48px → 32px → 24px → 16px"
    - "Generous line heights for readability"
    - "Monospace for code and technical content"

layout:
  grid: "12 columns, max-width 1200px"
  alignment: "Center-aligned sections, left-aligned text"
  aspect_ratio: "16:9 for hero, varied for content"
  notes:
    - "Generous vertical spacing between sections"
    - "Cards with subtle shadows and rounded corners"
    - "Alternating section backgrounds"

motion:
  transitions:
    - "subtle fade-in on scroll"
    - "smooth hover state transitions (0.2s)"
    - "parallax on hero backgrounds"
  animation_style: "Subtle, smooth, professional. Nothing bouncy or playful."
  pacing: "Measured, confident transitions"

mood:
  keywords:
    - "professional"
    - "trustworthy"
    - "clean"
    - "modern"
    - "approachable"
  era: "2020s fintech"
  cultural_reference: "Modern SaaS, developer-focused design"
  avoid:
    - "harsh or neon colors"
    - "busy patterns or textures"
    - "stock photography"
    - "overly playful animations"
    - "dark mode (unless requested)"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

Trust through clarity. Every element earns its place. Typography and whitespace
do the heavy lifting. Color is used sparingly and intentionally.

## Extraction Notes

Extracted from https://stripe.com on 2026-03-12.
Primary purple sampled from CTA buttons.
Typography stack identified via browser dev tools.
Mesh gradient patterns noted in hero sections.
```

## Tips

- **Use dev tools** — Inspect element to get exact hex values and font stacks
- **Check CSS variables** — Many sites define their palette in `:root`
- **Note responsive patterns** — How does the design adapt?
- **Capture the feel** — The `style_prompt_full` should evoke the same feeling
- **Be specific about avoids** — What does this brand clearly NOT do?
