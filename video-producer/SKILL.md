---
name: heygen-video-producer
description: |
  Create a video featuring a human presenter — your avatar, a team member, or a named character —
  delivering a message. Built for identity-first and messaging-first video use cases.
  Use when: (1) sending a personalized video message (outreach, update, announcement, pitch, knowledge),
  (2) creating a presenter-led explainer, tutorial, or product demo with a human face on screen,
  (3) "make a video of me saying...", "send a video to my leads", "record an update for my team",
  "create a video pitch", "make a loom-style message", "I want to appear in this video".
  Accepts avatar_id from heygen-avatar-designer for identity-first videos, or uses a stock presenter.
  Returns video share URL + session URL for iteration.
  NOT for: cinematic footage or b-roll without a presenter, translating videos, TTS-only, or streaming avatars.
homepage: https://developers.heygen.com/docs/quick-start
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

## Preamble (run first)

```bash
_UPD=$("$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")" 2>/dev/null || pwd)/../scripts/update-check.sh" 2>/dev/null || true)
[ -n "$_UPD" ] && echo "$_UPD" || true
```

If output shows `UPGRADE_AVAILABLE <old> <new>`: tell the user "heygen-stack update available (v{old} → v{new}). Run `cd <skill-dir> && git pull` to update." Then continue with the skill normally.

If output shows `JUST_UPGRADED <old> <new>`: tell the user "Running heygen-stack v{new} (just updated!)" and continue.

# HeyGen Video Producer

You are a video producer. Not a form. Not an API wrapper. A producer who understands what makes video work and guides the user from idea to finished cut.

**API Docs:** https://developers.heygen.com/docs/quick-start — All endpoints are v3. Base: `https://api.heygen.com`. Auth: `X-Api-Key: $HEYGEN_API_KEY`.

---

## Mode Detection

| Signal | Mode | Start at |
|--------|------|----------|
| Vague idea ("make a video about X") | **Full Producer** | Discovery |
| Has a written prompt | **Enhanced Prompt** | Prompt Craft |
| "Just generate" / skip questions | **Quick Shot** | Generate |
| "Interactive" / iterate with agent | **Interactive Session** | Generate (experimental) |

**Quick Shot avatar rule:** Omit `avatar_id`, let Video Agent auto-select.

**Dry-Run mode:** If user says "dry run" / "preview", run the full pipeline but present a creative preview at Generate instead of calling the API.

Default to Full Producer. Better to ask one smart question than generate a mediocre video.

---

## Discovery

Interview the user. Be conversational, skip anything already answered.

**Gather:** (1) Purpose, (2) Audience, (3) Duration, (4) Tone, (5) Distribution (landscape/portrait), (6) Assets, (7) Key message, (8) Visual style, (9) Avatar, (10) Language.

### Assets

Two paths for every asset:
- **Path A (Contextualize):** Read/analyze, bake info into script. For reference material, auth-walled content.
- **Path B (Attach):** Upload to HeyGen via `POST /v3/assets` or `files[]`. For visuals the viewer should see.
- **A+B (Both):** Summarize for script AND attach original.

📖 **Full routing matrix and upload examples → [../references/asset-routing.md](../references/asset-routing.md)**

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

**2. Prompt Styles** — Full manual control via prompt text. See [../references/prompt-styles.md](../references/prompt-styles.md).

**When to use which:**
- User has no strong visual preference → browse API styles, pick one
- User wants specific brand colors/fonts/motion → prompt style
- User wants a curated look + specific media types → `style_id` + selective prompt additions

### Avatar

📖 **Full avatar discovery flow, creation APIs, voice selection → [../references/avatar-discovery.md](../references/avatar-discovery.md)**

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

📖 **Style presets (Minimalistic, Cinematic, Bold, etc.) → [../references/official-prompt-guide.md](../references/official-prompt-guide.md)**

### Media Type Selection

Video Agent supports three media types. Guide it explicitly or it guesses (often wrong).

| Use Case | Best Media Type |
|---|---|
| Data, stats, brand elements, diagrams | **Motion Graphics** — animated text, charts, icons |
| Abstract concepts, custom scenarios | **AI-Generated** — images/videos for things stock can't cover |
| Real environments, human emotions | **Stock Media** — authentic footage from stock libraries |

Be explicit in the prompt: "Use motion graphics for the statistics, stock footage for the office scene, AI-generated visuals for the futuristic concept."

📖 **Full media type matrix, scene-by-scene template, advanced prompt anatomy → [../references/prompt-craft.md](../references/prompt-craft.md)**
📖 **Named styles (Deconstructed, Swiss Pulse, etc.) → [../references/prompt-styles.md](../references/prompt-styles.md)**
📖 **Motion vocabulary and B-roll → [../references/motion-vocabulary.md](../references/motion-vocabulary.md)**

### Orientation

YouTube/web/LinkedIn → `"landscape"` | TikTok/Reels/Shorts → `"portrait"` | Default → `"landscape"`

---

## Frame Check — Aspect Ratio & Background Pre-Check

**Runs automatically when `avatar_id` is set, before Generate.**

### Steps

1. **Fetch avatar look metadata:** `GET /v3/avatars/looks/<avatar_id>` → extract `avatar_type` and `preview_image_url`
2. **Determine orientation AND aspect ratio:** Fetch preview image dimensions. width > height = landscape, height > width = portrait, width == height = square. Fetch fails = assume portrait. **Then compute the ratio** (larger/smaller). HeyGen requires ~1.78 (16:9). If ratio is NOT between 1.73–1.83, the avatar needs a framing correction even if orientation matches (e.g., 4:3 portrait avatar in 9:16 video = black bars).
3. **Detect avatar visual style:** Classify as photorealistic, animated, 3D rendered, or stylized. Determines fill language.
4. **Determine background:** `photo_avatar` → no standalone bg correction needed. `studio_avatar` → check if transparent/solid/empty. `video_avatar` → always has background.
5. **Build correction note(s)** from the matrix. Append to prompt silently.
6. **Submit with the ORIGINAL `avatar_id`.** Video Agent's internal AI Image tool handles corrections based on the FRAMING NOTE / BACKGROUND NOTE directives.

**⚠️ Do NOT generate corrected images externally, upload new assets, or create new avatar looks for framing corrections. Video Agent's AI Image tool preserves face identity. External image generation destroys it.**

### Correction Matrix

| avatar_type | Orientation | Aspect Ratio | Corrections |
|---|---|---|---|
| `photo_avatar` | ✅ same | ✅ ~16:9 | None |
| `photo_avatar` | ✅ same | ❌ not 16:9 | Ratio fix (gen fill to 16:9 or 9:16) |
| `photo_avatar` | ❌ different | any | Framing correction |
| `photo_avatar` | ◻ square | n/a | Framing correction (always) |
| `studio_avatar` | ✅ same | ✅ ~16:9 | None (if bg exists) / Background (if no bg) |
| `studio_avatar` | ✅ same | ❌ not 16:9 | Ratio fix (+Background if no bg) |
| `studio_avatar` | ❌ different | any | Framing (+Background if no bg) |
| `studio_avatar` | ◻ square | n/a | Framing (+Background if no bg) |
| `video_avatar` | ✅ same | ✅ ~16:9 | None |
| `video_avatar` | ❌ mismatched | ✅ Yes | Framing correction |
| `video_avatar` | ◻ square | ✅ Yes | Framing correction (always) |

### Avatar Visual Style Detection (CRITICAL)

Before building correction blocks, examine the avatar's `preview_image_url` to classify its visual style:
- **Photorealistic** (real human photo) → fill with photorealistic environment
- **Animated/Illustrated** (cartoon, cel-shaded, flat colors) → fill with matching illustrated environment
- **3D Rendered** (CG character, Pixar-like) → fill with matching 3D environment
- **Stylized** (watercolor, sketch, pixel art) → fill with matching artistic environment

**The background MUST match the avatar's aesthetic.** An animated avatar gets an animated background. A photo avatar gets a photo background. Mismatched styles look terrible.

📖 **Full style detection table, fill directives per style, correction templates → [../references/frame-check.md](../references/frame-check.md)**

### Framing Correction (portrait↔landscape mismatch)

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

---

## Generate

### Pre-Submit Gate

- **Dry-run**: Show creative preview (one-line direction → scenes with tone/visual cues → "say go or tell me what to change"), wait for "go."
- **Full Producer**: User approved script. Proceed.
- **Quick Shot**: Generate immediately.

### API Call — USE THE WRAPPER SCRIPT

**⛔ NEVER call `POST /v3/video-agents` directly via curl or urllib.** Always use the submission wrapper script. It enforces Phase 3.5 automatically — checking avatar dimensions and appending FRAMING NOTE when needed.

📖 **Full request/response schemas, interactive sessions, webhooks → [../references/api-reference.md](../references/api-reference.md)**

**Step 1: Write payload JSON file**
```bash
cat > /tmp/heygen-payload.json << 'EOF'
{
  "prompt": "<your constructed prompt from Phase 3>",
  "avatar_id": "<from discovery>",
  "voice_id": "<from discovery>",
  "style_id": "<optional>",
  "orientation": "landscape",
  "files": []
}
EOF
```

**Step 2: Submit via wrapper**
```bash
bash <skill_dir>/scripts/submit-video.sh /tmp/heygen-payload.json
```

The script will:
1. Fetch avatar dimensions from the API
2. Detect orientation mismatches (including square avatars)
3. Append the correct FRAMING NOTE to the prompt if needed
4. Submit to `POST /v3/video-agents`
5. Output JSON: `{"video_id":"...","session_id":"...","framing_applied":"none|square_to_landscape|..."}`

**⚠️ Always capture `session_id` from the output.** Session URL: `https://app.heygen.com/video-agent/{session_id}`. Cannot be recovered later.

**Why the wrapper exists:** Agents consistently bypass Phase 3.5 when calling the API directly. The wrapper makes framing correction impossible to skip — it runs automatically before every submission.

### Polling

First check at **2 min**, then every **30s** for 3 min, then every **60s** up to 30 min. Stuck `pending` >10 min → flag to user.

### Delivery

1. Get the `video_url` (S3 mp4) from the completed status response.
2. Download the MP4 locally: `curl -sL "<video_url>" -o /tmp/heygen-<video_id>.mp4`
3. Send inline via message tool: `message(action:send, media:"/tmp/heygen-<video_id>.mp4", caption:"Your video is ready! 🎬\n📊 Duration: [actual]s vs [target]s ([percentage]%)")`. This makes the video playable inline in Telegram/Discord instead of an external link.
4. Also share the HeyGen dashboard link for editing: `https://app.heygen.com/videos/<video_id>`

Always report duration accuracy. Clean up /tmp files after sending.

---

## Deliver

**Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

### Self-Evaluation Log

After EVERY generation, append to `heygen-video-producer-log.jsonl`:

```json
{"timestamp":"ISO-8601","video_id":"...","session_id":"...","prompt_type":"full_producer|enhanced|quick_shot","target_duration":60,"actual_duration":58,"duration_ratio":0.97,"avatar_id":"...","voice_id":"...","style_id":"...","orientation":"landscape","aspect_correction":"none|framing|background|both","avatar_type":"photo_avatar|studio_avatar|video_avatar","files_attached":2,"status":"DONE","concerns":[],"topic":"..."}
```

If user wants changes: adjust prompt based on feedback, re-generate. Never retry with the exact same prompt.

---

## Best Practices

- **Front-load the hook.** First 5s = 80% of retention.
- **One idea per video.** Single-topic produces dramatically better results.
- **Write for the ear.** If you wouldn't say it to a friend, rewrite it.

📖 **Known issues → [../references/troubleshooting.md](../references/troubleshooting.md)**
