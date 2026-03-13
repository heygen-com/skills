# paper.design Connector

Apply a `visual-style.md` to paper.design documents.

## Overview

paper.design is a professional design tool for creating user interfaces. This connector maps `visual-style.md` fields to paper.design document defaults and AI layout guidance.

## Field Mapping

| visual-style.md field | paper.design usage |
|-----------------------|-------------------|
| `colors.primary` | Document color palette (primary colors) |
| `colors.accent` | Document color palette (accent colors) |
| `colors.neutral` | Document color palette (neutral colors) |
| `typography.display.family` | Default display font |
| `typography.body.family` | Default body font |
| `typography.caption.family` | Default caption font |
| `style_prompt_full` | AI layout suggestion prompt |
| `mood.keywords` | Design direction keywords |
| `mood.avoid` | Design constraint checklist |
| `assets.reference_images` | Style board references |
| `layout.grid` | Artboard grid system |
| `layout.alignment` | Default alignment rules |

## Applying the Style

### 1. Set up the color palette

When creating new artboards, apply the colors from the style:

```
Background: colors.primary[0].hex
Text: colors.primary[1].hex
Accent elements: colors.accent[0].hex
Secondary elements: colors.neutral[0].hex
```

### 2. Configure typography

Load the specified fonts and set defaults:

```
Display/Headlines: typography.display.family, typography.display.weight
Body text: typography.body.family, typography.body.weight
Labels/Captions: typography.caption.family, typography.caption.weight
```

### 3. Apply layout rules

Follow `layout.grid` for artboard structure:

- "12 columns" → Set up 12-column grid
- "Strict modular grid" → Enable grid snapping
- "Flush left" → Left-align all text blocks

### 4. Use style_prompt_full for AI guidance

When using AI features in paper.design, include the `style_prompt_full` in your prompt:

```
Create a landing page hero section.

Visual style:
[PASTE style_prompt_full HERE]

Constraints:
[ITEMS FROM mood.avoid]
```

## Example: Applying Swiss Style

Given `mueller-brockmann-swiss.visual-style.md`:

**Color setup:**
- Background: `#000000` (Pure Black)
- Text: `#FFFFFF` (Pure White)
- Accent: `#0066FF` (Electric Blue)
- Grid lines: `#CCCCCC` (Grid Gray)

**Typography:**
- All text: Helvetica family
- Headlines: Helvetica Bold, uppercase
- Body: Helvetica Regular, flush left
- Captions: Helvetica Light, small, uppercase

**Layout:**
- 12-column modular grid
- All elements snap to grid
- No centered text
- Strong diagonal compositions within orthogonal structure

**Design constraints (from mood.avoid):**
- No organic or curved shapes
- No gradients
- No stock photography
- No rounded corners
- No decorative elements

## Workflow

1. **Read the style** — Load the `visual-style.md` file
2. **Create artboard** — Set dimensions from `layout.aspect_ratio`
3. **Apply background** — Use `colors.primary[0].hex`
4. **Set up grid** — Follow `layout.grid` specification
5. **Configure fonts** — Load `typography.*` families
6. **Build content** — Follow `mood.keywords` for direction
7. **Review** — Check against `mood.avoid` constraints

## Design Brief Format

When starting a new design in paper.design, generate a brief from the style:

```markdown
## Design Brief

**Style:** [name]

**Color Palette:**
- [colors.primary[0].name]: [hex] — [role]
- [colors.primary[1].name]: [hex] — [role]
- [colors.accent[0].name]: [hex] — [role]

**Typography:**
- Display: [typography.display.family] [weight]
- Body: [typography.body.family] [weight]

**Layout:** [layout.grid], [layout.alignment]

**Mood:** [mood.keywords joined]

**Avoid:** [mood.avoid joined]
```

## Tips

- **Start with the grid** — Set up `layout.grid` before placing elements
- **Typography first** — Let `typography.rules` guide hierarchy decisions
- **Check constraints regularly** — Reference `mood.avoid` while designing
- **Use reference images** — If `assets.reference_images` has URLs, import them as a style board
