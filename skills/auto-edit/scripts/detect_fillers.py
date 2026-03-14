#!/usr/bin/env python3
"""Detect filler words in video/audio using Whisper word-level timestamps.

Outputs JSON with filler word locations and ready-to-use auto-editor --cut-out
flags. Feed the output directly into auto-editor or use the time ranges with
ffmpeg for manual editing.

Usage:
  python3 detect_fillers.py video.mp4
  python3 detect_fillers.py video.mp4 --filler-words "um,uh,like"
  python3 detect_fillers.py video.mp4 --whisper-model small
  python3 detect_fillers.py video.mp4 -q   # JSON only
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_FILLER_WORDS = {
    "um", "uh", "uhh", "umm", "hmm", "hm",
    "like", "you know", "basically", "actually",
    "literally", "right", "so", "i mean",
}


def die(message: str) -> None:
    print(json.dumps({"error": message}, indent=2))
    sys.exit(1)


def log(msg: str, quiet: bool = False) -> None:
    if not quiet:
        print(msg, file=sys.stderr)


def get_duration(path: str) -> float:
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


def transcribe(input_path: str, model: str = "base", quiet: bool = False) -> list[dict]:
    """Transcribe audio and return word-level timestamps."""
    log(f"Transcribing with Whisper (model={model})...", quiet)

    fd, wav_path = tempfile.mkstemp(suffix=".wav", prefix="whisper_")
    os.close(fd)

    try:
        # Extract audio
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-vn", "-acodec", "pcm_s16le",
            "-ar", "16000", "-ac", "1",
            wav_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            die(f"ffmpeg audio extraction failed: {result.stderr.strip()[-200:]}")

        # Try whisper Python module (faster)
        try:
            import whisper
            model_obj = whisper.load_model(model)
            result = model_obj.transcribe(wav_path, word_timestamps=True)

            words = []
            for segment in result.get("segments", []):
                for w in segment.get("words", []):
                    words.append({
                        "word": w["word"].strip(),
                        "start": round(w["start"], 3),
                        "end": round(w["end"], 3),
                    })
            log(f"Transcribed {len(words)} words.", quiet)
            return words
        except ImportError:
            pass

        # Fall back to whisper CLI
        if shutil.which("whisper") is None:
            die(
                "Whisper is not installed.\n"
                "Install with: pip install openai-whisper"
            )

        json_dir = tempfile.mkdtemp(prefix="whisper_out_")
        try:
            cmd = [
                "whisper", wav_path,
                "--model", model,
                "--output_format", "json",
                "--word_timestamps", "True",
                "--output_dir", json_dir,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if result.returncode != 0:
                die(f"Whisper failed: {result.stderr.strip()[-200:]}")

            json_files = list(Path(json_dir).glob("*.json"))
            if not json_files:
                die("Whisper produced no JSON output.")

            with open(json_files[0]) as f:
                data = json.load(f)

            words = []
            for segment in data.get("segments", []):
                for w in segment.get("words", []):
                    words.append({
                        "word": w["word"].strip(),
                        "start": round(w["start"], 3),
                        "end": round(w["end"], 3),
                    })
            log(f"Transcribed {len(words)} words.", quiet)
            return words
        finally:
            shutil.rmtree(json_dir, ignore_errors=True)
    finally:
        try:
            os.unlink(wav_path)
        except OSError:
            pass


def find_fillers(
    words: list[dict],
    filler_words: set[str],
    padding: float = 0.05,
) -> list[dict]:
    """Match words against filler word list. Returns time-stamped matches."""
    fillers = []

    # Single-word fillers
    for w in words:
        cleaned = w["word"].lower().strip(".,!?;:'\"")
        if cleaned in filler_words:
            fillers.append({
                "word": cleaned,
                "start": round(max(0, w["start"] - padding), 3),
                "end": round(w["end"] + padding, 3),
            })

    # Multi-word fillers (e.g., "you know", "i mean")
    multi_word = {f for f in filler_words if " " in f}
    for i in range(len(words) - 1):
        for mwf in multi_word:
            parts = mwf.split()
            if i + len(parts) > len(words):
                continue
            candidate = " ".join(
                words[i + j]["word"].lower().strip(".,!?;:'\"")
                for j in range(len(parts))
            )
            if candidate == mwf:
                fillers.append({
                    "word": mwf,
                    "start": round(max(0, words[i]["start"] - padding), 3),
                    "end": round(words[i + len(parts) - 1]["end"] + padding, 3),
                })

    return fillers


def main():
    parser = argparse.ArgumentParser(
        prog="detect_fillers.py",
        description="Detect filler words in video/audio using Whisper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s video.mp4
  %(prog)s video.mp4 --filler-words "um,uh,like"
  %(prog)s video.mp4 --whisper-model small
  %(prog)s video.mp4 -q  # JSON only, no progress
""",
    )
    parser.add_argument("input", help="Input video or audio file")
    parser.add_argument(
        "--whisper-model", default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--filler-words",
        help="Comma-separated filler words (default: um,uh,like,you know,...)",
    )
    parser.add_argument(
        "--padding", type=float, default=0.05,
        help="Seconds of padding around each filler cut (default: 0.05)",
    )
    parser.add_argument(
        "-o", "--output", help="Write result JSON to file instead of stdout",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Suppress progress messages, output only JSON",
    )

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.isfile(input_path):
        die(f"Input file not found: {input_path}")

    # Check deps
    if shutil.which("ffmpeg") is None:
        die("ffmpeg is not installed. Install with: brew install ffmpeg")

    # Transcribe
    words = transcribe(input_path, model=args.whisper_model, quiet=args.quiet)

    # Find fillers
    filler_words = DEFAULT_FILLER_WORDS.copy()
    if args.filler_words:
        filler_words = {w.strip().lower() for w in args.filler_words.split(",")}

    fillers = find_fillers(words, filler_words, padding=args.padding)
    log(f"Found {len(fillers)} filler word instances.", args.quiet)

    # Build auto-editor --cut-out flags
    cut_out_flags = []
    for f in fillers:
        cut_out_flags.append(f"--cut-out {f['start']}s,{f['end']}s")

    # Build result
    duration = get_duration(input_path)
    filler_duration = sum(f["end"] - f["start"] for f in fillers)

    result = {
        "input": input_path,
        "duration": round(duration, 2),
        "word_count": len(words),
        "fillers": fillers,
        "filler_count": len(fillers),
        "filler_duration": round(filler_duration, 2),
        "auto_editor_flags": " ".join(cut_out_flags),
        "auto_editor_command": (
            f"auto-editor {input_path} {' '.join(cut_out_flags)} -o output.mp4 --no-open"
            if cut_out_flags else None
        ),
    }

    output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        log(f"Written to {args.output}", args.quiet)
    else:
        print(output)


if __name__ == "__main__":
    main()
