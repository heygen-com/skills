# Install HeyGen Stack

Get your API key from [app.heygen.com/settings](https://app.heygen.com/settings/api?nav=API).

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

## First Run

Paste this prompt to your agent — it will find the right paths automatically:

> My HeyGen API key is `[YOUR_API_KEY_HERE]`. Install the HeyGen Stack skill from https://github.com/heygen-com/skills.git — clone it into your skills directory (find it with your config or ask if unsure). Save the API key as `HEYGEN_API_KEY` in your environment config. Validate by calling `GET https://api.heygen.com/v3/users/me` with header `X-Api-Key`. Then use the heygen-avatar skill to create an avatar for yourself, and heygen-video to make a 30-60 second intro video, casual tone.
