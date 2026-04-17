# HeyGen Skills

AI agent skills for creating avatar videos. Your agent gets a face, a voice, and the ability to send video like a message.

Works with Claude Code, OpenClaw, Codex, Cursor, and other AI coding agents.

```
"Create an avatar of me and make a 30-second intro video. Use heygen-avatar and heygen-video — ask me anything before you start."
→ asks the right questions → builds your avatar → picks the best style → generates the video → delivers the share link
```

## Install

Paste this into your agent to get started:

```
Install HeyGen Skills from https://github.com/heygen-com/skills — clone the repo into your skills directory and run ./setup. Then use heygen-avatar and heygen-video to create an avatar of me and make a short cinematic intro video. Ask me what you need before starting.
```

Or follow the steps below manually.

### Step 1 — Clone into your skills directory

Detect which agent you are and clone to the right path:

| Agent | Install path |
|-------|-------------|
| **Claude Code** | `~/.claude/skills/heygen-skills` |
| **OpenClaw** | `~/.openclaw/workspace/skills/heygen-skills` |
| **ClawHub** | Run `clawhub install heygen-skills` and skip to Step 2 |
| **Other** | Clone anywhere your agent loads skills from |

```bash
git clone --single-branch --depth 1 https://github.com/heygen-com/skills.git <install-path>/heygen-skills
```

### Step 2 — Connect to HeyGen (pick one)

The skills auto-detect which mode is available and prefer MCP when connected.

**Option A — MCP (recommended, no API key needed)**

Connect HeyGen's remote MCP server to your agent. OAuth handles auth and the skills use your existing HeyGen plan credits — no separate API billing.

Claude Code:
```bash
claude mcp add --transport http heygen https://mcp.heygen.com/mcp/v1/
```

OpenClaw: add to `~/.openclaw/openclaw.json`:
```json
{
  "mcp": {
    "servers": {
      "heygen": { "url": "https://mcp.heygen.com/mcp/v1/" }
    }
  }
}
```

The first call triggers an OAuth consent flow in your browser.

**Option B — API key (CLI fallback)**

If MCP is unavailable or you prefer direct API access:

```bash
cd <install-path>/heygen-skills && ./setup
```

The setup script will:
- Register the skills (heygen-avatar, heygen-video)
- Prompt for your HeyGen API key if not already configured
- Validate the key against `https://api.heygen.com/v3/users/me`
- Save the key to `~/.heygen/config` so it persists across sessions

Get your API key at [app.heygen.com/settings/api](https://app.heygen.com/settings/api?nav=API).

> **Either path works.** The skills detect MCP tools matching `mcp__heygen__*` and use them first. If none are found, they fall back to curl + `X-Api-Key`. You can have both configured — MCP wins.

### Step 3 — Create your avatar

Ask the user for a photo (URL or file), then use the **heygen-avatar** skill:

> Create my HeyGen avatar from this photo: [user's photo]

The skill uploads the photo, creates a persistent digital twin with a voice, and saves an `AVATAR-<NAME>.md` file for future use.

### Step 4 — Make your first video

Use the **heygen-video** skill to generate an intro video with the avatar you just created:

> Make a 30-60 second video of me introducing myself, casual tone.

The skill picks up the avatar automatically, writes a script, generates the video, and returns a share link.

**That's it. You're set up.** The avatar persists — every future video reuses it automatically.

---

## What's Included

Two skills that work standalone or chain together:

| Skill | What it does | Invoke |
|-------|-------------|--------|
| **heygen-avatar** | Photo → persistent digital twin (face + voice). Reusable across every video. | `/heygen-avatar` |
| **heygen-video** | Idea → script → prompt-engineered video with your avatar delivering the message. | `/heygen-video` |

**heygen-avatar** creates the identity. **heygen-video** uses it.

## How It Works

```
Photo / Description          Avatar File              Finished Video
       ↓                        ↓                        ↓
  heygen-avatar    →    AVATAR-NAME.md       →    heygen-video
  (identity + voice)    (reusable state)          (script + video)
```

Skills communicate through `AVATAR-<NAME>.md` files. heygen-avatar writes them, heygen-video reads them. Human-readable and machine-readable.

## Authentication

The skills support two auth modes and auto-detect which is available.

### MCP (preferred)

When HeyGen's remote MCP server is connected to your agent, the skills use it automatically. No API key needed, OAuth handles everything, and calls use your existing HeyGen plan credits.

- Endpoint: `https://mcp.heygen.com/mcp/v1/`
- Tool namespace: `mcp__heygen__*`
- [MCP docs](https://developers.heygen.com/docs/mcp-remote)

### API key (CLI fallback)

If MCP isn't available, the skills fall back to direct curl calls with `X-Api-Key`. The `./setup` script handles key storage automatically. To manage it manually:

- **Config file** (recommended): `~/.heygen/config` — persists across sessions
- **Environment variable**: `export HEYGEN_API_KEY="your-key"` — takes precedence over config, lasts the session
- **Verify anytime**: `curl -s https://api.heygen.com/v3/users/me -H "X-Api-Key: $HEYGEN_API_KEY"`

You can have both configured — the skills check for MCP first and only fall back to CLI if MCP tools aren't visible.

## Things to Try

After setup, try these prompts with your agent:

| Prompt | What happens |
|--------|-------------|
| "Use heygen-avatar and heygen-video to make a 30-second cinematic intro of me as a founder. Ask me what you need." | Full pipeline: avatar → style recommendation → video. The wow moment. |
| "I want to make a product launch video. Use heygen-video and suggest the best style for it." | Skill recommends from 20 curated styles (A24, editorial, clean tech, etc.) |
| "Use heygen-avatar — I have a headshot. What kind of look would work best for a founder intro?" | Skill asks questions, recommends setting and tone before creating |
| "Use heygen-video to summarize this article as a 60-second explainer from my avatar: [URL]" | Fetches content, extracts key points, scripts and generates the video |
| "Use heygen-video to turn the key points from this PDF into a video update for my team: [file]" | PDF → script → avatar video. Any content becomes a video message. |
| "Use heygen-video for my team's weekly update. Ask me what shipped before writing the script." | Skill interviews you first, then writes and generates |
| "Use heygen-video to make a 20-second outreach video to a potential investor. What should I include?" | Skill guides the message, you approve the script, avatar delivers it |
| "Use heygen-avatar to give me a new look — ask me what vibe I'm going for." | Discovery flow: skill suggests options (outdoor, studio, casual, cinematic) before committing |

## Requirements

- A HeyGen API key ([get one here](https://app.heygen.com/settings/api?nav=API))
- An AI agent that supports skills (Claude Code, OpenClaw, Codex, Cursor, or similar)
- No runtime dependencies. No packages. No build step.

## Security

One optional shell script:

- **`scripts/update-check.sh`** — compares your local `VERSION` against the latest on GitHub. Read-only, opt-in, no data transmitted.

Data only leaves your machine to `api.heygen.com` (video generation) and optionally `raw.githubusercontent.com` (version check).

## Looking for the v1 skills?

The previous version of this repo had individual skills for TTS, video translation, faceswap, video editing, and more. Those skills are preserved at [heygen-com/skills-legacy](https://github.com/heygen-com/skills-legacy).

## Links

- [HeyGen API Docs](https://developers.heygen.com/docs/quick-start)
- [Repository](https://github.com/heygen-com/skills)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

MIT
