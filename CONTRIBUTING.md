# Contributing to heygen-stack

## Git Workflow

All changes go through pull requests. No direct pushes to `main`.

### For every change:

```bash
# 1. Create a branch from main
git checkout main && git pull
git checkout -b <type>/<short-description>
# e.g. feat/multi-language-support, fix/duration-padding, refactor/avatar-flow

# 2. Make changes, commit with clear messages
git add -A
git commit -m "Short summary of what changed

- Bullet points explaining WHY, not just what
- Reference any eval results or test outputs
- Note any breaking changes to the skill interface"

# 3. Push and create PR
git push -u origin <branch-name>
gh pr create --title "Short summary" --body "$(cat <<'EOF'
## What

[One paragraph: what this PR does]

## Why

[One paragraph: why this change is needed]

## Changes

- [Bullet list of specific changes]

## Testing

- [ ] Dry-run tested (paste output or describe scenario)
- [ ] Full generation tested (video_id if applicable)
- [ ] SKILL.md reads clean end-to-end
- [ ] No spec-sheet language leaked into user-facing output

## Breaking changes

[None / describe what breaks]
EOF
)"
```

### Branch naming

| Prefix | Use for |
|--------|---------|
| `feat/` | New capability (new mode, new phase, asset handling) |
| `fix/` | Bug fix (duration math, API error handling) |
| `refactor/` | Internal cleanup (no behavior change) |
| `docs/` | README, CONTRIBUTING, eval docs only |
| `eval/` | New eval scenarios or test infrastructure |

### PR review checklist

Before merging, confirm:

1. **One pipeline** — dry-run and full generation share identical logic through prompt construction. No forked code paths.
2. **Creative, not clinical** — user-facing output reads like a pitch, not a form submission. No timestamps, no Settings blocks, no padding math.
3. **SKILL.md is the source of truth** — if behavior changed, SKILL.md reflects it. An agent reading only SKILL.md can execute the full skill correctly.
4. **Evals updated** — if the change affects prompt quality or output format, add or update scenarios in `evals/`.
5. **Commit messages explain why** — not just "updated SKILL.md".

### After merge

```bash
git checkout main && git pull
git branch -d <branch-name>
```

**NEVER reuse a merged or closed branch.** New work = new branch off main. Don't push additional commits to a branch whose PR was already merged or closed.

### Eve's workflow (for autonomous changes)

When Eve updates the skill without Ken online:
1. Create branch, commit, push, open PR
2. Post PR link to Ken on Telegram
3. Wait for review before merging
4. Never push directly to main

---

## How We Test: The Autoresearch Loop

This skill was built through 20 rounds of automated evaluation, producing 80+ videos. The methodology is inspired by Karpathy's autoresearch concept: define scenarios, run them blind, classify failures, fix the skill, repeat.

### The Loop

```
┌──────────────────────────────────────────────────────┐
│  1. DESIGN — Write 10 test scenarios                 │
│     Each has: user prompt, expected behavior,        │
│     avatar config, target duration, what to watch    │
├──────────────────────────────────────────────────────┤
│  2. EXECUTE — Fresh agent runs all 10 blind          │
│     No prior context. Only reads SKILL.md.           │
│     Logs: video_id, payload, duration, corrections   │
├──────────────────────────────────────────────────────┤
│  3. EVALUATE — Score each scenario 1-10              │
│     Write results to tracking database (Notion)      │
│     Classify issues: P0 (broken) → P3 (cosmetic)    │
├──────────────────────────────────────────────────────┤
│  4. FIX — Address P0/P1 findings in SKILL.md         │
│     Open PR with findings → fixes mapping            │
│     Human reviews videos + diffs before merge        │
├──────────────────────────────────────────────────────┤
│  5. REPEAT — Next round targets regressions +        │
│     new edge cases. Each round builds on the last.   │
└──────────────────────────────────────────────────────┘
```

### Why This Works

**The tester agent reads only SKILL.md.** No tribal knowledge, no chat history, no "you know what I mean." If the skill file doesn't say it clearly, the agent gets it wrong. This surfaces documentation gaps that human review misses.

**Scenarios escalate.** Early rounds test happy paths ("make a 30s product demo"). Later rounds push boundaries: square avatars, style_id combinations, 90-second long-form, Quick Shot mode, prompt-based framing corrections.

**Fixes are surgical.** Each round produces a branch, a PR, and a clear mapping from finding to fix. No rewrites unless the architecture is wrong.

### What We Learned (R1–R20)

| Finding | Round | Impact |
|---------|-------|--------|
| SKILL.md at 57KB consumed ~15K tokens/turn | R10 | Refactored to 259 lines (78% reduction) |
| avatar_id + appearance text in prompt conflict | R7 | Narrator framing rule: omit appearance when avatar_id set |
| Frame Check corrections not appended to prompt | R3 | Added explicit correction note templates |
| Timestamps per scene make delivery robotic | R8 | Switched to natural flow + tone description |
| 365% duration overshoot on short videos | R12 | Script framing directive added |
| Square (1:1) avatars letterboxed with black bars | R18 | Square detection + correction blocks D/E |
| External image gen in Frame Check degraded face identity | R20 | Reverted to prompt-only approach — Video Agent handles framing internally |

### Running Your Own Evals

The `evals/` directory (gitignored, not shipped) contains our scenario files and runner prompt. To run your own:

1. Create `evals/round-N-scenarios.md` with 10 scenarios
2. Each scenario needs: user prompt, avatar config, target duration, orientation, what to watch for
3. Have a fresh agent (no prior context) read SKILL.md and execute all 10
4. Score results, classify issues, fix SKILL.md, open PR
5. Repeat until the round scores 9+/10 average

The concept matters more than the tooling. Any agent framework can run this loop. The key insight: **the skill file is the product, and the eval loop is the compiler.**
