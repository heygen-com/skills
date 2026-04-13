# Avatar Discovery & Voice Selection

## Path A: Discover Existing Avatars

### A1: Check for private avatars first

**If user specifies an avatar by name** (e.g. "use Eve's Podcast look"), take the fast path:
```bash
curl -s "https://api.heygen.com/v3/avatars/looks?ownership=private&limit=50" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```
Filter client-side by name match. Avoids the 2-call group→looks pattern.

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

**ALWAYS show the preview image** when presenting an avatar look. Each look response includes `preview_image_url` — display inline.

### A2: Check last-used avatar

Check `heygen-video-log.jsonl` for last used avatar_id. If found:
```bash
curl -s "https://api.heygen.com/v3/avatars/looks/<look_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```
Show preview image: "Last time you used [Avatar Name]. Use her again?"

### A3: Avatar conversation

Ask: "Do you want a visible presenter, or voice-over only?"

If voice-over only → no `avatar_id`. State in prompt: "Voice-over narration only."

If presenter wanted, present private avatars first. For public/stock avatars, browse by group:

```bash
# Step 1: List avatar groups
curl -s "https://api.heygen.com/v3/avatars?ownership=public&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Show group names + one representative image. Let the user pick a person.

```bash
# Step 2: Show looks for the chosen group
curl -s "https://api.heygen.com/v3/avatars/looks?group_id=<group_id>&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

**Why group-first:** The flat `/v3/avatars/looks?ownership=public` endpoint returns 50+ results for only 3 unique people per page. Group-level browsing (2 calls) gives much better discovery UX.

### A4: Voice direction

After avatar is settled, confirm voice preferences (accent, delivery style, language).

**ALWAYS show a playable voice preview.** Each voice response includes `preview_audio_url` — share it.

**Handling missing/broken previews:** Some voices return bare `s3://` paths or `null`. When this happens: note "(no preview available)" and offer to generate a short TTS sample via `POST /v3/voices/speech`.

---

## Path B: Create a New Avatar

Use `POST /v3/avatars`. Supports two modes:

**Mode 1 — New character** (omit `avatar_group_id`): Creates a new person with their own group.
**Mode 2 — New look** (include `avatar_group_id`): Adds a variation to an existing character.

Always use Mode 2 when the avatar already exists and you're creating a variant (different outfit, orientation fix, bg change). Only use Mode 1 for genuinely new characters.

Three creation types:

**Photo avatar (from user's photo):**
```bash
curl -X POST "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "photo",
    "name": "My Avatar",
    "file": {"type": "url", "url": "https://example.com/headshot.jpg"},
    "avatar_group_id": "<optional — include to add look to existing character>"
  }'
```
Photo requirements: JPEG or PNG, min 512x512, clear front-facing face, good lighting.

**AI-generated avatar (from text prompt):**
```bash
curl -X POST "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "prompt",
    "name": "Tech Presenter",
    "prompt": "Young professional woman, modern workspace, confident smile",
    "avatar_group_id": "<optional — include to add look to existing character>"
  }'
```
Prompt max: 1000 characters. Optional: up to 3 `reference_images`.

**Video avatar (from user's video recording):**
```bash
curl -X POST "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "video",
    "name": "My Video Avatar",
    "file": {"type": "asset_id", "asset_id": "<uploaded_asset_id>"},
    "avatar_group_id": "<optional — include to add look to existing character>"
  }'
```

All three return `avatar_item` with `id` (look_id) and `group_id` — use `id` as `avatar_id` for videos.

Files: `{"type": "url", "url": "..."}`, `{"type": "asset_id", "asset_id": "..."}`, or `{"type": "base64", "data": "...", "content_type": "..."}`.

---

## Path C: Direct Image (Simplest for One-Off)

Skip avatar creation. Pass `image_url` directly to `POST /v3/videos`:

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
Also accepts `image_asset_id`. Fastest path for one-off talking-head video.

---

## Voice Selection

```bash
curl -s "https://api.heygen.com/v3/voices?type=private&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"

# Public voices with filters
curl -s "https://api.heygen.com/v3/voices?type=public&engine=starfish&language=en&gender=female&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

---

## How Avatar/Voice Are Passed

Video Agent (`POST /v3/video-agents`) accepts `avatar_id` and `voice_id` as top-level parameters:

```json
{
  "prompt": "...",
  "avatar_id": "look_id_from_discovery",
  "voice_id": "voice_id_from_discovery",
  "style_id": "optional_style_id",
  "orientation": "landscape"
}
```

- **Custom/stock avatar with known ID** → pass `avatar_id`. Do NOT describe avatar's appearance in prompt. Only delivery style + background/environment.
- **No avatar_id (auto-select)** → describe desired presenter in prompt. Less reliable (~80% vs ~97%).
- **Voice-over only** → omit `avatar_id`, state in prompt.

> 💡 Always provide explicit `avatar_id` for presenter videos. 97.6% duration accuracy vs ~80% without.
