# HeyGen Skills for Claude Code

A collection of skills for working with the HeyGen AI video creation API, designed for use with Claude Code and other skills-compatible agents.

## Skills

| Skill | Description |
|-------|-------------|
| [heygen](skills/heygen) | Create AI avatar videos with Video Agent or precise v2 API control. Covers avatars, voices, backgrounds, captions, prompts, and Remotion integration |
| [text-to-speech](skills/text-to-speech) | Generate standalone speech audio from text using HeyGen's Starfish TTS model with voice, speed, pitch, and emotion control |
| [video-translate](skills/video-translate) | Translate and dub existing videos into 12+ languages with lip-sync, voice cloning, and multi-speaker support |

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
npx skills add heygen-com/skills --skill text-to-speech
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
| Generate video from a prompt | `heygen` |
| Generate video with precise scene control | `heygen` |
| List avatars and voices | `heygen` |
| Generate speech audio from text | `text-to-speech` |
| List TTS voices | `text-to-speech` |
| Translate/dub an existing video | `video-translate` |
| Batch translate to multiple languages | `video-translate` |

## Example Prompts

```
"Create a 60-second product demo video using the Video Agent API"

"Generate a TTS audio file with an excited female voice"

"Translate this YouTube video to Spanish and French"

"Help me list available HeyGen avatars and pick one for my video"

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
| `POST /v1/video_agent/generate` | heygen | One-shot prompt-to-video |
| `POST /v2/video/generate` | heygen | Precise multi-scene video generation |
| `GET /v1/video_status.get` | heygen | Check video generation status |
| `GET /v2/avatars` | heygen | List available avatars |
| `GET /v2/voices` | heygen | List available voices |
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
