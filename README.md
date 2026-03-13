# HeyGen Skills for Claude Code

A collection of skills for working with the HeyGen AI video creation API, designed for use with Claude Code and other skills-compatible agents.

## Skills

| Skill | Description |
|-------|-------------|
| [create-video](skills/create-video) | Create videos from a text prompt — describe what you want and AI handles the rest (Video Agent API) |
| [avatar-video](skills/avatar-video) | Build videos with precise control over avatars, voices, scripts, scenes, and backgrounds (v2 API) |
| [text-to-speech](skills/text-to-speech) | Generate standalone speech audio from text using HeyGen's Starfish TTS model with voice, speed, pitch, and emotion control |
| [video-translate](skills/video-translate) | Translate and dub existing videos into 12+ languages with lip-sync, voice cloning, and multi-speaker support |
| [heygen](skills/heygen) | *(Deprecated)* Legacy combined skill — use `create-video` or `avatar-video` instead |

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
| Generate speech audio from text | `text-to-speech` |
| List TTS voices | `text-to-speech` |
| Translate/dub an existing video | `video-translate` |
| Batch translate to multiple languages | `video-translate` |

## Example Prompts

```
"Create a 60-second product demo video"

"I need avatar Josh to read this exact script with a blue background"

"Generate a TTS audio file with an excited female voice"

"Translate this YouTube video to Spanish and French"

"Build a 3-scene video: intro, feature demo, and CTA with different backgrounds"

"Use the prompt optimizer to create a scene-by-scene script"
```

## API Reference

All skills use the HeyGen API:
- Base URL: `https://api.heygen.com`
- Authentication: `X-Api-Key` header
- API Versions: v1, v2 (varies by endpoint)

### Key Endpoints

| Endpoint | Skill | Purpose |
|----------|-------|---------|
| `POST /v1/video_agent/generate` | create-video | One-shot prompt-to-video |
| `POST /v2/video/generate` | avatar-video | Precise multi-scene video generation |
| `GET /v2/videos/{video_id}` | create-video, avatar-video | Get video details and status |
| `GET /v2/videos` | create-video, avatar-video | List account videos |
| `DELETE /v2/videos/{video_id}` | create-video, avatar-video | Delete a video |
| `GET /v2/avatars` | avatar-video | List available avatars |
| `GET /v2/voices` | avatar-video | List available voices |
| `POST /v1/audio/text_to_speech` | text-to-speech | Generate speech audio |
| `GET /v1/audio/voices` | text-to-speech | List TTS-compatible voices |
| `POST /v2/video_translate` | video-translate | Start video translation |

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
