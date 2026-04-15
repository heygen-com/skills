# GSAP Animation — HyperFrames

GSAP (GreenSock Animation Platform) reference for HyperFrames compositions. Covers core methods, easing, timelines, performance, and HyperFrames-specific rules.

## Core Tween Methods

- **`gsap.to(targets, vars)`** — animate from current state to `vars`. Most common.
- **`gsap.from(targets, vars)`** — animate from `vars` to current state (entrances).
- **`gsap.fromTo(targets, fromVars, toVars)`** — explicit start and end.
- **`gsap.set(targets, vars)`** — apply immediately (duration 0).

Always use **camelCase** property names (e.g. `backgroundColor`, `rotationX`).

## Common Vars

| Property | Default | Notes |
|----------|---------|-------|
| `duration` | 0.5 | Seconds |
| `delay` | 0 | Seconds before start |
| `ease` | `"power1.out"` | See Easing section |
| `stagger` | — | Number `0.1` or object: `{ amount: 0.3, from: "center" }` |
| `overwrite` | `false` | `true` or `"auto"` |
| `repeat` | 0 | Count (never `-1` in HyperFrames) |
| `yoyo` | `false` | Alternate direction with repeat |
| `immediateRender` | `true` (from/fromTo) | Set `false` on later tweens targeting same property+element |
| `onComplete` | — | Callback |

## Transform Aliases

Prefer GSAP transform aliases over raw `transform` string:

| GSAP property | Equivalent |
|--------------|------------|
| `x`, `y`, `z` | translateX/Y/Z (px) |
| `xPercent`, `yPercent` | translateX/Y in % |
| `scale`, `scaleX`, `scaleY` | scale |
| `rotation` | rotate (deg) |
| `rotationX`, `rotationY` | 3D rotate |
| `skewX`, `skewY` | skew |
| `transformOrigin` | transform-origin |

- **`autoAlpha`** — prefer over `opacity`. At 0: also sets `visibility: hidden`.
- **CSS variables** — `"--hue": 180`
- **Relative values** — `"+=20"`, `"-=10"`, `"*=2"`
- **Directional rotation** — `"360_cw"`, `"-170_short"`, `"90_ccw"`
- **`clearProps`** — `"all"` or comma-separated; removes inline styles on complete

## Function-Based Values

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  stagger: 0.1,
});
```

## Easing

Built-in eases: `power1`–`power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`. Each has `.in`, `.out`, `.inOut`.

```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

Special: `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"none"` (linear).

## Timelines

### Creating

```javascript
const tl = gsap.timeline({ paused: true, defaults: { duration: 0.5, ease: "power2.out" } });
tl.to(".a", { x: 100 })
  .to(".b", { y: 50 })
  .to(".c", { opacity: 0 });
```

### Position Parameter

Third argument controls placement:

| Syntax | Meaning |
|--------|---------|
| `1` | At 1 second (absolute) |
| `"+=0.5"` | 0.5s after timeline end |
| `"-=0.2"` | 0.2s before timeline end |
| `"intro"` | At label "intro" |
| `"intro+=0.3"` | 0.3s after label |
| `"<"` | Same start as previous tween |
| `">"` | After previous tween ends |
| `"<0.2"` | 0.2s after previous starts |

```javascript
tl.to(".a", { x: 100 }, 0);
tl.to(".b", { y: 50 }, "<");       // same start as .a
tl.to(".c", { opacity: 0 }, "<0.2"); // 0.2s after .b starts
```

### Labels

```javascript
tl.addLabel("intro", 0);
tl.to(".a", { x: 100 }, "intro");
tl.addLabel("outro", "+=0.5");
tl.play("outro");
tl.tweenFromTo("intro", "outro");
```

### Timeline Options

- `paused: true` — **required in HyperFrames** (player controls playback)
- `repeat`, `yoyo` — apply to whole timeline (never `repeat: -1`)
- `defaults` — vars merged into every child tween

### Nesting Timelines

```javascript
const master = gsap.timeline();
const child = gsap.timeline();
child.to(".a", { x: 100 }).to(".b", { y: 50 });
master.add(child, 0);
```

**Note:** In HyperFrames, sub-composition timelines are auto-nested by the framework. Do NOT manually nest them.

### Playback Control

```javascript
tl.play(); tl.pause(); tl.reverse(); tl.restart();
tl.time(2); tl.progress(0.5); tl.kill();
```

## Responsive / Accessibility

```javascript
let mm = gsap.matchMedia();
mm.add({
  isDesktop: "(min-width: 800px)",
  reduceMotion: "(prefers-reduced-motion: reduce)",
}, (context) => {
  const { isDesktop, reduceMotion } = context.conditions;
  gsap.to(".box", {
    rotation: isDesktop ? 360 : 180,
    duration: reduceMotion ? 0 : 2,
  });
});
```

## Performance

### Prefer Transform and Opacity

Animating `x`, `y`, `scale`, `rotation`, `opacity` stays on the compositor. Avoid `width`, `height`, `top`, `left` when transforms achieve the same effect.

### will-change

```css
will-change: transform;  /* only on elements that actually animate */
```

### gsap.quickTo() for Frequent Updates

```javascript
let xTo = gsap.quickTo("#id", "x", { duration: 0.4, ease: "power3" });
let yTo = gsap.quickTo("#id", "y", { duration: 0.4, ease: "power3" });
```

### Stagger > Many Tweens

Use `stagger` instead of separate tweens with manual delays.

## HyperFrames-Specific Rules

1. All timelines start `{ paused: true }`
2. Register every timeline: `window.__timelines["<composition-id>"] = tl`
3. Duration comes from `data-duration`, not GSAP timeline length
4. No `repeat: -1` — calculate exact repeats from composition duration
5. Build timelines synchronously — never inside `async`/`await` or `setTimeout`
6. Only animate visual properties — never `visibility`, `display`, or media playback
7. Use `tl.set()` with a time position for elements from later scenes (not `gsap.set()`)

## Best Practices

- Use camelCase property names; prefer transform aliases and `autoAlpha`
- Prefer timelines over chaining with delay; use the position parameter
- Add labels with `addLabel()` for readable sequencing
- Pass defaults into timeline constructor
- Store tween/timeline return value when controlling playback
- Vary eases across entrance tweens — at least 3 different eases per scene
- Offset first animation 0.1-0.3s from t=0

## Do Not

- Animate layout properties (width/height/top/left) when transforms suffice
- Use both `svgOrigin` and `transformOrigin` on the same SVG element
- Chain animations with `delay` when a timeline can sequence them
- Create tweens before the DOM exists
- Skip cleanup — kill tweens when no longer needed
