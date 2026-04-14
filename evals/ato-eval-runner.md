# ATO Eval Runner — Tool Selection Accuracy
# Version: 1.0.0 | Apr 7, 2026

## Your Task

You are running an ATO (Agent Tool Optimization) evaluation. You will test whether you correctly route 100 user requests to the right HeyGen skill based on trigger language alone.

**This is a routing-only test. Do NOT call any APIs. Do NOT generate videos. Do NOT create avatars.**

---

## Setup

1. Read `evals/ato-eval-scenarios.md` — this is your scenario file
2. Read the skill descriptions from:
   - `identity/SKILL.md` (lines 1–15, the YAML front matter `description` field only)
   - `video-message/SKILL.md` (lines 1–15, the YAML front matter `description` field only)
3. You have ONLY these two description blocks to work from. Do NOT read the rest of either SKILL.md.
4. For each scenario, make a routing decision based solely on those descriptions.

---

## Routing Decision Rules

For each scenario message, decide:

| Decision | Meaning |
|---|---|
| `AVATAR` | Route to heygen-avatar |
| `VIDEO` | Route to heygen-video |
| `CHAIN` | Run heygen-avatar first, then heygen-video |
| `NONE` | Neither skill applies |
| `ASK` | Ambiguous — you would ask a clarifying question before routing |

**Important for Category D (Ambiguous):**
- `ASK` is a valid and often correct answer — it shows good judgment
- State what clarifying question you would ask
- Then state which skill you'd route to after the most likely answer

---

## Output Format

Write results to `/Users/heyeve/.openclaw/workspace/evals/ato-results-<AGENT_NAME>-<ROUND>.md`

Where:
- `AGENT_NAME` = your agent name (adam / adrian / eve)
- `ROUND` = 1 (increment if re-running)

### Results File Format

```markdown
# ATO Eval Results — <AGENT_NAME>
Date: <ISO timestamp>
Model: <model name>
Round: 1

## Summary
- Total scenarios: 100
- Correct: X
- Incorrect: Y  
- Score: X/100 (X%)
- By category:
  - A (Identity-First, 20): X/20
  - B (Messaging-First, 20): X/20
  - C (Generic, 20): X/20
  - D (Ambiguous, 20): X/20
  - E (Negative, 10): X/10
  - F (Chained, 10): X/10

## Scenario Results

| ID | User Message (truncated) | Your Decision | Expected | Correct? | Notes |
|----|--------------------------|---------------|----------|----------|-------|
| A1 | "I want to create my digital twin..." | AVATAR | AVATAR | ✅ | |
| A2 | "Can you set up an avatar..." | AVATAR | AVATAR | ✅ | |
...

## Misroutes (incorrect decisions)
List every incorrect routing with analysis:
- **<ID>**: Expected `<X>`, got `<Y>`. Trigger words that confused routing: "...". 
  Root cause: [description was ambiguous / trigger word overlap / missing use case / etc]

## Observations
- Which trigger words reliably activate the right skill?
- Which trigger words caused confusion?
- What's missing from the descriptions that would improve routing?
- Any patterns in misroutes?

## Recommendations
List specific description changes that would fix misroutes (quote the exact text to add/change).
```

---

## Scoring

### Categories A, B, C, E, F — Hard Correct/Incorrect
- Exact match to expected routing = ✅ correct
- Any other decision = ❌ incorrect (no partial credit)
- Exception: Category F `CHAIN` — credit if agent routes to `AVATAR` first with explicit mention of heygen-video as next step

### Category D — Ambiguous (judgment scoring)
Award full credit (✅) for any of:
- Correct routing per the expected answer in the scenario comment
- `ASK` with a sensible clarifying question that would lead to the right skill
- Either `AVATAR` or `VIDEO` when the scenario comment says "either valid"

Award half credit (0.5) for:
- Correct skill but unclear reasoning

Award no credit (❌) for:
- `NONE` on any Category D scenario
- Wrong skill with no clarifying question

---

## Rules

- **Do NOT read anything beyond the YAML front matter descriptions of each SKILL.md**
- **Do NOT make API calls of any kind**
- **Do NOT generate any content**
- Process all 100 scenarios in a single pass
- Write results to the file — do NOT send results as a Telegram message (too long)
- After writing the file, send Ken ONE summary message:

```
ATO Eval Round 1 — <AGENT_NAME>
Score: X/100 (X%)
A: X/20 | B: X/20 | C: X/20 | D: X/20 | E: X/10 | F: X/10
Top misroutes: [list 3 most interesting ones in one line each]
Full results: evals/ato-results-<agent>-1.md
```

---

## Why This Test Matters

The ATO research (toolrank.dev, Apr 2026) found:
- 73% of MCP/skill servers are invisible to agents because their tool descriptions are too vague
- Tools with quality descriptions get **3.6x higher selection probability**
- Action verbs, explicit enums, "Use when" / "NOT for" patterns, and return value descriptions are the key factors

This eval measures whether the current skill descriptions achieve correct routing. Misroutes = description gaps = lost agent selection = fewer videos generated = lower GTM impact.
