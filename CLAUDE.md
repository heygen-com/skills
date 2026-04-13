# CLAUDE.md

This repo contains Claude Code skills for the HeyGen AI video creation API. It is a multi-skill repository distributed via three channels: Claude Code plugin marketplace, Vercel skills.sh (`npx skills add`), and ClawHub.

## Project Structure

```
heygen-skills/
├── skills/
│   ├── create-video/                # Prompt-based video creation (Video Agent)
│   │   ├── SKILL.md                 # Skill manifest + workflow
│   │   └── references/              # Prompt optimizer, visual styles, etc.
│   ├── avatar-video/                # Precise avatar/scene video creation (v3 API)
│   │   ├── SKILL.md                 # Skill manifest + workflow
│   │   └── references/              # Avatars, voices, video-generation, etc.
│   ├── visual-style/                # Portable visual design systems
│   │   ├── SKILL.md                 # Skill manifest + workflow
│   │   └── references/              # Spec, connectors, extractors, gallery, templates
│   ├── heygen/                      # [DEPRECATED] Legacy combined skill
│   │   ├── SKILL.md                 # Deprecation notice + original content
│   │   └── references/              # Original reference docs
│   ├── ai-video-gen/                # AI video generation (VEO, Kling, Sora, etc.)
│   │   └── SKILL.md                 # Self-contained (Workflow Gateway v1 API)
│   ├── faceswap/                    # Face swap in videos
│   │   └── SKILL.md                 # Self-contained (Workflow Gateway v1 API)
│   ├── text-to-speech/              # Standalone TTS audio (v3 API)
│   │   └── SKILL.md                 # Self-contained (no references/)
│   ├── video-translate/             # Video translation & dubbing
│   │   └── SKILL.md                 # Self-contained (no references/)
│   ├── video-download/              # Download video/audio from URLs (yt-dlp)
│   │   └── SKILL.md                 # Self-contained, no API key needed
│   ├── video-edit/                  # Local video editing (ffmpeg)
│   │   ├── SKILL.md                 # Skill manifest + quick reference
│   │   └── references/              # Detailed operation recipes
│   └── video-understand/            # Local video understanding (ffmpeg + Whisper)
│       ├── SKILL.md                 # Skill manifest + CLI usage
│       ├── references/              # Output format docs
│       └── scripts/                 # Python script for extraction
├── .claude-plugin/
│   ├── plugin.json                  # Claude Code plugin manifest
│   └── marketplace.json             # Marketplace listing
├── .github/workflows/
│   └── publish-clawhub.yml          # CI: publishes all skills to ClawHub
├── README.md
└── CLAUDE.md                        # This file
```

## Skill Architecture

### Design Principles

1. **Each skill is self-contained.** No cross-skill dependencies. Skills must not reference files in sibling skill directories.
2. **Split by distinct user intent and output type.** A new skill is warranted when it has a different output type (audio vs video), different API surface, and can stand alone.
3. **Video creation is split by intent.** `create-video` covers prompt-based generation (Video Agent API, `POST /v3/video-agents`). `avatar-video` covers precise avatar/scene control (v3 API, `POST /v3/videos`). The legacy `heygen` skill is deprecated.
4. **`visual-style` is a design system skill.** It creates, extracts, and applies portable `visual-style.md` files. It does not require a HeyGen API key — it's a format/workflow skill with connectors for HeyGen, HTML slides, Figma, and paper.design.
5. **Smaller skills inline everything.** `text-to-speech` and `video-translate` have no `references/` directory — all content is in SKILL.md. Only split into references when SKILL.md would exceed ~500 lines.
6. **Auth is inlined per skill.** Each skill includes a brief authentication section rather than referencing a shared auth file.

### Naming Conventions

- **Skill directory names**: lowercase, hyphens (e.g., `text-to-speech`, `video-translate`)
- **Skill `name` in frontmatter**: matches directory name exactly
- **Generic names, not product-prefixed**: use `text-to-speech` not `heygen-tts`. The plugin namespace handles branding (`heygen:text-to-speech`).
- **ClawHub slugs**: match the skill name where possible (e.g., `video-agent`, `text-to-speech`, `video-translate`)

### SKILL.md Format

Every SKILL.md follows this structure:

```yaml
---
name: skill-name
description: |
  One-line summary. Use when: (1) first trigger, (2) second trigger, (3) etc.
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Skill Title

Brief intro paragraph.

## Authentication
(inline, 3-5 lines)

## Tool Selection
(MCP tools table if applicable)

## Default Workflow
(numbered steps)

## [API-specific sections]
(endpoints, request/response, TypeScript + Python examples)

## Best Practices
(numbered list)
```

### Description Guidelines

Descriptions must be **trigger-rich** — include explicit "Use when:" clauses with specific scenarios. This drives Claude's skill selection accuracy. Example:

```
Generate speech audio from text using HeyGen's Starfish TTS model. Use when: (1) Generating standalone speech audio files from text, (2) Converting text to speech with voice selection, speed, pitch, and emotion control, ...
```

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` following the format above
2. Include inline auth section (copy the 3-line pattern from an existing skill)
3. Include curl, TypeScript, and Python examples for each endpoint
4. Add the skill to the README.md skills table
5. Add a publish step in `.github/workflows/publish-clawhub.yml`
6. Update `.claude-plugin/plugin.json` description if the overall plugin scope changed
7. Do NOT add cross-references to other skills — each skill must stand alone

## Updating Existing Skills

- **API changes**: Update the affected SKILL.md and/or reference files. If a change affects auth or shared patterns, update it in EVERY skill that inlines it.
- **Adding a reference file**: For skills that already have a `references/` directory (`create-video`, `avatar-video`, `visual-style`, `video-edit`, `video-understand`). Add the file to `references/`, then add a link in the SKILL.md Reference Files section. The `heygen` skill is deprecated — do not add new reference files to it.
- **Smaller skills** (`text-to-speech`, `video-translate`): Edit SKILL.md directly. Only create a `references/` directory if SKILL.md would exceed ~500 lines.

## Distribution

Three channels, one repo:

| Channel | Mechanism | What it reads |
|---------|-----------|---------------|
| Claude Code plugins | `/plugin install heygen@heygen-skills` | `.claude-plugin/` manifests |
| Vercel skills.sh | `npx skills add heygen-com/skills` | `skills/*/SKILL.md` auto-discovery |
| ClawHub | CI publishes on merge to master | `.github/workflows/publish-clawhub.yml` |

## HeyGen API Conventions

- Base URL: `https://api.heygen.com`
- Auth header: `X-Api-Key: $HEYGEN_API_KEY`
- Response format: v3 uses `{ "data": T }` on success and `{ "error": { "code": string, "message": string } }` on error
- Video generation is async: generate returns `video_id`, poll `GET /v3/videos/{video_id}` for completion
- MCP tools (`mcp__heygen__*`) are preferred over direct API calls when available
