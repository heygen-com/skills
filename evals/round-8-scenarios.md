# Round 8 — Studio Avatar Deep Dive

**Theme:** Hammer studio avatars in every configuration. Photo avatars are solid — now stress-test studio avatars: as-is, with generative fill, with different looks from the same group, with framing corrections, with background requests, landscape vs portrait, with styles, with assets.
**Date:** 2026-03-31
**Prereq:** Discover 3-4 different studio avatar GROUPS via `GET /v3/avatars/groups?type=stock`. Pick groups with multiple looks. For each scenario, discover the specific look via `GET /v3/avatars/looks?group_id=<id>` and always pass explicit `avatar_id`.

## Scenarios

### S1 — Studio avatar as-is, landscape, no modifications
- Prompt: "Create a 45-second landscape video about 5 things every startup founder should know about AI."
- Avatar: Pick any studio_avatar with a REAL background (not transparent). Use them exactly as they are.
- Target: 45s landscape
- **What to verify:** Avatar renders correctly. No corrections needed (matched orientation, has background). Clean baseline.

### S2 — Studio avatar as-is, portrait, no modifications
- Prompt: "Create a 35-second portrait TikTok about why developers should learn prompt engineering."
- Avatar: Same avatar as S1 (landscape look). This forces a landscape→portrait mismatch.
- Target: 35s portrait
- **What to verify:** Phase 3.5 fires correction B (landscape→portrait framing). Check if framing looks natural in portrait.

### S3 — Studio avatar with transparent background + landscape (generative fill)
- Prompt: "Make a 40-second landscape video about the rise of AI coding agents."
- Avatar: Find a studio_avatar look where the preview image has a transparent/solid/empty background.
- Target: 40s landscape
- **What to verify:** Phase 3.5 fires correction C (background fill). "Use AI Image tool to generative fill" trigger present. Background looks natural, avatar isn't oversized or floating.

### S4 — Studio avatar with transparent bg + explicit background request
- Prompt: "Make a 45-second landscape video about remote team communication. Background should be a modern open-plan office with natural lighting."
- Avatar: Same transparent-bg studio_avatar as S3.
- Target: 45s landscape
- **What to verify:** Correction C fires with the user's specific background request ("modern open-plan office"). Background matches the request. Avatar looks naturally placed in the scene.

### S5 — Studio avatar with transparent bg + portrait (double correction)
- Prompt: "Create a 30-second portrait video about quick productivity hacks."
- Avatar: Same transparent-bg studio_avatar as S3 (landscape orientation).
- Target: 30s portrait
- **What to verify:** BOTH corrections fire: B (landscape→portrait framing) AND C (background fill). Corrections stack properly. Avatar reframed AND background generated.

### S6 — Different look from same studio avatar group
- Prompt: "Make a 50-second landscape video about the evolution of large language models."
- Avatar: Pick the SAME avatar group as S1 but a DIFFERENT look (different outfit/setting). Show both looks to compare.
- Target: 50s landscape
- **What to verify:** Different look from same person renders correctly. The look-specific outfit/setting appears. Proves multi-look discovery works.

### S7 — Studio avatar + HeyGen style
- Prompt: "Create a 40-second landscape video about why every SaaS company needs AI features in 2026."
- Avatar: Any studio_avatar with real background.
- Style: Pick a HeyGen style (cinematic, retro-tech, etc.) and pass `style_id`.
- Target: 40s landscape
- **What to verify:** Style is applied to the video. Visual treatment matches the chosen style. Avatar still renders correctly with style overlay.

### S8 — Studio avatar + PDF asset attachment
- Prompt: "Make a 60-second landscape video explaining the key findings from this research report."
- Avatar: Any studio_avatar (preferably different from previous scenarios).
- Asset: Attach a real public PDF URL (e.g., a HeyGen doc or any accessible PDF). Route through download→upload→asset_id path.
- Target: 60s landscape
- **What to verify:** Asset classification routes PDF correctly. asset_id passed. Video references the document content. Studio avatar + asset combo works.

### S9 — Studio avatar + Quick Shot mode
- Prompt: "Quick 30-second video: three reasons AI video will replace stock footage in 2026. Use a professional male presenter."
- Avatar: Discover a male studio_avatar, pass avatar_id.
- Target: 30s landscape
- **What to verify:** Quick Shot mode activates (no interview). Studio avatar discovered and avatar_id passed despite Quick Shot. Prompt says "The selected presenter" not appearance description.

### S10 — Studio avatar + portrait + explicit background + energetic tone
- Prompt: "Make a 40-second portrait Instagram Reel about the top 3 AI tools for content creators. Background should be a colorful creative studio with neon lights. Energetic, fun tone."
- Avatar: Pick a studio_avatar (any, transparent bg preferred to test full correction stack).
- Target: 40s portrait
- **What to verify:** Portrait orientation. Background request honored. Tone reflected in delivery style. If transparent bg, correction C fires with user's background description. If landscape avatar, correction B also fires.

## Discovery Instructions (CRITICAL)

Before starting scenarios, run these discovery calls:

```bash
# 1. List stock avatar groups
curl -s "https://api.heygen.com/v3/avatars/groups?type=stock&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# 2. For each interesting group, list looks
curl -s "https://api.heygen.com/v3/avatars/looks?group_id=<group_id>&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Pick groups strategically:
- At least one avatar with a REAL background (for S1, S2, S6, S7)
- At least one avatar with TRANSPARENT/empty background (for S3, S4, S5, S10)
- At least one group with MULTIPLE looks (for S6)
- Mix of male and female presenters

Log all discovered avatars (group name, look name, look_id, has_background, orientation) at the top of the transcript.

## Scoring

For each scenario:
1. **Avatar rendered correctly?** (Yes/No)
2. **Correct look appeared?** (Yes/No — verify against preview image)
3. **Phase 3.5 fired correctly?** (Expected corrections vs actual)
4. **Background quality** (natural/terrible/N/A)
5. **Duration accuracy** (actual/target %)
6. **Prompt followed avatar_id rule?** (No appearance description when avatar_id set)
7. **Session URL captured?** (Yes/No)
8. **Overall score** (1-10)

## Database Output
Write results to the Eval Tracker database (data_source_id: 17f54098-a085-4234-83ce-55c280266d73). Use text values for all number-like fields. Set Ken Verdict to "—". Prefix scenario names with "R8-".
