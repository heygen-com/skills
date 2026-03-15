---
name: scene-detect
description: |
  Detect scene boundaries and extract keyframes using ffmpeg scene detection filter. Generates thumbnails, chapter markers, and can split video at cut points.
  Use when the user says "detect scenes", "find cuts", "scene changes", "extract keyframes", "split by scene", "chapter markers".
argument-hint: "<video-file> [threshold=0.3]"
version: 1.0.0
---

# Scene Detect — Scene Boundary Detection & Keyframe Extraction

Detect scene changes in video files, extract thumbnail at each cut point, generate chapter markers, or split video into segments — all using ffmpeg's built-in scene detection.

## Step 0: Prerequisites

```bash
if ! command -v ffmpeg &>/dev/null; then
  echo "ffmpeg not found. Install via: brew install ffmpeg"
  exit 1
fi
```

## Step 1: Detect Scene Boundaries

Use the `select` filter with scene change detection. Default threshold is 0.3 (range 0.0–1.0, lower = more sensitive):

```bash
THRESHOLD=0.3
ffmpeg -i "$INPUT" -vf "select='gt(scene,$THRESHOLD)',showinfo" -vsync vfr -f null - 2>&1 | \
  grep showinfo | awk -F'pts_time:' '{print $2}' | awk '{printf "%.3f\n", $1}'
```

This outputs timestamps (in seconds) where scene changes occur.

**Threshold guide**:
- `0.1–0.2`: Very sensitive — catches subtle transitions, may over-detect
- `0.3`: Good default for most edited video
- `0.4–0.6`: Only hard cuts, ignores dissolves/fades
- `0.7+`: Only the most dramatic changes

## Step 2: Extract Thumbnails at Scene Changes

Generate a thumbnail image at each detected cut point:

```bash
THRESHOLD=0.3
OUTPUT_DIR="./scene_thumbnails"
mkdir -p "$OUTPUT_DIR"

ffmpeg -i "$INPUT" \
  -vf "select='gt(scene,$THRESHOLD)',scale=320:-1" \
  -vsync vfr \
  "$OUTPUT_DIR/scene_%04d.jpg" 2>&1
```

This creates `scene_0001.jpg`, `scene_0002.jpg`, etc. — one per scene change.

To also get the timestamp of each thumbnail:

```bash
ffmpeg -i "$INPUT" \
  -vf "select='gt(scene,$THRESHOLD)',showinfo,scale=320:-1" \
  -vsync vfr \
  "$OUTPUT_DIR/scene_%04d.jpg" 2>&1 | \
  grep showinfo | awk -F'pts_time:' '{print $2}' | awk '{printf "%.3f\n", $1}'
```

## Step 3: Generate Chapter Markers

Create an ffmetadata file with chapters at each scene boundary. This can be embedded into the video for chapter navigation:

```bash
THRESHOLD=0.3

# Get scene timestamps
TIMESTAMPS=$(ffmpeg -i "$INPUT" -vf "select='gt(scene,$THRESHOLD)',showinfo" -vsync vfr -f null - 2>&1 | \
  grep showinfo | awk -F'pts_time:' '{print $2}' | awk '{printf "%.3f\n", $1}')

# Get total duration in seconds
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$INPUT")

# Build ffmetadata file
{
  echo ";FFMETADATA1"
  PREV=0
  CHAPTER=1
  while IFS= read -r ts; do
    TS_MS=$(awk "BEGIN {printf \"%.0f\", $ts * 1000}")
    PREV_MS=$(awk "BEGIN {printf \"%.0f\", $PREV * 1000}")
    echo ""
    echo "[CHAPTER]"
    echo "TIMEBASE=1/1000"
    echo "START=$PREV_MS"
    echo "END=$TS_MS"
    echo "title=Scene $CHAPTER"
    PREV=$ts
    CHAPTER=$((CHAPTER + 1))
  done <<< "$TIMESTAMPS"
  # Final chapter to end
  DUR_MS=$(awk "BEGIN {printf \"%.0f\", $DURATION * 1000}")
  PREV_MS=$(awk "BEGIN {printf \"%.0f\", $PREV * 1000}")
  echo ""
  echo "[CHAPTER]"
  echo "TIMEBASE=1/1000"
  echo "START=$PREV_MS"
  echo "END=$DUR_MS"
  echo "title=Scene $CHAPTER"
} > chapters.ffmeta

echo "Chapter file written to chapters.ffmeta"
```

Embed chapters into the video:

```bash
ffmpeg -i "$INPUT" -i chapters.ffmeta -map_metadata 1 -codec copy "$OUTPUT"
```

## Step 4: Split Video at Scene Boundaries

Segment the video into separate files at each scene change:

```bash
THRESHOLD=0.3

# Get scene timestamps
TIMESTAMPS=$(ffmpeg -i "$INPUT" -vf "select='gt(scene,$THRESHOLD)',showinfo" -vsync vfr -f null - 2>&1 | \
  grep showinfo | awk -F'pts_time:' '{print $2}' | awk '{printf "%.3f\n", $1}')

# Build segment list
PREV=0
SEG=1
while IFS= read -r ts; do
  DURATION_SEG=$(awk "BEGIN {printf \"%.3f\", $ts - $PREV}")
  ffmpeg -i "$INPUT" -ss "$PREV" -t "$DURATION_SEG" -c copy "segment_$(printf '%03d' $SEG).mp4"
  PREV=$ts
  SEG=$((SEG + 1))
done <<< "$TIMESTAMPS"

# Final segment
ffmpeg -i "$INPUT" -ss "$PREV" -c copy "segment_$(printf '%03d' $SEG).mp4"

echo "Split into $SEG segments."
```

**Note**: `-c copy` is fast but may have imprecise cuts (cuts at nearest keyframe). For frame-accurate splits, re-encode:

```bash
ffmpeg -i "$INPUT" -ss "$PREV" -t "$DURATION_SEG" -c:v libx264 -c:a aac "segment_001.mp4"
```

## Common Workflows

1. **Quick scene count**: Run Step 1, count output lines
2. **Visual scene summary**: Run Step 2 to get thumbnail grid of all scenes
3. **Add chapters to a long video**: Run Step 3, then embed with `ffmpeg -map_metadata`
4. **Split interview into segments**: Run Step 4 with threshold 0.4 (hard cuts only)
5. **Combine with probe**: Use `/video-probe` first to check duration/codec, then detect scenes

## Error Handling

- **Too many scenes detected**: Increase threshold (e.g., 0.5 or higher)
- **No scenes detected**: Lower threshold (e.g., 0.1) — video may have only soft transitions
- **Segment splits are imprecise**: Use re-encoding instead of `-c copy` for frame-accurate cuts
- **Very long video is slow**: Add `-t 60` after `-i` to test on just the first 60 seconds first
- **Audio-only file**: Scene detection requires a video stream — this skill is video-only
