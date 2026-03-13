# HeyGen Video Agent Connector

Apply a `visual-style.md` to HeyGen Video Agent for AI-generated videos.

## Overview

HeyGen Video Agent accepts a text prompt that can include visual style instructions. The `style_prompt_full` field maps directly to this.

## Field Mapping

| visual-style.md field | HeyGen usage |
|-----------------------|--------------|
| `style_prompt_full` | Appended verbatim to the generation prompt |
| `motion.transitions` | Scene transition instructions |
| `motion.animation_style` | Animation behavior |
| `motion.pacing` | Timing guidance |
| `typography.caption` | Caption styling (if captions enabled) |
| `layout.aspect_ratio` | Orientation setting (16:9 = landscape, 9:16 = portrait) |
| `mood.avoid` | Negative prompt / exclusion instructions |
| `assets.gsep_elements` | Overlay assets (if supported) |
| `x_heygen.orientation` | Explicit orientation override |
| `x_heygen.video_id` | Reference to existing HeyGen video |

## Prompt Template

```
Create a video about [TOPIC].

Script:
[USER'S SCRIPT]

Visual style:
[PASTE style_prompt_full HERE]

Additional constraints:
- [ITEMS FROM mood.avoid]

Motion:
- Transitions: [motion.transitions]
- Pacing: [motion.pacing]
- Animation: [motion.animation_style]

Format: [layout.aspect_ratio OR x_heygen.orientation]
```

## Example: No-Avatar Motion Graphics

For pure motion graphics without an avatar:

```
Create a video about our Q4 results.

Script:
Revenue grew 40% year over year. We shipped 12 new features.
Customer satisfaction hit an all-time high of 94%.

Visual style:
Josef Müller-Brockmann Swiss International Style. Grid-locked layouts
with mathematical precision. Black and white base with ONE accent color
(electric blue #0066FF). Strong diagonal compositions. Helvetica
typography only. Data visualizations are the hero — animated charts,
counters, grids. Every frame snaps to a grid. Transitions are horizontal
grid wipes. No organic shapes. No gradients. No stock photography.
Everything is geometric, systematic, precise.

Additional constraints:
- No avatar
- No b-roll footage
- No stock photography
- Pure motion graphics only

Motion:
- Transitions: horizontal grid wipes, clean hard cuts
- Pacing: Measured, confident, unhurried
- Animation: Elements snap to grid positions, charts animate systematically

Format: landscape (16:9)
```

## Workflow

1. **Load the style** — Read the `visual-style.md` file
2. **Extract key fields:**
   - `style_prompt_full` (required)
   - `motion.*` fields (recommended)
   - `mood.avoid` (recommended)
   - `layout.aspect_ratio` or `x_heygen.orientation`
3. **Build the prompt** — Use the template above
4. **Call HeyGen Video Agent** — Use the HeyGen MCP tool or API
5. **Store reference** — Save the video ID to `x_heygen.video_id` if desired

## Tips

- **Be explicit about what you don't want** — HeyGen responds well to negative constraints
- **Motion graphics mode** — Add "No avatar. No b-roll. Pure motion graphics." for abstract styles
- **Data visualization** — Mention "animated charts, counters, data viz" for number-heavy content
- **Transitions matter** — Specify transition style explicitly; defaults may not match your style

## Supported Styles

These gallery styles work especially well with HeyGen Video Agent:

- `mueller-brockmann-swiss.visual-style.md` — Data-driven, grid-locked
- `neville-brody-industrial.visual-style.md` — Bold typography, industrial
- `saul-bass-cinematic.visual-style.md` — Cinematic titles, bold shapes
- `game-boy-color.visual-style.md` — Pixel art, retro gaming
- `heygen-ai-video.visual-style.md` — Modern AI/SaaS aesthetic
