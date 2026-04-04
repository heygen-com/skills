# Round 16 Scenarios — style_id + incognito_mode validation

**Focus:** Test style_id browsing workflow (new SKILL.md addition) + confirm incognito_mode isolation + baseline regression on core paths.

**New in this round:**
- All submissions MUST include `"incognito_mode": true` (per eval-runner-prompt.md setup step 4)
- S1–S4 test the new style_id browsing and selection flow
- S5–S8 are regression baselines on core paths

---

## S1: Style-First Video (User Picks from Browse)
**Prompt:** "Make me a 30-second product launch video for a new smart water bottle called HydroSync. I don't have a strong visual preference — show me some style options."
**Test:** Does SKILL.md guide the agent to browse styles via `GET /v3/video-agents/styles`, show thumbnails/previews, and let user pick? Does the chosen `style_id` get passed to the API call?
**Target:** 30s
**Expected:** Agent browses styles, shows previews, user picks one, `style_id` in API payload.

## S2: Style + Prompt Override (Brand Colors on Top of API Style)
**Prompt:** "Create a 45-second explainer about renewable energy trends. Use one of the cinematic styles from HeyGen, but I need my brand colors: #2D5F3B (forest green) and #F5E6CC (cream). Font: Playfair Display."
**Test:** Does the agent browse styles filtered by `tag=cinematic`, pick one, AND layer brand-specific prompt style on top?
**Target:** 45s
**Expected:** `style_id` set + additional color/font direction in prompt text. Both coexist.

## S3: Style Browse with Tag Filter
**Prompt:** "I want a retro-tech aesthetic for a 30-second AI tool demo. What styles do you have?"
**Test:** Does the agent filter by `tag=retro-tech` specifically? Does it show thumbnails and preview videos?
**Target:** 30s
**Expected:** Agent calls `GET /v3/video-agents/styles?tag=retro-tech`, shows results with visual previews.

## S4: No Style Preference — Catchall Default
**Prompt:** "Quick 15-second announcement that our app just hit 1 million downloads. Just make it look good."
**Test:** When user says "just make it look good" and it's Quick Shot mode, does the agent use the catchall style block from SKILL.md (or pick a style_id), rather than generating with zero visual direction?
**Target:** 15s
**Expected:** Either a style_id selected or the default catchall block injected. Not a bare prompt with no visual direction.

## S5: Photo Avatar + Landscape (Regression Baseline)
**Prompt:** "Create a 45-second tutorial about setting up a home office for remote work. Use my avatar Eve Park. Landscape for YouTube."
**Test:** Core path regression. Photo avatar lookup, landscape, script framing directive, no Phase 3.5 corrections needed (matched orientation).
**Target:** 45s
**Expected:** Clean generation, avatar_id resolved, script framing directive present, no corrections.

## S6: Voice-Over Only + Portrait (Regression)
**Prompt:** "Make a 30-second Instagram Reel about morning productivity routines. No presenter — voice-over only. Energetic and motivating."
**Test:** Voice-over path, portrait orientation, no avatar_id, script framing directive.
**Target:** 30s
**Expected:** No avatar_id in payload, portrait orientation, script framing directive present.

## S7: Photo Avatar + Portrait Mismatch (Phase 3.5 Test)
**Prompt:** "Create a 30-second LinkedIn post video about AI in healthcare. Use Eve Park avatar. Portrait format for mobile."
**Test:** Photo avatar is landscape, video is portrait. Phase 3.5 should fire Framing Correction (A or B).
**Target:** 30s
**Expected:** Phase 3.5 triggers, framing correction appended to prompt with "AI Image tool" trigger phrase.

## S8: Dry Run (Prompt Assembly Verification)
**Prompt:** "Dry run: Make a 60-second cinematic explainer about the future of autonomous vehicles. Use a cinematic style from HeyGen. Include stock footage for real driving scenes and AI-generated visuals for futuristic concepts."
**Test:** Full pipeline verification without API spend. Check: style_id selected, media type guidance explicit, script framing directive, no per-scene durations.
**Target:** 60s
**Expected:** Creative preview shown with style choice, media type directions, script framing directive visible in assembled prompt. No API call made.
