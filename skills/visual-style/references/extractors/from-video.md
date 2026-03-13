# Extract from Video

Generate a `visual-style.md` from video keyframes.

## Workflow

1. **Receive video** — User provides a video URL or file
2. **Sample keyframes** — Capture 4-6 screenshots at different points
3. **Analyze frames** — Identify consistent visual patterns across all frames
4. **Focus on motion** — Pay special attention to transitions and animation
5. **Generate** — Output complete `visual-style.md`
6. **Validate** — Ensure all required fields are present

## Keyframe Sampling Strategy

Sample frames at these intervals:
- **0:00-0:02** — Opening/title frame
- **0:05-0:10** — Early content frame
- **0:15-0:20** — Middle content frame
- **Near end** — Closing frame
- **Transitions** — Capture mid-transition if possible

Look for **consistency** across frames — the style is what stays the same.

## Extraction Prompt

Use this prompt template when analyzing video frames:

```
Analyze these video keyframes and extract a visual-style.md.

These are [N] frames from a single video. Identify the CONSISTENT visual
system across all frames, not the unique content of each frame.

Identify and output:

REQUIRED:
- name: A descriptive name for this style
- version: "1.0"
- style_prompt_short: 1-2 sentence hook
- style_prompt_full: Detailed generation prompt covering:
  - Color palette (consistent colors across frames)
  - Typography style (font appearance, text treatment)
  - Motion patterns (transitions, animation style)
  - Layout approach (composition, spacing)
  - Overall mood
- colors.primary: At least 2 consistent colors

CRITICAL FOR VIDEO:
- motion.transitions: How do scenes change?
- motion.animation_style: How do elements move?
- motion.pacing: Fast cuts vs. slow fades?
- mood.keywords: What feeling does the motion create?

Be specific about MOTION patterns:
- Do elements snap or ease?
- Are transitions hard cuts or smooth fades?
- Do things bounce, slide, or appear suddenly?
- What's the rhythm? Quick and energetic, or slow and measured?

Output format:
Complete YAML frontmatter between --- delimiters
Plus Markdown body sections
```

## Analysis Checklist

When extracting from video, look for:

### Colors
- [ ] Background colors (do they change between scenes?)
- [ ] Primary text/graphic colors
- [ ] Accent colors for emphasis
- [ ] Color transitions (do colors shift?)

### Typography
- [ ] Title treatment (size, weight, animation)
- [ ] Body text style (if present)
- [ ] Caption/subtitle style
- [ ] Text animation (fade, slide, type-on)

### Motion (Critical)
- [ ] Scene transitions (cut, wipe, dissolve, morph)
- [ ] Element entrances (fade, slide, pop, scale)
- [ ] Element exits (how do things leave?)
- [ ] Easing style (linear, ease-out, bounce, snap)
- [ ] Timing/rhythm (quick cuts, slow reveals)
- [ ] Looping patterns (if any)

### Layout
- [ ] Composition style (centered, asymmetric, grid-locked)
- [ ] Framing (full-bleed, contained, letterboxed)
- [ ] Text placement (bottom third, centered, dynamic)
- [ ] Aspect ratio (16:9, 9:16, 1:1)

### Mood
- [ ] Energy level (calm, energetic, intense)
- [ ] Tone (serious, playful, dramatic)
- [ ] Era/genre references
- [ ] Sound-visual relationship (if audio present)

## Example Output

Given frames from a retro arcade-style video:

```yaml
---
name: "Pac-Man Arcade Style"
version: "1.0"
tags:
  - pixel retro
  - gaming
author: "Extracted"
source_url: ""
created: "2026-03-12"

style_prompt_short: >
  8-bit arcade nostalgia. Pixel graphics, neon on black,
  classic Pac-Man yellow with ghost accents.

style_prompt_full: >
  Retro 8-bit arcade aesthetic inspired by Pac-Man. Pure black
  backgrounds with neon pixel graphics. Classic Pac-Man yellow
  (#FFFF00) as the hero color. Ghost colors for accents: Blinky
  red (#FF0000), Pinky pink (#FFB8FF), Inky cyan (#00FFFF),
  Clyde orange (#FFB852). Chunky pixel fonts. Elements move in
  discrete pixel steps, not smooth curves. Maze-like compositions.
  Screen flicker and CRT scanline effects. 8-bit sound design
  aesthetic applied visually. Hard cuts between scenes. No
  gradients, no anti-aliasing, no rounded corners.

colors:
  primary:
    - name: "Arcade Black"
      hex: "#000000"
      role: "background, the void"
    - name: "Pac-Man Yellow"
      hex: "#FFFF00"
      role: "hero element, primary accent"
  accent:
    - name: "Blinky Red"
      hex: "#FF0000"
      role: "danger, emphasis"
    - name: "Inky Cyan"
      hex: "#00FFFF"
      role: "secondary accent"
    - name: "Pinky Pink"
      hex: "#FFB8FF"
      role: "tertiary accent"
    - name: "Clyde Orange"
      hex: "#FFB852"
      role: "warm accent"
  neutral:
    - name: "Maze Blue"
      hex: "#2121DE"
      role: "structure, maze walls"

typography:
  display:
    family: "Press Start 2P, monospace"
    weight: "400"
    style: "uppercase, pixel-perfect"
  body:
    family: "VT323, monospace"
    weight: "400"
    style: "8-bit rendering"
  caption:
    family: "Press Start 2P, monospace"
    weight: "400"
    style: "small, all caps"
  rules:
    - "All text must appear pixel-perfect"
    - "No anti-aliasing on fonts"
    - "Text animates character by character"

layout:
  grid: "Pixel grid, 8px base unit"
  alignment: "Centered compositions"
  aspect_ratio: "4:3 or 16:9"
  notes:
    - "Maze-like structures as compositional elements"
    - "Frame content like an arcade cabinet"
    - "Leave scanline space at edges"

motion:
  transitions:
    - "hard cuts (no dissolves)"
    - "screen wipe from Pac-Man eating across"
    - "pixel dissolve / scatter"
  animation_style: >
    Discrete pixel movement — elements jump from position to position,
    never smooth tweening. Characters animate at 12fps max. Screen
    flicker for emphasis. Chomping animation on any moving element.
  pacing: "Energetic, game-loop rhythm"
  audio_cues:
    - "wakka-wakka sound on transitions"
    - "8-bit beeps and boops"

mood:
  keywords:
    - "nostalgic"
    - "playful"
    - "arcade"
    - "8-bit"
    - "energetic"
  era: "1980s arcade golden age"
  cultural_reference: "Pac-Man, Space Invaders, Galaga, arcade cabinets"
  avoid:
    - "smooth gradients"
    - "anti-aliased edges"
    - "photorealistic elements"
    - "modern UI patterns"
    - "slow, smooth animations"
    - "muted or desaturated colors"

assets:
  reference_images: []
  color_palette_image:
    url: ""
---

## Design Principles

Everything is a pixel. Movement is discrete, never continuous.
Colors are pure and saturated. The arcade cabinet is the frame.

## Extraction Notes

Extracted from video keyframes.
Color palette based on original Pac-Man game (1980).
Motion patterns reflect 8-bit hardware limitations as aesthetic choice.
```

## Tips

- **Focus on what's consistent** — Ignore unique content, find the system
- **Motion is primary** — Video styles are defined by how things move
- **Describe the rhythm** — Is it quick cuts or slow fades?
- **Note the easing** — Does it snap, bounce, or glide?
- **Reference the era** — Many video styles reference specific decades or genres
