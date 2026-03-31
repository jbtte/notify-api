#!/usr/bin/env bash
# Usage: ./notify.sh "my-project" "Deploy finished" "✅"
set -euo pipefail

NOTIFY_URL="${NOTIFY_URL:-http://localhost:8000}"
NOTIFY_TOKEN="${NOTIFY_TOKEN:-change-me-to-a-strong-secret}"

PROJECT="${1:?Usage: $0 <project> <message> [emoji]}"
MESSAGE="${2:?Usage: $0 <project> <message> [emoji]}"
EMOJI="${3:-🔔}"

curl -sf -X POST "$NOTIFY_URL/send" \
  -H "Authorization: Bearer $NOTIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"project\":\"$PROJECT\",\"message\":\"$MESSAGE\",\"emoji\":\"$EMOJI\"}"
