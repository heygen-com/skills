# heygen-video-producer

Your AI video producer. Tell it what you need, it handles the rest.

Turns ideas into polished HeyGen narrator videos through an intelligent production pipeline — scripting, prompt engineering, quality review, generation, and delivery.

## The Problem

Video Agent is powerful but one-shot. The quality of the output is 100% determined by the quality of the input prompt. Most users write flat paragraphs that produce generic, forgettable videos. This skill sits between you and the API like a senior video producer — it interviews, writes, crafts, reviews, and delivers.

**Without this skill:** 60s target → 36s actual. Flat prompt. No visual direction. Generic result.
**With this skill:** 60s target → ~55s actual. Scene-structured prompt with style blocks, media types, narrator framing, and independent quality review.

## Install

```bash
# ClawHub
clawhub install heygen-video-producer

# Or manually
git clone https://github.com/heygen-com/heygen-video-producer.git
cp -r heygen-video-producer ~/.openclaw/skills/
```

## Setup

Requires a [HeyGen API key](https://app.heygen.com/settings/api):

```json
{
  "env": {
    "vars": {
      "HEYGEN_API_KEY": "your-api-key"
    }
  }
}
```

## Usage

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
"I have a blog post at https://example.com — turn it into a 60-second video summary"
```

### Quick generation
```
"Just generate this: A confident narrator explains the three key benefits of our API in 30 seconds"
"Quick video, don't ask questions: 60-second overview of HeyGen for developers"
```

### Multi-language
```
"Create a 60-second product demo narrated in Brazilian Portuguese"
"Make a Japanese explainer about our API for the Tokyo team"
```

## How It Works

**Three modes:**

| You provide | Mode | What happens |
|-------------|------|-------------|
| An idea | Full Producer | Interviews → scripts → engineers prompt → reviews → generates |
| A prompt | Enhanced Prompt | Optimizes your prompt → reviews → generates |
| "Just generate this" | Quick Shot | Generates directly, no review, maximum speed |

**Production pipeline:**

1. **Discovery** — Conversational interview (adapts, doesn't interrogate)
2. **Script** — Narrator-optimized, 150 wpm pacing, 1.4x duration padding
3. **Prompt Engineering** — Scene-by-scene structure, visual style, media types
4. **Generate** — Video Agent API with asset attachments
5. **Deliver** — Session URL immediately, video URL on completion, status tracking

## What Makes It Different

This isn't an API wrapper. It's encoded video production expertise:

- **Duration intelligence** — compensates for Video Agent's ~70% compression with 1.4x padding. You ask for 60s, you get ~60s.
- **Scene-by-scene prompting** — not flat paragraphs. Structured scenes with Visual + VO + media type per scene.
- **Visual style enforcement** — style blocks with colors, fonts, and presets (minimalistic, cinematic, bold, etc.)
- **Media type matrix** — automatically picks motion graphics for data, stock for real environments, AI-generated for concepts.
- **One-shot optimization** — all best practices applied before generation. No wasted credits on bad prompts.
- **Asset handling** — uploads all attachments to HeyGen, describes how each should be used in the video.
- **Learning loop** — logs every generation to `heygen-video-producer-log.jsonl`. Reads past results to improve future videos.
- **Completion status** — DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT after every generation.

## Evaluation

Run prompt quality evals without spending credits:

```
# Dry-run: test prompt quality against 8 baselines
Read evals/run-eval.md and follow instructions

# Compare two eval runs
Read evals/compare.md and follow instructions
```

Baselines from batch test (March 24, 2026) in `evals/test-prompts.json`.

## API

Uses [HeyGen Video Agent](https://docs.heygen.com) (`POST /v1/video_agent/generate`). Cost: 2 credits per minute of generated video.

## Requirements

- `HEYGEN_API_KEY` environment variable
- OpenClaw, Claude Code, or any agent that reads SKILL.md files

## Inspired By

- [gstack](https://github.com/garrytan/gstack) — Skills that encode process and judgment, not just tool access
- [HeyGen Video Agent Prompt Guide](https://www.heygen.com/blog/video-agent-prompt-guide) — Official best practices

## License

MIT
