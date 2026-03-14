# Operations Reference

Complete reference for every operation supported by `edit_video.py`.

---

## trim

Cut a segment from a video using stream copy (no re-encoding, very fast).

```
edit_video.py trim <input> --start <time> [--end <time> | --duration <seconds>] [-o <output>]
```

| Flag | Description | Example |
|------|-------------|---------|
| `--start` | Start timestamp (required) | `00:01:30`, `90`, `1:30` |
| `--end` | End timestamp | `00:02:00`, `120` |
| `--duration` | Duration in seconds (alternative to `--end`) | `30`, `45.5` |
| `-o` | Output path (optional, auto-generated if omitted) | `clip.mp4` |

Timestamps accept: `HH:MM:SS`, `MM:SS`, or raw seconds (integer or float).

---

## concat

Join multiple video files into a single file.

```
edit_video.py concat <input1> <input2> [<input3> ...] [-o <output>]
```

All inputs should share the same codec, resolution, and frame rate for best results. Uses the ffmpeg concat demuxer with stream copy.

---

## resize

Resize a video to specific dimensions or a social-media platform preset.

```
edit_video.py resize <input> (--target <preset> | --width <w> --height <h>) [-o <output>]
```

### Platform presets

| Preset | Resolution | Aspect Ratio |
|--------|-----------|--------------|
| `tiktok` | 1080 x 1920 | 9:16 |
| `youtube` | 1920 x 1080 | 16:9 |
| `square` | 1080 x 1080 | 1:1 |
| `instagram` | 1080 x 1350 | 4:5 |
| `twitter` | 1920 x 1080 | 16:9 |

Videos are scaled to fit within the target dimensions and padded with black bars to preserve aspect ratio (no stretching).

---

## speed

Change playback speed of both video and audio.

```
edit_video.py speed <input> --factor <float> [-o <output>]
```

- `--factor 2.0` = 2x faster (half duration)
- `--factor 0.5` = half speed (double duration)
- Audio pitch is preserved via the `atempo` filter. Factors outside 0.5-2.0 are handled by chaining multiple `atempo` stages.

---

## extract-audio

Extract the audio track from a video file.

```
edit_video.py extract-audio <input> [--format mp3|wav|aac|flac] [-o <output>]
```

Default format is `mp3`.

---

## replace-audio

Replace a video's audio track with a different audio file.

```
edit_video.py replace-audio <video> <audio> [-o <output>]
```

The video stream is copied without re-encoding. `--shortest` is used so the output matches the shorter of the two inputs.

---

## overlay

Add an image overlay (watermark, logo) on top of a video.

```
edit_video.py overlay <video> <image> [--position <pos>] [--opacity <0.0-1.0>] [-o <output>]
```

### Positions

| Name | Location |
|------|----------|
| `top-left` | 10px from top-left corner |
| `top-right` | 10px from top-right corner |
| `bottom-left` | 10px from bottom-left corner |
| `bottom-right` | 10px from bottom-right corner (default) |
| `center` | Centered in frame |

Opacity defaults to 1.0 (fully opaque).

---

## compress

Reduce video file size via bitrate targeting or CRF.

```
edit_video.py compress <input> (--target-size <size> | --crf <int>) [-o <output>]
```

- `--target-size` accepts values like `25MB`, `10mb`, `500KB`.
- `--crf` accepts an integer (lower = better quality, larger file). Default: 23. Typical range: 18-28.

When using `--target-size`, the tool calculates the required bitrate from the video duration and allocates 128 kbps for audio.

---

## convert

Convert a video to a different container or format.

```
edit_video.py convert <input> --format <fmt> [-o <output>]
```

Supported formats: `mp4`, `mov`, `avi`, `mkv`, `webm`, `gif`.

GIF conversion uses a two-pass palette approach for high quality output, scaled to 480px wide at 15 fps.

---

## info

Display detailed metadata about a video file.

```
edit_video.py info <input>
```

Returns JSON with: duration, resolution, video codec, audio codec, bitrate, frame rate, and file size.
