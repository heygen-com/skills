# HeyGen Skills for Claude Code

A collection of skills for working with the HeyGen AI video creation API, designed for use with Claude Code and other skills-compatible agents.

## Skills

| Skill | Description |
|-------|-------------|
| [create-video](skills/create-video) | Create videos from a text prompt — describe what you want and AI handles the rest (Video Agent API) |
| [avatar-video](skills/avatar-video) | Build videos with precise control over avatars, voices, scripts, scenes, and backgrounds (v3 API) |
| [ai-video-gen](skills/ai-video-gen) | Generate AI videos from text prompts with multiple provider options (VEO, Kling, Sora, Runway) via the Workflow Gateway |
| [faceswap](skills/faceswap) | Swap a face from a source image into a target video using GPU-accelerated AI via the Workflow Gateway |
| [text-to-speech](skills/text-to-speech) | Generate standalone speech audio from text using HeyGen's Starfish TTS model with voice, speed, pitch, and emotion control |
| [video-translate](skills/video-translate) | Translate and dub existing videos into 12+ languages with lip-sync, voice cloning, and multi-speaker support |
| [visual-style](skills/visual-style) | Create, extract, and apply portable visual design systems (`visual-style.md`) across HeyGen, slides, Figma, and more |
| [video-download](skills/video-download) | Download video and audio from YouTube and 1000+ sites using yt-dlp |
| [video-edit](skills/video-edit) | Edit videos locally using ffmpeg — trim, concat, resize, speed, overlay, extract audio, compress, and convert |
| [video-understand](skills/video-understand) | Understand video content locally using ffmpeg frame extraction and Whisper transcription — no API keys needed |
| [heygen](skills/heygen) | *(Deprecated — uses v1/v2 endpoints)* Legacy combined skill — use `create-video` or `avatar-video` (v3 API) instead |

## Installation

### Option 1: Claude Code Plugin Marketplace

```bash
/plugin marketplace add heygen-com/skills
/plugin install heygen@heygen-skills
```

### Option 2: Using add-skill CLI (Recommended for multi-agent)

Install using the [skills](https://github.com/vercel-labs/skills) CLI:

```bash
# Install all skills globally
npx skills add heygen-com/skills -a claude-code -g

# Or install to current project only
npx skills add heygen-com/skills -a claude-code

# List available skills first
npx skills add heygen-com/skills --list

# Install a specific skill only
npx skills add heygen-com/skills --skill create-video
```

This works with Claude Code, Cursor, Codex, and [other agents](https://github.com/vercel-labs/skills#available-agents).

### Option 3: Manual Installation

Clone and symlink to your Claude skills directory:

```bash
# Clone the repository
git clone https://github.com/heygen-com/skills.git

# Symlink all skills to personal skills directory (available in all projects)
for skill in skills/skills/*/; do
  ln -s "$(pwd)/$skill" ~/.claude/skills/$(basename "$skill")
done

# OR symlink to project skills (available in current project only)
mkdir -p .claude/skills
for skill in skills/skills/*/; do
  ln -s "$(pwd)/$skill" .claude/skills/$(basename "$skill")
done
```

### Verify Installation

The skills should appear when Claude Code loads. You can verify by asking Claude about HeyGen APIs.

## Quick Reference

| Task | Skill |
|------|-------|
| Generate video from a prompt | `create-video` |
| Generate video with precise scene control | `avatar-video` |
| List avatars and voices | `avatar-video` |
| Generate AI video from a text prompt | `ai-video-gen` |
| Swap a face into a video | `faceswap` |
| Generate speech audio from text | `text-to-speech` |
| List TTS voices | `text-to-speech` |
| Translate/dub an existing video | `video-translate` |
| Batch translate to multiple languages | `video-translate` |
| Create a visual design system | `visual-style` |
| Extract a visual style from a website/video/PDF | `visual-style` |
| Apply a visual style to HeyGen/slides/Figma | `visual-style` |
| Download a video from YouTube or other sites | `video-download` |
| Extract audio from a video URL | `video-download` |
| Trim, resize, or compress a video | `video-edit` |
| Concatenate video clips | `video-edit` |
| Extract or replace audio in a video | `video-edit` |
| Understand / transcribe a local video | `video-understand` |
| Extract key frames from a video | `video-understand` |

## Example Prompts

```
"Create a 60-second product demo video"

"I need avatar Josh to read this exact script with a blue background"

"Generate a TTS audio file with an excited female voice"

"Translate this YouTube video to Spanish and French"

"Build a 3-scene video: intro, feature demo, and CTA with different backgrounds"

"Use the prompt optimizer to create a scene-by-scene script"

"Create a visual-style.md for a retro 80s neon aesthetic"

"Extract a visual style from https://stripe.com"

"Apply the Swiss International Style to a HeyGen video about Q4 results"
```

## API Reference

All skills use the HeyGen API:
- Base URL: `https://api.heygen.com`
- Authentication: `X-Api-Key` header
- Primary API Version: v3 (core video, avatar, voice, and TTS endpoints)

### Key Endpoints

| Endpoint | Skill | Purpose |
|----------|-------|---------|
| `POST /v3/video-agents` | create-video | One-shot prompt-to-video |
| `POST /v3/videos` | avatar-video | Precise multi-scene video generation |
| `GET /v3/videos/{video_id}` | create-video, avatar-video | Get video details and status |
| `GET /v3/videos` | create-video, avatar-video | List account videos |
| `DELETE /v3/videos/{video_id}` | create-video, avatar-video | Delete a video |
| `GET /v3/avatars` | avatar-video | List available avatar groups |
| `GET /v3/avatars/looks` | avatar-video | List avatar looks (get `avatar_id`) |
| `GET /v3/voices` | avatar-video, text-to-speech | List available voices |
| `POST /v3/voices/speech` | text-to-speech | Generate speech audio |
| `POST /v2/video_translate` | video-translate | Start video translation |
| `POST /v1/workflows/executions` | ai-video-gen, faceswap | Execute a workflow (video generation, face swap) |
| `GET /v1/workflows/executions/{id}` | ai-video-gen, faceswap | Check workflow execution status |

## Requirements

- HeyGen API key (get one at [HeyGen Developer Portal](https://app.heygen.com/settings?from=&nav=API))
- Claude Code CLI (or any skills-compatible agent)

## Contributing

To add or update skills:

1. Edit the relevant `SKILL.md` or reference files in `skills/<skill-name>/`
2. Include curl, TypeScript, and Python examples where applicable
3. Test that the skill loads correctly
4. Each skill should be self-contained — no cross-skill dependencies

## License

MIT

## Related Resources

- [HeyGen API Documentation](https://docs.heygen.com)
- [HeyGen Developer Portal](https://app.heygen.com/settings?from=&nav=API)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Agent Skills Specification](https://agentskills.io/specification)
