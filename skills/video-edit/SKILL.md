---
name: video-edit
description: |
  Edit videos locally using ffmpeg. Trim, concat, resize, speed, overlay, extract audio, compress, and convert.
  Use when: (1) Trimming or cutting video segments, (2) Concatenating multiple clips, (3) Resizing video for social platforms,
  (4) Extracting or replacing audio, (5) Compressing video, (6) Converting video formats, (7) Getting video info.
---

# Video Edit Skill

Edit videos locally using ffmpeg via a Python CLI.

## Prerequisites

Run the setup check first:

```bash
python3 skills/video-edit/scripts/setup.py
```

## Operations

### Trim a video

```bash
# By start/end timestamps (HH:MM:SS or seconds)
python3 skills/video-edit/scripts/edit_video.py trim video.mp4 --start 00:30 --end 01:45

# By start + duration (in seconds)
python3 skills/video-edit/scripts/edit_video.py trim video.mp4 --start 30 --duration 75
```

### Concatenate clips

```bash
python3 skills/video-edit/scripts/edit_video.py concat clip1.mp4 clip2.mp4 clip3.mp4
python3 skills/video-edit/scripts/edit_video.py concat clip1.mp4 clip2.mp4 -o merged.mp4
```

### Resize for a platform

```bash
python3 skills/video-edit/scripts/edit_video.py resize video.mp4 --target tiktok
python3 skills/video-edit/scripts/edit_video.py resize video.mp4 --target youtube
python3 skills/video-edit/scripts/edit_video.py resize video.mp4 --target square
python3 skills/video-edit/scripts/edit_video.py resize video.mp4 --width 1280 --height 720
```

### Change speed

```bash
python3 skills/video-edit/scripts/edit_video.py speed video.mp4 --factor 2.0   # 2x faster
python3 skills/video-edit/scripts/edit_video.py speed video.mp4 --factor 0.5   # half speed
```

### Extract audio

```bash
python3 skills/video-edit/scripts/edit_video.py extract-audio video.mp4
python3 skills/video-edit/scripts/edit_video.py extract-audio video.mp4 --format wav
```

### Replace audio

```bash
python3 skills/video-edit/scripts/edit_video.py replace-audio video.mp4 narration.mp3
```

### Add image overlay

```bash
python3 skills/video-edit/scripts/edit_video.py overlay video.mp4 logo.png --position top-right --opacity 0.8
python3 skills/video-edit/scripts/edit_video.py overlay video.mp4 watermark.png --position bottom-left
```

### Compress

```bash
python3 skills/video-edit/scripts/edit_video.py compress video.mp4 --target-size 25MB
python3 skills/video-edit/scripts/edit_video.py compress video.mp4 --crf 28
```

### Convert format

```bash
python3 skills/video-edit/scripts/edit_video.py convert video.mov --format mp4
python3 skills/video-edit/scripts/edit_video.py convert video.mp4 --format gif
```

### Get video info

```bash
python3 skills/video-edit/scripts/edit_video.py info video.mp4
```

## Output

All operations produce JSON output to stdout:

```json
{
  "operation": "trim",
  "input": {"path": "video.mp4", "duration": 120.5, "size_mb": 45.2},
  "output": {"path": "video_trimmed.mp4", "duration": 75.0, "size_mb": 28.1},
  "command": "ffmpeg -ss 00:30 -to 01:45 -i video.mp4 -c copy video_trimmed.mp4"
}
```
