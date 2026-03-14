# Setup Guide

## System Requirements

- Python 3.8 or later
- FFmpeg (required for frame extraction and audio processing)
- FFprobe (usually bundled with FFmpeg)
- openai-whisper (optional, for local audio transcription)

## Installation

### 1. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH.

### 2. Install Whisper (Optional)

Whisper enables local audio transcription. The skill works without it (frames-only mode).

```bash
pip install openai-whisper
```

### 3. Verify Installation

```bash
python3 skills/video-understand/scripts/setup.py
```

This will check for all required and optional dependencies and report any issues.

## Whisper Models

The skill uses OpenAI Whisper for transcription. Available models:

| Model | Size | Speed | Accuracy | VRAM |
|-------|------|-------|----------|------|
| tiny | 39M | Fastest | Lower | ~1 GB |
| base | 74M | Fast | Good | ~1 GB |
| small | 244M | Medium | Better | ~2 GB |
| medium | 769M | Slow | High | ~5 GB |
| large | 1550M | Slowest | Highest | ~10 GB |

The default model is `base`, which provides a good balance of speed and accuracy. Use `--whisper-model` to change:

```bash
python3 skills/video-understand/scripts/understand_video.py video.mp4 --whisper-model small
```

Models are downloaded automatically on first use and cached in `~/.cache/whisper/`.

## Troubleshooting

### FFmpeg not found
Ensure FFmpeg is installed and available in your PATH:
```bash
which ffmpeg
ffmpeg -version
```

### Whisper import error
Make sure you installed `openai-whisper`, not just `whisper`:
```bash
pip install openai-whisper
```

### CUDA / GPU acceleration
Whisper will automatically use CUDA if available. For CPU-only systems, it runs on CPU without any extra configuration.

For GPU acceleration:
```bash
pip install openai-whisper torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### No scenes detected
If scene detection mode returns zero frames, the script automatically falls back to interval mode. This happens with videos that have gradual transitions or are very short. You can also use `--mode interval` or `--mode keyframe` directly.
