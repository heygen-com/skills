# Autoresearch Eval Loop

A self-improving cycle where Eve (skill author) writes scenarios, Adam (fresh tester) runs them blind, produces structured feedback in Notion, and Eve fixes everything. Rinse and repeat.

## The Loop

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Eve writes 10 scenarios                        │
│  → evals/round-N-scenarios.md                           │
│  → Each: prompt, expected behavior, what to watch for   │
├─────────────────────────────────────────────────────────┤
│  STEP 2: Adam pulls latest skill                        │
│  → git pull main, read SKILL.md fresh                   │
│  → NO prior context. Blank slate.                       │
├─────────────────────────────────────────────────────────┤
│  STEP 3: Adam runs all 10 sequentially                  │
│  → Execute each scenario as a real user would            │
│  → Log everything: what worked, what broke, friction     │
│  → Score each scenario 1-10                             │
├─────────────────────────────────────────────────────────┤
│  STEP 4: Adam writes Notion doc                         │
│  → "HeyGen Video Producer Eval — Round N"               │
│  → Per-scenario results + aggregate findings + metrics   │
│  → P1/P2/P3 priorities with fix recommendations         │
├─────────────────────────────────────────────────────────┤
│  STEP 5: Ken feeds Notion URL to Eve                    │
│  → Eve reads the doc, creates branch                    │
│  → Fixes all P1/P2 items                                │
│  → Opens PR → merge → back to STEP 1                    │
└─────────────────────────────────────────────────────────┘
```

## How to Run a Round

### Ken says to Eve:
```
Run autoresearch eval round N
```

### Eve:
1. Reads `evals/round-N-scenarios.md`
2. Spawns Adam as subagent with the runner prompt from `evals/eval-runner-prompt.md`
3. Passes Adam the 10 scenarios + Notion parent page ID
4. Adam executes, writes Notion doc, reports back

### Ken reviews Notion doc, then says to Eve:
```
Here's the feedback: [Notion URL]
Address all findings and open a PR.
```

### Eve:
1. Fetches the Notion doc
2. Extracts all P1/P2 findings
3. Creates branch `fix/round-N-feedback`
4. Implements fixes in SKILL.md
5. Opens PR with findings → fixes mapping

## Naming Convention

- Scenarios: `evals/round-N-scenarios.md` (N = 1, 2, 3...)
- Notion docs: "HeyGen Video Producer Eval — Round N"
- Fix branches: `fix/round-N-feedback`
- Round themes: each round focuses on a specific area

## Round History

| Round | Theme | Scenarios | Videos | Date | Key Changes |
|-------|-------|-----------|--------|------|-------------|
| R1 | Full skill coverage | 10 | 6/10 | 2026-03-30 | Baseline. SKILL.md v2→v3 API architecture |
| R2 | Aspect ratio + background | 10 | 9/10 | 2026-03-30 | Phase 3.5 correction failures identified |
| R3 | Phase 3.5 rewrite validation | 10 | 8/10 | 2026-03-30 | Explicit "AI Image tool" trigger phrase |
| R4 | Consolidated fixes | 10 | 9/10 | 2026-03-31 | video_avatar backend bug confirmed |
| R5 | Consolidation (R1-R5) | — | — | 2026-03-31 | P0 issues: gen fill quality, file URL failures |
| R6 | Prescriptive Phase 3.5 | 10 | 7/10 | 2026-03-31 | PR #13 (7 fixes), asset_id-first routing |
| R7 | Avatar conflict fix | 10 | 9/10 | 2026-03-31 | avatar_id vs prompt text conflict discovered. PR #14 |
| R8 | Studio avatar deep dive | 10 | 10/10 | 2026-03-31 | Avg 7.6/10. HeyGen docs audit (48+ pages) |
| R9 | Official docs integration | 10 | — | 2026-03-31 | Styles system, timestamp-per-scene kills delivery |
| R10 | Slim SKILL.md baseline | 10 | 10/10 | 2026-04-01 | SKILL.md 57KB→12.7KB (78% reduction). Avg 8.2/10 |
| R11 | Regression check | 8 | 8/8 | 2026-04-01 | Zero functional regressions post-refactor |
| R12 | Boundary push (edge cases) | 10 | — | 2026-04-01 | PR #19 script framing, PR #20 Phase 3.5 restore |
| R13 | Duration padding | — | — | 2026-04-01 | 365% overshoot on 15s target. Write-first pattern |
| R14 | Optimization pass | — | — | 2026-04-01 | SKILL.md 383→259 lines. PR #21 (-1203 lines) |
| R15 | Regression | — | — | 2026-04-01 | Timed out (S1 stuck at `reviewing`) |
| R16 | style_id + incognito_mode | 8 | 8/8 | 2026-04-01 | PR #22. style_id browsing, incognito_mode mandatory |
| R17 | Photo avatar v3 compat | 10 | 8/10 | 2026-04-02 | 2 failures: photo_avatar + /v3/video-agents incompat |
| R18 | Square avatar (1:1) correction | 6 | 🔄 | 2026-04-03 | Phase 3.5 square detection + corrections D/E |

**Cumulative:** 18 rounds, 80+ videos generated, SKILL.md 57KB → 12.8KB (259 lines)
