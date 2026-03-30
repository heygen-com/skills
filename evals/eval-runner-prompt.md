# Eval Runner Prompt (for Adam)

You are testing the HeyGen Video Producer skill as a fresh user. You have ZERO prior context about how this skill works. Your only knowledge comes from reading SKILL.md right now.

## Setup

1. `cd /Users/heyeve/.openclaw/workspace/skills/heygen-video-producer && git checkout main && git pull origin main`
2. Read `SKILL.md` completely. This is your only guide.
3. Your HeyGen API key is in env var `HEYGEN_API_KEY`.

## For Each Scenario

Execute the scenario exactly as described. Follow SKILL.md to the letter. Do NOT improvise or work around issues. If the skill doesn't tell you what to do, that's a finding.

For each scenario, record:

```
### S[N]: [Scenario Name]
- **Input:** [exact prompt you gave]
- **Expected:** [from scenario file]
- **Actual:** [what actually happened]
- **Video ID:** [id or "N/A - dry run"]
- **🎬 Video:** [Video Page](https://app.heygen.com/videos/{video_id}) | [Session](https://app.heygen.com/video-agent/{session_id})
- **Duration:** [actual]s vs [target]s ([ratio]%)
- **Avatar:** [which avatar used, how selected]
- **Aspect Correction:** [was Phase 3.5 triggered? what was injected?]
- **Friction Points:** [anything confusing, missing, or wrong in SKILL.md]
- **Score:** [1-10]
- **Finding:** [P1/P2/P3] [one-line description]
- **Fix Recommendation:** [specific change to SKILL.md]
- **🧑 Human Review:** _(pending Ken's review)_
- **Ken's Notes:** _—_
```

> **Note on duration:** Duration accuracy is P2 at most. Video Agent controls final timing
> internally. Don't flag duration variance as P1 or P3.

## Scoring Rubric

- **10:** Perfect. Skill guided me flawlessly, output matched expectations.
- **8-9:** Minor friction but correct output. Small SKILL.md clarification needed.
- **6-7:** Worked but with workarounds. SKILL.md was unclear or incomplete.
- **4-5:** Partially worked. Had to deviate from SKILL.md significantly.
- **1-3:** Failed. SKILL.md gave wrong instructions or critical info was missing.

## Priority Definitions

- **P1 (Critical):** Breaks the workflow. Wrong API call, missing required info, video fails to generate.
- **P2 (Important):** Degrades quality. Bad framing, wrong avatar, unnecessary friction.
- **P3 (Nice-to-have):** Polish. Wording improvements, edge case docs, minor UX.

## After All 10 Scenarios

Write a Notion doc under the provided parent page with this structure:

### Page Title: "HeyGen Video Producer Eval — Round [N]"

### Content Structure:

```markdown
# HeyGen Video Producer Eval — Round [N]
**Theme:** [round theme]
**Date:** [date]
**Tester:** Adam (blank-slate, fresh SKILL.md read)
**Skill version:** [git commit hash from main]

## Summary
- Scenarios run: X/10
- Videos generated: X/10 (X dry-runs)
- P1 issues: X | P2: X | P3: X
- Overall skill score: X/100

## Per-Scenario Results
[paste each scenario result block from above]

## Aggregate Findings

| # | Priority | Finding | Affected Scenarios | Recommendation |
|---|----------|---------|-------------------|----------------|
| 1 | P1 | ... | S3, S7 | ... |

## Metrics
- Avg duration accuracy: X%
- Aspect correction triggered: X/10 scenarios
- Correction success rate: X/Y (did injected prompts fix the issue?)
- Videos with black bars despite correction: X/10 (pending Ken's visual review)
- Videos with missing backgrounds despite correction: X/10 (pending Ken's visual review)
- Avg score: X/10

## 🧑 Human Evaluation Tracker
Ken reviews every video. Fill in after watching each.

| Scenario | Video Page | Session | Quality (1-10) | Visual Issues | Script Quality | Avatar/Voice Fit | Ken's Verdict | Notes |
|----------|-----------|---------|----------------|---------------|----------------|-----------------|---------------|-------|
| S1 | [Video](url) | [Session](url) | _ | _ | _ | _ | _ | _ |
[...one row per scenario...]

**Columns guide:**
- **Quality (1-10):** Overall video quality
- **Visual Issues:** Black bars, cropping, background problems, framing
- **Script Quality:** Was the content good? Tone right? Pacing?
- **Avatar/Voice Fit:** Did the avatar look/sound right for the content?
- **Ken's Verdict:** ✅ Ship / 🛠️ Fix needed / ❌ Redo
- **Notes:** Anything else — what was wrong, what was surprisingly good

## Raw Notes
[anything else worth noting — API errors, timing, unexpected behavior]
```

## Rules

- Do NOT skip scenarios. Run all 10.
- Do NOT fix issues yourself. Document them.
- If a scenario requires a specific avatar and you can't find it, document that as a finding.
- Time each scenario. Note if any take unreasonably long.
- If the skill says to do something and the API rejects it, that's a P1.
- Be harsh. The point is to find problems.
- **⚠️ CRITICAL — ALWAYS capture `session_id` from the POST /v3/video-agents response.** The GET /v3/videos endpoint does NOT return session_id. If you don't capture it at creation time, it's GONE FOREVER. Parse it from the response JSON immediately after submission. Both URLs are REQUIRED for every scenario:
  - Session: `https://app.heygen.com/video-agent/{session_id}` ← **capture this FIRST**
  - Video Page: `https://app.heygen.com/videos/{video_id}`
- If the POST response doesn't include `session_id`, document that as a P1 finding.
- **Every row in the Human Evaluation Tracker MUST have a Session link.** "n/a" is only acceptable for dry-run scenarios.
