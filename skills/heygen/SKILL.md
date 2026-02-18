---
name: heygen
description: |
  HeyGen AI video creation API. Use when: (1) Using Video Agent for one-shot prompt-to-video generation, (2) Generating AI avatar videos with /v2/video/generate, (3) Working with HeyGen avatars, voices, backgrounds, or captions, (4) Creating transparent WebM videos for compositing, (5) Polling video status or handling webhooks, (6) Integrating HeyGen with Remotion for programmatic video, (7) Translating or dubbing existing videos, (8) Generating standalone TTS audio with the Starfish model via /v1/audio.
homepage: https://docs.heygen.com/reference/generate-video-agent
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen API

AI avatar video creation API for generating talking-head videos, explainers, and presentations.

## Default Workflow

**Prefer Video Agent API** (`POST /v1/video_agent/generate`) for most video requests.
Always use [prompt-optimizer.md](references/prompt-optimizer.md) guidelines to structure prompts with scenes, timing, and visual styles.

Only use v2/video/generate when user explicitly needs:
- Exact script without AI modification
- Specific voice_id selection
- Different avatars/backgrounds per scene
- Precise per-scene timing control
- Programmatic/batch generation with exact specs

## Quick Reference

| Task | Read |
|------|------|
| Generate video from prompt (easy) | [prompt-optimizer.md](references/prompt-optimizer.md) → [video-agent.md](references/video-agent.md) |
| Generate video with precise control | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |
| Check video status / get download URL | [video-status.md](references/video-status.md) |
| Add captions or text overlays | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |
| Transparent video for compositing | [video-generation.md](references/video-generation.md) (WebM section) |
| Generate standalone TTS audio | [text-to-speech.md](references/text-to-speech.md) |
| Translate/dub existing video | [video-translation.md](references/video-translation.md) |
| Use with Remotion | [remotion-integration.md](references/remotion-integration.md) |

## Reference Files

### Foundation
- [references/authentication.md](references/authentication.md) - API key setup and X-Api-Key header
- [references/quota.md](references/quota.md) - Credit system and usage limits
- [references/video-status.md](references/video-status.md) - Polling patterns and download URLs
- [references/assets.md](references/assets.md) - Uploading images, videos, audio

### Core Video Creation
- [references/avatars.md](references/avatars.md) - Listing avatars, styles, avatar_id selection
- [references/voices.md](references/voices.md) - Listing voices, locales, speed/pitch
- [references/scripts.md](references/scripts.md) - Writing scripts, pauses, pacing
- [references/video-generation.md](references/video-generation.md) - POST /v2/video/generate and multi-scene videos
- [references/video-agent.md](references/video-agent.md) - One-shot prompt video generation
- [references/prompt-optimizer.md](references/prompt-optimizer.md) - Writing effective Video Agent prompts
- [references/dimensions.md](references/dimensions.md) - Resolution and aspect ratios

### Video Customization
- [references/backgrounds.md](references/backgrounds.md) - Solid colors, images, video backgrounds
- [references/text-overlays.md](references/text-overlays.md) - Adding text with fonts and positioning
- [references/captions.md](references/captions.md) - Auto-generated captions and subtitles

### Advanced Features
- [references/templates.md](references/templates.md) - Template listing and variable replacement
- [references/video-translation.md](references/video-translation.md) - Translating videos and dubbing
- [references/text-to-speech.md](references/text-to-speech.md) - Standalone TTS audio with Starfish model
- [references/photo-avatars.md](references/photo-avatars.md) - Creating avatars from photos
- [references/webhooks.md](references/webhooks.md) - Webhook endpoints and events

### Integration
- [references/remotion-integration.md](references/remotion-integration.md) - Using HeyGen in Remotion compositions
