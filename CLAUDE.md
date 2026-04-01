# CLAUDE.md — heygen-video-producer

## What This Skill Does

Turns a user's idea into a polished HeyGen narrator video through an intelligent 5-phase production pipeline. The skill IS the missing interaction layer between the user and HeyGen's one-shot Video Agent API.

## Architecture

```
heygen-video-producer/
├── SKILL.md                    # Decision logic + phase flow (~300 lines target)
├── CLAUDE.md                   # This file. Repo rules, structure, contribution guide.
├── INSTALL.md                  # Installation instructions
├── README.md                   # Public-facing description
├── CONTRIBUTING.md             # PR workflow
├── references/                 # Loaded on-demand by phase (NOT every turn)
│   ├── avatar-discovery.md     # Phase 1: avatar lookup, voice selection, curl examples
│   ├── asset-routing.md        # Phase 1: asset classification engine, upload flows
│   ├── prompt-styles.md        # Phase 3: 6 prompt style templates (exists)
│   ├── motion-vocabulary.md    # Phase 3: camera/transition vocabulary (exists)
│   ├── prompt-craft.md         # Phase 3: prompt construction deep-dive (exists)
│   ├── official-prompt-guide.md# Phase 3: HeyGen's own prompt research (exists)
│   ├── phase-3-5.md            # Phase 3.5: aspect ratio correction logic + examples
│   ├── api-reference.md        # Phase 4: endpoints, polling, interactive sessions, errors
│   ├── troubleshooting.md      # Known issues, workarounds, duration variance
│   └── reviewer-prompt.md      # Phase 5: self-evaluation rubric (exists)
└── evals/                      # Test infrastructure (never loaded into skill context)
    ├── eval-runner-prompt.md    # Instructions for eval subagent
    ├── autoresearch-loop.md    # Loop methodology docs
    ├── round-N-scenarios.md    # Per-round test scenarios
    └── results/                # Round results and transcripts
```

## The 500-Line Rule

SKILL.md must stay under 300 lines. It is injected into EVERY prompt turn. At 1,192 lines (57KB), the original SKILL.md burned ~15K tokens of context before the agent read the user's message. Current: ~288 lines, ~12.8KB. Exceeding 300 lines causes:
- Slow first response (agent processes 57KB before acting)
- Wasted tokens on phases irrelevant to the current turn
- Eval subagents spending 3+ minutes just reading before making an API call

**What stays in SKILL.md:**
- Frontmatter (name, description, triggers, env requirements)
- Phase flow overview (what phases exist, when to enter each)
- Decision trees (mode detection, avatar path selection, style selection)
- Critical rules that apply EVERY turn (voice rules, orientation, style guidance)
- Short "Read references/X.md for details" pointers at each phase

**What moves to references/:**
- Curl examples and API request/response shapes
- Step-by-step procedural instructions (avatar lookup flow, Phase 3.5 steps)
- Asset classification tables and routing matrices
- Full prompt examples and style preset galleries
- Interactive session docs, webhook registration, video management
- Known issues and troubleshooting
- Error handling patterns

**The test:** If removing a section from SKILL.md would NOT break the agent's ability to decide what to do next, it belongs in references/. If it WOULD break decision-making, it stays.

## Design Principles

1. **SKILL.md = decision brain. references/ = execution details.** The skill file tells the agent WHAT to do and WHEN. Reference files tell it HOW, loaded only when needed.

2. **One phase, one reference file.** Don't make the agent read avatar-discovery.md during Phase 4 generation. Each reference maps to a phase.

3. **Self-contained skill.** No cross-skill dependencies. No references to files outside this directory. Auth is inlined.

4. **Trigger-rich description.** The frontmatter description drives skill selection. Include explicit "Use when:" clauses with specific scenarios.

5. **Evals are not skill content.** Nothing in evals/ should be referenced by SKILL.md. Evals test the skill; they don't define it.

6. **Learning log is append-only.** The skill writes findings to `heygen-video-producer-log.jsonl` in the user's workspace. This is the skill's long-term memory across sessions.

## API Conventions

- Base URL: `https://api.heygen.com`
- Auth header: `X-Api-Key: $HEYGEN_API_KEY`
- Primary endpoint: `POST /v3/video-agents` (Video Agent, prompt-driven)
- Secondary endpoint: `POST /v3/videos` (direct control, avatar_id required)
- All v3 endpoints. No v1 or v2 fallbacks.
- Response format: `{ "error": null | string, "data": T }`
- Video generation is async: returns `video_id` + `session_id`, poll `GET /v3/videos/{video_id}`
- Pricing: see HeyGen docs (changes frequently, not hardcoded in skill)

## Eval Infrastructure

### Running Evals

Evals are run by a subagent (typically Adam) that:
1. Reads the skill as installed (SKILL.md + references/)
2. Reads `evals/eval-runner-prompt.md` for scoring rubric
3. Reads `evals/round-N-scenarios.md` for test cases
4. Executes each scenario as a real user would
5. Reports results to the Notion Eval Tracker

### Eval Rules

- **Warm mode vs cold mode.** Round 1 for any SKILL.md change = cold (full install test). Subsequent rounds = warm (known avatar IDs, skip discovery).
- **Pre-baked context.** For warm evals, provide known avatar_id, voice_id, and group_id in the scenario file to skip 3+ minutes of discovery overhead.
- **Timeout.** If no API call within 3 minutes, something is wrong. Steer the subagent.
- **Parallelism.** For 10 scenarios: spawn 2-3 subagents with 3-4 scenarios each (stays within 5-subagent rule, cuts wall clock 3x).
- **One Notion batch.** All results written in one `notion-create-pages` call at the end, not per-scenario.

### Eval Tracker (Notion)

- Database ID: `a1b997926fe646929ef46cd6144d4b91`
- Data source ID: `17f54098-a085-4234-83ce-55c280266d73`
- All properties are TEXT type except: Phase 3.5 Fired (CHECKBOX), Status/Avatar Type/Ken Verdict (SELECT)

### Regression Testing

After any SKILL.md refactor:
1. Run the standard 10-scenario suite from the most recent round
2. Compare duration accuracy, score distribution, and pass rate against the previous round
3. Any regression >10% in average score or >15% in duration accuracy = revert
4. Phase 3.5 must fire on the same scenarios it fired on before
5. No new "stuck pending" scenarios that weren't stuck before

## Git Workflow

- `main` branch is the published skill
- Feature branches for changes: `refactor/slim-skill`, `fix/avatar-lookup`, etc.
- PRs require: description of what changed, which phase affected, whether evals needed
- Commit messages: `phase-N: description` or `refs: description` or `evals: description`
- Tag releases: `v0.N.0` for skill versions

## Key Decisions (Do Not Revisit Without Data)

These were validated across 9 rounds of testing (80+ videos):

1. **Video Agent as primary endpoint.** POST /v3/video-agents, not /v3/videos. Prompt-driven, not parameter-driven.
2. **avatar_id over prompt description.** Passing avatar_id achieves 97.6% duration accuracy vs 77-82% prompt-only.
3. **When avatar_id is set, omit appearance description from prompt.** Say "the selected presenter" instead. Avoids Video Agent ignoring avatar_id.
4. **Script-as-prompt approach.** Full scene-labeled script pasted into prompt for one-shot generation.
5. **Trust Video Agent for duration pacing.** No padding multipliers — the API has no structured duration enforcement. State target duration in prompt and let the agent interpret.
6. **Phase 3.5 correction prompts need explicit "Use AI Image tool to generative fill" trigger.** Without it, Video Agent ignores correction directives.
7. **Dry-run before API.** Always offer. Shows narrative pitch format before spending credits.
8. **Quick Shot mode: omit avatar_id, let Video Agent auto-select.** Reduces friction for casual use.
9. **video_avatar type has a known backend bug.** Narrator tags fail to resolve. Not a skill issue; document in troubleshooting.
