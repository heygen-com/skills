# Setup Guide

## System Requirements

- **Python**: 3.8 or later (ships with macOS)
- **ffmpeg**: includes both `ffmpeg` and `ffprobe`

## Installation

### macOS (Homebrew)

```bash
brew install ffmpeg
```

### Ubuntu / Debian

```bash
sudo apt update && sudo apt install -y ffmpeg
```

### Windows (Chocolatey)

```powershell
choco install ffmpeg
```

### Windows (winget)

```powershell
winget install ffmpeg
```

## Verify Installation

Run the setup checker:

```bash
python3 skills/video-edit/scripts/setup.py
```

Expected output when everything is installed:

```json
{
  "ok": true,
  "dependencies": [
    {
      "name": "ffmpeg",
      "installed": true,
      "path": "/opt/homebrew/bin/ffmpeg",
      "version": "ffmpeg version 7.x ..."
    },
    {
      "name": "ffprobe",
      "installed": true,
      "path": "/opt/homebrew/bin/ffprobe",
      "version": "ffprobe version 7.x ..."
    }
  ]
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ffmpeg: command not found` | Install ffmpeg (see above) |
| `Permission denied` | Run `chmod +x` on the script, or invoke via `python3` |
| Poor GIF quality | Ensure ffmpeg was built with `--enable-libx264` (default in Homebrew) |
| No audio after replace-audio | Confirm the audio file format is supported (mp3, aac, wav) |
