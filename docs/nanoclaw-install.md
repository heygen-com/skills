# HeyGen Stack — NanoClaw Install

## Install

Copy the NanoClaw container skill into your NanoClaw fork:

```bash
# From the heygen-skills repo root
cp -r platforms/nanoclaw/heygen/ /path/to/your-nanoclaw-fork/container/skills/heygen/
```

Or clone and copy:

```bash
git clone https://github.com/heygen-com/skills.git
cp -r skills/platforms/nanoclaw/heygen/ /path/to/your-nanoclaw-fork/container/skills/heygen/
```

## Required Environment

Set `HEYGEN_API_KEY` in your NanoClaw container environment:

```bash
export HEYGEN_API_KEY="your-api-key-here"
```

Get your key from [app.heygen.com/settings/api](https://app.heygen.com/settings?nav=API).

## What Gets Installed

A single `SKILL.md` file at `container/skills/heygen/SKILL.md` that teaches the container agent to:

1. Discover available avatars and voices via the HeyGen API
2. Write spoken-word scripts optimized for avatar delivery
3. Generate videos via `POST /v3/video-agents`
4. Poll for completion via `GET /v3/video-agents/sessions/{session_id}`
5. Download and deliver the finished MP4

## Usage

The container agent will automatically pick up the skill. Ask it to:

- "Make a video introducing our product"
- "Create a 30-second video pitch"
- "Record a video update for the team"

## More Info

- HeyGen API docs: https://developers.heygen.com/docs/quick-start
- Full skill repo: https://github.com/heygen-com/skills
