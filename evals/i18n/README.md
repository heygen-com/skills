# i18n Evaluation Suite

Tests that heygen-stack skills work correctly for non-English users without regressing English quality.

## Quick Start

Run all scenarios in dry-run mode for each language and score against the rubric.

```bash
# For each scenario in scenarios.json:
# 1. Invoke the skill with: "dry run: [scenario input for language X]"
# 2. Score the output against evals/i18n/rubric.md
# 3. Save results to evals/i18n/baselines/
```

## Structure

| File | Purpose |
|------|---------|
| `scenarios.json` | 8 test inputs per language (en, ja, es, ko) per skill |
| `rubric.md` | Scoring criteria, composite formula, regression thresholds |
| `baselines/` | Saved score snapshots for before/after comparison |
| `README.md` | This file |

## Languages Tested

| Code | Language | Script Type | Why |
|------|----------|-------------|-----|
| en | English | Latin | Baseline — must not regress |
| ja | Japanese | CJK | Tests CJK character handling, very different grammar |
| es | Spanish | Latin (non-English) | Tests non-English Latin script |
| ko | Korean | Hangul | Tests another non-Latin script, important HeyGen market |

## Scenarios

1. **routing-full-producer** — Vague video request triggers Full Producer
2. **routing-quick-shot** — Skip questions triggers Quick Shot
3. **discovery-interview** — Discovery questions in user's language
4. **voice-selection-language** — Voice matches user's language
5. **test-video-prompt** — Phase 5 test video in user's language
6. **script-generation** — Script in user's language, directives in English
7. **prompt-craft-mixed** — Content language + English technical directives
8. **error-messages** — Errors in user's language

## When to Run

- Before and after any i18n changes
- Before PRs that modify skill routing, Discovery, voice selection, or prompt construction
- After version bumps to verify no regression
