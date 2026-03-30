# Contributing to heygen-video-producer

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

### Eve's workflow (for autonomous changes)

When Eve updates the skill without Ken online:
1. Create branch, commit, push, open PR
2. Post PR link to Ken on Telegram
3. Wait for review before merging
4. Never push directly to main
