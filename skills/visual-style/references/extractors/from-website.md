# Extract from Website

Generate a `visual-style.md` from a website URL.

## Workflow

1. **Receive URL** — User provides a website URL
2. **Fetch the page** — Use web fetch to get the full HTML source
3. **Extract CSS data** — Parse inline styles, `<style>` blocks, and linked stylesheets. Look for CSS custom properties (`:root` / `[data-theme]` variables) first — these are the most reliable source of the design system
4. **Take screenshots** — Capture the page visually if possible to cross-reference extracted values
5. **Analyze deeply** — Apply the extraction checklist below to identify every design token
6. **Classify imagery** — Determine the visual style of any images, illustrations, or graphics on the page
7. **Generate** — Output complete `visual-style.md` with exact values
8. **Validate** — Ensure all required fields are present and values are precise (hex codes, px/em/rem units, font names)

## Where to Find Exact Values

### CSS Custom Properties (Best Source)

Most modern sites define their design tokens as CSS variables. Search the fetched HTML/CSS for these patterns:

```css
/* Color tokens — look for these in :root, [data-theme], or body */
--color-bg, --background, --bg-primary, --color-background
--color-text, --text-primary, --foreground, --color-body
--color-accent, --brand-primary, --color-cta, --color-link
--color-muted, --text-secondary, --color-subtle
--color-border, --border-color, --divider

/* Typography tokens */
--font-family, --font-sans, --font-display, --font-heading, --font-body, --font-mono
--font-size-*, --text-*, --heading-size-*
--line-height-*, --leading-*
--letter-spacing-*, --tracking-*
--font-weight-*

/* Spacing tokens */
--space-*, --gap-*, --padding-*, --radius-*
```

### Computed Styles (Fallback)

When CSS variables aren't available, extract values from the actual element styles:

| Property | Where to look | What to record |
|----------|--------------|----------------|
| `background-color` | `<body>`, `<main>`, `.hero`, section containers | Exact hex — this is the **primary background** |
| `color` | `<body>`, `<p>`, `.text-*` | Exact hex — this is the **primary text color** |
| `color` | `<h1>`, `<h2>`, `<h3>` | Exact hex — heading color (often different from body text) |
| `background-color` | `<button>`, `.btn`, `.cta`, `<a class="button">` | Accent / CTA color |
| `color` | `<a>` | Link color |
| `font-family` | `<body>` | Body font stack (full fallback chain) |
| `font-family` | `<h1>`, `<h2>` | Display/heading font (if different from body) |
| `font-size` | `<h1>`, `<h2>`, `<h3>`, `<p>`, `<small>` | Full type scale |
| `line-height` | `<p>`, `<h1>`, `<h2>` | Record as unitless ratio (e.g., `1.5`) or px |
| `letter-spacing` | `<h1>`, `<h2>`, `<p>`, nav links | Record in em (e.g., `-0.02em`, `0.05em`) |
| `font-weight` | headings, body, buttons, nav | Record numeric values (`400`, `600`, `700`) |

### Google Fonts / @font-face

Search the HTML for font loading to identify exact font names:

```html
<!-- Google Fonts link -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">

<!-- @font-face declarations -->
@font-face { font-family: "CustomFont"; src: url(...); }
```

The font family name in the `<link>` URL or `@font-face` declaration is the authoritative name to use.

## Extraction Prompt

Use this prompt template when analyzing a website:

```
Analyze this website and extract a visual-style.md following the spec.

URL: [URL]

STEP 1 — EXTRACT RAW CSS VALUES
Search the page source for:
- CSS custom properties (:root variables) — list every --color-*, --font-*, --spacing-* variable
- @font-face declarations and Google Fonts links — exact font family names
- Key element styles: body background-color, body color, h1/h2/h3 styles, button/CTA styles, link styles

STEP 2 — MAP TO COLORS
From the raw CSS values, identify:
- colors.primary: The page background color AND the primary text color (minimum 2)
- colors.accent: CTA/button background colors, link colors, hover states
- colors.neutral: Secondary text colors, border colors, muted backgrounds, dividers

Every hex value must come directly from the CSS. Do not approximate.
Name each color descriptively based on its appearance (not "Blue 1" but "Ocean Blue").

STEP 3 — MAP TO TYPOGRAPHY
For each typography tier (display, body, caption), record:
- family: Exact font-family value including fallbacks (e.g., "Inter, system-ui, sans-serif")
- weight: Numeric weight from CSS (e.g., "600")
- style: Descriptive notes (case, tracking description)
- size: The reference font-size from CSS (e.g., "48px", "1rem")
- line_height: The line-height from CSS as unitless ratio or px (e.g., "1.2", "56px")
- letter_spacing: The letter-spacing from CSS (e.g., "-0.02em", "0.05em", "normal")

Capture the full type scale in typography.rules (e.g., "64px → 48px → 32px → 24px → 16px → 14px").

STEP 4 — CLASSIFY IMAGERY
Look at any images, illustrations, icons, or graphics on the page:
- What is the visual style? (photographic, illustrated, 3d-rendered, sketch, abstract-geometric, collage, pixel-art, icon-driven, mixed)
- How are images treated? (filters, shapes, borders, shadows, overlays)
- What subjects appear? (people, products, screenshots, abstract, patterns)

STEP 5 — CAPTURE MOTION & ANIMATION
Look for CSS transitions, @keyframes, scroll-triggered animations:
- transition properties and durations (e.g., "all 0.3s ease")
- animation names and behaviors
- Scroll-triggered effects (fade-in, slide-up, parallax)
- Hover effects on buttons, cards, links

STEP 6 — GENERATE OUTPUT
Output complete YAML frontmatter between --- delimiters.
Plus Markdown body sections (## Design Principles, ## Extraction Notes).
Include every value with its exact CSS source.
```

## Analysis Checklist

When extracting, verify each item:

### Colors (extract exact hex from CSS)
- [ ] Page background color (`body` or `main` `background-color`) → `colors.primary[0]`
- [ ] Primary text color (`body` `color`) → `colors.primary[1]`
- [ ] Heading text color (`h1`/`h2` `color`, if different from body) → `colors.primary` or `colors.accent`
- [ ] CTA / button background color → `colors.accent`
- [ ] Link color (`a` `color`) → `colors.accent`
- [ ] Link hover color (`a:hover` `color`) → note in role description
- [ ] Secondary/muted text color → `colors.neutral`
- [ ] Card/section alternate background → `colors.neutral`
- [ ] Border/divider color → `colors.neutral`
- [ ] Gradient definitions (if any) → note in color roles and `style_prompt_full`
- [ ] **Cross-check**: Does the background + text color pair match what you see on the page?

### Typography (extract exact values from CSS)
- [ ] Display/heading `font-family` (with full fallback stack)
- [ ] Display/heading `font-weight` (numeric: 400, 500, 600, 700, 800, 900)
- [ ] Display/heading `font-size` (the h1 size — e.g., `"56px"`, `"3.5rem"`)
- [ ] Display/heading `line-height` (e.g., `"1.1"`, `"64px"`)
- [ ] Display/heading `letter-spacing` (e.g., `"-0.03em"`, `"normal"`)
- [ ] Body `font-family` (with full fallback stack)
- [ ] Body `font-weight`
- [ ] Body `font-size` (e.g., `"16px"`, `"1rem"`)
- [ ] Body `line-height` (e.g., `"1.6"`, `"28px"`)
- [ ] Body `letter-spacing` (e.g., `"normal"`, `"0.01em"`)
- [ ] Caption/small `font-family`, `font-size`, `line-height`
- [ ] Full type scale (all heading sizes h1→h6 and body) → `typography.rules`
- [ ] Text transforms used (uppercase headings? all-caps nav?)
- [ ] **Cross-check**: Are the font names from an actual @font-face or Google Fonts link?

### Imagery (classify what you see)
- [ ] Visual style of images (photographic, illustrated, 3d, sketch, geometric, etc.)
- [ ] Image treatment (filters, masks, rounded corners, shadows, overlays)
- [ ] Common subjects (people, products, screenshots, abstract, patterns)
- [ ] Icon style (outlined, filled, duotone, custom illustrated)
- [ ] Whether the site uses SVG illustrations, photos, or both

### Layout
- [ ] Max content width (`max-width` on container)
- [ ] Grid columns (if visible)
- [ ] Base spacing unit (look for consistent multiples: 4px, 8px, etc.)
- [ ] Alignment patterns (left, center, mixed)
- [ ] Card/component patterns (border-radius, shadow, padding)
- [ ] Negative space usage

### Motion & Animation
- [ ] CSS `transition` properties (what properties animate, duration, easing)
- [ ] `@keyframes` animations (name them, describe the effect)
- [ ] Scroll-triggered animations (fade-in, slide-up, parallax)
- [ ] Hover effects (buttons, cards, links — what changes and how fast)
- [ ] Page/route transitions (if SPA)
- [ ] Loading states and skeleton screens

### Mood
- [ ] Overall feeling (professional, playful, minimal, bold, luxurious)
- [ ] Design era (modern, retro, timeless, futuristic)
- [ ] Brand personality (serious, friendly, technical, creative)
- [ ] What they explicitly avoid (infer from absence)

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
  Modern fintech design inspired by Stripe. Clean white (#FFFFFF)
  backgrounds with generous whitespace. Deep purple (#635BFF) as
  the primary accent color for CTAs and links. Dark slate (#0A2540)
  for headings with lighter slate (#425466) for body text. Pale
  gray (#F6F9FC) for alternating section backgrounds. Typography
  uses Söhne (or Inter as fallback) — display at 600 weight with
  tight -0.02em tracking, body at 400 weight with 1.6 line height
  for comfortable reading. Type scale: 64px → 48px → 32px → 24px
  → 16px. Subtle mesh gradients in hero backgrounds using purple
  to cyan (#00D4FF). Rounded 12px corners on cards and buttons.
  Smooth 0.2s ease transitions on hover. Fade-in-up on scroll.
  Professional, trustworthy, approachable. Imagery is a mix of
  product UI screenshots and custom abstract gradient art — no
  stock photography, no illustrations of people. No harsh colors,
  no busy patterns, no overly playful animations.

colors:
  primary:
    - name: "Pure White"
      hex: "#FFFFFF"
      role: "primary background, negative space"
    - name: "Slate Dark"
      hex: "#0A2540"
      role: "primary headings, high-contrast text"
  accent:
    - name: "Stripe Purple"
      hex: "#635BFF"
      role: "CTAs, links, brand accent"
    - name: "Cyan Accent"
      hex: "#00D4FF"
      role: "secondary accent, gradient endpoint"
  neutral:
    - name: "Slate Gray"
      hex: "#425466"
      role: "body text, secondary content"
    - name: "Light Gray"
      hex: "#F6F9FC"
      role: "section backgrounds, card surfaces"
    - name: "Border Gray"
      hex: "#E3E8EE"
      role: "borders, dividers, subtle separators"

typography:
  display:
    family: "Söhne, Inter, system-ui, sans-serif"
    weight: "600"
    style: "sentence case, tight tracking"
    size: "64px"
    line_height: "1.1"
    letter_spacing: "-0.02em"
  body:
    family: "Söhne, Inter, system-ui, sans-serif"
    weight: "400"
    style: "sentence case, generous line height for readability"
    size: "16px"
    line_height: "1.6"
    letter_spacing: "normal"
  caption:
    family: "Söhne Mono, monospace"
    weight: "400"
    style: "code blocks, technical details"
    size: "14px"
    line_height: "1.5"
    letter_spacing: "normal"
  rules:
    - "Type scale: 64px → 48px → 32px → 24px → 16px → 14px"
    - "Display weight 600, body weight 400 — never use 300 or 800"
    - "Monospace only for code and technical content"
    - "Line height ≥ 1.5 for body text, tighter (1.1) for large display"

imagery:
  style: "photographic with abstract gradient art"
  treatment: "product screenshots in browser frames, mesh gradients as hero backgrounds, rounded 12px corners"
  subjects:
    - "product UI / dashboard screenshots"
    - "abstract mesh gradient backgrounds (purple → cyan)"
    - "code snippets in dark terminal frames"
  notes:
    - "No stock photography — all custom product shots or abstract art"
    - "Gradients are mesh/organic, never linear bands"
    - "Screenshots always shown in realistic device/browser frames"

layout:
  grid: "12 columns, max-width 1080px, 8px base spacing unit"
  alignment: "Center-aligned sections, left-aligned text blocks"
  aspect_ratio: "16:9 for hero, varied for content"
  notes:
    - "Generous vertical spacing (80-120px between sections)"
    - "Cards with subtle box-shadow and 12px border-radius"
    - "Alternating white / light-gray section backgrounds"

motion:
  transitions:
    - "all 0.2s ease on hover states"
    - "fade-in-up on scroll (300ms ease-out, 20px translate)"
    - "subtle parallax on hero backgrounds"
  animation_style: "Subtle, smooth, professional. Ease-out curves. Nothing bouncy or playful."
  pacing: "Measured, confident. 200-300ms for interactions, 400-600ms for scroll reveals."

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
    - "stock photography of people"
    - "overly playful or bouncy animations"
    - "dark mode (unless requested)"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

Trust through clarity. Every element earns its place. Typography and whitespace
do the heavy lifting. Color is used sparingly and intentionally. Purple accents
draw attention only to what matters — CTAs and key data points.

## Extraction Notes

Extracted from https://stripe.com on 2026-03-12.
Background #FFFFFF from body background-color.
Text #0A2540 from h1/h2 color property. Body text #425466 from p color.
Purple #635BFF sampled from .btn-primary background-color.
Typography identified from Google Fonts link: Söhne family at weights 400, 600.
Mesh gradient colors #635BFF → #00D4FF from hero section background.
Type scale measured from h1 (64px) through body (16px).
Letter-spacing -0.02em on h1, normal on body — from computed styles.
Line-height 1.1 on display, 1.6 on body — from CSS declarations.
```

## Tips

- **CSS variables first** — Search for `:root {` or `[data-theme]` blocks — these contain the authoritative design tokens
- **Font loading tags** — Look for `<link href="fonts.googleapis.com/..."` or `@font-face` blocks to get exact font names
- **Computed values matter** — Record the actual `px`, `em`, `rem` values you find, not approximations like "large" or "tight"
- **Background ≠ white by default** — Always verify the actual `background-color` on `body`/`main`. Many sites use off-whites like `#FAFAFA`, `#F8F9FA`, `#FFFDF5`
- **Heading color ≠ body color** — Check `<h1>` and `<p>` separately. Headings often use a darker/different color
- **Letter-spacing is often negative on display text** — Large headings commonly use `-0.01em` to `-0.04em` for tighter appearance
- **Classify the imagery** — Is it photography? Illustration? 3D renders? Abstract shapes? This defines the visual identity as much as colors do
- **Note what's absent** — If a site has zero stock photos, no illustrations, or no animations, that's a deliberate choice worth capturing in `mood.avoid`
- **Capture the feel** — The `style_prompt_full` should weave together colors, typography, imagery style, and motion into a cohesive description that could recreate the visual identity
