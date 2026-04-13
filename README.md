# HeyGen Stack

AI agent skills for creating avatar videos. Your agent gets a face, a voice, and the ability to send video like a message.

One install. One API key. Works with Claude Code, OpenClaw, Codex, and other AI coding agents.

```
"Send a 45-second video update to my team about the launch."
→ loads your avatar → writes the script → generates the video → delivers the share link
```

## Quick Start

**30-second setup.** Paste this into your agent:

> Install HeyGen Stack: run `git clone --single-branch --depth 1 https://github.com/heygen-com/heygen-stack.git ~/.claude/skills/heygen-stack && cd ~/.claude/skills/heygen-stack && ./setup` — the setup script will prompt for your API key and save it to `~/.heygen/config`. After setup, use the heygen-avatar skill to create an avatar from my photo, and heygen-video to make a 30-60 second intro video, casual tone.

Get your API key at [app.heygen.com/settings/api](https://app.heygen.com/settings/api?nav=API).

## What's Included

Two skills that work standalone or chain together:

| Skill | What it does | Invoke |
|-------|-------------|--------|
| **heygen-avatar** | Photo → persistent digital twin (face + voice). Reusable across every video. | `/heygen:avatar` |
| **heygen-video** | Idea → script → prompt-engineered video with your avatar delivering the message. | `/heygen:video` |

**heygen-avatar** creates the identity. **heygen-video** uses it. Chain them or use independently.

## Install

### Claude Code

```bash
git clone https://github.com/heygen-com/heygen-stack.git ~/.claude/skills/heygen-stack
cd ~/.claude/skills/heygen-stack && ./setup
```

### OpenClaw

```bash
git clone https://github.com/heygen-com/heygen-stack.git ~/.openclaw/workspace/skills/heygen-stack
cd ~/.openclaw/workspace/skills/heygen-stack && ./setup
```

### ClawHub

```bash
clawhub install heygen-stack
```

### Other agents

Clone the repo anywhere. Point your agent's skill/instruction loader at the `SKILL.md` files:
- `SKILL.md` (root router)
- `heygen-avatar/SKILL.md` (avatar creation)
- `heygen-video/SKILL.md` (video production)

## API Key Setup

The `./setup` script handles everything: it prompts for your key, validates it, and saves it to `~/.heygen/config` so it persists across terminal sessions.

1. Go to [app.heygen.com/settings/api](https://app.heygen.com/settings/api?nav=API)
2. Copy your API key
3. Run `./setup` — it will ask for the key and save it automatically

**Already have a key saved?** The setup script and all skills check `~/.heygen/config` automatically. No need to `export` every session.

**Manual override:** You can still use `export HEYGEN_API_KEY="your-key-here"` — the env var takes precedence over the config file. This is useful for temporary key switching but won't persist.

Verify your key anytime:

```bash
curl -s https://api.heygen.com/v3/users/me -H "X-Api-Key: $HEYGEN_API_KEY" | head -c 200
```

## Verify It Works

After setup, ask your agent:

> Create my HeyGen avatar from this photo: [paste a URL or upload a file]

The agent should upload the photo, create your avatar, ask about voice preferences, and save an `AVATAR-*.md` file. Then:

> Make a 30-second video of me introducing myself, casual tone.

## How It Works

```
Photo / Description          Avatar File              Finished Video
       ↓                        ↓                        ↓
  heygen-avatar    →    AVATAR-NAME.md       →    heygen-video
  (identity + voice)    (reusable state)          (script + video)
```

Skills communicate through `AVATAR-<NAME>.md` files. heygen-avatar writes them, heygen-video reads them. Human-readable and machine-readable.

## Requirements

- A HeyGen API key ([get one here](https://app.heygen.com/settings/api?nav=API))
- An AI agent that supports skills/instructions (Claude Code, OpenClaw, Codex, or similar)
- No runtime dependencies. No packages. No build step.

## Security

One optional shell script in `scripts/`:

- **`scripts/update-check.sh`** — compares your local `VERSION` against the latest on GitHub. Read-only, opt-in, no data transmitted.

Data only leaves your machine to `api.heygen.com` (video generation) and optionally `raw.githubusercontent.com` (version check).

## Links

- [HeyGen API Docs](https://developers.heygen.com/docs/quick-start)
- [Repository](https://github.com/heygen-com/heygen-stack)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

MIT
