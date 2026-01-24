# HeyGen Skills for Claude Code

A knowledge base of best practices and API documentation for working with the HeyGen AI avatar video creation API, designed for use with Claude Code.

## Overview

This skills package provides Claude Code with domain-specific knowledge about the HeyGen API, enabling it to:

- Generate AI avatar videos
- Work with avatars and voices
- Handle video translation and dubbing
- Manage streaming avatars
- Create photo avatars (talking photos)
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

## Contents

### Foundation
- **authentication.md** - API key setup and authentication patterns
- **quota.md** - Credit system and usage limits
- **video-status.md** - Polling and status checking
- **assets.md** - Asset upload and management

### Core Video Creation
- **avatars.md** - Avatar listing and selection
- **voices.md** - Voice configuration and languages
- **video-generation.md** - Video creation workflow (v2 API)
- **dimensions.md** - Resolution and aspect ratios

### Video Customization
- **backgrounds.md** - Colors, images, and video backgrounds
- **text-overlays.md** - Adding text to videos
- **captions.md** - Auto-generated captions

### Advanced Features
- **templates.md** - Template-based video generation
- **video-translation.md** - Translation and dubbing
- **streaming-avatars.md** - Real-time interactive avatars
- **photo-avatars.md** - Photo-based avatar creation
- **webhooks.md** - Event notifications

## Usage

When working with HeyGen code, Claude Code will automatically reference these rule files to provide accurate, up-to-date guidance.

### Example Prompts

```
"Help me generate a HeyGen video with a custom background"

"How do I list available avatars in HeyGen?"

"Create a video translation workflow for Spanish and French"

"Set up webhooks for video completion notifications"
```

## API Reference

The rules are based on the HeyGen API documentation:
- Base URL: `https://api.heygen.com`
- Authentication: `X-Api-Key` header
- API Versions: v1, v2, v3 (varies by endpoint)

## Requirements

- HeyGen API key (Enterprise tier or higher recommended)
- Claude Code CLI

## Contributing

To add or update rules:

1. Edit the relevant `.md` file in `skills/heygen/rules/`
2. Ensure YAML frontmatter includes: `name`, `description`, `metadata.tags`
3. Include both curl and TypeScript/Python examples
4. Test that the skill loads correctly

## License

MIT

## Related Resources

- [HeyGen API Documentation](https://docs.heygen.com)
- [HeyGen Developer Portal](https://app.heygen.com/settings/api)
- [Claude Code Documentation](https://claude.ai/code)
