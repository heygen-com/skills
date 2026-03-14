# Silence Removal with ffmpeg (No auto-editor)

When auto-editor is not installed, use ffmpeg directly for silence detection and removal.

## Step 1: Detect silence

```bash
ffmpeg -i video.mp4 -af "silencedetect=noise=0.04:d=0.5" -f null - 2>&1 | grep "silence_"
```

Parameters:
- `noise=0.04` — amplitude threshold (0.0-1.0). Lower = catches more silence.
- `d=0.5` — minimum silence duration in seconds.

Output lines look like:
```
[silencedetect @ 0x...] silence_start: 5.2
[silencedetect @ 0x...] silence_end: 6.8 | silence_duration: 1.6
```

## Step 2: Trim and concat keep segments

Use the video-edit skill or ffmpeg directly to trim out the keep segments and concat them:

```bash
# Trim each keep segment to MPEG-TS
ffmpeg -y -ss 0 -to 5.2 -i video.mp4 -c:v libx264 -preset fast -c:a aac -f mpegts seg_0.ts
ffmpeg -y -ss 6.8 -to 45.0 -i video.mp4 -c:v libx264 -preset fast -c:a aac -f mpegts seg_1.ts

# Concat
ffmpeg -y -i "concat:seg_0.ts|seg_1.ts" -c copy output.mp4
```

## Limitations vs auto-editor

- **No frame-accurate cuts** — ffmpeg's `-ss` with `-c copy` seeks to the nearest keyframe. Re-encoding (shown above) gives accurate cuts but is slower.
- **No margin control** — you must manually adjust the keep segment boundaries.
- **More manual work** — auto-editor handles detection + rendering in one pass.

Install auto-editor for better results: `pip install auto-editor` or `brew install auto-editor`.
