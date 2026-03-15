---
name: video-gif
description: |
  Convert video to optimized GIF, WebP, or APNG with two-pass palette generation and size targeting. Supports Discord, Slack, Twitter size limits.
  Use when the user says "make a gif", "convert to gif", "video to gif", "create webp", "animated png", "gif from video".
argument-hint: "<video-file> [format=gif] [max-size=10MB]"
version: 1.0.0
---

# Video GIF — Optimized GIF/WebP/APNG Conversion

Convert video clips to high-quality GIFs using two-pass palette optimization, or to WebP/APNG for smaller files. Includes size targeting for platform limits.

## Step 0: Prerequisites

```bash
if ! command -v ffmpeg &>/dev/null; then
  echo "ffmpeg not found. Install via: brew install ffmpeg"
  exit 1
fi
```

## Step 1: Two-Pass Palette GIF (High Quality)

The key to good GIFs — generate an optimized palette first, then apply it:

```bash
# Pass 1: Generate palette
ffmpeg -i "$INPUT" -vf "fps=15,scale=480:-1:flags=lanczos,palettegen=stats_mode=diff" \
  -y /tmp/palette.png

# Pass 2: Create GIF using palette
ffmpeg -i "$INPUT" -i /tmp/palette.png \
  -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5" \
  -y output.gif
```

**Key parameters**:
- `fps=15`: Frame rate (10–15 is typical for GIFs, 24+ for smooth)
- `scale=480:-1`: Width in pixels, height auto-calculated to preserve aspect ratio
- `stats_mode=diff`: Optimizes palette for animations (vs `full` for stills)
- `dither=bayer:bayer_scale=5`: Bayer dithering for smooth gradients (alternatives: `sierra2_4a`, `none`)

**To extract a specific time range**:

```bash
# Add -ss (start) and -t (duration) before the input
ffmpeg -ss 5 -t 3 -i "$INPUT" -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" -y /tmp/palette.png
ffmpeg -ss 5 -t 3 -i "$INPUT" -i /tmp/palette.png \
  -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse" -y output.gif
```

## Step 2: WebP Output (50% Smaller Than GIF)

WebP animated images are significantly smaller than GIF with better quality:

```bash
ffmpeg -i "$INPUT" -vf "fps=15,scale=480:-1:flags=lanczos" \
  -vcodec libwebp -lossless 0 -compression_level 6 \
  -q:v 70 -loop 0 -y output.webp
```

**Parameters**:
- `-q:v 70`: Quality (0–100, higher = better quality but larger)
- `-lossless 0`: Lossy mode (set to 1 for lossless, but much larger)
- `-loop 0`: Loop forever (1 = play once)

## Step 3: APNG Output (Best Quality, Largest)

APNG preserves full alpha transparency and has the best visual quality:

```bash
ffmpeg -i "$INPUT" -vf "fps=15,scale=480:-1:flags=lanczos" \
  -plays 0 -f apng -y output.apng
```

## Step 4: Size-Targeted Conversion

When you need to hit a specific file size limit, use binary search on width and fps:

**Platform limits**:
| Platform | Max Size | Recommended |
|-|-|-|
| Discord | 10 MB (25 MB Nitro) | 8 MB target |
| Slack | 5 MB (free), varies | 4 MB target |
| Twitter/X | 15 MB | 12 MB target |
| iMessage | 100 MB | No limit concern |

**Binary search approach**:

```bash
TARGET_KB=8000  # 8 MB in KB
INPUT="$1"
FPS=12
MIN_W=160
MAX_W=640
BEST_W=$MIN_W

# Get file size helper (cross-platform)
get_size_kb() {
  if [[ "$(uname)" == "Darwin" ]]; then
    echo $(( $(stat -f%z "$1") / 1024 ))
  else
    echo $(( $(stat -c%s "$1") / 1024 ))
  fi
}

while [ $MIN_W -le $MAX_W ]; do
  MID_W=$(( (MIN_W + MAX_W) / 2 ))
  # Round to even (required by some codecs)
  MID_W=$(( MID_W / 2 * 2 ))

  ffmpeg -i "$INPUT" -vf "fps=$FPS,scale=$MID_W:-2:flags=lanczos,palettegen" -y /tmp/palette.png 2>/dev/null
  ffmpeg -i "$INPUT" -i /tmp/palette.png \
    -lavfi "fps=$FPS,scale=$MID_W:-2:flags=lanczos [x]; [x][1:v] paletteuse" \
    -y /tmp/test_output.gif 2>/dev/null

  SIZE_KB=$(get_size_kb /tmp/test_output.gif)
  echo "Width: ${MID_W}px -> ${SIZE_KB}KB (target: ${TARGET_KB}KB)"

  if [ $SIZE_KB -le $TARGET_KB ]; then
    BEST_W=$MID_W
    MIN_W=$((MID_W + 2))
  else
    MAX_W=$((MID_W - 2))
  fi
done

echo "Optimal width: ${BEST_W}px"
# Final render at optimal width
ffmpeg -i "$INPUT" -vf "fps=$FPS,scale=$BEST_W:-2:flags=lanczos,palettegen" -y /tmp/palette.png
ffmpeg -i "$INPUT" -i /tmp/palette.png \
  -lavfi "fps=$FPS,scale=$BEST_W:-2:flags=lanczos [x]; [x][1:v] paletteuse" \
  -y output.gif
```

**If still too large after minimum width**: Reduce fps (try 8), shorten duration with `-t`, or switch to WebP.

## Step 5: Loop Control

```bash
# Play once (no loop)
ffmpeg -i "$INPUT" -i /tmp/palette.png \
  -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse" \
  -loop -1 -y output.gif

# Loop 3 times
ffmpeg -i "$INPUT" -i /tmp/palette.png \
  -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse" \
  -loop 3 -y output.gif

# Loop forever (default)
# -loop 0 (or omit)
```

## Common Workflows

1. **Quick GIF from video**: Run Step 1 with defaults (480px, 15fps)
2. **Discord-ready GIF**: Run Step 4 with `TARGET_KB=8000`
3. **Smallest possible animation**: Use Step 2 (WebP) at q:v 50
4. **GIF of specific moment**: Use `-ss 10 -t 3` to grab 3 seconds starting at 10s
5. **High-quality reaction GIF**: Step 1 with `scale=320:-1`, `fps=12`, `dither=sierra2_4a`

## Error Handling

- **"height not divisible by 2"**: Use `scale=480:-2` (rounds height to even) instead of `scale=480:-1`
- **GIF too large**: Reduce width, fps, or duration. Or switch to WebP (Step 2)
- **Colors look bad**: Try `dither=sierra2_4a` or `stats_mode=full` in palettegen
- **Palette file missing**: Ensure Pass 1 completed before Pass 2 — check for errors in palettegen step
- **WebP not supported**: Check `ffmpeg -encoders | grep webp` — if missing, rebuild ffmpeg with libwebp
