#!/usr/bin/env python3
"""Transcribe video and generate styled ASS subtitles.

Two modes:
  1. Transcribe-only:  video → Whisper → captions.json
  2. Style + ASS:      captions.json + style → captions.ass

Examples:
    # Transcribe to JSON
    python3 caption_video.py video.mp4 --transcribe-only

    # Generate ASS from JSON with a preset
    python3 caption_video.py video.mp4 --json captions.json --style pop

    # Override preset values via CLI
    python3 caption_video.py video.mp4 --json captions.json --style pop \
        --font-size 72 --primary-color "#FF0000"

    # List presets
    python3 caption_video.py --list-styles
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

PRESETS = {
    "classic": {
        "font_family": "Arial",
        "font_size": 48,
        "primary_color": "#FFFFFF",
        "secondary_color": "#FFA500",
        "outline_color": "#000000",
        "outline_width": 3,
        "shadow_depth": 0,
        "background_color": None,
        "position": "bottom",
        "animation": "karaoke-sweep",
        "words_per_line": 6,
        "single_words": False,
    },
    "pop": {
        "font_family": "Arial Black",
        "font_size": 60,
        "primary_color": "#FFFFFF",
        "secondary_color": "#00FFB2",
        "outline_color": "#000000",
        "outline_width": 3,
        "shadow_depth": 2,
        "background_color": None,
        "position": "center",
        "animation": "karaoke-sweep",
        "words_per_line": 4,
        "single_words": False,
    },
    "bold": {
        "font_family": "Arial Black",
        "font_size": 72,
        "primary_color": "#FFFFFF",
        "secondary_color": "#FFD700",
        "outline_color": "#000000",
        "outline_width": 4,
        "shadow_depth": 3,
        "background_color": None,
        "position": "center",
        "animation": "karaoke-sweep",
        "words_per_line": 3,
        "single_words": False,
    },
    "boxed": {
        "font_family": "Arial",
        "font_size": 52,
        "primary_color": "#FFFFFF",
        "secondary_color": "#00E5FF",
        "outline_color": "#000000",
        "outline_width": 0,
        "shadow_depth": 0,
        "background_color": "#000000",
        "position": "center",
        "animation": "karaoke-sweep",
        "words_per_line": 5,
        "single_words": False,
    },
    "single": {
        "font_family": "Arial Black",
        "font_size": 64,
        "primary_color": "#FFFFFF",
        "secondary_color": "#AA44FF",
        "outline_color": "#000000",
        "outline_width": 3,
        "shadow_depth": 2,
        "background_color": None,
        "position": "center",
        "animation": "karaoke-sweep",
        "words_per_line": 1,
        "single_words": True,
    },
}

ALIGNMENT_MAP = {"bottom": 2, "center": 5, "top": 8}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

_quiet = False


def log(msg):
    if not _quiet:
        print(f"[captions] {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def hex_to_ass_color(hex_color, alpha=0):
    """Convert '#RRGGBB' → '&HAABBGGRR' (ASS uses BGR order)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"


# ---------------------------------------------------------------------------
# Style resolution  (3-tier: CLI flags > JSON style > preset defaults)
# ---------------------------------------------------------------------------

def resolve_style(cli_args, json_style=None):
    """Merge preset defaults, JSON style section, and CLI flag overrides.

    Returns the final style dict.
    """
    preset_name = cli_args.style or (json_style or {}).get("preset", "classic")
    if preset_name not in PRESETS:
        raise ValueError(
            f"Unknown preset '{preset_name}'. Available: {', '.join(PRESETS)}"
        )
    style = dict(PRESETS[preset_name])
    style["preset"] = preset_name

    # Layer 2: JSON style overrides (from captions.json)
    if json_style:
        for k, v in json_style.items():
            if k != "preset" and v is not None:
                style[k] = v

    # Layer 3: CLI flag overrides
    flag_map = {
        "font_family": "font_family",
        "font_size": "font_size",
        "primary_color": "primary_color",
        "secondary_color": "secondary_color",
        "outline_color": "outline_color",
        "outline_width": "outline_width",
        "shadow_depth": "shadow_depth",
        "background_color": "background_color",
        "position": "position",
        "animation": "animation",
        "words_per_line": "words_per_line",
        "single_words": "single_words",
    }
    for attr, key in flag_map.items():
        val = getattr(cli_args, attr, None)
        if val is not None:
            style[key] = val

    # --single-words is a store_true flag; only override if explicitly set
    if getattr(cli_args, "single_words", False):
        style["single_words"] = True

    return style


# ---------------------------------------------------------------------------
# Smart chunking
# ---------------------------------------------------------------------------

_SENTENCE_ENDERS = {".", "!", "?"}
_CLAUSE_BREAKS = {",", ";", ":", "\u2014", "\u2013", "-"}
_PAUSE_THRESHOLD = 0.5


def smart_chunk_words(words, max_words=4):
    """Split words into display chunks on natural language breaks."""
    if max_words <= 1:
        return [[w] for w in words]

    chunks, cur = [], []
    for i, word in enumerate(words):
        cur.append(word)
        text = word.get("text", "").rstrip()
        is_sent = any(text.endswith(p) for p in _SENTENCE_ENDERS)
        is_clause = any(text.endswith(p) for p in _CLAUSE_BREAKS)
        has_pause = (
            i < len(words) - 1
            and (words[i + 1]["start"] - word["end"]) >= _PAUSE_THRESHOLD
        )
        at_max = len(cur) >= max_words
        if is_sent or has_pause or at_max or (is_clause and len(cur) >= 2):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


# ---------------------------------------------------------------------------
# FFmpeg / FFprobe helpers
# ---------------------------------------------------------------------------

def _run(cmd, check=True):
    log(f"  $ {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def get_video_info(video_path):
    """Return (resolution_dict, duration_float) via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", video_path,
    ]
    result = _run(cmd)
    data = json.loads(result.stdout)
    width, height, duration = 1920, 1080, 0.0
    for s in data.get("streams", []):
        if s.get("codec_type") == "video":
            width = int(s.get("width", width))
            height = int(s.get("height", height))
            break
    duration = float(data.get("format", {}).get("duration", 0.0))
    return {"width": width, "height": height}, duration


def extract_audio(video_path, output_wav):
    _run([
        "ffmpeg", "-y", "-i", video_path, "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_wav,
    ])
    return output_wav


# ---------------------------------------------------------------------------
# Transcription
# ---------------------------------------------------------------------------

def transcribe(video_path, model_name="base", resolution=None, duration=None):
    """Transcribe video → intermediate caption dict (segments + word timestamps)."""
    try:
        import whisper
    except ImportError:
        print("Error: openai-whisper not installed. Run: pip install openai-whisper",
              file=sys.stderr)
        sys.exit(1)

    if resolution is None or duration is None:
        res, dur = get_video_info(video_path)
        resolution = resolution or res
        duration = duration if duration is not None else dur

    tmp_dir = tempfile.mkdtemp(prefix="captions_")
    wav_path = os.path.join(tmp_dir, "audio.wav")

    log(f"Extracting audio from {os.path.basename(video_path)}...")
    extract_audio(video_path, wav_path)

    log(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)

    log("Transcribing with word timestamps...")
    result = model.transcribe(wav_path, word_timestamps=True)

    try:
        os.remove(wav_path)
        os.rmdir(tmp_dir)
    except OSError:
        pass

    segments = []
    for seg in result.get("segments", []):
        words = []
        for w in seg.get("words", []):
            words.append({
                "text": w["word"].strip(),
                "start": round(w["start"], 3),
                "end": round(w["end"], 3),
            })
        if words:
            segments.append({
                "start": round(seg["start"], 3),
                "end": round(seg["end"], 3),
                "text": " ".join(w["text"] for w in words),
                "words": words,
            })

    caption_data = {
        "video_path": os.path.abspath(video_path),
        "resolution": resolution,
        "duration": round(duration, 3),
        "style": {"preset": "classic"},
        "segments": segments,
    }

    log(f"Transcription complete: {len(segments)} segments, {duration:.1f}s")
    return caption_data


# ---------------------------------------------------------------------------
# ASS generation (no pysubs2 dependency — raw string output)
# ---------------------------------------------------------------------------

def _ass_timestamp(seconds):
    """Convert seconds (float) to ASS timestamp 'H:MM:SS.cc'."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _build_ass_header(style, resolution):
    """Return the [Script Info] and [V4+ Styles] sections as a string."""
    w = resolution.get("width", 1920)
    h = resolution.get("height", 1080)
    is_portrait = h > w
    margin_v = 80 if is_portrait else 40
    margin_h = 60 if is_portrait else 40

    align = ALIGNMENT_MAP.get(style["position"], 2)
    has_bg = style.get("background_color") is not None
    shadow = style.get("shadow_depth", 0)

    # In ASS karaoke mode: PrimaryColour is the highlight (sweep destination),
    # SecondaryColour is the base text (pre-highlight). We swap semantics so
    # that primary_color = base text and secondary_color = highlight matches
    # the user-facing mental model ("primary" = what you mostly see).
    anim = style.get("animation", "karaoke-sweep")
    if anim in ("karaoke", "karaoke-sweep"):
        # ASS: Primary = highlight target, Secondary = pre-highlight base
        pc = hex_to_ass_color(style["secondary_color"])
        sc = hex_to_ass_color(style["primary_color"])
    else:
        pc = hex_to_ass_color(style["primary_color"])
        sc = hex_to_ass_color(style["secondary_color"])

    oc = hex_to_ass_color(style["outline_color"])
    # Back color: used for shadow / box. Transparent black by default.
    bc = hex_to_ass_color("#000000", alpha=128)

    border_style = 1  # outline + shadow

    lines = [
        "[Script Info]",
        "Title: Generated by generate-captions skill",
        "ScriptType: v4.00+",
        f"PlayResX: {w}",
        f"PlayResY: {h}",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{style['font_family']},{style['font_size']},"
        f"{pc},{sc},{oc},{bc},"
        f"-1,0,0,0,100,100,0,0,{border_style},{style['outline_width']},{shadow},"
        f"{align},{margin_h},{margin_h},{margin_v},1",
    ]

    # Background box layer: a separate style with BorderStyle=3 (opaque box)
    if has_bg:
        bg_color = hex_to_ass_color(style["background_color"], alpha=80)
        lines.append(
            f"Style: DefaultBG,{style['font_family']},{style['font_size']},"
            f"{bg_color},{bg_color},{bg_color},{bg_color},"
            f"-1,0,0,0,100,100,0,0,3,0,0,"
            f"{align},{margin_h},{margin_h},{margin_v},1"
        )

    return "\n".join(lines)


def _build_ass_events(style, segments):
    """Return the [Events] section as a string."""
    anim = style.get("animation", "karaoke-sweep")
    wpl = 1 if style.get("single_words") else style.get("words_per_line", 4)
    has_bg = style.get("background_color") is not None

    lines = [
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for segment in segments:
        words = segment.get("words", [])
        if not words:
            ts = _ass_timestamp(segment["start"])
            te = _ass_timestamp(segment["end"])
            text = segment.get("text", "")
            if has_bg:
                lines.append(f"Dialogue: 0,{ts},{te},DefaultBG,,0,0,0,,{text}")
            lines.append(f"Dialogue: 1,{ts},{te},Default,,0,0,0,,{text}")
            continue

        chunks = smart_chunk_words(words, wpl)

        for chunk in chunks:
            ts = _ass_timestamp(chunk[0]["start"])
            te = _ass_timestamp(chunk[-1]["end"])

            # Build plain text (for BG layer) and tagged text (for main layer)
            plain_parts = []
            tagged_parts = []
            for i, word in enumerate(chunk):
                plain_parts.append(word["text"])
                if anim in ("karaoke", "karaoke-sweep"):
                    if i < len(chunk) - 1:
                        next_start = chunk[i + 1]["start"]
                    else:
                        next_start = word["end"]
                    dur_cs = max(1, int((next_start - word["start"]) * 100))
                    tag = "kf" if anim == "karaoke-sweep" else "k"
                    tagged_parts.append(f"{{\\{tag}{dur_cs}}}{word['text']}")
                else:
                    tagged_parts.append(word["text"])

                if i < len(chunk) - 1:
                    plain_parts.append(" ")
                    tagged_parts.append(" ")

            plain_text = "".join(plain_parts)
            tagged_text = "".join(tagged_parts)

            if has_bg:
                lines.append(
                    f"Dialogue: 0,{ts},{te},DefaultBG,,0,0,0,,{plain_text}"
                )
            lines.append(
                f"Dialogue: 1,{ts},{te},Default,,0,0,0,,{tagged_text}"
            )

    return "\n".join(lines)


def generate_ass(style, caption_data):
    """Generate a complete ASS subtitle string from style config and caption data."""
    resolution = caption_data.get("resolution", {"width": 1920, "height": 1080})
    segments = caption_data.get("segments", [])
    header = _build_ass_header(style, resolution)
    events = _build_ass_events(style, segments)
    return header + "\n" + events + "\n"


# ---------------------------------------------------------------------------
# List styles
# ---------------------------------------------------------------------------

def print_styles():
    print("Available style presets:\n")
    for name, p in PRESETS.items():
        bg = p["background_color"] or "none"
        print(f"  {name}")
        print(f"    Font:         {p['font_family']} {p['font_size']}pt")
        print(f"    Primary:      {p['primary_color']}  Secondary: {p['secondary_color']}")
        print(f"    Outline:      {p['outline_color']} ({p['outline_width']}px)  Shadow: {p['shadow_depth']}")
        print(f"    Background:   {bg}")
        print(f"    Position:     {p['position']}  Animation: {p['animation']}")
        print(f"    Words/line:   {p['words_per_line']}  Single: {p['single_words']}")
        print()


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="caption_video",
        description="Transcribe video and generate styled ASS subtitles.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s video.mp4 --transcribe-only              Whisper → captions.json
  %(prog)s video.mp4 --json captions.json --style pop   JSON → styled ASS
  %(prog)s video.mp4 --json c.json --font-size 72       Override preset font size
  %(prog)s --list-styles                                 Show all presets

presets: classic, pop, bold, boxed, single
whisper models: tiny, base, small, medium, large
""",
    )

    parser.add_argument("video", nargs="?", help="Input video file")
    parser.add_argument("--list-styles", action="store_true",
                        help="List all style presets and exit")

    # Mode flags
    mode = parser.add_argument_group("mode")
    mode.add_argument("--transcribe-only", action="store_true",
                      help="Only transcribe → captions.json (skip ASS)")
    mode.add_argument("--json", metavar="FILE",
                      help="Path to existing caption JSON (skip transcription)")

    # Whisper
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisper model size (default: base)")

    # Style
    style_g = parser.add_argument_group("style")
    style_g.add_argument("--style", "-s", default=None,
                         choices=list(PRESETS.keys()),
                         help="Style preset (default: classic)")
    style_g.add_argument("--font-family", default=None, dest="font_family",
                         help="Override font family")
    style_g.add_argument("--font-size", type=int, default=None, dest="font_size",
                         help="Override font size (pt)")
    style_g.add_argument("--primary-color", default=None, dest="primary_color",
                         help="Base text color (#RRGGBB)")
    style_g.add_argument("--secondary-color", default=None, dest="secondary_color",
                         help="Highlight/active word color (#RRGGBB)")
    style_g.add_argument("--outline-color", default=None, dest="outline_color",
                         help="Outline color (#RRGGBB)")
    style_g.add_argument("--outline-width", type=int, default=None, dest="outline_width",
                         help="Outline width (px)")
    style_g.add_argument("--shadow-depth", type=int, default=None, dest="shadow_depth",
                         help="Shadow depth (px, 0=none)")
    style_g.add_argument("--background-color", default=None, dest="background_color",
                         help="Background box color (#RRGGBB, enables boxed mode)")
    style_g.add_argument("--position", default=None,
                         choices=["bottom", "center", "top"],
                         help="Caption position")
    style_g.add_argument("--animation", default=None,
                         choices=["none", "karaoke", "karaoke-sweep"],
                         help="Animation type")
    style_g.add_argument("--words-per-line", type=int, default=None, dest="words_per_line",
                         help="Max words per display chunk")
    style_g.add_argument("--single-words", action="store_true", default=None,
                         dest="single_words",
                         help="Show one word at a time")

    # Output
    parser.add_argument("--output-dir", metavar="DIR",
                        help="Output directory (default: same as video)")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="Write result JSON to file instead of stdout")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress progress messages")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    global _quiet

    parser = build_parser()
    args = parser.parse_args()
    _quiet = args.quiet

    if args.list_styles:
        print_styles()
        sys.exit(0)

    if not args.video:
        parser.error("the following argument is required: video")

    video_abs = os.path.abspath(args.video)
    video_stem = os.path.splitext(os.path.basename(video_abs))[0]
    output_dir = args.output_dir or os.path.dirname(video_abs)
    os.makedirs(output_dir, exist_ok=True)

    transcript_path = os.path.join(output_dir, f"{video_stem}_captions.json")
    ass_path = os.path.join(output_dir, f"{video_stem}_captions.ass")

    result = {
        "video": os.path.basename(video_abs),
        "transcript_file": None,
        "ass_file": None,
        "segments_count": 0,
        "duration": 0.0,
    }

    # ---- Load or transcribe ----
    if args.json:
        log(f"Loading caption JSON: {args.json}")
        with open(args.json, "r", encoding="utf-8") as f:
            caption_data = json.load(f)
        transcript_path = os.path.abspath(args.json)
    else:
        if not os.path.isfile(video_abs):
            parser.error(f"video file not found: {video_abs}")

        log("Getting video info...")
        resolution, duration = get_video_info(video_abs)
        caption_data = transcribe(video_abs, model_name=args.model,
                                  resolution=resolution, duration=duration)

        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(caption_data, f, indent=2, ensure_ascii=False)
        log(f"Transcript saved: {transcript_path}")

    result["transcript_file"] = os.path.abspath(transcript_path)
    result["segments_count"] = len(caption_data.get("segments", []))
    result["duration"] = caption_data.get("duration", 0.0)

    if args.transcribe_only:
        result_json = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result_json + "\n")
            log(f"Result written to: {args.output}")
        else:
            print(result_json)
        return

    # ---- Resolve style and generate ASS ----
    json_style = caption_data.get("style", {})
    style = resolve_style(args, json_style)

    log(f"Style: {style['preset']} (font={style['font_family']} {style['font_size']}pt, "
        f"pos={style['position']}, anim={style['animation']})")

    ass_content = generate_ass(style, caption_data)

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    log(f"ASS file saved: {ass_path}")

    result["ass_file"] = os.path.abspath(ass_path)
    result["style"] = style

    # ---- Output result ----
    result_json = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result_json + "\n")
        log(f"Result written to: {args.output}")
    else:
        print(result_json)

    # Print burn-in hint
    log("")
    log("To burn captions into video:")
    log(f'  ffmpeg -y -i "{video_abs}" -vf "ass={ass_path}" -c:a copy "{os.path.join(output_dir, video_stem + "_captioned.mp4")}"')


if __name__ == "__main__":
    main()
