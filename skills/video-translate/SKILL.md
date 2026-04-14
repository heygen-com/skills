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

All requests require the `X-Api-Key` header. Set the `HEYGEN_API_KEY` environment variable.

```bash
curl -X GET "https://api.heygen.com/v3/video-translations/languages" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## Default Workflow

Translation quality depends heavily on choosing the right flags for the content type. Don't present users with a wall of boolean options — identify what kind of video they have and set flags accordingly.

### Step 0: Determine the video source

Ask the user where their video is. Three paths:

**Hosted URL** (YouTube, Google Drive, direct link) — pass directly:
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

Ask the user how many speakers are in the video, then map their content to one of these profiles:

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

### Step 4: Poll for completion

Check `GET /v3/video-translations/{id}` every ~30 seconds. Terminal states are `completed` and `failed`. Translations take longer than standard video generation — expect 5-30 minutes depending on video length.

### Step 5: Deliver the result

Return the translated video URL from the completed response.

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

### TypeScript

```typescript
interface Language {
  code: string;
  name: string;
}

interface LanguagesResponse {
  data: Language[];
}

async function getSupportedLanguages(): Promise<Language[]> {
  const response = await fetch(
    "https://api.heygen.com/v3/video-translations/languages",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: LanguagesResponse = await response.json();
  return json.data;
}
```

### Python

```python
import requests
import os

def get_supported_languages() -> list:
    response = requests.get(
        "https://api.heygen.com/v3/video-translations/languages",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]},
    )

    data = response.json()
    return data["data"]
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
