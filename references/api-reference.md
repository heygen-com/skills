# Command Reference — HeyGen v3

## Modes

**MCP (preferred):** HeyGen Remote MCP at `https://mcp.heygen.com/mcp/v1/` — OAuth-based, no API key needed. Tools prefixed `mcp__heygen__*`. Uses the user's existing HeyGen plan credits.

**CLI fallback:** The [HeyGen CLI](https://github.com/heygen-com/heygen-cli) — a single `heygen` binary. Pattern: `heygen <noun> <verb>`. Every command supports `--help`. Never call `api.heygen.com` with curl — use MCP or the CLI.

## CLI setup

Install:
```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash
```

Auth (pick one):
```bash
export HEYGEN_API_KEY=your-key-here     # agent/CI, ephemeral
echo "$KEY" | heygen auth login         # agent, persisted to ~/.heygen/credentials
heygen auth login                       # humans, interactive
heygen auth status                      # verify
```

## CLI behavior

| Aspect | Behavior |
|---|---|
| **stdout** | Always JSON. `heygen video download` writes binary to disk; stdout emits `{"asset", "message", "path"}`. |
| **stderr** | Structured envelope: `{"error": {"code", "message", "hint"}}`. Stable `code` values for branching. |
| **Exit codes** | `0` ok · `1` API/network · `2` usage · `3` auth · `4` timeout under `--wait` (stdout contains partial resource for resume). |
| **Request bodies** | Flags for simple inputs; `-d` for nested JSON (inline, file path, or `-` for stdin). Flags override matching fields. |
| **Async jobs** | `--wait` blocks with exponential backoff; `--timeout` sets max (default 20m). 429s and 5xx retry automatically. |

Extract fields with `jq`:
```bash
heygen video get <video_id> | jq -r '.data.video_page_url'
```

## Live documentation

Canonical docs with exact schemas, examples, and field descriptions:
- **API index:** https://developers.heygen.com/llms.txt
- **Any API page as markdown:** append `.md` to URL (e.g. `https://developers.heygen.com/docs/video-agent.md`)
- **API reference pages:** `https://developers.heygen.com/reference/<slug>.md`
- **CLI docs:** https://developers.heygen.com/cli
- **MCP docs:** https://developers.heygen.com/mcp.md

When in doubt about a field name or type, fetch the `.md` page (or run `heygen <noun> <verb> --help`) before guessing.

## Command surface

| Action | MCP Tool | CLI Command |
|--------|----------|-------------|
| **Video Agent (primary)** | `create_video_agent` | `heygen video-agent create` |
| **Poll Session** | `get_video_agent_session` | `heygen video-agent get --session-id <id>` |
| **Send Session Message** | `send_video_agent_message` | `heygen video-agent send --session-id <id> --message <m>` |
| **Stop Session** | `stop_video_agent_session` | `heygen video-agent stop --session-id <id>` |
| **Session Resources** | `get_video_agent_resource` | `heygen video-agent resources get --session-id <id> --resource-id <id>` |
| **Session Videos** | `list_video_agent_session_videos` | `heygen video-agent videos list --session-id <id>` |
| **Direct Video** | `create_video_from_avatar` / `create_video_from_image` | `heygen video create` |
| **Poll Video Status** | `get_video` | `heygen video get <video_id>` |
| **List Videos** | `list_videos` | `heygen video list` |
| **Delete Video** | `delete_video` | `heygen video delete <video_id>` |
| **Download Video** | — | `heygen video download <video_id>` |
| **List Avatar Groups** | `list_avatar_groups` | `heygen avatar list` |
| **Get Avatar Group** | `get_avatar_group` | `heygen avatar get --group-id <id>` |
| **List Avatar Looks** | `list_avatar_looks` | `heygen avatar looks list` |
| **Get Avatar Look** | `get_avatar_look` | `heygen avatar looks get --look-id <id>` |
| **Update Avatar Look** | `update_avatar_look` | `heygen avatar looks update --look-id <id> --name <n>` |
| **Create Avatar** | `create_photo_avatar` / `create_prompt_avatar` / `create_digital_twin` | `heygen avatar create -d <json>` |
| **Avatar Consent** | `create_avatar_consent` | `heygen avatar consent create --group-id <id>` |
| **List Voices** | `list_voices` | `heygen voice list` |
| **Design Voice** | `design_voice` | `heygen voice create --prompt <p>` |
| **TTS** | `create_speech` | `heygen voice speech create --text <t> --voice-id <id>` |
| **Lipsync** | `create_lipsync` / `list_lipsyncs` / `get_lipsync` | `heygen lipsync create` / `list` / `get --lipsync-id <id>` |
| **Video Translate** | `create_video_translation` | `heygen video-translate create` |
| **Get Translation** | `get_video_translation` | `heygen video-translate get --video-translation-id <id>` |
| **Translation Languages** | `list_video_translation_languages` | `heygen video-translate languages list` |
| **Account Info** | `get_current_user` | `heygen user` |
| **List Styles** | `list_video_agent_styles` | `heygen video-agent styles list` |
| **Upload Asset** | — | `heygen asset create --file <path>` |
| **Webhooks** | — | `heygen webhook endpoints create/list/update/delete` · `heygen webhook events list` |

## Video Agent — one-shot

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
heygen video-agent create \
  --prompt "<constructed prompt>" \
  --avatar-id "<optional, from discovery>" \
  --voice-id "<optional, from discovery>" \
  --style-id "<optional, from styles>" \
  --orientation landscape \
  --wait --timeout 45m
```

Attach files or override advanced fields (e.g. `callback_url`, `callback_id`, `incognito_mode`) via `-d '{...}'`. Flags override matching fields in `-d`.

| Flag | Description |
|------|-------------|
| `--prompt` | Constructed prompt with script, visual directions, style (required) |
| `--avatar-id` | Look ID from avatar discovery |
| `--voice-id` | Voice ID from voice listing |
| `--style-id` | Style ID from `video-agent styles list` |
| `--orientation` | `landscape` or `portrait` (default: landscape) |
| `--mode` | Generation mode override |
| `--callback-url` | Webhook URL for completion notification |
| `--callback-id` | Custom ID included in webhook payload |
| `--incognito-mode` | Disables cross-session memory. Use for evals. |
| `--wait` | Block until the video completes (handles polling with exponential backoff) |
| `--timeout` | Max wall time when using `--wait` (default 20m) |

Returns (submission): `{"data": {"video_id": "abc123", "session_id": "sess_xyz789"}}`. With `--wait`, the CLI blocks and returns the final status object.

**⚠️ Always capture `session_id`.** Cannot be recovered later.

## Interactive session mode (⚠️ EXPERIMENTAL)

> Sessions have known reliability issues: frequently stuck at `processing`, `reviewing` may never be reached, follow-up messages fail with timing errors, stop command may not trigger generation. Use one-shot for production.

```bash
# Create session (no --wait — interactive)
heygen video-agent create --prompt "<initial>" --avatar-id <id> --voice-id <id>

# Poll
heygen video-agent get --session-id <session_id>

# Send follow-up
heygen video-agent send --session-id <session_id> --message "Make the intro more energetic"

# Stop (finalize)
heygen video-agent stop --session-id <session_id>
```

Status flow: `processing` → `reviewing` → `generating` → `completed` | `failed`

## Direct Video (talking-head path)

For talking-head videos without Video Agent scene planning:

```bash
heygen video create -d '{
  "avatar_id": "<look_id>",
  "script": "<narrator script>",
  "voice_id": "<voice_id>",
  "title": "My Video",
  "resolution": "1080p",
  "aspect_ratio": "16:9"
}'
```

| Field | Notes |
|-------|-------|
| `avatar_id` | Mutually exclusive with `image_url` / `image_asset_id` |
| `image_url` | Direct photo URL — no avatar creation needed |
| `image_asset_id` | Uploaded photo asset ID (from `heygen asset create`) |
| `script` | Plain text narrator script |
| `voice_id` | Required |
| `audio_url` / `audio_asset_id` | Pre-recorded audio instead of TTS |
| `resolution` | `"1080p"` or `"720p"` |
| `aspect_ratio` | `"16:9"` or `"9:16"` |
| `motion_prompt` | Motion/expression direction (photo avatars) |
| `expressiveness` | `"high"`, `"medium"`, or `"low"` (photo avatars) |
| `remove_background` | Remove avatar background |
| `background` | `{type:"color", value:"#1E40AF"}` or `{type:"image", url:"..."}` |
| `voice_settings` | `{speed: 1.0, pitch: 0, locale: "en-US"}` — set locale to match video language (`ja-JP`, `es-ES`, `ko-KR`) |

**When to use which:**

| | Video Agent (`video-agent create`) | Direct Video (`video create`) |
|---|---|---|
| **Input** | Full prompt with creative direction | Script + avatar/image + voice |
| **Scenes** | Auto scene planning, B-roll, transitions | Single continuous take |
| **Best for** | Produced videos with graphics and scenes | Talking-head / narrator videos |
| **Cost** | $0.0333/sec | $0.10/sec |

## Polling

```bash
heygen video get <video_id>
```

Status: `pending` → `processing` → `completed` | `failed`

Completion response includes `video_url`, `video_page_url`, `thumbnail_url`, `duration`.

**Cadence (manual polling):**
1. First check at **2 minutes**
2. Every **30 seconds** for next 3 minutes
3. Every **60 seconds** up to 30 minutes
4. Stuck `pending` >10 min → flag to user
5. After 30 min → stop, give dashboard fallback

Prefer `--wait` on creation — the CLI handles this cadence automatically.

## Webhooks

### Inline callback (simplest)

Add `--callback-url` + `--callback-id` directly to `heygen video-agent create`:
```bash
heygen video-agent create --prompt "..." \
  --callback-url "https://your-server.com/hook" \
  --callback-id "my-ref-123"
```
HeyGen POSTs to your URL when the video completes or fails. Payload includes `video_id`, `video_url`, `callback_id`.

### Registered webhooks (persistent)

```bash
# Register endpoint for specific event types
heygen webhook endpoints create \
  --url "https://example.com/webhook" \
  --events video_agent.success --events video_agent.fail

# List registered endpoints
heygen webhook endpoints list

# Rotate signing secret
heygen webhook endpoints rotate-secret --endpoint-id <id>

# Delete
heygen webhook endpoints delete --endpoint-id <id>

# Browse delivered events (filter by type or entity)
heygen webhook events list --event-type video_agent.success --limit 10
```

### Event types

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

Browse all available event types: `heygen webhook event-types list`.

## Video management

```bash
heygen video list
heygen video list --folder-id <id> --limit 50
heygen video delete <video_id>
heygen video download <video_id>        # writes mp4 to disk, emits {"path"} on stdout
```

## Error handling

CLI errors come back as structured envelopes on stderr:
```json
{"error": {"code": "not_found", "message": "Video not found", "hint": "Check ID with: heygen video list"}}
```

| Exit code / error code | Action |
|-------|--------|
| Exit `3` / `auth_*` | API key invalid. Check `heygen auth status`, re-run `heygen auth login`, or set `HEYGEN_API_KEY`. |
| `402` / `payment_required` | Insufficient credits. Tell the user. |
| Exit `1` / `rate_limited` | CLI retries 429s automatically; if it still errors, wait 60s and re-run. |
| Exit `1` / 5xx | CLI retries; if it still errors, retry once after 30s. |
| Exit `4` / timeout under `--wait` | Submission succeeded — stdout contains partial resource with `session_id` / `video_id`. Resume via `heygen video-agent get --session-id <id>`. |
| Exit `2` / usage | Invalid flags or arguments. Run `heygen <command> --help`. |

**Asset upload failure:** Log which asset failed, proceed without it. Inform user.

## Voice Design

Find matching voices from HeyGen's library using natural language. Uses semantic search (Pinecone) over all existing voices. No new voices are generated and no quota is consumed. Returned `voice_id`s work immediately in any video command.

```bash
heygen voice create \
  --prompt "A calm, warm female voice with a slight Korean accent. Professional but approachable." \
  --seed 0
```

| Flag | Description |
|------|-------------|
| `--prompt` | Natural language description of the desired voice (required) |
| `--seed` | Start at 0. Controls which set of voices you get. Deterministic: same prompt + seed = same results. Increment for more options. |
| `--gender` | Optional filter |
| `--locale` | Optional filter |

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

**Key:** Semantic search, not generation. Free to call. No voice slots consumed.

**Language matching:** Include the target language in the voice design prompt (e.g., "Japanese speaker", "Korean native"). For voice browsing, use the `--language` flag:
```bash
heygen voice list --type public --language ja --limit 20
```

## Pricing

| Feature | Cost |
|---------|------|
| Video Agent | $0.0333/sec |
| Avatar Video | $0.10/sec |
| TTS (Starfish) | $0.000333/sec |
| Video Translation | $0.05/sec (speed) / $0.10/sec (precision) |
