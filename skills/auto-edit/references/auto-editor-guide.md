# auto-editor CLI Reference

[auto-editor](https://auto-editor.com) is an open-source tool for automatically editing video based on audio levels, motion, or subtitles. This skill uses it as the preferred rendering backend.

## Installation

```bash
# macOS (recommended)
brew install auto-editor

# pip
pip install auto-editor

# Verify
auto-editor --version
```

See full install guide: https://auto-editor.com/installing

## How This Skill Uses auto-editor

### Silence removal only

```bash
auto-editor video.mp4 --edit "audio:0.04" --margin 0.2s -o output.mp4 --no-open
```

### Silence + filler word removal

Filler word time ranges (from Whisper) are injected via `--cut-out`:

```bash
auto-editor video.mp4 --edit "audio:0.04" --margin 0.2s \
  --cut-out 9.63s,9.91s --cut-out 38.93s,39.39s \
  -o output.mp4 --no-open
```

### Filler words only (no silence removal)

```bash
auto-editor video.mp4 --edit none \
  --cut-out 9.63s,9.91s --cut-out 38.93s,39.39s \
  -o output.mp4 --no-open
```

## Key CLI Options

### `--edit METHOD`

Controls how auto-editor decides what to cut. Sugar syntax:

```
--edit "audio:THRESHOLD"
--edit "audio:0.04,stream=0"
--edit "motion:0.02"
--edit "none"                   # Don't auto-detect, only use --cut-out
```

**Audio parameters:**
| Param | Default | Description |
|-------|---------|-------------|
| threshold | 0.04 | Amplitude threshold (0.0-1.0). Lower = more sensitive |
| stream | all | Which audio stream(s) to analyze |
| mincut | 6 | Minimum cut length (in timebase frames) |
| minclip | 3 | Minimum clip length (in timebase frames) |

### `--margin LENGTH`

Sets how much padding to keep around "loud" sections. Prevents cuts from landing right at the edge of speech.

```
--margin 0.2s    # 200ms (default)
--margin 0.1s    # Tighter cuts
--margin 0.5s    # More breathing room
```

### `--cut-out START,STOP`

Cut a specific time range. Can be repeated for multiple ranges:

```
--cut-out 5.2s,6.8s --cut-out 12.1s,12.6s
```

Time values must include the `s` suffix for seconds.

### `--when-silent ACTION`

What to do with silent sections (default: `cut`):

```
--when-silent cut              # Remove completely (default)
--when-silent "speed:2"        # Speed up 2x instead of cutting
--when-silent "speed:3"        # Speed up 3x
```

### `--when-normal ACTION`

What to do with non-silent sections (default: `nil` / unchanged):

```
--when-normal nil              # Keep as-is (default)
--when-normal "speed:1.2"     # Slight speedup of speech
```

### `--preview` / `--stats`

Preview what would be cut without rendering:

```bash
auto-editor video.mp4 --preview --no-open
```

Shows clip count, cut count, and duration stats.

### Output options

```
-o, --output FILE        Output file path
--no-open                Don't auto-open output after rendering
-q, --quiet              Less output
--debug                  Verbose debug output
```

## Advanced: Speed Ramping Instead of Cutting

Instead of removing silence entirely, speed it up:

```bash
# 3x speed through silence
auto-editor video.mp4 --when-silent "speed:3" -o output.mp4 --no-open

# 2x speed through silence, slight speedup of speech
auto-editor video.mp4 --when-silent "speed:2" --when-normal "speed:1.1" -o output.mp4 --no-open
```

## Advanced: Motion-Based Editing

Edit based on visual motion instead of audio:

```bash
auto-editor video.mp4 --edit "motion:0.02" -o output.mp4 --no-open
```

## Docs

- Install guide: https://auto-editor.com/installing
- Full docs: https://auto-editor.com/docs/
- Edit flag reference: https://auto-editor.com/ref/edit
- GitHub: https://github.com/WyattBlue/auto-editor
