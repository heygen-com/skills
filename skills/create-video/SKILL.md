---
name: create-video
description: |
  Create videos from a text prompt using HeyGen's Video Agent. Use when: (1) Creating a video from a description or idea, (2) Generating explainer, demo, or marketing videos from a prompt, (3) Making a video without specifying exact avatars, voices, or scenes, (4) Quick video prototyping or drafts, (5) One-shot prompt-to-video generation, (6) User says "make me a video" or "create a video about X".
homepage: https://docs.heygen.com/reference/generate-video-agent
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
curl -X POST "https://api.heygen.com/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a 60-second product demo video."}'
```

## Tool Selection

If HeyGen MCP tools are available (`mcp__heygen__*`), **prefer them** over direct HTTP API calls — they handle authentication and request formatting automatically.

| Task | MCP Tool | Fallback (Direct API) |
|------|----------|----------------------|
| Generate video from prompt | `mcp__heygen__generate_video_agent` | `POST /v1/video_agent/generate` |
| Check video status / get URL | `mcp__heygen__get_video` | `GET /v2/videos/{video_id}` |
| List account videos | `mcp__heygen__list_videos` | `GET /v2/videos` |
| Delete a video | `mcp__heygen__delete_video` | `DELETE /v2/videos/{video_id}` |

If no HeyGen MCP tools are available, use direct HTTP API calls as documented in the reference files.

## Default Workflow

Always use [prompt-optimizer.md](references/prompt-optimizer.md) guidelines to structure prompts with scenes, timing, and visual styles.

**With MCP tools:**
1. Write an optimized prompt using [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md)
2. Call `mcp__heygen__generate_video_agent` with prompt and config (duration_sec, orientation, avatar_id)
3. Call `mcp__heygen__get_video` with the returned video_id to poll status and get the download URL

**Without MCP tools (direct API):**
1. Write an optimized prompt using [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md)
2. `POST /v1/video_agent/generate` — see [video-agent.md](references/video-agent.md)
3. `GET /v2/videos/<id>` — see [video-status.md](references/video-status.md)

## Quick Reference

| Task | MCP Tool | Read |
|------|----------|------|
| Generate video from prompt | `mcp__heygen__generate_video_agent` | [prompt-optimizer.md](references/prompt-optimizer.md) → [visual-styles.md](references/visual-styles.md) → [video-agent.md](references/video-agent.md) |
| Check video status / get download URL | `mcp__heygen__get_video` | [video-status.md](references/video-status.md) |
| Upload reference files for prompt | — | [assets.md](references/assets.md) |

## When to Use This Skill vs Avatar Video

This skill is for **prompt-based video creation** — describe what you want, and the AI handles the rest.

If the user needs **precise control** over specific avatars, exact scripts, per-scene voice/background configuration, or multi-scene composition, use the **avatar-video** skill instead.

| User Says | This Skill | Avatar Video Skill |
|-----------|:----------:|:------------------:|
| "Make me a video about X" | ✓ | |
| "Create a product demo" | ✓ | |
| "I want avatar Y to say exactly Z" | | ✓ |
| "Multi-scene video with different backgrounds" | | ✓ |
| "Transparent WebM for compositing" | | ✓ |

## Reference Files

### Core Workflow
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - Writing effective prompts (core workflow + rules)
- [references/visual-styles.md](references/visual-styles.md) - 20 named visual styles with full specs
- [references/prompt-examples.md](references/prompt-examples.md) - Full production prompt example + ready-to-use templates
- [references/video-agent.md](references/video-agent.md) - Video Agent API endpoint details

### Foundation
- [references/video-status.md](references/video-status.md) - Polling patterns and download URLs
- [references/webhooks.md](references/webhooks.md) - Webhook endpoints and events
- [references/assets.md](references/assets.md) - Uploading images, videos, audio as references
- [references/dimensions.md](references/dimensions.md) - Resolution and aspect ratios
- [references/quota.md](references/quota.md) - Credit system and usage limits

## Best Practices

1. **Optimize your prompt** — The difference between mediocre and professional results depends entirely on prompt quality. Always use the prompt optimizer
2. **Specify duration** — Use `config.duration_sec` for predictable length
3. **Lock avatar if needed** — Use `config.avatar_id` for consistency across videos
4. **Upload reference files** — Help the agent understand your brand/product
5. **Iterate on prompts** — Refine based on results; Video Agent is great for quick iterations
