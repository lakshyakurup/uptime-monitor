#!/usr/bin/env python3
"""Write a notification summary to a local text file."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def write_notification(output_file: Path, title: str, summary: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {title}\n")
        file.write(f"{summary}\n\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write notification summary to a text file.")
    parser.add_argument("title", help="Notification title")
    parser.add_argument("summary", help="Notification summary text")
    parser.add_argument(
        "--output",
        default="notifications.txt",
        help="Output text file path (default: notifications.txt)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    output_file = Path(args.output).expanduser().resolve()
    write_notification(output_file, args.title.strip(), args.summary.strip())

    print(f"Notification written to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
