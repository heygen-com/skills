# API Reference — HeyGen v3

All endpoints use base URL `https://api.heygen.com` with header `X-Api-Key: $HEYGEN_API_KEY`.

## Endpoints

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

## Video Agent — One-Shot

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
    "callback_url": "<optional webhook URL>"
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
| `voice_settings` | object | `{speed: 1.0, pitch: 0, locale: "en-US"}` |

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

```bash
# Register
curl -X POST "https://api.heygen.com/v3/webhooks" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/webhook", "events": ["video.completed"]}'

# List
curl -s "https://api.heygen.com/v3/webhooks" -H "X-Api-Key: $HEYGEN_API_KEY"

# Delete
curl -X DELETE "https://api.heygen.com/v3/webhooks/<id>" -H "X-Api-Key: $HEYGEN_API_KEY"
```

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

## Pricing

| Feature | Cost |
|---------|------|
| Video Agent | $0.0333/sec |
| Avatar Video | $0.10/sec |
| TTS (Starfish) | $0.000333/sec |
| Video Translation | $0.05/sec (speed) / $0.10/sec (precision) |
