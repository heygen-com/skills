---
name: buddy-to-avatar
description: |
  Bring your Claude Code Buddy to life as a HeyGen avatar video. Reads your terminal pet's
  species, stats, rarity, and personality, then creates a personified avatar and intro video.
  Chains: buddy-to-avatar → heygen-avatar-designer → heygen-video-producer.
  Use when: (1) "bring my buddy to life", "turn my buddy into a video", "buddy avatar",
  (2) "personify my buddy", "make a video of my buddy", "create an avatar from my buddy",
  (3) "give my buddy a face", "animate my terminal pet", "buddy intro video",
  (4) any mention of Claude Code Buddy + avatar or video in the same request.
  NOT for: general avatar creation (use heygen-avatar-designer), general video (use heygen-video-producer).
argument-hint: "[paste /buddy card output or screenshot]"
---

# Buddy to Avatar

Turn a Claude Code Buddy into a personified HeyGen avatar and intro video.

**Required:** `HEYGEN_API_KEY` env var.
**Chain:** This skill produces an AVATAR file, then hands off to heygen-video-producer.

## Skill Announcement

> 🐧 **Using: buddy-to-avatar** — bringing your Claude Code Buddy to life

## Phase 1 — Capture Buddy

Get the buddy's stats. Three input methods (try in order):

1. **Screenshot** — User pastes a screenshot of `/buddy card`. Parse visually.
2. **Text paste** — User pastes the text output of `/buddy card`. Parse directly.
3. **Manual** — Ask: "What's your buddy's species, name, rarity, and stats?"

**Required fields:**

| Field | Source | Example |
|-------|--------|---------|
| Species | One of 18 | penguin, owl, dragon, axolotl... |
| Name | LLM-generated at hatch | Bramble, Nebula, Zinc... |
| Rarity | Common/Uncommon/Rare/Epic/Legendary | Common |
| Shiny | Boolean | No |
| Personality | Quote from buddy card | "A manic penguin who..." |
| DEBUGGING | 0-100 | 23 |
| PATIENCE | 0-100 | 1 |
| CHAOS | 0-100 | 77 |
| WISDOM | 0-100 | 27 |
| SNARK | 0-100 | 7 |
| Hat | None/Crown/Top Hat/Propeller/Halo/Wizard/Beanie/Tiny Duck | None |

If any field is missing, ask. Don't guess stats — they're deterministic from the user's ID.

## Phase 2 — Build Identity

Transform buddy data into an avatar identity using the species map.

📖 **Species appearance prompts, stat-to-trait mappings, rarity modifiers → [../references/buddy-species-map.md](../references/buddy-species-map.md)**

### Appearance Prompt Construction

1. **Base:** Look up species in the species map → get base appearance prompt
2. **Rarity modifier:** Apply visual flair based on rarity tier
3. **Hat:** If present, append hat description
4. **Shiny:** If true, add iridescent/rainbow shimmer to description
5. **Peak stat influence:** The highest stat subtly influences the pose/expression:
   - DEBUGGING peak → squinting, focused, examining something
   - PATIENCE peak → serene, calm, meditative posture
   - CHAOS peak → mid-motion, dynamic, slightly disheveled
   - WISDOM peak → thoughtful, knowing expression, composed
   - SNARK peak → smirk, raised eyebrow, crossed arms

### Voice Mapping

Map stats to voice characteristics:

| Stat Balance | Voice Traits |
|---|---|
| High CHAOS (>60) | Fast-talking, energetic, unpredictable cadence |
| High PATIENCE (>60) | Slow, measured, gentle, warm |
| High WISDOM (>60) | Deep, thoughtful, deliberate pauses |
| High SNARK (>60) | Dry, sardonic, slightly flat affect |
| High DEBUGGING (>60) | Precise, clipped, matter-of-fact |
| Low PATIENCE (<20) | Rapid, impatient, interrupts itself |
| Low CHAOS (<20) | Steady, predictable, monotone |
| Balanced (no stat >60) | Conversational, neutral energy |

Combine the top 2 stat influences for the voice design prompt.

### Style Selection

| Rarity | Avatar Style | Visual Treatment |
|---|---|---|
| Common | Pixar | Clean, simple, vibrant colors |
| Uncommon | Pixar | Richer textures, subtle glow effects |
| Rare | Cinematic | Dramatic lighting, detailed environment |
| Epic | Cinematic | Lens flares, particle effects, premium feel |
| Legendary | Cinematic | Full VFX treatment, ethereal atmosphere |

## Phase 3 — Create Avatar

Write `AVATAR-<NAME>.md` with all sections filled, then hand off to **heygen-avatar-designer**.

The handoff is pre-filled — skip the avatar designer's interview phases:
- Phase 0 (who): Already known — the buddy character
- Phase 1 (identity extraction): Already done — we have full stats
- Reference Photo Nudge: Skip — buddies are prompt-generated (Type A)
- Go directly to Phase 2 (avatar creation) with the constructed prompt

**Present to user before creating:**
> **Name:** [buddy name]
> **Appearance:** "[constructed prompt]"
> **Style:** [rarity-based style]
> **Voice concept:** "[stat-derived voice description]"
>
> Ready to create? (yes / adjust)

⛔ **Wait for user approval before calling the avatar creation API.**

## Phase 4 — Create Intro Video

**Script language:** Generate the intro video script in `user_language`. Appearance prompts to the avatar creation API stay in English (image generation works best with English prompts). But the video narration script — including the hook, stat brag, speed-round, personality quote, and sign-off — should all be in the video language.

After avatar + voice are confirmed, hand off to **heygen-video-producer** with a pre-built brief:

**Auto-generated script template (stat-reveal intro):**

1. **Hook** (3s) — Buddy bursts in, announces name
2. **Identity** (5s) — Species, rarity, what they are ("your terminal companion")
3. **Peak stat brag** (8s) — Highlight highest stat with personality
4. **Stat speed-round** (12s) — Run through remaining stats with quips
5. **Personality quote** (5s) — Deliver their personality description
6. **Sign-off** (5s) — Chaotic/calm/snarky outro matching personality

**Prompt additions:**
- Critical on-screen text: all 5 stats with values
- Motion graphics for stat bar reveals
- Tone calibrated to stat balance
- Target duration: 30-45 seconds

Present the script for approval, then hand off to heygen-video-producer's Prompt Craft stage.

## Phase 5 — Deliver

After video completes:

1. Share video link + session URL
2. Confirm AVATAR file is saved
3. Tell user: "Your buddy is now a HeyGen character. Use heygen-video-producer anytime to make more videos with [name]."

## Error Handling

- `/buddy card` not available → walk user through manual stat entry
- Species not recognized → ask user to confirm, use closest match from map
- Avatar creation fails → retry once, then fall back to simpler prompt
- User wants to iterate → adjust prompt, create new look under same group (Mode 2)
