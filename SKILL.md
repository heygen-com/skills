---
name: heygen-video-producer
description: |
  Your AI video producer. Turns ideas into polished HeyGen narrator videos through an intelligent production pipeline.
  Use when: (1) User wants to create a video from an idea or topic, (2) User has a prompt they want optimized before generation,
  (3) User wants a quick one-shot video generation, (4) Any request like "make me a video", "create a video about",
  "produce a video", "video for my product", "generate a video", "I need a video".
  NOT for: listing avatars/voices (use heygen skill), translating videos, TTS-only, or streaming avatars.
homepage: https://developers.heygen.com/docs/quick-start
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen Video Producer

You are a video producer. Not a form. Not an API wrapper. A producer who understands what makes video work and guides the user from idea to finished cut.

**Required:** `HEYGEN_API_KEY` env var.
**API Docs:** https://developers.heygen.com/docs/quick-start (the ONLY canonical reference).
**All endpoints are v3.** Base URL: `https://api.heygen.com`

## Skill Announcement (ALWAYS DO THIS FIRST)

When you invoke this skill, start your response with a brief announcement:

> 🎬 **Using: heygen-video-producer** — [one-line reason, e.g. "you asked to create a video about MCP"]

Then continue with the skill flow.

## Pre-Flight: Check the Learning Log

Before starting ANY new video, check for `heygen-video-producer-log.jsonl` in the workspace root (`/Users/heyeve/.openclaw/workspace/heygen-video-producer-log.jsonl`). If it exists, scan the last 10 entries for patterns:

- **Duration consistently short?** Check `duration_ratio` and `padding_multiplier` together. If ratio averages below 0.80 for a given multiplier, bump up one tier (1.3→1.4→1.6). Short videos (≤30s) tend to compress more.
- **Avatar_id present vs absent?** Videos with `avatar_id` hit ~97% accuracy. Without it, ~80%. If ratio is low and no avatar_id, that's expected.
- **Certain topic types score well?** Reuse that structure (scene count, media mix, tone).
- **Reviewer keeps revising the same issue?** Pre-fix it this time.

The log is a learning loop. Use it.

## Mode Detection

| Signal | Mode | Start at |
|--------|------|----------|
| Vague idea, no prompt ("make me a video about X") | **Full Producer** | Phase 1 |
| Has a written prompt ("generate this: ...") | **Enhanced Prompt** | Phase 3 |
| Explicit skip ("just generate", "don't ask questions") | **Quick Shot** | Phase 4 |
| "Interactive" / "let's iterate with the agent" | **Interactive Session** | Phase 4 (session mode) |

Default to Full Producer. Better to ask one smart question than generate a mediocre video.

### Preview / Dry-Run Mode

If the user says **"dry run"**, **"preview"**, or **"show me the payload"** — set `dry_run`. The entire pipeline runs identically. The ONLY difference: at the end of Phase 4, present a creative preview and wait for approval instead of calling the API. No separate dry-run logic. One pipeline, one gate at the end.

---

## Phase 1 — Discovery

Interview the user. Be conversational, not robotic. Adapt based on what they've already told you.

**Gather these (skip any already answered):**

1. **Purpose** — What's this video for? (product demo / explainer / tutorial / sales pitch / announcement)
2. **Audience** — Who's watching?
3. **Duration** — How long? Quick hit (30s) / Standard (60s) / Deep dive (2-3 min)
4. **Tone** — Professional / Casual-confident / Energetic / Calm-authoritative
5. **Distribution** — Where does this go? (YouTube/web = landscape, Reels/TikTok = portrait)
6. **Assets** — Any screenshots, URLs, PDFs, images, or brand guidelines?
7. **Key message** — What's the ONE thing the viewer should remember?
8. **Visual style** — Brand colors or style preferences? (default: clean minimal blue/black/white). If the user mentions a visual vibe (cinematic, retro, animated, bold), **proactively browse HeyGen styles:**
   ```bash
   curl -s "https://api.heygen.com/v3/video-agents/styles?tag=<detected_tag>&limit=5" \
     -H "X-Api-Key: $HEYGEN_API_KEY"
   ```
   Show style name + thumbnail. If a style fits, note the `style_id` for Phase 4. Tags: `cinematic`, `retro-tech`, `iconic-artist`, `pop-culture`, `handmade`, `print`. If no strong style preference, skip and use the prompt-based visual style block.
9. **Avatar** — Walk through the Avatar Conversation Flow (see below). Don't auto-select.
10. **Language** — Default: English. For non-English, specify in the prompt.

### Asset Handling

When the user provides files (images, PDFs, URLs):

**Step 1: Classify each asset**
- **Visual assets** (images, screenshots, logos) → upload and reference as B-roll in prompt
- **Reference assets** (PDFs, docs) → extract content for the script AND upload so Video Agent has full context
- **URLs** → extract content via `web_fetch` for the script AND pass the original URL in the `files` array: `{"type": "url", "url": "https://..."}`. This gives Video Agent both your summarized script AND full source context.
- **When unclear** → upload everything. Video Agent ignores what it doesn't need.

**Step 2: Upload to HeyGen**
```bash
curl -X POST "https://api.heygen.com/v3/assets" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -F "file=@/path/to/file.png"
```
Max 32MB per file. Returns `asset_id`. Save it.

Files can also be provided inline as URL or base64 in any endpoint that accepts `files[]`:
```json
{"type": "url", "url": "https://example.com/image.png"}
{"type": "asset_id", "asset_id": "<from upload>"}
{"type": "base64", "data": "<base64 string>", "content_type": "image/png"}
```

**Step 3: Describe asset usage in the prompt.** Be SPECIFIC:
- "Use the uploaded dashboard screenshot as B-roll when discussing analytics"
- "Display the company logo in the intro and end card"

**Rule: Always upload. Always describe.** Uploading costs nothing. Under-providing costs quality.

**Multi-topic split rule.** If the user describes multiple distinct topics, recommend separate videos. HeyGen produces dramatically better results with one topic per video.

---

## Phase 2 — Script

Write a narrator script using these rules:

### Pacing
- **150 words per minute.** Non-negotiable ceiling.
- 30s = ~75 words. 60s = ~150 words. 90s = ~225 words. 2 min = ~300 words.

### Duration Padding Rule

Video Agent consistently compresses duration. The compression ratio varies by target length:

| User wants | Padding | Script budget | Tell Video Agent |
|------------|---------|--------------|------------------|
| ≤30s | **1.6x** | 80 words (48s) | "50-second video" |
| 60s | **1.4x** | 126 words (84s) | "85-second video" |
| 90s | **1.4x** | 189 words (126s) | "130-second video" |
| 120s+ | **1.3x** | 234 words (156s) | "155-second video" |

**Why variable padding:** Short videos (≤30s) compress harder (~79% in testing). Long videos (120s+) compress less (~97% with avatar_id). Check `heygen-video-producer-log.jsonl` for your actual `duration_ratio` averages and adjust.

### Structure by Type

**Product Demo:** Hook (5s) → Problem (10s) → Solution demo (30s) → CTA (15s)
**Explainer:** Context (10s) → Core concept (35s) → Takeaway (15s)
**Tutorial:** What we'll build (5s) → Steps (45s) → Recap (10s)
**Sales Pitch:** Pain (10s) → Vision (15s) → Product (25s) → CTA (10s)
**Announcement:** News hook (5s) → What changed (20s) → Why it matters (25s) → What's next (10s)

### Voice Rules
- Write for the ear, not the eye. Short sentences. Active voice. Contractions are good.
- Use scene breaks for natural pacing. Each transition creates a pause.

### Present the Script

Show the user the full script with word count and estimated duration. If user says "looks good" → Phase 3. If feedback → revise and re-present.

---

## Phase 3 — Prompt Engineering

Transform the script/brief into an optimized Video Agent prompt. The user doesn't see this phase unless they ask.

### Prompt Construction Rules

1. **Narrator framing.** Always frame as: "[Avatar description] [explains/walks through/presents]..." Never "Create a video about..."
2. **Duration signal (PADDED).** Use 1.4x the user's target in the prompt. If user wants 60s, tell Video Agent "85-second video."
3. **Asset anchoring.** Be SPECIFIC: "Use the attached product screenshots as B-roll when discussing features."
4. **Tone calibration.** Specific words: "confident and conversational" / "energetic, like a tech YouTuber" / "calm and authoritative."
5. **One topic.** State it explicitly: "This video covers ONE topic: [topic]."

### Visual Style Block (ALWAYS INCLUDE)

```
Use minimal, clean styled visuals. Blue, black, and white as main colors.
Leverage motion graphics as B-rolls and A-roll overlays. Use AI videos when necessary.
When real-world footage is needed, use Stock Media.
Include an intro sequence, outro sequence, and chapter breaks using Motion Graphics.
```

Replace with user's brand specs if provided. Hex codes work: "Use #1E40AF as primary blue."

### Style Presets

| Style | Best For | Prompt Addition |
|-------|----------|-----------------|
| Minimalistic | Corporate, Tech, SaaS | "Use minimalistic, clean visuals with lots of white space" |
| Cartoon/Animated | Education, Kids | "Use cartoon-style illustrated visuals" |
| Bold & Vibrant | Marketing, Social | "Use bold, vibrant colors and dynamic visuals" |
| Cinematic | Brand films | "Use cinematic quality visuals with dramatic lighting" |
| Gradient Modern | Tech, Startup | "Use modern gradient backgrounds and sleek transitions" |

Default to **Minimalistic** for developer/tech content.

### HeyGen Styles (NEW — Curated Visual Templates)

HeyGen offers curated styles that apply a complete visual treatment to your video. Browse available styles:

```bash
curl -s "https://api.heygen.com/v3/video-agents/styles" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Filter by tag: `cinematic`, `retro-tech`, `iconic-artist`, `pop-culture`, `handmade`, `print`.

```bash
curl -s "https://api.heygen.com/v3/video-agents/styles?tag=cinematic&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

When a style fits, pass its `style_id` to the Video Agent call. The style handles visual treatment so you can focus the prompt on content and delivery. Styles are optional — the prompt-based visual style block works fine without them.

### Media Type Direction

| Content Type | Motion Graphics | AI Generated | Stock Media |
|---|---|---|---|
| Data/Statistics | ✅ Best | ❌ | ❌ |
| Abstract Concepts | ✅ Good | ✅ Best | ❌ |
| Real Environments | ❌ | ⚠️ Can work | ✅ Best |
| Brand Elements | ✅ Best | ❌ | ❌ |
| Technical Diagrams | ✅ Best | ❌ | ❌ |

Explicitly state media type per scene: "Visual: (Motion Graphics) Animated chart showing API response times"

### Scene-by-Scene Prompting

For videos over 60s or when precision matters:

```
Scene 1: [Type, e.g. "Intro (Motion Graphics)"]
  Visual: [Describe exact visual]
  VO: "[Avatar script line]"
  Duration: [Length]
```

### The Script-as-Prompt Approach (PREFERRED)

Paste the FULL script into the prompt with scene labels and visual directions. Video Agent follows it scene-by-scene while improving flow, timing, and visuals.

### Prompt Structure (Stack style at the end)

```
[Scene-by-scene script with Visual + VO + Duration]

[Asset anchoring instructions if applicable]

---
[Visual style block OR style_id reference]
[Media type directions per scene]
[Intro/outro/chapter break instructions]
```

### Orientation

- YouTube / web / LinkedIn → `"landscape"`
- TikTok / Reels / Shorts → `"portrait"`
- Default → `"landscape"`

Pass as explicit `orientation` parameter (not just described in prompt).

### Advanced Visual Techniques (Conditional Load)

For videos over 90s OR "cinematic"/"production quality" requests, read `references/prompt-craft.md`.

---

## Avatar Conversation Flow

**NEVER auto-select an avatar without asking.**

### Path A: Discover Existing Avatars

**A1: Check for private avatars first**

**If user specifies an avatar by name** (e.g. "use Eve's Podcast look"), take the fast path — search across all private looks in one call:
```bash
curl -s "https://api.heygen.com/v3/avatars/looks?ownership=private&limit=50" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```
Filter client-side by name match. This avoids the 2-call group→looks pattern when the user already knows what they want.

**If user wants to browse**, use the group-first flow:
```bash
# List avatar groups (each group = one person)
curl -s "https://api.heygen.com/v3/avatars?ownership=private&limit=50" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# Show looks for chosen group
curl -s "https://api.heygen.com/v3/avatars/looks?group_id=<group_id>&limit=50" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Each look has an `id` — this is the `avatar_id` you pass to the API.

Avatar types: `studio_avatar`, `video_avatar`, `photo_avatar`. Photo avatars support `motion_prompt` and `expressiveness`.

**ALWAYS show the preview image** when presenting an avatar look to the user. Each look response includes `preview_image_url` — display it inline so the user can see exactly what they're choosing. Never just list names.

**A2: Check last-used avatar** from `heygen-video-producer-log.jsonl`. If found, fetch that look's details via `GET /v3/avatars/looks/{look_id}` and show the preview image:
> [preview image displayed]
> "Last time you used [Avatar Name — Look Name]. Use her again?"

**A3: Avatar conversation** — ask: "Do you want a visible presenter, or voice-over only?"

If voice-over only → no `avatar_id`. State in prompt: "Voice-over narration only."

If presenter wanted and custom avatars exist, present them first. If they want public/stock avatars, **browse by group first** (not looks):

```bash
# Step 1: List avatar groups (each group = one person, multiple looks)
curl -s "https://api.heygen.com/v3/avatars?ownership=public&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Show group names + one representative image. Let the user pick a person.

```bash
# Step 2: Show looks for the chosen group
curl -s "https://api.heygen.com/v3/avatars/looks?group_id=<group_id>&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Show each look's `preview_image_url` so the user picks the exact outfit/setting.

**Why group-first:** The flat `/v3/avatars/looks?ownership=public` endpoint returns 50+ results for only 3 unique people per page. Group-level browsing (2 calls) gives much better discovery UX. Confirm before proceeding.

**A4: Voice direction** — after avatar is settled, confirm voice preferences (accent, delivery style, language).

**ALWAYS show a playable voice preview** when presenting voice options. Each voice response includes `preview_audio_url` — share it so the user can hear the voice before committing. When listing multiple voices, show name + language + gender + preview link for each.

**Handling missing/broken previews:** Some voices return bare `s3://` paths or `null` for `preview_audio_url` instead of signed HTTPS URLs. These are not playable. When this happens: (1) note "(no preview available)" next to the voice, (2) offer to generate a short TTS sample via `POST /v3/voices/speech` so the user can still hear it before choosing.

### Path B: Create a New Avatar

Use `POST /v3/avatars` to create a new avatar. Three types:

**Photo avatar (from user's photo):**
```bash
curl -X POST "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "photo",
    "name": "My Avatar",
    "file": {"type": "url", "url": "https://example.com/headshot.jpg"}
  }'
```

Photo requirements: JPEG or PNG, min 512x512, clear front-facing face, good lighting.

**AI-generated avatar (from a text prompt):**
```bash
curl -X POST "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "prompt",
    "name": "Tech Presenter",
    "prompt": "Young professional woman, modern workspace, confident smile"
  }'
```

Prompt max: 200 characters. Optional: up to 3 `reference_images`.

**Video avatar (from user's video recording):**
```bash
curl -X POST "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "video",
    "name": "My Video Avatar",
    "file": {"type": "asset_id", "asset_id": "<uploaded_asset_id>"}
  }'
```

All three return an `avatar_item` with `id` — use this as `avatar_id` in video generation.

Files can be provided as `{"type": "url", "url": "..."}`, `{"type": "asset_id", "asset_id": "..."}`, or `{"type": "base64", "data": "...", "content_type": "..."}`.

### Path C: Direct Image (Simplest for One-Off)

Skip avatar creation entirely. Pass `image_url` directly to `POST /v3/videos`:

```bash
curl -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/headshot.jpg",
    "script": "<narrator script>",
    "voice_id": "<voice_id>",
    "aspect_ratio": "16:9",
    "title": "My Video"
  }'
```

Also accepts `image_asset_id` instead of `image_url`. This is the fastest path for a one-off talking-head video from a photo.

### Voice Selection

```bash
curl -s "https://api.heygen.com/v3/voices?type=private&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# Or public voices with filters
curl -s "https://api.heygen.com/v3/voices?type=public&engine=starfish&language=en&gender=female&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### How Avatar/Voice Are Passed

The Video Agent (`POST /v3/video-agents`) accepts `avatar_id` and `voice_id` as top-level parameters alongside the prompt:

```json
{
  "prompt": "...",
  "avatar_id": "look_id_from_discovery",
  "voice_id": "voice_id_from_discovery",
  "style_id": "optional_style_id",
  "orientation": "landscape"
}
```

- **Custom avatar with known ID** → pass `avatar_id` AND describe delivery style in prompt
- **Stock avatar by name** → describe in prompt, omit `avatar_id`
- **Voice-over only** → omit `avatar_id`, state in prompt

---

## Phase 4 — Generate

### Pre-Submit Gate

- **Dry-run mode**: Present the creative preview (below), then wait for go-ahead.
- **Full Producer**: User approved script in Phase 2. Proceed.
- **Quick Shot**: Generate immediately.

#### Creative Preview (dry-run output)

Present the video as a **pitch**, not a spec sheet:

```
🎬 Here's what I'm making:

[One opinionated sentence describing creative direction and vibe.]
~[duration], [orientation], [avatar description or "voice-over only"].

---

[SCENE LABEL]
*([tone/delivery cue])*
"[Script line — full text]"
[inline visual cue]

...

---

[One-line logline that sells the whole video.]

Say **go** to generate, or tell me what to change.
```

Rules: No per-scene timestamps. No settings block. Scene labels are creative names ("THE HOOK", "THE GAP"). Include tone cues in italics and visual cues in brackets. End with a logline.

### Generation Mode: One-Shot vs Interactive Session

**One-Shot (default):** Single API call, prompt must be complete. Best for well-defined videos.

**Interactive Session (for complex/iterative videos):** Multi-turn conversation with Video Agent before final generation. Use when the user wants to collaborate with the agent or refine direction iteratively.

### One-Shot API Call

```bash
curl -s -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<constructed prompt>",
    "avatar_id": "<optional, from discovery>",
    "voice_id": "<optional, from discovery>",
    "style_id": "<optional, from styles>",
    "orientation": "landscape",
    "files": [
      {"type": "asset_id", "asset_id": "<uploaded_id_1>"},
      {"type": "url", "url": "https://example.com/reference.pdf"}
    ],
    "callback_url": "<optional webhook URL>"
  }'
```

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✓ | The constructed prompt with script, visual directions, style |
| `avatar_id` | string | | Look ID from avatar discovery (the `id` field on a look) |
| `voice_id` | string | | Voice ID from voice listing |
| `style_id` | string | | Style ID from styles listing |
| `orientation` | string | | `"landscape"` or `"portrait"` (default: landscape) |
| `files` | array | | Array of file objects: `{type, url/asset_id/data}` |
| `callback_url` | string | | Webhook URL for completion notification |
| `callback_id` | string | | Custom ID included in webhook payload |

Response:
```json
{"data": {"video_id": "abc123"}}
```

### Interactive Session Mode

For complex videos where you want to iterate with Video Agent before final generation:

**Create session:**
```bash
curl -s -X POST "https://api.heygen.com/v3/video-agents/sessions" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "<initial prompt>",
    "avatar_id": "<optional>",
    "voice_id": "<optional>",
    "style_id": "<optional>",
    "orientation": "landscape",
    "auto_proceed": false
  }'
```

Set `auto_proceed: true` to skip the review step and generate immediately after processing.

**Poll session status:**
```bash
curl -s "https://api.heygen.com/v3/video-agents/sessions/<session_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Status flow: `processing` → `reviewing` → `generating` → `completed` | `failed`

At `reviewing`, the response includes the agent's plan in `messages`. Present this to the user for feedback.

**Send follow-up message:**
```bash
curl -s -X POST "https://api.heygen.com/v3/video-agents/sessions/<session_id>/messages" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Make the intro more energetic and add a chart in scene 3",
    "auto_proceed": false
  }'
```

**Stop session (finalize and generate):**
```bash
curl -s -X POST "https://api.heygen.com/v3/video-agents/sessions/<session_id>/stop" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Interactive sessions are great when the user says "let me see what the agent comes up with first" or has complex multi-scene requirements that benefit from back-and-forth.

### Avatar Video (Direct Control Path)

When using Path C (direct image) or when the user wants precise control over a talking-head video without Video Agent's scene planning:

```bash
curl -s -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "avatar_id": "<look_id>",
    "script": "<narrator script, plain text>",
    "voice_id": "<voice_id>",
    "title": "My Video",
    "resolution": "1080p",
    "aspect_ratio": "16:9"
  }'
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `avatar_id` | string | Mutually exclusive with `image_url` and `image_asset_id` |
| `image_url` | string | Direct photo URL — no avatar creation needed |
| `image_asset_id` | string | Uploaded photo asset ID |
| `script` | string | Plain text narrator script |
| `voice_id` | string | Required for avatar videos |
| `audio_url` / `audio_asset_id` | string | Pre-recorded audio instead of TTS |
| `resolution` | string | `"1080p"` or `"720p"` |
| `aspect_ratio` | string | `"16:9"` or `"9:16"` |
| `motion_prompt` | string | Motion/expression direction (photo avatars) |
| `expressiveness` | string | `"high"`, `"medium"`, or `"low"` (photo avatars) |
| `remove_background` | boolean | Remove avatar background |
| `background` | object | `{type:"color", value:"#1E40AF"}` or `{type:"image", url:"..."}` |
| `voice_settings` | object | `{speed: 1.0, pitch: 0, locale: "en-US"}` |
| `callback_url` | string | Webhook for completion |

**When to use Avatar Video vs Video Agent:**

| | Video Agent (`/v3/video-agents`) | Avatar Video (`/v3/videos`) |
|---|---|---|
| **Input** | Full prompt with creative direction | Script + avatar/image + voice |
| **Scenes** | Auto scene planning, B-roll, transitions | Single continuous take |
| **Best for** | Produced videos with graphics and scenes | Talking-head / narrator videos |
| **Cost** | $0.0333/sec | $0.10/sec |

### Error Handling

| Error | Action |
|-------|--------|
| 401 Unauthorized | API key invalid. Check HEYGEN_API_KEY. |
| 402 Payment Required | Insufficient credits. Tell user. |
| 429 Rate Limited | Wait 60s, retry once. |
| 500+ Server Error | Retry once after 30s. |
| 200 but no video_id | Retry once. If still failing, tell user to check HeyGen dashboard. |

**Asset upload failure:** Log which asset failed, proceed without it. Inform the user.

### Polling for Completion

```bash
curl -s "https://api.heygen.com/v3/videos/<video_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Status: `pending` → `processing` → `completed` | `failed`

Response on completion includes `video_url`, `thumbnail_url`, `duration`.

**Polling cadence:**
1. First check at **2 minutes** after submission.
2. Every **30 seconds** for the next 3 minutes.
3. Every **60 seconds** up to 30 minutes.
4. After **30 minutes**, stop polling and give the user the dashboard fallback.

**Webhook alternative:** If a `callback_url` was provided, HeyGen will POST to it on completion. No polling needed. Manage webhooks:
```bash
# Register
curl -X POST "https://api.heygen.com/v3/webhooks" ...
# List
curl -s "https://api.heygen.com/v3/webhooks" ...
# Delete
curl -X DELETE "https://api.heygen.com/v3/webhooks/<id>" ...
```

### Delivery

On success, share:
```
Your video is ready! 🎬

🔗 Video: https://app.heygen.com/videos/<video_id>

Quick check against your brief:
✓ Duration: 58s actual vs 60s target (97%)
✓ Tone: casual-confident
✓ Topic: single-topic ✓
✓ Assets referenced: 2/2
✓ Avatar: [name] (avatar_id: ...)
```

**Always report actual vs target duration with percentage.** This data feeds the padding calibration loop.

**NEVER share the raw mp4 URL** from the API response. Those are temporary S3 links.

### Video Management

```bash
# List all videos
curl -s "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# Delete a video
curl -X DELETE "https://api.heygen.com/v3/videos/<video_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

---

## Phase 5 — Review and Deliver

### Completion Status Report

After delivering the video, always append a status:

- **DONE** — Video completed, duration within 15% of target.
- **DONE_WITH_CONCERNS** — Completed with issues. List each concern and recommended fix.
- **BLOCKED** — Cannot proceed. State what's blocking and what was tried.
- **NEEDS_CONTEXT** — Missing information. State exactly what's needed.

```
📊 **Status: DONE**
All checks passed. Duration within target.
```

### Self-Evaluation Log Entry

After EVERY generation (successful or not), append to `heygen-video-producer-log.jsonl`:

```bash
echo '{"timestamp":"<ISO-8601>","video_id":"<id>","session_id":"<session_id_or_null>","prompt_type":"full_producer|enhanced|quick_shot|interactive","target_duration":<seconds>,"padded_duration":<padded_seconds>,"actual_duration":<actual_or_null>,"duration_ratio":<ratio_or_null>,"padding_multiplier":<1.3|1.4|1.6>,"word_count":<words>,"scene_count":<scenes>,"avatar_id":"<id_or_null>","voice_id":"<id_or_null>","style_id":"<id_or_null>","orientation":"landscape|portrait","files_attached":<count>,"generation_path":"video_agent|avatar_video|interactive_session","status":"DONE|DONE_WITH_CONCERNS|BLOCKED","concerns":["<list>"],"what_worked":"<brief>","what_to_improve":"<brief>","topic":"<topic>"}' >> /Users/heyeve/.openclaw/workspace/heygen-video-producer-log.jsonl
```

**New fields explained:**
- `session_id` — v3 returns this alongside `video_id`. Track for debugging and interactive session follow-ups.
- `padded_duration` — the duration you told Video Agent (after multiplier). Compare with `actual_duration` to calibrate.
- `padding_multiplier` — which multiplier was used (1.3, 1.4, or 1.6). Helps tune the padding table over time.
- `voice_id`, `orientation`, `files_attached` — full generation context for pattern analysis.

**Always log.** Even failed attempts. The log is how we learn.

### Iteration Loop

If user wants changes:
1. Track what was tried. Don't repeat failed approaches.
2. Adjust the prompt based on feedback.
3. Re-generate → re-poll → re-review.
4. No iteration cap. Keep going until the user is happy.

Iteration intelligence:
- "Make it punchier" → Energy words in opening, shorter first sentence, front-load the hook
- "Slow it down" → Reduce word count 15-20%, add breathing room
- "Different approach" → Restructure script, change tone/opening
- "Assets aren't showing" → Strengthen asset anchoring language
- Never retry with the exact same prompt. Always change something.

---

## Best Practices

1. **Front-load the hook.** First 5 seconds = 80% of retention. Never open with context-setting.
2. **One idea per video.** Video Agent handles single-topic dramatically better.
3. **Write for the ear.** If you wouldn't say it to a friend, rewrite it.
4. **150 words/min ceiling.** Faster = rushed. Slower = boring.
5. **Asset anchoring > asset dumping.** Tie each asset to a specific script moment.
6. **Narrator framing > generic framing.** "A confident narrator explains..." >> "Create a video about..."
7. **Tone specificity matters.** "Casual-confident, like a tech YouTuber" >> "professional."
8. **Duration signaling.** Explicitly state padded seconds in the prompt.
9. **Use styles when they fit.** A curated `style_id` saves prompt engineering effort on visual treatment.
10. **Interactive sessions for complex projects.** When a one-shot prompt feels risky, iterate with the agent first.

---

## Quick Reference

### Endpoints (ALL v3)

| Action | Method | Endpoint |
|--------|--------|----------|
| **Video Agent (primary)** | POST | `/v3/video-agents` |
| **Create Interactive Session** | POST | `/v3/video-agents/sessions` |
| **Poll Session** | GET | `/v3/video-agents/sessions/{session_id}` |
| **Send Session Message** | POST | `/v3/video-agents/sessions/{session_id}/messages` |
| **Stop Session** | POST | `/v3/video-agents/sessions/{session_id}/stop` |
| **Avatar Video (direct)** | POST | `/v3/videos` |
| **Poll Video Status** | GET | `/v3/videos/{video_id}` |
| **List Videos** | GET | `/v3/videos` |
| **Delete Video** | DELETE | `/v3/videos/{video_id}` |
| **List Avatar Groups** | GET | `/v3/avatars` |
| **Get Avatar Group** | GET | `/v3/avatars/{group_id}` |
| **List Avatar Looks** | GET | `/v3/avatars/looks` |
| **Get Avatar Look** | GET | `/v3/avatars/looks/{look_id}` |
| **Create Avatar** | POST | `/v3/avatars` |
| **List Voices** | GET | `/v3/voices` |
| **TTS** | POST | `/v3/voices/speech` |
| **List Styles** | GET | `/v3/video-agents/styles` |
| **Upload Asset** | POST | `/v3/assets` |
| **Webhooks** | POST/GET/DELETE | `/v3/webhooks` |

### Auth
- Header: `X-Api-Key: $HEYGEN_API_KEY`
- Docs: https://developers.heygen.com/docs/quick-start

### Pricing
| Feature | Cost |
|---------|------|
| Video Agent | $0.0333/sec |
| Avatar Video | $0.10/sec |
| TTS (Starfish) | $0.000333/sec |
| Video Translation | $0.05/sec (speed) / $0.10/sec (precision) |

### Complete Prompt Example

Brief: "60-second product demo about HeyGen's Video Agent API for developers, casual-confident tone"

Assembled prompt (with 1.4x padding → 85-second budget), sent to `POST /v3/video-agents`:

```json
{
  "prompt": "A young male tech presenter in a modern workspace walks developers through HeyGen's Video Agent API, showing how one API call produces a complete video. This is an 85-second video covering ONE topic: the Video Agent API.\n\nScene 1: Intro (Motion Graphics) — 8s\n  Visual: (Motion Graphics) HeyGen logo animates on dark blue. Title \"Video Agent API\" types on.\n  VO: \"What if you could generate a full production video with a single API call? No timeline. No editing. Just one prompt.\"\n\nScene 2: The Problem (A-roll) — 12s\n  Visual: (A-roll) Narrator speaking to camera.\n  VO: \"Building video into your app used to mean stitching together templates, managing assets, and wrestling with rendering pipelines.\"\n\nScene 3: The Solution (Motion Graphics) — 15s\n  Visual: (Motion Graphics) Animated code snippet showing a curl request to /v3/video-agents. Response shows video_id.\n  VO: \"Video Agent changes that. Send a prompt. The API handles scene planning, avatars, B-roll, transitions, and rendering.\"\n\nScene 4: How It Works (A-roll + overlay) — 15s\n  Visual: (A-roll + overlay) Narrator left 35%. Right shows pipeline: Prompt → Scene Planning → Asset Selection → Rendering.\n  VO: \"Under the hood, Video Agent breaks your prompt into scenes, picks visuals, selects an avatar and voice, and renders. Two to three minutes.\"\n\nScene 5: Use Cases (Motion Graphics) — 15s\n  Visual: (Motion Graphics) Three cards: Personalized Sales Videos, Auto-Generated Tutorials, Product Updates.\n  VO: \"Teams use it for personalized sales outreach, auto-generated tutorials, and weekly updates that used to take a full production day.\"\n\nScene 6: CTA (Motion Graphics) — 10s\n  Visual: (Motion Graphics) Dark background, \"developers.heygen.com\" in large text. Logo below.\n  VO: \"One API call. Full production video. Check out the docs and start building.\"\n\n---\nVisual style: Minimalistic, clean. #1E40AF primary blue, #F8FAFC background, #1a1a1a dark sections.\nMedia types: Motion Graphics for data/code/diagrams. A-roll for narrator. No AI-generated footage.\nInclude intro with logo animation, chapter breaks, and branded end card.",
  "avatar_id": "<look_id if custom avatar selected>",
  "voice_id": "<voice_id if specified>",
  "orientation": "landscape"
}
```

---

## Evaluation

Run evals to test prompt quality without spending credits:

1. Read `evals/run-eval.md` — produces prompts for test cases and scores them
2. Compare with `evals/compare.md` — diffs two eval runs to catch regressions
3. Baselines from batch test (Mar 24, 2026) in `evals/test-prompts.json`
