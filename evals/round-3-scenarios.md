# Round 3 Scenarios — Phase 3.5 Background Heuristic Validation

Focus: Validate avatar_type-based background detection, correction stacking, and "AI Image tool" trigger phrase.

---

## S1: photo_avatar + landscape (STACKING TEST)
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857) — photo_avatar, portrait
- **Orientation:** landscape (default)
- **Duration:** 30s
- **Topic:** "Quick tip: why every AI agent needs a video skill"
- **Expected corrections:** BOTH framing note (portrait→landscape) AND background note (photo_avatar)
- **Validates:** Correction stacking, "AI Image tool" trigger phrase

## S2: photo_avatar + portrait (MATCHED, background only)
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857) — photo_avatar, portrait
- **Orientation:** portrait
- **Duration:** 30s
- **Topic:** "TikTok: 3 reasons developers ignore video"
- **Expected corrections:** Background note ONLY (no framing — orientation matches)
- **Validates:** photo_avatar always gets background, no false framing injection

## S3: studio_avatar + landscape (MATCHED, no corrections)
- **Avatar:** Pick any studio_avatar from GET /v3/avatars/looks?ownership=public&avatar_type=studio_avatar (e.g. Daphne, Aditya)
- **Orientation:** landscape
- **Duration:** 30s
- **Topic:** "What is MCP and why it matters"
- **Expected corrections:** NONE (studio_avatar + matched orientation)
- **Validates:** studio_avatar skips background check entirely

## S4: studio_avatar + portrait (MISMATCHED, framing only)
- **Avatar:** Pick a LANDSCAPE studio_avatar from stock
- **Orientation:** portrait
- **Duration:** 30s
- **Topic:** "Instagram Reel: one tool every developer should try"
- **Expected corrections:** Framing note ONLY (landscape→portrait). NO background note.
- **Validates:** studio_avatar never gets background note even with mismatch

## S5: video_avatar + landscape (MATCHED, no corrections)
- **Avatar:** Pick any video_avatar from GET /v3/avatars/looks?ownership=public&avatar_type=video_avatar
- **Orientation:** landscape
- **Duration:** 30s
- **Topic:** "The state of AI video in 2026"
- **Expected corrections:** NONE (video_avatar + matched orientation)
- **Validates:** video_avatar treated same as studio_avatar

## S6: photo_avatar + landscape + 60s (STACKING + LONGER FORM)
- **Avatar:** Eve Park original upload (look from Eve Park group, NOT Eve's Podcast)
- **Orientation:** landscape
- **Duration:** 60s
- **Topic:** "Why Sora failed and what it means for AI video"
- **Expected corrections:** BOTH framing + background (photo_avatar + likely portrait mismatch)
- **Validates:** Stacking works on longer content, padding multiplier (1.4x)

## S7: Quick Shot + photo_avatar (QUICK SHOT + PHASE 3.5)
- **Prompt:** "Make a 30s video with Eve's Podcast look about the future of agent skills"
- **Mode:** Quick Shot (one-liner prompt)
- **Expected corrections:** BOTH framing + background (Quick Shot should still run Phase 3.5)
- **Validates:** Phase 3.5 runs in Quick Shot mode when avatar_id is present

## S8: Dry-run + photo_avatar (DRY-RUN SHOWS CORRECTIONS)
- **Avatar:** Eve's Podcast
- **Orientation:** landscape
- **Duration:** 60s
- **Topic:** "How HeyGen's Video Agent API works"
- **Mode:** Dry-run (preview only, zero API calls)
- **Expected:** Dry-run preview should SHOW which corrections would be injected
- **Validates:** Dry-run surfaces correction info before user approves

## S9: voice-over only (NO avatar — skip Phase 3.5)
- **Avatar:** None (voice-over only)
- **Orientation:** landscape
- **Duration:** 30s
- **Topic:** "5 things I learned building AI video skills"
- **Expected corrections:** NONE (no avatar_id → Phase 3.5 skipped entirely)
- **Validates:** Phase 3.5 correctly skips when no avatar

## S10: photo_avatar + landscape + multi-asset stress test
- **Avatar:** Eve's Podcast (05bf07b91de446a3b6e5d47c48214857)
- **Orientation:** landscape
- **Duration:** 120s
- **Topic:** "Complete guide to HeyGen's v3 API migration"
- **Assets:** Upload a PDF (use any public PDF URL) + reference URL (https://developers.heygen.com/docs/quick-start)
- **Expected corrections:** BOTH framing + background (photo_avatar + portrait→landscape)
- **Validates:** Stacking works with assets, long-form padding (1.3x), full pipeline

---

## Scoring Focus for Round 3

For each scenario, the eval runner MUST document:
1. **Which correction blocks were injected** (quote the exact text from the prompt)
2. **Whether the avatar_type was correctly identified** (photo_avatar vs studio_avatar vs video_avatar)
3. **Visual result:** Did the video actually have a proper background? Was framing correct?
4. **Log entry:** Does it contain `avatar_type` and `aspect_correction` fields?

### Pass Criteria
- S1, S6, S7, S10: Both corrections injected → PASS
- S2: Background only, no framing → PASS
- S3, S5: Zero corrections → PASS
- S4: Framing only, no background → PASS
- S8: Dry-run shows corrections → PASS
- S9: Phase 3.5 skipped → PASS
