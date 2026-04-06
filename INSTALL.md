# Install HeyGen Stack

Get your API key from [app.heygen.com/settings/api](https://app.heygen.com/settings/api). Then copy and paste the following prompt to your agent:

> Install the HeyGen Stack skill: `git clone https://github.com/heygen-com/heygen-stack.git` into your skills directory (OpenClaw: `~/.openclaw/skills/heygen-stack`, Claude Code: `~/.claude/skills/heygen-stack`). My HeyGen API key is `[HEYGEN_API_KEY]`. Save it to your persistent environment config and validate it works by calling `GET https://api.heygen.com/v3/user/me` with header `X-Api-Key`. Then create a video introducing yourself, 30-60 seconds, casual tone.
