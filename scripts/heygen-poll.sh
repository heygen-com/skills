#!/usr/bin/env bash
set -euo pipefail

# heygen-poll.sh — Poll HeyGen video status until completion or timeout.
# Usage: heygen-poll.sh <video_id> [--timeout <seconds>] [--interval <seconds>]
# Output: JSON status on each poll. Final output includes video_url on success.

API_BASE="https://api.heygen.com"

VIDEO_ID=""
TIMEOUT=600       # 10 minutes default
INTERVAL=30       # 30 seconds between polls

while [ $# -gt 0 ]; do
  case "$1" in
    --timeout)  TIMEOUT="$2"; shift 2 ;;
    --interval) INTERVAL="$2"; shift 2 ;;
    --help|-h)
      echo "Usage: heygen-poll.sh <video_id> [--timeout <sec>] [--interval <sec>]"
      exit 0 ;;
    -*)
      echo "{\"error\": \"Unknown option: $1\"}"; exit 1 ;;
    *)
      VIDEO_ID="$1"; shift ;;
  esac
done

if [ -z "$VIDEO_ID" ]; then
  echo '{"error": "No video_id provided."}'
  exit 1
fi

# Auth
if [ -z "${HEYGEN_API_KEY:-}" ] && [ -f "$HOME/.heygen/config" ]; then
  # shellcheck source=/dev/null
  source "$HOME/.heygen/config"
fi
if [ -z "${HEYGEN_API_KEY:-}" ]; then
  echo '{"error": "HEYGEN_API_KEY not set."}'
  exit 1
fi

ELAPSED=0
POLL_COUNT=0

while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  RESPONSE=$(curl -s -w "\n%{http_code}" \
    -X GET "$API_BASE/v1/video_status.get?video_id=$VIDEO_ID" \
    -H "X-Api-Key: $HEYGEN_API_KEY")

  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | sed '$d')

  if [ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ]; then
    echo "{\"poll\": true, \"elapsed\": $ELAPSED, \"error\": \"HTTP $HTTP_CODE\", \"retrying\": true}"
    sleep "$INTERVAL"
    ELAPSED=$((ELAPSED + INTERVAL))
    continue
  fi

  STATUS=$(echo "$BODY" | jq -r '.data.status // "unknown"' 2>/dev/null || echo "unknown")
  POLL_COUNT=$((POLL_COUNT + 1))

  case "$STATUS" in
    completed)
      VIDEO_URL=$(echo "$BODY" | jq -r '.data.video_url // empty' 2>/dev/null || echo "")
      THUMBNAIL=$(echo "$BODY" | jq -r '.data.thumbnail_url // empty' 2>/dev/null || echo "")
      DURATION=$(echo "$BODY" | jq -r '.data.duration // empty' 2>/dev/null || echo "")
      GIF_URL=$(echo "$BODY" | jq -r '.data.gif_url // empty' 2>/dev/null || echo "")
      echo "{\"success\": true, \"status\": \"completed\", \"video_id\": \"$VIDEO_ID\", \"video_url\": \"$VIDEO_URL\", \"thumbnail_url\": \"$THUMBNAIL\", \"gif_url\": \"$GIF_URL\", \"duration\": $DURATION, \"elapsed_seconds\": $ELAPSED, \"polls\": $POLL_COUNT}"
      exit 0
      ;;
    failed)
      ERROR=$(echo "$BODY" | jq -r '.data.error // "Unknown failure"' 2>/dev/null || echo "Unknown failure")
      echo "{\"success\": false, \"status\": \"failed\", \"video_id\": \"$VIDEO_ID\", \"error\": $(printf '%s' "$ERROR" | jq -Rs .), \"elapsed_seconds\": $ELAPSED}"
      exit 1
      ;;
    waiting|pending|processing)
      echo "{\"poll\": true, \"status\": \"$STATUS\", \"video_id\": \"$VIDEO_ID\", \"elapsed\": $ELAPSED, \"polls\": $POLL_COUNT}"
      ;;
    *)
      echo "{\"poll\": true, \"status\": \"$STATUS\", \"video_id\": \"$VIDEO_ID\", \"elapsed\": $ELAPSED, \"note\": \"unexpected status\"}"
      ;;
  esac

  sleep "$INTERVAL"
  ELAPSED=$((ELAPSED + INTERVAL))
done

# Timeout
echo "{\"success\": false, \"status\": \"timeout\", \"video_id\": \"$VIDEO_ID\", \"elapsed_seconds\": $ELAPSED, \"message\": \"Polling timed out after ${TIMEOUT}s. Check manually.\"}"
exit 1
