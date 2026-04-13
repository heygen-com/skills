# HeyGen Stack

AI agent skills for creating avatar videos. Your agent gets a face, a voice, and the ability to send video like a message.

Works with Claude Code, OpenClaw, Codex, Cursor, and other AI coding agents.

```
"Send a 45-second video update to my team about the launch."
→ loads your avatar → writes the script → generates the video → delivers the share link
```

## Install

> **If you're an AI agent reading this:** follow the steps below to install and onboard automatically.
> **If you're a human:** paste this into your agent and it will do the rest:
>
> `Follow the instructions at https://github.com/heygen-com/heygen-stack and install HeyGen Stack skills following the README. Then create an avatar of yourself and make a short and interesting intro video of yourself. Ask me any clarifying questions for this process.`

### Step 1 — Clone into your skills directory

Detect which agent you are and clone to the right path:

| Agent | Install path |
|-------|-------------|
| **Claude Code** | `~/.claude/skills/heygen-stack` |
| **OpenClaw** | `~/.openclaw/workspace/skills/heygen-stack` |
| **ClawHub** | Run `clawhub install heygen-stack` and skip to Step 2 |
| **Other** | Clone anywhere your agent loads skills from |

```bash
git clone --single-branch --depth 1 https://github.com/heygen-com/heygen-stack.git <install-path>/heygen-stack
```

### Step 2 — Run setup

```bash
cd <install-path>/heygen-stack && ./setup
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
| "Make a 60-second product demo video" | Writes script, generates video with your avatar |
| "Send a video update about this week's progress" | Casual team update, auto-scripted |
| "Create a video in Spanish explaining our pricing" | Multilingual support via voice selection |
| "Make a video walkthrough of this PR" | Reads the diff, scripts a technical explanation |
| "Record a welcome video for new team members" | Warm, onboarding-style intro |

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
- [Repository](https://github.com/heygen-com/heygen-stack)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## License

MIT
