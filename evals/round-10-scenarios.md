# Round 10 — Comprehensive Regression + Style System Validation

**Goal:** Well-balanced suite testing all major paths validated in Rounds 1–9. Covers custom/stock avatars, style system (API + prompt-injected), natural flow vs scene-by-scene, asset handling, quick shot, dry-run, corrections, and duration accuracy.

## Scenarios

### S1 — Custom Photo Avatar + Natural Flow + API Style
**User prompt:** "Make a 45-second video about the future of AI agents in business. Use my avatar Eve Park. I want a cinematic style."
**Tests:** Photo avatar lookup by name, Natural Flow mode (≤60s), API style selection (tag=cinematic), duration padding 1.6x, Phase 3.5 Correction C (background fill for photo_avatar).
**Expected:** Avatar_id passed explicitly, style_id from API browse, no scene labels in prompt, ~45s target.

### S2 — Studio Avatar + Scene-by-Scene + Prompt-Injected Style
**User prompt:** "Create a 2-minute explainer video with 4 scenes about how HeyGen's Video Agent API works. Use a stock presenter — someone professional. I want a clean, minimalist look."
**Tests:** Studio avatar group browse + selection, Scene-by-Scene mode (>90s), prompt-injected style (Minimalistic from prompt-styles.md), multi-scene structure, duration padding 1.3x.
**Expected:** Studio avatar_id discovered via group browse, 4 numbered scenes in prompt, Minimalistic style block injected, ~120s target.

### S3 — Quick Shot Mode + No Avatar Specified
**User prompt:** "Quick video: AI will replace 40% of jobs by 2030 according to Goldman Sachs."
**Tests:** Quick Shot detection, avatar auto-select exception (omit avatar_id), short-form content, minimal prompt.
**Expected:** No avatar discovery, no style selection, one-liner prompt, ≤30s, Quick Shot flow.

### S4 — Dry-Run + Bold & Vibrant Style + Photo Avatar
**User prompt:** "I want a video promoting our new product launch. Use Eve Park as presenter. Make it bold and vibrant. But don't generate yet — show me the plan first."
**Tests:** Dry-run flag detection, style mood mapping ("bold and vibrant" → Bold & Vibrant style), photo avatar, narrative pitch format, "say go or tell me what to change" CTA.
**Expected:** Full dry-run output with collapsible prompt, no API call, style block shown.

### S5 — PDF Asset Attachment + Custom Avatar + Landscape
**User prompt:** "Make a 90-second video summarizing this research paper: https://arxiv.org/pdf/2503.15613. Use Eve Park. Landscape format."
**Tests:** Asset routing (PDF URL → download → upload via /v3/assets → asset_id), landscape orientation, photo avatar + Correction C, content contextualization from PDF.
**Expected:** Asset_id-first routing, PDF content extracted and summarized in script, landscape aspect ratio, Phase 3.5 fires for photo_avatar background.

### S6 — Voice-Over Only (No Avatar)
**User prompt:** "Create a 60-second voice-over narration about the history of artificial intelligence. No avatar needed — just voice over a visual montage."
**Tests:** No-avatar path, voice selection, natural flow prompt, B-roll/visual directions without presenter.
**Expected:** No avatar_id, voice discovered via /v3/voices, motion verbs for B-roll (from motion-vocabulary.md), ~60s target.

### S7 — Studio Avatar + Portrait + Correction A (Landscape→Portrait Reframe)
**User prompt:** "Make a 30-second Instagram Reel with a stock presenter talking about 3 AI tools every creator needs. Portrait format."
**Tests:** Portrait orientation, studio avatar selection, short duration (1.6x padding), Phase 3.5 Correction A if avatar is landscape-native, social media framing.
**Expected:** Portrait aspect ratio, studio avatar_id, short punchy script, Phase 3.5 fires if mismatch detected.

### S8 — On-Screen Text Heavy + Data Visualization
**User prompt:** "Create a 75-second video presenting these stats: Revenue grew 34.7% YoY to $847M. Customer count hit 12,450. NPS score is 72. Churn dropped to 2.1%. Use Eve Park."
**Tests:** Critical On-Screen Text Extraction step (Phase 2), exact number preservation (no rounding), data visualization directions, photo avatar.
**Expected:** On-screen text block with exact figures confirmed before Phase 3, numbers not rounded or rephrased in prompt.

### S9 — Inaccessible URL Handling + Auth Wall
**User prompt:** "Make a video summarizing this internal doc: https://docs.google.com/document/d/1234567890_private/edit. Use any stock presenter."
**Tests:** Auth-wall detection, no content fabrication, user notification, graceful degradation.
**Expected:** Agent detects inaccessible URL, stops and informs user, does NOT fabricate content or pass URL to files[].

### S10 — Multi-Asset + Custom Style Override + Photo Avatar
**User prompt:** "Create a 2-minute video about our Q1 results. Reference these files: our logo at https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/OpenAI_Logo.svg/1200px-OpenAI_Logo.svg.png and this chart https://i.imgur.com/JjGkR9O.png. Use Eve Park. I want a dark, editorial look — think investigative journalism."
**Tests:** Multiple asset handling (2 images), mood-to-style mapping ("dark, editorial" → Contact Sheet/Brodovitch from prompt-styles.md), photo avatar, asset_id-first routing for images, long-form scene-by-scene.
**Expected:** Both assets uploaded via /v3/assets, style mapped from mood description, 4+ scenes, ~120s target.
