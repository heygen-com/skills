# API Reference — HeyGen v3

## API Modes

**MCP (preferred):** HeyGen Remote MCP at `https://mcp.heygen.com/mcp/v1/` — OAuth-based, no API key needed. Tools prefixed `mcp__heygen__*`. Uses the user's existing HeyGen plan credits.

**CLI fallback:** All endpoints use base URL `https://api.heygen.com` with header `X-Api-Key: $HEYGEN_API_KEY`.

## Live Documentation

Canonical docs with exact schemas, curl examples, and field descriptions:
- **Full index:** https://developers.heygen.com/llms.txt
- **Any page as markdown:** append `.md` to URL (e.g. `https://developers.heygen.com/docs/video-agent.md`)
- **API reference pages:** `https://developers.heygen.com/reference/<slug>.md`
- **MCP docs:** https://developers.heygen.com/mcp.md

When in doubt about a field name or type, fetch the `.md` page before guessing.

## Endpoints

| Action | MCP Tool | CLI Method | CLI Endpoint |
|--------|----------|------------|--------------|
| **Video Agent (primary)** | `create_video_agent` | POST | `/v3/video-agents` |
| **Poll Session** | `get_video_agent_session` | GET | `/v3/video-agents/sessions/{session_id}` |
| **Send Session Message** | `send_video_agent_message` | POST | `/v3/video-agents/sessions/{session_id}/messages` |
| **Stop Session** | `stop_video_agent_session` | POST | `/v3/video-agents/sessions/{session_id}/stop` |
| **Session Resources** | `get_video_agent_resource` | — | — |
| **Session Videos** | `list_video_agent_session_videos` | — | — |
| **Avatar Video (direct)** | `create_video_from_avatar` | POST | `/v3/videos` |
| **Image Video (direct)** | `create_video_from_image` | POST | `/v3/videos` |
| **Poll Video Status** | `get_video` | GET | `/v3/videos/{video_id}` |
| **List Videos** | `list_videos` | GET | `/v3/videos` |
| **Delete Video** | `delete_video` | DELETE | `/v3/videos/{video_id}` |
| **List Avatar Groups** | `list_avatar_groups` | GET | `/v3/avatars` |
| **Get Avatar Group** | `get_avatar_group` | GET | `/v3/avatars/{group_id}` |
| **List Avatar Looks** | `list_avatar_looks` | GET | `/v3/avatars/looks` |
| **Get Avatar Look** | `get_avatar_look` | GET | `/v3/avatars/looks/{look_id}` |
| **Update Avatar Look** | `update_avatar_look` | — | — |
| **Create Photo Avatar** | `create_photo_avatar` | POST | `/v3/avatars` |
| **Create Prompt Avatar** | `create_prompt_avatar` | POST | `/v3/avatars` |
| **Create Digital Twin** | `create_digital_twin` | POST | `/v3/avatars` |
| **Avatar Consent** | `create_avatar_consent` | — | — |
| **List Voices** | `list_voices` | GET | `/v3/voices` |
| **Design Voice** | `design_voice` | POST | `/v3/voices` |
| **TTS** | `create_speech` | POST | `/v3/voices/speech` |
| **Create Lip Sync** | `create_lipsync` | POST | `/v3/overdubs` |
| **List Lip Syncs** | `list_lipsyncs` | GET | `/v3/overdubs` |
| **Get Lip Sync** | `get_lipsync` | GET | `/v3/overdubs/{id}` |
| **Translate Video** | `create_video_translation` | POST | `/v3/video-translations` |
| **Get Translation** | `get_video_translation` | GET | `/v3/video-translations/{id}` |
| **Translation Languages** | `list_video_translation_languages` | GET | `/v3/video-translations/languages` |
| **Account Info** | `get_current_user` | — | — |
| **List Styles** | `list_video_agent_styles` | GET | `/v3/video-agents/styles` |
| **Upload Asset** | — | POST | `/v3/assets` |
| **Webhooks** | — | POST/GET/DELETE | `/v3/webhooks` |

## Video Agent — One-Shot

**MCP:**
```
create_video_agent(
  prompt=<constructed prompt>,
  avatar_id=<optional, from discovery>,
  voice_id=<optional, from discovery>,
  style_id=<optional, from styles>,
  orientation="landscape"
)
```

**CLI:**
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
      {"type": "asset_id", "asset_id": "<uploaded_id>"}
    ],
    "callback_url": "<optional webhook URL>",
    "callback_id": "<optional custom ID for webhook payload>",
    "incognito_mode": false
  }'
```

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✓ | Constructed prompt with script, visual directions, style |
| `avatar_id` | string | | Look ID from avatar discovery |
| `voice_id` | string | | Voice ID from voice listing |
| `style_id` | string | | Style ID from styles listing |
| `orientation` | string | | `"landscape"` or `"portrait"` (default: landscape) |
| `files` | array | | File objects: `{type, url/asset_id/data}` |
| `callback_url` | string | | Webhook URL for completion notification |
| `callback_id` | string | | Custom ID included in webhook payload |
| `incognito_mode` | boolean | | Disables cross-session memory injection/extraction. Use for evals. |

Response: `{"data": {"video_id": "abc123", "session_id": "sess_xyz789"}}`

**⚠️ Always capture `session_id`.** Cannot be recovered later via GET.

## Interactive Session Mode (⚠️ EXPERIMENTAL)

> Sessions have known reliability issues: frequently stuck at `processing`, `reviewing` may never be reached, follow-up messages fail with timing errors, stop command may not trigger generation. Use one-shot for production.

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

**Poll:** `GET /v3/video-agents/sessions/<session_id>`
Status flow: `processing` → `reviewing` → `generating` → `completed` | `failed`

**Send follow-up:** `POST /v3/video-agents/sessions/<session_id>/messages`
```json
{"message": "Make the intro more energetic", "auto_proceed": false}
```

**Stop (finalize):** `POST /v3/video-agents/sessions/<session_id>/stop`

## Avatar Video (Direct Control Path)

For talking-head videos without Video Agent scene planning:

```bash
curl -s -X POST "https://api.heygen.com/v3/videos" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "avatar_id": "<look_id>",
    "script": "<narrator script>",
    "voice_id": "<voice_id>",
    "title": "My Video",
    "resolution": "1080p",
    "aspect_ratio": "16:9"
  }'
```

| Parameter | Type | Notes |
|-----------|------|-------|
| `avatar_id` | string | Mutually exclusive with `image_url` / `image_asset_id` |
| `image_url` | string | Direct photo URL — no avatar creation needed |
| `image_asset_id` | string | Uploaded photo asset ID |
| `script` | string | Plain text narrator script |
| `voice_id` | string | Required |
| `audio_url` / `audio_asset_id` | string | Pre-recorded audio instead of TTS |
| `resolution` | string | `"1080p"` or `"720p"` |
| `aspect_ratio` | string | `"16:9"` or `"9:16"` |
| `motion_prompt` | string | Motion/expression direction (photo avatars) |
| `expressiveness` | string | `"high"`, `"medium"`, or `"low"` (photo avatars) |
| `remove_background` | boolean | Remove avatar background |
| `background` | object | `{type:"color", value:"#1E40AF"}` or `{type:"image", url:"..."}` |
| `voice_settings` | object | `{speed: 1.0, pitch: 0, locale: "en-US"}` — set locale to match video language (e.g., `ja-JP`, `es-ES`, `ko-KR`) |

**When to use which:**

| | Video Agent (`/v3/video-agents`) | Avatar Video (`/v3/videos`) |
|---|---|---|
| **Input** | Full prompt with creative direction | Script + avatar/image + voice |
| **Scenes** | Auto scene planning, B-roll, transitions | Single continuous take |
| **Best for** | Produced videos with graphics and scenes | Talking-head / narrator videos |
| **Cost** | $0.0333/sec | $0.10/sec |

## Polling

```bash
curl -s "https://api.heygen.com/v3/videos/<video_id>" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

Status: `pending` → `processing` → `completed` | `failed`

Completion includes `video_url`, `thumbnail_url`, `duration`.

**Cadence:**
1. First check at **2 minutes**
2. Every **30 seconds** for next 3 minutes
3. Every **60 seconds** up to 30 minutes
4. Stuck `pending` >10 min → flag to user
5. After 30 min → stop, give dashboard fallback

## Webhooks

### Inline Callback (Simplest)

Add `callback_url` + `callback_id` directly to your `POST /v3/video-agents` or `POST /v3/video-agents/sessions` request:
```json
{"prompt": "...", "callback_url": "https://your-server.com/hook", "callback_id": "my-ref-123"}
```
HeyGen POSTs to your URL when the video completes or fails. Payload includes `video_id`, `video_url`, `callback_id`.

### Registered Webhooks (Persistent)

```bash
# Register endpoint for specific event types
curl -X POST "https://api.heygen.com/v3/webhooks" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/webhook", "events": ["video_agent.success", "video_agent.fail"]}'

# List registered webhooks
curl -s "https://api.heygen.com/v3/webhooks" -H "X-Api-Key: $HEYGEN_API_KEY"

# Delete
curl -X DELETE "https://api.heygen.com/v3/webhooks/<id>" -H "X-Api-Key: $HEYGEN_API_KEY"

# Browse delivered events (filter by type or entity)
curl -s "https://api.heygen.com/v3/webhooks/events?event_type=video_agent.success&limit=10" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Event Types

| Event | Description |
|-------|-------------|
| `avatar_video.success` | Avatar video completed |
| `avatar_video.fail` | Avatar video failed |
| `video_agent.success` | Video Agent session completed |
| `video_agent.fail` | Video Agent session failed |
| `video_translate.success/fail` | Translation completed/failed |
| `photo_avatar_generation.success/fail` | Photo avatar created/failed |
| `photo_avatar_train.success/fail` | Photo avatar trained/failed |
| `live_avatar.success/fail` | Live avatar session ended |

Each event payload: `{event_id, event_type, event_data: {video_id, video_url, callback_id}, created_at}`

## Video Management

```bash
# List all videos
curl -s "https://api.heygen.com/v3/videos" -H "X-Api-Key: $HEYGEN_API_KEY"

# Delete a video
curl -X DELETE "https://api.heygen.com/v3/videos/<video_id>" -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Error Handling

| Error | Action |
|-------|--------|
| 401 Unauthorized | API key invalid. Check HEYGEN_API_KEY. |
| 402 Payment Required | Insufficient credits. Tell user. |
| 429 Rate Limited | Wait 60s, retry once. |
| 500+ Server Error | Retry once after 30s. |
| 200 but no video_id | Retry once. If still failing, tell user to check dashboard. |

**Asset upload failure:** Log which asset failed, proceed without it. Inform user.

## Voice Design

Find matching voices from HeyGen's library using natural language. Uses semantic search (Pinecone) over all existing voices. No new voices are generated and no quota is consumed. Returned `voice_id`s work immediately in any video endpoint.

```bash
curl -s -X POST "https://api.heygen.com/v3/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A calm, warm female voice with a slight Korean accent. Professional but approachable.",
    "seed": 0
  }'
```

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `prompt` | string | ✓ | Natural language description of the desired voice |
| `seed` | integer | | Start at 0. Controls which set of voices you get. Deterministic: same prompt + seed = same results. Increment for more options. |

**Response:**
```json
{
  "data": {
    "seed": 0,
    "voices": [
      {
        "voice_id": "kWwhw6YmjhNmgmLELlEy",
        "name": "Calm Korean Pro",
        "gender": "female",
        "language": "English",
        "preview_audio_url": "https://files2.heygen.ai/voice-design/previews/...",
        "support_pause": true,
        "support_locale": false,
        "type": "public"
      }
    ]
  }
}
```

Returns 3 voices per seed. Deterministic: same prompt + seed always returns the same set. If none match, increment seed and try again. Each voice has a `preview_audio_url` (MP3) for user auditioning.

**Key:** This is semantic search, not generation. Free to call. No voice slots consumed.

**Language matching:** Include the target language in the voice design prompt (e.g., "Japanese speaker", "Korean native"). For voice browsing, use the `language` query parameter:
```bash
curl -s "https://api.heygen.com/v3/voices?type=public&language=ja&limit=20" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Pricing

| Feature | Cost |
|---------|------|
| Video Agent | $0.0333/sec |
| Avatar Video | $0.10/sec |
| TTS (Starfish) | $0.000333/sec |
| Video Translation | $0.05/sec (speed) / $0.10/sec (precision) |
