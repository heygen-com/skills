---
name: video-probe
description: |
  Deep technical media inspection using ffprobe. Codec details, HDR detection, GOP analysis, bitrate distribution, audio/subtitle inventory.
  Use when the user says "inspect video", "video info", "what codec", "media info", "probe", "analyze file", or wants technical details about a media file.
argument-hint: "<file-or-url>"
version: 1.0.0
---

# Video Probe — Deep Media Inspection

Inspect any video/audio file for codec details, HDR metadata, keyframe intervals, bitrate distribution, and stream inventory using ffprobe.

## Step 0: Prerequisites

```bash
if ! command -v ffprobe &>/dev/null; then
  echo "ffprobe not found. Install via: brew install ffmpeg"
  exit 1
fi
```

ffprobe accepts local files and http(s) URLs directly.

## Step 1: Full Format + Stream Summary

The default starting point — shows container format, all streams, and chapters:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams -show_chapters "$INPUT" 2>/dev/null
```

Parse the JSON to report:
- **Container**: format name, duration, overall bitrate, file size
- **Video streams**: codec, resolution, frame rate, pixel format, bit depth, bitrate
- **Audio streams**: codec, sample rate, channels, layout, language
- **Subtitle streams**: codec, language
- **Chapters**: title, start/end times

## Step 2: HDR Detection

Check for HDR by examining color metadata:

```bash
ffprobe -v quiet -print_format json -show_streams \
  -select_streams v:0 "$INPUT" 2>/dev/null | \
  jq '{
    color_transfer: .streams[0].color_transfer,
    color_primaries: .streams[0].color_primaries,
    color_space: .streams[0].color_space,
    color_range: .streams[0].color_range
  }'
```

**HDR indicators**:
- `color_transfer`: `smpte2084` = HDR10/HDR10+, `arib-std-b67` = HLG
- `color_primaries`: `bt2020` = wide color gamut (HDR)
- `color_primaries`: `bt709` = SDR

For mastering display metadata (HDR10):

```bash
ffprobe -v quiet -show_frames -select_streams v:0 -read_intervals "%+#1" \
  -show_entries frame=side_data_list "$INPUT" 2>/dev/null | grep -A5 "Mastering"
```

## Step 3: Keyframe (GOP) Analysis

Analyze keyframe distribution to understand encoding structure:

```bash
ffprobe -v quiet -select_streams v:0 -show_entries frame=pict_type,pts_time \
  -print_format json "$INPUT" 2>/dev/null | \
  jq '[.frames[] | select(.pict_type == "I") | .pts_time | tonumber]'
```

Then compute GOP statistics:

```bash
# Get keyframe timestamps and compute intervals
ffprobe -v quiet -select_streams v:0 -show_entries frame=pict_type,pts_time \
  -print_format csv=p=0 "$INPUT" 2>/dev/null | \
  awk -F',' '$2=="I" {if(prev!="") print $1-prev; prev=$1}' | \
  awk '{sum+=$1; count++; if($1>max)max=$1; if(min==""||$1<min)min=$1}
       END {printf "GOP count: %d\nAvg interval: %.2fs\nMin: %.2fs\nMax: %.2fs\n", count, sum/count, min, max}'
```

## Step 4: Per-Second Bitrate Distribution

Useful for spotting bitrate spikes or understanding VBR behavior:

```bash
ffprobe -v quiet -select_streams v:0 \
  -show_entries packet=pts_time,size \
  -print_format csv=p=0 "$INPUT" 2>/dev/null | \
  awk -F',' '{sec=int($1); bytes[sec]+=$2}
       END {for(s in bytes) printf "%d,%.0f\n", s, bytes[s]*8/1000}' | \
  sort -t',' -k1 -n
```

This outputs `second,kbps` per line. For a quick summary:

```bash
# Pipe the above into stats
... | awk -F',' '{sum+=$2; count++; if($2>max)max=$2; if(min==""||$2<min)min=$2}
  END {printf "Avg: %.0f kbps\nPeak: %.0f kbps\nMin: %.0f kbps\n", sum/count, max, min}'
```

## Step 5: Audio Track & Subtitle Inventory

List all audio and subtitle streams with metadata:

```bash
ffprobe -v quiet -print_format json -show_entries \
  "stream=index,codec_name,codec_type,channels,channel_layout,sample_rate,bit_rate:stream_tags=language,title" \
  -select_streams a "$INPUT" 2>/dev/null

ffprobe -v quiet -print_format json -show_entries \
  "stream=index,codec_name,codec_type:stream_tags=language,title" \
  -select_streams s "$INPUT" 2>/dev/null
```

## Common Workflows

1. **Quick file overview**: Run Step 1, summarize in a table
2. **Is this HDR?**: Run Step 2, check color_transfer and color_primaries
3. **Why is seeking slow?**: Run Step 3 — large GOP intervals mean fewer keyframes
4. **Bitrate analysis before re-encoding**: Run Step 4 to see VBR distribution
5. **Multi-language inventory**: Run Step 5 to list all audio/subtitle tracks

## Error Handling

- **"No such file"**: Verify path exists. For URLs, check accessibility with `curl -I "$URL"`
- **Empty JSON output**: File may be corrupted or format unsupported — try `ffprobe -v error "$INPUT"` for diagnostics
- **Timeout on large files**: For bitrate/GOP analysis, use `-read_intervals "%+60"` to analyze only the first 60 seconds
- **Remote URL slow**: ffprobe streams only what it needs, but some servers don't support seeking — download first if needed
