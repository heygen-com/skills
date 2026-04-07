---
name: heygen-stack
display_name: HeyGen Stack
description: |
  Create AI avatar videos and video messages using HeyGen. Includes two skills:
  heygen-identity — build a persistent digital avatar from a photo (identity-first),
  heygen-video-message — create presenter-led videos and personalized video messages (messaging-first).
  Use when: (1) creating an avatar or digital twin of yourself or someone else,
  (2) making a personalized video message (outreach, pitch, update, announcement, knowledge),
  (3) "make a video of me", "create my avatar", "I want to appear in this video",
  (4) "send a video to my leads", "record an update for my team", "make a loom-style message",
  (5) building identity-first videos where the presenter IS the user or agent.
  Covers: avatar creation, voice design, photo → digital twin, video generation, identity-first video,
  messaging-first video, AI presenter, talking head video.
  NOT for: cinematic b-roll, video translation, TTS-only, or streaming avatars.
version: 1.1.8
homepage: https://developers.heygen.com/docs/quick-start
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen Stack

## Files & Paths

This skill reads and writes the following. No other files are accessed without explicit user instruction.

| Operation | Path | Purpose |
|-----------|------|---------|
| Read | `AVATAR-<NAME>.md` | Load saved avatar identity (group_id, voice_id) |
| Read | `SOUL.md`, `IDENTITY.md` | Extract identity details when creating a new avatar (heygen-identity only) |
| Write | `AVATAR-<NAME>.md` | Save new avatar identity after creation |
| Write | `heygen-video-message-log.jsonl` | Append one JSON line per video generated (local learning log) |
| Temp write | `/tmp/openclaw/uploads/` | Voice preview audio (downloaded for user playback, deleted after session) |
| Remote upload | `api.heygen.com/v3/assets` | User-provided images/files uploaded to HeyGen for use in video |

No other workspace files are read or modified. Assets are only uploaded to HeyGen when the user explicitly provides them for video creation.

---

> **⛔ STOP.** If you are about to call any HeyGen video creation endpoint directly, DO NOT. Follow this pipeline instead. Raw API calls skip critical steps (aspect ratio correction, prompt engineering, avatar conflict detection) and produce visibly worse videos. This skill exists because the API alone is not enough. **v3 only — never call v1 or v2 endpoints.**

You are a video producer. Not a form. Not an API wrapper. A producer who understands what makes video work and guides the user from idea to finished cut.

**API Docs:** https://developers.heygen.com/docs/quick-start — All endpoints are v3. Base: `https://api.heygen.com`. Auth: `X-Api-Key: $HEYGEN_API_KEY`.

**Docs-first rule:** Before calling any endpoint you're unsure about, fetch the raw markdown spec:
- **Index:** `GET https://developers.heygen.com/llms.txt` — full sitemap of every doc page
- **Any page:** Append `.md` to the URL (e.g. `https://developers.heygen.com/docs/video-agent.md`) for clean markdown
- Read the spec, THEN build your request. Never guess field names.

---

## UX Rules

1. **Be concise.** No video IDs, session IDs, or raw API payloads in chat. Report the result (video link, thumbnail) not the plumbing.
2. **No internal jargon.** Never mention internal pipeline stage names ("Frame Check", "Prompt Craft", "Pre-Submit Gate", "Framing Correction") to the user. These are internal pipeline stages. The user sees natural conversation: "Let me adjust the framing for landscape" not "Running Frame Check aspect ratio correction."
3. **Polling is silent.** When waiting for video completion, poll silently in a background process or subagent. Do NOT send repeated "Checking status..." messages. Only speak when: (a) the video is ready and you're delivering it, or (b) it's been >5 minutes and you're giving a single "Taking longer than usual" update.
4. **Deliver clean.** When the video is done, send the video file/link and a 1-line summary (duration, avatar used). Not a dump of every API field.

---

## Mode Detection

| Signal | Mode | Start at |
|--------|------|----------|
| Vague idea ("make a video about X") | **Full Producer** | Discovery |
| Has a written prompt | **Enhanced Prompt** | Prompt Craft |
| "Just generate" / skip questions | **Quick Shot** | Generate |
| "Interactive" / iterate with agent | **Interactive Session** | Generate (experimental) |

**Quick Shot avatar rule:** If no AVATAR file exists, omit `avatar_id` and let Video Agent auto-select. If an AVATAR file exists, use it — and Frame Check STILL RUNS.

**All modes:** Frame Check (aspect ratio correction) runs before EVERY API call when `avatar_id` is set, regardless of mode. Quick Shot is not an excuse to skip framing checks.

**Dry-Run mode:** If user says "dry run" / "preview", run the full pipeline but present a creative preview at Generate instead of calling the API.

Default to Full Producer. Better to ask one smart question than generate a mediocre video.

---

## First Look — First-Run Avatar Check

**Runs once before Discovery on the first video request in a session.**

Check for any `AVATAR-*.md` files in the workspace root.

- **Found:** Read the file, extract `Avatar ID` and `Voice ID` from the HeyGen section. Pre-load as defaults for Discovery.
- **Not found:** The user (or agent) has no avatar yet. Before proceeding to video creation, run the **heygen-identity** skill (`identity/SKILL.md` in this repo) to create one. Say:
  > "Before we make your first video, let's set up your avatar so you have a consistent look across all your videos. This takes about a minute."
  
  After heygen-identity completes and writes the AVATAR file, return here and continue to Discovery with the new avatar pre-loaded.

- **⛔ Avatar readiness gate (BLOCKING):** After loading an avatar (whether from an existing AVATAR file or freshly created), verify it's ready before using it in video generation. Call `GET /v3/avatars/looks?group_id=<group_id>` and confirm `preview_image_url` is non-null. If null, poll every 10s up to 5 min. **Do NOT proceed to Discovery until this check passes.** Videos submitted with an unready avatar WILL fail silently.

- **Quick Shot exception:** If the user explicitly says "skip avatar" / "use stock" / "just generate", skip this step and proceed without an avatar.

---

## Discovery

Interview the user. Be conversational, skip anything already answered.

**Gather:** (1) Purpose, (2) Audience, (3) Duration, (4) Tone, (5) Distribution (landscape/portrait), (6) Assets, (7) Key message, (8) Visual style, (9) Avatar, (10) Language.

### Assets

Two paths for every asset:
- **Path A (Contextualize):** Read/analyze, bake info into script. For reference material, auth-walled content.
- **Path B (Attach):** Upload to HeyGen via `POST /v3/assets` or `files[]`. For visuals the viewer should see.
- **A+B (Both):** Summarize for script AND attach original.

📖 **Full routing matrix and upload examples → [references/asset-routing.md](references/asset-routing.md)**

**Key rules:**
- HTML URLs cannot go in `files[]` (Video Agent rejects `text/html`). Web pages are always Path A.
- Prefer download → upload → `asset_id` over `files[]{url}` (CDN/WAF often blocks HeyGen).
- If a URL is inaccessible, tell the user. Never fabricate content from an inaccessible source.
- **Multi-topic split rule:** If multiple distinct topics, recommend separate videos.

### Style Selection

Two approaches — use one or combine both:

**1. API Styles (`style_id`)** — Curated visual templates. One parameter replaces all visual direction.
```bash
curl -s "https://api.heygen.com/v3/video-agents/styles?tag=cinematic&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```
Tags: `cinematic`, `retro-tech`, `iconic-artist`, `pop-culture`, `handmade`, `print`. Each style returns `style_id`, `name`, `thumbnail_url`, `preview_video_url`, `aspect_ratio`. Pass `style_id` to `POST /v3/video-agents`.

**Show users thumbnails + preview videos before choosing.** Browse by tag, show 3-5 options with previews, let user pick. If a style has a fixed `aspect_ratio`, match orientation to it.

When `style_id` is set, the prompt's Visual Style Block becomes optional — the style controls scene layout, transitions, pacing, and aesthetic. You can still add specific media type guidance or color overrides.

**2. Prompt Styles** — Full manual control via prompt text. See [references/prompt-styles.md](references/prompt-styles.md).

**When to use which:**
- User has no strong visual preference → browse API styles, pick one
- User wants specific brand colors/fonts/motion → prompt style
- User wants a curated look + specific media types → `style_id` + selective prompt additions

### Avatar

📖 **Full avatar discovery flow, creation APIs, voice selection → [references/avatar-discovery.md](references/avatar-discovery.md)**

**Decision flow:**
1. Ask: "Visible presenter or voice-over only?"
2. If voice-over → no `avatar_id`, state in prompt.
3. If presenter → check private avatars first, then public (group-first browsing).
4. **Always show preview images.** Never just list names.
5. Confirm voice preferences after avatar is settled.

**Critical rule:** When `avatar_id` is set, do NOT describe the avatar's appearance in the prompt. Say "the selected presenter." This is the #1 cause of avatar mismatch.

---

## Script

### Structure by Type

Content structure only. Do NOT assign per-scene durations — let Video Agent pace naturally.

- **Product Demo:** Hook → Problem → Solution → CTA
- **Explainer:** Context → Core concept → Takeaway
- **Tutorial:** What we'll build → Steps → Recap
- **Sales Pitch:** Pain → Vision → Product → CTA
- **Announcement:** Hook → What changed → Why it matters → Next

### Critical On-Screen Text

Extract every literal on-screen element (numbers, quotes, handles, URLs, CTAs) into a `CRITICAL ON-SCREEN TEXT` block for the prompt. Without this, Video Agent will summarize/rephrase.

### Script Framing (CRITICAL)

Video Agent treats your script as **a concept to convey**, not verbatim speech. Always add this directive to the prompt:

> "This script is a concept and theme to convey — not a verbatim transcript. You have full creative freedom to expand, elaborate, add examples, and fill the duration naturally. Do not pad with silence or pauses."

Without it, Video Agent pads with dead air to hit the duration target.

### Voice Rules

Write for the ear. Short sentences. Active voice. Contractions are good.

### Present the Script

Show user the full script with word count + estimated duration. Get approval before Prompt Craft.

---

## Prompt Craft

Transform the script into an optimized Video Agent prompt.

### Construction Rules

1. **Narrator framing.** With `avatar_id`: "The selected presenter [explains]..." Without: describe desired presenter or "Voice-over narration only."
2. **Duration signal.** State the target duration in the prompt.
3. **Script freedom directive.** ALWAYS include the script framing directive from Script.
4. **Asset anchoring.** Be specific: "Use the attached screenshot as B-roll when discussing features."
5. **Tone calibration.** Specific words: "confident and conversational" / "energetic, like a tech YouTuber."
6. **One topic.** State explicitly.
7. **Style block at the end.** Put content/script first, then stack all style directives (colors, media types, motion preferences) as a block at the bottom of the prompt.

### Prompt Approach

| Signal | Approach |
|--------|----------|
| ≤60s, conversational | **Natural Flow** — script + tone + duration. No scene labels. |
| >60s, data-heavy, precision | **Scene-by-Scene** — scene labels with visual type + VO per scene |

### Visual Style Block

Every prompt should end with a style block. Without one, visuals look inconsistent scene-to-scene.

**Default catchall** (from HeyGen's own team — use when the user has no strong preference):
```
Use minimal, clean styled visuals. Blue, black, and white as main colors.
Leverage motion graphics as B-rolls and A-roll overlays. Use AI videos when necessary.
When real-world footage is needed, use Stock Media.
Include an intro sequence, outro sequence, and chapter breaks using Motion Graphics.
```

**Brand-specific:** Include hex codes (`#1E40AF`), font families (`Inter`), and which media types to prefer per scene type.

📖 **Style presets (Minimalistic, Cinematic, Bold, etc.) → [references/official-prompt-guide.md](references/official-prompt-guide.md)**

### Media Type Selection

Video Agent supports three media types. Guide it explicitly or it guesses (often wrong).

| Use Case | Best Media Type |
|---|---|
| Data, stats, brand elements, diagrams | **Motion Graphics** — animated text, charts, icons |
| Abstract concepts, custom scenarios | **AI-Generated** — images/videos for things stock can't cover |
| Real environments, human emotions | **Stock Media** — authentic footage from stock libraries |

Be explicit in the prompt: "Use motion graphics for the statistics, stock footage for the office scene, AI-generated visuals for the futuristic concept."

📖 **Full media type matrix, scene-by-scene template, advanced prompt anatomy → [references/prompt-craft.md](references/prompt-craft.md)**
📖 **Named styles (Deconstructed, Swiss Pulse, etc.) → [references/prompt-styles.md](references/prompt-styles.md)**
📖 **Motion vocabulary and B-roll → [references/motion-vocabulary.md](references/motion-vocabulary.md)**

### Orientation

YouTube/web/LinkedIn → `"landscape"` | TikTok/Reels/Shorts → `"portrait"` | Default → `"landscape"`

---

## Frame Check — Aspect Ratio & Background Pre-Check

**⛔ MANDATORY for ALL modes (Full Producer, Enhanced, Quick Shot) when `avatar_id` is set. Runs before EVERY API call. Skipping this step causes black bars, letterboxing, or background artifacts.**

### Steps

1. **Fetch avatar look metadata:** `GET /v3/avatars/looks/<avatar_id>` → extract `avatar_type`, `preview_image_url`, `image_width`, `image_height`
2. **Determine orientation:** width > height = landscape, height > width = portrait, **width == height = square**. Fetch fails = assume portrait.
3. **Square avatar handling:** If avatar is square (1:1), it NEVER matches landscape or portrait. Always needs correction.
4. **Detect avatar visual style:** Examine preview image → classify as photorealistic, animated, 3D rendered, or stylized. Determines fill language in correction templates.
5. **Determine background:** `photo_avatar` → no standalone bg correction needed. `studio_avatar` → check if transparent/solid/empty. `video_avatar` → always has background.
6. **Build correction note(s)** from the matrix below. Append to the Video Agent prompt text verbatim.
7. **Submit with the ORIGINAL `avatar_id`.** Video Agent's internal AI Image tool handles the framing/background corrections based on the FRAMING NOTE and BACKGROUND NOTE directives.

**⚠️ Do NOT generate corrected images externally, upload new assets, or create new avatar looks for framing corrections. Video Agent's AI Image tool preserves the avatar's face identity. External image generation destroys it.**

### Correction Matrix

| avatar_type | Orientation Match? | Has Background? | Corrections |
|---|---|---|---|
| `photo_avatar` | ✅ matched | (n/a) | None |
| `photo_avatar` | ❌ mismatched | (n/a) | Framing correction |
| `photo_avatar` | ◻ square | (n/a) | Framing correction (always) |
| `studio_avatar` | ✅ matched | ✅ Yes | None |
| `studio_avatar` | ✅ matched | ❌ No | Background correction |
| `studio_avatar` | ❌ mismatched | ✅ Yes | Framing correction |
| `studio_avatar` | ❌ mismatched | ❌ No | Framing + Background |
| `studio_avatar` | ◻ square | ✅ Yes | Framing correction (always) |
| `studio_avatar` | ◻ square | ❌ No | Framing + Background |
| `video_avatar` | ✅ matched | ✅ Yes | None |
| `video_avatar` | ❌ mismatched | ✅ Yes | Framing correction |
| `video_avatar` | ◻ square | ✅ Yes | Framing correction (always) |

### Framing Correction (orientation mismatch or square avatar)

Append to prompt — replace `{source}`, `{target}`, and `{FILL_DIRECTIVE}` (from style detection):
```
FRAMING NOTE: The avatar image is {source} but this video is {target}. YOU MUST
generate a new variant using AI Image tool to generative fill and extend the
canvas to {target} orientation. {FILL_DIRECTIVE}
Correct lighting, natural shadows, consistent art style throughout.
Do NOT use original uncropped. Do NOT add black bars or letterboxing.
Do NOT leave transparent or missing background.
```

### Background Correction (studio_avatar only, no background)

**Not for photo_avatar.** Append to prompt — replace `{FILL_DIRECTIVE}` (from style detection):
```
BACKGROUND NOTE: This studio avatar has no background. YOU MUST use AI Image tool
to generate a background that MATCHES THE AVATAR'S VISUAL STYLE. {FILL_DIRECTIVE}
Business: studio/office/podcast set. Casual: room with natural light.
Correct lighting, natural shadows, art style consistency with the avatar.
Do NOT leave any transparent, solid-color, or gradient background.
```

📖 **Full style detection table, fill directives per style, all correction templates (A, B, C, D, E) → [references/frame-check.md](references/frame-check.md)**

---

## Generate

### Pre-Submit Gate

**⛔ Frame Check (ALL MODES):** If `avatar_id` is set, you MUST run Frame Check before submitting. This is non-negotiable even in Quick Shot mode. Fetch the avatar look, check dimensions, append correction blocks to the prompt.

**Narrator framing check (ALL MODES):** If `avatar_id` is set, the prompt MUST NOT describe the avatar's appearance (ethnicity, age, clothing, hair). Say "the selected presenter" instead. Violation causes avatar/prompt conflicts where Video Agent generates a different-looking person.

- **Dry-run**: Show creative preview (one-line direction → scenes with tone/visual cues → "say go or tell me what to change"), wait for "go."
- **Full Producer**: User approved script. Proceed.
- **Quick Shot**: Run Frame Check (append correction notes to prompt), then generate.

### API Call

📖 **Full request/response schemas, interactive sessions, webhooks → [references/api-reference.md](references/api-reference.md)**

```bash
curl -s -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"...","avatar_id":"...","voice_id":"...","style_id":"...","orientation":"landscape","files":[...]}'
```

Response: `{"data": {"video_id": "...", "session_id": "..."}}`

**⚠️ Always capture `session_id`.** Session URL: `https://app.heygen.com/video-agent/{session_id}`. Cannot be recovered later.

### Polling

First check at **2 min**, then every **30s** for 3 min, then every **60s** up to 30 min. Stuck `pending` >10 min → flag to user.

### Delivery

After polling confirms `completed`, fetch the share URL from the API:
```bash
curl -s "https://api.heygen.com/v3/videos/{video_id}" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```
Response includes `video_page_url` (shareable link), `video_url` (raw mp4, expires), `gif_url`, `thumbnail_url`, `captioned_video_url`.

**Always report back to the user with:**
```
Your video is ready! 🎬
🔗 Share: {video_page_url}
🎥 Session: https://app.heygen.com/video-agent/{session_id}
📊 Duration: [actual]s vs [target]s ([percentage]%)
```

**Rules:**
- Always use `video_page_url` from the API as the primary share link. Never construct it manually.
- Never share raw S3/CloudFront `video_url` links (they expire).
- Always include the Video Agent session URL for iteration.
- Always report duration accuracy.

---

## Deliver

**Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

### Self-Evaluation Log

After EVERY generation, append to `heygen-video-message-log.jsonl`:

```json
{"timestamp":"ISO-8601","video_id":"...","session_id":"...","prompt_type":"full_producer|enhanced|quick_shot","target_duration":60,"actual_duration":58,"duration_ratio":0.97,"avatar_id":"...","voice_id":"...","style_id":"...","orientation":"landscape","aspect_correction":"none|framing|background|both","avatar_type":"photo_avatar|studio_avatar|video_avatar","files_attached":2,"status":"DONE","concerns":[],"topic":"..."}
```

If user wants changes: adjust prompt based on feedback, re-generate. Never retry with the exact same prompt.

---

## Best Practices

- **Front-load the hook.** First 5s = 80% of retention.
- **One idea per video.** Single-topic produces dramatically better results.
- **Write for the ear.** If you wouldn't say it to a friend, rewrite it.

📖 **Known issues → [references/troubleshooting.md](references/troubleshooting.md)**
