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

### Basic
```
"Make me a video about our new feature"

"I need a video explaining MCP to developers"

"Create a quick 30-second announcement about our new pricing"
```

### Specific
```
"Make a 60-second product demo about HeyGen's Video Agent API, aimed at developers, casual-confident tone"

"Create a 2-minute explainer about why AI agents need video capabilities, for a technical audience"

"Produce a sales pitch video for our enterprise clients, professional tone, 90 seconds"
```

### With assets
```
"Make a product demo using these screenshots of our dashboard" [attach files]

"Create an explainer video based on this PDF documentation" [attach PDF]

"I have a blog post at [URL] — turn it into a 60-second video summary"
```

### Quick generation
```
"Just generate this: A confident narrator explains the three key benefits of our API in 30 seconds"

"Quick video, don't ask questions: 60-second overview of HeyGen for developers"
```

### With avatar (requires heygen-avatar-designer)
```
"Make a 30-second intro video using my agent's avatar"

"Create a product demo with Adam as the presenter"

"First design my avatar, then use it to make a video introducing our team"
```

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
- OpenClaw, Claude Code, or any agent that reads SKILL.md files

## License

MIT
