# HeyGen Stack

https://github.com/user-attachments/assets/ac2eef90-5356-4f45-a780-26dc44b294f9

Give your AI agent the ability to create videos featuring real people — and send them like messages.

**heygen-stack** is an AI skill for identity-first and messaging-first video. Your agent can create a persistent digital avatar of you (or anyone), then produce videos where that person delivers a message — personalized outreach, team updates, announcements, pitches, explainers. One install. One API key.

```
"Send a video message to my leads introducing our new feature."
```
→ Create your avatar → Write the message → Generate the video → Deliver the link

Two angles, one category:
- **Identity-first:** photo → avatar → voice → video. Your face, your voice, every video.
- **Messaging-first:** video as the new message — outreach, updates, pitches, knowledge, announcements.

## Quick Start

Get your API key from [app.heygen.com/settings](https://app.heygen.com/settings/api?nav=API).

**Option 1 — ClawHub (recommended):**
```bash
clawhub install heygen-stack
```

**Option 2 — Git clone:**
```bash
# OpenClaw
git clone https://github.com/heygen-com/heygen-stack.git ~/.openclaw/workspace/skills/heygen-stack

# Claude Code
git clone https://github.com/heygen-com/heygen-stack.git ~/.claude/skills/heygen-stack
```

Then copy and paste the following prompt to your agent:

> My HeyGen API key is `[HEYGEN_API_KEY]`. Save it to your persistent environment config and validate it works by calling `GET https://api.heygen.com/v3/users/me` with header `X-Api-Key`. Then use the heygen-avatar skill to create an avatar of me from this photo: [PHOTO_URL]. Once the avatar is ready, make a 30-second video of me introducing myself, casual tone.

## What's Inside

Two skills that work standalone or chain together:

### heygen-avatar
Create a persistent digital identity — your face, your voice — for use across every video you make.

- Reads identity files (`SOUL.md`, `IDENTITY.md`) or asks conversationally
- Creates a HeyGen avatar with matched voice
- Saves to `AVATAR-<NAME>.md` for automatic reuse across videos
- Returns `avatar_id` + `voice_id` — pass directly to heygen-video

```
You: "I want to appear in videos as myself"
Agent: [uploads your photo, creates avatar, matches voice]
Agent: → AVATAR-YOU.md (avatar_id + voice_id, reusable forever)
```

### heygen-video
Send a video as yourself — personalized, presenter-led, delivered like a message.

Use cases: personalized outreach, team updates, product announcements, pitches, knowledge transfer, explainers.

- **Discovery** — interviews you about purpose, audience, tone, duration
- **Script** — structures content by message type (outreach, update, announcement, pitch, explainer)
- **Prompt Craft** — transforms script into an optimized Video Agent prompt with style blocks and visual direction
- **Frame Check** — detects avatar orientation mismatches and applies generative fill (no black bars, ever)
- **Generate & Deliver** — submits to HeyGen API, polls, delivers share link with duration accuracy report

```
You: "Send a 45-second video update to my team about the launch"
Agent: [loads your avatar, asks 2 smart questions]
Agent: [writes the message, shows you for approval]
Agent: [generates video with your face, delivers share link]
```

### buddy-to-avatar
Bring your Claude Code Buddy to life as a HeyGen avatar and intro video.

- Reads your terminal pet's species, stats, rarity, and personality
- Maps buddy traits to avatar appearance, voice, and visual style
- Chains through heygen-avatar and heygen-video automatically
- Produces a personalized stat-reveal intro video

```
You: "Bring my buddy to life"
Agent: [reads buddy card, maps species to appearance]
Agent: [creates avatar, matches voice to personality stats]
Agent: -> 30-second intro video with stat reveals
```

When all three skills are installed, they chain automatically: buddy-to-avatar -> heygen-avatar -> heygen-video.

## How It Works

```
Identity Files              Avatar File              Finished Video
(SOUL.md, IDENTITY.md)  →  AVATAR-NAME.md       →  Share link + session URL
       ↓                        ↓                        ↓
  heygen-avatar          shared state            heygen-video
```

Each skill works independently. You don't need an avatar to make a video (stock avatars work), and you don't need to make videos to use the avatar designer.

## Requirements

- A HeyGen API key ([get one here](https://app.heygen.com/settings/api?nav=API))
- An AI agent that supports skills/instructions (OpenClaw, Claude Code, Codex, or similar)
- That's it. No runtime dependencies, no packages to install, no build step.

## Security & Scripts

This skill includes one shell script in `scripts/`:

- **`scripts/update-check.sh`** — checks `raw.githubusercontent.com/heygen-com/heygen-stack/main/VERSION` against your local VERSION file. Read-only. No data transmitted. Run manually with `bash scripts/update-check.sh` if you want a version check.

The script does not run automatically. The update check is opt-in only.

The skill reads and writes `AVATAR-<NAME>.md` files in your workspace. No data leaves your machine except to `api.heygen.com` (video generation) and `raw.githubusercontent.com` (version check, opt-in).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All changes go through pull requests with required review.

## License

MIT
