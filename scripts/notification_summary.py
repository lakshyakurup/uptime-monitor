#!/usr/bin/env python3
"""Write a simple notification summary to a local text file."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a local notification summary text file with a timestamp and message."
    )
    parser.add_argument("--output", default="notification_summary.txt", help="Path to the output text file")
    parser.add_argument("--title", default="System Update", help="Short title for the notification")
    parser.add_argument("--message", default="Automation task completed", help="Main notification message")
    parser.add_argument("--status", default="OK", help="Status label such as OK, WARNING, or ERROR")
    return parser


def write_summary(output: Path, title: str, message: str, status: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    content = "\n".join(
        [
            f"Notification: {title}",
            f"Status: {status}",
            f"Time: {timestamp}",
            f"Message: {message}",
        ]
    )
    output.write_text(content + "\n", encoding="utf-8")
    return output


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    written_path = write_summary(output, args.title, args.message, args.status)
    print(f"Notification summary written to {written_path}")


if __name__ == "__main__":
    main()
