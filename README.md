# HeyGen Skills for Claude Code

A knowledge base of best practices and API documentation for working with the HeyGen AI avatar video creation API, designed for use with Claude Code.

## Overview

This skills package provides Claude Code with domain-specific knowledge about the HeyGen API, enabling it to:

- Generate AI avatar videos with precise control (v2 API)
- Create videos from simple prompts using Video Agent
- Optimize prompts for better Video Agent results
- Work with avatars, voices, and backgrounds
- Handle video translation and dubbing
- Manage streaming avatars for real-time interaction
- Create photo avatars (talking photos)
- Integrate with Remotion for programmatic video composition
- Configure webhooks and callbacks

## Installation

### Option 1: Using add-skill CLI (Recommended)

Install using the [add-skill](https://github.com/vercel-labs/add-skill) CLI:

```bash
# Install to Claude Code globally
npx skills add heygen-com/skills -a claude-code -g

# Or install to current project only
npx skills add heygen-com/skills -a claude-code

# List available skills first
npx skills add heygen-com/skills --list
```

This works with Claude Code, Cursor, Codex, and [13 other agents](https://github.com/vercel-labs/add-skill#available-agents).

### Option 2: Manual Installation

Clone and symlink to your Claude skills directory:

```bash
# Clone the repository
git clone https://github.com/heygen-com/skills.git

# Symlink to personal skills (available in all projects)
ln -s $(pwd)/skills/skills/heygen ~/.claude/skills/heygen

# OR symlink to project skills (available in current project only)
mkdir -p .claude/skills
ln -s $(pwd)/skills/skills/heygen .claude/skills/heygen
```

### Option 3: Direct Copy

Copy the skill directly to your project:

```bash
git clone https://github.com/heygen-com/skills.git
mkdir -p .claude/skills
cp -r skills/skills/heygen .claude/skills/
```

### Verify Installation

The skill should appear when Claude Code loads. You can verify by asking Claude about HeyGen APIs.

## Quick Reference

| Task | Reference Files |
|------|-----------------|
| Generate video from prompt (easy) | [prompt-optimizer.md](skills/heygen/references/prompt-optimizer.md) → [video-agent.md](skills/heygen/references/video-agent.md) |
| Generate video with precise control | [video-generation.md](skills/heygen/references/video-generation.md), [avatars.md](skills/heygen/references/avatars.md), [voices.md](skills/heygen/references/voices.md) |
| Check video status / get download URL | [video-status.md](skills/heygen/references/video-status.md) |
| Add captions or text overlays | [captions.md](skills/heygen/references/captions.md), [text-overlays.md](skills/heygen/references/text-overlays.md) |
| Transparent video for compositing | [video-generation.md](skills/heygen/references/video-generation.md) (WebM section) |
| Real-time interactive avatar | [streaming-avatars.md](skills/heygen/references/streaming-avatars.md) |
| Translate/dub existing video | [video-translation.md](skills/heygen/references/video-translation.md) |
| Use with Remotion | [remotion-integration.md](skills/heygen/references/remotion-integration.md) |

## Contents

### Foundation
- **authentication.md** - API key setup and X-Api-Key header
- **quota.md** - Credit system and usage limits
- **video-status.md** - Polling patterns and download URLs
- **assets.md** - Uploading images, videos, audio

### Core Video Creation
- **avatars.md** - Listing avatars, styles, avatar_id selection
- **voices.md** - Voice configuration, locales, speed/pitch
- **scripts.md** - Writing scripts, pauses, pacing
- **video-generation.md** - Video creation workflow (v2 API)
- **video-agent.md** - One-shot prompt-to-video generation
- **prompt-optimizer.md** - Writing effective Video Agent prompts (scene-by-scene structure, timing, visual styles)
- **dimensions.md** - Resolution and aspect ratios

### Video Customization
- **backgrounds.md** - Solid colors, images, and video backgrounds
- **text-overlays.md** - Adding text with fonts and positioning
- **captions.md** - Auto-generated captions and subtitles

### Advanced Features
- **templates.md** - Template-based video generation
- **video-translation.md** - Translation and dubbing
- **streaming-avatars.md** - Real-time interactive avatars
- **photo-avatars.md** - Photo-based avatar creation
- **webhooks.md** - Event notifications

### Integration
- **remotion-integration.md** - Using HeyGen in Remotion compositions

## Usage

When working with HeyGen code, Claude Code will automatically reference these files to provide accurate, up-to-date guidance.

### Example Prompts

```
"Create a 60-second product demo video using the Video Agent API"

"Help me generate a HeyGen video with a custom background"

"How do I list available avatars in HeyGen?"

"Create a video translation workflow for Spanish and French"

"Set up webhooks for video completion notifications"

"Use the prompt optimizer to create a scene-by-scene script for my video"
```

### Video Agent Workflow

For quick video generation from a text prompt:

1. Use the **prompt-optimizer.md** guidelines to structure your prompt with scenes, timing, and visual styles
2. Call the Video Agent API endpoint (`POST /v1/video_agent/generate`)
3. Poll for status using **video-status.md** patterns
4. Download the completed video

## API Reference

The references are based on the HeyGen API documentation:
- Base URL: `https://api.heygen.com`
- Authentication: `X-Api-Key` header
- API Versions: v1, v2 (varies by endpoint)

### Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/video_agent/generate` | One-shot prompt-to-video (Video Agent) |
| `POST /v2/video/generate` | Precise multi-scene video generation |
| `GET /v1/video_status.get` | Check video generation status |
| `GET /v2/avatars` | List available avatars |
| `GET /v2/voices` | List available voices |

## Requirements

- HeyGen API key (get one at [HeyGen Developer Portal](https://app.heygen.com/settings?from=&nav=API))
- Claude Code CLI

## Contributing

To add or update references:

1. Edit the relevant `.md` file in `skills/heygen/references/`
2. Update `skills/heygen/SKILL.md` if adding new files
3. Include both curl and TypeScript/Python examples where applicable
4. Test that the skill loads correctly

## License

MIT

## Related Resources

- [HeyGen API Documentation](https://docs.heygen.com)
- [HeyGen Developer Portal](https://app.heygen.com/settings?from=&nav=API)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
