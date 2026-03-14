#!/usr/bin/env python3
"""Dependency verification for the video-understand skill.

Checks that all required and optional dependencies are installed and
reports their versions. Exits with code 0 if all required dependencies
are met, or 1 if any are missing.
"""

import importlib
import shutil
import subprocess
import sys


def check_command(name, version_flag="--version"):
    """Check if a system command is available and return its version string."""
    path = shutil.which(name)
    if path is None:
        return None, None
    try:
        result = subprocess.run(
            [name, version_flag],
            capture_output=True,
            text=True,
            timeout=10,
        )
        version = (result.stdout.strip() or result.stderr.strip()).split("\n")[0]
        return path, version
    except (subprocess.TimeoutExpired, OSError):
        return path, "unknown"


def check_python_package(name, import_name=None):
    """Check if a Python package is importable and return its version."""
    import_name = import_name or name
    try:
        mod = importlib.import_module(import_name)
        version = getattr(mod, "__version__", None)
        if version is None:
            try:
                from importlib.metadata import version as pkg_version
                version = pkg_version(name)
            except Exception:
                version = "installed"
        return True, version
    except ImportError:
        return False, None


def main():
    ok = True
    results = []

    # Required system commands
    for cmd in ("ffmpeg", "ffprobe"):
        path, version = check_command(cmd)
        if path:
            results.append(("OK", cmd, version))
        else:
            results.append(("MISSING", cmd, "not found -- install FFmpeg"))
            ok = False

    # Optional Python packages (recommended)
    for pkg, imp in [("openai-whisper", "whisper")]:
        found, version = check_python_package(pkg, imp)
        if found:
            results.append(("OK", f"{pkg} (recommended)", version))
        else:
            results.append(("OPTIONAL", f"{pkg} (recommended)", f"not found -- pip install {pkg}"))

    # Check whisper CLI fallback
    whisper_cli_path, whisper_cli_version = check_command("whisper", "--help")
    if whisper_cli_path:
        results.append(("OK", "whisper CLI (fallback)", whisper_cli_path))
    else:
        results.append(("OPTIONAL", "whisper CLI (fallback)", "not found"))

    # Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 8):
        results.append(("OK", "Python", py_version))
    else:
        results.append(("MISSING", "Python >= 3.8", f"found {py_version}"))
        ok = False

    # Print results
    print("video-understand dependency check")
    print("=" * 55)
    for status, name, detail in results:
        icon = "[OK]" if status == "OK" else "[!!]" if status == "MISSING" else "[--]"
        print(f"  {icon} {name}: {detail}")
    print("=" * 55)

    if ok:
        print("All required dependencies are installed.")
        # Check if whisper is available at all
        whisper_found, _ = check_python_package("openai-whisper", "whisper")
        if not whisper_found and not whisper_cli_path:
            print()
            print("Note: Whisper is not installed. Transcription will be skipped.")
            print("To enable transcription, install openai-whisper:")
            print()
            answer = input("Install openai-whisper now? [Y/n] ").strip().lower()
            if answer in ("", "y", "yes"):
                install_whisper()
    else:
        print("Some required dependencies are missing. See above.")
        sys.exit(1)


def install_whisper():
    """Attempt to pip-install openai-whisper."""
    print("\nInstalling: openai-whisper")
    cmd = [sys.executable, "-m", "pip", "install", "openai-whisper"]
    try:
        subprocess.run(cmd, check=True)
        print("\nInstallation complete. Re-run setup to verify:")
        print(f"  python3 {__file__}")
    except subprocess.CalledProcessError:
        print("\nInstallation failed. Try manually:")
        print("  pip install openai-whisper")
        sys.exit(1)


if __name__ == "__main__":
    main()
