# heygen-video-producer

Your AI video producer. Tell it what you need, it handles the rest.

Turns ideas into polished HeyGen narrator videos through an intelligent production pipeline — scripting, prompt engineering, quality review, generation, and delivery.

## Install

```bash
# ClawHub
clawhub install heygen-video-producer

# Or manually
git clone https://github.com/heygen-com/heygen-video-producer.git
cp -r heygen-video-producer ~/.openclaw/skills/
```

## Setup

Requires a [HeyGen API key](https://app.heygen.com/settings/api). Set it as an environment variable:

```bash
# In your openclaw.json
{
  "env": {
    "vars": {
      "HEYGEN_API_KEY": "your-api-key"
    }
  }
}
```

Or configure via OpenClaw skills config:

```bash
# In your openclaw.json
{
  "skills": {
    "entries": {
      "heygen-video-producer": {
        "apiKey": "your-api-key"
      }
    }
  }
}
```

## Usage

Just ask your agent to make a video:

- "Make me a 60-second product demo about our new API"
- "I need a video explaining MCP to developers"
- "Create a quick announcement about our new pricing"

The skill handles everything: interviewing you for details, writing a narrator script, engineering the optimal prompt, reviewing it for quality, and generating the video.

## How It Works

**Three modes:**

| You provide | Mode | What happens |
|-------------|------|-------------|
| An idea | Full Producer | Interviews you → writes script → engineers prompt → reviews → generates |
| A prompt | Enhanced Prompt | Optimizes your prompt with best practices → reviews → generates |
| "Just generate this" | Quick Shot | Generates directly → still reviews output |

**Five-phase pipeline:**

1. **Discovery** — Conversational interview (not a form)
2. **Script** — Narrator-optimized script with 150 wpm pacing
3. **Prompt Engineering** — Scene-by-scene structure, visual style, media types
4. **Quality Review** — Independent sub-agent reviews the prompt before generation
5. **Generate & Deliver** — Video Agent API call, live progress tracking, delivery

## What Makes It Different

This isn't an API wrapper. It's a production pipeline that encodes video expertise:

- **150 words/min pacing rule** — scripts are always timed correctly
- **Scene-by-scene prompting** — not flat paragraphs, structured scenes with Visual + VO + Duration
- **Visual style enforcement** — consistent look across all scenes
- **Media type intelligence** — motion graphics for data, stock for real environments, AI-generated for concepts
- **Independent quality gate** — a separate model reviews the prompt before generation
- **One-shot optimization** — maximizes success on the first API call

## API

Uses [HeyGen Video Agent](https://docs.heygen.com) (`POST /v1/video_agent/generate`). Cost: 2 credits per minute of generated video.

## Requirements

- `HEYGEN_API_KEY` environment variable
- `curl` and `jq` (for shell scripts)
- OpenClaw, Claude Code, or any agent that reads SKILL.md files

## License

MIT
