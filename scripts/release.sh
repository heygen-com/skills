#!/usr/bin/env bash
set -euo pipefail

# Release script for heygen-stack
# Usage: ./scripts/release.sh [patch|minor|major]
# Default: patch
#
# What it does:
#   1. Bumps VERSION file
#   2. Commits + tags
#   3. Pushes to GitHub
#   4. Publishes to ClawHub as "heygen-stack"

BUMP_TYPE="${1:-patch}"
CURRENT=$(cat VERSION)
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"

case "$BUMP_TYPE" in
  patch) PATCH=$((PATCH + 1)) ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
  *) echo "Usage: $0 [patch|minor|major]"; exit 1 ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
TAG="v$NEW_VERSION"

echo "Bumping $CURRENT → $NEW_VERSION"

# Update VERSION file
echo "$NEW_VERSION" > VERSION

# Commit and tag
git add VERSION
git commit -m "release: v$NEW_VERSION"
git tag -a "$TAG" -m "Release $TAG"

# Push
echo "Pushing to GitHub..."
git push origin main --follow-tags

# Publish to ClawHub
echo "Publishing to ClawHub..."
clawhub publish . \
  --slug "heygen-stack" \
  --name "HeyGen Stack" \
  --version "$NEW_VERSION" \
  --changelog "Release v$NEW_VERSION" \
  --tags "latest"

echo ""
echo "✅ v$NEW_VERSION released"
echo "   GitHub: pushed + tagged"
echo "   ClawHub: published as heygen-stack"
