# i18n Eval Rubric

## Scoring Dimensions

### 1. Routing Accuracy (binary: pass/fail)
Did the correct skill/mode fire regardless of input language?
- **PASS:** Correct mode detected (Full Producer, Quick Shot, Enhanced Prompt, etc.)
- **FAIL:** Wrong mode or no mode detected

### 2. Language Consistency (binary: pass/fail)
Are user-facing outputs in the user's language?
- **PASS:** Discovery questions, status messages, confirmations all in `user_language`
- **FAIL:** Any user-facing message in English when user is non-English

### 3. Prompt Quality (1-5 scale)
Is the API prompt coherent and well-structured?
- **5:** Indistinguishable from English baseline quality
- **4:** Minor awkwardness but fully functional
- **3:** Noticeable quality drop but video would be acceptable
- **2:** Significant issues — garbled mixed-language or lost context
- **1:** Broken — prompt would produce a bad or failed video

### 4. Voice Match (binary: pass/fail)
Did the skill select/filter voices in the correct language?
- **PASS:** Voice API call includes correct language filter + locale
- **FAIL:** Defaults to English or no language filter

### 5. Technical Directive Integrity (binary: pass/fail)
Are English-only directives preserved in English?
- **PASS:** Motion verbs, style blocks, frame check corrections, script framing directive all in English
- **FAIL:** Any technical directive translated (would break Video Agent)

### 6. Feature Parity (checklist, 0-7)
Do all pipeline stages execute?
- [ ] Mode Detection works
- [ ] Discovery gathers all 10 fields
- [ ] Script generation completes
- [ ] Prompt Craft produces structured output
- [ ] Frame Check runs (if avatar_id set)
- [ ] Style block appended
- [ ] Script framing directive present

## Composite Score

**Per scenario:** Sum of binary checks (4 max) + Prompt Quality (1-5) + Feature Parity (0-7) = max 16

**Per language:** Average composite score across all 8 scenarios.

**Regression threshold:**
- English baseline composite must not drop after i18n changes
- Non-English composite must score within 80% of English baseline on Prompt Quality dimension
- All binary checks (Routing, Language Consistency, Voice Match, Technical Directives) must pass for every language

## How to Run

1. For each scenario in `scenarios.json`, invoke the skill in **dry-run mode** with the input for each language
2. Capture the skill's output at each stage: mode detection result, discovery questions, script, prompt, voice API calls
3. Score each dimension per the rubric above
4. Record results in `baselines/` as `{YYYY-MM-DD}-{language}.json`

### Example dry-run invocation
```
dry run: 新製品の発売についてのビデオを作って
```
Then score the output against each dimension.

### Baseline file format
```json
{
  "date": "2026-04-10",
  "language": "ja",
  "version": "1.3.0",
  "scenarios": {
    "routing-full-producer": {
      "routing_accuracy": "pass",
      "language_consistency": "pass",
      "prompt_quality": 4,
      "voice_match": "pass",
      "technical_directive_integrity": "pass",
      "feature_parity": 7,
      "composite": 15,
      "notes": ""
    }
  },
  "average_composite": 14.5
}
```
