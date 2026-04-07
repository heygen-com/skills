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

Get your API key from [app.heygen.com/settings](https://app.heygen.com/settings/api?nav=API). Then copy and paste the following prompt to your agent:

> Install the HeyGen Stack skill: `git clone https://github.com/heygen-com/heygen-stack.git` into your skills directory (OpenClaw: `~/.openclaw/skills/heygen-stack`, Claude Code: `~/.claude/skills/heygen-stack`). My HeyGen API key is `[HEYGEN_API_KEY]`. Save it to your persistent environment config and validate it works by calling `GET https://api.heygen.com/v3/user/me` with header `X-Api-Key`. Then use the avatar-designer skill to create an avatar of me from this photo: [PHOTO_URL]. Once the avatar is ready, make a 30-second video of me introducing myself, casual tone.

## What's Inside

Two skills that work standalone or chain together:

### avatar-designer
Create a persistent digital identity — your face, your voice — for use across every video you make.

- Reads identity files (`SOUL.md`, `IDENTITY.md`) or asks conversationally
- Creates a HeyGen avatar with matched voice
- Saves to `AVATAR-<NAME>.md` for automatic reuse across videos
- Returns `avatar_id` + `voice_id` — pass directly to video-producer

```
You: "I want to appear in videos as myself"
Agent: [uploads your photo, creates avatar, matches voice]
Agent: → AVATAR-YOU.md (avatar_id + voice_id, reusable forever)
```

### video-producer
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

When both skills are installed, video-producer automatically picks up avatars created by avatar-designer.

## How It Works

```
Identity Files              Avatar File              Finished Video
(SOUL.md, IDENTITY.md)  →  AVATAR-NAME.md       →  Share link + session URL
       ↓                        ↓                        ↓
  avatar-designer          shared state            video-producer
```

Each skill works independently. You don't need an avatar to make a video (stock avatars work), and you don't need to make videos to use the avatar designer.

## Architecture

```
heygen-stack/
├── SKILL.md                     # Main skill: video production pipeline
├── avatar-designer/
│   └── SKILL.md                 # Avatar creation and voice matching
├── references/                  # On-demand deep docs (loaded per-phase, not every turn)
│   ├── api-reference.md         # Endpoints, polling, interactive sessions, webhooks
│   ├── asset-routing.md         # File upload, URL handling, content-type rules
│   ├── avatar-discovery.md      # Avatar browsing, creation, voice selection
│   ├── frame-check.md           # Aspect ratio correction logic
│   ├── prompt-craft.md          # Advanced prompt construction
│   ├── prompt-styles.md         # Named style presets (Cinematic, Swiss Pulse, etc.)
│   ├── motion-vocabulary.md     # Camera movement and transition vocabulary
│   ├── official-prompt-guide.md # HeyGen's internal prompt research
│   └── troubleshooting.md       # Known issues and workarounds
├── evals/                       # Evaluation infrastructure
│   ├── eval-runner-prompt.md    # Scoring rubric for automated testing
│   └── autoresearch-loop.md     # Eval methodology documentation
├── CLAUDE.md                    # Agent architecture guide
├── INSTALL.md                   # Copy-paste install instructions
├── CONTRIBUTING.md              # PR workflow
└── LICENSE                      # MIT
```

**Token-conscious design.** The main SKILL.md is under 300 lines (~3K tokens/turn). Reference docs are loaded on-demand per phase, not injected every turn. This matters when your agent has limited context.

## Eval Methodology

This skill was developed using an **autoresearch loop** — a human-supervised automated evaluation process inspired by [Karpathy's methodology](https://x.com/karpathy):

1. Define 10 test scenarios per round (product demos, explainers, tutorials, edge cases)
2. Agent executes each scenario as a real user would
3. Human reviews generated videos and scores on duration accuracy, visual quality, prompt adherence
4. Issues classified P0–P3, fixes applied to SKILL.md
5. Next round validates fixes and tests for regressions

Video success rate improved from 6/10 to 10/10. SKILL.md went from 57KB to 12.8KB (78% token reduction) with zero functional regressions.

Bugs caught that you won't hit:
- Avatar ID + prompt text conflicts (avatar appearance described in prompt overrides the actual avatar)
- Frame Check silent failures (correction prompts missing explicit tool trigger phrases)
- 365% duration overshoots on short videos (script freedom directive missing)
- CDN-protected URLs causing silent content fabrication
- Square avatars letterboxing with black bars (style-adaptive generative fill added)

Full eval history: [`evals/autoresearch-loop.md`](evals/autoresearch-loop.md)

## API

v3 only. All requests go to `https://api.heygen.com` with `X-Api-Key` header auth.

Key endpoints used:
| Endpoint | Purpose |
|----------|---------|
| `POST /v3/video-agents` | Primary video generation (prompt-driven) |
| `GET /v3/videos/{id}` | Poll status, get share URL |
| `POST /v3/avatars` | Create avatars and looks |
| `GET /v3/avatars` | Browse avatar inventory |
| `GET /v3/voices` | Voice listing and selection |
| `POST /v3/assets` | File uploads for video assets |
| `GET /v3/video-agents/styles` | Browse curated visual styles |

Full API reference: [`references/api-reference.md`](references/api-reference.md)

## Requirements

- A HeyGen API key ([get one here](https://app.heygen.com/settings/api?nav=API))
- An AI agent that supports skills/instructions (OpenClaw, Claude Code, Codex, or similar)
- That's it. No runtime dependencies, no packages to install, no build step.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All changes go through pull requests with required review.

## License

MIT
