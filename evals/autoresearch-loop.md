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

| Round | Theme | Date | Notion Doc | PR |
|-------|-------|------|-----------|-----|
| 1 | Full skill coverage (10 scenarios) | 2026-03-30 | [Report](https://www.notion.so/heygen/Video-Producer-Skill-10-Scenario-Test-Report-333449792c69819e9429e71126c37dc2) | #8 |
| 2 | Aspect ratio + background corrections | TBD | TBD | TBD |
