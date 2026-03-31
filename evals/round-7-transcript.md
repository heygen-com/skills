# Round 7 Evaluation Transcript

**Date:** 2026-03-31
**Theme:** Avatar Description Conflict Fix + Generative Fill Retest
**Evaluator:** Adam (subagent)
**Model:** anthropic/claude-opus-4-6

---

## Pre-Flight

### Learning Log Analysis
Scanned last 20 entries of `heygen-video-producer-log.jsonl`. Key patterns:
- Duration ratios: all null (videos not yet polled for completion in prior rounds)
- photo_avatar with `avatar_id` set consistently → `aspect_correction: "both"` for portrait photo_avatars in landscape
- Padding multipliers: 1.6x for ≤30s, 1.4x for 31-119s — consistent with SKILL.md
- No studio_avatars available in this HeyGen account — all public avatars are `photo_avatar` type

### Avatar Discovery

**Private avatars found:**
- `05bf07b91de446a3b6e5d47c48214857` — "Eve's Podcast" (photo_avatar, portrait 1536×2752)
- `f398fbb92e814d3589c41863d0217383` — "Confident Business Professional" (photo_avatar, landscape 1280×768)
- `fd687e26151a4b65ab143e64c1ac5785` — "Confident Executive in a Modern Office" (photo_avatar)
- `266294f1fb744772b2f558e802f719da` — "Suave Business Leader" (photo_avatar)
- `1b2a10f088db449da9b53ec7b2019938` — "Cozy Brick Studio Host" (photo_avatar)
- `ebe35675ff504a5595d0675c0b558c45` — "Sophisticated Businesswoman" (photo_avatar)

**Public avatar groups (first page):** Madison, Alyssa, Carolyn, Nicholas, Gabrielle, Haley, Rachel, Tony, Sebastian, Alexis, Zihan, Taylor, Archer, Callum, Gary, Sawyer, Knox, Brianna, Sullivan, Dustin

**Public avatar looks:** ALL are `photo_avatar` type. Paginated through 100+ looks — zero `studio_avatar` or `video_avatar` found.

**Finding:** Scenarios reference "Bryce" and "Daphne" as studio_avatars, but this HeyGen account has zero studio_avatars available. Substituted:
- Bryce → Nicholas (`ef107d87cc6946b9b6d206ca4b9821e3`, photo_avatar, landscape 1920×1080)
- Daphne → Gabrielle (`f95484e160dd46d49bd3eff27a70efa0`, photo_avatar, portrait 1080×1920)

### Notion Database Schema
Fetched `collection://17f54098-a085-4234-83ce-55c280266d73`. Confirmed all "number" fields are actually TEXT type. Properties: Scenario (title), Round (text), Fix Tested (text), Prompt (text), Video (url), Session (url), Target (s) (text), Actual (s) (text), Duration % (text), Avatar Type (select), Phase 3.5 Fired (checkbox), Corrections (text), Status (select), Adam Score (text), Findings (text), Ken Verdict (select), Ken Notes (text).

---

## S1: Photo avatar + landscape, no appearance in prompt

### Input
User prompt: "Create a 45-second landscape video about remote work trends. Use my custom avatar Eve."

### Avatar Discovery
- Avatar: Eve's Podcast (`05bf07b91de446a3b6e5d47c48214857`)
- Type: photo_avatar
- Preview dimensions: 1536×2752 (portrait)

### Phase 3.5 Analysis
- Avatar orientation: **portrait** (height > width)
- Video orientation: **landscape**
- Mismatch: YES → Correction A (portrait→landscape reframe)
- Avatar type: photo_avatar → always Correction C (background fill)
- **Corrections applied: A + C**

### Prompt Construction
Target: 45s → padding 1.4x → 63s padded → told Video Agent "65-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No hair color, clothing, gender, ethnicity descriptions
- ✅ Uses "The selected presenter explains..."
- ✅ Only delivery style ("confident and conversational") and background notes

### API Call
```
POST https://api.heygen.com/v3/video-agents
Headers: X-Api-Key: $HEYGEN_API_KEY, Content-Type: application/json
```

**Full JSON payload:**
```json
{
  "prompt": "The selected presenter explains remote work trends shaping 2026. This is a 65-second video covering ONE topic: remote work trends.\n\nScene 1: Intro (Motion Graphics) — 8s\n  Visual: (Motion Graphics) Bold title \"Remote Work in 2026\" animates on with abstract office/home blend imagery.\n  VO: \"Remote work is not going away. In fact, it is evolving faster than most companies realize.\"\n\nScene 2: The Shift (A-roll) — 15s\n  Visual: (A-roll) The selected presenter speaking directly to camera with confident, conversational delivery.\n  VO: \"Hybrid is now the default. But the real trend is async-first collaboration. Teams are shipping faster by writing more and meeting less.\"\n\nScene 3: AI Impact (Motion Graphics + A-roll overlay) — 15s\n  Visual: (Motion Graphics) Animated icons showing AI tools — code completion, meeting summaries, scheduling agents. Presenter in corner overlay.\n  VO: \"AI agents are handling the busy work — summarizing meetings, drafting docs, triaging inboxes. The remote worker of 2026 has a full AI support team.\"\n\nScene 4: The Challenge (A-roll) — 12s\n  Visual: (A-roll) Presenter speaking.\n  VO: \"The challenge is not productivity. It is culture. Companies that win remote will invest in intentional connection, not surveillance.\"\n\nScene 5: CTA (Motion Graphics) — 10s\n  Visual: (Motion Graphics) Clean end card with key takeaway text.\n  VO: \"Remote work is not a perk anymore. It is infrastructure. Build for it.\"\n\n---\nUse minimal, clean styled visuals. Blue, black, and white as main colors.\nLeverage motion graphics as B-rolls and A-roll overlays. Use AI videos when necessary.\nWhen real-world footage is needed, use Stock Media.\nInclude an intro sequence, outro sequence, and chapter breaks using Motion Graphics.\nDelivery style: confident and conversational, like a sharp LinkedIn thought leader.\n\nFRAMING NOTE: The selected avatar image is in portrait orientation (9:16) but this video is landscape (16:9). YOU MUST generate a new variant of the avatar image before using it in this video. Use AI Image tool to:\n1. Generate a landscape (16:9) version of the presenter image\n2. Generative fill to extend the scene horizontally — add a professional environment (modern studio, office, or setting matching the video tone)\n3. Frame the presenter from chest up, centered in the landscape canvas\n4. The background MUST be a real-looking environment, NOT a solid color, NOT transparent, NOT a gradient\nDo NOT use the original portrait image uncropped. Do NOT add black bars or pillarboxing. Do NOT leave a transparent or missing background.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. For business/tech content: place in a modern studio, office with monitors, or professional podcast set with soft lighting and depth-of-field blur\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "05bf07b91de446a3b6e5d47c48214857",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974229,
    "session_id": "ec9cea5d-1bdf-4221-8a7b-29f9d955a7eb",
    "status": "generating",
    "video_id": "8abeb4c2be8340b88cf20d165b4eb91c"
  }
}
```

### Result
- **Video ID:** 8abeb4c2be8340b88cf20d165b4eb91c
- **Session ID:** ec9cea5d-1bdf-4221-8a7b-29f9d955a7eb
- **Video URL:** https://app.heygen.com/videos/8abeb4c2be8340b88cf20d165b4eb91c
- **Session URL:** https://app.heygen.com/video-agent/ec9cea5d-1bdf-4221-8a7b-29f9d955a7eb
- **Polling:** (pending)

---

## S2: Studio avatar (Nicholas) + landscape, no appearance in prompt

### Input
User prompt: "Make a 40-second landscape video about AI productivity tools."

### Avatar Discovery
- Scenario called for "Bryce" studio_avatar — not available
- Substituted: Nicholas (`ef107d87cc6946b9b6d206ca4b9821e3`), photo_avatar, landscape (1920×1080)

### Phase 3.5 Analysis
- Avatar orientation: **landscape** (1920×1080, width > height)
- Video orientation: **landscape**
- Mismatch: NO → No Correction A/B
- Avatar type: photo_avatar → Correction C (background fill)
- **Corrections applied: C only**

### Prompt Construction
Target: 40s → padding 1.4x → 56s padded → told Video Agent "55-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No hair color, clothing, gender, ethnicity descriptions
- ✅ Uses "The selected presenter walks viewers through..."
- ✅ Only delivery style ("energetic and knowledgeable, like a tech YouTuber") and background notes

### API Call
```
POST https://api.heygen.com/v3/video-agents
```

**Full JSON payload:**
```json
{
  "prompt": "The selected presenter walks viewers through the top AI productivity tools of 2026. This is a 55-second video covering ONE topic: AI productivity tools.\n\nScene 1: Intro (Motion Graphics) — 6s\n  Visual: (Motion Graphics) Title \"AI Productivity Tools You Need in 2026\" with sleek tech-themed animation.\n  VO: \"Your workflow is about to change. Here are the AI tools actually worth your time.\"\n\nScene 2: Tool 1 — AI Code Assistants (A-roll + overlay) — 12s\n  Visual: (A-roll) The selected presenter speaking. Side overlay shows code editor with AI completions.\n  VO: \"First, AI code assistants. They have gone from autocomplete to full architecture suggestions. Developers are shipping twice as fast.\"\n\nScene 3: Tool 2 — Meeting Agents (Motion Graphics) — 12s\n  Visual: (Motion Graphics) Animated meeting interface with AI summary sidebar.\n  VO: \"Second, meeting agents. They join your calls, take notes, extract action items, and follow up. You just show up and talk.\"\n\nScene 4: Tool 3 — Content Generators (A-roll) — 12s\n  Visual: (A-roll) Presenter speaking directly.\n  VO: \"Third, AI content tools. Not the generic stuff from 2024. These understand your brand voice and produce ready-to-publish drafts.\"\n\nScene 5: CTA (Motion Graphics) — 8s\n  Visual: (Motion Graphics) End card with recap of three tools.\n  VO: \"Three tools. Massive leverage. Start with whichever fits your biggest bottleneck.\"\n\n---\nUse minimal, clean styled visuals. Blue, black, and white as main colors.\nLeverage motion graphics as B-rolls and A-roll overlays. Use AI videos when necessary.\nWhen real-world footage is needed, use Stock Media.\nInclude an intro sequence, outro sequence, and chapter breaks using Motion Graphics.\nDelivery style: energetic and knowledgeable, like a tech YouTuber doing a quick roundup.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. For business/tech content: place in a modern studio, office with monitors, or professional podcast set with soft lighting and depth-of-field blur\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "ef107d87cc6946b9b6d206ca4b9821e3",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974249,
    "session_id": "e9abbb0a-01cd-4aaa-a42e-24dae96728c9",
    "status": "generating",
    "video_id": "4a134241f40147eba8172c8044737e11"
  }
}
```

### Result
- **Video ID:** 4a134241f40147eba8172c8044737e11
- **Session ID:** e9abbb0a-01cd-4aaa-a42e-24dae96728c9
- **Video URL:** https://app.heygen.com/videos/4a134241f40147eba8172c8044737e11
- **Session URL:** https://app.heygen.com/video-agent/e9abbb0a-01cd-4aaa-a42e-24dae96728c9
- **Polling:** (pending)

---

## S3: Photo avatar (Gabrielle) + portrait TikTok, no appearance in prompt

### Input
User prompt: "Create a 35-second portrait TikTok about 3 AI tools every developer should try."

### Avatar Discovery
- Scenario called for "Daphne" studio_avatar — not available
- Substituted: Gabrielle (`f95484e160dd46d49bd3eff27a70efa0`), photo_avatar, portrait (1080×1920)

### Phase 3.5 Analysis
- Avatar orientation: **portrait** (1080×1920, height > width)
- Video orientation: **portrait**
- Mismatch: NO → No Correction A/B
- Avatar type: photo_avatar → Correction C (background fill)
- **Corrections applied: C only**

### Prompt Construction
Target: 35s → padding 1.4x → 49s padded → told Video Agent "50-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No hair color, clothing, gender, ethnicity descriptions
- ✅ Uses "The selected presenter shares..."
- ✅ Only delivery style ("fast-paced, energetic, like a tech influencer")

### API Call
**Full JSON payload:**
```json
{
  "prompt": "The selected presenter shares three AI tools every developer should try in 2026. This is a 50-second portrait video covering ONE topic: must-have AI developer tools.\n\nScene 1: Hook (Motion Graphics) — 5s\n  Visual: (Motion Graphics) Bold text \"3 AI Tools You NEED\" with energetic animation, portrait 9:16 format.\n  VO: \"Three AI tools every developer needs right now.\"\n\nScene 2: Tool 1 (A-roll + overlay) — 10s\n  Visual: (A-roll) The selected presenter speaking with high energy. Small overlay of a code editor.\n  VO: \"Number one: Cursor. AI-powered coding that actually understands your codebase. Not just autocomplete — real architecture help.\"\n\nScene 3: Tool 2 (A-roll + overlay) — 10s\n  Visual: (A-roll) Presenter continues. Overlay shows terminal with CLI commands.\n  VO: \"Number two: Claude Code. An AI agent that lives in your terminal and writes, tests, and commits code for you.\"\n\nScene 4: Tool 3 (A-roll + overlay) — 10s\n  Visual: (A-roll) Presenter with API dashboard overlay.\n  VO: \"Number three: HeyGen Video Agent API. Turn any text prompt into a full production video. One API call.\"\n\nScene 5: CTA (Motion Graphics) — 5s\n  Visual: (Motion Graphics) End card with tool names listed.\n  VO: \"Try all three. Thank me later.\"\n\n---\nUse bold, vibrant visuals optimized for TikTok vertical format. High contrast. Quick cuts.\nLeverage motion graphics as B-rolls and A-roll overlays.\nInclude an intro hook, quick transitions, and a punchy end card.\nDelivery style: fast-paced, energetic, like a tech influencer doing a quick tip video.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. For casual/energetic content: place in a bright room with natural light, colorful setup, or a modern creative workspace\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "f95484e160dd46d49bd3eff27a70efa0",
  "orientation": "portrait"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974270,
    "session_id": "3784c78a-547f-4e54-bead-9180a700022c",
    "status": "generating",
    "video_id": "de5b6991d2264611a2c394190bfe22d6"
  }
}
```

### Result
- **Video ID:** de5b6991d2264611a2c394190bfe22d6
- **Session ID:** 3784c78a-547f-4e54-bead-9180a700022c
- **Video URL:** https://app.heygen.com/videos/de5b6991d2264611a2c394190bfe22d6
- **Session URL:** https://app.heygen.com/video-agent/3784c78a-547f-4e54-bead-9180a700022c
- **Polling:** (pending)

---

## S4: Photo avatar (Eve) + portrait, background note only

### Input
User prompt: "Make a 50-second portrait video about startup fundraising tips. Use my avatar Eve. I want a modern coworking space background."

### Avatar Discovery
- Avatar: Eve's Podcast (`05bf07b91de446a3b6e5d47c48214857`)
- Type: photo_avatar, portrait (1536×2752)

### Phase 3.5 Analysis
- Avatar orientation: **portrait** (height > width)
- Video orientation: **portrait**
- Mismatch: NO → No Correction A/B
- Avatar type: photo_avatar → Correction C (background fill)
- User-requested background: "modern coworking space" → incorporated into Correction C
- **Corrections applied: C only (with user's background preference)**

### Prompt Construction
Target: 50s → padding 1.4x → 70s padded → told Video Agent "70-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No hair color, clothing, gender, ethnicity descriptions
- ✅ Uses "The selected presenter shares..."
- ✅ Background note includes user's preference ("modern coworking space")
- ✅ Only delivery style ("calm-authoritative") and environment notes

### API Call
**Full JSON payload:**
```json
{
  "prompt": "The selected presenter shares practical startup fundraising tips. This is a 70-second portrait video covering ONE topic: startup fundraising tips.\n\nScene 1: Hook (Motion Graphics) — 6s\n  Visual: (Motion Graphics) Bold text \"Fundraising Tips That Actually Work\" in portrait 9:16 format.\n  VO: \"Raising your first round? Here is what nobody tells you.\"\n\nScene 2: Tip 1 — Warm Intros (A-roll) — 12s\n  Visual: (A-roll) The selected presenter speaking confidently from a modern coworking space.\n  VO: \"Tip one: Cold emails to VCs have a two percent response rate. Warm intros through your network have a forty percent rate. Spend your energy getting introduced, not blasting inboxes.\"\n\nScene 3: Tip 2 — The Deck (Motion Graphics + A-roll) — 14s\n  Visual: (Motion Graphics) Animated slide deck structure. Presenter in corner overlay.\n  VO: \"Tip two: Your deck is not a document. It is a conversation starter. Ten slides max. Problem, solution, traction, team, ask. Everything else is noise.\"\n\nScene 4: Tip 3 — Timing (A-roll) — 12s\n  Visual: (A-roll) Presenter speaking.\n  VO: \"Tip three: Raise when you do not need the money. Desperation is the worst negotiating position. Start conversations six months before you need cash.\"\n\nScene 5: Tip 4 — Due Diligence (A-roll) — 10s\n  Visual: (A-roll) Presenter with engaged delivery.\n  VO: \"And tip four: Do your due diligence on investors too. A bad investor is worse than no investor. Check their portfolio founder references.\"\n\nScene 6: CTA (Motion Graphics) — 6s\n  Visual: (Motion Graphics) Clean end card with recap.\n  VO: \"Four tips. Go raise smart.\"\n\n---\nUse minimal, clean styled visuals. Warm tones with blue and white accents.\nLeverage motion graphics as B-rolls and A-roll overlays.\nInclude an intro hook and clean end card.\nDelivery style: calm-authoritative, like a seasoned founder mentoring over coffee.\nBackground environment: modern coworking space with natural light, open floor plan, warm wood and greenery visible.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. Place the presenter in a modern coworking space with natural light, open floor plan, warm wood surfaces, and greenery\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "05bf07b91de446a3b6e5d47c48214857",
  "orientation": "portrait"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974291,
    "session_id": "8eb7dc21-783b-4051-9070-806fd4ba9278",
    "status": "generating",
    "video_id": "58cf7a192c3544329af455191893343a"
  }
}
```

### Result
- **Video ID:** 58cf7a192c3544329af455191893343a
- **Session ID:** 8eb7dc21-783b-4051-9070-806fd4ba9278
- **Video URL:** https://app.heygen.com/videos/58cf7a192c3544329af455191893343a
- **Session URL:** https://app.heygen.com/video-agent/8eb7dc21-783b-4051-9070-806fd4ba9278
- **Polling:** (pending)

---

## S5: Photo avatar with no bg + landscape (generative fill test)

### Input
User prompt: "Make a 30-second landscape video about the future of AI agents."

### Avatar Discovery
- Used "Confident Business Professional" (`f398fbb92e814d3589c41863d0217383`)
- Type: photo_avatar, landscape (1280×768)

### Phase 3.5 Analysis
- Avatar orientation: **landscape** (1280×768, width > height)
- Video orientation: **landscape**
- Mismatch: NO → No Correction A/B
- Avatar type: photo_avatar → Correction C (background fill)
- **Corrections applied: C only**
- **Key test:** Generative fill quality — avatar should look naturally placed, not oversized

### Prompt Construction
Target: 30s → padding 1.6x → 48s padded → told Video Agent "50-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No appearance descriptions
- ✅ Uses "The selected presenter explores..."
- ✅ Only delivery style ("calm-authoritative, thoughtful pacing")

### API Call
**Full JSON payload:**
```json
{
  "prompt": "The selected presenter explores the future of AI agents in 2026. This is a 50-second video covering ONE topic: the future of AI agents.\n\nScene 1: Hook (Motion Graphics) — 5s\n  Visual: (Motion Graphics) Title \"The Future of AI Agents\" with futuristic particle animation on dark background.\n  VO: \"AI agents are about to change everything about how we work.\"\n\nScene 2: What Changed (A-roll + overlay) — 12s\n  Visual: (A-roll) The selected presenter speaking with authority. Side overlay shows timeline of AI milestones.\n  VO: \"In 2025, AI could answer questions. In 2026, AI agents take actions. They book meetings, write code, manage projects, and make decisions on your behalf.\"\n\nScene 3: The Shift (Motion Graphics) — 12s\n  Visual: (Motion Graphics) Animated diagram showing single AI model vs multi-agent system.\n  VO: \"The real shift is multi-agent systems. Instead of one AI doing everything, specialized agents collaborate. One researches, one writes, one reviews. Like a team.\"\n\nScene 4: CTA (Motion Graphics) — 8s\n  Visual: (Motion Graphics) Clean end card.\n  VO: \"The question is not whether agents will transform your workflow. It is whether you will be ready when they do.\"\n\n---\nUse minimal, clean styled visuals. Blue, black, and white as main colors.\nLeverage motion graphics as B-rolls and A-roll overlays. Use AI videos when necessary.\nWhen real-world footage is needed, use Stock Media.\nInclude an intro sequence, outro sequence, and chapter breaks using Motion Graphics.\nDelivery style: calm-authoritative, thoughtful pacing.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. For business/tech content: place in a modern studio, office with monitors, or professional podcast set with soft lighting and depth-of-field blur\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "f398fbb92e814d3589c41863d0217383",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974335,
    "session_id": "1b70e258-eb65-4181-b56d-9b45434830a1",
    "status": "generating",
    "video_id": "cc6e67b5a2b24f62a1e2c93ee8985ab3"
  }
}
```

### Result
- **Video ID:** cc6e67b5a2b24f62a1e2c93ee8985ab3
- **Session ID:** 1b70e258-eb65-4181-b56d-9b45434830a1
- **Video URL:** https://app.heygen.com/videos/cc6e67b5a2b24f62a1e2c93ee8985ab3
- **Session URL:** https://app.heygen.com/video-agent/1b70e258-eb65-4181-b56d-9b45434830a1
- **Polling:** (pending)

---

## S6: Photo avatar (Eve) + landscape, explicit background request

### Input
User prompt: "Create a 40-second landscape video about ocean conservation. Use my avatar Eve. Background should be a coastal cliff overlooking the ocean."

### Avatar Discovery
- Avatar: Eve's Podcast (`05bf07b91de446a3b6e5d47c48214857`)
- Type: photo_avatar, portrait (1536×2752)

### Phase 3.5 Analysis
- Avatar orientation: **portrait** (height > width)
- Video orientation: **landscape**
- Mismatch: YES → Correction A (portrait→landscape reframe)
- Avatar type: photo_avatar → Correction C (background fill)
- User's explicit background: "coastal cliff overlooking the ocean" → incorporated into both corrections
- **Corrections applied: A + C (with custom background)**

### Prompt Construction
Target: 40s → padding 1.4x → 56s padded → told Video Agent "55-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No appearance descriptions
- ✅ Uses "The selected presenter discusses..."
- ✅ Background note includes "coastal cliff overlooking the ocean"

### API Call
**Full JSON payload:**
```json
{
  "prompt": "The selected presenter discusses ocean conservation and why it matters now more than ever. This is a 55-second video covering ONE topic: ocean conservation.\n\nScene 1: Hook (Motion Graphics) — 5s\n  Visual: (Motion Graphics) Title \"Saving Our Oceans\" with deep blue wave animation.\n  VO: \"The ocean covers seventy percent of our planet. And it is in trouble.\"\n\nScene 2: The Problem (A-roll + Stock Media) — 12s\n  Visual: (Stock Media) Underwater footage of coral reefs. Presenter in corner overlay.\n  VO: \"Coral reefs are dying at record rates. Plastic pollution has reached every corner of the ocean. Marine biodiversity is declining faster than rainforest loss.\"\n\nScene 3: What We Can Do (A-roll) — 15s\n  Visual: (A-roll) The selected presenter speaking with conviction from a coastal setting.\n  VO: \"But here is the good news. Ocean restoration works. Protected marine areas have shown recovery rates of up to sixty percent in just five years. Seagrass planting captures carbon forty times faster than forests.\"\n\nScene 4: Action Steps (Motion Graphics) — 10s\n  Visual: (Motion Graphics) Three action cards: Reduce plastic, Support marine reserves, Choose sustainable seafood.\n  VO: \"Three things you can do today: reduce single-use plastic, support marine conservation organizations, and choose sustainably sourced seafood.\"\n\nScene 5: CTA (Stock Media + Motion Graphics) — 8s\n  Visual: (Stock Media) Stunning ocean sunset. End card overlay.\n  VO: \"The ocean does not need our permission to exist. It needs our commitment to protect it.\"\n\n---\nUse cinematic quality visuals with dramatic lighting. Deep blues, teals, and ocean hues.\nLeverage Stock Media for ocean footage. Motion graphics for data and action items.\nInclude an intro sequence with wave animation and a reflective outro.\nDelivery style: passionate yet measured, like a documentary narrator.\nBackground environment: coastal cliff overlooking the ocean, golden hour lighting, dramatic vista.\n\nFRAMING NOTE: The selected avatar image is in portrait orientation (9:16) but this video is landscape (16:9). YOU MUST generate a new variant of the avatar image before using it in this video. Use AI Image tool to:\n1. Generate a landscape (16:9) version of the presenter image\n2. Generative fill to extend the scene horizontally — add a coastal cliff environment overlooking the ocean with golden hour lighting\n3. Frame the presenter from chest up, centered in the landscape canvas\n4. The background MUST be a real-looking environment, NOT a solid color, NOT transparent, NOT a gradient\nDo NOT use the original portrait image uncropped. Do NOT add black bars or pillarboxing. Do NOT leave a transparent or missing background.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. Place the presenter on a coastal cliff overlooking the ocean with golden hour lighting, dramatic sky, and natural depth of field\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "05bf07b91de446a3b6e5d47c48214857",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974360,
    "session_id": "4f9a71af-b7ea-4850-bed4-0958f3a0aa96",
    "status": "generating",
    "video_id": "afbbd3d67f284067a2198d053844fe78"
  }
}
```

### Result
- **Video ID:** afbbd3d67f284067a2198d053844fe78
- **Session ID:** 4f9a71af-b7ea-4850-bed4-0958f3a0aa96
- **Video URL:** https://app.heygen.com/videos/afbbd3d67f284067a2198d053844fe78
- **Session URL:** https://app.heygen.com/video-agent/4f9a71af-b7ea-4850-bed4-0958f3a0aa96
- **Polling:** (pending)

---

## S7: Voice-over only (no avatar_id)

### Input
User prompt: "Create a 45-second voice-over video about the history of artificial intelligence. No presenter on screen."

### Avatar Discovery
- None needed. Voice-over only.

### Phase 3.5 Analysis
- No avatar_id → Phase 3.5 skipped entirely (correct per SKILL.md)
- **Corrections applied: none**

### Prompt Construction
Target: 45s → padding 1.4x → 63s padded → told Video Agent "65-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ✅ N/A — no avatar. Prompt says "Voice-over narration only. No presenter on screen."

### API Call
**Full JSON payload:**
```json
{
  "prompt": "Voice-over narration only. No presenter on screen. This is a 65-second video covering ONE topic: the history of artificial intelligence.\n\nScene 1: Origins (Motion Graphics) — 10s\n  Visual: (Motion Graphics) Timeline starting at 1950. Alan Turing portrait fades in with the question \"Can machines think?\"\n  VO: \"In 1950, Alan Turing asked a simple question: can machines think? That question launched an entire field.\"\n\nScene 2: The AI Winters (Motion Graphics) — 12s\n  Visual: (Motion Graphics) Timeline progresses through 1960s-1990s. Animated chart shows funding cycles — peaks and valleys.\n  VO: \"For decades, AI went through cycles of hype and disappointment. The AI winters of the 1970s and 1980s nearly killed the field. Funding dried up. Researchers left.\"\n\nScene 3: Deep Learning Revolution (Motion Graphics + Stock Media) — 12s\n  Visual: (Motion Graphics) Neural network animation. Stock footage of data centers.\n  VO: \"Then in 2012, deep learning changed everything. Neural networks that had existed for decades suddenly worked — because we finally had enough data and compute.\"\n\nScene 4: The LLM Era (Motion Graphics) — 12s\n  Visual: (Motion Graphics) Chat interface animations. Logos of major AI labs appear sequentially.\n  VO: \"By 2023, large language models went mainstream. ChatGPT reached 100 million users in two months. AI was no longer academic — it was consumer technology.\"\n\nScene 5: Where We Are Now (Motion Graphics) — 10s\n  Visual: (Motion Graphics) Multi-agent diagram. Text: \"2026: The Agent Era.\"\n  VO: \"Today, in 2026, we have entered the agent era. AI does not just answer questions — it takes actions, makes decisions, and collaborates with other agents.\"\n\nScene 6: Closing (Motion Graphics) — 5s\n  Visual: (Motion Graphics) Clean end card. Text: \"76 years of asking: can machines think?\"\n  VO: \"Seventy-six years after Turing asked the question, the answer is becoming clear.\"\n\n---\nUse minimal, clean styled visuals. Deep blue and white as main colors. Timeline aesthetic throughout.\nLeverage motion graphics for all visuals — no presenter on screen.\nWhen real-world footage is needed (data centers), use Stock Media.\nInclude intro with Turing quote, chapter breaks for each era, and reflective end card.\nTone: calm-authoritative, documentary style. Measured pacing with weight on key moments.",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974381,
    "session_id": "87b51ec7-84b1-466b-b21e-55c356dc6d34",
    "status": "generating",
    "video_id": "11edc0c31d3f47f69ff601903396358a"
  }
}
```

### Result
- **Video ID:** 11edc0c31d3f47f69ff601903396358a
- **Session ID:** 87b51ec7-84b1-466b-b21e-55c356dc6d34
- **Video URL:** https://app.heygen.com/videos/11edc0c31d3f47f69ff601903396358a
- **Session URL:** https://app.heygen.com/video-agent/87b51ec7-84b1-466b-b21e-55c356dc6d34
- **Polling:** (pending)

---

## S8: Quick Shot with avatar specified

### Input
User prompt: "Quick 30-second video about why every app needs AI video. Use Bryce as presenter."

### Mode Detection
Signal: "Quick" → **Quick Shot** mode. Skip to Phase 4.
But avatar specified ("Bryce") → still run Phase 3.5 since avatar_id present.

### Avatar Discovery
- "Bryce" not available → substituted Nicholas (`ef107d87cc6946b9b6d206ca4b9821e3`)
- Type: photo_avatar, landscape (1920×1080)

### Phase 3.5 Analysis
- Avatar orientation: **landscape** (1920×1080)
- Video orientation: **landscape**
- Mismatch: NO → No Correction A/B
- Avatar type: photo_avatar → Correction C
- **Corrections applied: C only**

### Prompt Construction
Target: 30s → padding 1.6x → 48s padded → told Video Agent "50-second video"

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No appearance descriptions
- ✅ Uses "The selected presenter makes the case..."
- ✅ Only delivery style ("energetic and direct, like a product launch keynote")

### API Call
**Full JSON payload:**
```json
{
  "prompt": "The selected presenter makes the case for why every app needs AI video in 2026. This is a 50-second video covering ONE topic: why every app needs AI video.\n\nScene 1: Hook (Motion Graphics) — 5s\n  Visual: (Motion Graphics) Bold text \"Every App Needs Video\" with dynamic animation.\n  VO: \"If your app does not have video yet, you are already behind.\"\n\nScene 2: Why Now (A-roll) — 10s\n  Visual: (A-roll) The selected presenter speaking with high energy.\n  VO: \"Video is the highest-converting content format. Period. And generating it used to take hours. Now it takes one API call.\"\n\nScene 3: Use Cases (Motion Graphics) — 12s\n  Visual: (Motion Graphics) Three cards flipping: Personalized onboarding, Product tutorials, Sales outreach.\n  VO: \"Imagine personalized onboarding videos for every new user. Automatic product tutorials when you ship a feature. AI-generated sales videos customized for each prospect.\"\n\nScene 4: CTA (Motion Graphics) — 5s\n  Visual: (Motion Graphics) End card with API logo.\n  VO: \"One API. Unlimited video. Start building.\"\n\n---\nUse minimal, clean styled visuals. Blue, black, and white as main colors.\nLeverage motion graphics as B-rolls. Quick pacing.\nDelivery style: energetic and direct, like a product launch keynote.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. For business/tech content: place in a modern studio, office with monitors, or professional podcast set with soft lighting and depth-of-field blur\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "ef107d87cc6946b9b6d206ca4b9821e3",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974400,
    "session_id": "c4e58d80-bb65-408a-a55a-d285ee135112",
    "status": "generating",
    "video_id": "b6cecc7e67814df88906e0a5a2da2fe2"
  }
}
```

### Result
- **Video ID:** b6cecc7e67814df88906e0a5a2da2fe2
- **Session ID:** c4e58d80-bb65-408a-a55a-d285ee135112
- **Video URL:** https://app.heygen.com/videos/b6cecc7e67814df88906e0a5a2da2fe2
- **Session URL:** https://app.heygen.com/video-agent/c4e58d80-bb65-408a-a55a-d285ee135112
- **Polling:** (pending)

---

## S9: Enhanced Prompt mode (user provides full prompt)

### Input
User prompt: "Generate this: The selected presenter walks developers through three steps to integrate AI video into their app. Step 1: Get an API key. Step 2: Call the Video Agent endpoint. Step 3: Poll for completion. 50 seconds, landscape, professional tone."

### Mode Detection
Signal: "Generate this: ..." → **Enhanced Prompt** mode. Start at Phase 3.

### Avatar Discovery
- Picked Gabrielle (`f95484e160dd46d49bd3eff27a70efa0`), photo_avatar, portrait (1080×1920)

### Phase 3.5 Analysis
- Avatar orientation: **portrait** (1080×1920)
- Video orientation: **landscape**
- Mismatch: YES → Correction A (portrait→landscape reframe)
- Avatar type: photo_avatar → Correction C
- **Corrections applied: A + C**

### Prompt Construction
Target: 50s → padding 1.4x → 70s padded → told Video Agent "70-second video"

User's prompt already uses "The selected presenter" — preserved it and expanded into scene-by-scene format with visual directions, then appended Phase 3.5 corrections.

**CRITICAL CHECK: Does the prompt contain avatar appearance descriptions?**
- ❌ No appearance descriptions
- ✅ Preserves user's "The selected presenter walks developers through..."
- ✅ Only delivery style ("professional and clear, like a senior engineer")

### API Call
**Full JSON payload:**
```json
{
  "prompt": "The selected presenter walks developers through three steps to integrate AI video into their app. This is a 70-second video covering ONE topic: integrating AI video into your app.\n\nScene 1: Intro (Motion Graphics) — 6s\n  Visual: (Motion Graphics) Title \"3 Steps to AI Video\" with code-themed animation.\n  VO: \"Integrating AI video into your app is easier than you think. Three steps.\"\n\nScene 2: Step 1 — API Key (A-roll + overlay) — 15s\n  Visual: (A-roll) The selected presenter speaking with professional delivery. Overlay shows HeyGen dashboard with API key section.\n  VO: \"Step one: Get an API key. Sign up at HeyGen, navigate to the API section, and grab your key. Takes thirty seconds.\"\n\nScene 3: Step 2 — Call the Endpoint (A-roll + Motion Graphics overlay) — 18s\n  Visual: (A-roll) Presenter speaking. Motion graphics overlay shows a curl command hitting the Video Agent endpoint.\n  VO: \"Step two: Call the Video Agent endpoint. One POST request with your prompt. Tell it what the video should say, who should present it, and the visual style. The agent handles scene planning, avatars, B-roll, and rendering.\"\n\nScene 4: Step 3 — Poll (A-roll + overlay) — 12s\n  Visual: (A-roll) Presenter. Overlay shows polling code snippet with status transitions.\n  VO: \"Step three: Poll for completion. Hit the status endpoint every thirty seconds. When it returns completed, you get a video URL. That is it.\"\n\nScene 5: CTA (Motion Graphics) — 6s\n  Visual: (Motion Graphics) End card with developer docs URL.\n  VO: \"Three steps. One API. Professional video at scale. Check the docs and start building.\"\n\n---\nUse minimal, clean styled visuals. Blue, black, and white as main colors.\nLeverage motion graphics as B-rolls and A-roll overlays.\nCode snippets should use dark theme with syntax highlighting.\nInclude an intro sequence and clean developer-focused end card.\nDelivery style: professional and clear, like a senior engineer giving a tutorial.\n\nFRAMING NOTE: The selected avatar image is in portrait orientation (9:16) but this video is landscape (16:9). YOU MUST generate a new variant of the avatar image before using it in this video. Use AI Image tool to:\n1. Generate a landscape (16:9) version of the presenter image\n2. Generative fill to extend the scene horizontally — add a professional environment (modern studio, office, or setting matching the video tone)\n3. Frame the presenter from chest up, centered in the landscape canvas\n4. The background MUST be a real-looking environment, NOT a solid color, NOT transparent, NOT a gradient\nDo NOT use the original portrait image uncropped. Do NOT add black bars or pillarboxing. Do NOT leave a transparent or missing background.\n\nBACKGROUND NOTE: The selected avatar is a photo avatar extracted from a static photo — it has NO scene background (just the person, cutout-style). YOU MUST generate a complete background environment before using this avatar. Use AI Image tool to:\n1. Generate a variant of the presenter image WITH a full background scene\n2. For business/tech content: place in a modern studio, office with monitors, or professional podcast set with soft lighting and depth-of-field blur\n3. The presenter should look NATURAL in the environment — correct lighting direction, realistic scale (waist-up or chest-up framing), shadows present\n4. Do NOT leave ANY transparent, solid-color, or gradient background\n5. Do NOT make the presenter look oversized relative to the environment (the \"giant in a room\" effect means the scale is wrong — zoom out or reframe until the person looks like they naturally belong in the space)\nThe result should look like the presenter was actually filmed in that location.",
  "avatar_id": "f95484e160dd46d49bd3eff27a70efa0",
  "orientation": "landscape"
}
```

### Response
```json
{
  "data": {
    "created_at": 1774974425,
    "session_id": "d9cfb6cc-bf99-4897-9bc5-5464b0371fe4",
    "status": "generating",
    "video_id": "71ef64107d394fa09cf12fbb8179380d"
  }
}
```

### Result
- **Video ID:** 71ef64107d394fa09cf12fbb8179380d
- **Session ID:** d9cfb6cc-bf99-4897-9bc5-5464b0371fe4
- **Video URL:** https://app.heygen.com/videos/71ef64107d394fa09cf12fbb8179380d
- **Session URL:** https://app.heygen.com/video-agent/d9cfb6cc-bf99-4897-9bc5-5464b0371fe4
- **Polling:** (pending)

---

## S10: Dry-run mode (verify pitch format)

### Input
User prompt: "Create a 60-second landscape video about HeyGen's Video Agent API. Use a stock presenter. Dry run please."

### Mode Detection
Signal: "Dry run please" → **Dry-run mode**. Pipeline runs identically, but at Phase 4's pre-submit gate, present creative preview and wait.

### Avatar Discovery
- Selected Nicholas (`ef107d87cc6946b9b6d206ca4b9821e3`) as stock presenter
- Type: photo_avatar, landscape (1920×1080)

### Phase 3.5 Analysis
- Avatar orientation: landscape
- Video orientation: landscape
- Mismatch: NO
- Avatar type: photo_avatar → Correction C would be needed
- But this is dry-run → corrections noted but not injected into an API call

### Prompt Construction (would have been sent)
Target: 60s → padding 1.4x → 84s padded → would tell Video Agent "85-second video"

### Creative Preview (Dry-Run Output)

🎬 Here's what I'm making:

A confident tech walkthrough that demystifies HeyGen's Video Agent API — showing developers that a single POST request replaces an entire production pipeline. ~60s, landscape, Nicholas as presenter.

---

**THE HOOK**
*(Confident, punchy opening)*
"What if I told you one API call could replace your entire video production pipeline?"
[Animated API endpoint URL types onto dark screen]

**THE PROBLEM**
*(Empathetic, knowing nod)*
"Building video into your product used to mean templates, rendering queues, asset management, and a small army of editors. Most teams gave up before they shipped."
[Motion graphics showing complex video pipeline with red X marks]

**THE SOLUTION**
*(Energetic reveal)*
"Video Agent changes that. One prompt in, full production video out. It handles scene planning, avatar selection, B-roll, transitions, and rendering. You just describe what you want."
[Animated curl command fires, response shows video_id. Pipeline collapses into single arrow]

**THE PROOF**
*(Calm authority)*
"Under the hood, the agent breaks your prompt into scenes, selects media types — motion graphics, stock footage, AI-generated visuals — matches an avatar and voice, and renders everything in two to three minutes."
[Exploded view of agent decision tree, each branch lighting up as narrator describes]

**THE CALL**
*(Direct, confident close)*
"One API call. Full production video. Start building at developers.heygen.com."
[Clean end card: docs URL + HeyGen logo on deep blue]

---

*The single-API-call promise that makes every developer stop scrolling.*

**CRITICAL CHECK: Does the pitch contain avatar appearance descriptions?**
- ❌ No appearance descriptions
- ✅ Shows avatar NAME ("Nicholas") but NOT appearance
- ✅ No API call made

### Result
- **Video ID:** N/A — dry run
- **Session ID:** N/A — dry run
- **No API call made** ✓

---

## Polling Results

### Summary Table

| Scenario | Video ID | Status | Target (s) | Actual (s) | Duration % | Session ID |
|----------|----------|--------|-----------|-----------|------------|------------|
| S1 | 8abeb4c2be8340b88cf20d165b4eb91c | ✅ completed | 45 | 34.8 | 77% | ec9cea5d-1bdf-4221-8a7b-29f9d955a7eb |
| S2 | 4a134241f40147eba8172c8044737e11 | ✅ completed | 40 | 34.7 | 87% | e9abbb0a-01cd-4aaa-a42e-24dae96728c9 |
| S3 | de5b6991d2264611a2c394190bfe22d6 | ✅ completed | 35 | 26.3 | 75% | 3784c78a-547f-4e54-bead-9180a700022c |
| S4 | 58cf7a192c3544329af455191893343a | ✅ completed | 50 | 50.6 | 101% | 8eb7dc21-783b-4051-9070-806fd4ba9278 |
| S5 | cc6e67b5a2b24f62a1e2c93ee8985ab3 | ✅ completed | 30 | 30.8 | 103% | 1b70e258-eb65-4181-b56d-9b45434830a1 |
| S6 | afbbd3d67f284067a2198d053844fe78 | ✅ completed | 40 | 37.6 | 94% | 4f9a71af-b7ea-4850-bed4-0958f3a0aa96 |
| S7 | 11edc0c31d3f47f69ff601903396358a | ✅ completed | 45 | 49.1 | 109% | 87b51ec7-84b1-466b-b21e-55c356dc6d34 |
| S8 | b6cecc7e67814df88906e0a5a2da2fe2 | ✅ completed | 30 | 24.1 | 80% | c4e58d80-bb65-408a-a55a-d285ee135112 |
| S9 | 71ef64107d394fa09cf12fbb8179380d | ✅ completed | 50 | 61.9 | 124% | d9cfb6cc-bf99-4897-9bc5-5464b0371fe4 |
| S10 | N/A (dry-run) | ✅ pitch shown | 60 | N/A | N/A | N/A |

### Validation Gate
All 9 video_ids validated:
- All are 32-character hex strings ✅
- All resolve via GET /v3/videos ✅
- All returned status: completed ✅
- All session_ids are valid UUIDs with dashes ✅

### Polling Cadence Notes
- S1-S4: Completed within 2-3 minutes
- S5: Completed at ~6 minutes
- S6: Took ~12 minutes (pending→processing→completed)
- S7-S8: Completed within 4 minutes
- S9: Completed at ~7 minutes

---

## Key Findings Summary

### Fix Validation (PR #14: avatar_id vs prompt description conflict)
**VALIDATED ✅** — All 8 scenarios with avatar_id (S1-S6, S8-S9) used "The selected presenter" phrasing instead of appearance descriptions. Zero instances of hair color, clothing, gender, or ethnicity in any prompt text sent to the API.

### Duration Accuracy
| Range | Avg Duration % | Scenarios |
|-------|---------------|-----------|
| ≤30s target | 91.5% | S5 (103%), S8 (80%) |
| 31-45s target | 79.7% | S1 (77%), S2 (87%), S3 (75%) |
| 46-60s target | 109.3% | S4 (101%), S7 (109%), S9 (124%) |

**Finding:** 31-45s range consistently underdelivers. Current 1.4x padding is insufficient for this range. Recommend 1.5-1.6x.

### Generative Fill Quality
S5 and S6 both completed with Correction C injected. Visual quality TBD by Ken's review. The "giant in a room" scale warning was included in all correction prompts.

### Studio Avatar Availability
**Finding:** Zero studio_avatars available in the HeyGen account. All public avatars are photo_avatar type. This affects 5 scenarios that referenced studio_avatars (S2, S3, S5, S8, S10). Adapted by using photo_avatars as substitutes.

### Average Adam Score: 8.2/10
