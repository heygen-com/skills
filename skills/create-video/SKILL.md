---
name: create-video
description: |
  Create videos from a text prompt using HeyGen's Video Agent (POST /v3/video-agents). The default for most video requests — AI handles script, avatar, visuals, voiceover, and captions automatically. Use when: (1) Creating a video from a description or idea, (2) Generating explainer, demo, or marketing videos from a prompt, (3) Making a video without specifying exact avatars, voices, or scenes, (4) Quick video prototyping or drafts, (5) User says "make me a video" or "create a video about X". For precise control over specific avatars, exact scripts, or per-scene configuration, use the avatar-video skill instead.
homepage: https://docs.heygen.com/reference/create-video-with-video-agent
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Create Video

Generate complete videos from a text prompt. Describe what you want and the AI handles script writing, avatar selection, visuals, voiceover, pacing, and captions automatically.

## Authentication

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X POST "https://api.heygen.com/v3/video-agents" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a 60-second product demo video."}'
```

## Tool Selection

If HeyGen MCP tools are available (`mcp__heygen__*`), **prefer them** over direct HTTP API calls — they handle authentication and request formatting automatically.

| Task | MCP Tool | Fallback (Direct API) |
|------|----------|----------------------|
| Generate video from prompt | `mcp__heygen__generate_video_agent` | `POST /v3/video-agents` |
| Check video status / get URL | `mcp__heygen__get_video` | `GET /v3/videos/{video_id}` |
| List account videos | `mcp__heygen__list_videos` | `GET /v3/videos` |
| Delete a video | `mcp__heygen__delete_video` | `DELETE /v3/videos/{video_id}` |

If no HeyGen MCP tools are available, use direct HTTP API calls as documented in the reference files.

## Default Workflow

Always use [prompt-optimizer.md](references/prompt-optimizer.md) guidelines to structure prompts with scenes, timing, and visual styles.

**With MCP tools:**
1. Write an optimized prompt using [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md)
2. Call `mcp__heygen__generate_video_agent` with prompt and config (duration_sec, orientation, avatar_id)
3. Call `mcp__heygen__get_video` with the returned video_id to poll status and get the download URL

**Without MCP tools (direct API):**
1. Write an optimized prompt using [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md)
2. `POST /v3/video-agents` — see [video-agent.md](references/video-agent.md)
3. `GET /v3/videos/<id>` — see [video-status.md](references/video-status.md)

## Reference Files

Read these as needed — they contain endpoint details, request/response schemas, and code examples (curl, TypeScript, Python).

**Core workflow:**
- [references/prompt-optimizer.md](references/prompt-optimizer.md) — Writing effective prompts (scenes, timing, visual styles)
- [references/visual-styles.md](references/visual-styles.md) — 20 named visual styles with full specs
- [references/prompt-examples.md](references/prompt-examples.md) — Production prompt examples and templates
- [references/video-agent.md](references/video-agent.md) — `POST /v3/video-agents` request fields, response format, file inputs

**Foundation:**
- [references/video-status.md](references/video-status.md) — `GET /v3/videos/{id}` polling and download
- [references/webhooks.md](references/webhooks.md) — Webhook endpoints and events
- [references/assets.md](references/assets.md) — Uploading images, videos, audio as references
- [references/dimensions.md](references/dimensions.md) — Resolution and aspect ratios
- [references/quota.md](references/quota.md) — Credit system and usage limits

## Best Practices

1. **Optimize your prompt** — quality depends entirely on prompt structure. Always use the prompt optimizer
2. **Lock avatar if needed** — pass `avatar_id` for consistency across videos
3. **Specify voice** — pass `voice_id` for a specific narrator voice
4. **Upload reference files** — help the agent understand your brand/product
5. **Iterate on prompts** — refine based on results; Video Agent is great for quick iterations
