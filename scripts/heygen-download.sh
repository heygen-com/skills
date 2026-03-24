#!/usr/bin/env bash
set -euo pipefail

# heygen-download.sh — Download a completed HeyGen video.
# Usage: heygen-download.sh <video_url> [output_path]
# Default output: /tmp/openclaw/uploads/heygen-<timestamp>.mp4

VIDEO_URL=""
OUTPUT_PATH=""

while [ $# -gt 0 ]; do
  case "$1" in
    --help|-h)
      echo "Usage: heygen-download.sh <video_url> [output_path]"
      exit 0 ;;
    -*)
      echo "{\"error\": \"Unknown option: $1\"}"; exit 1 ;;
    *)
      if [ -z "$VIDEO_URL" ]; then VIDEO_URL="$1"
      elif [ -z "$OUTPUT_PATH" ]; then OUTPUT_PATH="$1"
      fi
      shift ;;
  esac
done

if [ -z "$VIDEO_URL" ]; then
  echo '{"error": "No video URL provided."}'
  exit 1
fi

if [ -z "$OUTPUT_PATH" ]; then
  mkdir -p /tmp/openclaw/uploads
  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
  OUTPUT_PATH="/tmp/openclaw/uploads/heygen-${TIMESTAMP}.mp4"
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"

HTTP_CODE=$(curl -s -w "%{http_code}" -L -o "$OUTPUT_PATH" "$VIDEO_URL")

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  FILE_SIZE=$(wc -c < "$OUTPUT_PATH" | tr -d ' ')
  FILE_SIZE_MB=$(echo "scale=1; $FILE_SIZE / 1048576" | bc 2>/dev/null || echo "?")
  echo "{\"success\": true, \"path\": \"$OUTPUT_PATH\", \"size_bytes\": $FILE_SIZE, \"size_mb\": \"${FILE_SIZE_MB}MB\"}"
else
  rm -f "$OUTPUT_PATH"
  echo "{\"error\": true, \"http_code\": $HTTP_CODE, \"message\": \"Download failed\"}"
  exit 1
fi
