# Buddy Species Map

Appearance prompts and trait mappings for Claude Code Buddy characters.

## Species → Appearance Prompt

The buddy's species is provided by the user (from `/buddy card`). **Do not assume a fixed species list** — new species may be added at any time. Build the appearance prompt dynamically from whatever species the user provides.

Avatar prompt limit is 1000 characters. Style enum and orientation are set separately via API parameters.

### How to Build the Prompt

For ANY species, construct the appearance prompt using this pattern:

```
A [adjective] cartoon [species] with [2-3 distinctive physical features of that animal],
[expressive eyes description matching personality], [pose/body language reflecting peak stat],
[1-2 detail touches that add character]
```

**Key principles:**
- Lead with the species' most recognizable physical traits
- Eyes convey personality — make them expressive and stat-appropriate
- Pose should reflect the peak stat (see Stat → Peak Stat Pose below)
- Add 1-2 small details that make the character feel alive
- Keep it under 1000 characters total (including rarity/hat/shiny modifiers)

### Example Prompts

These are examples for common species, not an exhaustive list. For any species not shown, follow the construction pattern above.

**penguin** (Bramble, CHAOS:77):
> A round adorable cartoon penguin with oversized expressive eyes that dart around excitedly, slightly ruffled and disheveled black and white feathers as if just tumbled through snow, stubby wings mid-flap caught in perpetual motion, a bright white belly, tiny orange feet, leaning forward energetically as if about to sprint somewhere

**owl** (high WISDOM):
> A distinguished cartoon owl with enormous round amber eyes that seem to hold ancient knowledge, rich layered brown and cream feathers with intricate patterns, small pointed ear tufts standing at attention, a compact round body perched upright on a branch, a short curved beak, head slightly tilted as if contemplating

**dragon** (high CHAOS):
> A small fierce cartoon dragon with brilliant iridescent scales shifting between emerald and gold, tiny bat-like wings spread wide showing translucent membranes, large glowing amber eyes with slit pupils burning with determination, a rounded snout puffing a tiny adorable flame, a spiky ridged tail curled upward, compact muscular build with tiny horns

**cat** (high SNARK):
> A sleek cartoon cat with large luminous green eyes that catch the light, soft velvety fur with subtle tabby markings, tall pointed ears slightly rotated outward listening to everything, a long graceful tail curled at the tip, alert curious expression with one paw raised mid-step, sitting poised on a surface edge

**capybara** (high PATIENCE):
> A serene cartoon capybara with calm half-lidded eyes that have seen everything and chosen peace, smooth warm brown fur with a golden undertone, a large barrel-shaped body sitting in perfect stillness, a flat wide nose with a gentle expression, tiny rounded ears, sitting peacefully as if the entire world is background noise

**robot** (high DEBUGGING):
> A retro cartoon robot with a charmingly boxy brushed-metal body, large round glowing cyan eyes like vintage monitors, a single bobbing antenna on top with a blinking light, visible brass gears and rivets along the joints, a small speaker-grille mouth that curves into a smile, stubby mechanical arms with pincer hands

**ghost** (high WISDOM):
> A cute translucent cartoon ghost with a soft ethereal glow emanating from within, large gentle eyes like luminous orbs shifting between blue and violet, a wispy trailing form that fades at the edges into mist, subtle internal shimmer like captured starlight, a friendly warm expression, hovering slightly off the ground

## Rarity Visual Modifiers

Append to the base prompt before submitting to the avatar API.

| Rarity | Stars | Style Enum | Modifier (append to prompt) |
|---|---|---|---|
| Common | 1 | Pixar | Clean simple background, bright solid colors |
| Uncommon | 2 | Pixar | Soft glow aura, richer color palette, subtle sparkles |
| Rare | 3 | Cinematic | Dramatic rim lighting, detailed environment, depth of field |
| Epic | 4 | Cinematic | Golden particle effects, lens flare, premium atmospheric lighting |
| Legendary | 5 | Cinematic | Ethereal cosmic aura, floating light particles, mythic atmosphere |

## Shiny Modifier

If the buddy is Shiny, prepend to the appearance prompt:
> "Iridescent rainbow shimmer across the entire character, holographic prismatic reflections on every surface."

## Hat Modifiers

Append to appearance prompt if a hat is present. If the user's hat isn't listed here, describe it naturally.

| Hat | Prompt Addition |
|---|---|
| Crown | Wearing a small golden crown tilted slightly to one side |
| Top Hat | Wearing a dapper black top hat |
| Propeller | Wearing a colorful propeller beanie hat |
| Halo | Floating golden halo above head |
| Wizard | Wearing a tall purple wizard hat with silver stars |
| Beanie | Wearing a cozy knitted beanie |
| Tiny Duck | A tiny rubber duck sitting on top of head |

## Stat → Voice Design Prompt

Build the voice design prompt by combining the **top 2 stat influences**. Pick the two highest stats and merge their voice descriptors.

### Primary Stat Voice Descriptors

| Stat | High (>60) | Low (<20) |
|---|---|---|
| DEBUGGING | Precise, analytical, clipped diction, matter-of-fact | Vague, meandering, loses track mid-sentence |
| PATIENCE | Slow, measured, warm, gentle, reassuring pauses | Rapid-fire, impatient, cuts itself off, restless |
| CHAOS | Fast-talking, unpredictable cadence, wild energy shifts, excitable | Steady, predictable, metronomic, flat |
| WISDOM | Deep, thoughtful, deliberate pauses, knowing tone | Naive, bright-eyed, everything sounds like a question |
| SNARK | Dry, sardonic, deadpan delivery, slightly flat affect | Earnest, sincere, zero irony, wholesome |

### Construction Pattern

```
"[Primary stat descriptor], [secondary stat descriptor]. [Species] personality.
[Gender] voice, {video_language}. Think: [one-line character analogy]."
```

Use the video language from `user_language` (e.g., English, Japanese, Korean, Spanish). Never hardcode "English."

**Example (Bramble — CHAOS:77, WISDOM:27, English):**
```
"Fast-talking, unpredictable cadence, wild energy shifts, excitable.
Slightly thoughtful undertone but overwhelmed by chaos.
Gender neutral voice, English.
Think: an overexcited cartoon sidekick who talks before thinking."
```

**Example (same buddy, Japanese):**
```
"Fast-talking, unpredictable cadence, wild energy shifts, excitable.
Slightly thoughtful undertone but overwhelmed by chaos.
Gender neutral voice, Japanese.
Think: an overexcited cartoon sidekick who talks before thinking."
```

## Stat → Peak Stat Pose

The highest stat influences the avatar's pose/expression in the prompt:

| Peak Stat | Pose Modifier |
|---|---|
| DEBUGGING | Squinting slightly, leaning forward examining something closely |
| PATIENCE | Serene expression, eyes gently closed or half-lidded, still posture |
| CHAOS | Mid-motion, dynamic angle, slightly disheveled, leaning forward |
| WISDOM | Thoughtful knowing expression, chin slightly raised, composed |
| SNARK | Subtle smirk, one eyebrow raised, arms crossed or leaning back |

## Stat → Video Script Tone

How each stat balance affects the intro video script:

| Dominant Stat | Script Tone | Sign-off Style (generate in video language) |
|---|---|---|
| DEBUGGING | Analytical, breaks down own stats like code review | A nerdy self-deprecating quip about creating bugs |
| PATIENCE | Warm, takes time with each stat, reassuring | A gentle reassurance that they'll be there when needed |
| CHAOS | Manic, rapid-fire, jumps between topics | An excited promise of wild adventures ahead |
| WISDOM | Reflective, frames stats as lessons learned | A wry observation about listening to code |
| SNARK | Deadpan, self-deprecating, roasts own low stats | A dismissive "you're welcome" |

Generate the sign-off naturally in the video language. The descriptions above are the *vibe*, not literal translations.

## Video Prompt Style Block by Rarity

| Rarity | Visual Style Direction |
|---|---|
| Common | Use vibrant Pixar-style visuals. Bold primary colors. Motion graphics for stat reveals. Clean transitions. |
| Uncommon | Use rich Pixar-style visuals with subtle glow effects. Smooth animated transitions. Sparkle accents on stat reveals. |
| Rare | Use cinematic visuals with dramatic lighting. Camera depth of field. Stat reveals with light-streak animations. |
| Epic | Use premium cinematic visuals. Lens flares, golden particles. Stats revealed with explosive motion graphics. Epic orchestral energy. |
| Legendary | Use ethereal cinematic visuals. Cosmic atmosphere, floating light particles. Stats materialize from stardust. Mythic reveal sequence. |
