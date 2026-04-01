# Round 14 Scenarios — Phase 3.5 Regression Fix Validation

**Focus:** Validate inlined Phase 3.5 corrections (PR #20), photo_avatar bg logic fix, and script framing directive. No interactive sessions. No dry runs.

**Round:** 14
**Date:** 2026-04-01
**Fixes Tested:** Inlined correction templates (A/B/C), photo_avatar no longer gets Correction C, script framing directive

---

## S1: Quick Shot — 15s (Script Framing Fix Retest)
- **Type:** Quick Shot
- **Target Duration:** 15 seconds
- **Prompt:** "The best AI tools don't replace creativity — they remove the boring parts so you can focus on what actually matters"
- **Avatar:** None (voice-over only)
- **Expected:** Script framing directive in prompt, natural delivery without weird pauses, ~15s output
- **Fix Tested:** Script-as-concept directive preventing pause insertion

## S2: Photo Avatar — Portrait in Landscape (Correction A Retest)
- **Type:** Full Producer
- **Target Duration:** 30 seconds
- **Topic:** "Why every startup needs video content in 2026"
- **Avatar:** Use any photo_avatar from your account. Pick one that is in PORTRAIT orientation.
- **Video Orientation:** Landscape (16:9)
- **Expected:** Phase 3.5 fires Correction A (portrait→landscape framing). Generative fill extends canvas. Photo-realistic background. NO Correction C (photo_avatar doesn't need standalone bg fill).
- **Fix Tested:** Correction A inlined in SKILL.md + photo_avatar excluded from Correction C

## S3: Photo Avatar — Landscape Matched (No Correction Needed)
- **Type:** Full Producer
- **Target Duration:** 45 seconds
- **Topic:** "3 things I learned building AI agents this year"
- **Avatar:** Use any photo_avatar from your account. Pick one that is in LANDSCAPE orientation.
- **Video Orientation:** Landscape (16:9)
- **Expected:** Phase 3.5 runs but detects orientation match → NO corrections fired. Clean generation.
- **Fix Tested:** photo_avatar with matching orientation should get ZERO corrections

## S4: Photo Avatar — Landscape in Portrait (Correction B Retest)
- **Type:** Full Producer
- **Target Duration:** 30 seconds
- **Topic:** "Quick tip: how to use AI video for Instagram Reels"
- **Avatar:** Use any photo_avatar in LANDSCAPE orientation.
- **Video Orientation:** Portrait (9:16)
- **Expected:** Phase 3.5 fires Correction B (landscape→portrait). Generative fill extends vertically. NO Correction C.
- **Fix Tested:** Correction B inlined + photo_avatar excluded from Correction C

## S5: 60s Explainer — Script Framing at Length
- **Type:** Full Producer
- **Target Duration:** 60 seconds
- **Topic:** "How HeyGen's Video Agent API works — from prompt to finished video in under 2 minutes"
- **Avatar:** Use any photo_avatar with matching orientation to requested video (landscape)
- **Video Orientation:** Landscape (16:9)
- **Expected:** Script framing directive present. No per-scene time allocations. Natural pacing. Phase 3.5 fires only if orientation mismatch.
- **Fix Tested:** Script-as-concept at 60s length + no per-scene durations

## S6: 90s Tutorial — Long Form Script Framing
- **Type:** Full Producer
- **Target Duration:** 90 seconds
- **Topic:** "Step by step: building your first AI video pipeline with HeyGen and OpenClaw"
- **Avatar:** Use any photo_avatar, landscape orientation
- **Video Orientation:** Landscape (16:9)
- **Expected:** Script framing directive present. Content structured by flow (Hook → Problem → Solution → CTA) without per-scene timestamps. ~90s output.
- **Fix Tested:** Script framing at 90s scale, no per-scene duration dictation

## S7: Voice-Over Only — No Avatar (Script Framing Baseline)
- **Type:** Full Producer
- **Target Duration:** 45 seconds
- **Topic:** "The future of content creation is agents that understand your brand"
- **Avatar:** None — voice-over only, no presenter
- **Video Orientation:** Landscape (16:9)
- **Expected:** No Phase 3.5 (no avatar_id set). Script framing directive still present. Clean voice-over generation.
- **Fix Tested:** Script framing without avatar, Phase 3.5 correctly skipped

## S8: Photo Avatar — Portrait in Portrait (Matched, No Correction)
- **Type:** Full Producer
- **Target Duration:** 30 seconds
- **Topic:** "One thing most people get wrong about AI video"
- **Avatar:** Use any photo_avatar in PORTRAIT orientation
- **Video Orientation:** Portrait (9:16)
- **Expected:** Phase 3.5 detects matching orientation → ZERO corrections. photo_avatar in portrait for portrait video = perfect match.
- **Fix Tested:** Matched portrait photo_avatar gets no corrections
