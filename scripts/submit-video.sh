#!/usr/bin/env bash
# submit-video.sh — HeyGen Video Agent submission wrapper
# NEVER call POST /v3/video-agents directly. Always use this script.
#
# This script enforces Phase 3.5 (aspect ratio correction) automatically.
# It checks avatar dimensions, detects orientation mismatches, and appends
# the correct FRAMING NOTE to the prompt before submission.
#
# Usage:
#   ./scripts/submit-video.sh <payload.json>
#
# The payload.json must contain at minimum:
#   { "prompt": "...", "orientation": "landscape"|"portrait" }
#
# Optional fields (passed through to API):
#   avatar_id, voice_id, style_id, files, callback_url, callback_id, incognito_mode
#
# What this script does:
#   1. If avatar_id is set, fetches look metadata (dimensions, type)
#   2. Detects orientation mismatch (including square avatars)
#   3. Appends the correct FRAMING NOTE to the prompt
#   4. Submits to POST /v3/video-agents
#   5. Outputs JSON: {"video_id":"...","session_id":"...","framing_applied":"none|..."}
#
# Exit codes:
#   0 = success (video submitted)
#   1 = usage error / missing deps
#   2 = API key missing
#   3 = avatar lookup failed
#   4 = API submission failed

set -euo pipefail

if [ -z "${HEYGEN_API_KEY:-}" ]; then
  echo '{"error":"HEYGEN_API_KEY not set"}' >&2
  exit 2
fi

if [ $# -lt 1 ] || [ ! -f "$1" ]; then
  cat >&2 <<'USAGE'
Usage: submit-video.sh <payload.json>

payload.json must contain at minimum:
  { "prompt": "...", "orientation": "landscape" }

Optional: avatar_id, voice_id, style_id, files, callback_url, callback_id, incognito_mode
USAGE
  exit 1
fi

export PAYLOAD_FILE="$1"
export BASE_URL="https://api.heygen.com"

# All logic in Python for safe JSON handling
python3 << 'PYEOF'
import json, os, sys, urllib.request, urllib.error

payload_file = os.environ["PAYLOAD_FILE"]
base_url = os.environ["BASE_URL"]
api_key = os.environ["HEYGEN_API_KEY"]

with open(payload_file) as f:
    payload = json.load(f)

prompt = payload.get("prompt", "")
if not prompt:
    print(json.dumps({"error": "prompt is empty in payload"}), file=sys.stderr)
    sys.exit(1)

avatar_id = payload.get("avatar_id", "")
orientation = payload.get("orientation", "landscape")
framing_applied = "none"

# --- Phase 3.5: Aspect ratio check ---
if avatar_id:
    print(f"Checking avatar {avatar_id}...", file=sys.stderr)

    try:
        req = urllib.request.Request(
            f"{base_url}/v3/avatars/looks/{avatar_id}",
            headers={"X-Api-Key": api_key}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            look = json.loads(resp.read()).get("data", {})
    except Exception as e:
        print(f"Warning: Could not fetch avatar look: {e}. Proceeding without frame check.", file=sys.stderr)
        look = None

    if look:
        w = look.get("image_width", 0)
        h = look.get("image_height", 0)
        avatar_type = look.get("avatar_type", "unknown")
        name = look.get("name", "unknown")

        if w == 0 and h == 0:
            av_orient = "unknown"
        elif w == h:
            av_orient = "square"
        elif w > h:
            av_orient = "landscape"
        else:
            av_orient = "portrait"

        print(f"  Name: {name}", file=sys.stderr)
        print(f"  Dimensions: {w}x{h} ({av_orient})", file=sys.stderr)
        print(f"  Type: {avatar_type}", file=sys.stderr)
        print(f"  Target: {orientation}", file=sys.stderr)

        # Default fill directive (photorealistic — safest)
        fill = (
            "HYPER PHOTO-REALISTIC environment. Real photography: actual office spaces, "
            "real studios, genuine room interiors with natural imperfections. "
            "NOT CGI. NOT stock photo. NOT 3D-rendered."
        )

        needs_framing = False
        framing_note = ""

        if av_orient == "square" and orientation == "landscape":
            needs_framing = True
            framing_applied = "square_to_landscape"
            framing_note = f"""

FRAMING NOTE: The selected avatar image is SQUARE (1:1) but this video is landscape (16:9). HeyGen does not support square video output — without correction, the video will have black bars on both sides. YOU MUST generate a new variant of the avatar image before using it. Use AI Image tool to:
1. Generate a landscape (16:9) version of the presenter image
2. Generative fill to extend the scene horizontally — add a {fill} Extend on both sides with environment consistent with the avatar's visual style.
3. Frame the presenter centered in the landscape canvas
4. The background MUST visually match the avatar's own style and rendering. Correct lighting direction, natural shadows, consistent art style throughout. NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original square image uncropped. Do NOT add black bars or pillarboxing. Do NOT leave a transparent or missing background."""

        elif av_orient == "square" and orientation == "portrait":
            needs_framing = True
            framing_applied = "square_to_portrait"
            framing_note = f"""

FRAMING NOTE: The selected avatar image is SQUARE (1:1) but this video is portrait (9:16). HeyGen does not support square video output — without correction, the video will have black bars on top and bottom. YOU MUST generate a new variant of the presenter image before using it. Use AI Image tool to:
1. Generate a portrait (9:16) version of the presenter image
2. Generative fill to extend vertically — add {fill} Extend above and below the presenter with environment consistent with their style.
3. Frame the presenter centered in the portrait canvas
4. The background MUST visually match the avatar's own style and rendering. Correct lighting, natural shadows, consistent art style throughout. NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original square image uncropped. Do NOT add letterboxing. Do NOT leave transparent or missing background areas."""

        elif av_orient == "portrait" and orientation == "landscape":
            needs_framing = True
            framing_applied = "portrait_to_landscape"
            framing_note = f"""

FRAMING NOTE: The selected avatar image is in portrait orientation (9:16) but this video is landscape (16:9). YOU MUST generate a new variant of the avatar image before using it. Use AI Image tool to:
1. Generate a landscape (16:9) version of the presenter image
2. Generative fill to extend the scene horizontally — add a {fill}
3. Frame the presenter from chest up, centered in the landscape canvas
4. The background MUST visually match the avatar's own style and rendering. Correct lighting direction, natural shadows, consistent art style throughout. NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original portrait image uncropped. Do NOT add black bars or pillarboxing. Do NOT leave a transparent or missing background."""

        elif av_orient == "landscape" and orientation == "portrait":
            needs_framing = True
            framing_applied = "landscape_to_portrait"
            framing_note = f"""

FRAMING NOTE: The selected avatar image is in landscape orientation (16:9) but this video is portrait (9:16). YOU MUST generate a new variant of the presenter image before using it. Use AI Image tool to:
1. Generate a portrait (9:16) version of the presenter image
2. Generative fill to extend vertically — add {fill} Extend above and below the presenter with environment consistent with their style.
3. Focus on head and shoulders, presenter centered in portrait frame
4. The background MUST visually match the avatar's own style and rendering. Correct lighting, natural shadows, consistent art style throughout. NOT a solid color, NOT transparent, NOT a gradient.
Do NOT use the original landscape image uncropped. Do NOT add letterboxing. Do NOT leave transparent or missing background areas."""

        if needs_framing:
            print(f"  ⚠️  MISMATCH: {av_orient} avatar → {orientation} video", file=sys.stderr)
            print(f"  Appending FRAMING NOTE ({len(framing_note)} chars)", file=sys.stderr)
            payload["prompt"] = prompt + framing_note
        else:
            print(f"  ✅ Orientation match — no correction needed", file=sys.stderr)

# --- Submit to API ---
print("Submitting to Video Agent API...", file=sys.stderr)

req = urllib.request.Request(
    f"{base_url}/v3/video-agents",
    data=json.dumps(payload).encode(),
    headers={
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        data = result.get("data", {})
        video_id = data.get("video_id", "")
        session_id = data.get("session_id", "")

        output = {
            "video_id": video_id,
            "session_id": session_id,
            "framing_applied": framing_applied,
            "avatar_id": avatar_id,
            "orientation": orientation,
            "dashboard_url": f"https://app.heygen.com/videos/{video_id}" if video_id else "",
            "session_url": f"https://app.heygen.com/video-agent/{session_id}" if session_id else ""
        }
        print(json.dumps(output))
        print(f"✅ Submitted: video_id={video_id}, framing={framing_applied}", file=sys.stderr)
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(json.dumps({"error": f"HTTP {e.code}", "detail": body, "framing_applied": framing_applied}))
    sys.exit(4)
except Exception as e:
    print(json.dumps({"error": str(e), "framing_applied": framing_applied}))
    sys.exit(4)
PYEOF
