# Changelog

## [2.2.1](https://github.com/heygen-com/skills/compare/v2.2.0...v2.2.1) (2026-04-27)


### Bug Fixes

* **install:** make avatar creation a first-class install step ([#71](https://github.com/heygen-com/skills/issues/71)) ([64ab640](https://github.com/heygen-com/skills/commit/64ab6404a3c2d0c7f32b55e2decf5de511c75f9e))

## [2.2.0](https://github.com/heygen-com/skills/compare/v2.1.2...v2.2.0) (2026-04-27)


### Features

* add Codex and Cursor plugin manifests ([#65](https://github.com/heygen-com/skills/issues/65)) ([df9458c](https://github.com/heygen-com/skills/commit/df9458cc3543eb0fbda4b32822886eaba6234380))
* INSTALL_FOR_AGENTS.md + 2-line paste-prompt install ([#68](https://github.com/heygen-com/skills/issues/68)) ([d58fa24](https://github.com/heygen-com/skills/commit/d58fa2411601cd97385c04f3bae9c0f087cbcc4a))
* route video generation through @heygen/openclaw-plugin-heygen when available ([#67](https://github.com/heygen-com/skills/issues/67)) ([a2526d0](https://github.com/heygen-com/skills/commit/a2526d0c5bdb91860882e0cbdadb326edfb41145))

## [2.1.2](https://github.com/heygen-com/skills/compare/v2.1.1...v2.1.2) (2026-04-17)


### Bug Fixes

* **frame-check:** specify AI Image tool for generative fill ([#62](https://github.com/heygen-com/skills/issues/62)) ([af77568](https://github.com/heygen-com/skills/commit/af77568e3f7c6fd76144869a05f8b20fb8639fec))

## [2.1.1](https://github.com/heygen-com/skills/compare/v2.1.0...v2.1.1) (2026-04-17)


### Bug Fixes

* **heygen-avatar:** agent-first default + prompt-based as primary path ([#55](https://github.com/heygen-com/skills/issues/55)) ([57c319b](https://github.com/heygen-com/skills/commit/57c319b656ffa8b88ea7ce6f85d49be30e27e927))
* **heygen-avatar:** Before You Start ran user-centric logic before Phase 0 ([#56](https://github.com/heygen-com/skills/issues/56)) ([0c1e9d3](https://github.com/heygen-com/skills/commit/0c1e9d38b96247fbd124966f85760e3b652ec18e))
* prevent batch-asking and fix agent onboarding flow ([#51](https://github.com/heygen-com/skills/issues/51)) ([e5e5db3](https://github.com/heygen-com/skills/commit/e5e5db358ada7429d1f1f2a51a232e4cfc5c763e))
* remove api-reference.md, enforce MCP xor CLI (no cross-lookup) ([#59](https://github.com/heygen-com/skills/issues/59)) ([75f1ee3](https://github.com/heygen-com/skills/commit/75f1ee3556ac051834a90914a6e2cf96ca6f46ef))
* silent mode detection, no CLI-broken narration ([#54](https://github.com/heygen-com/skills/issues/54)) ([ff7b6a3](https://github.com/heygen-com/skills/commit/ff7b6a32ffbd533b56f0aa8c040f78eef09500fd))
* **SKILL:** add UX rules against narrating skill internals, next-action, and transport choice ([#58](https://github.com/heygen-com/skills/issues/58)) ([3e8b06d](https://github.com/heygen-com/skills/commit/3e8b06df38538245596588909d4404b1eb850f1d))
* **SKILL:** HEYGEN_API_KEY presence → use CLI, short-circuit MCP ([#60](https://github.com/heygen-com/skills/issues/60)) ([808dd77](https://github.com/heygen-com/skills/commit/808dd776fc5c3f19b905f549a4a6c1ee46a2a656))

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
