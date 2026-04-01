# Known Issues & Troubleshooting

## Known Bug: Video Agent "Talking Photo Not Found"

**Discovered:** March 30, 2026 (Round 3 autoresearch testing)

**Error message:** "The Talking Photo for the current narrator could not be found."

**Root Cause:** Confirmed as a Video Agent backend bug by HeyGen engineering (Jerry Yan). Affects `video_avatar` type narrators and stock avatar auto-selection.

**Workaround:**
- Prefer explicit `avatar_id` over auto-selection
- If `video_avatar` fails, retry with a `studio_avatar` or `photo_avatar`

**Status:** Fix in progress at HeyGen.

---

## Duration Variance (Expected Behavior)

Video Agent controls final video timing internally. Duration accuracy ranges from 79-174% of target across testing. This is NOT a bug.

**Mitigation:** Variable padding multipliers (Phase 2):
- ≤30s target: 1.6x padding
- 31-119s target: 1.4x padding
- ≥120s target: 1.3x padding

With explicit `avatar_id`: ~97% duration accuracy average.
Without `avatar_id`: ~80% accuracy average.

---

## Phase 3.5 Correction Prompts Not Executing

If aspect ratio corrections (generative fill, reframing) aren't applied, check that the correction prompt includes the exact phrase: **"Use AI Image tool to generative fill"**

Without this trigger phrase, Video Agent acknowledges the directive but doesn't execute it.

---

## Generative Fill Visual Quality

Phase 3.5 correction prompts can produce unnatural-looking environments when Video Agent's AI Image tool generates backgrounds. This is a known quality limitation.

**Mitigation:**
- Prescriptive correction prompts (added Round 5) improve results
- Explicit environment description ("modern studio with monitors and soft lighting") beats vague ("professional background")
- Short videos (≤30s) with corrections tend to overshoot duration (~163%)

---

## Stock Avatar Auto-Selection Unreliable

When no `avatar_id` is provided, Video Agent uses narrator tags (`{{@narrator_l0ug91}}`) that sometimes fail to resolve during render.

**Fix:** Always use explicit `avatar_id` from discovery. The only exception is Quick Shot mode where the user explicitly wants speed over reliability.

---

## HTML URLs in files[] Rejected

Video Agent rejects `text/html` content type in the `files[]` array. Web pages (blogs, docs sites, articles) must be handled via Path A (contextualize) only.

**What works in files[]:** Direct file URLs (PDFs, images, videos) — but prefer download→upload→asset_id since CDN/WAF often blocks HeyGen's servers.

---

## Interactive Sessions Reliability

Interactive sessions (`POST /v3/video-agents/sessions`) have known issues:
- Sessions frequently stuck at `processing` status
- `reviewing` state may never be reached
- Follow-up messages fail with timing errors
- Stop command may not trigger video generation

**Recommendation:** Use one-shot mode for production. Interactive sessions documented for future use once HeyGen stabilizes the API.
