---
name: video-translate
description: |
  Translate and dub existing videos into 40+ languages with lip-sync using HeyGen's v3 Video Translation API. Use when: (1) Translating a video into another language, (2) Dubbing video content with lip-sync and voice cloning, (3) Creating multi-language versions of existing videos, (4) Audio-only translation for podcasts or manual compositing, (5) Working with HeyGen's /v3/video-translations endpoints, (6) Localizing presenter, corporate, or marketing videos.
homepage: https://docs.heygen.com/reference/video-translate
allowed-tools: mcp__heygen__*
metadata:
  openclaw:
    requires:
      env:
        - HEYGEN_API_KEY
    primaryEnv: HEYGEN_API_KEY
---

# Video Translation

Translate and dub existing videos into 40+ languages. HeyGen clones the speaker's voice into the target language, re-syncs lip movements, and returns a fully dubbed video. You provide a video URL and a target language — the system handles transcription, translation, voice synthesis, and lip-sync automatically.

## Authentication

All requests require the `X-Api-Key` header.

**Before claiming the key is missing, resolve it in this order:**

1. `$HEYGEN_API_KEY` environment variable (takes precedence)
2. `~/.heygen/config` file — persistent storage written by `./setup`. Load it with:
   ```bash
   export HEYGEN_API_KEY=$(grep '^HEYGEN_API_KEY=' ~/.heygen/config | cut -d= -f2-)
   ```
   Or source in-process (no `source` — the file isn't a full shell script):
   ```bash
   HEYGEN_API_KEY=$(awk -F= '/^HEYGEN_API_KEY=/{print $2}' ~/.heygen/config)
   ```
3. Only if both are empty: tell the user "No API key found. Run `./setup` in the heygen-skills directory, or `export HEYGEN_API_KEY=<your-key>`."

Do NOT stop and ask the user to re-export if `~/.heygen/config` exists — load it and proceed.

### Shell hygiene (read this before your first curl)

These bite every time and look like API failures when they aren't:

1. **Env vars do NOT persist across `Bash` tool calls.** Claude Code spawns a fresh shell for each call. An `export` from one call is gone by the next. **Inline the auth load in every curl call**, like this:

   ```bash
   [ -z "$HEYGEN_API_KEY" ] && [ -f ~/.heygen/config ] && \
     export HEYGEN_API_KEY=$(grep '^HEYGEN_API_KEY=' ~/.heygen/config | cut -d= -f2-)
   curl -sS "https://api.heygen.com/v3/video-translations/languages" \
     -H "X-Api-Key: $HEYGEN_API_KEY"
   ```

   If you skip the prefix, you get HTTP 401 unauthorized — which looks like a key problem but is actually a shell-state problem.

2. **zsh "no matches found" = a glob char wasn't quoted.** zsh expands `?`, `*`, `[…]` in unquoted arguments and aborts when no file matches. URLs with query strings (`?foo=bar`) and jq filters (`.[]`) both trip this. Always single-quote URLs and jq expressions:

   ```bash
   # bad — zsh tries to glob the URL
   curl -sS https://api.heygen.com/v3/videos/abc?lang=es

   # good
   curl -sS 'https://api.heygen.com/v3/videos/abc?lang=es'
   curl -sS "$URL" | jq -r '.languages[]'   # jq filter in single quotes
   ```

3. **Don't burn approvals on diagnostics.** If a curl fails, do not run a second curl just to confirm the env var is empty. Read the error: 401 = no/bad key, jq error = wrong response shape, "no matches" = unquoted glob.

```bash
curl -sS "https://api.heygen.com/v3/video-translations/languages" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Default Workflow

Translation quality depends heavily on choosing the right flags for the content type. Don't present users with a wall of boolean options — identify what kind of video they have and set flags accordingly.

### Intake rules (how to ask, not just what)

**Ask one question at a time. Wait for the answer. Then ask the next.** Do not present a numbered list of 3+ questions in a single message — that's a form, not a conversation, and users bounce off it.

**Extract before asking.** If the user's first message already answers a question (e.g. "translate https://youtu.be/xyz into Spanish"), skip that question. Only ask what's still missing.

**Validate inline.** When you get a URL, run the HEAD check before moving to the next question — don't defer it. If the language is unsupported, surface that immediately.

**Offer sensible defaults.** For content type and speaker count, suggest the most likely answer based on context and let the user confirm or correct. Example: "Looks like a talking-head video — single speaker? (yes / no / other)".

Turn order (each turn = one question + one answer):

1. **Source** — "Where's the video? URL, local file path, or HeyGen asset ID?" → immediately sanity-check URLs with `curl -sI`; offer local-upload fallback if the URL fails.
2. **Target language** — "What language should I translate it to?" → validate against `/v3/video-translations/languages` before proceeding.
3. **Content type** — propose the likely profile based on what you know. "This looks like a talking-head video — that right?" Accept a short confirmation. Only fall back to the full menu if the user says "no" or "other".
4. **Speaker count** — "How many speakers are in the video?" Ask even for experienced users; wrong speaker count degrades voice separation.

If everything above was supplied in the first message, skip straight to the dry-run confirmation ("Ready to translate <title> into <lang> with <profile>, <N> speakers — go?") and submit on yes.

### Narrate before each Bash call

Before running any `Bash` / `curl` call (URL sanity check, asset upload, language list, translation submit, background poll, status check), state in **one short sentence** what you're trying to achieve. The user only sees the command name and a truncated argument list in the tool-call header — they need a one-liner from you to know *why* it's running and what to expect from the result.

Examples:
- "Sanity-checking the URL with a HEAD request before submission."
- "Uploading the local file to HeyGen — this returns an asset_id."
- "Validating that Spanish and Mandarin are in the supported languages list."
- "Submitting the translation request — should return 2 translation IDs."
- "Spawning 2 background poll loops — you'll see 2 approval prompts, one per language."

This applies to background `Bash` calls too — don't dump three `run_in_background` approvals on the user without a single sentence explaining what each one is for.

### Step 0: Determine the video source

Three paths:

**Hosted URL** (YouTube, Google Drive, direct link) — verify first, then pass:

Before submitting, sanity check the URL with a HEAD request:
```bash
curl -sI "https://example.com/video.mp4" | head -1
```
Verify: (1) status is 200 or 206, (2) `Content-Type` starts with `video/` or `audio/` (not `text/html` — that's an error page or auth wall), (3) if `Content-Length` is present, it's a reasonable file size (not a few hundred bytes).

If the URL isn't publicly accessible (403, 404, wrong content type), tell the user and offer to download the file locally and upload it via the local file path instead.

```json
{ "video": { "type": "url", "url": "https://example.com/video.mp4" } }
```

**Local file** — upload to HeyGen first, then reference by asset ID:
```bash
curl -X POST "https://api.heygen.com/v3/assets" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -F "file=@/path/to/local-video.mp4"
```
Response returns `asset_id`. Then:
```json
{ "video": { "type": "asset_id", "asset_id": "<returned asset_id>" } }
```
Note: max upload size is 32 MB via this endpoint.

**Existing HeyGen asset** — use the asset ID directly:
```json
{ "video": { "type": "asset_id", "asset_id": "existing_asset_id" } }
```

### Step 1: Validate the target language

Call the languages endpoint to confirm the target language is supported before doing anything else. This avoids wasted time on unsupported language pairs.

### Step 2: Identify content type and set flags

Map the user's content to one of these profiles. Propose the most likely profile first rather than listing all four — only surface the menu if the user declines your guess.

**Talking head / presenter video** (the common case):
```json
{
  "mode": "precision",
  "enable_speech_enhancement": true,
  "enable_caption": true,
  "enable_dynamic_duration": true,
  "keep_the_same_format": true
}
```

**Podcast / audio-heavy content** (no visual lip-sync needed):
```json
{
  "mode": "precision",
  "translate_audio_only": true,
  "enable_speech_enhancement": true,
  "enable_caption": true
}
```

**Video with prominent soundtrack** (music interferes with speech):
```json
{
  "mode": "precision",
  "disable_music_track": true,
  "enable_speech_enhancement": true,
  "enable_dynamic_duration": true,
  "keep_the_same_format": true
}
```

**Corporate / branded content** (brand voice consistency):
```json
{
  "mode": "precision",
  "brand_voice_id": "<ask user for brand voice ID>",
  "enable_caption": true,
  "enable_dynamic_duration": true,
  "keep_the_same_format": true
}
```

### Step 3: Create the translation

`POST /v3/video-translations` with the video source and flags from the content profile above.

### Step 4: Poll for completion (backgrounded bash)

> ⛔ **POLLING RULE:** The main session MUST NOT poll in the foreground. After `POST /v3/video-translations` returns translation IDs, run **one backgrounded `Bash` call per translation ID**. Each call contains the entire soak + poll loop in a single shell script, so the user approves once per language, not once per curl.

> 🚫 **Do NOT use `Agent` subagents for polling.** Tried and rejected — subagents in Claude Code can't inherit the parent session's Bash approvals, so every curl inside them fails on permission denial. Backgrounded bash works because it runs in the main session's permission scope.

**Step 4a: Set expectations BEFORE submitting any background polls.** Tell the user upfront:

> "I need an approval for each submitted translation — that's N prompts coming up, one per language. After you approve them, polling runs silently in the background and I'll surface results as each one finishes (5–30 min)."

Don't surprise the user with a wall of approval prompts. One sentence of warning is enough.

**Step 4b: Main session submits the translation request** — one `POST /v3/video-translations` with `output_languages` array. Response returns `video_translation_ids[]`, one ID per target language.

**Step 4c: Launch one backgrounded bash poll per translation ID.** Send a single message with N `Bash` tool calls, each with `run_in_background: true`. The user gets N approval prompts (one per language) at this moment — that's the cost we accept. After approval, each loop runs unattended.

Script template (substitute `<TRANSLATION_ID>` and `<LANG>`):

```bash
# Load API key (env wins, else ~/.heygen/config)
[ -z "$HEYGEN_API_KEY" ] && [ -f ~/.heygen/config ] && \
  export HEYGEN_API_KEY=$(grep '^HEYGEN_API_KEY=' ~/.heygen/config | cut -d= -f2-)

ID="<TRANSLATION_ID>"
LANG="<LANG>"

# Soak: translations almost never finish under 5 min
sleep 300

# Tight poll until terminal.
# NOTE: use `st`, not `status`. In zsh, $status is read-only (mirrors $?) and
# assignment aborts the script silently. Rename here propagates to bash too.
START=$(date +%s)
while :; do
  resp=$(curl -sS "https://api.heygen.com/v3/video-translations/$ID" \
    -H "X-Api-Key: $HEYGEN_API_KEY")
  st=$(printf '%s' "$resp" | jq -r '.data.status')
  case "$st" in
    completed|failed)
      printf '=== %s (%s) ===\n%s\n' "$LANG" "$st" "$resp" | jq .
      exit 0
      ;;
  esac
  # 30s polls for the first 30 min, then 2-min intervals
  elapsed=$(( $(date +%s) - START ))
  [ $elapsed -lt 1800 ] && sleep 30 || sleep 120
done
```

**Step 4d: Wait for completion notifications.** The main session is notified when each background task exits. Do NOT poll the background tasks yourself. As each completes, render its per-language deliverable (Step 5) from the JSON in stdout.

**Parallel by default.** N translation IDs = N concurrent background polls. HeyGen pre-queues translations at submit, so concurrent polling causes no contention — no batching needed (unlike `heygen-video`'s batch-of-2-3 rule for video generation).

### Step 5: Deliver the result

For each completed translation, render this exact block. **Wrap signed URLs in markdown link syntax** — raw signed URLs are 200+ characters of query-string noise that ruins the output. Show only the short, stable dashboard URL as plain text.

```markdown
🇪🇸 <Language Name> — <title>

- **View online:** https://app.heygen.com/videos/<translation_id>
- **Direct video:** [Download .mp4](<video_url>)
- **Captions:** [SRT](<srt_caption_url>) · [VTT](<vtt_caption_url>)
- Duration: <duration>s
```

Rules:
- Lead with the View online link — it's the most useful output for most users (preview, share, re-download from the dashboard).
- Use a flag emoji for the language header (🇪🇸 Spanish, 🇨🇳 Mandarin, 🇰🇷 Korean, 🇯🇵 Japanese, etc.).
- Combine SRT and VTT on one line separated by `·` — they're two formats of the same captions.
- Mention caption-URL expiration ("signed URLs expire in ~7 days") **once per session, after the last block** — not on every translation.

## First-Time User Detection

Before creating a translation, check if the user has translated before by listing their recent translations. If they have no history:

1. Suggest trying a shorter segment first (under 2 minutes) to preview quality
2. Briefly explain what the system does: voice cloning, lip-sync, and caption generation
3. Mention the source quality disclaimer (below)

If they have translation history, skip onboarding and proceed directly.

## Source Quality Disclaimer

Always mention once per session, especially for first-time users:

> Translation works best with clear speech, minimal background noise, and visible faces for lip-sync. Noisy audio, fast overlapping speech, or heavily stylized visuals will degrade output quality.

## Supported Languages

Call the languages endpoint to get the current list. Do NOT hardcode language codes — the list updates as HeyGen adds support.

### curl

```bash
curl -X GET "https://api.heygen.com/v3/video-translations/languages" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### Response shape

```json
{
  "languages": [
    "Afrikaans (South Africa)",
    "Spanish",
    "Spanish (Mexico)",
    "Japanese",
    "..."
  ]
}
```

Top-level `languages` array of human-readable strings. **No** `data` wrapper, **no** `{ code, name }` objects. Pass these strings verbatim as `output_languages` when creating a translation.

### TypeScript

```typescript
interface LanguagesResponse {
  languages: string[];
}

async function getSupportedLanguages(): Promise<string[]> {
  const response = await fetch(
    "https://api.heygen.com/v3/video-translations/languages",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: LanguagesResponse = await response.json();
  return json.languages;
}
```

### Python

```python
import requests
import os

def get_supported_languages() -> list[str]:
    response = requests.get(
        "https://api.heygen.com/v3/video-translations/languages",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    )

    return response.json()["languages"]
```

### jq quick-checks

```bash
# all languages
curl -sS "https://api.heygen.com/v3/video-translations/languages" \
  -H "X-Api-Key: $HEYGEN_API_KEY" | jq -r '.languages[]'

# filter for a specific name (case-insensitive)
curl -sS "https://api.heygen.com/v3/video-translations/languages" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  | jq -r '.languages[] | select(test("spanish"; "i"))'
```

## Create Translation

### Endpoint

`POST https://api.heygen.com/v3/video-translations`

### Request Fields

| Field | Type | Req | Description |
|-------|------|:---:|-------------|
| `video` | object | Y | Source video: `{ "type": "url", "url": "..." }` or `{ "type": "asset_id", "asset_id": "..." }` |
| `output_languages` | string[] | Y | Target language names from the languages endpoint. Array — supports multiple languages in one call |
| `mode` | string | | `"precision"` (recommended) or `"speed"`. Always use precision |
| `speaker_num` | number | | Number of speakers in the video. Always ask the user |
| `title` | string | | Name for the translated video |
| `translate_audio_only` | boolean | | Audio-only output, no lip-sync. For podcasts or manual compositing |
| `enable_speech_enhancement` | boolean | | Improve audio clarity. On by default in all profiles |
| `enable_caption` | boolean | | Generate captions in target language |
| `enable_dynamic_duration` | boolean | | Allow output duration to flex for natural pacing |
| `keep_the_same_format` | boolean | | Preserve source video format/resolution |
| `disable_music_track` | boolean | | Strip background music that interferes with speech |
| `brand_voice_id` | string | | Brand voice ID for consistent voice across translations |
| `enable_watermark` | boolean | | Add HeyGen watermark. Leave off |
| `callback_url` | string | | Webhook URL for completion notification |
| `callback_id` | string | | Custom ID for webhook tracking |

Input language is auto-detected — don't require the user to specify it.

### curl

```bash
curl -X POST "https://api.heygen.com/v3/video-translations" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video": { "type": "url", "url": "https://example.com/presenter-video.mp4" },
    "output_languages": ["Spanish"],
    "mode": "precision",
    "speaker_num": 1,
    "enable_speech_enhancement": true,
    "enable_caption": true,
    "enable_dynamic_duration": true,
    "keep_the_same_format": true,
    "title": "Spanish Version"
  }'
```

### TypeScript

```typescript
type VideoSource =
  | { type: "url"; url: string }
  | { type: "asset_id"; asset_id: string };

interface VideoTranslateRequest {
  video: VideoSource;
  output_languages: string[];
  mode?: "precision" | "speed";
  speaker_num?: number;
  title?: string;
  translate_audio_only?: boolean;
  enable_speech_enhancement?: boolean;
  enable_caption?: boolean;
  enable_dynamic_duration?: boolean;
  keep_the_same_format?: boolean;
  disable_music_track?: boolean;
  brand_voice_id?: string;
  enable_watermark?: boolean;
  callback_url?: string;
  callback_id?: string;
}

interface VideoTranslateResponse {
  data: {
    video_translation_ids: string[];
  };
}

async function createTranslation(config: VideoTranslateRequest): Promise<string[]> {
  const response = await fetch(
    "https://api.heygen.com/v3/video-translations",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    }
  );

  const json: VideoTranslateResponse = await response.json();
  return json.data.video_translation_ids;
}

// Talking head / presenter (the common case)
const ids = await createTranslation({
  video: { type: "url", url: "https://example.com/presenter.mp4" },
  output_languages: ["Spanish"],
  mode: "precision",
  speaker_num: 1,
  enable_speech_enhancement: true,
  enable_caption: true,
  enable_dynamic_duration: true,
  keep_the_same_format: true,
});
```

### Python

```python
import requests
import os

def create_translation(config: dict) -> list[str]:
    response = requests.post(
        "https://api.heygen.com/v3/video-translations",
        headers={
            "X-Api-Key": os.environ["HEYGEN_API_KEY"],
            "Content-Type": "application/json",
        },
        json=config,
    )

    data = response.json()
    return data["data"]["video_translation_ids"]


# Talking head / presenter (the common case)
translation_ids = create_translation({
    "video": {"type": "url", "url": "https://example.com/presenter.mp4"},
    "output_languages": ["Spanish"],
    "mode": "precision",
    "speaker_num": 1,
    "enable_speech_enhancement": True,
    "enable_caption": True,
    "enable_dynamic_duration": True,
    "keep_the_same_format": True,
})
```

### Response Format

Returns one translation ID per target language:

```json
{
  "data": {
    "video_translation_ids": ["vt_abc123def456"]
  }
}
```

## Check Translation Status

### Endpoint

`GET https://api.heygen.com/v3/video-translations/{id}`

States: `pending` -> `running` -> `completed` | `failed`

Poll every ~30 seconds. `completed` and `failed` are terminal states.

### curl

```bash
curl -X GET "https://api.heygen.com/v3/video-translations/{video_translate_id}" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface TranslationStatus {
  data: {
    id: string;
    status: "pending" | "running" | "completed" | "failed";
    video_url?: string;
    message?: string;
  };
}

async function getTranslationStatus(id: string): Promise<TranslationStatus["data"]> {
  const response = await fetch(
    `https://api.heygen.com/v3/video-translations/${id}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: TranslationStatus = await response.json();
  return json.data;
}
```

### Python

```python
import requests
import os

def get_translation_status(translate_id: str) -> dict:
    response = requests.get(
        f"https://api.heygen.com/v3/video-translations/{translate_id}",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    )

    data = response.json()
    return data["data"]
```

### Response Format (completed)

```json
{
  "data": {
    "id": "vt_abc123def456",
    "status": "completed",
    "title": "Spanish Version",
    "output_language": "Spanish",
    "input_language": "English",
    "duration": 65.4,
    "video_url": "https://resource.heygen.ai/video_translate/...",
    "audio_url": "https://resource.heygen.ai/video_translate/.../audio.mp3",
    "srt_caption_url": "https://resource.heygen.ai/.../captions.srt",
    "vtt_caption_url": "https://resource.heygen.ai/.../captions.vtt"
  }
}
```

### Response Format (failed)

```json
{
  "data": {
    "id": "vt_abc123def456",
    "status": "failed",
    "failure_message": "Insufficient audio quality for translation"
  }
}
```

## Flag Guidance

These are encoded into the content-type profiles above. Don't present them as a checklist — use them when the situation calls for it.

- **`mode: "precision"`** — Always. The quality difference over "speed" is substantial and the time cost is negligible. Only use "speed" if the user explicitly asks for faster processing and accepts lower quality.

- **`enable_speech_enhancement`** — On by default. Only turn off if the source audio is studio-quality and the user reports the enhancement is degrading it.

- **`translate_audio_only`** — For audio-only output. Use for podcasts or when the user plans to composite the audio into a different video. This is NOT a quality workaround — it simply skips lip-sync because there's no visual component to match.

- **`disable_music_track`** — For videos where background music drowns out or interferes with speech. If the user mentions music in their video and translation quality is poor, suggest enabling this.

- **`enable_dynamic_duration`** — On for all visual translations. Lets the output video flex in duration so the translated speech sounds natural rather than being crammed into the original timing.

- **`enable_caption`** — On by default. Generates captions in the target language. Users rarely want this off.

- **`keep_the_same_format`** — On by default. Preserves the source video's format and resolution.

- **`enable_watermark`** — Off. Don't enable unless the user specifically asks.

## Phase 2 Features (Coming Soon)

These are on the roadmap but not fully supported in the current workflow. Mention them if the user asks, but set expectations that they're not production-ready yet:

- **`brand_voice_id`** — Use a consistent brand voice across all translations. Available via the corporate content profile above. The user needs to create a brand voice in HeyGen first.
- **Custom SRT** — Provide your own subtitle file instead of auto-generated captions.
- **Partial translation** — Translate only a segment of the video using `start_time` / `end_time` parameters.
- **Multi-language batch** — Translate to multiple languages in a single API call.

## Best Practices

1. **Always use precision mode** — the quality gap is large, the time difference is small
2. **Always ask speaker count** — even for experienced users. Wrong speaker count degrades voice separation and quality
3. **Validate the target language first** — call the languages endpoint before attempting translation
4. **Suggest a short test clip for new users** — a 30-60 second segment catches issues before committing to a full video
5. **Source quality is the ceiling** — translation cannot improve on noisy audio, muffled speech, or low-resolution faces
6. **Don't over-configure** — the content-type profiles above cover 90% of use cases. Only deviate when the user has a specific need
7. **Translations take time** — 5-30 minutes is normal. Set expectations upfront so users don't think it's stuck
