# Eval Runner Prompt (for Adam)

You are testing the HeyGen Video Producer skill as a fresh user. You have ZERO prior context about how this skill works. Your only knowledge comes from reading SKILL.md right now.

## Setup

1. `cd /Users/heyeve/.openclaw/workspace/skills/heygen-video-producer && git checkout main && git pull origin main`
2. Read `SKILL.md` completely. This is your only guide.
3. Your HeyGen API key is in env var `HEYGEN_API_KEY`.

## Write-First Pattern (CRITICAL)

After EACH scenario's POST /v3/video-agents call completes, IMMEDIATELY write a Notion row to the Eval Tracker BEFORE polling for completion. This ensures data survives timeouts.

**Step 1: Submit** → POST /v3/video-agents, capture video_id + session_id from response.
**Step 2: Write Notion row** → Status: "🔄 Running", with video_id, session_id, prompt, avatar, target duration, corrections fired. All fields you know AT SUBMISSION TIME.
**Step 3: Move to next scenario** → Do NOT wait for video completion before moving on.
**Step 4: After ALL scenarios submitted** → Poll all video_ids in a batch loop. Update each Notion row with actual duration, duration %, score, findings.

This way, even if you time out during polling, we have every submission recorded with correct video_id, session_id, avatar choice, and prompt.

## For Each Scenario

Execute the scenario exactly as described. Follow SKILL.md to the letter. Do NOT improvise or work around issues. If the skill doesn't tell you what to do, that's a finding.

For each scenario, record:

```
### S[N]: [Scenario Name]
- **Input:** [exact prompt you gave]
- **Expected:** [from scenario file]
- **Actual:** [what actually happened]
- **Video ID:** [id or "N/A - dry run"]
- **🎬 Video:** [Video Page](https://app.heygen.com/videos/{video_id}) | [Session](https://app.heygen.com/video-agent/{session_id})  ← NOT ?session= query param
- **Duration:** [actual]s vs [target]s ([ratio]%)
- **Avatar:** [which avatar used, how selected]
- **Aspect Correction:** [was Phase 3.5 triggered? what was injected?]
- **Assets Provided:** [list of assets with types, or "none"]
- **Classification:** [per-asset: type → route chosen (contextualize/attach/both) + reason]
- **User Questions Asked:** [0 if none. List any questions the skill asked about asset routing.]
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

## After All Scenarios

### Output: Notion Database Rows

Write results to the **Eval Tracker** database: `collection://17f54098-a085-4234-83ce-55c280266d73`

For EACH scenario, create one row using `notion-create-pages` with `data_source_id: 17f54098-a085-4234-83ce-55c280266d73`.

Properties per row:
```
"Scenario": "R{round}-S{number}: {short name}"     ← TITLE
"Round": {round_number}                              ← NUMBER
"Fix Tested": "{what fix or path this tests}"        ← TEXT
"Prompt": "{the exact prompt used}"                  ← TEXT (truncate to ~200 chars if long)
"Video": "https://app.heygen.com/videos/{video_id}"  ← URL (or null for dry-run/non-generation)
"Session": "https://app.heygen.com/video-agent/{session_id}" ← URL (path-based, NOT ?session= query param)
"Target (s)": {target_seconds}                       ← NUMBER
"Actual (s)": {actual_seconds_or_null}               ← NUMBER
"Duration %": {percentage_as_integer}                 ← NUMBER (e.g. 106 for 106%)
"Avatar Type": "photo_avatar|studio_avatar|video_avatar|none" ← SELECT
"Phase 3.5 Fired": "__YES__" or "__NO__"             ← CHECKBOX
"Corrections": ["A: Portrait→Landscape", "C: Background Fill"] ← MULTI_SELECT (array)
"Status": "✅ Complete|⚠️ Stuck Pending|❌ Failed|🔄 Running" ← SELECT
"Adam Score": {1-10}                                 ← NUMBER
"Findings": "[P1] {description}. Fix: {recommendation}" ← TEXT
"Ken Verdict": "—"                                   ← SELECT (Ken fills in later)
"Ken Notes": ""                                      ← TEXT (Ken fills in later)
```

**Write-first, NOT batch:** Write EACH row immediately after its POST call returns (with video_id + session_id). Do NOT wait to batch all scenarios. The goal is crash-resilient data capture. Update rows later with polling results via `notion-update-page`.

**After creating rows**, also log to `heygen-video-producer-log.jsonl` as before (for machine-readable history).

## Rules

- Do NOT skip scenarios. Run all of them (check the scenario file for the exact count).
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

## ⛔ MANDATORY VALIDATION GATE (before writing to Notion)

**After completing all scenarios and BEFORE creating the Notion doc**, you MUST run this validation step:

For EVERY video_id you recorded (except dry-runs):
```bash
curl -s "https://api.heygen.com/v3/videos/{video_id}" -H "X-Api-Key: $HEYGEN_API_KEY"
```

Check each response:
1. The response MUST return a valid JSON object with `data.video_id` matching your recorded ID.
2. The `video_id` MUST be a full 32-character hex string (e.g. `c4b5a87dc32748f89f717576ee01d5aa`). If yours is shorter, it's wrong.
3. The `session_id` MUST be a valid UUID with dashes (e.g. `c87582f1-fc0f-4074-a7e5-b5140336c734`).

**If ANY video_id fails validation:**
- Mark that scenario as `❌ UNVERIFIED — video_id did not resolve via GET /v3/videos`
- Do NOT fabricate or guess IDs. If you lost the ID, say so.
- Re-run the scenario if time permits. If not, mark it as incomplete.

**If MORE THAN 3 scenarios fail validation, STOP and report the failure to Eve. Do not write a Notion doc with unverified data.**

This gate exists because fabricated video IDs waste Ken's review time. Every link in the Notion doc must work.
