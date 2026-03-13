---
name: prompt-optimizer
description: Write production-quality prompts for HeyGen Video Agent — from basic ideas to fully art-directed scene-by-scene scripts
---

# Video Agent Prompt Optimizer

Write effective prompts for the HeyGen Video Agent API. Based on patterns from 40+ produced videos.

**The core insight: Video Agent is an HTML interpreter.** It renders layouts, typography, and structured content natively. Describe B-roll as layered text motion graphics with action verbs ("slams in," "types on," "counts up") — not layout specs ("upper-left, 48pt").

## Reference Files

| File | Load when... |
|------|-------------|
| [visual-styles.md](visual-styles.md) | Choosing a visual style (20 styles with full specs) |
| [prompt-examples.md](prompt-examples.md) | Writing a prompt from scratch (full production example + templates) |

## Workflow: Brief to Prompt

1. **Pull data** — Research the topic: web search, APIs, internal docs. Gather real quotes, stats, handles
2. **Synthesize a thesis** — Not a list. A story. *"X is happening because Y — here's the proof."* Group into 3-5 themes with a narrative arc
3. **Choose a style** — Match mood first, content second. Ask: *"What should the viewer FEEL?"* See [visual-styles.md](visual-styles.md)
4. **Write the avatar** — Thematic wardrobe matching content's emotional context. Brand logos and content-specific props in the set (see Avatar Guide below)
5. **Extract critical text** — List every number, quote, handle, and label that must appear literally
6. **Break into scenes** — One concept per scene. Rotate scene types. Never 3+ of same type in a row. At least 2 pure B-roll scenes
7. **Write voiceover** — Spell out numbers in VO ("one-point-eight-five million"), use figures on screen ("1.85M"). Narration on EVERY scene including B-roll
8. **Layer each B-roll scene** — L1 background, L2 hero, L3 supporting, L4 info bar, L5 effects. Every element must MOVE
9. **Add music direction** — Reference artists, describe energy arc
10. **Add narration style** — How to deliver: fast/slow, where to pause, emotional register per section

## Prompt Anatomy

Every production-quality prompt follows this structure:

```
FORMAT:    What kind of video, how long, what energy
TONE:      Emotional register, references
AVATAR:    Detailed physical + environment description (60-100 words)
STYLE:     Named aesthetic with colors, typography, motion rules, transitions
CRITICAL ON-SCREEN TEXT:  Exact strings that must appear
SCENE-BY-SCENE:  Individual scene breakdowns with VO and layered visuals
MUSIC:     Genre, reference artists, energy arc
NARRATION STYLE:  How to deliver the voiceover
```

### FORMAT

```
FORMAT: 75-second high-energy tech daily briefing. Think: a creator who just got amazing news.
FORMAT: Bloomberg-style strategy briefing. 100-120 seconds. CEO-delivered.
```

### TONE

```
TONE: Confident, direct, data-backed. Highlights hit hard. Lowlights are honest — no spin.
TONE: Edgy, punk tech commentary. Vice News meets The Face magazine — raw, confrontational.
```

### CRITICAL ON-SCREEN TEXT

List every exact string that must appear on screen. Without this, the agent may summarize, round numbers, or rephrase quotes.

```
CRITICAL ON-SCREEN TEXT (display literally):
- "$141M ARR — All-Time High"
- "1.85M Signups — +28% MoM"
- Quote: "Use technology to serve the message, not distract from it." — Shalev Hani
- "@username" — exact social handle
```

### MUSIC & NARRATION

```
MUSIC: Driving electronic, heavy bass drops on key numbers. Run the Jewels meets
a tech keynote. Builds relentlessly, only softens for customer stories.

NARRATION STYLE: High energy throughout. Let numbers PUNCH — pause before big ones,
then deliver hard. Customer stories get warmth. The close should feel like a mic drop.
```

## Avatar Description Guide

**The avatar is NOT a fixed headshot** — design it for each video like a movie character. Think costume designer + set designer.

### Thematic Wardrobe Rule

The avatar's outfit and environment MUST match the content's emotional/cultural context:

| Content Type | Avatar Design | NOT This |
|---|---|---|
| Chinese New Year | Red qipao with gold embroidery, lantern-lit courtyard | "Reporter in a blazer" |
| Breaking tech news | Field reporter, windswept hair, earpiece, city skyline | "Anchor at a desk" |
| Sleep science | Oversized cream knit, cross-legged on bed, warm lamp | "Analyst in a lab" |
| Reddit community | Messy desk, Reddit alien on monitors, upvote arrows on wall | "Researcher in a studio" |

### What to Specify

| Element | Weak | Strong |
|---------|------|--------|
| Clothing | "Business casual" | "Black ribbed merino turtleneck, high collar framing jaw" |
| Environment | "An office" | "Glass-walled conference room. Whiteboard with hand-drawn tier pyramid" |
| Monitor content | "Computer screens" | "Monitor shows scrolling green terminal text and red security alerts" |
| Lighting | "Well lit" | "Cool blue monitor glow from left, warm amber desk lamp from right" |

### Template

```
AVATAR: [Clothing — fabric, color, fit, accessories, posture].
[Setting — specific props, brand logos, what's on the walls].
[Monitors/desk — content visible on screens, items on desk].
[Lighting — direction, color temperature]. [Mood of the space].
60-100 words. 3+ content-specific props. Brand elements visible.
```

## Scene Types

| Type | Format | When to Use |
|------|--------|-------------|
| **A-ROLL** | Avatar speaking to camera | Intros, key insights, CTAs, emotional beats |
| **FULL SCREEN B-ROLL** | No avatar — motion graphics only | Data visualization, information-dense content |
| **A-ROLL + OVERLAY** | Split frame: avatar + content | Presenting data while maintaining human connection |

**Rotation is mandatory.** Never 3+ of the same type in a row. Every prompt needs at least 2 pure B-roll scenes.

**Voiceover on EVERY scene.** Every B-roll scene MUST include a `VOICEOVER:` line. Silent B-roll = broken video.

### Scene Anatomy

**A-ROLL:**
```
SCENE 1 — A-ROLL (10s)
[Avatar center-frame, excited, hands gesturing]
VOICEOVER: "The exact script for this scene."
Lower-third: "TITLE TEXT" white on blue bar.
```

**B-ROLL with layers:**
```
SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "The exact script for this scene."
LAYER 1: Dark #1a1a1a background with subtle grid lines pulsing.
LAYER 2: "HEADLINE" SLAMS in from left in white Bold 100pt at -5 degrees.
LAYER 3: Three data cards CASCADE from right, staggered 0.3s.
LAYER 4: Bottom ticker SLIDES in: "supporting text scrolling continuously."
LAYER 5: Grid lines RIPPLE outward from impact point.
Hard cut.
```

**A-ROLL + OVERLAY:**
```
SCENE 3 — A-ROLL + OVERLAY (10s)
[SPLIT — Avatar LEFT 35%. Content RIGHT 65%. NO overlap.]
Avatar gestures toward content side.
VOICEOVER: "The exact script for this scene."
RIGHT SIDE: "HEADLINE" in cyan 60pt. Three stats COUNT UP below.
```

Alternate which side the avatar appears on between overlay scenes.

## The Visual Layer System

Break B-roll into 5 stacked layers. This is the most powerful technique for motion graphics scenes.

| Layer | Purpose | Examples |
|-------|---------|---------|
| **L1** | Background | Textured surface, grid, gradient, color field |
| **L2** | Hero content | Main headline/number that dominates the frame |
| **L3** | Supporting data | Cards, stats, bullet points, secondary information |
| **L4** | Information bar | Tickers, labels, source attributions, quotes |
| **L5** | Effects | Particles, glitches, grid animations, ambient motion |

Every B-roll: 4+ layers. Every overlay content side: 3+ layers. **Every element must MOVE.**

## Motion Vocabulary

### High Energy
| Verb | Example |
|------|---------|
| **SLAMS** | `"$95M" SLAMS in from left at -5 degrees` |
| **CRASHES** | `Title CRASHES in from right, screen-shake on impact` |
| **PUNCHES** | `Quote card PUNCHES up from bottom` |
| **STAMPS** | `Data blocks STAMP in staggered 0.4s` |
| **SHATTERS** | `Text SHATTERS after 1.5s, revealing number underneath` |

### Medium Energy
| Verb | Example |
|------|---------|
| **CASCADE** | `Three cards CASCADE from top, staggered 0.3s` |
| **SLIDES** | `Ticker SLIDES in from right — continuous scroll` |
| **DROPS** | `"TIER 1" DROPS in with white flash` |
| **FILLS** | `Progress bar FILLS 0 to 90% in orange` |
| **DRAWS** | `Chart line DRAWS itself left to right` |

### Low Energy
| Verb | Example |
|------|---------|
| **types on** | `Quote types on word by word in italic white` |
| **fades in** | `Logo fades in at center, held for 3 seconds` |
| **FLOATS** | `Bokeh orbs FLOAT across frame at different speeds` |
| **morphs** | `Number morphs from 17 to 18.9` |
| **COUNTS UP** | `"1.85M" COUNTS UP from 0 in amber 96pt` |

## Transition Types

| Transition | Energy | Styles It Fits |
|------------|--------|---------------|
| Smash cut | Aggressive | Deconstructed, Maximalist, Carnival Surge |
| White flash frame | Punchy | Deconstructed, Maximalist |
| Grid wipe | Systematic | Swiss Pulse, Digital Grid |
| Hard cut | Clean | Swiss Pulse, Shadow Cut |
| Liquid dissolve | Elegant | Data Drift, Dream State |
| Slow cross-dissolve | Refined | Velvet Standard |
| Pop cut / bounce | Fun | Play Mode, Carnival Surge |
| Snap cut | Urgent | Red Wire, Contact Sheet |
| Soft dissolve | Warm | Soft Signal, Warm Grain, Quiet Drama |
| Iris wipe | Nostalgic | Heritage Reel |

## Timing Guidelines

| Content Type | Duration |
|--------------|----------|
| Hook/Intro (A-roll) | 6-10 seconds |
| Data-heavy B-roll | 10-15 seconds (NEVER ≤5s — causes black frames) |
| A-roll + Overlay | 8-12 seconds |
| CTA / Close (A-roll) | 6-8 seconds |

**Common video lengths:** Social clip: 30-45s (5-7 scenes) | Briefing: 60-75s (7-9 scenes) | Deep dive: 90-120s (10-13 scenes)

**Speaking pace:** ~150 words/minute. Calculate: `words / 150 * 60 = seconds`

## What Doesn't Work

Patterns that consistently produce poor results:

**Layout language** — Screen coordinates cause empty/black B-roll:
```
❌ "UPPER-LEFT: headline in 48pt Helvetica"
❌ "CENTER-SCREEN: display at coordinates (400, 300)"
✅ "135K" SLAMS in from left, white Impact 120pt, fills 40% of frame.
```

**Named artists without specs** — "Ikko Tanaka style" means nothing to Video Agent. Translate to concrete rules:
```
❌ "Use an Ikko Tanaka style"
✅ "Flat color blocks, maximum 3 colors per frame, 60% negative space, typography as primary element"
```

**Style examples injected into prompts** — Full example scenes from a style library confuse the agent. Use the style's **rules**, not example scenes.

**Forced short B-roll (≤5 seconds)** — Too short for rendering. Every tested video with 5s B-roll had empty/black screens. Use 10-15s.

**Content as a list, not a story** — "Here are 5 tweets" produces flat videos. Always synthesize: *"X is happening because Y — here's the proof."*

## Production Insights

### Style Performance (from 40+ videos)

| Rank | Style | Strength |
|------|-------|----------|
| 1 | Deconstructed (Brody) | Most reliable across all topics |
| 2 | Swiss Pulse (Müller-Brockmann) | Best for data-heavy content |
| 3 | Digital Grid (Crouwel) | Strong for tech topics |
| 4 | Geometric Bold (Tanaka) | Elegant and versatile |
| 5 | Maximalist Type (Scher) | High energy, use sparingly |

### Duration by Approach

| Approach | Avg Duration | Quality |
|----------|-------------|---------|
| Natural storyboard + custom avatar | ~106s | Best |
| Natural storyboard, no custom avatar | ~69s | Good |
| Forced short scenes + custom avatar | ~71s | Mixed |
| Layout language prompts | ~48s | Poor |

## Quality Checklist

- [ ] Thesis-driven — story, not bullet points
- [ ] Style named with colors, typography, motion, transitions (see [visual-styles.md](visual-styles.md))
- [ ] Avatar has thematic wardrobe + branded environment (60-100 words)
- [ ] Critical text listed — every stat, quote, label
- [ ] Scenes rotate types — never 3+ same type. At least 2 B-roll scenes
- [ ] Every scene has VOICEOVER — including B-roll
- [ ] B-roll scenes have 4+ layers, every element has motion verbs
- [ ] B-roll scenes are 10-15 seconds (never ≤5s)
- [ ] Brand logos appear when discussing companies
- [ ] Every element moves — no static frames
