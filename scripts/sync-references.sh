#!/usr/bin/env bash
# sync-references.sh — propagate canonical root references/ into per-skill copies.
#
# Source of truth: references/ at the repo root.
# Destinations:    heygen-avatar/references/ and heygen-video/references/.
#
# Each skill bundles only the references it actually links to. This script
# enforces that mapping and copies the canonical root file into each
# destination. It does NOT touch:
#
#   - heygen-avatar/references/avatar-creation.md
#       (per-skill creator-side cleave, no root counterpart)
#   - heygen-video/references/avatar-discovery.md
#       (per-skill consumer-side cleave from the original avatar-discovery.md;
#        the cleave is intentional and the two halves diverge by design)
#
# Usage:
#   ./scripts/sync-references.sh           # propagate root → subdirs
#   ./scripts/sync-references.sh --check   # exit 1 if any subdir copy drifts from root
#
# CI gate: validate-skills.yml runs this with --check on every PR.

set -euo pipefail

# Resolve repo root regardless of where the script is invoked from.
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Format: <subdir-copy>|<canonical-root-source>
PAIRS=(
  'heygen-avatar/references/asset-routing.md|references/asset-routing.md'
  'heygen-avatar/references/troubleshooting.md|references/troubleshooting.md'
  'heygen-video/references/asset-routing.md|references/asset-routing.md'
  'heygen-video/references/frame-check.md|references/frame-check.md'
  'heygen-video/references/motion-vocabulary.md|references/motion-vocabulary.md'
  'heygen-video/references/official-prompt-guide.md|references/official-prompt-guide.md'
  'heygen-video/references/prompt-craft.md|references/prompt-craft.md'
  'heygen-video/references/prompt-styles.md|references/prompt-styles.md'
  'heygen-video/references/troubleshooting.md|references/troubleshooting.md'
)

mode="sync"
case "${1:-}" in
  --check) mode="check" ;;
  -h|--help)
    sed -n '1,28p' "$0"
    exit 0
    ;;
  "") ;;
  *)
    echo "unknown argument: $1" >&2
    echo "usage: $0 [--check]" >&2
    exit 2
    ;;
esac

fail=0
synced=0

for pair in "${PAIRS[@]}"; do
  sub="${pair%%|*}"
  root="${pair##*|}"

  if [ ! -f "$root" ]; then
    echo "::error::canonical source missing: $root"
    fail=1
    continue
  fi

  if [ "$mode" = "check" ]; then
    if [ ! -f "$sub" ]; then
      echo "::error::subdir copy missing: $sub (run scripts/sync-references.sh to create it)"
      fail=1
    elif ! diff -q "$root" "$sub" >/dev/null 2>&1; then
      echo "::error::drift detected — '$sub' differs from canonical '$root'"
      diff -u "$root" "$sub" | head -40 || true
      fail=1
    fi
  else
    mkdir -p "$(dirname "$sub")"
    if [ -f "$sub" ] && diff -q "$root" "$sub" >/dev/null 2>&1; then
      :
    else
      cp "$root" "$sub"
      echo "synced: $root → $sub"
      synced=$((synced + 1))
    fi
  fi
done

if [ "$mode" = "check" ]; then
  if [ "$fail" -ne 0 ]; then
    echo ""
    echo "Drift detected. Run: ./scripts/sync-references.sh"
    exit 1
  fi
  echo "✓ All ${#PAIRS[@]} shared references are in sync with canonical root copies."
else
  if [ "$synced" -eq 0 ]; then
    echo "✓ All ${#PAIRS[@]} shared references already in sync — no changes."
  else
    echo ""
    echo "Synced $synced file(s). Review and commit:"
    echo "  git add heygen-avatar/references heygen-video/references"
    echo "  git commit"
  fi
fi
