# CLAUDE.md — HeyGen Skills

## What This Is

The HeyGen Skills. Two skills that chain together: **heygen-avatar** (identity → avatar → voice) and **heygen-video** (idea → script → video). SKILL.md at root routes between them.

## Architecture

```
heygen-skills/
├── SKILL.md                    # Router: detects intent, dispatches to sub-skill
├── CLAUDE.md                   # This file. Structure, rules, conventions.
├── INSTALL.md                  # Installation instructions
├── README.md                   # Public-facing description
├── CONTRIBUTING.md             # PR workflow
├── LICENSE
├── heygen-avatar/
│   └── SKILL.md                # Avatar creation workflow (identity → avatar → voice → AVATAR file)
├── heygen-video/
│   └── SKILL.md                # Video production workflow (7-stage pipeline)
├── references/                 # Shared. Loaded on-demand by phase (NOT every turn)
│   ├── avatar-discovery.md     # Discovery: avatar lookup, voice selection, curl examples
│   ├── asset-routing.md        # Discovery: asset classification engine, upload flows
│   ├── prompt-styles.md        # Prompt Craft: 6 prompt style templates
│   ├── motion-vocabulary.md    # Prompt Craft: camera/transition vocabulary
│   ├── prompt-craft.md         # Prompt Craft: prompt construction deep-dive
│   ├── official-prompt-guide.md# Prompt Craft: HeyGen's own prompt research
│   ├── frame-check.md          # Frame Check: aspect ratio correction prompts
│   ├── troubleshooting.md      # Known issues, workarounds, duration variance
│   └── reviewer-prompt.md      # Deliver: self-evaluation rubric
└── evals/                      # Dev-only test infrastructure (not shipped to users)
    ├── eval-runner-prompt.md   # Instructions for eval subagent
    ├── autoresearch-loop.md    # Loop methodology docs
    └── round-N-scenarios.md    # Per-round test scenarios
```

## The 300-Line Rule

Each SKILL.md must stay under 300 lines. Skill files are injected into EVERY prompt turn.

**What stays in SKILL.md:**
- Frontmatter (name, description, triggers, env requirements)
- Stage flow overview (what stages exist, when to enter each)
- Decision trees (mode detection, avatar path selection, style selection)
- Critical rules that apply EVERY turn
- Short "Read ../references/X.md for details" pointers at each stage

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
