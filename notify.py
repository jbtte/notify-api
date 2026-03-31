#!/usr/bin/env python3
"""
Minimal notify-api client.

Usage:
    python notify.py <project> <message> [emoji]

Environment:
    NOTIFY_URL    — base URL of the API  (default: http://localhost:8000)
    NOTIFY_TOKEN  — Bearer token         (default: change-me-to-a-strong-secret)
"""
import os
import sys
import httpx

NOTIFY_URL = os.getenv("NOTIFY_URL", "http://localhost:8000")
NOTIFY_TOKEN = os.getenv("NOTIFY_TOKEN", "change-me-to-a-strong-secret")


def send(project: str, message: str, emoji: str = "🔔") -> None:
    resp = httpx.post(
        f"{NOTIFY_URL}/send",
        headers={"Authorization": f"Bearer {NOTIFY_TOKEN}"},
        json={"project": project, "message": message, "emoji": emoji},
        timeout=10,
    )
    resp.raise_for_status()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    send(
        project=sys.argv[1],
        message=sys.argv[2],
        emoji=sys.argv[3] if len(sys.argv) > 3 else "🔔",
    )
