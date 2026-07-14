# HeyGen Video Agent — NanoClaw Container Skill

## When to Use

Use this skill when the user wants to create a video with an AI avatar presenter.
Triggers: "make a video", "create a video message", "record a video", "avatar video",
"talking head video", "video pitch", "video update".

NOT for: image generation, audio-only TTS, video translation, or cinematic b-roll.

## Required Environment

- `HEYGEN_API_KEY` — Get from https://app.heygen.com/settings?nav=API
- `heygen` CLI — install: `curl -fsSL https://static.heygen.ai/cli/install.sh | bash`. Verify: `heygen auth status`.

## Steps

### Step 1: Discover Available Avatars

```bash
heygen avatar list --ownership public --limit 5 | jq '.data[] | {group_id: .id, avatar_name: .name}'
```

`avatar list` returns avatar **groups** — each `.id` is a `group_id`, not an `avatar_id`. The `avatar_id` you pass to generation is a specific **look**: list looks with `heygen avatar looks list --group-id <group_id> | jq '.data[] | {avatar_id: .id, preview_image_url}'` and pick a look's `.id`. If the user already has a specific look id, use it directly.

### Step 2: Find a Voice

```bash
heygen voice list --limit 10 | jq '.data[] | {voice_id, name, language}'
```

Pick a `voice_id` matching the desired language and tone.

### Step 3: Write the Script

Write a spoken-word script for the avatar. Rules:
- Write for speech, not text. Short sentences. Natural pauses.
- 150 words per minute is the target pace.
- 30 seconds = ~75 words. 60 seconds = ~150 words.
- No stage directions. No markdown. Just what the avatar says.

### Step 4: Generate the Video

```bash
heygen video-agent create \
  --prompt "YOUR SCRIPT HERE" \
  --avatar-id "AVATAR_ID_HERE" \
  --voice-id "VOICE_ID_HERE" \
  --orientation landscape \
  --wait --timeout 10m
```

With `--wait`, the CLI blocks until the video completes and emits the final status object. Without `--wait`, submission returns immediately — save the `session_id` from stdout for manual polling.

`--timeout 10m` is sized for short videos (≤60s). **Bump to `--timeout 45m` for videos >60s** or when targeting 2+ minute output — Video Agent generation routinely takes 20-45m for longer clips.

### Step 5: Poll for Completion (only without `--wait`)

```bash
heygen video-agent get SESSION_ID | jq '{status: .data.status, video_id: .data.video_id}'
```

Poll every 15 seconds. Session `status` is one of `thinking`, `waiting_for_input`, `reviewing`, `generating`, `completed`, `failed` — not a strict linear sequence (`waiting_for_input` only occurs in chat mode). Terminal states are `completed` and `failed`.

Once `.data.video_id` is present, run `heygen video get <video_id>` and read `.data.video_url` for the download URL (and `.data.failure_message` on failure).

### Step 6: Deliver

Download the video and present it to the user:

```bash
heygen video download <video_id>
```

Writes the MP4 to disk and emits `{"asset", "message", "path"}` on stdout — chain on `.path`.

## Verification

After generating a video, confirm:
1. CLI exits `0` (generation accepted). Without `--wait`, stdout includes a `session_id` for polling; with `--wait`, the CLI polls the video to completion and stdout is the final **video** resource (`.data.id`, `.data.video_url`).
2. Polling (or `--wait`) returns `status: "completed"` within 5 minutes
3. `heygen video get <video_id>` returns a valid HTTPS `.data.video_url`
4. Downloaded file is a playable MP4

## Report Feedback

After the video is delivered and verified, report how the run went (once per task):

```bash
heygen feedback --rating <1-5> --comment "<what worked, or what broke>"
```

`--rating` runs 1 (broke / unusable) to 5 (worked great); put any bug or friction in `--comment`. Anonymous, no API key; no-ops if analytics are opted out (`HEYGEN_NO_ANALYTICS` or `heygen config set analytics false`).

## Troubleshooting

| Symptom | Fix |
|-------|-----|
| Exit code `3` / auth error on stderr | Check `heygen auth status`; run `heygen auth login` or set `HEYGEN_API_KEY` |
| Exit code `2` / usage error | Run `heygen video-agent create --help` — verify flag names and required args |
| Status stuck on `thinking` / `generating` | Wait up to 5 minutes. Videos over 60s take longer. |
| Missing `video_id` | Session may have failed. Check `.data.status`; if `failed`, inspect the full `heygen video-agent get <session_id>` response for the failure detail. |

## Limits

- Free tier: 1 minute of video per month
- API trial: 3 free credits on signup
- Max video length per request: ~5 minutes
- Concurrent generation: depends on plan tier
