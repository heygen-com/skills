# Install HeyGen Skills

Sign in via MCP (OAuth, no key needed) — or grab an [API key](https://app.heygen.com/settings/api?nav=API) if you'll use the CLI fallback.

## Option 1 — ClawHub (recommended)

```bash
clawhub install heygen-skills
```

ClawHub installs to your agent's default skills directory automatically.

## Option 2 — Git clone

Clone into your agent's skills directory:

**OpenClaw** (default: `~/.openclaw/skills/heygen-skills`, custom installs may differ — check your config):
```bash
git clone https://github.com/heygen-com/skills.git ~/.openclaw/skills/heygen-skills
```

**Claude Code** (default: `~/.claude/skills/heygen-skills`):
```bash
git clone https://github.com/heygen-com/skills.git ~/.claude/skills/heygen-skills
```

> Not sure where your skills directory is? Ask your agent: *"Where is your skills directory?"*

## Auth

Two options — the skills prefer MCP when it's available:

**MCP (recommended, no API key needed):** connect HeyGen's remote MCP server to your agent — OAuth handles auth. See README for agent-specific setup.

**HeyGen CLI (fallback):** install the CLI and authenticate:
```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash
heygen --version        # verify binary is on PATH
heygen auth login       # persists to ~/.heygen/credentials
# OR
export HEYGEN_API_KEY=<your-key>
heygen auth status      # verify auth
```

## First Run

Paste this prompt to your agent — it will find the right paths automatically:

> Install the HeyGen Skills from https://github.com/heygen-com/skills.git — clone it into your skills directory (find it with your config or ask if unsure). If MCP isn't connected, install the HeyGen CLI via `curl -fsSL https://static.heygen.ai/cli/install.sh | bash` and run `heygen auth login`. Then use the heygen-avatar skill to create an avatar for me, and heygen-video to make a 30-60 second intro video, casual tone.
