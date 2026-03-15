---
name: audio-mix
description: |
  Audio loudness normalization (EBU R128), ducking, mixing, and crossfading using ffmpeg. Platform-specific LUFS targets for YouTube, podcasts, Spotify.
  Use when the user says "normalize audio", "loudness", "duck music", "mix audio", "crossfade", "replace audio", "extract audio", "LUFS".
argument-hint: "<audio-or-video-file> [target-lufs=-16]"
version: 1.0.0
---

# Audio Mix — Loudness Normalization, Ducking & Mixing

Two-pass EBU R128 loudness normalization, auto-ducking music under speech, crossfading, and audio extraction/replacement — all via ffmpeg.

## Step 0: Prerequisites

```bash
if ! command -v ffmpeg &>/dev/null; then
  echo "ffmpeg not found. Install via: brew install ffmpeg"
  exit 1
fi
```

## Step 1: Measure Loudness (EBU R128)

Before normalizing, measure the current loudness:

```bash
ffmpeg -i "$INPUT" -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/{/,/}/p'
```

This outputs JSON with:
- `input_i`: Integrated loudness (LUFS) — the main number
- `input_tp`: True peak (dBTP)
- `input_lra`: Loudness range (LU)
- `input_thresh`: Threshold

**Important**: The JSON output is on stderr mixed with other ffmpeg output. Use `sed -n '/{/,/}/p'` to extract just the JSON block (more reliable than `tail -12`).

## Step 2: Two-Pass Loudness Normalization

Single-pass `loudnorm` is imprecise. Two-pass gives broadcast-quality results:

```bash
TARGET_I=-16   # Target integrated loudness (LUFS)
TARGET_TP=-1.5 # Target true peak (dBTP)
TARGET_LRA=11  # Target loudness range (LU)

# Pass 1: Measure
MEASURE=$(ffmpeg -i "$INPUT" -af loudnorm=print_format=json -f null - 2>&1 | sed -n '/{/,/}/p')

# Extract values from measurement JSON
INPUT_I=$(echo "$MEASURE" | grep input_i | tr -d '", \t' | cut -d: -f2)
INPUT_TP=$(echo "$MEASURE" | grep input_tp | tr -d '", \t' | cut -d: -f2)
INPUT_LRA=$(echo "$MEASURE" | grep input_lra | tr -d '", \t' | cut -d: -f2)
INPUT_THRESH=$(echo "$MEASURE" | grep input_thresh | tr -d '", \t' | cut -d: -f2)

# Pass 2: Normalize with measured values
ffmpeg -i "$INPUT" -af "loudnorm=I=$TARGET_I:TP=$TARGET_TP:LRA=$TARGET_LRA:measured_I=$INPUT_I:measured_TP=$INPUT_TP:measured_LRA=$INPUT_LRA:measured_thresh=$INPUT_THRESH:linear=true" \
  -ar 48000 -y "$OUTPUT"
```

**Platform LUFS targets**:

| Platform | Target LUFS | True Peak |
|-|-|-|
| YouTube | -14 | -1.0 dBTP |
| Spotify | -14 | -1.0 dBTP |
| Apple Music | -16 | -1.0 dBTP |
| Podcast (general) | -16 | -1.5 dBTP |
| Broadcast TV (EBU) | -23 | -1.0 dBTP |
| Cinema | -24 | -1.0 dBTP |

## Step 3: Auto-Duck Music Under Speech

Lower the music volume when speech is present using sidechain compression:

```bash
# speech.wav = voice track, music.wav = background music
ffmpeg -i speech.wav -i music.wav \
  -filter_complex "[1:a]sidechaincompress=threshold=0.02:ratio=8:attack=200:release=1000[ducked];[0:a][ducked]amix=inputs=2:duration=longest" \
  -y output.wav
```

**Parameters**:
- `threshold=0.02`: How loud speech must be to trigger ducking (lower = more sensitive)
- `ratio=8`: How much to reduce music (higher = more ducking)
- `attack=200`: Ms to start ducking after speech detected
- `release=1000`: Ms to restore music after speech stops

**Alternative approach** — volume automation using silence detection:

```bash
# Step 1: Detect speech segments (non-silent parts)
ffmpeg -i speech.wav -af "silencedetect=noise=-30dB:d=0.5" -f null - 2>&1 | \
  grep "silence_"

# Step 2: Use the timestamps to create volume keyframes
# (Manual approach — build a volume filter string from silence boundaries)
```

## Step 4: Crossfade Between Audio Tracks

Smoothly transition between two audio files:

```bash
# 3-second crossfade between track1 and track2
ffmpeg -i track1.wav -i track2.wav \
  -filter_complex "acrossfade=d=3:c1=tri:c2=tri" \
  -y output.wav
```

**Curve types** (`c1`/`c2`):
- `tri`: Linear (default)
- `qsin`: Quarter sine — smooth and natural
- `hsin`: Half sine
- `log`: Logarithmic — slow start, fast end
- `esin`: Exponential sine
- `exp`: Exponential

For multiple tracks, chain crossfades:

```bash
ffmpeg -i track1.wav -i track2.wav -i track3.wav \
  -filter_complex "[0:a][1:a]acrossfade=d=3:c1=qsin:c2=qsin[mix1];[mix1][2:a]acrossfade=d=3:c1=qsin:c2=qsin" \
  -y output.wav
```

## Step 5: Extract Audio from Video

```bash
# Extract as WAV (uncompressed)
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 44100 -ac 2 -y audio.wav

# Extract as MP3
ffmpeg -i video.mp4 -vn -acodec libmp3lame -q:a 2 -y audio.mp3

# Extract as AAC (copy without re-encoding, if source is AAC)
ffmpeg -i video.mp4 -vn -acodec copy -y audio.aac

# Extract specific audio track (e.g., second audio stream)
ffmpeg -i video.mp4 -map 0:a:1 -y audio_track2.wav
```

## Step 6: Replace Audio in Video

```bash
# Replace audio entirely (keep video, use new audio)
ffmpeg -i video.mp4 -i new_audio.wav \
  -c:v copy -map 0:v:0 -map 1:a:0 -shortest -y output.mp4

# Add audio track alongside existing audio
ffmpeg -i video.mp4 -i additional_audio.wav \
  -c:v copy -map 0:v -map 0:a -map 1:a -y output.mp4
```

## Common Workflows

1. **Normalize podcast for publishing**: Measure (Step 1), then two-pass normalize to -16 LUFS (Step 2)
2. **YouTube-ready audio**: Two-pass normalize to -14 LUFS
3. **Background music under narration**: Use auto-duck (Step 3)
4. **DJ-style transition**: Crossfade (Step 4) with `qsin` curves
5. **Swap music in a video**: Extract audio (Step 5), mix new track, replace (Step 6)

## Error Handling

- **"measured_I" not found**: The measurement JSON is in stderr — make sure to capture with `2>&1 | sed -n '/{/,/}/p'`
- **Output sounds distorted**: True peak too high — lower `TARGET_TP` to -2.0
- **Loudness unchanged after normalize**: Check that you're using two-pass (not single-pass) and that `linear=true` is set
- **Crossfade fails**: Both inputs must have the same sample rate — add `-ar 48000` to both inputs
- **Ducking too aggressive**: Increase `threshold` or decrease `ratio`
- **Audio/video out of sync after replace**: Add `-shortest` flag, or match audio duration to video with `-t`
