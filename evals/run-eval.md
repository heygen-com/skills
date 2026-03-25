# Eval Runner — Dry Run (Prompt Quality)

This is an agent-driven evaluation that tests prompt quality without spending HeyGen credits. You'll construct Video Agent prompts for each test case and score them against the reviewer criteria.

## Prerequisites

- Access to the skill at `../SKILL.md`
- Reviewer criteria at `../references/reviewer-prompt.md`
- Test cases at `./test-prompts.json`

## Instructions

Follow these steps exactly.

### Step 1: Load Context

1. Read `../SKILL.md` — this is the full heygen-video-producer skill
2. Read `../references/reviewer-prompt.md` — this is the reviewer scoring rubric
3. Read `./test-prompts.json` — these are the 8 test cases with baselines

### Step 2: For Each Test Case, Construct the Prompt

For each entry in `test-prompts.json`, act as if a user sent you the `prompt` field. Use the `context` field as additional background (audience, tone, duration hints).

**Mode detection:** Use the `expected_mode` field to determine which skill path to follow:
- `full_producer` → Follow Phases 1-3 of the SKILL.md (Discovery → Script → Prompt Engineering). Since there's no real user to interview, use the `context` field to fill in discovery gaps. Make reasonable assumptions for anything not specified (default to: developer audience, landscape orientation, minimalistic style, no assets).
- `quick_shot` → Follow the Quick Shot path (skip to Phase 4 prompt construction). Still apply prompt engineering rules (scene structure, visual style block, media types).

**For each test case, produce:**
1. The full constructed prompt exactly as it would be sent to `POST /v1/video_agent/generate`
2. Word count of the VO/script portion
3. Number of scenes
4. Estimated duration based on word count at 150 wpm

**Do NOT call the HeyGen API.** This is a dry run. Just produce the prompts.

### Step 3: Score Each Prompt

For each constructed prompt, apply the reviewer criteria from `../references/reviewer-prompt.md`. Score on the 10-point scale:

| Criterion | Weight | What to Check |
|-----------|--------|---------------|
| Scene Structure | High | Scenes with Visual + VO + Duration? Or flat paragraph? |
| Opening Hook | High | Grabs attention in <10s? Or context-setting? |
| Visual Style | Medium | Style block present? Colors, descriptor, fonts? |
| Media Type Direction | Medium | Each scene specifies media type? Appropriate choices? |
| Pacing & Word Count | High | Within 150 wpm budget? Durations balanced? |
| Script Quality | Medium | Written for the ear? Short sentences? Active voice? |
| Narrator Framing | Low | "A narrator explains..." vs "Create a video about..."? |
| Negative Constraints | Low | Only present if user explicitly asked? |
| Overall Production Quality | High | Would a real producer approve this? |

Assign a score 1-10 and a verdict: APPROVE (8+), REVISE (5-7), REJECT (<5).

### Step 4: Compare to Baselines

For each test case, compare your scores to the baseline:

```
Test: {id}
  Baseline reviewer_score: {baseline.reviewer_score}
  New reviewer_score: {your_score}
  Delta: {+/-difference}
  
  Baseline duration_ratio: {baseline.duration_ratio}
  Estimated duration_ratio: {estimated_duration / target_duration}
  Delta: {+/-difference}
  
  Expected min scenes: {expected_min_scenes}
  Actual scenes: {your_scene_count}
  Met minimum: {yes/no}
```

### Step 5: Write Results

Create a results file at `./results/{timestamp}.json` where `{timestamp}` is ISO-8601 format (e.g., `2026-03-24T18-49-00Z.json`). Use dashes instead of colons in the filename for filesystem compatibility.

The results file schema:

```json
{
  "timestamp": "2026-03-24T18:49:00Z",
  "skill_version": "git commit hash or 'unknown'",
  "evaluator_model": "model name used for this eval",
  "test_cases": [
    {
      "id": "basic-feature",
      "mode_detected": "full_producer",
      "mode_expected": "full_producer",
      "mode_match": true,
      "constructed_prompt": "full prompt text...",
      "word_count": 190,
      "scene_count": 6,
      "estimated_duration_seconds": 76,
      "target_duration_seconds": 60,
      "estimated_duration_ratio": 1.27,
      "reviewer_score": 8,
      "reviewer_verdict": "APPROVE",
      "reviewer_strengths": [
        "Strong opening hook",
        "Good scene variety"
      ],
      "reviewer_issues": [
        "[MINOR] Scene 4 could use more specific visual direction"
      ],
      "baseline_comparison": {
        "score_delta": 0,
        "duration_ratio_delta": 0.67,
        "scenes_met_minimum": true
      }
    }
  ],
  "summary": {
    "total_tests": 8,
    "approved": 6,
    "revised": 2,
    "rejected": 0,
    "avg_score": 7.8,
    "avg_baseline_score_delta": 0.5,
    "mode_detection_accuracy": 1.0,
    "avg_estimated_duration_ratio": 1.15,
    "scenes_minimum_met_rate": 1.0
  }
}
```

### Step 6: Print Summary

After writing the results file, print a summary table:

```
═══════════════════════════════════════════════════════════════
  EVAL RESULTS — {timestamp}
═══════════════════════════════════════════════════════════════

  ID                  │ Score │ Baseline │ Delta │ Verdict │ Scenes │ Words
  ────────────────────┼───────┼──────────┼───────┼─────────┼────────┼──────
  basic-feature       │  8/10 │     8/10 │    +0 │ APPROVE │   6/4  │  190
  mcp-explainer       │  9/10 │     8/10 │    +1 │ APPROVE │   6/5  │  190
  ...

  ─────────────────────────────────────────────────────────────
  SUMMARY
  ─────────────────────────────────────────────────────────────
  Average Score:         7.8/10  (baseline avg: 7.6)
  Approved:              6/8
  Revised:               2/8
  Rejected:              0/8
  Mode Detection:        8/8 correct
  Scenes Met Minimum:    8/8
  Avg Duration Ratio:    1.15x (target: ~1.4x with padding)

  OVERALL: {PASS if avg_score >= 7.5 and rejected == 0, else NEEDS_WORK}
═══════════════════════════════════════════════════════════════
```

## Notes

- This eval tests PROMPT QUALITY only. It does not test actual video output.
- To test actual generation, use the prompts from results and submit them manually via the skill or API.
- Run this eval after any SKILL.md changes to catch regressions.
- The 1.4x duration padding rule is critical. Check that padded word counts are correct.
- Mode detection accuracy matters. Quick shot prompts that go through full producer waste user time. Full producer prompts in quick shot mode miss quality.
