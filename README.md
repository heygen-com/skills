# heygen-video-producer

Your AI video producer. Tell it what you need, it handles the rest.

Turns ideas into polished HeyGen narrator videos through an intelligent production pipeline — scripting, prompt engineering, avatar selection, quality review, and delivery.

## Why This Exists

HeyGen's [Video Agent](https://developers.heygen.com/docs/quick-start) is powerful but one-shot. The quality of the output is 100% determined by the quality of the input prompt. Most users write flat paragraphs that produce generic, forgettable videos.

This skill sits between you and the API like a senior video producer. It interviews you, writes a script, engineers an optimized prompt with scene structure and visual direction, selects the right avatar, handles aspect ratio corrections, attaches your assets, and delivers a finished video.

**Without this skill:** 60s target → 36s actual. Flat prompt. No visual direction. Generic result.

**With this skill:** 60s target → ~55s actual. Scene-structured prompt with style blocks, narrator framing, media types, and avatar matched by ID.

## Quick Start

### One-paste install

Open [INSTALL.md](./INSTALL.md), copy the prompt below the line, and paste it into your agent (OpenClaw, Claude Code, Codex, or any SKILL.md-compatible agent). The agent will install the skill, walk you through API key setup, validate everything, and ask what video to make. One paste, zero config files.

### Manual install

```bash
clawhub install heygen-video-producer
```

Or clone directly:

```bash
git clone https://github.com/heygen-com/heygen-video-producer.git ~/.openclaw/skills/heygen-video-producer
```

Then just say "make me a video" — the skill will prompt you for your API key if it's not already set.

### Try it

```
"Make me a 60-second video about our new API"
"Create a product demo using these screenshots" [attach files]
"Quick video: 30-second overview of our pricing changes"
"Turn this blog post into a video: https://example.com/post"
```

## How It Works

### Three Modes

| You say | Mode | What happens |
|---------|------|-------------|
| An idea or topic | **Producer** | Interviews → scripts → prompt engineers → generates |
| A written prompt | **Enhanced Prompt** | Optimizes your prompt → generates |
| "Just generate this" | **Quick Shot** | Generates directly, no interview |

Add **"dry run"** to any request to preview the full prompt without spending API credits.

### Five-Phase Pipeline

```
Discovery → Script → Prompt Engineering → Generate → Deliver
```

1. **Discovery** — Conversational interview. Captures topic, audience, tone, duration, assets. Adapts depth to complexity.
2. **Script** — Scene-by-scene structure with script framing directive. Video Agent handles pacing and duration internally.
3. **Prompt Engineering** — Visual style blocks, media type direction, narrator framing. Scene labels with VO + visual + media type per scene.
4. **Generate** — Submits to `POST /v3/video-agents` with avatar_id, voice selection, and asset attachments. Polls for completion.
5. **Deliver** — Session URL immediately (for interactive follow-up), video URL on completion, duration accuracy report.

### Avatar Selection

The skill discovers and selects avatars through the HeyGen API, not by describing them in the prompt:

- **Custom avatars** — looks up by name, passes `avatar_id` to the API
- **Stock avatars** — browses avatar groups with preview images, selects by ID
- **Voice-over only** — no avatar, narration only

**Important:** when `avatar_id` is set, the prompt never describes the avatar's appearance. Video Agent ignores the `avatar_id` parameter if the prompt text describes a different-looking person. The prompt only includes delivery style and background/environment notes.

### Asset Handling

The skill classifies every URL and file attachment:

| Asset type | What happens |
|-----------|-------------|
| Direct file URL (PDF, image) | Downloads → uploads via `/v3/assets` → passes `asset_id` |
| HTML page (blog, docs) | Fetches content → summarizes → adds context to prompt |
| Attached file | Uploads to HeyGen → referenced in prompt |
| Auth-walled URL | Checks access, notifies user if inaccessible — never fabricates content |

### Aspect Ratio Corrections (Phase 3.5)

Before submitting, the skill checks for avatar/video orientation mismatches:

- Portrait avatar in landscape video → injects reframing correction
- Studio avatar with transparent background → triggers generative fill
- Landscape avatar in portrait video → adjusts framing notes

Correction prompts use explicit trigger phrases that Video Agent recognizes and executes.

## What Makes It Different

This isn't an API wrapper. It encodes video production expertise:

- **Duration intelligence** — script framing directive tells Video Agent to treat the script as a concept to convey, not verbatim speech
- **Scene-by-scene prompting** — structured scenes with Visual + VO + media type, not flat paragraphs
- **Visual style enforcement** — style blocks with colors, fonts, media type guidance, and HeyGen's curated style presets (from their official prompt guide)
- **Avatar-by-ID** — explicit `avatar_id` for ~97% duration accuracy vs ~80% with auto-selection
- **One-shot optimization** — all best practices applied before generation. No wasted credits.
- **Learning loop** — logs every generation to `heygen-video-producer-log.jsonl` with duration accuracy, settings, and self-evaluation scores
- **Media type direction** — guides Video Agent on when to use motion graphics vs AI-generated vs stock footage per scene
- **Multi-language** — supports any language HeyGen offers: "Create a 60-second demo narrated in Brazilian Portuguese"

## Why Direct API (Not MCP)

This skill uses HeyGen's REST API directly instead of their [MCP server](https://github.com/HeyGen-Official/heygen-mcp). Here's why:

**The MCP server covers ~15% of the API.** It exposes 6 tools: credits, voices (capped at 100), avatar groups, avatars in group, generate video, and check status. That's it.

**We need endpoints MCP doesn't have:**

| What we need | API endpoint | In MCP? |
|-------------|-------------|---------|
| Video Agent (prompt-driven) | `POST /v3/video-agents` | ❌ |
| Style browsing | `GET /v3/video-agents/styles` | ❌ |
| Asset upload | `POST /v3/assets` | ❌ |
| Avatar looks with group filtering | `GET /v3/avatars/looks` | ❌ |
| Voice previews with signed URLs | `GET /v3/voices` | ❌ (capped at 100) |
| Interactive sessions | `POST /v3/video-agents/sessions` | ❌ |

The MCP's `generate_avatar_video` wraps the old v2 scene-by-scene API, not the Video Agent. Different endpoint, different capabilities.

**No extra dependencies.** Direct API is just HTTPS with an API key. No Python process, no `uvx`, no MCP client required. The skill works anywhere that can make HTTP calls.

**When MCP would make sense:** If HeyGen ships a v3 MCP server that wraps Video Agent, styles, and assets, the transport difference becomes irrelevant. The prompt quality is still the critical factor regardless of how you call the API. We'd revisit then.

## API

All endpoints are **v3**. Base URL: `https://api.heygen.com`

| Endpoint | Purpose |
|----------|---------|
| `POST /v3/video-agents` | Primary — prompt-driven video generation |
| `GET /v3/videos/{id}` | Poll for completion |
| `GET /v3/avatars/looks` | Avatar discovery (with group filtering) |
| `GET /v3/voices` | Voice listing with preview URLs |
| `GET /v3/video-agents/styles` | Style browsing with tag filtering |
| `POST /v3/assets` | Upload files for attachment |
| `POST /v3/videos` | Direct control path (avatar videos) |

## Evaluation

The skill includes a multi-round autoresearch evaluation framework:

```
evals/
├── eval-runner-prompt.md     # Eval runner instructions + scoring rubric
├── autoresearch-loop.md      # Loop infrastructure docs
├── dry-run.md                # 8 dry-run prompt quality scenarios
├── run-eval.md               # How to run prompt quality evals
├── round-{2..7}-scenarios.md # Per-round test scenarios
└── test-prompts.json         # Baseline prompts from batch test
```

Run a dry-run eval (no API credits):
```
Read evals/run-eval.md and follow instructions
```

Run a full autoresearch round:
```
Read evals/eval-runner-prompt.md and the latest round-N-scenarios.md
```

Results are tracked in the [Eval Tracker](https://www.notion.so/a1b997926fe646929ef46cd6144d4b91) Notion database with per-scenario scoring, video/session URLs, and human verdicts.

## Known Issues

| Issue | Status | Workaround |
|-------|--------|------------|
| `video_avatar` type fails with "Talking Photo not found" | HeyGen backend bug, fix in progress | Use `studio_avatar` or `photo_avatar` instead |
| Duration variance (±20%) | Expected — Video Agent controls final timing | Script framing directive helps; variance is inherent |
| Interactive sessions stuck at `processing` | Backlogged | Use one-shot mode |
| `files[]` URL attachment blocked by CDN/WAF | Known limitation | Download → upload → `asset_id` (primary path) |

## Requirements

- `HEYGEN_API_KEY` environment variable
- OpenClaw, Claude Code, or any agent that reads SKILL.md files

## Links

- [HeyGen API Docs](https://developers.heygen.com/docs/quick-start)
- [Video Agent Prompt Guide](https://www.heygen.com/blog/video-agent-prompt-guide)
- [HeyGen Remote MCP Server](https://mcp.heygen.com)

## License

MIT
