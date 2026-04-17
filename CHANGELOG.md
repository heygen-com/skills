# Changelog

## [2.1.0](https://github.com/heygen-com/skills/compare/v2.0.3...v2.1.0) (2026-04-17)


### Features

* MCP-first API mode with CLI fallback ([#47](https://github.com/heygen-com/skills/issues/47)) ([4b052ae](https://github.com/heygen-com/skills/commit/4b052aee846589c0aefb861191fc6285d8c95c4e))


### Bug Fixes

* remove prompt injection triggers from README ([#44](https://github.com/heygen-com/skills/issues/44)) ([94981e0](https://github.com/heygen-com/skills/commit/94981e042429e2c6b4c3aebd72cf2dfbdcffd958))

## v1.3.7 (2026-04-13) — Auto-Proceed Fix

### Fixed
- **Video Agent review checkpoint** — The HeyGen v3 Video Agent API supports an `auto_proceed` flag in the request body. This skill documents passing `"auto_proceed": true` as a server-side API parameter that tells the HeyGen backend to skip its own internal review checkpoint — it is not granting the agent discretion to submit jobs unilaterally. The agent still requires the user to initiate a video generation request before any API call is made; no video jobs are submitted autonomously.
- **Batch submission throttle** — Capped parallel video submissions at 2–3 max to prevent queue congestion.
- Simplified polling status flow: `thinking → generating → completed` (no checkpoint approval step)

---

## v1.3.2 (2026-04-11) — Multi-Platform Distribution

### Added
- **Claude Code Marketplace** — Submission docs with plugin metadata, skill listing, and install instructions (`docs/claude-code-submission.md`)
- **Hermes Agent support** — `hermes` metadata block in root SKILL.md frontmatter (tags + category) and install guide (`docs/hermes-install.md`)
- **Manus support** — Import workflow docs (`docs/manus-install.md`)
- **NanoClaw container skill** — Compact 112-line SKILL.md at `platforms/nanoclaw/heygen/SKILL.md` covering avatar discovery, voice selection, script writing, v3 video generation, polling, and delivery
- **NanoClaw install guide** — `docs/nanoclaw-install.md`

### Fixed
- Synced `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` version from 1.2.7 → 1.3.2

---

## v1.3.0 (2026-04-10) — i18n Support

### Added
- **Language Detection** — Skills detect user's language from input and communicate in that language
- **Language-aware voice selection** — Voice API calls filter by detected language; `voice_settings.locale` guidance added
- **Non-English script generation** — Scripts and narration generated in the video language
- **i18n eval suite** — Test scenarios across English, Japanese, Spanish, Korean with scoring rubric
- **Japanese example prompt** in prompt-craft reference
- **Language consistency criterion** (#11) in reviewer prompt

### Changed
- Mode Detection is now explicitly language-agnostic (semantic intent matching, not English keyword matching)
- User-facing messages converted from hardcoded English strings to semantic descriptions the LLM adapts to user's language
- Buddy voice construction pattern uses `{video_language}` instead of hardcoded "English"
- Buddy sign-off lines converted to semantic descriptions instead of English idioms
- Test video prompt (Phase 5) generates greeting in video language instead of hardcoded English

### Documentation
- Added `> Language note` callouts to motion-vocabulary.md and prompt-styles.md explaining English-only directives
- Updated api-reference.md with `voice_settings.locale` guidance and language filter examples
- All reference files document the content-language vs directive-language separation

---

## v1.2.7 (2026-04-09)

### Bug Fixes
- Synced version numbers across all files (SKILL.md frontmatter, User-Agent headers, plugin.json, marketplace.json) to match VERSION file
- Fixed Quick Shot avatar_id rule in heygen-video to use AVATAR file when available instead of always omitting
- Completed Frame Check correction matrix with Aspect Ratio column and ratio-fix corrections (F, G) across root SKILL.md and frame-check.md
- Fixed frame-check.md correction stacking matrix: removed stale 4-column header, corrected intro sentence (photo_avatar never gets background correction C)
- Replaced macOS-incompatible `readlink -f` in heygen-video preamble with POSIX-compatible path resolution

### Architecture
- Trimmed root SKILL.md from 399 to ~215 lines by extracting duplicated Script, Prompt Craft, and Generate content into the producer sub-skill where it belongs
- Fixed stale path reference: `identity/SKILL.md` -> `heygen-avatar/SKILL.md`
- Registered buddy-to-avatar skill in marketplace.json

### Documentation
- Added buddy-to-avatar to README "What's Inside" section

## v1.1.0 (2026-04-06)

### heygen-video
- Prompt-only Frame Check architecture (no external image generation, preserves face identity)
- submit-video.sh wrapper enforces aspect ratio checks before every API call
- Phase naming overhaul: action verbs replace numbered phases (Discovery, Script, Prompt Craft, Frame Check, Generate, Deliver)
- Style-adaptive Phase 3.5: 3D, animated, and photorealistic avatars get matching fill directives
- ATO lane carving: distinct tool descriptions for agent discoverability vs built-in video_generate
- Version check system with cache TTLs and snooze backoff
- Inline MP4 delivery (downloads video, sends as media attachment)
- Hard gates at all user decision points

### heygen-avatar
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
