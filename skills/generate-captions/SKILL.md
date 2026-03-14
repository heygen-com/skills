---
name: generate-captions
description: |
  Generate styled captions for video using local Whisper transcription and ASS subtitles.
  Use when: (1) Adding captions/subtitles to a video, (2) Creating TikTok/Reels-style word-by-word captions,
  (3) Transcribing video with word-level timestamps, (4) Previewing and editing captions before final render.
---

# Generate Captions Skill

Local-first caption generation: transcribe with Whisper, style with presets or CLI flags, burn in with ffmpeg.

## Workflow

```bash
# 1. Transcribe → JSON (word-level timestamps)
python3 scripts/caption_video.py video.mp4 --transcribe-only

# 2. Style + generate ASS (preset or custom)
python3 scripts/caption_video.py video.mp4 --json captions.json --style pop
python3 scripts/caption_video.py video.mp4 --json captions.json --style pop --font-size 72 --primary-color "#FF0000"

# 3. (Optional) Preview in browser
python3 scripts/generate_preview.py captions.json --video video.mp4
python3 -m http.server 8123 --directory output/

# 4. Burn captions into video (just ffmpeg)
ffmpeg -y -i video.mp4 -vf "ass=captions.ass" -c:a copy captioned.mp4

# 5. Or use your own ASS file
ffmpeg -y -i video.mp4 -vf "ass=custom.ass" -c:a copy captioned.mp4
```

## Style Presets

| Preset | Position | Animation | Key Visual |
|--------|----------|-----------|------------|
| `classic` | bottom | karaoke-sweep | White text, black outline, orange highlight. Standard subtitles. |
| `pop` | center | karaoke-sweep | White text, mint highlight, outline+shadow. TikTok style. |
| `bold` | center | karaoke-sweep | Large text, gold highlight, high impact. |
| `boxed` | center | karaoke-sweep | White text on black semi-transparent box, cyan highlight. |
| `single` | center | karaoke-sweep | One word at a time, purple highlight, outline+shadow. |

See [references/style-presets.md](references/style-presets.md) for full preset details.

## CLI Flags

### Mode

| Flag | Description |
|------|-------------|
| `video` | Input video file (positional) |
| `--transcribe-only` | Only transcribe → captions.json (skip ASS generation) |
| `--json FILE` | Load existing caption JSON (skip transcription) |
| `--list-styles` | List all presets and exit |

### Whisper

| Flag | Description |
|------|-------------|
| `--model` | Whisper model size: tiny, base, small, medium, large (default: base) |

### Style Overrides

All override flags take precedence over preset defaults and JSON style values.

| Flag | Description |
|------|-------------|
| `--style` | Preset name: classic, pop, bold, boxed, single |
| `--font-family` | Font family name |
| `--font-size` | Font size in pt |
| `--primary-color` | Base text color (`#RRGGBB`) |
| `--secondary-color` | Highlight/active word color (`#RRGGBB`) |
| `--outline-color` | Outline color (`#RRGGBB`) |
| `--outline-width` | Outline width in px |
| `--shadow-depth` | Drop shadow depth in px (0=none) |
| `--background-color` | Background box color (`#RRGGBB`, enables boxed mode) |
| `--position` | Caption position: bottom, center, top |
| `--animation` | Animation: none, karaoke, karaoke-sweep |
| `--words-per-line` | Max words per display chunk |
| `--single-words` | Show one word at a time |

### Output

| Flag | Description |
|------|-------------|
| `--output-dir DIR` | Output directory (default: same as video) |
| `-o, --output FILE` | Write result JSON to file instead of stdout |
| `-q, --quiet` | Suppress progress messages |

## Color Semantics

- `primary_color` — base text color (what you see most of the time)
- `secondary_color` — highlight/active word color (the karaoke sweep target)

In the ASS file, these map to ASS PrimaryColour (highlight) and SecondaryColour (base) respectively, since ASS karaoke sweeps _from_ secondary _to_ primary.

## Caption JSON Schema

```json
{
  "video_path": "/abs/path/video.mp4",
  "resolution": { "width": 1920, "height": 1080 },
  "duration": 120.5,
  "style": {
    "preset": "pop",
    "font_family": "Arial Black",
    "font_size": 60,
    "primary_color": "#FFFFFF",
    "secondary_color": "#00FFB2",
    "outline_color": "#000000",
    "outline_width": 3,
    "shadow_depth": 2,
    "background_color": null,
    "position": "center",
    "animation": "karaoke-sweep",
    "words_per_line": 4,
    "single_words": false
  },
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "Hello world this is a test",
      "words": [
        { "text": "Hello", "start": 0.0, "end": 0.4 },
        { "text": "world", "start": 0.5, "end": 0.9 }
      ]
    }
  ]
}
```

## Dependencies

- **FFmpeg + FFprobe** (system) — audio extraction, video burn-in
- **openai-whisper** (pip) — transcription (auto-installed on first run)

No pysubs2 dependency. ASS files are generated as raw strings for full control.

## ASS Format Reference

The generated ASS uses [Advanced SubStation Alpha v4+](https://fileformats.fandom.com/wiki/SubStation_Alpha#Advanced_SubStation_Alpha).

- `\kf<cs>` — karaoke sweep (smooth fill over centiseconds)
- `\k<cs>` — karaoke instant (fill at start of duration)
- Background boxes use a two-layer approach: `DefaultBG` style (BorderStyle=3, opaque box) on layer 0, `Default` style (text+outline) on layer 1
