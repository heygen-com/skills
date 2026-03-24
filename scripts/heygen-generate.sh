#!/usr/bin/env bash
set -euo pipefail

# heygen-generate.sh — Submit a prompt to HeyGen Video Agent.
# Usage: heygen-generate.sh <prompt> [--duration <seconds>] [--orientation landscape|portrait] [--avatar <id>]
# Output: JSON with video_id on success, error details on failure.

API_BASE="https://api.heygen.com"

PROMPT=""
DURATION=""
ORIENTATION=""
AVATAR_ID=""

while [ $# -gt 0 ]; do
  case "$1" in
    --duration)    DURATION="$2"; shift 2 ;;
    --orientation) ORIENTATION="$2"; shift 2 ;;
    --avatar)      AVATAR_ID="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: heygen-generate.sh <prompt> [--duration <sec>] [--orientation landscape|portrait] [--avatar <id>]"
      exit 0 ;;
    -*)
      echo "{\"error\": \"Unknown option: $1\"}"; exit 1 ;;
    *)
      if [ -z "$PROMPT" ]; then PROMPT="$1"; else PROMPT="$PROMPT $1"; fi
      shift ;;
  esac
done

if [ -z "$PROMPT" ]; then
  echo '{"error": "No prompt provided."}'
  exit 1
fi

# Auth: prefer env var, fall back to config file
if [ -z "${HEYGEN_API_KEY:-}" ] && [ -f "$HOME/.heygen/config" ]; then
  # shellcheck source=/dev/null
  source "$HOME/.heygen/config"
fi
if [ -z "${HEYGEN_API_KEY:-}" ]; then
  echo '{"error": "HEYGEN_API_KEY not set. Set it as an env var or in ~/.heygen/config."}'
  exit 1
fi

# Build JSON body
BODY="{\"prompt\": $(printf '%s' "$PROMPT" | jq -Rs .)}"

# Build config object if any options provided
CONFIG_PARTS=""
[ -n "$DURATION" ]    && CONFIG_PARTS="${CONFIG_PARTS}\"duration_sec\": $DURATION,"
[ -n "$ORIENTATION" ] && CONFIG_PARTS="${CONFIG_PARTS}\"orientation\": $(printf '%s' "$ORIENTATION" | jq -Rs .),"
[ -n "$AVATAR_ID" ]   && CONFIG_PARTS="${CONFIG_PARTS}\"avatar_id\": $(printf '%s' "$AVATAR_ID" | jq -Rs .),"

if [ -n "$CONFIG_PARTS" ]; then
  CONFIG_PARTS="${CONFIG_PARTS%,}"
  BODY="{\"prompt\": $(printf '%s' "$PROMPT" | jq -Rs .), \"config\": {$CONFIG_PARTS}}"
fi

# API call
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "$API_BASE/v1/video_agent/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BODY")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY_RESPONSE=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  VIDEO_ID=$(echo "$BODY_RESPONSE" | jq -r '.data.video_id // empty' 2>/dev/null || echo "")
  SESSION_ID=$(echo "$BODY_RESPONSE" | jq -r '.data.session_id // empty' 2>/dev/null || echo "")
  if [ -n "$VIDEO_ID" ]; then
    echo "{\"success\": true, \"video_id\": \"$VIDEO_ID\", \"session_id\": \"$SESSION_ID\", \"session_url\": \"https://app.heygen.com/video-agent/$SESSION_ID\", \"video_url\": \"https://app.heygen.com/videos/$VIDEO_ID\", \"status\": \"submitted\"}"
  else
    echo "$BODY_RESPONSE"
  fi
else
  ERROR_MSG=$(echo "$BODY_RESPONSE" | jq -r '.error // .message // "Unknown error"' 2>/dev/null || echo "Request failed")
  echo "{\"error\": true, \"http_code\": $HTTP_CODE, \"message\": $(printf '%s' "$ERROR_MSG" | jq -Rs .)}"
  exit 1
fi
