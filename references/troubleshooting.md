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

## Weird Pauses / Unnatural Silence in Videos

**Discovered:** March 31, 2026 (R11 testing, confirmed by Jerry Yan, HeyGen engineer)

**Symptom:** Video has awkward pauses or breaks between sentences. Narrator stops speaking but video continues with dead air before next line.

**Root Cause:** When Video Agent receives a script shorter than the target duration, it treats the script as verbatim speech and inserts silence/breaks to stretch it to the exact requested duration. It won't ad-lib or expand — it just pads with dead air.

**Fix:** Add this directive to EVERY prompt:
> "This script is a concept and theme to convey — not a verbatim transcript. You have full creative freedom to expand, elaborate, add examples, and fill the duration naturally. Do not pad with silence or pauses."

This tells Video Agent it can expand the script naturally instead of treating it as a fixed speech transcript. Per Jerry Yan: "If you tell it it's not a script to be strictly followed but concept or theme or give it green light to expand the script it will do well."

**Status:** Skill-side fix (prompt directive). HeyGen is also tuning the default behavior but the explicit directive is the reliable workaround.

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

If aspect ratio corrections (generative fill, reframing) aren't applied, check:

1. **Correction templates must be in SKILL.md, not just referenced.** If the agent only sees a summary pointer ("read references/phase-3-5.md"), it may skip loading the reference and generate without corrections. The full correction text blocks (A, B, C) are inlined in SKILL.md to prevent this.
2. The correction prompt must include the exact phrase: **"Use AI Image tool to generative fill"** — without this trigger, Video Agent acknowledges the directive but doesn't execute it.
3. **photo_avatar does NOT need Correction C** (background fill). Video Agent generates avatar + environment together for photo_avatars. Only apply framing corrections (A/B) for orientation mismatches. Correction C is for studio_avatars with transparent/empty backgrounds only.

---

## Generative Fill Visual Quality

Phase 3.5 correction prompts can produce synthetic-looking backgrounds. The bar is **hyper photo-realistic** — backgrounds should be indistinguishable from real photography.

**Mitigation:**
- All correction prompts (A, B, C) now include explicit "HYPER PHOTO-REALISTIC" + anti-CGI directives
- Specific real-world details beat generic descriptions: "visible mic stands, actual monitors with content" >> "professional studio"
- Request depth-of-field blur, natural lighting direction, and realistic imperfections
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

## Avatar Not Ready for Video Generation

**Discovered:** April 5, 2026 (Adrian onboarding test)

**Symptom:** Video generation fails or produces errors immediately after creating a new avatar. The avatar exists in the HeyGen dashboard but videos referencing it fail.

**Root Cause:** Avatar creation is asynchronous. `POST /v3/avatars` returns success immediately, but the avatar image is still being processed. If you submit a video request before processing completes, it fails.

**Detection:** Poll `GET /v3/avatars/looks?group_id=<group_id>`. The avatar is NOT ready until:
- `preview_image_url` is non-null
- `image_width` and `image_height` are non-zero

At the group level (`GET /v3/avatars`), an unready avatar will have no `preview_image_url` on the group object.

**Fix:** Poll every 10 seconds after creation, wait for preview URL to appear. Typical: 30-90s for photo avatars, 1-3 min for prompt avatars. Timeout at 5 min.

**The avatar-designer skill handles this automatically.** If you bypass the skill and call the API directly, you must implement this polling yourself.

---

## Interactive Sessions Reliability

Interactive sessions (`POST /v3/video-agents/sessions`) have known issues:
- Sessions frequently stuck at `processing` status
- `reviewing` state may never be reached
- Follow-up messages fail with timing errors
- Stop command may not trigger video generation

**Recommendation:** Use one-shot mode for production. Interactive sessions documented for future use once HeyGen stabilizes the API.
