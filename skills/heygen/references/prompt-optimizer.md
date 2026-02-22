---
name: prompt-optimizer
description: Write production-quality prompts for HeyGen Video Agent — from basic ideas to fully art-directed scene-by-scene scripts
---

# Video Agent Prompt Optimizer

## Table of Contents
- [Prompt Anatomy](#prompt-anatomy)
- [The Six Sections of a Great Prompt](#the-six-sections-of-a-great-prompt)
- [Visual Style Library](#visual-style-library)
- [Avatar Description Guide](#avatar-description-guide)
- [Scene Types and Layout](#scene-types-and-layout)
- [The Visual Layer System](#the-visual-layer-system)
- [Motion Vocabulary](#motion-vocabulary)
- [Transition Types](#transition-types)
- [Critical On-Screen Text](#critical-on-screen-text)
- [Music and Narration Direction](#music-and-narration-direction)
- [Timing Guidelines](#timing-guidelines)
- [Copy Guidelines](#copy-guidelines)
- [Media Types: When to Use What](#media-types-when-to-use-what)
- [Using Attachments](#using-attachments)
- [Prompt Complexity Levels](#prompt-complexity-levels)
- [Full Example: Brief to Production Prompt](#full-example-brief-to-production-prompt)
- [Ready-to-Use Templates](#ready-to-use-templates)
- [Workflow: Brief to Prompt](#workflow-brief-to-prompt)
- [Optimization Checklist](#optimization-checklist)
- [Common Mistakes](#common-mistakes)

---

The difference between forgettable AI-generated content and professional, broadcast-quality video is how precisely you direct the Video Agent. This guide teaches a layered prompting system — from quick one-liners to fully art-directed productions — based on patterns from the highest-quality videos produced on the platform.

## Prompt Anatomy

Every production-quality prompt follows this structure. Each section gives the Video Agent a different type of instruction:

```
FORMAT:    What kind of video, how long, what energy
TONE:      Emotional register, references
AVATAR:    Detailed physical + environment description
STYLE:     Named aesthetic with colors, typography, motion rules, transitions
CRITICAL ON-SCREEN TEXT:  Exact strings that must appear
SCENE-BY-SCENE:  Individual scene breakdowns with VO and layered visuals
MUSIC:     Genre, reference artists, energy arc
NARRATION STYLE:  How to deliver the voiceover
```

You don't need every section for every video. But the more you include, the more control you have over the output. The sections below explain each one in detail.

## The Six Sections of a Great Prompt

### 1. FORMAT

Sets the video type, duration, and energy level in one line.

```
FORMAT: 75-second high-energy tech daily briefing. Think: a creator who just got amazing news.
FORMAT: Bloomberg-style strategy briefing. 100-120 seconds. CEO-delivered.
FORMAT: 60-second Beacon Signal — punchy tech product comparison. MKBHD meets Bloomberg.
```

**What to include:** Duration, genre/format reference, energy level, and optionally a pop-culture comparison that sets the vibe.

### 2. TONE

Defines the emotional quality of the narration and visuals.

```
TONE: Confident, direct, data-backed. Highlights hit hard. Lowlights are honest — no spin.
TONE: Measured, authoritative, premium. Every word carries weight. Confidence from understatement.
TONE: Edgy, punk tech commentary. Vice News meets The Face magazine — raw, confrontational.
```

### 3. AVATAR

Describe your presenter in cinematic detail. The more specific, the better the result.

See [Avatar Description Guide](#avatar-description-guide) below.

### 4. STYLE

Name a visual style, reference an artist/designer, and specify exact color codes, typography, motion rules, and transition types.

See [Visual Style Library](#visual-style-library) below.

### 5. CRITICAL ON-SCREEN TEXT

List every exact string that must appear as readable text in the video.

See [Critical On-Screen Text](#critical-on-screen-text) below.

### 6. SCENE-BY-SCENE

Break the video into individual scenes with scene type, visual layers, voiceover script, and duration.

See [Scene Types and Layout](#scene-types-and-layout) and [The Visual Layer System](#the-visual-layer-system) below.

---

## Visual Style Library

**The single most impactful thing you can do is name a visual style.** Give it a name, reference a designer or aesthetic movement, and define its colors, typography, motion, and transitions.

The styles below are **examples to use directly or as inspiration for creating your own.** You are not limited to this list — invent new styles by combining elements, referencing other designers, art movements, film genres, or cultural aesthetics. The pattern is what matters: **a named style + designer/movement reference + color palette + typography + motion rules + transition types.**

For example, you could create:
- **"Noir Signal" (Saul Bass)** — high-contrast black/white/red, dramatic shadows, bold silhouettes
- **"Vapor Grid" (Vaporwave)** — pastel gradients, Roman busts, retro computing, VHS scan lines
- **"Paper Cut" (Matisse)** — bold organic shapes, primary colors, hand-cut collage feel
- **"Wire Frame" (Dieter Rams)** — ultra-minimal, thin lines, grey/white/one accent, form follows function

Use the examples below as starting points or pick one that fits your content:

### Swiss Pulse
**Reference:** Josef Muller-Brockmann
**Best for:** Data-heavy briefings, corporate reports, strategy presentations

| Element | Specification |
|---------|--------------|
| **Colors** | Black (#1a1a1a), white, ONE accent: electric blue (#0066FF) |
| **Typography** | Helvetica Bold headlines, Regular labels. Numbers LARGE (80-120pt) |
| **Layout** | Grid-locked compositions. Every element snaps to a 12-column grid |
| **Motion** | Animated counters, progress bars, comparison columns. Numbers COUNT UP from 0 |
| **Accents** | Diagonal compositions on key moments (5-15 degree tilt). Thin grid lines in backgrounds |
| **Transitions** | Grid wipes, hard cuts. No dissolves |

```
STYLE — SWISS PULSE (Muller-Brockmann): Grid-locked layouts, mathematical precision.
Black/white + electric blue #0066FF only. Helvetica Bold headlines. Data-viz hero content.
Animated counters. Diagonal compositions on accent moments. Grid wipe transitions.
```

### Deconstructed
**Reference:** Neville Brody / The Face magazine
**Best for:** Tech news, security alerts, punk energy, raw editorial

| Element | Specification |
|---------|--------------|
| **Colors** | Dark grey (#1a1a1a), black, rust orange (#D4501E or #FF6B35), raw white (#f0f0f0) |
| **Typography** | Type at angles, overlapping edges, escaping frames. Bold industrial |
| **Layout** | High contrast, gritty textures: scratched metal, peeling paint, scan-line glitch |
| **Motion** | Text SLAMS, SHATTERS, PUNCHES. Letters scramble then snap back |
| **Accents** | Diagonal slash marks, glitch flickers, concrete/metal textures |
| **Transitions** | Smash cuts, glitch transitions, white flash frames |

```
STYLE — DECONSTRUCTED (Neville Brody): Dark grey #1a1a1a, black, rust orange #D4501E.
Type at angles, overlapping edges. Gritty textures: scratched metal, scan-line glitch.
Smash cut transitions with flash frames.
```

### Maximalist Type
**Reference:** Paula Scher
**Best for:** High-energy announcements, marketing, social content, celebrations

| Element | Specification |
|---------|--------------|
| **Colors** | Bold saturated: blue (#0066FF), amber (#FF9500), red, yellow, black, white — max contrast |
| **Typography** | Text IS the visual. Overlapping layers at different scales and angles, filling 50-80% of frame |
| **Layout** | Text layered OVER real footage — never on empty backgrounds |
| **Motion** | Everything moving, slamming, sliding. Nothing stays still. 1-2 second clips in montages |
| **Accents** | Flash frames between sections. Numbers that PUNCH on bass hits |
| **Transitions** | Smash cuts, text slamming from edges, flash frames |

```
STYLE — MAXIMALIST TYPE (Paula Scher): Red, yellow, black, white — max contrast.
Text IS the visual. Overlapping at different scales and angles, 50-80% of frame.
Kinetic energy: everything moving, slamming, sliding. Smash cuts, flash frames.
```

### Data Drift
**Reference:** Refik Anadol
**Best for:** Premium reports, visionary content, investor-facing presentations

| Element | Specification |
|---------|--------------|
| **Colors** | Iridescent: holographic silver, electric purple (#7c3aed), cyan (#06b6d4), deep black (#0a0a0a) |
| **Typography** | Thin futuristic sans-serif. Minimal, floating, almost weightless |
| **Layout** | Fluid, morphing compositions. Data that flows like liquid. Extreme scale shifts |
| **Motion** | Particles coalesce into numbers, streams of light trace data paths |
| **Accents** | Reflective luminous surfaces, flowing light, particle clouds |
| **Transitions** | Liquid dissolves, particles dispersing and reforming |

```
STYLE — DATA DRIFT (Refik Anadol): Iridescent palette — purple #7c3aed, cyan #06b6d4,
deep black #0a0a0a. Fluid morphing compositions. Data flows like liquid. Thin futuristic type.
Liquid dissolve transitions. Particles coalesce into numbers.
```

### Velvet Standard
**Reference:** Massimo Vignelli
**Best for:** Premium keynotes, investor updates, luxury brands, understated authority

| Element | Specification |
|---------|--------------|
| **Colors** | Black, white, ONE rich accent — deep navy (#1a237e) or gold (#c9a84c). Nothing else |
| **Typography** | Thin sans-serif, ALL CAPS, letter-spaced wide. Refined, not loud |
| **Layout** | Generous negative space. Symmetrical, centered, architectural precision |
| **Motion** | Slow, deliberate. Numbers fade in with weight. Sequential reveals, not simultaneous |
| **Accents** | Perfect lighting, no visible grain. High production quality. Restraint IS the message |
| **Transitions** | Slow, elegant cross-dissolves. Never jarring. Deliberate pacing |

```
STYLE — VELVET STANDARD (Massimo Vignelli): Black, white, one accent: gold #c9a84c.
Generous negative space. Symmetrical, centered. Thin sans-serif, ALL CAPS, wide letter-spacing.
Slow elegant cross-dissolves. Restraint IS the message.
```

### Carnival Surge
**Reference:** Rico Lins (Brazil)
**Best for:** Social media ads, product launches, celebrations, maximum energy

| Element | Specification |
|---------|--------------|
| **Colors** | Maximum color: hot pink (#FF1493), electric yellow (#FFE000), teal (#00CED1), orange, violet |
| **Typography** | MASSIVE, BOLD, layered at ANGLES over footage. Collage-style overlapping |
| **Layout** | Collage layering with multiple elements overlapping. Never static |
| **Motion** | Rapid 1-2 second clips, confetti bursts, elements bounce and overshoot |
| **Accents** | Confetti particles, flash frames, euphoric celebratory energy |
| **Transitions** | Smash cuts, flash frames, pop cuts |

```
STYLE — CARNIVAL SURGE (Rico Lins): Maximum color — hot pink #FF1493, electric yellow #FFE000,
teal #00CED1, orange, violet. Collage layering. Text MASSIVE at ANGLES. Confetti bursts.
Smash cuts and flash frames. Everything euphoric.
```

### Digital Grid
**Reference:** Wim Crouwel
**Best for:** Tech comparisons, platform analysis, developer content

| Element | Specification |
|---------|--------------|
| **Colors** | Dark backgrounds (#0a0a0a) with cyan (#00E5FF), amber (#FFB300), green (#00FF88) accents |
| **Typography** | Monospaced type throughout. Code-terminal aesthetic |
| **Layout** | Pixel grid overlays visible. Everything snaps to a system. Two-color coding for comparisons |
| **Motion** | Grid nodes light up sequentially. Network maps activating. Data pulsing |
| **Accents** | Scan-line effects, cursor blinks, terminal log scrolling |
| **Transitions** | Clean wipe transitions, grid wipes |

```
STYLE — DIGITAL GRID (Wim Crouwel): Monospaced type. Dark #0a0a0a with cyan #00E5FF
and amber #FFB800. Pixel grid overlays. Code-terminal aesthetic. Clean wipe transitions.
```

### Shadow Cut
**Reference:** Brutalist architecture
**Best for:** Confrontational analysis, hard comparisons, dramatic reveals

| Element | Specification |
|---------|--------------|
| **Colors** | Black (#0A0A0A), white (#F5F5F5), ONE accent: blood red (#FF0000). Nothing else |
| **Typography** | Ultra-heavy condensed grotesque. Headlines MASSIVE, filling 70%+ of frame |
| **Layout** | Every frame looks like a protest poster or brutalist architecture |
| **Motion** | HARD CUTS ONLY. No easing. SLAM in, SLAM out. Frames stamped onto screen |
| **Accents** | Concrete textures, newsprint grain. Nothing polished |
| **Transitions** | Hard cuts. Black frame for 2 frames, then SLAM to next scene |

```
STYLE — SHADOW CUT (Brutalist): Black #0A0A0A, white, ONE accent: blood red #FF0000.
Ultra-heavy condensed type filling 70%+ of frame. HARD CUTS ONLY. No easing.
Concrete textures, newsprint grain. Protest poster aesthetic.
```

### Dream State
**Reference:** Henryk Tomaszewski / Polish Poster School
**Best for:** Brand films, artistic content, ethereal storytelling

| Element | Specification |
|---------|--------------|
| **Colors** | Soft neon gradients: lavender to coral, mint to gold. No hard edges |
| **Typography** | Thin elegant sans-serif that FLOATS and DRIFTS. Text breathes — subtle scale oscillation |
| **Layout** | Everything floats. Slow parallax layers at different depths. Soft focus, lens flare |
| **Motion** | Elements morph and dissolve. Slow parallax. Bokeh orbs drift through frame |
| **Accents** | Chromatic aberration at edges. Frosted glass look. Colors bleed like watercolors |
| **Transitions** | NEVER hard cuts. Everything dissolves, morphs, melts into the next scene |

```
STYLE — DREAM STATE (Tomaszewski): Soft neon gradients — lavender to coral, mint to gold.
Thin elegant floating type. Everything drifts at different parallax depths.
Chromatic aberration. NEVER hard cuts — everything melts and morphs.
```

### Play Mode
**Reference:** Gaming/K-pop stream aesthetic
**Best for:** Comparisons as battles, listicles, fun educational content

| Element | Specification |
|---------|--------------|
| **Colors** | Neon pink (#FF2D78), electric blue (#00D4FF), lime green (#7FFF00), hot purple (#BF00FF) |
| **Typography** | Bold with scanline overlay. Glossy with sparkle particles |
| **Layout** | Score cards, achievement popups, XP bars, combo counters |
| **Motion** | Bouncy spring physics on everything — text overshoots and settles, screen shakes on impacts |
| **Accents** | Achievement popup badges, sparkle bursts, "OVER 9000" moments |
| **Transitions** | Pop cuts, whip pans, bounce effects |

```
STYLE — PLAY MODE: Neon pink #FF2D78, electric blue #00D4FF, lime green #7FFF00.
Bouncy spring physics. Score cards, XP bars, achievement popups. Screen shakes on impact.
Glossy scanline overlay, sparkle particles. Pop cuts, bounce effects.
```

---

## Avatar Description Guide

Generic avatar descriptions produce generic results. Describe your presenter like a film director describing a character to a cinematographer.

### What to Specify

| Element | Generic (Weak) | Specific (Strong) |
|---------|----------------|-------------------|
| **Clothing** | "Business casual" | "Black ribbed merino turtleneck, high collar framing jaw" |
| **Accessories** | "Some jewelry" | "Silver geometric pendant, small hoop earrings, thin silver chain" |
| **Environment** | "An office" | "Glass-walled conference room. Whiteboard with hand-drawn tier pyramid" |
| **Desk items** | "A desk" | "Laptop, half-empty flat white, scattered sticky notes" |
| **Monitor content** | "Computer screens" | "Monitor shows scrolling green terminal text and red security alerts" |
| **Lighting** | "Well lit" | "Cool blue monitor glow from left, warm amber desk lamp from right" |

### Template

```
AVATAR: [Clothing in detail]. [Accessories]. [Setting description]. [What's on/behind the desk].
[Monitor content]. [Specific lighting — direction, color, quality]. [Overall mood of the space].
```

### Examples by Tone

**Corporate/Strategic:**
```
AVATAR: Navy slim-fit blazer over dark grey crew-neck tee, no tie, sleeves pushed up.
Glass-walled conference room. Whiteboard behind with hand-drawn framework diagrams.
Floor-to-ceiling windows, dusk skyline. Table with documents, water glass, blue marker.
```

**Tech/Editorial:**
```
AVATAR: Black leather jacket over dark grey vintage tee with faded circuit board graphic.
Small silver hoop earrings, thin silver chain. Industrial workspace — dual monitors showing
Reddit threads and scrolling green terminal text, mechanical keyboard with RGB backlighting,
scattered neon sticky notes, half-empty energy drink. Exposed brick wall, dim neon sign
casting warm orange glow. Warm tungsten desk lamp from left, cool monitor glow from behind.
```

**Premium/Keynote:**
```
AVATAR: Tailored black crew-neck sweater — fine-knit merino, subtle texture visible.
Spacious, architecturally precise room: floor-to-ceiling windows casting diffused natural light,
polished walnut conference table. A single laptop, closed, and a glass of water. Deep charcoal
wall with logo etched in matte finish. One recessed spotlight. Every object intentional.
```

---

## Scene Types and Layout

### Three Scene Types

| Type | Format | When to Use |
|------|--------|-------------|
| **A-ROLL** | Avatar speaking to camera, full frame | Intros, key insights, transitions, CTAs, emotional beats |
| **FULL SCREEN B-ROLL** | No avatar — motion graphics/visuals only | Data visualization, feature showcases, information-dense content |
| **A-ROLL + OVERLAY** | Split frame: avatar on one side, content on the other | Presenting data while maintaining human connection |

### Split Frame Percentages

For A-ROLL + OVERLAY scenes, always specify the split:

```
[SPLIT — Avatar LEFT 35%. Content RIGHT 65%. NO overlap.]
[SPLIT — Avatar RIGHT 30%. Content LEFT 70%.]
```

Alternate which side the avatar appears on between overlay scenes to create visual variety.

### Scene Anatomy

**A-ROLL scene:**
```
SCENE 1 — A-ROLL (10s)
[Avatar center-frame, excited, hands gesturing]
VOICEOVER: "The exact script for this scene."
Lower-third: "TITLE TEXT" white on blue bar.
```

**B-ROLL scene with visual layers:**
```
SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "The exact script for this scene."
LAYER 1: Dark #1a1a1a background with subtle grid lines pulsing.
LAYER 2: "HEADLINE" SLAMS in from left in white Bold 100pt at -5 degrees.
LAYER 3: Three data cards CASCADE from right, staggered 0.3s.
LAYER 4: Bottom ticker SLIDES in: "supporting text scrolling continuously."
LAYER 5: Grid lines RIPPLE outward from impact point. Scan-line glitch flickers.
Hard cut.
```

**A-ROLL + OVERLAY scene:**
```
SCENE 3 — A-ROLL + OVERLAY (10s)
[SPLIT — Avatar LEFT 35%. Content RIGHT 65%. NO overlap.]
Avatar gestures toward content side, impressed expression.
VOICEOVER: "The exact script for this scene."
RIGHT SIDE: "HEADLINE" in cyan 60pt at top. Three stats COUNT UP below.
Quote card with border types on at bottom.
```

---

## The Visual Layer System

**This is the most powerful technique for B-roll scenes.** Instead of describing a scene as one visual, break it into 5 layers that stack on top of each other. The Video Agent can interpret each layer independently.

| Layer | Purpose | Examples |
|-------|---------|---------|
| **LAYER 1** | Background | Textured surface, grid, gradient, color field |
| **LAYER 2** | Hero content | Main headline/number that dominates the frame |
| **LAYER 3** | Supporting data | Cards, stats, bullet points, secondary information |
| **LAYER 4** | Information bar | Tickers, labels, source attributions, quotes |
| **LAYER 5** | Effects | Particles, glitches, grid animations, ambient motion |

### Example

```
LAYER 1: Dark concrete #1a1a1a with industrial scratch textures, subtle scan-line effect.
LAYER 2: "$141M" SLAMS in from left, white Impact 140pt, fills 40% of frame.
         "+28% MoM" appears in amber to the right.
LAYER 3: Three stat cards CASCADE from top-right, staggered 0.3s:
         "$2.12M New Revenue" — "$3.4M Business ARR" — "$3M Pro ARR."
         Each number COUNTS UP from 0.
LAYER 4: Bottom ticker scrolls: "Source: Company Report • Jan 2026 • All-Time Highs"
LAYER 5: Grid lines RIPPLE outward on the "$141M" slam. Diagonal amber bar
         (5 degree tilt) behind stat cards. Scan-line glitch at 0.5s and 1.2s marks.
```

---

## Motion Vocabulary

Use precise verbs to describe how elements enter, move, and exit. Each verb implies a different speed and energy.

### High Energy
| Verb | Meaning | Example |
|------|---------|---------|
| **SLAMS** | Fast, forceful entrance from an edge | `"$95M" SLAMS in from left at -5 degrees` |
| **CRASHES** | Even more forceful, with screen shake | `Title CRASHES in from right, screen-shake on impact` |
| **PUNCHES** | Quick, compact appearance | `Quote card PUNCHES up from bottom` |
| **STAMPS** | Hard placement, no easing, industrial | `Data blocks STAMP in one after another, staggered 0.4s` |
| **SMASHES** | Destructive entry | `"85K+" SMASHES in from bottom-left, tilted 12 degrees` |
| **SHATTERS** | Breaks apart after appearing | `Text SHATTERS after 1.5s, revealing number underneath` |

### Medium Energy
| Verb | Meaning | Example |
|------|---------|---------|
| **CASCADE** | Sequential staggered appearance | `Three cards CASCADE from top, staggered 0.3s` |
| **SLIDES** | Smooth directional movement | `Ticker SLIDES in from right — continuous scroll` |
| **DROPS** | Falls from above with weight | `"TIER 1" DROPS in with white flash` |
| **BUILDS** | Constructs progressively | `Pyramid BUILDS bottom-up from blocks` |
| **FILLS** | Progress bar or area expanding | `Progress bar FILLS 0 to 90% in orange` |
| **DRAWS** | Line or path tracing itself | `Chart line DRAWS itself left to right` |

### Low Energy
| Verb | Meaning | Example |
|------|---------|---------|
| **types on** | Letter-by-letter reveal | `Quote types on word by word in italic white` |
| **fades in** | Gradual opacity increase | `Logo fades in at center, held for 3 seconds` |
| **FLOATS / DRIFTS** | Gentle, weightless movement | `Bokeh orbs FLOAT across frame at different speeds` |
| **materializes** | Appears from particles or nothing | `"AVATAR IV" materializes from abstract particles` |
| **morphs** | Transforms from one shape to another | `Number morphs from 17 to 18.9` |
| **breathes** | Subtle scale oscillation | `The text breathes — gentle scale oscillation` |

### Counting
| Verb | Meaning | Example |
|------|---------|---------|
| **COUNTS UP** | Animated number incrementing | `"1.85M" COUNTS UP from 0 in amber 96pt` |
| **counts down** | Animated number decrementing | `Timer COUNTS DOWN from 5:00` |

### Timing Modifiers

Add stagger timing to sequential animations:
```
Three cards CASCADE from right, staggered 0.3s
Five items STAMP in one after another, staggered 0.4s
```

Add angle modifiers to entries:
```
"HEADLINE" SLAMS in from left at -5 degrees, white Impact 100pt
Title crashes in at +3 degrees, filling 60% of frame
```

---

## Transition Types

Match your transitions to your visual style:

| Transition | Energy | Styles It Fits |
|------------|--------|---------------|
| **Smash cut** | Aggressive | Deconstructed, Maximalist, Carnival Surge |
| **White flash frame** | Punchy | Deconstructed, Maximalist |
| **Grid wipe** | Systematic | Swiss Pulse, Digital Grid |
| **Hard cut** | Clean | Swiss Pulse, Shadow Cut |
| **Liquid dissolve** | Elegant | Data Drift, Dream State |
| **Particle dissolve** | Premium | Data Drift |
| **Slow cross-dissolve** | Refined | Velvet Standard |
| **Glitch transition** | Raw | Deconstructed |
| **Clean wipe** | Technical | Digital Grid |
| **Pop cut / bounce** | Fun | Play Mode, Carnival Surge |

Specify transitions at the end of each scene:
```
Smash cut — white flash.
Grid wipe.
Liquid dissolve to next scene — colors bleed into each other.
Hard cut — black frame for 2 frames, then SLAM to next.
```

---

## Critical On-Screen Text

**Always list exact strings that must appear on screen.** This prevents the agent from paraphrasing your data or quotes.

Place this section before your scene-by-scene breakdown:

```
CRITICAL ON-SCREEN TEXT (display literally):
- "$141M ARR — All-Time High"
- "1.85M Signups — +28% MoM"
- Quote: "Use technology to serve the message, not distract from it." — Shalev Hani
- "@username" — exact social handle
- "SOC 2 Type II Certified"
```

**Why this matters:** Without explicit text, the agent may summarize, round numbers, or rephrase quotes. This section ensures data integrity and brand accuracy.

---

## Music and Narration Direction

### Music
Specify genre, reference artists, and energy arc:

```
MUSIC: Driving electronic, heavy bass drops on key numbers. Run the Jewels meets
a tech keynote. Builds relentlessly, only softens for customer stories, then
hammers back for the close.
```

```
MUSIC: Minimal ambient piano with subtle electronic undertones. Nils Frahm meets
a premium brand film. Elegant, unhurried, building slowly. No drops — just gradual swell.
```

```
MUSIC: Upbeat electronic with a driving beat. Tycho meets Bloomberg opening theme.
Builds through highlights, warms for stories, peaks on close.
```

### Narration Style
Add a closing section describing HOW to deliver the voiceover:

```
NARRATION STYLE: High energy throughout. Let numbers PUNCH — pause before big ones,
then deliver hard. Customer stories get warmth. Lowlights are fast and honest.
The close should feel like a mic drop.
```

```
NARRATION STYLE: Measured, deliberate. Every word earns its place. Customer stories
get warmth but not sentimentality. Lowlights delivered with clarity. The close is
understated — confidence, not bravado.
```

---

## Timing Guidelines

| Content Type | Recommended Duration |
|--------------|---------------------|
| Hook/Intro (A-roll) | 6-10 seconds |
| Data-heavy B-roll | 10-15 seconds |
| A-roll + Overlay | 8-12 seconds |
| Story/narrative B-roll | 10-12 seconds |
| Quick transition A-roll | 5-6 seconds |
| CTA (A-roll) | 6-8 seconds |
| End Card | 3-5 seconds |

**Calculating duration from script:** ~150 words/minute speaking pace.

```
Words / 150 * 60 = Duration in seconds
```

**Common video lengths:**
- Social clip: 30-45 seconds (5-7 scenes)
- Standard briefing: 60-75 seconds (7-9 scenes)
- Deep dive: 90-120 seconds (10-13 scenes)

---

## Copy Guidelines

Apply these rules to VO scripts and text overlays:

| Rule | Do | Don't |
|------|-----|-------|
| Ampersands | Spell out "and" | Use & (except known terms like L&D) |
| Acronyms | Spell out on first use | Jump straight to acronym |
| Numbers in VO | Spell out: "one-point-eight-five million" | Say "1.85M" |
| Numbers on screen | Use figures: "1.85M" | Write out "one point eight five million" |
| Lists | Use Oxford comma | Skip final comma |
| Headlines | Sentence case | Title Case Every Word |
| CTAs | 3-4 words, no punctuation | Long CTAs with periods |

**Length limits:**
- Headlines: 35-55 characters max
- Body copy: 20-30 words per section
- CTAs: 3-4 words max
- Ticker text: continuous, concise phrases separated by bullets

---

## Media Types: When to Use What

| Content Type | Motion Graphics | AI Generated | Stock Media |
|--------------|:---------------:|:------------:|:-----------:|
| Data/Statistics | **Best** | - | - |
| Abstract Concepts | Good | **Best** | - |
| Real Environments | - | Can work | **Best** |
| Brand Elements | **Best** | - | - |
| Human Emotions | - | Uncanny | **Best** |
| UI/Product Demos | **Best** | - | - |
| Code/Technical | **Best** | - | - |
| Futuristic/Conceptual | Good | **Best** | - |
| Industry Context | - | - | **Best** |

**Production-level prompt rule:** In most cases, motion graphics B-roll with layered text produces more professional results than stock footage or AI-generated imagery. Default to motion graphics unless the scene specifically needs real-world footage or an abstract visual that text can't convey.

---

## Using Attachments

Upload files to help Video Agent understand your content:

| Type | Use For |
|------|---------|
| Images | Product screenshots, diagrams, brand assets |
| Videos | Existing footage, demo recordings |
| PDFs | Training materials, research, product docs |
| Photos | Your own photo to use as avatar |

**Critical: Always add context** about how attachments should be used:

```
Use the attached product screenshots as B-roll when discussing features.
Reference the attached PDF for accurate technical specifications.
The company logo should appear in the intro and outro.
```

---

## Prompt Complexity Levels

Not every video needs full art direction. Match your prompt depth to your needs:

### Level 1: Quick Prompt (10 seconds to write)
```
Create a 60-second product demo for our AI calendar app.
Target: busy professionals. Tone: professional but friendly.
Highlight smart scheduling and time zone handling.
CTA: Visit our website to start free trial.
```

### Level 2: Script-Driven (5 minutes to write)
Paste your full script with scene type hints. Let Video Agent handle visuals:

```
Intro (A-roll, motion graphics overlay)
VO: "If your work is mostly explaining things, video helps — but making it takes too much time."

Problem (B-roll motion graphics)
VO: "Traditional video production requires cameras, editing software, and hours of work."

Solution (A-roll)
VO: "Our platform turns your ideas into production-ready videos in minutes."

CTA (A-roll, end beat)
VO: "Try it free today."

End card: [Your Brand] - Make Video Easy
```

### Level 3: Art-Directed (15-30 minutes to write)
Full FORMAT + STYLE + AVATAR + SCENES + LAYERS. This is what produces broadcast-quality results. See the full example below.

---

## Full Example: Brief to Production Prompt

### Input Brief

```
Topic: Monthly company report for a SaaS startup
Key data: $141M ARR (up from $54M), 1.85M signups (+28%), 3M paid videos/month
Customer story: Creator built AI character, 2.5M followers, 20 min/video
Challenge: Organic traffic volatile, -16% last week
Duration: ~90 seconds
Tone: Confident CEO, data-backed
```

### Output Prompt

```
FORMAT: Bloomberg-style company report. 90 seconds. Fast-paced, data-dense.
Record-breaking month. Proud but analytical.

TONE: Confident, direct, data-backed. Highlights hit hard with numbers.
Customer stories are the emotional core. Challenges are honest — no spin.

AVATAR: Man in simple black crew-neck tee, standing in a modern glass-walled
office at golden hour. Behind him, a wall-mounted display shows the company logo
in soft blue glow. Monitor to his right shows a dashboard with upward-trending
charts. Desk beside him: laptop, half-empty flat white, scattered sticky notes.
Warm afternoon light through floor-to-ceiling windows, long shadows on polished
concrete. Minimal, focused startup HQ.

STYLE — SWISS PULSE (Muller-Brockmann): Grid-locked compositions. Black (#1a1a1a),
white, electric blue (#0066FF), warm amber (#FF9500) for records. Helvetica Bold
headlines, Regular labels. Numbers LARGE. Animated counters count up from 0.
Diagonal compositions on accent moments. Grid wipe transitions. No dissolves.

CRITICAL ON-SCREEN TEXT (display literally):
- "1.85M SIGNUPS — +28% MoM"
- "$2.12M NEW SUBSCRIPTION REVENUE"
- "$54M → $141M ARR"
- "2.5M FOLLOWERS" and "20 MIN / VIDEO"
- Quote: "Use technology to serve the message, not distract from it."
- "ORGANIC: 65% OF SUBS — VOLATILE"

MUSIC: Upbeat electronic with a driving beat. Tycho meets Bloomberg opening theme.
Builds through highlights, warms for customer story, softens for challenges, peaks
on close.

---

SCENE 1 — A-ROLL (8s)
[Avatar center-frame, energetic, leaning slightly forward]
VOICEOVER: "January was a record month. New highs across acquisition, revenue,
and product velocity. Here's the full picture."
Lower-third SLIDES in: "COMPANY NAME | JANUARY 2026" white on blue bar.
Grid wipe.

SCENE 2 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "One-point-eight-five million signups — twenty-eight percent month
over month. Two-point-one-two million in new subscription revenue. Both all-time
highs."
LAYER 1: Dark #1a1a1a background with thin grid lines pulsing at 8% opacity.
LAYER 2: "1.85M" SLAMS in from left, white Bold 140pt. "SIGNUPS" types on
         in electric blue 32pt uppercase. "+28% MoM" appears in amber.
LAYER 3: Three stat cards CASCADE from top-right, staggered 0.3s:
         "$2.12M New Revenue" — "$3.4M Business ARR" — "$3M Pro ARR."
         Each number COUNTS UP from 0.
LAYER 4: Bottom ticker scrolls: "Non-brand search +36% • Brand impressions 9.2M
         • Weekly subs +20.5%"
LAYER 5: Grid lines RIPPLE outward on "1.85M" slam. Diagonal amber bar behind
         stat cards.
Hard cut.

SCENE 3 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic only]
VOICEOVER: "Zoom out. Twelve months ago — fifty-four million ARR. Today —
one hundred forty-one million. Nearly three X in a single year."
LAYER 1: Dark background, subtle grid scrolling upward.
LAYER 2: Animated line chart DRAWS ITSELF left to right. Y-axis: $50M to $150M.
         Final point "$140.84M" glows amber and pulses.
LAYER 3: Milestone annotations float in at key data points.
LAYER 4: Second smaller chart below — "Paid Videos" 0.91M to 2.97M, same
         animation style.
LAYER 5: Thin grid lines converge toward final data point. Scan line sweeps.
Grid wipe.

SCENE 4 — A-ROLL (8s)
[Avatar center-frame, warm tone, genuine smile]
VOICEOVER: "But the numbers only tell half the story. The other half is the
people building on the platform."
Lower-third: "Customer Spotlight"

SCENE 5 — FULL SCREEN B-ROLL (12s)
[NO AVATAR — motion graphic, warm palette]
VOICEOVER: "An AI character built entirely on the platform. Twenty minutes
per video. Two-point-five million Instagram followers. The creator's principle:
use technology to serve the message, not distract from it."
LAYER 1: Dark background with warm amber grid lines at low opacity.
LAYER 2: "CHARACTER NAME" in large white, center-top, 80pt.
LAYER 3: Stats cascade from right: "2.5M Followers" COUNTS UP in amber —
         "20 min/video" — "7x Faster." Each a glowing node.
LAYER 4: Quote card SLIDES UP from bottom: "Use technology to serve the
         message, not distract from it." Types on word by word.
LAYER 5: Warm light bloom. Grid lines soften into curved arcs.
Grid wipe.

SCENE 6 — A-ROLL (10s)
[Avatar center-frame, serious/candid]
VOICEOVER: "Now the honest part. Organic drives sixty-five percent of
subscriptions and it's volatile. Non-brand traffic dropped sixteen percent
last week. We've rebuilt attribution and we're investing in SEO."
Lower-third: "Challenges"

SCENE 7 — A-ROLL (7s)
[Avatar center-frame, energy lifts, direct eye contact]
VOICEOVER: "Fifty-four million to one-forty-one in twelve months. Three million
paid videos a month. January set the bar — now we raise it."
End card: Logo centered, blue glow fade-in. Grid lines converge. Music peaks.

---

NARRATION STYLE: CEO energy — conviction backed by data. Fast on highlights.
Warm on customer stories. Candid on challenges. Close with forward momentum,
not a victory lap.
```

---

## Ready-to-Use Templates

### Tech News Briefing
```
FORMAT: 75-second high-energy tech briefing. Think: Bloomberg meets Vice.

AVATAR: [Presenter in tech-casual clothing at a multi-monitor command station.
Describe clothing, monitors content, desk items, lighting.]

STYLE — DECONSTRUCTED (Neville Brody): Dark grey #1a1a1a, rust orange #D4501E.
Type at angles, overlapping. Gritty textures. Smash cut transitions.

CRITICAL ON-SCREEN TEXT:
- [List every stat, quote, handle that must appear]

SCENE 1 — A-ROLL (8s): Hook with energy. State what's happening.
SCENE 2 — B-ROLL (12s): First story with layered visuals (L1-L5).
SCENE 3 — A-ROLL + OVERLAY (10s): Second story, split frame.
SCENE 4 — B-ROLL (10s): Third story or dramatic data point.
SCENE 5 — A-ROLL (8s): Wrap-up and forward look.
```

### Product Comparison
```
FORMAT: 60-second comparison. [Product A] vs [Product B]. Data-driven.

AVATAR: [Presenter in review studio. Describe desk, monitors showing both products.]

STYLE — DIGITAL GRID (Wim Crouwel): Dark #0a0a0a, cyan #00D4FF and amber #FFB800.
Two-color coding: cyan = Product A, amber = Product B. Monospaced type.

CRITICAL ON-SCREEN TEXT:
- [Key stats for each product]
- [Pricing, features, differentiators]

Use SPLIT FRAME B-roll scenes with Product A data on left, Product B on right.
```

### Strategy Presentation
```
FORMAT: 90-second strategy briefing. Bloomberg meets board meeting.

AVATAR: [Executive in blazer over tee. Conference room with whiteboard frameworks.]

STYLE — SWISS PULSE (Muller-Brockmann): Black/white + blue #0066FF.
Grid-locked. Helvetica. Animated counters. Grid wipe transitions.

CRITICAL ON-SCREEN TEXT:
- [Framework labels, axis names, quadrant labels]
- [Key quotes and data points]

Build frameworks visually: draw axes, plot positions, animate labels.
```

### Social Ad (30 seconds)
```
FORMAT: 30-second social ad. Maximum energy. Portrait 9:16.

AVATAR: [Creator-style presenter. Ring light, colorful background.]

STYLE — CARNIVAL SURGE (Rico Lins): Hot pink, yellow, teal. Collage layering.
Text MASSIVE at angles. Confetti. Smash cuts.

Three scenes only: Hook (8s) → Value prop (12s) → CTA (10s).
Text fills 50-80% of every frame. Numbers SLAM.
```

### Premium Report
```
FORMAT: 120-second investor-grade report. Understated authority.

AVATAR: [Tailored merino sweater. Architectural room, diffused natural light.]

STYLE — VELVET STANDARD (Vignelli): Black, white, gold #c9a84c.
Thin sans-serif, ALL CAPS, wide spacing. Generous negative space.
Slow cross-dissolves. Let numbers land with weight.

Numbers fade in one at a time. Never crowd the frame.
```

---

## Workflow: Brief to Prompt

When transforming a creative brief into a Video Agent prompt:

1. **Choose a style** — Pick from the Visual Style Library or define your own with colors, type, motion rules, and transitions
2. **Write the avatar** — Clothing, accessories, environment, monitor content, lighting. Be cinematic
3. **Extract critical text** — List every number, quote, handle, and label that must appear literally
4. **Break into scenes** — One concept per scene. Alternate A-roll and B-roll for visual rhythm
5. **Write voiceover** — Spell out numbers in VO ("one-point-eight-five million"), use figures on screen ("1.85M")
6. **Layer each B-roll scene** — L1 background, L2 hero, L3 supporting, L4 info bar, L5 effects
7. **Add music direction** — Reference artists, describe energy arc
8. **Add narration style** — How to deliver: fast/slow, where to pause, emotional register per section

---

## Optimization Checklist

Before submitting your prompt, verify:

- [ ] **Style named** with colors, typography, motion rules, and transitions
- [ ] **Avatar described** with clothing, environment, lighting, and desk items
- [ ] **Critical text listed** — every stat, quote, and label that must appear literally
- [ ] **Scenes alternate** between A-roll and B-roll for visual variety
- [ ] **B-roll scenes** have 3-5 visual layers (background, hero, supporting, info, effects)
- [ ] **Split frames** specify percentages and which side the avatar occupies
- [ ] **Motion verbs** are specific (SLAMS, CASCADE, types on — not "appears")
- [ ] **Transitions** match the chosen visual style
- [ ] **VO numbers** are spelled out; **on-screen numbers** use figures
- [ ] **Duration** is specified per scene in seconds
- [ ] **Music** has genre, reference artists, and energy arc
- [ ] **Narration style** describes delivery approach

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No named visual style | Pick from the library or define your own with colors + type + motion + transitions |
| Generic avatar: "a person in an office" | Describe clothing fabric, accessories, monitor content, lighting direction |
| Saying "show some stats" | Use the layer system: L1 background, L2 hero number, L3 supporting cards |
| Vague motion: "text appears" | Use specific verbs: SLAMS, CASCADE, types on, COUNTS UP |
| Missing critical text section | List every exact string before the scene breakdown |
| All A-roll or all B-roll | Alternate scene types for visual rhythm |
| B-roll with no layers | Every B-roll scene needs at least 3 layers |
| Same avatar side every overlay | Alternate LEFT/RIGHT between split-frame scenes |
| Numbers in VO as digits | Spell out in voiceover: "one-point-eight-five million" |
| No transition specified | End each scene with a transition that matches your style |
| Forgetting music direction | Add genre, reference artists, and energy arc |
