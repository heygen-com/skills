# Round 9 — Style System + Prompt Engineering Overhaul

**Theme:** Validate the style system integration (PR #17). Test API styles, prompt styles, no styles, style combinations, critical on-screen text, natural flow vs scene-by-scene, and core flow regression.
**Date:** 2026-03-31
**Branch:** `feat/styles-and-prompt-system` (merge to main first or read SKILL.md from this branch)
**Prereq:** Read the updated SKILL.md carefully. Note the new Style Selection section, Critical On-Screen Text step, and Natural Flow vs Scene-by-Scene branching in Phase 3.

## Scenarios

### S1 — API Style: Browse + Pick (cinematic tag)
**Mode:** Full Producer
**Prompt idea:** "Make a 60-second video about the history of jazz music"
**Style instruction:** User says: "I want it to look cinematic"
**What to do:** Browse `GET /v3/video-agents/styles?tag=cinematic&limit=5`. Show thumbnails. Pick a style. Pass `style_id` in the API call. Use Natural Flow prompt approach (≤60s).
**What to verify:**
- [ ] Style discovery API called with `tag=cinematic`
- [ ] Thumbnail/preview shown to simulate user choice
- [ ] `style_id` passed in POST /v3/video-agents request body
- [ ] Visual Style Block in prompt is simplified or omitted (style handles it)
- [ ] Video generates successfully
- [ ] Duration accuracy logged

### S2 — API Style: Browse + Skip (none fit)
**Mode:** Full Producer
**Prompt idea:** "Make a 45-second video about sustainable farming practices"
**Style instruction:** User says: "Something earthy and organic"
**What to do:** Browse `GET /v3/video-agents/styles?tag=handmade&limit=5`. Show results. Decide none fit perfectly. Fall back to Prompt Style: use "Warm Grain (Eksell)" from prompt-styles.md.
**What to verify:**
- [ ] Style discovery API called
- [ ] Explicit decision: "API styles don't quite match, using prompt style instead"
- [ ] No `style_id` in API call
- [ ] Warm Grain STYLE block present in prompt text
- [ ] Video generates successfully

### S3 — Prompt Style: Manual Pick (Swiss Pulse, data-heavy)
**Mode:** Full Producer
**Prompt idea:** "Make a 75-second video about Q1 2026 AI market data: $847M market size, 18.8% CAGR, 97M MCP downloads/month, 5800+ MCP servers"
**Style instruction:** User says: "Data-heavy, clinical, like a Bloomberg briefing"
**What to do:** Recommend Swiss Pulse from prompt-styles.md. Use Scene-by-Scene approach (>60s + data-heavy). Include Critical On-Screen Text block with all 4 stats.
**What to verify:**
- [ ] Swiss Pulse STYLE block in prompt
- [ ] Scene-by-Scene prompt structure used (not Natural Flow)
- [ ] CRITICAL ON-SCREEN TEXT block present with exact stats
- [ ] Numbers spelled out in voiceover text ("eight hundred forty-seven million")
- [ ] Figures used on screen ("$847M")
- [ ] No `style_id` (prompt style only)
- [ ] Motion verbs used in B-roll scenes (from motion-vocabulary.md)
- [ ] Video generates successfully

### S4 — Prompt Style: Mood-Based Selection
**Mode:** Full Producer
**Prompt idea:** "Make a 50-second video about a breaking security vulnerability in a popular AI framework"
**Style instruction:** User says: "Urgent, breaking news energy"
**What to do:** Consult mood-to-style guide. "Urgent" maps to Red Wire (Tartakover). Copy the STYLE block. Use Natural Flow (≤60s).
**What to verify:**
- [ ] Mood-to-style mapping consulted
- [ ] Red Wire STYLE block in prompt
- [ ] Natural Flow approach used (≤60s, no scene labels)
- [ ] Tone words match the style energy ("urgent", "immediate", "high alert")
- [ ] Video generates successfully

### S5 — No Style: Core Flow Regression (Quick Shot)
**Mode:** Quick Shot
**Prompt idea:** "Make a 30-second video about why every developer needs an AI coding assistant"
**Style instruction:** None. User just says "just generate it, don't ask questions"
**What to do:** Quick Shot mode. No style browsing. No `style_id`. Default Visual Style Block. No avatar_id (Quick Shot auto-select exception). Natural Flow approach.
**What to verify:**
- [ ] No style discovery calls made
- [ ] No `style_id` in API request
- [ ] Default Visual Style Block used
- [ ] No avatar_id (Quick Shot auto-select)
- [ ] Duration padding 1.6x applied (≤30s target)
- [ ] Video generates successfully
- [ ] **REGRESSION CHECK:** Core Quick Shot flow unchanged from pre-PR behavior

### S6 — No Style: Core Flow Regression (Full Producer, custom avatar)
**Mode:** Full Producer
**Prompt idea:** "Make a 60-second product demo about HeyGen's Video Agent API"
**Style instruction:** None mentioned
**What to do:** Full Producer flow. Discover a private avatar (or any available avatar). Pass `avatar_id`. No style. Default Visual Style Block. Natural Flow (60s).
**What to verify:**
- [ ] Avatar discovery flow works normally
- [ ] `avatar_id` passed, no appearance description in prompt (existing rule)
- [ ] Phase 3.5 correction runs if needed
- [ ] No `style_id`
- [ ] Default Visual Style Block used
- [ ] Session ID captured from response
- [ ] Duration accuracy tracked
- [ ] **REGRESSION CHECK:** Full Producer flow unchanged from pre-PR behavior

### S7 — API Style + Prompt Style Combined (Power User)
**Mode:** Enhanced Prompt
**Prompt idea:** "Make a 45-second video about the rise of agentic AI"
**Style instruction:** User says: "Use the retro-tech style from HeyGen but override the colors to be neon green on black, terminal aesthetic"
**What to do:** Browse `GET /v3/video-agents/styles?tag=retro-tech&limit=5`. Pick a style. Pass `style_id` AND add a prompt style override: "Override base colors: neon green #00FF41 on black #0a0a0a. Monospaced type. Terminal cursor blink." Natural Flow (≤60s).
**What to verify:**
- [ ] `style_id` present in API call (retro-tech style)
- [ ] STYLE override block ALSO present in prompt text
- [ ] Both coexist without conflict
- [ ] Video generates successfully (may or may not honor both — that's a finding)

### S8 — Critical On-Screen Text: Stress Test
**Mode:** Full Producer
**Prompt idea:** "Make a 90-second Synthesia competitor analysis video"
**Key data:** "$4B valuation", "$200M Series E", "$146M ARR", "65% enterprise", Quote: "AI avatars are the next interface" — CEO, "@synthaborgs" handle
**Style instruction:** User says: "Make it investigative, editorial"
**What to do:** Use Contact Sheet (Brodovitch) prompt style. Scene-by-Scene approach (90s). Extract ALL data points into CRITICAL ON-SCREEN TEXT block. Verify voiceover spells out numbers.
**What to verify:**
- [ ] CRITICAL ON-SCREEN TEXT block has all 6 items
- [ ] Each number spelled out in voiceover (e.g., "four billion dollar valuation")
- [ ] Figures used on screen ("$4B")
- [ ] Quote appears with attribution
- [ ] Handle appears exactly as "@synthaborgs"
- [ ] Scene-by-Scene structure used (>60s)
- [ ] Motion verbs from motion-vocabulary.md used in B-roll
- [ ] Video generates successfully

### S9 — Natural Flow vs Scene-by-Scene Decision
**Mode:** Full Producer
**Prompt idea A (short):** "Make a 40-second video about why sleep is the ultimate productivity hack"
**Prompt idea B (long):** "Make a 120-second deep dive into how MCP protocol works under the hood"
**What to do:** Generate TWO videos. Video A uses Natural Flow (≤60s, no scene labels). Video B uses Scene-by-Scene (>60s, with visual layers and motion verbs).
**What to verify:**
- [ ] Video A prompt has NO scene labels, just flowing script + tone
- [ ] Video B prompt HAS scene labels, Visual/VO/Duration per scene
- [ ] Video B uses 5-layer system for at least one B-roll scene
- [ ] Both generate successfully
- [ ] Duration accuracy compared between approaches

### S10 — Dry Run + Style Preview
**Mode:** Full Producer, dry-run
**Prompt idea:** "Make a 75-second video about the death of Sora and what it means for AI video"
**Style instruction:** User says: "Dark, dramatic, like an exposé"
**What to do:** Consult mood guide. "Dark, cinematic" → Shadow Cut (Hillmann). Build the full prompt. Present dry-run creative preview. Do NOT call the API.
**What to verify:**
- [ ] Shadow Cut STYLE block used
- [ ] Dry-run creative preview shown (pitch format, not spec sheet)
- [ ] Scene labels are creative names ("THE HOOK", "THE FALLOUT")
- [ ] Tone cues in italics, visual cues in brackets
- [ ] Logline at end
- [ ] "Say go or tell me what to change" CTA present
- [ ] API NOT called
- [ ] Prompt structure is correct for Scene-by-Scene (>60s)

---

## Scoring

For each scenario, score 1-10:
- **Style handling (1-3):** Did the skill correctly browse/pick/skip/inject styles?
- **Prompt quality (1-3):** Is the prompt well-structured? Correct approach (natural flow vs scene-by-scene)?
- **Execution (1-2):** Did the video generate? Duration accuracy?
- **Regression (1-2):** For S5/S6: does core flow work exactly as before PR #17?

**Pass threshold:** 7/10 per scenario, 75/100 aggregate.

## Eval Tracker

Write results to the Notion Eval Tracker database (ID: a1b997926fe646929ef46cd6144d4b91). One row per scenario. Include: Scenario, Round (9), Fix Tested, Status, Target/Actual duration, Style Used (API/prompt/none), Corrections, Adam Score, Video URL, Session URL, Findings.
