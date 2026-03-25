# Advanced Prompt Craft

> ⚠️ **EXPERIMENTAL:** These advanced techniques (5-layer B-roll, motion vocabulary) have not been validated against Video Agent output. Use with caution. The main SKILL.md techniques are tested and proven.

Production-quality prompts for scene-by-scene control. Load this when the user wants cinematic or highly polished output beyond standard narrator videos.

## When to Use This

- User asks for "production quality" or "cinematic" results
- Video is longer than 90 seconds
- User wants specific visual styles or B-roll
- Iterating on a video that needs more visual polish

## The Core Insight

Video Agent is an HTML interpreter. It renders layouts, typography, and structured content natively. Describe B-roll as layered text motion graphics with action verbs ("slams in," "types on," "counts up"). NOT as layout specs ("upper-left, 48pt").

## Prompt Anatomy (Production Quality)

```
FORMAT:    What kind of video, how long, what energy
TONE:      Emotional register, references
AVATAR:    Detailed physical + environment description (60-100 words)
STYLE:     Named aesthetic with colors, typography, motion rules, transitions
CRITICAL ON-SCREEN TEXT:  Exact strings that must appear literally
SCENE-BY-SCENE:  Individual scene breakdowns with VO and layered visuals
MUSIC:     Genre, reference artists, energy arc
NARRATION STYLE:  How to deliver the voiceover
```

### Example FORMAT + TONE

```
FORMAT: 75-second high-energy tech briefing. Think: a creator who just got amazing news.
TONE: Confident, direct, data-backed. Highlights hit hard. Lowlights are honest.
```

### Critical On-Screen Text

List every exact string. Without this, the agent may rephrase, summarize, or round numbers.

```
CRITICAL ON-SCREEN TEXT (display literally):
- "$141M ARR — All-Time High"
- "1.85M Signups — +28% MoM"
- Quote: "Use technology to serve the message." — Shalev Hani
```

## Scene Types

| Type | Format | When |
|------|--------|------|
| **A-ROLL** | Avatar speaking to camera | Intros, key insights, CTAs, emotional beats |
| **FULL SCREEN B-ROLL** | No avatar, motion graphics only | Data visualization, info-dense content |
| **A-ROLL + OVERLAY** | Split frame: avatar + content | Presenting data while maintaining human connection |

**Rotation is mandatory.** Never 3+ of the same type in a row. At least 2 pure B-roll scenes per video.

**Voiceover on EVERY scene.** Silent B-roll = broken video.

### Scene Templates

**A-ROLL:**
```
SCENE 1 — A-ROLL (10s)
[Avatar center-frame, excited, hands gesturing]
VOICEOVER: "The exact script for this scene."
Lower-third: "TITLE TEXT" white on blue bar.
```

**B-ROLL with 5 layers:**
```
SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "The exact script for this scene."
LAYER 1: Dark #1a1a1a background with subtle grid lines pulsing.
LAYER 2: "HEADLINE" SLAMS in from left in white Bold 100pt at -5 degrees.
LAYER 3: Three data cards CASCADE from right, staggered 0.3s.
LAYER 4: Bottom ticker SLIDES in: "supporting text scrolling."
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

## Visual Layer System

Every B-roll scene needs 4+ layers. Every element must MOVE.

| Layer | Purpose | Examples |
|-------|---------|---------|
| L1 | Background | Textured surface, grid, gradient |
| L2 | Hero content | Main headline/number dominating the frame |
| L3 | Supporting data | Cards, stats, bullet points |
| L4 | Information bar | Tickers, labels, attributions |
| L5 | Effects | Particles, glitches, ambient motion |

## Motion Vocabulary

### High Energy
- **SLAMS** — `"$95M" SLAMS in from left at -5 degrees`
- **CRASHES** — `Title CRASHES in from right, screen-shake on impact`
- **PUNCHES** — `Quote card PUNCHES up from bottom`
- **STAMPS** — `Data blocks STAMP in staggered 0.4s`

### Medium Energy
- **CASCADE** — `Three cards CASCADE from top, staggered 0.3s`
- **SLIDES** — `Ticker SLIDES in from right, continuous scroll`
- **FILLS** — `Progress bar FILLS 0 to 90% in orange`
- **DRAWS** — `Chart line DRAWS itself left to right`

### Low Energy
- **types on** — `Quote types on word by word in italic white`
- **fades in** — `Logo fades in at center, held 3 seconds`
- **COUNTS UP** — `"1.85M" COUNTS UP from 0 in amber 96pt`

## Avatar Description Guide

The avatar is NOT a fixed headshot. Design it for each video like a costume + set designer.

| Element | Weak | Strong |
|---------|------|--------|
| Clothing | "Business casual" | "Black ribbed merino turtleneck, high collar framing jaw" |
| Environment | "An office" | "Glass-walled conference room. Whiteboard with hand-drawn diagrams" |
| Monitors | "Computer screens" | "Monitor shows scrolling green terminal text and red alerts" |
| Lighting | "Well lit" | "Cool blue monitor glow from left, warm amber desk lamp from right" |

## Timing Guidelines

| Content Type | Duration |
|---|---|
| Hook/Intro A-roll | 6-10 seconds |
| Data-heavy B-roll | 10-15 seconds (NEVER ≤5s — causes black frames) |
| A-roll + Overlay | 8-12 seconds |
| CTA / Close A-roll | 6-8 seconds |

**Common video lengths:** Social clip: 30-45s (5-7 scenes) | Briefing: 60-75s (7-9 scenes) | Deep dive: 90-120s (10-13 scenes)

## What Doesn't Work

- **Layout coordinates** — "upper-left: headline in 48pt" produces blank frames. Use motion verbs instead.
- **Named artists without specs** — "Ikko Tanaka style" means nothing. Translate to concrete rules.
- **B-roll under 5 seconds** — Always causes black/empty frames. Use 10-15s minimum.
- **Static elements** — Every element must have a motion verb. No static frames.

## Top 5 Performing Styles (from 40+ videos)

1. **Deconstructed (Brody)** — Most reliable across all topics
2. **Swiss Pulse (Müller-Brockmann)** — Best for data-heavy content
3. **Digital Grid (Crouwel)** — Strong for tech topics
4. **Geometric Bold (Tanaka)** — Elegant and versatile
5. **Maximalist Type (Scher)** — High energy, use sparingly
