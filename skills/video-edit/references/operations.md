# Operations Reference

Detailed ffmpeg recipes for every operation. Each section shows the command, explains key flags, and lists common variations.

---

## info

Get full metadata about a video file using ffprobe.

```bash
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

**Key flags:**
- `-v quiet` — suppress banner/log noise, output only the requested data.
- `-print_format json` — output as JSON (easy to parse). Also accepts `csv`, `flat`, `ini`.
- `-show_format` — container-level info: duration, bitrate, format name, size.
- `-show_streams` — per-stream info: codec, resolution, frame rate, sample rate, channels.

**Variations:**
```bash
# Duration only (seconds, as plain text)
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4

# Resolution only
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 video.mp4
```

---

## trim

Cut a segment from a video using stream copy (no re-encoding, very fast).

```bash
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c copy trimmed.mp4
```

**Key flags:**
- `-ss <time>` — seek to start position. Placed before `-i` for fast input seeking.
- `-to <time>` — stop at this timestamp (absolute). Alternative: `-t <duration>` for relative duration.
- `-c copy` — copy streams without re-encoding. Fast but cuts only on keyframes (may be off by a few frames).

**Timestamps** accept `HH:MM:SS`, `HH:MM:SS.mmm`, `MM:SS`, or raw seconds (`90`, `90.5`).

**Variations:**
```bash
# By duration instead of end time
ffmpeg -y -ss 00:00:30 -t 75 -i video.mp4 -c copy trimmed.mp4

# Frame-accurate trim (re-encodes, slower but exact)
ffmpeg -y -ss 00:00:30 -to 00:01:45 -i video.mp4 -c:v libx264 -c:a aac trimmed.mp4
```

---

## concat

Join multiple video files into a single file.

```bash
# Step 1: Create a concat list file
printf "file '%s'\n" clip1.mp4 clip2.mp4 clip3.mp4 > list.txt

# Step 2: Concat with stream copy
ffmpeg -y -f concat -safe 0 -i list.txt -c copy joined.mp4
```

**Key flags:**
- `-f concat` — use the concat demuxer.
- `-safe 0` — allow absolute paths in the file list.
- `-c copy` — copy streams without re-encoding. Requires all inputs to share the same codec, resolution, and frame rate.

**Variations:**
```bash
# Re-encode to normalize mismatched clips (slower)
ffmpeg -y -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac joined.mp4

# Inline concat without a file (only for same-format files)
ffmpeg -y -i "concat:part1.ts|part2.ts" -c copy joined.ts
```

---

## resize

Resize a video to specific dimensions with aspect-ratio-preserving padding.

```bash
ffmpeg -y -i video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:a copy resized.mp4
```

**Key flags:**
- `-vf` — video filter chain.
- `scale=W:H:force_original_aspect_ratio=decrease` — scale down to fit within WxH, preserving aspect ratio.
- `pad=W:H:(ow-iw)/2:(oh-ih)/2:black` — pad to exact WxH with centered black bars.
- `-c:a copy` — copy audio without re-encoding.

**Variations:**
```bash
# Scale to width, auto-calculate height (maintains aspect ratio)
ffmpeg -y -i video.mp4 -vf "scale=1280:-2" -c:a copy resized.mp4

# Scale to height, auto-calculate width
ffmpeg -y -i video.mp4 -vf "scale=-2:720" -c:a copy resized.mp4

# Custom dimensions without padding (stretches)
ffmpeg -y -i video.mp4 -vf "scale=1280:720" -c:a copy resized.mp4
```

---

## speed

Change playback speed of both video and audio.

```bash
# 2x faster
ffmpeg -y -i video.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" fast.mp4

# Half speed (slow motion)
ffmpeg -y -i video.mp4 -filter:v "setpts=2.0*PTS" -filter:a "atempo=0.5" slow.mp4
```

**Key flags:**
- `-filter:v "setpts=N*PTS"` — multiply presentation timestamps. `0.5` = 2x faster, `2.0` = half speed. Formula: `N = 1 / speed_factor`.
- `-filter:a "atempo=F"` — adjust audio speed. Preserves pitch. Only supports values between 0.5 and 2.0.

**For factors outside 0.5-2.0**, chain multiple atempo filters:
```bash
# 4x faster
ffmpeg -y -i video.mp4 -filter:v "setpts=0.25*PTS" -filter:a "atempo=2.0,atempo=2.0" fast4x.mp4

# 0.25x (very slow)
ffmpeg -y -i video.mp4 -filter:v "setpts=4.0*PTS" -filter:a "atempo=0.5,atempo=0.5" slow025x.mp4
```

---

## extract-audio

Extract the audio track from a video file.

```bash
ffmpeg -y -i video.mp4 -vn -acodec libmp3lame audio.mp3
```

**Key flags:**
- `-vn` — disable video (audio only output).
- `-acodec <codec>` — audio codec to use.

**Audio codec map:**

| Format | Codec flag       |
|--------|------------------|
| mp3    | `libmp3lame`     |
| wav    | `pcm_s16le`      |
| aac    | `aac`            |
| flac   | `flac`           |

**Variations:**
```bash
# Extract as WAV (lossless)
ffmpeg -y -i video.mp4 -vn -acodec pcm_s16le audio.wav

# Extract as AAC
ffmpeg -y -i video.mp4 -vn -acodec aac audio.aac

# Copy audio codec as-is (fastest, keeps original format)
ffmpeg -y -i video.mp4 -vn -acodec copy audio.aac
```

---

## replace-audio

Replace a video's audio track with a different audio file.

```bash
ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
```

**Key flags:**
- `-i video.mp4 -i audio.mp3` — two inputs: video (index 0) and audio (index 1).
- `-c:v copy` — copy video stream without re-encoding.
- `-map 0:v:0` — take video from the first input.
- `-map 1:a:0` — take audio from the second input.
- `-shortest` — stop when the shorter input ends.

**Variations:**
```bash
# Remove audio entirely (silent video)
ffmpeg -y -i video.mp4 -c:v copy -an silent.mp4

# Mix original audio with new audio (overlay, not replace)
ffmpeg -y -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy mixed.mp4
```

---

## overlay

Add an image overlay (watermark, logo) on top of a video.

```bash
# Bottom-right corner (10px padding)
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-10:H-h-10" -c:a copy watermarked.mp4
```

**Key flags:**
- `-filter_complex "overlay=X:Y"` — position the overlay image at coordinates X,Y.
- `-c:a copy` — copy audio without re-encoding.

**Position expressions:**

| Position     | Expression              |
|--------------|-------------------------|
| Top-left     | `overlay=10:10`         |
| Top-right    | `overlay=W-w-10:10`     |
| Bottom-left  | `overlay=10:H-h-10`    |
| Bottom-right | `overlay=W-w-10:H-h-10` |
| Center       | `overlay=(W-w)/2:(H-h)/2` |

`W`/`H` = video dimensions, `w`/`h` = overlay image dimensions.

**Variations:**
```bash
# With opacity (semi-transparent watermark)
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.5[ovr];[0:v][ovr]overlay=W-w-10:10" \
  -c:a copy watermarked.mp4

# Overlay only during a time range (show from 5s to 15s)
ffmpeg -y -i video.mp4 -i logo.png \
  -filter_complex "overlay=10:10:enable='between(t,5,15)'" -c:a copy watermarked.mp4
```

---

## compress

Reduce video file size.

### CRF-based (simple, recommended)

```bash
ffmpeg -y -i video.mp4 -crf 23 -preset medium -c:a copy compressed.mp4
```

**Key flags:**
- `-crf <int>` — Constant Rate Factor. Lower = better quality, larger file. 0 = lossless, 18 = visually lossless, 23 = default, 28 = smaller/lower quality.
- `-preset <speed>` — encoding speed/compression tradeoff: `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`. Slower = smaller file at same quality.
- `-c:a copy` — copy audio as-is.

### Target file size

To hit a specific file size, calculate the required video bitrate:

```bash
# Formula: video_bitrate = (target_MB * 8 * 1024) / duration_seconds - audio_bitrate
# Example: 25MB target, 120s video, 128kbps audio
# video_bitrate = (25 * 8 * 1024) / 120 - 128 = 1578 kbps

ffmpeg -y -i video.mp4 \
  -b:v 1578k -maxrate 1578k -bufsize 3156k \
  -c:a aac -b:a 128k \
  compressed.mp4
```

**Variations:**
```bash
# Aggressive compression (smaller, lower quality)
ffmpeg -y -i video.mp4 -crf 28 -preset slow -c:a copy small.mp4

# High quality (larger file)
ffmpeg -y -i video.mp4 -crf 18 -preset slow -c:a copy hq.mp4
```

---

## convert

Convert a video to a different container format.

```bash
ffmpeg -y -i video.mov output.mp4
```

ffmpeg infers the output format from the file extension. For most conversions, this is all you need.

**Supported formats:** mp4, mov, avi, mkv, webm, gif.

### GIF conversion (high quality, two-pass palette)

```bash
# Step 1: Generate optimized palette
ffmpeg -y -i video.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png

# Step 2: Use palette for high-quality GIF
ffmpeg -y -i video.mp4 -i palette.png \
  -filter_complex "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif

# Clean up
rm palette.png
```

**Variations:**
```bash
# Quick GIF (lower quality, single pass)
ffmpeg -y -i video.mp4 -vf "fps=10,scale=320:-1" output.gif

# Convert to WebM (VP9)
ffmpeg -y -i video.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm
```
