---
name: heygen
description: |
  HeyGen AI avatar video creation API. Use when: (1) Generating AI avatar videos with /v2/video/generate, (2) Using Video Agent for one-shot prompt-to-video generation, (3) Working with HeyGen avatars, voices, backgrounds, or captions, (4) Creating transparent WebM videos for compositing, (5) Polling video status or handling webhooks, (6) Integrating HeyGen with Remotion for programmatic video, (7) Translating or dubbing existing videos.
---

# HeyGen API

AI avatar video creation API for generating talking-head videos, explainers, and presentations.

## Quick Reference

| Task | Read |
|------|------|
| Generate video from prompt (easy) | [prompt-optimizer.md](references/prompt-optimizer.md) → [video-agent.md](references/video-agent.md) |
| Generate video with precise control | [video-generation.md](references/video-generation.md), [avatars.md](references/avatars.md), [voices.md](references/voices.md) |
| Check video status / get download URL | [video-status.md](references/video-status.md) |
| Add captions or text overlays | [captions.md](references/captions.md), [text-overlays.md](references/text-overlays.md) |
| Transparent video for compositing | [video-generation.md](references/video-generation.md) (WebM section) |
| Real-time interactive avatar | [streaming-avatars.md](references/streaming-avatars.md) |
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
- [references/streaming-avatars.md](references/streaming-avatars.md) - Real-time interactive sessions
- [references/photo-avatars.md](references/photo-avatars.md) - Creating avatars from photos
- [references/webhooks.md](references/webhooks.md) - Webhook endpoints and events

### Integration
- [references/remotion-integration.md](references/remotion-integration.md) - Using HeyGen in Remotion compositions
