#!/usr/bin/env bash
# heygen-validate-prompt.sh — Structural validator for Video Agent prompts
# Usage: echo "$prompt" | ./heygen-validate-prompt.sh
#    or: ./heygen-validate-prompt.sh prompt.txt
# Returns JSON with pass/fail, score, and list of issues.

set -euo pipefail

# Read prompt from file arg or stdin
if [[ $# -ge 1 && -f "$1" ]]; then
  PROMPT="$(cat "$1")"
else
  PROMPT="$(cat)"
fi

if [[ -z "$PROMPT" ]]; then
  echo '{"pass":false,"score":0,"max_score":7,"issues":[{"level":"FAIL","check":"empty_prompt","message":"Prompt is empty. Nothing to validate."}]}'
  exit 0
fi

ISSUES=()
SCORE=0
MAX_SCORE=7

# --- Check 1: Scene structure (FAIL) ---
if echo "$PROMPT" | grep -qiE '(scene\s*[0-9]+[:\s]|scene\s*[0-9]+\s*[-–—]|##?\s*scene)'; then
  SCORE=$((SCORE + 1))
else
  ISSUES+=("{\"level\":\"FAIL\",\"check\":\"scene_structure\",\"message\":\"Prompt is a flat paragraph. Must use Scene 1/Scene 2 structure with Visual + VO + Duration per scene.\"}")
fi

# --- Check 2: Visual style block (WARN) ---
STYLE_PATTERN='(minimalistic|clean visuals|clean styled|brand colors|hex\s*#[0-9a-fA-F]{3,6}|#[0-9a-fA-F]{6}|color palette|visual style|flat design|gradient|cinematic|bold.*vibrant|retro|cartoon)'
if echo "$PROMPT" | grep -qiE "$STYLE_PATTERN"; then
  SCORE=$((SCORE + 1))
else
  ISSUES+=("{\"level\":\"WARN\",\"check\":\"style_block\",\"message\":\"No visual style block found. Add color/style directives (e.g. minimalistic, brand colors, hex codes).\"}")
fi

# --- Check 3: Media type directions (WARN) ---
MEDIA_PATTERN='(motion graphics|stock media|stock footage|ai generated|ai video|ai image|b-roll|a-roll)'
if echo "$PROMPT" | grep -qiE "$MEDIA_PATTERN"; then
  SCORE=$((SCORE + 1))
else
  ISSUES+=("{\"level\":\"WARN\",\"check\":\"media_types\",\"message\":\"No media type directions found. Specify Motion Graphics, Stock Media, or AI Generated per scene.\"}")
fi

# --- Check 4: Duration per scene (WARN) ---
DURATION_PATTERN='(duration:\s*[0-9]|[0-9]+\s*seconds?|[0-9]+s\b|~[0-9]+s)'
if echo "$PROMPT" | grep -qiE "$DURATION_PATTERN"; then
  SCORE=$((SCORE + 1))
else
  ISSUES+=("{\"level\":\"WARN\",\"check\":\"scene_duration\",\"message\":\"No per-scene duration found. Add Duration: Xs to each scene for precise timing control.\"}")
fi

# --- Check 5: Word count / pacing check (WARN) ---
# Extract VO/script text: lines starting with VO:, quote-wrapped lines, or lines after "VO:"
VO_TEXT=""
# Try extracting VO lines
VO_LINES="$(echo "$PROMPT" | grep -iE '^\s*(vo|voiceover|script|narrator)\s*:' | sed 's/^[^:]*://' || true)"
if [[ -n "$VO_LINES" ]]; then
  VO_TEXT="$VO_LINES"
else
  # Fall back to quoted text (lines wrapped in double quotes)
  VO_TEXT="$(echo "$PROMPT" | grep -oE '"[^"]{10,}"' | tr -d '"' || true)"
fi

if [[ -n "$VO_TEXT" ]]; then
  WORD_COUNT=$(echo "$VO_TEXT" | wc -w | tr -d ' ')
  # Extract target duration from prompt — prefer total/overall duration signals
  TARGET_DURATION=""
  # First: look for "This is a X-second video" or "X-second video" (total duration)
  TARGET_DURATION="$(echo "$PROMPT" | grep -oiE '(this is a\s+)?[0-9]+-second video' | head -1 | grep -oE '[0-9]+' || true)"
  if [[ -z "$TARGET_DURATION" ]]; then
    # Try "total duration: 60s" or "total: 60 seconds"
    TARGET_DURATION="$(echo "$PROMPT" | grep -oiE 'total\s*(duration)?[:\s]*~?[0-9]+' | head -1 | grep -oE '[0-9]+' || true)"
  fi
  if [[ -z "$TARGET_DURATION" ]]; then
    # Sum all scene durations: lines like "Duration: 5 seconds" or "Duration: 5s"
    SCENE_DURATIONS="$(echo "$PROMPT" | grep -oiE 'duration[:\s]*~?[0-9]+' | grep -oE '[0-9]+' || true)"
    if [[ -n "$SCENE_DURATIONS" ]]; then
      TARGET_DURATION=0
      while IFS= read -r d; do
        TARGET_DURATION=$((TARGET_DURATION + d))
      done <<< "$SCENE_DURATIONS"
    fi
  fi

  if [[ -n "$TARGET_DURATION" && "$TARGET_DURATION" -gt 0 ]]; then
    # 150 words per minute = 2.5 words per second
    MAX_WORDS=$(echo "$TARGET_DURATION * 2.5" | bc | cut -d. -f1 2>/dev/null || echo "0")
    if [[ "$MAX_WORDS" -gt 0 && "$WORD_COUNT" -gt "$MAX_WORDS" ]]; then
      OVER=$((WORD_COUNT - MAX_WORDS))
      ISSUES+=("{\"level\":\"WARN\",\"check\":\"word_count\",\"message\":\"VO is ~${WORD_COUNT} words for a ${TARGET_DURATION}s video (max ~${MAX_WORDS} at 150 wpm). Over by ~${OVER} words. Trim for natural pacing.\"}")
    else
      SCORE=$((SCORE + 1))
    fi
  else
    # No target duration to compare against, pass by default
    SCORE=$((SCORE + 1))
  fi
else
  # No VO text extracted, can't check — pass with info
  SCORE=$((SCORE + 1))
fi

# --- Check 6: Unwanted default negative constraints (WARN) ---
HAS_UNWANTED=false
UNWANTED_ITEMS=()
if echo "$PROMPT" | grep -qi 'no text-on-screen overlays\|no text on screen'; then
  HAS_UNWANTED=true
  UNWANTED_ITEMS+=("no text-on-screen overlays")
fi
if echo "$PROMPT" | grep -qi 'no stock footage transitions\|no stock transitions'; then
  HAS_UNWANTED=true
  UNWANTED_ITEMS+=("no stock footage transitions")
fi

if [[ "$HAS_UNWANTED" == true ]]; then
  UNWANTED_LIST=""
  for item in "${UNWANTED_ITEMS[@]}"; do
    if [[ -n "$UNWANTED_LIST" ]]; then
      UNWANTED_LIST="${UNWANTED_LIST}, ${item}"
    else
      UNWANTED_LIST="$item"
    fi
  done
  ISSUES+=("{\"level\":\"WARN\",\"check\":\"negative_constraints\",\"message\":\"Default negative constraints found (${UNWANTED_LIST}). These reduce visual variety. Remove unless user explicitly requested a minimal/clean look.\"}")
else
  SCORE=$((SCORE + 1))
fi

# --- Check 7: Opening hook (INFO) ---
# Check if first scene has duration under 10 seconds
FIRST_SCENE_DURATION="$(echo "$PROMPT" | grep -iA5 -m1 'scene\s*1' | grep -oiE '(duration[:\s]*~?[0-9]+|[0-9]+\s*seconds?|[0-9]+s\b)' | head -1 | grep -oE '[0-9]+' || true)"
if [[ -n "$FIRST_SCENE_DURATION" ]]; then
  if [[ "$FIRST_SCENE_DURATION" -le 10 ]]; then
    SCORE=$((SCORE + 1))
  else
    ISSUES+=("{\"level\":\"INFO\",\"check\":\"opening_hook\",\"message\":\"Scene 1 is ${FIRST_SCENE_DURATION}s. Opening hooks work best under 10 seconds. Front-load the most compelling statement.\"}")
  fi
else
  # Can't determine, give benefit of the doubt
  SCORE=$((SCORE + 1))
fi

# --- Determine pass/fail ---
PASS=true
for issue in "${ISSUES[@]+"${ISSUES[@]}"}"; do
  if echo "$issue" | grep -q '"FAIL"'; then
    PASS=false
    break
  fi
done

# --- Build JSON output ---
ISSUES_JSON="["
FIRST=true
for issue in "${ISSUES[@]+"${ISSUES[@]}"}"; do
  if [[ "$FIRST" == true ]]; then
    ISSUES_JSON="${ISSUES_JSON}${issue}"
    FIRST=false
  else
    ISSUES_JSON="${ISSUES_JSON},${issue}"
  fi
done
ISSUES_JSON="${ISSUES_JSON}]"

cat <<EOF
{"pass":${PASS},"score":${SCORE},"max_score":${MAX_SCORE},"issues":${ISSUES_JSON}}
EOF
