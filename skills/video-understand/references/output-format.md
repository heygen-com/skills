# Output Format

## Result JSON

The main script (`understand_video.py`) outputs a JSON object to stdout (or to a file with `-o`) containing video metadata, extracted frame paths, and transcription data.

```json
{
  "video": "video.mp4",
  "duration": 18.076,
  "resolution": {
    "width": 1224,
    "height": 1080
  },
  "mode": "scene",
  "frames": [
    {
      "path": "/absolute/path/to/frames/frame_0001.jpg",
      "timestamp": 0.0,
      "timestamp_formatted": "00:00"
    },
    {
      "path": "/absolute/path/to/frames/frame_0002.jpg",
      "timestamp": 3.2,
      "timestamp_formatted": "00:03"
    }
  ],
  "frame_count": 12,
  "transcript": [
    {
      "start": 0.0,
      "end": 2.5,
      "text": "Hello and welcome to this video."
    },
    {
      "start": 2.8,
      "end": 5.1,
      "text": "Today we will discuss..."
    }
  ],
  "text": "Hello and welcome to this video. Today we will discuss...",
  "note": "Use the Read tool to view frame images for visual understanding."
}
```

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `video` | string | Original video filename (basename) |
| `duration` | float | Video duration in seconds |
| `resolution` | object | Video resolution with `width` and `height` |
| `mode` | string | Extraction mode used: `scene`, `keyframe`, or `interval` |
| `frames` | array | Array of extracted frame objects |
| `frame_count` | integer | Number of frames extracted |
| `transcript` | array or null | Array of transcript segments, or `null` if transcription was skipped |
| `text` | string or null | Full transcript as a single string, or `null` if skipped |
| `note` | string | Hint for Claude on how to use the frame images |

## Frame Object

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Absolute path to the extracted JPEG frame |
| `timestamp` | float | Frame timestamp in seconds from the start of the video |
| `timestamp_formatted` | string | Human-readable timestamp in `MM:SS` or `HH:MM:SS` format |

## Transcript Segment

| Field | Type | Description |
|-------|------|-------------|
| `start` | float | Segment start time in seconds |
| `end` | float | Segment end time in seconds |
| `text` | string | Transcribed text for this segment |

## Frame Path Convention

Frames are extracted to a directory next to the video file:

```
video.mp4
video_frames/
  frame_0001.jpg
  frame_0002.jpg
  ...
```

The directory name is `{video_stem}_frames`. All frame paths in the JSON output are absolute paths, suitable for direct use with the Read tool.

## Null Fields

- `transcript` and `text` are `null` when `--no-transcribe` is used or when Whisper is not installed.
- If scene detection finds no scenes, mode automatically falls back to `interval` and the `mode` field reflects the actual mode used.

## Using with Claude

To visually inspect the video content, use the Read tool on the frame paths returned in the `frames` array. Claude can view JPEG images directly and describe their contents. Combined with the transcript, this provides full video understanding without any cloud APIs.
