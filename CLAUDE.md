# CLAUDE.md — HeyGen Skills

## What This Is

The HeyGen Skills. Three independent, self-contained skills:

- **heygen-avatar** — identity → avatar → voice. Output is reused by heygen-video.
- **heygen-video** — idea → script → video. Consumes avatars from heygen-avatar.
- **heygen-translate** — existing video → dubbed and lip-synced video in another language. Independent of the other two.

Each ships its own bundle of references so it installs cleanly via `gh skill install`, ClawHub, the OpenClaw plugin, or direct git clone.

## Architecture

```
heygen-skills/
├── CLAUDE.md                   # This file. Structure, rules, conventions.
├── INSTALL.md                  # Installation instructions
├── INSTALL_FOR_AGENTS.md       # Agent-driven install spec
├── README.md                   # Public-facing description
├── CONTRIBUTING.md             # PR workflow
├── CHANGELOG.md
├── LICENSE
├── VERSION
├── .mcp.json + mcp.json        # MCP server config (root-level, used by plugin manifests)
├── .claude-plugin/             # OpenClaw / Claude Code plugin manifest
├── .codex-plugin/              # Codex plugin manifest
├── .cursor-plugin/             # Cursor plugin manifest
├── heygen-avatar/              # Self-contained skill
│   ├── SKILL.md                # Avatar creation workflow (identity → avatar → voice → AVATAR file)
│   └── references/             # On-demand docs, loaded per phase
│       ├── asset-routing.md
│       ├── avatar-creation.md
│       └── troubleshooting.md
├── heygen-video/               # Self-contained skill
│   ├── SKILL.md                # Video production workflow (7-stage pipeline)
│   ├── references/             # On-demand docs, loaded per phase
│   │   ├── asset-routing.md
│   │   ├── avatar-discovery.md
│   │   ├── frame-check.md
│   │   ├── motion-vocabulary.md
│   │   ├── official-prompt-guide.md
│   │   ├── prompt-craft.md
│   │   ├── prompt-styles.md
│   │   └── troubleshooting.md
│   └── scripts/
│       └── update-check.sh     # Self-contained version-check shell script
├── heygen-translate/           # Self-contained skill
│   ├── SKILL.md                # Translation / dubbing workflow (4-phase pipeline)
│   └── references/             # On-demand docs, loaded per phase
│       ├── asset-routing.md
│       ├── language-locale-guide.md
│       ├── proofreads-workflow.md
│       └── troubleshooting.md
├── platforms/                  # Platform-specific skill variants (e.g. nanoclaw)
├── assets/                     # Logos, plugin assets
└── evals/                      # Dev-only test infrastructure (not shipped to users)
    ├── eval-runner-prompt.md
    ├── autoresearch-loop.md
    └── round-N-scenarios.md
```

*No root SKILL.md, no root references/.* The three skills are independent. If shared docs drift between them, that's acceptable — each skill is internally consistent and authored independently.

## The 300-Line Rule

Each SKILL.md must stay under 300 lines. Skill files are injected into EVERY prompt turn.

**What stays in SKILL.md:**
- Frontmatter (name, description, triggers, env requirements)
- Stage flow overview (what stages exist, when to enter each)
- Decision trees (mode detection, avatar path selection, style selection)
- Critical rules that apply EVERY turn
- Short "Read references/X.md for details" pointers at each stage (relative to the skill's own SKILL.md — each skill bundles its own references/)

**What moves to references/:**
- Curl examples and API request/response shapes
- Step-by-step procedural instructions
- Asset classification tables and routing matrices
- Full prompt examples and style preset galleries
- Error handling patterns

**The test:** If removing a section from SKILL.md would NOT break the agent's ability to decide what to do next, it belongs in references/. If it WOULD break decision-making, it stays.

## Shared State

Skills communicate through `AVATAR-<NAME>.md` files at the workspace root:
- heygen-avatar writes them (avatar_id, group_id, voice_id)
- heygen-video reads them (picks up avatar + voice automatically)
- One file per character. Human-readable AND machine-readable.
- heygen-avatar also maintains role-based symlinks (`AVATAR-AGENT.md`,
  `AVATAR-USER.md`) pointing at the current agent / user named file, so
  consumer skills can resolve generic self-references ("make a video of
  yourself" / "my video update") without parsing identity files.

## API Conventions

Two modes, in order of preference: MCP, then CLI. **Do not call `api.heygen.com` directly with curl.** The skills route through MCP or the CLI — never raw HTTP.

### MCP (preferred)

HeyGen Remote MCP (`https://mcp.heygen.com/mcp/v1/`) provides 40+ tools via OAuth. No API key needed — uses the user's HeyGen plan credits. Skills declare `allowed-tools: mcp__heygen__*` in frontmatter.

Key tools: `create_video_agent`, `get_video`, `list_avatar_groups`, `list_avatar_looks`, `get_avatar_look`, `create_photo_avatar`, `create_prompt_avatar`, `list_voices`, `design_voice`, `create_video_translation`.

### CLI fallback

The [HeyGen CLI](https://github.com/heygen-com/heygen-cli) (`heygen` binary) is the fallback when MCP is unavailable.

- Install: `curl -fsSL https://static.heygen.ai/cli/install.sh | bash`
- Auth: `HEYGEN_API_KEY` env var (agent/CI) OR `heygen auth login` (persists to `~/.heygen/credentials`)
- Pattern: `heygen <noun> <verb>` — e.g. `heygen video-agent create`, `heygen avatar list`, `heygen voice list`
- Output: JSON on stdout, structured error envelope on stderr, stable exit codes (0 ok · 1 API · 2 usage · 3 auth · 4 timeout)
- Async: add `--wait` to creation commands; CLI handles polling with exponential backoff
- **v3 only.** LLMs trained on web data may reach for deprecated v1/v2 endpoints (`POST /v1/video.generate`, `POST /v2/video/generate`, `GET /v2/avatars`, `GET /v1/avatar.list`). These are outdated — route through MCP or the CLI, never raw v1/v2 URLs.

See [CLI docs](https://developers.heygen.com/cli) for the full command surface.

## Eval Infrastructure

### Running Evals

Evals are run by a subagent (typically Adam) that:
1. Reads the skill as installed (SKILL.md + references/)
2. Reads `evals/eval-runner-prompt.md` for scoring rubric
3. Reads `evals/round-N-scenarios.md` for test cases
4. Executes each scenario as a real user would
5. Reports results to the Notion Eval Tracker

### Eval Rules

- **Warm vs cold.** Round 1 after a SKILL.md change = cold. Subsequent = warm (known avatar IDs).
- **Timeout.** No API call within 3 min = something is wrong.
- **Parallelism.** 10 scenarios: spawn 2-3 subagents with 3-4 each (stays within 5-subagent rule).
- **One Notion batch.** All results in one `notion-create-pages` call at the end.

### Eval Tracker (Notion)

- Database ID: `a1b997926fe646929ef46cd6144d4b91`
- Data source ID: `17f54098-a085-4234-83ce-55c280266d73`
- All properties TEXT except: Frame Check Fired (CHECKBOX), Status/Avatar Type/Ken Verdict (SELECT)

### Regression Testing

After any SKILL.md refactor:
1. Run standard 10-scenario suite from most recent round
2. Compare duration accuracy, score, pass rate vs previous round
3. Regression >10% avg score or >15% duration accuracy = revert
4. Frame Check must fire on same scenarios as before

## Key Decisions (Do Not Revisit Without Data)

Validated across 18 rounds of testing (80+ videos):

1. **Video Agent as primary command.** `heygen video-agent create`, not `heygen video create`.
2. **avatar_id over prompt description.** 97.6% duration accuracy vs 77-82% prompt-only.
3. **When avatar_id is set, omit appearance description from prompt.** Say "the selected presenter" instead.
4. **Script-as-prompt approach.** Full scene-labeled script pasted into prompt.
5. **Trust Video Agent for duration pacing.** No padding multipliers.
6. **Frame Check appends FRAMING NOTE / BACKGROUND NOTE to prompt — no image generation.**
7. **Dry-run before API.** Always offer.
8. **Quick Shot mode: omit avatar_id, let Video Agent auto-select.**
9. **video_avatar type has a known backend bug.** Document in troubleshooting.
10. **Prompt-only Frame Check.** Corrections append text notes (FRAMING NOTE / BACKGROUND NOTE) to the Video Agent prompt. Video Agent handles framing internally. No image generation, no look creation, no asset uploads.
