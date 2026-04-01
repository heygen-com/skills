# Eval Runner Prompt (for Adam)

You are testing the HeyGen Video Producer skill as a fresh user. You have ZERO prior context about how this skill works. Your only knowledge comes from reading SKILL.md right now.

## Setup

1. `cd /Users/heyeve/.openclaw/workspace/skills/heygen-video-producer && git checkout main && git pull origin main`
2. Read `SKILL.md` completely. This is your only guide.
3. Your HeyGen API key is in env var `HEYGEN_API_KEY`.
4. **Always add `incognito_mode: true`** to every `POST /v3/video-agents` call. This prevents cross-session memory from influencing results and ensures clean, reproducible evaluations.

## Execution Pattern: SUBMIT → WRITE → STOP (CRITICAL)

You MUST follow this exact flow. Violations of this pattern are a BLOCKING failure.

### For each scenario, in order:
**Step 1: Build prompt** following SKILL.md phases.
**Step 2: Submit** → POST /v3/video-agents with `incognito_mode: true`. Capture video_id + session_id from response.
**Step 3: Log the POST payload** → Immediately after submission, echo the EXACT JSON body you sent. Specifically confirm:
  - Was `incognito_mode: true` present? YES/NO
  - Was `style_id` present? If so, what value?
  - Was `avatar_id` present? If so, what value?
  - What `orientation` was set?
**Step 4: Write Notion row** → Status: "🔄 Running", with video_id, session_id, prompt summary, avatar, target duration, corrections fired, payload flags (incognito, style_id, avatar_id, orientation). ALL fields you know AT SUBMISSION TIME.
**Step 5: Move to next scenario.** Do NOT poll. Do NOT wait. Do NOT check video status.

### After ALL scenarios are submitted and written to Notion:
**Step 6: STOP.** Print a summary table of all submissions (scenario, video_id, session_id, payload flags) and exit.

⛔ **DO NOT POLL FOR VIDEO COMPLETION. EVER.** Eve will poll later. Your ONLY job is submit + record + move on.
⛔ **DO NOT sleep() or wait() between scenarios.** Submit, write row, next.
⛔ **If you find yourself writing `sleep` or `poll` or checking video status, you are doing it wrong. STOP.**

This pattern exists because polling burns your entire timeout budget. 8 submissions + 8 Notion writes should take <10 minutes total.

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
- **Duration:** [actual]s vs [target]s ([ratio]%) — LEAVE BLANK if not yet polled
- **Avatar:** [which avatar used, how selected]
- **Payload Flags:** incognito_mode=[true/false], style_id=[value/none], avatar_id=[value/none], orientation=[value]
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
"Scenario": "{short descriptive name}"               ← TITLE (NO round prefix! e.g. "Style-First Video" not "R16-S1: Style-First Video")
"Scenario #": "{number}"                             ← TEXT (e.g. "1", "2", "9A")
"Round": "R{round_number}"                           ← SELECT (e.g. "R16", "R17". Must include "R" prefix)
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
"Incognito Mode": "__YES__" or "__NO__"              ← CHECKBOX (was incognito_mode:true in payload?)
"Style ID Used": "{style_id value or empty}"          ← TEXT (the actual style_id, or empty string if none)
"Status": "✅ Complete|⚠️ Stuck Pending|❌ Failed|🔄 Running" ← SELECT
"Adam Score": {1-10}                                 ← NUMBER
"Findings": "[P1] {description}. Fix: {recommendation}" ← TEXT
"Ken Verdict": "—"                                   ← SELECT (Ken fills in later)
"Ken Notes": ""                                      ← TEXT (Ken fills in later)
```

### ⛔ DEDUP RULE (CRITICAL)

Before writing a Notion row, check if a row with the SAME Round + Scenario # already exists:
1. Search the database for rows where Round = "R{n}" AND Scenario # = "{s}"
2. If a match exists, UPDATE the existing row instead of creating a new one
3. If no match exists, create a new row

Duplicate rows are a BLOCKING failure. Every (Round, Scenario #) combination must be unique.

**Write-first, NOT batch:** Write EACH row immediately after its POST call returns (with video_id + session_id). Do NOT wait to batch all scenarios. The goal is crash-resilient data capture.

**DO NOT poll or update rows.** Eve handles polling and scoring separately. Your job ends after all rows are written.

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

## ⛔ VALIDATION (lightweight — no polling)

For each submission, validate BEFORE writing the Notion row:
1. `video_id` is a full 32-character hex string.
2. `session_id` is a valid UUID with dashes.
3. You echoed the POST payload and confirmed `incognito_mode: true` was present.

If any ID looks wrong (short, missing, malformed), mark it and move on. Do NOT re-run or poll to verify. Do NOT fabricate IDs.
