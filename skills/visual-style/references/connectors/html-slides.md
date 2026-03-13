# HTML Slides Connector (frontend-slides)

Apply a `visual-style.md` to HTML slide presentations.

## Overview

This connector maps `visual-style.md` fields to CSS variables and styling rules for use with [frontend-slides](https://github.com/zarazhangrui/frontend-slides) or similar HTML presentation frameworks.

## Field Mapping

| visual-style.md field | CSS output |
|-----------------------|------------|
| `colors.primary[0].hex` | `--color-bg` |
| `colors.primary[1].hex` | `--color-text` |
| `colors.accent[0].hex` | `--color-accent` |
| `colors.neutral[0].hex` | `--color-muted` |
| `typography.display.family` | `--font-display` |
| `typography.body.family` | `--font-body` |
| `typography.display` | `h1, h2, h3` styling |
| `typography.body` | `p, li` styling |
| `typography.caption` | `.label, code, small` styling |
| `typography.rules` | Additional CSS rules |
| `layout.grid` | CSS grid/flexbox system |
| `layout.aspect_ratio` | Slide dimensions |
| `motion.transitions` | CSS slide transitions |
| `mood.avoid` | Design constraints checklist |

## CSS Variables Template

```css
:root {
  /* Colors */
  --color-bg: [colors.primary[0].hex];
  --color-text: [colors.primary[1].hex];
  --color-accent: [colors.accent[0].hex];
  --color-muted: [colors.neutral[0].hex];

  /* Typography */
  --font-display: "[typography.display.family]", system-ui, sans-serif;
  --font-body: "[typography.body.family]", system-ui, sans-serif;

  /* Spacing (derive from style) */
  --space-sm: clamp(0.5rem, 1vw, 1rem);
  --space-md: clamp(1rem, 2vw, 2rem);
  --space-lg: clamp(2rem, 4vw, 4rem);
}

body {
  font-family: var(--font-body);
  background: var(--color-bg);
  color: var(--color-text);
}

h1, h2, h3 {
  font-family: var(--font-display);
  font-weight: [typography.display.weight];
  /* Apply typography.display.style rules */
}

.accent {
  color: var(--color-accent);
}

.muted {
  color: var(--color-muted);
}
```

## frontend-slides Constraints

When generating HTML slides, follow these rules:

1. **Single HTML file** — Zero dependencies, inline CSS/JS
2. **Viewport units** — All sizes use `clamp()`, never fixed px/rem
3. **No scrolling** — `height: 100vh; overflow: hidden;` per slide
4. **Content overflow** — If content doesn't fit, split into multiple slides
5. **Google Fonts** — Load via `<link>` tag in `<head>`

## Example: Swiss Style Slides

Given `mueller-brockmann-swiss.visual-style.md`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presentation</title>
  <link href="https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --color-bg: #000000;
      --color-text: #FFFFFF;
      --color-accent: #0066FF;
      --color-muted: #CCCCCC;
      --font-display: "Helvetica Neue", Helvetica, Arial, sans-serif;
      --font-body: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-body);
      background: var(--color-bg);
      color: var(--color-text);
    }

    .slide {
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: clamp(2rem, 5vw, 6rem);
    }

    h1 {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: clamp(3rem, 8vw, 8rem);
      text-transform: uppercase;
      letter-spacing: -0.02em;
      line-height: 0.9;
      text-align: left;
    }

    .accent { color: var(--color-accent); }

    /* Grid overlay for Swiss style */
    .slide::before {
      content: '';
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(
        90deg,
        transparent,
        transparent calc(100% / 12 - 1px),
        var(--color-muted) calc(100% / 12 - 1px),
        var(--color-muted) calc(100% / 12)
      );
      opacity: 0.1;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <section class="slide">
    <h1>Grid-locked<br><span class="accent">precision</span></h1>
  </section>
</body>
</html>
```

## Workflow

1. **Load the style** — Read the `visual-style.md` file
2. **Generate CSS variables** — Map colors and typography
3. **Apply typography rules** — Follow `typography.rules` constraints
4. **Check constraints** — Verify against `mood.avoid` list
5. **Generate slides** — One `<section class="slide">` per slide
6. **Validate** — Ensure no scrolling, all sizes responsive

## Tips

- **Typography drives hierarchy** — Use `typography.display` for headlines, `typography.body` for content
- **Honor the avoid list** — Check `mood.avoid` before adding decorative elements
- **Transitions** — Map `motion.transitions` to CSS transitions between slides
- **Font loading** — Always include fallback fonts in the stack
