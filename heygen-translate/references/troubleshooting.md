# Troubleshooting & Polling

## Polling

**Don't poll in foreground.** Long translations (5–30 min) will block the
session and burn approval prompts on every status check. Background-poll
instead.

### CLI mode polling

For a SINGLE language, prefer `--wait`:

```bash
heygen video-translate create -d '...' \
  --output-languages "Spanish (Spain)" \
  --mode precision \
  --enable-speech-enhancement \
  --enable-caption \
  --enable-dynamic-duration \
  --keep-the-same-format \
  --wait \
  --timeout 30m
```

`--wait` blocks until success or failure. The CLI uses a server-side polling
strategy with sane backoff. Exit code `0` = succeeded; `4` = timeout (job is
still running, just exceeded `--timeout`); `1` = failed; check stderr for the
error envelope.

For BATCH translations (multiple languages), you can't `--wait` on all of them
together. Strategy: submit without `--wait`, capture the array of
`video_translation_id`s, then run one backgrounded poll per ID.

```bash
# Submit
heygen video-translate create -d '...' \
  --output-languages "Spanish (Spain)" "Japanese (Japan)" "German (Germany)" \
  --mode precision --enable-speech-enhancement --enable-caption \
  --enable-dynamic-duration --keep-the-same-format \
  > /tmp/translation-batch.json

# Extract IDs
jq -r '.data.video_translations[].video_translation_id' /tmp/translation-batch.json
```

For each ID, run a backgrounded poll loop in a single shell invocation so the
user only approves once per language:

```bash
ID="<video-translation-id>"
LANG="Spanish (Spain)"
while true; do
  resp=$(heygen video-translate get "$ID" 2>/dev/null)
  status=$(echo "$resp" | jq -r '.data.status')
  case "$status" in
    succeeded)
      url=$(echo "$resp" | jq -r '.data.video_url // .data.translated_video_url // empty')
      echo "DONE $LANG $url"
      break
      ;;
    failed)
      msg=$(echo "$resp" | jq -r '.data.failure_reason // "unknown"')
      echo "FAILED $LANG $msg"
      break
      ;;
  esac
  sleep 30
done
```

Polling cadence: 30 s for the first 3 minutes, then 60 s. Hard timeout: 60 min.

### Harness-specific polling notes

- **Claude Code:** Backgrounded `Bash` calls inherit session permissions cleanly. Subagents spawned with `Agent` do NOT inherit `Bash` approvals — every `heygen` call inside a subagent will fail on permission denial. Use backgrounded bash, not subagents, for translation polling.
- **OpenClaw:** Use `exec` with `background: true` and rely on automatic completion wake. The runtime announces completion when the loop exits. Don't tight-poll the process from the main session.
- **Cursor / generic CDP harnesses:** Backgrounded tasks may be killed when the parent turn ends. Prefer webhook callbacks (`--callback-url`) for these environments.

### MCP mode polling

If `mcp__heygen__get_video_translation` is exposed in your toolset, use it. If
not, fall through to CLI for the polling step specifically — that's the one
acceptable place to mix MCP for submission and CLI for status checks.

### Webhook callbacks (skip polling)

If the user has a webhook endpoint, set `--callback-url` and `--callback-id`
on the create call. HeyGen POSTs to the URL on completion. This is the cleanest
path for production pipelines.

```bash
heygen video-translate create -d '...' \
  --callback-url "https://example.com/heygen-webhooks" \
  --callback-id "session-12345" \
  --output-languages "Spanish (Spain)" \
  --mode precision
```

---

## Errors → Action Mapping

### Auth errors

**`exit 3` from CLI / 401 from API:**
`HEYGEN_API_KEY` is missing, expired, or wrong. Action:

1. Confirm the env var: `echo "${HEYGEN_API_KEY:0:8}…" `
2. Test with a known-good call: `heygen user`
3. If that fails, regenerate the key at <https://app.heygen.com/api>

**`heygen auth login` worked but a call says `unauthorized`:**
Token cached but rotated server-side. Run `heygen auth logout && heygen auth login`.

### Source video errors

**`400` "video URL not accessible" / "Could not fetch video":**
The URL requires auth, returned HTML, returned wrong MIME, or 404'd. Run a quick
sanity check:

```bash
curl -sI "<URL>" | head -5
```

Expect a `200` + `Content-Type: video/...`. If you see `403`, `404`, `text/html`,
or a redirect chain to a login page, ask the user for a public URL or a local
file. For local files, route through `heygen asset create --file`.

**`400` "asset_id not found":**
The asset_id was for a different account, was deleted, or doesn't exist.
Re-upload via `heygen asset create --file <path>`.

**File >32 MB:**
HeyGen asset upload caps at 32 MB. Options:

1. Re-encode the source at lower bitrate (often a 32 MB file is over-encoded).
2. Host the file at a public URL (S3, Bucket, etc.) and pass as `{type:"url"}`.
3. Use a presigned URL if it's behind auth — make sure the URL is reachable
   without additional headers.

### Language errors

**`400` "language not supported":**
The string didn't match the canonical list exactly. Re-run:

```bash
heygen video-translate languages list | jq -r '.data.languages[]' > /tmp/heygen-langs.txt
grep -i "<user-said>" /tmp/heygen-langs.txt
```

Present the closest matches. Common mismatches:

| User said | Canonical |
|-----------|-----------|
| "Spanish" | "Spanish (Spain)" |
| "Mexican Spanish" | "Spanish (Mexico)" |
| "Chinese" / "Mandarin" | "Chinese (Mandarin, Simplified)" |
| "Cantonese" | "Chinese (Cantonese, Traditional)" |
| "Portuguese" | "Portuguese (Portugal)" or "Portuguese (Brazil)" — ASK |
| "Arabic" | "Arabic" or one of 19 region variants — ASK |
| "Japanese" | "Japanese (Japan)" or just "Japanese" |
| "French" | "French (France)" |
| "German" | "German (Germany)" |
| "English" | "English (United States)" or just "English" |

### Submission errors

**`failed` with `failure_message: "Your video's audio is missing or corrupted, please try with another video"`** (verified empirically):
The source has no audible speech, very corrupted audio, or unsupported codec.
Fails fast (~30 s after submit). Verify by previewing the source. If the user says speech is present, try re-encoding to a clean MP4 with AAC audio (`ffmpeg -i input.mp4 -c:v libx264 -c:a aac -b:a 128k output.mp4`). For animation / b-roll / silent sources, video translation is the wrong tool — route to a different workflow.

**`failed` with `failure_message: "Failed to download video from url, please check the url is valid or the video is public"`** (verified empirically):
Fails almost instantly on submit. Source URL was 401/403/404, returned HTML instead of a video, redirected to a login page, or had a presigned URL that already expired. HEAD-check first with `curl -sI "$URL"` — expect `200` + `Content-Type: video/...`. Ask the user for a public URL or fall back to local-file upload.

**`failed` with `failure_reason: "speaker detection"`:**
`speaker_num` mismatched the actual speakers, or audio was too noisy for
diarization. Re-submit with correct speaker count and
`enable_speech_enhancement: true`.

**`failed` with `failure_reason: "lip-sync"`:**
Face was not detected or detection was unstable. Likely cause: occlusion,
profile shots, low resolution, or fast cuts. Either:

1. Re-submit as `translate_audio_only: true` (the user gets translated audio,
   composites manually).
2. Tell the user the source isn't viable for visual translation.

### Stuck jobs

**Stuck >30 min in `running`:**
Most translations finish in 5–15 min; some legitimately take 30–45 min for
long source videos or batched languages. Beyond 60 min, treat as stuck:

1. `heygen video-translate get <id>` and capture the response.
2. Surface to the user: *"This translation has been running for over an hour.
   Backend may be stuck. Want me to delete the job and re-submit, or wait
   another 30 minutes?"*
3. If they re-submit, `heygen video-translate delete <id>` first.

### SRT upload errors (proofreads workflow)

**`heygen asset create` returns `Content type not supported application/x-subrip` when uploading an edited SRT** (verified):
The asset upload endpoint only accepts `png/jpeg/mp4/webm/mp3/wav/pdf`. SRT files are not supported regardless of extension (server sniffs content; renaming `.srt` to `.txt` or `.mp3` does NOT bypass it). The `asset_id` shape is in the `srt update` request schema for forward-compatibility but the upload path is currently blocked.

**Fix:** host the edited SRT at a public URL and use the URL route:

```bash
heygen video-translate proofreads srt update <proofread-id> \
  -d '{"srt":{"type":"url","url":"https://example.com/proofread-edited.srt"}}'
```

Working host options: GitHub gists (raw URL), GitHub repo files (raw URL), S3/GCS with public-read or a presigned URL ≥2 h, Vercel/static hosts. The URL must serve `application/x-subrip` or `text/plain` with the SRT body — verify with `curl -sI`.

### Output / delivery errors

**`succeeded` but `video_url` is null:**
Race condition between job completion and CDN propagation. Retry the `get`
call after 30 seconds.

**`video_url` returns 403 or expired:**
Presigned URLs from HeyGen expire. Re-fetch with `heygen video-translate get
<id>` to get a fresh URL.

**Captions in wrong direction (RTL languages):**
Burned-in captions for Arabic / Hebrew / Urdu / Persian render right-to-left
and may collide with source video graphics in the lower-third. Switch to the
proofreads workflow and use the SRT as a sidecar caption file.

### Lip-sync quality issues

**Output looks fine in some shots but bad in others:**
Source face conditions (occlusion, profile, fast cuts) are degrading lip-sync
in those segments. Set expectations upfront in Phase 2 next time. For this
output, options:

1. Accept it (lip-sync was always going to be best-effort with this source).
2. Re-edit the source to use cleaner shots, then re-translate.
3. Switch to audio-only translation for use in a different video.

**Voice clone sounds off (wrong gender, accent, age):**
Almost always a `speaker_num` issue — the engine separated voices wrong and
clipped a different speaker's audio into the dub. Re-submit with corrected
speaker count, or use proofreads to scrub the SRT and re-dub.

---

## Debug Checklist (run before escalating)

1. **Auth:** `heygen user` returns user info ✅ / fails ❌
2. **CLI version:** `heygen --version` returns v0.0.6 or newer
3. **Languages list:** `heygen video-translate languages list | jq '.data.languages | length'` returns >0
4. **Source URL reachable:** `curl -sI "<URL>" | head -1` returns `200`
5. **Source MIME:** `curl -sI "<URL>" | grep -i content-type` shows `video/...`
6. **Recent jobs:** `heygen video-translate list` to see if past jobs succeeded

If all six pass and the translation still fails: capture the `failure_reason`
from `heygen video-translate get <id>` and surface it — that's HeyGen-side, not
something the skill can resolve.
