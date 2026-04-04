# Round 18 Scenarios — Square Avatar (1:1) Correction Validation

**Focus:** Validate that Phase 3.5 correctly detects square avatars and applies generative fill corrections instead of producing letterboxed video with black bars.

**Test avatar:** Cleo — `avatar_id: 636c7609d11546b999c93ee343fde086` (photo_avatar, 2048×2048 square image, talking photo type)

**Pre-baked context (warm eval):**
- avatar_id: `636c7609d11546b999c93ee343fde086`
- Avatar name: Cleo
- Avatar type: photo_avatar (talking photo)
- Source image: 2048×2048 (1:1 square)
- Voice: use default voice (voice_id `TmvdH7pic9RpWJ1hUe0Q`) or let Video Agent pick

**Critical validation per scenario:**
1. Phase 3.5 MUST fire (square avatar always needs correction)
2. Correction block D (square→landscape) or E (square→portrait) MUST be appended to prompt
3. The prompt MUST contain "AI Image tool" trigger phrase
4. The prompt MUST NOT describe Cleo's appearance (avatar_id is set)

---

## S1: Square Avatar + Landscape (Core Case)
**Prompt:** "Create a 30-second weekly update video for a plant care app called GreenThumb. Use the Cleo avatar. Landscape for YouTube. Friendly and upbeat tone."
**Test:** Square (1:1) avatar → landscape (16:9) video. Phase 3.5 must detect square dimensions and inject Correction D (square→landscape). This is the primary bug case — without correction, video gets pillarboxed (black bars on sides).
**Target:** 30s
**Expected:** Phase 3.5 fires, Correction D appended, avatar_id in payload, no appearance description in prompt, video fills full 16:9 frame.

## S2: Square Avatar + Portrait (Inverse Case)
**Prompt:** "Make a 20-second TikTok announcing a flash sale on succulents. Use the Cleo avatar. Portrait format. Energetic, fun, use motion graphics for the sale prices."
**Target:** 20s
**Test:** Square (1:1) avatar → portrait (9:16) video. Phase 3.5 must inject Correction E (square→portrait).
**Expected:** Phase 3.5 fires, Correction E appended, portrait orientation, avatar_id in payload.

## S3: Square Avatar + Style ID + Landscape
**Prompt:** "Create a 45-second explainer about indoor plant care basics using the Cleo avatar. Browse HeyGen styles and pick something that fits a nature/lifestyle theme. Landscape."
**Test:** Combines style_id selection with square avatar correction. Both should coexist — style_id for visual template, Phase 3.5 for avatar framing.
**Target:** 45s
**Expected:** style_id in payload AND Phase 3.5 Correction D appended. Both features work together without conflict.

## S4: Square Avatar + Quick Shot Mode
**Prompt:** "Just generate a quick 15-second video with Cleo talking about weekend gardening tips. Landscape."
**Test:** Quick Shot mode with explicit avatar_id. Phase 3.5 should STILL fire even in Quick Shot — square detection isn't skipped for fast paths.
**Target:** 15s
**Expected:** Quick Shot flow (minimal questions), but Phase 3.5 still fires with Correction D. avatar_id: 636c7609d11546b999c93ee343fde086 in payload.

## S5: Square Avatar + Voice-Over Hybrid
**Prompt:** "Make a 30-second Instagram Reel. Cleo introduces herself in the first 10 seconds, then transition to voice-over with plant care tips and stock footage of gardens. Portrait format."
**Test:** Avatar used for partial narration + voice-over sections. Phase 3.5 must still correct the square avatar for the presenter sections. Portrait orientation.
**Target:** 30s
**Expected:** Phase 3.5 fires, Correction E (square→portrait) appended, avatar_id in payload, prompt describes the presenter/VO transition clearly.

## S6: Square Avatar + Dry Run (Prompt Assembly Verification)
**Prompt:** "Dry run: Create a 60-second cinematic plant documentary narrated by Cleo. She's introducing rare tropical plants. Landscape. Use stock footage for plant close-ups and AI-generated visuals for dramatic jungle environments."
**Test:** Full pipeline dry run — verify the assembled prompt includes Correction D for the square avatar without making an API call. Allows manual inspection of the complete prompt.
**Target:** 60s
**Expected:** Creative preview shown. Assembled prompt visible with Correction D (square→landscape) appended. No API call. Script framing directive present. Media type guidance explicit.
