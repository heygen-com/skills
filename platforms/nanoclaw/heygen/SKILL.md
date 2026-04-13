# HeyGen Video Agent — NanoClaw Container Skill

## When to Use

Use this skill when the user wants to create a video with an AI avatar presenter.
Triggers: "make a video", "create a video message", "record a video", "avatar video",
"talking head video", "video pitch", "video update".

NOT for: image generation, audio-only TTS, video translation, or cinematic b-roll.

## Required Environment

- `HEYGEN_API_KEY` — Get from https://app.heygen.com/settings?nav=API

## Steps

### Step 1: Discover Available Avatars

```bash
curl -s -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq '.data.avatars[:5] | .[] | {avatar_id, avatar_name}'
```

Pick an avatar_id. If the user has a specific avatar, use that ID.

### Step 2: Find a Voice

```bash
curl -s -X GET "https://api.heygen.com/v2/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq '.data.voices[:10] | .[] | {voice_id, display_name, language}'
```

Pick a voice_id matching the desired language and tone.

### Step 3: Write the Script

Write a spoken-word script for the avatar. Rules:
- Write for speech, not text. Short sentences. Natural pauses.
- 150 words per minute is the target pace.
- 30 seconds = ~75 words. 60 seconds = ~150 words.
- No stage directions. No markdown. Just what the avatar says.

### Step 4: Generate the Video

```bash
curl -s -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_inputs": [{
      "character": {
        "type": "avatar",
        "avatar_id": "AVATAR_ID_HERE",
        "avatar_style": "normal"
      },
      "voice": {
        "type": "text",
        "input_text": "YOUR SCRIPT HERE",
        "voice_id": "VOICE_ID_HERE"
      }
    }],
    "dimension": {
      "width": 1920,
      "height": 1080
    }
  }'
```

Save the `session_id` from the response.

### Step 5: Poll for Completion

```bash
curl -s -X GET "https://api.heygen.com/v3/video-agents/sessions/SESSION_ID" \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq '{status: .data.status, video_url: .data.video_url}'
```

Poll every 15 seconds. Status progression: `pending` → `processing` → `completed`.

When status is `completed`, the `video_url` field contains the download URL.

### Step 6: Deliver

Download the video and present it to the user:

```bash
curl -sL -o output.mp4 "VIDEO_URL_HERE"
```

## Verification

After generating a video, confirm:
1. Response contains `session_id` (generation accepted)
2. Polling returns `status: "completed"` within 5 minutes
3. `video_url` is a valid HTTPS URL
4. Downloaded file is a playable MP4

## Troubleshooting

| Error | Fix |
|-------|-----|
| 401 Unauthorized | Check HEYGEN_API_KEY is set and valid |
| 400 Bad Request | Verify avatar_id and voice_id exist (re-run Steps 1-2) |
| Status stuck on "processing" | Wait up to 5 minutes. Videos over 60s take longer. |
| Empty video_url | Video may have failed. Check `error` field in poll response. |

## Limits

- Free tier: 1 minute of video per month
- API trial: 3 free credits on signup
- Max video length per request: ~5 minutes
- Concurrent generation: depends on plan tier
