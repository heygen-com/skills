---
version: 3.1.0 # x-release-please-version
name: heygen-translate
description: |
  Translate and dub a video into another language with voice cloning and lip-sync,
  powered by HeyGen Video Translation. The presenter keeps their face, their voice
  is cloned into the target language, and lips re-sync to the new audio — viewers
  see the same person speaking natively.
  Use when: (1) localizing an existing video into one or more languages
  ("translate this video to Spanish", "make this in French and German",
  "dub this into Japanese", "I need this in 10 languages for a launch"),
  (2) the user has a finished video and wants the SAME presenter speaking another
  language (not a new presenter — that's heygen-video),
  (3) podcast / audio-only translation ("translate this podcast", "dub the audio
  but keep my video"),
  (4) high-stakes translations where the user wants to review/edit subtitles
  before final render (the proofreads workflow),
  (5) "translate my video", "dub this", "localize this clip", "make a multilingual
  version", "subtitle and dub".
  Returns the translated video URL (or audio file for audio-only mode), one per
  target language.
  Chain signal: if the user wants to CREATE a new video in another language (no
  source video exists yet), route to heygen-video and write the script in the
  target language — do not use heygen-translate. Use heygen-translate only when
  there is an existing source video to localize.
  NOT for: creating new videos from scratch (use heygen-video), avatar creation
  (use heygen-avatar), TTS-only synthesis (use heygen-video with audio-only
  output), or text-only translation.
argument-hint: "[video_url_or_path] [--to language]"
homepage: https://docs.heygen.com/reference/video-translate
allowed-tools: Bash, WebFetch, Read, Write, mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# HeyGen Video Translation

Translate and dub an existing video into 175+ languages. The system clones the
presenter's voice into the target language, re-syncs their lips to the new
audio, and returns a fully dubbed video. You provide a source video and a target
language — the engine handles transcription, translation, voice cloning,
lip-sync, and (optionally) burned-in captions.

This is **not** new-video generation. The presenter, performance, framing, and
brand assets in the original video are preserved. Translation rides on top of
what's already there.

## User-Facing Behavior

1. **Be concise.** Don't dump translation IDs, raw API payloads, or status JSON in chat. Report the result (video link, language) not the plumbing.
2. **No internal jargon.** Don't say "polling", "video_translation_id", "asset_id", "v3 endpoint". Say "translating", "almost done", "your file".
3. **Polling is silent.** Background long-running translations and only speak on (a) result delivered, (b) >5 min stall (one update), (c) hard failure.
4. **One result, one message.** When the video is done, send the link plus a one-line summary (target language, duration, mode). Not every API field.
5. **Don't narrate transport choice.** MCP vs CLI vs OpenClaw plugin is internal. Pick silently at session start; never mention which is in use.
6. **Communicate in the user's language.** Detect from their first message. Replies, confirmations, and questions in their language. Technical CLI/API directives stay in English.

## API Mode Detection

**Pick one transport at session start. Never mix, never switch mid-session, never narrate the choice.**

Detect in this order:

1. **OpenClaw plugin mode** — If running inside OpenClaw and the `video_generate` tool exposes a HeyGen translation model, prefer that. *Currently the plugin generates videos but does not expose translation directly — fall through to the next tier until HeyGen ships translation through `video_generate`.*
2. **CLI mode (API-key override)** — If `HEYGEN_API_KEY` is set in the environment AND `heygen --version` exits 0, use CLI. API-key presence is an explicit signal that the user wants direct API access.
3. **MCP mode** — No `HEYGEN_API_KEY` AND HeyGen MCP tools are visible (`mcp__heygen__*`). OAuth auth, runs against the user's plan credits.
4. **CLI mode (fallback)** — MCP tools not available AND `heygen --version` exits 0. Auth via `heygen auth login`.
5. **Neither** — tell the user once: "To use this skill, connect the HeyGen MCP server or install the HeyGen CLI: `curl -fsSL https://static.heygen.ai/cli/install.sh | bash` then `heygen auth login`."

**Hard rules:**

- **Never call `curl api.heygen.com/...`** Every operation in this skill has a CLI command and (where supported) an MCP tool. Use those.
- **MCP mode: only `mcp__heygen__*` tools.** If translation isn't exposed via MCP yet, fall through to CLI for translation operations specifically. Do not synthesize raw HTTP calls.
- **CLI mode: only `heygen ...` commands.** Run `heygen video-translate --help` and `heygen video-translate <subcommand> --help` to discover arguments. Use `--request-schema` to see the full JSON shape of any create command.
- **Operations below show MCP and CLI side-by-side** — read only the column for your detected mode.

### MCP tool names (MCP mode only)

`create_video_translation` (single language). Multi-language and proofreads are
not yet exposed via MCP — fall through to CLI for those. Run `mcp__heygen__*`
tool listing at session start to confirm what's available; tool surface evolves.

### CLI command groups (CLI mode only)

```
heygen video-translate
├── languages list              # supported target languages
├── create                      # submit a translation job (single or batch)
├── get <id>                    # check status / fetch result
├── list                        # list past translations
├── update                      # update job metadata
├── delete                      # delete a job
└── proofreads
    ├── create                  # extract editable subtitles before final render
    ├── get <id>                # check proofread session status
    ├── srt get <id>            # download the extracted SRT
    ├── srt update <id>         # upload edited SRT
    └── generate <id>           # render the final video from approved SRT
heygen asset create --file <path>   # for local source video uploads (max 32 MB)
```

Every command supports `--help`. Use `--request-schema` on any `create` to see the full JSON body. CLI output: JSON on stdout, `{error:{code,message,hint}}` envelope on stderr, exit codes `0` ok · `1` API · `2` usage · `3` auth · `4` timeout. Add `--wait` on `create` to block until the job completes (default timeout 20m).

📖 **Detailed CLI/MCP error → action mapping → [references/troubleshooting.md](references/troubleshooting.md)**

---

## Default Workflow

The skill runs four phases. Phase 1 (Discovery) is the only place you ask questions. Phase 2 (Pre-flight) is silent. Phase 3 (Submit + Poll) is silent. Phase 4 (Deliver) is one short message.

```
Phase 1 — Discovery       — gather minimum needed inputs from the user
Phase 2 — Pre-flight      — validate language, classify content, set flags
Phase 3 — Submit + Poll   — kick off, background poll, surface only on done/fail
Phase 4 — Deliver         — post the result with one-line summary
```

### Phase 1 — Discovery

Ask only what you don't already have. Communicate in the user's language. **Never run a form.** One or two questions per turn, max.

**Required inputs (block until you have these):**

1. **Source video.** Public URL, local file path, or a HeyGen asset_id from a previous step. If the user hasn't supplied it, ask: *"What's the source video — a URL, file path, or an existing HeyGen asset?"*
2. **Target language(s).** Ask in the user's language: *"Which language should I translate it into?"* If they want multiple, accept a list. Validate each against the canonical languages list (see Phase 2).

**Important inputs (ask if not provided, with smart defaults):**

3. **Speaker count.** Single speaker is the default and what most users have. Ask once when ambiguous: *"How many distinct speakers are in the video?"* Wrong speaker count is the #1 quality killer — speaker confusion creates voice swaps mid-translation. Don't skip this for multi-person content.
4. **Content type.** You usually don't need to ask — infer from the video and confirm. The five profiles below cover ~95% of cases. Only ask if genuinely ambiguous.
5. **Caption preference.** Default ON for talking-head and corporate; default OFF for podcast/audio-only. If you flip the default, mention it briefly in Phase 4.

**Optional (ask only if relevant):**

6. **Glossary / do-not-translate terms.** For corporate or technical content, ask: *"Any product names, company names, or jargon I should keep in the original language?"* HeyGen doesn't currently accept a hard glossary, so this becomes guidance for the proofread step (Phase 3-Proofread) when stakes are high.
7. **Partial translation.** If the user mentions a specific segment ("just the intro", "from 1:30 to 4:00"), capture `start_time` and `end_time` in seconds.
8. **Proofread before final render?** Default OFF (faster, fewer approvals). Default ON for: long videos (>3 min), corporate/branded content, high-stakes legal/medical/educational, languages the user reads natively (so they can verify). Ask: *"Want to review and edit the subtitles before final render? Adds about 5 minutes but lets you fix any wrong terms."*

📖 **Locale-pair gotchas (formality registers, RTL languages, tonal compression, lip-sync ceiling) → [references/language-locale-guide.md](references/language-locale-guide.md)**

### Phase 2 — Pre-flight

Silent. No user-facing chatter. Three checks, in order.

**Check 2a: Language validation.**

**MCP:** `list_video_translation_languages()` (if exposed). Otherwise CLI.
**CLI:** `heygen video-translate languages list | jq -r '.data.languages[]'`

The list contains exact strings ("Spanish (Spain)", "Chinese (Mandarin, Simplified)", "Arabic (Saudi Arabia)"). Match the user's input case-insensitively against these exact strings. If they say "Spanish", default to "Spanish (Spain)" and confirm in Phase 4. If they say "Chinese", default to "Chinese (Mandarin, Simplified)". If they specify a region ("Mexican Spanish"), map it ("Spanish (Mexico)"). If no match: ask the user to pick from the closest options.

**Check 2b: Source video routing.**

| Source the user gave you | Route |
|--------------------------|-------|
| Public HTTPS URL (no auth, returns video MIME on `HEAD`) | Pass directly as `{type: "url", url: "..."}` |
| Auth-walled URL, 403, 404, or HTML response | Tell the user, ask for a public URL or local file |
| Local file path | Upload via `heygen asset create --file <path>` (CLI) or `upload_asset` (MCP). Max 32 MB. Use the returned `asset_id` as `{type: "asset_id", asset_id: "..."}` |
| Existing HeyGen asset_id | Pass directly as `{type: "asset_id", asset_id: "..."}` |

📖 **Asset routing edge cases (very large files, presigned URLs, auth-walled sources) → [references/asset-routing.md](references/asset-routing.md)**

**Check 2c: Content profile.**

Pick one profile based on the source. Don't list all five to the user — propose silently and only ask if the source is genuinely ambiguous (e.g., a music-heavy talking-head where you can't tell if speech enhancement will help).

| Profile | Use when | Flags |
|---------|----------|-------|
| **Talking head / presenter** (default) | One person speaks to camera; clean audio | `mode: precision`, `enable_speech_enhancement: true`, `enable_caption: true`, `enable_dynamic_duration: true`, `keep_the_same_format: true` |
| **Podcast / audio-only** | The visual is static, doesn't matter, or doesn't exist | `mode: precision`, `translate_audio_only: true`, `enable_speech_enhancement: true`, `enable_caption: true` |
| **Music / high-soundtrack** | Background music interferes with speech | `mode: precision`, `disable_music_track: true`, `enable_speech_enhancement: true`, `enable_dynamic_duration: true`, `keep_the_same_format: true` |
| **Multi-speaker** | Two or more distinct speakers | Talking-head defaults + `speaker_num: <count>`. Speaker count is REQUIRED here — don't guess. |
| **Corporate / branded** | Brand voice, glossary discipline, high-stakes | Talking-head defaults + (if user has one) `brand_voice_id`. Strongly consider proofreads for this profile. |

**Always:**
- `mode: "precision"` unless the user explicitly asks for "fast" / "quick" / "speed".
- `enable_dynamic_duration: true` for visual translations — lets translated speech breathe instead of being crammed into the source's exact timing. Tonal compression makes this critical for en→zh, en→ja, en→ko (Asian languages run shorter); de→en, ja→en (run longer); ar/he/ur (RTL + register shifts).
- `keep_the_same_format: true` for visual translations — preserves the source's resolution and bitrate so the dubbed video matches the original's encoding.
- `enable_watermark: false` (the default).

### Phase 3 — Submit + Poll

Silent. Background work. Surface only on (a) per-language completion, (b) per-language hard failure, (c) >5 min progress check.

**Branching:**

- **Standard path** (proofread = OFF): submit translations, background-poll, deliver.
- **Proofread path** (proofread = ON): create proofread session → download SRT → user edits or you assist → upload edited SRT → generate final → background-poll → deliver.

#### Standard path

Submit one job per target language using batch syntax (`--output-languages` accepts multiple).

**MCP** *(single language only at time of writing)*:
```
create_video_translation(
  video={type, url|asset_id},
  output_languages=["Spanish (Spain)"],
  mode="precision",
  enable_speech_enhancement=true,
  enable_caption=true,
  enable_dynamic_duration=true,
  keep_the_same_format=true,
  speaker_num=<n>,           # only when known multi-speaker
)
```

**CLI:**
```bash
heygen video-translate create \
  -d '{"video":{"type":"url","url":"https://..."},"output_languages":["Spanish (Spain)","Japanese (Japan)"]}' \
  --mode precision \
  --enable-speech-enhancement \
  --enable-caption \
  --enable-dynamic-duration \
  --keep-the-same-format \
  --speaker-num 1 \
  --title "<short title>"
```

Response returns one `video_translation_id` per language. Capture all of them.

**Polling (silent, backgrounded):**

Use `--wait` on `create` to block until completion when running ONE language. For batch, drop `--wait` and poll each ID:

```bash
# CLI mode polling (background)
heygen video-translate get <video-translation-id>
# Returns { data: { status: "pending"|"running"|"succeeded"|"failed", video_url, ... } }
```

Polling cadence: 30s for the first 3 minutes, then 60s. Most translations complete in 5–15 min; some (long videos, batched languages) take 30+ min. Hard timeout: 60 min per translation — beyond that, treat as stuck and surface the issue.

**MCP equivalents:** `get_video_translation(id)` (if exposed). Otherwise fall through to CLI for polling.

📖 **Background polling pattern (don't poll in foreground / harness-specific notes) → [references/troubleshooting.md#polling](references/troubleshooting.md)**

#### Proofread path

For high-stakes content, run a proofread session first so the user can review/edit the translated subtitles before the engine commits to a final render.

```bash
# 1. Create proofread session — extracts editable subtitles per language
heygen video-translate proofreads create \
  -d '{"video":{"type":"url","url":"https://..."},"output_languages":["Spanish (Spain)"]}' \
  --mode precision \
  --enable-speech-enhancement \
  --keep-the-same-format \
  --title "<short title>"

# 2. Wait for the session to extract subtitles
heygen video-translate proofreads get <proofread-id>

# 3. Download the SRT for review
heygen video-translate proofreads srt get <proofread-id> > /tmp/proofread.srt

# 4. User edits /tmp/proofread.srt (or you assist with glossary corrections,
#    name preservation, register fixes — see references/proofreads-workflow.md)

# 5. Upload the corrected SRT
heygen video-translate proofreads srt update <proofread-id> \
  -d '{"srt":{"type":"url","url":"file:///tmp/proofread.srt"}}'
# (or upload via heygen asset create then reference asset_id)

# 6. Render final
heygen video-translate proofreads generate <proofread-id> --captions
```

📖 **When to insist on proofread, common SRT edits, glossary discipline → [references/proofreads-workflow.md](references/proofreads-workflow.md)**

### Phase 4 — Deliver

One message per completed language. Format:

> ✅ Spanish (Spain) — <video_url>
> 1m 47s, precision mode, captions on.

If a language failed: one short line with the cause (from troubleshooting reference). Don't flood the user with retry options unless they ask. If the user batched many languages, deliver each as it completes — don't wait for all to finish before posting any.

**Source-quality disclaimer.** Translation can't improve on the source. If the source has muffled audio, fast cuts, heavy occlusion of the face, or low resolution, lip-sync and voice quality will degrade. When you detect these conditions in Phase 2 (or the user mentions them), warn upfront. Don't surface this *after* a bad result.

---

## Embedded Expertise

The defaults above cover the common case. The decisions below are what separate this skill from a generic API wrapper. Use them as judgement calls during the workflow, not as a checklist to recite.

### Speaker count is the #1 quality killer

For talking-head: 1 speaker. For interviews / podcasts / panels: count exactly, don't guess. The engine separates voices by `speaker_num`; wrong count means voices bleed across speakers in the dubbed output. If the user is unsure, ask them to scrub the video and count.

### Source-quality triage (do this before submitting)

A 30-second triage in Phase 2 saves 10–30 minutes of bad translation. Watch/listen to the first ~10 seconds of the source and check:

- **Audio:** Is the speech clear? Background music dominant? Noise / hiss? → if speech is unclear, default `enable_speech_enhancement: true`. If music dominates, `disable_music_track: true`. If both, warn the user that quality may be lower regardless of flags.
- **Face visibility:** Is the speaker's face on-camera most of the time, front-facing, well-lit? → heavy occlusion (sunglasses, hands on face), profile-only shots, very fast cuts, or sub-720p faces all cap lip-sync quality.
- **Text on screen:** Burned-in captions in the source language? → these don't get re-rendered. They'll remain in the source language in the dubbed output. If the user wants new-language captions, they'll have two caption tracks — propose `enable_caption: true` AND warn about the existing burn-in.

### Locale-pair gotchas

- **Tonal compression / expansion.** en→zh, en→ja, en→ko run ~30% shorter; de→en, ja→en run longer; en→ar/he typically expands. Always `enable_dynamic_duration: true` so the dub doesn't feel rushed or stretched. Without this flag, en→zh sounds artificially slow (speech crammed to fit a 30%-too-long timeline).
- **Formality / register.** ja-JP (敬語/keigo), ko-KR (honorifics), de-DE (Sie vs du), th-TH (royal/polite/casual), id-ID (formal vs colloquial) — the engine picks neutral-formal by default. If the source is conversational and the user wants matching register in target, flag it in proofread or pre-warn that it'll sound slightly more formal than the original.
- **RTL languages.** Arabic, Hebrew, Urdu, Persian — captions render right-to-left. Burned-in captions can collide with the source video's lower-third graphics on the wrong side. If the source has on-screen text or graphics in the lower-third, propose audio-only translation OR proofread with caption styling review.
- **Regional variants matter.** Spanish (Spain) vs Spanish (Mexico) vs Spanish (Argentina) have distinctly different vocabulary, intonation, and speech rate. Latin American audiences often perceive Castilian Spanish as foreign. Default to the user's stated audience region; if unspecified for Spanish, ask once. Same for Portuguese (Portugal vs Brazil), French (France vs Canada vs Switzerland), Arabic (which has 19 region variants).
- **Mandarin specifically.** "Chinese (Mandarin, Simplified)" is the standard default for mainland China audiences. "Chinese (Cantonese, Traditional)" for Hong Kong / overseas Cantonese-speaking diaspora. "Chinese (Taiwanese Mandarin, Traditional)" for Taiwan. These are not interchangeable.

📖 **Full locale-pair table with register notes and known quirks → [references/language-locale-guide.md](references/language-locale-guide.md)**

### Lip-sync ceiling

Lip-sync is best on:
- Stable, front-facing shots
- ≥720p face resolution
- Clean, well-lit faces
- Minimal cuts (long takes work better)

Lip-sync degrades on:
- Profile shots, looking-down shots, partial-face occlusion
- Fast cuts (<2s shots)
- Low light, motion blur, or low-res faces
- Heavy gesturing where the face moves rapidly

If the user's source has these conditions, warn them in Phase 1/2: *"Heads up — the source has [X], so lip-sync won't be as tight as it would on a static talking-head. Want me to proceed anyway, or switch to audio-only translation?"*

### Captions: burned-in vs sidecar

`enable_caption: true` produces captions burned into the video by default. Pros: no separate file, plays anywhere. Cons: not editable later, can collide with source graphics, fixed font/style. For high-stakes content where the user might want to restyle captions (brand kit, language-specific font), prefer the proofreads workflow — it gives an SRT they can use as a sidecar caption file.

### Audio-only translation

`translate_audio_only: true` skips lip-sync entirely. Use it for:
- Podcasts (the "video" is a static image or waveform)
- Audio you'll re-composite into a different video later
- Any case where lip-sync would be impossible (no face, very poor source face quality)

Output is an audio file (typically MP3). Tell the user how to use it: *"This gives you a translated audio track. Composite it back over the original video in your editor, or use it standalone."* Do NOT pitch audio-only as a "quality workaround" for bad lip-sync — it's a different deliverable.

### Cost & time awareness

Translations bill by source video duration. A 5-minute video translated into 5 languages = 25 billable minutes. Surface time and cost expectations in Phase 1 when the user requests batches: *"That's 5 languages × 5 minutes = ~25 min of translation time. Each one will take 10–20 min to render. Sound good?"*

Don't quote dollar figures (pricing changes, varies by plan). Quote source minutes × language count, plus an honest render-time range.

### Failure-mode decoder

Common error responses → human-readable causes → next action:

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `400` "video URL not accessible" | URL requires auth, returned HTML, or wrong MIME | Ask for public URL or local file → upload route |
| `400` "language not supported" | String didn't match canonical languages list | Re-run `languages list`, present closest matches |
| `failed` status with "audio extraction" | Source has no audible speech, very corrupted audio, or wrong codec | Verify the source has speech; consider re-encoding |
| `failed` with "speaker detection" | `speaker_num` mismatched actual speakers, or audio is too noisy | Re-submit with correct speaker count or `enable_speech_enhancement: true` |
| Stuck >30 min in `running` | Backend queue / occasional stalls | Check status, give it 60 min total, then surface to user |
| Lip-sync looks bad on output | Source face conditions (see lip-sync ceiling) | Re-frame expectation; offer audio-only as alternative |
| Captions in wrong direction | RTL language with burned-in caption colliding with source layout | Switch to proofread + sidecar SRT |

📖 **Full error → action table including auth and asset upload errors → [references/troubleshooting.md](references/troubleshooting.md)**

---

## First-Time User Detection

Signals the user is new to HeyGen translation specifically:
- Asks "what languages do you support?"
- Doesn't know about lip-sync vs audio-only
- Hasn't used HeyGen before (no avatars, no past translations on `heygen video-translate list`)

For first-timers, suggest a 30–60 second test clip before committing to a full video. This catches source-quality issues, voice-clone fidelity, and lip-sync ceiling without burning a long-video translation.

## Source Quality Disclaimer (verbatim, for delivery)

When the source is borderline:

> "Heads up — the source video has [muffled audio / dim lighting / fast cuts / heavy music / etc.]. The translation engine can't improve on the source, so the dub might inherit some of that. Want to proceed, fix the source first, or test with a short clip?"

Don't surface this *after* a bad result. Surface it in Phase 2.

## Phase 2 / Roadmap (mention only if asked)

Currently best-supported via the proofreads workflow but not yet first-class flags:

- **Brand glossary / do-not-translate lists.** Inject during proofread by reverting auto-translated terms in the SRT. The `brand_voice_id` flag is for voice consistency across translations, not for glossaries.
- **Custom SRT input.** Supported via `srt` field (Enterprise plan) on `create`, or via `proofreads srt update` for any plan. Use `srt_role: "input"` to apply YOUR subtitles to the source language; `output` to apply them as the target-language captions.
- **Partial translation.** `start_time` / `end_time` in seconds. Useful for "translate just minute 2:00–4:00".
- **Multi-language batch.** Already supported — pass multiple values to `--output-languages` (CLI) or `output_languages` array (MCP). One job ID returned per language.
- **Webhook callbacks.** `--callback-url` and `--callback-id` skip polling entirely. Use when you have a webhook endpoint and want event-driven completion.

## Best Practices (the short version)

1. **Always precision mode** unless the user explicitly asks for speed.
2. **Always confirm speaker count** for non-obvious cases.
3. **Validate the language string** against the canonical list before submitting.
4. **Suggest a short test clip for new users.**
5. **Source quality is the ceiling** — say it upfront, not after.
6. **Don't over-configure** — the five content profiles cover ~95% of cases.
7. **Translations take time** — set 5–30 min expectations.
8. **Match register** — if the source is conversational and the target is a register-heavy language (ja, ko, th, de), proofread.
9. **Default proofread ON for: long videos, corporate, languages the user reads natively.**
10. **Never narrate transport.** MCP vs CLI is internal.
