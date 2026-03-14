#!/usr/bin/env python3
"""Dependency verification for the video-edit skill.

Checks that ffmpeg and ffprobe are installed and accessible on the system PATH.
No pip dependencies are required.
"""

import shutil
import subprocess
import sys
import json


def check_binary(name: str) -> dict:
    """Check whether a binary is available and return its version info."""
    path = shutil.which(name)
    if path is None:
        return {"name": name, "installed": False, "path": None, "version": None}

    try:
        result = subprocess.run(
            [name, "-version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        first_line = result.stdout.strip().split("\n")[0] if result.stdout else ""
        return {
            "name": name,
            "installed": True,
            "path": path,
            "version": first_line,
        }
    except Exception as exc:
        return {
            "name": name,
            "installed": True,
            "path": path,
            "version": f"error retrieving version: {exc}",
        }


def main() -> int:
    """Run all dependency checks and report results."""
    dependencies = ["ffmpeg", "ffprobe"]
    results = [check_binary(dep) for dep in dependencies]
    all_ok = all(r["installed"] for r in results)

    print(json.dumps({"ok": all_ok, "dependencies": results}, indent=2))

    if not all_ok:
        missing = [r["name"] for r in results if not r["installed"]]
        print(
            f"\nMissing: {', '.join(missing)}",
            file=sys.stderr,
        )
        print("Install with:  brew install ffmpeg", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
