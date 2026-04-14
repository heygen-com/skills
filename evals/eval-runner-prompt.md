# Eval Runner Prompt — heygen-video

You are an evaluator running a fresh-install test of the `heygen-video` skill.

## Setup (CRITICAL — simulate fresh install)

1. **Delete** your local copy of the skill: `rm -rf <your_workspace>/skills/heygen-skills`
2. **Clone fresh** from GitHub: `cd <your_workspace>/skills && git clone git@github.com:heygen-com/skills.git heygen-skills`
3. **Read ONLY** `heygen-skills/video-message/SKILL.md` — this is your sole source of truth
4. You have NO prior knowledge of how this skill works. Follow SKILL.md exactly as written.

## For Each Scenario

Read the scenario from the file you were given. For each one:

1. Follow the SKILL.md pipeline step by step
2. For video submission: use ONLY the method described in SKILL.md (currently: `scripts/submit-video.sh` wrapper)
3. Capture all outputs: video_id, session_id, framing_applied, duration
4. Poll for completion: `GET https://api.heygen.com/v3/videos/<video_id>` with header `X-Api-Key: $HEYGEN_API_KEY`
5. When status is `completed`, get the video URL from the response
6. Download the MP4: `curl -o /tmp/r<round>-s<num>.mp4 "<video_url>"`
7. Send the MP4 to Ken on Telegram with caption:
   ```
   R<round> S<num>: <scenario_title>
   Duration: <actual>s (target: <target>s)
   Framing: <framing_applied>
   Video ID: <video_id>
   ```

## After All Scenarios

Write results to the specified results file. For each scenario include:

| Field | Description |
|-------|-------------|
| Video ID | From API response |
| Status | completed / failed / timeout |
| Duration | Actual vs target (seconds) |
| Duration Accuracy | actual/target as percentage |
| framing_applied | From wrapper output (none, square_to_landscape, etc.) |
| Wrapper Used | YES if used submit-video.sh, NO if raw curl |
| Avatar ID | Which avatar was used |
| Issues | Any problems encountered |

## Scoring Rubric

Score each video 1–10:

- **10**: Perfect. Correct avatar, correct orientation, good framing, duration within 20%, natural delivery.
- **8-9**: Minor issues. Slight duration overshoot, acceptable framing, good overall.
- **6-7**: Functional but flawed. Duration off by >30%, framing issues visible but not broken, minor quality problems.
- **4-5**: Significant problems. Wrong orientation, black bars visible, major duration mismatch, avatar issues.
- **1-3**: Broken. Failed to generate, completely wrong avatar, unwatchable output.

## Issue Classification

- **P0 (Broken)**: Video fails to generate, or generates with fundamentally wrong output
- **P1 (Major)**: Visible quality issue that would block production use (wrong orientation, black bars, identity loss)
- **P2 (Minor)**: Noticeable but acceptable (duration 30%+ off, slightly awkward framing)
- **P3 (Cosmetic)**: Polish items (could be better but functional)

## Rules

- Do NOT use any prior knowledge about the HeyGen API
- Do NOT skip steps in SKILL.md
- Do NOT call the HeyGen API directly unless SKILL.md tells you to
- If SKILL.md is unclear or missing information, note it as a finding
- Use `incognito_mode: true` in all payloads
- Always include `orientation` in payloads
