#!/usr/bin/env python3
"""Local video editing CLI powered by ffmpeg.

Provides subcommands for common video operations: trim, concat, resize,
speed, extract-audio, replace-audio, overlay, compress, convert, and info.

Every operation outputs a JSON result to stdout containing the operation name,
input/output metadata, and the exact ffmpeg command that was executed.
"""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Platform presets for resize
# ---------------------------------------------------------------------------

PLATFORM_PRESETS = {
    "tiktok":    {"width": 1080, "height": 1920},   # 9:16
    "youtube":   {"width": 1920, "height": 1080},   # 16:9
    "square":    {"width": 1080, "height": 1080},   # 1:1
    "instagram": {"width": 1080, "height": 1350},   # 4:5
    "twitter":   {"width": 1920, "height": 1080},   # 16:9
}

# ---------------------------------------------------------------------------
# Overlay position map
# ---------------------------------------------------------------------------

POSITIONS = {
    "top-left":     "10:10",
    "top-right":    "W-w-10:10",
    "bottom-left":  "10:H-h-10",
    "bottom-right": "W-w-10:H-h-10",
    "center":       "(W-w)/2:(H-h)/2",
}

# ---------------------------------------------------------------------------
# Audio codec map
# ---------------------------------------------------------------------------

AUDIO_CODECS = {
    "mp3":  "libmp3lame",
    "wav":  "pcm_s16le",
    "aac":  "aac",
    "flac": "flac",
}


# ===================================================================
# Utility helpers
# ===================================================================

def die(message: str) -> None:
    """Print an error as JSON to stdout and exit with code 1."""
    print(json.dumps({"error": message}, indent=2))
    sys.exit(1)


def require_ffmpeg() -> None:
    """Exit immediately if ffmpeg or ffprobe is missing."""
    for binary in ("ffmpeg", "ffprobe"):
        if shutil.which(binary) is None:
            die(f"{binary} is not installed. Install with: brew install ffmpeg")


def validate_input(path: str) -> str:
    """Return the absolute path after confirming the file exists."""
    abspath = os.path.abspath(path)
    if not os.path.isfile(abspath):
        die(f"Input file not found: {abspath}")
    return abspath


def parse_timestamp(ts: str) -> str:
    """Normalise a timestamp to HH:MM:SS.mmm format.

    Accepts:
        "01:30:00"   -> "01:30:00"
        "1:30"       -> "00:01:30"
        "90"         -> "00:01:30"
        "90.5"       -> "00:01:30.500"
    """
    if ts is None:
        return None

    ts = ts.strip()

    # Already in HH:MM:SS(.mmm) form
    if re.match(r"^\d{1,2}:\d{2}:\d{2}(\.\d+)?$", ts):
        return ts

    # MM:SS form
    if re.match(r"^\d{1,2}:\d{2}(\.\d+)?$", ts):
        return f"00:{ts}"

    # Raw seconds
    try:
        total = float(ts)
    except ValueError:
        die(f"Invalid timestamp format: {ts}")

    hours = int(total // 3600)
    remainder = total - hours * 3600
    minutes = int(remainder // 60)
    seconds = remainder - minutes * 60
    whole_sec = int(seconds)
    millis = int(round((seconds - whole_sec) * 1000))

    if millis:
        return f"{hours:02d}:{minutes:02d}:{whole_sec:02d}.{millis:03d}"
    return f"{hours:02d}:{minutes:02d}:{whole_sec:02d}"


def parse_size(size_str: str) -> float:
    """Parse a human-readable file size string into megabytes.

    Accepts: "25MB", "10mb", "500KB", "500kb", "1GB", etc.
    """
    size_str = size_str.strip().upper()
    match = re.match(r"^([\d.]+)\s*(GB|MB|KB|B)?$", size_str)
    if not match:
        die(f"Invalid size format: {size_str}. Use e.g. 25MB, 500KB, 1GB.")

    value = float(match.group(1))
    unit = match.group(2) or "MB"

    multipliers = {"B": 1 / (1024 * 1024), "KB": 1 / 1024, "MB": 1, "GB": 1024}
    return value * multipliers[unit]


def get_duration(path: str) -> float:
    """Return the duration of a media file in seconds via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception as exc:
        die(f"Could not determine duration of {path}: {exc}")


def get_video_info(path: str) -> dict:
    """Return rich metadata about a video file."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        path,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return json.loads(result.stdout)
    except Exception as exc:
        die(f"Could not read video info for {path}: {exc}")


def file_size_mb(path: str) -> float:
    """Return the file size in megabytes, rounded to 2 decimals."""
    try:
        return round(os.path.getsize(path) / (1024 * 1024), 2)
    except OSError:
        return 0.0


def generate_output_path(input_path: str, suffix: str, ext: str = None) -> str:
    """Create an output filename like ``video_trimmed.mp4``.

    If *ext* is None the input extension is reused.
    """
    base, orig_ext = os.path.splitext(input_path)
    ext = ext or orig_ext
    if not ext.startswith("."):
        ext = f".{ext}"
    return f"{base}_{suffix}{ext}"


def run_ffmpeg(cmd: list[str], quiet: bool = False) -> subprocess.CompletedProcess:
    """Execute an ffmpeg/ffprobe command list and return the CompletedProcess.

    On failure, prints the stderr output and exits.
    """
    if not quiet:
        # Add -y (overwrite) if not already present and this is an ffmpeg call
        if cmd[0] == "ffmpeg" and "-y" not in cmd:
            cmd.insert(1, "-y")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        die("ffmpeg timed out after 10 minutes.")

    if result.returncode != 0:
        stderr = result.stderr.strip().split("\n")
        # Show the last few lines which usually contain the real error
        relevant = "\n".join(stderr[-10:]) if len(stderr) > 10 else "\n".join(stderr)
        die(f"ffmpeg failed (exit {result.returncode}):\n{relevant}")

    return result


def validate_output(path: str) -> None:
    """Confirm that the output file was created and is non-empty."""
    if not os.path.isfile(path):
        die(f"Output file was not created: {path}")
    if os.path.getsize(path) == 0:
        os.remove(path)
        die(f"Output file is empty (0 bytes): {path}")


def make_result(operation: str, input_path: str, output_path: str,
                cmd_str: str, extra: dict = None) -> dict:
    """Build the standard JSON result dict."""
    result = {
        "operation": operation,
        "input": {
            "path": input_path,
            "size_mb": file_size_mb(input_path),
        },
        "output": {
            "path": output_path,
            "size_mb": file_size_mb(output_path),
        },
        "command": cmd_str,
    }
    # Add duration when possible
    try:
        result["input"]["duration"] = round(get_duration(input_path), 2)
    except SystemExit:
        pass
    try:
        result["output"]["duration"] = round(get_duration(output_path), 2)
    except SystemExit:
        pass

    if extra:
        result.update(extra)
    return result


def build_atempo_chain(factor: float) -> str:
    """Build an atempo filter chain for arbitrary speed factors.

    ffmpeg's atempo filter only supports values in [0.5, 2.0].  For factors
    outside that range we chain multiple atempo stages.
    """
    if factor <= 0:
        die("Speed factor must be a positive number.")

    filters = []
    remaining = factor
    while remaining > 2.0:
        filters.append("atempo=2.0")
        remaining /= 2.0
    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5
    filters.append(f"atempo={remaining:.6f}")
    return ",".join(filters)


# ===================================================================
# Operation implementations
# ===================================================================

def trim_video(args) -> None:
    input_path = validate_input(args.input)
    output = args.output or generate_output_path(input_path, "trimmed")

    if args.start is None:
        die("--start is required for trim.")

    start = parse_timestamp(args.start)

    cmd = ["ffmpeg", "-ss", start]

    if args.end:
        cmd += ["-to", parse_timestamp(args.end)]
    elif args.duration:
        cmd += ["-t", str(args.duration)]
    else:
        die("Either --end or --duration is required for trim.")

    cmd += ["-i", input_path, "-c", "copy", output]

    cmd_str = " ".join(cmd)
    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("trim", input_path, output, cmd_str), indent=2))


def concat_videos(args) -> None:
    inputs = [validate_input(p) for p in args.inputs]
    if len(inputs) < 2:
        die("concat requires at least 2 input files.")

    output = args.output or generate_output_path(inputs[0], "concat")

    # Build a temporary concat list file
    fd, list_file = tempfile.mkstemp(suffix=".txt", prefix="ffconcat_")
    try:
        with os.fdopen(fd, "w") as f:
            for clip in inputs:
                f.write(f"file '{clip}'\n")

        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", list_file, "-c", "copy", output,
        ]
        cmd_str = " ".join(cmd)
        run_ffmpeg(cmd)
    finally:
        os.unlink(list_file)

    validate_output(output)
    print(json.dumps(make_result("concat", inputs[0], output, cmd_str), indent=2))


def resize_video(args) -> None:
    input_path = validate_input(args.input)

    if args.target:
        key = args.target.lower()
        if key not in PLATFORM_PRESETS:
            die(f"Unknown platform preset: {key}. Choose from: {', '.join(PLATFORM_PRESETS)}")
        preset = PLATFORM_PRESETS[key]
        w, h = preset["width"], preset["height"]
        suffix = f"resize_{key}"
    elif args.width and args.height:
        w, h = args.width, args.height
        suffix = f"resize_{w}x{h}"
    else:
        die("Provide --target <preset> or both --width and --height.")

    output = args.output or generate_output_path(input_path, suffix)

    vf = (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
    )
    cmd = ["ffmpeg", "-i", input_path, "-vf", vf, "-c:a", "copy", output]
    cmd_str = " ".join(cmd)

    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("resize", input_path, output, cmd_str), indent=2))


def change_speed(args) -> None:
    input_path = validate_input(args.input)
    factor = args.factor
    if factor <= 0:
        die("Speed factor must be a positive number.")

    suffix = f"speed_{factor}x"
    output = args.output or generate_output_path(input_path, suffix)

    video_pts = round(1.0 / factor, 6)
    audio_chain = build_atempo_chain(factor)

    cmd = [
        "ffmpeg", "-i", input_path,
        "-filter:v", f"setpts={video_pts}*PTS",
        "-filter:a", audio_chain,
        output,
    ]
    cmd_str = " ".join(cmd)

    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("speed", input_path, output, cmd_str), indent=2))


def extract_audio(args) -> None:
    input_path = validate_input(args.input)
    fmt = (args.format or "mp3").lower()

    if fmt not in AUDIO_CODECS:
        die(f"Unsupported audio format: {fmt}. Choose from: {', '.join(AUDIO_CODECS)}")

    codec = AUDIO_CODECS[fmt]
    output = args.output or generate_output_path(input_path, "audio", ext=fmt)

    cmd = ["ffmpeg", "-i", input_path, "-vn", "-acodec", codec, output]
    cmd_str = " ".join(cmd)

    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("extract-audio", input_path, output, cmd_str), indent=2))


def replace_audio(args) -> None:
    video_path = validate_input(args.video)
    audio_path = validate_input(args.audio)

    output = args.output or generate_output_path(video_path, "newaudio")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        output,
    ]
    cmd_str = " ".join(cmd)

    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("replace-audio", video_path, output, cmd_str), indent=2))


def add_overlay(args) -> None:
    video_path = validate_input(args.video)
    image_path = validate_input(args.image)

    position = (args.position or "bottom-right").lower()
    pos_expr = POSITIONS.get(position)
    if pos_expr is None:
        die(
            f"Unknown position: {position}. "
            f"Choose from: {', '.join(POSITIONS)} or use a custom 'x:y' expression."
        )

    opacity = args.opacity if args.opacity is not None else 1.0
    suffix = f"overlay_{position.replace('-', '')}"
    output = args.output or generate_output_path(video_path, suffix)

    if opacity < 1.0:
        fc = (
            f"[1:v]format=rgba,colorchannelmixer=aa={opacity}[ovr];"
            f"[0:v][ovr]overlay={pos_expr}"
        )
    else:
        fc = f"overlay={pos_expr}"

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", image_path,
        "-filter_complex", fc,
        "-c:a", "copy",
        output,
    ]
    cmd_str = " ".join(cmd)

    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("overlay", video_path, output, cmd_str), indent=2))


def compress_video(args) -> None:
    input_path = validate_input(args.input)

    if args.target_size:
        size_mb = parse_size(args.target_size)
        duration = get_duration(input_path)
        if duration <= 0:
            die("Cannot determine video duration for bitrate calculation.")

        # target_bitrate in kbps: (size_MB * 8 * 1024) / duration - 128 audio
        audio_kbps = 128
        total_kbps = (size_mb * 8 * 1024) / duration
        video_kbps = max(int(total_kbps - audio_kbps), 100)

        suffix = f"compress_{args.target_size.replace(' ', '')}"
        output = args.output or generate_output_path(input_path, suffix)

        cmd = [
            "ffmpeg", "-i", input_path,
            "-b:v", f"{video_kbps}k",
            "-maxrate", f"{video_kbps}k",
            "-bufsize", f"{video_kbps * 2}k",
            "-c:a", "aac", "-b:a", f"{audio_kbps}k",
            output,
        ]
    elif args.crf is not None:
        crf = args.crf
        suffix = f"compress_crf{crf}"
        output = args.output or generate_output_path(input_path, suffix)

        cmd = [
            "ffmpeg", "-i", input_path,
            "-crf", str(crf),
            "-preset", "medium",
            "-c:a", "copy",
            output,
        ]
    else:
        # Default CRF 23
        crf = 23
        suffix = f"compress_crf{crf}"
        output = args.output or generate_output_path(input_path, suffix)

        cmd = [
            "ffmpeg", "-i", input_path,
            "-crf", str(crf),
            "-preset", "medium",
            "-c:a", "copy",
            output,
        ]

    cmd_str = " ".join(cmd)
    run_ffmpeg(cmd)
    validate_output(output)

    print(json.dumps(make_result("compress", input_path, output, cmd_str), indent=2))


def convert_video(args) -> None:
    input_path = validate_input(args.input)
    fmt = args.format.lower().lstrip(".")
    output = args.output or generate_output_path(input_path, "converted", ext=fmt)

    if fmt == "gif":
        # Two-pass palette approach for high-quality GIFs
        palette = os.path.join(tempfile.gettempdir(), "palette.png")

        cmd1 = [
            "ffmpeg", "-i", input_path,
            "-vf", "fps=15,scale=480:-1:flags=lanczos,palettegen",
            "-y", palette,
        ]
        cmd2 = [
            "ffmpeg", "-i", input_path, "-i", palette,
            "-filter_complex",
            "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse",
            output,
        ]

        cmd_str = " && ".join([" ".join(cmd1), " ".join(cmd2)])
        run_ffmpeg(cmd1)
        run_ffmpeg(cmd2)

        # Clean up palette
        try:
            os.remove(palette)
        except OSError:
            pass
    else:
        cmd = ["ffmpeg", "-i", input_path, output]
        cmd_str = " ".join(cmd)
        run_ffmpeg(cmd)

    validate_output(output)
    print(json.dumps(make_result("convert", input_path, output, cmd_str), indent=2))


def show_info(args) -> None:
    input_path = validate_input(args.input)
    data = get_video_info(input_path)

    fmt = data.get("format", {})
    streams = data.get("streams", [])

    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), None)

    info = {
        "operation": "info",
        "path": input_path,
        "size_mb": file_size_mb(input_path),
        "duration": round(float(fmt.get("duration", 0)), 2),
        "bitrate_kbps": round(int(fmt.get("bit_rate", 0)) / 1000),
        "format_name": fmt.get("format_name"),
    }

    if video_stream:
        info["video"] = {
            "codec": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "fps": video_stream.get("r_frame_rate"),
            "pixel_format": video_stream.get("pix_fmt"),
        }

    if audio_stream:
        info["audio"] = {
            "codec": audio_stream.get("codec_name"),
            "sample_rate": audio_stream.get("sample_rate"),
            "channels": audio_stream.get("channels"),
            "bitrate_kbps": round(int(audio_stream.get("bit_rate", 0)) / 1000)
            if audio_stream.get("bit_rate")
            else None,
        }

    print(json.dumps(info, indent=2))


# ===================================================================
# CLI argument parsing
# ===================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="edit_video.py",
        description="Local video editing CLI powered by ffmpeg.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s trim video.mp4 --start 00:30 --end 01:45
  %(prog)s concat clip1.mp4 clip2.mp4 -o merged.mp4
  %(prog)s resize video.mp4 --target tiktok
  %(prog)s speed video.mp4 --factor 2.0
  %(prog)s extract-audio video.mp4 --format wav
  %(prog)s replace-audio video.mp4 narration.mp3
  %(prog)s overlay video.mp4 logo.png --position top-right --opacity 0.8
  %(prog)s compress video.mp4 --target-size 25MB
  %(prog)s convert video.mov --format mp4
  %(prog)s info video.mp4
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="Operation to perform")

    # -- trim --
    p_trim = subparsers.add_parser(
        "trim",
        help="Cut a segment from a video",
        description="Trim a video by specifying start time and either end time or duration.",
        epilog="""\
examples:
  %(prog)s video.mp4 --start 00:30 --end 01:45
  %(prog)s video.mp4 --start 30 --duration 75
  %(prog)s video.mp4 --start 1:30 --end 2:00 -o clip.mp4
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_trim.add_argument("input", help="Input video file")
    p_trim.add_argument("--start", "-s", required=True,
                        help="Start timestamp (HH:MM:SS, MM:SS, or seconds)")
    p_trim.add_argument("--end", "-e",
                        help="End timestamp (HH:MM:SS, MM:SS, or seconds)")
    p_trim.add_argument("--duration", "-d", type=float,
                        help="Duration in seconds (alternative to --end)")
    p_trim.add_argument("-o", "--output", help="Output file path")
    p_trim.set_defaults(func=trim_video)

    # -- concat --
    p_concat = subparsers.add_parser(
        "concat",
        help="Join multiple video clips into one",
        description="Concatenate two or more video files. All clips should share the same codec and resolution.",
        epilog="""\
examples:
  %(prog)s clip1.mp4 clip2.mp4 clip3.mp4
  %(prog)s clip1.mp4 clip2.mp4 -o merged.mp4
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_concat.add_argument("inputs", nargs="+", help="Input video files (at least 2)")
    p_concat.add_argument("-o", "--output", help="Output file path")
    p_concat.set_defaults(func=concat_videos)

    # -- resize --
    p_resize = subparsers.add_parser(
        "resize",
        help="Resize video for a platform or custom dimensions",
        description=(
            "Resize a video to platform presets (tiktok, youtube, square, instagram, twitter) "
            "or custom width/height. Aspect ratio is preserved with black padding."
        ),
        epilog="""\
examples:
  %(prog)s video.mp4 --target tiktok
  %(prog)s video.mp4 --target youtube
  %(prog)s video.mp4 --width 1280 --height 720
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_resize.add_argument("input", help="Input video file")
    p_resize.add_argument("--target", "-t",
                          choices=list(PLATFORM_PRESETS.keys()),
                          help="Platform preset")
    p_resize.add_argument("--width", "-W", type=int, help="Target width in pixels")
    p_resize.add_argument("--height", "-H", type=int, help="Target height in pixels")
    p_resize.add_argument("-o", "--output", help="Output file path")
    p_resize.set_defaults(func=resize_video)

    # -- speed --
    p_speed = subparsers.add_parser(
        "speed",
        help="Change playback speed",
        description="Speed up or slow down a video. Audio pitch is preserved.",
        epilog="""\
examples:
  %(prog)s video.mp4 --factor 2.0    # 2x faster
  %(prog)s video.mp4 --factor 0.5    # half speed
  %(prog)s video.mp4 --factor 4.0    # 4x faster
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_speed.add_argument("input", help="Input video file")
    p_speed.add_argument("--factor", "-f", type=float, required=True,
                         help="Speed factor (2.0 = 2x faster, 0.5 = half speed)")
    p_speed.add_argument("-o", "--output", help="Output file path")
    p_speed.set_defaults(func=change_speed)

    # -- extract-audio --
    p_extract = subparsers.add_parser(
        "extract-audio",
        help="Extract audio track from video",
        description="Extract the audio track from a video file into a standalone audio file.",
        epilog="""\
examples:
  %(prog)s video.mp4                    # outputs video_audio.mp3
  %(prog)s video.mp4 --format wav       # outputs video_audio.wav
  %(prog)s video.mp4 --format flac -o audio.flac
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_extract.add_argument("input", help="Input video file")
    p_extract.add_argument("--format", "-f",
                           choices=list(AUDIO_CODECS.keys()),
                           default="mp3",
                           help="Output audio format (default: mp3)")
    p_extract.add_argument("-o", "--output", help="Output file path")
    p_extract.set_defaults(func=extract_audio)

    # -- replace-audio --
    p_replace = subparsers.add_parser(
        "replace-audio",
        help="Replace a video's audio track",
        description="Replace the audio track of a video with a different audio file.",
        epilog="""\
examples:
  %(prog)s video.mp4 narration.mp3
  %(prog)s video.mp4 music.aac -o final.mp4
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_replace.add_argument("video", help="Input video file")
    p_replace.add_argument("audio", help="Replacement audio file")
    p_replace.add_argument("-o", "--output", help="Output file path")
    p_replace.set_defaults(func=replace_audio)

    # -- overlay --
    p_overlay = subparsers.add_parser(
        "overlay",
        help="Add an image overlay (watermark, logo)",
        description="Overlay an image on top of a video at a specified position with optional opacity.",
        epilog="""\
examples:
  %(prog)s video.mp4 logo.png --position top-right --opacity 0.8
  %(prog)s video.mp4 watermark.png --position bottom-left
  %(prog)s video.mp4 badge.png --position center --opacity 0.5
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_overlay.add_argument("video", help="Input video file")
    p_overlay.add_argument("image", help="Overlay image file (PNG recommended)")
    p_overlay.add_argument("--position", "-p",
                           choices=list(POSITIONS.keys()),
                           default="bottom-right",
                           help="Overlay position (default: bottom-right)")
    p_overlay.add_argument("--opacity", type=float, default=1.0,
                           help="Opacity from 0.0 (invisible) to 1.0 (opaque, default)")
    p_overlay.add_argument("-o", "--output", help="Output file path")
    p_overlay.set_defaults(func=add_overlay)

    # -- compress --
    p_compress = subparsers.add_parser(
        "compress",
        help="Compress video to reduce file size",
        description=(
            "Compress a video by targeting a specific file size or CRF value. "
            "If neither is provided, CRF 23 is used."
        ),
        epilog="""\
examples:
  %(prog)s video.mp4 --target-size 25MB
  %(prog)s video.mp4 --crf 28
  %(prog)s video.mp4 --target-size 10mb -o small.mp4
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_compress.add_argument("input", help="Input video file")
    p_compress.add_argument("--target-size",
                            help="Target file size (e.g. 25MB, 500KB)")
    p_compress.add_argument("--crf", type=int,
                            help="Constant Rate Factor (lower = better quality). Typical: 18-28")
    p_compress.add_argument("-o", "--output", help="Output file path")
    p_compress.set_defaults(func=compress_video)

    # -- convert --
    p_convert = subparsers.add_parser(
        "convert",
        help="Convert video to another format",
        description="Convert a video to a different container format. GIF uses a two-pass palette approach.",
        epilog="""\
examples:
  %(prog)s video.mov --format mp4
  %(prog)s video.mp4 --format gif
  %(prog)s video.avi --format mkv -o output.mkv
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_convert.add_argument("input", help="Input video file")
    p_convert.add_argument("--format", "-f", required=True,
                           help="Target format (mp4, mov, avi, mkv, webm, gif)")
    p_convert.add_argument("-o", "--output", help="Output file path")
    p_convert.set_defaults(func=convert_video)

    # -- info --
    p_info = subparsers.add_parser(
        "info",
        help="Display video metadata",
        description="Show detailed information about a video file: duration, resolution, codecs, bitrate, etc.",
        epilog="""\
examples:
  %(prog)s video.mp4
  %(prog)s clip.mov
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_info.add_argument("input", help="Input video file")
    p_info.set_defaults(func=show_info)

    return parser


def main() -> None:
    require_ffmpeg()

    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
