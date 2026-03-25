# Eval Comparison — Diff Two Result Sets

This is an agent-driven comparison tool. Given two eval result files, it produces a detailed diff showing what improved, what regressed, and the overall delta.

## Prerequisites

- Two result files in `./results/` (produced by `run-eval.md`)

## Instructions

### Step 1: Load Both Result Files

Read the two result files the user specifies. If not specified, use the two most recent files in `./results/` sorted by filename (which encodes the timestamp).

Designate:
- **A** = the older result (baseline for comparison)
- **B** = the newer result (the one being evaluated)

### Step 2: Per-Test-Case Comparison

For each test case ID present in both files, compare:

| Metric | A Value | B Value | Delta | Status |
|--------|---------|---------|-------|--------|
| Reviewer Score | X/10 | Y/10 | +/-N | ✅ improved / ⚠️ regressed / — same |
| Verdict | APPROVE | REVISE | — | ✅ / ⚠️ / — |
| Word Count | N | M | +/-D | ✅ closer to budget / ⚠️ over/under |
| Scene Count | N | M | +/-D | ✅ met minimum / ⚠️ below minimum |
| Estimated Duration Ratio | X.XX | Y.YY | +/-D | ✅ closer to 1.0 / ⚠️ further from 1.0 |
| Mode Detection | match/mismatch | match/mismatch | — | ✅ / ⚠️ |

Also compare the constructed prompts qualitatively:
- **Structure changes:** Did scene organization improve?
- **Style block:** Was it added, removed, or changed?
- **Hook quality:** Is the opening stronger or weaker?
- **Media type usage:** More appropriate or less?

### Step 3: Summary Comparison

```
═══════════════════════════════════════════════════════════════
  EVAL COMPARISON — A vs B
═══════════════════════════════════════════════════════════════

  Result A: {filename_a} ({timestamp_a})
  Result B: {filename_b} ({timestamp_b})

  ─────────────────────────────────────────────────────────────
  AGGREGATE METRICS
  ─────────────────────────────────────────────────────────────
  
  Metric                │   A    │   B    │ Delta  │ Status
  ──────────────────────┼────────┼────────┼────────┼────────
  Avg Score             │ 7.6/10 │ 8.1/10 │  +0.5  │ ✅
  Approved              │  6/8   │  7/8   │   +1   │ ✅
  Revised               │  2/8   │  1/8   │   -1   │ ✅
  Rejected              │  0/8   │  0/8   │    0   │ —
  Mode Detection        │  8/8   │  8/8   │    0   │ —
  Scenes Met Min        │  7/8   │  8/8   │   +1   │ ✅
  Avg Duration Ratio    │ 1.10   │ 1.18   │ +0.08  │ ✅
  
  ─────────────────────────────────────────────────────────────
  PER-TEST DELTAS
  ─────────────────────────────────────────────────────────────
  
  ID                  │ Score Δ │ Words Δ │ Scenes Δ │ Status
  ────────────────────┼─────────┼─────────┼──────────┼────────
  basic-feature       │    +1   │   +15   │    +1    │ ✅ improved
  mcp-explainer       │     0   │    -5   │     0    │ — stable
  pricing-announcement│    -1   │   -20   │    -1    │ ⚠️ regressed
  ...

  ─────────────────────────────────────────────────────────────
  IMPROVEMENTS (Score went up or issues fixed)
  ─────────────────────────────────────────────────────────────
  - basic-feature: Added scene structure (was flat paragraph). Score 7 → 8.
  - sales-pitch: Stronger opening hook. Score 7 → 8.

  ─────────────────────────────────────────────────────────────
  REGRESSIONS (Score went down or new issues)
  ─────────────────────────────────────────────────────────────
  - pricing-announcement: Lost visual style block. Score 8 → 7.

  ─────────────────────────────────────────────────────────────
  STABLE (No significant change)
  ─────────────────────────────────────────────────────────────
  - mcp-explainer, product-demo, long-explainer, quick-benefits, quick-overview

  ─────────────────────────────────────────────────────────────
  VERDICT
  ─────────────────────────────────────────────────────────────
  
  Overall: {NET_POSITIVE if more improvements than regressions, 
            NET_NEGATIVE if more regressions, 
            NEUTRAL if balanced}
  
  Recommendation: {specific action, e.g. "Investigate pricing-announcement 
                    regression — likely caused by the style block change in 
                    commit abc123. All other tests improved or held steady."}
═══════════════════════════════════════════════════════════════
```

### Step 4: Write Comparison Report

Save the comparison to `./results/compare-{timestamp_a}-vs-{timestamp_b}.md` as a markdown file.

## Interpretation Guide

- **Score delta of +1 or more** = meaningful improvement
- **Score delta of -1 or more** = investigate regression
- **Duration ratio moving toward 1.0** = better duration targeting
- **Duration ratio > 1.3** = prompt is too long (padding too aggressive)
- **Duration ratio < 0.8** = prompt is too short (padding insufficient)
- **Mode detection mismatches** = mode detection logic needs tuning
- **Scenes below minimum** = prompt structure too sparse

## When to Run

- After modifying SKILL.md (especially prompt engineering rules, phase 3)
- After changing reviewer-prompt.md (recalibrate scoring)
- After updating duration padding rules
- Before publishing a new skill version
