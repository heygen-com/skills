# Install HeyGen Stack

Get your API key from [app.heygen.com/settings](https://app.heygen.com/settings/api?nav=API).

## Option 1 — ClawHub (recommended)

```bash
clawhub install heygen-stack
```

## Option 2 — Git clone

**OpenClaw:**
```bash
git clone https://github.com/heygen-com/heygen-stack.git ~/.openclaw/workspace/skills/heygen-stack
```

**Claude Code:**
```bash
git clone https://github.com/heygen-com/heygen-stack.git ~/.claude/skills/heygen-stack
```

## First Run

Paste the following prompt to your agent:

> My HeyGen API key is `[HEYGEN_API_KEY]`. Save it to your persistent environment config and validate it works by calling `GET https://api.heygen.com/v3/user/me` with header `X-Api-Key`. Then create an avatar for yourself using the heygen-identity skill and make a video introducing yourself, 30-60 seconds, casual tone.
