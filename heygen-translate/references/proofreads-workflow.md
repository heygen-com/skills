# Proofreads Workflow

The proofreads endpoint extracts editable subtitles BEFORE final video render.
This is the high-stakes path for translation: you (or the user) review the
translated SRT, fix wrong terms, preserve names, adjust register, and only
then commit to the dubbed video render.

Use this when stakes are high and the cost of a re-translation (time, plan
credits, frustration) outweighs the ~5 minutes of proofread overhead.

---

## When to insist on proofreads

- **Long videos** (>3 minutes). The cost of re-rendering a 10-minute mistranslation is high.
- **Corporate / branded content.** Brand names, product names, slogans, claims need to land exactly.
- **Legal, medical, educational content.** Wrong terminology has consequences beyond user disappointment.
- **The user reads the target language natively.** They'll catch errors you can't, and they'll want to.
- **Source has named entities** (people, companies, products, places) that the engine will likely auto-translate or mangle.
- **High-formality languages** (ja, ko, th, de) where the source is conversational and the user wants the dub to match register.
- **RTL languages** (ar, he, ur, fa) where caption styling matters.

If two or more of these apply: default proofreads ON. Don't even ask — propose
it: *"For [reason], let's do a quick proofread before final render."*

---

## When to skip proofreads

- Short videos (<60s) that aren't high-stakes.
- The user wants speed and is willing to re-translate if the result is off.
- Single language, single speaker, neutral content (e.g., a 30-second product
  demo into Spanish).
- The user explicitly says "just go" or "fast as possible".

---

## CLI workflow

Replace `<proofread-id>` with the ID returned from `create`. The example below
uses Spanish (Spain); for batch, pass multiple `--output-languages`.

### Step 1 — Create the proofread session

```bash
heygen video-translate proofreads create \
  -d '{"video":{"type":"url","url":"https://example.com/source.mp4"}}' \
  --output-languages "Spanish (Spain)" \
  --mode precision \
  --enable-speech-enhancement \
  --keep-the-same-format \
  --speaker-num 1 \
  --title "Q4 launch — Spanish proofread"
```

Capture the `proofread_id` from the response.

### Step 2 — Wait for SRT extraction

```bash
heygen video-translate proofreads get <proofread-id>
```

The session's `status` field transitions from `running` → `succeeded`. SRT
extraction takes 1–5 minutes. Poll on the same cadence as a translation
(30s → 60s).

### Step 3 — Download the SRT

```bash
heygen video-translate proofreads srt get <proofread-id> > /tmp/proofread.srt
```

This returns the translated SRT in standard format:

```
1
00:00:01,200 --> 00:00:04,800
Bienvenidos a la presentación del Q4.

2
00:00:05,000 --> 00:00:09,400
Este trimestre lanzamos tres productos nuevos.
```

### Step 4 — Review and edit

The user (or you, with their guidance) edits `/tmp/proofread.srt`. Common
edits:

#### Brand glossary / do-not-translate

The engine WILL translate brand names, product names, and proper nouns by
default. Find-and-replace these:

```bash
# Example: keep "ClawHub" in English instead of translated
sed -i 's/Centro Garra/ClawHub/g' /tmp/proofread.srt
sed -i 's/CenterClaw/ClawHub/g' /tmp/proofread.srt

# Example: keep founder name as written
sed -i 's/José Joshua/Joshua Xu/g' /tmp/proofread.srt
```

For non-trivial glossaries, write a small Python or sed script with the full
list. Have the user confirm the list before applying.

#### Register / formality fixes

For ja/ko/de/th/hi conversational content where the engine landed too formal:

- **German:** Sie → du, Ihr → dein, Ihre → deine, Sie haben → du hast, Ihren → deinen
- **French:** vous → tu, votre → ton/ta, vos → tes
- **Japanese:** strip ます/です endings, replace with casual forms (review per line)
- **Korean:** swap ㅂ니다 / 요 endings to match target register
- **Thai:** drop ค่ะ / ครับ particles for casual feel
- **Spanish:** usted → tú (LATAM); vosotros → ustedes (es-ES → LATAM)

Don't blindly sed-replace these — context matters. Walk through line by line
or batch with the user's confirmation per pass.

#### Numbers, dates, units

The engine usually localizes numbers and dates correctly, but check:

- Currency: $1,000 might become "mil dólares" or "US$1.000" — pick the convention the audience expects.
- Dates: 4/27 → "27 de abril" (es) vs "4月27日" (ja) vs "27.04." (de).
- Units: imperial → metric conversions are NOT done. Surface to the user if the source uses miles/feet/Fahrenheit and the audience expects metric.

#### Cultural references

Idioms, sports references, and pop-culture callouts often translate literally
and lose meaning. The user knows the audience — flag the lines, ask whether
to adapt or keep literal.

### Step 5 — Upload corrected SRT

Two ways:

**Inline URL** (if you've uploaded the SRT to a public location):

```bash
heygen video-translate proofreads srt update <proofread-id> \
  -d '{"srt":{"type":"url","url":"https://example.com/proofread.srt"}}'
```

**Asset upload** (cleanest path — upload the file to HeyGen as an asset first):

```bash
SRT_ASSET=$(heygen asset create --file /tmp/proofread.srt | jq -r '.data.id')
heygen video-translate proofreads srt update <proofread-id> \
  -d "{\"srt\":{\"type\":\"asset_id\",\"asset_id\":\"$SRT_ASSET\"}}"
```

### Step 6 — Generate final video

```bash
heygen video-translate proofreads generate <proofread-id> \
  --captions \
  --callback-url "https://example.com/webhook"  # optional
```

`--captions` burns the corrected captions into the final video. Drop this flag
if you want the SRT delivered as a sidecar file instead.

`--translate-audio-only` is also supported here, same as on `create`.

### Step 7 — Poll the final render

The proofreads `generate` step kicks off a normal translation render. Poll
with `heygen video-translate get <video-translation-id>` (the `generate`
response includes the resulting `video_translation_id`).

---

## Sidecar SRT delivery

If the user wants captions as a sidecar (.srt file) instead of burned-in:

1. Run the proofreads workflow normally.
2. On `generate`, omit `--captions`.
3. Deliver the dubbed video AND the corrected SRT file from Step 4 to the user.

This is the cleanest path for: RTL languages, brand-styled captions (their
editor will style), or accessibility workflows where SRT is required.

---

## Cost / time math

Proofreads add roughly:

- **5 min** for SRT extraction (Step 2)
- **2–10 min** for review/edit (Step 4) — depends on video length and editing depth
- **Same render time** as a normal translation for the final generate (Step 6–7)

Total proofreads overhead: ~10–15 minutes. For high-stakes content, that's
trivially worth it. For a 30-second product demo, it's overkill.

---

## When the user CAN'T review the SRT

If the user doesn't read the target language and there's no native speaker to
review:

- Skip proofreads. They can't add value to a review they can't perform.
- Set lower expectations on the result. Suggest a test clip first.
- Offer to deliver the dubbed video plus the SRT as a sidecar so they can
  share with a native-speaking colleague to review BEFORE distribution.

Don't run proofreads as a checkbox if no one will actually read the SRT — it
just adds time without adding accuracy.

---

## Failure modes specific to proofreads

| Symptom | Cause | Fix |
|---------|-------|-----|
| SRT extraction `failed` | Source had no audible speech, or speech was un-diarizable | Re-submit with `enable_speech_enhancement: true` and correct `speaker_num` |
| Uploaded SRT timing is off | SRT timecodes don't match the source video | Re-download the SRT from `proofreads srt get` and edit text only — don't change timecodes |
| `generate` fails after a successful SRT update | SRT format invalid (rare; usually mangled timecodes) | Validate with `ffmpeg -i input.mp4 -i edited.srt -c copy out.mkv` locally before re-uploading |
| Proofread session expires | Sessions have a TTL (typically 24h) | Re-create the proofread session and re-edit; don't try to revive the expired one |
