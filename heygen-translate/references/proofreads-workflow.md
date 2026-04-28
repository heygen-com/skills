# Proofreads Workflow

The proofreads endpoint extracts editable subtitles BEFORE the engine
commits to the final translated render. Use it for high-stakes content
where a re-translation would be expensive (time, plan credits,
disappointment) compared with the proofread overhead.

This page documents what the proofread CLI **actually performs**, verified
against the live `heygen video-translate proofreads` commands and the v3
HeyGen API as of skill v3.1.0. Where API docs and live behavior diverge,
this page reflects live behavior.

---

## What the proofread workflow does

Five subcommands and three resources:

```
heygen video-translate proofreads
├── create        POST /v3/video-translations/proofreads
├── get           GET  /v3/video-translations/proofreads/{id}
├── srt get       GET  /v3/video-translations/proofreads/{id}/srt
├── srt update    PUT  /v3/video-translations/proofreads/{id}/srt
└── generate      POST /v3/video-translations/proofreads/{id}/generate
```

Resource lifecycle:

```
   create                    srt get          srt update         generate
     |                          |                 |                  |
     v                          v                 v                  v
proofread session  ----->  edited SRT      replace SRT         video_translation_id
   (status:                  + original                          (continues as a
   processing→completed)     auto-extracted                      normal translation
                             transcript                          render — poll via
                                                                 video-translate get)
```

**Each language gets its own proofread_id.** Submitting `output_languages: ["Spanish", "French"]` returns two ids; each is reviewed and finalized independently.

---

## Step-by-step: what each command actually does

### `proofreads create`

**Inputs (per CLI `--request-schema`):**

- `video` (required): `{type: "url", url: "..."}` or `{type: "asset_id", asset_id: "..."}`
- `output_languages` (required): array of canonical language strings (e.g. `["Spanish"]`)
- `title` (required): short label that appears in the dashboard and in the downloaded SRT filename
- `mode`: `"speed"` or `"precision"` — `precision` is recommended; final render quality follows from this
- `speaker_num`: integer, sets diarization expectation
- `enable_speech_enhancement`, `disable_music_track`, `enable_video_stretching`, `keep_the_same_format`: booleans matching the same flags on `create`
- `brand_voice_id`: optional brand voice
- `folder_id`: optional project folder
- `srt`: OPTIONAL initial SRT to seed the proofread session — `{type:"url",url:"..."}` (asset_id route is also accepted by the schema but only specific media types upload via `heygen asset create` — see Caveats below)

**What the engine does after submission:**

1. Downloads the video.
2. Runs ASR on the source audio → produces an **original SRT** in the source language (this is fetched via `srt get` as `original_srt_url`).
3. Translates that SRT into each target language → produces an **editable SRT** per language (returned via `srt get` as `srt_url`).
4. Marks the proofread `status: completed`.

**No video render happens at this stage.** That's the point — all the upfront ASR + translation cost is paid, but no avatar inference / lip-sync work is done until you `generate`.

**Response (verified):**

```json
{
  "data": {
    "proofread_ids": ["b84c8e8d8a18418a8f6a001f8c8b2423-es"],
    "status": "processing"
  }
}
```

`status` is the **session-level submit status**, not per-id. Each id is then independently checked via `proofreads get`.

### `proofreads get`

**Inputs:** the proofread id.

**What it returns (verified, while `processing`):**

```json
{
  "data": {
    "created_at": 1777334587,
    "id": "8ce0fba6c1bf41339f991dcc0a0fc3e6-es",
    "output_language": "Spanish",
    "status": "processing",
    "title": "PR82 sintel proofread"
  }
}
```

**While `failed`:**

```json
{
  "data": {
    "created_at": 1777334317,
    "failure_message": "Your video's audio is missing or corrupted, please try with another video",
    "id": "b84c8e8d8a18418a8f6a001f8c8b2423-es",
    "output_language": "Spanish",
    "status": "failed",
    "title": "..."
  }
}
```

**While `completed`:** same shape as `processing`, just `status: "completed"`. `submitted_for_review` and `input_language` are nullable schema fields and may not appear on every response.

**Polling cadence (verified empirically):** typical extraction time for a 50-second source video is 3–5 minutes. Poll every 60 s after the first 30 s. Hard timeout: 30 min — beyond that, treat the session as stuck.

### `proofreads srt get`

**Inputs:** the proofread id (must be `completed`).

**What it returns (verified):**

```json
{
  "data": {
    "original_srt_url": "https://resource2.heygen.ai/video_translate/.../<title>_proofread_original.srt?...",
    "srt_url":          "https://resource2.heygen.ai/video_translate/.../<title>_proofread.srt?..."
  }
}
```

Both URLs are **presigned and short-lived**. Download immediately:

```bash
SRT_URL=$(heygen video-translate proofreads srt get "$PR_ID" \
  | jq -r '.data.srt_url')
curl -s "$SRT_URL" -o /tmp/proofread.srt
```

**`srt_url`** = the editable, target-language SRT that the engine produced. This is what you edit and re-upload.

**`original_srt_url`** = the engine's transcription of the source audio in the source language. Useful as ground-truth context when the user is verifying the translation against what was actually said in the source. NEVER upload this back as a target-language SRT — it'll fail or render the wrong language.

**Verified format of the SRT files:** standard SRT (UTF-8), well-formed timecodes, line numbers, separator blank lines. No HeyGen-proprietary format. Editable by hand, by sed, or by any subtitle tool.

Example (real output from a Sintel trailer test):

```
1
00:00:12,220 --> 00:00:14,320
¿Qué te trae a la tierra de los guardianes?

2
00:00:18,660 --> 00:00:19,900
Busco a alguien.
```

### `proofreads srt update`

**Inputs:**

- `proofread-id` as positional argument
- `srt` body: `{type: "url", url: "..."}` or `{type: "asset_id", asset_id: "..."}`

**Verified upload behavior:**

✅ **URL route works.** Host the edited SRT at any publicly reachable URL and pass `{type:"url", url:"..."}`.

⚠️ **`asset_id` route is currently blocked for SRT files.** `heygen asset create` only accepts `png, jpeg, mp4, webm, mp3, wav, pdf` — uploading an SRT (MIME `application/x-subrip`) returns:

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "Content type not supported application/x-subrip"
  }
}
```

This is true regardless of file extension (renaming `.srt` to `.txt` or `.mp3` does not bypass it — the server sniffs content). The `asset_id` route is in the request schema but you cannot currently produce a HeyGen `asset_id` for an SRT through the standard upload path. **Use the URL route.**

**Practical patterns for hosting the edited SRT:**

| Where the SRT lives | How to make it reachable |
|---------------------|--------------------------|
| Local file | Upload to S3 / Cloud Storage with public-read OR a presigned URL ≥2 h |
| GitHub gist | Use the raw URL: `https://gist.githubusercontent.com/<user>/<id>/raw/<file>.srt` |
| GitHub repo | Use the raw URL: `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>.srt` |
| Vercel / static host | Drop into `public/` and reference the absolute URL |
| Already-uploaded HeyGen presigned URL | The presigned URLs from `srt get` work for round-tripping, but they expire — use only for very short edit cycles |

The URL must return `Content-Type` of `application/x-subrip` or `text/plain` and the SRT body. Verify with `curl -sI "$URL"` before submitting.

**Response (verified):** the full proofread resource shape. The session is still `completed`; the SRT replacement takes effect immediately for the next `generate` call.

### `proofreads generate`

**Inputs:**

- `proofread-id` as positional argument
- `--captions` (default false): burn the corrected captions into the final video
- `--translate-audio-only` (default false): skip lip-sync, output dubbed audio only
- `--callback-url`, `--callback-id`: optional webhook for completion

**What the engine does:**

1. Reads the proofread session's current SRT (the most recently uploaded one).
2. Runs the actual translation render (precision-mode avatar inference + voice clone + lip-sync).
3. Returns a `video_translation_id` that is then polled via the regular `heygen video-translate get` (NOT `proofreads get` — at this point the resource graduates from "proofread" to "translation").

**Response (verified):**

```json
{
  "data": {
    "status": "processing",
    "video_translation_id": "10c0808c39d847c2b1412af252ce50b5-es"
  }
}
```

**After this call**, polling shifts to:

```bash
heygen video-translate get "$VID_ID"
```

…which returns the standard translation response shape (`status`, eventual `video_url`, `failure_message`, etc.).

---

## Full CLI walkthrough (verified end-to-end)

Substitute `<proofread-id>` and `<vid-id>` with the actual ids you receive.

```bash
# 1. Submit proofread session
heygen video-translate proofreads create \
  -d '{"video":{"type":"url","url":"https://example.com/source.mp4"}}' \
  --output-languages "Spanish" \
  --mode precision \
  --enable-speech-enhancement \
  --keep-the-same-format \
  --speaker-num 1 \
  --title "Q4 launch — Spanish proofread"
# → {"data":{"proofread_ids":["<id-es>"],"status":"processing"}}

# 2. Poll until completed (typical: 3–5 min for short videos)
heygen video-translate proofreads get <proofread-id>
# → status: processing → completed (or failed + failure_message)

# 3. Fetch the editable SRT and the original-language transcript
heygen video-translate proofreads srt get <proofread-id> > /tmp/srt-resp.json
SRT_URL=$(jq -r '.data.srt_url' /tmp/srt-resp.json)
ORIG_URL=$(jq -r '.data.original_srt_url' /tmp/srt-resp.json)
curl -s "$SRT_URL"  -o /tmp/proofread.srt
curl -s "$ORIG_URL" -o /tmp/proofread-original.srt

# 4. Edit /tmp/proofread.srt — by hand, by sed, by tool
#    Example: brand glossary find-replace
sed -i 's/Centro Garra/ClawHub/g'        /tmp/proofread.srt
sed -i 's/José Joshua/Joshua Xu/g'       /tmp/proofread.srt

# 5. Host the edited SRT at a public URL, then upload by reference
EDITED_URL="https://example.com/proofread-edited.srt"
heygen video-translate proofreads srt update <proofread-id> \
  -d "{\"srt\":{\"type\":\"url\",\"url\":\"$EDITED_URL\"}}"
# → returns the proofread resource (status still completed)

# 6. Kick off the final render with the corrected captions
heygen video-translate proofreads generate <proofread-id> --captions
# → {"data":{"video_translation_id":"<vid-id>","status":"processing"}}

# 7. Poll the resulting translation to completion
heygen video-translate get <vid-id>
# → status: running → succeeded; data.video_url has the final mp4
```

---

## When to insist on proofreads

- **Long videos** (>3 minutes). The cost of re-rendering a 10-minute mistranslation is high; ASR + glossary fixes are cheap.
- **Corporate / branded content.** Brand names, product names, slogans, claims need to land exactly.
- **Legal, medical, educational content.** Wrong terminology has consequences beyond user disappointment.
- **The user reads the target language natively.** They'll catch things you can't.
- **Source has named entities** (people, companies, products, places) that auto-translation will likely mangle.
- **High-formality languages** (ja, ko, th, de) where the source is conversational and the user wants register-matched output.
- **RTL languages** (ar, he, ur, fa) where caption styling matters — sidecar SRT delivery via proofread is cleaner than burned-in captions.

If two or more apply: default proofreads ON. Don't ask — propose: *"For [reason], let's do a quick proofread before final render."*

## When to skip proofreads

- Short videos (<60 s) that aren't high-stakes.
- The user wants speed and is willing to re-translate if quality is off.
- Single language, single speaker, neutral content.
- The user explicitly says "just go" or "fast as possible".

## When the user CAN'T review the SRT

If neither the user nor a reachable native speaker reads the target language:

- Skip proofreads — they can't add value to a review nobody performs.
- Set lower expectations on the result. Suggest a test clip first.
- Offer to deliver the dubbed video plus the SRT as a sidecar so they can share with a native-speaking colleague to review BEFORE distribution.

Don't run proofreads as a checkbox if no one will actually read the SRT — it just adds time without adding accuracy.

---

## Common SRT edits

The engine WILL translate proper nouns and jargon by default. Find-and-replace is the fastest way to surgically restore them.

### Brand glossary / do-not-translate

```bash
# Names, products, companies, slogans
sed -i 's/Centro Garra/ClawHub/g'   /tmp/proofread.srt
sed -i 's/José Joshua/Joshua Xu/g'  /tmp/proofread.srt
sed -i 's/Garra/Claw/g'             /tmp/proofread.srt   # only if "Garra" wasn't intended
```

For non-trivial glossaries, write a small Python script with the full list. Show the user the list first; have them confirm before applying.

### Register / formality fixes

For ja/ko/de/fr/es/th/hi conversational content where the engine landed too formal:

| Language | Find | Replace |
|----------|------|---------|
| German   | `Sie ` | `du ` |
| German   | `Ihr ` | `dein ` |
| German   | `Ihre ` | `deine ` |
| German   | `Sie haben` | `du hast` |
| French   | `vous` | `tu` (context-aware — see caveat below) |
| French   | `votre` | `ton` / `ta` |
| French   | `vos` | `tes` |
| Japanese | `です` (declarative) → strip | per-line review needed |
| Japanese | `ます` (verb suffix) → strip | per-line review needed |
| Korean   | `ㅂ니다` → `요` | per-line review needed |
| Thai     | `ค่ะ` / `ครับ` (particles) → strip | per-line review needed |
| Spanish  | `usted` → `tú` | LATAM informal target |
| Spanish  | `vosotros` → `ustedes` | es-ES → LATAM |

> Caveat: bulk sed-replace on register markers can break sentences in CJK/SEA languages where the marker is part of a verb. Walk through line-by-line for ja/ko/th, batch with confirmation for de/fr/es.

### Numbers, dates, units

The engine usually localizes numbers and dates correctly. Spot-check:

- Currency: `$1,000` may render as `mil dólares`, `US$1.000`, or `1.000 $`. Pick the audience convention.
- Dates: `4/27` → `27 de abril` (es), `4月27日` (ja), `27.04.` (de), `27/4` (UK).
- Units: imperial → metric is NOT done. Surface to the user if the source uses miles/feet/Fahrenheit and the audience expects metric.

### Cultural references

Idioms, sports references, and pop-culture callouts often translate literally and lose meaning. Flag affected lines, ask whether to adapt or keep literal.

---

## Sidecar SRT delivery

If the user wants captions as a sidecar (.srt) instead of burned-in:

1. Run the proofread workflow normally.
2. On `generate`, **omit `--captions`**.
3. Deliver the dubbed video AND the corrected SRT (which you already have at `/tmp/proofread.srt` from Step 4) to the user.

This is the cleanest path for: RTL languages, brand-styled captions (their editor styles), or accessibility workflows where SRT is required.

---

## Cost / time math

Proofreads add roughly:

- **3–5 min** for SRT extraction (Step 2). Verified empirically on a 50-second source video.
- **2–10 min** for review/edit (Step 4) — depends on length and editing depth.
- **Same render time** as a normal translation for the final generate (Step 6–7).

Total proofreads overhead: ~10–20 minutes. For high-stakes content, trivially worth it. For a 30-second product demo, overkill.

Cost: HeyGen bills the final render the same as a non-proofread translation. The proofread session itself is light — no avatar inference happens until `generate`. So you effectively pay once (for the final render) regardless of how many SRT-edit cycles you ran.

---

## Failure modes specific to proofreads

| Symptom | Verified `failure_message` | Cause | Fix |
|---------|----------------------------|-------|-----|
| `failed` immediately on submit | `Failed to download video from url, please check the url is valid or the video is public` | Source URL was 401/403/404, returned HTML, redirected to a login page, or had wrong MIME | HEAD-check the URL with `curl -sI`; ask user for public URL or local file → upload route |
| `failed` after ~30 s of `processing` | `Your video's audio is missing or corrupted, please try with another video` | Source has no audible speech, audio track is silent / missing, or codec is unparseable | Verify the source has speech; consider re-encoding to MP4 + AAC; for silent / animation-only sources, route to a different workflow (this skill won't help) |
| SRT update returns `Content type not supported application/x-subrip` | (CLI error envelope, not API status) | You tried to upload the edited SRT via `heygen asset create` — that endpoint only accepts png/jpeg/mp4/webm/mp3/wav/pdf | Host the SRT at a public URL and use `srt update -d '{"srt":{"type":"url","url":"..."}}'` |
| Uploaded SRT timing is off | n/a — bad render result | SRT timecodes were edited or shifted | Re-download the SRT from `proofreads srt get` and edit text only, never timecodes; re-upload |
| `generate` runs but final render uses old text | n/a | `srt update` didn't take or you forgot to call it before `generate` | Re-upload, then re-call `proofreads generate` |
| Proofread session expired | session not found | Sessions have a TTL (typically 24 h) | Re-create the proofread; don't try to revive an expired one |

For other failure_message strings, see [troubleshooting.md](troubleshooting.md#errors--action-mapping).

---

## Caveats and known quirks (verified)

- **`heygen asset create` does not accept SRT files.** Only `png/jpeg/mp4/webm/mp3/wav/pdf`. Renaming the extension does not bypass it (server sniffs content). The `asset_id` shape is in the request schema for `srt update` for forward-compatibility, but the upload path is currently blocked. Use the URL route.
- **`proofreads create` returns `proofread_ids` (plural, one per language) and a `status` at the SESSION level.** The session-level `status` is just the submit ack; per-id status comes from `proofreads get`.
- **`status` enum is `processing | completed | failed`.** Not `pending` / `running`. (The translation-render endpoint uses `pending | running | succeeded | failed` — these are different state machines.)
- **`original_srt_url`** is auto-populated even when no SRT was provided at create time. It's the engine's source-language transcription, not a copy of an SRT you uploaded. Useful for verification, never re-upload as a target-language SRT.
- **SRT filenames carry the title.** The downloaded SRTs are named `<title>_proofread.srt` and `<title>_proofread_original.srt`. Pick a clean, fileNAME-safe `--title`.
- **Polling shifts after `generate`.** Up through `srt update`, you poll `heygen video-translate proofreads get`. After `generate` returns a `video_translation_id`, you poll `heygen video-translate get` instead — same translation poll loop as a non-proofread workflow.
- **Captions on `generate` are independent of captions in the proofread session.** The proofread session always produces an editable SRT (that's its purpose); whether the FINAL video has captions burned in is controlled by `--captions` on `generate`.
