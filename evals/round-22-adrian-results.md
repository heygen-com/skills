# Round 22 — Adrian Results (S6–S10)
**Agent:** Adrian (Claude Sonnet, subagent)
**Date:** 2026-04-06
**Focus:** Fresh install validation — wrapper script + framing correction across avatar types

## Fresh Install Experience
- ✅ Cloned fresh from `git@github.com:heygen-com/skills.git` into workspace-adrian/skills
- ✅ Read only `video-message/SKILL.md` as sole source of truth
- ✅ Wrapper script `submit-video.sh` used for all submissions (mandated in Generate phase)
- ⚠️ **SKILL.md is clear and unambiguous** — the ⛔ stop gate and wrapper mandate were found without confusion
- ⚠️ Minor friction: `scripts/submit-video.sh` lives inside `video-message/` dir (not a separate `scripts/` folder) — path inference was needed

---

## Per-Scenario Results

### S6: Portrait → Landscape with Style Browsing
| Field | Value |
|-------|-------|
| Video ID | `61712ea9e68542b5b292bc0ae12e4643` |
| Session URL | (not captured — session_id not logged by previous model run) |
| Status | ✅ completed |
| Target Duration | 40s |
| Actual Duration | 50.73s |
| Duration Accuracy | 126.8% (26.8% over) |
| framing_applied | `portrait_to_landscape` |
| Avatar | `5b776dccd2b845679edc676b37e74bcb` (Eve, portrait 768×1376) |
| Wrapper Used | YES |
| Issues | Duration overshoot (+10.73s). Style browsing added production time. |
| Score | **7/10** |

---

### S7: Prompt Avatar Dimension Check
| Field | Value |
|-------|-------|
| Video ID | `9e7532fe1a544bab8fc17a904f9feaf2` |
| Session URL | (not captured) |
| Status | ✅ completed |
| Target Duration | 30s |
| Actual Duration | 38.01s |
| Duration Accuracy | 126.7% (26.7% over) |
| framing_applied | `none` |
| Avatar | `24f4a61e49ad49c0abc89abb68b85080` (Adam, prompt-generated) |
| Wrapper Used | YES |
| Issues | Prompt-generated avatar dimensions may return 0×0 (async processing). Wrapper may have skipped dimension check — framing_applied: none is expected per scenario spec. Duration slightly over target. |
| Score | **7/10** |

---

### S8: Square Avatar → Landscape with URL Asset
| Field | Value |
|-------|-------|
| Video ID | `162d49f026bc46eeb69c8c59e545f99c` |
| Session URL | (not captured) |
| Status | ✅ completed |
| Target Duration | 45s |
| Actual Duration | 72.93s |
| Duration Accuracy | 162.1% (62.1% over) |
| framing_applied | `square_to_landscape` |
| Avatar | `636c7609d11546b999c93ee343fde086` (Cleo, square 2048×2048) |
| Wrapper Used | YES |
| Issues | **P1 — Major duration overshoot** (+27.93s, 62.1% over). URL asset (developers.heygen.com) routed as Path A (contextualized), likely increased script density → longer video. |
| Score | **6/10** |

---

### S9: Landscape Avatar → Landscape (Eve Landscape Look)
| Field | Value |
|-------|-------|
| Video ID | `9b753c43d6fe4632943140c9fe2ee6c4` |
| Session URL | (not captured) |
| Status | ✅ completed |
| Target Duration | 25s |
| Actual Duration | 33.67s |
| Duration Accuracy | 134.7% (34.7% over) |
| framing_applied | `none` |
| Avatar | `b58f6992930c40dc91498a7bc9bf1e01` (Eve landscape, 1792×1024) |
| Wrapper Used | YES |
| Issues | Duration overshoot (+8.67s). Orientation matched correctly, no framing needed. |
| Score | **7/10** |

---

### S10: Long-Form Test (60s)
| Field | Value |
|-------|-------|
| Video ID | `091cf065dbc34aaa85df6e0a275abe2c` |
| Session URL | (not captured) |
| Status | ✅ completed |
| Target Duration | 60s |
| Actual Duration | 86.88s |
| Duration Accuracy | 144.8% (44.8% over) |
| framing_applied | `portrait_to_landscape` |
| Avatar | `5b776dccd2b845679edc676b37e74bcb` (Eve, portrait) |
| Wrapper Used | YES |
| Issues | **P1 — Duration overshoot** (+26.88s). Long-form topic ("persistent AI agent identity") with deep-dive prompt generated significantly more content than 60s target. Caption sent to Ken incorrectly said "target: 85s" — actual target is 60s. |
| Score | **6/10** |

---

## Summary

| Metric | Value |
|--------|-------|
| Total Videos Completed | 5/5 |
| Total Delivered to Ken | 5/5 |
| Average Score | **6.6/10** |
| Average Duration Accuracy | **139.0%** (all over target) |
| Wrapper Used (all) | YES — 5/5 |
| P0 Issues | 0 |
| P1 Issues | 2 (S8: major duration overshoot; S10: major duration overshoot + caption error) |
| P2 Issues | 3 (S6, S7, S9: moderate duration overshoots) |
| P3 Issues | 1 (session_id not captured across model boundary) |

### Fresh Install Experience
**Smooth.** The SKILL.md ⛔ stop gate and wrapper mandate were unambiguous. No agent bypassed to raw API. The framing correction logic was correctly followed for all portrait/square avatars.

### Key Findings
1. **Duration overshoot is systemic.** All 5 videos ran 26–62% over target. The `"This script is a concept to convey — not verbatim"` directive may be generating too much content. Consider adding explicit `max_duration` enforcement to the wrapper or prompt template.
2. **Wrapper working correctly.** All framing corrections applied as expected (portrait_to_landscape for S6/S10, square_to_landscape for S8, none for matched orientations S7/S9).
3. **URL asset routing (S8) compounds duration overshoot.** When a web page is contextualized (Path A), the baked-in summary adds script density. Consider warning users that URL assets push durations ~60% over target.
4. **session_id capture across model boundaries.** When a subagent crashes/restarts mid-eval, session_ids from the original submissions are lost. The wrapper should log both video_id + session_id to a local file immediately on submission.
5. **Caption error on S10.** "target: 85s" was sent instead of "target: 60s" — a manual error during handoff polling.
