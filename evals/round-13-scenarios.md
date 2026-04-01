# Round 13 Scenarios — Validating R11/R12 Fixes

**Focus:** Three specific fixes from PR #19. No interactive sessions.
1. Script framing (Jerry's "concept not verbatim" directive) — fixes weird pauses
2. Photo-realistic backgrounds (Phase 3.5 hyper-realism rewrite)
3. Per-scene duration removal (Video Agent paces itself)

---

## S1: Short Quick Shot — Pause Regression Test
**Tests:** Script framing fix (weird pauses were worst on short videos ≤30s)
**Input:** "Make a quick 15-second video about why AI agents need video capabilities"
**Mode:** Quick Shot
**Expected:** No awkward pauses or dead air. Natural delivery that fills the time.
**Why:** R11-S3 and R11-S10 both got "weird pauses" verdict from Ken. This is the exact scenario type that triggered it. If Jerry's fix works, delivery should be smooth.

## S2: 60s Explainer — Natural Pacing Test
**Tests:** Script framing + no per-scene duration dictation
**Input:** "Create a 60-second explainer about how MCP (Model Context Protocol) is changing how AI agents connect to tools. Audience: developers. Tone: confident, technical but accessible."
**Mode:** Full Producer
**Avatar:** Use any available photo_avatar (private first, then public)
**Expected:** Smooth delivery with natural pacing. No scene-by-scene time allocation in the prompt. Video Agent decides how to distribute time across sections.
**Why:** Tests that removing per-scene durations + adding "concept not verbatim" produces natural flow.

## S3: Photo Avatar + Landscape — Background Realism Test
**Tests:** Phase 3.5 Correction C (hyper photo-realistic background)
**Input:** "Create a 45-second product announcement: HeyGen now lets any AI agent create videos with a single API call. Exciting, energetic tone."
**Mode:** Full Producer
**Avatar:** Use a photo_avatar (private first). Must be portrait orientation if possible.
**Orientation:** Landscape (16:9)
**Expected:** Phase 3.5 fires Correction C (background fill). Background should look like a real photograph — real studio/office, depth-of-field blur, natural lighting. NOT synthetic/CGI.
**Why:** Ken flagged R11-S5 and R12-S8 backgrounds as not realistic enough. This tests the rewritten correction prompts.

## S4: Portrait Photo Avatar in Landscape — Stacked Corrections
**Tests:** Phase 3.5 Corrections A+C stacking (reframing + background)
**Input:** "Make a 30-second sales pitch for an AI-powered customer support tool. Pain: slow response times. Solution: instant AI responses. Confident, professional."
**Mode:** Full Producer  
**Avatar:** Use a portrait-oriented photo_avatar
**Orientation:** Landscape (16:9)
**Expected:** Phase 3.5 fires BOTH Correction A (portrait→landscape reframing) AND Correction C (background generation). Both should produce hyper photo-realistic results.
**Why:** Stacked corrections were the hardest case in R7-R8. Tests that the rewritten prompts handle the combo.

## S5: 90s Tutorial — Long-Form Pacing Test
**Tests:** Script framing + natural pacing at longer duration (no per-scene times)
**Input:** "Create a 90-second tutorial on how to set up HeyGen's Video Agent API. Walk through: getting an API key, making your first call, and checking the result. Audience: developers new to HeyGen. Friendly, encouraging tone."
**Mode:** Full Producer
**Avatar:** Any available avatar with explicit avatar_id
**Expected:** Natural pacing across the tutorial. No weird pauses between sections. Video Agent distributes time across setup/call/result without us dictating "30s for setup, 40s for call, 20s for result."
**Why:** 90s is mid-range where pacing matters most. Tests that Video Agent can self-pace a multi-section tutorial.

## S6: Voice-Over Only — No Avatar Pause Test
**Tests:** Script framing on voice-over path (no avatar_id, historically had more pauses)
**Input:** "Make a 45-second voice-over video about the rise of AI video generation. Cinematic B-roll, no visible presenter. Tone: documentary-style, authoritative."
**Mode:** Full Producer
**Avatar:** None (voice-over only)
**Orientation:** Landscape
**Expected:** No pauses. Smooth narration. The "concept not verbatim" directive should work equally well without an avatar.
**Why:** Voice-over videos had different pause patterns in R11. Need to confirm the fix works on both paths.

## S7: Studio Avatar in Landscape — Background Check
**Tests:** Phase 3.5 studio_avatar background detection
**Input:** "Create a 30-second announcement: our company just raised Series A funding. Tone: excited but professional."
**Mode:** Full Producer
**Avatar:** Use a public studio_avatar (group-first browsing per SKILL.md)
**Orientation:** Landscape
**Expected:** Phase 3.5 checks if studio avatar has a real background or solid/transparent. If no background, fires Correction C with hyper photo-realistic environment. If background exists, no correction needed.
**Why:** Studio avatars are the ambiguous case (maybe background, maybe not). Tests the detection logic.

## S8: Dry Run — Prompt Inspection
**Tests:** Verify the "concept not verbatim" directive appears in the assembled prompt
**Input:** "Make a 60-second video about why every startup needs AI video for marketing. Dry run."
**Mode:** Dry Run
**Avatar:** Any available
**Expected:** Creative preview shown. The assembled prompt (in the collapsible block) MUST contain the "concept and theme to convey" directive. No per-scene duration allocations visible in the prompt.
**Why:** Meta-test. Confirms the fix is actually being applied in prompt assembly, not just documented.
