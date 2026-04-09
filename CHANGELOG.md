# Changelog

## v1.1.0 (2026-04-06)

### heygen-video-producer
- Prompt-only Frame Check architecture (no external image generation, preserves face identity)
- submit-video.sh wrapper enforces aspect ratio checks before every API call
- Phase naming overhaul: action verbs replace numbered phases (Discovery, Script, Prompt Craft, Frame Check, Generate, Deliver)
- Style-adaptive Phase 3.5: 3D, animated, and photorealistic avatars get matching fill directives
- ATO lane carving: distinct tool descriptions for agent discoverability vs built-in video_generate
- Version check system with cache TTLs and snooze backoff
- Inline MP4 delivery (downloads video, sends as media attachment)
- Hard gates at all user decision points

### heygen-avatar-designer
- Voice Design endpoint (POST /v3/voices) with semantic search, seed pagination
- Reference photo nudge on first-time avatar creation
- Inline audio previews for voice selection
- Hard gates: voice selection and avatar approval require explicit user confirmation
- UX Rules: interactive at checkpoints, silent everywhere else
- Moved into heygen-stack monorepo

### Infrastructure
- submit-video.sh: auto-validates avatar dimensions, appends FRAMING NOTE if mismatch detected
- update-check script moved from bin/ to scripts/
- Branch protection: 1 approval required, CODEOWNERS enforced
- README trimmed to essentials (Quick Start, What's Inside, How It Works)

## v1.0.0 (2026-04-01)

Initial release. Five-phase video production pipeline with avatar discovery, prompt engineering, aspect ratio corrections, and HeyGen Video Agent API integration. 22 eval rounds, 80+ test videos generated.
