# HeyGen Stack

AI agent skills for creating avatar videos. Your agent gets a face, a voice, and the ability to send video like a message.

Works with Claude Code, OpenClaw, Codex, Cursor, and other AI coding agents.

```
"Create an avatar of me and make a 30-second intro video. Use heygen-avatar and heygen-video — ask me anything before you start."
→ asks the right questions → builds your avatar → picks the best style → generates the video → delivers the share link
```

## Install

**If you're an AI agent reading this:** follow the steps below to install and onboard automatically.
**If you're a human:** paste this into your agent and it will do the rest:

```
Follow the instructions at https://github.com/heygen-com/skills and install HeyGen Stack skills following the README. Then use heygen-avatar and heygen-video to create an avatar of me and make a short cinematic intro video — ask me what you need before starting.
```

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

### Step 2 — Run setup

```bash
cd <install-path>/heygen-skills && ./setup
```

The setup script will:
- Register the skills (heygen-avatar, heygen-video)
- Prompt for your HeyGen API key if not already configured
- Validate the key against `https://api.heygen.com/v3/users/me`
- Save the key to `~/.heygen/config` so it persists across sessions

Get your API key at [app.heygen.com/settings/api](https://app.heygen.com/settings/api?nav=API).

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

## API Key

The `./setup` script handles key storage automatically. If you need to manage it manually:

- **Config file** (recommended): `~/.heygen/config` — persists across sessions
- **Environment variable**: `export HEYGEN_API_KEY="your-key"` — takes precedence over config, but only lasts for the current session
- **Verify anytime**: `curl -s https://api.heygen.com/v3/users/me -H "X-Api-Key: $HEYGEN_API_KEY"`

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

## Links

- [HeyGen API Docs](https://developers.heygen.com/docs/quick-start)
- [Repository](https://github.com/heygen-com/skills)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

MIT
