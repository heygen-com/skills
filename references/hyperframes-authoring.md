# Composition Authoring — HyperFrames

Full reference for HTML video composition structure, data attributes, layout, animation rules, transitions, and quality checks.

## Composition Structure

### Standalone Composition (index.html)

Put `data-composition-id` directly on a `<div>` inside `<body>`. Do NOT use `<template>` — it hides content and breaks rendering.

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body>
  <div data-composition-id="my-video" data-width="1920" data-height="1080">
    <!-- clips, styles, scripts -->
  </div>
</body>
</html>
```

### Sub-Compositions

Sub-compositions loaded via `data-composition-src` use a `<template>` wrapper:

```html
<template id="my-comp-template">
  <div data-composition-id="my-comp" data-width="1920" data-height="1080">
    <!-- content -->
    <style>
      [data-composition-id="my-comp"] { /* scoped styles */ }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      // tweens...
      window.__timelines["my-comp"] = tl;
    </script>
  </div>
</template>
```

Load in root:
```html
<div id="el-1" data-composition-id="my-comp"
     data-composition-src="compositions/my-comp.html"
     data-start="0" data-duration="10" data-track-index="1"
     data-width="1920" data-height="1080"></div>
```

## Data Attributes

### All Clips

| Attribute | Required | Values |
|-----------|----------|--------|
| `id` | Yes | Unique identifier |
| `data-start` | Yes | Seconds or clip ID reference (`"el-1"`, `"intro + 2"`) |
| `data-duration` | Required for img/div/compositions | Seconds. Video/audio defaults to media duration. |
| `data-track-index` | Yes | Integer. Same-track clips cannot overlap. |
| `data-media-start` | No | Trim offset into source (seconds) |
| `data-volume` | No | 0-1 (default 1) |

`data-track-index` does NOT affect visual layering — use CSS `z-index`.

### Composition Clips

| Attribute | Required | Values |
|-----------|----------|--------|
| `data-composition-id` | Yes | Unique composition ID |
| `data-start` | Yes | Start time (root: use `"0"`) |
| `data-duration` | Yes | Takes precedence over GSAP timeline duration |
| `data-width` / `data-height` | Yes | Pixel dimensions (1920x1080 or 1080x1920) |
| `data-composition-src` | No | Path to external HTML file |

## Video and Audio

Video must be `muted playsinline`. Audio is always a separate `<audio>` element:

```html
<video id="el-v" data-start="0" data-duration="30" data-track-index="0"
       src="video.mp4" muted playsinline></video>
<audio id="el-a" data-start="0" data-duration="30" data-track-index="2"
       src="video.mp4" data-volume="1"></audio>
```

## Layout Before Animation

Position every element where it should be at its **most visible moment** — the frame where it's fully entered, correctly placed, and not yet exiting. Write this as static HTML+CSS first. No GSAP yet.

### Process

1. **Identify the hero frame** for each scene — the moment when the most elements are simultaneously visible
2. **Write static CSS** for that frame:
   ```css
   .scene-content {
     display: flex;
     flex-direction: column;
     justify-content: center;
     width: 100%; height: 100%;
     padding: 120px 160px;
     gap: 24px;
     box-sizing: border-box;
   }
   ```
   Use padding to push content inward. NEVER `position: absolute; top: Npx` on content containers. Reserve `position: absolute` for decoratives only.
3. **Add entrances with `gsap.from()`** — animate FROM offscreen/invisible TO the CSS position
4. **Add exits with `gsap.to()`** — animate TO offscreen/invisible FROM the CSS position

### Wrong — hardcoded dimensions:
```css
.scene-content {
  position: absolute; top: 200px; left: 160px;
  width: 1920px; height: 1080px; /* breaks on different canvas sizes */
}
```

## Timeline Contract

- All timelines start `{ paused: true }` — the player controls playback
- Register every timeline: `window.__timelines["<composition-id>"] = tl`
- Framework auto-nests sub-timelines — do NOT manually add them
- Duration comes from `data-duration`, not from GSAP timeline length
- Never create empty tweens to set duration

## Non-Negotiable Rules

1. **Deterministic** — no `Math.random()`, `Date.now()`, or time-based logic. Use seeded PRNG (e.g. mulberry32) if needed.
2. **GSAP visual-only** — animate `opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, transforms. Never `visibility`, `display`, or call `video.play()`/`audio.play()`.
3. **No animation conflicts** — never animate the same property on the same element from multiple timelines simultaneously.
4. **No `repeat: -1`** — calculate exact repeat count: `repeat: Math.ceil(duration / cycleDuration) - 1`.
5. **Synchronous timeline construction** — never build timelines inside `async`/`await`, `setTimeout`, or Promises. Capture engine reads `window.__timelines` synchronously after page load.

### Never Do

1. Forget `window.__timelines` registration
2. Use video for audio — always muted video + separate `<audio>`
3. Nest video inside a timed div — use a non-timed wrapper
4. Use `data-layer` (use `data-track-index`) or `data-end` (use `data-duration`)
5. Animate video element dimensions — animate a wrapper div
6. Call play/pause/seek on media — framework owns playback
7. Create a top-level container without `data-composition-id`
8. Use `repeat: -1` on any timeline or tween
9. Build timelines asynchronously
10. Use `gsap.set()` on clip elements from later scenes — use `tl.set(selector, vars, timePosition)` inside the timeline
11. Use `<br>` in content text — use `max-width` wrapping instead

## Scene Transitions

Every multi-scene composition MUST follow ALL of these rules:

1. **ALWAYS use transitions between scenes.** No jump cuts. No exceptions.
2. **ALWAYS entrance-animate every element** via `gsap.from()`. No element appears fully-formed.
3. **NEVER use exit animations** except on the final scene. The transition IS the exit. Outgoing scene content MUST be fully visible when the transition starts.
4. **Final scene only:** may fade elements out (e.g., fade to black).

### Wrong — exit animation before transition:
```js
// BANNED — empties the scene before the transition can use it
tl.to("#s1-title", { opacity: 0, y: -40, duration: 0.4 }, 6.5);
// transition fires on empty frame
```

### Right — entrance only, transition handles exit:
```js
// Scene 1 entrance
tl.from("#s1-title", { y: 50, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.3);
tl.from("#s1-subtitle", { y: 30, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.6);
// NO exit tweens — transition at 7.2s handles the scene change
// Scene 2 entrance
tl.from("#s2-heading", { x: -40, opacity: 0, duration: 0.6, ease: "expo.out" }, 8.0);
```

## Animation Guardrails

- Offset first animation 0.1-0.3s from t=0
- Vary eases across entrance tweens — at least 3 different eases per scene
- Don't repeat an entrance pattern within a scene
- Avoid full-screen linear gradients on dark backgrounds (H.264 banding — use radial or solid + glow)
- 60px+ headlines, 20px+ body, 16px+ data labels
- `font-variant-numeric: tabular-nums` on number columns

## Typography and Assets

- **Fonts:** Write `font-family` in CSS — the compiler embeds supported fonts automatically
- Add `crossorigin="anonymous"` to external media
- For dynamic text overflow: `window.__hyperframes.fitTextFontSize(text, { maxWidth, fontFamily, fontWeight })`
- All files at project root alongside `index.html`; sub-compositions use `../`

## Editing Existing Compositions

- Read the full composition first — match existing fonts, colors, animation patterns
- Only change what was requested
- Preserve timing of unrelated clips

## Quality Checks

### Contrast Audit

`hyperframes validate` runs WCAG contrast checking. Fix warnings:
- Dark backgrounds: brighten failing color until 4.5:1 (normal) or 3:1 (large text 24px+)
- Light backgrounds: darken it
- Stay within the palette family

### Animation Map

After authoring animations, verify choreography:
```bash
node skills/hyperframes/scripts/animation-map.mjs <dir> --out <dir>/.hyperframes/anim-map
```

Reports: per-tween summaries, ASCII timeline, stagger detection, dead zones (>1s with no animation), element lifecycles, flags (offscreen, collision, invisible, paced-fast/slow).

Skip on small edits. Run on new compositions and significant animation changes.

## Output Checklist

- [ ] `npx hyperframes lint` passes
- [ ] `npx hyperframes validate` passes
- [ ] Contrast warnings addressed
- [ ] Animation choreography verified (for new/major compositions)
