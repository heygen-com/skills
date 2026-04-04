---
name: avatar-video
description: |
  Create AI avatar videos with precise control over avatars, voices, scripts, and backgrounds using HeyGen's v3 API (POST /v3/videos). Two modes: type="avatar" with avatar_id, or type="image" with an image AssetInput (Avatar IV). Use when: (1) Choosing a specific avatar and voice for a video, (2) Writing exact scripts for an avatar to speak, (3) Animating a photo into a speaking video (type="image"), (4) Transparent background videos with remove_background, (5) Integrating HeyGen avatars with Remotion, (6) Batch video generation with exact specs, (7) Brand-consistent production videos with precise control.
homepage: https://docs.heygen.com/reference/create-an-avatar-video
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Avatar Video

Create AI avatar videos with full control over avatars, voices, scripts, and backgrounds using `POST /v3/videos`. Two creation modes via discriminated union on `type`:
- `"type": "avatar"` + `avatar_id` — use a HeyGen avatar from the library
- `"type": "image"` + `image` (AssetInput) — animate any photo via Avatar IV

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X GET "https://api.heygen.com/v3/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Tool Selection

If HeyGen MCP tools are available (`mcp__heygen__*`), **prefer them** over direct HTTP API calls — they handle authentication and request formatting automatically.

| Task | MCP Tool | Fallback (Direct API) |
|------|----------|----------------------|
| Check video status / get URL | `mcp__heygen__get_video` | `GET /v3/videos/{video_id}` |
| List account videos | `mcp__heygen__list_videos` | `GET /v3/videos` |
| Delete a video | `mcp__heygen__delete_video` | `DELETE /v3/videos/{video_id}` |

Video generation (`POST /v3/videos`) and avatar/voice listing are done via direct API calls — see reference files below.

## Default Workflow

1. **List avatar looks** — `GET /v3/avatars/looks` → pick a look, note its `id` (this is the `avatar_id`) and `default_voice_id`. See [avatars.md](references/avatars.md)
2. **List voices** (if needed) — `GET /v3/voices` → pick a voice matching the avatar's gender/language. See [voices.md](references/voices.md)
3. **Write the script** — Structure scenes with one concept each. See [scripts.md](references/scripts.md)
4. **Generate the video** — `POST /v3/videos` with `avatar_id`, `voice_id`, `script`, and optional `background` per scene. See [video-generation.md](references/video-generation.md)
5. **Poll for completion** — `GET /v3/videos/{video_id}` until status is `completed`. See [video-status.md](references/video-status.md)

## Routing: This Skill vs Create Video

**This skill** = precise control (specific avatar, exact script, custom background).
**create-video** = prompt-based ("make me a video about X", AI handles the rest).

## Reference Files

Read these as needed — they contain endpoint details, request/response schemas, and code examples (curl, TypeScript, Python).

**Core workflow:**
- [references/video-generation.md](references/video-generation.md) — `POST /v3/videos` request fields, avatar input modes, voice settings, backgrounds
- [references/avatars.md](references/avatars.md) — `GET /v3/avatars` (groups) and `GET /v3/avatars/looks` (looks → `avatar_id`)
- [references/voices.md](references/voices.md) — `GET /v3/voices` with filtering by language, gender, engine
- [references/video-status.md](references/video-status.md) — `GET /v3/videos/{id}` polling patterns and download

**Customization:**
- [references/scripts.md](references/scripts.md) — Script writing, SSML break tags, pacing
- [references/backgrounds.md](references/backgrounds.md) — Solid color and image backgrounds
- [references/captions.md](references/captions.md) — Auto-generated captions/subtitles
- [references/text-overlays.md](references/text-overlays.md) — Text overlays with fonts and positioning

**Advanced:**
- [references/photo-avatars.md](references/photo-avatars.md) — Animate photos via `type: "image"` (Avatar IV), AI-generated avatars
- [references/templates.md](references/templates.md) — Template listing and variable replacement
- [references/remotion-integration.md](references/remotion-integration.md) — Using HeyGen avatars in Remotion compositions
- [references/webhooks.md](references/webhooks.md) — Webhook endpoints and events
- [references/assets.md](references/assets.md) — Uploading images, videos, audio
- [references/dimensions.md](references/dimensions.md) — Resolution and aspect ratios
- [references/quota.md](references/quota.md) — Credit system and usage limits

## Best Practices

1. **Preview avatars before generating** — Use `GET /v3/avatars/looks` and download `preview_image_url` so the user can see the avatar before committing
2. **Use avatar's default voice** — Most avatars have a `default_voice_id` pre-matched for natural results
3. **Fallback: match gender manually** — If no default voice, ensure avatar and voice genders match
4. **Use test mode for development** — Set `test: true` to avoid consuming credits (output will be watermarked)
5. **Set generous timeouts** — Video generation often takes 5-15 minutes, sometimes longer
6. **Validate inputs** — Check avatar and voice IDs exist before generating
