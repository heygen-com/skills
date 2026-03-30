# Round 2 Scenarios — Aspect Ratio & Background Corrections

**Theme:** Test Phase 3.5 (Aspect Ratio & Background Pre-Check) across every combination of avatar type, orientation, and edge case.

**Notion parent page:** 🌱 Agentic Skills GTM (31e44979-2c69-8097-a181-f16d2fa8149f)

---

## S1: Portrait Custom Avatar → Landscape Video
**Prompt:** "Create a 60-second video about why startups should use AI video for investor updates. Use Eve's Podcast look. Landscape orientation. Energetic YouTuber tone."
**Expected behavior:**
- Phase 3.5 triggers: detects portrait avatar in landscape request
- "FRAMING NOTE" correction injected into prompt silently
- No user-facing question about aspect ratio
- Output: Eve framed chest-up in 16:9, NO black bars or pillarboxing
- Log entry includes `"aspect_correction": "portrait_to_landscape"`
**Watch for:** Black bars, awkward cropping, correction prompt visible to user

---

## S2: Portrait Custom Avatar → Portrait Video (Matched)
**Prompt:** "Create a 30-second TikTok-style video about the top 3 AI video tools in 2026. Use Eve's Podcast look. Portrait orientation. Fast-paced, punchy."
**Expected behavior:**
- Phase 3.5 runs but detects NO mismatch (portrait avatar + portrait video)
- No correction injected
- Log entry includes `"aspect_correction": "none"`
**Watch for:** False positive — correction injected when it shouldn't be

---

## S3: Landscape Stock Avatar → Portrait TikTok
**Prompt:** "Create a 30-second vertical video about how MCP servers work, for TikTok. Use a stock avatar — browse what's available. Portrait orientation. Casual explainer."
**Expected behavior:**
- Stock avatar selected via group-first browsing
- Phase 3.5 detects landscape stock avatar in portrait request
- "FRAMING NOTE" for landscape→portrait correction injected
- Output: avatar fills portrait frame naturally
- Log entry includes `"aspect_correction": "landscape_to_portrait"`
**Watch for:** Stock avatar browsing UX (pagination issues), correction quality

---

## S4: Custom Avatar with Transparent Background → Landscape
**Prompt:** "Create a 60-second video about HeyGen's API ecosystem. Use Eve Park original upload look. Landscape. Professional tech demo tone."
**Expected behavior:**
- Phase 3.5 detects transparent/missing background on the original upload look
- "BACKGROUND NOTE" correction injected
- Video Agent places Eve in appropriate professional environment
- Log entry includes `"aspect_correction": "background_fill"`
**Watch for:** Floating head on empty canvas, generic/ugly background, correction not triggering

---

## S5: Voice-Over Only → Landscape (No Avatar)
**Prompt:** "Create a 45-second voice-over explainer about the future of agentic AI. No visible presenter — voice only. Landscape. Thoughtful, documentary tone."
**Expected behavior:**
- No avatar_id set → Phase 3.5 SKIPS entirely
- No correction injected (nothing to correct)
- Video Agent generates visuals from prompt without avatar
- Log should NOT have `aspect_correction` field or show `"none"`
**Watch for:** Phase 3.5 crashing on missing avatar_id, unnecessary corrections

---

## S6: Quick Shot with Custom Avatar (No Explicit Orientation)
**Prompt:** "Quick video: Eve's Podcast look explains what MCP is in 30 seconds."
**Expected behavior:**
- Quick Shot mode detected (one-liner)
- Default orientation applied (should be landscape per SKILL.md defaults)
- Phase 3.5 detects portrait Eve look vs default landscape
- Correction injected automatically
**Watch for:** Does Quick Shot mode still trigger Phase 3.5? Does default orientation get set correctly?

---

## S7: Dry-Run with Portrait Avatar → Landscape
**Prompt:** "Dry run: Create a 90-second video about Synthesia vs HeyGen for enterprise. Use Eve's Podcast look. Landscape. Analytical, confident tone."
**Expected behavior:**
- Full Phase 1-3 pipeline runs (discovery, script, prompt engineering)
- Phase 3.5 triggers, detects mismatch, prepares correction
- Dry-run preview shows the creative pitch
- Correction is documented in the preview (user can see it will be applied)
- NO API call made, NO credits consumed
- No video_id generated
**Watch for:** Does dry-run preview mention the aspect correction? Does Phase 3.5 run before or after the preview gate?

---

## S8: Stock Avatar (Unknown Preview) → Landscape
**Prompt:** "Create a 60-second video about Claude Code vs OpenClaw. Pick any stock avatar that looks like a tech reviewer. Landscape. Opinionated YouTuber."
**Expected behavior:**
- Stock avatar selected by description
- If preview URL is unavailable/broken, Phase 3.5 falls through to "background safety" path
- Background safety prompt injected as fallback
- Video still generates successfully
**Watch for:** How skill handles missing preview_image_url, error handling in Phase 3.5

---

## S9: Custom Avatar + Style Preset → Landscape
**Prompt:** "Create a 60-second cinematic-style video about the death of Sora. Use Eve's Cozy Studio Host look. Landscape. Dramatic documentary tone. Use a cinematic style if available."
**Expected behavior:**
- Style discovery runs (Phase 1)
- Avatar look selected (Cozy Studio Host)
- Phase 3.5 runs: aspect ratio check + any background check
- Style preset AND correction coexist in the final prompt without conflict
- Both style_id and avatar_id passed to API
**Watch for:** Style + correction prompt conflicting, one overriding the other

---

## S10: Long-Form Stress Test — Portrait Avatar + Landscape + PDF + Multiple Concerns
**Prompt:** "Create a 2-minute deep-dive video about Anthropic's Responsible Scaling Policy. Use Eve's Podcast look. Landscape. Attach this PDF as reference: https://www-cdn.anthropic.com/1adf000c8f675958c2ee23805d91aaade1f9d1c8/responsible-scaling-policy.pdf. Analytical, measured tone. Include on-screen data points from the PDF."
**Expected behavior:**
- Full Producer mode with maximum complexity
- Phase 3.5: portrait→landscape correction
- PDF uploaded as asset via `POST /v3/assets`, passed in `files` array
- 1.3x padding multiplier (120s+ content)
- Multi-scene script with data points extracted from PDF
- Duration target: 120s padded → ~156s target
- All features coexist: avatar_id + correction + files + long-form padding
**Watch for:** Asset upload failures, correction + files interaction, duration accuracy on long-form, prompt getting too large, any Phase 3.5 issues when combined with file attachments
