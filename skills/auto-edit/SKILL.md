---
name: auto-edit
description: |
  Auto-edit video by removing silence and filler words. Uses auto-editor CLI for silence removal
  and Whisper for filler word detection. No API keys needed.
  Use when: (1) Removing awkward pauses and silence from a video, (2) Cutting filler words like
  "um", "uh", "like", (3) Tightening up a talking-head or podcast video, (4) Speed-ramping
  silent sections instead of cutting them, (5) Combining silence removal with filler word removal.
---

# auto-edit

Remove silence and filler words from video. Two tools, one workflow:

- **auto-editor** — CLI tool for silence removal and rendering. Run it directly.
- **detect_fillers.py** — Script that finds filler words via Whisper and outputs `--cut-out` flags for auto-editor.

## Prerequisites

**Required:** `ffmpeg` — `brew install ffmpeg`

**Recommended:** `auto-editor` — handles silence detection + rendering in one pass.
```bash
pip install auto-editor   # or: brew install auto-editor
auto-editor --version     # verify
```
See https://auto-editor.com/installing for other methods.

**For filler detection:** `openai-whisper` — needed only for `detect_fillers.py`.
```bash
pip install openai-whisper
whisper --help            # verify
```

## Workflows

### 1. Remove silence (most common)

Run auto-editor directly:

```bash
auto-editor video.mp4 -o video_edited.mp4 --no-open
```

Adjust sensitivity with `--edit` and `--margin`:

```bash
# More aggressive (lower threshold = catches more silence)
auto-editor video.mp4 --edit "audio:0.02" --margin 0.1s -o output.mp4 --no-open

# Less aggressive (higher threshold, wider margin)
auto-editor video.mp4 --edit "audio:0.08" --margin 0.3s -o output.mp4 --no-open
```

Preview what would be cut (no rendering):

```bash
auto-editor video.mp4 --preview --no-open
```

### 2. Remove filler words

Detect fillers first, then pass the cut ranges to auto-editor:

```bash
# Step 1: Detect fillers (outputs JSON with auto-editor flags)
python3 skills/auto-edit/scripts/detect_fillers.py video.mp4

# Step 2: Use the auto_editor_command from the JSON output, or manually:
auto-editor video.mp4 --edit none --cut-out 9.63s,9.91s --cut-out 38.93s,39.39s -o output.mp4 --no-open
```

Custom filler word list:

```bash
python3 skills/auto-edit/scripts/detect_fillers.py video.mp4 --filler-words "um,uh,like,so"
```

### 3. Remove both silence and fillers

Combine auto-editor's silence detection with filler word `--cut-out` flags:

```bash
# Step 1: Get filler cut flags
python3 skills/auto-edit/scripts/detect_fillers.py video.mp4 -q

# Step 2: Run auto-editor with silence detection + filler cuts
auto-editor video.mp4 --edit "audio:0.04" --cut-out 9.63s,9.91s --cut-out 38.93s,39.39s -o output.mp4 --no-open
```

### 4. Speed-ramp silence (instead of cutting)

Instead of removing silence entirely, speed it up for a smoother result:

```bash
# 3x speed through silence
auto-editor video.mp4 --when-silent "speed:3" -o output.mp4 --no-open

# 2x speed through silence, slight speedup of speech too
auto-editor video.mp4 --when-silent "speed:2" --when-normal "speed:1.1" -o output.mp4 --no-open
```

### 5. Without auto-editor (ffmpeg fallback)

If auto-editor is not installed, use ffmpeg's silencedetect filter to find silent segments, then trim and concat:

```bash
# Detect silence
ffmpeg -i video.mp4 -af "silencedetect=noise=0.04:d=0.5" -f null - 2>&1 | grep "silence_"

# Then use video-edit skill to trim and concat the keep segments
```

See `references/ffmpeg-fallback.md` for the full ffmpeg-based workflow.

## detect_fillers.py Reference

| Flag | Description |
|------|-------------|
| `input` | Input video or audio file (positional) |
| `--whisper-model` | tiny, base (default), small, medium, large |
| `--filler-words` | Comma-separated custom list |
| `--padding` | Seconds of padding around cuts (default: 0.05) |
| `-o, --output` | Write JSON to file |
| `-q, --quiet` | JSON only, no progress |

Output includes ready-to-use `auto_editor_command` and `auto_editor_flags` fields.

Default filler words: um, uh, uhh, umm, hmm, hm, like, you know, basically, actually, literally, right, so, i mean

## auto-editor Quick Reference

See `references/auto-editor-guide.md` for the full CLI reference.

| What | Command |
|------|---------|
| Remove silence | `auto-editor video.mp4 -o out.mp4 --no-open` |
| Adjust threshold | `--edit "audio:0.04"` (default), lower=more sensitive |
| Adjust margin | `--margin 0.2s` (default), padding around speech |
| Cut specific ranges | `--cut-out 5.2s,6.8s` (repeat for multiple) |
| Speed-ramp silence | `--when-silent "speed:3"` |
| Preview (no render) | `--preview --no-open` |
| Quiet mode | `-q` |

## References

- `references/auto-editor-guide.md` — Full auto-editor CLI reference and advanced usage
- `references/ffmpeg-fallback.md` — Silence detection and rendering without auto-editor
